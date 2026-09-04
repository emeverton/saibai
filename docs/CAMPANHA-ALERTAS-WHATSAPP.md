# Empório Saibai — Alertas diários WhatsApp

Agente automático que audita **loja Shopify + Meta + tracking proxy** todo dia e dispara WhatsApp via **Evolution API** (`api.ehos.com.br`).

## Arquitetura

```
VPS cron 07:10 BRT
  └─ monitor-saibai-campaigns-daily.mjs
       ├─ Health check emporiosaibai.com.br + G-VWX77SGD1W
       ├─ Meta Graph API (act_1199864388174624)
       ├─ Gate: campanha SALES ACTIVE antes de pagamentos → CRITICO
       ├─ Tracking proxy tracking-eta-eight.vercel.app
       └─ POST Evolution sendText/veltrus-agent

VPS cron 07:20 BRT
  └─ send-saibai-account-whatsapp-daily.mjs
       ├─ Meta + Google MTD vs Growth Pack
       ├─ GA4 purchase / ATC / whatsapp_click (pos property access)
       └─ Evolution → SAIBAI_ACCOUNT_WHATSAPP

VPS cron */10 7-23h BRT (pos gate B go-live)
  └─ notify-saibai-sales-whatsapp.mjs
       ├─ Poll GA4 purchase (primario)
       ├─ Fallback Supabase tracking_events
       ├─ POST n8n webhook saibai-ecom-sale-notify (opcional)
       └─ Evolution → SAIBAI_SALES_WHATSAPP
```

## Ordem diária

| Horário | Job |
|---------|-----|
| 06:55 | Growth sheet sync (futuro · n8n cron) |
| **07:10** | **Alertas WhatsApp (só se houver problema)** |
| **07:20** | **Resumo account WhatsApp (sempre)** |
| **07–23h /10min** | **Nova venda e-com (pos go-live)** |

## Alertas monitorados

| Severidade | Gatilho |
|------------|---------|
| **CRITICO** | Loja `emporiosaibai.com.br` ≠ HTTP 200 |
| **CRITICO** | Campanha Meta **SALES** ACTIVE antes do gate pagamento |
| **ATENCAO** | Loja sem `G-VWX77SGD1W` ou `saibai-tracking` no HTML |
| **ATENCAO** | Meta ACTIVE · 0 spend/impressões ontem |
| **ATENCAO** | LEADS-GRUPO-WHATS ACTIVE · 0 entrega ontem |
| **ATENCAO** | Tracking proxy com falha HTTP |

Sem alertas → **não envia WhatsApp** (silencioso).

## Resumo account (07:20)

Conteúdo: plano Growth Pack vs realizado MTD · forecast · GA4 e-com (purchase receita) · status Google MCC.

## Env (VPS)

Carregados de:

- `/opt/meta-ads-mcp-veltrus/.env`
- `/opt/google-ads-mcp-veltrus/.env`
- `/opt/veltrus-analytics-mcp/.env.remote`
- `/opt/veltrus/.env` ← Evolution + telefones

| Variável | Uso |
|----------|-----|
| `EVOLUTION_API_BASE_URL` | default `https://api.ehos.com.br` |
| `EVOLUTION_API_KEY` | apikey header |
| `EVOLUTION_INSTANCE_NAME` | default `veltrus-agent` |
| `SAIBAI_ALERT_WHATSAPP_LIST` | alertas ops |
| `SAIBAI_ACCOUNT_WHATSAPP` | resumo account |
| `SAIBAI_SALES_WHATSAPP` | nova venda e-com |
| `SAIBAI_GA4_PROPERTY_ID` | GA4 Data API (pos acesso) |
| `SAIBAI_SUPABASE_URL` | fallback vendas |
| `SAIBAI_SUPABASE_SERVICE_KEY` | fallback vendas |
| `SAIBAI_ECOM_WEBHOOK_URL` | `https://n8n.ehos.com.br/webhook/saibai-ecom-sale-notify` |
| `SAIBAI_SALES_STATE_FILE` | `/opt/veltrus-scripts/saibai-sales-notified.json` |

## Comandos

```bash
# Deploy completo VPS
bash docs/agents/scripts/deploy-saibai-campaign-alerts.sh

# Manual local / VPS
node docs/agents/scripts/monitor-saibai-campaigns-daily.mjs --dry-run
node docs/agents/scripts/send-saibai-account-whatsapp-daily.mjs --dry-run
node docs/agents/scripts/notify-saibai-sales-whatsapp.mjs --dry-run

# Forçar teste alerta
node monitor-saibai-campaigns-daily.mjs --force
node notify-saibai-sales-whatsapp.mjs --force
```

Logs:

- `/var/log/saibai-campaign-alerts.log`
- `/var/log/saibai-account-whatsapp.log`
- `/var/log/saibai-sales-whatsapp.log`

## Pré-requisitos

| Gate | Bloqueio |
|------|----------|
| Go-live P0 | Vendas poll só após purchase validado |
| GA4 property | `SAIBAI_GA4_PROPERTY_ID` numérico |
| Google MCC | Alertas Google vazios até campanhas live |
| n8n | Importar workflows em `clients/saibai/n8n/` |

Ver também: [NOTIFICACOES-ECOM-N8N.md](./NOTIFICACOES-ECOM-N8N.md)
