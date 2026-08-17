/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { getFirestore, FieldValue } from "firebase-admin/firestore";
import { HttpsError, onCall } from "firebase-functions/v2/https";
import { logger } from "firebase-functions/v2";
import { checkStaffMessage } from "./staffMessagePolicy";

/** Cap kept in step with MAX_ITEMS in components/gc/gcNotifications.ts. */
const MAX_ITEMS = 200;
/** One call may not spray the whole school; the dashboard sends a year group. */
const MAX_RECIPIENTS = 400;

/**
 * sendStaffNotification
 *
 * The ONLY way a member of school staff can put a notification in front of a
 * student. Staff writes to /notifications are denied by firestore.rules, so
 * every field a student sees is composed here from a preset id.
 *
 * See ./staffMessagePolicy for why this moved server-side: the previous control
 * lived in the student's own React bundle and keyed on a field the sender
 * controlled, so a staff account could deliver arbitrary prose to a minor with
 * one setDoc from the browser console.
 *
 * Authorisation mirrors the rule it replaces: the caller must be gc/staff, and
 * every recipient must be a student at the caller's own school.
 */
export const sendStaffNotification = onCall({ cors: true }, async (request) => {
  if (!request.auth) {
    throw new HttpsError("unauthenticated", "Must be logged in.");
  }

  const { studentUids, kind, messageId, toolId } = request.data as {
    studentUids?: unknown; kind?: unknown; messageId?: unknown; toolId?: unknown;
  };

  const check = checkStaffMessage(kind, messageId);
  if (!check.ok) {
    throw new HttpsError("invalid-argument",
      check.reason === "kind" ? "Unknown message kind." : "That is not a message staff may send.");
  }
  if (!Array.isArray(studentUids) || studentUids.length === 0 || studentUids.length > MAX_RECIPIENTS) {
    throw new HttpsError("invalid-argument", "Choose between 1 and 400 recipients.");
  }
  if (!studentUids.every(uid => typeof uid === "string" && uid.length > 0 && uid.length <= 128)) {
    throw new HttpsError("invalid-argument", "Invalid recipient.");
  }
  // A tool id only ever names a tool the client will look up in its own
  // registry; it is never rendered as prose. Bounded so it cannot smuggle text.
  if (toolId !== undefined && (typeof toolId !== "string" || toolId.length > 60)) {
    throw new HttpsError("invalid-argument", "Invalid tool.");
  }

  const db = getFirestore();
  const callerSnap = await db.collection("users").doc(request.auth.uid).get();
  const caller = callerSnap.data();
  const callerRole = caller?.role;
  if (callerRole !== "gc" && callerRole !== "staff") {
    throw new HttpsError("permission-denied", "Only school staff can send this.");
  }
  const callerSchool = typeof caller?.school === "string" ? caller.school : "";
  if (!callerSchool) {
    throw new HttpsError("failed-precondition", "Your account is not linked to a school.");
  }

  const senderName = typeof caller?.name === "string" && caller.name.trim() !== ""
    ? caller.name.trim().slice(0, 50)
    : "Your school";

  let delivered = 0;
  for (const studentUid of studentUids as string[]) {
    // Same-school check per recipient — the caller supplies the uid list, so it
    // is never trusted. A staff member cannot reach a student at another school.
    const studentSnap = await db.collection("users").doc(studentUid).get();
    if (!studentSnap.exists || studentSnap.data()?.school !== callerSchool) {
      logger.warn(`sendStaffNotification: ${request.auth.uid} tried to message ${studentUid} outside ${callerSchool}`);
      continue;
    }

    const item: Record<string, unknown> = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`,
      type: check.type,
      title: check.title,
      // Legacy display field. Kept empty on purpose: the student's client
      // renders staff-originated notifications from messageId, and leaving a
      // sender-supplied string here is exactly what this change removes.
      body: "",
      messageId: check.messageId,
      fromGCName: senderName,
      fromGCUid: request.auth.uid,
      severity: check.kind === "encouragement" ? "success" : "info",
      timestamp: Date.now(),
      read: false,
    };
    if (typeof toolId === "string" && toolId !== "") item.actionToolId = toolId;

    const ref = db.collection("notifications").doc(studentUid);
    await db.runTransaction(async txn => {
      const snap = await txn.get(ref);
      const existing = snap.exists ? ((snap.data()?.items || []) as unknown[]) : [];
      txn.set(ref, {
        items: [item, ...existing].slice(0, MAX_ITEMS),
        updatedAt: FieldValue.serverTimestamp(),
      }, { merge: true });
    }).then(() => { delivered += 1; })
      .catch(err => logger.error(`sendStaffNotification: write failed for ${studentUid}`, err));
  }

  logger.info(`sendStaffNotification: ${check.kind} from ${request.auth.uid} to ${delivered} student(s)`);
  return { success: true as const, delivered };
});
