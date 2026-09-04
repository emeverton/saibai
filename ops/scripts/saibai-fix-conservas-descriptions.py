#!/usr/bin/env python3
"""Limpa HTML ChatGPT das conservas e alinha tamanhos da descrição aos rótulos reais."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

FOOTER = (
    "<hr><p><strong>Por que Empório Saibai?</strong></p>"
    "<ul>"
    "<li><strong>Produção própria:</strong> Do plantio à colheita em Piedade, interior de São Paulo.</li>"
    "<li><strong>Sem atravessadores:</strong> Controle total de qualidade, do campo à sua mesa.</li>"
    "<li><strong>Artesanal de verdade:</strong> Processos cuidadosos que preservam sabor, textura e procedência.</li>"
    "</ul>"
)

# Pesos = rótulo dos packshots Drive (líquido / drenado)
PRODUCTS: Dict[str, Dict[str, Any]] = {
    "conserva-de-alcachofras-coracao": {
        "descriptionHtml": (
            "<p><strong>Coração de Alcachofra em Conserva</strong> — a parte mais tenra e nobre da alcachofra, "
            "conservada artesanalmente na fazenda Saibai em Piedade/SP.</p>"
            "<p>Corações selecionados para preservar textura macia, sabor delicado e qualidade. "
            "Prontos para servir: entradas, saladas, antepastos, massas, risotos, pizzas e tábuas especiais.</p>"
            "<ul>"
            "<li><strong>Tamanhos:</strong> P (uso imediato) · M (jantares) · G (eventos)</li>"
            "<li><strong>Tempero suave:</strong> água, sal e vinagre</li>"
            "<li><strong>Pronto para servir:</strong> abra, escorra e use</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Antepasto com azeite trufado e parmesão ralado na hora.</li>"
            "<li>Risoto de coração de alcachofra com limão siciliano.</li>"
            "<li>Salada mediterrânea com rúcula, tomate cereja e balsâmico.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica — tamanhos</strong></p>"
            "<ul>"
            "<li><strong>P:</strong> peso líquido aprox. 180&nbsp;g</li>"
            "<li><strong>M:</strong> peso líquido 330&nbsp;g · drenado 180&nbsp;g</li>"
            "<li><strong>G:</strong> peso líquido 550&nbsp;g · drenado 340&nbsp;g</li>"
            "<li><strong>Validade:</strong> 12 meses a partir da fabricação</li>"
            "<li><strong>Conservação:</strong> local seco e ao abrigo da luz; após aberto, refrigerar e consumir em até 3 dias</li>"
            "<li><strong>Ingredientes:</strong> coração de alcachofra, água, sal e acidulante ácido cítrico</li>"
            "<li>Sem conservantes artificiais · Vegano · Sem glúten · Produção própria · Piedade/SP</li>"
            "</ul>"
            + FOOTER
        ),
        # Featured = M (rótulo CORAÇÃO bem legível na grade)
        "featured_first": ["coracao-m-330g.jpg", "coracao-g-550g.jpg"],
    },
    "conserva-de-alcachofras-fundo-pedaco": {
        "descriptionHtml": (
            "<p><strong>Fundo de Alcachofra em Pedaços</strong> — fundos selecionados e cortados em pedaços, "
            "conserva artesanal Saibai de Piedade/SP.</p>"
            "<p>Textura macia e sabor delicado, prontos para massas, risotos, saladas, molhos, recheios, "
            "pizzas e preparos do dia a dia com toque gourmet.</p>"
            "<ul>"
            "<li><strong>Tamanhos:</strong> M · G</li>"
            "<li><strong>Formato:</strong> pedaços — ideais para recheios e molhos</li>"
            "<li><strong>Tempero suave:</strong> água, sal e vinagre</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Rechear com queijos cremosos, cogumelos ou servir gratinado.</li>"
            "<li>Antepasto mediterrâneo com azeite, limão e pimenta-do-reino.</li>"
            "<li>Saladas autorais, bruschettas e tábuas de frios premium.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica — tamanhos</strong></p>"
            "<ul>"
            "<li><strong>M:</strong> peso líquido 330&nbsp;g · drenado 220&nbsp;g</li>"
            "<li><strong>G:</strong> peso líquido 550&nbsp;g · drenado 330&nbsp;g</li>"
            "<li><strong>Validade:</strong> 12 meses a partir da fabricação</li>"
            "<li><strong>Conservação:</strong> local seco e ao abrigo da luz; após aberto, refrigerar e consumir em até 3 dias</li>"
            "<li><strong>Ingredientes:</strong> fundo de alcachofra em pedaços, água, sal e acidulante ácido cítrico</li>"
            "<li>Sem conservantes artificiais · Vegano · Sem glúten · Produção própria · Piedade/SP</li>"
            "</ul>"
            + FOOTER
        ),
        # Featured = G (rótulo traz "pedaços" — diferencia na coleção)
        "featured_first": ["fundo-pedaco-g-550g.jpg", "fundo-pedaco-m-330g.jpg"],
    },
    "conserva-de-alcachofras-fundo-inteiro": {
        "descriptionHtml": (
            "<p><strong>Fundo de Alcachofra Inteiro</strong> — fundos íntegros e carnosos em conserva artesanal, "
            "produção própria Saibai em Piedade/SP.</p>"
            "<p>Peças firmes e macias para entradas, saladas, antepastos, massas, risotos e receitas especiais. "
            "O “filé mignon” da horta, pronto para servir.</p>"
            "<ul>"
            "<li><strong>Tamanhos:</strong> M · G</li>"
            "<li><strong>Formato:</strong> fundo inteiro — destaque visual no prato</li>"
            "<li><strong>Tempero suave:</strong> água, sal e vinagre</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Antepasto com azeite extra virgem, alho confitado e ervas finas.</li>"
            "<li>Base para risotos, massas artesanais e saladas premium.</li>"
            "<li>Entrada quente gratinada com queijo de cabra e tomilho.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica — tamanhos</strong></p>"
            "<ul>"
            "<li><strong>M:</strong> peso líquido 330&nbsp;g · drenado 220&nbsp;g</li>"
            "<li><strong>G:</strong> peso líquido 600&nbsp;g · drenado 380&nbsp;g</li>"
            "<li><strong>Validade:</strong> 12 meses a partir da fabricação</li>"
            "<li><strong>Conservação:</strong> local seco e ao abrigo da luz; após aberto, refrigerar e consumir em até 3 dias</li>"
            "<li><strong>Ingredientes:</strong> fundo de alcachofra, água, sal e acidulante ácido cítrico</li>"
            "<li>Sem conservantes artificiais · Vegano · Sem glúten · Produção própria · Piedade/SP</li>"
            "</ul>"
            + FOOTER
        ),
        # Featured = G 600g (pote alto — diferencia do Pedaço na grade)
        "featured_first": [
            "fundo-inteiro-g-600g.jpg",
            "fundo-inteiro-m-330g.jpg",
            "saibai-conserva-fundo-600g.jpg",
            "saibai-conserva-fundo-600g-hand.jpg",
        ],
    },
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


def get_product(handle: str) -> dict:
    data = gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) {
            id
            title
            media(first: 20) {
              nodes { id ... on MediaImage { image { url } } }
            }
          }
        }
        """,
        {"handle": handle},
    )
    product = data.get("productByHandle")
    if not product:
        raise RuntimeError(f"Não encontrado: {handle}")
    return product


def update_description(product_id: str, description_html: str) -> None:
    data = gql(
        """
        mutation productUpdate($input: ProductInput!) {
          productUpdate(input: $input) {
            product { id }
            userErrors { field message }
          }
        }
        """,
        {"input": {"id": product_id, "descriptionHtml": description_html}},
    )
    errs = data["productUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)


def reorder_media(product_id: str, media_ids: List[str]) -> None:
    if len(media_ids) < 2:
        return
    moves = [{"id": mid, "newPosition": str(i)} for i, mid in enumerate(media_ids)]
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


def apply_one(handle: str, cfg: dict, dry_run: bool = False) -> dict:
    product = get_product(handle)
    nodes = product["media"]["nodes"]
    by_name = {}
    for n in nodes:
        url = ((n.get("image") or {}).get("url")) or ""
        by_name[basename(url)] = n["id"]

    order_names = cfg.get("featured_first") or []
    ordered = [by_name[n] for n in order_names if n in by_name]
    # append remaining in current order
    for n in nodes:
        if n["id"] not in ordered:
            ordered.append(n["id"])

    report = {
        "handle": handle,
        "title": product["title"],
        "desc_chars": len(cfg["descriptionHtml"]),
        "media_order": [n for n in order_names if n in by_name],
        "dry_run": dry_run,
    }
    print(f"\n=== {product['title']} ===")
    print(f"desc={report['desc_chars']} chars | featured→ {report['media_order'][:2]}")

    if dry_run:
        return report

    update_description(product["id"], cfg["descriptionHtml"])
    time.sleep(0.8)
    reorder_media(product["id"], ordered)
    print("OK description + reorder")
    return report


def main() -> int:
    dry = "--dry-run" in sys.argv
    handles = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = {h: PRODUCTS[h] for h in handles} if handles else PRODUCTS
    reports = [apply_one(h, cfg, dry_run=dry) for h, cfg in targets.items()]
    print("\n" + json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
