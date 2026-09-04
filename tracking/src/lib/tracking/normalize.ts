import type { TrackingEventInput } from './schemas';
import { hashEmail, hashPhone, stripPii } from './hash';
import type { NormalizedTrackingEvent } from './types';

export async function normalizeEvent(
  input: TrackingEventInput,
  context: {
    clientIp?: string;
    ipHash?: string;
    shopifyShopId?: string;
  },
): Promise<NormalizedTrackingEvent> {
  const emailHash = input.email ? await hashEmail(input.email) : undefined;
  const phoneHash = input.phone ? await hashPhone(input.phone) : undefined;
  const eventTime = input.event_time
    ? new Date(input.event_time * 1000)
    : new Date();

  const sanitizedRaw = stripPii(input as Record<string, unknown>);

  return {
    eventId: input.event_id,
    eventName: input.event_name,
    eventTime,
    source: input.source ?? 'shopify',
    channel: input.channel,
    shopifyShopId: input.shopify_shop_id ?? context.shopifyShopId,
    shopifyCustomerId: input.shopify_customer_id,
    anonymousId: input.anonymous_id,
    sessionId: input.session_id,
    visitorId: input.visitor_id,
    emailHash,
    phoneHash,
    externalId: input.external_id,
    gclid: input.gclid,
    fbclid: input.fbclid,
    ttclid: input.ttclid,
    msclkid: input.msclkid,
    utmSource: input.utm_source,
    utmMedium: input.utm_medium,
    utmCampaign: input.utm_campaign,
    utmContent: input.utm_content,
    utmTerm: input.utm_term,
    landingPage: input.landing_page || undefined,
    referrer: input.referrer,
    pageUrl: input.page_url || undefined,
    userAgent: input.user_agent,
    clientIp: context.clientIp,
    ipHash: context.ipHash,
    fbp: input.fbp,
    fbc: input.fbc,
    productId: input.product_id,
    variantId: input.variant_id,
    sku: input.sku,
    quantity: input.quantity,
    currency: input.currency?.toUpperCase(),
    value: input.value,
    orderId: input.order_id,
    checkoutId: input.checkout_id,
    consentAnalytics: input.consent_analytics,
    consentMarketing: input.consent_marketing,
    items: input.items,
    properties: input.properties,
    rawPayload: sanitizedRaw,
  };
}
