#!/usr/bin/env python3
"""Políticas legais Saibai 10/10 — Admin → Configurações → Políticas (/settings/legal)."""

import json
import subprocess
import sys
from typing import Any, Dict, Optional

STORE = "byinbz-0k.myshopify.com"
CANONICAL_EMAIL = "contato@saibai.com.br"

CONTACT_INFORMATION = """
<p><strong>Empório Saibai</strong></p>
<p>Razão social conforme CNPJ · Piedade, SP — Capital Nacional da Alcachofra</p>
<p><strong>Telefone:</strong> <a href="tel:+5515997999938">(15) 99799-9938</a></p>
<p><strong>E-mail:</strong> <a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a></p>
<p><strong>Endereço:</strong> Estrada dos Lavradores, 7 — Piedade, SP — CEP 18170-000, Brasil</p>
<p><strong>CNPJ:</strong> 34.754.939/0001-63</p>
<p><strong>Site:</strong> <a href="https://emporiosaibai.com.br">emporiosaibai.com.br</a></p>
<p>Atendimento: segunda a sexta, em horário comercial. Resposta por e-mail em até 2 dias úteis.</p>
""".strip()

PRIVACY_POLICY = """
<p><strong>Empório Saibai</strong> — Piedade, SP</p>
<p>Esta política descreve como coletamos, usamos e protegemos seus dados pessoais, em conformidade com a Lei Geral de Proteção de Dados (LGPD — Lei nº 13.709/2018).</p>
<p><strong>Controlador dos dados</strong></p>
<p>Empório Saibai · CNPJ 34.754.939/0001-63 · Estrada dos Lavradores, 7, Piedade, SP, CEP 18170-000.</p>
<p><strong>Dados coletados</strong></p>
<p>Nome, e-mail, telefone, CPF (quando exigido pela operação), endereço de entrega e dados de pagamento processados de forma segura pelo Shopify e gateways homologados.</p>
<p><strong>Finalidade</strong></p>
<ul>
<li>Processamento e entrega de pedidos;</li>
<li>Comunicação sobre compras, rastreamento e suporte;</li>
<li>Envio de newsletter e ofertas (somente com consentimento);</li>
<li>Medição de desempenho da loja e campanhas (com consentimento no banner de cookies);</li>
<li>Prevenção a fraudes e cumprimento de obrigações legais.</li>
</ul>
<p><strong>Base legal (LGPD)</strong></p>
<p>Execução de contrato (pedidos), consentimento (marketing e cookies não essenciais), legítimo interesse (segurança e melhoria da loja) e cumprimento de obrigação legal.</p>
<p><strong>Compartilhamento</strong></p>
<p>Compartilhamos dados apenas com prestadores essenciais: Shopify (plataforma), transportadoras (Loggi, Frenet e parceiros logísticos), processadores de pagamento e Meta/Google (publicidade e analytics), quando você consente no banner de cookies.</p>
<p><strong>Cookies e tecnologias similares</strong></p>
<ul>
<li><strong>Essenciais:</strong> Shopify — carrinho, checkout, segurança e login.</li>
<li><strong>Análise (opcional):</strong> Google Analytics via canal oficial Google &amp; YouTube.</li>
<li><strong>Marketing (opcional):</strong> Meta Pixel via canal Facebook &amp; Instagram.</li>
<li><strong>Medição server-side:</strong> Stape (quando configurado) — envio de conversões ao servidor, sem cookies de navegador adicionais.</li>
</ul>
<p>Você gerencia preferências no banner de cookies da loja ou nas configurações do navegador.</p>
<p><strong>Retenção</strong></p>
<p>Mantemos os dados pelo tempo necessário para cumprir as finalidades acima e obrigações fiscais/contábeis. Dados de marketing são mantidos até revogação do consentimento.</p>
<p><strong>Seus direitos</strong></p>
<p>Você pode solicitar confirmação de tratamento, acesso, correção, anonimização, portabilidade, eliminação, informação sobre compartilhamento e revogação de consentimento.</p>
<p><strong>Encarregado (DPO)</strong></p>
<p>E-mail: <a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a></p>
<p><strong>Autoridade</strong></p>
<p>Reclamações podem ser dirigidas à Autoridade Nacional de Proteção de Dados (ANPD).</p>
<p>Última atualização: junho de 2026.</p>
""".strip()

SHIPPING_POLICY = """
<p><strong>Prazos de envio</strong></p>
<p>Os pedidos são processados em até <strong>2 dias úteis</strong> após a confirmação do pagamento. O prazo de entrega varia conforme a região e a transportadora selecionada no checkout.</p>
<p><strong>Frete grátis</strong></p>
<p>Frete grátis para pedidos acima de <strong>R$ 320,00</strong> (consulte regiões elegíveis no carrinho).</p>
<p><strong>Transportadoras</strong></p>
<p>Utilizamos parceiros logísticos integrados (Loggi, Frenet e transportadoras regionais). O valor e o prazo são calculados automaticamente no checkout conforme CEP e peso do pedido.</p>
<p><strong>Alcachofras frescas</strong></p>
<p>Produtos frescos são enviados com embalagem térmica especial para preservar qualidade. Recomendamos consumir em até <strong>5 dias</strong> após o recebimento, refrigerando imediatamente.</p>
<p><strong>Conservas e produtos não perecíveis</strong></p>
<p>Enviados em embalagem adequada. Armazene conforme instruções do rótulo.</p>
<p><strong>Rastreamento</strong></p>
<p>Você receberá o código de rastreamento por e-mail assim que o pedido for despachado.</p>
<p><strong>Áreas de entrega</strong></p>
<p>Entregamos em todo o território nacional onde houver cobertura da transportadora selecionada. Em caso de indisponibilidade para seu CEP, entraremos em contato antes do cancelamento.</p>
<p>Dúvidas: <a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a></p>
""".strip()

REFUND_POLICY = """
<p><strong>Direito de arrependimento</strong></p>
<p>Conforme o Código de Defesa do Consumidor (CDC), você pode solicitar a devolução em até <strong>7 dias corridos</strong> após o recebimento do produto, desde que esteja lacrado e em condições de revenda (produtos não perecíveis).</p>
<p><strong>Produtos frescos</strong></p>
<p>Alcachofras frescas e produtos perecíveis: em caso de produto danificado, fora do padrão ou com problemas no transporte, entre em contato em até <strong>24 horas</strong> após o recebimento com fotos do produto e da embalagem.</p>
<p><strong>Como solicitar</strong></p>
<p>Envie e-mail para <a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a> informando número do pedido, motivo e fotos (quando aplicável). Nossa equipe retorna em até 2 dias úteis.</p>
<p><strong>Trocas</strong></p>
<p>Para produtos elegíveis, a troca segue as mesmas condições de devolução. O reenvio ocorre após recebimento e conferência do item devolvido.</p>
<p><strong>Reembolso</strong></p>
<p>Após aprovação, o reembolso é processado no mesmo meio de pagamento em até <strong>10 dias úteis</strong>, conforme prazos do emissor do cartão ou instituição financeira.</p>
<p><strong>Exceções</strong></p>
<p>Produtos consumidos, violados ou armazenados incorretamente após o recebimento não se enquadram no direito de arrependimento.</p>
""".strip()

TERMS_OF_SERVICE = """
<p><strong>1. Identificação</strong></p>
<p>Estes Termos regem o uso da loja virtual Empório Saibai (<a href="https://emporiosaibai.com.br">emporiosaibai.com.br</a>), operada por pessoa jurídica inscrita no CNPJ 34.754.939/0001-63, com sede em Estrada dos Lavradores, 7, Piedade, SP, CEP 18170-000.</p>
<p><strong>2. Produtos</strong></p>
<p>Comercializamos alcachofras frescas (safra sazonal), conservas artesanais e produtos derivados, com descrições, fotos e preços apresentados na loja. Imagens são ilustrativas; variações naturais de produto agrícola podem ocorrer.</p>
<p><strong>3. Preços e pagamento</strong></p>
<p>Preços em reais (BRL), incluindo impostos quando aplicável. Pagamentos processados de forma segura pelo Shopify e gateways homologados. Pedidos só são confirmados após aprovação do pagamento.</p>
<p>Formas de pagamento disponíveis: Pix, cartão de crédito (parcelado conforme operadora) e boleto bancário, conforme exibido no checkout.</p>
<p><strong>Desconto no Pix</strong></p>
<p>Pagamentos via Pix recebem <strong>5% de desconto</strong> sobre o valor dos produtos, aplicado no checkout quando a opção estiver disponível. Não cumulativo com cupons ou outras promoções, salvo indicação em contrário na loja.</p>
<p><strong>4. Pedidos e disponibilidade</strong></p>
<p>Reservamo-nos o direito de cancelar pedidos por indisponibilidade de estoque, falha de pagamento ou suspeita de fraude, com reembolso integral quando aplicável. Produtos de safra fresca podem ter disponibilidade limitada.</p>
<p><strong>5. Entrega</strong></p>
<p>Condições de frete, prazos e regiões conforme nossa <a href="/pages/politica-de-entrega">Política de Entrega</a>. O risco de atraso por transportadora terceira não configura, por si só, descumprimento contratual da Saibai após despacho.</p>
<p><strong>6. Trocas e devoluções</strong></p>
<p>Conforme <a href="/pages/politica-de-troca">Política de Troca e Devolução</a> e o CDC.</p>
<p><strong>7. Conta do cliente</strong></p>
<p>Você é responsável pela veracidade dos dados informados e pela confidencialidade de sua senha.</p>
<p><strong>8. Propriedade intelectual</strong></p>
<p>Marcas, textos, fotos e conteúdos do site são de propriedade do Empório Saibai ou licenciados. Reprodução não autorizada é proibida.</p>
<p><strong>9. Limitação de responsabilidade</strong></p>
<p>Não nos responsabilizamos por danos decorrentes de armazenamento inadequado de produtos perecíveis após entrega, uso diverso do recomendado ou eventos de força maior.</p>
<p><strong>10. Privacidade</strong></p>
<p>Tratamento de dados conforme nossa <a href="/pages/politica-de-privacidade">Política de Privacidade</a> (LGPD).</p>
<p><strong>11. Legislação e foro</strong></p>
<p>Estes Termos são regidos pelas leis da República Federativa do Brasil. Fica eleito o foro da comarca de Piedade/SP, salvo disposição legal em contrário aplicável ao consumidor.</p>
<p><strong>12. Contato</strong></p>
<p><a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a> · <a href="/pages/contato">Fale conosco</a></p>
<p>Última atualização: junho de 2026.</p>
""".strip()

SUBSCRIPTION_POLICY = """
<p><strong>Compras recorrentes, pré-venda e pagamento diferido</strong></p>
<p>Alguns produtos podem ser oferecidos com opções de assinatura, pré-venda (safra) ou pagamento em parcelas, conforme disponibilidade no checkout. Esta política descreve cancelamentos e alterações nesses casos.</p>
<p><strong>Assinaturas</strong></p>
<p>Se disponível para um produto, a assinatura gera cobranças e entregas recorrentes na frequência escolhida. Você pode alterar ou cancelar antes da próxima cobrança pela área do cliente ou contato <a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a>. Cancelamentos já processados não geram reembolso retroativo de ciclos anteriores.</p>
<p><strong>Pré-venda / safra</strong></p>
<p>Pedidos de alcachofra fresca em pré-venda seguem o calendário de colheita informado no produto. Se houver impossibilidade de cumprimento, oferecemos reembolso integral ou crédito, conforme sua preferência.</p>
<p><strong>Pagamento diferido (compre agora, pague depois)</strong></p>
<p>Quando oferecido por parceiros de pagamento, os termos específicos do provedor prevalecem além desta política.</p>
<p><strong>Cancelamento de pedido</strong></p>
<p>Pedidos ainda não despachados podem ser cancelados mediante solicitação por e-mail. Após despacho, aplicam-se as regras da <a href="/pages/politica-de-troca">Política de Troca</a>.</p>
<p>Dúvidas: <a href="mailto:contato@saibai.com.br">contato@saibai.com.br</a></p>
""".strip()

POLICY_UPDATES = [
    {"type": "CONTACT_INFORMATION", "body": CONTACT_INFORMATION},
    {"type": "PRIVACY_POLICY", "body": PRIVACY_POLICY},
    {"type": "SHIPPING_POLICY", "body": SHIPPING_POLICY},
    {"type": "REFUND_POLICY", "body": REFUND_POLICY},
    {"type": "TERMS_OF_SERVICE", "body": TERMS_OF_SERVICE},
    {"type": "SUBSCRIPTION_POLICY", "body": SUBSCRIPTION_POLICY},
]


def gql(query: str, variables: Optional[Dict[str, Any]] = None) -> dict:
    cmd = [
        "shopify", "store", "execute",
        "-s", STORE,
        "--allow-mutations",
        "-j", "-q", query,
    ]
    if variables:
        cmd.extend(["-v", json.dumps(variables)])
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    start = out.find("{")
    if start < 0:
        raise ValueError(f"Sem JSON: {out[:300]}")
    return json.loads(out[start:])


def update_policies() -> int:
    mutation = """
    mutation updatePolicy($policy: ShopPolicyInput!) {
      shopPolicyUpdate(shopPolicy: $policy) {
        shopPolicy { type title url updatedAt }
        userErrors { field message }
      }
    }
    """
    ok = 0
    privacy_blocked = False
    for policy in POLICY_UPDATES:
        r = gql(mutation, {"policy": {"type": policy["type"], "body": policy["body"]}})
        payload = r.get("shopPolicyUpdate", {})
        errs = payload.get("userErrors", [])
        if errs:
            msg = errs[0]["message"]
            print(f"  ✗ {policy['type']}: {msg}")
            if policy["type"] == "PRIVACY_POLICY" and "automático" in msg.lower():
                privacy_blocked = True
            continue
        sp = payload.get("shopPolicy", {})
        print(f"  ✓ {sp.get('title', policy['type'])} ({len(policy['body'])} chars)")
        ok += 1
    if privacy_blocked:
        paste_path = write_privacy_paste_file()
        print("\n  ⚠ PRIVACY_POLICY — passo manual (1 min):")
        print("    1. Admin → Configurações → Políticas → Política de privacidade")
        print("    2. Desative «Gerenciamento automático» / «Use custom policy»")
        print("    3. Cole o HTML de:", paste_path)
        print("    4. Rode novamente: python3 scripts/optimize-saibai-legal-policies.py")
    return ok


def write_privacy_paste_file() -> str:
    import os
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "saibai-privacy-policy-paste.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(PRIVACY_POLICY)
    return path


def audit_policies() -> None:
    q = """
    query {
      shop {
        contactEmail
        email
        shopPolicies { type title body }
      }
    }
    """
    r = gql(q)
    shop = r.get("shop", {})
    print(f"  shop.email .......... {shop.get('email')}")
    print(f"  shop.contactEmail ... {shop.get('contactEmail')}")
    if shop.get("contactEmail") != CANONICAL_EMAIL:
        print(
            f"  ⚠ Ajuste manual: Configurações → Geral → "
            f"E-mail do cliente → {CANONICAL_EMAIL}"
        )
    for p in shop.get("shopPolicies", []):
        body = p.get("body", "")
        flag = "✓" if "{{" not in body and len(body) > 200 else "⚠"
        print(f"  {flag} {p['type']}: {len(body)} chars — {p.get('title')}")


def main() -> int:
    print("=== Saibai Legal Policies 10/10 ===\n")
    print("1. Atualizando 6 políticas via shopPolicyUpdate …")
    updated = update_policies()
    print(f"\n   {updated}/{len(POLICY_UPDATES)} políticas atualizadas\n")
    print("2. Auditoria pós-update …")
    audit_policies()
    print("\n=== Concluído ===")
    print("Admin: https://admin.shopify.com/store/emporiosaibai/settings/legal")
    return 0 if updated == len(POLICY_UPDATES) else 1


if __name__ == "__main__":
    sys.exit(main())
