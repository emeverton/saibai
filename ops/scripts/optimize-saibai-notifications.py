#!/usr/bin/env python3
"""Notificações Saibai 10/10 — Admin → Configurações → Notificações."""

import json
import os
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"
ADMIN_URL = "https://admin.shopify.com/store/emporiosaibai/settings/notifications"
CANONICAL_EMAIL = "contato@saibai.com.br"
LOGO_URL = (
    "https://cdn.shopify.com/s/files/1/0923/8193/7982/files/"
    "LOGO_SAIBAI_RUCULA_2022_f61dca0b-ac73-4665-a141-c6ecf6689198.png?v=1741964529"
)
ACCENT = "#76BD22"
TEXT = "#444643"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output", "notifications")

EMAIL_HEADER = f"""<!-- Saibai — colar no INÍCIO do corpo HTML de cada notificação -->
<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="margin-bottom:24px;">
  <tr>
    <td align="center" style="padding:20px 0 16px;border-bottom:3px solid {ACCENT};">
      <a href="https://emporiosaibai.com.br" style="text-decoration:none;">
        <img src="{LOGO_URL}" alt="Empório Saibai" width="180" style="max-width:180px;height:auto;display:block;">
      </a>
    </td>
  </tr>
</table>
"""

EMAIL_FOOTER = f"""<!-- Saibai — colar no FINAL do corpo HTML de cada notificação -->
<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="margin-top:32px;">
  <tr>
    <td style="padding-top:20px;border-top:1px solid #e8e8e8;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:1.6;color:{TEXT};text-align:center;">
      <p style="margin:0 0 8px;"><strong>Empório Saibai</strong><br>Piedade, SP — Capital Nacional da Alcachofra</p>
      <p style="margin:0 0 8px;">Produção própria · Do plantio à entrega</p>
      <p style="margin:0;">
        Dúvidas?
        <a href="mailto:{CANONICAL_EMAIL}" style="color:{ACCENT};text-decoration:none;">{CANONICAL_EMAIL}</a>
        ·
        <a href="https://emporiosaibai.com.br/pages/contato" style="color:{ACCENT};text-decoration:none;">Fale conosco</a>
      </p>
    </td>
  </tr>
</table>
"""

TEMPLATES = {
    "order_confirmation": {
        "title": "Confirmação de pedido",
        "subject": "Pedido {{ name }} confirmado — Empório Saibai",
        "intro": """<p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#2A3A1A;margin:0 0 16px;">
  Obrigado por comprar no <strong>Empório Saibai</strong>! Recebemos seu pedido e já estamos preparando tudo com o cuidado da nossa produção em Piedade, SP.
</p>
<p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#444643;margin:0 0 16px;">
  <strong>Alcachofras frescas:</strong> enviamos com embalagem térmica. Refrigerar imediatamente e consumir em até 5 dias.
</p>
<p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#444643;margin:0 0 16px;">
  Conservas artesanais ficam bem em casa o ano todo. Em algumas semanas você recebe no e-mail um cupom de recompra exclusivo para clientes Saibai.
</p>""",
    },
    "shipping_confirmation": {
        "title": "Confirmação de envio",
        "subject": "Seu pedido {{ order.name }} foi despachado — Empório Saibai",
        "intro": """<p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#2A3A1A;margin:0 0 16px;">
  Boas notícias! Seu pedido Saibai foi despachado. Acompanhe o rastreamento abaixo.
</p>
<p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#444643;margin:0 0 16px;">
  Produtos frescos: receba e refrigere imediatamente. Dúvidas sobre entrega?
  <a href="mailto:contato@saibai.com.br" style="color:#76BD22;">contato@saibai.com.br</a>
</p>""",
    },
    "order_cancelled": {
        "title": "Pedido cancelado",
        "subject": "Pedido {{ name }} cancelado — Empório Saibai",
        "intro": """<p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#2A3A1A;margin:0 0 16px;">
  Seu pedido foi cancelado conforme solicitado. Se o pagamento já foi processado, o reembolso seguirá o prazo da operadora (até 10 dias úteis).
</p>""",
    },
    "refund_notification": {
        "title": "Reembolso",
        "subject": "Reembolso do pedido {{ order.name }} — Empório Saibai",
        "intro": """<p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#2A3A1A;margin:0 0 16px;">
  Processamos o reembolso do seu pedido. O valor retornará ao mesmo meio de pagamento em até 10 dias úteis.
</p>""",
    },
    "customer_welcome": {
        "title": "Boas-vindas (conta cliente)",
        "subject": "Bem-vindo(a) ao Empório Saibai",
        "intro": """<p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#2A3A1A;margin:0 0 16px;">
  Sua conta foi criada! Acompanhe pedidos, endereços e histórico de compras a qualquer momento.
</p>
<p style="font-family:Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#444643;margin:0 0 16px;">
  Cupom de boas-vindas: <strong>5%NOVOCLIENTE</strong> na primeira compra.
</p>""",
    },
    "contact_customer": {
        "title": "Contato com cliente",
        "subject": "Mensagem da Empório Saibai",
        "intro": """<p style="font-family:Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#2A3A1A;margin:0 0 16px;">
  Olá! A equipe Empório Saibai entrou em contato. Confira a mensagem abaixo.
</p>""",
    },
}


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = [
        "shopify", "store", "execute", "-s", STORE,
        "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:300]}")
    return json.loads(out[start:])


def audit_shop() -> None:
    q = """
    query {
      shop {
        name email contactEmail myshopifyDomain
        primaryDomain { url }
        currencyCode
      }
    }
    """
    r = gql(q)
    shop = r.get("shop", {})
    print(f"  Loja .............. {shop.get('name')}")
    print(f"  shop.email ........ {shop.get('email')}")
    print(f"  shop.contactEmail . {shop.get('contactEmail')}")
    print(f"  Domínio ........... {shop.get('primaryDomain', {}).get('url')}")
    print(f"  Moeda ............. {shop.get('currencyCode')}")
    if shop.get("contactEmail") != CANONICAL_EMAIL:
        print(f"  ⚠ Remetente cliente: altere para {CANONICAL_EMAIL} no admin")
    else:
        print(f"  ✓ E-mail remetente alinhado")
    if shop.get("name") != "Empório Saibai":
        print("  ⚠ Nome da loja: considere «Empório Saibai» (com acento)")


def write_output_files() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(OUTPUT_DIR, "_saibai-email-header.html"), "w", encoding="utf-8") as f:
        f.write(EMAIL_HEADER.strip() + "\n")

    with open(os.path.join(OUTPUT_DIR, "_saibai-email-footer.html"), "w", encoding="utf-8") as f:
        f.write(EMAIL_FOOTER.strip() + "\n")

    checklist = f"""# Notificações Saibai 10/10

Admin: {ADMIN_URL}

## 1. Branding global (todas as notificações)

Configurações → Notificações → **Personalizar modelos de e-mail**

| Campo | Valor |
|-------|-------|
| Logo | {LOGO_URL} |
| Cor de destaque | {ACCENT} |
| Idioma | Português (Brasil) |

## 2. Remetente

Configurações → Geral → **E-mail do cliente** → `{CANONICAL_EMAIL}`

(shop.email já deve ser `{CANONICAL_EMAIL}`)

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

- Destinatário: `{CANONICAL_EMAIL}` (ou equipe comercial)
- Ative: Novo pedido, Cancelamento, Estoque baixo (frescas)

## 5. SMS (opcional)

Se ativo: textos em pt-BR, opt-in explícito no checkout.

## 6. Validar

- [ ] Teste confirmação de pedido (pedido teste)
- [ ] Teste confirmação de envio (fulfillment teste)
- [ ] Logo + verde Saibai visíveis
- [ ] Footer com contato@saibai.com.br
- [ ] Assuntos em português
"""
    with open(os.path.join(OUTPUT_DIR, "CHECKLIST.md"), "w", encoding="utf-8") as f:
        f.write(checklist)

    for key, spec in TEMPLATES.items():
        body = f"{EMAIL_HEADER}\n{spec['intro']}\n{{{{ content }}}}\n{EMAIL_FOOTER}"
        body = body.replace("{{ content }}", "<!-- Mantenha o conteúdo Liquid original da Shopify abaixo do intro Saibai -->")
        content = f"""<!--
  {spec['title']}
  Admin → Notificações → {spec['title']} → Editar código
-->

ASSUNTO SUGERIDO:
{spec['subject']}

CORPO HTML — cole header + intro + (conteúdo Shopify existente) + footer:
-->
{EMAIL_HEADER}
{spec['intro']}
<!-- ↓ Manter o HTML/Liquid original da Shopify abaixo ↓ -->

{EMAIL_FOOTER}
"""
        with open(os.path.join(OUTPUT_DIR, f"{key}.html"), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")


def print_checklist_summary() -> None:
    print("\n=== Checklist Admin → Notificações ===")
    print(f"URL: {ADMIN_URL}\n")
    steps = [
        ("Branding global", f"Logo + cor {ACCENT} + pt-BR"),
        ("Remetente", f"E-mail do cliente → {CANONICAL_EMAIL}"),
        ("Modelos cliente", "6 arquivos em scripts/output/notifications/*.html"),
        ("Equipe", f"Novo pedido → {CANONICAL_EMAIL}"),
        ("Teste", "Enviar e-mail de teste em cada modelo editado"),
    ]
    for i, (title, detail) in enumerate(steps, 1):
        print(f"  {i}. {title}: {detail}")
    print(f"\n  Arquivos: {OUTPUT_DIR}/")


def main() -> int:
    print("=== Saibai Notifications 10/10 ===\n")

    print("1. Auditoria loja")
    audit_shop()

    print("\n2. API Shopify")
    print("  ⚠ Templates de notificação não expõem API pública")
    print("  → Personalização via admin + arquivos HTML gerados")

    print("\n3. Gerando templates Saibai (header/footer + 6 modelos)")
    write_output_files()
    print(f"  ✓ {len(TEMPLATES) + 3} arquivos em {OUTPUT_DIR}")

    print_checklist_summary()
    print("\n=== Concluído ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
