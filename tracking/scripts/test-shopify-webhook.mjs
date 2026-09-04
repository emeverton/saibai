#!/usr/bin/env node
/**
 * Simula webhook orders/paid com HMAC Shopify.
 * Uso: node scripts/test-shopify-webhook.mjs [baseUrl]
 */
import { createHmac } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const baseUrl = process.argv[2] || 'https://tracking-eta-eight.vercel.app';

function loadSecret() {
  if (process.env.SHOPIFY_APP_PROXY_SECRET) return process.env.SHOPIFY_APP_PROXY_SECRET;
  const env = readFileSync(resolve(__dirname, '../.env'), 'utf8');
  const match = env.match(/^SHOPIFY_APP_PROXY_SECRET=(.+)$/m);
  if (match) return match[1].trim();
  throw new Error('SHOPIFY_APP_PROXY_SECRET não encontrado');
}

const secret = loadSecret();
const orderId = Math.floor(Date.now() / 1000);
const body = JSON.stringify({
  id: orderId,
  name: '#TEST-WEBHOOK',
  email: 'test@emporiosaibai.com.br',
  currency: 'BRL',
  total_price: '149.90',
  current_total_price: '149.90',
  buyer_accepts_marketing: true,
  processed_at: new Date().toISOString(),
  created_at: new Date().toISOString(),
  landing_site: 'https://emporiosaibai.com.br/',
  referring_site: 'https://google.com/',
  customer: { id: 900001, email: 'test@emporiosaibai.com.br' },
  line_items: [
    {
      product_id: 1001,
      variant_id: 2001,
      title: 'Conserva Saibai Teste',
      quantity: 1,
      price: '149.90',
      sku: 'TEST-SKU',
    },
  ],
  client_details: {
    browser_ip: '203.0.113.10',
    user_agent: 'SaibaiWebhookTest/1.0',
  },
});

const hmac = createHmac('sha256', secret).update(body, 'utf8').digest('base64');
const url = `${baseUrl}/api/shopify/webhooks/orders-paid`;

const res = await fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Shopify-Hmac-SHA256': hmac,
    'X-Shopify-Topic': 'orders/paid',
    'X-Shopify-Shop-Domain': 'byinbz-0k.myshopify.com',
  },
  body,
});

const text = await res.text();
console.log('URL:', url);
console.log('Order ID:', orderId);
console.log('Status:', res.status);
console.log('Body:', text);
