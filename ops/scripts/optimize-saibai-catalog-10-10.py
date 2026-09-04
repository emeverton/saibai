#!/usr/bin/env python3
"""Catálogo 10/10 — coleções, menu, arquivados, redirect fresca."""

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

COLLECTIONS = {
    "em-conserva": "gid://shopify/Collection/487766425918",
    "alcachofras": "gid://shopify/Collection/487766393150",
    "in-natura-1": "gid://shopify/Collection/489065447742",
}

ARCHIVED_TO_REMOVE = [
    "gid://shopify/Product/11853744963902",
    "gid://shopify/Product/11858955895102",
    "gid://shopify/Product/11858949341502",
    "gid://shopify/Product/11858949308734",
    "gid://shopify/Product/11858949275966",
    "gid://shopify/Product/11858948981054",
    "gid://shopify/Product/11858948915518",
    "gid://shopify/Product/11858948882750",
    "gid://shopify/Product/12030990418238",
    "gid://shopify/Product/12030990582078",
]

MAIN_MENU_ID = "gid://shopify/Menu/289574388030"


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
        raise ValueError(f"Sem JSON: {out[:400]}")
    data = json.loads(out[start:])
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data


def remove_archived_from_smart_collections() -> None:
    """Coleções inteligentes — remove tags dos arquivados para saírem das regras."""
    q_list = """
    query {
      products(first: 50, query: "tag:alcachofra status:archived") {
        nodes { id title tags }
      }
    }
    """
    q_remove = """
    mutation tagsRemove($id: ID!, $tags: [String!]!) {
      tagsRemove(id: $id, tags: $tags) {
        userErrors { message }
      }
    }
    """
    products = gql(q_list)["products"]["nodes"]
    strip_tags = {"alcachofra", "conservados", "in_natura"}
    for p in products:
        to_remove = [t for t in p["tags"] if t in strip_tags]
        if not to_remove:
            continue
        r = gql(q_remove, {"id": p["id"], "tags": to_remove})
        errs = r["tagsRemove"]["userErrors"]
        if errs:
            print(f"  AVISO {p['title'][:40]}: {errs[0]['message']}")
        else:
            print(f"  OK tags removidas ({', '.join(to_remove)}): {p['title'][:50]}")


def update_main_menu() -> None:
    q = """
    mutation menuUpdate($id: ID!, $title: String!, $items: [MenuItemUpdateInput!]!) {
      menuUpdate(id: $id, title: $title, items: $items) {
        menu { id title }
        userErrors { field message }
      }
    }
    """
    items = [
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
                {"id": "gid://shopify/MenuItem/778615718206", "title": "Alcachofras Frescas · Em breve", "url": "/pages/contato", "type": "PAGE", "resourceId": "gid://shopify/Page/160224051518"},
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
    r = gql(q, {"id": MAIN_MENU_ID, "title": "Menu principal", "items": items})
    errs = r["menuUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs[0]["message"])
    print("  OK main-menu — Produtos → /collections/todos; fresca Em breve")


def create_fresca_redirect() -> None:
    q = """
    mutation urlRedirectCreate($urlRedirect: UrlRedirectInput!) {
      urlRedirectCreate(urlRedirect: $urlRedirect) {
        urlRedirect { id path target }
        userErrors { field message }
      }
    }
    """
    r = gql(q, {"urlRedirect": {"path": "/collections/in-natura-1", "target": "/pages/contato"}})
    errs = r["urlRedirectCreate"]["userErrors"]
    if errs:
        msg = errs[0]["message"]
        if "already" in msg.lower() or "taken" in msg.lower() or "exists" in msg.lower():
            print(f"  OK redirect (já existe): {msg}")
            return
        raise RuntimeError(msg)
    redir = r["urlRedirectCreate"]["urlRedirect"]
    print(f"  OK redirect {redir['path']} → {redir['target']}")


def update_fresca_collection_seo() -> None:
    q = """
    mutation collectionUpdate($input: CollectionInput!) {
      collectionUpdate(input: $input) {
        collection { handle productsCount { count } seo { title description } }
        userErrors { field message }
      }
    }
    """
    payload = {
        "id": COLLECTIONS["in-natura-1"],
        "title": "Alcachofras Frescas · Em breve",
        "seo": {
            "title": "Alcachofra Fresca Safra 2026 · Em Breve | Empório Saibai",
            "description": "Safra 2026 em preparação. Alcachofra fresca de Piedade/SP com logística refrigerada Saibai. Cadastre interesse pelo contato ou WhatsApp.",
        },
    }
    r = gql(q, {"input": payload})
    errs = r["collectionUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(errs[0]["message"])
    c = r["collectionUpdate"]["collection"]
    print(f"  OK {c['handle']} — {c['productsCount']['count']} produtos visíveis")


def verify_counts() -> None:
    q = """
    query {
      em: collection(id: "gid://shopify/Collection/487766425918") { productsCount { count } }
      al: collection(id: "gid://shopify/Collection/487766393150") { productsCount { count } }
      fr: collection(id: "gid://shopify/Collection/489065447742") { productsCount { count } }
    }
    """
    r = gql(q)
    print("\nContagens finais:")
    print(f"  em-conserva:   {r['em']['productsCount']['count']}")
    print(f"  alcachofras:   {r['al']['productsCount']['count']}")
    print(f"  in-natura-1:   {r['fr']['productsCount']['count']}")


def main() -> int:
    print("1/4 Remover arquivados das coleções inteligentes (tags)…")
    remove_archived_from_smart_collections()

    print("\n2/4 Menu principal…")
    update_main_menu()

    print("\n3/4 Redirect fresca…")
    create_fresca_redirect()

    print("\n4/4 SEO coleção fresca…")
    update_fresca_collection_seo()

    verify_counts()
    return 0


if __name__ == "__main__":
    sys.exit(main())
