# Guia do Tema Empório Saibai — Para quem não programa

**Versão:** 1.2.4 · Junho 2026  
**Desenvolvido por:** Veltrus Growth & Technology  
**Loja:** [emporiosaibai.com.br](https://emporiosaibai.com.br)

---

## O que é este documento?

Este guia explica, em linguagem simples, **o que foi feito na loja online da Saibai** e **como cada parte funciona**. Você não precisa saber programar para entender a estrutura e saber onde pedir alterações.

---

## 1. Visão geral — Como a loja está organizada

Imagine a loja como um **prédio com andares**:

| Andar | Nome técnico | O que o visitante vê |
|-------|--------------|----------------------|
| Fundação | `layout/theme.liquid` | Estrutura de todas as páginas (cabeçalho, rodapé, conteúdo) |
| Paredes e cores | `saibai-tokens.css` + `snippets/saibai-shell-css.liquid` | Cores oficiais, botões, cards de produto |
| Cômodos | `sections/saibai-*.liquid` | Cada bloco da home e páginas institucionais |
| Móveis | `snippets/saibai-*.liquid` | Peças reutilizáveis (menu, hero, popups) |
| Decoração | `assets/saibai-*.css` e `.js` | Visual e interatividade de cada módulo |

**Regra de ouro:** cada módulo Saibai tem seu próprio arquivo de estilo e, quando necessário, seu próprio JavaScript. Isso evita que uma alteração na barra fixa quebre o vídeo do hero, por exemplo.

---

## 2. Cores oficiais (identidade visual)

| Cor | Código | Uso |
|-----|--------|-----|
| Fundo cream (LP) | `#F2F5EE` | Fundo do site, seções, rodapé claro |
| Fundo topo (barra) | `#FAFBF7` | Barra fixa de anúncios |
| Grafite (texto/CTA) | `#2A3A1A` | Títulos, botões primários, badges |
| Grafite hover | `#384E28` | Hover de botões CTA |
| Verde destaque | `#8ABE0A` | Links no hover, bullets, detalhes |
| Verde hover | `#7AAA08` | Hover de links e ícones |
| Texto secundário | `#4E6040` | Parágrafos e legendas |
| Marrom premium | `#8B5E4A` | Destaques editoriais (estilo Loro Piana) |
| WhatsApp | `#25D366` | Botão flutuante de contato |

Essas cores estão centralizadas no arquivo `assets/saibai-tokens.css`. Se um dia mudar a paleta, **só esse arquivo precisa ser atualizado** (mais o shell global).

---

## 3. Passo a passo — O que acontece quando alguém abre a loja

### Passo 1 — O navegador carrega a base
1. O Shopify entrega `layout/theme.liquid`.
2. O corpo da página recebe a classe `saibai-theme` — isso ativa todas as regras visuais Saibai.
3. Carregam os arquivos globais: tokens, shell, páginas internas.

### Passo 2 — Aparece a barra fixa (announcement bar)
- **Arquivo visual:** `assets/saibai-announcement-bar.css`
- **Arquivo de comportamento:** `assets/saibai-announcement-bar.js`
- **Conteúdo dos textos:** `snippets/saibai-announcement-bar-slides.liquid`

**O que foi feito:**
- Fundo alinhado ao KV (`#FAFBF7` na barra, `#F2F5EE` no header), sem “faixa” estranha entre barra e menu.
- Botões **anterior**, **pausar/reproduzir** e **próximo** visíveis no carrossel de anúncios.
- Faixa decorativa dupla **só no topo** (estilo premium).
- Textos mais escuros para melhor leitura.
- Transição suave com o menu — sem linha dupla na junção.

**Para alterar mensagens da barra:** edite o arquivo de slides (não precisa mexer em CSS).

### Passo 3 — O menu principal (header)
- **Section:** `sections/saibai-header.liquid`
- **HTML:** `snippets/saibai-header.liquid`
- **Mega menu:** `snippets/saibai-header-mega-panel.liquid`
- **Menu mobile (gaveta):** `snippets/saibai-header-drawer.liquid`
- **Estilo:** `snippets/saibai-header-css.liquid` (módulos `saibai-header-*.css`, ≤300 lin cada)
- **Comportamento:** `assets/saibai-header.js`

**O que foi feito:**
- Layout inspirado em marcas de luxo (Loro Piana): logo central, navegação fina, mega menu em gaveta que desce de cima.
- Ícones de busca, conta e sacola alinhados e proporcionais.
- No celular: menu lateral (drawer) em vez do mega menu.
- Logo oficial: `assets/saibai-logo-header.png`.

**Para alterar itens do menu:** Shopify Admin → Navegação → menu principal.

### Passo 4 — O vídeo hero (primeira impressão da home)
- **Section:** `sections/saibai-home-hero.liquid`
- **HTML:** `snippets/saibai-home-hero.liquid`
- **Estilo:** `assets/saibai-hero.css`
- **Vídeo:** `assets/saibai-hero.mp4` (otimizado: 1440×688, ~7 MB)
- **Comportamento:** `assets/saibai-hero.js` (play/pause, parallax leve no scroll)

**O que foi feito:**
- Vídeo alinhado com a mesma largura do header (máx. 1320px nas laterais).
- Sem espaço vazio entre menu e vídeo.
- Card de texto premium no canto inferior esquerdo (título + links).
- Controles discretos no estilo LP (botões 24×24px, fundo `#F7F5F1`).
- Card acompanha levemente o scroll (efeito parallax).

### Passo 5 — Demais blocos da home (em ordem)
| Ordem | Bloco | CSS | Função |
|-------|-------|-----|--------|
| 2 | Editorial | `saibai-editorial.css` | Grade de coleções/categorias |
| 3 | Marquee | `saibai-marquee.css` | Faixa de texto em movimento |
| 4 | Serviços | `saibai-services.css` | Ícones de benefícios |
| 5 | História da fazenda | `saibai-split.css` | Texto + imagem lado a lado |
| 6 | Destaque produto | `saibai-feature-layout.css` + `saibai-feature-product.css` | Banner de produto em destaque |
| 7 | Produtos | `saibai-prod-home-*.css` + `saibai-products.js` | Carrossel de produtos |
| 8 | Conservas | usa `saibai-split.css` | Segundo bloco split |
| 9 | Newsletter | `saibai-newsletter.css` + `.js` | Captura de e-mail |

**Otimização feita na auditoria:** o CSS `saibai-split.css` agora carrega **uma única vez** na home (antes carregava duas vezes). O JavaScript da newsletter carrega **só na home**, não em todas as páginas.

### Passo 6 — Popups e extras
| Popup | Quando aparece | Arquivos |
|-------|----------------|----------|
| Consentimento LGPD | Primeira visita | `saibai-consent-popup.*` |
| Cupom de desconto | Regra de exibição configurada | `saibai-coupon-popup.*` |
| WhatsApp flutuante | Sempre (canto inferior direito) | `snippets/saibai-whatsapp-float.liquid` |

### Passo 7 — Páginas institucionais
Páginas: História, Sobre, Fazenda, Conquistas.

- **CSS único:** `snippets/saibai-inst-css.liquid` — carrega **uma vez** por página (módulos `saibai-inst-*.css`).
- **Sections:** `saibai-inst-hero`, `saibai-inst-nav`, `saibai-inst-timeline`, etc.

---

## 4. Glossário rápido

| Termo | Significado simples |
|-------|---------------------|
| **Section** | Bloco que você arrasta no editor Shopify |
| **Snippet** | Pedaço de HTML reutilizável (como um componente) |
| **Asset** | Arquivo CSS, JS ou imagem na pasta `assets/` |
| **Liquid** | Linguagem de template do Shopify (mistura HTML com dados da loja) |
| **Modular** | Cada parte tem seu arquivo — mudança isolada, sem efeito dominó |
| **Cascata** | Quando duas regras CSS brigam e uma sobrescreve a outra sem querer |
| **KV** | Kit Visual — cores, fontes e estilo da marca |

---

## 5. O que NÃO mexer sem ajuda técnica

1. `layout/theme.liquid` — estrutura global e ordem de carregamento.
2. `snippets/global-css.liquid` e `global-script.liquid` — arquivos carregados em todas as páginas.
3. `snippets/saibai-shell-css.liquid` (módulos `saibai-shell-*.css`) — regras globais de botões, cards e grids.
4. Pasta `../client-assets/Saibai/` (fora do repo tema) — materiais do cliente (fotos, vídeos), **não faz parte do tema Shopify**.

---

## 6. Como pedir uma alteração (checklist)

1. **Diga qual bloco** — ex.: “barra fixa”, “vídeo hero”, “mega menu Produtos”.
2. **Diga o que quer** — ex.: “trocar texto”, “mudar cor do botão”, “nova imagem”.
3. **Informe desktop ou celular** — muitas regras são diferentes por tamanho de tela.
4. **Não peça para editar `base.css` ou `vendor.css`** — são do CSS legado Veltrus base (base.css / vendor.css); customizações vão em arquivos `saibai-*`.

---

## 7. Mapa de arquivos por necessidade

| Quero alterar… | Arquivo principal |
|----------------|-------------------|
| Mensagens da barra superior | `snippets/saibai-announcement-bar-slides.liquid` |
| Itens do menu | Shopify Admin → Navegação |
| Vídeo da home | `assets/saibai-hero.mp4` + section hero |
| Textos do card sobre o vídeo | `snippets/saibai-home-hero.liquid` |
| Produtos em destaque na home | `sections/saibai-home-products.liquid` |
| Popup de cookies | `sections/saibai-consent-popup.liquid` |
| Popup de cupom | `sections/saibai-coupon-popup.liquid` |
| Página História / Sobre | templates `page.historia.json`, etc. |
| Cores globais | `assets/saibai-tokens.css` |

---

## 8. Resumo do que a auditoria corrigiu

| Problema | Solução |
|----------|---------|
| CSS institucional baixado 5–9 vezes na mesma página | Carregamento único via `snippets/saibai-conditional-assets.liquid` |
| CSS split baixado 2 vezes na home | Mesmo snippet — 1 link só |
| Newsletter JS em todas as páginas | Movido para `sections/saibai-home-newsletter.liquid` |
| Regras de botão/card duplicadas em tokens e shell | Tokens ficou só com variáveis + utilitários únicos |
| Arquivo órfão `saibai-header-cta.liquid` | Removido (não era usado) |

---

## 9. Próximos passos sugeridos (opcional)

- Conectar tracking GA4/Meta nos snippets `tracking-*.liquid` (já existem, aguardam ativação no layout).
- ~~Dividir header CSS~~ — concluído (loaders `saibai-header-css.liquid`, módulos ≤300 lin).
- ~~Templates demo~~ — removidos na auditoria Fase 3 (33 JSON landing/lookbook).

---

## 10. Sprint 8 — O que mudou (auditoria premium)

### Passo 1 — Comparação com referência de luxo
A Veltrus comparou a loja ao vivo com [Loro Piana Interactive](https://ii.loropiana.com/en/) e referências como LG.com. O padrão “quiet luxury” usa fundo cream, tipografia fina (peso 400), cards verticais alongados e hovers discretos. A Saibai mantém **suas cores oficiais** (verde `#8ABE0A`, grafite `#2A3A1A`, fundo `#F2F5EE`) dentro desse padrão.

### Passo 2 — Cards de produto na home
- **Antes:** proporção padrão (mais quadrada).
- **Agora:** proporção oficial `--saibai-tile-aspect: 558 / 780` (token em `saibai-tokens.css`).
- **No celular:** você vê 1 produto inteiro + metade do próximo (convida a deslizar).

### Passo 3 — Páginas de coleção (ex.: Conservas)
- Removida a barra lateral “Categorias” duplicada do tema demo.
- Grid centralizado, igual à home — sem botões estranhos (2, 3, 4 colunas).

### Passo 4 — Rodapé
- Links de Política de Entrega/Troca/Privacidade **não aparecem mais duas vezes**.
- Texto discreto: **“Desenvolvido por Veltrus · Shopify Partner”** (sem logo grande).

### Passo 5 — Proteção do tema
- Arquivo `saibai-license.js` impede uso do visual em outros domínios.
- Aviso no console do navegador identifica a Veltrus como desenvolvedora.

### Passo 6 — Fotos de produto
- Imagens preenchem o card inteiro, sem faixa cinza ao redor.

---

## 11. Como publicar as mudanças

Peça à Veltrus ou ao responsável técnico:

```bash
shopify theme push --theme 186124239166
```

Depois, abra a loja em modo anônimo e confira home + uma coleção + um produto no celular.

---

**Dúvidas?** Entre em contato com a Veltrus informando a seção desejada e este guia como referência.
