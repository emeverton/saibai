#!/usr/bin/env node
/**
 * Simula request do Shopify App Proxy para testar HMAC + ingestão.
 * Uso: node scripts/test-shopify-proxy.mjs [baseUrl]
 */
import { createHmac } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const baseUrl = process.argv[2] || 'https://tracking-eta-eight.vercel.app';
const shop = 'byinbz-0k.myshopify.com';

function loadSecret() {
  if (process.env.SHOPIFY_APP_PROXY_SECRET) return process.env.SHOPIFY_APP_PROXY_SECRET;
  try {
    const env = readFileSync(resolve(__dirname, '../.env'), 'utf8');
    const match = env.match(/^SHOPIFY_APP_PROXY_SECRET=(.+)$/m);
    if (match) return match[1].trim();
  } catch { /* ignore */ }
  throw new Error('SHOPIFY_APP_PROXY_SECRET não encontrado');
}

function signParams(params, secret) {
  const pairs = [];
  params.forEach((value, key) => {
    if (key !== 'signature') pairs.push(`${key}=${value}`);
  });
  pairs.sort();
  const message = pairs.join('');
  return createHmac('sha256', secret).update(message).digest('hex');
}

const secret = loadSecret();
const params = new URLSearchParams({
  shop,
  path_prefix: '/apps/vlt-tracking',
  timestamp: String(Math.floor(Date.now() / 1000)),
});
params.set('signature', signParams(params, secret));

const eventId = crypto.randomUUID();
const body = {
  event_id: eventId,
  event_name: 'page_view',
  event_time: Math.floor(Date.now() / 1000),
  source: 'shopify',
  shopify_shop_id: shop,
  visitor_id: crypto.randomUUID(),
  session_id: crypto.randomUUID(),
  page_url: 'https://emporiosaibai.com.br/',
  consent_analytics: true,
  consent_marketing: false,
};

const url = `${baseUrl}/api/shopify-proxy/events?${params.toString()}`;
const res = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

const text = await res.text();
console.log('URL:', url.split('?')[0]);
console.log('Status:', res.status);
console.log('Body:', text);
