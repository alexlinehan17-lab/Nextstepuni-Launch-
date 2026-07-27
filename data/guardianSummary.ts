/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Weekly guardian summary (feature E10). An opt-in weekly email to a parent or
 * guardian — effort, not grades — a proven, low-bandwidth channel for DEIS
 * homes. Consent (a guardian email + opt-in) is stored in the student's own
 * settings doc (self-write). The actual SEND is a scheduled Cloud Function that
 * reads consent + aggregates each student's week and calls `buildGuardianEmail`;
 * that function and an email provider are the activation step.
 *
 * SHIP-GATED via `GUARDIAN_EMAILS_LIVE` (false) — the consent UI and the send
 * both stay off until the function is deployed. See
 * compliance/guardian-summary-plan.md. The email builder below is pure and
 * unit-tested, and is the exact code the function will reuse.
 */

import { db } from '../firebase';
import { doc, getDoc, setDoc } from 'firebase/firestore';

/** Master switch — keep false until the send function is deployed. */
export const GUARDIAN_EMAILS_LIVE = false;

export interface GuardianConsent {
  /** Parent/guardian email address. */
  email: string;
  /** Whether weekly summaries are switched on. */
  optIn: boolean;
}

export interface GuardianWeekSummary {
  studentName?: string;
  /** Minutes focused this week. */
  weekMinutes: number;
  /** Questions/cards reviewed this week. */
  cardsReviewed: number;
  /** Current practice streak, days. */
  currentStreak: number;
  /** A topic the student is choosing to focus on next (not a grade/ranking). */
  focusTopic?: string;
}

const clean = (s: string) => s.replace(/\s+/g, ' ').trim();

/** Compose the weekly email. Effort-only — never a grade, mark or percentage. */
export function buildGuardianEmail(s: GuardianWeekSummary): { subject: string; text: string } {
  const name = s.studentName?.trim() || 'your student';
  const subject = `${name}'s study week on Nextstepuni`;
  const bits: string[] = [
    `Hi — a quick, encouraging note about ${name}'s week.`,
    s.weekMinutes > 0 ? `They spent ${s.weekMinutes} focused minutes revising` : `They logged some revision this week`,
    s.cardsReviewed > 0 ? `and worked through ${s.cardsReviewed} practice question${s.cardsReviewed === 1 ? '' : 's'}.` : '.',
    s.currentStreak > 1 ? `They're on a ${s.currentStreak}-day practice streak.` : '',
    s.focusTopic ? `Next up, they're focusing on ${s.focusTopic}.` : '',
    `This is about effort, not results — just a sign they've been putting the work in. Nothing to reply to.`,
    `— The Nextstepuni team`,
  ];
  return { subject, text: clean(bits.filter(Boolean).join(' ')) };
}

// ─── consent (student settings doc; only touched when GUARDIAN_EMAILS_LIVE) ──

export async function loadGuardianConsent(uid: string): Promise<GuardianConsent | null> {
  try {
    const snap = await getDoc(doc(db, 'settings', uid));
    const v = snap.exists() ? (snap.data().guardianSummary as GuardianConsent | undefined) : undefined;
    return v ?? null;
  } catch {
    return null;
  }
}

export function saveGuardianConsent(uid: string, consent: GuardianConsent): Promise<void> {
  // See data/assignments.saveAssignments — return the promise, don't await or
  // swallow it. The caller chooses the offline-safe wrapper.
  return setDoc(doc(db, 'settings', uid), { guardianSummary: consent }, { merge: true });
}
