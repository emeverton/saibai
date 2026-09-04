# Empório Saibai — ChatGPT AUDIT validado · 28/06/2026

**Veredito ChatGPT:** **BLOQUEADO** escala D2C · **PODE MANTER** B2B WhatsApp R$20/d  
**Mutations:** **ZERO**

---

## Alinhamento Cursor ↔ ChatGPT

| Item | Status |
|------|--------|
| Veredito BLOQUEADO D2C | ✅ |
| B2B WhatsApp manter orçamento | ✅ |
| Meta MCP oficial OK | ✅ |
| GA4 fora OAuth | ✅ SB-AI-INFRA-001 |
| Google gateway 500 | ✅ SB-AI-INFRA-002 |
| KPI purchase GA4 (≠ conv platform) | ✅ |
| Sales D2C pausadas — não ativar | ✅ SB-M-002 |
| Go-live P0 antes de Sales | ✅ SB-AI-P0-001 |

---

## Refinamento ChatGPT (KPI B2B correto)

| Métrica | Cursor (raw) | ChatGPT (canônico) |
|---------|--------------|-------------------|
| Conv. platform | 2.040 ❌ infladas | **ignorar** |
| lead_grupo_whats | — | **46** |
| CPL B2B | — | **R$ 3,55** |
| Decisão | MANTER watch | **MANTER · sem escala agressiva** |

---

## PLANO APROVADO

| ID | Ação |
|----|------|
| **SB-AI-INFRA-001** | GA4 OAuth + purchase/begin_checkout/add_to_cart/view_item/revenue |
| **SB-AI-INFRA-002** | Google gateway 500 · customerId `9513237350` |
| **SB-AI-P0-001** | Go-live Shopify P0 (#9712969) |
| **SB-M-001** | HOLD escala B2B · manter R$20/d |
| **SB-M-002** | NO Sales D2C · 3 campanhas pausadas hold |

### Sales D2C — NÃO ATIVAR

- `120237873462540155` [F][SALES] Venda Direta 05-10-25  
- `120237596031000155` [F][SALES] Venda Direta Brasil 30-09-25  
- `120237169476030155` [F][SALES] Venda Direta 23-09-25  

---

## Dual Track H2

| Track | Alvo | Status |
|-------|------|--------|
| D2C purchase | 70% mídia | **HOLD** |
| B2B WhatsApp | 20% mídia | **ACTIVE** |
| Escala geral | — | **BLOQUEADA** |

---

## Próximo passo

1. **Paralelo infra:** SB-AI-INFRA-001 GA4 + SB-AI-P0-001 merchant (#9712969)  
2. **Cursor EXECUTE:** **nenhuma mutation** até go-live P0 + purchase GA4  
3. Re-audit quando GA4 + Google OK

Export: [exports/ads-audit-2026-06-28.json](../exports/ads-audit-2026-06-28.json)
