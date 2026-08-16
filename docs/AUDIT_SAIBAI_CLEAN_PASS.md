# Auditoria de Código — Saibai Theme (clean pass)

**Branch:** `audit/saibai-clean-theme-pass`
**Escopo:** auditoria de qualidade, modularização, cascata, duplicação e arquivos mortos.
**Regra geral:** preservar 100% da aparência/comportamento; nada publicado na live (theme 186124239166).

> Resumo executivo: o tema está **limpo e bem arquitetado**. Sem leftovers de debug, sem
> referências quebradas, sem snippets mortos. Os itens acionáveis exigem confirmação do
> dono (arquivos nativos Ella) ou já estão tratados em outra PR (Boleto).

## Inventário (Part 1)

| Pasta | Arquivos | Linhas |
|---|---|---|
| assets | 268 | 93.331 |
| blocks | 124 | 45.262 |
| sections | 68 | 20.736 |
| snippets | 184 | 19.951 |
| locales | 4 | 8.906 |
| templates | 28 | 6.242 |
| config | 1 | 3.556 |
| layout | 2 | 269 |
| docs | 10 | 1.924 |

Tipos: 377 liquid · 119 css · 61 svg · 57 js · 34 json · 31 imagens.

## Achados

### Sem problemas
- **Debug/leftovers:** 0 `console.log/debug/debugger/TODO` em JS Saibai.
- **Referências quebradas:** 0 — todos os 184 `render`/`include` apontam para snippets existentes.
- **Snippets mortos:** 0 — todos referenciados.
- **Tracking:** `meta_pixel_id` e `ga4_measurement_id` vazios; `fbq('track','AddToCart')`
  em `sections/main-product.liquid` está **gated por `settings.meta_pixel_id != blank`**
  (inerte hoje → sem risco de add_to_cart duplicado). Consent Mode v2 default em
  `layout/theme.liquid`. App Proxy `/apps/vlt-tracking/events` responde **202**.
- **Proporcionalidade:** cards/hero usam `aspect-ratio` + `object-fit: contain|cover`;
  **nenhum `object-fit: fill`** (sem distorção). `base.css` é carregado async/skip em
  templates Saibai (perf ok).

### Requer confirmação do dono (arquivos nativos Ella — NÃO removidos)
Candidatos a "morto" (basename nunca referenciado), mas são arquivos nativos do tema —
podem ser carregados dinamicamente; **não deletar sem confirmação**:
- `assets/icon-flag.css` (736 linhas)
- `assets/component-menu-drawer.css` (232 linhas)
- `assets/share.js` (56 linhas)

### Intencional (não é defeito)
- **`!important` (897 em CSS Saibai):** arquitetura documentada de override sobre o tema
  nativo Ella. Remover quebraria os overrides.
- **Tokens em 2 arquivos** (`saibai-tokens.css` `:root` + `saibai-shell-kv.css`
  `body.saibai-theme` e seletores `color-scheme` com `!important`): re-asserção proposital
  em níveis de especificidade distintos para vencer o color-scheme do Ella. Valores
  equivalentes (`0.2s ease` ≡ `all 0.2s ease`). Não consolidar sem QA visual.

### Cosmético / baixo risco
- **i18n morto:** `locales/pt-BR.json` → `collection_link: "Comprar agora"` não é
  referenciado em nenhum template (chave órfã herdada do Ella). Inofensivo.
- **Boleto storefront:** removido do tema na PR de pagamentos (footer seal + textos
  PDP/cart). Não duplicado aqui.
- `@keyframes indeterminateAnimation` definido 2x em `assets/animation.css` (nativo).

### Arquivos Saibai > 300 linhas (candidatos a split — recomendação, requer QA)
`saibai-shell-layout.css` (480), `saibai-header.js` (405), `saibai-consent-popup.js` (398),
`saibai-pages-pdp-recs.css` (354), `saibai-pages-pdp-gallery.css` (353),
`saibai-coupon-popup.js` (351), `saibai-pdp-shipping.js` (344), `saibai-services.css` (329),
`saibai-pages-static.css` (310), `saibai-pages-pdp-shipping.css` (309).
Split exigiria atualizar os loaders (`saibai-shell-css`/`saibai-pages-css`/`global-css`)
preservando ordem de cascata + regressão visual. Não aplicado nesta passada.

## Áreas NÃO tocadas (confirmação)
Pagamentos, checkout, taxas, frete, markets, fulfillment, apps, app embeds, legal —
nenhuma alteração. Nada publicado na live.
