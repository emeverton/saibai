# Sprint 5 — Log de limpeza final

**Loja:** emporiosaibai.myshopify.com  
**Tema:** Ella 7.2.0 + customização Saibai v1.0.0  
**Data:** 2026-06-06  
**Escopo:** Auditoria, segurança IP, botões, ícones, textos, SVGs, theme check

---

## 1. Auditoria e limpeza

| Item | Ação |
|------|------|
| `assets/saibai-tokens.css` | Consolidado 355 → **129 linhas** (regras duplicadas removidas) |
| `assets/global.js` | Removido `console.log` Halothemes branding |
| `assets/product-bundle.js` | Removidos 2× `console.log` debug |
| `assets/product-info.js` | Removido `console.log` fetch abort |
| `assets/quick-add-bulk.js` | Removido `console.log` em catch |
| `snippets/global-script.liquid` | `window.info` → Empório Saibai / Veltrus |
| `config/settings_schema.json` | Corrigida vírgula trailing em `t:content.fonts` |

**Nota:** `console.error` em assets Ella (cart.js, edit-cart.js) mantidos — tratamento de erro em produção, não debug.

---

## 2. Cabeçalho IP (Veltrus)

Aplicado em:
- `layout/theme.liquid`
- `assets/saibai-tokens.css`
- Todos os `snippets/saibai-*.liquid`
- `snippets/critical-css.liquid`, `seo-meta.liquid`, `schema-organization.liquid`, `tracking-meta-pixel.liquid`

---

## 3. Verificação de botões

| Página | Botão | Destino | Status |
|--------|-------|---------|--------|
| Home | Ver coleção | `/collections/todos` | OK |
| Home | Conhecer a fazenda | `/pages/sobre` | OK (página criada via API) |
| Home | Comprar agora (header) | `/collections/todos` | OK |
| Home | Sou restaurante | `/pages/contato` | OK |
| Home | Ver coleção (conservas) | `/collections/todos` | OK (corrigido de `/collections/conservas`) |
| Collection | Filtros / paginação | Nativo Ella | OK (Liquid routes) |
| Product | Adicionar ao carrinho | `routes.cart_add_url` | OK |
| Cart / Drawer | Finalizar compra | Shopify checkout | OK |
| Cart / Drawer | Continuar comprando | `routes.root_url` / collections | OK |
| Institucionais | CTAs internos | `/pages/sobre`, `/pages/contato`, políticas | OK |

**Links quebrados encontrados:** 1 — `/collections/conservas` (coleção inexistente) → corrigido para `/collections/todos`.

**Não implementados na home (Ella nativo):** botões do slideshow hero e editorial-collections vêm do Theme Editor — validar visualmente após push.

---

## 4. Verificação de ícones

| Ícone | Status |
|-------|--------|
| Cart + bubble quantidade | OK — nativo Ella header |
| Search | OK — `settings.predictive_search_enabled` |
| Account | OK — header icon |
| WhatsApp footer | OK — link Grupo VIP |
| WhatsApp float | OK — z-index 9999, aria-label PT |
| Social Instagram/Facebook/YouTube | OK — links em `settings_data.json` |
| Hover `--color-primary` | OK — `saibai-tokens.css` unificado |
| Footer social hover | OK — `#76BD22` em `footer-group.json` |

---

## 5. Verificação de textos

| Check | Resultado |
|-------|-----------|
| Demo SF / mail@domain / HALOTHEMES | **0** em templates ativos Saibai |
| `Welcome to our store!` | Presente apenas em `primary_text` (typing animation inativa) — não visível |
| HTML entities visíveis | Nenhum em snippets Saibai |
| Inglês visível PDP/collection | Strings via `locales/pt-BR.json` |

---

## 6. SVGs

| Item | Ação |
|------|------|
| `assets/icon-inventory-status.svg` | Adicionado `viewBox="0 0 15 15"` + width/height |
| Demais SVGs em `assets/` | viewBox presente (audit: 1 exceção corrigida) |
| Selos footer | Pix, Visa, Mastercard, **Amex**, Elo, Boleto via `payment_type_svg_tag` width/height 40×24 |

---

## 7. Imagens

| Item | Status |
|------|--------|
| Placeholders Ella clothing | Apenas em templates demo não usados (landing-1/2/3) — **fora do fluxo Saibai** |
| Home custom sections | Gradientes Saibai (sem demo clothing) |
| Alt text logos | `Empório Saibai` em `saibai-logo.liquid` |
| Cards produto | aspect-ratio 1:1, object-fit cover |

---

## 8. Shopify Theme Check

```
649 files inspected | 406 offenses | 23 errors | 383 warnings
```

### Erros corrigidos (Saibai)

| Arquivo | Erro | Fix |
|---------|------|-----|
| `snippets/saibai-logo.liquid` | ImgWidthAndHeight | Adicionado `height` |
| `config/settings_schema.json` | ValidSchema (trailing comma) | Vírgula removida |
| `assets/icon-inventory-status.svg` | viewBox ausente | Corrigido |

### Erros remanescentes (Ella vendor — 21)

- `LiquidHTMLSyntaxError` em blocks/sections nativos Ella
- `ValidSchemaTranslations` — chaves schema sem tradução pt-BR
- `ValidVisibleIf`, `ValidBlockTarget`, `TranslationKeyExists`
- Não alterados — risco de regressão no tema base

---

## 9. Configurações adicionadas

```json
"social_instagram_link": "https://www.instagram.com/saibaisaladas/",
"social_facebook_link": "https://web.facebook.com/saladas.saibai",
"social_youtube_link": "https://www.youtube.com/@emporiosaibai"
```

---

## Validação final

```bash
wc -l assets/saibai-tokens.css                    # 129
grep -r "685 Market\|mail@domain\|HALOTHEMES" templates/index.json templates/page.sobre.json sections/footer-group.json  # 0
grep -c "console.log" assets/global.js assets/product-bundle.js assets/product-info.js assets/quick-add-bulk.js  # 0
shopify theme check 2>&1 | grep saibai-logo         # 0 errors
grep "Empório Saibai — Tema Oficial" snippets/saibai-*.liquid layout/theme.liquid assets/saibai-tokens.css
```

---

## Ação pós-deploy

1. Theme Editor → confirmar slideshow hero sem CTAs demo
2. Testar `/collections/todos` e checkout em preview
3. Configurar Meta Pixel ID se ainda vazio
4. Validar YouTube URL real se handle `@emporiosaibai` diferir
