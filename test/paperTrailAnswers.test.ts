/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail answer-map integrity — guards the committed per-paper answer
 * sidecars (scripts/paper-trail/answers/), permits reviewed hosted paper-only
 * fallbacks (public/paper-anchors/), and checks their contract with the
 * generated paperTrailData.ts. Runs in CI WITHOUT the gitignored corpus: it reads
 * only committed sidecars + the committed index. The deep, corpus-dependent checks
 * (does a region actually contain that question?) live in the Python
 * test_anchor_map.py, run locally where the corpus exists.
 */

import { readFileSync, existsSync, readdirSync } from 'fs';
import path from 'path';
import { describe, it, expect } from 'vitest';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import type { PaperAnswerMap } from '../types/paperTrail';

const ANSWERS_DIR = path.resolve(__dirname, '../scripts/paper-trail/answers');
const ANCHORS_DIR = path.resolve(__dirname, '../public/paper-anchors');

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

      // PRINT-ORDER gate. paperRegion.ts derives a question's crop by sorting
      // the anchors into print order (page, then y) and running each one to the
      // next — so a marker matched somewhere it does not belong silently steals
      // a crop. The decoy-numbering families are the ones that do it: a matching
      // exercise ("1. Jobs bei der EU … a. die für …"), a numbered passage
      // paragraph, or an instructions page naming a later question ("Question 13
      // in Section B"). Reading DOWN the paper, question numbers must ascend.
      //
      // Scoped to page granularity on purpose: a bilingual two-column page
      // prints the same question twice side by side, so y alone orders those
      // legitimately-equal anchors arbitrarily. Crossing a PAGE backwards has no
      // such excuse. anchor-map.py never applied this gate; paper_anchors.py
      // always has.
      const explicitPrintOrder = map.q.some(q => q.printOrder !== undefined);
      if (explicitPrintOrder) {
        expect(map.q.every(q => Number.isInteger(q.printOrder) && q.printOrder! > 0), `${file} partial printOrder`).toBe(true);
        expect(new Set(map.q.map(q => q.printOrder)).size, `${file} duplicate printOrder`).toBe(map.q.length);
      }
      const byPage = new Map<number, number[]>();
      for (const q of map.q) {
        const list = byPage.get(q.pP);
        const printRank = q.printOrder ?? Number(q.n);
        if (list) list.push(printRank);
        else byPage.set(q.pP, [printRank]);
      }
      let priorPagesMax = 0;
      for (const page of [...byPage.keys()].sort((a, b) => a - b)) {
        const here = byPage.get(page)!;
        for (const n of here) {
          expect(
            n > priorPagesMax,
            `${file} print rank ${n} anchors on page ${page}, behind rank ${priorPagesMax} on an earlier page — anchor matched decoy numbering`,
          ).toBe(true);
        }
        priorPagesMax = Math.max(priorPagesMax, ...here);
      }

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
  it('every paper flagged answers:1 has a committed answer or paper-anchor sidecar', () => {
    const missing: string[] = [];
    for (const entries of Object.values(PAPER_TRAIL_INDEX)) {
      for (const entry of entries) {
        for (const item of entry.papers) {
          if (item.answers === 1) {
            const answer = path.join(ANSWERS_DIR, String(entry.year), `${item.doc.f}.json`);
            const anchor = path.join(ANCHORS_DIR, String(entry.year), `${item.doc.f}.json`);
            if (!existsSync(answer) && !existsSync(anchor)) missing.push(`${entry.year}/${item.doc.f}`);
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
