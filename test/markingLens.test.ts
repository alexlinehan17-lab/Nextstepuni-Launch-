/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — integrity gates. The lens shows students exactly how the SEC
 * scheme allocates marks, so a wrong breakdown is as bad as a wrong crop.
 * These gates are the machine-checked half of the honesty rules in
 * data/markingLens/types.ts:
 *
 *  1. Every entry keys to a REAL Topic Vault question (its paper is tagged and
 *     its n is one of that paper's tagged questions) — no orphan lenses.
 *  2. The parts of every entry sum EXACTLY to its totalMarks — a ladder that
 *     doesn't add up misstates the scheme.
 *  3. Every entry cites its scheme; every pitfall cites its report.
 *  4. No duplicate keys.
 */

import { describe, it, expect } from 'vitest';
import { MARKING_LENS, lensFor } from '../data/markingLens';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';

const tagKey = (subjectId: string, year: number, level: string, lang: string, fileid: string) =>
  `${subjectId}|${year}|${level}|${lang}|${fileid}`;

const taggedNs = new Map<string, Set<string>>();
for (const p of PAPER_TOPIC_TAGS) {
  taggedNs.set(tagKey(p.subjectId, p.year, p.level, p.lang, p.fileid), new Set(p.q.map(q => q.n)));
}

describe('Marking Lens integrity', () => {
  it('there are lens entries to check', () => {
    expect(MARKING_LENS.length).toBeGreaterThan(0);
    expect(MARKING_LENS.flatMap(s => s.entries).length).toBeGreaterThan(0);
  });

  it('every entry keys to a real tagged Topic Vault question', () => {
    const orphans: string[] = [];
    for (const s of MARKING_LENS) {
      for (const e of s.entries) {
        const ns = taggedNs.get(tagKey(s.subjectId, e.year, e.level, e.lang, e.fileid));
        if (!ns) orphans.push(`${s.subjectId} ${e.year} ${e.fileid}: paper not tagged`);
        else if (!ns.has(e.n)) orphans.push(`${s.subjectId} ${e.year} ${e.fileid} Q${e.n}: n not tagged`);
      }
    }
    expect(orphans).toEqual([]);
  });

  it('every entry’s parts sum exactly to its totalMarks', () => {
    const bad: string[] = [];
    for (const s of MARKING_LENS) {
      for (const e of s.entries) {
        const sum = e.parts.reduce((a, p) => a + p.marks, 0);
        if (sum !== e.totalMarks) bad.push(`${s.subjectId} ${e.year} ${e.fileid} Q${e.n}: parts sum ${sum} ≠ ${e.totalMarks}`);
      }
    }
    expect(bad).toEqual([]);
  });

  it('every entry is fully sourced and non-empty', () => {
    for (const s of MARKING_LENS) {
      for (const e of s.entries) {
        const id = `${s.subjectId} ${e.year} Q${e.n}`;
        expect(e.cite.trim().length, `${id} cite`).toBeGreaterThan(10);
        expect(e.headline.trim().length, `${id} headline`).toBeGreaterThan(10);
        expect(e.parts.length, `${id} parts`).toBeGreaterThan(0);
        for (const p of e.parts) {
          expect(p.task.trim().length, `${id} task`).toBeGreaterThan(0);
          expect(p.notation.trim().length, `${id} notation`).toBeGreaterThan(0);
          expect(p.decoded.trim().length, `${id} decoded`).toBeGreaterThan(0);
          expect(p.marks, `${id} marks`).toBeGreaterThan(0);
        }
        if (e.pitfall) {
          expect(e.pitfall.text.trim().length, `${id} pitfall text`).toBeGreaterThan(10);
          expect(e.pitfall.cite, `${id} pitfall cite`).toMatch(/Report|Marking Scheme/i);
        }
      }
    }
  });

  it('keys are unique', () => {
    const seen = new Set<string>();
    for (const s of MARKING_LENS) {
      for (const e of s.entries) {
        const k = `${s.subjectId}|${e.year}|${e.level}|${e.lang}|${e.fileid}|${e.n}`;
        expect(seen.has(k), `duplicate ${k}`).toBe(false);
        seen.add(k);
      }
    }
  });

  it('lensFor resolves a real key and misses an unknown one', () => {
    const s = MARKING_LENS[0];
    const e = s.entries[0];
    expect(lensFor({ subjectId: s.subjectId, ...e })).toBe(e);
    expect(lensFor({ subjectId: 'nope', year: 1990, level: 'higher', lang: 'ev', fileid: 'x.pdf', n: '1' })).toBeNull();
  });
});
