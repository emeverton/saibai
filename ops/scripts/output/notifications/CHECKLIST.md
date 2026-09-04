# Notificações Saibai 10/10

Admin: https://admin.shopify.com/store/emporiosaibai/settings/notifications

## 1. Branding global (todas as notificações)

Configurações → Notificações → **Personalizar modelos de e-mail**

| Campo | Valor |
|-------|-------|
| Logo | https://cdn.shopify.com/s/files/1/0923/8193/7982/files/LOGO_SAIBAI_RUCULA_2022_f61dca0b-ac73-4665-a141-c6ecf6689198.png?v=1741964529 |
| Cor de destaque | #76BD22 |
| Idioma | Português (Brasil) |

## 2. Remetente

Configurações → Geral → **E-mail do cliente** → `contato@saibai.com.br`

(shop.email já deve ser `contato@saibai.com.br`)

## 3. Modelos prioritários (Editar código em cada um)

Para cada modelo abaixo:
1. Abra a notificação no admin
2. **Assunto do e-mail** → use o subject sugerido no arquivo `.html`
3. **Corpo do e-mail (HTML)** → cole `_saibai-email-header.html` + intro do modelo + conteúdo Shopify + `_saibai-email-footer.html`
4. **Enviar e-mail de teste** antes de salvar

| Arquivo | Notificação no admin |
|---------|---------------------|
| order_confirmation.html | Confirmação de pedido |
| shipping_confirmation.html | Confirmação de envio |
| order_cancelled.html | Pedido cancelado |
| refund_notification.html | Reembolso |
| customer_welcome.html | Boas-vindas à conta |
| contact_customer.html | Contato com cliente |

## 4. Notificações da equipe

Configurações → Notificações → **Notificações da equipe**

- Destinatário: `contato@saibai.com.br` (ou equipe comercial)
- Ative: Novo pedido, Cancelamento, Estoque baixo (frescas)

## 5. SMS (opcional)

Se ativo: textos em pt-BR, opt-in explícito no checkout.

## 6. Validar

- [ ] Teste confirmação de pedido (pedido teste)
- [ ] Teste confirmação de envio (fulfillment teste)
- [ ] Logo + verde Saibai visíveis
- [ ] Footer com contato@saibai.com.br
- [ ] Assuntos em português
