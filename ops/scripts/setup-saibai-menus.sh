#!/usr/bin/env bash
# Empório Saibai — Configuração completa de menus (Shopify Admin API)
# Pré-requisito:
# shopify store auth --store byinbz-0k.myshopify.com \
#   --scopes read_content,write_content,read_online_store_navigation,write_online_store_navigation,read_products

set -euo pipefail
STORE="byinbz-0k.myshopify.com"

echo "Menus Saibai configurados via Admin API."
echo "Handles: main-menu, produtos, footer, footer-shop-classic, footer-about-classic, footer-help-classic, nossas-redes"
echo "Reexecute os mutations em scripts/patch-saibai-settings.py ou este arquivo se necessário."
