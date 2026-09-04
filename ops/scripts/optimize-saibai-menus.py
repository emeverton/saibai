#!/usr/bin/env python3
"""Menus C-level Empório Saibai — conteúdo, loja, ajuda, header."""

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

# Páginas Saibai permitidas nos menus (template suffix Saibai)
SAIBAI_PAGE_HANDLES = {
    "sobre", "historia", "fazenda", "conquistas", "contato",
    "politica-de-entrega", "politica-de-troca", "politica-de-privacidade",
}

R = {
    "home": {"type": "FRONTPAGE"},
    "catalog": {"type": "CATALOG"},
    "sobre": {"type": "PAGE", "resourceId": "gid://shopify/Page/160224018750"},
    "historia": {"type": "PAGE", "resourceId": "gid://shopify/Page/160234996030"},
    "fazenda": {"type": "PAGE", "resourceId": "gid://shopify/Page/160235028798"},
    "conquistas": {"type": "PAGE", "resourceId": "gid://shopify/Page/160235061566"},
    "contato": {"type": "PAGE", "resourceId": "gid://shopify/Page/160224051518"},
    "entrega": {"type": "PAGE", "resourceId": "gid://shopify/Page/159994249534"},
    "troca": {"type": "PAGE", "resourceId": "gid://shopify/Page/160224084286"},
    "privacidade": {"type": "PAGE", "resourceId": "gid://shopify/Page/148227817790"},
    "receitas": {"type": "BLOG", "resourceId": "gid://shopify/Blog/121266110782"},
    "coll_fresca": {"type": "COLLECTION", "resourceId": "gid://shopify/Collection/489065447742"},
    "coll_conserva": {"type": "COLLECTION", "resourceId": "gid://shopify/Collection/487766425918"},
    "coll_flores": {"type": "COLLECTION", "resourceId": "gid://shopify/Collection/501163983166"},
    "coll_chaveiro": {"type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164278078"},
    "coll_todos": {"type": "COLLECTION", "resourceId": "gid://shopify/Collection/500673741118"},
    "coll_fresca_live": {"type": "COLLECTION", "resourceId": "gid://shopify/Collection/503630692670"},
    "fresca_aviso": {"type": "PAGE", "resourceId": "gid://shopify/Page/160224051518"},
    "ig": {"type": "HTTP", "url": "https://www.instagram.com/saibaisaladas/"},
    "fb": {"type": "HTTP", "url": "https://www.facebook.com/saladas.saibai"},
}


def item(title: str, ref: str, children: Optional[List[Dict]] = None) -> Dict[str, Any]:
    base = {"title": title, **R[ref]}
    if children:
        base["items"] = children
    return base


MENUS = {
    "footer-about-classic": {
        "id": "gid://shopify/Menu/310021325118",
        "title": "Footer Conteúdo",
        "items": [
            item("Sobre", "sobre"),
            item("Nossa história", "historia"),
            item("A fazenda", "fazenda"),
            item("Conquistas e parcerias", "conquistas"),
            item("Receitas", "receitas"),
        ],
    },
    "footer-help-classic": {
        "id": "gid://shopify/Menu/310021357886",
        "title": "Footer Ajuda",
        "items": [
            item("Contato", "contato"),
            item("Política de Entrega", "entrega"),
            item("Trocas e Devoluções", "troca"),
            item("Política de Privacidade", "privacidade"),
        ],
    },
    "footer-shop-classic": {
        "id": "gid://shopify/Menu/310021292350",
        "title": "Footer Loja",
        "items": [
            item("Ver todos", "coll_todos"),
            item("Conservas de Alcachofra", "coll_conserva"),
            item("Flores Desidratadas", "coll_flores"),
            item("Chaveiro Saibai", "coll_chaveiro"),
            item("Alcachofras Frescas", "coll_fresca_live"),
        ],
    },
    "main-menu": {
        "id": "gid://shopify/Menu/289574388030",
        "title": "Menu principal",
        "items": [
            item("Início", "home"),
            item("Produtos", "coll_todos", [
                item("Alcachofras Frescas", "coll_fresca_live"),
                item("Conservas de Alcachofra", "coll_conserva"),
                item("Flores Desidratadas", "coll_flores"),
                item("Chaveiro Saibai", "coll_chaveiro"),
                item("— Ver todos —", "coll_todos"),
            ]),
            item("Sobre", "sobre", [
                item("Nossa história", "historia"),
                item("A fazenda", "fazenda"),
                item("Conquistas e parcerias", "conquistas"),
            ]),
            item("Contato", "contato"),
            item("Receitas", "receitas"),
        ],
    },
    "produtos": {
        "id": "gid://shopify/Menu/294731743550",
        "title": "Produtos",
        "items": [
            item("Alcachofras Frescas", "coll_fresca_live"),
            item("Conservas de Alcachofra", "coll_conserva"),
            item("Flores Desidratadas", "coll_flores"),
            item("Chaveiro Saibai", "coll_chaveiro"),
            item("— Ver todos —", "coll_todos"),
        ],
    },
    "footer": {
        "id": "gid://shopify/Menu/289574420798",
        "title": "Menu de rodapé",
        "items": [
            item("Sobre", "sobre"),
            item("Nossa história", "historia"),
            item("A fazenda", "fazenda"),
            item("Conquistas e parcerias", "conquistas"),
            item("Receitas", "receitas"),
            item("Contato", "contato"),
        ],
    },
    "nossas-redes": {
        "id": "gid://shopify/Menu/300923879742",
        "title": "Nossas Redes",
        "items": [
            item("Instagram", "ig"),
            item("Facebook", "fb"),
        ],
    },
}


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = [
        "shopify", "store", "execute", "-s", STORE,
        "--allow-mutations", "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(out[:300])
    return json.loads(out[start:])


def update_menu(handle: str, cfg: Dict[str, Any]) -> bool:
    q = """
    mutation menuUpdate($id: ID!, $title: String!, $items: [MenuItemUpdateInput!]!) {
      menuUpdate(id: $id, title: $title, items: $items) {
        menu { handle title items { title url items { title url } } }
        userErrors { field message }
      }
    }
    """
    r = gql(q, {"id": cfg["id"], "title": cfg["title"], "items": cfg["items"]})
    errs = r.get("menuUpdate", {}).get("userErrors", [])
    if errs:
        print(f"  ERRO {handle}: {errs[0]['message']}")
        return False
    n = len(r["menuUpdate"]["menu"]["items"])
    print(f"  OK {handle} ({n} itens)")
    return True


def main() -> int:
    print("Menus C-level Saibai\n")
    ok = 0
    for handle, cfg in MENUS.items():
        print(f"→ {handle}")
        if update_menu(handle, cfg):
            ok += 1
    print(f"\nConcluído: {ok}/{len(MENUS)}")
    return 0 if ok == len(MENUS) else 1


if __name__ == "__main__":
    sys.exit(main())
