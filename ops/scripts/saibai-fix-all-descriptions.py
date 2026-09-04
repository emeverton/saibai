#!/usr/bin/env python3
"""Revisa descriptionHtml de todos os produtos ACTIVE Saibai (HTML limpo + tamanhos)."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"

FOOTER = (
    "<hr><p><strong>Por que Empório Saibai?</strong></p>"
    "<ul>"
    "<li><strong>Produção própria:</strong> Do plantio à colheita em Piedade, interior de São Paulo.</li>"
    "<li><strong>Sem atravessadores:</strong> Controle total de qualidade, do campo à sua mesa.</li>"
    "<li><strong>Artesanal de verdade:</strong> Processos cuidadosos que preservam sabor, textura e procedência.</li>"
    "</ul>"
)

FRESH_CONSERVE = (
    "<li><strong>Conservação:</strong> mantenha sob refrigeração e consuma preferencialmente "
    "nos primeiros dias após o recebimento (idealmente até 5 dias)</li>"
    "<li><strong>Variedade:</strong> roxa de São Roque · cultivo próprio Saibai · Piedade/SP</li>"
    "<li>Tamanho e coloração podem apresentar pequenas variações naturais</li>"
)


def in_natura(title: str, lead: str, size_line: str, ficha_items: list[str]) -> str:
    ficha = "".join(f"<li>{item}</li>" for item in ficha_items)
    return (
        f"<p><strong>{title}</strong> — {lead}</p>"
        f"<p>{size_line}</p>"
        "<ul>"
        "<li><strong>Produto:</strong> alcachofra in natura</li>"
        "<li><strong>Uso:</strong> assar, cozinhar, rechear, entradas e acompanhamentos</li>"
        "<li><strong>Origem:</strong> cultivo próprio Saibai, Piedade/SP</li>"
        "</ul>"
        "<hr><p><strong>Sugestões de uso</strong></p>"
        "<ul>"
        "<li>Alcachofra assada com azeite, alho e ervas.</li>"
        "<li>Recheada com farofa ou queijos, ao forno.</li>"
        "<li>Cozida e servida como acompanhamento ou antepasto.</li>"
        "</ul>"
        "<hr><p><strong>Ficha técnica — tamanho</strong></p>"
        f"<ul>{ficha}{FRESH_CONSERVE}</ul>"
        + FOOTER
    )


DESCRIPTIONS: Dict[str, Dict[str, Any]] = {
    # ── Conservas (já revisadas; reaplicar para garantir padrão) ──
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
    },
    # ── Flores / Chaveiro ──
    "flores-desidratadas": {
        "descriptionHtml": (
            "<p><strong>Flores Desidratadas Selecionadas Saibai</strong> — o detalhe que transforma pratos e drinks "
            "em obras de arte, cultivadas com rigor em Piedade/SP.</p>"
            "<p>Processo de desidratação cuidadoso que preserva cores vibrantes e formas naturais por muito mais "
            "tempo que flores frescas. Ideais para chefs e mixologistas.</p>"
            "<ul>"
            "<li><strong>Conteúdo:</strong> aprox. 15&nbsp;g (mix variado conforme safra)</li>"
            "<li><strong>100% natural:</strong> sem aditivos</li>"
            "<li><strong>Uso:</strong> gastronomia e decoração</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Guarnição de coquetéis, gin tônica e drinques autorais.</li>"
            "<li>Decoração de sobremesas, bolos e mesas de eventos.</li>"
            "<li>Finalização de risotos, saladas e pratos de alta gastronomia.</li>"
            "</ul>"
            "<hr><p><strong>Ficha técnica</strong></p>"
            "<ul>"
            "<li><strong>Peso:</strong> aprox. 15&nbsp;g</li>"
            "<li><strong>Validade:</strong> 12 meses em embalagem fechada</li>"
            "<li><strong>Conservação:</strong> local fresco, seco, ao abrigo de umidade e luz direta</li>"
            "<li><strong>Ingredientes:</strong> mix de flores comestíveis desidratadas (espécies conforme safra)</li>"
            "<li>Sem conservantes · Natural · Vegano · Produção artesanal · Piedade/SP</li>"
            "</ul>"
            + FOOTER
        ),
    },
    "chaveiro-saibai": {
        "descriptionHtml": (
            "<p><strong>Chaveiro Alcachofra Empório Saibai</strong> — leve o símbolo da fazenda em Piedade/SP "
            "sempre com você.</p>"
            "<p>Design autoral em formato de alcachofra, acabamento premium em metal esmaltado. "
            "Souvenir exclusivo para quem valoriza o lifestyle Saibai.</p>"
            "<ul>"
            "<li><strong>Material:</strong> metal esmaltado</li>"
            "<li><strong>Dimensões:</strong> aprox. 4&nbsp;cm de altura</li>"
            "<li><strong>Inclui:</strong> argola metálica</li>"
            "</ul>"
            "<hr><p><strong>Sugestões de uso</strong></p>"
            "<ul>"
            "<li>Souvenir de visita à fazenda ou evento Saibai.</li>"
            "<li>Presente para clientes, parceiros e amantes de gastronomia.</li>"
            "<li>Charm em bolsas, mochilas e chaves.</li>"
            "</ul>"
            "<hr><p><strong>Informações do produto</strong></p>"
            "<ul>"
            "<li>Produção exclusiva Empório Saibai · Piedade/SP</li>"
            "<li>Edição limitada</li>"
            "</ul>"
            + FOOTER
        ),
    },
    # ── In natura (T) ──
    "alcachofra-in-natura-t8": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura T8",
            "alcachofras de tamanho especial, cultivadas pela Saibai em Piedade/SP e colhidas no ponto ideal.",
            "A classificação <strong>T8</strong> corresponde a uma caixa com <strong>8 unidades</strong> — "
            "ideais para assar, cozinhar, rechear e pratos sofisticados.",
            [
                "<strong>Classificação:</strong> T8",
                "<strong>Conteúdo:</strong> caixa com 8 unidades",
            ],
        ),
    },
    "alcachofra-in-natura-t12": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura T12",
            "alcachofras selecionadas, cultivadas pela Saibai em Piedade/SP e enviadas frescas.",
            "A classificação <strong>T12</strong> corresponde a uma caixa com <strong>12 unidades</strong> — "
            "ideais para assar, cozinhar, rechear ou servir como acompanhamento.",
            [
                "<strong>Classificação:</strong> T12",
                "<strong>Conteúdo:</strong> caixa com 12 unidades",
            ],
        ),
    },
    "alcachofra-in-natura-t14": {
        # Título live já é T16; handle legado t14. Descrição segue a classificação real T16.
        "title": "Alcachofra In Natura T16",
        "descriptionHtml": in_natura(
            "Alcachofra In Natura T16",
            "alcachofras cultivadas pela Saibai em Piedade/SP, colhidas no ponto ideal de sabor e textura.",
            "A classificação <strong>T16</strong> corresponde a uma caixa com <strong>16 unidades</strong> — "
            "versáteis para assar, cozinhar, rechear ou compor entradas sofisticadas.",
            [
                "<strong>Classificação:</strong> T16",
                "<strong>Conteúdo:</strong> caixa com 16 unidades",
            ],
        ),
    },
    "alcachofra-in-natura-t20": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura T20",
            "alcachofras cultivadas pela Saibai em Piedade/SP, colhidas no ponto ideal para preservar frescor.",
            "A classificação <strong>T20</strong> corresponde a uma caixa com <strong>20 unidades</strong> — "
            "ideais para servir inteiras, entradas, antepastos e acompanhamentos.",
            [
                "<strong>Classificação:</strong> T20",
                "<strong>Conteúdo:</strong> caixa com 20 unidades",
            ],
        ),
    },
    # ── In natura (P/M/G/Mini) ──
    "alcachofra-in-natura-p": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura — P",
            "alcachofras cultivadas pela Saibai em Piedade/SP, colhidas no ponto ideal.",
            "A <strong>Caixa P</strong> contém <strong>13 unidades</strong> (Tipo 25) — "
            "ideais para entradas, antepastos e preparos com apresentação delicada.",
            [
                "<strong>Classificação:</strong> P · Tipo 25",
                "<strong>Conteúdo:</strong> caixa com 13 unidades",
            ],
        ),
    },
    "alcachofra-in-natura-m": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura — M",
            "alcachofras cultivadas pela Saibai em Piedade/SP, colhidas no ponto ideal.",
            "A <strong>Caixa M</strong> contém <strong>10 unidades</strong> (Tipo 16) — "
            "ideais para entradas, antepastos e preparos com apresentação delicada.",
            [
                "<strong>Classificação:</strong> M · Tipo 16",
                "<strong>Conteúdo:</strong> caixa com 10 unidades",
            ],
        ),
    },
    "alcachofra-in-natura-g": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura — G",
            "alcachofras cultivadas pela Saibai em Piedade/SP, colhidas no ponto ideal.",
            "A <strong>Caixa G</strong> contém <strong>8 unidades</strong> (Tipo 12) — "
            "ideais para entradas, antepastos e preparos com apresentação sofisticada.",
            [
                "<strong>Classificação:</strong> G · Tipo 12",
                "<strong>Conteúdo:</strong> caixa com 8 unidades",
            ],
        ),
    },
    "alcachofra-in-natura-mini": {
        "descriptionHtml": in_natura(
            "Alcachofra In Natura — Mini (AAA)",
            "alcachofras mini selecionadas, cultivadas pela Saibai em Piedade/SP.",
            "A <strong>Caixa Mini AAA</strong> pesa aprox. <strong>2,9&nbsp;kg</strong> — "
            "ideal para entradas, antepastos e apresentações delicadas.",
            [
                "<strong>Classificação:</strong> Mini · AAA",
                "<strong>Conteúdo:</strong> caixa aprox. 2,9&nbsp;kg",
            ],
        ),
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


def product_id(handle: str) -> tuple[str, str]:
    data = gql(
        """
        query($handle: String!) {
          productByHandle(handle: $handle) { id title }
        }
        """,
        {"handle": handle},
    )
    p = data.get("productByHandle")
    if not p:
        raise RuntimeError(f"Não encontrado: {handle}")
    return p["id"], p["title"]


def update_product(product_id: str, fields: dict) -> None:
    inp = {"id": product_id, **fields}
    data = gql(
        """
        mutation productUpdate($input: ProductInput!) {
          productUpdate(input: $input) {
            product { id title }
            userErrors { field message }
          }
        }
        """,
        {"input": inp},
    )
    errs = data["productUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs)


def main() -> int:
    dry = "--dry-run" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    targets = {h: DESCRIPTIONS[h] for h in only} if only else DESCRIPTIONS

    reports = []
    for handle, cfg in targets.items():
        pid, current_title = product_id(handle)
        payload = {"descriptionHtml": cfg["descriptionHtml"]}
        if cfg.get("title") and cfg["title"] != current_title:
            payload["title"] = cfg["title"]
        print(f"\n=== {handle} ===")
        print(f"title={payload.get('title', current_title)} | desc={len(cfg['descriptionHtml'])} chars")
        if dry:
            reports.append({"handle": handle, "dry_run": True})
            continue
        update_product(pid, payload)
        print("OK")
        reports.append({"handle": handle, "ok": True, "chars": len(cfg["descriptionHtml"])})
        time.sleep(0.6)

    print("\n" + json.dumps(reports, ensure_ascii=False, indent=2))
    print(f"\nTotal: {len(reports)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
