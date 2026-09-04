#!/usr/bin/env python3
"""Sobe packshots Drive (tamanhos) e associa às variantes P/M/G."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

STORE = "byinbz-0k.myshopify.com"
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "scripts" / "output" / "conservas-drive"
OUT = ROOT / "scripts" / "output" / "conservas-drive-opt"
OUT.mkdir(parents=True, exist_ok=True)

# preview_N.png → produto + variante + alt
MAPPING = [
    {
        "src": "preview_1.png",
        "file": "fundo-inteiro-g-600g.jpg",
        "handle": "conserva-de-alcachofras-fundo-inteiro",
        "size": "Tamanho G",
        "alt": "Fundo Inteiro Saibai — Tamanho G · 600g (packshot Drive)",
    },
    {
        "src": "preview_2.png",
        "file": "fundo-inteiro-m-330g.jpg",
        "handle": "conserva-de-alcachofras-fundo-inteiro",
        "size": "Tamanho M",
        "alt": "Fundo Inteiro Saibai — Tamanho M · 330g (packshot Drive)",
    },
    {
        "src": "preview_3.png",
        "file": "coracao-g-550g.jpg",
        "handle": "conserva-de-alcachofras-coracao",
        "size": "Tamanho G",
        "alt": "Coração Saibai — Tamanho G · 550g (packshot Drive)",
    },
    {
        "src": "preview_4.png",
        "file": "coracao-m-330g.jpg",
        "handle": "conserva-de-alcachofras-coracao",
        "size": "Tamanho M",
        "alt": "Coração Saibai — Tamanho M · 330g (packshot Drive)",
    },
    {
        "src": "preview_5.png",
        "file": "fundo-pedaco-g-550g.jpg",
        "handle": "conserva-de-alcachofras-fundo-pedaco",
        "size": "Tamanho G",
        "alt": "Fundo Pedaço Saibai — Tamanho G · 550g (packshot Drive)",
    },
    {
        "src": "preview_6.png",
        "file": "fundo-pedaco-m-330g.jpg",
        "handle": "conserva-de-alcachofras-fundo-pedaco",
        "size": "Tamanho M",
        "alt": "Fundo Pedaço Saibai — Tamanho M · 330g (packshot Drive)",
    },
]


def run_graphql(query: str, variables=None, mutate: bool = False) -> dict:
    cmd = ["shopify", "store", "execute", "--store", STORE, "--query", query, "-j"]
    if mutate:
        cmd.append("--allow-mutations")
    if variables is not None:
        cmd.extend(["--variables", json.dumps(variables)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    raw = result.stdout
    start = raw.find("{")
    if start < 0:
        raise RuntimeError(raw[:500])
    payload = json.loads(raw[start:])
    if "errors" in payload:
        raise RuntimeError(json.dumps(payload["errors"], ensure_ascii=False))
    return payload.get("data", payload)


def optimize(src: Path, dest: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    scale = min(1.0, 1600 / max(w, h))
    if scale < 1:
        im = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    im.save(dest, "JPEG", quality=90, optimize=True)


def upload_staged(path: Path) -> str:
    mime = "image/jpeg"
    size = path.stat().st_size
    data = run_graphql(
        """
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { message }
          }
        }
        """,
        {
            "input": [{
                "filename": path.name,
                "mimeType": mime,
                "resource": "IMAGE",
                "fileSize": str(size),
                "httpMethod": "POST",
            }]
        },
        mutate=True,
    )
    block = data["stagedUploadsCreate"]
    if block.get("userErrors"):
        raise RuntimeError(block["userErrors"])
    target = block["stagedTargets"][0]
    boundary = "----SaibaiBoundary"
    parts = []
    for p in target["parameters"]:
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode()
        )
    blob = path.read_bytes()
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{path.name}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
        + blob
        + f"\r\n--{boundary}--\r\n".encode()
    )
    tmp = path.with_suffix(".multipart")
    tmp.write_bytes(b"".join(parts))
    try:
        result = subprocess.run(
            [
                "curl", "-sS", "-f", "--max-time", "90",
                "-X", "POST",
                "-H", f"Content-Type: multipart/form-data; boundary={boundary}",
                "--data-binary", f"@{tmp}",
                target["url"],
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout or "curl failed")
    finally:
        if tmp.exists():
            tmp.unlink()
    return target["resourceUrl"]


def product_bundle(handle: str) -> dict:
    data = run_graphql(
        """
        query ($handle: String!) {
          productByHandle(handle: $handle) {
            id
            handle
            media(first: 30) {
              nodes {
                ... on MediaImage { id alt }
              }
            }
            variants(first: 10) {
              nodes {
                id
                title
                selectedOptions { name value }
              }
            }
          }
        }
        """,
        {"handle": handle},
    )
    node = data["productByHandle"]
    if not node:
        raise RuntimeError(f"missing product {handle}")
    return node


def find_media_by_alt(product: dict, alt: str):
    for n in product.get("media", {}).get("nodes") or []:
        if (n.get("alt") or "").strip() == alt.strip():
            return n.get("id")
    return None


def create_media(product_id: str, resource_url: str, alt: str) -> str:
    data = run_graphql(
        """
        mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { ... on MediaImage { id } }
            mediaUserErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "media": [{
                "alt": alt,
                "mediaContentType": "IMAGE",
                "originalSource": resource_url,
            }],
        },
        mutate=True,
    )
    block = data["productCreateMedia"]
    if block.get("mediaUserErrors"):
        raise RuntimeError(block["mediaUserErrors"])
    return block["media"][0]["id"]


def variant_id_for_size(product: dict, size: str) -> str:
    for v in product.get("variants", {}).get("nodes") or []:
        opts = v.get("selectedOptions") or []
        for o in opts:
            if o.get("value") == size:
                return v["id"]
        if v.get("title") == size:
            return v["id"]
    raise RuntimeError(f"variant {size} not found on {product.get('handle')}")


def append_variant_media(product_id: str, variant_id: str, media_id: str) -> None:
    data = run_graphql(
        """
        mutation productVariantAppendMedia($productId: ID!, $variantMedia: [ProductVariantAppendMediaInput!]!) {
          productVariantAppendMedia(productId: $productId, variantMedia: $variantMedia) {
            product { id }
            userErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "variantMedia": [{
                "variantId": variant_id,
                "mediaIds": [media_id],
            }],
        },
        mutate=True,
    )
    errs = data["productVariantAppendMedia"].get("userErrors") or []
    if errs:
        # already linked is acceptable
        msg = json.dumps(errs, ensure_ascii=False)
        if "already" in msg.lower() or "duplicate" in msg.lower():
            print(f"    note: {msg}")
            return
        raise RuntimeError(msg)


def main() -> int:
    cache = {}
    for item in MAPPING:
        src = SRC / item["src"]
        if not src.exists():
            print(f"SKIP missing {src}")
            continue
        dest = OUT / item["file"]
        if not dest.exists():
            optimize(src, dest)
        print(f"\n== {item['handle']} · {item['size']}")
        print(f"   {item['file']} ({dest.stat().st_size // 1024} KB)")

        if item["handle"] not in cache:
            cache[item["handle"]] = product_bundle(item["handle"])
        product = cache[item["handle"]]

        media_id = find_media_by_alt(product, item["alt"])
        if media_id:
            print(f"   media exists: {media_id}")
        else:
            resource = upload_staged(dest)
            media_id = create_media(product["id"], resource, item["alt"])
            print(f"   uploaded: {media_id}")
            # refresh cache media list
            cache[item["handle"]] = product_bundle(item["handle"])
            product = cache[item["handle"]]

        vid = variant_id_for_size(product, item["size"])
        print(f"   link variant {item['size']} → {vid}")
        append_variant_media(product["id"], vid, media_id)
        print("   OK linked")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
