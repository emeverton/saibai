#!/usr/bin/env python3
"""Checklist + deep-link helper for App Embeds Saibai (Theme Editor)."""

THEME_ID = "186124239166"
STORE = "byinbz-0k.myshopify.com"
EDITOR = f"https://admin.shopify.com/store/emporiosaibai/themes/{THEME_ID}/editor?context=apps"

RECOMMENDED = """
App embeds — padrão Veltrus Saibai
=================================

Abra: {editor}

LIGAR (ON):
  TinySEO — Article JSON-LD
  TinySEO — Breadcrumb JSON-LD
  TinySEO — Collection JSON-LD
  TinySEO — Product JSON-LD
  TinySEO — Store JSON-LD
  TinySEO — Website JSON-LD
  TinySEO — Broken link detection
  Judge.me — preview badge / widgets (após instalar Judge.me)
  Stape — Conversion Tracking (se container Stape configurado)
  Avada Order Limit — se regra de pedido mínimo/máximo ativa

DESLIGAR (OFF):
  Microsoft Clarity — Clarity JS
  Microsoft Clarity — Clarity Agents JS
  (desinstalar app Clarity em Admin → Apps antes de desligar embeds)

KLAVIYO:
  Instalar app → sync Shopify → fluxos no dashboard Klaviyo
  Form footer Saibai pode coexistir; evitar double opt-in conflitante

Instalação completa:
  python3 scripts/optimize-saibai-apps-install.py

Após ligar, clique SALVAR no editor.
Depois rode:
  shopify theme pull --theme {theme_id} --only config/settings_data.json
  grep -c '"blocks"' config/settings_data.json

Os block IDs são gerados pelo Shopify na primeira ativação — não editar manualmente.
""".format(editor=EDITOR, theme_id=THEME_ID)

if __name__ == "__main__":
    print(RECOMMENDED)
