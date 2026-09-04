# Empório Saibai — Análise Growth Pack · 25/06/2026

**Cliente:** Empório Saibai · Piedade SP · Shopify D2C + B2B WhatsApp  
**Fonte:** Meta MCP LIVE · blueprint Growth Pack Veltrus · estratégia v1  
**Export JSON:** `exports/growth-pack-analysis-saibai-2026-06-25.json`  
**Veredito:** **PRECISA AUDITORIA** — mídia B2B ok · e-com sem baseline · planilha ainda não criada

> Reportei: **sem projeto** · Growth Sheet: **PENDING_CREATE** · Google/GA4: bloqueados.

---

## 1. Resumo executivo

A Saibai investiu **R$ 2.322** em Meta (jan–25/jun/26) com **zero visibilidade Google** e **zero purchase GA4** no stack Veltrus. Quase todo o spend recente vai para **grupo WhatsApp B2B** — coerente com safra/legado V4, **desalinhado** com a loja Shopify pronta para D2C.

O Growth Pack 2026 deve tratar **dois tracks separados** na planilha:

| Track | KPI Growth Pack | Mídia hoje |
|-------|-----------------|------------|
| **B2C e-com** | GA4 `purchase` · ROAS · AOV | ❌ sem campanha ativa |
| **B2B WhatsApp** | `whatsapp_click` · leads grupo | ✅ R$ 20/d LEADS-GRUPO-WHATS |

**Não** usar conv. plataforma Meta (97k YTD) como KPI — são eventos messaging/engagement.

---

## 2. Meta Ads — evolução mensal (MCP LIVE)

| Mês | Spend | Impressões | Cliques | CTR | CPC | Conv. plat. | Leitura |
|-----|------:|-----------:|--------:|----:|----:|------------:|---------|
| Jan–Mar | R$ 319 | 57.073 | 74 | 0,13% | R$ 4,30 | 21.236 | ❌ Engajamento Insta — waste |
| Abr | R$ 1.225 | 146.676 | 2.629 | 1,79% | R$ 0,47 | 53.246 | ⚠️ Transição WhatsApp + engajamento |
| Mai | R$ 618 | 43.105 | 1.430 | 3,32% | R$ 0,43 | 19.915 | ✅ B2B WhatsApp eficiente |
| Jun 1–25 | R$ 160 | 9.511 | 409 | 4,30% | R$ 0,39 | 2.977 | ✅ 1 camp ativa · spend baixo |
| **YTD** | **R$ 2.322** | **256.369** | **4.542** | **1,77%** | **R$ 0,51** | **97.374** | ❌ KPI plataforma inválido |

### Campanha ativa (jun/26)

| Campo | Valor |
|-------|-------|
| Nome | `22.04.2026 [V4] [WB] [LEADS-GRUPO-WHATS] 02` |
| Budget | R$ 20/dia (~R$ 600/mês) |
| Adset | SP metropolitana · 30+ · IG+FB |
| Objetivo | OUTCOME_LEADS · OFFSITE_CONVERSIONS |
| Spend jun | R$ 132,92 (83% do mês) |

### O que os números provam

1. **Abril foi o pico de desperdício** — R$ 664 em engajamento Insta com CTR 0,2% e CPC R$ 3,71.
2. **Maio corrigiu parcialmente** — LEADS-GRUPO-WHATS com CTR 5,6% e CPC R$ 0,25.
3. **Junho sub-investido** — R$ 160 em 25 dias vs plano B2B R$ 600/mês.
4. **Zero campanha Sales D2C** ativa — 4 campanhas e-com 2025 pausadas.
5. **ROAS plataforma YTD 1,97** — irrelevante sem purchase GA4.

---

## 3. Google Ads — gap total

| Item | Status |
|------|--------|
| Conta `9513237350` | MCC pending |
| Spend YTD no Growth Pack | **R$ —** |
| Campanhas visíveis MCP | ❌ gateway 500 |

**Impacto Growth Pack:** abas `ImportaçãoGoogleAds` e `4.1 Meta x Realizado` ficam vazias até merchant aceitar MCC.

---

## 4. GA4 / receita — gap total

| Item | Status |
|------|--------|
| `G-VWX77SGD1W` | Fora MCP Veltrus |
| Purchase YTD | **Não auditável** |
| Receita e-com | **Não auditável** |

**Impacto Growth Pack:** sem `purchase` · `add_to_cart` · `revenue` — Painel Executivo e CAC-LTV-ROAS não fecham.

---

## 5. Plano vs realizado (jun/26)

| Canal | Plano Growth Pack Fase 0 | Realizado 1–25/jun | Δ |
|-------|-------------------------:|-------------------:|---|
| Meta | R$ 600/mês (~R$ 500 em 25d) | R$ 160 | **−68%** sub-investido |
| Google | R$ 0 (pré-MCC) | R$ 0 | — |
| **Total mídia** | **R$ 600** | **R$ 160** | **−73%** |

Plano alvo **pós-go-live** (jul+): **R$ 3.750/mês** · Meta R$ 1.800 · Google R$ 1.950 (ref. estratégia v1).

---

## 6. Blueprint Growth Pack 2026 — Saibai

### Planilha (criar)

| Item | Valor |
|------|-------|
| Nome sugerido | `[GROWTHPACK] [2026] - EMPÓRIO SAIBAI` |
| `SHEET_ID` | **PENDING_CREATE** → `SAIBAI_GROWTH_SHEET_ID` |
| Template base | Clonar Malhas ou Empório Vitório · adaptar KPIs e-com |

### Abas automatizadas (proposta)

| Aba | Fonte | KPI |
|-----|-------|-----|
| `ImportaçãoMeta - Adveronix` | Meta Graph API | spend · imp · clk |
| `ImportaçãoGoogleAds - Adveronix` | Google Ads API | spend · conv (pós-MCC) |
| `Relatório Diário` | Meta + Google + GA4 + Shopify | purchase · AOV · WA |
| `4.1 Meta x Realizado` | Plano vs real | pacing mensal |
| **`Consolidado`** | Semanal | **fórmulas template — sync não escreve** |
| `CAC - LTV - ROAS` | GA4 purchase + ERP futuro | pós 30d baseline |

### Colunas extras Relatório Diário (e-com)

| Coluna | Evento GA4 |
|--------|------------|
| Purchase GA4 | `purchase` |
| Receita GA4 | `purchase` value |
| Add to cart | `add_to_cart` |
| WhatsApp click | `whatsapp_click` (custom) |
| Sessões | `sessions` |

### Arquitetura (quando sheet existir)

```
VPS cron 06:55 BRT
  └─ sync-saibai-growth-sheet.mjs  (a criar)
       ├─ Meta Graph API (act_1199864388174624)
       ├─ Google Ads API (9513237350) — pós-MCC
       ├─ GA4 Data API (property PENDING)
       └─ POST n8n.ehos.com.br/webhook/saibai-growth-sheet-sync
```

Plano de mídia: `docs/agents/scripts/saibai-growth-plan.mjs`

---

## 7. Matriz de decisão Growth Pack

### Fase 0 — agora (sem purchase GA4)

| # | Ação | Impacto planilha |
|---|------|------------------|
| 0.1 | Criar planilha Growth Pack + compartilhar n8n | Desbloqueia sync |
| 0.2 | Preencher manual jan–jun Meta (import histórico) | Baseline YTD |
| 0.3 | Manter LEADS-GRUPO-WHATS R$ 20/d | Aba B2B separada |
| 0.4 | Merchant: MCC Google + GA4 access | Desbloqueia Google + purchase cols |

### Fase 1 — pós purchase validado (30 dias)

| # | Ação | Budget |
|---|------|-------:|
| 1.1 | Meta `[SAIBAI][SALES][D2C][PURCHASE]` | R$ 40/d |
| 1.2 | Google PMax feed Shopify | R$ 50/d |
| 1.3 | Search marca | R$ 15/d |
| 1.4 | Deploy sync VPS + cron | — |
| 1.5 | Criar projeto Reportei Saibai | Consolidado multi-canal |

### Fase 2 — otimização (60 dias)

| # | Ação |
|---|------|
| 2.1 | CAC-LTV-ROAS com receita Shopify |
| 2.2 | Lead Score B2B (WhatsApp grupo → pedido B2B) |
| 2.3 | Alertas WhatsApp pacing (modelo Gás do Nilson) |

---

## 8. Comparativo clientes Veltrus (Growth Pack maduro)

| Cliente | Sheet | Meta/mês ref. | Google | GA4 MCP | Reportei |
|---------|-------|--------------:|--------|---------|----------|
| Malhas | ✅ | R$ 2.000 | ✅ | ✅ | ✅ 819967 |
| Gás Nilson | ✅ | ~R$ 1.800 | ✅ | ✅ | — |
| Empório Vitório | ✅ | R$ 2.100 | ✅ | ✅ | — |
| **Saibai** | ❌ | R$ 160 real jun | ❌ | ❌ | ❌ |

Saibai está **2–3 fases atrás** no Growth Pack — falta planilha, sync, GA4 e Google.

---

## 9. Vereditos

| Área | Veredito |
|------|----------|
| Dados Meta MCP | **PASS** |
| Leitura estratégica | **PRECISA AUDITORIA** |
| Growth Sheet | **PENDING_CREATE** |
| Automação sync | **BLOQUEADO** (sheet + GA4 + MCC) |
| KPI purchase | **PENDING_TRACKING** |

---

## 10. Próximos passos Veltrus

1. Criar planilha `[GROWTHPACK] [2026] - EMPÓRIO SAIBAI` (clone template)
2. Backfill manual Meta jan–jun nas abas Importação
3. Concluir go-live P0 (`GO-LIVE-RUNBOOK-P0.md`)
4. Implementar `sync-saibai-growth-sheet.mjs` + n8n workflow
5. Criar projeto Reportei + registrar `reportei_project_id`

**Gate de escala mídia D2C:** purchase GA4 validado 7 dias consecutivos.

---

## Referências

- Estratégia: `CAMPAIGN_OPTIMIZATION_STRATEGY.md`
- Plataformas: `PLATFORMS-AUDIT-2026-06-25.md`
- Go-live: `GO-LIVE-RUNBOOK-P0.md`
- Plano código: `docs/agents/scripts/saibai-growth-plan.mjs`
