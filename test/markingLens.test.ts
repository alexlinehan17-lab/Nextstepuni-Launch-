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
 *  5. Booklet-safety: when the same n is tagged under more than one booklet
 *     (dual-booklet / dual-numbering papers), a lens for that n could silently
 *     point at the WRONG booklet's question — the exact geography Part One/Part
 *     Two miskey caught pre-ship 2026-07. Gate 5 forces every ambiguous booklet
 *     a lens uses onto an explicit verified list, so the "which booklet does this
 *     n belong to" check is done consciously, not assumed.
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

  // Booklets a human has verified carry the questions their lens describes, for
  // papers where the same n is tagged under more than one booklet. Adding a
  // booklet here is an explicit statement: "I checked which booklet each n is on."
  // (Geography 2024 HL / 2025 OL: LP042 = Part One shorts, NOT LP043 = Part Two.
  //  Biology 2025: LP038 = Sections A+B Q1–10, LP040 = Section C Q11–17.
  //  Business: LP032 = Section 1 (12 short questions), LP041 = Section 2 (applied
  //  long questions, n1–8); the golden file keys shorts→LP032, longs→LP041.)
  const VERIFIED_AMBIGUOUS_BOOKLETS = new Set<string>([
    'business|LC033ALP032EV.pdf', 'business|LC033ALP041EV.pdf', 'business|LC033ALP041IV.pdf',
    'business|LC033GLP033EV.pdf', 'business|LC033GLP033IV.pdf',
    'biology|LC025ALP038EV.pdf', 'biology|LC025ALP040EV.pdf',
    'biology|LC025ALP038IV.pdf', 'biology|LC025ALP040IV.pdf',
    'biology|LC025GLP038EV.pdf', 'biology|LC025GLP040EV.pdf',
    'biology|LC025GLP038IV.pdf', 'biology|LC025GLP040IV.pdf',
    'geography|LC005ALP042EV.pdf', 'geography|LC005ALP042IV.pdf',
    'geography|LC005GLP042EV.pdf',
    // DCG: LP014 is the separately printed Section-A sheet (A1–A4), while
    // LP039 is the Section-B/C answer booklet (B1–B3 and C1–C5). The shipped
    // lenses below are verified against LP039; adding Section A to Atlas makes
    // n1–4 deliberately ambiguous across the two physical documents.
    'design-and-communication-graphics|LC562ALP039EV.pdf',
    'design-and-communication-graphics|LC562ALP039IV.pdf',
    // Home Economics: LP014 = Section A (14 short questions, 6 marks each),
    // LP039 = Section B (long questions, Q1=80 / Q2–5=50). They share n1–5.
    'home-economics-s-and-s|LC098ALP014EV.pdf', 'home-economics-s-and-s|LC098ALP039EV.pdf',
    'home-economics-s-and-s|LC098ALP014IV.pdf', 'home-economics-s-and-s|LC098ALP039IV.pdf',
    'home-economics-s-and-s|LC098GLP014EV.pdf', 'home-economics-s-and-s|LC098GLP039EV.pdf',
    'home-economics-s-and-s|LC098GLP014IV.pdf', 'home-economics-s-and-s|LC098GLP039IV.pdf',
  ]);

  it('booklet-ambiguous entries use only explicitly verified booklets', () => {
    // (subjectId|year|level|lang|n) -> set of fileids that tag it.
    const fileidsForN = new Map<string, Set<string>>();
    for (const p of PAPER_TOPIC_TAGS) {
      for (const q of p.q) {
        const k = `${p.subjectId}|${p.year}|${p.level}|${p.lang}|${q.n}`;
        let set = fileidsForN.get(k);
        if (!set) { set = new Set(); fileidsForN.set(k, set); }
        set.add(p.fileid);
      }
    }
    const unverified = new Set<string>();
    for (const s of MARKING_LENS) {
      for (const e of s.entries) {
        const fileids = fileidsForN.get(`${s.subjectId}|${e.year}|${e.level}|${e.lang}|${e.n}`);
        if (fileids && fileids.size > 1) {
          const bk = `${s.subjectId}|${e.fileid}`;
          if (!VERIFIED_AMBIGUOUS_BOOKLETS.has(bk)) {
            unverified.add(`${bk} (n${e.n} also tagged on: ${[...fileids].filter(f => f !== e.fileid).join(', ')})`);
          }
        }
      }
    }
    expect([...unverified]).toEqual([]);
  });

  it('lensFor resolves a real key and misses an unknown one', () => {
    const s = MARKING_LENS[0];
    const e = s.entries[0];
    expect(lensFor({ subjectId: s.subjectId, ...e })).toBe(e);
    expect(lensFor({ subjectId: 'nope', year: 1990, level: 'higher', lang: 'ev', fileid: 'x.pdf', n: '1' })).toBeNull();
  });
});
