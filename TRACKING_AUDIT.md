# Empório Saibai — Auditoria de Tracking

**Atualizado:** 2026-06-25  
**Veredito:** **PRECISA AUDITORIA** — código deployado · go-live manual pendente

## Stack (não é GTM-primary)

| Camada | Componente | Status | Detalhe |
|--------|------------|--------|---------|
| Storefront browser | Canais Shopify Google/Meta | ⚠️ | Conectar no Admin · Theme Settings IDs **vazios** |
| Storefront browser | `saibai-tracking-client.js` | ✅ | Pós-consent LGPD · proxy `/apps/vlt-tracking/events` |
| Storefront browser | `saibai-consent-popup` | ✅ | Consent Mode v2 |
| Checkout | Customer Events pixel | ⚠️ | Gerar via `configure-saibai-customer-events-pixel.py` |
| Server | Vercel `tracking-eta-eight.vercel.app` | ✅ | API produção |
| Server | Supabase `vlqxrmejvkxnlmpqhkvt` | ✅ | Tabela `tracking_events` |
| Server | Meta CAPI | ✅ | Token configurado · purchase testado |
| Server | GA4 Measurement Protocol | ❌ | **GA4_API_SECRET** pendente |
| Server | Webhook `orders/paid` | ⚠️ | Reinstalar app (`read_orders`) |
| Opcional | Stape sGTM | ⏸ | Auditar duplicatas se ativo |

## IDs canônicos

| Canal | ID | Onde configurar |
|-------|-----|-----------------|
| GA4 | `G-VWX77SGD1W` | Canal Google Shopify · Vercel env |
| Meta Pixel | `2017630342068049` | Canal Meta Shopify · CAPI Vercel |
| Theme Settings | **vazios** | Anti-duplicata com canais |
| tracking_endpoint | `/apps/vlt-tracking/events` | Theme Settings |

## Regra anti-duplicata

```
Browser: Canais Shopify (1 GA4 + 1 fbq) OU theme IDs — NUNCA ambos
Checkout purchase: Canal OU Customer Events pixel — NUNCA ambos
Server: Vercel CAPI/MP dedupe por order_id + event_id
```

## Eventos alvo

| Evento | Browser | Server | Key event GA4 |
|--------|:-------:|:------:|:-------------:|
| page_view | ✅ canal | — | — |
| view_item | ✅ client | — | — |
| add_to_cart | ✅ client + canal | — | — |
| begin_checkout | ✅ pixel checkout | — | — |
| purchase | ⚠️ 1 fonte only | ✅ webhook | **purchase** |
| scroll_depth | ✅ client | — | — |
| whatsapp_click | ✅ float button | — | opcional |

## Arquivos-chave (tema)

| Arquivo | Função |
|---------|--------|
| `theme/assets/saibai-tracking-client.js` | Client pós-LGPD |
| `theme/snippets/saibai-tracking-config.liquid` | JSON config |
| `theme/sections/saibai-consent-popup.liquid` | Banner LGPD |
| `theme/assets/saibai-consent-popup.js` | Consent Mode v2 |
| `ops/scripts/configure-saibai-customer-events-pixel.py` | Pixel checkout |
| `ops/scripts/saibai-martech-audit.py` | Checklist martech |

## Pendências P0 (manual)

| # | Ação | Doc |
|---|------|-----|
| T-1 | Gerar GA4 API Secret → Vercel | CHECKLIST_MANUAL §1.1 |
| T-2 | Reinstalar app Saibai Tracking | CHECKLIST_MANUAL §1.1 |
| T-3 | Conectar canais Google/Meta | CHECKLIST_MANUAL §1.4 |
| T-4 | Validar proxy 202 + purchase teste | CHECKLIST_MANUAL §3 |
| T-5 | Desligar banner cookies nativo Shopify | CHECKLIST_MANUAL §1.3 |
| T-6 | Conceder GA4 à conta Veltrus (MCP) | GA4_REPORT.md |
| T-7 | Auditar Stape se instalado (sem duplicata) | saibai-martech-audit.py |

## Validação

```bash
# Theme settings vazios (anti-duplicata)
grep -E "meta_pixel_id|ga4_measurement_id" clients/saibai/theme/config/settings_data.json

# Martech checklist
python3 clients/saibai/ops/scripts/saibai-martech-audit.py

# Tracking API (se repo tracking local)
cd tracking && npm run test:proxy && npm run test:webhook
```

## Vereditos por camada

| Camada | Veredito |
|--------|----------|
| Tema + consent | **PASS** |
| Client JS | **PASS** |
| Vercel API | **PASS** |
| CAPI Meta | **PASS** |
| GA4 MP | **PRECISA HOTFIX** |
| Webhook purchase | **PRECISA HOTFIX** |
| Canais browser | **PRECISA HOTFIX** |
| GA4 MCP audit | **PENDING_ACCESS** |
