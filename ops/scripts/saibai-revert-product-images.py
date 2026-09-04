#!/usr/bin/env python3
"""Reverte imagens quebradas pelo packshot rembg — restaura URLs originais do CDN."""

import json
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

# URLs originais ainda disponíveis no CDN Shopify
RESTORE: Dict[str, str] = {
    "conserva-de-alcachofras-coracao": "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/33ac18aae7cf948bb149282e3cf3cc29.jpg?v=1743615552",
    "conserva-de-alcachofras-fundo-pedaco": "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/fe2303377f1432e1d3d8330070ffbcbf.jpg?v=1743952989",
    "conserva-de-alcachofras-fundo-inteiro": "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/e0edea1bd75c50096acf7f7b6b44231e.jpg?v=1743952989",
    "alcachofra-p-saibai-caixa": "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/TIPO16-CAIXA10UN.png?v=1757377815",
    "alcachofra-mini-saibai-caixa": "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/TIPOAAA-CAIXA2.9KG.png?v=1757378120",
}


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


def product_info(handle: str) -> tuple:
    data = gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) { id title media(first: 20) { nodes { id } } }
        }
        """,
        {"handle": handle},
    )
    product = data.get("productByHandle")
    if not product:
        raise RuntimeError(f"Produto não encontrado: {handle}")
    media_ids = [n["id"] for n in product["media"]["nodes"]]
    return product["id"], product["title"], media_ids


def delete_media(product_id: str, media_ids: List[str]) -> None:
    if not media_ids:
        return
    data = gql(
        """
        mutation productDeleteMedia($productId: ID!, $mediaIds: [ID!]!) {
          productDeleteMedia(productId: $productId, mediaIds: $mediaIds) {
            deletedMediaIds
            mediaUserErrors { field message }
          }
        }
        """,
        {"productId": product_id, "mediaIds": media_ids},
    )
    errs = data["productDeleteMedia"]["mediaUserErrors"]
    if errs:
        raise RuntimeError(errs)


def attach_image(product_id: str, url: str, alt: str) -> str:
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
    image = media.get("image") or {}
    result = image.get("url")
    if result:
        return result
    media_id = media["id"]
    for _ in range(8):
        time.sleep(2)
        node = gql(
            "query($id: ID!) { node(id: $id) { ... on MediaImage { image { url } } } }",
            {"id": media_id},
        ).get("node") or {}
        result = (node.get("image") or {}).get("url")
        if result:
            return result
    return media_id


def revert_one(handle: str, url: str) -> str:
    product_id, title, media_ids = product_info(handle)
    delete_media(product_id, media_ids)
    return attach_image(product_id, url, title)


def main() -> None:
    dry = "--dry-run" in sys.argv
    results = {}
    for handle, url in RESTORE.items():
        print(f"{'[dry] ' if dry else ''}{handle}")
        print(f"  → {url[:90]}...")
        if dry:
            continue
        try:
            restored = revert_one(handle, url)
            results[handle] = restored
            print(f"  OK")
        except Exception as exc:
            print(f"  ERRO: {exc}")
    if results:
        print("\n=== IMAGENS RESTAURADAS ===")
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
