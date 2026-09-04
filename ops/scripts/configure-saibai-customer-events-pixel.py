#!/usr/bin/env python3
"""Gera pixel Customer Events Saibai (purchase GA4 + Meta) a partir do settings_data."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = ROOT.parent / "theme" / "config" / "settings_data.json"
TEMPLATE_PATH = ROOT / "scripts" / "saibai-customer-events-pixel.js"
OUTPUT_PATH = ROOT / "scripts" / "saibai-customer-events-pixel.generated.js"

DEFAULT_GA4 = "G-VWX77SGD1W"
DEFAULT_META = "2017630342068049"
# IDs do canal Shopify — NÃO espelhar em Theme Settings → Saibai Tracking (dedupe)


def load_settings() -> dict:
    text = SETTINGS_PATH.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    data = json.loads(text)
    return data.get("current", {})


def main() -> None:
    settings = load_settings()
    ga4 = (settings.get("ga4_measurement_id") or "").strip() or DEFAULT_GA4
    meta = (settings.get("meta_pixel_id") or "").strip() or DEFAULT_META

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    pixel = template.replace("{{GA4_MEASUREMENT_ID}}", ga4).replace("{{META_PIXEL_ID}}", meta)
    OUTPUT_PATH.write_text(pixel, encoding="utf-8")

    print("✓ Pixel gerado:", OUTPUT_PATH.relative_to(ROOT))
    print(f"  GA4:  {ga4}")
    print(f"  Meta: {meta}")
    print()
    print("Instalação manual (Customer Events):")
    print("  1. Admin → Configurações → Eventos do cliente")
    print("  2. Adicionar pixel personalizado → Nome: Saibai Veltrus Checkout Events")
    print("  3. Permissões: Análise + Marketing → Conectar")
    print("  4. Colar o conteúdo de scripts/saibai-customer-events-pixel.generated.js")
    print("  5. Salvar → testar checkout em modo de teste do pixel")
    print()
    print("Eventos: checkout_started, checkout_completed (purchase), product_added_to_cart")


if __name__ == "__main__":
    main()
