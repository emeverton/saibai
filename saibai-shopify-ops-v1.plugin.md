# Plugin — Empório Saibai Shopify, Tracking & Ads Ops v1.0

Atualizado em: 2026-06-25  
Cliente: Empório Saibai (Saibai Saladas)  
Projeto: Shopify theme + tracking Veltrus server-side + Meta/Google Ads  
Status: Tema PASS · Tracking código PASS · Go-live manual PRECISA HOTFIX · Meta MCP LIVE · Google PENDING_PERMISSION.

---

## 1. Regra-mãe operacional

Este plugin deve ser usado para iniciar novos chats sobre **Empório Saibai** quando o objetivo for:

- consultar contexto consolidado do projeto;
- trabalhar no tema Shopify Saibai (Liquid/CSS/JS);
- auditar tracking Veltrus (Vercel + CAPI + Shopify channels);
- analisar campanhas Meta Ads e Google Ads;
- planejar transição WhatsApp leads → e-commerce purchase;
- criar approval requests;
- preparar relatório executivo.

Modo padrão:

```txt
Somente leitura inicialmente.
Não executar mutations em mídia sem aprovação explícita.
Não criar campanha ativa automaticamente.
Não fazer shopify theme push --allow-live sem autorização.
Não duplicar GA4/Meta (canais vs theme settings vs server).
KPI e-commerce: GA4 purchase.
Não confiar CPA/ROAS Meta plataforma (conv. messaging infladas).
```

---

## 2. Diferença vs outros clientes Veltrus

| Aspecto | Bautech (Tray) | Empório Saibai |
|---|---|---|
| Plataforma | Tray Commerce | **Shopify** |
| Tracking | GTM Web + sGTM | **Veltrus Vercel + CAPI** + canais Shopify |
| Produto | Materiais construção | **Alcachofras frescas + conservas** |
| Dual track | WhatsApp vendas secundário | **B2C purchase + B2B WhatsApp** |
| Meta atual | E-com purchase | **WhatsApp grupo leads** (legado) |
| GTM | Central | **Opcional** (Stape) — não obrigatório |

**Regra crítica Saibai:** nunca duplicar purchase (canal checkout + pixel custom + server webhook).

---

## 3. Identificadores

| Campo | Valor | Status |
|---|---|---|
| clientKey | `saibai` | OK |
| GA4 | `G-VWX77SGD1W` | PENDING_ACCESS MCP |
| Meta ad account | `act_1199864388174624` | OK |
| Meta pixel | `2017630342068049` | OK |
| Google customer | `9513237350` | MCC pending |
| Shopify store | `byinbz-0k.myshopify.com` | OK |
| Tema live | `186124239166` | v1.2.4 |
| Tracking API | `tracking-eta-eight.vercel.app` | OK |
| KPI GA4 | `purchase` | Pós-go-live |

---

## 4. KV Design (hardcode — não CSS variables Shopify)

| Token | Hex | Uso |
|-------|-----|-----|
| Primary | `#8ABE0A` | Tokens tema (CTA secundário) |
| Checkout CTA | `#76BD22` | Checkout branding manual |
| Dark / CTA | `#2A3A1A` | Texto, botões cards |
| Secondary | `#4E7E8A` | Acentos |
| WhatsApp | `#25D366` | Float button |
| Font | **Jost** | Body + heading |
| Background | `#F2F5EE` | Shell |

---

## 5. Docs canônicos

| Doc | Uso |
|-----|-----|
| `CLIENT_CONTEXT.md` | IDs + snapshot |
| `CHECKLIST_MANUAL_SAIBAI.md` | Ações manuais merchant |
| `TRACKING_AUDIT.md` | Stack + anti-duplicata |
| `CAMPAIGN_OPTIMIZATION_STRATEGY.md` | Estratégia v1 |
| `theme/docs/DESPACHO_SAIBAI.md` | Checklist operacional tema |
| `theme/docs/RELATORIO_EXECUTIVO_SAIBAI.md` | Entrega diretoria |
| `APPROVAL_REQUESTS.md` | Mutations |

---

## 6. Prompt de abertura sugerido

```txt
Modo: Empório Saibai Ops v1 — Veltrus.

Cliente: Empório Saibai (saibai)
Negócio: alcachofras D2C Shopify + B2B restaurantes WhatsApp
Plataforma: Shopify · tema v1.2.4 · tracking Veltrus server-side
Dossiê: clients/saibai/
Skill: saibai-company-expert

IDs:
- GA4: G-VWX77SGD1W (property MCP pending)
- Meta: act_1199864388174624 · pixel 2017630342068049
- Google: 9513237350 (MCC pending)
- Shopify: byinbz-0k · tema 186124239166

Estado jun/2026:
- Tema: LIVE PASS
- Tracking código: PASS · go-live manual PRECISA HOTFIX
- Meta: R$158 spend · 1 camp ACTIVE (WhatsApp leads) · conv. infladas
- Google: gateway 500 PENDING_PERMISSION

Regras:
- Somente leitura até aprovação
- Mutations: APPROVAL_REQUESTS.md
- KPI e-com: GA4 purchase
- Theme Settings tracking IDs = VAZIOS

Próximo P0: CHECKLIST_MANUAL_SAIBAI.md seção 1
```

---

## 7. Validação MCP inicial

1. `meta_ads_build_client_report` adAccountId=act_1199864388174624
2. `google_ads_build_client_report` customerId=9513237350 (após MCC)
3. `ga4_build_client_report` clientKey=saibai (após property access)

## Vereditos esperados

| Área | Veredito |
|------|----------|
| Tema | PASS |
| Tracking go-live | PRECISA HOTFIX |
| Meta MCP | PASS |
| Google | PENDING_PERMISSION |
| GA4 | PENDING_ACCESS |
| Dossiê | PASS |
