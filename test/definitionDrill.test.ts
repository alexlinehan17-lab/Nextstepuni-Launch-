/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Definition Drill — integrity gates. Definition Drill is a read-only projection
 * of the Marking Lens corpus (data/markingLens), keeping only parts that are a
 * definition prompt AND whose decoded field carries the scheme's real
 * mark-earning WORDING. These gates guard the projection:
 *   1. Non-empty; every definition traces to a real Marking Lens part.
 *   2. THE ACCREDITATION GATE — no `answer` is a mark-split description: every
 *      answer carries actual wording, not just how the marks divide. A drill card
 *      whose reveal is "the explanation earns 2 marks" would teach nothing and
 *      invites invention; it must never ship.
 *   3. Prompt/term non-empty; marks > 0.
 *   4. Every source is SEC-attributed.
 *   5. Ids unique; subject counts reconcile.
 */
import { describe, it, expect } from 'vitest';
import { DRILL_DEFINITIONS, drillSubjects, definitionsForSubject } from '../data/definitionDrill';
import { MARKING_LENS } from '../data/markingLens';

// A real Marking Lens part key set: subjectId|year|level|lang|fileid|n|partIndex.
const partKeys = new Set<string>();
for (const s of MARKING_LENS) {
  for (const e of s.entries) {
    e.parts.forEach((_p, i) => partKeys.add(`${s.subjectId}|${e.year}|${e.level}|${e.lang}|${e.fileid}|${e.n}|${i}`));
  }
}

// The shapes an answer must NEVER have — a mark-split description with no wording.
const MARK_SPLIT_SHAPES = [
  /\bearns?\s+\d+\s+marks?\b/i,
  /^correct answer\b/i,
  /\bpart\s*\(i+\)\s*:/i,
  /\bexample\s+\d/i,
  /\bworth\s+\d/i,
  /\bstate\s*\(\d.*develop\s*\(\d/i,
  /\bfor\s+(the|its)\s+(explanation|development)\b/i,
  /\d-mark elements?\s+of\s+the\b/i,
  /^three elements\b/i,
  /\bboth terms treated\b/i,
];

describe('Definition Drill integrity', () => {
  it('has definitions to check', () => {
    expect(DRILL_DEFINITIONS.length).toBeGreaterThan(0);
  });

  it('every definition traces to a real Marking Lens part', () => {
    const orphans = DRILL_DEFINITIONS.filter(d => !partKeys.has(d.id)).map(d => d.id);
    expect(orphans).toEqual([]);
  });

  it('no answer is a mark-split description — every reveal carries real wording', () => {
    const bad: string[] = [];
    for (const d of DRILL_DEFINITIONS) {
      if (MARK_SPLIT_SHAPES.some(re => re.test(d.answer.trim()))) bad.push(`${d.id}: "${d.answer}"`);
      // strip mark tags; a genuine definition still has substantive wording left
      const core = d.answer.replace(/\(\d+\s*m\)/gi, '').trim();
      if (core.length < 12) bad.push(`${d.id}: wording too thin ("${d.answer}")`);
    }
    expect(bad).toEqual([]);
  });

  it('prompt and term are non-empty and marks are positive', () => {
    const bad: string[] = [];
    for (const d of DRILL_DEFINITIONS) {
      if (d.prompt.trim().length < 3) bad.push(`${d.id}: empty prompt`);
      if (d.term.trim().length < 2) bad.push(`${d.id}: empty term`);
      if (d.marks <= 0) bad.push(`${d.id}: non-positive marks`);
    }
    expect(bad).toEqual([]);
  });

  it('every source is SEC-attributed', () => {
    const bad = DRILL_DEFINITIONS.filter(d => !/State Examinations Commission|SEC Marking Scheme/i.test(d.source)).map(d => d.id);
    expect(bad).toEqual([]);
  });

  it('ids are unique', () => {
    const seen = new Set<string>();
    for (const d of DRILL_DEFINITIONS) {
      expect(seen.has(d.id), `duplicate id ${d.id}`).toBe(false);
      seen.add(d.id);
    }
  });

  it('subject counts reconcile with the definition list', () => {
    const subs = drillSubjects();
    const total = subs.reduce((a, s) => a + s.count, 0);
    expect(total).toBe(DRILL_DEFINITIONS.length);
    for (const s of subs) expect(definitionsForSubject(s.id).length).toBe(s.count);
  });
});
