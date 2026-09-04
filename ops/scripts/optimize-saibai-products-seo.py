#!/usr/bin/env python3
"""SEO 10/10 — produtos ativos Empório Saibai."""

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

UPDATES: List[Dict[str, Any]] = [
    {
        "id": "gid://shopify/Product/12367495201086",
        "title": "Conserva de Alcachofras - Fundo Inteiro",
        "productType": "Conservas",
        "tags": ["alcachofra", "conservados", "conserva", "gourmet"],
        "seo": {
            "title": "Fundo Inteiro de Alcachofra em Conserva | Empório Saibai",
            "description": "Fundo inteiro de alcachofra artesanal em conserva. O filé mignon da horta, firme e carnoso. Tamanhos M e G. Produção própria Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367495266622",
        "title": "Conserva de Alcachofras - Fundo Pedaço",
        "productType": "Conservas",
        "tags": ["alcachofra", "conservados", "conserva", "gourmet"],
        "seo": {
            "title": "Fundo de Alcachofra em Pedaços em Conserva | Empório Saibai",
            "description": "Fundo de alcachofra em pedaços, conserva artesanal Saibai. Ingrediente ideal para receitas gourmet. Tamanhos M e G. Produção própria, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367495528766",
        "title": "Conserva de Alcachofras - Coração",
        "productType": "Conservas",
        "tags": ["alcachofra", "conservados", "conserva", "gourmet"],
        "seo": {
            "title": "Coração de Alcachofra em Conserva | Empório Saibai",
            "description": "Coração de alcachofra em conserva artesanal, a parte mais tenra e nobre. Tamanhos P, M e G. Direto do campo ao prato. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367498772798",
        "title": "Flores Desidratadas",
        "productType": "Flores Desidratadas",
        "tags": ["flores", "desidratados", "decoracao", "gastronomia"],
        "seo": {
            "title": "Flores Desidratadas Selecionadas | Empório Saibai",
            "description": "Flores desidratadas para decoração e gastronomia. Eleve o visual das suas criações com delicadeza e sofisticação. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367499329854",
        "title": "Frutas Desidratadas - Doce Pomar 200g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "natural"],
        "seo": {
            "title": "Frutas Desidratadas Doce Pomar 200g | Empório Saibai",
            "description": "Mix Doce Pomar com frutas desidratadas selecionadas. Energia natural, sabor intenso e zero aditivos. 200g. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367499493694",
        "title": "Frutas Desidratadas - Pomar de Verão 200g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "natural"],
        "seo": {
            "title": "Frutas Desidratadas Pomar de Verão 200g | Empório Saibai",
            "description": "Pomar de Verão: mix de frutas desidratadas com o sabor das estações mais quentes. 200g sem conservantes. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367499886910",
        "title": "Maçã Desidratada Sem Casca 100g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "maca"],
        "seo": {
            "title": "Maçã Desidratada Sem Casca 100g | Empório Saibai",
            "description": "Maçã desidratada sem casca, textura macia e sabor suave. Snack saudável e natural, sem aditivos. 100g. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367500050750",
        "title": "Abacaxi Desidratado 150g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "abacaxi"],
        "seo": {
            "title": "Abacaxi Desidratado Selecionado 150g | Empório Saibai",
            "description": "Abacaxi desidratado com desidratação lenta para preservar o sabor tropical. Snack natural sem conservantes. 150g. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367500214590",
        "title": "Manga Desidratada 100g",
        "productType": "Frutas Desidratadas",
        "tags": ["frutas", "desidratados", "snack", "manga"],
        "seo": {
            "title": "Manga Desidratada Selecionada 100g | Empório Saibai",
            "description": "Manga desidratada suculenta no ápice da maturação. Snack natural com sabor intenso e concentrado. 100g. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Product/12367500804414",
        "title": "Chaveiro Saibai",
        "productType": "Acessórios",
        "tags": ["decoracao", "souvenir", "acessorios"],
        "seo": {
            "title": "Chaveiro Alcachofra Empório Saibai | Souvenir Exclusivo",
            "description": "Chaveiro exclusivo em formato de alcachofra, símbolo do Empório Saibai. Souvenir artesanal da fazenda em Piedade/SP. Design único e premium.",
        },
    },
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
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:300]}")
    return json.loads(out[start:])


def update_product(item: Dict[str, Any]) -> bool:
    q = """
    mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product { id title productType tags seo { title description } }
        userErrors { field message }
      }
    }
    """
    payload = {
        "id": item["id"],
        "productType": item["productType"],
        "tags": item["tags"],
        "seo": item["seo"],
    }
    r = gql(q, {"input": payload})
    errs = r.get("productUpdate", {}).get("userErrors", [])
    if errs:
        print(f"  ERRO {item['title']}: {errs[0]['message']}")
        return False
    seo = r["productUpdate"]["product"]["seo"]
    print(f"  OK {item['title']}")
    print(f"     type={item['productType']} | tags={len(item['tags'])} | title={len(seo['title'])} | desc={len(seo['description'])}")
    return True


def main() -> int:
    print(f"SEO 10/10 — {len(UPDATES)} produtos ativos\n")
    ok = 0
    for item in UPDATES:
        if update_product(item):
            ok += 1
    print(f"\nConcluído: {ok}/{len(UPDATES)}")
    return 0 if ok == len(UPDATES) else 1


if __name__ == "__main__":
    sys.exit(main())
