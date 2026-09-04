# Empório Saibai — Runbook Go-Live P0

**Data:** 2026-06-25  
**Veredito geral:** **PRECISA HOTFIX** — código Veltrus PASS · ações merchant + auth Shopify pendentes  
**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br) · Admin `byinbz-0k.myshopify.com`  
**Tema live:** `#186124239166` · **Tracking:** [tracking-eta-eight.vercel.app](https://tracking-eta-eight.vercel.app)

> Runbook operacional da seção **1** do `CHECKLIST_MANUAL_SAIBAI.md`.  
> Ordem importa — não pular etapas de tracking antes de ligar campanhas Sales.

---

## Visão rápida

| Bloco | Quem | Veredito |
|-------|------|----------|
| Deploy hotfix cart drawer | Veltrus (Shopify CLI auth) | **PENDENTE_AUTH** |
| GA4 API Secret → Vercel | Veltrus + merchant GA4 | [ ] |
| App Saibai Tracking (`read_orders`) | Merchant | [ ] |
| Pagamentos PIX/cartão live | Merchant | [ ] |
| Canais Google/Meta + pixel checkout | Merchant + Veltrus QA | [ ] |
| LGPD (banner Shopify off) | Merchant | [ ] |
| Acesso GA4 Veltrus + MCC Google | Merchant | [ ] |

---

## Fase A — Veltrus (terminal)

### A1. Auth Shopify + deploy hotfix CSS

**Bloqueio atual:** CLI sem acesso à loja `byinbz-0k`.

```bash
bash clients/saibai/ops/scripts/shopify-auth-full.sh

cd clients/saibai/theme
shopify theme push --store byinbz-0k.myshopify.com --theme 186124239166 --allow-live \
  --only assets/saibai-shell-cta.css assets/saibai-shell-kv.css \
         assets/saibai-shell-layout.css assets/saibai-pages-cart.css
```

**QA drawer (aba anônima):**

| # | Teste | Esperado |
|---|-------|----------|
| 1 | Ícones cupom/nota/frete | Visíveis · fundo claro |
| 2 | Hover function block | Verde `#76BD22` + ícone branco |
| 3 | Qty +/- | Ícones brancos sempre |
| 4 | X remover | Visível sem hover |
| 5 | Preço | Uma vez só (coluna direita) |

Doc: `theme/docs/HOTFIX-2026-06-25-cart-drawer-icons.md` · eKyte **#9712906**

**Probe live (pré-deploy):** CSS live **não** contém regras `function-block` — hotfix ainda **não** publicado.

---

### A2. GA4 Measurement Protocol → Vercel

```bash
cd tracking
GA4_API_SECRET="<secret do merchant>" ./scripts/configure-destinations.sh
```

| ID | Valor |
|----|-------|
| GA4 | `G-VWX77SGD1W` |
| Meta Pixel | `2017630342068049` |

**Probe proxy (25/06):** `GET /apps/vlt-tracking/events` → `405` (esperado POST-only) · rota Vercel ativa.

---

### A3. Pixel checkout (Customer Events)

```bash
python3 clients/saibai/ops/scripts/configure-saibai-customer-events-pixel.py
```

Arquivo gerado: `clients/saibai/ops/scripts/saibai-customer-events-pixel.generated.js`

**Merchant cola em:** Admin → Configurações → Eventos do cliente  
Nome: `Saibai Veltrus Checkout Events` · Permissões: Análise + Marketing

**Anti-duplicata:** Theme Settings → Saibai Tracking → GA4/Meta **vazios**. Browser = canais Shopify. Server = Vercel.

---

## Fase B — Merchant (Admin Shopify)

### B1. Reinstalar app tracking (webhook `orders/paid`)

[Instalar Saibai Tracking](https://admin.shopify.com/store/byinbz-0k/oauth/install?client_id=0f5ea7f8dd46a060c5416f21573c9256)

Scope necessário: `read_orders`

---

### B2. Pagamentos

| # | Ação |
|---|------|
| 1 | Concluir Shopify Payments Brasil (CNPJ + conta) |
| 2 | Ativar PIX, Boleto, Cartão, Shop Pay |
| 3 | Descriptor: `EMPORIO SAIBAI` |
| 4 | Modo teste **OFF** em produção |

Links: [Pagamentos](https://admin.shopify.com/store/emporiosaibai/settings/payments)

---

### B3. LGPD

| # | Ação |
|---|------|
| 1 | Desligar banner cookies nativo Shopify |
| 2 | Região Brasil (BR) — consentimento obrigatório |
| 3 | Política custom — colar `ops/scripts/output/saibai-privacy-policy-paste.html` |

Links: [Privacidade](https://admin.shopify.com/store/emporiosaibai/settings/privacy) · [Legal](https://admin.shopify.com/store/emporiosaibai/settings/legal)

---

### B4. Canais martech browser

| Canal | ID | Link |
|-------|-----|------|
| Google & YouTube | `G-VWX77SGD1W` | [Canal Google](https://admin.shopify.com/store/emporiosaibai/marketing/channels/google) |
| Facebook & Instagram | `2017630342068049` | [Canal Meta](https://admin.shopify.com/store/emporiosaibai/marketing/channels/facebook) |

Confirmar Theme Settings → `tracking_endpoint` = `/apps/vlt-tracking/events`

---

### B5. Acessos Veltrus (desbloqueia MCP)

| Plataforma | Ação merchant |
|------------|---------------|
| GA4 | Conceder property `G-VWX77SGD1W` à conta Veltrus |
| Google Ads | Aceitar convite MCC na conta `9513237350` |

---

## Fase C — Validação conjunta (smoke test)

Ordem recomendada após B1 + A2:

1. Aba anônima → aceitar cookies Saibai → DevTools → POST `vlt-tracking` → **202**
2. Pedido teste pago → Supabase `tracking_events` → evento `purchase`
3. [Meta Test Events](https://business.facebook.com/events_manager2/list/pixel/2017630342068049) → Purchase server
4. GA4 DebugView → `purchase` + `add_to_cart`
5. Checkout teste → pixel Customer Events → `checkout_completed`

Checklist completo: `theme/docs/SMOKE_TEST_v1.2.4.md`

---

## Fase D — Pós-validação (Veltrus ads)

Só após purchase validado end-to-end:

1. Atualizar `VELTRUS-GA4-REGISTRY.json` (GA4 MCP)
2. Re-auditar Meta MCP
3. Approval request campanha Meta Sales D2C (`APPROVAL_REQUESTS.md`)

---

## Referências

| Doc | Uso |
|-----|-----|
| `CHECKLIST_MANUAL_SAIBAI.md` | Checklist completo merchant |
| `TRACKING_AUDIT.md` | Stack server-side |
| `CLIENT_CONTEXT.md` | IDs canônicos |
| `DELIVERY-2026-06-25-dossie-v1.md` | Entrega dossiê v1 |
| `APPROVAL_REQUESTS.md` | Fila mutations ads |

---

## Vereditos

| Área | Veredito |
|------|----------|
| Código tema + tracking | **PASS** |
| Deploy hotfix CSS | **PENDENTE_AUTH** |
| Go-live merchant | **PRECISA HOTFIX** |
| Meta estratégia Sales | **PRECISA AUDITORIA** (após purchase) |
