# Empório Saibai — Entrega Theme Consolidation · 22/07/2026

**Veredito:** **LIVE APROVADO** (sessão encerrada)  
**Loja:** https://emporiosaibai.com.br  
**Tema live:** `#186796147006` (`ella-saibai-homepage`)  
**Escopo:** consolidação CSS/JS Saibai + hotfixes header/hero mobile (sem gut Ella `base.css`)

---

## Texto para o cliente

Publicamos hoje uma limpeza grande do tema da loja (menos arquivos CSS carregando, site mais leve) e correções no celular:

1. **Header / menu** — barra opaca, logo centralizado, menu mobile sem travar nem “gaveta translúcida”.
2. **Home mobile** — foto do hero limpa; o menu “Safra 2026” fica **abaixo** da foto (não por cima).
3. **Categorias** — In Natura, Conservas, Flores e Chaveiro na home.
4. **Contato** — telefone **(15) 3010-1451** e CEP **18176-210**.

Pode testar no celular em https://emporiosaibai.com.br (hard refresh se parecer antigo).

---

## Scorecard consolidação

| Escopo | Antes | Depois |
|--------|--------|--------|
| Header CSS | 11 arquivos | **3** (`base` · `mega` · `util`) |
| Shell CSS | 6 arquivos | **2** (`core` · `cards`) + legacy condicional |
| Home CSS async | 9 arquivos | **2** (`prod-home` · `home-sections`) + hero sync |
| PLP pages | 3 | **1** (`pages-collection`) |
| PDP pages | 10 | **3** (`buybox` · `media` · `content`) |
| Inst pages | até 7 | **2** (`inst-core` · `inst-pages`) / PLP **1** (`inst-plp`) |
| Pages light | search+blog+list | **1** (`pages-light`) |
| Ella `component-card` / slider | em skip-base | **omitidos** (home/PLP/inst/search…) |
| Ella `base.css` | skip em vários templates | **mantido** em `/cart` + async na PDP (sem gut) |

Fragmentos antigos viraram stub `DEPRECATED` (CDN limpo quando ainda referenciados).

---

## Hotfixes desta sessão (após consolidação)

| Issue | Causa | Fix live |
|-------|--------|----------|
| Mega/header “translúcido” na PDP mobile | `--sh-bg` só no desktop (≥1025px); `#header-group` transparente | Tokens em todos viewports; header-group opaco `#F2F5EE`; mega bloqueado &lt;1025px |
| Logo desalinhado no mobile | `flex:1` no logo entre ícones desiguais | Logo `absolute` centro; slots menu/cart iguais |
| Menu Safra em cima da foto (home mobile) | Box `top:0` + scroll-dock JS sobre a mídia | Mobile: layout estático (foto → box abaixo); animação só desktop |

Arquivos-chave: `saibai-header-base.css`, `saibai-header-mega.css`, `saibai-header-util.css`, `saibai-header.js`, `saibai-hero.css`, `saibai-hero.js`.

---

## Smoke validado (live)

- Home: masters CSS (hero · prod-home · home-sections · header 3 · shell 2+legacy); sem Ella `base`/`component-card`
- Tabs produtos: 4 (In Natura · Conservas · Flores · Chaveiro)
- Drawer mobile: portaled → `body`, full viewport
- PLP conservas: `inst-plp` + `pages-collection`, hero estático
- Telefone footer: `(15) 3010-1451`

---

## Fora de escopo (próximo ciclo, se pedir)

1. Consolidar footer/consent (ainda fragmentados)
2. Gut seletivo Ella `base.css` (alto risco)
3. Coração P packshot (quando SKU/foto existirem)
4. Commit git local dos masters (working tree ainda tem stubs/WIP não commitados)

---

## Plataformas

| Canal | Link |
|-------|------|
| Loja | https://emporiosaibai.com.br |
| Theme editor | https://byinbz-0k.myshopify.com/admin/themes/186796147006/editor |
| Hub Notion | https://app.notion.com/p/38a968afab6681bb8a03e2d2e6848147 |
| Entrega consolidation | https://app.notion.com/p/3a5968afab668171b3c3e0cf7a70395c |
| Entrega UX manhã | https://app.notion.com/p/3a5968afab6681008685d344442c1c62 |
| Sync | `docs/SYNC-NOTION-SLACK-EKYTE-2026-07-22-THEME-CONSOLIDATION.md` |

---

## Veredito final

**LIVE APROVADO** · consolidação Saibai + hotfixes mobile encerrados neste ciclo.
