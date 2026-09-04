#!/usr/bin/env python3
"""Checklist + API — Admin → Configurações → Geral."""

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

STORE = "byinbz-0k.myshopify.com"
ADMIN_GENERAL = "https://admin.shopify.com/store/emporiosaibai/settings/general"
ADMIN_DOMAINS = "https://admin.shopify.com/store/emporiosaibai/settings/domains"
ADMIN_PLAN = "https://admin.shopify.com/store/emporiosaibai/settings/plan"

CANONICAL_NAME = "Empório Saibai"
CANONICAL_EMAIL = "contato@saibai.com.br"
CANONICAL_DESCRIPTION = (
    "Empório Saibai — produtora e distribuidora de alcachofras frescas e conservas artesanais "
    "em Piedade, SP, Capital Nacional da Alcachofra. Entrega para todo o Brasil."
)
CANONICAL_DOMAIN = "emporiosaibai.com.br"
CANONICAL_CEP = "18170-000"
CANONICAL_PHONE = "+55 15 99799-9938"


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = [
        "shopify", "store", "execute",
        "-s", STORE,
        "--allow-mutations",
        "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.stdout or str(e))
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
        name description email contactEmail
        myshopifyDomain
        primaryDomain { url host sslEnabled }
        currencyCode enabledPresentmentCurrencies
        currencyFormats { moneyFormat moneyWithCurrencyFormat }
        ianaTimezone timezoneAbbreviation
        unitSystem weightUnit
        orderNumberFormatPrefix orderNumberFormatSuffix
        setupRequired checkoutApiSupported
        billingAddress {
          address1 address2 city province provinceCode zip country countryCodeV2 phone
        }
        plan { displayName shopifyPlus }
      }
      shopLocales { locale name primary published }
      markets(first: 5) { nodes { id name primary enabled } }
    }
    """
    return gql(q)


def score_general(api: dict) -> Tuple[int, List[str]]:
    score = 0
    notes: List[str] = []
    shop = api.get("shop", {})

    name = shop.get("name", "")
    if name == CANONICAL_NAME:
        score += 1
        notes.append(f"✓ Nome da loja: {name}")
    else:
        notes.append(f"⚠ Nome: «{name}» → «{CANONICAL_NAME}» (com acento)")

    if shop.get("email") == CANONICAL_EMAIL:
        score += 1
        notes.append(f"✓ E-mail da loja: {CANONICAL_EMAIL}")
    else:
        notes.append(f"⚠ E-mail da loja: {shop.get('email')} → {CANONICAL_EMAIL}")

    contact = shop.get("contactEmail", "")
    if contact == CANONICAL_EMAIL:
        score += 2
        notes.append(f"✓ E-mail do cliente (remetente): {contact}")
    else:
        notes.append(f"⚠ E-mail do cliente: {contact} → {CANONICAL_EMAIL}")

    domain = shop.get("primaryDomain", {})
    if domain.get("host") == CANONICAL_DOMAIN:
        score += 1
        notes.append(f"✓ Domínio primário: {domain.get('url')}")
    else:
        notes.append(f"⚠ Domínio: {domain.get('host')}")

    if shop.get("currencyCode") == "BRL" and shop.get("enabledPresentmentCurrencies") == ["BRL"]:
        score += 1
        notes.append("✓ Moeda BRL (única)")
    else:
        notes.append(f"⚠ Moedas: {shop.get('enabledPresentmentCurrencies')}")

    if shop.get("ianaTimezone") == "America/Sao_Paulo":
        score += 1
        notes.append("✓ Fuso: America/Sao_Paulo (Brasília)")
    else:
        notes.append(f"⚠ Fuso: {shop.get('ianaTimezone')}")

    if shop.get("unitSystem") == "METRIC_SYSTEM" and shop.get("weightUnit") == "KILOGRAMS":
        score += 1
        notes.append("✓ Unidades: métrico + quilogramas")
    else:
        notes.append("⚠ Unidades: conferir métrico/kg")

    locales = api.get("shopLocales", [])
    pt = next((l for l in locales if l.get("locale") == "pt-BR"), None)
    if pt and pt.get("primary") and pt.get("published"):
        score += 1
        notes.append("✓ Idioma primário: pt-BR publicado")
    else:
        notes.append("⚠ Idioma pt-BR — definir como primário e publicado")

    money = shop.get("currencyFormats", {}).get("moneyFormat", "")
    if "comma_separator" in money and "R$" in money:
        score += 1
        notes.append(f"✓ Formato moeda: {money}")
    else:
        notes.append(f"⚠ Formato moeda: {money}")

    if shop.get("orderNumberFormatPrefix") == "#":
        score += 1
        notes.append("✓ Pedidos: prefixo #")
    else:
        notes.append("⚠ Formato número do pedido")

    addr = shop.get("billingAddress", {})
    if addr.get("countryCodeV2") == "BR" and addr.get("provinceCode") == "SP":
        score += 1
        notes.append(f"✓ Endereço legal: {addr.get('city')}, {addr.get('provinceCode')}")
    else:
        notes.append("⚠ Endereço legal incompleto")

    zip_code = (addr.get("zip") or "").replace("-", "")
    if zip_code == CANONICAL_CEP.replace("-", ""):
        notes.append(f"✓ CEP: {addr.get('zip')}")
    else:
        notes.append(f"⚠ CEP: {addr.get('zip')} → conferir {CANONICAL_CEP} (CNPJ/políticas)")

    desc = (shop.get("description") or "").strip()
    if len(desc) >= 80 and "Piedade" in desc:
        notes.append("✓ Descrição da loja preenchida")
    else:
        notes.append("⚠ Descrição da loja — atualizar copy Saibai")

    if not shop.get("setupRequired"):
        notes.append("✓ Setup inicial concluído")
    else:
        notes.append("✗ Setup inicial pendente")

    markets = api.get("markets", {}).get("nodes", [])
    if not markets or (len(markets) == 1 and markets[0].get("primary")):
        notes.append("✓ Mercados: Brasil (primário)")
    else:
        notes.append(f"ℹ Mercados: {len(markets)} configurados")

    return min(score, 10), notes


def print_admin_checklist() -> None:
    print(f"\n=== Checklist Admin → Geral ===")
    print(f"URL: {ADMIN_GENERAL}\n")
    steps = [
        (
            "1. Detalhes da loja",
            [
                f"Nome da loja: «{CANONICAL_NAME}»",
                f"E-mail da loja: {CANONICAL_EMAIL}",
                f"E-mail do cliente (remetente checkout/e-mails): {CANONICAL_EMAIL}",
                f"Descrição sugerida:",
                f"  {CANONICAL_DESCRIPTION}",
                "Telefone: (15) 99799-9938",
            ],
        ),
        (
            "2. Endereço padrão / legal",
            [
                "Empório Saibai · CNPJ 34.754.939/0001-63",
                "Estrada dos Lavradores, 7 — Piedade, SP",
                f"CEP: {CANONICAL_CEP} (alinhar com políticas legais)",
                f"Telefone: {CANONICAL_PHONE}",
            ],
        ),
        (
            "3. Padrões da loja",
            [
                "Fuso horário: (GMT-03:00) America/Sao_Paulo — Horário de Brasília",
                "Unidade de peso: Quilogramas (kg)",
                "Sistema de unidades: Métrico",
                "Formato moeda: R$ 1.234,56 (vírgula decimal)",
                "Prefixo pedido: # (ex.: #1001)",
            ],
        ),
        (
            "4. Idioma e mercado",
            [
                "Idioma padrão: Português (Brasil) — primário",
                "Mercado primário: Brasil",
                "Sem mercados internacionais extras (DTC nacional)",
            ],
        ),
        (
            "5. Domínio",
            [
                f"Primário: https://{CANONICAL_DOMAIN}",
                f"Conferir SSL ativo em {ADMIN_DOMAINS}",
                "Redirecionar byinbz-0k.myshopify.com → domínio customizado",
            ],
        ),
        (
            "6. SEO e consistência (tema já OK)",
            [
                "Tema/schema usa «Empório Saibai» com acento",
                "Checkout usa shop.name — corrige ao ajustar nome no admin",
                "Notificações usam contato@ — alinhar remetente cliente",
            ],
        ),
    ]
    for title, items in steps:
        print(title)
        for item in items:
            print(f"  · {item}")
        print()


def print_manual_blockers() -> None:
    print("API disponível (escopos atuais):")
    print("  ✓ shopLocaleUpdate — idioma publicado")
    print("  ✗ shop.name / contactEmail / description — SEM mutation GraphQL")
    print("  → Nome, e-mails e descrição = passo manual obrigatório no admin\n")


def main() -> int:
    print("=== Saibai General Settings 10/10 ===\n")

    api = audit_api()
    score, notes = score_general(api)
    shop = api.get("shop", {})

    print(f"Loja: {shop.get('name')} | {shop.get('myshopifyDomain')}")
    print(f"Plano: {shop.get('plan', {}).get('displayName')}")
    print(f"Score: {score}/10\n")
    for n in notes:
        print(f"  {n}")

    print_manual_blockers()
    print_admin_checklist()

    print("7. Validação pós-ajuste:")
    print("  · Checkout mostra «Empório Saibai» no título")
    print("  · E-mail pedido vem de contato@saibai.com.br")
    print("  · Rodapé checkout: © Empório Saibai")
    print("  · Rode: python3 scripts/optimize-saibai-general-settings.py")

    gaps = sum(1 for n in notes if n.startswith("⚠") or n.startswith("✗"))
    if score >= 9 and gaps == 0:
        print(f"\n→ Geral: {score}/10 — configuração completa.")
    elif score >= 7:
        print(f"\n→ Geral: {score}/10 — {gaps} ajuste(s) manuais no admin (nome + e-mail cliente).")
    else:
        print(f"\n→ Corrija itens ✗/⚠ em {ADMIN_GENERAL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
