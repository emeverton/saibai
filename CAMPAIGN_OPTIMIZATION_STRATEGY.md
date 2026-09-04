# Empório Saibai — Estratégia de Otimização v1

**Atualizado:** 2026-06-25  
**Superseded by (estratégia completa H2):** [docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md](./docs/ESTRATEGIA-ABERTURA-ECOM-H2-2026.md)  
**KPI primário:** GA4 **`purchase`** (pós-go-live tracking)  
**KPI secundário:** `add_to_cart` · AOV · B2B WhatsApp leads  
**Veredito:** **PRECISA AUDITORIA**

> Nenhuma mutation neste documento. Execução via APPROVAL_REQUESTS.md.

---

## 1. Diagnóstico (jun/2026)

| Indicador | Valor | Leitura |
|-----------|------:|---------|
| Tema Shopify | v1.2.4 LIVE | Fundação e-com pronta |
| Tracking código | Deployado | Go-live manual pendente |
| Meta ACTIVE | 1 camp (WhatsApp leads) | **Não otimiza purchase** |
| Meta spend jun | R$ 160 | Baixo · legado V4 |
| Meta conv. plataforma | 2.977 | ❌ Infladas (messaging) |
| Google Ads | MCC pending | Sem auditoria |
| GA4 MCP | Sem acesso | propertyId desconhecido |
| Pagamentos | Manual pendente | **Bloqueia vendas reais** |

### O que os dados provam

1. **Negócio dual** — B2C e-commerce (alcachofras/conservas) + B2B restaurantes (WhatsApp).
2. **Mídia desalinhada** — Meta ativa otimiza grupo WhatsApp, não checkout Shopify.
3. **Infra pronta, operação não** — tema + tracking server existem; merchant precisa concluir checklist manual.
4. **Google inexplorado** — sem MCC link, zero visibilidade PMax/Search.
5. **Sazonalidade** — safra alcachofra = janela crítica para escalar D2C.

---

## 2. Modelo de negócio

| Track | Público | Jornada | KPI |
|-------|---------|---------|-----|
| **B2C D2C** | Consumidor, chef doméstico | Anúncio → loja → purchase | purchase · ROAS |
| **B2B** | Restaurantes, food service SP | Anúncio → WhatsApp/Contato | lead · conversa |
| **Comunidade** | Fãs safra | Grupo VIP WhatsApp | engajamento |

**Não** tratar como varejo local (Malhas) nem materiais construção (Bautech).  
**Não** misturar otimização purchase com messaging na mesma campanha.

---

## 3. Verba sugerida (pós-go-live)

| Canal | R$/dia | R$/mês | Funil | Pré-requisito |
|-------|-------:|-------:|-------|--------------|
| Meta Sales D2C | 40 | 1.200 | purchase | Tracking purchase ✅ |
| Meta Leads B2B | 20 | 600 | WhatsApp grupo | Manter ou pausar |
| Google PMax | 50 | 1.500 | purchase | MCC + feed |
| Google Search marca | 15 | 450 | purchase/brand | MCC linked |
| **Total** | **125** | **3.750** | — | — |

*Valores referência — ajustar com diretoria após 30 dias baseline GA4.*

---

## 4. Princípio estratégico

### Regra de ouro

**KPI e-commerce = GA4 `purchase`.** Não otimizar com conv. Meta messaging ou page view.

| Motor | Destino | Objetivo | KPI |
|-------|---------|----------|-----|
| Meta Sales | `emporiosaibai.com.br` | Purchase / Advantage+ | CPA ≤ R$ 80 · ROAS ≥ 3 |
| Meta Leads | Grupo WhatsApp | Leads B2B | CPL ≤ R$ 15 |
| Google PMax | Shopify feed | Purchase | CPA ≤ R$ 70 |
| Google Search | Marca + alcachofra | Purchase/brand | CPA ≤ R$ 50 |

### Tom e mensagem

- **Origem:** Piedade SP · Capital Nacional da Alcachofra · 50 anos tradição
- **Produto:** Fresca sazonal + conservas artesanais
- **CTAs B2C:** Comprar agora · Ver coleção · Pix/cartão
- **CTAs B2B:** Sou restaurante · Grupo VIP
- **Evitar:** urgência fake · stock falso · misturar hortaliças genéricas

---

## 5. Meta Ads — plano

### Fase 0 (agora) — estabilizar

| Item | Ação |
|------|------|
| LEADS-GRUPO-WHATS | Manter R$ 20/d se B2B prioritário · senão pausar |
| Conv. plataforma | Ignorar até Events Manager validado |
| Pixel | Confirmar `2017630342068049` + CAPI dedupe |

### Fase 1 (pós-tracking) — e-com

| Campanha | Tipo | Budget | Audiência |
|----------|------|-------:|-----------|
| `[SAIBAI][SALES][D2C][PURCHASE]` | Advantage+ Shopping | R$ 40/d | BR · interesse gastronomia |
| `[SAIBAI][RMKT][D2C][ATC]` | Remarketing | R$ 15/d | ATC 7d · visitantes 30d |

### Fase 2 — limpeza

- Arquivar 17+ campanhas Instagram boost 2025
- Padronizar nomenclatura `[SAIBAI][TIPO][FUNIL][OBJETIVO]`

---

## 6. Google Ads — plano (pós-MCC)

| Campanha | Tipo | Budget | Notas |
|----------|------|-------:|-------|
| `[SAIBAI][PMAX][D2C][BR]` | PMax | R$ 50/d | Feed Shopify · purchase import GA4 |
| `[SAIBAI][SEARCH][BRAND]` | Search | R$ 15/d | saibai, alcachofra saibai |
| `[SAIBAI][SEARCH][B2B][SP]` | Search | R$ 20/d | alcachofra restaurante SP |

**Conversões primárias:** import GA4 `purchase` only.

---

## 7. Shopify / CRO (tema)

| Área | Status | Próximo |
|------|--------|---------|
| Homepage dual B2C/B2B | ✅ | Fotos profissionais |
| PDP urgência estoque | ✅ | Validar SKUs safra |
| Checkout branding | ⚠️ manual | KV verde #76BD22 |
| Judge.me reviews | ⚠️ instalar | Substituir Loox |
| Klaviyo flows | ⚠️ instalar | Abandoned cart |
| Performance | ✅ Fase 2 | Desativar preloader/float |

---

## 8. Tracking — gate de escala

**Não escalar mídia paga até:**

- [ ] GA4_API_SECRET no Vercel
- [ ] Webhook purchase testado (Supabase + Events Manager)
- [ ] Canais Shopify conectados (1 GA4 + 1 Meta browser)
- [ ] Purchase sem duplicata checkout
- [ ] GA4 property acessível MCP Veltrus

---

## 9. Cronograma sugerido

| Semana | Foco |
|--------|------|
| S1 | Checklist manual P0 (pagamentos + tracking) |
| S2 | Baseline GA4 7 dias · conceder acesso MCP |
| S3 | Google MCC + primeira campanha PMax |
| S4 | Meta Sales D2C · pausar/ajustar WhatsApp leads |
| S8 | Review ROAS · Klaviyo · fotos catálogo |

---

## 10. Vereditos

| Área | Veredito |
|------|----------|
| Tema Shopify | **PASS** |
| Tracking código | **PASS** |
| Go-live operacional | **PRECISA HOTFIX** |
| Meta estrutura | **PRECISA AUDITORIA** |
| Google | **PENDING_PERMISSION** |
| GA4 | **PENDING_ACCESS** |
| Estratégia v1 | **PASS** |
