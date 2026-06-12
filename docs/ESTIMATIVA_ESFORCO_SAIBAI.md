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

*Veltrus Growth & Technology — Shopify Partner ID 4969609*
