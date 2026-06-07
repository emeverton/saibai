# Sprint 3 — Log de alterações

**Loja:** emporiosaibai.myshopify.com  
**Tema:** Ella 7.2.0  
**Data:** 2026-06-06  
**Escopo:** Responsividade mobile, carousel cards, textos demo, ícones, selos pagamento, páginas institucionais

---

## Parte A — Responsividade global

| Arquivo | Alteração |
|---------|-----------|
| `assets/saibai-tokens.css` | `overflow-x: hidden` html/body; tipografia fluida h1–h3 + body clamp; logo mobile max 120px; touch targets 44px header; footer colunas empilhadas + links 44px |

### Homepage — 4 custom-liquid

| Seção | Snippet | Mobile |
|-------|---------|--------|
| `s_farm_story` | `snippets/saibai-home-farm-story.liquid` | column, imagem min-height 300px |
| `s_feature` | `snippets/saibai-home-feature.liquid` | texto acima, imagem abaixo |
| `s_conservas` | `snippets/saibai-home-conservas.liquid` | texto acima, imagem abaixo |
| `s_newsletter` | `snippets/saibai-home-newsletter.liquid` | padding 40px 20px, form coluna |

Ordem em `templates/index.json`: hero → marquee → editorial → farm → feature → produtos → conservas → newsletter

---

## Parte B — Carousel mobile cards

| Arquivo | Alteração |
|---------|-----------|
| `assets/saibai-tokens.css` | `@media (max-width:767px)` flex scroll-snap 66.66vw em `.product-grid`, `.collection-grid`, `[class*="grid--"]` |

---

## Parte C — Textos demo

Substituições em massa (59 arquivos): `mail@domain.com`, endereços SF, HALOTHEMES, Shop Now → Ver produtos, etc.

| Arquivo ativo | Alteração |
|---------------|-----------|
| `sections/footer-group.json` | Textos Saibai, Veltrus credit |
| `templates/page.contact.json` | Contato PT, botão Enviar mensagem |
| `templates/page.contato.json` | Cópia de contact (formulário funcional) |
| `templates/page.about.json` | CONTACT US → Contato |
| `blocks/text.liquid` | Default typing text PT |

---

## Parte D — Ícones e pagamento

| Arquivo | Alteração |
|---------|-----------|
| `assets/saibai-tokens.css` | `.icon, svg` transition; header hover verde |
| `snippets/saibai-payment-icons.liquid` | **Novo** — Pix, Visa, Mastercard, Elo, Boleto |
| `blocks/payment-icons.liquid` | Renderiza snippet Saibai |

---

## Parte E — Páginas institucionais

| Template | Rota | Conteúdo |
|----------|------|----------|
| `page.sobre.json` | `/pages/sobre` | História Saibai, Piedade SP |
| `page.contato.json` | `/pages/contato` | Formulário + dados (via page.contact) |
| `page.politica-de-entrega.json` | `/pages/politica-de-entrega` | Política entrega + frete R$280 |
| `page.politica-de-troca.json` | `/pages/politica-de-troca` | CDC + produtos frescos |

`main-page.liquid` herda `color_scheme` do JSON via `snippets/section.liquid` → `color-{{ section.settings.color_scheme }}` ✓

**Customers:** textos via `locales/pt-BR.json` — sem strings hardcoded em inglês nos templates.

---

## Validação

```bash
grep -r "685 Market" templates/ sections/footer-group.json  # 0
grep -r "HALOTHEMES" templates/ sections/footer-group.json # 0
grep -r "s_farm_story\|saibai-home-" templates/index.json snippets/
grep -r "saibai-payment-icons" snippets/ blocks/
grep -r "scroll-snap-type" assets/saibai-tokens.css
wc -l assets/saibai-tokens.css
```

---

## Ação no admin Shopify

1. Criar páginas com handles: `sobre`, `contato`, `politica-de-entrega`, `politica-de-troca`
2. Atribuir templates correspondentes (`sobre`, `contato`, etc.)
3. Confirmar selos Pix/Boleto habilitados em Pagamentos (SVG via `payment_type_svg_tag`)
