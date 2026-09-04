export const SHOPIFY_EVENTS = [
  'page_view',
  'product_view',
  'collection_view',
  'search',
  'add_to_cart',
  'remove_from_cart',
  'begin_checkout',
  'add_shipping_info',
  'add_payment_info',
  'purchase',
  'customer_login',
  'customer_register',
] as const;

export const CUSTOM_EVENTS = [
  'whatsapp_click',
  'phone_click',
  'email_click',
  'coupon_apply',
  'coupon_remove',
  'cta_click',
  'scroll_depth',
  'video_view',
] as const;

export const TRACKING_EVENTS = [...SHOPIFY_EVENTS, ...CUSTOM_EVENTS] as const;

export type TrackingEventName = (typeof TRACKING_EVENTS)[number];

export type IdentifierType =
  | 'email'
  | 'phone'
  | 'shopify_customer_id'
  | 'visitor_id'
  | 'session_id'
  | 'gclid'
  | 'fbclid'
  | 'ttclid'
  | 'msclkid';

export interface TrackingItem {
  product_id?: string;
  variant_id?: string;
  sku?: string;
  name?: string;
  quantity?: number;
  price?: number;
}

export interface ClientTrackingPayload {
  event_id: string;
  event_name: TrackingEventName;
  event_time?: number;
  source?: string;
  channel?: string;
  shopify_shop_id?: string;
  shopify_customer_id?: string;
  anonymous_id?: string;
  session_id?: string;
  visitor_id?: string;
  email?: string;
  phone?: string;
  external_id?: string;
  gclid?: string;
  fbclid?: string;
  ttclid?: string;
  msclkid?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
  utm_term?: string;
  landing_page?: string;
  referrer?: string;
  page_url?: string;
  user_agent?: string;
  fbp?: string;
  fbc?: string;
  product_id?: string;
  variant_id?: string;
  sku?: string;
  quantity?: number;
  currency?: string;
  value?: number;
  order_id?: string;
  checkout_id?: string;
  consent_analytics?: boolean;
  consent_marketing?: boolean;
  items?: TrackingItem[];
  properties?: Record<string, unknown>;
}

export interface NormalizedTrackingEvent {
  eventId: string;
  eventName: TrackingEventName;
  eventTime: Date;
  source: string;
  channel?: string;
  shopifyShopId?: string;
  shopifyCustomerId?: string;
  personId?: string;
  anonymousId?: string;
  sessionId?: string;
  visitorId?: string;
  emailHash?: string;
  phoneHash?: string;
  externalId?: string;
  gclid?: string;
  fbclid?: string;
  ttclid?: string;
  msclkid?: string;
  utmSource?: string;
  utmMedium?: string;
  utmCampaign?: string;
  utmContent?: string;
  utmTerm?: string;
  landingPage?: string;
  referrer?: string;
  pageUrl?: string;
  userAgent?: string;
  clientIp?: string;
  ipHash?: string;
  fbp?: string;
  fbc?: string;
  productId?: string;
  variantId?: string;
  sku?: string;
  quantity?: number;
  currency?: string;
  value?: number;
  orderId?: string;
  checkoutId?: string;
  consentAnalytics?: boolean;
  consentMarketing?: boolean;
  items?: TrackingItem[];
  properties?: Record<string, unknown>;
  rawPayload: Record<string, unknown>;
}

export type IngestStatus = 'accepted' | 'duplicate' | 'invalid' | 'failed';

export interface IngestResponse {
  status: IngestStatus;
  event_id?: string;
  person_id?: string;
  destinations?: DestinationResult[];
  message?: string;
}

export interface DestinationResult {
  destination: string;
  status: 'success' | 'failed' | 'skipped';
  responseCode?: number;
  responseBody?: string;
  error?: string;
}

export interface TrackingDestination {
  name: string;
  send(event: NormalizedTrackingEvent): Promise<DestinationResult>;
}

export interface ResolvePersonResult {
  personId: string;
  isNew: boolean;
}
