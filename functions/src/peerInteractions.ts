import { createHash } from "crypto";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { CALLABLE_OPTIONS, assertUnrevokedAuth } from "./security";
import { giftPrice, isKudosMessageId } from "./peerInteractionPolicy";

function requireUid(value: unknown, field: string): string {
  if (typeof value !== "string" || value.length < 1 || value.length > 128) {
    throw new HttpsError("invalid-argument", `${field} is invalid.`);
  }
  return value;
}

function utcDay(now = new Date()): string {
  return now.toISOString().slice(0, 10);
}

function stableId(...parts: string[]): string {
  return createHash("sha256").update(parts.join("\u0000")).digest("hex");
}

function logRef(uid: string): string {
  return stableId(uid).slice(0, 12);
}

function isStudentProfile(data: FirebaseFirestore.DocumentData | undefined): boolean {
  return data?.role !== "gc"
    && data?.role !== "staff"
    && data?.role !== "admin"
    && data?.isAdmin !== true
    && data?.accountDisabled !== true;
}

async function requirePeerPair(fromUid: string, toUid: string) {
  if (fromUid === toUid) throw new HttpsError("invalid-argument", "Choose another student.");
  const db = getFirestore();
  const [fromSnap, toSnap] = await Promise.all([
    db.collection("users").doc(fromUid).get(),
    db.collection("users").doc(toUid).get(),
  ]);
  const from = fromSnap.data();
  const to = toSnap.data();
  if (!fromSnap.exists || !toSnap.exists || !isStudentProfile(from) || !isStudentProfile(to)) {
    throw new HttpsError("not-found", "That student is not available.");
  }
  if (typeof from?.school !== "string" || !from.school || from.school !== to?.school) {
    throw new HttpsError("permission-denied", "You can only interact with students at your school.");
  }
  return { db, school: from.school };
}

/** One preset kudos message per sender/recipient/day, composed server-side. */
export const sendKudos = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { toUid: rawToUid, messageId } = request.data as { toUid?: unknown; messageId?: unknown };
  const toUid = requireUid(rawToUid, "Recipient");
  if (!isKudosMessageId(messageId)) {
    throw new HttpsError("invalid-argument", "Choose one of the available kudos messages.");
  }

  const { db, school } = await requirePeerPair(request.auth.uid, toUid);
  const day = utcDay();
  const ref = db.collection("kudos").doc(stableId(request.auth.uid, toUid, day));
  const quotaRef = db.collection("peerInteractionRateLimits")
    .doc(`kudos-${stableId(request.auth.uid, day)}`);
  let created = false;
  await db.runTransaction(async transaction => {
    if ((await transaction.get(ref)).exists) return;
    const quotaSnap = await transaction.get(quotaRef);
    const sent = Number(quotaSnap.data()?.count || 0);
    if (sent >= 10) {
      throw new HttpsError("resource-exhausted", "You have reached today's kudos limit.");
    }
    transaction.create(ref, {
      fromUid: request.auth!.uid,
      fromName: "A classmate",
      toUid,
      school,
      messageId,
      day,
      createdAt: FieldValue.serverTimestamp(),
    });
    transaction.set(quotaRef, {
      uid: request.auth!.uid,
      day,
      count: sent + 1,
      expiresAt: new Date(Date.now() + 48 * 60 * 60 * 1000),
      updatedAt: FieldValue.serverTimestamp(),
    });
    created = true;
  });
  logger.info(`sendKudos: ${logRef(request.auth.uid)} -> ${logRef(toUid)} (${messageId})`);
  return { success: true as const, created };
});

/** One allowlisted gift per sender/day with an atomic server-side JP debit. */
export const sendGift = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const { toUid: rawToUid, itemId } = request.data as { toUid?: unknown; itemId?: unknown };
  const toUid = requireUid(rawToUid, "Recipient");
  const price = giftPrice(itemId);
  if (price === null || typeof itemId !== "string") {
    throw new HttpsError("invalid-argument", "That item cannot be gifted.");
  }

  const { db, school } = await requirePeerPair(request.auth.uid, toUid);
  const day = utcDay();
  const giftRef = db.collection("gifts").doc(stableId(request.auth.uid, day));
  const progressRef = db.collection("progress").doc(request.auth.uid);

  await db.runTransaction(async transaction => {
    if ((await transaction.get(giftRef)).exists) {
      throw new HttpsError("already-exists", "You have already sent a gift today.");
    }
    const progressSnap = await transaction.get(progressRef);
    const points = progressSnap.data()?.pointsData || {};
    const earned = Number(points.totalEarned || 0);
    const spent = Number(points.totalSpent || 0);
    if (!Number.isFinite(earned) || !Number.isFinite(spent) || earned - spent < price) {
      throw new HttpsError("failed-precondition", "You do not have enough JP for this gift.");
    }
    transaction.create(giftRef, {
      fromUid: request.auth!.uid,
      fromName: "A classmate",
      toUid,
      school,
      itemId,
      price,
      status: "pending",
      day,
      createdAt: FieldValue.serverTimestamp(),
    });
    transaction.update(progressRef, { "pointsData.totalSpent": FieldValue.increment(price) });
  });

  logger.info(`sendGift: ${logRef(request.auth.uid)} -> ${logRef(toUid)} (${itemId})`);
  return { success: true as const };
});

/** Recipient-only, field-pinned placement transition. */
export const placeGift = onCall(CALLABLE_OPTIONS, async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  await assertUnrevokedAuth(request.auth);
  const giftId = requireUid((request.data as { giftId?: unknown }).giftId, "Gift");
  const db = getFirestore();
  const ref = db.collection("gifts").doc(giftId);
  await db.runTransaction(async transaction => {
    const snap = await transaction.get(ref);
    if (!snap.exists) throw new HttpsError("not-found", "Gift not found.");
    const gift = snap.data();
    if (gift?.toUid !== request.auth!.uid) {
      throw new HttpsError("permission-denied", "This gift belongs to another student.");
    }
    if (gift.status === "placed") return;
    if (gift.status !== "pending") throw new HttpsError("failed-precondition", "This gift cannot be placed.");
    transaction.update(ref, { status: "placed", placedAt: FieldValue.serverTimestamp() });
  });
  return { success: true as const };
});
