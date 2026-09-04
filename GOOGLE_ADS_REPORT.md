# Empório Saibai — Relatório Google Ads

**Atualizado:** 2026-06-25 (re-audit MCP)  
**Fonte:** veltrus-google-ads-mcp  
**Veredito:** **PENDING_PERMISSION** — MCC não linked · gateway 500

## Status conta

| Campo | Valor | Status |
|-------|-------|--------|
| customerId | `9513237350` | Registry OK |
| Nome | Saibai Saladas | — |
| MCC Veltrus | `9217486074` | **invite pending** |
| Em `allowedCustomers` gateway | ✅ Sim | — |
| Em contas acessíveis MCP | ❌ Não | **Não linkada** |
| MCP `google_ads_build_client_report` | gateway 500 | ❌ 25/06 |
| MCP `google_ads_get_campaigns` | gateway 500 | ❌ 25/06 |
| MCP `google_ads_get_conversions` | gateway 500 | ❌ 25/06 |

## Bloqueio

A conta Google Ads Saibai **não está linkada** ao MCC Veltrus. Sem o aceite do convite, não é possível auditar campanhas, conversões ou spend via MCP.

## Ação requerida (merchant)

1. Aceitar convite MCC Veltrus na conta `9513237350`
2. Confirmar acesso editor para automação Veltrus
3. Revalidar MCP após link

## Plano pós-MCC (proposto)

| Campanha | Tipo | Objetivo | Budget ref. |
|----------|------|----------|------------:|
| `[SAIBAI][PMAX][D2C][BR]` | Performance Max | Purchase (import GA4) | R$ 40–60/d |
| `[SAIBAI][SEARCH][BRAND]` | Search | Marca Saibai/alcachofra | R$ 15/d |
| `[SAIBAI][SEARCH][B2B][SP]` | Search | Restaurantes SP | R$ 20/d |

**Pré-requisito:** GA4 `purchase` como conversão primária + Merchant Center feed Shopify.

## Próximo passo

Após MCC linked → rodar `google_ads_build_client_report` + `google_ads_get_conversions` e atualizar este relatório.
