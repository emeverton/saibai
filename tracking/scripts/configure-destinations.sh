#!/usr/bin/env bash
# Configura META_ACCESS_TOKEN + GA4_API_SECRET no Vercel e valida destinos.
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

META_TOKEN="${1:-${META_ACCESS_TOKEN:-}}"
GA4_SECRET="${2:-${GA4_API_SECRET:-}}"

if [[ -z "$META_TOKEN" || -z "$GA4_SECRET" ]]; then
  echo "Uso: META_ACCESS_TOKEN=... GA4_API_SECRET=... $0"
  echo "  ou: $0 <META_ACCESS_TOKEN> <GA4_API_SECRET>"
  exit 1
fi

# Atualiza .env local (sem commitar)
if [[ -f .env ]]; then
  if grep -q '^META_ACCESS_TOKEN=' .env; then
    sed -i '' "s|^META_ACCESS_TOKEN=.*|META_ACCESS_TOKEN=$META_TOKEN|" .env
  else
    echo "META_ACCESS_TOKEN=$META_TOKEN" >> .env
  fi
  if grep -q '^GA4_API_SECRET=' .env; then
    sed -i '' "s|^GA4_API_SECRET=.*|GA4_API_SECRET=$GA4_SECRET|" .env
  else
    echo "GA4_API_SECRET=$GA4_SECRET" >> .env
  fi
fi

printf '%s' "$META_TOKEN" | vercel env add META_ACCESS_TOKEN production --force
printf '%s' "$GA4_SECRET" | vercel env add GA4_API_SECRET production --force

echo "Redeploy produção..."
vercel --prod --yes

echo ""
echo "Teste destinos (consent analytics + marketing)..."
node -e "
const body = {
  event_id: crypto.randomUUID(),
  event_name: 'page_view',
  event_time: Math.floor(Date.now()/1000),
  source: 'shopify',
  shopify_shop_id: 'byinbz-0k.myshopify.com',
  visitor_id: crypto.randomUUID(),
  session_id: crypto.randomUUID(),
  page_url: 'https://emporiosaibai.com.br/',
  consent_analytics: true,
  consent_marketing: true,
};
const res = await fetch('https://emporiosaibai.com.br/apps/vlt-tracking/events', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});
console.log('Status:', res.status);
console.log(await res.text());
"

echo "Concluído."
