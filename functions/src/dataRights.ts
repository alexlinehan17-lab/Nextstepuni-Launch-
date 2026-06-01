import { onCall, HttpsError } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { getAuth } from "firebase-admin/auth";
import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { createHash } from "crypto";

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
  settingsDeleted: number;
  responsesDeleted: number;
  notificationsDeleted: number;
  kudosDeleted: number;
  giftsDeleted: number;
  teachbacksDeleted: number;
  flaresDeleted: number;
  gcNotesDeleted: number;
  gcFlagsDeleted: number;
  islandPublicDeleted: number;
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

  if (targetUid === callerUid) {
    if (requireFreshAuth) {
      const authTime = request.auth.token.auth_time as number | undefined;
      const nowSec = Math.floor(Date.now() / 1000);
      if (!authTime || nowSec - authTime > 300) {
        throw new HttpsError(
          "failed-precondition",
          "Please re-enter your password before deleting your account.",
        );
      }
    }
    return "self";
  }

  const callerDoc = await db.collection("users").doc(callerUid).get();
  const caller = callerDoc.data() || {};
  const isAdmin =
    request.auth.token.email === "admin@nextstep.app" ||
    caller.role === "admin" ||
    caller.isAdmin === true;
  if (isAdmin) return "admin";

  if (caller.role === "gc") {
    const targetDoc = await db.collection("users").doc(targetUid).get();
    if (!targetDoc.exists) throw new HttpsError("not-found", "Student not found.");
    if (targetDoc.data()?.school !== caller.school) {
      throw new HttpsError("permission-denied", "Student is not in your school.");
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
    usersDeleted: 0, progressDeleted: 0, sessionsDeleted: 0, settingsDeleted: 0,
    responsesDeleted: 0, notificationsDeleted: 0, kudosDeleted: 0, giftsDeleted: 0,
    teachbacksDeleted: 0, flaresDeleted: 0, gcNotesDeleted: 0, gcFlagsDeleted: 0,
    islandPublicDeleted: 0, authDeleted: false,
  };

  // School is needed for the gcNotes path; read it before deleting the doc.
  const userSnap = await db.collection("users").doc(uid).get();
  const school = userSnap.exists ? (userSnap.data()?.school as string | undefined) : undefined;

  // progress/{uid}/sessions/* subcollection
  r.sessionsDeleted = await deleteAll(db, db.collection("progress").doc(uid).collection("sessions"));

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
  r.teachbacksDeleted = await deleteAll(db, db.collection("teachbacks").where("authorUid", "==", uid));

  // Flares (feature decommissioned; defensive cleanup of anything sent by uid
  // plus its responses subcollection).
  const flares = await db.collection("flares").where("senderUid", "==", uid).get();
  for (const f of flares.docs) {
    await deleteAll(db, f.ref.collection("responses"));
    await f.ref.delete();
    r.flaresDeleted++;
  }

  // GC private notes about this student (path keyed by school).
  if (school) {
    const ref = db.collection("gcNotes").doc(school).collection("students").doc(uid);
    if ((await ref.get()).exists) { await ref.delete(); r.gcNotesDeleted = 1; }
  }

  // GC flags on this student, under any GC's gcFlags/{gcUid}/flaggedStudents/{uid}.
  const flags = await db.collectionGroup("flaggedStudents").get();
  for (const d of flags.docs) {
    if (d.id === uid) { await d.ref.delete(); r.gcFlagsDeleted++; }
  }

  // users doc last — its deletion also triggers onUserWritten to clean up the
  // island projection (we already deleted it explicitly above).
  if (userSnap.exists) { await db.collection("users").doc(uid).delete(); r.usersDeleted = 1; }

  // Firebase Auth account.
  try {
    await auth.deleteUser(uid);
    r.authDeleted = true;
  } catch (err) {
    logger.warn(`cascadeDeleteUser: auth.deleteUser failed for ${uid}`, err);
  }

  return r;
}

/**
 * requestAccountDeletion — GDPR Article 17.
 * data: { uid?: string }  (defaults to the caller; GC/admin pass a student uid)
 */
export const requestAccountDeletion = onCall({ cors: true }, async (request) => {
  const targetUid = ((request.data as { uid?: string })?.uid) || request.auth?.uid;
  if (!targetUid) throw new HttpsError("invalid-argument", "No target user.");
  const actorRole = await authorize(request, targetUid, /* requireFreshAuth */ true);

  const db = getFirestore();
  const auth = getAuth();
  const report = await cascadeDeleteUser(db, auth, targetUid);

  try {
    await db.collection("dataRequests").add({
      type: "erasure",
      requesterUid: targetUid,
      actorUid: request.auth!.uid,
      actorRole,
      requestedAt: FieldValue.serverTimestamp(),
      fulfilledAt: FieldValue.serverTimestamp(),
      status: "fulfilled",
      cascadeReport: report,
    });
  } catch (err) {
    logger.warn("requestAccountDeletion: failed to write audit record", err);
  }

  logger.info(`Account erased: ${targetUid} by ${actorRole}`, report);
  return { success: true, report };
});

/**
 * exportMyData — GDPR Article 15 (and Article 20 portability).
 * Returns the personal data inline as JSON (pilot scale). Peer identifiers are
 * hashed (DSAR_SPEC §4.4).
 * data: { uid?: string }
 */
export const exportMyData = onCall({ cors: true }, async (request) => {
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
  data.teachbacks = (await db.collection("teachbacks").where("authorUid", "==", targetUid).get()).docs.map((d) => d.data());

  const school = (data.profile as { school?: string } | null)?.school;
  if (school) {
    data.gcNotes = (await db.collection("gcNotes").doc(school).collection("students").doc(targetUid).get()).data() ?? null;
  }

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
