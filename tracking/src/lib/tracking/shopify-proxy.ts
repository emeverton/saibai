import { createHmac, timingSafeEqual } from 'node:crypto';

/**
 * Verifica assinatura HMAC do Shopify App Proxy.
 * @see https://shopify.dev/docs/apps/build/online-store/app-proxies/authenticate-app-proxies
 */
export function verifyShopifyAppProxySignature(
  searchParams: URLSearchParams,
  secret: string,
): boolean {
  const signature = searchParams.get('signature');
  if (!signature || !secret) return false;

  const pairs: string[] = [];
  searchParams.forEach((value, key) => {
    if (key !== 'signature') {
      pairs.push(`${key}=${value}`);
    }
  });
  pairs.sort();
  const message = pairs.join('');

  const digest = createHmac('sha256', secret).update(message).digest('hex');

  try {
    return timingSafeEqual(Buffer.from(digest), Buffer.from(signature));
  } catch {
    return digest === signature;
  }
}

export function getShopifyProxyShop(searchParams: URLSearchParams): string | undefined {
  return searchParams.get('shop') ?? undefined;
}
