# Growth Pack 2026 — Automação · Empório Saibai

**Status:** **PENDING_CREATE** — planilha ainda não existe · sync não deployado  
**Análise:** [ANALISE-GROWTH-PACK-2026-06-25.md](./ANALISE-GROWTH-PACK-2026-06-25.md)  
**Plano mídia:** `docs/agents/scripts/saibai-growth-plan.mjs`

## IDs

| Campo | Valor |
|-------|-------|
| Growth Sheet ID | `PENDING_CREATE` → env `SAIBAI_GROWTH_SHEET_ID` |
| Meta account | `act_1199864388174624` |
| Google customer | `9513237350` (MCC pending) |
| GA4 | `G-VWX77SGD1W` · propertyId `PENDING_ACCESS` |
| Reportei | **sem projeto** |

## Arquitetura (proposta)

```
VPS cron 06:55 BRT
  └─ sync-saibai-growth-sheet.mjs  (a implementar)
       ├─ Meta Graph API (act_1199864388174624)
       ├─ Google Ads API (9513237350) — pós-MCC
       ├─ GA4 Data API — pós property access
       └─ POST n8n.ehos.com.br/webhook/saibai-growth-sheet-sync
            └─ n8n [SB] Growth Sheet Sync (a criar)
                 ├─ ImportaçãoGoogleAds - Adveronix
                 ├─ ImportaçãoMeta - Adveronix
                 ├─ Relatório Diário (+ purchase · AOV · WA)
                 └─ 4.1 Meta x Realizado
```

## Abas alvo

| Aba | Chave upsert | Fonte |
|-----|--------------|-------|
| `ImportaçãoGoogleAds - Adveronix` | `Day` | Google Ads API |
| `ImportaçãoMeta - Adveronix` | `Day` | Meta Graph API |
| `Relatório Diário` | `Data` | Ads + GA4 + plano |
| `4.1 Meta x Realizado` | Mês | Plano vs real |
| `Consolidado` | Semanal | **Fórmulas template — sync NÃO escreve** |

## KPIs Relatório Diário (Saibai)

| Métrica | Origem | Track |
|---------|--------|-------|
| Invest. Meta / Google | APIs | Ambos |
| Purchase | GA4 | B2C |
| Receita | GA4 | B2C |
| Add to cart | GA4 | B2C |
| WhatsApp click | GA4 custom | B2B |
| Conv. plataforma Meta | Meta API | **Referência only — não KPI** |

## Orçamento referência

| Fase | R$/mês | Meta | Google |
|------|-------:|-----:|-------:|
| Fase 0 (jun/26) | 600 | 600 | 0 |
| Fase 1 (pós-go-live) | 3.750 | 1.800 | 1.950 |

Ver `saibai-growth-plan.mjs` · `MEDIA_BUDGET_BY_MONTH`.

## Pré-requisitos deploy

- [ ] Planilha criada + ID no registry
- [ ] Go-live tracking P0 (`GO-LIVE-RUNBOOK-P0.md`)
- [ ] MCC Google linked
- [ ] GA4 property no MCP Veltrus
- [x] Workflow n8n `[SB] Growth Sheet Sync` → `clients/saibai/n8n/n8n-saibai-growth-sheet-sync.json` (stub batchUpdate)
- [ ] Script `sync-saibai-growth-sheet.mjs`
- [ ] Copiar jsCode `Montar batchUpdate` de Malhas quando planilha live

## Comandos (futuro)

```bash
node docs/agents/scripts/sync-saibai-growth-sheet.mjs --days 30
bash docs/agents/scripts/deploy-saibai-growth-sheet-sync.sh
```

## Env (futuro VPS)

| Variável | Uso |
|----------|-----|
| `SAIBAI_GROWTH_SHEET_ID` | ID planilha |
| `SAIBAI_GROWTH_SHEET_WEBHOOK` | webhook n8n |
| `SAIBAI_GROWTH_SHEET_TOKEN` | header `X-Veltrus-Token` |
