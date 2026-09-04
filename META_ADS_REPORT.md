# Empório Saibai — Relatório Meta Ads

**Atualizado:** 2026-06-25 (re-audit MCP)  
**Fonte:** veltrus-meta-ads-mcp · `meta_ads_build_client_report`  
**Período:** 2026-06-01 → 2026-06-25  
**Veredito:** **PRECISA AUDITORIA** — conv. plataforma infladas · foco legado WhatsApp

## Totais período

| Métrica | Valor |
|---------|------:|
| Investimento | R$ 160,09 |
| Impressões | 9.511 |
| Cliques | 409 |
| CTR | 4,30% |
| CPC médio | R$ 0,39 |
| Conv. plataforma | 2.977 |
| CPA plataforma | R$ 0,05 ❌ |
| ROAS plataforma | 8,86 ❌ |

> **Não confiar** conversões/CPA/ROAS Meta até cruzar com GA4 `purchase` e Events Manager.

## Pixel (MCP 25/06)

| Campo | Valor |
|-------|-------|
| ID | `2017630342068049` |
| Status | ACTIVE |
| Last fired | 2026-06-24 23:37 UTC ✅ |

## Top campanhas (spend)

| ID | Nome | Status | Spend | Cliques | Conv. plat. |
|----|------|--------|------:|--------:|------------:|
| `120248254459350155` | 22.04.2026 [V4] [WB] [LEADS-GRUPO-WHATS] 02 | **ACTIVE** | R$ 132,92 | 379 | 1.913 |
| `120250647777130155` | [SAIBAI] Hortaliças — WhatsApp Direto | PAUSED | R$ 27,17 | 30 | 1.064 |

## Inventário (24 campanhas)

| Tipo | Qtd | Nota |
|------|----:|------|
| ACTIVE | 1 | LEADS-GRUPO-WHATS R$20/d |
| PAUSED | 23 | Legacy Instagram boosts + e-com sales 2025 |
| OUTCOME_LEADS | 3 | WhatsApp grupo |
| OUTCOME_SALES | 4 | E-com direto (pausadas) |
| LINK_CLICKS / ENGAGEMENT | 17 | Boost posts safra |

## Leitura estratégica

1. **Mídia atual ≠ e-commerce Shopify** — campanha ativa otimiza leads WhatsApp, não purchase.
2. **Conv. infladas** — 2.969 provavelmente messaging/on-site events, não vendas.
3. **Legado forte** — 23 campanhas pausadas desde safra 2025; limpar nomenclatura antes de escalar.
4. **Próxima fase** — campanha `[SAIBAI][SALES][D2C][PURCHASE]` → `emporiosaibai.com.br` após tracking purchase validado.

## Próximas ações (sem execução)

| # | Ação | Prioridade |
|---|------|:----------:|
| M-1 | Validar pixel `2017630342068049` Events Manager pós-go-live | P0 |
| M-2 | Pausar/manter LEADS-GRUPO-WHATS conforme estratégia B2B | P1 |
| M-3 | Criar campanha Sales catalogo/advantage+ após purchase GA4 | P1 |
| M-4 | Arquivar campanhas legacy Instagram boost (limpeza conta) | P2 |
| M-5 | UTMs padronizados `utm_source=meta&utm_medium=paid` | P1 |

Export JSON: `exports/meta-audit-saibai-2026-06-25.json`
