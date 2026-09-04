import { eq } from 'drizzle-orm';
import type { Db } from '@/db';
import { destinationLogs } from '@/db/schema';
import type { DestinationResult } from './types';

export async function logDestinationResult(
  db: Db,
  eventId: string,
  result: DestinationResult,
  retryCount = 0,
) {
  await db.insert(destinationLogs).values({
    eventId,
    destination: result.destination,
    status: result.status,
    responseCode: result.responseCode,
    responseBody: result.responseBody ?? result.error,
    retryCount,
    updatedAt: new Date(),
  });
}

export async function getFailedLogs(db: Db, limit = 50) {
  return db.query.destinationLogs.findMany({
    where: eq(destinationLogs.status, 'failed'),
    limit,
    orderBy: (table, { desc }) => [desc(table.createdAt)],
  });
}
