/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail answer-map integrity — guards the committed per-paper answer
 * sidecars (scripts/paper-trail/answers/) and their contract with the generated
 * paperTrailData.ts. Runs in CI WITHOUT the gitignored corpus: it reads only the
 * committed sidecars + the committed index. The deep, corpus-dependent checks
 * (does a region actually contain that question?) live in the Python
 * test_anchor_map.py, run locally where the corpus exists.
 */

import { readFileSync, existsSync, readdirSync } from 'fs';
import path from 'path';
import { describe, it, expect } from 'vitest';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import type { PaperAnswerMap } from '../types/paperTrail';

const ANSWERS_DIR = path.resolve(__dirname, '../scripts/paper-trail/answers');

function allSidecars(): { year: string; file: string; map: PaperAnswerMap }[] {
  if (!existsSync(ANSWERS_DIR)) return [];
  const out: { year: string; file: string; map: PaperAnswerMap }[] = [];
  for (const year of readdirSync(ANSWERS_DIR)) {
    const ydir = path.join(ANSWERS_DIR, year);
    for (const file of readdirSync(ydir)) {
      if (!file.endsWith('.json')) continue;
      out.push({ year, file, map: JSON.parse(readFileSync(path.join(ydir, file), 'utf-8')) });
    }
  }
  return out;
}

const sidecars = allSidecars();

describe('Paper Trail answer sidecars — shape', () => {
  it('there is at least one committed sidecar (pilot present)', () => {
    expect(sidecars.length).toBeGreaterThan(0);
  });

  for (const { year, file, map } of sidecars) {
    it(`${year}/${file} conforms to PaperAnswerMap and stays in-band`, () => {
      expect(map.v, 'schema version').toBe(1);
      expect(typeof map.paperFileid).toBe('string');
      expect(typeof map.schemeFileid).toBe('string');
      expect(map.copyright).toContain('State Examinations Commission');
      // filename is the paper fileid + .json
      expect(`${map.paperFileid}.json`).toBe(file);
      // band is a 1-based half-open [lo, hi)
      const [lo, hi] = map.band;
      expect(Number.isInteger(lo)).toBe(true);
      expect(Number.isInteger(hi)).toBe(true);
      expect(hi).toBeGreaterThan(lo);
      expect(map.q.length).toBeGreaterThan(0);

      const nums = map.q.map(q => Number(q.n));
      // question numbers strictly increasing (monotonic, no dupes)
      for (let i = 1; i < nums.length; i++) expect(nums[i]).toBeGreaterThan(nums[i - 1]);

      for (const q of map.q) {
        expect(q.mode === 'crop' || q.mode === 'pagejump', `${q.n} mode`).toBe(true);
        expect(q.pP).toBeGreaterThanOrEqual(1);
        expect(q.pY[0]).toBeGreaterThanOrEqual(0);
        expect(q.pY[1]).toBeLessThanOrEqual(1);
        expect(q.region.length).toBeGreaterThan(0);
        const pages = q.region.map(s => s.p);
        for (const seg of q.region) {
          // EVERY region page inside the paper's own band (the P1/P2 guard)
          expect(seg.p >= lo && seg.p < hi, `${file} Q${q.n} page ${seg.p} in [${lo},${hi})`).toBe(true);
          if (seg.r) {
            for (const v of seg.r) expect(v >= 0 && v <= 1, `${file} Q${q.n} rect ∈[0,1]`).toBe(true);
          }
        }
        // crop region pages are sorted; page-jump carries exactly one target
        if (q.mode === 'crop') {
          expect(pages).toEqual([...pages].sort((a, b) => a - b));
        } else {
          expect(q.region.length).toBe(1);
        }
      }
    });
  }
});

describe('Paper Trail answer flag ↔ sidecar consistency', () => {
  it('every paper flagged answers:1 has a committed sidecar', () => {
    const missing: string[] = [];
    for (const entries of Object.values(PAPER_TRAIL_INDEX)) {
      for (const entry of entries) {
        for (const item of entry.papers) {
          if (item.answers === 1) {
            const p = path.join(ANSWERS_DIR, String(entry.year), `${item.doc.f}.json`);
            if (!existsSync(p)) missing.push(`${entry.year}/${item.doc.f}`);
          }
        }
      }
    }
    expect(missing, `flagged papers without a sidecar: ${missing.join(', ')}`).toEqual([]);
  });

  it('the answers flag, where present, is exactly 1', () => {
    for (const entries of Object.values(PAPER_TRAIL_INDEX)) {
      for (const entry of entries) {
        for (const item of entry.papers) {
          if ('answers' in item && item.answers !== undefined) {
            expect(item.answers).toBe(1);
          }
        }
      }
    }
  });
});
