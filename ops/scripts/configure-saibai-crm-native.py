#!/usr/bin/env python3
"""CRM nativo Shopify — cupons + checklist e-mail/recovery/remarketing.

Tracking permanece nativo (canais Google/Meta). Sem Klaviyo, sem pixel no tema.
Cria/atualiza códigos: 5%NOVOCLIENTE · SAIBAIRECOMPRA.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

STORE = "byinbz-0k.myshopify.com"
ADMIN = "https://admin.shopify.com/store/emporiosaibai"

CODES = [
    {
        "code": "5%NOVOCLIENTE",
        "title": "Boas-vindas 5% — novo cliente",
        "percentage": 0.05,
        "applies_once": True,
        "min_subtotal": None,
        "combines_shipping": True,
        "usage": "Popup + newsletter + Shopify Email Welcome + dica no carrinho",
    },
    {
        "code": "SAIBAIRECOMPRA",
        "title": "Recompra 8% — cliente Saibai",
        "percentage": 0.08,
        "applies_once": True,
        "min_subtotal": "120.00",
        "combines_shipping": True,
        "usage": "Somente e-mail win-back 45–60d (não exibir no site)",
    },
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
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:400]}")
    data = json.loads(out[start:])
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))
    return data


def list_code_discounts() -> List[Dict[str, Any]]:
    q = """
    query {
      discountNodes(first: 50) {
        nodes {
          id
          discount {
            __typename
            ... on DiscountCodeBasic {
              title
              status
              appliesOncePerCustomer
              codes(first: 10) { nodes { code } }
              customerGets {
                value { ... on DiscountPercentage { percentage } }
              }
            }
            ... on DiscountAutomaticFreeShipping {
              title
              status
            }
          }
        }
      }
    }
    """
    nodes = gql(q).get("discountNodes", {}).get("nodes", [])
    out: List[Dict[str, Any]] = []
    for node in nodes:
        disc = node.get("discount") or {}
        codes = [c.get("code") for c in (disc.get("codes") or {}).get("nodes") or []]
        value = ((disc.get("customerGets") or {}).get("value") or {}).get("percentage")
        out.append({
            "id": node.get("id"),
            "typename": disc.get("__typename"),
            "title": disc.get("title"),
            "status": disc.get("status"),
            "codes": codes,
            "percentage": value,
            "once": disc.get("appliesOncePerCustomer"),
        })
    return out


def find_code(rows: List[Dict[str, Any]], code: str) -> Optional[Dict[str, Any]]:
    needle = code.upper()
    for row in rows:
        for existing in row.get("codes") or []:
            if (existing or "").upper() == needle:
                return row
    return None


def basic_input(spec: Dict[str, Any]) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "title": spec["title"],
        "code": spec["code"],
        "startsAt": "2026-08-26T00:00:00Z",
        "appliesOncePerCustomer": spec["applies_once"],
        "customerSelection": {"all": True},
        "customerGets": {
            "value": {"percentage": spec["percentage"]},
            "items": {"all": True},
        },
        "combinesWith": {
            "orderDiscounts": False,
            "productDiscounts": False,
            "shippingDiscounts": bool(spec["combines_shipping"]),
        },
    }
    if spec.get("min_subtotal"):
        payload["minimumRequirement"] = {
            "subtotal": {"greaterThanOrEqualToSubtotal": spec["min_subtotal"]}
        }
    return payload


def create_code(spec: Dict[str, Any]) -> bool:
    q = """
    mutation createCode($basicCodeDiscount: DiscountCodeBasicInput!) {
      discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) {
        codeDiscountNode {
          id
          codeDiscount {
            ... on DiscountCodeBasic {
              title
              status
              codes(first: 3) { nodes { code } }
            }
          }
        }
        userErrors { field message code }
      }
    }
    """
    payload = gql(q, {"basicCodeDiscount": basic_input(spec)}).get("discountCodeBasicCreate", {})
    errs = payload.get("userErrors") or []
    if errs:
        print(f"  ✗ {spec['code']}: {errs[0].get('message')}")
        return False
    node = payload.get("codeDiscountNode") or {}
    disc = node.get("codeDiscount") or {}
    print(f"  ✓ criado {spec['code']} — {disc.get('title')} ({disc.get('status')})")
    return True


def print_admin_checklist() -> None:
    print("\n=== Checklist Admin — CRM nativo (sem Klaviyo) ===\n")
    steps = [
        (
            "1. Shopify Email (marketing)",
            [
                f"Abra {ADMIN}/email_marketing",
                "Instalar Shopify Email se ainda não estiver",
                "Remetente: contato@saibai.com.br · nome Empório Saibai",
                "Cor destaque #76BD22 · fundo #F2F5EE · texto #2A3A1A · fonte Jost/Arial",
            ],
        ),
        (
            "2. Automações Shopify Email",
            [
                f"Abra {ADMIN}/marketing/automations",
                "Welcome — trigger: inscrito newsletter (tag newsletter) · cupom 5%NOVOCLIENTE",
                "Abandoned cart — 1h · desconto único 5% expira 48h (não reutilizar SAIBAIRECOMPRA)",
                "Abandoned checkout — 10h · MESMO desconto único 5% 48h",
                "Browse abandonment — 24h · sem cupom (só lembrete produto)",
                "Post-purchase — +3d · conservas + review (sem cupom)",
                "Win-back — 45d sem compra · cupom SAIBAIRECOMPRA (mín. R$120)",
                "⚠ Desligar e-mail nativo de checkout abandonado se a automação Shopify Email estiver ON (evita duplicata)",
            ],
        ),
        (
            "3. Recuperação nativa checkout",
            [
                f"Abra {ADMIN}/settings/checkout",
                "Checkout abandonado: se Shopify Email Abandoned checkout = ON → desligar e-mail padrão Shopify",
                "Se Shopify Email ainda não estiver ativo: ligar e-mail nativo de checkout abandonado (10h)",
            ],
        ),
        (
            "4. Remarketing (pixel nativo canal Meta)",
            [
                f"Canal Meta: {ADMIN}/marketing/channels/facebook → Pixel 2017630342068049",
                "Ads Manager → Audiências (pixel Shopify, NÃO pixel do tema):",
                "  · Visitantes 30d (PageView)",
                "  · ViewContent 14d",
                "  · AddToCart 7d",
                "  · InitiateCheckout 7d",
                "  · Purchase 180d (exclusão)",
                "Campanha [SAIBAI][RMKT][D2C][ATC] só após aprovação (APPROVAL_REQUESTS SB-M-004)",
                "Google remarketing: BLOQUEADO até MCC 9513237350",
            ],
        ),
        (
            "5. Tracking — não mexer",
            [
                "Theme Settings → Saibai Tracking → IDs GA4/Meta VAZIOS",
                "Browser = canais Shopify · sem Klaviyo pixel · sem GTM extra",
            ],
        ),
    ]
    for title, items in steps:
        print(title)
        for item in items:
            print(f"  · {item}")
        print()


def main() -> int:
    print("=== Saibai CRM nativo Shopify ===\n")
    print("1. Descontos atuais")
    rows = list_code_discounts()
    for row in rows:
        codes = ", ".join(row.get("codes") or ["—"])
        pct = row.get("percentage")
        pct_s = f" {int(pct * 100)}%" if isinstance(pct, (int, float)) else ""
        print(f"  · {row.get('status')} | {row.get('title')} | {codes}{pct_s}")

    print("\n2. Garantir cupons CRM")
    created = 0
    for spec in CODES:
        existing = find_code(rows, spec["code"])
        if existing and existing.get("status") == "ACTIVE":
            print(f"  · já ativo {spec['code']} ({existing.get('title')}) — {spec['usage']}")
            continue
        if existing and existing.get("status") != "ACTIVE":
            print(f"  ⚠ {spec['code']} existe como {existing.get('status')} — reative no Admin, não duplicar")
            continue
        if create_code(spec):
            created += 1

    leftover = find_code(rows, "PAIZAO6%")
    if leftover and leftover.get("status") == "ACTIVE":
        print("  ⚠ PAIZAO6% ainda ACTIVE (campanha Dia dos Pais) — expirar no Admin se a ação acabou")

    vip = find_code(rows, "CLIENTEVIPSAIBAI")
    if vip:
        print("  · CLIENTEVIPSAIBAI 10% mantido (VIP — não misturar com welcome/recompra)")

    print_admin_checklist()
    print("Doc: clients/saibai/docs/CRM-NATIVO-SHOPIFY-SAIBAI.md")
    print(f"Cupons novos nesta execução: {created}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
