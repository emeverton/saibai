# Sprint 7 — Go-Live Readiness

**Data:** junho 2025  
**Tema:** Ella 7.2.0 + Saibai custom  
**Dev theme:** #186131218750

---

## Entregas

| Item | Arquivo(s) | Status |
|------|------------|--------|
| Slideshow play/pause + dots verdes | `sections/slideshow.liquid`, `snippets/saibai-slideshow-autoplay.liquid`, `templates/index.json`, `saibai-tokens.css` | ✅ |
| Card hover overlay ATC | `snippets/card-product.liquid`, `saibai-tokens.css` | ✅ |
| Logo Saibai no footer | `sections/footer.liquid` | ✅ |
| Política de privacidade | `templates/page.politica-de-privacidade.json` | ✅ |
| GA4 + dataLayer | `snippets/tracking-ga4.liquid`, `layout/theme.liquid`, `settings_schema.json` | ✅ |
| Meta ViewContent | `snippets/tracking-meta-pixel.liquid` | ✅ |
| Customers color scheme | `templates/customers/order.json`, `addresses.json`, `reset_password.json`, `activate_account.json` | ✅ |
| README propriedade intelectual | `README.md` | ✅ |
| Grid 2 tab / 4 desk | `saibai-tokens.css` | ✅ |

---

## Configuração manual (merchant)

1. **Theme Settings → Saibai Tracking**
   - Meta Pixel ID (ex.: `1515673690245683` ou ID da loja)
   - GA4 Measurement ID (`G-XXXXXXXXXX`)
2. **Páginas → Nova página** handle `politica-de-privacidade` → template `page.politica-de-privacidade`
3. **Hero slideshow** — substituir slide 2 por foto diferente quando assets pro estiverem prontos
4. **Publicar tema** dev → live quando validado

---

## Validação

```bash
grep -c "saibai-slideshow-toggle" snippets/saibai-slideshow-autoplay.liquid   # 1
grep -c "saibai-card-overlay" snippets/card-product.liquid                     # 1
grep -c "saibai-footer-logo" sections/footer.liquid                              # 1
grep -c "view_item" snippets/tracking-ga4.liquid                                 # 1
grep -c "ViewContent" snippets/tracking-meta-pixel.liquid                        # 1
grep -c "politica-de-privacidade" templates/page.politica-de-privacidade.json  # 1
```

---

## Pendências pós-Sprint 7

- Purchase event (checkout Shopify — requer CAPI/sGTM ou Shopify Pixels)
- Fotografia pro nas seções home (gradientes)
- Klaviyo / Judge.me instalação
- GTmetrix baseline em produção
- Meta Pixel ID + GA4 ID no admin

---

*Veltrus Growth & Technology — Shopify Partner*
