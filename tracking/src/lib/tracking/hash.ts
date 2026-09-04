const encoder = new TextEncoder();

export async function sha256(value: string): Promise<string> {
  const digest = await crypto.subtle.digest('SHA-256', encoder.encode(value));
  return Array.from(new Uint8Array(digest))
    .map((byte) => byte.toString(16).padStart(2, '0'))
    .join('');
}

export async function hashEmail(email: string): Promise<string> {
  return sha256(email.trim().toLowerCase());
}

export function normalizePhoneE164(phone: string): string {
  const digits = phone.replace(/\D/g, '');
  if (!digits) return '';
  if (digits.startsWith('55') && digits.length >= 12) return `+${digits}`;
  if (digits.length === 10 || digits.length === 11) return `+55${digits}`;
  return `+${digits}`;
}

export async function hashPhone(phone: string): Promise<string | undefined> {
  const normalized = normalizePhoneE164(phone);
  if (!normalized) return undefined;
  return sha256(normalized);
}

export function stripPii<T extends Record<string, unknown>>(payload: T): T {
  const clone = { ...payload };
  delete clone.email;
  delete clone.phone;
  delete clone.client_ip;
  return clone;
}
