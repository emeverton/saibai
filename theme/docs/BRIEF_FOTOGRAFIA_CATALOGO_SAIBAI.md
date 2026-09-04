# Brief de Fotografia — Catálogo Empório Saibai

**Versão:** 1.1 · Junho 2026  
**Para:** Equipe Saibai / fotógrafo / estúdio  
**Objetivo:** Padronizar imagens de produto para PLP, home e PDP no padrão editorial (referência: carrossel `saibai-prod` + Loro Piana)

---

## Por que isso importa

Hoje o site mistura **fotos lifestyle** (caixa, mesa, fundo desfocado) com **packshots** (fundo branco, ângulos diferentes). O tema já trata as imagens com `cover`, fundo cream e tom unificado — mas **fotos consistentes na origem** são o que elevam a percepção de marca premium.

**Meta:** visitante vê o grid e pensa “catálogo de produtor artesanal”, não “marketplace genérico”.

---

## Especificações técnicas (obrigatórias)

| Item | Especificação |
|------|----------------|
| **Proporção** | **4:5 vertical** (ex.: 1600 × 2000 px) — mesma lógica do tile `558×780` da home |
| **Fundo** | Cream Saibai **`#F2F5EE`** (pintura, papel ou LED panel calibrado — evitar branco puro `#FFFFFF`) |
| **Produto** | Centralizado, ocupa **~70–80%** da altura do frame |
| **Ângulo** | Frontal ou 3/4 leve; **mesmo ângulo** para toda a linha |
| **Sombra** | Suave, difusa, abaixo do produto (sem sombra dura de estúdio varejo) |
| **Luz** | Natural difusa; temperatura neutra-levemente quente |
| **Formato entrega** | JPG alta (qualidade 90+) ou PNG; Veltrus converte para WebP no tema |
| **Resolução mínima** | 1600 px no lado maior |
| **Nome do arquivo** | `saibai-[categoria]-[produto-handle].jpg` (ex.: `saibai-conserva-coracao.jpg`) |

### Segunda imagem (hover — opcional mas recomendado)

| Item | Especificação |
|------|----------------|
| **Uso** | Aparece no hover do card na PLP e home |
| **Conteúdo** | Detalhe (textura, corte, rótulo, prato servido) ou lifestyle **no mesmo fundo cream** |
| **Proporção** | Idêntica à imagem principal (4:5) |

---

## O que fotografar — checklist por linha

| Linha | Produtos prioritários | Sugestão de enquadramento |
|-------|----------------------|---------------------------|
| **Conservas** | Coração, Fundo Pedaço, Fundo Inteiro | Pote + rótulo legível; tampa visível em 1 foto, aberto em hover |
| **Frutas desidratadas** | Doce Pomar, Pomar de Verão, abacaxi, maçã, manga | Embalagem fechada (hero) + mix de frutas (hover) |
| **Flores desidratadas** | Kit flores | Caixa ou sachê centralizado; detalhe de pétalas no hover |
| **Frescas / in natura** | Caixas P e Mini | Caixa Saibai fechada; alcachofras visíveis por vão |
| **Chaveiro** | Chaveiro alcachofra | Objeto isolado, macro limpo |
| **Congelados** | Quando ativos | Embalagem + indício de produto (sem gelo exagerado) |

**Prioridade 1 (impacto imediato na PLP):** conservas + frutas + flores — são os itens com maior contraste visual hoje.

---

## O que NÃO fazer

- Fundo branco puro ou cinza de e-commerce genérico  
- Misturar lifestyle com fundo de cozinha/mesa **na mesma grade** sem padrão  
- Recortes diferentes (um produto zoom, outro longe)  
- Texto promocional, preço ou logo Photoshop na imagem  
- Marca d’água, borda, colagem de vários produtos no mesmo frame  
- Filtros saturados ou HDR forte  

---

## Referência visual no site (já aprovada)

Use como **north star** (não precisa copiar cenário, só o **nível de limpeza**):

- Home → carrossel de produtos (`saibai-prod`)  
- Home → blocos editoriais (`saibai-ed`) — conservas, flores, frutas, fresca  
- PLP coleção → [Conservas](https://emporiosaibai.com.br/collections/em-conserva) (hero + grid)

**Cores de apoio no set:** grafite `#2A3A1A` (props discretos), marrom `#8B5E4A` (opcional em lifestyle controlado).

---

## Entrega e publicação no Shopify

1. Enviar pasta organizada por coleção (`/conservas`, `/frutas`, etc.).  
2. **Imagem 1** = foto principal do produto no admin Shopify.  
3. **Imagem 2** = segunda foto (hover) na mesma ficha do produto.  
4. Texto alternativo (alt): `[Nome do produto] — Empório Saibai` (sem “promoção”, “oferta”).  
5. Avisar Veltrus após upload → validamos PLP, home e PDP em preview.

---

## Critério de aceite (checklist Veltrus)

- [ ] Mesmo fundo cream em todos os SKUs da mesma coleção  
- [ ] Mesma proporção 4:5 em todo o catálogo  
- [ ] Produto centralizado; nenhuma imagem “flutuando” com letterbox excessivo  
- [ ] Hover (img 2) presente nos 10+ SKUs principais  
- [ ] Rótulo legível nas conservas (nome Saibai visível)  
- [ ] Grid `/collections/todos` visualmente uniforme em desktop e mobile
- [ ] Links internos e menus apontam para `/collections/todos` (não `/collections/all`)  

---

**Contato técnico:** Veltrus · tema Saibai by Veltrus (#186124239166) · emporiosaibai.com.br  
**Dúvidas sobre proporção ou crop:** enviar 2 amostras antes do shoot completo.
