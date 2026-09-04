import { NextResponse } from 'next/server';
import { ZodError } from 'zod';
import { ingestTrackingEvent } from '@/lib/tracking/pipeline';
import { trackingEventSchema } from '@/lib/tracking/schemas';
import {
  assertPayloadSize,
  checkRateLimit,
  getClientIp,
  hashIp,
} from '@/lib/tracking/security';
import {
  getShopifyProxyShop,
  verifyShopifyAppProxySignature,
} from '@/lib/tracking/shopify-proxy';

export const runtime = 'nodejs';

/**
 * Target do Shopify App Proxy:
 * Proxy URL → https://SEU_DOMINIO/api/shopify-proxy
 * Storefront → POST /apps/vlt-tracking/events
 */
export async function POST(request: Request) {
  const url = new URL(request.url);
  const secret = process.env.SHOPIFY_APP_PROXY_SECRET;

  if (!secret || !verifyShopifyAppProxySignature(url.searchParams, secret)) {
    return NextResponse.json({ status: 'invalid', message: 'Invalid proxy signature' }, { status: 401 });
  }

  try {
    const rawBody = await request.text();
    assertPayloadSize(rawBody);

    const clientIp = getClientIp(request);
    const shop = getShopifyProxyShop(url.searchParams);
    const rateKey = `${clientIp ?? 'unknown'}:${shop ?? 'proxy'}`;

    if (!checkRateLimit(rateKey)) {
      return NextResponse.json({ status: 'invalid', message: 'Rate limit exceeded' }, { status: 429 });
    }

    const json = JSON.parse(rawBody);
    const input = trackingEventSchema.parse(json);

    if (input.consent_analytics === false && input.consent_marketing === false) {
      return NextResponse.json({ status: 'invalid', message: 'No consent granted' }, { status: 400 });
    }

    const ipHash = clientIp ? await hashIp(clientIp) : undefined;
    const result = await ingestTrackingEvent(input, {
      clientIp,
      ipHash,
      shopifyShopId: shop ?? input.shopify_shop_id,
    });

    const statusCode =
      result.status === 'accepted' ? 202 :
      result.status === 'duplicate' ? 200 : 500;

    return NextResponse.json(result, { status: statusCode });
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json(
        { status: 'invalid', message: 'Validation failed', issues: error.flatten() },
        { status: 400 },
      );
    }
    console.error('[shopify-proxy/events]', error);
    return NextResponse.json({ status: 'failed', message: 'Internal error' }, { status: 500 });
  }
}
