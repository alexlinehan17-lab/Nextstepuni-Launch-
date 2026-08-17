/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * What a member of school staff is allowed to say to a student.
 *
 * ─── WHY THIS IS ON THE SERVER (security review 2026-08-17) ────────────────
 *
 * Commit 6b30f259 replaced the free-text "Send Encouragement" and tool-note
 * fields with preset pickers, and claimed arbitrary text could not reach a
 * minor "even if a document were written directly through the SDK, bypassing
 * the dashboard UI". That claim was false. The whole control lived in
 * displayBody() in the STUDENT'S OWN React bundle, and it keyed on `type` — a
 * field the sender writes. Three paths defeated it:
 *
 *   1. type laundering — write type:'study-insight' (not staff-originated) and
 *      `body` rendered verbatim;
 *   2. `title` was rendered raw for every type, never consulting any table;
 *   3. `fromGCName` was rendered raw, and is settable to 50 characters of prose
 *      through the UI alone by renaming yourself.
 *
 * The enabling rule allowed any same-school staff account to create/update
 * /notifications/{studentUid} with NO field validation at all.
 *
 * Firestore rules cannot fix this: the document is a single `items` array and
 * rules cannot iterate arrays. So staff writes are denied at the rules layer
 * and routed through sendStaffNotification instead, which builds every field
 * here, server-side, from an id. The student's client is no longer where the
 * safeguarding decision is made.
 *
 * Keep the ids in step with data/staffEncouragement.ts (client display copy).
 * A student renders text from that table; this file decides what may be sent.
 * A message id present here but missing there renders as a neutral fallback —
 * safe by construction, since the fallback contains no sender-supplied text.
 */

/** Kinds of message staff may send. Anything else is rejected. */
export const STAFF_MESSAGE_KINDS = ["encouragement", "recommendation", "broadcast"] as const;
export type StaffMessageKind = (typeof STAFF_MESSAGE_KINDS)[number];

/** Preset ids for "Send Encouragement". Mirrors STAFF_ENCOURAGEMENT. */
export const ENCOURAGEMENT_IDS = ["se1", "se2", "se3", "se4", "se5", "se6", "se7", "se8"];

/** Preset ids for the optional note on a tool recommendation. */
export const RECOMMENDATION_NOTE_IDS = ["sr1", "sr2", "sr3", "sr4", "sr5"];

/**
 * Preset ids for a whole-year broadcast.
 *
 * Broadcasts were the one staff→student channel still carrying free text after
 * 6b30f259, and because 'gc-broadcast' counts as staff-originated the student
 * client had already stopped rendering that text — so every broadcast sent
 * since then displayed as the neutral fallback and no student saw the message.
 * Presets close the hole and un-break the feature at the same time.
 */
export const BROADCAST_IDS = ["sb1", "sb2", "sb3", "sb4", "sb5", "sb6"];

/** Titles are generated here too — they used to be free text rendered raw. */
const TITLES: Record<StaffMessageKind, string> = {
  encouragement: "Words of encouragement",
  recommendation: "A tool your school suggests",
  broadcast: "Message from your school",
};

const ALLOWED_IDS: Record<StaffMessageKind, string[]> = {
  encouragement: ENCOURAGEMENT_IDS,
  recommendation: RECOMMENDATION_NOTE_IDS,
  broadcast: BROADCAST_IDS,
};

/** The notification type each kind maps to, matching NotificationType. */
const TYPES: Record<StaffMessageKind, string> = {
  encouragement: "gc-kudos",
  recommendation: "gc-recommendation",
  broadcast: "gc-broadcast",
};

export type StaffMessageCheck =
  | { ok: true; kind: StaffMessageKind; messageId: string; title: string; type: string }
  | { ok: false; reason: "kind" | "messageId" };

/**
 * Validate a requested staff message and return every field the notification
 * will carry. Nothing the caller sends becomes display text — they choose from
 * a menu, and the server writes the words.
 */
export function checkStaffMessage(kind: unknown, messageId: unknown): StaffMessageCheck {
  if (typeof kind !== "string" || !(STAFF_MESSAGE_KINDS as readonly string[]).includes(kind)) {
    return { ok: false, reason: "kind" };
  }
  const validKind = kind as StaffMessageKind;
  // A recommendation's note is optional — the tool name alone is a valid message.
  if (validKind === "recommendation" && (messageId === undefined || messageId === null || messageId === "")) {
    return { ok: true, kind: validKind, messageId: "", title: TITLES[validKind], type: TYPES[validKind] };
  }
  if (typeof messageId !== "string" || !ALLOWED_IDS[validKind].includes(messageId)) {
    return { ok: false, reason: "messageId" };
  }
  return { ok: true, kind: validKind, messageId, title: TITLES[validKind], type: TYPES[validKind] };
}
