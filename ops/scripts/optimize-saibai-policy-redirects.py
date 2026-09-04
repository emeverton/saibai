#!/usr/bin/env python3
"""Redirects /policies/* → páginas Saibai (evita conteúdo duplicado/legado)."""

import json
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"

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
        raise ValueError(f"Sem JSON: {out[:300]}")
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
    r = gql(q, {"urlRedirect": {"path": path, "target": target}})
    errs = r.get("urlRedirectCreate", {}).get("userErrors", [])
    if errs:
        msg = errs[0]["message"]
        if "já está em uso" in msg or "already" in msg.lower():
            print(f"  · {path} (já existe)")
            return True
        print(f"  ✗ {path}: {msg}")
        return False
    print(f"  ✓ {path} → {target}")
    return True


def main() -> int:
    print(f"Redirects /policies/* → páginas Saibai ({len(POLICY_REDIRECTS)} regras)\n")
    ok = 0
    for path, target in POLICY_REDIRECTS:
        if create_redirect(path, target):
            ok += 1
    print(f"\nConcluído: {ok}/{len(POLICY_REDIRECTS)}")
    return 0 if ok == len(POLICY_REDIRECTS) else 1


if __name__ == "__main__":
    sys.exit(main())
