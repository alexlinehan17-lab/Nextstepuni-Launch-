/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Assignments (feature E9) — a guidance counsellor sets a revision task for their
 * school; students see it and mark it done. The task DEFINITION lives in a
 * per-school doc (`assignments/{school}`) the GC writes and students read (same
 * rule shape as gcEvents). Student COMPLETION is recorded in the student's own
 * `progress` doc (self-write the GC can already read) — so no student write to
 * the shared doc is needed.
 *
 * SHIP-GATED. `ASSIGNMENTS_LIVE` is false until the Firestore rule for the
 * `assignments/{school}` collection has been deployed and the student surface is
 * wired with the student's school. See compliance/assignments-plan.md. The pure
 * status helpers below are always safe to use and unit-tested.
 */

import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';

/** Master switch. Keep false until the assignments rule is deployed. */
export const ASSIGNMENTS_LIVE = false;

export type AssignmentKind = 'topic' | 'mock' | 'pack' | 'module' | 'general';

export interface Assignment {
  id: string;
  title: string;
  kind: AssignmentKind;
  /** Optional reference (a topic id, subject id, or module id per kind). */
  ref?: string;
  /** ISO due date (YYYY-MM-DD). */
  dueIso?: string;
  createdTs: number;
  createdByName?: string;
}

export type AssignmentStatus = 'done' | 'overdue' | 'open';

/** Pure: an assignment's status for a student. `todayIso` is YYYY-MM-DD so ISO
 *  date strings compare lexicographically. */
export function assignmentStatus(a: Assignment, completedTs: number | undefined, todayIso: string): AssignmentStatus {
  if (completedTs) return 'done';
  if (a.dueIso && a.dueIso < todayIso) return 'overdue';
  return 'open';
}

/** Count open / overdue / done across a set for a student's completion map. */
export function summariseAssignments(
  items: Assignment[],
  completions: Record<string, number>,
  todayIso: string,
): { open: number; overdue: number; done: number } {
  const out = { open: 0, overdue: 0, done: 0 };
  for (const a of items) out[assignmentStatus(a, completions[a.id], todayIso)] += 1;
  return out;
}

// ─── Firestore accessors (only invoked when ASSIGNMENTS_LIVE) ────────────────

export async function loadAssignments(school: string): Promise<Assignment[]> {
  try {
    const snap = await getDoc(doc(db, 'assignments', school));
    return snap.exists() ? ((snap.data().items as Assignment[]) ?? []) : [];
  } catch {
    return [];
  }
}

/** GC-only: write the school's full assignment list. */
export function saveAssignments(school: string, items: Assignment[]): Promise<void> {
  // Returns the write promise WITHOUT awaiting or swallowing. Awaiting here
  // would hang offline (a write settles only on server ack), and the empty
  // catch silently ate rules rejections — which made the caller's rollback
  // dead code. The caller decides: saveInBackground() or awaitWriteOrTimeout().
  return setDoc(doc(db, 'assignments', school), { items });
}

/** Student marks an assignment done in their own progress doc (self-write). */
export function markAssignmentComplete(uid: string, assignmentId: string, now: number): Promise<void> {
  return setDoc(doc(db, 'progress', uid), { assignmentCompletions: { [assignmentId]: now } }, { merge: true });
}
