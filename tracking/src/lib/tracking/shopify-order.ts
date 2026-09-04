import { createHash } from 'node:crypto';
import type { TrackingEventInput } from './schemas';

interface ShopifyOrderLineItem {
  product_id?: number | null;
  variant_id?: number | null;
  sku?: string | null;
  title?: string | null;
  quantity?: number | null;
  price?: string | null;
}

interface ShopifyOrderCustomer {
  id?: number | null;
  email?: string | null;
  phone?: string | null;
}

interface ShopifyOrderNoteAttribute {
  name?: string | null;
  value?: string | null;
}

export interface ShopifyPaidOrder {
  id: number;
  name?: string | null;
  email?: string | null;
  phone?: string | null;
  currency?: string | null;
  total_price?: string | null;
  current_total_price?: string | null;
  buyer_accepts_marketing?: boolean | null;
  checkout_id?: number | null;
  checkout_token?: string | null;
  landing_site?: string | null;
  referring_site?: string | null;
  processed_at?: string | null;
  created_at?: string | null;
  customer?: ShopifyOrderCustomer | null;
  line_items?: ShopifyOrderLineItem[] | null;
  note_attributes?: ShopifyOrderNoteAttribute[] | null;
  client_details?: {
    browser_ip?: string | null;
    user_agent?: string | null;
  } | null;
}

function purchaseEventId(orderId: number | string): string {
  const hash = createHash('sha256').update(`saibai:purchase:${orderId}`).digest();
  hash[6] = (hash[6]! & 0x0f) | 0x40;
  hash[8] = (hash[8]! & 0x3f) | 0x80;
  const hex = hash.subarray(0, 16).toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20, 32)}`;
}

function parseNoteAttributes(
  attributes: ShopifyOrderNoteAttribute[] | null | undefined,
): Record<string, string> {
  const out: Record<string, string> = {};
  if (!attributes) return out;
  for (const attr of attributes) {
    if (attr.name && attr.value) out[attr.name] = attr.value;
  }
  return out;
}

function parseOrderTime(order: ShopifyPaidOrder): number {
  const raw = order.processed_at ?? order.created_at;
  if (raw) {
    const ms = Date.parse(raw);
    if (!Number.isNaN(ms)) return Math.floor(ms / 1000);
  }
  return Math.floor(Date.now() / 1000);
}

function parseMoney(value: string | null | undefined): number | undefined {
  if (!value) return undefined;
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

export function mapShopifyPaidOrderToPurchase(
  order: ShopifyPaidOrder,
  shopDomain: string,
): TrackingEventInput {
  const notes = parseNoteAttributes(order.note_attributes);
  const email = order.email ?? order.customer?.email ?? undefined;
  const phone = order.phone ?? order.customer?.phone ?? undefined;
  const marketingConsent = order.buyer_accepts_marketing === true;

  return {
    event_id: purchaseEventId(order.id),
    event_name: 'purchase',
    event_time: parseOrderTime(order),
    source: 'shopify_webhook',
    channel: 'orders/paid',
    shopify_shop_id: shopDomain,
    shopify_customer_id: order.customer?.id ? String(order.customer.id) : undefined,
    visitor_id: notes.vlt_visitor_id ?? notes.visitor_id,
    session_id: notes.vlt_session_id ?? notes.session_id,
    email: email ?? undefined,
    phone: phone ?? undefined,
    gclid: notes.gclid,
    fbclid: notes.fbclid,
    utm_source: notes.utm_source,
    utm_medium: notes.utm_medium,
    utm_campaign: notes.utm_campaign,
    utm_content: notes.utm_content,
    utm_term: notes.utm_term,
    landing_page: order.landing_site ?? undefined,
    referrer: order.referring_site ?? undefined,
    page_url: order.landing_site ?? undefined,
    user_agent: order.client_details?.user_agent ?? undefined,
    currency: order.currency?.toUpperCase(),
    value: parseMoney(order.current_total_price ?? order.total_price),
    order_id: String(order.id),
    checkout_id: order.checkout_token ?? (order.checkout_id ? String(order.checkout_id) : undefined),
    consent_analytics: true,
    consent_marketing: marketingConsent,
    items: (order.line_items ?? []).map((item) => ({
      product_id: item.product_id ? String(item.product_id) : undefined,
      variant_id: item.variant_id ? String(item.variant_id) : undefined,
      sku: item.sku ?? undefined,
      name: item.title ?? undefined,
      quantity: item.quantity ?? undefined,
      price: parseMoney(item.price),
    })),
    properties: {
      order_name: order.name ?? undefined,
      webhook: 'orders/paid',
    },
  };
}
