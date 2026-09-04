# HOTFIX-2026-06-25 — Cart drawer · ícones invisíveis (hover-only)

**Cliente:** Empório Saibai  
**Loja:** `emporiosaibai.com.br` · Tema `#186124239166` v1.2.4  
**Escopo:** CSS tema Shopify · cart drawer + página cart  
**Veredito código:** **PASS** · deploy live **LIVE APROVADO** (2026-07-16)  
**Encerramento Veltrus:** 2026-06-25 (repo + doc) · **push live 2026-07-16** (tema `#186124239166`)

---

## Resumo

Ícones do mini-cart (cupom/nota/frete, +/- quantidade, remover item) apareciam **só no hover** ou como **bloco verde vazio**, porque:

1. `saibai-shell-cta.css` aplicava fundo grafite `#2A3A1A` em `.function-block.button`
2. Ícones herdavam `#2A3A1A` via `saibai-shell-kv.css` → **mesma cor do fundo**
3. Regra de ícone branco no qty só cobria `quantity-input` (PDP), **não** `quantity-selector-component` (drawer)

---

## Sintomas reportados

| Elemento | Comportamento |
|----------|---------------|
| Bloco verde abaixo do item | Function block (cupom/nota) com fundo CTA e ícone invisível |
| Botões +/- | Ícones só visíveis no hover |
| X remover | Contraste ruim em alguns estados |
| Preço | Duplicado (detalhes + coluna totals) |

---

## Arquivos alterados

| Arquivo | Mudança |
|---------|---------|
| `assets/saibai-shell-cta.css` | Exclui `.function-block` e `.button-close-circle` do CTA grafite; inclui `quantity-selector-component` |
| `assets/saibai-shell-kv.css` | Ícones +/- brancos sempre (`quantity-selector-component` + `.quantity-selector`) |
| `assets/saibai-shell-layout.css` | Function blocks fundo claro + ícones visíveis; remove/edit sempre visíveis; preço duplicado oculto no drawer |
| `assets/saibai-pages-cart.css` | Mesmas regras na página `/cart` |

---

## Deploy

**Status 25/06:** tentativas automáticas falharam — **sem stored auth** para `byinbz-0k` nesta máquina.

```
No stored app authentication found for byinbz-0k.myshopify.com
```

Reauth **obrigatório no terminal interativo** (OAuth abre browser):

```bash
# 1) Reauth (terminal local)
bash clients/saibai/ops/scripts/shopify-auth-full.sh

# 2) Push parcial (4 CSS)
cd clients/saibai/theme
shopify theme push --store byinbz-0k.myshopify.com --theme 186124239166 --allow-live \
  --only assets/saibai-shell-cta.css assets/saibai-shell-kv.css assets/saibai-shell-layout.css assets/saibai-pages-cart.css
```

---

## QA pós-deploy

| # | Teste | Esperado |
|---|-------|----------|
| 1 | Abrir drawer · aba anônima | Ícones cupom/nota/frete visíveis (fundo claro) |
| 2 | Hover function block | Fundo verde Saibai + ícone branco |
| 3 | Qty +/- | Ícones brancos sempre no botão grafite |
| 4 | X remover | Visível sem hover |
| 5 | Preço | Uma vez só (coluna direita) |
| 6 | `/cart` página | Mesmo comportamento qty/remove |
| 7 | Mobile 375px | Touch targets 44px OK |

---

## Double-check — outros pontos auditados

| Área | Status |
|------|--------|
| PDP qty (`quantity-input`) | Já OK antes |
| Sticky ATC | Já OK |
| Header icons | OK (seletores próprios) |
| Cards quick-add | OK |

---

## eKyte

- **Workspace:** Saibai (`123736`)
- **Task hotfix:** **#9712906** ✅ concluída 25/06 (repo + doc · deploy live → P0 A1)
- **Task P0:** **#9712969** — `[Saibai] Go-live P0 — tracking, pagamentos, canais + pixel checkout`
- **Runbook:** `clients/saibai/docs/GO-LIVE-RUNBOOK-P0.md`

---

## Referências

- Dossiê: `clients/saibai/CLIENT_CONTEXT.md`
- Smoke test: `theme/docs/SMOKE_TEST_v1.2.4.md`
- Skill: `.cursor/skills/saibai-company-expert/SKILL.md`
