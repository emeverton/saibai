#!/usr/bin/env python3
"""Upload fotos de tamanhos das conservas aos 3 produtos pai (P/M/G)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

STORE = "byinbz-0k.myshopify.com"
ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "scripts" / "output" / "conservas-sizes"

# Produto pai → imagens (ordem: destaque de tamanhos primeiro)
PRODUCT_IMAGES = {
    "conserva-de-alcachofras-coracao": [
        ("saibai-conservas-tamanhos-comparativo.jpg", "Conservas Saibai — tamanhos P, M e G lado a lado"),
        ("saibai-conserva-coracao-330g-trio.jpg", "Coração de alcachofra em conserva — 330g"),
        ("saibai-conserva-coracao-330g-dupla.jpg", "Coração de alcachofra em conserva — detalhe 330g"),
        ("saibai-conserva-coracao-330g-flor.jpg", "Coração de alcachofra em conserva com flor"),
    ],
    "conserva-de-alcachofras-fundo-inteiro": [
        ("saibai-conservas-tamanhos-comparativo.jpg", "Conservas Saibai — tamanhos P, M e G lado a lado"),
        ("saibai-conserva-fundo-600g.jpg", "Fundo de alcachofra em conserva — 600g"),
        ("saibai-conserva-fundo-600g-hand.jpg", "Fundo de alcachofra em conserva — 600g em destaque"),
    ],
    "conserva-de-alcachofras-fundo-pedaco": [
        ("saibai-conservas-tamanhos-comparativo.jpg", "Conservas Saibai — tamanhos P, M e G lado a lado"),
        ("saibai-conserva-fundo-600g.jpg", "Fundo em pedaço — referência de tamanho G"),
        ("saibai-conserva-fundo-600g-hand.jpg", "Fundo em pedaço — detalhe do pote"),
    ],
}


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
    return payload


def product_by_handle(handle: str) -> dict:
    data = run_graphql(
        """
        query ($handle: String!) {
          productByHandle(handle: $handle) {
            id
            handle
            title
            media(first: 20) {
              nodes {
                ... on MediaImage {
                  id
                  alt
                  image { url }
                }
              }
            }
          }
        }
        """,
        {"handle": handle},
    )
    node = data.get("data", data).get("productByHandle")
    if not node:
        raise RuntimeError(f"Produto não encontrado: {handle}")
    return node


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
    block = data.get("data", data)["stagedUploadsCreate"]
    errs = block.get("userErrors") or []
    if errs:
        raise RuntimeError(errs)
    target = block["stagedTargets"][0]
    # Prefer curl — urllib costuma travar no CDN Shopify
    boundary = "----SaibaiBoundary"
    parts = []
    for p in target["parameters"]:
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode()
        )
    with open(path, "rb") as f:
        blob = f.read()
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{path.name}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
        + blob
        + f"\r\n--{boundary}--\r\n".encode()
    )
    body = b"".join(parts)
    tmp = path.with_suffix(path.suffix + ".multipart")
    tmp.write_bytes(body)
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
            raise RuntimeError(result.stderr or result.stdout or "curl upload failed")
    finally:
        if tmp.exists():
            tmp.unlink()
    return target["resourceUrl"]


def create_media(product_id: str, resource_url: str, alt: str) -> str:
    data = run_graphql(
        """
        mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media { id ... on MediaImage { id } }
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
    block = data.get("data", data)["productCreateMedia"]
    errs = block.get("mediaUserErrors") or []
    if errs:
        raise RuntimeError(errs)
    return block["media"][0]["id"]


def already_has_alt(product: dict, alt: str) -> bool:
    for node in product.get("media", {}).get("nodes") or []:
        if (node.get("alt") or "").strip() == alt.strip():
            return True
        url = ((node.get("image") or {}).get("url") or "")
        if "tamanhos-comparativo" in alt and "tamanhos" in (node.get("alt") or "").lower():
            return True
    return False


def main() -> int:
    dry = "--dry-run" in sys.argv
    for handle, images in PRODUCT_IMAGES.items():
        product = product_by_handle(handle)
        print(f"\n== {product['title']} ({handle})")
        for filename, alt in images:
            path = IMG_DIR / filename
            if not path.exists():
                print(f"  SKIP missing {filename}")
                continue
            if already_has_alt(product, alt):
                print(f"  SKIP already present: {alt}")
                continue
            print(f"  UPLOAD {filename} → {alt}")
            if dry:
                continue
            resource = upload_staged(path)
            media_id = create_media(product["id"], resource, alt)
            print(f"  OK {media_id}")
    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
