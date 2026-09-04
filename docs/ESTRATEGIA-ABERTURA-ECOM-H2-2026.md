# Empório Saibai — Estratégia de Abertura E-commerce · H2 2026

**Versão:** 2.0 · **Data:** 25/06/2026  
**Escopo:** Abertura de vendas online (Shopify D2C) + plano jul–dez/2026  
**Tipo:** Documento estratégico · **sem execução de mídia** (mutations via `APPROVAL_REQUESTS.md`)  
**Veredito:** **PODE SEGUIR** (estratégia) · operação **PRECISA HOTFIX** (pré-requisitos)

---

## Índice

1. [Tese e objetivo](#1-tese-e-objetivo)
2. [Diagnóstico consolidado](#2-diagnóstico-consolidado)
3. [Pré-requisitos — gate de abertura](#3-pré-requisitos--gate-de-abertura)
4. [Fase 0 — Abertura controlada (S1–S2 · jun/jul)](#4-fase-0--abertura-controlada)
5. [Fase 1 — Aquisição paga D2C (S3–S4 · jul/ago)](#5-fase-1--aquisição-paga-d2c)
6. [Fase 2 — Escala conservas + retenção (set–out)](#6-fase-2--escala-conservas--retenção)
7. [Fase 3 — Natal + B2B fechamento (nov–dez)](#7-fase-3--natal--b2b-fechamento)
8. [Dual track B2C × B2B](#8-dual-track-b2c--b2b)
9. [Catálogo e mensagem por temporada](#9-catálogo-e-mensagem-por-temporada)
10. [CRO, CRM e operação loja](#10-cro-crm-e-operação-loja)
11. [Medição e Growth Pack](#11-medição-e-growth-pack)
12. [Orçamento H2 2026](#12-orçamento-h2-2026)
13. [Riscos e mitigações](#13-riscos-e-mitigações)
14. [Cronograma semanal (jun–dez)](#14-cronograma-semanal)
15. [Vereditos e referências](#15-vereditos-e-referências)

---

## 1. Tese e objetivo

### Tese

A Saibai tem **infraestrutura e-com pronta** (tema v1.2.4, tracking server-side em código, catálogo Shopify), mas **opera como negócio B2B de WhatsApp** na mídia. Abrir vendas online não é “ligar anúncio” — é **fechar o ciclo pagamento → purchase rastreado → mídia otimizada por receita**.

### Objetivo H2 2026

| Horizonte | Meta |
|-----------|------|
| **Jul/26** | Primeiras vendas D2C rastreadas (PIX/cartão live + purchase GA4) |
| **Ago–Set/26** | Baseline ROAS · CPA purchase · 30+ pedidos/mês |
| **Out–Dez/26** | Conservas + kits natal · **ROAS ≥ 3** em mídia D2C · B2B paralelo |

### KPI único de sucesso e-com

**GA4 `purchase`** (receita + volume). Secundários: `add_to_cart`, AOV, taxa checkout, `whatsapp_click` (B2B).

**Nunca** otimizar por conv. plataforma Meta (97k YTD = messaging).

---

## 2. Diagnóstico consolidado

### O que está pronto

| Área | Status | Evidência |
|------|--------|-----------|
| Loja Shopify | ✅ LIVE | `emporiosaibai.com.br` · tema `#186124239166` |
| KV + LGPD + consent | ✅ | Banner Saibai · Consent Mode v2 |
| Tracking server | ✅ código | Vercel + CAPI Meta + Supabase |
| Catálogo | ✅ | Conservas · desidratados · safra `in-natura-1` |
| Frete grátis | ✅ | R$ 280+ |
| Cupom entrada | ✅ | `5%NOVOCLIENTE` |
| Pixel Meta | ✅ firing | last fired 24/06 |

### O que bloqueia vendas hoje

| Bloqueio | Impacto | Responsável |
|----------|---------|-------------|
| Pagamentos Shopify (PIX/cartão) | **Zero checkout pago** | Merchant |
| GA4 API Secret + webhook app | Purchase server incompleto | Merchant + Veltrus |
| Canais Google/Meta + pixel checkout | Browser/checkout gap | Merchant |
| Google MCC pending | Zero Google Ads | Merchant |
| GA4 fora MCP Veltrus | Sem baseline ROAS | Merchant |
| Hotfix cart drawer (CSS) | UX carrinho | Veltrus (auth Shopify) |

### Mídia atual (Meta MCP · jan–25/jun/26)

| Métrica | Valor | Leitura |
|---------|------:|---------|
| Spend YTD | R$ 2.322 | 83% legado V4 |
| Campanha ACTIVE | LEADS-GRUPO-WHATS R$ 20/d | B2B · não e-com |
| CTR jun | 4,3% | B2B eficiente |
| Conv. plataforma YTD | 97.374 | ❌ irrelevante para ROAS |

**Conclusão:** mídia B2B **não precisa pausar** na abertura — precisa **conviver** com track D2C separado, com budget e KPI distintos.

---

## 3. Pré-requisitos — gate de abertura

**Nenhuma campanha Sales D2C antes deste gate.**

### Gate A — Loja pode cobrar (merchant)

| # | Item | Referência |
|---|------|------------|
| A1 | Shopify Payments BR verificado | CHECKLIST §1.2 |
| A2 | PIX + cartão + Shop Pay ativos | CHECKLIST §1.2 |
| A3 | Modo teste OFF | CHECKLIST §1.2 |
| A4 | Estoque safra/conservas conferido | Operação Saibai |

### Gate B — Purchase rastreado (Veltrus + merchant)

| # | Item | Referência |
|---|------|------------|
| B1 | GA4 API Secret → Vercel | GO-LIVE-RUNBOOK A2 |
| B2 | App Saibai Tracking reinstalado | GO-LIVE-RUNBOOK B1 |
| B3 | Canais Shopify Google + Meta | GO-LIVE-RUNBOOK B4 |
| B4 | Pixel Customer Events checkout | GO-LIVE-RUNBOOK A3 |
| B5 | Pedido teste → purchase GA4 + Meta CAPI | GO-LIVE-RUNBOOK C |
| B6 | Acesso GA4 property Veltrus | CLIENT_CONTEXT |

### Gate C — UX mínima (Veltrus)

| # | Item |
|---|------|
| C1 | Deploy hotfix cart drawer (4 CSS) |
| C2 | Smoke test mobile 375px |
| C3 | Checkout branding KV (#76BD22) |

**Veredito gate:** quando A + B + C = **PASS** → autorizar Fase 1 mídia D2C.

---

## 4. Fase 0 — Abertura controlada

**Período:** S1–S2 (final jun / início jul 2026)  
**Investimento mídia D2C:** **R$ 0** (orgânico + CRM only)  
**Investimento B2B:** manter R$ 20/d LEADS-GRUPO-WHATS (decisão diretoria)

### Ações operacionais

| Área | Ação | Dono |
|------|------|------|
| Go-live | Concluir gates A + B + C | Merchant + Veltrus |
| Orgânico | Stories safra + link bio loja | Saibai |
| E-mail | Instalar Klaviyo · fluxo boas-vindas + popup cupom | Veltrus + merchant |
| Reviews | Instalar Judge.me · migrar de Loox | Merchant |
| SEO | TinySEO embeds ON | Merchant |
| Pedido real | 3–5 pedidos reais (equipe + clientes fiéis) | Saibai |

### Metas Fase 0

| KPI | Meta |
|-----|------|
| Pedidos pagos rastreados | ≥ 5 |
| Purchase GA4 sem duplicata | 100% match pedido Shopify |
| Taxa erro checkout | 0 bloqueios pagamento |
| AOV inicial | Medir (sem target) |

### Comunicação

- **Não** anunciar “grande lançamento” antes do gate B.
- Comunicar soft launch para base WhatsApp/Instagram existente.
- CTA: “Compre online” → coleção conservas (estoque estável pós-safra).

---

## 5. Fase 1 — Aquisição paga D2C

**Período:** S3–S4 (jul–ago 2026)  
**Pré-requisito:** Gate A+B+C **PASS** + 7 dias purchase GA4 estável

### Orçamento Fase 1 (ramp)

| Canal | R$/dia | R$/mês | Objetivo |
|-------|-------:|-------:|----------|
| Meta `[SAIBAI][SALES][D2C][PURCHASE]` | 25 → 40 | 750 → 1.200 | Advantage+ · catálogo Shopify |
| Meta `[SAIBAI][RMKT][D2C][ATC]` | 10 → 15 | 300 → 450 | ATC 7d · visitantes 14d |
| Google `[SAIBAI][PMAX][D2C][BR]` | 30 → 50 | 900 → 1.500 | Feed Shopify · purchase GA4 |
| Google `[SAIBAI][SEARCH][BRAND]` | 10 → 15 | 300 → 450 | Marca + alcachofra saibai |
| B2B LEADS-GRUPO-WHATS | 20 | 600 | Manter separado |
| **Total mídia** | **95 → 140** | **~2.850 → 4.200** | Ramp 4 semanas |

*Semana 1 Fase 1: metade dos budgets · dobrar se CPA purchase ≤ R$ 100 e ROAS ≥ 2.*

### Estrutura de campanhas Meta D2C

| Campanha | Tipo | Audiência | Criativo |
|----------|------|-----------|----------|
| SALES D2C | Advantage+ Shopping | BR · 28–55 · interesse gastronomia/gourmet | Pack conservas · origem Piedade |
| RMKT D2C | Conversões purchase | ATC + view content 14d | Urgência estoque real · frete grátis R$280 |

**UTM padrão:** `utm_source=meta&utm_medium=paid&utm_campaign={{campaign.name}}`

### Estrutura Google (pós-MCC)

| Campanha | Foco | Conversão |
|----------|------|-----------|
| PMax D2C | Catálogo completo Shopify | GA4 purchase |
| Search Brand | saibai · alcachofra saibai · emporio saibai | purchase + brand |

### Metas Fase 1 (30 dias após ligar mídia)

| KPI | Target conservador | Target stretch |
|-----|-------------------:|---------------:|
| Pedidos/mês | 20 | 40 |
| AOV | R$ 180 | R$ 220 |
| CPA purchase (mídia D2C) | ≤ R$ 100 | ≤ R$ 80 |
| ROAS blended D2C | ≥ 2,0 | ≥ 3,0 |
| Taxa add_to_cart → purchase | ≥ 2% | ≥ 4% |

### Kill rules (pausar se)

- CPA purchase > R$ 150 por 7 dias consecutivos **e** ROAS < 1,5
- Zero purchase GA4 com spend > R$ 500 → auditar tracking antes de escalar
- Feed PMax com > 30% produtos reprovados

---

## 6. Fase 2 — Escala conservas + retenção

**Período:** set–out 2026  
**Contexto sazonal:** pós-safra fresca · **hero = conservas + desidratados** (shelf-stable · margem · frete)

### Produto foco

| Linha | Papel | Mensagem |
|-------|-------|----------|
| Conservas coração/pedaço | Hero D2C | “Alcachofra o ano todo” |
| Flores/frutas desidratadas | Cross-sell | Presente · gastronomia |
| Fresca in natura | Limitado | Só se estoque + logística OK |
| Kits degustação | Novo SKU sugerido | 3 conservas · entry AOV |

### Mídia Fase 2 (steady state)

| Canal | R$/dia | Notas |
|-------|-------:|-------|
| Meta Sales D2C | 45 | Escalar top criativos Fase 1 |
| Meta RMKT | 15 | Carrinho abandonado sync Klaviyo |
| Google PMax | 55 | Priorizar conservas no feed |
| Google Search | 15 | + termos “conserva alcachofra” |
| B2B WhatsApp | 20 | `[SAIBAI][LEADS][B2B][SP]` separado |
| **Total** | **~150/d** | **~R$ 4.500/mês** |

### Retenção (sem mídia)

| Fluxo Klaviyo | Trigger | Objetivo |
|---------------|---------|----------|
| Abandoned cart | ATC 1h / 24h | Recuperar 8–12% carrinhos |
| Post-purchase | purchase +3d | Receita + review Judge.me |
| Win-back | 60d sem compra | Conservas promo |

### Metas Fase 2

| KPI | Target |
|-----|-------:|
| Pedidos/mês | 50 |
| Repeat rate 60d | ≥ 15% |
| ROAS D2C | ≥ 3,0 |
| % receita conservas | ≥ 70% |

---

## 7. Fase 3 — Natal + B2B fechamento

**Período:** nov–dez 2026

### Oportunidade

Conservas artesanais + origem Piedade = **presente premium** (Natal · corporate gifting B2B).

### Produto

| SKU / ação | Detalhe |
|------------|---------|
| Kit Natal Saibai | 2–3 conservas + embalagem gift |
| Corporate B2B | Caixas 6+ un · WhatsApp + landing B2B |
| Frete grátis | Reforçar R$ 280 · considerar promo Natal R$ 250 |

### Mídia nov–dez

| Canal | R$/dia | Pico |
|-------|-------:|------|
| Meta Sales (gift angle) | 50–60 | Black Friday · Dez |
| Meta RMKT | 20 | Compradores 90d |
| Google PMax | 60 | Gift keywords |
| Google Search | 20 | “presente gourmet” · “cesto natal” |
| B2B Search SP | 25 | Restaurantes · ceia corporate |
| **Total pico** | **~175/d** | **~R$ 5.250/mês (dez)** |

### Metas Fase 3

| KPI | Target |
|-----|-------:|
| Receita e-com nov+dez | R$ 40–60k (stretch) |
| Pedidos dez | 80+ |
| AOV dez (kits) | R$ 250+ |

---

## 8. Dual track B2C × B2B

### Regra de ouro

**Campanhas, budgets e KPIs separados.** Nunca Advantage+ purchase com destino WhatsApp grupo.

| Track | Budget ref. | KPI | Destino |
|-------|------------:|-----|---------|
| **B2C D2C** | 70% mídia H2 | purchase · ROAS | `emporiosaibai.com.br` |
| **B2B** | 20% mídia H2 | CPL WhatsApp · pedidos B2B | Grupo VIP · contato |
| **Comunidade** | 10% orgânico | engajamento | Instagram · safra |

### Decisão LEADS-GRUPO-WHATS

| Opção | Quando | Ação |
|-------|--------|------|
| **Manter R$ 20/d** | B2B prioritário · safra comunidade | Manter · renomear `[SAIBAI][LEADS][B2B][WHATS]` |
| **Reduzir R$ 10/d** | D2C precisa caixa | Cortar 50% B2B |
| **Pausar** | ROAS D2C < 2 com budget apertado | Realocar para RMKT D2C |

**Recomendação Veltrus:** manter R$ 20/d B2B em jul–ago · revisar set se ROAS D2C ≥ 3.

---

## 9. Catálogo e mensagem por temporada

| Mês | Hero produto | Ângulo criativo | Evitar |
|-----|--------------|-----------------|--------|
| **Jul** | Conservas coração | Abertura loja · 50 anos Piedade | Fresca esgotada sem estoque |
| **Ago** | Conservas + desidratados | Receitas · chef em casa | Urgência falsa |
| **Set** | Kits degustação | “Leve Saibai para sua mesa” | Boost Instagram legado |
| **Out** | Conservas premium | Origem · tradição | Hortaliças genéricas |
| **Nov** | Kit presente | Black Friday real (estoque) | Desconto > 15% sem margem |
| **Dez** | Cestas Natal | Presente corporativo | Misturar B2B msg em ad D2C |

### Tom KV

- Verde `#76BD22` · grafite `#2A3A1A` · origem Piedade
- **CTA D2C:** Comprar agora · Frete grátis acima de R$280 · Pix e cartão
- **CTA B2B:** Sou restaurante · Fale no WhatsApp

---

## 10. CRO, CRM e operação loja

### Prioridade CRO (ordem)

| # | Item | Impacto | Fase |
|---|------|---------|------|
| 1 | Pagamentos live | Crítico | 0 |
| 2 | Cart drawer UX (hotfix) | Alto | 0 |
| 3 | Judge.me reviews | Médio | 0–1 |
| 4 | Klaviyo abandoned cart | Alto | 1 |
| 5 | Checkout branding KV | Médio | 0 |
| 6 | Fotos profissionais PDP | Alto | 1–2 |
| 7 | Sticky ATC mobile | Médio | ✅ tema |
| 8 | Desativar preloader | Performance | 2 |

### Operação pós-pedido

| Item | Ação |
|------|------|
| E-mails transacionais | Branding `#76BD22` · templates `ops/scripts/output/notifications/` |
| SLA envio | Comunicar prazo real PDP + e-mail |
| WhatsApp pós-venda | Opcional B2C · obrigatório B2B |

### Apps (ordem instalação)

Clarity OFF → TinySEO → Judge.me → Klaviyo (ref. CHECKLIST §2.3)

---

## 11. Medição e Growth Pack

### Framework KPI

```
Investimento (Meta + Google)
        ↓
Sessões / view_item (GA4)
        ↓
add_to_cart
        ↓
begin_checkout
        ↓
purchase ← KPI primário
        ↓
ROAS = receita purchase / spend D2C
```

### Growth Pack H2

| Milestone | Quando | Entrega |
|-----------|--------|---------|
| Criar planilha `[GROWTHPACK] 2026 SAIBAI` | Jul S1 | Sheet ID |
| Backfill Meta jan–jun | Jul S1 | ImportaçãoMeta |
| Sync automático VPS | Após gate B | `sync-saibai-growth-sheet.mjs` |
| Reportei projeto | Ago | Integrações Meta + GA4 |
| CAC-LTV-ROAS | Out+ | Após 60d purchase |

Ref: `docs/ANALISE-GROWTH-PACK-2026-06-25.md` · `docs/GROWTH-SHEET-AUTOMATION.md`

### Revisões cadência

| Ritual | Frequência | Participantes |
|--------|------------|---------------|
| Check ROAS/CPA | Semanal | Veltrus |
| Growth Pack review | Quinzenal | Veltrus + account |
| Steering diretoria | Mensal | Saibai + V4 |

---

## 12. Orçamento H2 2026

### Resumo por fase

| Fase | Período | Mídia/mês (ref.) | Foco |
|------|---------|----------------:|------|
| 0 Abertura | jun–jul S1–2 | R$ 600 (só B2B) | Gate + orgânico |
| 1 Ramp D2C | jul–ago | R$ 2.850 → 4.200 | Primeiras campanhas purchase |
| 2 Steady | set–out | R$ 4.500 | Conservas + retenção |
| 3 Pico Natal | nov–dez | R$ 5.000–5.250 | Kits + B2B corporate |

### Total investimento mídia H2 (jul–dez)

| Cenário | Total 6 meses |
|---------|--------------:|
| Conservador | R$ 24.000 |
| Base (recomendado) | R$ 27.000 |
| Agressivo (ROAS ≥ 3 em out) | R$ 30.000 |

*Fee V4/agência fora do escopo · não inclui produção criativa.*

### Metas receita e-com H2 (stretch)

| Mês | Pedidos | Receita ref. | ROAS alvo |
|-----|--------:|-------------:|----------:|
| Jul | 10 | R$ 2k | — (baseline) |
| Ago | 25 | R$ 5k | 2,0 |
| Set | 40 | R$ 8k | 2,5 |
| Out | 50 | R$ 10k | 3,0 |
| Nov | 65 | R$ 14k | 3,0 |
| Dez | 80 | R$ 18k | 3,0 |
| **H2 total** | **~270** | **~R$ 57k** | **≥ 2,5 blended** |

*Receita = referência estratégica · validar com margem e capacidade operacional Saibai.*

---

## 13. Riscos e mitigações

| Risco | Prob. | Impacto | Mitigação |
|-------|:-----:|:-------:|-----------|
| Pagamentos não ativados | Alta | Crítico | Gate A bloqueante |
| Purchase duplicado | Média | Alto | Anti-duplicata TRACKING_AUDIT |
| Fresca sem logística | Média | Médio | Hero conservas H2 |
| MCC Google atrasado | Alta | Médio | Meta-only Fase 1 · Google S4 |
| ROAS baixo inicial | Alta | Médio | Ramp budget · RMKT · Klaviyo |
| Capacidade envio | Média | Alto | Limitar SKUs promovidos |
| Abril-repeat (engajamento waste) | Baixa | Alto | Proibir campanhas ENGAGEMENT puro |

---

## 14. Cronograma semanal

| Semana | Calendário | Foco principal |
|--------|------------|----------------|
| S1 | 23–29 jun | Gate A+B · deploy cart drawer · soft launch orgânico |
| S2 | 30 jun–6 jul | 5+ pedidos teste · Klaviyo + Judge.me · gate C PASS |
| S3 | 7–13 jul | Meta Sales D2C R$ 25/d · MCC Google push |
| S4 | 14–20 jul | Google PMax R$ 30/d · baseline 7d |
| S5–8 | ago | Ramp budgets · criativos conservas |
| S9–12 | set | Steady R$ 4.5k/m · kits degustação |
| S13–16 | out | ROAS review · repeat rate |
| S17–20 | nov | BF · kits presente |
| S21–26 | dez | Pico Natal · B2B corporate · retrospectiva |

---

## 15. Vereditos e referências

### Vereditos

| Área | Veredito |
|------|----------|
| Estratégia abertura e-com H2 | **PASS** |
| Prontidão operacional hoje | **PRECISA HOTFIX** |
| Mídia D2C imediata | **BLOQUEADO** (gate A+B) |
| Dual track B2C/B2B | **PASS** |
| Orçamento H2 | **PASS** (referência) |

### Documentos relacionados

| Doc | Uso |
|-----|-----|
| `GO-LIVE-RUNBOOK-P0.md` | Execução gate A+B |
| `CHECKLIST_MANUAL_SAIBAI.md` | Checklist merchant |
| `TRACKING_AUDIT.md` | Anti-duplicata |
| `CAMPAIGN_OPTIMIZATION_STRATEGY.md` | v1 tática Meta/Google |
| `ANALISE-GROWTH-PACK-2026-06-25.md` | Baseline mídia YTD |
| `APPROVAL_REQUESTS.md` | Fila mutations |
| `docs/agents/scripts/saibai-growth-plan.mjs` | Orçamento mensal código |

### Fila aprovações (pós-gate)

| ID | Ação | Quando |
|----|------|--------|
| SB-M-001 | Criar SALES D2C purchase | Gate B PASS |
| SB-M-002 | Decidir LEADS-GRUPO-WHATS | Jul S2 |
| SB-G-002 | PMax feed Shopify | MCC linked |
| SB-T-001 | GA4 API Secret | Gate B |

---

**Próximo passo merchant:** concluir Gate A (pagamentos) + Gate B (tracking) — ver `GO-LIVE-RUNBOOK-P0.md`.  
**Próximo passo Veltrus:** documentação ✅ · aguardar gate para mutations.

---

## Publicação (25/06)

| Plataforma | Link |
|------------|------|
| Notion | [05 — Estratégia H2](https://app.notion.com/p/38a968afab6681018105fb8c483b7bef) |
| Slack | [#ops-clientes](https://veltrus.slack.com/archives/C0BA1AA7D7U/p1782387029778069) |
| eKyte | **#9713234** · Ativa · prazo 31/12/2026 · **não finalizada** |

Ref: `docs/SYNC-NOTION-SLACK-EKYTE-2026-06-25.md`
