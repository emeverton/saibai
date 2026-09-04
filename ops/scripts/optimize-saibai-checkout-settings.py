#!/usr/bin/env python3
"""Checklist + API — Admin → Configurações → Checkout."""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
LOCALE_PATH = ROOT / "locales" / "pt-BR.json"
STORE = "byinbz-0k.myshopify.com"
PROFILE_ID = "gid://shopify/CheckoutProfile/5598216510"
ADMIN_CHECKOUT = "https://admin.shopify.com/store/emporiosaibai/settings/checkout"
ADMIN_PAYMENTS = "https://admin.shopify.com/store/emporiosaibai/settings/payments"
ADMIN_SHIPPING = "https://admin.shopify.com/store/emporiosaibai/settings/shipping"
ADMIN_EVENTS = "https://admin.shopify.com/store/emporiosaibai/settings/customer_events"

KV = {
    "accent": "#76BD22",
    "accent_hover": "#5A9018",
    "background": "#F4F9F0",
    "text": "#2A3A1A",
    "border": "#E2EDDA",
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
    data = json.loads(out[start:])
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data


def audit_api() -> dict:
    q = """
    query {
      shop {
        name currencyCode primaryDomain { url }
        paymentSettings { supportedDigitalWallets }
        shopPolicies { type title url }
        customerAccounts
        customerAccountsV2 {
          loginRequiredAtCheckout
          loginLinksVisibleOnStorefrontAndCheckout
        }
      }
      checkoutProfiles(first: 3) {
        nodes { id name isPublished }
      }
      deliveryProfiles(first: 5) {
        nodes { id name default activeMethodDefinitionsCount }
      }
      discountNodes(first: 5, query: "type:free_shipping status:active") {
        nodes { discount { ... on DiscountAutomaticFreeShipping { title } } }
      }
    }
    """
    return gql(q)


def audit_locale() -> Tuple[int, int, List[str]]:
    text = LOCALE_PATH.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    data = json.loads(text)
    shopify = data.get("shopify", {})
    checkout = shopify.get("checkout", {})

    def flatten(obj: dict, prefix: str = "") -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                out.update(flatten(v, key))
            else:
                out[key] = v
        return out

    flat = flatten(checkout, "checkout")
    eng = [
        (k, v)
        for k, v in flat.items()
        if isinstance(v, str)
        and re.search(r"\b(Checkout|Sign in|Log in|Thank you for your|Continue shopping)\b", v, re.I)
    ]
    return len(flat), len(eng), [f"{k}: {v[:70]}" for k, v in eng[:8]]


def score_checkout(api: dict, locale_keys: int, eng_count: int) -> Tuple[int, List[str]]:
    score = 0
    notes: List[str] = []
    shop = api.get("shop", {})

    profiles = api.get("checkoutProfiles", {}).get("nodes", [])
    published = [p for p in profiles if p.get("isPublished")]
    if published:
        score += 1
        notes.append(f"✓ Perfil checkout publicado: {published[0]['name']}")
    else:
        notes.append("✗ Nenhum perfil de checkout publicado")

    policies = shop.get("shopPolicies", [])
    required = {"PRIVACY_POLICY", "REFUND_POLICY", "SHIPPING_POLICY", "TERMS_OF_SERVICE", "CONTACT_INFORMATION"}
    found = {p["type"] for p in policies}
    if required.issubset(found):
        score += 2
        notes.append(f"✓ Políticas legais no checkout ({len(policies)}/6)")
    else:
        missing = required - found
        notes.append(f"⚠ Políticas faltando: {', '.join(missing)}")

    v2 = shop.get("customerAccountsV2", {})
    if shop.get("customerAccounts") == "OPTIONAL" and not v2.get("loginRequiredAtCheckout"):
        score += 1
        notes.append("✓ Checkout como convidado permitido")
    else:
        notes.append("⚠ Login obrigatório no checkout")

    if v2.get("loginLinksVisibleOnStorefrontAndCheckout"):
        score += 1
        notes.append("✓ Link «Entrar» visível no checkout")

    delivery = api.get("deliveryProfiles", {}).get("nodes", [])
    default = next((d for d in delivery if d.get("default")), None)
    if default and default.get("activeMethodDefinitionsCount", 0) >= 1:
        score += 1
        notes.append(f"✓ Frete ativo: {default['activeMethodDefinitionsCount']} métodos (perfil geral)")
    else:
        notes.append("✗ Sem métodos de frete ativos")

    discounts = api.get("discountNodes", {}).get("nodes", [])
    if any("280" in (n.get("discount", {}).get("title", "")) for n in discounts):
        score += 1
        notes.append("✓ Frete grátis R$280 ativo")
    else:
        notes.append("⚠ Frete grátis R$280 não encontrado")

    if locale_keys >= 2400:
        score += 2
        notes.append(f"✓ Traduções checkout pt-BR: {locale_keys} chaves")
    elif locale_keys >= 1000:
        score += 1
        notes.append(f"⚠ Traduções parciais: {locale_keys} chaves")
    else:
        notes.append(f"✗ Traduções insuficientes: {locale_keys}")

    if eng_count <= 3:
        score += 1
        notes.append(f"✓ Inglês residual mínimo ({eng_count} strings)")
    else:
        notes.append(f"⚠ {eng_count} strings com inglês residual")

    wallets = shop.get("paymentSettings", {}).get("supportedDigitalWallets", [])
    if wallets:
        score += 1
        notes.append(f"✓ Carteiras digitais: {', '.join(wallets)}")
    else:
        notes.append("⚠ Shop Pay / Apple Pay / Google Pay — verificar no admin")

    return score, notes


def try_branding() -> bool:
    try:
        r = subprocess.run(
            [sys.executable, "scripts/configure-saibai-checkout-branding.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        print(r.stdout.strip() or r.stderr.strip())
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def try_translations() -> bool:
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
    print(f"\n=== Checklist Admin → Checkout ===")
    print(f"URL: {ADMIN_CHECKOUT}\n")
    steps = [
        (
            "1. Branding visual (KV Saibai)",
            [
                f"Abra {ADMIN_CHECKOUT} → «Personalizar»",
                f"Cor de destaque / botão primário: {KV['accent']} (hover {KV['accent_hover']})",
                f"Fundo: {KV['background']} | Texto: {KV['text']} | Borda: {KV['border']}",
                f"Fonte: {KV['font']}",
                "Cantos: 4px (botões SMALL, global NONE)",
                "Logo: Empório Saibai (mesmo do header)",
                "Plano Basic: branding só via editor (API exige Plus)",
            ],
        ),
        (
            "2. Pagamentos",
            [
                f"Abra {ADMIN_PAYMENTS}",
                "Ative: Cartão, PIX, Boleto (conforme gateway Saibai)",
                "Ative Shop Pay (checkout acelerado + parcelamento)",
                "Teste modo sandbox antes de ir live",
            ],
        ),
        (
            "3. Frete e entrega",
            [
                f"Abra {ADMIN_SHIPPING}",
                "Perfil geral: Correios / transportadora BR ativos",
                "Frete grátis R$280 (desconto automático já criado)",
                "Prazos realistas por região (Sudeste, Sul, NE, N, CO)",
            ],
        ),
        (
            "4. Campos e informações",
            [
                "Checkout → Configurações → Campos de endereço",
                "Brasil: CEP, número, complemento, bairro",
                "Telefone obrigatório (WhatsApp pós-venda)",
                "E-mail de contato: contato@saibai.com.br",
            ],
        ),
        (
            "5. Tracking checkout (Customer Events)",
            [
                f"Abra {ADMIN_EVENTS}",
                "Pixel: Saibai Veltrus Checkout Events",
                "Rode: python3 scripts/configure-saibai-customer-events-pixel.py",
                "Cole scripts/saibai-customer-events-pixel.generated.js",
                "Eventos: checkout_started, checkout_completed (purchase)",
            ],
        ),
        (
            "6. Pós-compra",
            [
                "Página de status do pedido: branding consistente",
                "E-mail confirmação pt-BR (scripts/optimize-saibai-notifications.py)",
                "Link rastreamento + WhatsApp Saibai no e-mail",
            ],
        ),
    ]
    for title, items in steps:
        print(title)
        for item in items:
            print(f"  · {item}")
        print()


def main() -> int:
    print("=== Saibai Checkout Settings 10/10 ===\n")

    api = audit_api()
    locale_keys, eng_count, eng_samples = audit_locale()
    score, notes = score_checkout(api, locale_keys, eng_count)

    shop = api.get("shop", {})
    print(f"Loja: {shop.get('name')} | {shop.get('currencyCode')} | {shop.get('primaryDomain', {}).get('url')}")
    print(f"Score: {score}/10\n")
    for n in notes:
        print(f"  {n}")

    if eng_samples:
        print("\n  Amostra inglês residual:")
        for s in eng_samples:
            print(f"    • {s}")

    print("\n1. Traduções pt-BR (API):")
    if try_translations():
        print("  ✓ locales/pt-BR.json sincronizado")
    else:
        print("  ⚠ Falhou — rode manualmente optimize-saibai-checkout-translations.py")

    print("\n2. Branding KV (API — requer Plus):")
    if not try_branding():
        print("  → Aplicar branding manualmente no editor (passo 1 do checklist)")

    print_admin_checklist()

    print("7. Validação pós-deploy:")
    print("  · Carrinho → «Finalizar compra» → checkout pt-BR")
    print("  · Botão «Finalizar compra» / «Pagar agora» verde #76BD22")
    print("  · CEP BR → autocompletar endereço")
    print("  · Cupom + frete grátis R$280+")
    print("  · Compra convidado sem login forçado")
    print("  · Thank you page pt-BR + pixel purchase no GTM Preview")

    if score >= 8:
        print(f"\n→ Checkout API/tema: {score}/10 — complete branding + pagamentos no admin.")
    else:
        print(f"\n→ Corrija itens ✗/⚠ antes de considerar 10/10.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
