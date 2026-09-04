# Checkout Branding Saibai — Guia Manual (Plano Basic)

**Loja:** emporiosaibai.com.br · Admin: `byinbz-0k.myshopify.com`  
**Script automático:** `../ops/scripts/configure-saibai-checkout-branding.py`  
**Status:** Requer **Shopify Plus** para API `checkoutBrandingUpsert` — no Basic, use o editor visual abaixo.

---

## Cores KV (copiar no editor)

| Token | Hex | Uso |
|-------|-----|-----|
| Fundo | `#F4F9F0` | Background checkout |
| Texto | `#2A3A1A` | Tipografia |
| Borda | `#E2EDDA` | Campos e divisores |
| Accent | `#76BD22` | Links e destaques |
| Botão primário | `#76BD22` | Finalizar compra |
| Botão hover | `#5A9018` | Hover do CTA |
| Decorative | `#E8F5D4` | Seleções / chips |

**Fonte:** Jost 400 (heading e body)

**Cantos:** 4px (SMALL) — padrão LP Saibai

---

## Passo a passo no Admin

1. Acesse **Configurações → Checkout → Personalizar**
2. Aba **Branding** (ou Design)
3. **Cores** — aplique a tabela acima em Background, Text, Buttons, Forms
4. **Tipografia** — selecione **Jost** para título e corpo
5. **Logo** — upload do PNG Saibai (fundo transparente ou branco)
6. **Botões** — cantos 4px, primário `#76BD22`, texto branco
7. **Salvar** e teste um pedido sandbox

---

## Contas de cliente (Customer Accounts)

1. **Configurações → Customer accounts → Customize**
2. Mesma paleta e fonte Jost
3. Manter consistência com footer e home

---

## Quando migrar para Plus

Rode novamente:

```bash
python3 ../ops/scripts/configure-saibai-checkout-branding.py
```

O script aplica branding via GraphQL automaticamente.

---

*Veltrus Growth & Technology · Shopify Partner #4969609*
