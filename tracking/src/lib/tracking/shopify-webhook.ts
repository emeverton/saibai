import { createHmac, timingSafeEqual } from 'node:crypto';

/**
 * Verifica HMAC de webhooks Shopify (X-Shopify-Hmac-SHA256).
 * @see https://shopify.dev/docs/apps/build/webhooks/subscribe/https
 */
export function verifyShopifyWebhookHmac(
  rawBody: string,
  hmacHeader: string | null,
  secret: string,
): boolean {
  if (!hmacHeader || !secret) return false;

  const digest = createHmac('sha256', secret).update(rawBody, 'utf8').digest('base64');

  try {
    return timingSafeEqual(Buffer.from(digest), Buffer.from(hmacHeader));
  } catch {
    return digest === hmacHeader;
  }
}

export function getShopifyWebhookSecret(): string | undefined {
  return process.env.SHOPIFY_APP_PROXY_SECRET ?? process.env.SHOPIFY_API_SECRET;
}

export function getShopifyShopDomain(request: Request): string | undefined {
  return request.headers.get('x-shopify-shop-domain') ?? undefined;
}

export function getShopifyWebhookTopic(request: Request): string | undefined {
  return request.headers.get('x-shopify-topic') ?? undefined;
}
