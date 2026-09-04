# Setup Saibai — Tracking Server-Side

Ordem recomendada (já iniciada no código):

## ✅ Feito no repo

| Camada | Arquivo |
|--------|---------|
| Client theme (pós-LGPD) | `theme/assets/saibai-tracking-client.js` |
| Config theme | `snippets/saibai-tracking-config.liquid` |
| API ingestão | `tracking/src/app/api/tracking/events` |
| App Proxy | `tracking/src/app/api/shopify-proxy/events` |
| Meta CAPI + GA4 MP | `tracking/src/lib/tracking/destinations/` |
| Consent gate server | `consent_analytics` / `consent_marketing` no payload |

## 1. Supabase ✅

Projeto criado via MCP:

| Campo | Valor |
|-------|-------|
| Nome | `saibai-tracking` |
| Ref | `vlqxrmejvkxnlmpqhkvt` |
| Região | `sa-east-1` |
| URL | https://vlqxrmejvkxnlmpqhkvt.supabase.co |
| Dashboard | https://supabase.com/dashboard/project/vlqxrmejvkxnlmpqhkvt |
| Tabelas | `persons`, `identities`, `tracking_events`, `destination_logs`, `ad_costs` |
| RLS | Habilitado (sem policies públicas — só service role) |

Copiar **DATABASE_URL** em Settings → Database → Connection string → URI (pooler):

```bash
cd tracking
cp .env.saibai.example .env
# colar DATABASE_URL no .env
```

## 2. Credenciais Meta + GA4 (10 min)

| Secret | Onde obter |
|--------|------------|
| `META_ACCESS_TOKEN` | Meta Events Manager → Pixel `2017630342068049` → Settings → Conversions API → Generate token |
| `GA4_API_SECRET` | GA4 Admin → Data Streams → `G-VWX77SGD1W` → Measurement Protocol → Create |

## 3. Deploy Vercel ✅

| Campo | Valor |
|-------|--------|
| URL produção | https://tracking-eta-eight.vercel.app |
| Projeto | `emevertons-projects/tracking` |
| Dashboard | https://vercel.com/emevertons-projects/tracking |

Env vars configuradas: `DATABASE_URL`, secrets, IDs Saibai.

Teste produção:

```bash
curl -X POST https://tracking-eta-eight.vercel.app/api/tracking/events \
  -H "Content-Type: application/json" \
  -H "x-tracking-secret: SEU_TRACKING_ENDPOINT_SECRET" \
  -d '{"event_id":"'$(uuidgen | tr '[:upper:]' '[:lower:]')'","event_name":"page_view","consent_analytics":true,"visitor_id":"test","session_id":"test","page_url":"https://emporiosaibai.com.br/"}'
```

Resposta esperada: `"status":"accepted"`

## 4. Shopify App Proxy — deployado via CLI

App **Saibai Tracking** na org Emporio Saibai (`client_id`: `0f5ea7f8dd46a060c5416f21573c9256`).

Config em `tracking/saibai-tracking-app/saibai-tracking/shopify.app.toml`:

| Campo | Valor |
|-------|-------|
| Subpath prefix | `apps` |
| Subpath | `vlt-tracking` |
| Proxy URL | `https://tracking-eta-eight.vercel.app/api/shopify-proxy` |

**Instalar na loja (obrigatório — proxy retorna 404 sem install):**

1. Abrir: [Instalar Saibai Tracking](https://admin.shopify.com/store/byinbz-0k/oauth/install?client_id=0f5ea7f8dd46a060c5416f21573c9256)
2. Confirmar permissão `write_app_proxy`

**Secret:** `SHOPIFY_APP_PROXY_SECRET` = API secret do app (`shopify app env show` na pasta do app).

**Redeploy Vercel** após setar o secret: `cd tracking && vercel --prod --yes`

**Teste HMAC direto (sem Shopify):** `npm run test:proxy` → esperado `202 accepted`

Storefront chama: `POST /apps/vlt-tracking/events` (first-party, sem secret no browser).

## 5. Theme deploy

```bash
cd theme
shopify theme push --store byinbz-0k.myshopify.com --theme 186124239166 --allow-live \
  --only assets/saibai-tracking-client.js snippets/saibai-tracking-config.liquid \
  sections/saibai-consent-popup.liquid config/settings_schema.json
```

Theme Settings → Saibai Tracking → **Server-side tracking** = `/apps/vlt-tracking/events` (default).

## 6. Validar

1. Aba anônima → aceitar cookies
2. DevTools → Network → filtrar `vlt-tracking` → deve retornar `202 accepted`
3. Supabase → `tracking_events` → nova linha
4. Meta Events Manager → Test Events
5. GA4 → DebugView

## Arquitetura final

```
Browser (após LGPD)
  → /apps/vlt-tracking/events (Shopify App Proxy + HMAC)
  → Vercel /api/shopify-proxy/events
  → Postgres + identity graph
  → Meta CAPI (se consent_marketing)
  → GA4 MP (se consent_analytics)
  → Inngest retry (async)

Browser paralelo (sem duplicar):
  → Canais Shopify Google/Meta (pixel nativo)
  → Stape sGTM (server-only, auditar dedupe)
```

## 7. Meta CAPI + GA4 MP (destinos server-side)

Gerar os secrets (não estão no repo):

| Secret | Onde gerar |
|--------|------------|
| `META_ACCESS_TOKEN` | [Meta Events Manager → Pixel 2017630342068049 → Settings → Conversions API → Generate access token](https://business.facebook.com/events_manager2/list/pixel/2017630342068049/settings?tab=conversionsAPI) |
| `GA4_API_SECRET` | [GA4 Admin → Data Streams → Web → Measurement Protocol API secrets → Create](https://analytics.google.com/) (property `G-VWX77SGD1W`) |

Configurar no Vercel (com os valores em mãos):

```bash
cd tracking
chmod +x scripts/configure-destinations.sh
META_ACCESS_TOKEN="EAA..." GA4_API_SECRET="..." ./scripts/configure-destinations.sh
```

Resposta esperada no teste final: `destinations` com `meta: success` e `ga4: success`.


- Theme Settings `ga4_measurement_id` / `meta_pixel_id` → **vazios**
- Canais Shopify = browser pixel oficial
- `/tracking` API = server-side enrichment + CAPI/MP backup
- Stape = auditar para não reenviar o que CAPI já recebe

## 8. Webhook `orders/paid` — purchase server-side

Rota: `POST /api/shopify/webhooks/orders-paid`

| Campo | Valor |
|-------|-------|
| Topic | `orders/paid` |
| Scope app | `read_orders` |
| Secret HMAC | `SHOPIFY_APP_PROXY_SECRET` (API secret do app) |

**Reinstalar app** após deploy (novo scope `read_orders`):
[Instalar Saibai Tracking](https://admin.shopify.com/store/byinbz-0k/oauth/install?client_id=0f5ea7f8dd46a060c5416f21573c9256)

Teste local/simulado:

```bash
cd tracking && npm run test:webhook
```

Resposta esperada: `"event_name":"purchase"`, `"status":"accepted"`, Meta `success` se `consent_marketing: true`.

**Consentimento no webhook:**
- GA4 (`consent_analytics`): `true` — purchase ecommerce
- Meta (`consent_marketing`): `buyer_accepts_marketing` do pedido Shopify

**Dedupe:** mesmo `order_id` não dispara purchase duplicado (browser + webhook).

## Pendente (fase 2)

- [ ] Google Ads Enhanced Conversions (OAuth)
- [ ] TikTok / Klaviyo destinations
- [x] Webhook Shopify `orders/paid` → purchase server-side garantido
- [ ] Rate limit em Redis/KV (multi-instance)
- [ ] Import `ad_costs` diário

---

Veltrus · Empório Saibai
