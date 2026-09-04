#!/usr/bin/env python3
"""Checklist + API — Admin → Configurações → Contas de cliente."""

import json
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"
ADMIN_ACCOUNTS = "https://admin.shopify.com/store/emporiosaibai/settings/customer_accounts"
ADMIN_BRANDING = "https://admin.shopify.com/store/emporiosaibai/settings/checkout"
ACCOUNTS_URL = "https://shopify.com/92381937982/account"

KV = {
    "accent": "#76BD22",
    "background": "#F4F9F0",
    "text": "#2A3A1A",
    "font": "Jost",
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
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:300]}")
    return json.loads(out[start:])


def audit_accounts() -> dict:
    q = """
    query {
      shop {
        name
        customerAccounts
        customerAccountsV2 {
          customerAccountsVersion
          loginLinksVisibleOnStorefrontAndCheckout
          loginRequiredAtCheckout
          url
        }
      }
    }
    """
    return gql(q).get("shop", {})


def try_branding() -> bool:
    try:
        r = subprocess.run(
            [sys.executable, "scripts/configure-saibai-checkout-branding.py"],
            cwd=".",
            capture_output=True,
            text=True,
            timeout=60,
        )
        print(r.stdout.strip() or r.stderr.strip())
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def score_settings(shop: dict) -> tuple[int, list[str]]:
    score = 0
    notes: list[str] = []
    v2 = shop.get("customerAccountsV2", {})

    if shop.get("customerAccounts") == "OPTIONAL":
        score += 2
        notes.append("✓ Contas opcionais (melhor conversão DTC)")
    elif shop.get("customerAccounts") == "REQUIRED":
        score += 1
        notes.append("⚠ Contas obrigatórias — considere OPTIONAL para Saibai")
    else:
        notes.append("✗ Contas desativadas")

    if v2.get("customerAccountsVersion") == "NEW_CUSTOMER_ACCOUNTS":
        score += 3
        notes.append("✓ Novas contas de cliente (Shopify hosted)")
    else:
        notes.append("⚠ Contas legadas — migrar para novas contas no admin")

    if v2.get("loginLinksVisibleOnStorefrontAndCheckout"):
        score += 2
        notes.append("✓ Links de login visíveis na loja e checkout")
    else:
        notes.append("✗ Ative links de login na loja e checkout")

    if not v2.get("loginRequiredAtCheckout"):
        score += 2
        notes.append("✓ Login não obrigatório no checkout")
    else:
        notes.append("⚠ Login obrigatório no checkout — pode reduzir conversão")

    if v2.get("url"):
        score += 1
        notes.append(f"✓ Portal: {v2['url']}")

    return score, notes


def print_admin_checklist() -> None:
    print(f"\n=== Checklist Admin → Contas de cliente ===")
    print(f"URL: {ADMIN_ACCOUNTS}\n")
    steps = [
        (
            "1. Versão das contas",
            [
                "Confirme «Novas contas de cliente» (não legadas)",
                "Contas: «Opcional» — cliente pode comprar como convidado",
                "Links de login: visíveis na loja e no checkout",
                "Login no checkout: NÃO obrigatório",
            ],
        ),
        (
            "2. Branding contas + checkout",
            [
                f"Abra {ADMIN_BRANDING} → Personalizar",
                f"Cor de destaque: {KV['accent']}",
                f"Fundo: {KV['background']} | Texto: {KV['text']}",
                f"Fonte: {KV['font']}",
                "Aplique o mesmo visual em «Contas de cliente» e «Checkout»",
                "Ou rode: python3 scripts/configure-saibai-checkout-branding.py",
            ],
        ),
        (
            "3. Login with Shop",
            [
                "Em Contas de cliente → ative «Entrar com Shop» se disponível",
                "Checkout one-click para clientes Shop Pay",
            ],
        ),
        (
            "4. Perfil e pedidos",
            [
                "Teste login em janela anônima → portal shopify.com/account",
                "Verifique histórico de pedidos, endereços e perfil em pt-BR",
                "Confirme e-mails de pedido com link «Ver pedido» funcional",
            ],
        ),
        (
            "5. Tema (já no push)",
            [
                "Header/drawer/carrinho → links para novas contas (storefront_login_url)",
                "Drawer de conta → CTAs portal (sem formulário legado)",
                "Páginas legacy /account/* com KV Saibai como fallback",
                "Formulário BR em endereços (CEP, número, bairro)",
            ],
        ),
    ]
    for title, items in steps:
        print(title)
        for item in items:
            print(f"  · {item}")
        print()


def main() -> int:
    print("=== Saibai Customer Accounts 10/10 ===\n")

    shop = audit_accounts()
    score, notes = score_settings(shop)
    print(f"Loja: {shop.get('name')}")
    print(f"Score API: {score}/10\n")
    for n in notes:
        print(f"  {n}")

    print("\n1. Tema (implementado):")
    print("  ✓ saibai-customer-account-url.liquid (classic vs novas contas)")
    print("  ✓ Header, drawer mobile, carrinho → storefront_login_url")
    print("  ✓ Account drawer → portal CTAs (novas contas)")
    print("  ✓ pt-BR account_drawer + endereços BR")

    print("\n2. Branding checkout/contas (API):")
    if not try_branding():
        print("  ⚠ Branding via API falhou — aplicar manualmente no editor")

    print_admin_checklist()

    print("6. Validação pós-deploy:")
    print("  · Ícone conta no header → abre portal ou redireciona login")
    print("  · Carrinho vazio → link «Entrar» vai ao portal")
    print("  · Checkout → link «Entrar» visível, compra como convidado OK")
    print(f"  · Portal: {ACCOUNTS_URL}")
    print("  · Pedido teste → «Ver pedido» na conta do cliente")

    if score >= 9:
        print(f"\n→ Configuração API: {score}/10 — complete branding manual se API falhou.")
    else:
        print(f"\n→ Ajuste itens marcados com ✗/⚠ no admin.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
