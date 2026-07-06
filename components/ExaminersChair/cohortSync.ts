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
 * Storage shape (mirrors the teachbacks/flares validated-increment pattern):
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
  increment,
  onSnapshot,
  setDoc,
} from 'firebase/firestore';
import { db } from '../../firebase';
import type { CohortAgg, CohortRule, MissDelta } from './store';

const codeId = (code: string) => code.trim().toLowerCase();

const cohortDoc = (code: string) => doc(db, 'chairCohorts', codeId(code));
const rulesCol = (code: string) => collection(db, 'chairCohorts', codeId(code), 'rules');

/** Stable, collision-resistant Firestore doc id for an arbitrary rule key
 * (FNV-1a → base36). The human-readable key/subject/label ride as fields. */
function ruleDocId(key: string): string {
  let h = 0x811c9dc5;
  for (let i = 0; i < key.length; i++) {
    h ^= key.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return 'r' + (h >>> 0).toString(36);
}

/** Collapse a submission's deltas per rule, so each submission counts once per
 * rule (matching aggregateCohort's local behaviour). */
function collapse(deltas: MissDelta[]): MissDelta[] {
  const perRule = new Map<string, MissDelta>();
  for (const d of deltas) {
    const cur = perRule.get(d.key);
    if (cur) { cur.over += d.over; cur.under += d.under; }
    else perRule.set(d.key, { ...d });
  }
  return [...perRule.values()];
}

/** Write one student's session blind-spots to a class code (best-effort).
 * Silent on failure — the local aggregate is the offline fallback. */
export async function submitToCohortRemote(code: string, deltas: MissDelta[]): Promise<void> {
  const c = code.trim();
  if (!c) return;
  try {
    await setDoc(cohortDoc(c), { submissions: increment(1) }, { merge: true });
    await Promise.all(
      collapse(deltas).map(d =>
        setDoc(
          doc(rulesCol(c), ruleDocId(d.key)),
          {
            key: d.key,
            subject: d.subject,
            label: d.label,
            over: increment(d.over),
            under: increment(d.under),
            students: increment(1),
          },
          { merge: true },
        ),
      ),
    );
  } catch (err) {
    console.error('[Chair] cohort submit failed:', err);
  }
}

/** Live-subscribe to a class code's aggregate. Calls back with the current
 * CohortAgg whenever the parent doc or any rule changes. Returns an
 * unsubscribe. Permission / network errors resolve to an empty aggregate. */
export function subscribeCohort(code: string, cb: (agg: CohortAgg) => void): () => void {
  const c = code.trim();
  if (!c) { cb({ submissions: 0, rules: {} }); return () => {}; }

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
