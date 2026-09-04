#!/usr/bin/env python3
"""Checklist + API — Admin → Configurações → Pagamentos."""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
LOCALE_PATH = ROOT / "locales" / "pt-BR.json"
STORE = "byinbz-0k.myshopify.com"
ADMIN_PAYMENTS = "https://admin.shopify.com/store/emporiosaibai/settings/payments"
ADMIN_PAYMENTS_SP = "https://admin.shopify.com/store/emporiosaibai/settings/payments/shopify-payments"
ADMIN_CHECKOUT = "https://admin.shopify.com/store/emporiosaibai/settings/checkout"
ADMIN_EVENTS = "https://admin.shopify.com/store/emporiosaibai/settings/customer_events"

DESCRIPTOR = "EMPORIO SAIBAI"
CONTACT_EMAIL = "contato@saibai.com.br"


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
    data = json.loads(out[start:])
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data


def try_shopify_payments() -> Optional[dict]:
    q = """
    query {
      shopifyPaymentsAccount {
        activated
        chargeStatementDescriptor
        payoutStatementDescriptor
        accountOpenerName
      }
    }
    """
    try:
        return gql(q).get("shopifyPaymentsAccount")
    except (RuntimeError, subprocess.CalledProcessError):
        return None


def audit_api() -> dict:
    q = """
    query {
      shop {
        name currencyCode email contactEmail
        billingAddress { countryCodeV2 }
        paymentSettings { supportedDigitalWallets }
        shopPolicies { type title url }
        plan { displayName shopifyPlus }
      }
      paymentCustomizations(first: 10) { nodes { id title enabled } }
    }
    """
    return gql(q)


def audit_locale_payments() -> Tuple[int, List[str], Dict[str, str]]:
    text = LOCALE_PATH.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    data = json.loads(text)
    checkout = data.get("shopify", {}).get("checkout", {})
    payment = checkout.get("payment", {})
    gateway = checkout.get("payment_gateway", {})

    critical = {
        "payment.title": payment.get("title", ""),
        "payment.card_security_notice": payment.get("card_security_notice", ""),
        "payment.local_payment_method_receiver_notice": payment.get("local_payment_method_receiver_notice", ""),
        "payment_gateway.credit_or_debit_card_label": gateway.get("credit_or_debit_card_label", ""),
        "payment.shop_pay_installments_label": payment.get("shop_pay_installments_label", ""),
    }

    missing = [k for k, v in critical.items() if not v]
    return len(missing), missing, critical


def audit_theme_footer() -> bool:
    footer_group = ROOT / "sections" / "footer-group.json"
    if footer_group.exists():
        text = footer_group.read_text(encoding="utf-8")
        if '"payment_enable": true' in text or '"payment_enable":true' in text:
            return True
    settings_path = ROOT / "config" / "settings_data.json"
    if settings_path.exists():
        text = re.sub(r"/\*.*?\*/", "", settings_path.read_text(encoding="utf-8"), flags=re.S)
        return '"payment_enable": true' in text or '"payment_enable":true' in text
    return False


def score_payments(api: dict, sp: Optional[dict], locale_missing: int, footer_icons: bool) -> Tuple[int, List[str]]:
    score = 0
    notes: List[str] = []
    shop = api.get("shop", {})

    if shop.get("currencyCode") == "BRL":
        score += 1
        notes.append("✓ Moeda BRL")
    else:
        notes.append(f"⚠ Moeda: {shop.get('currencyCode')}")

    if shop.get("billingAddress", {}).get("countryCodeV2") == "BR":
        score += 1
        notes.append("✓ Loja configurada no Brasil")
    else:
        notes.append("⚠ País da loja não é BR")

    wallets = shop.get("paymentSettings", {}).get("supportedDigitalWallets", [])
    if wallets:
        score += 2
        notes.append(f"✓ Carteiras digitais: {', '.join(wallets)}")
    else:
        notes.append("⚠ Shop Pay / Apple Pay / Google Pay — ativar no admin")

    if sp:
        if sp.get("activated"):
            score += 2
            notes.append("✓ Shopify Payments ativado")
            desc = sp.get("chargeStatementDescriptor") or ""
            if DESCRIPTOR.upper() in desc.upper() or "SAIBAI" in desc.upper():
                score += 1
                notes.append(f"✓ Descriptor fatura: {desc}")
            else:
                notes.append(f"⚠ Descriptor fatura: «{desc or 'não definido'}» → use {DESCRIPTOR}")
        else:
            notes.append("✗ Shopify Payments não concluído — complete verificação")
    else:
        notes.append("⚠ Shopify Payments — escopo read_shopify_payments ausente (auditoria manual)")

    policies = {p["type"] for p in shop.get("shopPolicies", [])}
    if "REFUND_POLICY" in policies:
        score += 1
        notes.append("✓ Política de reembolso vinculada ao checkout")
    else:
        notes.append("✗ Política de reembolso ausente")

    if locale_missing == 0:
        score += 1
        notes.append("✓ Strings críticas de pagamento pt-BR no tema")
    else:
        notes.append(f"⚠ {locale_missing} strings críticas faltando no locale")

    if footer_icons:
        score += 1
        notes.append("✓ Ícones de pagamento no footer do tema")
    else:
        notes.append("⚠ Ative ícones de pagamento no footer (Theme → Footer)")

    email = shop.get("contactEmail") or shop.get("email") or ""
    if CONTACT_EMAIL in email:
        score += 1
        notes.append(f"✓ E-mail contato: {email}")
    else:
        notes.append(f"⚠ E-mail contato: {email or 'vazio'} → {CONTACT_EMAIL}")

    return min(score, 10), notes


def try_sync_payment_translations() -> bool:
    try:
        r = subprocess.run(
            [sys.executable, "scripts/optimize-saibai-checkout-translations.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        print(r.stdout.strip() or r.stderr.strip())
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def print_admin_checklist() -> None:
    print(f"\n=== Checklist Admin → Pagamentos ===")
    print(f"URL: {ADMIN_PAYMENTS}\n")
    steps = [
        (
            "1. Shopify Payments (Brasil)",
            [
                f"Abra {ADMIN_PAYMENTS_SP}",
                "Complete verificação da conta (CNPJ/CPF + conta bancária BR)",
                "Ative métodos: Cartão crédito, Cartão débito, PIX, Boleto",
                f"Descriptor na fatura do cartão: «{DESCRIPTOR}» (máx. 22 caracteres)",
                "Captura: automática no checkout (padrão DTC)",
                "Modo teste DESLIGADO em produção",
            ],
        ),
        (
            "2. Shop Pay + parcelamento",
            [
                "Em Pagamentos → Shop Pay → Ativar",
                "Ative «Parcelamento Shop Pay» (até 12x conforme elegibilidade)",
                "Teste checkout logado com Shop Pay",
            ],
        ),
        (
            "3. Ordem e prioridade dos métodos",
            [
                "Ordem recomendada Saibai BR:",
                "  1. PIX (conversão imediata)",
                "  2. Cartão crédito/débito",
                "  3. Shop Pay / Parcelamento",
                "  4. Boleto (fallback)",
                "Desative gateways duplicados ou apps redundantes",
            ],
        ),
        (
            "4. Segurança e fraude",
            [
                "3D Secure ativo para cartões",
                "Shopify Protect / análise de fraude habilitada",
                "Não armazenar CVV — padrão Shopify PCI",
            ],
        ),
        (
            "5. Reembolsos e chargebacks",
            [
                "Política de reembolso pt-BR já publicada",
                "Prazo alinhado ao Código de Defesa do Consumidor (7 dias arrependimento)",
                f"E-mail chargeback/disputas: {CONTACT_EMAIL}",
            ],
        ),
        (
            "6. Tema + checkout (já implementado)",
            [
                "Footer: ícones `shop.enabled_payment_types` automáticos",
                "Checkout pt-BR: «Pagamento», «Pagar agora», aviso segurança cartão",
                "Instruções PIX/boleto pós-pedido traduzidas",
                f"Pixel purchase: {ADMIN_EVENTS}",
            ],
        ),
        (
            "7. Teste end-to-end",
            [
                "Pedido teste PIX → QR code + confirmação automática",
                "Pedido teste cartão → thank you + e-mail confirmação",
                "Pedido teste boleto → instruções + prazo vencimento",
                "Reembolso parcial/total no admin → status atualizado",
            ],
        ),
    ]
    for title, items in steps:
        print(title)
        for item in items:
            print(f"  · {item}")
        print()


def main() -> int:
    print("=== Saibai Payments Settings 10/10 ===\n")

    api = audit_api()
    sp = try_shopify_payments()
    locale_missing_count, locale_missing, critical = audit_locale_payments()
    footer_icons = audit_theme_footer()
    score, notes = score_payments(api, sp, locale_missing_count, footer_icons)

    shop = api.get("shop", {})
    print(f"Loja: {shop.get('name')} | {shop.get('currencyCode')} | Plano: {shop.get('plan', {}).get('displayName')}")
    print(f"Score: {score}/10\n")
    for n in notes:
        print(f"  {n}")

    if critical:
        print("\n  Strings checkout pagamento:")
        for k, v in critical.items():
            print(f"    · {k}: {v[:72]}{'…' if len(v) > 72 else ''}")

    print("\n1. Traduções pagamento pt-BR (API):")
    if try_sync_payment_translations():
        print("  ✓ locales/pt-BR.json sincronizado")
    else:
        print("  ⚠ Falhou — rode optimize-saibai-checkout-translations.py")

    print_admin_checklist()

    print("8. Reauth com escopo pagamentos (opcional, auditoria API):")
    print("  bash scripts/shopify-auth-full.sh")
    print("  → inclui read_shopify_payments para auditar PIX/boleto/cartão via API")

    if score >= 8:
        print(f"\n→ Pagamentos: {score}/10 — complete Shopify Payments + Shop Pay no admin.")
    else:
        print(f"\n→ Corrija itens ✗/⚠ no admin de pagamentos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
