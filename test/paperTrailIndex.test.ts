/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail index integrity — guards the generated paperTrailData.ts the
 * same way syllabusSourceOfTruth guards curriculum overlays. Shape-based, not
 * count-based, so it passes on a partial harvest and keeps passing on the
 * full corpus; anything count-sensitive (e.g. "JC subjects exist") lives in
 * jcToolVisibility.test.ts instead.
 */

import { describe, it, expect } from 'vitest';
import { CURRICULUM } from '../curriculum';
import {
  PAPER_TRAIL_GAPS,
  PAPER_TRAIL_INDEX,
  PAPER_TRAIL_SUBJECTS,
} from '../paperTrailData';

const VALID_LEVELS = new Set(['higher', 'ordinary', 'foundation', 'common']);
const VALID_CYCLES = new Set(['lc', 'jc', 'lca']);
const subjectIds = new Set(PAPER_TRAIL_SUBJECTS.map(s => s.id));
const curriculumIds = new Set(CURRICULUM.map(s => s.id));

describe('Paper Trail subject registry', () => {
  it('subject ids are unique, kebab-case, and cycle-prefixed correctly', () => {
    expect(subjectIds.size).toBe(PAPER_TRAIL_SUBJECTS.length);
    for (const s of PAPER_TRAIL_SUBJECTS) {
      expect(s.id, s.id).toMatch(/^[a-z0-9-]+$/);
      expect(VALID_CYCLES.has(s.cycle), `${s.id} cycle`).toBe(true);
      if (s.cycle === 'jc') expect(s.id, `${s.id} should be jc- prefixed`).toMatch(/^jc-/);
      if (s.cycle === 'lca') expect(s.id, `${s.id} should be lca- prefixed`).toMatch(/^lca-/);
      if (s.cycle === 'lc') expect(s.id).not.toMatch(/^(jc|lca)-/);
    }
  });

  it('declared levels are valid and non-empty', () => {
    for (const s of PAPER_TRAIL_SUBJECTS) {
      expect(s.levels.length, `${s.id} levels`).toBeGreaterThan(0);
      s.levels.forEach(lv => expect(VALID_LEVELS.has(lv), `${s.id}: ${lv}`).toBe(true));
    }
  });

  it('curriculumId links point at real curriculum subjects', () => {
    for (const s of PAPER_TRAIL_SUBJECTS) {
      if (s.curriculumId) {
        expect(curriculumIds.has(s.curriculumId), `${s.id} → ${s.curriculumId}`).toBe(true);
      }
    }
  });
});

describe('Paper Trail index entries', () => {
  it('indexes the complete 2026 Geography paper and companion set', () => {
    const entries = PAPER_TRAIL_INDEX.geography.filter(entry =>
      entry.year === 2026 && entry.lang === 'ev');
    const byLevel = new Map(entries.map(entry => [entry.level, entry]));

    expect(byLevel.get('higher')?.papers.map(paper => [
      paper.label, paper.doc.f, paper.scheme?.f,
    ])).toEqual([
      ['Part 1', 'LC005ALP042EV.pdf', 'LC005ALP000EV.pdf'],
      ['Part 2', 'LC005ALP043EV.pdf', 'LC005ALP000EV.pdf'],
    ]);
    expect(byLevel.get('ordinary')?.papers.map(paper => [
      paper.label, paper.doc.f, paper.scheme?.f,
    ])).toEqual([
      ['Part 1', 'LC005GLP042EV.pdf', 'LC005GLP000EV.pdf'],
      ['Part 2', 'LC005GLP043EV.pdf', 'LC005GLP000EV.pdf'],
    ]);
    expect(byLevel.get('common')?.papers.map(paper => [
      paper.label, paper.doc.f,
    ])).toEqual([
      ['Ordnance Survey Map', 'LC005CLPC00EV.pdf'],
      ['Map Legend', 'LC005CLP003EV.pdf'],
      ['Aerial Photograph', 'LC005CLP004EV.pdf'],
    ]);
  });

  it('every index key is a registered subject, and vice versa', () => {
    for (const id of Object.keys(PAPER_TRAIL_INDEX)) {
      expect(subjectIds.has(id), `index key ${id}`).toBe(true);
    }
    for (const s of PAPER_TRAIL_SUBJECTS) {
      const entries = PAPER_TRAIL_INDEX[s.id];
      expect(entries, `registry subject ${s.id} has index entries`).toBeTruthy();
      expect(entries.length, `${s.id} entry count`).toBeGreaterThan(0);
    }
  });

  it('entries are well-formed: sane years, declared levels, valid docs', () => {
    for (const [id, entries] of Object.entries(PAPER_TRAIL_INDEX)) {
      const subj = PAPER_TRAIL_SUBJECTS.find(s => s.id === id)!;
      for (const e of entries) {
        expect(e.year, `${id} year`).toBeGreaterThanOrEqual(2010);
        expect(e.year, `${id} year`).toBeLessThanOrEqual(2026);
        expect(subj.levels.includes(e.level), `${id} ${e.year}: level ${e.level} not declared`).toBe(true);
        expect(['ev', 'iv'].includes(e.lang), `${id} ${e.year} lang`).toBe(true);
        expect(e.papers.length, `${id} ${e.year} ${e.level} ${e.lang} has papers`).toBeGreaterThan(0);
        for (const p of e.papers) {
          // Docs are PDFs, or the image supplements (Geography-family aerial
          // photo / map sheets) that build-index normalises to lowercase .jpg.
          expect(p.doc.f, `${id} ${e.year} fileid`).toMatch(/\.(pdf|jpg)$/i);
          expect(p.label.length, `${id} ${e.year} label`).toBeGreaterThan(0);
          // Schemes are always PDFs — an image never carries a marking scheme.
          if (p.scheme) expect(p.scheme.f).toMatch(/\.pdf$/i);
          if (/\.jpg$/i.test(p.doc.f)) {
            expect(p.doc.f, `${id} ${e.year}: image fileids are normalised lowercase .jpg`).toMatch(/\.jpg$/);
            expect(p.scheme, `${id} ${e.year}: image supplement with a scheme`).toBeUndefined();
          }
        }
      }
    }
  });

  it('JC entries respect the new-spec floor (no old-spec years)', () => {
    const NEW_SPEC_FLOOR: Record<string, number> = {
      'jc-english': 2017,
      'jc-science': 2019,
      'jc-business-studies': 2019,
    };
    for (const [id, entries] of Object.entries(PAPER_TRAIL_INDEX)) {
      if (!id.startsWith('jc-')) continue;
      const floor = NEW_SPEC_FLOOR[id] ?? 2022;
      for (const e of entries) {
        expect(e.year, `${id} ${e.year} below new-spec floor`).toBeGreaterThanOrEqual(floor);
        expect([2020, 2021].includes(e.year), `${id} ${e.year}: JC exams were cancelled`).toBe(false);
      }
    }
  });

  it('gaps reference registered subjects with non-empty reasons', () => {
    for (const g of PAPER_TRAIL_GAPS) {
      expect(subjectIds.has(g.subjectId), `gap subject ${g.subjectId}`).toBe(true);
      expect(g.reason.length, 'gap reason').toBeGreaterThan(10);
    }
  });
});
