#!/usr/bin/env python3
"""Aplica branding KV Saibai no checkout via Admin API."""

import json
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"
PROFILE_ID = "gid://shopify/CheckoutProfile/5598216510"

BRANDING_INPUT = {
    "designSystem": {
        "colors": {
            "schemes": {
                "scheme1": {
                    "base": {
                        "background": "#F4F9F0",
                        "text": "#2A3A1A",
                        "border": "#E2EDDA",
                        "icon": "#4E6040",
                        "accent": "#76BD22",
                        "decorative": "#E8F5D4",
                    },
                    "control": {
                        "background": "#FFFFFF",
                        "text": "#2A3A1A",
                        "border": "#E2EDDA",
                        "accent": "#76BD22",
                        "selected": {
                            "background": "#E8F5D4",
                            "text": "#2A3A1A",
                            "border": "#76BD22",
                            "accent": "#5A9018",
                        },
                    },
                    "primaryButton": {
                        "background": "#76BD22",
                        "text": "#FFFFFF",
                        "border": "#76BD22",
                        "hover": {
                            "background": "#5A9018",
                            "text": "#FFFFFF",
                            "border": "#5A9018",
                        },
                    },
                    "secondaryButton": {
                        "background": "rgba(0,0,0,0)",
                        "text": "#3D2B1F",
                        "border": "#E2EDDA",
                        "hover": {
                            "background": "#E8F5D4",
                            "text": "#2A3A1A",
                            "border": "#76BD22",
                        },
                    },
                }
            }
        },
        "typography": {
            "size": {"base": 16, "ratio": 1.2},
            "primary": {
                "shopifyFontGroup": {
                    "name": "Jost",
                    "baseWeight": 400,
                    "boldWeight": 600,
                    "loadingStrategy": "SWAP",
                }
            },
            "secondary": {
                "shopifyFontGroup": {
                    "name": "Jost",
                    "baseWeight": 400,
                    "boldWeight": 600,
                    "loadingStrategy": "SWAP",
                }
            },
        },
        "cornerRadius": {"small": 4, "base": 4, "large": 4},
    },
    "customizations": {
        "global": {"cornerRadius": "NONE"},
        "control": {"cornerRadius": "SMALL", "labelPosition": "OUTSIDE"},
        "primaryButton": {"cornerRadius": "SMALL"},
    },
}

UPSERT = """
mutation upsertBranding($profileId: ID!, $input: CheckoutBrandingInput!) {
  checkoutBrandingUpsert(checkoutProfileId: $profileId, checkoutBrandingInput: $input) {
    checkoutBranding {
      designSystem {
        colors { schemes { scheme1 { base { accent background text } } } }
      }
    }
    userErrors { field message }
  }
}
"""

CONFIG_QUERY = """
query {
  checkoutAndAccountsConfigurations(first: 5) {
    nodes { id name isPublished }
  }
}
"""

CONFIG_MUTATION = """
mutation updateBranding($id: ID!, $config: CheckoutAndAccountsConfigurationInput!) {
  checkoutAndAccountsConfigurationUpdate(id: $id, configuration: $config) {
    configuration { id name isPublished }
    userErrors { field message }
  }
}
"""

PALETTE = {
    "color1": "#FFFFFF",
    "color2": "#F4F9F0",
    "color3": "#E8F5D4",
    "color4": "#76BD22",
    "color5": "#5A9018",
    "color6": "#2A3A1A",
    "color7": "#4E6040",
    "color8": "#3D2B1F",
    "color9": "#E2EDDA",
    "color10": "#FFFFFF",
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


def try_branding_upsert() -> bool:
    print("→ checkoutBrandingUpsert (CheckoutProfile)...")
    try:
        r = gql(UPSERT, {"profileId": PROFILE_ID, "input": BRANDING_INPUT})
    except RuntimeError as e:
        msg = str(e)
        if "Plus plan" in msg or "ACCESS_DENIED" in msg:
            print("  ⚠ Plano Basic/Shopify — branding via API requer Plus ou editor manual")
        else:
            print(f"  ✗ {msg[:500]}")
        return False

    payload = r.get("checkoutBrandingUpsert", {})
    errs = payload.get("userErrors", [])
    if errs:
        print("  userErrors:", json.dumps(errs, indent=2, ensure_ascii=False))
        return False

    colors = (
        payload.get("checkoutBranding", {})
        .get("designSystem", {})
        .get("colors", {})
    )
    print(f"  ✓ Branding aplicado via CheckoutProfile")
    print(f"    accent={colors}")
    return True


def try_accounts_config() -> bool:
    print("→ checkoutAndAccountsConfigurationUpdate...")
    try:
        data = gql(CONFIG_QUERY)
    except RuntimeError as e:
        if "ACCESS_DENIED" in str(e):
            print("  ⚠ Escopo write_checkout_and_accounts_configurations ausente")
        return False

    nodes = data.get("checkoutAndAccountsConfigurations", {}).get("nodes", [])
    if not nodes:
        return False

    config_id = next((n["id"] for n in nodes if n.get("isPublished")), nodes[0]["id"])
    variables = {
        "id": config_id,
        "config": {
            "branding": {
                "designTokens": {
                    "colors": {"palette": PALETTE},
                    "cornerRadius": {"small": 4, "base": 4, "large": 4},
                    "typography": {
                        "primary": {"name": "Jost", "loadingStrategy": "SWAP"},
                        "secondary": {"name": "Jost", "loadingStrategy": "SWAP"},
                    },
                },
                "customizations": {
                    "global": {"cornerRadius": "NONE"},
                    "control": {"cornerRadius": "SMALL", "labelPosition": "OUTSIDE"},
                    "primaryButton": {"cornerRadius": "SMALL"},
                },
            }
        },
    }

    try:
        r = gql(CONFIG_MUTATION, variables)
    except RuntimeError:
        return False

    payload = r.get("checkoutAndAccountsConfigurationUpdate", {})
    errs = payload.get("userErrors", [])
    if errs:
        print("  userErrors:", json.dumps(errs, indent=2, ensure_ascii=False))
        return False

    cfg = payload.get("configuration", {})
    print(f"  ✓ Contas/checkout config: {cfg.get('name')}")
    return True


def main() -> int:
    if try_branding_upsert():
        try_accounts_config()
        return 0

    if try_accounts_config():
        return 0

    print("\nFalhou. Aprove a reauth no browser e rode:")
    print("  bash scripts/shopify-auth-full.sh")
    return 1


if __name__ == "__main__":
    sys.exit(main())
