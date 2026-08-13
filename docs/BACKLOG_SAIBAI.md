# Backlog — Saibai (itens diferidos)

Itens registrados durante o closeout. Nenhum bloqueia a operação atual.

## 1. Refatorar módulos Saibai > 300 linhas (com QA de regressão visual)
Dividir em módulos lógicos, atualizando os loaders (`saibai-shell-css`,
`saibai-pages-css`, `global-css`) e preservando a ordem de cascata. Requer
teste visual antes/depois. Arquivos:
`saibai-shell-layout.css` (480), `saibai-header.js` (405), `saibai-consent-popup.js` (398),
`saibai-pages-pdp-recs.css` (354), `saibai-pages-pdp-gallery.css` (353),
`saibai-coupon-popup.js` (351), `saibai-pdp-shipping.js` (344), `saibai-services.css` (329),
`saibai-pages-static.css` (310), `saibai-pages-pdp-shipping.css` (309).

## 2. Corrigir erro pré-existente `ModalDialog is not defined` (quick-view)
Console error em `quick-view` no storefront (não introduzido por nenhuma alteração
desta entrega). Investigar dependência/ordem de carregamento de `ModalDialog`
(provável `global.js`/web component) antes de `quick-view.js`. Requer alteração de
código de tema + republicação.

## 3. Revisar consent region Brasil / Consent API (Customer Privacy)
Em Configurações → Privacidade do cliente, o banner nativo Shopify está desligado
(correto — usamos o banner Saibai LGPD), mas nenhuma região de consentimento está
configurada (Brasil ausente). Confirmar se o banner Saibai registra o consentimento
via Consent API do Shopify e se o Brasil deve ser adicionado à gestão de consentimento.
Item legal/consentimento — requer decisão do dono.

## 4. Inconsistência Boleto em "Termos de serviço" (Legal Settings)
O texto de Termos de serviço lista "boleto bancário" como forma de pagamento, mas o
Boleto não está ativo no checkout (loja usa Mercado Pago Cartões + Pix). O storefront
já foi alinhado (Boleto removido). Avaliar remover "boleto bancário" do texto legal —
alteração de texto legal, requer aprovação do dono.

## 5. Testar cupom `5%NOVOCLIENTE` (se ainda aplicável)
Validar aplicação do cupom no carrinho/checkout caso esteja ativo.
