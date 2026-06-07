# Guia do Leigo — Loja Empório Saibai

**Para quem administra a loja sem conhecimento técnico**  
**Loja:** [emporiosaibai.myshopify.com](https://emporiosaibai.myshopify.com)  
**Versão do tema:** Saibai 1.0.0 (base Ella 7.2.0)  
**Desenvolvido por:** Veltrus Growth & Technology

---

## O que é o tema da loja?

Pense no **tema** como a “casa” da sua loja na internet. Ele define:

- Como as páginas aparecem (cores, fontes, botões)
- Onde ficam menu, logo, carrinho e rodapé
- Como os produtos são exibidos no celular e no computador

A Saibai usa a plataforma **Shopify** (sistema de e-commerce) com um tema personalizado chamado **Saibai**, construído sobre o tema profissional **Ella**. Tudo que o cliente vê ao entrar no site — home, produtos, carrinho, checkout — passa por esse tema.

Você **não precisa programar** para o dia a dia. A maior parte das alterações é feita pelo painel da Shopify: **Produtos**, **Páginas**, **Temas → Personalizar**.

---

## O que mudou na aparência (antes × depois)

| Antes (tema demo Ella) | Depois (tema Saibai) |
|------------------------|----------------------|
| Cores genéricas do template | Verde Saibai (#76BD22), azul-petróleo (#4E7E8A), textos em tom grafite |
| Textos em inglês (“Shop Now”, endereço em San Francisco) | Textos em português, endereço Piedade/SP, e-mail contato@saibai.com.br |
| Logo e identidade de outra marca | Logo oficial Empório Saibai (PNG do arquivo da loja) |
| WhatsApp com número placeholder | **Grupo VIP** no rodapé e botão flutuante verde |
| Layout genérico de moda | Home com história da fazenda, alcachofra, conservas e produtos em destaque |
| Rodapé com crédito de outro desenvolvedor | Crédito **Veltrus** + selos Pix, Visa, Mastercard, Amex, Elo, Boleto |
| Site pouco adaptado ao celular | Menu, cards e botões otimizados para mobile (toque fácil, carrossel de produtos) |

Em resumo: a loja **parece Saibai**, fala **português** e está **pronta para vender** alcachofras e produtos derivados.

---

## Como as cores foram definidas

As cores principais da marca foram fixadas no arquivo de design do tema (`saibai-tokens.css`). Você não precisa editar esse arquivo no dia a dia.

| Nome | Cor | Uso na loja |
|------|-----|-------------|
| Verde Saibai | `#76BD22` | Botões principais, hover de links, badges de desconto |
| Verde escuro (hover) | `#5A9018` | Quando o mouse passa sobre botões verdes |
| Azul-petróleo | `#4E7E8A` | Faixas, detalhes, textos de urgência |
| Grafite | `#2A3A1A` | Títulos e textos escuros |
| Creme claro | `#F4F9F0` | Fundos suaves de seções |
| WhatsApp | `#25D366` | Botão flutuante do Grupo VIP |

No admin Shopify, em **Temas → Personalizar → Configurações do tema → Cores**, você também pode ajustar esquemas de cor (scheme-1, scheme-2, etc.) sem mexer em código.

---

## O que é o Grupo VIP e como funciona no site

O **Grupo VIP** é um grupo de WhatsApp exclusivo para clientes e interessados na Saibai (ofertas da safra, novidades, receitas).

**Link do grupo:**  
[https://chat.whatsapp.com/LmGiN0C8QT04AQ4VB9PDdO](https://chat.whatsapp.com/LmGiN0C8QT04AQ4VB9PDdO)

**Onde aparece no site:**

1. **Botão flutuante** — círculo verde no canto inferior direito, em todas as páginas
2. **Rodapé** — link “WhatsApp — Grupo VIP” na coluna de contato

Ao clicar, o visitante abre o WhatsApp (celular ou web) e pode entrar no grupo. Não é chat direto 1:1; é participação no grupo da comunidade Saibai.

**Para trocar o link no futuro:** peça ao desenvolvedor ou, no personalizador, edite o bloco de texto do rodapé e o snippet do botão flutuante (requer acesso técnico).

---

## Como adicionar um novo produto (passo a passo)

### Passo 1 — Entrar no admin

1. Acesse [admin.shopify.com](https://admin.shopify.com)
2. Faça login com sua conta
3. No menu lateral esquerdo, clique em **Produtos**

📸 *Print sugerido: menu lateral com “Produtos” destacado*

### Passo 2 — Criar o produto

1. Clique no botão **Adicionar produto** (canto superior direito)
2. Preencha:
   - **Título** — ex.: “Alcachofra Fresca Caixa 3 kg”
   - **Descrição** — origem, modo de conservar, receitas
   - **Mídia** — arraste fotos (fundo claro, produto nítido)
   - **Preço** — valor de venda
   - **Estoque** — quantidade disponível (importante para mensagem “Apnas X em estoque”)

📸 *Print sugerido: formulário de produto com título, preço e imagem*

### Passo 3 — Organizar na loja

1. Em **Organização do produto**, escolha:
   - **Tipo** — ex.: Alcachofra fresca
   - **Fornecedor** — Empório Saibai (opcional)
   - **Coleções** — marque **todos** (ou a coleção correta) para aparecer na home e listagens

📸 *Print sugerido: campo “Coleções” com “todos” selecionado*

### Passo 4 — Publicar

1. No canto superior direito, defina **Status** como **Ativo**
2. Clique em **Salvar**

O produto passa a aparecer automaticamente na coleção escolhida e na vitrine, conforme o tema.

---

## Como trocar uma imagem do banner (passo a passo)

O banner principal da home é o **slideshow** (primeira seção, tela cheia).

### Passo 1 — Abrir o personalizador

1. Admin Shopify → **Loja online** → **Temas**
2. No tema Saibai (ou “Cópia de…” em desenvolvimento), clique em **Personalizar**

📸 *Print sugerido: botão “Personalizar” no tema ativo*

### Passo 2 — Ir até a home

1. No topo do personalizador, confirme que está em **Página inicial**
2. Na lista de seções à esquerda, clique em **Slideshow** (ou nome similar do hero)

📸 *Print sugerido: lista de seções com Slideshow selecionado*

### Passo 3 — Trocar a imagem

1. Clique no **slide** (bloco interno)
2. Em **Imagem** (desktop) e **Imagem mobile**, clique em **Selecionar imagem**
3. Envie arquivo novo ou escolha da biblioteca **Conteúdo → Arquivos**
4. Recomendação: JPG/WebP, boa resolução (mín. 1920 px de largura), produto ou campo Saibai

📸 *Print sugerido: painel do slide com botão “Selecionar imagem”*

### Passo 4 — Salvar

1. Clique em **Salvar** (canto superior direito)
2. Abra a loja em outra aba e atualize para conferir

**Dica:** imagens muito pesadas deixam o site lento. Prefira fotos comprimidas (até ~300 KB quando possível).

---

## Como editar textos (passo a passo)

Há dois tipos de texto: **páginas institucionais** e **blocos da home**.

### Opção A — Páginas (Sobre, Contato, Políticas)

1. Admin → **Loja online** → **Páginas**
2. Clique na página desejada (ex.: **Sobre Nós** → handle `sobre`)
3. Edite o conteúdo no editor de texto
4. **Salvar**

📸 *Print sugerido: editor de página “Sobre”*

Páginas criadas para a Saibai:

- `/pages/sobre` — Sobre Nós  
- `/pages/contato` — Contato (formulário)  
- `/pages/politica-de-entrega` — Política de entrega  
- `/pages/politica-de-troca` — Política de troca  

### Opção B — Textos da home (faixa, newsletter, rodapé)

1. **Temas → Personalizar** → Página inicial
2. Clique na seção desejada, por exemplo:
   - **Marquee** — faixa com texto da safra
   - **Newsletter** — título e descrição do e-mail
   - **Rodapé** — colunas de links e textos
3. Edite os campos de texto no painel direito
4. **Salvar**

📸 *Print sugerido: seção Marquee com campo de texto editável*

### Opção C — Announcement bar (topo)

1. No personalizador, clique no **Header** ou **Barra de anúncio**
2. Edite o texto (ex.: “Safra 2026 aberta · Frete grátis acima de R$280…”)
3. **Salvar**

**Atenção:** alguns blocos da home (história da fazenda, feature alcachofra) foram configurados via código. Para mudanças grandes nesses textos, contate a Veltrus.

---

## Perguntas frequentes

**Preciso publicar o tema para os clientes verem?**  
Sim. Alterações no personalizador do tema **publicado** vão ao ar ao salvar. Se estiver editando um tema de **desenvolvimento**, só quem acessa o link de preview vê — é preciso **Publicar** quando estiver pronto.

**Como altero o logo?**  
Admin → **Conteúdo → Arquivos** (já existem os PNGs oficiais). Para trocar no header: **Temas → Personalizar → Header → Logo**, ou peça suporte Veltrus.

**O cliente não recebe e-mail da newsletter?**  
Os inscritos vão para **Clientes** no Shopify. Para campanhas automáticas, o próximo passo recomendado é integrar **Klaviyo** (veja relatório executivo).

---

## Contato do desenvolvedor

**Veltrus Growth & Technology**  
Shopify Partner · ID 4969609  

- Site: [veltrus.com.br](https://veltrus.com.br)  
- E-mail comercial: via canal acordado com a Saibai  
- Suporte técnico do tema: solicitar à Veltrus (alterações em código, tracking, performance)

---

*Documento gerado no Sprint 6 — Empório Saibai · Propriedade intelectual protegida · Reprodução proibida sem autorização.*
