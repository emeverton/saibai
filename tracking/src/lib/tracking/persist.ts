import type { Db } from '@/db';
import { trackingEvents } from '@/db/schema';
import type { NormalizedTrackingEvent } from './types';

export async function persistEvent(
  db: Db,
  event: NormalizedTrackingEvent,
  personId: string,
) {
  const [row] = await db
    .insert(trackingEvents)
    .values({
      eventId: event.eventId,
      eventName: event.eventName,
      eventTime: event.eventTime,
      source: event.source,
      channel: event.channel,
      shopifyShopId: event.shopifyShopId,
      shopifyCustomerId: event.shopifyCustomerId,
      personId,
      anonymousId: event.anonymousId,
      sessionId: event.sessionId,
      visitorId: event.visitorId,
      emailHash: event.emailHash,
      phoneHash: event.phoneHash,
      externalId: event.externalId,
      gclid: event.gclid,
      fbclid: event.fbclid,
      ttclid: event.ttclid,
      msclkid: event.msclkid,
      utmSource: event.utmSource,
      utmMedium: event.utmMedium,
      utmCampaign: event.utmCampaign,
      utmContent: event.utmContent,
      utmTerm: event.utmTerm,
      landingPage: event.landingPage,
      referrer: event.referrer,
      pageUrl: event.pageUrl,
      userAgent: event.userAgent,
      ipHash: event.ipHash,
      productId: event.productId,
      variantId: event.variantId,
      sku: event.sku,
      quantity: event.quantity,
      currency: event.currency,
      value: event.value != null ? String(event.value) : undefined,
      orderId: event.orderId,
      checkoutId: event.checkoutId,
      rawPayload: event.rawPayload,
      normalizedPayload: JSON.parse(
        JSON.stringify({
          ...event,
          eventTime: event.eventTime.toISOString(),
        }),
      ),
    })
    .returning({ id: trackingEvents.id });

  return row;
}
