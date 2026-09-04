import { and, eq, gte, lt, sql } from 'drizzle-orm';
import { getDb } from '@/db';
import { destinationLogs, trackingEvents } from '@/db/schema';

export interface HealthReport {
  ok: boolean;
  checks: Array<{
    name: string;
    ok: boolean;
    detail: string;
  }>;
}

export async function runHealthChecks(): Promise<HealthReport> {
  const db = getDb();
  const since = new Date(Date.now() - 24 * 60 * 60 * 1000);
  const checks: HealthReport['checks'] = [];

  const purchases = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(trackingEvents)
    .where(and(eq(trackingEvents.eventName, 'purchase'), gte(trackingEvents.createdAt, since)));

  const purchaseCount = purchases[0]?.count ?? 0;
  checks.push({
    name: 'purchase_volume_24h',
    ok: purchaseCount > 0,
    detail: `purchase events in last 24h: ${purchaseCount}`,
  });

  const addToCartNow = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(trackingEvents)
    .where(and(eq(trackingEvents.eventName, 'add_to_cart'), gte(trackingEvents.createdAt, since)));

  const since48h = new Date(Date.now() - 48 * 60 * 60 * 1000);
  const addToCartPrevWindow = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(trackingEvents)
    .where(
      and(
        eq(trackingEvents.eventName, 'add_to_cart'),
        gte(trackingEvents.createdAt, since48h),
        lt(trackingEvents.createdAt, since),
      ),
    );

  const currentAtc = addToCartNow[0]?.count ?? 0;
  const prevAtc = addToCartPrevWindow[0]?.count ?? 0;
  const dropPct = prevAtc > 0 ? ((prevAtc - currentAtc) / prevAtc) * 100 : 0;

  checks.push({
    name: 'add_to_cart_drop',
    ok: prevAtc === 0 || dropPct <= 50,
    detail: `add_to_cart drop: ${dropPct.toFixed(1)}% (prev=${prevAtc}, now=${currentAtc})`,
  });

  const failedDestinations = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(destinationLogs)
    .where(and(eq(destinationLogs.status, 'failed'), gte(destinationLogs.createdAt, since)));

  const failedCount = failedDestinations[0]?.count ?? 0;
  checks.push({
    name: 'destination_failures_24h',
    ok: failedCount < 50,
    detail: `failed destination logs: ${failedCount}`,
  });

  const metaFailures = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(destinationLogs)
    .where(
      and(
        eq(destinationLogs.destination, 'meta'),
        eq(destinationLogs.status, 'failed'),
        gte(destinationLogs.createdAt, since),
      ),
    );

  checks.push({
    name: 'meta_capi_errors',
    ok: (metaFailures[0]?.count ?? 0) < 20,
    detail: `meta failures: ${metaFailures[0]?.count ?? 0}`,
  });

  const ga4Failures = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(destinationLogs)
    .where(
      and(
        eq(destinationLogs.destination, 'ga4'),
        eq(destinationLogs.status, 'failed'),
        gte(destinationLogs.createdAt, since),
      ),
    );

  checks.push({
    name: 'ga4_errors',
    ok: (ga4Failures[0]?.count ?? 0) < 20,
    detail: `ga4 failures: ${ga4Failures[0]?.count ?? 0}`,
  });

  const missingAttribution = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(trackingEvents)
    .where(
      and(
        gte(trackingEvents.createdAt, since),
        sql`${trackingEvents.gclid} is null and ${trackingEvents.fbclid} is null and ${trackingEvents.utmSource} is null`,
      ),
    );

  const totalRecent = await db
    .select({ count: sql<number>`count(*)::int` })
    .from(trackingEvents)
    .where(gte(trackingEvents.createdAt, since));

  const missing = missingAttribution[0]?.count ?? 0;
  const total = totalRecent[0]?.count ?? 0;
  const missingRatio = total > 0 ? missing / total : 0;

  checks.push({
    name: 'attribution_coverage',
    ok: missingRatio < 0.95,
    detail: `${missing}/${total} events without utm/gclid/fbclid (${(missingRatio * 100).toFixed(1)}%)`,
  });

  return {
    ok: checks.every((check) => check.ok),
    checks,
  };
}
