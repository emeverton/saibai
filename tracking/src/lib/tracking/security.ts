import { sha256 } from './hash';
import { MAX_PAYLOAD_BYTES } from './schemas';

const rateLimitStore = new Map<string, { count: number; resetAt: number }>();

export function getClientIp(request: Request): string | undefined {
  const forwarded = request.headers.get('x-forwarded-for');
  if (forwarded) return forwarded.split(',')[0]?.trim();
  return request.headers.get('x-real-ip') ?? undefined;
}

export async function hashIp(ip: string): Promise<string> {
  return sha256(ip);
}

export function verifyTrackingAuth(request: Request): boolean {
  const secret = process.env.TRACKING_ENDPOINT_SECRET;
  if (!secret) return false;

  const header = request.headers.get('x-tracking-secret');
  const auth = request.headers.get('authorization');
  if (header && header === secret) return true;
  if (auth === `Bearer ${secret}`) return true;
  return false;
}

export function verifyAdminAuth(request: Request): boolean {
  const secret = process.env.TRACKING_ADMIN_SECRET ?? process.env.TRACKING_ENDPOINT_SECRET;
  if (!secret) return false;
  const auth = request.headers.get('authorization');
  return auth === `Bearer ${secret}`;
}

export function assertPayloadSize(rawBody: string): void {
  if (rawBody.length > MAX_PAYLOAD_BYTES) {
    throw new Error('Payload too large');
  }
}

export function checkRateLimit(key: string, limit = 120, windowMs = 60_000): boolean {
  const now = Date.now();
  const current = rateLimitStore.get(key);

  if (!current || current.resetAt < now) {
    rateLimitStore.set(key, { count: 1, resetAt: now + windowMs });
    return true;
  }

  if (current.count >= limit) return false;
  current.count += 1;
  return true;
}
