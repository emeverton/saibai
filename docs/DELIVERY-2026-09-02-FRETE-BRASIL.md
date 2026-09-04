# Empório Saibai — Frete Brasil LIVE (02/09/2026)

**Veredito:** **LIVE APROVADO** (tema + shipping profile)  
**Tema live:** `#187189297470` · `veltrus-saibai-consolidated-2026-08-08`  
**Ticket origem:** clientes não encontram frete · abrir cobertura Brasil

---

## Causa raiz (corrigida 02/09/2026 ~19h)

Três camadas. Tema e Frenet painel **não** bloqueavam Brasil. A cotação sumia no Shopify.

1. **Gate do tema** — allowlist só Sudeste / 34 bairros. **Corrigido no live** (Brasil 27 UFs + DF + aviso fora de SP).
2. **Frenet painel** — PAC/Sedex já cotavam Brasil (ex.: DF `70040-010` PAC R$ 37,11 / Sedex R$ 62,93).
3. **Perfil de entrega Shopify (o buraco real)** — o catálogo inteiro (17 variantes: T8/T12/T16/T20, P/M/G/MINI, conservas, chaveiro, flores) estava no perfil **Entrega Local - Sorocaba** `#131706749246`, zona sem métodos de transportadora. Só Local Delivery nativo (R$ 39) em SP capital. Fora disso: `shipping_rates: []`. O perfil **General** `#123914125630` já tinha Frenet + Loggi na zona América do Sul, mas **nenhum produto de alcachofra usava esse perfil**.

**Hotfix Admin (02/09):** `variantsToDissociate` do perfil Sorocaba → catálogo volta ao General. Frenet com `participantServices` PAC + Sedex ativos.

Smoke Admin `draftOrderAvailableDeliveryOptions` (T8, 1 un.):

| CEP | Antes | Depois |
|-----|-------|--------|
| `01310-100` SP | só Local Delivery R$ 39 | PAC R$ 29,89 · Loggi R$ 30,66 · Sedex R$ 35,48 · Local Delivery R$ 39 |
| `70040-010` DF | `[]` | Loggi R$ 34,76 · PAC R$ 37,11 · Sedex R$ 62,93 |
| `80010-000` PR | `[]` | Loggi R$ 31,41 · PAC R$ 37,11 · Sedex R$ 62,93 |

PAC/Sedex DF batem com o simulador Frenet.

## O que mudou no tema (local)

| Item | Antes | Depois |
|------|-------|--------|
| Gate checkout | Sudeste SP/RJ/MG/ES | **Brasil** (27 UFs + DF) |
| Copy PDP/política/carrinho | “todo o Sudeste” / 34 bairros | “todo o Brasil” |
| CSV Flex Frete | 4 UFs Sudeste | 27 UFs + DF |
| Meta Ads | — | **sem mutation** |

## Arquivos

- `theme/assets/saibai-delivery.js`
- `theme/assets/saibai-delivery-zones.js`
- `theme/assets/saibai-pdp-shipping.js`
- `theme/snippets/saibai-cart-policy.liquid`
- `theme/snippets/saibai-delivery-zones.liquid`
- `theme/snippets/saibai-pdp-shipping.liquid`
- `theme/snippets/saibai-pdp-accordions.liquid`
- `theme/snippets/cart-shipping-calculator.liquid`
- `theme/snippets/saibai-policy-entrega.liquid`
- `exports/flex-frete-cep-ranges-saibai.csv`
- `docs/FLEX-FRETE-CEP-ZONAS-SAIBAI-2026-07-29.md`

## Deploy

**LIVE** `veltrus-saibai-consolidated-2026-08-08` `#187189297470` · 02/09/2026  
Autorização: “publicar agora”. 9 arquivos via Admin GraphQL `themeFilesUpsert`.

HTML live PDP (sem cookie de preview): `Entrega refrigerada em todo o Brasil` · `Sudeste` = 0.

## QA

1. CEP `01310-100` (Bela Vista/SP) → PAC R$ 29,89 · Loggi R$ 30,66 · Sedex R$ 35,48 · Local Delivery R$ 39  
2. CEP `70040-010` (DF) → Loggi R$ 34,76 · PAC R$ 37,11 · Sedex R$ 62,93 + aviso fora de SP · **PDP live confirmado**  
3. CEP `80010-000` (PR) → Loggi R$ 31,41 · PAC R$ 37,11 · Sedex R$ 62,93  
4. Checkout: produtos agora no perfil General (32 variantes). Perfil Sorocaba ficou com 0 produtos.
