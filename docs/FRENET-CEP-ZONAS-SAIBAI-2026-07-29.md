# Frenet — cobertura Brasil (auditoria 02/09/2026)

**Parceiro de cotação live:** **Frenet** (painel `painel.frenet.com.br`, conta Otavio / `comercial@saibai.com.br`).  
**Origem:** CEP `18176-210` · Piedade/SP.  
**Plataforma:** Shopify (`emporiosaibai.com.br`).

CSV de faixas (referência operacional, não importação Frenet): `exports/flex-frete-cep-ranges-saibai.csv`

## Veredito

**PODE SEGUIR** no painel Frenet — cobertura **já é Brasil**. Não havia regra de CEP a ampliar.

| Camada | Status |
|--------|--------|
| Correios via Frenet PAC | **Ativo** · status na plataforma **Ativada** |
| Correios via Frenet Sedex | **Ativo** · **Ativada** |
| Mini Envios | **Ativo**, mas **rejeita** o pacote padrão 30×14×50 cm / 5 kg |
| Restrição Mini `#74876` | **Desabilitada** |
| Regras simples (prazo alcachofra / desconto SP) | Fora de vigência |
| Jadlog Package | Cotou DF, **não ativada** (`Quero ativar` · hash `onboardingRejected`) |

## Smoke simulador (02/09)

Pacote Clara: 30×14×50 cm · 5 kg · R$ 100 · origem `18176-210`.

| CEP | Resultado Frenet |
|-----|------------------|
| `70040-010` DF | PAC **R$ 37,11** / 7 du · Sedex **R$ 62,93** / 3 du · Mini: dimensões excedidas |

Banner simultâneo: instabilidade temporária dos Correios. Cotação no checkout Shopify pode falhar **mesmo com PAC/Sedex ativos**.

## O que não é Frenet

Se a PDP/checkout ainda mostra *“Não encontramos frete”* com CEP válido, o bloqueio está no **app de frete do Shopify** (Flex Frete / zonas) ou na instabilidade dos Correios — não em faixa CEP da Frenet.
