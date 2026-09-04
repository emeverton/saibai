# Empório Saibai — Entrega Shopify Ops · 21/07/2026

**Veredito:** **LIVE APROVADO**  
**Loja:** https://emporiosaibai.com.br  
**Tema live:** `#186796147006` (`ella-saibai-homepage`)  
**Origem:** pedidos WhatsApp Clara (16–17/07) + follow-ups 21/07

---

## Checklist

| # | Solicitação | Status |
|---|-------------|--------|
| 1 | Limite **2 caixas** alcachofra fresca / pedido | ✅ Live |
| 2 | Peso envio **5 kg** (todas variantes ativas) | ✅ Live |
| 3 | Pacote **30 × 14 × 50 cm** | ✅ Confirmado merchant |
| 4 | Remover **Frutas Desidratadas** do menu | ✅ Live |
| 5 | **T8** na coleção frescas | ✅ Live (8 SKUs) |
| 6 | Frete grátis **R$ 389,90** | ✅ Live |

---

## Detalhe técnico

### Limite 2 caixas
- `assets/saibai-cart-limits.js` + loader Liquid
- Agregado por `product_type = Alcachofra In Natura`

### Pesos / pacote
- Inventory weights → **5.0 KILOGRAMS**
- Metafield shop `saibai.shipping_package_standard` (JSON 30×14×50 · 5 kg)
- Pacote Admin/Frenet: confirmado pelo merchant 21/07

### Catálogo / navegação
- Coleção `alcachofra-in-natura` + T8
- Menus `main-menu`, `produtos`, `footer-shop-classic` sem Frutas

### Frete grátis
- DiscountAutomaticFreeShipping → mínimo **389.9**
- Copy tema: announcement, política, PDP, cards, settings

---

## Plataformas

| Canal | Link |
|-------|------|
| Notion | https://app.notion.com/p/3a4968afab66814bbcfce11f8baa4b10 |
| Slack `#cliente-saibai` | https://veltrus.slack.com/archives/C0BD28VMD4N/p1784647395835769 |
| eKyte | https://app.ekyte.com/#/tasks/9959655 |

---

## Próximo

1. Smoke cotação Frenet/Loggi (CEP SP/RJ) com 5 kg + dims  
2. Gates P0 tracking/pagamento (#9712969)  
