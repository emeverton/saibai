# Sprint 4 — Log de alterações

**Loja:** emporiosaibai.myshopify.com  
**Tema:** Ella 7.2.0  
**Data:** 2026-06-06  
**Escopo:** Performance, SEO, Meta Pixel, CRO

---

## Parte A — Performance

| Arquivo | Alteração |
|---------|-----------|
| `layout/theme.liquid` | Preload logo LCP, preconnect CDN, critical-css antes dos CSS |
| `snippets/critical-css.liquid` | **Novo** — tokens + header + hero above-the-fold (~75 linhas) |
| `snippets/image.liquid` | WebP width 800; `is_lcp`/preload → eager + fetchpriority high |
| `snippets/card-product-media.liquid` | Featured 800px webp; eager quando `lazy_load: false` |
| `sections/slideshow.liquid` | Primeiro slide com `is_lcp: true` |
| `assets/saibai-tokens.css` | `prefers-reduced-motion: reduce` |

Scripts em `global-script.liquid` já usam `defer`. Meta Pixel com `defer`.

---

## Parte B — SEO

| Arquivo | Alteração |
|---------|-----------|
| `layout/theme.liquid` | Title pipe `\|`, description com fallback, robots index/follow |
| `snippets/seo-meta.liquid` | **Novo** — Open Graph + Twitter Card |
| `snippets/schema-organization.liquid` | **Novo** — JSON-LD Organization Saibai |
| `snippets/schema.liquid` | Brand → Empório Saibai |
| `sections/main-article.liquid` | JSON-LD Article explícito |

Product schema: `sections/main-product.liquid` → `{% render 'schema' %}` (completo, multi-variant).

---

## Parte C — Tracking

| Arquivo | Alteração |
|---------|-----------|
| `snippets/tracking-meta-pixel.liquid` | **Novo** — PageView condicional a `settings.meta_pixel_id` |
| `config/settings_schema.json` | Campo `meta_pixel_id` |
| `sections/main-product.liquid` | AddToCart via fbq no clique `[name="add"]` |

---

## Parte D — CRO

| Arquivo | Alteração |
|---------|-----------|
| `blocks/buy-buttons.liquid` | Urgência estoque < 10 unidades |
| `snippets/saibai-whatsapp-float.liquid` | z-index 9999 (CSS), aria-label PT ✓ |
| `snippets/cart-checkout.liquid` | Trust line acima do checkout |
| `snippets/cart-drawer.liquid` | Trust line no drawer |
| `assets/saibai-tokens.css` | `.saibai-urgency`, `.saibai-cart-trust` |

---

## Validação

```bash
grep -E "critical-css|seo-meta|schema-organization|tracking-meta-pixel" layout/theme.liquid
grep "prefers-reduced-motion" assets/saibai-tokens.css
grep "meta_pixel_id" config/settings_schema.json
grep "saibai-urgency\|saibai-cart-trust" assets/saibai-tokens.css blocks/ snippets/
grep "is_lcp\|width: 800" snippets/image.liquid snippets/card-product-media.liquid
```

---

## Ação no admin

1. **Theme settings → Saibai Tracking** — inserir Meta Pixel ID
2. **GTmetrix/PageSpeed** — validar LCP após deploy (hero slideshow + preload logo)
3. **Meta Events Manager** — testar PageView + AddToCart no preview
