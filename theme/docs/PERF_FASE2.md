# Performance — Fase 2 (Jun/2026)

**Escopo acordado:** manter YouTube lazy no hero até trocar por imagem estática.  
**Foco:** `base.css` legado (461 KB) + LCP do poster WebP.

---

## Diagnóstico base.css legado

| Arquivo | Tamanho | Render-blocking (antes) | Uso Saibai |
|---------|---------|-------------------------|------------|
| `base.css` | **461 KB** | Sim, todas as páginas | Legado base theme — home 100% `saibai-*` |
| `vendor.css` | 15 KB | Sim | Variáveis + reset mínimo |
| `vendor.js` | 183 KB | defer | Cart drawer, modais base |
| `global.js` | 186 KB | defer | Core base theme |
| `animation.css` | 5 KB | async print | Scroll reveal — não usado na home |

**Referências no base.css (135+ ocorrências):** quick-view, wishlist, compare, lookbook, countdown, floating icons, blog, preload screen, multitasking bar — **desativados ou substituídos** no fluxo Saibai, mas o CSS ainda baixa.

**Home (`index.json`):** só sections `saibai-*` — nenhuma section base nativa. Seguro adiar `base.css` + `vendor.css` na home.

---

## Otimizações aplicadas (Fase 2a)

| Mudança | Arquivo | Impacto esperado |
|---------|---------|------------------|
| `base.css` + `vendor.css` async na home | `snippets/global-css.liquid` | FCP −1~3s (461 KB fora do critical path) |
| Preload poster hero WebP | `layout/theme.liquid` | LCP usa imagem local, não YouTube |
| Removido preconnect YouTube na home | `layout/theme.liquid` | Evita conexão antecipada ao embed |
| Critical CSS reserva 16:9 do hero | `snippets/critical-css.liquid` | CLS/FOUC até CSS modular carregar |
| `animation.css` omitido na home | `snippets/global-css.liquid` | −5 KB async |
| `animations.js` omitido na home | `snippets/global-script.liquid` | −JS scroll reveal desnecessário |

**YouTube:** mantido com `data-src` + IntersectionObserver + `requestIdleCallback` (`saibai-hero.js`). Só carrega quando o hero entra no viewport — **não compete com LCP** (poster WebP é o LCP).

---

## Admin — desativar manualmente (Theme settings)

Recomendado desligar no customizer (Theme settings) se ainda estiverem ativos:

1. **Preloading screen** — atrasa first paint
2. **Floating icons** — JS + CSS extra
3. **Countdown nos cards** — CSS/JS condicional
4. **Reveal on scroll** — home não precisa

---

## Fase 2b (aplicada 09/06/2026)

| Mudança | Arquivo | Impacto |
|---------|---------|---------|
| Poster hero responsivo (800/1200 WebP) | `saibai-hero-fresca-*.webp`, `saibai-home-hero.liquid` | LCP mobile −50% bytes (~103 KB vs 205 KB) |
| Preload com `media` por breakpoint | `layout/theme.liquid` | Preload certo por viewport |
| YouTube só após clique play/mute | `saibai-hero.js` | Zero iframe no load inicial |
| Removido CSS Saibai duplicado no footer | `layout/theme.liquid` | −2 requests duplicados |
| `snippets/saibai-pages-css.liquid` async na home | `global-css.liquid` | Fora do critical path index |
| `base.css` async na PLP (collection) | `global-css.liquid` | −461 KB blocking em coleções |
| Cards produto max 600px | `saibai-prod-card.liquid` | −~300 KB transfer home |

## Fase 2c (aplicada 09/06/2026)

| Mudança | Arquivo | Impacto |
|---------|---------|---------|
| `base.css` async em PDP, cart, search, page, blog, 404 | `saibai-perf-flags.liquid`, `global-css.liquid` | −461 KB blocking em 9 templates |
| `snippets/saibai-pages-css.liquid` async em PLP, cart, search, inst, 404 | `global-css.liquid` | Fora do critical path (PDP mantém sync) |
| Removido `text-animation.js` global | `global-script.liquid` | −JS decorativo base theme em todas as páginas |
| Critical CSS PLP + PDP | `critical-css.liquid` | Menos FOUC com base async |
| Settings live: preload/float/anim OFF | `settings_data.json` (current) | Já desligado no tema publicado |

## Fase 2d (aplicada 08/06/2026)

| Mudança | Arquivo | Impacto |
|---------|---------|---------|
| Skip total `base.css` + `vendor.css` em templates Saibai-only | `global-css.liquid` | −476 KB em index, blog, page, 404, etc. |
| Utilities drawer/cart mínimas | `snippets/saibai-shell-css.liquid` | Compensa base.css removido |
| CLS popups zero-altura | `saibai-consent/coupon-*`, `critical-css.liquid` | GTmetrix CLS 1.09 → meta &lt;0.1 |
| Removido `snippets/saibai-pages-css.liquid` duplicado no `<noscript>` | `global-css.liquid` | −1 request fantasma |

**Templates sem base.css:** `index`, `blog`, `article`, `page`, `404`, `list-collections`, `password`

## Fase 2e (aplicada 08/06/2026)

| Mudança | Arquivo | Impacto |
|---------|---------|---------|
| Skip `base.css` em PLP, busca, carrinho | `global-css.liquid` | −461 KB em collection/search/cart |
| PDP: só `vendor.css` async (Swiper galeria) | `global-css.liquid` | −461 KB; mantém 15 KB Swiper |
| Grid/spacing/layout-panel-flex mínimos | `snippets/saibai-shell-css.liquid` | PLP/PDP sem FOUC de layout |
| Swiper arrows galeria PDP | `snippets/saibai-pages-css.liquid` | Setas visíveis sem base.css |

**Único template que ainda carrega base.css:** nenhum — removido de todo o fluxo Saibai.

---

## Fase 3 — Modularização CSS (aplicada 09/06/2026)

| Mudança | Arquivo | Impacto |
|---------|---------|---------|
| Monolito `saibai-shell.css` (1074 lin) → 8 módulos | `snippets/saibai-shell-css.liquid` | Todos ≤273 lin |
| Monolito `saibai-pages.css` (2783 lin) → 18 módulos | `snippets/saibai-pages-css.liquid` | Todos ≤293 lin |
| Monolito `saibai-inst.css` → loader | `snippets/saibai-inst-css.liquid` | Institucionais |
| Header/footer/consent split | `saibai-*-css.liquid` | ≤300 lin/arquivo |
| Token `--saibai-tile-aspect: 558 / 780` | `saibai-tokens.css` | Proporção cards unificada |
| Removidos 82 lin `{% style %}` duplicados | `layout/theme.liquid` | Cascata eliminada |
| 40 blocks + 33 templates demo removidos | `blocks/`, `templates/` | Repo −1.5 GB |
| Veltrus → branding tema | `settings_schema.json`, loaders | v1.2.4 |

**Validação Fase 3:**
```bash
test ! -f assets/saibai-shell.css && test ! -f assets/saibai-pages.css && echo "monolitos OK"
wc -l assets/saibai-*.css | awk '$1>300 {exit 1} END {print "all <=300"}'
grep "558 / 780" assets/saibai-tokens.css
```

---

## Validação pós-deploy

```bash
# Home / PLP / PDP — zero link ativo para base.css
curl -sL "https://emporiosaibai.com.br/?v=$(date +%s)" | grep -c 'href=.*base\.css'
curl -sL "https://emporiosaibai.com.br/collections/todos?v=$(date +%s)" | grep -c 'href=.*base\.css'
# meta: 0

# PDP — só vendor.css async
curl -sL "https://emporiosaibai.com.br/products/ALGUM?v=$(date +%s)" | grep -c 'vendor\.css'
# meta: ≥1

# Lighthouse mobile — comparar FCP/LCP vs baseline 71 / 5.6s LCP
# GTmetrix — gtmetrix.com → emporiosaibai.com.br (re-testar CLS pós-P0)
```

---

*Veltrus Growth & Technology — Shopify Partner ID 4969609*
