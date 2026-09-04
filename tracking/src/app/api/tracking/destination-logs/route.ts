import { desc, eq } from 'drizzle-orm';
import { NextResponse } from 'next/server';
import { getDb } from '@/db';
import { destinationLogs } from '@/db/schema';
import { verifyAdminAuth } from '@/lib/tracking/security';

export const runtime = 'nodejs';

export async function GET(request: Request) {
  if (!verifyAdminAuth(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const url = new URL(request.url);
  const limit = Math.min(Number(url.searchParams.get('limit') ?? 50), 200);
  const status = url.searchParams.get('status');

  const db = getDb();
  const baseQuery = db.select().from(destinationLogs);
  const rows = await (status
    ? baseQuery.where(eq(destinationLogs.status, status))
    : baseQuery
  )
    .orderBy(desc(destinationLogs.createdAt))
    .limit(limit);

  return NextResponse.json({ logs: rows });
}
