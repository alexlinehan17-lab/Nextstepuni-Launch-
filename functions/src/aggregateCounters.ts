import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { CALLABLE_OPTIONS, assertUnrevokedAuth } from "./security";

function codeId(value: unknown): string {
  if (typeof value !== "string") throw new HttpsError("invalid-argument", "Class code is required.");
  const code = value.trim().toLowerCase();
  if (!/^[a-z0-9-]{3,40}$/.test(code)) throw new HttpsError("invalid-argument", "Invalid class code.");
  return code;
}

function boundedText(value: unknown, max: number, label: string): string {
  if (typeof value !== "string" || !value || value.length > max) {
    throw new HttpsError("invalid-argument", `${label} is invalid.`);
  }
  return value;
}

function boundedInt(value: unknown, min: number, max: number, label: string): number {
  if (!Number.isInteger(value) || (value as number) < min || (value as number) > max) {
    throw new HttpsError("invalid-argument", `${label} is invalid.`);
  }
  return value as number;
}

function ruleDocId(key: string): string {
  let hash = 0x811c9dc5;
  for (let index = 0; index < key.length; index++) {
    hash ^= key.charCodeAt(index);
    hash = Math.imul(hash, 0x01000193);
  }
  return `r${(hash >>> 0).toString(36)}`;
}

async function takeQuota(uid: string, kind: string, bucket: string, maximum: number): Promise<void> {
  const db = getFirestore();
  const ref = db.collection("aggregateRateLimits").doc(`${uid}-${kind}-${bucket}`);
  await db.runTransaction(async transaction => {
    const snap = await transaction.get(ref);
    const count = Number(snap.data()?.count || 0);
    if (count >= maximum) throw new HttpsError("resource-exhausted", "Submission limit reached. Try again later.");
    transaction.set(ref, {
      uid,
      kind,
      bucket,
      count: count + 1,
      updatedAt: FieldValue.serverTimestamp(),
      expiresAt: new Date(Date.now() + 48 * 60 * 60 * 1000),
    });
  });
}

export const submitChairCohort = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { code: rawCode, deltas: rawDeltas } = request.data as { code?: unknown; deltas?: unknown };
  const code = codeId(rawCode);
  if (!Array.isArray(rawDeltas) || rawDeltas.length > 50) {
    throw new HttpsError("invalid-argument", "Too many marking-rule results.");
  }
  const collapsed = new Map<string, { key: string; subject: string; label: string; over: number; under: number }>();
  for (const raw of rawDeltas) {
    const value = raw as Record<string, unknown>;
    const key = boundedText(value.key, 200, "Rule key");
    const next = {
      key,
      subject: boundedText(value.subject, 60, "Subject"),
      label: boundedText(value.label, 200, "Rule label"),
      over: boundedInt(value.over, 0, 100, "Over-mark count"),
      under: boundedInt(value.under, 0, 100, "Under-mark count"),
    };
    const current = collapsed.get(key);
    if (current) {
      current.over = Math.min(100, current.over + next.over);
      current.under = Math.min(100, current.under + next.under);
    } else collapsed.set(key, next);
  }
  const hour = new Date().toISOString().slice(0, 13);
  await takeQuota(request.auth.uid, "cohort", hour, 10);
  const db = getFirestore();
  const batch = db.batch();
  batch.set(db.collection("chairCohorts").doc(code), { submissions: FieldValue.increment(1) }, { merge: true });
  for (const delta of collapsed.values()) {
    batch.set(db.collection("chairCohorts").doc(code).collection("rules").doc(ruleDocId(delta.key)), {
      key: delta.key,
      subject: delta.subject,
      label: delta.label,
      over: FieldValue.increment(delta.over),
      under: FieldValue.increment(delta.under),
      students: FieldValue.increment(1),
    }, { merge: true });
  }
  await batch.commit();
  return { success: true as const };
});

export const submitChairDecisions = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { code: rawCode, deltas } = request.data as { code?: unknown; deltas?: unknown };
  const code = codeId(rawCode);
  if (!Array.isArray(deltas) || deltas.length < 1 || deltas.length > 100) {
    throw new HttpsError("invalid-argument", "Choose between 1 and 100 decisions.");
  }
  const hour = new Date().toISOString().slice(0, 13);
  await takeQuota(request.auth.uid, "decisions", hour, 20);
  const db = getFirestore();
  const batch = db.batch();
  for (const raw of deltas) {
    const value = raw as Record<string, unknown>;
    const sessionId = boundedText(value.sessionId, 80, "Session");
    const scriptId = boundedText(value.scriptId, 80, "Script");
    const choice = boundedText(value.choice, 160, "Choice");
    batch.set(db.collection("chairCohorts").doc(code).collection("decisions")
      .doc(ruleDocId(`${sessionId}|${scriptId}|${choice}`)), {
      sessionId, scriptId, choice, n: FieldValue.increment(1),
    }, { merge: true });
  }
  await batch.commit();
  return { success: true as const };
});

export const submitChairDaily = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { code: rawCode, day: rawDay, bucket: rawBucket } = request.data as Record<string, unknown>;
  const code = codeId(rawCode);
  const day = boundedText(rawDay, 10, "Day");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) throw new HttpsError("invalid-argument", "Day is invalid.");
  const bucket = boundedInt(rawBucket, 0, 10, "Bucket");
  await takeQuota(request.auth.uid, `daily-${code}`, day, 1);
  await getFirestore().collection("chairCohorts").doc(code).collection("daily").doc(`${day}-b${bucket}`).set({
    day, bucket, n: FieldValue.increment(1),
  }, { merge: true });
  return { success: true as const };
});

export const recordFocusPresence = onCall(CALLABLE_OPTIONS, async request => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { code: rawCode, bucket: rawBucket } = request.data as Record<string, unknown>;
  const code = codeId(rawCode);
  const bucket = boundedInt(rawBucket, 0, Number.MAX_SAFE_INTEGER, "Presence bucket");
  const current = Math.floor(Date.now() / (5 * 60_000));
  if (Math.abs(bucket - current) > 1) throw new HttpsError("invalid-argument", "Presence bucket is stale.");
  await takeQuota(request.auth.uid, `presence-${code}`, String(bucket), 1);
  await getFirestore().collection("focusPresence").doc(code).collection("buckets").doc(String(bucket)).set({
    n: FieldValue.increment(1),
  }, { merge: true });
  return { success: true as const };
});
