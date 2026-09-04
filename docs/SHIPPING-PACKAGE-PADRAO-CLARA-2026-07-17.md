# Pacote de envio padrão — Clara 17/07/2026

**Padrão:** `30 × 14 × 50 cm` · **5 kg** em todos os produtos ativos.

## Feito via API (21/07/2026)

| Campo | Status |
|-------|--------|
| Peso de envio (variantes ativas) | ✅ **5,0 kg** em 17 variantes / 13 produtos |
| Shop metafield `saibai.shipping_package_standard` | ✅ JSON com medidas |
| Pacote físico Shopify (dims 30×14×50) | ✅ Confirmado merchant 21/07 |
| Dimensões no painel Flex Frete | ✅ Confirmado merchant 21/07 (antes citado como Frenet — parceiro real: Flex Frete) |

### Produtos atualizados para 5 kg

- Alcachofra In Natura: T8, T12, T16, T20, P, M, G, MINI *(antes: 0 kg)*
- Conservas: Fundo Inteiro M/G, Fundo Pedaço M/G, Coração P/M/G
- Flores desidratadas · Chaveiro Saibai

## Manual restante (P0 frete)

### 1. Shopify — Pacotes

1. [Configurações → Frete e entrega → Pacotes](https://admin.shopify.com/store/emporiosaibai/settings/shipping/packages)
2. Criar / editar pacote **Caixa padrão Saibai**
3. Dimensões externas: **comprimento 30 · largura 14 · altura 50** (cm)
4. Peso da embalagem vazia: `0` (o peso do produto já é 5 kg)
5. Marcar como **pacote padrão** (usado no cálculo do checkout)

### 2. Flex Frete

1. Abrir app **Flex Frete** → configurações de volume/dimensões padrão
2. Aplicar **30 × 14 × 50 cm** e garantir uso do peso do produto Shopify (5 kg)
3. Salvar e testar cotação com CEP SP / RJ

## QA

1. PDP In Natura → carrinho → calculadora CEP → cotação deve refletir ~5 kg  
2. Checkout: Flex Frete (modalidades ativas) com valores coerentes  
3. Pedido teste: confirmar peso na etiqueta / Flex Frete
