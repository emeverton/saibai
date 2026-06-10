# DESPACHO — Empório Saibai · Operação & Go-Live

**Veltrus Growth & Technology** · Shopify Partner  
**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br) · Admin: `byinbz-0k.myshopify.com`  
**Tema live:** Saibai by Veltrus · ID **#186124239166**  
**Atualizado:** junho 2026 · **Safra 2026** (alcachofra fresca ativa)

> Checklist operacional único. Tudo que **não** dá para fazer via API/CLI está na **seção 2**.  
> Scripts de auditoria: seção 8.

---

## 1. Status rápido (já no ar via API/tema)

| Área | Status |
|------|--------|
| Tema Saibai (KV, header, home, footer, LGPD) | ✅ Live |
| Conta cliente BR + novas contas Shopify (links portal) | ✅ Live |
| Cupom popup `5%NOVOCLIENTE` + hint no carrinho | ✅ Live |
| Checkout & system pt-BR | ✅ 2.550 strings (`locales/pt-BR.json` → `shopify`) |
| Coleções SEO (6 do menu) + produtos metafields Saibai | ✅ API |
| Safra fresca `in-natura-1` (2 SKUs) | ✅ Ativa |
| Frete grátis automático R$ 280 | ✅ API |
| Políticas legais 5/6 (Contato, Frete, Reembolso, Termos, Cancelamentos) | ✅ API |
| Páginas institucionais + redirects legado | ✅ API |
| Metaobjetos demo fashion removidos | ✅ API |
| Menus header/footer Saibai | ✅ API |
| Theme Settings → Saibai Tracking (IDs vazios) | ✅ Anti-duplicata |
| Contas: OPTIONAL · novas contas · login visível | ✅ API |
| Moeda BRL · fuso Brasília · mercado Brasil | ✅ API |

---

## 2. CHECKLIST MANUAL — Admin Shopify (completo)

Base admin: `https://admin.shopify.com/store/emporiosaibai`

### Prioridade P0 — bloqueia go-live 10/10

#### 2.1 Configurações → Geral  
`…/settings/general` · Script: `python3 ../ops/scripts/optimize-saibai-general-settings.py`

- [ ] **Nome da loja:** `Empório Saibai` (com acento — hoje: `Emporio Saibai`)
- [ ] **E-mail do cliente** (remetente checkout/e-mails): `contato@saibai.com.br` (hoje: `comercial@saibai.com.br`)
- [ ] **E-mail da loja:** confirmar `contato@saibai.com.br` (já OK)
- [ ] **Descrição da loja:**  
  `Empório Saibai — produtora e distribuidora de alcachofras frescas e conservas artesanais em Piedade, SP, Capital Nacional da Alcachofra. Entrega para todo o Brasil.`
- [ ] **Endereço legal:** Estrada dos Lavradores, 7 · Piedade, SP · CEP **18170-000** (conferir — API mostra 18176-210)
- [ ] **Telefone:** (15) 99799-9938
- [ ] **Domínios** `…/settings/domains` — SSL ativo em `emporiosaibai.com.br`

#### 2.2 Configurações → Legal  
`…/settings/legal` · Script: `python3 ../ops/scripts/optimize-saibai-legal-policies.py`

- [ ] **Política de privacidade** — API bloqueada (gerenciamento automático Shopify):
  1. Desative «Gerenciamento automático»
  2. Cole HTML de `../ops/scripts/output/saibai-privacy-policy-paste.html`
  3. Salve

#### 2.3 Configurações → Privacidade do cliente  
`…/settings/privacy` · Script: `python3 ../ops/scripts/optimize-saibai-privacy-settings.py`

- [ ] **Banner cookies Shopify nativo:** DESLIGAR (tema usa banner Saibai LGPD)
- [ ] **Consentimento por região:** adicionar **Brasil (BR)** — consentimento obrigatório
- [ ] **Política de privacidade custom** (mesmo passo 2.2 se ainda automática)
- [ ] CCPA/opt-out EUA: só se vender para Califórnia (DTC BR: ignorar)

#### 2.4 Configurações → Checkout  
`…/settings/checkout` · Script: `python3 ../ops/scripts/optimize-saibai-checkout-settings.py`

- [ ] **Personalizar** → branding KV Saibai (API exige Shopify Plus — plano Basic = manual):
  - Destaque / botão: `#76BD22` (hover `#5A9018`)
  - Fundo: `#F4F9F0` · Texto: `#2A3A1A` · Borda: `#E2EDDA`
  - Fonte: **Jost** · Cantos 4px
  - Logo Empório Saibai
- [ ] Aplicar o **mesmo visual** na aba **Contas de cliente**

#### 2.5 Configurações → Pagamentos  
`…/settings/payments` · Script: `python3 ../ops/scripts/optimize-saibai-payments-settings.py`

- [ ] **Shopify Payments Brasil** `…/payments/shopify-payments` — concluir verificação (CNPJ + conta bancária)
- [ ] Ativar: **PIX**, **Boleto**, **Cartão crédito/débito**
- [ ] **Shop Pay** + **Parcelamento Shop Pay**
- [ ] Descriptor fatura cartão: `EMPORIO SAIBAI`
- [ ] Modo teste **DESLIGADO** em produção
- [ ] Ordem sugerida no checkout: PIX → Cartão → Shop Pay → Boleto

#### 2.6 Configurações → Eventos do cliente  
`…/settings/customer_events` · Script: `python3 ../ops/scripts/configure-saibai-customer-events-pixel.py`

- [ ] Gerar pixel: `python3 ../ops/scripts/configure-saibai-customer-events-pixel.py`
- [ ] Adicionar pixel personalizado → colar `../ops/scripts/saibai-customer-events-pixel.generated.js`
- [ ] Nome: `Saibai Veltrus Checkout Events` · Permissões: **Análise + Marketing**
- [ ] ⚠️ **Não duplicar `purchase`:** se canal Google/Meta já dispara no checkout → manter **só um** lado (canal OU pixel)

---

### Prioridade P1 — comunicação & confiança

#### 2.7 Configurações → Notificações  
`…/settings/notifications` · Script: `python3 ../ops/scripts/optimize-saibai-notifications.py`

- [ ] **Personalizar modelos de e-mail** — logo Saibai + cor `#76BD22` + pt-BR
- [ ] **E-mail do cliente** (Geral) → `contato@saibai.com.br` *(impacta remetente)*
- [ ] Colar templates de `../ops/scripts/output/notifications/`:

| Arquivo | Notificação no admin |
|---------|---------------------|
| `order_confirmation.html` | Confirmação de pedido |
| `shipping_confirmation.html` | Confirmação de envio |
| `order_cancelled.html` | Pedido cancelado |
| `refund_notification.html` | Reembolso |
| `customer_welcome.html` | Boas-vindas à conta |
| `contact_customer.html` | Contato com cliente |

- [ ] Usar `_saibai-email-header.html` + corpo Shopify + `_saibai-email-footer.html`
- [ ] **Notificações da equipe:** novo pedido → `contato@saibai.com.br`
- [ ] Enviar **e-mail de teste** em cada modelo editado

#### 2.8 Configurações → Contas de cliente  
`…/settings/customer_accounts` · Script: `python3 ../ops/scripts/optimize-saibai-customer-accounts.py`

- [ ] Confirmar (já OK na API — só validar visual):
  - Novas contas de cliente (não legadas)
  - Contas **opcionais**
  - Links de login visíveis
  - Login **não** obrigatório no checkout
- [ ] Ativar **Entrar com Shop** (se disponível)
- [ ] Branding portal = mesmo KV checkout (passo 2.4)
- [ ] Teste: login anônimo → `shopify.com/…/account` · pedidos · endereços BR

#### 2.9 Configurações → Dados personalizados  
`…/settings/custom_data` · Script: `python3 ../ops/scripts/optimize-saibai-custom-data.py`

- [ ] **Ocultar** definições fashion não usadas (não removíveis via API):
  - `shopify.color-pattern` · `shopify.material` · `shopify.target-gender`
- [ ] Confirmar definições Saibai visíveis/pinned: `custom_badge`, `short_description`, `origem`, `conservacao`, `custom_tab`

#### 2.10 Configurações → Frete e entrega  
`…/settings/shipping`

- [ ] Perfil geral: métodos Correios/transportadora BR ativos (API: 3 métodos)
- [ ] Prazos realistas por região
- [ ] Perfil «Entrega Local Sorocaba» — ativar só se operar localmente

---

### Prioridade P2 — Martech & apps

#### 2.11 Remover — Microsoft Clarity  
`…/settings/apps` · **Sem permissão apps via CLI**

- [ ] **Desinstalar** app Microsoft Clarity
- [ ] Theme Editor → App embeds → **DESLIGAR** `Clarity JS` + `Clarity Agents JS`  
  `…/themes/186124239166/editor?context=apps`

#### 2.12 Instalar apps (aprovação Saibai)  
Script: `python3 ../ops/scripts/optimize-saibai-apps-install.py`

Ordem: **Clarity OFF → TinySEO → Judge.me → Klaviyo**

| # | App | Instalar | Pós-instalação |
|---|-----|----------|----------------|
| 1 | **TinySEO** | [App Store](https://apps.shopify.com/smart-image-optimizer) | 7 embeds JSON-LD + broken links ON no Theme Editor |
| 2 | **Judge.me** | [App Store](https://apps.shopify.com/judgeme) | Sync Shopify · widget PDP · badge embed |
| 3 | **Klaviyo** | [App Store](https://apps.shopify.com/klaviyo-email-marketing-sms) | Sync · welcome · carrinho · pós-compra · safra |

- [ ] **TinySEO** — ligar embeds: Article, Breadcrumb, Collection, Product, Store, Website JSON-LD + Broken links
- [ ] **Judge.me** — após 1ª review: pedir Veltrus remover fallback Loox em `snippets/product-review-rating.liquid`
- [ ] **Klaviyo** — atualizar política privacidade (menção processamento e-mail marketing)
- [ ] **Stape** — auditar GTM server: CAPI + dedupe; **sem** tags browser duplicando GA4/Meta dos canais Shopify

#### 2.13 Marketing → Canais  
Script: `python3 ../ops/scripts/saibai-martech-audit.py`

- [ ] **Google** `…/marketing/channels/google` → GA4 `G-VWX77SGD1W`
- [ ] **Meta** `…/marketing/channels/facebook` → Pixel `2017630342068049`
- [ ] Theme Settings → **Saibai Tracking** → `ga4_measurement_id` e `meta_pixel_id` **VAZIOS**  
  `…/themes/186124239166/editor?context=settings`
- [ ] Validar: 1 GA4 + 1 Meta no storefront após consentimento LGPD

#### 2.14 Theme Editor → App embeds (resumo)  
Script: `python3 ../ops/scripts/saibai-app-embeds-checklist.py`

**LIGAR:** TinySEO (7) · Judge.me badge · Stape (se ativo) · Avada Order Limit (se usar)  
**DESLIGAR:** Clarity JS · Clarity Agents JS  
**Salvar tema** após alterar embeds.

---

### Prioridade P3 — operação contínua

#### 2.15 Safra 2026 — checklist semanal

- [ ] Estoque/preço SKUs frescos (`in-natura-1`)
- [ ] Fotos e copy alinhadas à embalagem
- [ ] Comunicar embalagem térmica + consumo em 5 dias
- [ ] Aviso safra no Grupo VIP WhatsApp
- [ ] Frete grátis R$ 280 coerente com barra de anúncios

**Fim de safra:** arquivar SKUs + menu «Em breve» → `/pages/contato`

#### 2.16 Veltrus — pós-instalação Judge.me (código)

- [ ] Remover bloco Loox em `snippets/product-review-rating.liquid` (só após Judge.me sincronizado)

---

## 3. Mapa rápido Admin → URL

| Tela Shopify | URL |
|--------------|-----|
| Geral | [settings/general](https://admin.shopify.com/store/emporiosaibai/settings/general) |
| Pagamentos | [settings/payments](https://admin.shopify.com/store/emporiosaibai/settings/payments) |
| Checkout | [settings/checkout](https://admin.shopify.com/store/emporiosaibai/settings/checkout) |
| Contas de cliente | [settings/customer_accounts](https://admin.shopify.com/store/emporiosaibai/settings/customer_accounts) |
| Notificações | [settings/notifications](https://admin.shopify.com/store/emporiosaibai/settings/notifications) |
| Legal | [settings/legal](https://admin.shopify.com/store/emporiosaibai/settings/legal) |
| Privacidade | [settings/privacy](https://admin.shopify.com/store/emporiosaibai/settings/privacy) |
| Dados personalizados | [settings/custom_data](https://admin.shopify.com/store/emporiosaibai/settings/custom_data) |
| Eventos do cliente | [settings/customer_events](https://admin.shopify.com/store/emporiosaibai/settings/customer_events) |
| Apps | [settings/apps](https://admin.shopify.com/store/emporiosaibai/settings/apps) |
| Domínios | [settings/domains](https://admin.shopify.com/store/emporiosaibai/settings/domains) |
| Frete | [settings/shipping](https://admin.shopify.com/store/emporiosaibai/settings/shipping) |
| Google channel | [marketing/channels/google](https://admin.shopify.com/store/emporiosaibai/marketing/channels/google) |
| Meta channel | [marketing/channels/facebook](https://admin.shopify.com/store/emporiosaibai/marketing/channels/facebook) |
| App embeds | [Theme Editor → Apps](https://admin.shopify.com/store/emporiosaibai/themes/186124239166/editor?context=apps) |
| Theme Settings | [Theme Editor → Settings](https://admin.shopify.com/store/emporiosaibai/themes/186124239166/editor?context=settings) |

---

## 4. Catálogo & navegação

| Destino | URL |
|---------|-----|
| Todos os produtos | `/collections/todos` |
| Conservas | `/collections/em-conserva` |
| Flores desidratadas | `/collections/flores-desidratadas` |
| Frutas desidratadas | `/collections/frutas-desidratadas` |
| Chaveiro | `/collections/chaveiro` |
| Fresca (safra) | `/collections/in-natura-1` |

**Contagens ativas:** em-conserva **3** · alcachofras **4** · in-natura-1 **2**

---

## 5. Tracking & IDs (não duplicar)

| Canal | ID |
|-------|-----|
| GA4 | `G-VWX77SGD1W` |
| Meta Pixel | `2017630342068049` |
| Cupom | `5%NOVOCLIENTE` |
| E-mail canônico | `contato@saibai.com.br` |
| KV accent | `#76BD22` |

**Regra:** IDs de pixel/GA4 **fora** do Theme Settings. Browser = canais Shopify. Checkout = pixel Customer Events. Stape = server-side only.

---

## 6. Deploy tema (Veltrus)

```bash
cd theme
shopify theme push --theme 186124239166 --allow-live
```

Push parcial:

```bash
shopify theme push --theme 186124239166 --allow-live --only snippets/arquivo.liquid
```

Reauth CLI (escopos amplos):

```bash
bash ../ops/scripts/shopify-auth-full.sh
```

---

## 7. Validação pós-deploy (15 min)

1. Home → **Fresca** → coleção 2 produtos  
2. Menu **Produtos** → `/collections/todos`  
3. Banner LGPD → aceitar → 1 GA4 + 1 Meta (Network)  
4. Checkout teste → pt-BR · branding verde · convidado OK  
5. Pagamento teste PIX/cartão (sandbox)  
6. E-mail confirmação → remetente `contato@` · logo Saibai  
7. Cupom `5%NOVOCLIENTE`  
8. Ícone conta → portal novas contas  
9. Mobile 375px — drawer, 2 cards, WhatsApp  
10. View-source PDP → 1 JSON-LD Product (após TinySEO)

---

## 8. Scripts de auditoria (repo)

| Script | Admin / uso |
|--------|-------------|
| `optimize-saibai-general-settings.py` | Geral |
| `optimize-saibai-payments-settings.py` | Pagamentos |
| `optimize-saibai-checkout-settings.py` | Checkout |
| `optimize-saibai-customer-accounts.py` | Contas de cliente |
| `optimize-saibai-notifications.py` | Notificações |
| `optimize-saibai-legal-policies.py` | Legal |
| `optimize-saibai-privacy-settings.py` | Privacidade |
| `optimize-saibai-custom-data.py` | Dados personalizados |
| `optimize-saibai-apps-install.py` | Apps (TinySEO, Judge.me, Klaviyo) |
| `saibai-app-embeds-checklist.py` | Theme Editor embeds |
| `saibai-martech-audit.py` | Martech completo |
| `configure-saibai-customer-events-pixel.py` | Pixel checkout |
| `configure-saibai-checkout-branding.py` | Branding checkout (Plus only) |
| `optimize-saibai-checkout-translations.py` | Traduções checkout pt-BR |
| `reactivate-saibai-fresca.py` | Reativar menus safra |

**Arquivos para colar no admin:**

| Arquivo | Onde colar |
|---------|------------|
| `../ops/scripts/output/saibai-privacy-policy-paste.html` | Legal → Privacidade |
| `../ops/scripts/output/notifications/*.html` | Notificações → modelos |
| `../ops/scripts/saibai-customer-events-pixel.generated.js` | Eventos do cliente |

---

## 9. Docs & contatos

| Doc | Uso |
|-----|-----|
| `DESPACHO_SAIBAI.md` | **Este checklist** (Notion / operação) |
| `GUIA_SAIBAI_LEIGO.md` | Operação diária sem código |
| `RELATORIO_EXECUTIVO_SAIBAI.md` | Visão estratégica |

**Suporte técnico tema:** Veltrus · **Loja:** contato@saibai.com.br

---

## 10. Histórico de decisões

- **Jun/2026:** Safra reativada — `in-natura-1`, menus, home links.  
- **Jun/2026:** Legal 5/6 API · privacidade manual · LGPD banner Saibai + Consent Mode v2.  
- **Jun/2026:** Checkout/contas/pagamentos/geral — scripts audit 10/10; gaps = admin manual.  
- **Jun/2026:** Anti-duplicata tracking · custom data Saibai · novas contas cliente no tema.  
- **Jun/2026:** DESPACHO consolidado — checklist manual único por tela Admin.
