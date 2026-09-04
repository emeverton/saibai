import type { DestinationResult, NormalizedTrackingEvent, TrackingDestination } from '../types';

const META_EVENT_MAP: Record<string, string> = {
  page_view: 'PageView',
  product_view: 'ViewContent',
  add_to_cart: 'AddToCart',
  begin_checkout: 'InitiateCheckout',
  add_payment_info: 'AddPaymentInfo',
  purchase: 'Purchase',
  search: 'Search',
  customer_register: 'CompleteRegistration',
};

function mapMetaEventName(eventName: string): string {
  return META_EVENT_MAP[eventName] ?? 'CustomEvent';
}

export class MetaDestination implements TrackingDestination {
  name = 'meta';

  async send(event: NormalizedTrackingEvent): Promise<DestinationResult> {
    const pixelId = process.env.META_PIXEL_ID;
    const accessToken = process.env.META_ACCESS_TOKEN;

    if (!pixelId || !accessToken) {
      return {
        destination: this.name,
        status: 'skipped',
        error: 'META_PIXEL_ID or META_ACCESS_TOKEN not configured',
      };
    }

    const contentIds =
      event.items?.map((item) => item.product_id || item.variant_id).filter(Boolean) ??
      (event.productId ? [event.productId] : []);

    const payload = {
      data: [
        {
          event_name: mapMetaEventName(event.eventName),
          event_time: Math.floor(event.eventTime.getTime() / 1000),
          event_id: event.eventId,
          action_source: 'website',
          event_source_url: event.pageUrl,
          user_data: {
            em: event.emailHash ? [event.emailHash] : undefined,
            ph: event.phoneHash ? [event.phoneHash] : undefined,
            external_id: event.externalId ? [event.externalId] : event.visitorId ? [event.visitorId] : undefined,
            client_ip_address: event.clientIp,
            client_user_agent: event.userAgent,
            fbc: event.fbc,
            fbp: event.fbp,
          },
          custom_data: {
            currency: event.currency,
            value: event.value,
            content_ids: contentIds.length ? contentIds : undefined,
            content_type: 'product',
            contents: event.items?.map((item) => ({
              id: item.product_id || item.variant_id,
              quantity: item.quantity ?? 1,
              item_price: item.price,
            })),
            order_id: event.orderId,
          },
        },
      ],
    };

    const response = await fetch(
      `https://graph.facebook.com/v21.0/${pixelId}/events?access_token=${accessToken}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      },
    );

    const body = await response.text();

    return {
      destination: this.name,
      status: response.ok ? 'success' : 'failed',
      responseCode: response.status,
      responseBody: body.slice(0, 4000),
      error: response.ok ? undefined : 'Meta CAPI request failed',
    };
  }
}
