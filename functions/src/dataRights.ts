import { onCall, HttpsError } from "firebase-functions/v2/https";
import { onSchedule } from "firebase-functions/v2/scheduler";
import { logger } from "firebase-functions/v2";
import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { createHash } from "crypto";
import { CALLABLE_OPTIONS, assertSensitiveAuth, assertUnrevokedAuth, isVerifiedAdminToken } from "./security";
import { feedbackRateLimitId } from "./anonymousFeedbackPolicy";

/**
 * Data-subject rights — GDPR Article 15 (access/export) and Article 17 (erasure).
 *
 * Pragmatic, synchronous, pilot-scale implementation of compliance/DSAR_SPEC.md
 * (the spec's async Cloud-Tasks/Storage/SLA-monitor machinery is deferred; for
 * ~534 students the work is small enough to run inline in the callable).
 *
 * Both functions authorise: the data subject themselves (self), a Guidance
 * Counsellor of the same school, or admin. Erasure self-service additionally
 * requires a fresh re-authentication (token issued in the last 5 minutes).
 *
 * Audit (DSAR_SPEC §5.2 / Art 17(3)(b) accountability): each request appends a
 * server-only record to /dataRequests; the erasure record carries a count-only
 * cascadeReport and is retained after the underlying data is gone.
 */

type ActorRole = "self" | "gc" | "admin";

interface CascadeReport {
  usersDeleted: number;
  progressDeleted: number;
  sessionsDeleted: number;
  srsDeleted: number;
  settingsDeleted: number;
  responsesDeleted: number;
  notificationsDeleted: number;
  kudosDeleted: number;
  giftsDeleted: number;
  gcFlagsDeleted: number;
  islandPublicDeleted: number;
  staffMembershipsDeleted: number;
  accessRecordsDeleted: number;
  rateLimitsDeleted: number;
  authDeleted: boolean;
}

// Stable, non-reversible label for another data subject's UID, so an export is
// portable without leaking peer identifiers (DSAR_SPEC §4.4).
function peerHash(uid: string): string {
  return "peer-" + createHash("sha256").update(uid).digest("hex").slice(0, 8);
}

// Delete every doc matched by a query/collection, batched (Firestore caps a
// batch at 500 writes). Returns the number deleted.
async function deleteAll(
  db: FirebaseFirestore.Firestore,
  query: FirebaseFirestore.Query,
): Promise<number> {
  const snap = await query.get();
  for (let i = 0; i < snap.docs.length; i += 450) {
    const batch = db.batch();
    for (const d of snap.docs.slice(i, i + 450)) batch.delete(d.ref);
    await batch.commit();
  }
  return snap.docs.length;
}

// Authorise the caller against the target. Read-only for export; erasure passes
// requireFreshAuth=true so self-service deletion forces a recent re-auth.
async function authorize(
  request: { auth?: { uid: string; token: Record<string, unknown> } },
  targetUid: string,
  requireFreshAuth: boolean,
): Promise<ActorRole> {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be logged in.");
  const db = getFirestore();
  const callerUid = request.auth.uid;

  if (requireFreshAuth) await assertSensitiveAuth(request.auth);
  else await assertUnrevokedAuth(request.auth);

  if (targetUid === callerUid) {
    return "self";
  }

  const callerDoc = await db.collection("users").doc(callerUid).get();
  const caller = callerDoc.data() || {};
  const isAdmin = isVerifiedAdminToken(request.auth.token);
  if (isAdmin) return "admin";

  if (caller.role === "gc" && caller.accountDisabled !== true) {
    const targetDoc = await db.collection("users").doc(targetUid).get();
    if (!targetDoc.exists) throw new HttpsError("not-found", "Student not found.");
    const target = targetDoc.data() || {};
    if (target.school !== caller.school) {
      throw new HttpsError("permission-denied", "Student is not in your school.");
    }
    // A GC may only export/erase *student* accounts — never another GC or an
    // admin. Without this a GC could pass a colleague-GC/admin uid (same
    // school) and cascade-delete that staff account. (Security review
    // 2026-07-16, HIGH.)
    if (target.role === "gc" || target.role === "staff" || target.role === "admin" || target.isAdmin === true) {
      throw new HttpsError("permission-denied", "Guidance counsellors can only act on student accounts.");
    }
    return "gc";
  }

  throw new HttpsError("permission-denied", "Not authorised for this account.");
}

// Cascade-delete every collection that holds the student's data, then the Auth
// account. Collection set verified against firestore.rules + the write sites.
async function cascadeDeleteUser(
  db: FirebaseFirestore.Firestore,
  auth: ReturnType<typeof getAuth>,
  uid: string,
): Promise<CascadeReport> {
  const r: CascadeReport = {
    usersDeleted: 0, progressDeleted: 0, sessionsDeleted: 0, srsDeleted: 0, settingsDeleted: 0,
    responsesDeleted: 0, notificationsDeleted: 0, kudosDeleted: 0, giftsDeleted: 0,
    gcFlagsDeleted: 0, islandPublicDeleted: 0, staffMembershipsDeleted: 0,
    accessRecordsDeleted: 0, rateLimitsDeleted: 0, authDeleted: false,
  };

  // School is needed for the cohortTags path; read it before deleting the doc.
  const userSnap = await db.collection("users").doc(uid).get();
  const school = userSnap.exists ? (userSnap.data()?.school as string | undefined) : undefined;

  // Make the Firestore session cutoff effective before the first destructive
  // step. Disabling an Auth user does not invalidate an already-issued ID token
  // inside Firestore rules, whereas these server-owned fields do.
  if (userSnap.exists) {
    await userSnap.ref.update({
      accountDisabled: true,
      sessionValidAfterSeconds: Math.floor(Date.now() / 1000),
    });
  }

  // Disable and revoke first so a partially completed retry cannot race a live
  // client recreating documents. Missing Auth users are already effectively
  // disabled and make the rest of the cascade idempotent.
  try {
    await auth.updateUser(uid, { disabled: true });
    await auth.revokeRefreshTokens(uid);
  } catch (err) {
    if ((err as { code?: string }).code !== "auth/user-not-found") throw err;
  }

  // progress/{uid}/sessions/* subcollection
  r.sessionsDeleted = await deleteAll(db, db.collection("progress").doc(uid).collection("sessions"));

  // progress/{uid}/srs/* — Mark Bank's spaced-repetition memory, one document
  // per deck. Deleting a Firestore DOCUMENT does not delete its subcollections,
  // so erasing progress/{uid} below would leave this behind: a live record of
  // what a named student has and has not learned, keyed by their uid, surviving
  // an account deletion. Every subcollection under progress/ must be listed here
  // explicitly — add the next one at the same time you add the feature.
  r.srsDeleted = await deleteAll(db, db.collection("progress").doc(uid).collection("srs"));

  // Single docs keyed by uid.
  const singles: Array<[string, keyof CascadeReport]> = [
    ["progress", "progressDeleted"],
    ["settings", "settingsDeleted"],
    ["responses", "responsesDeleted"],
    ["notifications", "notificationsDeleted"],
    ["islandPublic", "islandPublicDeleted"],
  ];
  for (const [coll, key] of singles) {
    const ref = db.collection(coll).doc(uid);
    if ((await ref.get()).exists) { await ref.delete(); (r[key] as number) = 1; }
  }

  // Peer-feature docs sent by or to this student.
  r.kudosDeleted =
    (await deleteAll(db, db.collection("kudos").where("fromUid", "==", uid))) +
    (await deleteAll(db, db.collection("kudos").where("toUid", "==", uid)));
  r.giftsDeleted =
    (await deleteAll(db, db.collection("gifts").where("fromUid", "==", uid))) +
    (await deleteAll(db, db.collection("gifts").where("toUid", "==", uid)));

  // GC notes (gcNotes) were removed 2026-07-18, so there is nothing to erase
  // there. Cohort tags remain and are keyed by school.
  if (school) {
    // Cohort tags (DEIS/At-risk/Priority) about this student, held in
    // cohortTags/{school}.tags[uid]. Remove the student's entry (security
    // review 2026-07-16, M-8 — these must be in the erasure cascade).
    const cohortRef = db.collection("cohortTags").doc(school);
    if ((await cohortRef.get()).exists) {
      // This is welfare-sensitive data. Failure is material and must leave the
      // erasure request in a retryable failed state, never falsely fulfilled.
      await cohortRef.update({ [`tags.${uid}`]: FieldValue.delete() });
    }
  }

  // GC flags on this student, under any GC's gcFlags/{gcUid}/flaggedStudents/{uid}.
  const flags = await db.collectionGroup("flaggedStudents").get();
  for (const d of flags.docs) {
    if (d.id === uid) { await d.ref.delete(); r.gcFlagsDeleted++; }
  }

  // Staff membership documents contain a name and email and live below a
  // school-keyed parent, so deleting users/{uid} alone would not remove them.
  r.staffMembershipsDeleted = await deleteAll(
    db,
    db.collectionGroup("members").where("uid", "==", uid),
  );

  // Provisioning registries and abuse-prevention counters are also keyed by or
  // contain a UID. Remove direct records and any current access-code audit
  // references so account erasure is complete across security collections.
  const accessRecords = await db.collection("gcAccounts").where("uid", "==", uid).get();
  for (const record of accessRecords.docs) {
    await record.ref.delete();
    r.accessRecordsDeleted++;
  }
  for (const collectionName of ["staffClaimAttempts", "schoolClaimAttempts"] as const) {
    const ref = db.collection(collectionName).doc(uid);
    if ((await ref.get()).exists) {
      await ref.delete();
      r.rateLimitsDeleted++;
    }
  }
  // Feedback quotas use rotating, one-way daily IDs so feedback itself stays
  // anonymous. Recompute the only still-live buckets during erasure instead of
  // retaining even that pseudonymous link until TTL happens to run.
  for (let daysAgo = 0; daysAgo <= 2; daysAgo++) {
    const day = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000).toISOString().slice(0, 10);
    const ref = db.collection("feedbackRateLimits").doc(feedbackRateLimitId(uid, day));
    if ((await ref.get()).exists) {
      await ref.delete();
      r.rateLimitsDeleted++;
    }
  }
  r.rateLimitsDeleted += await deleteAll(
    db,
    db.collection("staffMessageRateLimits").where("uid", "==", uid),
  );
  r.rateLimitsDeleted += await deleteAll(
    db,
    db.collection("aggregateRateLimits").where("uid", "==", uid),
  );
  r.rateLimitsDeleted += await deleteAll(
    db,
    db.collection("peerInteractionRateLimits").where("uid", "==", uid),
  );
  for (const collectionName of ["staffAccessSecrets", "studentAccessSecrets"] as const) {
    const secretDocs = await db.collection(collectionName).get();
    for (const secret of secretDocs.docs) {
      const data = secret.data();
      const patch: Record<string, FirebaseFirestore.FieldValue> = {};
      if (data.rotatedBy === uid) patch.rotatedBy = FieldValue.delete();
      if (data.consumedBy === uid) patch.consumedBy = FieldValue.delete();
      if (Object.keys(patch).length > 0) await secret.ref.update(patch);
    }
  }

  // users doc last — its deletion also triggers onUserWritten to clean up the
  // island projection (we already deleted it explicitly above).
  if (userSnap.exists) { await db.collection("users").doc(uid).delete(); r.usersDeleted = 1; }

  // Firebase Auth account. Failure is material: do not report an erasure as
  // fulfilled while a login credential still exists.
  try {
    await auth.deleteUser(uid);
    r.authDeleted = true;
  } catch (err) {
    if ((err as { code?: string }).code === "auth/user-not-found") {
      r.authDeleted = true;
    } else {
      throw err;
    }
  }

  return r;
}

/**
 * requestAccountDeletion — GDPR Article 17.
 * data: { uid?: string }  (defaults to the caller; GC/admin pass a student uid)
 */
export const requestAccountDeletion = onCall(CALLABLE_OPTIONS, async (request) => {
  const targetUid = ((request.data as { uid?: string })?.uid) || request.auth?.uid;
  if (!targetUid) throw new HttpsError("invalid-argument", "No target user.");
  const actorRole = await authorize(request, targetUid, /* requireFreshAuth */ true);

  const db = getFirestore();
  const auth = getAuth();
  const auditRef = db.collection("dataRequests").doc();
  await auditRef.set({
      type: "erasure",
      requesterUid: targetUid,
      actorUid: request.auth!.uid,
      actorRole,
      requestedAt: FieldValue.serverTimestamp(),
      status: "processing",
      attempts: 1,
  });

  try {
    const report = await cascadeDeleteUser(db, auth, targetUid);
    await auditRef.update({
      fulfilledAt: FieldValue.serverTimestamp(),
      status: "fulfilled",
      cascadeReport: report,
    });
    logger.info(`Account erased: ${targetUid} by ${actorRole}`, report);
    return { success: true, requestId: auditRef.id, report };
  } catch (err) {
    logger.error(`requestAccountDeletion: cascade failed for ${targetUid}`, err);
    await auditRef.update({
      status: "failed",
      failedAt: FieldValue.serverTimestamp(),
      failureCode: (err as { code?: string }).code || "unknown",
    });
    throw new HttpsError(
      "internal",
      `Account deletion is recorded as ${auditRef.id} but did not complete. Support can safely retry it.`,
    );
  }
});

/**
 * Retry partial erasures without requiring a now-disabled student to sign in
 * again. Each run claims failed records one at a time and the cascade itself is
 * idempotent, so a transient Firestore/Auth failure cannot become a silently
 * abandoned Article 17 request.
 */
export const retryFailedAccountDeletions = onSchedule(
  { schedule: "every 24 hours", timeZone: "Europe/Dublin" },
  async () => {
    const db = getFirestore();
    const auth = getAuth();
    const failed = await db.collection("dataRequests")
      .where("status", "==", "failed")
      .limit(20)
      .get();

    for (const requestDoc of failed.docs) {
      const data = requestDoc.data();
      if (data.type !== "erasure" || typeof data.requesterUid !== "string") continue;
      const attempts = typeof data.attempts === "number" ? data.attempts : 1;
      if (attempts >= 5) {
        logger.error(`Erasure ${requestDoc.id} requires manual intervention after ${attempts} attempts.`);
        continue;
      }

      const claimed = await db.runTransaction(async transaction => {
        const current = (await transaction.get(requestDoc.ref)).data();
        if (current?.status !== "failed") return false;
        transaction.update(requestDoc.ref, {
          status: "processing",
          attempts: attempts + 1,
          retryStartedAt: FieldValue.serverTimestamp(),
        });
        return true;
      });
      if (!claimed) continue;

      try {
        const report = await cascadeDeleteUser(db, auth, data.requesterUid);
        await requestDoc.ref.update({
          status: "fulfilled",
          fulfilledAt: FieldValue.serverTimestamp(),
          cascadeReport: report,
          failureCode: FieldValue.delete(),
        });
      } catch (err) {
        logger.error(`Scheduled erasure retry failed for ${requestDoc.id}`, err);
        await requestDoc.ref.update({
          status: "failed",
          failedAt: FieldValue.serverTimestamp(),
          failureCode: (err as { code?: string }).code || "unknown",
        });
      }
    }
  },
);

/**
 * exportMyData — GDPR Article 15 (and Article 20 portability).
 * Returns the personal data inline as JSON (pilot scale). Peer identifiers are
 * hashed (DSAR_SPEC §4.4).
 * data: { uid?: string }
 */
export const exportMyData = onCall(CALLABLE_OPTIONS, async (request) => {
  const targetUid = ((request.data as { uid?: string })?.uid) || request.auth?.uid;
  if (!targetUid) throw new HttpsError("invalid-argument", "No target user.");
  const actorRole = await authorize(request, targetUid, /* requireFreshAuth */ false);

  const db = getFirestore();
  const auth = getAuth();
  const get1 = async (coll: string) => (await db.collection(coll).doc(targetUid).get()).data() ?? null;

  const data: Record<string, unknown> = {};
  data.profile = await get1("users");
  data.progress = await get1("progress");
  data.settings = await get1("settings");
  data.responses = await get1("responses");
  data.notifications = await get1("notifications");
  data.studySessions = (await db.collection("progress").doc(targetUid).collection("sessions").get()).docs.map((d) => d.data());
  // Mark Bank spaced-repetition memory, one document per deck. Held in a
  // SUBCOLLECTION of progress/{uid}, so data.progress above does not contain
  // it — an Article 15 export that omitted this would be incomplete.
  data.markBankMemory = (await db.collection("progress").doc(targetUid).collection("srs").get())
    .docs.map((d) => ({ deckId: d.id, ...d.data() }));

  data.kudosSent = (await db.collection("kudos").where("fromUid", "==", targetUid).get()).docs.map((d) => {
    const x = { ...d.data() }; if (x.toUid) x.toUid = peerHash(x.toUid); return x;
  });
  data.kudosReceived = (await db.collection("kudos").where("toUid", "==", targetUid).get()).docs.map((d) => {
    const x = { ...d.data() }; if (x.fromUid) x.fromUid = peerHash(x.fromUid); return x;
  });
  data.giftsSent = (await db.collection("gifts").where("fromUid", "==", targetUid).get()).docs.map((d) => {
    const x = { ...d.data() }; if (x.toUid) x.toUid = peerHash(x.toUid); return x;
  });
  data.giftsReceived = (await db.collection("gifts").where("toUid", "==", targetUid).get()).docs.map((d) => {
    const x = { ...d.data() }; if (x.fromUid) x.fromUid = peerHash(x.fromUid); return x;
  });

  // (GC free-text notes were removed 2026-07-18, so there is nothing to export
  // from gcNotes.)

  try {
    const u = await auth.getUser(targetUid);
    data.account = { email: u.email ?? null, createdAt: u.metadata.creationTime ?? null, lastSignInAt: u.metadata.lastSignInTime ?? null };
  } catch {
    data.account = null;
  }

  try {
    await db.collection("dataRequests").add({
      type: "access",
      requesterUid: targetUid,
      actorUid: request.auth!.uid,
      actorRole,
      requestedAt: FieldValue.serverTimestamp(),
      fulfilledAt: FieldValue.serverTimestamp(),
      status: "fulfilled",
    });
  } catch (err) {
    logger.warn("exportMyData: failed to write audit record", err);
  }

  return {
    _audit: {
      generatedAt: new Date().toISOString(),
      schemaVersion: 1,
      requesterUid: targetUid,
      actorRole,
      note: "Personal data held by NextStepUni Ltd (Processor) on behalf of your school (Controller). Identifiers belonging to other students are replaced with stable hashes. See the Privacy Notice for the categories, recipients, retention period and your rights.",
    },
    data,
  };
});
