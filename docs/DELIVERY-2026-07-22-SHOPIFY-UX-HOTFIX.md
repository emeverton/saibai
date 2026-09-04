# Empório Saibai — Entrega Shopify UX · 22/07/2026

**Veredito:** **LIVE APROVADO**  
**Loja:** https://emporiosaibai.com.br  
**Tema live:** `#186796147006` (`ella-saibai-homepage`)  
**Origem:** últimos ajustes solicitados pelo cliente (menu mobile · fotos conservas · chaveiro · telefone/CEP)

---

## Texto para o cliente

Olá! Publicamos hoje na loja os ajustes pedidos:

1. **Menu no celular** — corrigimos o travamento ao abrir o menu (agora abre e fecha normalmente).
2. **Fotos das conservas por tamanho** — cada pote (M e G) tem a foto correta do Drive; ao trocar o tamanho na página do produto, a imagem muda.
3. **Chaveiro na página inicial** — aparece no hero, na aba de produtos e no bloco de coleções.
4. **Telefone e CEP** — fixo **(15) 3010-1451** e CEP **18176-210** no rodapé e na página de contato.

Pode testar no celular em https://emporiosaibai.com.br (se algo parecer antigo, atualize a página / limpe o cache).

Obs.: tamanho **P** do Coração fica de fora por enquanto (não tem na loja ainda). Quando tiver foto/SKU, a gente inclui.

---

## Checklist técnico

| # | Solicitação | Status |
|---|-------------|--------|
| 1 | Menu mobile travando | ✅ Live — freeze por `pointer-events:none` no header |
| 2 | Fotos tamanhos conservas (Drive) | ✅ Live — M/G vinculados às variantes |
| 3 | Categoria Chaveiro na home | ✅ Live — hero · tab · editorial |
| 4 | Fixo (15) 3010-1451 + CEP 18176-210 | ✅ Live — footer · contato · schema |

---

## Detalhe técnico

### Menu mobile
- Causa: `#header-group.is-scroll-hidden` com `pointer-events: none` engolia o drawer
- Fix: `assets/saibai-header.js` + override em `saibai-header-util-rwd.css`

### Fotos conservas
- 6 packshots Drive → Coração M/G · Fundo Inteiro M/G · Fundo Pedaço M/G
- Script: `ops/scripts/saibai-upload-drive-size-packshots.py`

### Chaveiro home
- `templates/index.json` + tabs products + editorial 4 cards
- Asset: `assets/saibai-ed-chaveiro.webp`

### Contato
- Telefone/CEP em footer, contato, sobre, schema Organization, privacidade

---

## Plataformas

| Canal | Link |
|-------|------|
| Notion | https://app.notion.com/p/3a5968afab6681008685d344442c1c62 |
| Slack `#cliente-saibai` | https://veltrus.slack.com/archives/C0BD28VMD4N/p1784749102008469 |
| eKyte **#9975680** (ABERTA) | https://app.ekyte.com/#/tasks/9975680 |
| Sync | `docs/SYNC-NOTION-SLACK-EKYTE-2026-07-22-SHOPIFY-UX.md` |

---

## Aberto / próximo

1. ~~Smoke cliente no celular~~ → seguido por consolidação tema (ver `DELIVERY-2026-07-22-THEME-CONSOLIDATION.md`)
2. Quando houver Coração P (SKU + foto) → incluir packshot na variante
3. Gates tracking P0 (#9712969) seguem em paralelo
