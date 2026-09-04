#!/usr/bin/env python3
"""Otimização C-level Admin Saibai — páginas, redirects, metaobjetos demo."""

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"

# Páginas legadas duplicadas → redirect antes de excluir
LEGACY_PAGES = [
    {
        "id": "gid://shopify/Page/159994216766",
        "handle": "sobre-nos",
        "redirect_to": "/pages/sobre",
    },
    {
        "id": "gid://shopify/Page/146558255422",
        "handle": "contact",
        "redirect_to": "/pages/contato",
    },
    {
        "id": "gid://shopify/Page/159994282302",
        "handle": "politica-de-troca-e-devolucao",
        "redirect_to": "/pages/politica-de-troca",
    },
]

# Metaobjetos demo Ella/fashion — irrelevantes para food Saibai
DEMO_METAOBJECT_IDS = [
    "gid://shopify/Metaobject/195076522302",  # silver
    "gid://shopify/Metaobject/195076489534",  # metal
    "gid://shopify/Metaobject/195076555070",  # plastic
    "gid://shopify/Metaobject/195076456766",  # unisex
]

REDIRECTS = [
    ("/pages/sobre-nos", "/pages/sobre"),
    ("/pages/contact", "/pages/contato"),
    ("/pages/politica-de-troca-e-devolucao", "/pages/politica-de-troca"),
    ("/pages/sobre-nos/", "/pages/sobre"),
    ("/pages/contact/", "/pages/contato"),
]

# Shopify legal policies (/policies/*) → páginas Saibai com KV e copy atualizada
POLICY_REDIRECTS = [
    ("/policies/privacy-policy", "/pages/politica-de-privacidade"),
    ("/policies/shipping-policy", "/pages/politica-de-entrega"),
    ("/policies/refund-policy", "/pages/politica-de-troca"),
    ("/policies/contact-information", "/pages/contato"),
    ("/policies/legal-notice", "/pages/sobre"),
    ("/policies/privacy-policy/", "/pages/politica-de-privacidade"),
    ("/policies/shipping-policy/", "/pages/politica-de-entrega"),
    ("/policies/refund-policy/", "/pages/politica-de-troca"),
    ("/pt-br/policies/privacy-policy", "/pt-br/pages/politica-de-privacidade"),
    ("/pt-br/policies/shipping-policy", "/pt-br/pages/politica-de-entrega"),
    ("/pt-br/policies/refund-policy", "/pt-br/pages/politica-de-troca"),
    ("/pt-br/policies/contact-information", "/pt-br/pages/contato"),
    ("/pt-br/policies/legal-notice", "/pt-br/pages/sobre"),
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
        raise ValueError(f"Sem JSON na resposta: {out[:300]}")
    return json.loads(out[start:])


def create_redirect(path: str, target: str) -> bool:
    q = """
    mutation urlRedirectCreate($urlRedirect: UrlRedirectInput!) {
      urlRedirectCreate(urlRedirect: $urlRedirect) {
        urlRedirect { id path target }
        userErrors { field message }
      }
    }
    """
    try:
        r = gql(q, {"urlRedirect": {"path": path, "target": target}})
        errs = r.get("urlRedirectCreate", {}).get("userErrors", [])
        if errs:
            msg = errs[0]["message"]
            if "já está em uso" in msg or "already" in msg.lower():
                print(f"  · redirect {path} (já existe)")
                return True
            print(f"  redirect {path}: {msg}")
            return False
        print(f"  ✓ redirect {path} → {target}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ redirect {path}: {e.output[:200]}")
        return False


def delete_page(page_id: str, handle: str) -> bool:
    q = """
    mutation pageDelete($id: ID!) {
      pageDelete(id: $id) {
        deletedPageId
        userErrors { field message }
      }
    }
    """
    try:
        r = gql(q, {"id": page_id})
        errs = r.get("pageDelete", {}).get("userErrors", [])
        if errs:
            print(f"  ✗ delete page {handle}: {errs[0]['message']}")
            return False
        print(f"  ✓ página removida: {handle}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ delete page {handle}: {e.output[:200]}")
        return False


def delete_metaobject(obj_id: str) -> bool:
    q = """
    mutation metaobjectDelete($id: ID!) {
      metaobjectDelete(id: $id) {
        deletedId
        userErrors { field message }
      }
    }
    """
    try:
        r = gql(q, {"id": obj_id})
        errs = r.get("metaobjectDelete", {}).get("userErrors", [])
        if errs:
            print(f"  ✗ metaobject {obj_id}: {errs[0]['message']}")
            return False
        print(f"  ✓ metaobject removido: {obj_id.split('/')[-1]}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ metaobject: {e.output[:200]}")
        return False


def ensure_page_templates() -> None:
    """Garante templateSuffix correto nas páginas institucionais."""
    updates = [
        ("gid://shopify/Page/160224018750", "sobre"),
        ("gid://shopify/Page/160224051518", "contato"),
        ("gid://shopify/Page/160224084286", "politica-de-troca"),
        ("gid://shopify/Page/160234996030", "historia"),
        ("gid://shopify/Page/160235028798", "fazenda"),
        ("gid://shopify/Page/160235061566", "conquistas"),
        ("gid://shopify/Page/159994249534", "politica-de-entrega"),
        ("gid://shopify/Page/148227817790", "politica-de-privacidade"),
    ]
    q = """
    mutation pageUpdate($id: ID!, $page: PageUpdateInput!) {
      pageUpdate(id: $id, page: $page) {
        page { handle templateSuffix }
        userErrors { message }
      }
    }
    """
    for page_id, suffix in updates:
        try:
            r = gql(q, {"id": page_id, "page": {"templateSuffix": suffix}})
            errs = r.get("pageUpdate", {}).get("userErrors", [])
            if errs:
                print(f"  template {suffix}: {errs[0]['message']}")
            else:
                handle = r.get("pageUpdate", {}).get("page", {}).get("handle", suffix)
                print(f"  ✓ template {handle} → {suffix}")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ template {suffix}: {e.output[:150]}")


def clean_chaveiro_demo_metafields() -> None:
    """Remove metafields demo fashion do Chaveiro Saibai."""
    q = """
    mutation {
      metafieldsDelete(metafields: [
        {ownerId: "gid://shopify/Product/12367500804414", namespace: "shopify", key: "color-pattern"},
        {ownerId: "gid://shopify/Product/12367500804414", namespace: "shopify", key: "material"},
        {ownerId: "gid://shopify/Product/12367500804414", namespace: "shopify", key: "target-gender"}
      ]) {
        userErrors { message }
      }
    }
    """
    try:
        r = gql(q)
        errs = r.get("metafieldsDelete", {}).get("userErrors", [])
        if errs:
            print(f"  · chaveiro metafields: {errs[0]['message']}")
        else:
            print("  ✓ chaveiro Saibai — metafields demo removidos")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ chaveiro: {e.output[:150]}")


def main() -> int:
    print("=== Saibai Admin Optimize ===\n")

    print("1. Redirects legados")
    for path, target in REDIRECTS:
        create_redirect(path, target)

    print("\n1b. Redirects /policies/* → páginas Saibai")
    for path, target in POLICY_REDIRECTS:
        create_redirect(path, target)

    print("\n2. Remover páginas duplicadas")
    for p in LEGACY_PAGES:
        create_redirect(f"/pages/{p['handle']}", p["redirect_to"])
        delete_page(p["id"], p["handle"])

    print("\n3. Templates institucionais")
    ensure_page_templates()

    print("\n4. Metaobjetos demo (fashion)")
    clean_chaveiro_demo_metafields()
    for oid in DEMO_METAOBJECT_IDS:
        delete_metaobject(oid)

    print("\n5. Locale pt-BR")
    try:
        r = gql(
            'mutation { shopLocaleUpdate(locale: "pt-BR", shopLocale: { published: true }) '
            "{ shopLocale { locale published primary } userErrors { message } } }"
        )
        loc = r.get("shopLocaleUpdate", {}).get("shopLocale", {})
        print(f"  ✓ pt-BR published={loc.get('published')} primary={loc.get('primary')}")
        if not loc.get("primary"):
            print("  ⚠ Defina pt-BR como idioma padrão em Configurações → Idiomas")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ locale: {e.output[:200]}")

    print("\n=== Concluído ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
