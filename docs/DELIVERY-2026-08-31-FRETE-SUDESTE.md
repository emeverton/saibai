# Empório Saibai — Frete Sudeste LIVE (código local 31/08/2026)

**Veredito:** **LIVE APROVADO** · tema `#187189297470`  
**Ticket origem:** e-mail Fragata Jr — CEP `04520-000` Av. Juriti 246 Moema (ViaCEP: Vila Uberabinha)  
**Pendente:** Clara cadastrar faixas Sudeste no Flex Frete (CSV canônico)

---

## O que mudou

| Item | Antes | Depois |
|------|-------|--------|
| Gate checkout | 34 bairros SP + Sorocaba | **Sudeste** SP/RJ/MG/ES |
| CEP Moema 04520 | ❌ fora 04077–04094 | ✅ UF SP |
| Copy PDP/política/carrinho | “bairros selecionados” | “todo o Sudeste” |
| CSV Flex Frete | 34 linhas | 4 UFs |
| Meta Ads | — | **sem mutation** (AS SP ACTIVE intactos) |

## Arquivos

- `theme/assets/saibai-delivery-zones.js` (v2 · STORAGE_KEY)
- `theme/assets/saibai-pdp-shipping.js`
- `theme/snippets/saibai-pdp-shipping.liquid`
- `theme/snippets/saibai-pdp-accordions.liquid`
- `theme/snippets/cart-shipping-calculator.liquid`
- `theme/snippets/saibai-policy-entrega.liquid`
- `exports/flex-frete-cep-ranges-saibai.csv`
- `exports/flex-frete-cep-ranges-saibai-34-bairros-LEGACY.csv`
- `docs/FLEX-FRETE-CEP-ZONAS-SAIBAI-2026-07-29.md`

## Deploy

**LIVE** `veltrus-saibai-consolidated-2026-08-08` `#187189297470` · 31/08/2026

Arquivos publicados:
- `assets/saibai-delivery-zones.js` + `snippets/saibai-delivery-zones.liquid` (loader restaurado)
- `assets/saibai-delivery.js` + `snippets/saibai-cart-policy.liquid` (Sudeste)
- copy PDP/política/carrinho

CDN cart: `saibai-delivery-zones.js` com `SUDESTE_UFS` ✅

```bash
# referência (já executado via Admin GraphQL themeFilesUpsert)
cd clients/saibai/theme
shopify theme push --store byinbz-0k --theme 187189297470 --allow-live \
  --only assets/saibai-delivery-zones.js \
  --only snippets/saibai-delivery-zones.liquid \
  --only assets/saibai-delivery.js \
  --only snippets/saibai-cart-policy.liquid \
  --only assets/saibai-pdp-shipping.js \
  --only snippets/saibai-pdp-shipping.liquid \
  --only snippets/saibai-pdp-accordions.liquid \
  --only snippets/cart-shipping-calculator.liquid \
  --only snippets/saibai-policy-entrega.liquid
```


## QA

1. CEP `04520-000` → gate OK · checkout liberado  
2. CEP `20040-020` (RJ) → OK  
3. CEP `30130-000` (MG) → OK  
4. CEP `70040-010` (DF) → bloqueado  
5. Flex Frete Clara: cotação Sudeste após cadastrar CSV
