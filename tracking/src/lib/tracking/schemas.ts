import { z } from 'zod';
import { TRACKING_EVENTS } from './types';

const trackingItemSchema = z.object({
  product_id: z.string().max(128).optional(),
  variant_id: z.string().max(128).optional(),
  sku: z.string().max(128).optional(),
  name: z.string().max(512).optional(),
  quantity: z.number().int().min(0).max(9999).optional(),
  price: z.number().min(0).max(1_000_000).optional(),
});

export const trackingEventSchema = z
  .object({
    event_id: z.string().uuid(),
    event_name: z.enum(TRACKING_EVENTS),
    event_time: z.number().int().positive().optional(),
    source: z.string().max(64).default('shopify'),
    channel: z.string().max(64).optional(),
    shopify_shop_id: z.string().max(128).optional(),
    shopify_customer_id: z.string().max(128).optional(),
    anonymous_id: z.string().max(128).optional(),
    session_id: z.string().max(128).optional(),
    visitor_id: z.string().max(128).optional(),
    email: z.string().email().max(320).optional(),
    phone: z.string().max(32).optional(),
    external_id: z.string().max(128).optional(),
    gclid: z.string().max(256).optional(),
    fbclid: z.string().max(256).optional(),
    ttclid: z.string().max(256).optional(),
    msclkid: z.string().max(256).optional(),
    utm_source: z.string().max(256).optional(),
    utm_medium: z.string().max(256).optional(),
    utm_campaign: z.string().max(256).optional(),
    utm_content: z.string().max(256).optional(),
    utm_term: z.string().max(256).optional(),
    landing_page: z.string().max(2048).optional(),
    referrer: z.string().max(2048).optional(),
    page_url: z.string().max(2048).optional(),
    user_agent: z.string().max(1024).optional(),
    fbp: z.string().max(256).optional(),
    fbc: z.string().max(256).optional(),
    product_id: z.string().max(128).optional(),
    variant_id: z.string().max(128).optional(),
    sku: z.string().max(128).optional(),
    quantity: z.number().int().min(0).max(9999).optional(),
    currency: z.string().length(3).optional(),
    value: z.number().min(0).max(10_000_000).optional(),
    order_id: z.string().max(128).optional(),
    checkout_id: z.string().max(128).optional(),
    consent_analytics: z.boolean().optional(),
    consent_marketing: z.boolean().optional(),
    items: z.array(trackingItemSchema).max(100).optional(),
    properties: z.record(z.unknown()).optional(),
  })
  .strict();

export type TrackingEventInput = z.infer<typeof trackingEventSchema>;

export const MAX_PAYLOAD_BYTES = 32_768;
