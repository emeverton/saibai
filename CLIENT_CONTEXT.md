# Empório Saibai — Contexto Operacional

**Atualizado:** 2026-06-25  
**Prioridade roadmap:** #13 (novo)  
**Pasta:** `clients/saibai/`  
**Veredito dossier:** **PASS** · operação **PRECISA AUDITORIA**  
**Notion hub:** [Documentação Técnica](https://app.notion.com/p/38a968afab6681bb8a03e2d2e6848147) · [AUDIT 28/06](https://app.notion.com/p/38d968afab6681bca003eb06677fad76) · [Auditoria 25/06](https://app.notion.com/p/38a968afab66814b9587f7a9338accd9)  
**Veredito Campaign Optimizer 28/06:** **BLOQUEADO** D2C · **PODE MANTER** B2B WhatsApp · ChatGPT ✅ validado  
**Slack:** `#cliente-saibai` · https://veltrus.slack.com/archives/C0BD28VMD4N  
**Sync:** [docs/SYNC-NOTION-SLACK-EKYTE-2026-06-28.md](./docs/SYNC-NOTION-SLACK-EKYTE-2026-06-28.md)

## Foco atual

**Estratégia H2 2026:** abertura e-commerce D2C (gates pagamento + tracking) → ramp mídia jul–ago → escala conservas set–out → Natal dez.  
Doc mestre: [docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md)

Dual track **B2C purchase (70% mídia)** + **B2B WhatsApp (20%)** — KPI e-com = GA4 `purchase`.

## Identificadores confirmados

| Campo | Valor | Status |
|-------|-------|--------|
| clientKey | `saibai` | OK |
| GA4 measurementId | `G-VWX77SGD1W` | ⚠️ propertyId não no MCP Veltrus |
| GA4 propertyId | `PENDING_ACCESS` | Conceder acesso conta GA4 Veltrus |
| Meta adAccountId | `act_1199864388174624` | ✅ MCP LIVE |
| Meta pixelId | `2017630342068049` | OK |
| Google customerId | `9513237350` | ⚠️ MCC invite pending · gateway 500 |
| Google MCC login | `9217486074` | OK |
| Shopify store | `byinbz-0k.myshopify.com` | OK |
| Shopify admin slug | `emporiosaibai` | OK |
| Domínio live | `emporiosaibai.com.br` | OK |
| Tema live ID | `186124239166` | Saibai v1.2.4 |
| Tracking API | `tracking-eta-eight.vercel.app` | ✅ Deploy |
| Supabase project | `vlqxrmejvkxnlmpqhkvt` | ✅ `tracking_events` |
| Shopify app | `saibai-tracking-3` | ✅ Partners · webhook pendente reinstall |
| Telefone | `(15) 3010-1451` | Fixo |
| E-mail | `contato@saibai.com.br` | Checkout/e-mails |
| Endereço | Estrada dos Lavradores, 7 · Piedade, SP · CEP **18176-210** | Capital Nacional da Alcachofra |
| Plataforma | **Shopify** (tema Veltrus/Halo fork) | Não Tray |
| Cupom ativo | `5%NOVOCLIENTE` (5% 1x) · `SAIBAIRECOMPRA` (8% · mín. R$120) | CRM nativo 26/08 |
| Frete grátis | R$ 280+ | API configurado |
| **Notificações WhatsApp** | VPS + n8n LIVE | ✅ 25/06 · dest. Everton |
| **n8n workflows [SB]** | 3 ACTIVE | e-com · shopify · growth stub |

## Notificações operacionais (25/06 — LIVE)

| Camada | Componente | Status |
|--------|------------|--------|
| VPS cron | `monitor-saibai-campaigns-daily.mjs` | ✅ 07:10 · alertas silenciosos |
| VPS cron | `send-saibai-account-whatsapp-daily.mjs` | ✅ 07:20 · resumo MTD |
| VPS cron | `notify-saibai-sales-whatsapp.mjs` | ✅ */10 7–23h · pós gate B |
| n8n | `[SB] E-com Sale WhatsApp` | ✅ `A5gLX8OsP6cHjt4o` |
| n8n | `[SB] Shopify Order Paid` | ✅ `qcNWhnAEsaipS5my` |
| n8n | `[SB] Growth Sheet Sync` | ✅ `qhkj95bVNCYliIIZ` (stub) |
| Evolution | `api.ehos.com.br` / `veltrus-agent` | ✅ smoke test OK |
| Destinatário ops | `5517991661332` (Everton) | ✅ alertas + account + vendas |

**Webhooks:** `saibai-ecom-sale-notify` · `saibai-shopify-order-paid` · `saibai-growth-sheet-sync`  
**Deploy:** `docs/agents/scripts/deploy-saibai-campaign-alerts.sh` · `deploy-saibai-n8n.sh`  
**Docs:** [CAMPANHA-ALERTAS-WHATSAPP.md](./docs/CAMPANHA-ALERTAS-WHATSAPP.md) · [NOTIFICACOES-ECOM-N8N.md](./docs/NOTIFICACOES-ECOM-N8N.md)

## MCPs necessários

| MCP | Status 25/06 |
|-----|--------------|
| veltrus-analytics-mcp | ⚠️ GA4 Saibai **fora** da lista de properties |
| veltrus-meta-ads-mcp | ✅ LIVE — 24 campanhas |
| veltrus-google-ads-mcp | ⚠️ **gateway 500** — MCC não linked |

Registry: `docs/agents/VELTRUS-ACCOUNTS-REGISTRY.json` · `docs/agents/VELTRUS-GA4-REGISTRY.json`

## Fluxo de mutations (obrigatório)

1. `create_request` — APPROVAL_REQUESTS.md
2. `approve` — aprovação humana
3. `execute(confirm:true)` — execução real

**Nenhuma mutation executada neste dossiê.**

## Snapshot jun/2026 (01–25)

### Meta Ads (MCP LIVE — re-audit 25/06)

| Métrica | Valor |
|---------|------:|
| Spend | R$ 160,09 |
| Impressões | 9.511 |
| Cliques | 409 |
| Conv. plataforma | 2.977 ❌ infladas |
| Campanha ACTIVE | `120248254459350155` — LEADS-GRUPO-WHATS R$20/d |
| Pixel last fired | 2026-06-24 ✅ |

### GA4 / Google

| Métrica | Status |
|---------|--------|
| GA4 MCP | **PENDING_ACCESS** — property não listada |
| Google Ads MCP | **PENDING_PERMISSION** — `9513237350` no allowlist mas não linked · gateway 500 |
| Purchase server-side | Código deployado · **GA4_API_SECRET pendente** |

## Pendências P0

1. **GA4** — conceder acesso Veltrus + configurar `GA4_API_SECRET` no Vercel
2. **Shopify** — pagamentos live (PIX/cartão) + canais Google/Meta
3. **Webhook** — reinstalar app Saibai Tracking (`read_orders`)
4. **Google MCC** — aceitar convite conta `9513237350`
5. **Meta** — não confiar conv. plataforma (2.969) · auditar vs purchase GA4
6. **Manual** — `CHECKLIST_MANUAL_SAIBAI.md` seção 1

## Referências internas

- Entrega: [DELIVERY-2026-06-25-dossie-v1.md](./DELIVERY-2026-06-25-dossie-v1.md)
- Estratégia: [CAMPAIGN_OPTIMIZATION_STRATEGY.md](./CAMPAIGN_OPTIMIZATION_STRATEGY.md) (tática v1)
- **Abertura e-com H2:** [docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md)
- **Notion hub:** [Documentação Técnica](https://app.notion.com/p/38a968afab6681bb8a03e2d2e6848147) · [05 Estratégia H2](https://app.notion.com/p/38a968afab6681018105fb8c483b7bef) · [06 Notificações](https://app.notion.com/p/38a968afab66812abdecf99e6e608fc5)
- **Slack:** [#ops-clientes · notificações](https://veltrus.slack.com/archives/C0BA1AA7D7U/p1782390207622889) · [#cliente-saibai · notificações](https://veltrus.slack.com/archives/C0BD28VMD4N/p1782390172841209)
- **eKyte:** #9713234 (estratégia H2 · **Ativa**) · #9712969 (P0)
- Sync estratégia: [docs/SYNC-NOTION-SLACK-EKYTE-2026-06-25.md](./docs/SYNC-NOTION-SLACK-EKYTE-2026-06-25.md)
- Sync notificações: [docs/SYNC-NOTIFICACOES-2026-06-25.md](./docs/SYNC-NOTIFICACOES-2026-06-25.md)
- Alertas WhatsApp: [docs/CAMPANHA-ALERTAS-WHATSAPP.md](./docs/CAMPANHA-ALERTAS-WHATSAPP.md)
- Notificações e-com n8n: [docs/NOTIFICACOES-ECOM-N8N.md](./docs/NOTIFICACOES-ECOM-N8N.md)
- Tracking: [TRACKING_AUDIT.md](./TRACKING_AUDIT.md)
- Checklist manual: [CHECKLIST_MANUAL_SAIBAI.md](./CHECKLIST_MANUAL_SAIBAI.md)
- Tema: [theme/README.md](./theme/README.md)
- Plugin: [saibai-shopify-ops-v1.plugin.md](./saibai-shopify-ops-v1.plugin.md)
- Skill: `.cursor/skills/saibai-company-expert/SKILL.md`
- Roadmap: `../CLIENTS_OPTIMIZATION_ROADMAP.md`
