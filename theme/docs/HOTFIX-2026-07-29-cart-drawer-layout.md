# HOTFIX-2026-07-29 — Cart drawer layout (home/PLP sem base.css)

**Cliente:** Empório Saibai  
**Loja:** `emporiosaibai.com.br` · Tema live `#186796147006` (`ella-saibai-homepage`)  
**Escopo:** CSS · `assets/saibai-shell-core.css` apenas  
**Veredito código:** **PASS** · deploy live **LIVE APROVADO** (2026-07-29 · push `#186796147006`)

---

## Causa raiz

Após a consolidação 22/07, templates `index` / `collection` / `page` / `search` **pulam** Ella `base.css`.

O layout de `.quantity-selector` (flex + botões `position:absolute`) vivia **só** no `base.css`. Sem ele:

| Sintoma | Causa |
|---------|-------|
| Qty +/- empilhados + input solto | `quantity-selector-component` fica `display:inline` |
| "Tam / anh / o M" letra a letra | grid 6 colunas / media ~130px esmaga details (~85px) |
| X remover fora do lugar | área `remove` sem flex + qty quebrado |
| Function blocks ~95px | `.button` sem altura Ella |

## Fix

Em `saibai-shell-core.css` (master — sem arquivo novo):

1. Grid compacto do drawer: `5rem | minmax(0,1fr) | max-content`
2. Qty selector self-contained (flex + absolute ±) sem depender de `base.css`
3. Function blocks travados em 48px
4. Variant `nowrap` + details `min-width:0`

## Deploy

```bash
bash clients/saibai/ops/scripts/shopify-auth-full.sh

cd clients/saibai/theme
shopify theme push --store byinbz-0k.myshopify.com --theme 186796147006 --allow-live \
  --only assets/saibai-shell-core.css
```

**Requer:** reauth CLI + frase explícita **"PUBLICAR LIVE AGORA"**.

## QA

| # | Teste | Esperado |
|---|-------|----------|
| 1 | Home · abrir drawer com item | Título legível · "Tamanho M" numa linha |
| 2 | Qty − / input / + | Uma linha · ícones brancos no botão grafite |
| 3 | X remover | Ao lado do qty · 44px |
| 4 | Function blocks | Altura 48px |
| 5 | PLP conservas · drawer | Mesmo layout |
| 6 | PDP (tem base.css async) | Sem regressão qty |
| 7 | `/cart` | Sem regressão |

## Validação DOM (pré-push, CSS injetado)

```
qty.display = inline-flex · h=44 · buttons position=absolute
details.w ≈ 143 (antes 85)
variant = "Tamanho M"
function-block.h = 48 (antes 95)
```
