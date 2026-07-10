/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Answer Architect — integrity gates. Answer Architect is a read-only projection
 * of the Marking Lens corpus (data/markingLens), whose own gate
 * (test/markingLens.test.ts) already proves every entry is a real tagged SEC
 * question whose parts sum honestly. These gates guard the PROJECTION:
 *   1. Non-empty, and every skeleton traces back to a real lens entry.
 *   2. Beats reconcile — they sum to totalMarks (catches a dropped/duped part).
 *   3. Beat ordering is dense and 1-based.
 *   4. Every skeleton is genuinely multi-beat (structure, not a mark-ladder).
 *   5. Every source is SEC-attributed; every pitfall carries an examiner cite.
 *   6. Ids unique; subject counts reconcile.
 * A skeleton that doesn't sum, or that shows an answer shape with no exam
 * source, is exactly the kind of unmoored claim the accreditation rule forbids.
 */
import { describe, it, expect } from 'vitest';
import { ANSWER_SKELETONS, architectSubjects, skeletonsForSubject } from '../data/answerArchitect';
import { MARKING_LENS } from '../data/markingLens';

const lensKeys = new Set<string>();
for (const s of MARKING_LENS) {
  for (const e of s.entries) {
    lensKeys.add(`${s.subjectId}|${e.year}|${e.level}|${e.lang}|${e.fileid}|${e.n}`);
  }
}

describe('Answer Architect integrity', () => {
  it('has skeletons to check', () => {
    expect(ANSWER_SKELETONS.length).toBeGreaterThan(0);
  });

  it('every skeleton traces to a real Marking Lens entry', () => {
    const orphans = ANSWER_SKELETONS.filter(s => !lensKeys.has(s.id)).map(s => s.id);
    expect(orphans).toEqual([]);
  });

  it('beats reconcile with totalMarks', () => {
    const bad: string[] = [];
    for (const s of ANSWER_SKELETONS) {
      const sum = s.beats.reduce((a, b) => a + b.marks, 0);
      if (sum !== s.totalMarks) bad.push(`${s.id}: beats sum ${sum} != totalMarks ${s.totalMarks}`);
    }
    expect(bad).toEqual([]);
  });

  it('beat ordering is dense and 1-based', () => {
    const bad: string[] = [];
    for (const s of ANSWER_SKELETONS) {
      const orders = s.beats.map(b => b.order);
      const expected = s.beats.map((_, i) => i + 1);
      if (JSON.stringify(orders) !== JSON.stringify(expected)) bad.push(s.id);
    }
    expect(bad).toEqual([]);
  });

  it('every skeleton is genuinely multi-beat', () => {
    const thin = ANSWER_SKELETONS.filter(s => s.beats.length < 2).map(s => s.id);
    expect(thin).toEqual([]);
  });

  it('every source is SEC-attributed and every beat carries content', () => {
    const bad: string[] = [];
    for (const s of ANSWER_SKELETONS) {
      if (!/State Examinations Commission|SEC Marking Scheme/i.test(s.source)) bad.push(`${s.id}: source not SEC-attributed`);
      if (s.structure.trim().length < 10) bad.push(`${s.id}: structure too short`);
      for (const b of s.beats) {
        if (b.requirement.trim().length < 3) bad.push(`${s.id} beat ${b.order}: empty requirement`);
        if (b.earns.trim().length < 3) bad.push(`${s.id} beat ${b.order}: empty earns`);
        if (b.marks <= 0) bad.push(`${s.id} beat ${b.order}: non-positive marks`);
      }
      if (s.pitfall && !/Report|Marking Scheme/i.test(s.pitfall.cite)) bad.push(`${s.id}: pitfall cite not SEC-attributed`);
    }
    expect(bad).toEqual([]);
  });

  it('ids are unique', () => {
    const seen = new Set<string>();
    for (const s of ANSWER_SKELETONS) {
      expect(seen.has(s.id), `duplicate id ${s.id}`).toBe(false);
      seen.add(s.id);
    }
  });

  it('subject counts reconcile with the skeleton list', () => {
    const subs = architectSubjects();
    const total = subs.reduce((a, s) => a + s.count, 0);
    expect(total).toBe(ANSWER_SKELETONS.length);
    for (const s of subs) {
      expect(skeletonsForSubject(s.id).length).toBe(s.count);
    }
  });
});
