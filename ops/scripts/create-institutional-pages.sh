#!/usr/bin/env bash
# Cria páginas institucionais Saibai no Shopify Admin
# Pré-requisito: shopify store auth --store emporiosaibai.myshopify.com --scopes write_content,read_content

set -euo pipefail
STORE="emporiosaibai.myshopify.com"

create_page() {
  local title="$1"
  local handle="$2"
  local suffix="$3"
  shopify store execute -s "$STORE" --allow-mutations -j \
    -q "mutation(\$page: PageCreateInput!) { pageCreate(page: \$page) { page { id handle title templateSuffix } userErrors { field message } } }" \
    -v "{\"page\":{\"title\":\"$title\",\"handle\":\"$handle\",\"templateSuffix\":\"$suffix\",\"body\":\"\"}}"
}

echo "→ Criando páginas institucionais em $STORE ..."

create_page "Nossa história" "historia" "historia"
create_page "A fazenda" "fazenda" "fazenda"
create_page "Conquistas e parcerias" "conquistas" "conquistas"

echo "✓ Páginas criadas. Atualize /pages/sobre para template 'sobre' no Admin se necessário."
