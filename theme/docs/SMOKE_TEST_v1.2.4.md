# Smoke Test — Saibai v1.2.4

**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br)  
**Tema:** Saibai by Veltrus 1.2.4  
**Quando rodar:** após `shopify theme push` em staging, antes de publicar na live.

Marque `[x]` só após testar em **desktop** e **mobile 375px** (quando aplicável).

---

## 0. Pré-voo (terminal)

```bash
shopify theme check          # → 0 offenses
grep -c "saibai-license" snippets/global-script.liquid   # → 1
```

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 0.1 | Theme Check 0 offenses | — | — | |
| 0.2 | `saibai-license.js` carrega (DevTools → Network) | | | |
| 0.3 | Console: aviso "Empório Saibai — Tema Oficial" | | | |
| 0.4 | Nenhum 404 de CSS/JS Saibai no Network | | | |

---

## 1. Home (`/`)

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 1.1 | Announcement bar visível + carrossel | | | |
| 1.2 | Botões prev / pause / next na barra | | | |
| 1.3 | Header central: logo, nav, busca, conta, sacola | | | |
| 1.4 | Hero vídeo: play, pause, mute | | | |
| 1.5 | Vitrine produtos: tabs Fresca / Conservas | | | |
| 1.6 | Carrossel produtos: nav anterior / próximo | | | |
| 1.7 | Blocos editorial, farm, feature, inside | | | |
| 1.8 | Footer: newsletter, colunas, crédito Veltrus | | | |
| 1.9 | Selos pagamento (Pix, Visa, MC…) | | | |
| 1.10 | WhatsApp flutuante abre conversa | | | |
| 1.11 | Popup LGPD (aba anônima) | | | |
| 1.12 | Sem scroll horizontal | | | |

---

## 2. PLP — Coleção (`/collections/em-conserva`)

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 2.1 | Hero coleção + H1 | | | |
| 2.2 | Grid full-width, cards proporcionais | | | |
| 2.3 | Cards iguais visualmente à home | | | |
| 2.4 | Sidebar demo oculta (desktop) | | | |
| 2.5 | Filtros mobile (drawer) abre/fecha | | | |
| 2.6 | Paginação ou infinite scroll | | | |
| 2.7 | Link card → PDP correto | | | |

---

## 3. PDP — Produto (`/products/conserva-de-alcachofras-coracao`)

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 3.1 | Galeria: thumb + imagem principal | | | |
| 3.2 | Título, preço, compare-at | | | |
| 3.3 | Seletor de variantes | | | |
| 3.4 | Quantidade + Adicionar ao carrinho | | | |
| 3.5 | CEP frete (calculadora BR) | | | |
| 3.6 | Tabs: detalhes / conservação / troca / entrega | | | |
| 3.7 | Sticky ATC mobile ao rolar | | | |
| 3.8 | Produtos relacionados | | | |
| 3.9 | Schema / rich snippets (View Source) | | | |

**Produto alternativo (variantes):** `/products/…` com múltiplas variantes — repetir 3.3–3.5.

---

## 4. Carrinho

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 4.1 | Drawer abre ao add-to-cart | | | |
| 4.2 | Bubble sacola atualiza qty | | | |
| 4.3 | Página `/cart` — itens, qty, subtotal | | | |
| 4.4 | Cupom / hint de cupom Saibai | | | |
| 4.5 | Barra frete grátis (se configurada) | | | |
| 4.6 | Botão checkout → Shopify checkout | | | |

---

## 5. Busca (`/search?q=alcachofra`)

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 5.1 | Predictive search no header | | | |
| 5.2 | Página de resultados: produtos + layout | | | |
| 5.3 | Filtros / ordenação | | | |
| 5.4 | Estado vazio (termo inexistente) | | | |

---

## 6. Conta cliente

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 6.1 | `/account/login` — formulário PT | | | |
| 6.2 | `/account/register` — campos BR | | | |
| 6.3 | `/account/addresses` — CEP, UF, campos BR | | | |
| 6.4 | `/account` — pedidos listados (conta teste) | | | |

---

## 7. Institucionais

| URL | Check | Desktop | Mobile | Notas |
|-----|-------|---------|--------|-------|
| `/pages/sobre` | Layout Saibai, imagens, CTA | | | |
| `/pages/contato` | Formulário / WhatsApp | | | |
| `/pages/historia` | Timeline / conteúdo | | | |
| `/pages/fazenda` | Conteúdo + imagens | | | |
| `/policies/privacy-policy` | Política publicada | | | |
| `/policies/shipping-policy` | Entrega | | | |
| `/policies/refund-policy` | Troca | | | |
| `/blogs/receitas` | Listagem blog | | | |
| Artigo blog (1 URL) | Template artigo Saibai | | | |

---

## 8. Módulos Ella herdados (regressão pós-auditoria)

| # | Check | Desktop | Mobile | Notas |
|---|-------|---------|--------|-------|
| 8.1 | Compare produtos (se ativo) | | | |
| 8.2 | Quick-add modal | | | |
| 8.3 | Edit cart popup | | | |
| 8.4 | Notify me (sold out) | | | produto esgotado |
| 8.5 | Shipping calculator no cart | | | |

---

## 9. Performance (pós-deploy)

| # | Check | Meta | Resultado |
|---|-------|------|-----------|
| 9.1 | Lighthouse mobile (home) | ≥ atual | |
| 9.2 | LCP home | < 2.5s | |
| 9.3 | Sem `base.css` na home (Network) | 0 requests | |
| 9.4 | GTmetrix / PageSpeed (opcional) | Grade A | |

---

## 10. Tracking (GTM Preview)

| # | Evento | Disparou? | Notas |
|---|--------|-----------|-------|
| 10.1 | `page_view` / GA4 config | | |
| 10.2 | `view_item` (PDP) | | |
| 10.3 | `add_to_cart` | | |
| 10.4 | `begin_checkout` | | |
| 10.5 | Meta Pixel PageView | | |
| 10.6 | Consent Mode v2 (LGPD) | | |

---

## Sign-off

| Papel | Nome | Data | OK |
|-------|------|------|-----|
| Dev Veltrus | | | |
| QA | | | |
| Cliente Saibai | | | |

**Após todos os checks:** publicar tema → tag git `saibai-v1.2.4-final`.

---

*Veltrus Growth & Technology — Shopify Partner #4969609*
