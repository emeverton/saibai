import { and, eq, inArray } from 'drizzle-orm';
import type { Db } from '@/db';
import { identities, persons } from '@/db/schema';
import { sha256 } from './hash';
import type { IdentifierType, NormalizedTrackingEvent, ResolvePersonResult } from './types';

interface IdentifierCandidate {
  type: IdentifierType;
  value: string;
  hash?: string;
}

function buildCandidates(event: NormalizedTrackingEvent): IdentifierCandidate[] {
  const candidates: IdentifierCandidate[] = [];

  if (event.emailHash) {
    candidates.push({ type: 'email', value: event.emailHash, hash: event.emailHash });
  }
  if (event.phoneHash) {
    candidates.push({ type: 'phone', value: event.phoneHash, hash: event.phoneHash });
  }
  if (event.shopifyCustomerId) {
    candidates.push({ type: 'shopify_customer_id', value: event.shopifyCustomerId });
  }
  if (event.visitorId) {
    candidates.push({ type: 'visitor_id', value: event.visitorId });
  }
  if (event.sessionId) {
    candidates.push({ type: 'session_id', value: event.sessionId });
  }
  if (event.gclid) candidates.push({ type: 'gclid', value: event.gclid });
  if (event.fbclid) candidates.push({ type: 'fbclid', value: event.fbclid });
  if (event.ttclid) candidates.push({ type: 'ttclid', value: event.ttclid });
  if (event.msclkid) candidates.push({ type: 'msclkid', value: event.msclkid });

  return candidates;
}

async function hashIdentifierValue(value: string): Promise<string> {
  return sha256(value.trim().toLowerCase());
}

export async function resolvePerson(
  db: Db,
  event: NormalizedTrackingEvent,
): Promise<ResolvePersonResult> {
  const candidates = buildCandidates(event);
  const hashedCandidates = await Promise.all(
    candidates.map(async (candidate) => ({
      type: candidate.type,
      hash: candidate.hash ?? (await hashIdentifierValue(candidate.value)),
    })),
  );

  if (hashedCandidates.length === 0) {
    const [person] = await db
      .insert(persons)
      .values({ lastSeenAt: new Date() })
      .returning({ id: persons.id });
    return { personId: person.id, isNew: true };
  }

  const hashes = hashedCandidates.map((item) => item.hash);
  const matches = await db.query.identities.findMany({
    where: inArray(identities.identifierValueHash, hashes),
  });

  let personId = matches[0]?.personId;

  if (!personId) {
    const [person] = await db
      .insert(persons)
      .values({
        primaryEmailHash: event.emailHash,
        primaryPhoneHash: event.phoneHash,
        shopifyCustomerId: event.shopifyCustomerId,
        lastSeenAt: new Date(),
      })
      .returning({ id: persons.id });
    personId = person.id;
  } else {
    await db
      .update(persons)
      .set({
        lastSeenAt: new Date(),
        primaryEmailHash: event.emailHash ?? undefined,
        primaryPhoneHash: event.phoneHash ?? undefined,
        shopifyCustomerId: event.shopifyCustomerId ?? undefined,
      })
      .where(eq(persons.id, personId));
  }

  for (const candidate of hashedCandidates) {
    const existing = await db.query.identities.findFirst({
      where: and(
        eq(identities.identifierType, candidate.type),
        eq(identities.identifierValueHash, candidate.hash),
      ),
    });

    if (!existing) {
      await db.insert(identities).values({
        personId,
        identifierType: candidate.type,
        identifierValueHash: candidate.hash,
      });
      continue;
    }

    if (existing.personId !== personId) {
      await db
        .update(identities)
        .set({ personId, lastSeenAt: new Date() })
        .where(eq(identities.id, existing.id));
    } else {
      await db
        .update(identities)
        .set({ lastSeenAt: new Date() })
        .where(eq(identities.id, existing.id));
    }
  }

  return { personId, isNew: matches.length === 0 };
}
