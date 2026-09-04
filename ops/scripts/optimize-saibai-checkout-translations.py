#!/usr/bin/env python3
"""
Checkout & system pt-BR 10/10 — Empório Saibai.

Idioma primário (pt-BR): translationsRegister NÃO funciona.
Estratégia: themeFilesUpsert em locales/pt-BR.json com bloco `shopify`
+ correções no storefront (Login, etc.).
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
LOCALE_PATH = ROOT / "locales" / "pt-BR.json"
STORE = "byinbz-0k.myshopify.com"
THEME_ID = "gid://shopify/OnlineStoreTheme/186124239166"
LOCALE = "pt-BR"

# Premium manual — purchase_options + títulos críticos
MANUAL: Dict[str, str] = {
    "shopify.checkout.general.page_title": "Finalizar compra",
    "shopify.checkout.general.title": "Finalizar compra — {{shopName}}",
    "shopify.checkout.general.full_title": "{{pageTitle}} — {{shopName}}",
    "shopify.checkout.general.loading_title": "Finalizar compra — {{shopName}}",
    "shopify.checkout.general.complete_purchase_button_label": "Finalizar compra",
    "shopify.checkout.general.pay_now_button_label": "Pagar agora",
    "shopify.checkout.general.authenticate_purchase_button_label": "Confirmar pagamento",
    "shopify.checkout.general.continue_button_label": "Continuar",
    "shopify.checkout.general.all_rights_reserved": "© %{shop_name}. Todos os direitos reservados.",
    "shopify.checkout.stock.continue_cta_label": "Ir para finalizar compra",
    "shopify.checkout.order_summary.title": "Resumo do pedido",
    "shopify.checkout.order_summary.subtotal_label": "Subtotal",
    "shopify.checkout.order_summary.order_total_label": "Total",
    "shopify.checkout.order_summary.shipping_label": "Frete",
    "shopify.checkout.order_summary.discount_label": "Desconto",
    "shopify.checkout.order_summary.discount_placeholder": "Cupom ou vale-presente",
    "shopify.checkout.order_summary.apply_discount_button_label": "Aplicar",
    "shopify.checkout.payment.title": "Pagamento",
    "shopify.checkout.payment.card_security_notice": "Todas as transações são seguras e criptografadas.",
    "shopify.checkout.payment.card_security_vault_notice": "Suas informações ficam salvas com segurança. Todas as transações são criptografadas.",
    "shopify.checkout.payment.local_payment_method_receiver_notice": (
        "Após finalizar, você receberá as instruções de pagamento (PIX ou boleto). "
        "O prazo é de até {{dueDays}} dias úteis."
    ),
    "shopify.checkout.payment.shop_pay_installments_label": "Parcelamento Shop Pay",
    "shopify.checkout.payment_gateway.credit_or_debit_card_label": "Cartão de crédito ou débito",
    "shopify.checkout.payment_gateway.credit_card_label": "Cartão de crédito",
    "shopify.checkout.payment_gateway.debit_card_label": "Cartão de débito",
    "shopify.checkout.payment_errors.payment_gateway_missing": "Escolha uma forma de pagamento para continuar.",
    "shopify.checkout.contact.title": "Informações de contato",
    "shopify.checkout.shipping.title": "Endereço de entrega",
    "shopify.checkout.delivery.title": "Forma de entrega",
    "shopify.checkout.thank_you.title": "Obrigado pela compra!",
    "shopify.checkout.thank_you.page_title": "Pedido confirmado",
    "shopify.checkout.thank_you.return_to_store_label": "Continuar comprando",
    "shopify.checkout.shop_policies.purchase_options_policy": "Compras recorrentes e diferidas",
    "shopify.checkout.shop_policies.purchase_options_cancellation_policy": "Cancelamento de assinaturas",
    "shopify.checkout.payment.purchase_options_cancellation_policy_label": "política de cancelamento",
    "shopify.checkout.field_errors.purchase_options_agreement_blank": (
        "Para continuar, aceite os termos de compra recorrente ou diferida."
    ),
    "shopify.checkout.payment.continue_to_guest_checkout": "Continuar como visitante",
    "shopify.page_titles.cart": "Carrinho",
    "shopify.page_titles.account": "Minha conta",
    "shopify.page_titles.create_account": "Criar conta",
    "shopify.page_titles.collections_all": "Todos os produtos",
}

# Regras automáticas pós-tradução Shopify (remove inglês residual)
RULES: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"^Checkout$"), "Finalizar compra"),
    (re.compile(r"^Checkout - "), "Finalizar compra — "),
    (re.compile(r" - checkout$", re.I), ""),
    (re.compile(r"\bcheckout\b", re.I), "finalização da compra"),
    (re.compile(r"\bGift card\b", re.I), "Vale-presente"),
    (re.compile(r"\bgift card\b", re.I), "vale-presente"),
    (re.compile(r"\bGift cards\b", re.I), "Vales-presente"),
    (re.compile(r"\bgift cards\b", re.I), "vales-presente"),
    (re.compile(r"\bSubtotal\b"), "Subtotal"),  # ok BR
    (re.compile(r"\bContinue shopping\b", re.I), "Continuar comprando"),
    (re.compile(r"\bSign in\b", re.I), "Entrar"),
    (re.compile(r"\bLog in\b", re.I), "Entrar"),
]


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = ["shopify", "store", "execute", "-s", STORE, "--allow-mutations", "-j", "-q", query]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    start = out.find("{")
    data = json.loads(out[start:])
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data


def fetch_checkout_content() -> Dict[str, str]:
    q = """
    query($id: ID!) {
      translatableResource(resourceId: $id) {
        translatableContent { key value locale }
      }
    }
    """
    r = gql(q, {"id": THEME_ID})
    out = {}
    for c in r["translatableResource"]["translatableContent"]:
        if c["locale"] != LOCALE:
            continue
        k = c["key"]
        if k.startswith(("shopify.checkout.", "shopify.page_titles.", "shopify.notices.", "shopify.sentence.")):
            out[k] = c["value"]
    return out


def polish(value: str) -> str:
    if not isinstance(value, str):
        return value
    v = value
    for pattern, repl in RULES:
        v = pattern.sub(repl, v)
    v = re.sub(r"  +", " ", v).strip()
    v = v.replace(" .", ".").replace(" ,", ",")
    return v


def set_nested(root: dict, dotted_key: str, value: str) -> None:
    parts = dotted_key.split(".")
    cur = root
    for part in parts[:-1]:
        cur = cur.setdefault(part, {})
    cur[parts[-1]] = value


def load_locale_json() -> dict:
    text = LOCALE_PATH.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return json.loads(text)


def save_locale_json(data: dict) -> str:
    header = (
        "/*\n * ------------------------------------------------------------\n"
        " * IMPORTANT: The contents of this file are auto-generated.\n *\n"
        " * Checkout & system (shopify.*) — Empório Saibai / Veltrus\n"
        " * ------------------------------------------------------------\n */\n"
    )
    body = json.dumps(data, ensure_ascii=False, indent=2)
    LOCALE_PATH.write_text(header + body + "\n", encoding="utf-8")
    return header + body


def upsert_theme_file(content: str) -> None:
    q = """
    mutation themeFilesUpsert($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
      themeFilesUpsert(themeId: $themeId, files: $files) {
        userErrors { message field }
        upsertedThemeFiles { filename }
      }
    }
    """
    r = gql(
        q,
        {
            "themeId": THEME_ID,
            "files": [
                {
                    "filename": "locales/pt-BR.json",
                    "body": {"type": "TEXT", "value": content},
                }
            ],
        },
    )
    errs = r["themeFilesUpsert"]["userErrors"]
    if errs:
        raise RuntimeError(errs[0]["message"])
    print("  ✓ themeFilesUpsert locales/pt-BR.json")


def fix_storefront_locale(data: dict) -> int:
    fixes = {
        ("customer", "login_page", "title"): "Entrar",
        ("customer", "account", "title"): "Minha conta",
    }
    n = 0
    for path, val in fixes.items():
        cur = data
        for p in path[:-1]:
            cur = cur.setdefault(p, {})
        if cur.get(path[-1]) != val:
            cur[path[-1]] = val
            n += 1
    return n


def build_shopify_block(source: Dict[str, str]) -> dict:
    flat: Dict[str, str] = {}
    for key, default in source.items():
        if not isinstance(default, str):
            continue
        if key in MANUAL:
            flat[key] = MANUAL[key]
        else:
            flat[key] = polish(default)

    nested: dict = {}
    for key, value in flat.items():
        if key.startswith("shopify."):
            set_nested(nested, key, value)
    return nested.get("shopify", {})


def audit(source: Dict[str, str], flat: Dict[str, str]) -> None:
    bad = []
    for key, val in flat.items():
        if re.search(r"\b(Checkout|Sign in|Log in|Gift card|Thank you for your)\b", val, re.I):
            bad.append((key, val))
    po = [k for k in flat if "purchase_option" in k]
    print(f"\nAuditoria: {len(bad)} strings com inglês residual (amostra 15)")
    for k, v in bad[:15]:
        print(f"  • {k}: {v[:80]}")
    print(f"Purchase options: {len(po)} chaves")
    print(f"page_title => {flat.get('shopify.checkout.general.page_title')}")


def main() -> int:
    print("Checkout & system pt-BR 10/10 — Saibai\n")

    source = fetch_checkout_content()
    print(f"  {len(source)} chaves checkout/system na loja")

    shopify_block = build_shopify_block(source)
    locale = load_locale_json()
    locale["shopify"] = shopify_block
    n = fix_storefront_locale(locale)

    content = save_locale_json(locale)
    upsert_theme_file(content)

    flat = {}
    for key in source:
        if not isinstance(source.get(key), str):
            continue
        if key in MANUAL:
            flat[key] = MANUAL[key]
        else:
            flat[key] = polish(source[key])
    audit(source, flat)

    print(f"\nStorefront fixes: {n}")
    print("Push tema se editar localmente: shopify theme push --theme 186124239166 --only locales/pt-BR.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
