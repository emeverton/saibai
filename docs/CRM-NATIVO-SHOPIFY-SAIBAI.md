# Empório Saibai — CRM nativo Shopify

**Atualizado:** 2026-09-02  
**Veredito:** cupons + tema **LIVE** · Shopify Email **PENDING** (Admin) · remarketing **ACTIVE** · recuperação checkout **ENVIADO** 35/35  
**Tracking:** nativo (canais Shopify Google/Meta). Theme Settings IDs **vazios**. Sem Klaviyo pixel.

> KPI e-com continua GA4 `purchase`. CRM não duplica pixel.

---

## O que já está LIVE (API 26/08)

| Código | Tipo | Regra | Onde aparece |
|--------|------|------:|--------------|
| `5%NOVOCLIENTE` | 5% pedido | 1x por cliente · combina com frete grátis | Popup exit-intent · dica carrinho · newsletter · e-mail Welcome |
| `SAIBAIRECOMPRA` | 8% pedido | 1x por cliente · mínimo R$ 120 · combina com frete | **Só e-mail win-back** (não mostrar no site) |
| Frete grátis | automático | Subtotal ≥ R$ 389,90 | Checkout |
| `CLIENTEVIPSAIBAI` | 10% | VIP existente | Manter |
| `PAIZAO6%` | 6% | Dia dos Pais | **Expirar no Admin** se a ação acabou |

Script: `python3 ops/scripts/configure-saibai-crm-native.py`

---

## Recuperação 02/09 (pós-hotfix frete Brasil)

Quem chegou no checkout nos últimos 14 dias e não pagou recebeu fatura Shopify agora, com o checkout novo (PAC/Sedex/Loggi já cotam).

| Item | Valor |
|------|------:|
| Checkouts únicos (19/08–02/09) | 35 |
| Faturas enviadas | **35/35** (#D30–#D64) |
| Pipeline | R$ 8.429,91 |
| Tag | `saibai-recup-frete-20260902` |
| Segmento | `Saibai recup frete Brasil 02/09` `#654975172926` |
| E-mail nativo abandonado | já estava ON (19/35 com `emailState=SENT` **antes** do hotfix) |
| Carrinho sem e-mail | Meta RMKT ATC 14d + Checkout 14d **ACTIVE** (`120254745092470155`) · audiência ~20 |

Assunto: *Seu pedido Saibai está pronto — agora entregamos em todo o Brasil*  
Admin drafts: https://admin.shopify.com/store/emporiosaibai/draft_orders

Carrinho anônimo (sem checkout/e-mail) não tem 1:1 — só pixel. Automação Shopify Email Abandoned cart continua **SB-CRM-002** (clique Admin).

---

## Stack (nativo)

| Camada | Ferramenta | Não usar |
|--------|------------|----------|
| Browser ads | Canal Meta + canal Google | Pixel no tema · Klaviyo · GTM extra |
| E-mail marketing | **Shopify Email** | Klaviyo (adiado) |
| Carrinho abandonado | Shopify Email · Abandoned cart | App terceiro |
| Checkout abandonado | Shopify Email **ou** e-mail nativo checkout — **nunca os dois** | — |
| Newsletter | `{% form 'customer' %}` footer (tag `newsletter`) | Embed Klaviyo |

---

## 1. Shopify Email — ligar automações

Admin: [E-mail](https://admin.shopify.com/store/emporiosaibai/email_marketing) · [Automações](https://admin.shopify.com/store/emporiosaibai/marketing/automations)

Remetente: `contato@saibai.com.br` · Empório Saibai  
KV: botão `#76BD22` · fundo `#F2F5EE` · texto `#2A3A1A`

| Automação | Trigger | Delay | Cupom | Objetivo |
|-----------|---------|------:|-------|----------|
| Welcome | Inscrito (tag `newsletter`) | 0 + 2º e-mail 2d | `5%NOVOCLIENTE` | Primeira compra |
| Abandoned cart | Item no carrinho, sem checkout | 1h | **Único 5% · expira 48h** | Recuperar carrinho |
| Abandoned checkout | Checkout iniciado, não pago | 10h | Mesmo único 5% 48h | Recuperar checkout |
| Browse abandonment | View produto, sem ATC | 24h | Nenhum | Trazer à PDP |
| Post-purchase | Pedido pago | +3d | Nenhum | Conservas + review |
| Win-back | 45d sem compra | 0 | `SAIBAIRECOMPRA` | Recompra |

**Anti-duplicata checkout:** se Abandoned checkout Shopify Email = ON → desligar [e-mail nativo de checkout abandonado](https://admin.shopify.com/store/emporiosaibai/settings/checkout).

Desconto único 5%/48h: no editor da automação → Add discount → Generate unique codes → 5% · expires in 2 days · once per customer. **Não** usar `SAIBAIRECOMPRA` no carrinho (esse é win-back).

---

## 2. Copy pronta (colar no editor)

### Welcome (assunto)
`5% na primeira compra no Empório Saibai`

Corpo curto:
> Olá! Bem-vindo à produção de alcachofras de Piedade, SP.  
> Cupom de boas-vindas: **5%NOVOCLIENTE** — um uso por cliente, válido no checkout.  
> CTA: Ver conservas → `https://emporiosaibai.com.br/collections/todos`

### Abandoned cart (assunto)
`Seu carrinho Saibai ainda está aqui`

> Você separou alcachofras/conservas e não finalizou.  
> Frete grátis acima de R$ 389,90.  
> CTA: Voltar ao carrinho (link nativo Shopify)

### Abandoned checkout (assunto)
`Faltou pouco para receber Saibai em casa`

> Seu pedido está reservado no checkout. PIX e cartão no mesmo fluxo.  
> CTA: Concluir compra (link checkout Shopify)

### Win-back (assunto)
`8% de recompra — conservas Saibai o ano todo`

> Já faz um tempo desde o último pedido. Conservas artesanais não dependem da safra.  
> Cupom **SAIBAIRECOMPRA** — 8% acima de R$ 120, um uso.  
> CTA: Ver conservas

### Post-purchase (assunto)
`Como guardar sua alcachofra Saibai`

> Fresca: refrigerar e consumir em até 5 dias.  
> Quer alcachofra o ano todo? As conservas estão na loja.  
> CTA: Ver conservas

---

## 3. Remarketing (pixel nativo)

Pré-requisito: [Canal Meta](https://admin.shopify.com/store/emporiosaibai/marketing/channels/facebook) → pixel `2017630342068049`.

**Criado 26/08 (ACTIVE — ads em review):**

| Recurso | ID | Status |
|---------|-----|--------|
| Campanha ABO | `120254745092470155` | ACTIVE |
| Ad set | `120254745105900155` | ACTIVE |
| Ad CR1 diferença | `120254745477920155` | ACTIVE / IN_PROCESS |
| Ad CR1 jul | `120254745478710155` | ACTIVE / IN_PROCESS |
| Cart 7d | `120254745030010155` | — |
| Checkout 7d | `120254745030300155` | — |
| Site 14d | `120254745030200155` | — |
| Exclusão Purchase 180d | `120233992642380155` | — |
| CBO vazia (ignorar) | `120254745036130155` | PAUSED |

Ads Manager: https://www.facebook.com/adsmanager/manage/adsets?act=1199864388174624&selected_adset_ids=120254745105900155

Falta: Shopify Email automações no Admin (segmentos já criados via CLI). Budget R$ 15/d · bid cap R$ 80 purchase.

Campanha paga: **SB-M-004** — **ACTIVE** 26/08 (ads IN_PROCESS).  
Google remarketing: **BLOQUEADO** até MCC `9513237350`.

---

## 4. Tema (LIVE `#187189297470`)

| Arquivo | Mudança |
|---------|---------|
| `layout/theme.liquid` | Carrega `saibai-coupon-popup` (antes o popup existia e **não renderizava**) |
| `sections/saibai-coupon-popup.liquid` | JS sempre no ar (apply no carrinho); popup oculto para quem já comprou |
| `snippets/saibai-cart-coupon-hint.liquid` | Hide se já cliente ou cupom aplicado |
| `assets/saibai-coupon-popup.js` | Botão «Aplicar cupom» preenche o form nativo |
| `sections/saibai-footer.liquid` | Sucesso newsletter cita `5%NOVOCLIENTE` |

Push (preview primeiro; live só com **PUBLICAR LIVE AGORA**):

```bash
cd clients/saibai/theme
shopify theme push --store byinbz-0k.myshopify.com --theme 186124239166 \
  --only layout/theme.liquid \
  --only sections/saibai-coupon-popup.liquid \
  --only snippets/saibai-cart-coupon-hint.liquid \
  --only assets/saibai-coupon-popup.js \
  --only sections/saibai-footer.liquid
```

---

## 5. Validação

| # | Teste | Esperado |
|---|-------|----------|
| 1 | Admin → Descontos | `5%NOVOCLIENTE` e `SAIBAIRECOMPRA` ACTIVE |
| 2 | Aba anônima → aceitar cookies → sair da página | Popup 5% |
| 3 | Carrinho → cupom → Aplicar | 5% no subtotal |
| 4 | Cliente com pedido anterior | Sem popup / sem dica welcome |
| 5 | Newsletter footer | Cliente tag `newsletter` + e-mail Welcome (após ligar automação) |
| 6 | Checkout abandonado teste | 1 e-mail só (Email **ou** nativo) |
| 7 | DevTools | 1 GA4 + 1 Meta browser · IDs tema vazios |

---

## Vereditos

| Área | Veredito |
|------|----------|
| Tracking nativo | **PASS** — não alterado |
| Cupons CRM | **PASS** — criados na API |
| Tema popup/carrinho | **PASS** — live `#187189297470` |
| Shopify Email automações | **PENDING** — clique Admin (API ACCESS_DENIED) |
| Remarketing pago | **ACTIVE** — SB-M-004 · 2 ads IN_PROCESS |
| Klaviyo | **NÃO INSTALAR** nesta fase |
