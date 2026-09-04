#!/usr/bin/env python3
"""Configurações Saibai via Admin API — frete, políticas, e-mail (quando possível)."""

import json
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"

# E-mail canônico Saibai (loja + contato cliente)
CANONICAL_EMAIL = "contato@saibai.com.br"

FREE_SHIPPING_DISCOUNT = {
    "title": "Frete grátis acima de R$389,90",
    "startsAt": "2025-01-01T00:00:00Z",
    "minimumSubtotal": "389.90",
}

# Políticas completas: python3 scripts/optimize-saibai-legal-policies.py
POLICY_UPDATES: list = []


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


def get_shop_emails() -> Dict[str, str]:
    r = gql("query { shop { email contactEmail } }")
    shop = r.get("shop", {})
    return {"email": shop.get("email", ""), "contactEmail": shop.get("contactEmail", "")}


def ensure_free_shipping_discount() -> bool:
    q_check = """
    query {
      discountNodes(first: 20, query: "type:free_shipping status:active") {
        nodes {
          id
          discount {
            ... on DiscountAutomaticFreeShipping {
              title
              minimumRequirement {
                ... on DiscountMinimumSubtotal {
                  greaterThanOrEqualToSubtotal { amount }
                }
              }
            }
          }
        }
      }
    }
    """
    r = gql(q_check)
    for node in r.get("discountNodes", {}).get("nodes", []):
        disc = node.get("discount", {})
        title = disc.get("title", "")
        min_req = disc.get("minimumRequirement", {}) or {}
        sub = min_req.get("greaterThanOrEqualToSubtotal", {}) or {}
        amount = str(sub.get("amount", "") or "")
        node_id = node.get("id")
        if amount in ("320.0", "320.00") or "320" in title:
            print(f"  · frete grátis R$320 já ativo ({title})")
            return True
        if amount in ("280.0", "280.00") or "280" in title:
            q_update = """
            mutation updateFreeShip($id: ID!, $input: DiscountAutomaticFreeShippingInput!) {
              discountAutomaticFreeShippingUpdate(id: $id, freeShippingAutomaticDiscount: $input) {
                automaticDiscountNode { id automaticDiscount { ... on DiscountAutomaticFreeShipping { title status } } }
                userErrors { field message }
              }
            }
            """
            variables = {
                "id": node_id,
                "input": {
                    "title": FREE_SHIPPING_DISCOUNT["title"],
                    "minimumRequirement": {
                        "subtotal": {
                            "greaterThanOrEqualToSubtotal": FREE_SHIPPING_DISCOUNT["minimumSubtotal"],
                        }
                    },
                },
            }
            ur = gql(q_update, variables)
            payload = ur.get("discountAutomaticFreeShippingUpdate", {})
            errs = payload.get("userErrors", [])
            if errs:
                print(f"  ✗ update frete grátis: {errs[0]['message']}")
                return False
            disc_u = payload.get("automaticDiscountNode", {}).get("automaticDiscount", {})
            print(f"  ✓ frete grátis atualizado 280→320: {disc_u.get('title')} ({disc_u.get('status')})")
            return True

    q_create = """
    mutation createFreeShip($input: DiscountAutomaticFreeShippingInput!) {
      discountAutomaticFreeShippingCreate(freeShippingAutomaticDiscount: $input) {
        automaticDiscountNode { id automaticDiscount { ... on DiscountAutomaticFreeShipping { title status } } }
        userErrors { field message }
      }
    }
    """
    variables = {
        "input": {
            "title": FREE_SHIPPING_DISCOUNT["title"],
            "startsAt": FREE_SHIPPING_DISCOUNT["startsAt"],
            "combinesWith": {
                "orderDiscounts": True,
                "productDiscounts": True,
                "shippingDiscounts": False,
            },
            "minimumRequirement": {
                "subtotal": {
                    "greaterThanOrEqualToSubtotal": FREE_SHIPPING_DISCOUNT["minimumSubtotal"],
                }
            },
            "destination": {"all": True},
        }
    }
    r = gql(q_create, variables)
    payload = r.get("discountAutomaticFreeShippingCreate", {})
    errs = payload.get("userErrors", [])
    if errs:
        print(f"  ✗ frete grátis: {errs[0]['message']}")
        return False
    disc = payload.get("automaticDiscountNode", {}).get("automaticDiscount", {})
    print(f"  ✓ desconto frete grátis criado: {disc.get('title')} ({disc.get('status')})")
    return True


def update_shop_policies() -> int:
    q = """
    mutation updatePolicy($policy: ShopPolicyInput!) {
      shopPolicyUpdate(shopPolicy: $policy) {
        shopPolicy { title url }
        userErrors { message }
      }
    }
    """
    ok = 0
    for policy in POLICY_UPDATES:
        r = gql(q, {"policy": {"type": policy["type"], "body": policy["body"]}})
        payload = r.get("shopPolicyUpdate", {})
        errs = payload.get("userErrors", [])
        if errs:
            print(f"  ⚠ {policy['type']}: {errs[0]['message']}")
            continue
        title = payload.get("shopPolicy", {}).get("title", policy["type"])
        print(f"  ✓ política {title}")
        ok += 1
    return ok


def report_delivery_profile() -> None:
    q = """
    query {
      deliveryProfiles(first: 5) {
        nodes { id name default }
      }
      locations(first: 5) {
        nodes { name fulfillsOnlineOrders isActive }
      }
    }
    """
    r = gql(q)
    profiles = r.get("deliveryProfiles", {}).get("nodes", [])
    locations = r.get("locations", {}).get("nodes", [])
    print("  Perfis de envio:")
    for p in profiles:
        flag = " (padrão)" if p.get("default") else ""
        print(f"    · {p['name']}{flag}")
    print("  Locais:")
    for loc in locations:
        status = "ativo" if loc.get("isActive") else "inativo"
        print(f"    · {loc['name']} — {status}, online={loc.get('fulfillsOnlineOrders')}")
    print("  Tarifas: Loggi + Frenet (calculadas por transportadora — OK para BR)")


def main() -> int:
    print("=== Saibai Config API ===\n")

    print("1. E-mail da loja")
    emails = get_shop_emails()
    print(f"  shop.email ........... {emails.get('email')}")
    print(f"  shop.contactEmail .... {emails.get('contactEmail')}")
    if emails.get("contactEmail") != CANONICAL_EMAIL:
        print(
            f"  ⚠ contactEmail diverge de {CANONICAL_EMAIL} — "
            "API não expõe shopUpdate; ajuste em Configurações → Geral → E-mail do cliente"
        )
    else:
        print("  ✓ e-mails alinhados")

    print("\n2. Frete grátis checkout (automático R$320)")
    ensure_free_shipping_discount()

    print("\n3. Políticas legais — rode: python3 scripts/optimize-saibai-legal-policies.py")
    if POLICY_UPDATES:
        update_shop_policies()

    print("\n4. Perfil de envio (auditoria)")
    report_delivery_profile()

    print("\n5. Theme settings — rode: python3 scripts/patch-saibai-settings.py")
    print("   Depois: shopify theme push --theme 186124239166 --allow-live --only config/settings_data.json")

    print("\n=== Concluído ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
