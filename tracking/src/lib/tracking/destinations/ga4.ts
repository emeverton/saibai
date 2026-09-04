import type { DestinationResult, NormalizedTrackingEvent, TrackingDestination } from '../types';

const GA4_EVENT_MAP: Record<string, string> = {
  page_view: 'page_view',
  product_view: 'view_item',
  collection_view: 'view_item_list',
  search: 'search',
  add_to_cart: 'add_to_cart',
  remove_from_cart: 'remove_from_cart',
  begin_checkout: 'begin_checkout',
  add_shipping_info: 'add_shipping_info',
  add_payment_info: 'add_payment_info',
  purchase: 'purchase',
  customer_login: 'login',
  customer_register: 'sign_up',
  whatsapp_click: 'whatsapp_click',
  phone_click: 'phone_click',
  email_click: 'email_click',
  coupon_apply: 'coupon_apply',
  coupon_remove: 'coupon_remove',
  cta_click: 'cta_click',
  scroll_depth: 'scroll_depth',
  video_view: 'video_view',
};

export class Ga4Destination implements TrackingDestination {
  name = 'ga4';

  async send(event: NormalizedTrackingEvent): Promise<DestinationResult> {
    const measurementId = process.env.GA4_MEASUREMENT_ID;
    const apiSecret = process.env.GA4_API_SECRET;

    if (!measurementId || !apiSecret) {
      return {
        destination: this.name,
        status: 'skipped',
        error: 'GA4_MEASUREMENT_ID or GA4_API_SECRET not configured',
      };
    }

    const clientId = event.visitorId ?? event.sessionId ?? event.eventId;
    const gaEventName = GA4_EVENT_MAP[event.eventName] ?? event.eventName;

    const params: Record<string, unknown> = {
      currency: event.currency,
      value: event.value,
      transaction_id: event.orderId,
      engagement_time_msec: 1,
      campaign: event.utmCampaign,
      source: event.utmSource,
      medium: event.utmMedium,
      content: event.utmContent,
      term: event.utmTerm,
      page_location: event.pageUrl,
      page_referrer: event.referrer,
    };

    if (event.items?.length) {
      params.items = event.items.map((item) => ({
        item_id: item.product_id || item.variant_id || item.sku,
        item_name: item.name,
        quantity: item.quantity ?? 1,
        price: item.price,
      }));
    }

    const payload = {
      client_id: clientId,
      user_id: event.shopifyCustomerId ?? event.externalId,
      timestamp_micros: event.eventTime.getTime() * 1000,
      events: [
        {
          name: gaEventName,
          params,
        },
      ],
    };

    const url = `https://www.google-analytics.com/mp/collect?measurement_id=${measurementId}&api_secret=${apiSecret}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const body = await response.text();

    return {
      destination: this.name,
      status: response.ok ? 'success' : 'failed',
      responseCode: response.status,
      responseBody: body.slice(0, 4000),
      error: response.ok ? undefined : 'GA4 Measurement Protocol request failed',
    };
  }
}
