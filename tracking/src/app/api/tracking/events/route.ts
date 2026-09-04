import { NextResponse } from 'next/server';
import { ZodError } from 'zod';
import { ingestTrackingEvent } from '@/lib/tracking/pipeline';
import { trackingEventSchema } from '@/lib/tracking/schemas';
import {
  assertPayloadSize,
  checkRateLimit,
  getClientIp,
  hashIp,
  verifyTrackingAuth,
} from '@/lib/tracking/security';

export const runtime = 'nodejs';

export async function POST(request: Request) {
  if (!verifyTrackingAuth(request)) {
    return NextResponse.json({ status: 'invalid', message: 'Unauthorized' }, { status: 401 });
  }

  try {
    const rawBody = await request.text();
    assertPayloadSize(rawBody);

    const clientIp = getClientIp(request);
    const rateKey = `${clientIp ?? 'unknown'}:direct`;
    if (!checkRateLimit(rateKey)) {
      return NextResponse.json({ status: 'invalid', message: 'Rate limit exceeded' }, { status: 429 });
    }

    const json = JSON.parse(rawBody);
    const input = trackingEventSchema.parse(json);
    const ipHash = clientIp ? await hashIp(clientIp) : undefined;

    const result = await ingestTrackingEvent(input, {
      clientIp,
      ipHash,
      shopifyShopId: input.shopify_shop_id ?? process.env.SHOPIFY_SHOP_ID,
    });

    const statusCode =
      result.status === 'accepted' ? 202 :
      result.status === 'duplicate' ? 200 :
      result.status === 'invalid' ? 400 : 500;

    return NextResponse.json(result, { status: statusCode });
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json(
        { status: 'invalid', message: 'Validation failed', issues: error.flatten() },
        { status: 400 },
      );
    }
    if (error instanceof Error && error.message === 'Payload too large') {
      return NextResponse.json({ status: 'invalid', message: 'Payload too large' }, { status: 413 });
    }
    console.error('[tracking/events]', error);
    return NextResponse.json({ status: 'failed', message: 'Internal error' }, { status: 500 });
  }
}
