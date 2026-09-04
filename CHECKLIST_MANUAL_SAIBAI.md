# Checklist Manual — Empório Saibai

**Veltrus Growth & Technology** · Atualizado: junho 2026  
**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br) · Admin: `byinbz-0k.myshopify.com`  
**Tema live:** #186124239166 · **Tracking:** [tracking-eta-eight.vercel.app](https://tracking-eta-eight.vercel.app)

> Tudo que **não** roda sozinho — credenciais, cliques no Admin, instalações, validações.  
> Código/API já feito pela Veltrus está na seção **0**. Marque `[x]` conforme concluir.

---

## 0. Já feito (Veltrus — não precisa refazer)

| Item | Status |
|------|--------|
| Tema Saibai (KV, header, home, footer, LGPD) | ✅ Live |
| Banner cookies Saibai + Consent Mode v2 | ✅ No tema |
| Client tracking `saibai-tracking-client.js` (pós-LGPD) | ✅ No repo |
| App Proxy `/apps/vlt-tracking/events` | ✅ Deployado |
| App Shopify **Saibai Tracking** (`saibai-tracking-3`) | ✅ Partners |
| API Vercel + Supabase (`saibai-tracking`) | ✅ Produção |
| Meta CAPI server-side | ✅ Token configurado + testado |
| Webhook `orders/paid` (código + rota) | ✅ Deployado |
| Dedupe purchase por `order_id` | ✅ No código |
| Theme Settings → IDs GA4/Meta **vazios** (anti-duplicata) | ✅ Configurado |
| Coleções, menus, cupom, frete grátis R$280, traduções pt-BR | ✅ Via API |

---

## 1. CRÍTICO — faça primeiro (bloqueia tracking + vendas)

### 1.1 Tracking server-side

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Gerar **GA4 API Secret** | [GA4 Admin](https://analytics.google.com/) → Admin → Data Streams → `G-VWX77SGD1W` → Measurement Protocol → Create | [ ] |
| 2 | Configurar no Vercel | `cd tracking && GA4_API_SECRET="..." ./scripts/configure-destinations.sh` | [ ] |
| 3 | **Reinstalar app** Saibai Tracking (scope `read_orders` para webhook) | [Instalar app](https://admin.shopify.com/store/byinbz-0k/oauth/install?client_id=0f5ea7f8dd46a060c5416f21573c9256) | [ ] |
| 4 | Validar proxy na loja | Aba anônima → aceitar cookies → DevTools → `vlt-tracking` → `202` | [ ] |
| 5 | Validar webhook | Pedido teste pago → Supabase `tracking_events` → `purchase` | [ ] |
| 6 | Meta Test Events | [Events Manager](https://business.facebook.com/events_manager2/list/pixel/2017630342068049) → Purchase server | [ ] |
| 7 | GA4 DebugView | Property `G-VWX77SGD1W` → evento `purchase` após pedido teste | [ ] |

**IDs fixos (não mudar):**

| Canal | ID |
|-------|-----|
| GA4 | `G-VWX77SGD1W` |
| Meta Pixel | `2017630342068049` |

**Regra:** GA4/Meta browser = **canais Shopify**. Theme Settings → Saibai Tracking → IDs **vazios**. Server = Vercel.

---

### 1.2 Pagamentos (vender de verdade)

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Concluir verificação **Shopify Payments Brasil** (CNPJ + conta) | [Pagamentos](https://admin.shopify.com/store/emporiosaibai/settings/payments/shopify-payments) | [ ] |
| 2 | Ativar **PIX**, **Boleto**, **Cartão**, **Shop Pay** | [Pagamentos](https://admin.shopify.com/store/emporiosaibai/settings/payments) | [ ] |
| 3 | Descriptor fatura: `EMPORIO SAIBAI` | Pagamentos | [ ] |
| 4 | Modo teste **DESLIGADO** em produção | Pagamentos | [ ] |
| 5 | Ordem checkout: PIX → Cartão → Shop Pay → Boleto | Pagamentos | [ ] |

---

### 1.3 LGPD & legal

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | **Desligar** banner cookies nativo Shopify | [Privacidade](https://admin.shopify.com/store/emporiosaibai/settings/privacy) | [ ] |
| 2 | Adicionar região **Brasil (BR)** — consentimento obrigatório | Privacidade | [ ] |
| 3 | Política de privacidade custom: desativar «Gerenciamento automático» | [Legal](https://admin.shopify.com/store/emporiosaibai/settings/legal) | [ ] |
| 4 | Colar HTML | Arquivo: `ops/scripts/output/saibai-privacy-policy-paste.html` | [ ] |

---

### 1.4 Martech browser (canais + checkout)

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Conectar canal **Google** → GA4 `G-VWX77SGD1W` | [Google channel](https://admin.shopify.com/store/emporiosaibai/marketing/channels/google) | [ ] |
| 2 | Conectar canal **Meta** → Pixel `2017630342068049` | [Meta channel](https://admin.shopify.com/store/emporiosaibai/marketing/channels/facebook) | [ ] |
| 3 | Gerar pixel checkout: `python3 ops/scripts/configure-saibai-customer-events-pixel.py` | Terminal | [ ] |
| 4 | Colar pixel em **Eventos do cliente** | [Customer Events](https://admin.shopify.com/store/emporiosaibai/settings/customer_events) · arquivo: `ops/scripts/saibai-customer-events-pixel.generated.js` | [ ] |
| 5 | Nome: `Saibai Veltrus Checkout Events` · Permissões: Análise + Marketing | Customer Events | [ ] |
| 6 | ⚠️ **Não duplicar purchase** — canal OU pixel no checkout, não os dois | Customer Events + canais | [ ] |
| 7 | Confirmar Theme Settings → Saibai Tracking → IDs **vazios** | [Theme Settings](https://admin.shopify.com/store/emporiosaibai/themes/186124239166/editor?context=settings) | [ ] |
| 8 | Confirmar `tracking_endpoint` = `/apps/vlt-tracking/events` | Theme Settings | [ ] |

---

### 1.5 Checkout branding (plano Basic = manual)

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Branding KV Saibai no checkout | [Checkout](https://admin.shopify.com/store/emporiosaibai/settings/checkout) → Personalizar | [ ] |
| 2 | Botão `#76BD22` · Fundo `#F4F9F0` · Texto `#2A3A1A` · Fonte **Jost** | Checkout | [ ] |
| 3 | Logo Empório Saibai | Checkout | [ ] |
| 4 | Repetir visual em **Contas de cliente** | [Customer accounts](https://admin.shopify.com/store/emporiosaibai/settings/customer_accounts) | [ ] |

Guia detalhado: `theme/docs/CHECKOUT_BRANDING_GUIA.md`

---

## 2. ALTO — identidade & confiança

### 2.1 Configurações gerais

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Nome: `Empório Saibai` (com acento) | [Geral](https://admin.shopify.com/store/emporiosaibai/settings/general) | [ ] |
| 2 | E-mail do cliente: `contato@saibai.com.br` | Geral | [ ] |
| 3 | Descrição da loja (copy Saibai) | Geral | [ ] |
| 4 | Endereço legal + CEP (conferir 18170-000 vs 18176-210) | Geral | [ ] |
| 5 | Telefone: (15) 99799-9938 | Geral | [ ] |
| 6 | SSL ativo em `emporiosaibai.com.br` | [Domínios](https://admin.shopify.com/store/emporiosaibai/settings/domains) | [ ] |

---

### 2.2 E-mails transacionais

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Branding e-mails (logo + `#76BD22`) | [Notificações](https://admin.shopify.com/store/emporiosaibai/settings/notifications) | [ ] |
| 2 | Colar 6 templates HTML | `ops/scripts/output/notifications/*.html` | [ ] |
| 3 | Notificações equipe → `contato@saibai.com.br` | Notificações | [ ] |
| 4 | Enviar e-mail de teste em cada modelo | Notificações | [ ] |

Checklist templates: `ops/scripts/output/notifications/CHECKLIST.md`

---

### 2.3 Apps (aprovação Saibai)

Ordem: **Clarity OFF → TinySEO → Judge.me → Shopify Email**  
Klaviyo **não** nesta fase (tracking nativo + CRM Shopify).

| # | App | Ação | Status |
|---|-----|------|--------|
| 1 | **Microsoft Clarity** | Desinstalar + desligar embeds no tema | [ ] |
| 2 | **TinySEO** | [Instalar](https://apps.shopify.com/smart-image-optimizer) + 7 embeds JSON-LD ON | [ ] |
| 3 | **Judge.me** | [Instalar](https://apps.shopify.com/judgeme) + widget PDP | [ ] |
| 4 | **Shopify Email** | [Automações](https://admin.shopify.com/store/emporiosaibai/marketing/automations) · Welcome + cart + checkout + win-back | [ ] |
| 5 | Cupons CRM | `5%NOVOCLIENTE` + `SAIBAIRECOMPRA` já LIVE via API · playbook `docs/CRM-NATIVO-SHOPIFY-SAIBAI.md` | [x] |
| 6 | **Stape** (se usar) | Auditar sGTM — sem duplicar GA4/Meta browser | [ ] |
| 7 | Salvar tema após alterar app embeds | [Theme Editor → Apps](https://admin.shopify.com/store/emporiosaibai/themes/186124239166/editor?context=apps) | [ ] |

Script guia: `python3 ops/scripts/optimize-saibai-apps-install.py` · CRM: `python3 ops/scripts/configure-saibai-crm-native.py`

---

### 2.4 Deploy tema (se houver alterações locais)

```bash
cd theme
shopify theme push --store byinbz-0k.myshopify.com --theme 186124239166 --allow-live
```

Push parcial tracking:

```bash
shopify theme push --store byinbz-0k.myshopify.com --theme 186124239166 --allow-live \
  --only assets/saibai-tracking-client.js snippets/saibai-tracking-config.liquid \
  sections/saibai-consent-popup.liquid config/settings_schema.json
```

| # | Ação | Status |
|---|------|--------|
| 1 | Push tema para live | [ ] |
| 2 | Confirmar publicação no Admin → Temas | [ ] |
| 3 | Reauth CLI se falhar: `bash ops/scripts/shopify-auth-full.sh` | [ ] |

---

## 3. VALIDAÇÃO — 15 min após concluir seção 1

| # | Teste | Como validar | Status |
|---|-------|--------------|--------|
| 1 | Banner LGPD | Aba anônima → modal aparece | [ ] |
| 2 | Consent → tracking | Aceitar → Network `vlt-tracking` → `202` | [ ] |
| 3 | 1 GA4 + 1 Meta browser | DevTools após consent (sem duplicata) | [ ] |
| 4 | Checkout teste | pt-BR · branding verde · convidado OK | [ ] |
| 5 | Pagamento sandbox | PIX ou cartão teste | [ ] |
| 6 | E-mail confirmação | Remetente `contato@` · logo Saibai | [ ] |
| 7 | Cupom `5%NOVOCLIENTE` | Carrinho | [ ] |
| 8 | Mobile 375px | Drawer, hero, WhatsApp | [ ] |
| 9 | Purchase server | Pedido pago → Meta Events Manager + Supabase | [ ] |
| 10 | Smoke test completo | `theme/docs/SMOKE_TEST_v1.2.4.md` | [ ] |

---

## 4. MÉDIO — performance & operação

### 4.1 Theme settings (performance)

Desativar no Theme Editor → Settings:

| # | Setting | Motivo | Status |
|---|---------|--------|--------|
| 1 | Preloading screen | Atrasa first paint | [ ] |
| 2 | Floating icons | JS/CSS extra | [ ] |
| 3 | Countdown nos cards | Performance | [ ] |
| 4 | Reveal on scroll (home) | Não necessário | [ ] |

Guia: `theme/docs/PERF_FASE2.md`

---

### 4.2 Contas de cliente & frete

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | Validar portal cliente (login, pedidos, endereços BR) | `shopify.com/.../account` | [ ] |
| 2 | Ativar **Entrar com Shop** (se disponível) | Customer accounts | [ ] |
| 3 | Validar prazos frete por região | [Frete](https://admin.shopify.com/store/emporiosaibai/settings/shipping) | [ ] |
| 4 | Ocultar metafields fashion não usados | [Dados personalizados](https://admin.shopify.com/store/emporiosaibai/settings/custom_data) | [ ] |

---

### 4.3 Tracking fase 2 (opcional agora)

| # | Ação | Onde | Status |
|---|------|------|--------|
| 1 | `INNGEST_EVENT_KEY` + `INNGEST_SIGNING_KEY` | [Inngest](https://www.inngest.com/) + Vercel | [ ] |
| 2 | Alertas Slack/n8n | Vercel env (opcional) | [ ] |
| 3 | Link GA4 → BigQuery | GA4 Admin → Product Links | [ ] |
| 4 | Google Ads Enhanced Conversions | Google Ads (fase 2) | [ ] |
| 5 | Regenerar token Meta (segurança — foi exposto no chat) | Meta Events Manager | [ ] |

---

## 5. CONTÍNUO — safra & conteúdo

| # | Ação | Frequência | Status |
|---|------|------------|--------|
| 1 | Estoque/preço SKUs frescos (`in-natura-1`) | Semanal | [ ] |
| 2 | Fotos alinhadas ao brief | Quando trocar imagens | [ ] |
| 3 | Comunicar safra no WhatsApp VIP | Sazonal | [ ] |
| 4 | GTmetrix / PageSpeed | Mensal | [ ] |
| 5 | Google Search Console + sitemap | Uma vez | [ ] |
| 6 | Remover fallback Loox (após Judge.me) | Uma vez — pedir Veltrus | [ ] |

Brief fotografia: `theme/docs/BRIEF_FOTOGRAFIA_CATALOGO_SAIBAI.md`

---

## 6. Onde acompanhar os dados

| O quê | Onde |
|-------|------|
| Vendas reais | [Shopify Admin → Pedidos](https://admin.shopify.com/store/emporiosaibai/orders) |
| Tráfego & funil | [GA4](https://analytics.google.com/) · property `G-VWX77SGD1W` |
| Campanhas Meta | [Events Manager](https://business.facebook.com/events_manager2/) + Ads Manager |
| Eventos server-side (debug) | [Supabase](https://supabase.com/dashboard/project/vlqxrmejvkxnlmpqhkvt) → `tracking_events` |
| Saúde da API | [Vercel](https://vercel.com/emevertons-projects/tracking) → Logs |
| BI avançado (futuro) | BigQuery (export GA4) |

**GTM/Stape:** não obrigatório. Stack atual = Canais Shopify (browser) + Vercel (server). Só adicionar GTM se precisar de tags extras (TikTok, etc.) — ver `tracking/SETUP_SAIBAI.md`.

---

## 7. Arquivos para colar no Admin

| Arquivo local | Colar em |
|---------------|----------|
| `ops/scripts/output/saibai-privacy-policy-paste.html` | Legal → Privacidade |
| `ops/scripts/output/notifications/*.html` | Notificações → modelos |
| `ops/scripts/saibai-customer-events-pixel.generated.js` | Eventos do cliente |

---

## 8. Scripts úteis (terminal)

```bash
# Auditoria martech completa
python3 ops/scripts/saibai-martech-audit.py

# Gerar pixel checkout
python3 ops/scripts/configure-saibai-customer-events-pixel.py

# Testar tracking local
cd tracking && npm run test:proxy && npm run test:webhook

# Testar DB Supabase
cd tracking && npm run test:db
```

---

## 9. Ordem recomendada (resumo)

```
1. GA4_API_SECRET + reinstalar app (webhook)
2. Pagamentos live (PIX/cartão)
3. LGPD (privacidade + banner Shopify OFF)
4. Canais Google/Meta + pixel checkout
5. Checkout branding
6. Validar tracking (aba anônima + pedido teste)
7. Geral + e-mails + Shopify Email (TinySEO/Judge.me)
8. Performance settings + QA smoke test
```

---

## 10. Docs de referência

| Documento | Uso |
|-----------|-----|
| `CHECKLIST_MANUAL_SAIBAI.md` | **Este arquivo** — ações manuais |
| `theme/docs/DESPACHO_SAIBAI.md` | Checklist operacional completo |
| `tracking/SETUP_SAIBAI.md` | Setup tracking server-side |
| `theme/docs/CHECKOUT_BRANDING_GUIA.md` | Branding checkout manual |
| `theme/docs/SMOKE_TEST_v1.2.4.md` | QA pós-deploy |
| `theme/docs/GUIA_SAIBAI_LEIGO.md` | Operação diária sem código |

---

**Suporte técnico:** Veltrus · **Loja:** contato@saibai.com.br
