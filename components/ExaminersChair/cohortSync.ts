/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — cross-device cohort sync (Firestore).
 *
 * The pure aggregation lives in ./store (aggregateCohort / topCohortMisses),
 * which is unit-tested and localStorage-backed for the single-device case.
 * This module is the thin network layer that makes "62% of your class
 * mis-marks this rule" work across a real classroom: students write their
 * anonymised blind-spots to a class code, the teacher view subscribes.
 *
 * Storage shape (bounded, validated-increment counter pattern):
 *   chairCohorts/{classCode}                 → { submissions }
 *   chairCohorts/{classCode}/rules/{ruleId}  → { key, subject, label, over, under, students }
 *
 * ONLY aggregate counts are stored — no names, no uids — so the collection
 * carries no personal data (anonymous by construction). Per-rule counts use
 * FieldValue.increment for atomic, race-free writes; the rules subcollection
 * (one doc per rule) sidesteps Firestore's field-path restrictions on the
 * arbitrary "subject::label" rule keys.
 */

import {
  collection,
  doc,
  getDocs,
  onSnapshot,
  query,
  where,
} from 'firebase/firestore';
import { getFunctions, httpsCallable } from 'firebase/functions';
import app, { db } from '../../firebase';
import type { CohortAgg, CohortRule, MissDelta } from './store';

const codeId = (code: string) => code.trim().toLowerCase();

const cohortDoc = (code: string) => doc(db, 'chairCohorts', codeId(code));
const rulesCol = (code: string) => collection(db, 'chairCohorts', codeId(code), 'rules');

/** Write one student's session blind-spots to a class code (best-effort).
 * Silent on failure — the local aggregate is the offline fallback. */
export async function submitToCohortRemote(code: string, deltas: MissDelta[]): Promise<void> {
  const c = code.trim();
  if (!c) return;
  try {
    const submit = httpsCallable<{ code: string; deltas: MissDelta[] }, { success: boolean }>(
      getFunctions(app),
      'submitChairCohort',
    );
    await submit({ code: c, deltas });
  } catch (err) {
    console.error('[Chair] cohort submit failed:', err);
  }
}

// ── Moderation Meeting (F5): anonymous per-decision class distribution ──
//
// One counter doc per (session, script, choice). Grid choices are
// "attemptId:criterionId:earned|withheld"; scale choices are the level id.
// Written only as part of the student's explicit "Send to class" action;
// read on the reveal so the class before you becomes your conference.

export interface DecisionDelta {
  sessionId: string;
  scriptId: string;
  choice: string;
}

const decisionsCol = (code: string) => collection(db, 'chairCohorts', codeId(code), 'decisions');

/** Increment the class counters for one session's marking decisions (best-effort). */
export async function submitDecisions(code: string, deltas: DecisionDelta[]): Promise<void> {
  const c = code.trim();
  if (!c || deltas.length === 0) return;
  try {
    const submit = httpsCallable<{ code: string; deltas: DecisionDelta[] }, { success: boolean }>(
      getFunctions(app),
      'submitChairDecisions',
    );
    await submit({ code: c, deltas });
  } catch (err) {
    console.error('[Chair] decision submit failed:', err);
  }
}

/** One script's class distribution: choice → count. Empty map on any failure. */
export async function fetchScriptDistribution(
  code: string,
  sessionId: string,
  scriptId: string,
): Promise<Record<string, number>> {
  const c = code.trim();
  if (!c) return {};
  try {
    const snap = await getDocs(
      query(decisionsCol(c), where('sessionId', '==', sessionId), where('scriptId', '==', scriptId)),
    );
    const out: Record<string, number> = {};
    snap.forEach(d => {
      const data = d.data() as Partial<DecisionDelta> & { n?: number };
      if (data.choice) out[data.choice] = data.n ?? 0;
    });
    return out;
  } catch {
    return {};
  }
}

// ── Daily Mark duel (F9): anonymous agreement histogram per class + day ──
//
// One counter doc per (day, decile bucket 0–10). "You 9/10, class median 6."

const dailyCol = (code: string) => collection(db, 'chairCohorts', codeId(code), 'daily');

/** Add one submission to the class histogram for the day (best-effort). */
export async function submitDailyBucket(code: string, day: string, bucket: number): Promise<void> {
  const c = code.trim();
  const b = Math.max(0, Math.min(10, Math.round(bucket)));
  if (!c || !day) return;
  try {
    const submit = httpsCallable<{ code: string; day: string; bucket: number }, { success: boolean }>(
      getFunctions(app),
      'submitChairDaily',
    );
    await submit({ code: c, day, bucket: b });
  } catch (err) {
    console.error('[Chair] daily duel submit failed:', err);
  }
}

/** The day's histogram as an 11-slot array (bucket 0–10 → count). */
export async function fetchDailyHistogram(code: string, day: string): Promise<number[]> {
  const c = code.trim();
  const out = new Array<number>(11).fill(0);
  if (!c || !day) return out;
  try {
    const snap = await getDocs(query(dailyCol(c), where('day', '==', day)));
    snap.forEach(d => {
      const data = d.data() as { bucket?: number; n?: number };
      if (typeof data.bucket === 'number' && data.bucket >= 0 && data.bucket <= 10) {
        out[data.bucket] = data.n ?? 0;
      }
    });
    return out;
  } catch {
    return out;
  }
}

/** Class median agreement (0–10) from a histogram, or null when empty. */
export function histogramMedian(hist: number[]): number | null {
  const total = hist.reduce((a, b) => a + b, 0);
  if (total === 0) return null;
  let seen = 0;
  for (let b = 0; b < hist.length; b++) {
    seen += hist[b];
    if (seen * 2 >= total) return b;
  }
  return null;
}

/** Live-subscribe to a class code's aggregate. Calls back with the current
 * CohortAgg whenever the parent doc or any rule changes. Returns an
 * unsubscribe. Permission / network errors resolve to an empty aggregate. */
export function subscribeCohort(code: string, cb: (agg: CohortAgg) => void): () => void {
  const c = code.trim();
  if (!c) { cb({ submissions: 0, rules: {} }); return () => {}; }
  try {
    return subscribeCohortInner(c, cb);
  } catch {
    // A broken Firestore handle must never take the teacher view down —
    // the local aggregate remains the fallback.
    cb({ submissions: 0, rules: {} });
    return () => {};
  }
}

function subscribeCohortInner(c: string, cb: (agg: CohortAgg) => void): () => void {
  let submissions = 0;
  let rules: Record<string, CohortRule> = {};
  const emit = () => cb({ submissions, rules });

  const unsubDoc = onSnapshot(
    cohortDoc(c),
    snap => {
      submissions = (snap.exists() ? (snap.data().submissions as number) : 0) || 0;
      emit();
    },
    () => {},
  );
  const unsubRules = onSnapshot(
    rulesCol(c),
    snap => {
      const next: Record<string, CohortRule> = {};
      snap.forEach(d => {
        const data = d.data() as Partial<CohortRule>;
        if (!data.key) return;
        next[data.key] = {
          key: data.key,
          subject: data.subject as CohortRule['subject'],
          label: data.label ?? '',
          over: data.over ?? 0,
          under: data.under ?? 0,
          students: data.students ?? 0,
        };
      });
      rules = next;
      emit();
    },
    () => {},
  );

  return () => { unsubDoc(); unsubRules(); };
}
