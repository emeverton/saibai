#!/usr/bin/env python3
"""Importa imagens de Saibai imagens/ → assets/ + produtos Shopify."""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Saibai imagens"
ASSETS = ROOT / "assets"
STORE = "byinbz-0k.myshopify.com"

BANNERS = {
    "saibai-hero-fresca.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_37.png",
    "saibai-hero-fresca-1200.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_37.png",
    "saibai-hero-fresca-800.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_37.png",
    "saibai-hero-fresca-480.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_37.png",
    "saibai-conservas-jars.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_41.png",
    "saibai-feature-fresca.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_21 (1).png",
    "saibai-farm-harvest.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_31.png",
    "saibai-flores.webp": "Flores Desidratadas/ChatGPT Image 9 de jun. de 2026, 10_21_56 (2).png",
    "saibai-frutas.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_14_43.png",
    "saibai-inst-harvest.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 10_50_01.png",
    "saibai-inst-variedades.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_08_18.png",
    "saibai-banner-flores-hero.webp": "Banners/ChatGPT Image 9 de jun. de 2026, 11_10_15.png",
}

PRODUCT_GROUPS = {
    "Conserva de Alcachofras - Coração": [
        "conserva-de-alcachofras-coracao",
        "coracao-de-alcachofra-330g-conserva-saibai",
        "coracao-de-alcachofra-550g-conserva-saibai",
        "coracao-de-alcachofra-180g-conserva-saibai",
    ],
    "Conserva de Alcachofras - Fundo inteiro": [
        "conserva-de-alcachofras-fundo-inteiro",
        "fundo-de-alcachofra-600g-conserva-saibai",
        "fundo-de-alcachofra-330g-conserva-saibai",
    ],
    "Conserva de Alcachofras - Pedaço": [
        "conserva-de-alcachofras-fundo-pedaco",
        "fundo-de-alcachofra-550g-conserva-em-pedacos-saibai",
        "fundo-de-alcachofra-330g-conserva-em-pedacos-saibai",
        "fundo-de-alcachofra-600g-conserva-com-tempero-saibai",
    ],
    "Flores Desidratadas": ["flores-desidratadas"],
    "Frutas Desidratadas - Doce Pomar 200g": ["frutas-desidratadas-doce-pomar-200g"],
    "Frutas Desidratadas - Pomar de Verão 200g": ["frutas-desidratadas-pomar-de-verao-200g"],
    "Maçã Desidratada Sem Casca 100g": ["maca-desidratada-sem-casca-100g"],
    "Abacaxi Desidratado 150g": ["abacaxi-desidratado-150g"],
    "Manga Desidratada 100g": ["manga-desidratada-100g"],
    "Alcachofra P Saibai Caixa": ["alcachofra-p-saibai-caixa"],
    "Alcachofra Mini Saibai Caixa 2,5 Kg": ["alcachofra-mini-saibai-caixa"],
    "Chaveiro Saibai": ["chaveiro-saibai"],
}

VARIANT_PREF = re.compile(r"\(2\)\.png$", re.I)


def run_graphql(query, variables=None, mutate=False):
    cmd = ["shopify", "store", "execute", "--store", STORE, "--query", query]
    if mutate:
        cmd.append("--allow-mutations")
    if variables is not None:
        cmd.extend(["--variables", json.dumps(variables)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout)
    raw = result.stdout
    start = raw.find("{")
    if start == -1:
        raise RuntimeError(raw)
    payload = json.loads(raw[start:])
    if "data" not in payload:
        payload = {"data": payload}
    return payload


def resolve_folder(folder_name):
    exact = SRC / folder_name
    if exact.is_dir():
        return exact
    target = folder_name.lower().replace("ç", "c").replace("ã", "a").replace("á", "a").replace("é", "e")
    for child in SRC.iterdir():
        if not child.is_dir() or child.name == "Banners":
            continue
        norm = child.name.lower().replace("ç", "c").replace("ã", "a").replace("á", "a").replace("é", "e")
        if norm == target:
            return child
    return None


def pick_image(folder_name):
    folder = resolve_folder(folder_name)
    if folder is None:
        return None
    files = sorted([p for p in folder.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}])
    if not files:
        return None
    for f in files:
        if VARIANT_PREF.search(f.name):
            return f
    return files[min(1, len(files) - 1)]


def to_webp(src: Path, dest: Path, max_width=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        img = img.convert("RGB")
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            size = (max_width, max(1, int(img.height * ratio)))
            img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(dest, "WEBP", quality=82, method=6)
    print(f"  asset: {dest.name} ({dest.stat().st_size // 1024} KB)")


def upload_staged(path: Path):
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
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
    target = data["data"]["stagedUploadsCreate"]["stagedTargets"][0]
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
    req = urllib.request.Request(
        target["url"],
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        resp.read()
    return target["resourceUrl"]


def product_id_by_handles(handles):
    mapping = {}
    cursor = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        data = run_graphql(
            f"""
            query {{
              products(first: 50{after}) {{
                nodes {{ id handle title }}
                pageInfo {{ hasNextPage endCursor }}
              }}
            }}
            """
        )
        block = data["data"]["products"]
        for n in block["nodes"]:
            mapping[n["handle"]] = n["id"]
        if not block["pageInfo"]["hasNextPage"]:
            break
        cursor = block["pageInfo"]["endCursor"]
    return {h: mapping[h] for h in handles if h in mapping}


def set_product_image(product_id, resource_url, alt):
    created = run_graphql(
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
    errs = created["data"]["productCreateMedia"].get("mediaUserErrors") or []
    if errs:
        raise RuntimeError(errs)
    media = created["data"]["productCreateMedia"]["media"]
    if not media:
        return
    new_id = media[0]["id"]
    run_graphql(
        """
        mutation productReorderMedia($id: ID!, $moves: [MoveInput!]!) {
          productReorderMedia(id: $id, moves: $moves) {
            job { id }
            userErrors { field message }
          }
        }
        """,
        {"id": product_id, "moves": [{"id": new_id, "newPosition": "0"}]},
        mutate=True,
    )


def process_assets():
    print("\n=== ASSETS ===")
    widths = {
        "saibai-hero-fresca-1200.webp": 1200,
        "saibai-hero-fresca-800.webp": 800,
        "saibai-hero-fresca-480.webp": 480,
    }
    for asset_name, rel in BANNERS.items():
        src = SRC / rel
        if not src.exists():
            print(f"  SKIP missing: {rel}")
            continue
        to_webp(src, ASSETS / asset_name, widths.get(asset_name))


def process_products():
    print("\n=== PRODUTOS ===")
    all_handles = [h for handles in PRODUCT_GROUPS.values() for h in handles]
    ids = product_id_by_handles(all_handles)

    for folder, handles in PRODUCT_GROUPS.items():
        img = pick_image(folder)
        if not img:
            print(f"  SKIP sem imagem: {folder}")
            continue
        print(f"\n{folder} → {img.name}")
        resource_url = upload_staged(img)
        for handle in handles:
            pid = ids.get(handle)
            if not pid:
                print(f"  ! handle não encontrado: {handle}")
                continue
            alt = f"{handle.replace('-', ' ').title()} — Empório Saibai"
            set_product_image(pid, resource_url, alt)
            print(f"  ✓ {handle}")


def main():
    if not SRC.is_dir():
        print(f"Pasta não encontrada: {SRC}", file=sys.stderr)
        sys.exit(1)
    process_assets()
    process_products()
    print("\nConcluído.")


if __name__ == "__main__":
    main()
