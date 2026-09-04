#!/usr/bin/env python3
"""SEO 10/10 — coleções ativas Empório Saibai."""

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

UPDATES: List[Dict[str, Any]] = [
    {
        "id": "gid://shopify/Collection/500673741118",
        "handle": "todos",
        "title": "Todos os produtos",
        "seo": {
            "title": "Todos os Produtos Saibai | Comprar Online",
            "description": "Catálogo completo Empório Saibai: conservas de alcachofra, flores e frutas desidratadas e acessórios exclusivos. Produção própria em Piedade/SP. Entrega Brasil.",
        },
    },
    {
        "id": "gid://shopify/Collection/487766425918",
        "handle": "em-conserva",
        "title": "Conservas de Alcachofra",
        "seo": {
            "title": "Conservas de Alcachofra Artesanal | Empório Saibai",
            "description": "Coração, fundo inteiro e pedaços de alcachofra em conserva artesanal. Receita própria Saibai, sem conservantes artificiais. Compre online com entrega Brasil.",
        },
    },
    {
        "id": "gid://shopify/Collection/501163983166",
        "handle": "flores-desidratadas",
        "title": "Flores Desidratadas",
        "seo": {
            "title": "Flores Desidratadas Gourmet | Empório Saibai",
            "description": "Flores desidratadas selecionadas para decoração e gastronomia. Eleve pratos e ambientes com delicadeza e sofisticação. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Collection/501164114238",
        "handle": "frutas-desidratadas",
        "title": "Frutas Desidratadas",
        "seo": {
            "title": "Frutas Desidratadas Naturais | Empório Saibai",
            "description": "Snacks de frutas desidratadas sem aditivos: maçã, abacaxi, manga e mixes Doce Pomar. Energia natural e sabor intenso. Empório Saibai, Piedade/SP.",
        },
    },
    {
        "id": "gid://shopify/Collection/501164278078",
        "handle": "chaveiro",
        "title": "Chaveiro Saibai",
        "seo": {
            "title": "Chaveiro Alcachofra Saibai | Souvenir Exclusivo",
            "description": "Chaveiro exclusivo em formato de alcachofra, símbolo do Empório Saibai. Souvenir artesanal da fazenda em Piedade/SP. Presente único e premium.",
        },
    },
    {
        "id": "gid://shopify/Collection/489065447742",
        "handle": "in-natura-1",
        "title": "Alcachofras Frescas",
        "seo": {
            "title": "Alcachofra Fresca Safra 2026 | Empório Saibai",
            "description": "Alcachofra fresca da safra 2026, colhida em Piedade/SP com logística refrigerada. Produção própria Saibai, do campo à mesa. Avisos de disponibilidade.",
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


def update_collection(item: Dict[str, Any]) -> bool:
    q = """
    mutation collectionUpdate($input: CollectionInput!) {
      collectionUpdate(input: $input) {
        collection { id handle seo { title description } }
        userErrors { field message }
      }
    }
    """
    payload = {
        "id": item["id"],
        "seo": item["seo"],
    }
    r = gql(q, {"input": payload})
    errs = r.get("collectionUpdate", {}).get("userErrors", [])
    if errs:
        print(f"  ERRO {item['title']}: {errs[0]['message']}")
        return False
    seo = r["collectionUpdate"]["collection"]["seo"]
    print(f"  OK {item['title']} ({item['handle']})")
    print(f"     title={len(seo['title'])} chars | desc={len(seo['description'])} chars")
    return True


def main() -> int:
    print(f"SEO 10/10 — {len(UPDATES)} coleções\n")
    ok = 0
    for item in UPDATES:
        if update_collection(item):
            ok += 1
    print(f"\nConcluído: {ok}/{len(UPDATES)}")
    return 0 if ok == len(UPDATES) else 1


if __name__ == "__main__":
    sys.exit(main())
