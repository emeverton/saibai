# Sprint 2 — Log de alterações

**Loja:** emporiosaibai.myshopify.com  
**Tema:** Ella 7.2.0  
**Data:** 2026-06-06  
**Escopo:** KV da marca, hover states, cards de produto, ícones, textos demo, WhatsApp VIP

---

## Pré-Sprint 2 — WhatsApp VIP

| Arquivo | Alteração |
|---------|-----------|
| `sections/footer-group.json` | Link WhatsApp placeholder → `https://chat.whatsapp.com/LmGiN0C8QT04AQ4VB9PDdO` |
| `snippets/saibai-whatsapp-float.liquid` | **Novo** — botão float Grupo VIP |
| `layout/theme.liquid` | Render do float antes de `</body>` |

---

## 1. Color schemes por template

| Template | Seção | Antes | Depois |
|----------|-------|-------|--------|
| `collection.json` | banner, product-grid | scheme-1 | ✓ mantido |
| `product.json` | main | scheme-6 | **scheme-1** |
| `cart.json` | cart-section | (vazio) | **scheme-1** |
| `search.json` | main-search | scheme-1 | ✓ mantido |
| `404.json` | main | scheme-1 | **scheme-7** |
| `page.json` | main | scheme-1 | **scheme-2** |
| `page.contact.json` | main, section_ApznVq | scheme-4, scheme-8 | **scheme-2** |
| `blog.json` | main | scheme-1 | **scheme-2** |
| `article.json` | main | (vazio) | **scheme-2** |
| `customers/account.json` | main | (ausente) | **scheme-1** |
| `customers/login.json` | main | (ausente) | **scheme-1** |
| `customers/register.json` | main | (ausente) | **scheme-1** |
| `password.json` | media_banner | (vazio) | **scheme-7** |

---

## 2–3. Hover states e botões

| Arquivo | Alteração |
|---------|-----------|
| `assets/saibai-tokens.css` | Links `transition` + hover `#76BD22`; botões 48px, padding 28px, radius 4px, hover `#5A9018`; secondary hover verde |

---

## 4. Cards de produto

| Arquivo | Alteração |
|---------|-----------|
| `snippets/card-product.liquid` | Classe `saibai-product-card` no wrapper |
| `snippets/card-product-flex.liquid` | Classe `saibai-product-card` no wrapper |
| `assets/saibai-tokens.css` | Imagem cover 1:1, título hover, compare riscado, badge verde, mobile 66.66vw peek |

Aplica-se automaticamente em: featured-collection, collection grid, search, related products, recently viewed (todos usam `card-product`).

---

## 5–6. Ícones e contraste

| Arquivo | Alteração |
|---------|-----------|
| `assets/saibai-tokens.css` | SVG stroke 1.5, cor dark/light por scheme, hover verde; overrides de foreground em schemes claros/escuros |

---

## 7. Logo Saibai

| Arquivo | Alteração |
|---------|-----------|
| `snippets/saibai-logo.liquid` | Fallback SVG (Fase 1) |
| `snippets/header-logo.liquid` | Usa fallback quando `settings.logo` vazio |
| `assets/logo-saibai.svg` | Wordmark provisório |

**Nota:** `settings.logo` permanece vazio — logo renderizado via fallback asset. Upload no admin substitui automaticamente.

---

## 8. WhatsApp float

| Arquivo | Alteração |
|---------|-----------|
| `snippets/saibai-whatsapp-float.liquid` | Link Grupo VIP + ícone SVG |
| `layout/theme.liquid` | Injetado globalmente |
| `assets/saibai-tokens.css` | Estilos fixed bottom-right 56px #25D366 |

---

## 9. Textos demo removidos

| Arquivo | Alteração |
|---------|-----------|
| `sections/footer-group.json` | WhatsApp VIP, newsletter Saibai, removido HALOTHEMES |
| `templates/page.contact.json` | Endereço Piedade SP, contato@saibai.com.br, telefone |
| `templates/page.about.json` | Idem |
| `templates/page.faqs.json` | econtato@saibai.com.br → contato@saibai.com.br |

---

## Validação

```bash
grep -r "wa.me/5515" .          # 0 ocorrências
grep -r "685 Market" templates/ # 0 ocorrências
grep -r "saibai-product-card" snippets/
grep -r "saibai-whatsapp-float" layout/ snippets/
wc -l assets/saibai-tokens.css  # ≤300 linhas
```
