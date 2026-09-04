import { eq } from 'drizzle-orm';
import { getDb } from '@/db';
import { destinationLogs } from '@/db/schema';
import { sendN8nAlert, sendSlackAlert } from '@/lib/tracking/alerts/slack';
import { retryFailedEvent } from '@/lib/tracking/pipeline';
import { runHealthChecks } from '@/lib/tracking/health/checks';
import { inngest } from './client';

export const retryDestinationFunction = inngest.createFunction(
  { id: 'tracking-retry-destination', retries: 3 },
  { event: 'tracking/destination.failed' },
  async ({ event, step }) => {
    const eventId = event.data.event_id as string;

    await step.run('retry-destinations', async () => {
      return retryFailedEvent(eventId);
    });
  },
);

export const dailyHealthcheckFunction = inngest.createFunction(
  { id: 'tracking-healthcheck-daily' },
  { cron: '0 8 * * *' },
  async ({ step }) => {
    const report = await step.run('run-healthchecks', async () => runHealthChecks());

    if (!report.ok) {
      await step.run('alert-health-failure', async () => {
        await sendSlackAlert('Saibai tracking healthcheck failed', { checks: report.checks });
        await sendN8nAlert({ type: 'tracking_health_failed', checks: report.checks });
      });
    }

    return report;
  },
);

export const dailyCostsImportFunction = inngest.createFunction(
  { id: 'tracking-costs-import-daily' },
  { cron: '0 6 * * *' },
  async () => {
    return { status: 'placeholder', message: 'Meta/Google cost import not implemented yet' };
  },
);

export const eventReceivedFunction = inngest.createFunction(
  { id: 'tracking-event-received' },
  { event: 'tracking/event.received' },
  async ({ event }) => {
    return { received: true, event_id: event.data.event_id };
  },
);

export const inngestFunctions = [
  retryDestinationFunction,
  dailyHealthcheckFunction,
  dailyCostsImportFunction,
  eventReceivedFunction,
];

export async function listRetryableFailures(limit = 100) {
  const db = getDb();
  return db.query.destinationLogs.findMany({
    where: eq(destinationLogs.status, 'failed'),
    limit,
    orderBy: (table, { desc }) => [desc(table.createdAt)],
  });
}
