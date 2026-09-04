import {
  bigint,
  index,
  integer,
  jsonb,
  numeric,
  pgTable,
  text,
  timestamp,
  uniqueIndex,
  uuid,
} from 'drizzle-orm/pg-core';

export const trackingEvents = pgTable(
  'tracking_events',
  {
    id: uuid('id').defaultRandom().primaryKey(),
    eventId: text('event_id').notNull(),
    eventName: text('event_name').notNull(),
    eventTime: timestamp('event_time', { withTimezone: true }).notNull(),
    source: text('source').notNull(),
    channel: text('channel'),
    shopifyShopId: text('shopify_shop_id'),
    shopifyCustomerId: text('shopify_customer_id'),
    personId: uuid('person_id'),
    anonymousId: text('anonymous_id'),
    sessionId: text('session_id'),
    visitorId: text('visitor_id'),
    emailHash: text('email_hash'),
    phoneHash: text('phone_hash'),
    externalId: text('external_id'),
    gclid: text('gclid'),
    fbclid: text('fbclid'),
    ttclid: text('ttclid'),
    msclkid: text('msclkid'),
    utmSource: text('utm_source'),
    utmMedium: text('utm_medium'),
    utmCampaign: text('utm_campaign'),
    utmContent: text('utm_content'),
    utmTerm: text('utm_term'),
    landingPage: text('landing_page'),
    referrer: text('referrer'),
    pageUrl: text('page_url'),
    userAgent: text('user_agent'),
    ipHash: text('ip_hash'),
    productId: text('product_id'),
    variantId: text('variant_id'),
    sku: text('sku'),
    quantity: integer('quantity'),
    currency: text('currency'),
    value: numeric('value', { precision: 14, scale: 4 }),
    orderId: text('order_id'),
    checkoutId: text('checkout_id'),
    rawPayload: jsonb('raw_payload').notNull(),
    normalizedPayload: jsonb('normalized_payload').notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
  },
  (table) => [
    uniqueIndex('tracking_events_event_id_uidx').on(table.eventId),
    index('tracking_events_event_name_idx').on(table.eventName),
    index('tracking_events_order_id_idx').on(table.orderId),
    index('tracking_events_person_id_idx').on(table.personId),
    index('tracking_events_created_at_idx').on(table.createdAt),
    index('tracking_events_purchase_dedupe_idx').on(table.eventName, table.orderId),
  ],
);

export const persons = pgTable('persons', {
  id: uuid('id').defaultRandom().primaryKey(),
  firstSeenAt: timestamp('first_seen_at', { withTimezone: true }).defaultNow().notNull(),
  lastSeenAt: timestamp('last_seen_at', { withTimezone: true }).defaultNow().notNull(),
  primaryEmailHash: text('primary_email_hash'),
  primaryPhoneHash: text('primary_phone_hash'),
  shopifyCustomerId: text('shopify_customer_id'),
});

export const identities = pgTable(
  'identities',
  {
    id: uuid('id').defaultRandom().primaryKey(),
    personId: uuid('person_id')
      .notNull()
      .references(() => persons.id, { onDelete: 'cascade' }),
    identifierType: text('identifier_type').notNull(),
    identifierValueHash: text('identifier_value_hash').notNull(),
    firstSeenAt: timestamp('first_seen_at', { withTimezone: true }).defaultNow().notNull(),
    lastSeenAt: timestamp('last_seen_at', { withTimezone: true }).defaultNow().notNull(),
  },
  (table) => [
    uniqueIndex('identities_type_value_uidx').on(
      table.identifierType,
      table.identifierValueHash,
    ),
    index('identities_person_id_idx').on(table.personId),
  ],
);

export const destinationLogs = pgTable(
  'destination_logs',
  {
    id: uuid('id').defaultRandom().primaryKey(),
    eventId: text('event_id').notNull(),
    destination: text('destination').notNull(),
    status: text('status').notNull(),
    responseCode: integer('response_code'),
    responseBody: text('response_body'),
    retryCount: integer('retry_count').default(0).notNull(),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
    updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow().notNull(),
  },
  (table) => [
    index('destination_logs_event_id_idx').on(table.eventId),
    index('destination_logs_status_idx').on(table.status),
    index('destination_logs_destination_idx').on(table.destination),
  ],
);

export const adCosts = pgTable(
  'ad_costs',
  {
    id: uuid('id').defaultRandom().primaryKey(),
    platform: text('platform').notNull(),
    accountId: text('account_id'),
    campaignId: text('campaign_id'),
    campaignName: text('campaign_name'),
    adsetId: text('adset_id'),
    adsetName: text('adset_name'),
    adId: text('ad_id'),
    adName: text('ad_name'),
    date: timestamp('date', { withTimezone: true }).notNull(),
    impressions: bigint('impressions', { mode: 'number' }),
    clicks: bigint('clicks', { mode: 'number' }),
    spend: numeric('spend', { precision: 14, scale: 4 }),
    currency: text('currency'),
    rawPayload: jsonb('raw_payload'),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
  },
  (table) => [
    index('ad_costs_platform_date_idx').on(table.platform, table.date),
    index('ad_costs_campaign_id_idx').on(table.campaignId),
  ],
);

export type TrackingEventRow = typeof trackingEvents.$inferSelect;
export type PersonRow = typeof persons.$inferSelect;
export type IdentityRow = typeof identities.$inferSelect;
export type DestinationLogRow = typeof destinationLogs.$inferSelect;
