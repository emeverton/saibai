import { NextResponse } from 'next/server';
import { ZodError } from 'zod';
import { ingestTrackingEvent } from '@/lib/tracking/pipeline';
import { trackingEventSchema } from '@/lib/tracking/schemas';
import { assertPayloadSize, getClientIp, hashIp } from '@/lib/tracking/security';
import {
  mapShopifyPaidOrderToPurchase,
  type ShopifyPaidOrder,
} from '@/lib/tracking/shopify-order';
import {
  getShopifyShopDomain,
  getShopifyWebhookSecret,
  getShopifyWebhookTopic,
  verifyShopifyWebhookHmac,
} from '@/lib/tracking/shopify-webhook';

export const runtime = 'nodejs';

export async function POST(request: Request) {
  const secret = getShopifyWebhookSecret();
  const rawBody = await request.text();
  const hmac = request.headers.get('x-shopify-hmac-sha256');

  if (!secret || !verifyShopifyWebhookHmac(rawBody, hmac, secret)) {
    return NextResponse.json({ status: 'invalid', message: 'Invalid webhook signature' }, { status: 401 });
  }

  const topic = getShopifyWebhookTopic(request);
  if (topic && topic !== 'orders/paid') {
    return NextResponse.json({ status: 'ignored', message: `Unexpected topic: ${topic}` }, { status: 200 });
  }

  try {
    assertPayloadSize(rawBody);

    const order = JSON.parse(rawBody) as ShopifyPaidOrder;
    if (!order?.id) {
      return NextResponse.json({ status: 'invalid', message: 'Missing order id' }, { status: 400 });
    }

    const shopDomain = getShopifyShopDomain(request) ?? process.env.SHOPIFY_SHOP_ID;
    if (!shopDomain) {
      return NextResponse.json({ status: 'invalid', message: 'Missing shop domain' }, { status: 400 });
    }

    const mapped = mapShopifyPaidOrderToPurchase(order, shopDomain);
    const input = trackingEventSchema.parse(mapped);

    const clientIp =
      order.client_details?.browser_ip ?? getClientIp(request) ?? undefined;
    const ipHash = clientIp ? await hashIp(clientIp) : undefined;

    const result = await ingestTrackingEvent(input, {
      clientIp,
      ipHash,
      shopifyShopId: shopDomain,
    });

    const statusCode =
      result.status === 'accepted' ? 200 :
      result.status === 'duplicate' ? 200 : 500;

    return NextResponse.json(result, { status: statusCode });
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json(
        { status: 'invalid', message: 'Validation failed', issues: error.flatten() },
        { status: 400 },
      );
    }
    console.error('[shopify/webhooks/orders-paid]', error);
    return NextResponse.json({ status: 'failed', message: 'Internal error' }, { status: 500 });
  }
}
