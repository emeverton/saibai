import { getDb } from '@/db';
import { isDuplicateEvent } from './dedupe';
import { logDestinationResult } from './destination-logs';
import { getDestinations } from './destinations';
import { resolvePerson } from './identity';
import { normalizeEvent } from './normalize';
import { persistEvent } from './persist';
import type { TrackingEventInput } from './schemas';
import type { DestinationResult, IngestResponse, NormalizedTrackingEvent } from './types';
import { inngest } from '@/inngest/client';

function hydrateStoredEvent(payload: unknown): NormalizedTrackingEvent {
  const event = payload as NormalizedTrackingEvent & { eventTime: string | Date };
  if (typeof event.eventTime === 'string') {
    event.eventTime = new Date(event.eventTime);
  }
  return event;
}

interface IngestContext {
  clientIp?: string;
  ipHash?: string;
  shopifyShopId?: string;
}

export async function ingestTrackingEvent(
  input: TrackingEventInput,
  context: IngestContext,
): Promise<IngestResponse> {
  const db = getDb();
  const event = await normalizeEvent(input, context);
  event.personId = undefined;

  if (await isDuplicateEvent(db, event)) {
    return {
      status: 'duplicate',
      event_id: event.eventId,
      message: 'Event already processed',
    };
  }

  const { personId } = await resolvePerson(db, event);
  event.personId = personId;

  await persistEvent(db, event, personId);

  const destinations = await dispatchDestinations(event);

  try {
    await inngest.send({
      name: 'tracking/event.received',
      data: {
        event_id: event.eventId,
        event_name: event.eventName,
        person_id: personId,
      },
    });
  } catch {
    /* non-blocking */
  }

  return {
    status: 'accepted',
    event_id: event.eventId,
    person_id: personId,
    destinations,
  };
}

export async function dispatchDestinations(
  event: Awaited<ReturnType<typeof normalizeEvent>> & { personId?: string },
): Promise<DestinationResult[]> {
  const db = getDb();
  const results: DestinationResult[] = [];

  for (const destination of getDestinations()) {
    let result: DestinationResult;

    const skipMeta = destination.name === 'meta' && event.consentMarketing === false;
    const skipGa4 =
      destination.name === 'ga4' && event.consentAnalytics === false;
    const skipAds =
      destination.name === 'google_ads' && event.consentMarketing === false;

    if (skipMeta || skipGa4 || skipAds) {
      result = {
        destination: destination.name,
        status: 'skipped',
        error: 'Consent not granted for this destination',
      };
      await logDestinationResult(db, event.eventId, result);
      results.push(result);
      continue;
    }

    try {
      result = await destination.send(event);
    } catch (error) {
      result = {
        destination: destination.name,
        status: 'failed',
        error: error instanceof Error ? error.message : 'Unknown destination error',
      };
    }

    await logDestinationResult(db, event.eventId, result);
    results.push(result);

    if (result.status === 'failed') {
      try {
        await inngest.send({
          name: 'tracking/destination.failed',
          data: {
            event_id: event.eventId,
            destination: destination.name,
            error: result.error ?? result.responseBody,
          },
        });
      } catch {
        /* non-blocking */
      }
    }
  }

  return results;
}

export async function retryFailedEvent(eventId: string): Promise<DestinationResult[]> {
  const db = getDb();
  const stored = await db.query.trackingEvents.findFirst({
    where: (table, { eq }) => eq(table.eventId, eventId),
  });

  if (!stored) {
    throw new Error('Event not found');
  }

  const event = hydrateStoredEvent(stored.normalizedPayload);
  event.personId = stored.personId ?? undefined;
  event.clientIp = undefined;

  const results: DestinationResult[] = [];
  const failedLogs = await db.query.destinationLogs.findMany({
    where: (table, { and, eq }) =>
      and(eq(table.eventId, eventId), eq(table.status, 'failed')),
  });

  const failedDestinations = new Set(failedLogs.map((log) => log.destination));

  for (const destination of getDestinations()) {
    if (!failedDestinations.has(destination.name)) continue;

    const result = await destination.send(event);
    await logDestinationResult(
      db,
      eventId,
      result,
      (failedLogs.find((log) => log.destination === destination.name)?.retryCount ?? 0) + 1,
    );
    results.push(result);
  }

  return results;
}
