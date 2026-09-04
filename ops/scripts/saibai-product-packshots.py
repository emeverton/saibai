#!/usr/bin/env python3
"""DESATIVADO — rembg quebrou imagens. Use saibai-revert-product-images.py para restaurar."""

import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image
from rembg import remove

STORE = "byinbz-0k.myshopify.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PACKSHOTS: Dict[str, str] = {
    "conserva-de-alcachofras-coracao": "Saibai/GRUPO VIP - SAIBAI/ALCACHOFRAS CONGELADAS/CORACAO.png",
    "conserva-de-alcachofras-fundo-pedaco": "Saibai/GRUPO VIP - SAIBAI/ALCACHOFRAS CONGELADAS/FUNDO PEDACO.png",
    "conserva-de-alcachofras-fundo-inteiro": "Saibai/GRUPO VIP - SAIBAI/ALCACHOFRAS CONGELADAS/FUNDO INTEIRO.png",
    "alcachofra-p-saibai-caixa": "Saibai/Conteúdos - Cliente/Fotos/ALCACHOFRA SAIBAI.png",
    "alcachofra-mini-saibai-caixa": "Saibai/Conteúdos - Cliente/Fotos/ALCACHOFRA SAIBAI(1).png",
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


def remove_background(src_path: str) -> Image.Image:
    with open(src_path, "rb") as fh:
        raw = fh.read()
    out = remove(raw)
    return Image.open(io.BytesIO(out)).convert("RGBA")


def normalize_packshot(src_path: str, out_path: str, size: int = 2048, pad: float = 0.08) -> None:
    cutout = remove_background(src_path)
    flat = Image.new("RGB", cutout.size, (255, 255, 255))
    flat.paste(cutout, mask=cutout.split()[3])
    w, h = flat.size
    max_dim = int(size * (1 - 2 * pad))
    scale = min(max_dim / w, max_dim / h)
    nw = max(1, int(w * scale))
    nh = max(1, int(h * scale))
    resized = flat.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), (255, 255, 255))
    canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2))
    canvas.save(out_path, "JPEG", quality=92, optimize=True)


def staged_upload(path: str) -> str:
    filename = "saibai-packshot.jpg"
    size = os.path.getsize(path)
    data = gql(
        """
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets { url resourceUrl parameters { name value } }
            userErrors { field message }
          }
        }
        """,
        {
            "input": [{
                "filename": filename,
                "mimeType": "image/jpeg",
                "resource": "PRODUCT_IMAGE",
                "fileSize": str(size),
                "httpMethod": "POST",
            }]
        },
    )
    errs = data["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)
    target = data["stagedUploadsCreate"]["stagedTargets"][0]
    boundary = "----SaibaiPackshot"
    body_parts = []
    for p in target["parameters"]:
        body_parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode()
        )
    with open(path, "rb") as fh:
        file_data = fh.read()
    body_parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode()
        + file_data
        + f"\r\n--{boundary}--\r\n".encode()
    )
    req = urllib.request.Request(
        target["url"],
        data=b"".join(body_parts),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        resp.read()
    return target["resourceUrl"]


def product_media_ids(handle: str) -> Tuple[str, List[str]]:
    data = gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            title
            media(first: 20) { nodes { id } }
          }
        }
        """,
        {"handle": handle},
    )
    product = data.get("productByHandle")
    if not product:
        raise RuntimeError(f"Produto não encontrado: {handle}")
    media_ids = [n["id"] for n in product["media"]["nodes"]]
    return product["id"], media_ids


def delete_product_media(product_id: str, media_ids: List[str]) -> None:
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


def upload_product_image(product_id: str, resource_url: str, alt: str) -> str:
    data = gql(
        """
        mutation productCreateMedia($productId: ID!, $media: [CreateMediaInput!]!) {
          productCreateMedia(productId: $productId, media: $media) {
            media {
              ... on MediaImage { id image { url } }
            }
            mediaUserErrors { field message }
          }
        }
        """,
        {
            "productId": product_id,
            "media": [{
                "originalSource": resource_url,
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
    image = media.get("image") or {}
    url = image.get("url")
    if url:
        return url
    return wait_media_url(media_id)


def wait_media_url(media_id: str, attempts: int = 8, delay: float = 2.0) -> str:
    query = """
    query($id: ID!) {
      node(id: $id) {
        ... on MediaImage { id image { url } }
      }
    }
    """
    for _ in range(attempts):
        data = gql(query, {"id": media_id})
        node = data.get("node") or {}
        image = node.get("image") or {}
        url = image.get("url")
        if url:
            return url
        time.sleep(delay)
    return media_id


def process_one(handle: str, rel_path: str) -> Tuple[str, str]:
    src = os.path.join(ROOT, rel_path)
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    product_id, old_media = product_media_ids(handle)
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        normalize_packshot(src, tmp_path)
        delete_product_media(product_id, old_media)
        resource_url = staged_upload(tmp_path)
        alt = handle.replace("-", " ").title()
        url = upload_product_image(product_id, resource_url, alt)
        return handle, url
    finally:
        if os.path.isfile(tmp_path):
            os.unlink(tmp_path)


def main() -> None:
    dry = "--dry-run" in sys.argv
    results = {}
    for handle, rel in PACKSHOTS.items():
        src = os.path.join(ROOT, rel)
        print(f"{'[dry] ' if dry else ''}{handle} ← {rel}")
        if not os.path.isfile(src):
            print(f"  ERRO: arquivo ausente: {src}")
            continue
        if dry:
            continue
        try:
            h, url = process_one(handle, rel)
            results[h] = url
            print(f"  OK → {url[:100]}")
        except Exception as exc:
            print(f"  ERRO: {exc}")
    if results:
        print("\n=== PACKSHOTS ATUALIZADOS ===")
        print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
