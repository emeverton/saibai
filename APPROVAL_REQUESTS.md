# Empório Saibai — Approval Requests

**Atualizado:** 2026-08-26  
**Fluxo:** `create_request → approve → execute(confirm:true)`

---

## Fila ativa

| ID | Tipo | Descrição | Pré-requisito | Status |
|----|------|-----------|---------------|--------|
| **SB-S-002** | Shopify catálogo | Pacote padrão Clara: **30×14×50 cm · 5 kg todas** | Pesos API ✅ · Dimensões merchant ✅ | **LIVE** 21/07 |
| **SB-S-001** | Shopify tema | Limite **2 caixas** alcachofra fresca (`Alcachofra In Natura`) por pedido — pedido Clara 16/07 | Auth CLI + push live | **LIVE** 21/07 · tema `#186796147006` |
| **SB-CRM-001** | Shopify CRM | Cupons `5%NOVOCLIENTE` + `SAIBAIRECOMPRA` + tema popup/carrinho | Push live `#187189297470` | **LIVE** 26/08 |
| **SB-S-003** | Shopify frete | Abrir gate Sudeste (SP/RJ/MG/ES) — fix CEP Moema `04520-000` | Push tema + Flex Frete Clara | **LIVE** 31/08 · `#187189297470` · Flex Frete Clara **ainda pendente** |
| **SB-S-004** | Shopify frete | Abrir gate **Brasil** (27 UFs) — clientes não encontram frete | Push tema + auditoria Frenet | **LIVE** 02/09 · `#187189297470` · Frenet PAC/Sedex **já cotam Brasil**; checkout sem taxa = app Shopify/Flex Frete ou instabilidade Correios |
| **SB-CRM-003** | Shopify recuperação | Fatura checkout abandonado 14d — frete Brasil liberado | Tag `saibai-recup-frete-20260902` · drafts #D30–#D64 | **ENVIADO** 02/09 · 35/35 |
| **SB-CRM-002** | Shopify Email | Ligar automações Welcome / cart / checkout / win-back | Clique Admin · playbook CRM nativo | **PENDENTE** (API marketing ACCESS_DENIED) |
| **SB-M-001** | Meta | `[SAIBAI][SALES][D2C][PURCHASE] · R$1.500/mês` | Campanha+AS+**8 ads** | **ACTIVE** |
| **SB-M-004** | Meta | `[SAIBAI][RMKT][D2C][ATC] · R$15/d` · 2 ads vinculados | Campanha+AS+ads ACTIVE (review IN_PROCESS) | **ACTIVE** 26/08 |
| SB-M-002 | Meta | Pausar LEADS-GRUPO-WHATS (realocar budget) | Decisão diretoria B2B | **PENDENTE** |
| SB-M-003 | Meta | Arquivar campanhas legacy Instagram 2025 | — | **PENDENTE** |
| SB-G-001 | Google | Aceitar MCC + auditar conta | Convite merchant | **BLOQUEADO** |
| SB-G-002 | Google | Criar PMax feed Shopify | MCC + purchase GA4 | **BLOQUEADO** |
| SB-T-001 | Tracking | Configurar GA4_API_SECRET Vercel | Secret merchant | **BLOQUEADO** |
| SB-T-002 | Shopify | Push tema se alterações locais | CLI auth | **LIVE** 26/08 · `#187189297470` |

### SB-S-001 — detalhe

**Pedido:** Clara (16/07/2026) — “limitar caixas de alcachofra a duas por pedido”.

**Escopo interpretado:** máximo **2 unidades agregadas** por pedido em todos os SKUs `product_type = Alcachofra In Natura` (T8/T12/T16/T20/P/M/G/MINI). Conservas e outros produtos **sem** limite.

**Código local (pronto):**
- `theme/assets/saibai-cart-limits.js`
- `theme/snippets/saibai-cart-limits.liquid`
- `theme/layout/theme.liquid` (loader)
- `theme/snippets/quantity-selector.liquid` + `cart-products.liquid` (UX max)

**Deploy:**
```bash
cd clients/saibai/theme
# reauth se token expirado:
../ops/scripts/shopify-auth-full.sh
shopify theme push --store byinbz-0k --theme 186124239166 --only assets/saibai-cart-limits.js --only snippets/saibai-cart-limits.liquid --only layout/theme.liquid --only snippets/quantity-selector.liquid --only snippets/cart-products.liquid
```
⚠️ Sem `--allow-live` até autorização explícita. Preferir push em tema draft/preview primeiro.

**QA smoke:**
1. Adicionar 2 caixas In Natura → OK
2. Tentar 3ª (mesmo ou outro SKU) → mensagem de limite
3. Conserva + 2 caixas → OK
4. Carrinho: aumentar qty acima do teto → bloqueado

---

## Template create_request

```txt
Cliente: saibai
Tipo: meta_ads_create_campaign_request | google_ads_create_search_campaign_request
Descrição: [ação específica]
Budget: R$ X/dia
KPI: purchase (GA4)
Pré-check: TRACKING_AUDIT.md gate de escala ✅
Aprovação: [nome] · [data]
```
