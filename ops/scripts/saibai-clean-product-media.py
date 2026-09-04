#!/usr/bin/env python3
"""Limpa galeria PDP: remove duplicatas e fotos de outro SKU. Mantém packshots + lifestyle do produto."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Sequence

STORE = "byinbz-0k.myshopify.com"

# keep = filenames canônicos (basename sem query). Ordem = ordem final da galeria.
CLEAN: Dict[str, List[str]] = {
    "conserva-de-alcachofras-coracao": [
        "coracao-m-330g.jpg",
        "coracao-g-550g.jpg",
        "saibai-conserva-coracao-330g-trio.jpg",
        "saibai-conserva-coracao-330g-dupla.jpg",
        "saibai-conserva-coracao-330g-flor.jpg",
    ],
    "conserva-de-alcachofras-fundo-pedaco": [
        "fundo-pedaco-m-330g.jpg",
        "fundo-pedaco-g-550g.jpg",
    ],
    "conserva-de-alcachofras-fundo-inteiro": [
        "fundo-inteiro-m-330g.jpg",
        "fundo-inteiro-g-600g.jpg",
        "saibai-conserva-fundo-600g.jpg",
        "saibai-conserva-fundo-600g-hand.jpg",
    ],
    # foto lateral TIPO16 é do M — não pertence ao G
    "alcachofra-in-natura-g": [
        "TIPO12-CAIXA8UN.png",
    ],
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


def basename(url: str) -> str:
    return url.split("?")[0].rstrip("/").split("/")[-1]


def product_media(handle: str) -> tuple[str, str, List[dict]]:
    data = gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            title
            media(first: 50) {
              nodes {
                id
                alt
                ... on MediaImage { image { url } }
              }
            }
          }
        }
        """,
        {"handle": handle},
    )
    product = data.get("productByHandle")
    if not product:
        raise RuntimeError(f"Produto não encontrado: {handle}")
    return product["id"], product["title"], product["media"]["nodes"]


def delete_media(product_id: str, media_ids: Sequence[str]) -> List[str]:
    if not media_ids:
        return []
    data = gql(
        """
        mutation productDeleteMedia($productId: ID!, $mediaIds: [ID!]!) {
          productDeleteMedia(productId: $productId, mediaIds: $mediaIds) {
            deletedMediaIds
            mediaUserErrors { field message }
          }
        }
        """,
        {"productId": product_id, "mediaIds": list(media_ids)},
    )
    payload = data["productDeleteMedia"]
    errs = payload.get("mediaUserErrors") or []
    if errs:
        raise RuntimeError(errs)
    return payload.get("deletedMediaIds") or []


def reorder_media(product_id: str, media_ids_in_order: Sequence[str]) -> None:
    if len(media_ids_in_order) < 2:
        return
    moves = [{"id": mid, "newPosition": str(i)} for i, mid in enumerate(media_ids_in_order)]
    data = gql(
        """
        mutation productReorderMedia($id: ID!, $moves: [MoveInput!]!) {
          productReorderMedia(id: $id, moves: $moves) {
            job { id }
            userErrors { field message }
          }
        }
        """,
        {"id": product_id, "moves": moves},
    )
    errs = (data.get("productReorderMedia") or {}).get("userErrors") or []
    if errs:
        raise RuntimeError(errs)


def clean_one(handle: str, keep_names: List[str], dry_run: bool = False) -> dict:
    product_id, title, nodes = product_media(handle)
    by_name: Dict[str, dict] = {}
    for node in nodes:
        url = ((node.get("image") or {}).get("url")) or ""
        name = basename(url)
        # primeira ocorrência do nome canônico (ignora cópias com UUID no filename)
        if name in keep_names and name not in by_name:
            by_name[name] = node
        # match UUID-suffixed dups: saibai-x_uuid.jpg → only if exact keep name
        for keep in keep_names:
            if name == keep and keep not in by_name:
                by_name[keep] = node

    keep_ids = []
    missing = []
    for name in keep_names:
        node = by_name.get(name)
        if node:
            keep_ids.append(node["id"])
        else:
            missing.append(name)

    delete_ids = [n["id"] for n in nodes if n["id"] not in keep_ids]

    report = {
        "handle": handle,
        "title": title,
        "before": len(nodes),
        "keep": [basename((by_name[n].get("image") or {}).get("url", "")) for n in keep_names if n in by_name],
        "delete_count": len(delete_ids),
        "missing": missing,
        "dry_run": dry_run,
    }

    print(f"\n=== {title} ({handle}) ===")
    print(f"antes={len(nodes)} manter={len(keep_ids)} remover={len(delete_ids)} missing={missing}")
    for n in nodes:
        url = ((n.get("image") or {}).get("url")) or ""
        name = basename(url)
        flag = "KEEP" if n["id"] in keep_ids else "DEL "
        print(f"  {flag} {name}")

    if dry_run:
        return report

    deleted = delete_media(product_id, delete_ids)
    report["deleted"] = len(deleted)
    time.sleep(1.5)
    # re-fetch keep ids in desired order (positions after delete)
    _, _, after_nodes = product_media(handle)
    after_by_name = {}
    for node in after_nodes:
        url = ((node.get("image") or {}).get("url")) or ""
        after_by_name[basename(url)] = node["id"]
    ordered = [after_by_name[n] for n in keep_names if n in after_by_name]
    if ordered:
        reorder_media(product_id, ordered)
    report["after"] = len(after_nodes)
    print(f"depois={report['after']} deleted={report['deleted']}")
    return report


def main() -> int:
    dry = "--dry-run" in sys.argv
    handles = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = {h: CLEAN[h] for h in handles} if handles else CLEAN
    reports = []
    for handle, keep in targets.items():
        reports.append(clean_one(handle, keep, dry_run=dry))
    print("\n" + json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
