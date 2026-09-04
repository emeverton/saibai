# Empório Saibai — Relatório GA4

**Atualizado:** 2026-06-25  
**Veredito:** **PENDING_ACCESS** — measurement ID conhecido · property fora do MCP Veltrus

## Identificadores

| Campo | Valor | Status |
|-------|-------|--------|
| measurementId | `G-VWX77SGD1W` | Confirmado checklist/manual |
| propertyId | — | **Não listado** em `ga4_list_properties` MCP |
| clientKey | `saibai` | Registry: `not_found` |

## Bloqueio

A propriedade GA4 do Empório Saibai **não aparece** na conta Google Analytics acessível pelo veltrus-analytics-mcp (27 properties listadas, jun/2026). Sem propertyId numérico, não é possível rodar `ga4_build_client_report`.

## Ação requerida

1. No GA4 Admin → **Access Management** → adicionar conta de serviço/usuário Veltrus com role Viewer+
2. Confirmar que a property correta é a do stream `G-VWX77SGD1W`
3. Atualizar `docs/agents/VELTRUS-GA4-REGISTRY.json` com propertyId
4. Revalidar MCP

## Eventos esperados (pós-go-live)

| Evento | Tipo | Uso |
|--------|------|-----|
| `purchase` | Key event | KPI e-commerce primário |
| `add_to_cart` | Evento | Funil CRO |
| `begin_checkout` | Evento | Funil checkout |
| `view_item` | Evento | PDP performance |
| `generate_lead` | Key event opcional | B2B contato |

## KPI recomendado

**Primário:** `purchase` (receita + transações)  
**Secundário:** `add_to_cart` rate · AOV · canal Paid Social vs Paid Search  
**B2B:** cliques WhatsApp float · página Contato

## Próximo passo

Após acesso concedido:

```txt
ga4_build_client_report clientKey=saibai propertyId=<ID> dateFrom=2026-06-01 dateTo=2026-06-25
```

Salvar export em `exports/ga4-build-client-report-2026-06-01-25.json`
