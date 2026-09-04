# Empório Saibai

Dossiê operacional Veltrus — Shopify theme, tracking server-side, Meta/Google Ads, dual B2C/B2B alcachofras.

> **Notion:** [Hub](https://app.notion.com/p/38a968afab6681bb8a03e2d2e6848147) · [05 Estratégia H2](https://app.notion.com/p/38a968afab6681018105fb8c483b7bef) · [06 Notificações](https://app.notion.com/p/38a968afab66812abdecf99e6e608fc5)  
> **Slack:** `#cliente-saibai` · https://veltrus.slack.com/archives/C0BD28VMD4N  
> **eKyte:** #9713234 (estratégia H2 · Ativa) · #9712969 (P0)  
> **Plugin v1:** [saibai-shopify-ops-v1.plugin.md](./saibai-shopify-ops-v1.plugin.md)  
> **Agente:** `.cursor/skills/saibai-company-expert/SKILL.md`  
> **Checklist manual:** [CHECKLIST_MANUAL_SAIBAI.md](./CHECKLIST_MANUAL_SAIBAI.md)

## Estado jun/2026

| Área | Status |
|------|--------|
| Tema Shopify | LIVE `#187189297470` (popup cupom 26/08) |
| Tracking server | ✅ Vercel + CAPI · ⚠️ GA4 secret + webhook pendente |
| Meta MCP | ✅ LIVE — 1 camp ACTIVE (WhatsApp leads) |
| Google MCP | ⚠️ MCC pending · gateway 500 |
| GA4 MCP | ⚠️ property fora do acesso Veltrus |
| Pagamentos Shopify | **PRECISA HOTFIX** — PIX/cartão manual |
| Go-live 10/10 | **PRECISA AUDITORIA** |
| Growth Pack 2026 | **PENDING_CREATE** — análise Meta YTD ✅ |
| Notificações WhatsApp + n8n | ✅ **LIVE** 25/06 · VPS cron + 3 workflows |
| Estratégia e-com H2 | ✅ [ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md) |

## Estrutura

| Arquivo / pasta | Propósito |
|-----------------|-----------|
| [CLIENT_CONTEXT.md](./CLIENT_CONTEXT.md) | IDs, KPI, MCPs, snapshot |
| [CAMPAIGN_STATUS.md](./CAMPAIGN_STATUS.md) | Status campanhas live |
| [CAMPAIGN_OPTIMIZATION_STRATEGY.md](./CAMPAIGN_OPTIMIZATION_STRATEGY.md) | Estratégia Meta/Google/e-com |
| [TRACKING_AUDIT.md](./TRACKING_AUDIT.md) | Stack Veltrus + Shopify channels |
| [META_ADS_REPORT.md](./META_ADS_REPORT.md) | Relatório Meta MCP |
| [GOOGLE_ADS_REPORT.md](./GOOGLE_ADS_REPORT.md) | Relatório Google (bloqueado MCC) |
| [GA4_REPORT.md](./GA4_REPORT.md) | Relatório GA4 (pending access) |
| [APPROVAL_REQUESTS.md](./APPROVAL_REQUESTS.md) | Fila aprovações |
| [DELIVERY-2026-06-25-dossie-v1.md](./DELIVERY-2026-06-25-dossie-v1.md) | Entrega dossiê v1 |
| [docs/CRM-NATIVO-SHOPIFY-SAIBAI.md](./docs/CRM-NATIVO-SHOPIFY-SAIBAI.md) | **CRM nativo:** cupons, e-mail, recovery, remarketing |
| [docs/GO-LIVE-RUNBOOK-P0.md](./docs/GO-LIVE-RUNBOOK-P0.md) | Runbook go-live P0 (tracking + vendas) |
| [docs/PLATFORMS-AUDIT-2026-06-25.md](./docs/PLATFORMS-AUDIT-2026-06-25.md) | Auditoria Meta + Google (MCP) |
| [docs/ANALISE-GROWTH-PACK-2026-06-25.md](./docs/ANALISE-GROWTH-PACK-2026-06-25.md) | Análise Growth Pack · Meta mensal YTD |
| [docs/GROWTH-SHEET-AUTOMATION.md](./docs/GROWTH-SHEET-AUTOMATION.md) | Blueprint automação planilha |
| [docs/RESUMO-DIRETORIA-ECOM-H2-2026.md](./docs/RESUMO-DIRETORIA-ECOM-H2-2026.md) | Resumo diretoria e-com H2 |
| [docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md) | **Estratégia abertura + jul–dez/2026** |
| [docs/SYNC-NOTION-SLACK-EKYTE-2026-06-25.md](./docs/SYNC-NOTION-SLACK-EKYTE-2026-06-25.md) | Links Notion · Slack · eKyte |
| [docs/SYNC-NOTIFICACOES-2026-06-25.md](./docs/SYNC-NOTIFICACOES-2026-06-25.md) | Sync notificações WhatsApp + n8n |
| [docs/CAMPANHA-ALERTAS-WHATSAPP.md](./docs/CAMPANHA-ALERTAS-WHATSAPP.md) | Alertas + resumo account VPS |
| [docs/NOTIFICACOES-ECOM-N8N.md](./docs/NOTIFICACOES-ECOM-N8N.md) | Vendas e-com · n8n webhooks |
| [n8n/](./n8n/) | Workflows JSON importáveis |
| [theme/](./theme/) | Tema Shopify Saibai (Git) |
| [ops/scripts/](./ops/scripts/) | Scripts Shopify API/Python |
| [exports/](./exports/) | JSON audits MCP |

**Mutations:** `create_request → approve → execute(confirm:true)` — nenhuma execução real sem aprovação.

## Funil

**B2C:** Anúncio → `emporiosaibai.com.br` → PDP → carrinho → checkout Shopify → purchase  
**B2B:** Anúncio/WhatsApp → Grupo VIP / Contato → lead restaurante

## Próximo passo P0

1. Seguir [docs/GO-LIVE-RUNBOOK-P0.md](./docs/GO-LIVE-RUNBOOK-P0.md) (eKyte **#9712969**)
2. Deploy hotfix cart drawer — runbook **A1** (auth Shopify local + push 4 CSS)
3. Conceder acesso GA4 Veltrus + link Google MCC
4. Após purchase validado → approval Meta Sales D2C
