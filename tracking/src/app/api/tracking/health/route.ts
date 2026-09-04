import { NextResponse } from 'next/server';
import { runHealthChecks } from '@/lib/tracking/health/checks';
import { verifyAdminAuth } from '@/lib/tracking/security';

export const runtime = 'nodejs';

export async function GET(request: Request) {
  if (!verifyAdminAuth(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const report = await runHealthChecks();
  return NextResponse.json(report, { status: report.ok ? 200 : 503 });
}
