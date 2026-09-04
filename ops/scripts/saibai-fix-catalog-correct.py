#!/usr/bin/env python3
"""Deixa o catálogo ACTIVE Saibai consistente: handle, SKU, SEO, Coração P, drafts."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

# handle → SEO + SKU da variante única
IN_NATURA: Dict[str, Dict[str, str]] = {
    "alcachofra-in-natura-t8": {
        "sku": "SAI-AN-T8",
        "seo_title": "Alcachofra In Natura T8 — Caixa 8 un | Empório Saibai",
        "seo_description": "Caixa T8 com 8 alcachofras in natura, cultivo próprio Saibai em Piedade/SP. Variedade roxa de São Roque, colhida no ponto ideal.",
    },
    "alcachofra-in-natura-t12": {
        "sku": "SAI-AN-T12",
        "seo_title": "Alcachofra In Natura T12 — Caixa 12 un | Empório Saibai",
        "seo_description": "Caixa T12 com 12 alcachofras in natura. Produção própria Empório Saibai, Piedade/SP. Frescas para assar, cozinhar e rechear.",
    },
    "alcachofra-in-natura-t14": {
        "new_handle": "alcachofra-in-natura-t16",
        "sku": "SAI-AN-T16",
        "seo_title": "Alcachofra In Natura T16 — Caixa 16 un | Empório Saibai",
        "seo_description": "Caixa T16 com 16 alcachofras in natura. Cultivo próprio Saibai em Piedade/SP. Ideal para entradas e receitas especiais.",
    },
    "alcachofra-in-natura-t20": {
        "sku": "SAI-AN-T20",
        "seo_title": "Alcachofra In Natura T20 — Caixa 20 un | Empório Saibai",
        "seo_description": "Caixa T20 com 20 alcachofras in natura. Produção própria Empório Saibai, Piedade/SP. Frescor direto da fazenda.",
    },
    "alcachofra-in-natura-p": {
        "sku": "SAI-AN-P",
        "seo_title": "Alcachofra In Natura P — Caixa 13 un | Empório Saibai",
        "seo_description": "Caixa P (Tipo 25) com 13 alcachofras in natura. Cultivo próprio Saibai, Piedade/SP. Apresentação delicada.",
    },
    "alcachofra-in-natura-m": {
        "sku": "SAI-AN-M",
        "seo_title": "Alcachofra In Natura M — Caixa 10 un | Empório Saibai",
        "seo_description": "Caixa M (Tipo 16) com 10 alcachofras in natura. Produção própria Empório Saibai, Piedade/SP.",
    },
    "alcachofra-in-natura-g": {
        "sku": "SAI-AN-G",
        "seo_title": "Alcachofra In Natura G — Caixa 8 un | Empório Saibai",
        "seo_description": "Caixa G (Tipo 12) com 8 alcachofras in natura. Cultivo próprio Saibai, Piedade/SP. Peças especiais.",
    },
    "alcachofra-in-natura-mini": {
        "sku": "SAI-AN-MINI",
        "seo_title": "Alcachofra In Natura Mini AAA — 2,9 kg | Empório Saibai",
        "seo_description": "Caixa Mini AAA com aprox. 2,9 kg de alcachofras in natura. Produção própria Empório Saibai, Piedade/SP.",
    },
}

CORACAO_P_IMAGE = (
    "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/"
    "coracao-01-principal_a9b9f044-ac68-44a3-a8dc-bf4313adbdcf.webp?v=1781031553"
)

DRAFTS_TO_ARCHIVE = [
    "alcachofra-p-saibai-caixa",
    "alcachofra-mini-saibai-caixa",
]


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = [
        "shopify", "store", "execute",
        "-s", STORE,
        "--allow-mutations",
        "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    start = out.find("{")
    if start < 0:
        raise RuntimeError(f"Sem JSON: {out[:400]}")
    data = json.loads(out[start:])
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data


def get_product(handle: str) -> dict:
    data = gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            title
            handle
            status
            variants(first: 10) { nodes { id title sku } }
            media(first: 20) {
              nodes { id ... on MediaImage { image { url } } }
            }
          }
        }
        """,
        {"handle": handle},
    )
    p = data.get("productByHandle")
    if not p:
        raise RuntimeError(f"Não encontrado: {handle}")
    return p


def update_product(product_id: str, fields: dict) -> None:
    data = gql(
        """
        mutation productUpdate($input: ProductInput!) {
          productUpdate(input: $input) {
            product { id handle title status }
            userErrors { field message }
          }
        }
        """,
        {"input": {"id": product_id, **fields}},
    )
    errs = data["productUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)


def update_variant_sku(product_id: str, variant_id: str, sku: str) -> None:
    data = gql(
        """
        mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
          productVariantsBulkUpdate(productId: $productId, variants: $variants) {
            productVariants { id sku }
            userErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "variants": [{"id": variant_id, "inventoryItem": {"sku": sku}}],
        },
    )
    errs = data["productVariantsBulkUpdate"]["userErrors"]
    if errs:
        # fallback older shape
        data = gql(
            """
            mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
              productVariantsBulkUpdate(productId: $productId, variants: $variants) {
                productVariants { id sku }
                userErrors { field message }
              }
            }
            """,
            {"productId": product_id, "variants": [{"id": variant_id, "sku": sku}]},
        )
        errs = data["productVariantsBulkUpdate"]["userErrors"]
        if errs:
            raise RuntimeError(errs)


def create_media(product_id: str, url: str, alt: str) -> str:
    data = gql(
        """
        mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { ... on MediaImage { id image { url } } }
            mediaUserErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "media": [{
                "originalSource": url,
                "alt": alt,
                "mediaContentType": "IMAGE",
            }],
        },
    )
    errs = data["productCreateMedia"]["mediaUserErrors"]
    if errs:
        raise RuntimeError(errs)
    media = data["productCreateMedia"]["media"][0]
    media_id = media["id"]
    for _ in range(10):
        time.sleep(1.2)
        node = gql(
            "query($id: ID!) { node(id: $id) { ... on MediaImage { id image { url } } } }",
            {"id": media_id},
        ).get("node") or {}
        if (node.get("image") or {}).get("url"):
            return media_id
    return media_id


def attach_media_to_variant(product_id: str, variant_id: str, media_id: str) -> None:
    data = gql(
        """
        mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
          productVariantsBulkUpdate(productId: $productId, variants: $variants) {
            productVariants { id image { url } }
            userErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "variants": [{"id": variant_id, "mediaId": media_id}],
        },
    )
    errs = data["productVariantsBulkUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)


def basename(url: str) -> str:
    return url.split("?")[0].rstrip("/").split("/")[-1]


def fix_in_natura(handle: str, cfg: dict, dry: bool) -> dict:
    product = get_product(handle)
    variant = product["variants"]["nodes"][0]
    report = {"handle": handle, "actions": []}
    fields: Dict[str, Any] = {
        "seo": {"title": cfg["seo_title"], "description": cfg["seo_description"]},
    }
    if cfg.get("new_handle") and cfg["new_handle"] != product["handle"]:
        fields["handle"] = cfg["new_handle"]
        report["actions"].append(f"handle→{cfg['new_handle']}")
    report["actions"].append("seo")
    print(f"\n=== {handle} ===")
    print(" ", ", ".join(report["actions"]), f"| sku={cfg['sku']}")
    if dry:
        return report
    update_product(product["id"], fields)
    time.sleep(0.5)
    if (variant.get("sku") or "") != cfg["sku"]:
        update_variant_sku(product["id"], variant["id"], cfg["sku"])
        report["actions"].append(f"sku={cfg['sku']}")
        print("  SKU OK")
    return report


def fix_coracao_p(dry: bool) -> dict:
    product = get_product("conserva-de-alcachofras-coracao")
    variant_p = next(v for v in product["variants"]["nodes"] if "P" in v["title"])
    # já tem mídia coracao-p?
    existing = None
    for m in product["media"]["nodes"]:
        url = ((m.get("image") or {}).get("url")) or ""
        name = basename(url)
        if "180" in name or "coracao-01-principal_a9b9" in name or name.startswith("coracao-p"):
            existing = m["id"]
            break
    print("\n=== conserva-de-alcachofras-coracao (P) ===")
    if dry:
        return {"handle": "conserva-de-alcachofras-coracao", "actions": ["media+variant P"]}
    media_id = existing
    if not media_id:
        media_id = create_media(
            product["id"],
            CORACAO_P_IMAGE,
            "Coração Saibai — Tamanho P · aprox. 180g",
        )
        print("  mídia P criada", media_id)
    attach_media_to_variant(product["id"], variant_p["id"], media_id)
    print("  variante P vinculada")
    return {"handle": "conserva-de-alcachofras-coracao", "actions": ["P image"]}


def archive_drafts(dry: bool) -> List[dict]:
    out = []
    for handle in DRAFTS_TO_ARCHIVE:
        try:
            product = get_product(handle)
        except RuntimeError:
            print(f"\n=== {handle} (já ausente) ===")
            continue
        print(f"\n=== {handle} → ARCHIVED ===")
        if dry:
            out.append({"handle": handle, "actions": ["archive"]})
            continue
        update_product(product["id"], {"status": "ARCHIVED"})
        out.append({"handle": handle, "actions": ["archived"]})
        print("  ARCHIVED")
        time.sleep(0.4)
    return out


def main() -> int:
    dry = "--dry-run" in sys.argv
    reports = []
    for handle, cfg in IN_NATURA.items():
        reports.append(fix_in_natura(handle, cfg, dry))
        time.sleep(0.4)
    reports.append(fix_coracao_p(dry))
    reports.extend(archive_drafts(dry))
    print("\n" + json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
