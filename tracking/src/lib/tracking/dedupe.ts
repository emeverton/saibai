import { and, eq } from 'drizzle-orm';
import type { Db } from '@/db';
import { trackingEvents } from '@/db/schema';
import type { NormalizedTrackingEvent } from './types';

export async function isDuplicateEvent(
  db: Db,
  event: NormalizedTrackingEvent,
): Promise<boolean> {
  const byEventId = await db.query.trackingEvents.findFirst({
    where: eq(trackingEvents.eventId, event.eventId),
    columns: { id: true },
  });

  if (byEventId) return true;

  if (event.eventName === 'purchase' && event.orderId) {
    const byPurchase = await db.query.trackingEvents.findFirst({
      where: and(
        eq(trackingEvents.eventName, 'purchase'),
        eq(trackingEvents.orderId, event.orderId),
      ),
      columns: { id: true },
    });
    if (byPurchase) return true;
  }

  return false;
}
