# Saibai Tracking — Server-Side E-commerce Infrastructure

Infraestrutura modular de tracking para Shopify com ingestão API-first, identity graph, deduplicação e envio para Meta CAPI + GA4 Measurement Protocol.

## Arquitetura

```text
Shopify Storefront (Customer Events + vlt_* cookies)
        │
        ▼
POST /api/tracking/events  (Next.js 15 API Route)
        │
        ├─ Zod validation + rate limit + auth
        ├─ normalize + SHA-256 PII hashing
        ├─ dedupe (event_id + purchase/order_id)
        ├─ resolvePerson() → persons + identities
        ├─ persist tracking_events
        ├─ dispatch destinations (Meta, GA4, placeholders)
        ├─ destination_logs
        └─ Inngest async (retry, healthcheck, alerts)
                │
                ├─ Meta CAPI
                ├─ GA4 MP
                ├─ Google Ads (placeholder)
                ├─ TikTok (placeholder)
                └─ Klaviyo (placeholder)
```

**Princípios**
- Nada crítico depende de n8n (apenas alertas opcionais via webhook).
- IP resolvido server-side (`x-forwarded-for`), nunca enviado pelo client como fonte de verdade.
- Email/telefone nunca persistidos em texto puro — apenas SHA-256 normalizado.
- `event_id` UUID para deduplicação browser + server.

## Stack

| Camada | Tecnologia |
|--------|------------|
| API | Next.js 15 App Router |
| DB | Supabase Postgres + Drizzle ORM |
| Jobs | Inngest |
| Validação | Zod |
| Destinations | Meta CAPI, GA4 MP |

## Setup

```bash
cd tracking
cp .env.example .env
npm install
npm run db:push   # ou aplicar drizzle/migrations/0000_init.sql no Supabase
npm run dev
```

### Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | Sim | Postgres (Supabase) |
| `TRACKING_ENDPOINT_SECRET` | Sim | Auth do endpoint público |
| `TRACKING_ADMIN_SECRET` | Recomendado | Auth endpoints admin |
| `META_PIXEL_ID` | Para Meta | Pixel ID |
| `META_ACCESS_TOKEN` | Para Meta | CAPI token |
| `GA4_MEASUREMENT_ID` | Para GA4 | G-XXXXXXXX |
| `GA4_API_SECRET` | Para GA4 | API secret do stream |
| `INNGEST_EVENT_KEY` | Prod | Inngest |
| `INNGEST_SIGNING_KEY` | Prod | Inngest |
| `SLACK_WEBHOOK_URL` | Opcional | Alertas async |
| `N8N_ALERT_WEBHOOK_URL` | Opcional | Alertas via n8n |

## Endpoints

### Público (storefront)

`POST /api/tracking/events`

Headers:
- `Content-Type: application/json`
- `x-tracking-secret: <TRACKING_ENDPOINT_SECRET>`

Respostas:
- `202 accepted`
- `200 duplicate`
- `400 invalid`
- `401 unauthorized`
- `429 rate limit`
- `500 failed`

### Admin (interno)

| Método | Rota | Auth |
|--------|------|------|
| GET | `/api/tracking/health` | `Authorization: Bearer <ADMIN_SECRET>` |
| GET | `/api/tracking/events/recent?limit=50` | Admin |
| GET | `/api/tracking/destination-logs?status=failed` | Admin |
| POST | `/api/tracking/retry-failed` | Admin |

## Payload exemplo

```json
{
  "event_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "event_name": "add_to_cart",
  "event_time": 1717958400,
  "source": "shopify",
  "shopify_shop_id": "byinbz-0k",
  "visitor_id": "v_abc123",
  "session_id": "s_xyz789",
  "page_url": "https://emporiosaibai.com.br/products/alcachofra",
  "utm_source": "instagram",
  "utm_medium": "paid",
  "gclid": "TeSter-123",
  "product_id": "8123456789012",
  "variant_id": "44556677889",
  "quantity": 1,
  "currency": "BRL",
  "value": 49.9,
  "items": [
    {
      "product_id": "8123456789012",
      "variant_id": "44556677889",
      "quantity": 1,
      "price": 49.9
    }
  ]
}
```

## Eventos suportados

**Shopify**
`page_view`, `product_view`, `collection_view`, `search`, `add_to_cart`, `remove_from_cart`, `begin_checkout`, `add_shipping_info`, `add_payment_info`, `purchase`, `customer_login`, `customer_register`

**Custom**
`whatsapp_click`, `phone_click`, `email_click`, `coupon_apply`, `coupon_remove`, `cta_click`, `scroll_depth`, `video_view`

## Client Shopify

Ver `src/client/shopify-tracking.ts`. Uso:

```ts
import { createShopifyTrackingClient } from './shopify-tracking';

const tracking = createShopifyTrackingClient({
  endpoint: 'https://tracking.emporiosaibai.com.br/api/tracking/events',
  secret: 'PUBLIC_STOREFRONT_PROXY_SECRET', // usar proxy, não expor secret real
  shopId: 'byinbz-0k',
});

// Após consentimento LGPD:
tracking.init();
```

> **Importante:** não exponha `TRACKING_ENDPOINT_SECRET` no theme. Use Cloudflare Worker / app proxy com secret server-side.

## Identity resolution

`resolvePerson(event)` procura identities por:
`email_hash` → `phone_hash` → `shopify_customer_id` → `visitor_id` → `session_id` → click IDs.

Regras:
- Email: `trim().toLowerCase()` + SHA-256
- Telefone: normalização E.164 + SHA-256
- Novos identifiers são vinculados à mesma `person_id`

## Deduplicação

1. `event_id` único (índice unique)
2. `purchase` também deduplica por `order_id + event_name`

## Inngest jobs

| Evento/Cron | Função |
|-------------|--------|
| `tracking/event.received` | Auditoria pós-ingestão |
| `tracking/destination.failed` | Retry automático |
| `0 8 * * *` | Healthcheck diário + Slack/n8n |
| `0 6 * * *` | Import custos (placeholder) |

## Como testar

```bash
curl -X POST http://localhost:3000/api/tracking/events \
  -H "Content-Type: application/json" \
  -H "x-tracking-secret: $TRACKING_ENDPOINT_SECRET" \
  -d '{
    "event_id":"f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "event_name":"page_view",
    "visitor_id":"test-visitor",
    "session_id":"test-session",
    "page_url":"https://emporiosaibai.com.br/"
  }'
```

```bash
curl http://localhost:3000/api/tracking/health \
  -H "Authorization: Bearer $TRACKING_ADMIN_SECRET"
```

## Limitações (v0.1)

- Google Ads Enhanced Conversions: placeholder (OAuth pendente)
- TikTok / Klaviyo: placeholders
- Rate limit em memória (trocar por KV/Redis em produção multi-instance)
- Import `ad_costs`: não implementado
- Client Shopify Customer Events depende de `shopify:analytics:publish` (Shopify Plus / extensões)

## Estrutura de pastas

```text
tracking/
├── drizzle/migrations/
├── src/
│   ├── app/api/tracking/
│   ├── client/shopify-tracking.ts
│   ├── db/
│   ├── inngest/
│   └── lib/tracking/
│       ├── destinations/
│       ├── alerts/
│       └── health/
└── README.md
```

## Segurança & LGPD

- Sem PII pura no banco
- Payload máximo 32 KB
- Rate limit 120 req/min/IP
- Consentimento LGPD deve gatear o client (`saibai-consent-popup.js` no theme)
- Alertas nunca bloqueiam ingestão

---

Veltrus Growth & Technology — Empório Saibai
