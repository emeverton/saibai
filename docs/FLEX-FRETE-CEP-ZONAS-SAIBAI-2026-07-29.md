# Zonas de frete Saibai — Brasil (canônico desde 2026-09-02)

**Parceiro de cotação live:** **Frenet** (PAC + Sedex via Frenet já cotam Brasil — ver `FRENET-CEP-ZONAS-SAIBAI-2026-07-29.md`).  
**CSV canônico (referência / Flex Frete se ainda instalado):** `exports/flex-frete-cep-ranges-saibai.csv` (todas as UFs)  
**Legacy Sudeste:** `exports/flex-frete-cep-ranges-saibai-sudeste-LEGACY.csv`  
**Legacy 34 bairros:** `exports/flex-frete-cep-ranges-saibai-34-bairros-LEGACY.csv`

| Regra | Valor |
|-------|-------|
| Cobertura | **Brasil** — 27 UFs + DF |
| Frete | Cotado no checkout (Flex Frete) |
| Frete grátis | acima de **R$ 389,90** |
| Pedido mínimo | **R$ 100,00** |
| Gate tema | UF ViaCEP ∈ qualquer UF brasileira |

## Motivo da mudança

Clientes fora do Sudeste (e CEPs de SP fora da planilha antiga de 34 bairros) não conseguiam cotar frete. O gate do tema + Flex Frete ainda restritos bloqueavam checkout. Pedido: abrir cobertura em nível Brasil.

## Faixas CEP (resumo)

| Região | CEP inicial | CEP final |
|--------|-------------|-----------|
| Brasil | 01000 | 99999 |

Detalhamento por UF no CSV canônico.

## Tema Shopify

`saibai-delivery.js` + `saibai-delivery-zones.js` — allowlist por **UF Brasil**.

## Ação manual Clara (bloqueia cotação)

1. Flex Frete: substituir faixas atuais pelo CSV canônico Brasil.  
2. Smoke: cotar CEP `04520-000` (Moema) → deve retornar taxa.  
3. Smoke: CEP `70040-010` (DF) → deve retornar taxa.  
4. Smoke: CEP `80010-000` (Curitiba/PR) → deve retornar taxa.
