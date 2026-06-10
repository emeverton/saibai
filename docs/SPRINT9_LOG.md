# SPRINT 9 — Duplo check C-Level + blindagem Veltrus

**Data:** 09/06/2026  
**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br)  
**Referências:** [Loro Piana Interactive](https://ii.loropiana.com/en/) · LG.com  
**Desenvolvedor:** Veltrus Growth & Technology · Shopify Partner ID 4969609

---

## 1. Auditoria visual ao vivo (prints + DOM)

### Home (`/`)
| Elemento | Status | Notas |
|----------|--------|-------|
| Announcement bar | ✅ | Carrossel prev/next · **pause/play adicionado Sprint 9** |
| Header central LP | ✅ | Logo, nav fina, mega menu, busca/conta/sacola |
| Hero vídeo | ✅ | Pause + mute visíveis (`saibai-hero.js`) |
| Vitrine produtos | ✅ | Tabs Fresca/Conservas · nav anterior/próximo |
| Editorial / split / feature | ✅ | KV cream + grafite |
| Inside carousel | ✅ | Nav anterior/próximo |
| Footer Saibai | ✅ | Newsletter, colunas, crédito Veltrus |
| Selos pagamento | 🔧→✅ | Fallback hardcoded quando admin sem types |

### PLP (`/collections/em-conserva`)
| Elemento | Status |
|----------|--------|
| Hero coleção + H1 | ✅ |
| Grid full-width LP | ✅ |
| Cards = home | ✅ |
| Sidebar legado demo | ✅ Oculta via CSS |
| Filtros mobile | ✅ Drawer nativo (DOM presente, visual oculto desktop) |

### PDP (`/products/conserva-de-alcachofras-coracao`)
| Elemento | Status |
|----------|--------|
| Galeria + info | ✅ |
| CEP frete | ✅ |
| Variantes + qty + ATC | ✅ |
| Tabs detalhes/conservação/troca/entrega | ✅ |
| Sticky ATC mobile | ✅ |

### Páginas testadas (snapshot a11y)
- `/` home · `/collections/em-conserva` · `/products/conserva-de-alcachofras-coracao`
- Footer links: Sobre, Contato, Políticas, Receitas — todos presentes no DOM
- `saibai-license.js` carregado (`__saibaiLicenseInit: true`)
- Textos com cor = background: **0 ocorrências** na home

---

## 2. Comparativo benchmark

| Critério | Loro Piana / LG | Saibai |
|----------|-----------------|--------|
| Paleta neutra cream | Wool/cream | `#F2F5EE` / `#FAFBF7` |
| Tipografia leve | 300–400 | Jost 400, letter-spacing 0.02em |
| Cards verticais | Alongados | Aspect 558/780 home (+20% LP) |
| Nav minimalista | Centro/discreta | Logo central + mega gaveta |
| Hovers discretos | Cor sutil | Verde `#8ABE0A` em links |
| CTA | Contraste alto | Grafite `#2A3A1A` → hover `#384E28` |

**Veredito:** Saibai no **mesmo patamar editorial** das referências, com identidade verde/grafite própria (não cópia LP).

---

## 3. Proteção código Veltrus (item 2)

| Camada | Implementação |
|--------|---------------|
| Legal | README + cabeçalhos IP em todos `saibai-*` |
| Técnica | `saibai-license.js` whitelist domínios |
| Console | Aviso de licença no DevTools |
| Bloqueio | Domínio não autorizado → mensagem Veltrus |
| Crédito | `saibai-veltrus-credit.liquid` no footer |

**Limitação:** tema Shopify é entregue ao browser — proteção absoluta não existe. Combinação licença + contrato é a barreira comercial.

**Domínios autorizados:**
- emporiosaibai.com.br / www
- emporiorsaibai.myshopify.com
- byinbz-0k.myshopify.com

---

## 4. Modularização — mapa de arquivos Saibai

### Layout
| Arquivo | Linhas | Função |
|---------|--------|--------|
| `layout/theme.liquid` | 250 | Shell HTML, preload LCP, CTA inline final |

### CSS global (loaders Liquid — Fase 3 ✅)
| Loader | Módulos | Função |
|--------|---------|--------|
| `snippets/saibai-shell-css.liquid` | 8× `saibai-shell-*.css` (≤273 lin) | Hovers, cards, grids, neutralização demo |
| `snippets/saibai-pages-css.liquid` | 18× `saibai-pages-*.css` (≤293 lin) | KV por template (PDP, PLP, cart, search…) |
| `snippets/saibai-inst-css.liquid` | `saibai-inst-*.css` | Institucionais + blog |
| `snippets/saibai-header-css.liquid` | 10× `saibai-header-*.css` | Header modular |
| `snippets/saibai-footer-css.liquid` | `saibai-footer-*.css` | Rodapé |

**Token proporção cards:** `--saibai-tile-aspect: 558 / 780` em `saibai-tokens.css`.

### JS modular
| Arquivo | Função |
|---------|--------|
| `saibai-license.js` | Licença domínio |
| `saibai-header.js` | Mega menu + drawer |
| `saibai-hero.js` | Vídeo pause/mute/parallax |
| `saibai-announcement-bar.js` | Carrossel + **pause Sprint 9** |
| `saibai-products.js` | Tabs + carrossel produtos |
| `saibai-consent-popup.js` | LGPD Consent Mode v2 |
| `saibai-coupon-popup.js` | Cupom exit intent |

### Sections home (ordem típica)
`saibai-home-hero` → `saibai-home-products` → `saibai-home-editorial` → `saibai-marquee` → `saibai-home-farm` → `saibai-home-conservas` → `saibai-home-feature` → `saibai-home-at-service` → `saibai-home-services` → `saibai-home-inside` → `saibai-footer`

### Dívida técnica identificada
- ~~Monolitos `saibai-shell.css` / `saibai-pages.css`~~ → **✅ Fase 3:** loaders Liquid + módulos ≤300 lin
- `sections/footer.liquid` — legado base (4895+ lin) não usado (`footer-group.json` → `saibai-footer`)
- Assets cliente em `../client-assets/Saibai/` — fora do repo tema deployável

---

## 5. Alterações Sprint 9

| Arquivo | Mudança |
|---------|---------|
| `sections/saibai-footer.liquid` | Fallback `saibai-payment-icons` |
| `snippets/saibai-announcement-bar.liquid` | Botão pause/play |
| `assets/saibai-announcement-bar.js` | Toggle autoplay |
| `assets/saibai-announcement-bar.css` | Estado `.is-paused` |
| `assets/saibai-footer.css` | Estilo selos fallback |
| `GUIA_SAIBAI_LEIGO.md` | KV atualizado v1.1 |
| `RELATORIO_DIRETORIA_SAIBAI.md` | Seção Sprint 9 |

---

## 6. Validações grep

```bash
# Licença carregada
grep -c "saibai-license" snippets/global-script.liquid  # → 1

# Tokens KV primário
grep "saibai-primary: #8ABE0A" assets/saibai-tokens.css  # → ok

# Footer fallback pagamento
grep "saibai-payment-icons" sections/saibai-footer.liquid  # → ok

# Pause announcement bar
grep "saibai-ab__btn--pause" snippets/saibai-announcement-bar.liquid  # → ok

# Overflow responsivo
grep "overflow-x: clip" assets/saibai-tokens.css snippets/saibai-shell-css.liquid  # → ok
grep "558 / 780" assets/saibai-tokens.css  # → proporção cards
```

---

## 7. Pós-deploy checklist

- [ ] Publicar tema no Shopify Admin
- [ ] GTmetrix em emporiosaibai.com.br (meta A)
- [ ] GTM Preview — eventos GA4 + Meta com consent
- [ ] Admin → Pagamentos → habilitar tipos (complementa fallback)
- [ ] Testar pause barra fixa + hero em mobile
- [ ] Verificar selos Pix/Visa no footer

---

*Veltrus Growth & Technology — Shopify Partner #4969609*
