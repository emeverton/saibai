#!/usr/bin/env python3
"""Checklist + API parcial — Admin → Configurações → Privacidade do cliente."""

import json
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"
PRIVACY_HTML_PATH = "scripts/output/saibai-privacy-policy-paste.html"

ADMIN_PRIVACY = "https://admin.shopify.com/store/emporiosaibai/settings/privacy"
ADMIN_LEGAL = "https://admin.shopify.com/store/emporiosaibai/settings/legal"


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


def audit_privacy_policy() -> None:
    q = """
    query {
      shop {
        shopPolicies { type title body }
      }
    }
    """
    r = gql(q)
    for p in r.get("shop", {}).get("shopPolicies", []):
        if p["type"] != "PRIVACY_POLICY":
            continue
        body = p.get("body", "")
        auto = "{{" in body or len(body) > 5000
        print(f"  Política de privacidade: {len(body)} chars")
        if auto:
            print("  ⚠ Ainda é template automático Shopify — requer passo manual no admin")
        else:
            print("  ✓ Política customizada Saibai LGPD")


def try_privacy_policy_update(body: str) -> bool:
    q = """
    mutation updatePolicy($policy: ShopPolicyInput!) {
      shopPolicyUpdate(shopPolicy: $policy) {
        shopPolicy { title }
        userErrors { message }
      }
    }
    """
    r = gql(q, {"policy": {"type": "PRIVACY_POLICY", "body": body}})
    errs = r.get("shopPolicyUpdate", {}).get("userErrors", [])
    if errs:
        print(f"  ⚠ shopPolicyUpdate: {errs[0]['message']}")
        return False
    print("  ✓ Política de privacidade atualizada via API")
    return True


def print_admin_checklist() -> None:
    print("\n=== Checklist Admin → Privacidade do cliente ===")
    print(f"URL: {ADMIN_PRIVACY}\n")
    steps = [
        (
            "1. Política de privacidade",
            [
                f"Abra {ADMIN_LEGAL} (ou aba Política de privacidade em Privacidade)",
                "Desative «Gerenciamento automático» / «Use custom policy»",
                f"Cole o HTML de {PRIVACY_HTML_PATH}",
                "Salve",
            ],
        ),
        (
            "2. Banner de cookies Shopify",
            [
                "Em Privacidade do cliente → Banner de cookies",
                "DESATIVE o banner nativo da Shopify (tema usa banner Saibai LGPD)",
                "Se mantiver nativo + Saibai = banner duplicado",
            ],
        ),
        (
            "3. Consentimento por região",
            [
                "Em «Consentimento para cookies» / «Cookie consent»",
                "Adicione Brasil (BR) — consentimento obrigatório",
                "Opcional: UE (GDPR) se vender para Europa",
            ],
        ),
        (
            "4. Venda de dados (CCPA)",
            [
                "Ative opt-out apenas se vender para EUA/Califórnia",
                "Brasil/LGPD: não obrigatório para loja DTC nacional",
            ],
        ),
        (
            "5. E-mail do cliente",
            [
                "Configurações → Geral → E-mail do cliente → contato@saibai.com.br",
            ],
        ),
    ]
    for title, items in steps:
        print(title)
        for item in items:
            print(f"  · {item}")
        print()


def main() -> int:
    print("=== Saibai Privacy Settings 10/10 ===\n")

    print("1. Tema (já implementado no push):")
    print("  ✓ Banner LGPD Saibai + Consent Mode v2 (denied default)")
    print("  ✓ Shopify Customer Privacy API (setTrackingConsent → checkout/pixels)")
    print("  ✓ Opt-in LGPD (analytics/marketing desmarcados por padrão)")
    print("  ✓ Footer: «Preferências de cookies»")

    print("\n2. Política de privacidade (API):")
    audit_privacy_policy()
    try:
        with open(PRIVACY_HTML_PATH, encoding="utf-8") as f:
            body = f.read().strip()
        try_privacy_policy_update(body)
    except FileNotFoundError:
        print(f"  ⚠ Rode antes: python3 scripts/optimize-saibai-legal-policies.py")

    print("\n3. Escopos API:")
    print("  ⚠ consentPolicyUpdate / privacySettings exigem write_privacy_settings")
    print("  → Região BR (consentimento obrigatório) = passo manual no admin")

    print_admin_checklist()
    print("4. Após admin, valide:")
    print("  · Janela anônima → banner Saibai aparece")
    print("  · Recusar → GA4/Meta não carregam (Network tab)")
    print("  · Aceitar → setTrackingConsent + pixels ativos")
    print("  · Footer → Preferências de cookies reabre painel")
    print("  · Checkout → consentimento respeitado (mesmo domínio)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
