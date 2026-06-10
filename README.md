# Empório Saibai — Tema Shopify Oficial

**Desenvolvido por:** [Veltrus Growth & Technology](https://veltrus.com.br) — Shopify Partner ID 4969609  
**Cliente:** Empório Saibai — Piedade, SP  
**Base técnica:** Veltrus Commerce Stack (Halothemes Ella 7.2.0 fork)  
**Versão Saibai:** 1.2.4 | 2026-06-09

---

## Propriedade intelectual

Todo o código customizado identificado pelos cabeçalhos `Empório Saibai — Tema Oficial` é propriedade exclusiva de **Veltrus Growth & Technology** e licenciado ao **Empório Saibai** para uso na loja `emporiorsaibai.myshopify.com`.

**É proibido**, sem autorização escrita da Veltrus:

- Copiar, redistribuir ou revender snippets, seções e assets Saibai
- Remover créditos de desenvolvimento do footer
- Reutilizar o tema em outras lojas sem contrato de licença

Arquivos nativos do tema Ella permanecem sujeitos à licença original do fornecedor.

---

## Arquivos Saibai (principais)

| Arquivo | Função |
|---------|--------|
| `assets/saibai-tokens.css` | Design tokens, hovers, cards, home LP |
| `snippets/saibai-shell-css.liquid` | KV global modular (5–6 CSS por template) |
| `snippets/saibai-pages-css.liquid` | KV por template modular (cart, PDP, PLP…) |
| `assets/saibai-header.css` | Header modular LP × Saibai |
| `snippets/saibai-logo.liquid` | Logo PNG via CDN Shopify Files |
| `snippets/saibai-whatsapp-float.liquid` | Botão WhatsApp VIP |
| `snippets/saibai-payment-icons.liquid` | Selos Pix, Visa, MC, Amex, Elo, Boleto |
| `snippets/tracking-meta-pixel.liquid` | Meta Pixel (PageView) |
| `snippets/tracking-ga4.liquid` | GA4 + dataLayer ecommerce |
| `snippets/critical-css.liquid` | CSS crítico inline |
| `snippets/seo-meta.liquid` | Open Graph + Twitter Cards |
| `snippets/schema-organization.liquid` | Schema.org Organization |

---

## Configuração no admin

1. **Theme Settings → Saibai Tracking** — Meta Pixel ID e GA4 Measurement ID (G-XXXXXXXX)
2. **Páginas** — associar templates: `sobre`, `contato`, `politica-de-entrega`, `politica-de-troca`, `politica-de-privacidade`
3. **Logo** — PNGs em Shopify Files (fallback automático via snippet)

---

## Documentação

Documentação do projeto em `docs/`:

- `docs/GUIA_SAIBAI_LEIGO.md` — instruções para o merchant (sem código)
- `docs/RELATORIO_DIRETORIA_SAIBAI.md` — impacto de negócio para diretoria
- `docs/SPRINT2_LOG.md` … `docs/SPRINT9_LOG.md` — histórico técnico

Scripts operacionais Shopify: `../ops/scripts/` (fora deste repo).  
Mídia e materiais do cliente: `../client-assets/` (fora deste repo).

---

*Veltrus Growth & Technology — Shopify Partner*
