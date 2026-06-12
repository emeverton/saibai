# Estimativa de Esforço — Projeto Empório Saibai

**Elaborado por:** Veltrus Growth & Technology  
**Uso:** orçamento, proposta comercial, registro interno de task  
**Atualizado:** junho 2026

---

## Contexto

Estimativa baseada no escopo entregue no repositório:

- Tema Shopify Ella 7.2.0 + camada Saibai (`saibai-*`)
- ~197 arquivos custom · ~13.700 linhas CSS/JS Saibai
- Sprints 0–9 + closeout (LGPD, tracking, performance, QA, documentação)
- Theme Check 0 offenses · loja pronta para venda

**Não há timesheet real no Git** — os valores abaixo são ordem de grandeza para planejamento.

---

## Tabela 1 — Estimativa por fase (horas)

| Fase | Entrega | Sem ferramentas | Com parceiro Shopify + automação* | Redução |
|------|---------|----------------:|----------------------------------:|--------:|
| 0 | Setup Ella + repo | 12–20 h | 4–8 h | ~60% |
| 1 | KV / tokens / shell CSS | 20–32 h | 6–12 h | ~65% |
| 2 | Header + mega menu | 32–48 h | 10–18 h | ~65% |
| 3 | Home (todos os módulos) | 48–72 h | 14–28 h | ~65% |
| 4 | PLP / cards / coleção | 24–40 h | 8–14 h | ~65% |
| 5 | PDP completa | 32–48 h | 10–18 h | ~65% |
| 6 | Cart / drawer | 16–24 h | 5–10 h | ~60% |
| 7 | Footer | 16–24 h | 5–10 h | ~60% |
| 8 | Páginas institucionais | 32–48 h | 10–16 h | ~65% |
| 9 | Mobile QA | 24–40 h | 8–14 h | ~65% |
| 10 | Performance | 24–40 h | 8–14 h | ~65% |
| 11 | SEO / Schema | 12–20 h | 4–8 h | ~60% |
| 12 | LGPD / consentimento | 24–36 h | 8–14 h | ~65% |
| 13 | Tracking / proxy / CAPI | 20–32 h | 8–12 h | ~60% |
| 14 | Locale PT-BR | 20–32 h | 6–12 h | ~65% |
| 15 | Theme Check + auditoria | 20–32 h | 6–10 h | ~70% |
| 16 | Admin / go-live | 20–32 h | 8–12 h | ~60% |
| 17 | QA final + documentação | 24–40 h | 8–14 h | ~65% |
| 18 | Retrabalho CSS / cascata | 32–56 h | 10–18 h | ~70% |
| | **TOTAL** | **380–500 h** | **~125–242 h** | **~65–75%** |

\* Shopify Partner + ferramentas internas de produtividade (geração de código, auditoria, documentação e QA acelerados).

---

## Tabela 2 — Cenários consolidados

| Cenário | Sem ferramentas | Com parceiro + automação | Redução | Prazo (40 h/sem) | Prazo com automação |
|---------|----------------:|-------------------------:|--------:|-----------------:|--------------------:|
| Otimista | 280–350 h | 80–110 h | ~68–72% | 7–9 semanas | 2–3 semanas |
| **Realista** | **380–500 h** | **120–180 h** | **~65–70%** | **10–13 semanas** | **3–5 semanas** |
| Pessimista | 550–750 h | 180–250 h | ~65–67% | 14–19 semanas | 5–7 semanas |

---

## Tabela 3 — Referência rápida (uso comercial)

| Métrica | Valor |
|---------|------:|
| Esforço tradicional (1 dev solo) | **~400 h** |
| Esforço com stack Veltrus | **~120–150 h** |
| **Horas economizadas** | **~250–280 h** |
| **Redução percentual** | **~65–70%** |
| Equivalente em dias úteis (8 h) | ~31–38 dias → **~15–19 dias** |

---

## Tabela 4 — Comparativo de prazo

| Dedicação | Sem ferramentas | Com parceiro + automação |
|-----------|----------------:|-------------------------:|
| Full-time (40 h/sem) | 2,5–4 meses | **3–5 semanas** |
| Meio período (20 h/sem) | 4,5–7 meses | **6–9 semanas** |
| Intensivo (projeto sprint) | 6–8 semanas | **2–3 semanas** |

---

## Fora do escopo desta estimativa

- Fotografia e produção de catálogo
- Configuração financeira (gateways, CNPJ, conta bancária)
- Campanhas de mídia paga
- Scripts operacionais externos (`ops/`)
- Backlog fase 3 (refactor profundo, SEO expandido)

---

## Texto para task (copiar e colar)

> **Estimativa Saibai:** escopo completo manual ≈ **380–500 h** (~400 h referência). Como **Shopify Partner** com **ferramentas internas de automação**, esforço equivalente ≈ **120–180 h** (**~65–70% de redução**, ~**250–280 h economizadas**). Prazo: de **2,5–4 meses** para **3–5 semanas** em dedicação integral.

---

## Valor estimado de mercado (Brasil · 2026)

Referências de mercado para escopo equivalente (tema premium refatorado + performance + LGPD + tracking + QA + documentação):

| Fonte / perfil | Faixa típica | Observação |
|----------------|-------------|------------|
| Freelancer pleno (BR) | R$ 80–160/h | Projetos fechados costumam descontar escopo [4] |
| Agência Shopify entrada | R$ 9.000–25.000 | Tema custom + integrações BR básicas [3] |
| PME média (implementação) | R$ 18.000–45.000 | Tema + tracking + SEO + LGPD [1] |
| PME consolidada / premium | R$ 35.000–80.000 | Tracking server-side + QA + evolução [1] |
| Projeto robusto custom | 8–12 semanas | Tema fortemente personalizado + migração [2] |

**Escopo Saibai entregue** situa-se entre **agência premium** e **PME consolidada** — acima de “só trocar logo no tema”, abaixo de headless/Hydrogen.

---

## Tabela 5 — Valor por hora × esforço (custo de mercado)

| Perfil | R$/hora | × 400 h (manual) | × 150 h (stack Veltrus)* |
|--------|--------:|-----------------:|-------------------------:|
| Freelancer pleno | 80–120 | R$ 32.000–48.000 | R$ 12.000–18.000 |
| Agência pleno/sênior | 150–200 | R$ 60.000–80.000 | R$ 22.500–30.000 |
| **Agência premium Shopify** | **180–250** | **R$ 72.000–100.000** | **R$ 27.000–37.500** |
| Especialista sênior / consultoria | 220–280 | R$ 88.000–112.000 | R$ 33.000–42.000 |

\* Horas internas com automação — **não** significa que o valor comercial ao cliente deva cair na mesma proporção; o mercado precifica **resultado e escopo**, não só horas da agência.

---

## Tabela 6 — Valor de projeto fechado (recomendado para proposta)

| Cenário | O que o mercado cobraria | Valor estimado |
|---------|--------------------------|---------------:|
| **Básico** | Tema premium adaptado, sem LGPD/tracking profundo | R$ 15.000–28.000 |
| **Intermediário** | Tema custom + mobile + SEO + páginas institucionais | R$ 28.000–45.000 |
| **Saibai (entregue)** | Camada custom completa + LGPD + tracking + performance + QA + docs + go-live | **R$ 55.000–85.000** |
| **Premium+** | Acima + e-mail transacional + campanhas + fotografia + ERP | R$ 85.000–120.000+ |

### Referência única (uso comercial Veltrus)

| Métrica | Valor |
|---------|------:|
| **Valor de mercado justo (projeto fechado)** | **R$ 68.000–82.000** |
| Faixa conservadora | R$ 55.000–68.000 |
| Faixa agressiva (posicionamento premium) | R$ 82.000–95.000 |
| Equivalente USD (câmbio ~R$ 5,50) | **US$ 12.000–15.000** |

---

## Tabela 7 — O que compõe o valor (vs tema “barato”)

| Item entregue | Valor de mercado isolado* |
|---------------|-------------------------:|
| Tema premium Ella + licença base | R$ 2.000–4.000 |
| Camada visual Saibai (~197 arquivos custom) | R$ 25.000–40.000 |
| Home + PDP + cart + footer premium | R$ 12.000–18.000 |
| LGPD / Consent Mode v2 | R$ 4.000–8.000 |
| Arquitetura tracking (anti-dup + proxy + CAPI ready) | R$ 6.000–12.000 |
| Performance (CSS modular, LCP, Theme Check 0) | R$ 5.000–10.000 |
| Institucionais + legal/footer | R$ 4.000–8.000 |
| QA mobile + smoke test + auditoria | R$ 4.000–8.000 |
| Pacote documentação (guias + relatórios) | R$ 3.000–6.000 |
| **Soma referência** | **R$ 65.000–114.000** |

\* Soma não é preço final — itens se sobrepõem; serve para justificar **R$ 68k–82k** como faixa coerente.

---

## Tabela 8 — Valor percebido vs custo interno (parceiro + automação)

| Métrica | Manual | Com stack Veltrus |
|---------|-------:|------------------:|
| Horas equivalentes | ~400 h | ~120–150 h |
| Custo interno (R$ 150/h ref.) | R$ 60.000 | R$ 18.000–22.500 |
| **Valor de venda mercado** | **R$ 68.000–82.000** | **R$ 68.000–82.000** |
| Margem bruta estimada | Baixa (~15–35%) | **Alta (~65–75%)** |

O diferencial comercial: **mesmo valor ao cliente**, com **menor custo interno** via Partner + automação — sem precificar como “tema barato”.

---

## Texto para task — valor (copiar e colar)

> **Valor de mercado Saibai (escopo entregue):** **R$ 68.000–82.000** (projeto fechado · agência premium Shopify BR · 2026). Referência hora: ~400 h × R$ 180–200/h. Com stack Veltrus (Partner + automação), custo interno cai ~65–70%, mas **valor comercial se mantém** pelo escopo (LGPD, tracking, performance, QA, docs). Equivalente internacional: ~**US$ 12k–15k**.

---

## Aviso

Valores são **estimativas de mercado** para planejamento comercial — não constituem proposta vinculante. Orçamento final depende de contrato, escopo adicional, suporte pós-go-live e condições de pagamento.

---

*Veltrus Growth & Technology — Shopify Partner ID 4969609*
