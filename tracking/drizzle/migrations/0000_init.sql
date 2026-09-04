CREATE TABLE IF NOT EXISTS "persons" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
  "first_seen_at" timestamp with time zone DEFAULT now() NOT NULL,
  "last_seen_at" timestamp with time zone DEFAULT now() NOT NULL,
  "primary_email_hash" text,
  "primary_phone_hash" text,
  "shopify_customer_id" text
);

CREATE TABLE IF NOT EXISTS "identities" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
  "person_id" uuid NOT NULL,
  "identifier_type" text NOT NULL,
  "identifier_value_hash" text NOT NULL,
  "first_seen_at" timestamp with time zone DEFAULT now() NOT NULL,
  "last_seen_at" timestamp with time zone DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS "tracking_events" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
  "event_id" text NOT NULL,
  "event_name" text NOT NULL,
  "event_time" timestamp with time zone NOT NULL,
  "source" text NOT NULL,
  "channel" text,
  "shopify_shop_id" text,
  "shopify_customer_id" text,
  "person_id" uuid,
  "anonymous_id" text,
  "session_id" text,
  "visitor_id" text,
  "email_hash" text,
  "phone_hash" text,
  "external_id" text,
  "gclid" text,
  "fbclid" text,
  "ttclid" text,
  "msclkid" text,
  "utm_source" text,
  "utm_medium" text,
  "utm_campaign" text,
  "utm_content" text,
  "utm_term" text,
  "landing_page" text,
  "referrer" text,
  "page_url" text,
  "user_agent" text,
  "ip_hash" text,
  "product_id" text,
  "variant_id" text,
  "sku" text,
  "quantity" integer,
  "currency" text,
  "value" numeric(14, 4),
  "order_id" text,
  "checkout_id" text,
  "raw_payload" jsonb NOT NULL,
  "normalized_payload" jsonb NOT NULL,
  "created_at" timestamp with time zone DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS "destination_logs" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
  "event_id" text NOT NULL,
  "destination" text NOT NULL,
  "status" text NOT NULL,
  "response_code" integer,
  "response_body" text,
  "retry_count" integer DEFAULT 0 NOT NULL,
  "created_at" timestamp with time zone DEFAULT now() NOT NULL,
  "updated_at" timestamp with time zone DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS "ad_costs" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
  "platform" text NOT NULL,
  "account_id" text,
  "campaign_id" text,
  "campaign_name" text,
  "adset_id" text,
  "adset_name" text,
  "ad_id" text,
  "ad_name" text,
  "date" timestamp with time zone NOT NULL,
  "impressions" bigint,
  "clicks" bigint,
  "spend" numeric(14, 4),
  "currency" text,
  "raw_payload" jsonb,
  "created_at" timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE "identities" ADD CONSTRAINT "identities_person_id_persons_id_fk"
  FOREIGN KEY ("person_id") REFERENCES "public"."persons"("id") ON DELETE cascade ON UPDATE no action;

CREATE UNIQUE INDEX IF NOT EXISTS "tracking_events_event_id_uidx" ON "tracking_events" USING btree ("event_id");
CREATE INDEX IF NOT EXISTS "tracking_events_event_name_idx" ON "tracking_events" USING btree ("event_name");
CREATE INDEX IF NOT EXISTS "tracking_events_order_id_idx" ON "tracking_events" USING btree ("order_id");
CREATE INDEX IF NOT EXISTS "tracking_events_person_id_idx" ON "tracking_events" USING btree ("person_id");
CREATE INDEX IF NOT EXISTS "tracking_events_created_at_idx" ON "tracking_events" USING btree ("created_at");
CREATE INDEX IF NOT EXISTS "tracking_events_purchase_dedupe_idx" ON "tracking_events" USING btree ("event_name", "order_id");

CREATE UNIQUE INDEX IF NOT EXISTS "identities_type_value_uidx" ON "identities" USING btree ("identifier_type", "identifier_value_hash");
CREATE INDEX IF NOT EXISTS "identities_person_id_idx" ON "identities" USING btree ("person_id");

CREATE INDEX IF NOT EXISTS "destination_logs_event_id_idx" ON "destination_logs" USING btree ("event_id");
CREATE INDEX IF NOT EXISTS "destination_logs_status_idx" ON "destination_logs" USING btree ("status");
CREATE INDEX IF NOT EXISTS "destination_logs_destination_idx" ON "destination_logs" USING btree ("destination");

CREATE INDEX IF NOT EXISTS "ad_costs_platform_date_idx" ON "ad_costs" USING btree ("platform", "date");
CREATE INDEX IF NOT EXISTS "ad_costs_campaign_id_idx" ON "ad_costs" USING btree ("campaign_id");
