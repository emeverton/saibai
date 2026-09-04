# Empório Saibai — Prompt Novo Chat v1

**Atualizado:** 2026-06-25

## Prompt de abertura

```txt
Modo: Empório Saibai Ops v1 — Veltrus.

Cliente: Empório Saibai (saibai)
Negócio: produtora alcachofras Piedade SP · D2C Shopify + B2B WhatsApp
Plataforma: Shopify (NÃO Tray)
Dossiê: clients/saibai/
Skill: saibai-company-expert

IDs:
- GA4: G-VWX77SGD1W (property MCP pending)
- Meta: act_1199864388174624 · pixel 2017630342068049
- Google: 9513237350 (MCC pending)
- Shopify: byinbz-0k.myshopify.com · tema 186124239166
- Loja: emporiosaibai.com.br

Estado jun/2026:
- Tema v1.2.4: LIVE PASS
- Tracking Vercel+CAPI: código PASS · manual PRECISA HOTFIX
- Meta: 1 ACTIVE (LEADS-GRUPO-WHATS R$20/d) · conv. plataforma infladas
- Google: gateway 500 · MCC não linked
- GA4 MCP: property fora do acesso Veltrus

Regras:
- Somente leitura até aprovação
- Mutations: APPROVAL_REQUESTS.md
- KPI e-com: GA4 purchase
- Theme Settings → Saibai Tracking → IDs VAZIOS (anti-duplicata)
- Nunca duplicar purchase checkout

Próximo P0: CHECKLIST_MANUAL_SAIBAI.md seção 1
```

## Validação MCP inicial

1. `meta_ads_get_campaigns` adAccountId=act_1199864388174624
2. `meta_ads_build_client_report` (jun/2026)
3. `google_ads_get_campaigns` customerId=9513237350 (após MCC)
4. `ga4_list_properties` → confirmar Saibai aparece

## Vereditos esperados

| Área | Veredito |
|------|----------|
| Tema Shopify | PASS |
| Tracking go-live | PRECISA HOTFIX |
| Meta MCP | PASS |
| Google | PENDING_PERMISSION |
| GA4 | PENDING_ACCESS |
| Dossiê | PASS |
