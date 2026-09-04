#!/usr/bin/env python3
"""
Instalação apps Saibai — TinySEO, Shopify Email, Judge.me + remoção Clarity.

A Shopify CLI NÃO instala apps de terceiros (sem read_apps / OAuth App Store).
Este script imprime ordem, links e pós-configuração.
"""

STORE_ADMIN = "https://admin.shopify.com/store/emporiosaibai"
THEME_ID = "186124239166"
EDITOR_APPS = f"{STORE_ADMIN}/themes/{THEME_ID}/editor?context=apps"
APPS_SETTINGS = f"{STORE_ADMIN}/settings/apps"

# App Store → instalar (abrir logado no admin emporiosaibai)
INSTALL_URLS = {
    "TinySEO": "https://apps.shopify.com/smart-image-optimizer",
    "ShopifyEmail": "https://admin.shopify.com/store/emporiosaibai/marketing/automations",
    "Judge.me": "https://apps.shopify.com/judgeme",
}

ORDER = [
    {
        "step": 0,
        "title": "Desinstalar Microsoft Clarity (obrigatório antes)",
        "manual": True,
        "why": "Duplica heatmap com GA4/Meta; sem escopo apps na CLI.",
        "actions": [
            f"Abra {APPS_SETTINGS}",
            "Microsoft Clarity → Desinstalar (ou ⋯ → Delete app)",
            f"Depois: {EDITOR_APPS}",
            "App embeds → DESLIGAR «Clarity JS» e «Clarity Agents JS» se ainda aparecerem",
            "Salvar tema",
        ],
    },
    {
        "step": 1,
        "title": "TinySEO (primeiro — SEO + JSON-LD, zero conflito tracking)",
        "manual": True,
        "install": INSTALL_URLS["TinySEO"],
        "why": "Rich snippets + broken links; não mexe em e-mail nem reviews.",
        "actions": [
            f"Instalar: {INSTALL_URLS['TinySEO']}",
            "Plano: comece Free (1500 imgs/mês) ou Pro se catálogo grande",
            f"Theme Editor → App embeds: {EDITOR_APPS}",
            "LIGAR os 7 embeds TinySEO:",
            "  · Article JSON-LD",
            "  · Breadcrumb JSON-LD",
            "  · Collection JSON-LD",
            "  · Product JSON-LD",
            "  · Store JSON-LD",
            "  · Website JSON-LD",
            "  · Broken link detection",
            "Salvar tema → Google Search Console → validar Rich Results em 1 produto",
            "⚠ Desligar JSON-LD duplicado se outro app SEO existir",
        ],
    },
    {
        "step": 2,
        "title": "Judge.me (segundo — reviews + estrelas no Google)",
        "manual": True,
        "install": INSTALL_URLS["Judge.me"],
        "why": "Popula metafield padrão reviews.rating (já lido pelo tema).",
        "actions": [
            f"Instalar: {INSTALL_URLS['Judge.me']}",
            "Plano: Awesome (free tier) ou superior conforme volume",
            "Judge.me → Settings → Shopify integration → Sync ON",
            "Widget: Star rating + Review widget na PDP (template product Saibai)",
            "Importar reviews existentes (se houver Loox/outro)",
            "Theme Editor → App embeds → Judge.me preview badge ON (se disponível)",
            "Após 1ª review sincronizada: avisar Veltrus para remover fallback Loox no tema",
            "Validar: card produto + schema aggregateRating no JSON-LD",
        ],
    },
    {
        "step": 3,
        "title": "Shopify Email (nativo — e-mail + recuperação). Klaviyo adiado.",
        "manual": True,
        "install": INSTALL_URLS["ShopifyEmail"],
        "why": "CRM nativo usa o mesmo pixel/canais Shopify. Sem app terceiro, sem pixel extra.",
        "actions": [
            f"Automações: {INSTALL_URLS['ShopifyEmail']}",
            "Remetente contato@saibai.com.br · Empório Saibai",
            "Welcome · 5%NOVOCLIENTE (newsletter tag)",
            "Abandoned cart 1h · unique 5% 48h",
            "Abandoned checkout 10h · unique 5% 48h (desligar e-mail nativo se esta automação ON)",
            "Post-purchase +3d · conservas (sem cupom)",
            "Win-back 45d · SAIBAIRECOMPRA (mín. R$120)",
            "Playbook: docs/CRM-NATIVO-SHOPIFY-SAIBAI.md",
            "⚠ Não instalar Klaviyo nesta fase — duplicaria e-mail e pode injetar pixel",
        ],
    },
]


def print_header() -> None:
    print("=== Saibai — Instalação Apps (manual Admin) ===\n")
    print("A CLI não instala apps de terceiros (ACCESS_DENIED em appInstallations).")
    print("Siga a ordem abaixo no browser logado como admin emporiosaibai.\n")
    print(f"Apps:     {APPS_SETTINGS}")
    print(f"Embeds:   {EDITOR_APPS}\n")


def print_order() -> None:
    for block in ORDER:
        print(f"{'─' * 60}")
        print(f"Passo {block['step']}: {block['title']}")
        if block.get("why"):
            print(f"  Por quê: {block['why']}")
        if block.get("install"):
            print(f"  Instalar: {block['install']}")
        for action in block["actions"]:
            print(f"  · {action}")
        print()


def print_recommendation() -> None:
    print("=" * 60)
    print("RECOMENDAÇÃO VELOTRUS")
    print("=" * 60)
    print("""
Pode instalar os 3 na mesma sessão (App Store), mas CONFIGURE nesta ordem:

  0. Clarity OFF     → evita script duplicado
  1. TinySEO         → JSON-LD + links quebrados (15 min)
  2. Judge.me        → reviews na PDP + rich snippets (30 min)
  3. Shopify Email   → Welcome + cart + checkout + win-back (30–45 min)

Se quiser só UM primeiro: TinySEO (impacto SEO imediato, menor risco).

Após cada app + embeds ON, rode:
  python3 scripts/saibai-app-embeds-checklist.py

Tema já preparado:
  · snippets/product-review-rating.liquid → lê reviews.rating (Judge.me)
  · Banner LGPD Saibai → não conflita com apps
  · Theme Settings tracking vazio → anti-duplicata GA4/Meta
  · Cupons 5%NOVOCLIENTE + SAIBAIRECOMPRA LIVE
""")


def print_validation() -> None:
    print("Validação pós-instalação:")
    checks = [
        "View-source PDP → 1 bloco JSON-LD Product (TinySEO, sem duplicata tema)",
        "Judge.me → estrelas visíveis em 1 produto com review",
        "Shopify Email → teste Welcome no e-mail próprio com 5%NOVOCLIENTE",
        "Network tab → sem clarity.ms após desinstalar Clarity",
        "DevTools → 1 GA4 + 1 Meta browser (canais nativos, sem pixel tema)",
    ]
    for c in checks:
        print(f"  ☐ {c}")
    print()


def main() -> int:
    print_header()
    print_order()
    print_recommendation()
    print_validation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
