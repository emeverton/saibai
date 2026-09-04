#!/usr/bin/env python3
"""Custom Data Saibai 10/10 — metafields + metaobjects (/settings/custom_data)."""

import json
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

STORE = "byinbz-0k.myshopify.com"
ORIGEM = "Piedade, SP — produção própria Empório Saibai"
GOOGLE_CAT = "5798"

MO = {
    "food_outro": "gid://shopify/Metaobject/112745677118",
}

# Definições Saibai (namespace custom + Google)
CREATE_DEFINITIONS = [
    {
        "ownerType": "PRODUCT",
        "namespace": "custom",
        "key": "custom_badge",
        "name": "Selo do produto",
        "type": "single_line_text_field",
        "description": "Ex.: Safra 2026, Novo, Edição limitada. Exibido no card e na galeria.",
        "pin": True,
        "access": {"storefront": "PUBLIC_READ"},
    },
    {
        "ownerType": "PRODUCT",
        "namespace": "custom",
        "key": "custom_tab",
        "name": "Aba personalizada (PDP)",
        "type": "multi_line_text_field",
        "description": "Conteúdo da aba Custom na página do produto.",
        "pin": True,
        "access": {"storefront": "PUBLIC_READ"},
    },
    {
        "ownerType": "PRODUCT",
        "namespace": "custom",
        "key": "short_description",
        "name": "Descrição curta (card)",
        "type": "multi_line_text_field",
        "description": "Resumo exibido nos cards de produto e comparador.",
        "pin": True,
        "access": {"storefront": "PUBLIC_READ"},
    },
    {
        "ownerType": "PRODUCT",
        "namespace": "custom",
        "key": "origem",
        "name": "Origem / procedência",
        "type": "single_line_text_field",
        "description": "Procedência do produto (campo Saibai).",
        "pin": False,
        "access": {"storefront": "PUBLIC_READ"},
    },
    {
        "ownerType": "PRODUCT",
        "namespace": "custom",
        "key": "conservacao",
        "name": "Conservação",
        "type": "single_line_text_field",
        "description": "Instruções de armazenamento e validade.",
        "pin": False,
        "access": {"storefront": "PUBLIC_READ"},
    },
]

# Fashion/demo — irrelevante para food Saibai
DELETE_DEFINITION_KEYS = [
    ("shopify", "color-pattern"),
    ("shopify", "material"),
    ("shopify", "target-gender"),
]

PIN_DEFINITION_KEYS = [
    ("custom", "descri_o_do_produto"),
    ("custom", "custom_badge"),
    ("custom", "short_description"),
]


def gql(query: str, variables: Optional[Dict[str, Any]] = None, soft: bool = False) -> dict:
    cmd = [
        "shopify", "store", "execute", "-s", STORE,
        "--allow-mutations", "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    try:
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        if soft:
            return {"userErrors": [{"message": (e.output or str(e))[:200]}]}
        raise
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:300]}")
    return json.loads(out[start:])


def fetch_product_definitions() -> Dict[Tuple[str, str], str]:
    q = """
    query {
      metafieldDefinitions(first: 50, ownerType: PRODUCT) {
        nodes { id namespace key name pinnedPosition }
      }
    }
    """
    r = gql(q)
    out: Dict[Tuple[str, str], str] = {}
    for node in r.get("metafieldDefinitions", {}).get("nodes", []):
        out[(node["namespace"], node["key"])] = node["id"]
    return out


def create_definitions(existing: Dict[Tuple[str, str], str]) -> int:
    q = """
    mutation createDef($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition { id name namespace key }
        userErrors { field message }
      }
    }
    """
    ok = 0
    for spec in CREATE_DEFINITIONS:
        key = (spec["namespace"], spec["key"])
        if key in existing:
            print(f"  · {spec['namespace']}.{spec['key']} (já existe)")
            continue
        definition = {
            "ownerType": spec["ownerType"],
            "namespace": spec["namespace"],
            "key": spec["key"],
            "name": spec["name"],
            "type": spec["type"],
            "description": spec.get("description", ""),
            "pin": spec.get("pin", False),
        }
        if spec.get("access"):
            definition["access"] = spec["access"]
        r = gql(q, {"definition": definition})
        payload = r.get("metafieldDefinitionCreate", {})
        errs = payload.get("userErrors", [])
        if errs:
            print(f"  ✗ {spec['namespace']}.{spec['key']}: {errs[0]['message']}")
            continue
        created = payload.get("createdDefinition", {})
        print(f"  ✓ {created.get('namespace')}.{created.get('key')} — {created.get('name')}")
        existing[key] = created.get("id", "")
        ok += 1
        time.sleep(0.3)
    return ok


def delete_fashion_definitions(existing: Dict[Tuple[str, str], str]) -> int:
    q = """
    mutation deleteDef($id: ID!, $deleteAll: Boolean!) {
      metafieldDefinitionDelete(id: $id, deleteAllAssociatedMetafields: $deleteAll) {
        deletedDefinitionId
        userErrors { message }
      }
    }
    """
    ok = 0
    for ns, key in DELETE_DEFINITION_KEYS:
        def_id = existing.get((ns, key))
        if not def_id:
            print(f"  · {ns}.{key} (ausente)")
            continue
        r = gql(q, {"id": def_id, "deleteAll": True}, soft=True)
        errs = r.get("metafieldDefinitionDelete", {}).get("userErrors", [])
        if not errs and r.get("userErrors"):
            errs = r.get("userErrors", [])
        if errs:
            print(f"  ⚠ {ns}.{key}: {errs[0]['message'][:120]}")
            continue
        if r.get("metafieldDefinitionDelete", {}).get("deletedDefinitionId"):
            print(f"  ✓ removido {ns}.{key}")
            ok += 1
        else:
            print(f"  ⚠ {ns}.{key}: não removível (definição padrão Shopify)")
        time.sleep(0.3)
    return ok


def pin_definitions(existing: Dict[Tuple[str, str], str]) -> int:
    q = """
    mutation pinDef($definitionId: ID!) {
      metafieldDefinitionPin(definitionId: $definitionId) {
        pinnedDefinition { id }
        userErrors { message }
      }
    }
    """
    ok = 0
    for ns, key in PIN_DEFINITION_KEYS:
        def_id = existing.get((ns, key))
        if not def_id:
            continue
        r = gql(q, {"definitionId": def_id})
        errs = r.get("metafieldDefinitionPin", {}).get("userErrors", [])
        if errs:
            msg = errs[0]["message"]
            if "already pinned" in msg.lower() or "já" in msg.lower():
                print(f"  · {ns}.{key} (já fixado)")
            else:
                print(f"  ⚠ {ns}.{key}: {msg}")
            continue
        print(f"  ✓ fixado {ns}.{key}")
        ok += 1
        time.sleep(0.2)
    return ok


def fetch_active_products() -> List[Dict[str, Any]]:
    products: List[Dict[str, Any]] = []
    cursor = None
    while True:
        q = """
        query ($cursor: String) {
          products(first: 50, query: "status:active", after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id handle title productType
              metafields(first: 25) {
                nodes { namespace key value }
              }
            }
          }
        }
        """
        r = gql(q, {"cursor": cursor})
        conn = r.get("products", {})
        products.extend(conn.get("nodes", []))
        if not conn.get("pageInfo", {}).get("hasNextPage"):
            break
        cursor = conn["pageInfo"]["endCursor"]
    return products


def mf_value(product: Dict[str, Any], namespace: str, key: str) -> str:
    for m in product.get("metafields", {}).get("nodes", []):
        if m["namespace"] == namespace and m["key"] == key:
            return m.get("value") or ""
    return ""


def badge_for(handle: str) -> str:
    if "alcachofra-p" in handle or "alcachofra-mini" in handle or "fresca" in handle:
        return "Safra 2026"
    if "chaveiro" in handle:
        return "Edição limitada"
    return ""


def conservacao_for(handle: str, product_type: str) -> str:
    ptype = (product_type or "").lower()
    h = handle.lower()
    if "conserva" in h or "conservas" in ptype:
        return "Local seco, ao abrigo da luz. Após aberto, refrigerar e consumir em até 3 dias."
    if "desidrat" in h or "desidrat" in ptype or "flores" in ptype:
        return "Local fresco, seco, ao abrigo da luz. Após aberto, consumir em até 30 dias."
    if "alcachofra" in h:
        return "Refrigerar imediatamente. Consumir em até 5 dias após recebimento."
    return "Consulte informações no rótulo."


def custom_tab_for(handle: str, product_type: str) -> str:
    h = handle.lower()
    ptype = (product_type or "").lower()
    if "conserva" in h:
        return (
            "Conservas artesanais Saibai — produção própria em Piedade, SP.\n"
            "Após abrir, transferir para recipiente limpo, refrigerar e consumir em até 3 dias.\n"
            "Ideal para antepastos, risotos, massas e pratos gourmet."
        )
    if "alcachofra-p" in h or "alcachofra-mini" in h:
        return (
            "Alcachofra fresca colhida na safra Saibai, Piedade/SP.\n"
            "Refrigere imediatamente ao receber. Consuma em até 5 dias.\n"
            "Envio com embalagem térmica para preservar qualidade."
        )
    if "desidrat" in h or "desidrat" in ptype:
        return (
            "Frutas desidratadas 100% naturais, sem conservantes artificiais.\n"
            "Mantenha em local fresco, seco e ao abrigo da luz direta."
        )
    if "flores" in ptype:
        return "Flores comestíveis desidratadas para gastronomia e decoração. Uso ornamental e culinário."
    if "chaveiro" in h:
        return "Chaveiro exclusivo Empório Saibai. Metal esmaltado, acabamento premium. Edição limitada."
    return "Produto Empório Saibai — produção própria em Piedade, SP, Capital Nacional da Alcachofra."


def build_product_metafields(product: Dict[str, Any]) -> List[Dict[str, str]]:
    handle = product.get("handle", "")
    ptype = product.get("productType", "")
    pid = product["id"]
    summary = mf_value(product, "custom", "descri_o_do_produto") or product.get("title", "")

    fields: List[Dict[str, str]] = [
        {"ownerId": pid, "namespace": "custom", "key": "origem", "type": "single_line_text_field", "value": ORIGEM},
        {
            "ownerId": pid,
            "namespace": "custom",
            "key": "conservacao",
            "type": "single_line_text_field",
            "value": conservacao_for(handle, ptype),
        },
        {
            "ownerId": pid,
            "namespace": "custom",
            "key": "short_description",
            "type": "multi_line_text_field",
            "value": summary,
        },
    ]

    badge = badge_for(handle)
    if badge:
        fields.append({
            "ownerId": pid, "namespace": "custom", "key": "custom_badge",
            "type": "single_line_text_field", "value": badge,
        })

    tab = custom_tab_for(handle, ptype)
    fields.append({
        "ownerId": pid, "namespace": "custom", "key": "custom_tab",
        "type": "multi_line_text_field", "value": tab,
    })

    return fields


def metafields_set_batch(metafields: List[Dict[str, str]]) -> Tuple[int, int]:
    q = """
    mutation setMf($metafields: [MetafieldsSetInput!]!) {
      metafieldsSet(metafields: $metafields) {
        metafields { key namespace }
        userErrors { field message }
      }
    }
    """
    ok = 0
    err = 0
    for mf in metafields:
        r = gql(q, {"metafields": [mf]}, soft=True)
        payload = r.get("metafieldsSet", {})
        user_errs = payload.get("userErrors", [])
        if user_errs:
            err += 1
            if err <= 3:
                print(f"  ⚠ {mf.get('namespace')}.{mf.get('key')} ({mf.get('ownerId', '')[-6:]}): {user_errs[0]['message'][:100]}")
        elif payload.get("metafields"):
            ok += 1
        time.sleep(0.15)
    return ok, err


def audit() -> None:
    defs = fetch_product_definitions()
    saibai_keys = [
        "custom_badge", "custom_tab", "short_description", "origem",
        "conservacao", "descri_o_do_produto", "google_product_category",
        "dietary-preferences", "food-product-form", "cooking-method",
    ]
    print("\n  Definições PRODUCT (Saibai-relevantes):")
    for ns, key in sorted(defs.keys()):
        if ns in ("custom", "shopify", "mm-google-shopping", "shopify--discovery--product_search_boost", "shopify--discovery--product_recommendation"):
            if key in saibai_keys or ns == "custom" or "discovery" in ns or ns == "mm-google-shopping":
                print(f"    ✓ {ns}.{key}")
    missing_fashion = [f"{ns}.{k}" for ns, k in DELETE_DEFINITION_KEYS if (ns, k) in defs]
    if missing_fashion:
        print(f"  ⚠ Fashion ainda presente: {', '.join(missing_fashion)}")
    else:
        print("  ✓ Fashion (color/material/gender) removido")

    products = fetch_active_products()
    with_badge = sum(1 for p in products if mf_value(p, "custom", "custom_badge"))
    with_short = sum(1 for p in products if mf_value(p, "custom", "short_description"))
    with_food = sum(1 for p in products if mf_value(p, "shopify", "food-product-form") or "chaveiro" in p["handle"])
    print(f"\n  Produtos ativos: {len(products)}")
    print(f"  · com selo (custom_badge): {with_badge}")
    print(f"  · com descrição curta: {with_short}")
    print(f"  · com ficha alimento / N/A chaveiro: {with_food}/{len(products)}")


def main() -> int:
    print("=== Saibai Custom Data 10/10 ===\n")

    print("1. Definições de metafield (PRODUCT)")
    existing = fetch_product_definitions()
    created = create_definitions(existing)
    existing = fetch_product_definitions()

    print("\n2. Definições fashion (color/material/gender)")
    print("  · Padrão Shopify — oculte no admin se não usar (não removível via API)")

    print("\n3. Fixar definições no admin (pinned)")
    pinned = pin_definitions(existing)

    print("\n4. Popular metafields nos produtos ativos")
    products = fetch_active_products()
    all_mfs: List[Dict[str, str]] = []
    for p in products:
        all_mfs.extend(build_product_metafields(p))
    ok, errs = metafields_set_batch(all_mfs)
    print(f"  ✓ {ok} metafields gravados ({len(products)} produtos, {errs} erros)")

    print("\n5. Auditoria")
    audit()

    print(f"\nAdmin: https://admin.shopify.com/store/emporiosaibai/settings/custom_data")
    print("=== Concluído ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
