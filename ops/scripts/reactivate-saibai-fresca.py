#!/usr/bin/env python3
"""Reativa safra fresca — menus apontando para /collections/in-natura-1."""

import json
import subprocess
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"
FRESH_COLLECTION = "gid://shopify/Collection/489065447742"

MAIN_MENU_ITEMS = [
    {"id": "gid://shopify/MenuItem/778615521598", "title": "Início", "url": "/", "type": "FRONTPAGE"},
    {
        "id": "gid://shopify/MenuItem/778615554366",
        "title": "Produtos",
        "url": "/collections/todos",
        "type": "COLLECTION",
        "resourceId": "gid://shopify/Collection/500673741118",
        "items": [
            {"id": "gid://shopify/MenuItem/778615587134", "title": "Conservas de Alcachofra", "url": "/collections/em-conserva", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/487766425918"},
            {"id": "gid://shopify/MenuItem/778615619902", "title": "Flores Desidratadas", "url": "/collections/flores-desidratadas", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501163983166"},
            {"id": "gid://shopify/MenuItem/778615652670", "title": "Frutas Desidratadas", "url": "/collections/frutas-desidratadas", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164114238"},
            {"id": "gid://shopify/MenuItem/778615685438", "title": "Chaveiro Saibai", "url": "/collections/chaveiro", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164278078"},
            {"id": "gid://shopify/MenuItem/778615718206", "title": "Alcachofras Frescas", "url": "/collections/in-natura-1", "type": "COLLECTION", "resourceId": FRESH_COLLECTION},
            {"id": "gid://shopify/MenuItem/778615750974", "title": "— Ver todos —", "url": "/collections/todos", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/500673741118"},
        ],
    },
    {
        "id": "gid://shopify/MenuItem/778615783742",
        "title": "Sobre",
        "url": "/pages/sobre",
        "type": "PAGE",
        "resourceId": "gid://shopify/Page/160224018750",
        "items": [
            {"id": "gid://shopify/MenuItem/778615816510", "title": "Nossa história", "url": "/pages/historia", "type": "PAGE", "resourceId": "gid://shopify/Page/160234996030"},
            {"id": "gid://shopify/MenuItem/778615849278", "title": "A fazenda", "url": "/pages/fazenda", "type": "PAGE", "resourceId": "gid://shopify/Page/160235028798"},
            {"id": "gid://shopify/MenuItem/778615882046", "title": "Conquistas e parcerias", "url": "/pages/conquistas", "type": "PAGE", "resourceId": "gid://shopify/Page/160235061566"},
        ],
    },
    {"id": "gid://shopify/MenuItem/778615914814", "title": "Contato", "url": "/pages/contato", "type": "PAGE", "resourceId": "gid://shopify/Page/160224051518"},
    {"id": "gid://shopify/MenuItem/778615947582", "title": "Receitas", "url": "/blogs/receitas", "type": "BLOG", "resourceId": "gid://shopify/Blog/121266110782"},
]

MENUS = [
    {"id": "gid://shopify/Menu/289574388030", "title": "Menu principal", "items": MAIN_MENU_ITEMS},
    {
        "id": "gid://shopify/Menu/294731743550",
        "title": "Produtos",
        "items": [
            {"id": "gid://shopify/MenuItem/778615980350", "title": "Conservas de Alcachofra", "url": "/collections/em-conserva", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/487766425918"},
            {"id": "gid://shopify/MenuItem/778616013118", "title": "Flores Desidratadas", "url": "/collections/flores-desidratadas", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501163983166"},
            {"id": "gid://shopify/MenuItem/778616045886", "title": "Frutas Desidratadas", "url": "/collections/frutas-desidratadas", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164114238"},
            {"id": "gid://shopify/MenuItem/778616078654", "title": "Chaveiro Saibai", "url": "/collections/chaveiro", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164278078"},
            {"id": "gid://shopify/MenuItem/778616111422", "title": "Alcachofras Frescas", "url": "/collections/in-natura-1", "type": "COLLECTION", "resourceId": FRESH_COLLECTION},
            {"id": "gid://shopify/MenuItem/778616144190", "title": "— Ver todos —", "url": "/collections/todos", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/500673741118"},
        ],
    },
    {
        "id": "gid://shopify/Menu/310021292350",
        "title": "Footer Loja",
        "items": [
            {"id": "gid://shopify/MenuItem/778615324990", "title": "Ver todos", "url": "/collections/todos", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/500673741118"},
            {"id": "gid://shopify/MenuItem/778615357758", "title": "Conservas de Alcachofra", "url": "/collections/em-conserva", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/487766425918"},
            {"id": "gid://shopify/MenuItem/778615390526", "title": "Flores Desidratadas", "url": "/collections/flores-desidratadas", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501163983166"},
            {"id": "gid://shopify/MenuItem/778615423294", "title": "Frutas Desidratadas", "url": "/collections/frutas-desidratadas", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164114238"},
            {"id": "gid://shopify/MenuItem/778615456062", "title": "Chaveiro Saibai", "url": "/collections/chaveiro", "type": "COLLECTION", "resourceId": "gid://shopify/Collection/501164278078"},
            {"id": "gid://shopify/MenuItem/778615488830", "title": "Alcachofras Frescas", "url": "/collections/in-natura-1", "type": "COLLECTION", "resourceId": FRESH_COLLECTION},
        ],
    },
]


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = ["shopify", "store", "execute", "-s", STORE, "--allow-mutations", "-j", "-q", query]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    start = out.find("{")
    return json.loads(out[start:])


def update_menu(menu_id: str, menu_title: str, items: list) -> None:
    q = """
    mutation menuUpdate($id: ID!, $title: String!, $items: [MenuItemUpdateInput!]!) {
      menuUpdate(id: $id, title: $title, items: $items) {
        userErrors { message }
      }
    }
    """
    r = gql(q, {"id": menu_id, "title": menu_title, "items": items})
    errs = r["menuUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(f"{menu_title}: {errs[0]['message']}")
    print(f"  OK {menu_title}")


def main() -> None:
    print("Menus → Alcachofras Frescas /collections/in-natura-1")
    for m in MENUS:
        update_menu(m["id"], m["title"], m["items"])


if __name__ == "__main__":
    main()
