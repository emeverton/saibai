# Empório Saibai — Entrega completa · 25/06/2026

**Cliente:** Empório Saibai · Shopify D2C conservas · B2B WhatsApp  
**Escopo:** Tema Shopify · Tracking Vercel/CAPI · Meta · Google · Estratégia H2 · Notificações  
**Veredito geral:** Dossiê **PASS** · go-live merchant **PRECISA HOTFIX** · GA4/Google **PENDING_ACCESS**

> Dossiê: [DELIVERY-2026-06-25-dossie-v1.md](../DELIVERY-2026-06-25-dossie-v1.md) · Estratégia: [ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./ESTRATEGIA-ABERTURA-ECOM-H2-2026.md)

---

## Índice

1. [Antes vs Depois](#antes-vs-depois)
2. [Shopify + tema](#shopify)
3. [Tracking Vercel + CAPI](#tracking)
4. [Meta Ads](#meta-ads)
5. [Google Ads](#google-ads)
6. [Estratégia e-com H2 2026](#estrategia)
7. [Notificações WhatsApp + n8n](#whatsapp)
8. [Arquivos e scripts](#arquivos)
9. [Pendências](#pendencias)

---

## Antes vs Depois {#antes-vs-depois}

| Área | Como estava | Como está (25/06) |
|------|-------------|-------------------|
| **Pasta cliente** | Fragmentada | `clients/saibai/` inventariado · skill agente |
| **Meta** | 24 campanhas legado | 23 pausadas · 1 ACTIVE LEADS-GRUPO-WHATS R$ 20/d |
| **Google** | Sem audit MCP | Gateway 500 · MCC pending |
| **GA4** | Sem acesso Veltrus | **PENDING_ACCESS** property |
| **Tema** | Cart drawer issues | v1.2.4 LIVE · hotfix CSS repo |
| **Estratégia** | Implícita | Doc H2 jul–dez · 4 fases · ~R$ 27k mídia |
| **Notificações** | Ausentes | VPS cron + 3 workflows n8n **LIVE** |
| **Go-live merchant** | Não documentado | Runbook P0 · checklist manual |

---

## Shopify + tema {#shopify}

| Item | Detalhe |
|------|---------|
| Loja | `byinbz-0k.myshopify.com` · admin `emporiosaibai` |
| Tema LIVE | ID `186124239166` · **v1.2.4** |
| Produto ativo | Safra fresca `in-natura-1` |
| Frete grátis | R$ 280 |
| Pagamentos | **Pendente** PIX/cartão Shopify Payments |

**Doc:** [CHECKLIST_MANUAL_SAIBAI.md](../CHECKLIST_MANUAL_SAIBAI.md) · [GO-LIVE-RUNBOOK-P0.md](./GO-LIVE-RUNBOOK-P0.md)

---

## Tracking Vercel + CAPI {#tracking}

| Componente | Valor | Status |
|------------|-------|--------|
| GA4 | `G-VWX77SGD1W` | PENDING_ACCESS MCP |
| Meta Pixel | `2017630342068049` | Deploy código OK |
| Tracking API | `tracking-eta-eight.vercel.app` | Deploy OK |
| Supabase | `vlqxrmejvkxnlmpqhkvt` | Ativo |
| KPI futuro | `purchase` (70% mídia H2) + WhatsApp B2B (20%) |

**Pendente:** webhook app Saibai Tracking · GA4 API Secret · validar purchase 7 dias

---

## Meta Ads {#meta-ads}

| Campo | Valor |
|-------|-------|
| Ad account | `act_1199864388174624` |
| Campanha ACTIVE | LEADS-GRUPO-WHATS · R$ 20/d |
| Spend 01–25/jun | R$ 158,45 · 405 cliques · 9.468 imp |
| Conv. plataforma | 2.969 ❌ (messaging inflado — não confiar) |
| Campanhas pausadas | 23 (legado Instagram + e-com 2025) |

**Próximo marco:** purchase validado → approval **SB-M-001** Meta Sales D2C

---

## Google Ads {#google-ads}

| Campo | Valor |
|-------|-------|
| Customer ID | `9513237350` |
| MCC Veltrus | `9217486074` — **convite pendente** |
| MCP | Gateway 500 |

---

## Estratégia e-com H2 2026 {#estrategia}

| Fase | Período | Foco | Mídia ref. |
|------|---------|------|------------|
| 0 | Jul/26 | B2B WhatsApp validado | R$ 600 |
| 1 | Ago–Set | Purchase D2C teste | R$ 3–5k/mês |
| 2 | Out–Nov | Escala + RMKT | R$ 8–12k/mês |
| 3 | Dez | Natal peak | R$ 5,2k/mês |

**Doc mestre:** [ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./ESTRATEGIA-ABERTURA-ECOM-H2-2026.md)  
**Resumo diretoria:** [RESUMO-DIRETORIA-ECOM-H2-2026.md](./RESUMO-DIRETORIA-ECOM-H2-2026.md)

---

## Notificações WhatsApp + n8n {#whatsapp}

| Workflow n8n | ID | Função |
|--------------|-----|--------|
| Alertas campanha | `A5gLX8OsP6cHjt4o` | Monitor Meta/Google |
| Resumo account | `qcNWhnAEsaipS5my` | Briefing diário |
| Vendas/purchase | `qhkj95bVNCYliIIZ` | Eventos GA4 |

**Doc:** [SYNC-NOTIFICACOES-2026-06-25.md](./SYNC-NOTIFICACOES-2026-06-25.md)

---

## Arquivos e scripts {#arquivos}

| Path | Conteúdo |
|------|----------|
| `DELIVERY-2026-06-25-dossie-v1.md` | Dossiê v1 |
| `exports/meta-audit-saibai-2026-06-25.json` | Audit Meta |
| `docs/PLATFORMS-AUDIT-2026-06-25.md` | Audit plataformas |
| `CLIENT_CONTEXT.md` | Hub operacional |

---

## Pendências {#pendencias}

| # | Item | Prioridade | Owner |
|---|------|------------|-------|
| 1 | CHECKLIST_MANUAL — GA4 secret · pagamentos · canais | P0 | Cliente |
| 2 | GA4 access property Veltrus MCP | P0 | Cliente |
| 3 | Google MCC convite `9513237350` | P0 | Cliente |
| 4 | Reinstalar app Saibai Tracking (webhook orders) | P0 | Cliente + Veltrus |
| 5 | Validar pixel purchase 7 dias antes SB-M-001 | P1 | Tracking |
| 6 | Growth Pack planilha + sync | P2 | Veltrus |

---

## Vereditos finais

| Área | Veredito |
|------|----------|
| Tema Shopify | **PASS** |
| Tracking código | **PASS** |
| Meta MCP + audit | **PASS** |
| Notificações n8n | **LIVE APROVADO** |
| Go-live merchant | **PRECISA HOTFIX** |
| Google MCP | **PENDING_PERMISSION** |
| GA4 MCP | **PENDING_ACCESS** |

**Próximo marco:** Gate A+B merchant → Fase 0 estratégia jul/26

---

## Notion e Slack {#publicacao}

| Canal | Link |
|-------|------|
| **Hub Notion** | [Empório Saibai — Documentação](https://app.notion.com/p/388968afab6681a0a0e0e5c4070726) |
| **Notificações 25/06** | [Notion 06](https://app.notion.com/p/38a968afab66812abdecf99e6e608fc5) |

**Padrão Veltrus:** Repo `clients/saibai/` = fonte técnica canônica.
