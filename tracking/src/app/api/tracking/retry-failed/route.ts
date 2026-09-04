import { NextResponse } from 'next/server';
import { z } from 'zod';
import { retryFailedEvent } from '@/lib/tracking/pipeline';
import { verifyAdminAuth } from '@/lib/tracking/security';

export const runtime = 'nodejs';

const bodySchema = z.object({
  event_id: z.string().uuid(),
});

export async function POST(request: Request) {
  if (!verifyAdminAuth(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const body = bodySchema.parse(await request.json());
    const results = await retryFailedEvent(body.event_id);
    return NextResponse.json({ event_id: body.event_id, results });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Retry failed';
    return NextResponse.json({ error: message }, { status: 400 });
  }
}
