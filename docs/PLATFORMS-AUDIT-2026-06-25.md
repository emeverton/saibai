# Empório Saibai — Auditoria Plataformas Meta + Google

**Data:** 2026-06-25  
**Fonte:** veltrus-meta-ads-mcp · veltrus-google-ads-mcp · veltrus-analytics-mcp  
**Veredito:** **PRECISA AUDITORIA** — Meta operacional · Google bloqueado MCC · GA4 sem acesso Veltrus

---

## Resumo executivo

| Plataforma | MCP | Veredito | Bloqueio |
|------------|-----|----------|----------|
| **Meta Ads** | ✅ LIVE | **PRECISA AUDITORIA** | Mídia ≠ purchase e-com |
| **Google Ads** | ❌ gateway 500 | **PENDING_PERMISSION** | MCC `9513237350` não linked |
| **GA4** | ⚠️ parcial | **PENDING_ACCESS** | `G-VWX77SGD1W` fora do MCP |

**Regra de ouro:** KPI e-commerce = GA4 `purchase`. Não otimizar com conv. Meta messaging (2.977 no período).

---

## Meta Ads — snapshot 01–25/06/2026

| Métrica | Valor | Leitura |
|---------|------:|---------|
| Investimento | R$ 160,09 | +R$ 1,64 vs audit anterior |
| Impressões | 9.511 | — |
| Cliques | 409 | CTR 4,30% |
| CPC médio | R$ 0,39 | Eficiente para leads |
| Conv. plataforma | 2.977 | ❌ **Infladas** (WhatsApp/messaging) |
| CPA plataforma | R$ 0,05 | ❌ **Não confiar** |
| ROAS plataforma | 8,86 | ❌ **Não confiar** |

### Campanhas com spend no período

| Campanha | Status | Objetivo | Budget | Spend | Conv. plat. |
|----------|--------|----------|-------:|------:|------------:|
| `120248254459350155` LEADS-GRUPO-WHATS 02 | **ACTIVE** | OUTCOME_LEADS | R$ 20/d | R$ 132,92 | 1.913 |
| `120250647777130155` Hortaliças WhatsApp | PAUSED | ENGAGEMENT | — | R$ 27,17 | 1.064 |

### Inventário conta (24 campanhas)

| Status | Qtd |
|--------|----:|
| ACTIVE | 1 |
| PAUSED | 23 |

| Objetivo | Qtd | Nota |
|----------|----:|------|
| OUTCOME_LEADS | 3 | WhatsApp grupo B2B |
| OUTCOME_SALES | 4 | E-com 2025 (pausadas) |
| LINK_CLICKS / ENGAGEMENT / outros | 17 | Boost Instagram safra |

### Campanha ativa — detalhe

| Campo | Valor |
|-------|-------|
| ID | `120248254459350155` |
| Nome | `22.04.2026 [V4] [WB] [LEADS-GRUPO-WHATS] 02` |
| Budget | R$ 20/dia |
| Adset ativo | `ADV - [IG] [FB] [30+] [SP METROPOLE] VÁRIOS` |
| Otimização | OFFSITE_CONVERSIONS (WhatsApp grupo) |
| Geo | SP metropolitana · 30+ |

### Pixel

| Campo | Valor |
|-------|-------|
| ID | `2017630342068049` |
| Nome | Pixel - Saibai |
| Status | **ACTIVE** |
| Last fired | 2026-06-24 23:37 UTC ✅ |

Pixel dispara na loja — falta validar evento **Purchase** server-side pós-go-live tracking.

---

## Google Ads — snapshot

| Campo | Valor | Status |
|-------|-------|--------|
| customerId | `9513237350` | Registry OK |
| Nome | Saibai Saladas | — |
| MCC Veltrus | `9217486074` | **invite pending** |
| Na lista `allowedCustomers` | ✅ Sim | — |
| Na lista contas acessíveis MCP | ❌ **Não** | Bloqueio link |
| `google_ads_build_client_report` | gateway 500 | ❌ |
| `google_ads_get_campaigns` | gateway 500 | ❌ |
| `google_ads_get_conversions` | gateway 500 | ❌ |

**Diagnóstico:** conta está no allowlist do gateway, mas **não linkada ao MCC** — API retorna 500 em todas as rotas de dados.

### Ação merchant (desbloqueio)

1. Login Google Ads conta `9513237350`
2. Aceitar convite MCC Veltrus (`9217486074`)
3. Confirmar permissão **Standard** ou **Admin** para automação
4. Avisar Veltrus → revalidar MCP

### Plano pós-MCC (proposto — não executar antes purchase GA4)

| Campanha | Tipo | Budget ref. | KPI |
|----------|------|------------:|-----|
| `[SAIBAI][PMAX][D2C][BR]` | Performance Max | R$ 50/d | purchase |
| `[SAIBAI][SEARCH][BRAND]` | Search | R$ 15/d | marca |
| `[SAIBAI][SEARCH][B2B][SP]` | Search | R$ 20/d | leads B2B |

---

## GA4 — snapshot

| Campo | Valor | Status |
|-------|-------|--------|
| measurementId | `G-VWX77SGD1W` | Confirmado tema/registry |
| propertyId MCP | — | **Não listada** (27 properties Veltrus, zero Saibai) |
| Purchase server-side | Código deployado | **GA4_API_SECRET pendente** |

Sem GA4 MCP não há cruzamento Meta spend × purchase real.

---

## Matriz de decisão (próximos 30 dias)

### Fase 0 — Desbloqueio (merchant + Veltrus)

| # | Ação | Quem | Desbloqueia |
|---|------|------|-------------|
| 0.1 | GA4 API Secret → Vercel | Merchant + Veltrus | Purchase server-side |
| 0.2 | Aceitar MCC Google `9513237350` | Merchant | Google Ads MCP |
| 0.3 | Conceder GA4 property Veltrus | Merchant | GA4 MCP |
| 0.4 | Canais Shopify Google/Meta + pixel checkout | Merchant | Browser + checkout events |
| 0.5 | Pedido teste pago | Conjunto | Baseline purchase |

### Fase 1 — Meta (após purchase validado)

| # | Ação | Tipo | Budget |
|---|------|------|-------:|
| 1.1 | Criar `[SAIBAI][SALES][D2C][PURCHASE]` | Advantage+ / catálogo | R$ 40/d |
| 1.2 | UTMs padronizados `utm_source=meta&utm_medium=paid` | Config | — |
| 1.3 | Decidir LEADS-GRUPO-WHATS: manter R$ 20/d B2B ou pausar | Diretoria | — |
| 1.4 | Arquivar 17 campanhas boost Instagram 2025 | Limpeza | — |

Ver `APPROVAL_REQUESTS.md` — SB-M-001 a SB-M-003.

### Fase 2 — Google (após MCC + purchase)

| # | Ação | Tipo | Budget |
|---|------|------|-------:|
| 2.1 | Auditar conta existente via MCP | Diagnóstico | — |
| 2.2 | PMax feed Shopify | Performance Max | R$ 50/d |
| 2.3 | Search marca Saibai/alcachofra | Search | R$ 15/d |

Ver `APPROVAL_REQUESTS.md` — SB-G-001 a SB-G-002.

---

## Vereditos

| Área | Veredito |
|------|----------|
| Meta MCP leitura | **PASS** |
| Meta estratégia vs e-com | **PRECISA AUDITORIA** |
| Meta pixel firing | **PASS** (last fired 24/06) |
| Google Ads MCP | **PENDING_PERMISSION** |
| GA4 MCP | **PENDING_ACCESS** |
| Mutations ads | **BLOQUEADO** (pré purchase GA4) |

---

## Referências

- [META_ADS_REPORT.md](../META_ADS_REPORT.md)
- [GOOGLE_ADS_REPORT.md](../GOOGLE_ADS_REPORT.md)
- [GA4_REPORT.md](../GA4_REPORT.md)
- [CAMPAIGN_OPTIMIZATION_STRATEGY.md](../CAMPAIGN_OPTIMIZATION_STRATEGY.md)
- [GO-LIVE-RUNBOOK-P0.md](./GO-LIVE-RUNBOOK-P0.md)

---

## Notion e Slack {#publicacao}

| Canal | Link |
|-------|------|
| **Hub Notion** | [Empório Saibai — Documentação Técnica](https://app.notion.com/p/38a968afab6681bb8a03e2d2e6848147) |
| **Auditoria 25/06** | [01 — Auditoria Plataformas](https://app.notion.com/p/38a968afab66814b9587f7a9338accd9) |
| **Notificações 25/06** | [06 — WhatsApp + n8n](https://app.notion.com/p/38a968afab66812abdecf99e6e608fc5) |
| **Slack ops** | [#ops-clientes · notificações](https://veltrus.slack.com/archives/C0BA1AA7D7U/p1782390207622889) |
| **Slack cliente** | [#cliente-saibai · notificações](https://veltrus.slack.com/archives/C0BD28VMD4N/p1782390172841209) |

**Padrão Veltrus:** Slack = resumo + link Notion. Repo `clients/saibai/` = fonte técnica canônica.
