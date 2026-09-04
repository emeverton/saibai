# Empório Saibai — Campaign Optimizer AUDIT · 28/06/2026

**Veredito:** **BLOQUEADO** · EXECUTE **HOLD**  
**Período:** 2026-06-14 → 2026-06-28  
**Export:** [ads-audit-2026-06-28.json](../exports/ads-audit-2026-06-28.json)

> **Dual track:** B2C purchase GA4 (70% mídia H2) + B2B WhatsApp grupo (20%).  
> Campanha ACTIVE hoje = **LEADS-GRUPO-WHATS** — **≠ purchase e-com**.

---

## Status MCP (Cursor preflight 28/06)

| Canal | ID | Status |
|-------|-----|--------|
| Meta Veltrus | `act_1199864388174624` | ✅ LIVE |
| Google | `9513237350` | ❌ gateway **500** |
| GA4 | `G-VWX77SGD1W` | ❌ fora OAuth (27 props listadas) |
| Reportei | — | ❌ projeto não criado |

---

## Meta 14d

| Métrica | Valor |
|---------|------:|
| Spend | R$ 163,20 |
| Cliques | 330 |
| CTR | 4,25% |
| CPC | R$ 0,49 |
| Conv. plataforma | **2.040** ❌ infladas |
| Campanhas ACTIVE | **1** (WhatsApp grupo R$20/d) |

---

## Bloqueios P0 (antes de EXECUTE)

1. **GA4** — conceder acesso Veltrus + `GA4_API_SECRET` Vercel  
2. **Google MCC** — aceitar convite `9513237350`  
3. **Go-live merchant** — pagamentos · app tracking · canais Sales  
4. **Reportei** — criar projeto Saibai  

Runbook: [GO-LIVE-RUNBOOK-P0.md](./GO-LIVE-RUNBOOK-P0.md) · eKyte **#9712969**

---

## ## PLANO APROVADO (infra + hold)

| ID | Ação |
|----|------|
| **SB-AI-INFRA-001** | GA4 property Saibai no OAuth Veltrus |
| **SB-AI-INFRA-002** | Google MCC link + re-audit gateway |
| **SB-AI-P0-001** | Gates merchant GO-LIVE-RUNBOOK-P0 |
| **SB-M-001** | HOLD escala WhatsApp · manter R$20/d watch |
| **SB-M-002** | **NÃO** ligar Sales D2C até purchase GA4 validado |

---

## Próximo (fluxo ChatGPT)

1. ChatGPT msg 1+2 → validar AUDIT  
2. Merchant + Everton: P0 infra  
3. Cursor EXECUTE **somente** waste/hold · **zero** budget up até purchase GA4
