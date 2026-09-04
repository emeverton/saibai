# Empório Saibai — Sync Notificações WhatsApp + n8n · 25/06/2026

**Escopo:** Deploy VPS cron + n8n workflows + destinatário Everton  
**Veredito:** **PASS** · smoke WhatsApp confirmado

---

## Notion

| Item | Link |
|------|------|
| **Hub** | [Empório Saibai — Documentação Técnica](https://app.notion.com/p/38a968afab6681bb8a03e2d2e6848147) |
| **06 — Notificações** | [Notificações WhatsApp + n8n](https://app.notion.com/p/38a968afab66812abdecf99e6e608fc5) |
| Page ID | `38a968af-ab66-812a-bdec-f99e6e608fc5` |

Índice do hub: tópico **06 — Notificações WhatsApp + n8n**.

---

## Slack

| Canal | Mensagem |
|-------|----------|
| `#ops-clientes` | [sync notificações · 25/06](https://veltrus.slack.com/archives/C0BA1AA7D7U/p1782390207622889) |
| `#cliente-saibai` | [notificações LIVE](https://veltrus.slack.com/archives/C0BD28VMD4N/p1782390172841209) |

---

## eKyte (workspace Saibai `123736`)

| Task | ID | Ação |
|------|-----|------|
| Estratégia H2 execução | **#9713234** | ✅ Comentário deploy notificações |
| Go-live P0 | **#9712969** | ✅ Comentário integração vendas pós gate B |

**Status tasks:** permanecem **Ativa** (não finalizadas).

---

## Repo (canônico)

| Doc | Path |
|-----|------|
| Alertas campanha | `docs/CAMPANHA-ALERTAS-WHATSAPP.md` |
| E-com + n8n | `docs/NOTIFICACOES-ECOM-N8N.md` |
| Workflows | `n8n/n8n-saibai-*.json` |
| Deploy VPS | `docs/agents/scripts/deploy-saibai-campaign-alerts.sh` |
| Deploy n8n | `docs/agents/scripts/deploy-saibai-n8n.sh` |
| Dossiê | `CLIENT_CONTEXT.md` § Notificações operacionais |

---

## Stack LIVE

| Componente | Detalhe |
|------------|---------|
| Destinatário | `5517991661332` (Everton) — alertas + account + vendas |
| Cron 07:10 | `monitor-saibai-campaigns-daily.mjs` |
| Cron 07:20 | `send-saibai-account-whatsapp-daily.mjs` |
| Cron */10 7–23h | `notify-saibai-sales-whatsapp.mjs` |
| n8n e-com | `A5gLX8OsP6cHjt4o` · `/webhook/saibai-ecom-sale-notify` |
| n8n Shopify | `qcNWhnAEsaipS5my` · `/webhook/saibai-shopify-order-paid` |
| n8n Growth | `qhkj95bVNCYliIIZ` · stub até planilha |

---

## Próximo passo

1. Gate B go-live → vendas passam a notificar de verdade
2. `SAIBAI_GA4_PROPERTY_ID` no VPS quando GA4 Veltrus liberado
3. Growth sheet → completar batchUpdate no workflow stub
