#!/usr/bin/env python3
"""Checklist martech Saibai — limpeza, dedupe e instalações pendentes."""

STORE = "byinbz-0k.myshopify.com"
THEME_ID = "186124239166"
GA4 = "G-VWX77SGD1W"
META = "2017630342068049"

LINKS = {
    "apps": f"https://admin.shopify.com/store/emporiosaibai/settings/apps",
    "discounts": f"https://admin.shopify.com/store/emporiosaibai/discounts",
    "customer_events": f"https://admin.shopify.com/store/emporiosaibai/settings/customer_events",
    "google_channel": f"https://admin.shopify.com/store/emporiosaibai/marketing/channels/google",
    "meta_channel": f"https://admin.shopify.com/store/emporiosaibai/marketing/channels/facebook",
    "theme_apps": f"https://admin.shopify.com/store/emporiosaibai/themes/{THEME_ID}/editor?context=apps",
    "theme_tracking": f"https://admin.shopify.com/store/emporiosaibai/themes/{THEME_ID}/editor?context=settings",
}

CHECKLIST = """
MARTECH SAIBAI — CHECKLIST VELTRUS
==================================

REMOVER AGORA
-------------
[ ] Microsoft Clarity
    Admin → Configurações → Apps → Microsoft Clarity → Desinstalar
    {apps}

[ ] App embeds Clarity (se aparecer após instalação)
    Theme Editor → App embeds → DESLIGAR Clarity JS + Clarity Agents JS
    {theme_apps}

[ ] Desconto automático órfão "Discount" (EXPIRED)
    ✓ Removido via API (DiscountAutomaticNode/1561238995262)

CONFIGURAR (sem instalar apps novos)
------------------------------------
[ ] Eventos do cliente → Pixel personalizado
    {customer_events}
    - Se "shopify-custom-pixel" estiver VAZIO: colar scripts/saibai-customer-events-pixel.generated.js
    - Nome: Saibai Veltrus Checkout Events
    - Permissões: Análise + Marketing
    - Se canais Google/Meta já disparam purchase no checkout: desative UM dos lados (canal OU pixel)

[ ] Theme Settings → Saibai Tracking
    {theme_tracking}
    ✓ meta_pixel_id e ga4_measurement_id devem ficar VAZIOS (anti-duplicata com canais)

[ ] Canais Google & Meta
    Google: {google_channel}  → GA4 {ga4}
    Meta:   {meta_channel}    → Pixel {meta}
    Consent Mode v2: banner LGPD do tema atualiza gtag antes dos canais carregarem

[ ] Stape — auditar container GTM server
    - GA4/Meta browser tags: NÃO re-disparar se canais Shopify já ativos
    - Stape deve fazer: server-side GA4 + Meta CAPI + dedupe event_id
    - Desligar tags browser duplicadas no container web vinculado

INSTALAR (somente com aprovação do cliente)
-------------------------------------------
[ ] TinySEO → JSON-LD (6 tipos) + broken links → App embeds ON
[ ] Shopify Email → Welcome + abandoned cart + abandoned checkout + win-back
    → Playbook: docs/CRM-NATIVO-SHOPIFY-SAIBAI.md
    → Cupons LIVE: 5%NOVOCLIENTE · SAIBAIRECOMPRA
    → NÃO instalar Klaviyo nesta fase (tracking nativo)
[ ] Judge.me (vs Loox) → depois desativar fallback Loox em snippets/product-review-rating.liquid

GERAR PIXEL CHECKOUT
--------------------
  python3 scripts/configure-saibai-customer-events-pixel.py

VALIDAÇÃO PÓS-DEPLOY
--------------------
  grep -E "meta_pixel_id|ga4_measurement_id" config/settings_data.json
  # valores devem ser "" (vazios)

  # No navegador (após consentimento):
  # - 1 tag GA4 no storefront (canal Google)
  # - 1 fbq no storefront (canal Meta)
  # - purchase só no checkout (pixel custom OU canal, não ambos)
""".format(
    **LINKS,
    ga4=GA4,
    meta=META,
)


def main() -> None:
    print(CHECKLIST)


if __name__ == "__main__":
    main()
