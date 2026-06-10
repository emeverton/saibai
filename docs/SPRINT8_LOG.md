# SPRINT 8 — Auditoria C-Level × Loro Piana

**Data:** 08/06/2026  
**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br)  
**Referência visual:** [Loro Piana Interactive](https://ii.loropiana.com/en/)  
**Desenvolvedor:** Veltrus Growth & Technology · Shopify Partner ID 4969609

---

## 1. Auditoria visual (site ao vivo)

| Área | Status | Observação |
|------|--------|------------|
| Header / logo central | ✅ KV Saibai | Minimalista, cream + grafite, alinhado ao padrão LP |
| Announcement bar | ✅ | Carrossel com prev/next visíveis |
| Hero (vídeo YouTube) | ✅ | Controles play/pause e mute visíveis |
| Dobra produtos (home) | 🔧 | Cards alongados +20% (558×780) · mobile 1,5 card |
| Editorial / coleções | ✅ | Grid LP, hover lift |
| Footer | 🔧 | Links duplicados removidos · crédito Veltrus + Shopify Partner |
| PLP (coleções) | 🔧 | Sidebar legado demo oculta · grid full-width LP |
| PDP / Cart / Search | ✅ | KV via `snippets/saibai-pages-css.liquid` |
| Páginas institucionais | ✅ | Módulos `saibai-inst-*` |
| Consent LGPD | ✅ | Popup + preferências cookies |
| Tracking | ✅ | GA4 + Meta via consent + Customer Events pixel |

**Comparativo Loro Piana:** paleta neutra cream/wool, tipografia leve (400), cards verticais alongados, hovers discretos, navegação minimalista. Saibai adapta o padrão ao KV verde `#76BD22` + grafite `#2A3A1A`.

---

## 2. Alterações de código (Sprint 8)

| Arquivo | Mudança |
|---------|---------|
| `assets/saibai-products.css` | Aspect ratio home 558/780 (+20%) · mobile 1,5 card |
| `snippets/saibai-pages-css.liquid` (módulos `saibai-pages-*.css`) | PLP LP full-width · cover imagens sem pad |
| `snippets/saibai-shell-css.liquid` (módulos `saibai-shell-*.css`) | Crédito Veltrus estilizado · cards cover |
| `assets/saibai-footer.css` | Selos pagamento visíveis |
| `assets/saibai-license.js` | **NOVO** — licença de domínio |
| `snippets/saibai-veltrus-credit.liquid` | Texto "Desenvolvido por Veltrus · Shopify Partner" |
| `sections/saibai-footer.liquid` | Remove links legais duplicados |
| `snippets/global-script.liquid` | Carrega `saibai-license.js` |

---

## 3. Proteção de código (item 2)

**Implementado:**
- Cabeçalhos de copyright em todos os arquivos Saibai
- `saibai-license.js` — whitelist de domínios + aviso no console
- Bloqueio de renderização em domínios não autorizados

**Limitação técnica (transparência):** temas Shopify são entregues ao navegador; proteção absoluta contra cópia não existe. A combinação licença + contrato Veltrus/Saibai é a barreira legal.

---

## 4. Responsividade (item 4)

- `overflow-x: clip` global
- Grids: mobile carousel 1,5 · tablet 2 col · desktop 4 col
- Ultra-wide: max-width 1440px nos shells LP
- `prefers-reduced-motion` respeitado

---

## 5. Hovers padronizados (item 5)

Centralizados em `snippets/saibai-shell-css.liquid`:
- Links → verde `#76BD22`
- Botões primários → hover `#5A9018`
- Botões secundários → inversão fill
- Ícones sociais → verde no hover

---

## 6. Slideshow / autoplay (item 7)

- Hero: botões pause + mute (`saibai-hero.js`)
- Announcement bar: prev/next
- `saibai-slideshow-autoplay.liquid` para Swiper sections
- Controles com opacity 1 forçada em `snippets/saibai-shell-css.liquid`

---

## 7. Performance / SEO / CRO (item 9)

| Item | Status |
|------|--------|
| CSS crítico inline | ✅ `critical-css.liquid` |
| Preconnect CDN / YouTube | ✅ `theme.liquid` |
| Lazy load imagens | ✅ nativo Shopify |
| Schema.org Organization | ✅ |
| Open Graph / Twitter | ✅ `seo-meta.liquid` |
| Consent Mode v2 | ✅ default denied |
| Customer Events pixel | ✅ script gerado |
| GTmetrix A | ⏳ Requer deploy + teste pós-push |

**Próximo passo performance:** rodar GTmetrix após publicar tema; otimizar LCP do hero (poster WebP).

---

## 8. Mapa modular Saibai (item 13)

```
layout/theme.liquid          → shell global
assets/saibai-tokens.css     → design tokens
assets/snippets/saibai-shell-css.liquid      → KV global + hovers + cards
assets/snippets/saibai-pages-css.liquid       → KV por template
assets/saibai-header-*.css    → header modular
assets/saibai-hero.css/js     → hero homepage
assets/saibai-products.css/js → carousel safra
assets/saibai-footer.css      → footer C-level
sections/saibai-*.liquid      → blocos editáveis
snippets/saibai-*.liquid      → peças reutilizáveis
```

Arquivos base nativos permanecem; regras Saibai neutralizam widgets demo via shell modular Saibai.

---

## 9. Pendências para próximas sessões Cursor

1. ~~Publicar tema no Shopify~~ ✅ Sprint 8
2. **GTmetrix** — rodar em gtmetrix.com (Lighthouse mobile: 65 pós-otimização hero)
3. **Checkout branding manual** — ver `CHECKOUT_BRANDING_GUIA.md` (plano Basic)
4. ~~Consolidar CSS legado (base.css 461 KB)~~ → **Fase 2a:** defer na home (`PERF_FASE2.md`)
5. ~~Substituir hero YouTube por MP4~~ → **Adiado:** manter lazy YouTube; LCP = poster WebP até trocar por imagem estática

---

## 10. Performance Sprint 8 (Lighthouse mobile)

| Métrica | Antes | Depois | Meta A |
|---------|-------|--------|--------|
| Score | 56 | **65** | 90+ |
| FCP | 7.3s | **3.0s** | < 1.8s |
| LCP | 20.2s | **15.8s** | < 2.5s |
| TBT | 90ms | **50ms** | < 200ms |
| CLS | 0.008 | 0.008 | < 0.1 |

**Otimizações aplicadas:**
- Hero YouTube lazy (poster WebP + iframe via IntersectionObserver)
- Removido preload concorrente em 5 CSS
- `text-animation.js` desativado na home

**Gargalos restantes:**
- `base.css` (461 KB) + `vendor.js` (183 KB) — legado base theme
- YouTube ainda domina LCP quando carrega no viewport
- Imagens produto oversized (~374 KB economia possível)

---

*Veltrus Growth & Technology — Shopify Partner*
