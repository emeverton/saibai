import { desc } from 'drizzle-orm';
import { NextResponse } from 'next/server';
import { getDb } from '@/db';
import { trackingEvents } from '@/db/schema';
import { verifyAdminAuth } from '@/lib/tracking/security';

export const runtime = 'nodejs';

export async function GET(request: Request) {
  if (!verifyAdminAuth(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const url = new URL(request.url);
  const limit = Math.min(Number(url.searchParams.get('limit') ?? 50), 200);

  const db = getDb();
  const rows = await db
    .select({
      event_id: trackingEvents.eventId,
      event_name: trackingEvents.eventName,
      event_time: trackingEvents.eventTime,
      person_id: trackingEvents.personId,
      order_id: trackingEvents.orderId,
      value: trackingEvents.value,
      currency: trackingEvents.currency,
      utm_source: trackingEvents.utmSource,
      gclid: trackingEvents.gclid,
      fbclid: trackingEvents.fbclid,
      created_at: trackingEvents.createdAt,
    })
    .from(trackingEvents)
    .orderBy(desc(trackingEvents.createdAt))
    .limit(limit);

  return NextResponse.json({ events: rows });
}
