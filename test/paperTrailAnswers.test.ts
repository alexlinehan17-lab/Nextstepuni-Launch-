/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail answer-map integrity — guards the committed per-paper answer
 * sidecars (scripts/paper-trail/answers/ and public/paper-answers/), permits reviewed hosted paper-only
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
import { preferredAnswersUrl } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor, printedQuestionAnchors } from '../components/PaperTrail/paperRegion';

const ANSWERS_DIR = path.resolve(__dirname, '../scripts/paper-trail/answers');
const ANCHORS_DIR = path.resolve(__dirname, '../public/paper-anchors');
const HOSTED_ANSWERS_DIR = path.resolve(__dirname, '../public/paper-answers');

function allSidecars(): { source: string; year: string; file: string; map: PaperAnswerMap }[] {
  const out: { source: string; year: string; file: string; map: PaperAnswerMap }[] = [];
  for (const [source, directory] of [['storage', ANSWERS_DIR], ['hosted', HOSTED_ANSWERS_DIR]]) {
    if (!existsSync(directory)) continue;
    for (const year of readdirSync(directory)) {
      const ydir = path.join(directory, year);
      for (const file of readdirSync(ydir)) {
        if (!file.endsWith('.json')) continue;
        out.push({ source, year, file, map: JSON.parse(readFileSync(path.join(ydir, file), 'utf-8')) });
      }
    }
  }
  return out;
}

const sidecars = allSidecars();

describe('Paper Trail answer sidecars — shape', () => {
  it('there is at least one committed sidecar (pilot present)', () => {
    expect(sidecars.length).toBeGreaterThan(0);
  });

  for (const { source, year, file, map } of sidecars) {
    it(`${source}/${year}/${file} conforms to PaperAnswerMap and stays in-band`, () => {
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

      // Printed questions are the anchors: numeric, strictly ascending and in
      // print order. Reviewed practice tasks (Accounting 1(a), 8(a)(ii)-…) are
      // appended to the same map with their own audited paper region; they
      // have a separate contract below and never take part in anchor ordering.
      const printed = printedQuestionAnchors(map.q);
      const tasks = map.q.filter(q => !printed.includes(q));
      // A map may add only reviewed sub-tasks to a paper whose whole questions
      // were never anchored (Agricultural Science 2018 HL): then every entry is
      // a parentN sub-task with its own audited region.
      const subTasksOnly = map.q.every(q => Boolean(q.parentN));
      if (!subTasksOnly) expect(printed.length).toBeGreaterThan(0);
      const nums = printed.map(q => Number(q.n));
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
      const explicitPrintOrder = printed.some(q => q.printOrder !== undefined);
      if (explicitPrintOrder) {
        expect(printed.every(q => Number.isInteger(q.printOrder) && q.printOrder! > 0), `${file} partial printOrder`).toBe(true);
        expect(new Set(printed.map(q => q.printOrder)).size, `${file} duplicate printOrder`).toBe(printed.length);
      }
      const byPage = new Map<number, number[]>();
      for (const q of printed) {
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
        // A printed question's crop region pages are sorted. A reviewed
        // practice task lists its scheme pages in display order instead (its
        // answer pages, then the scheme's shared marking-conventions page).
        // Page-jump carries exactly one target.
        if (q.mode === 'crop') {
          if (printed.includes(q)) expect(pages).toEqual([...pages].sort((a, b) => a - b));
          else expect(new Set(q.region.map(seg => JSON.stringify(seg))).size, `${file} ${q.n} duplicate segment`).toBe(q.region.length);
        } else {
          expect(q.region.length).toBe(1);
        }
      }

      // Practice-task contract. Each task is an independently reviewed part of
      // a retained printed question: a unique key rooted in that question's
      // number, a label, the prompt and its published tariff, and an explicit
      // audited paper region (never inferred from neighbouring anchors).
      if (tasks.length) {
        expect(new Set(map.q.map(q => q.n)).size, `${file} duplicate keys`).toBe(map.q.length);
        const parents = new Set(printed.map(q => q.n));
        for (const task of tasks) {
          const id = `${file} ${task.n}`;
          if (task.parentN) {
            // Agricultural Science reviewed sub-task: rooted in a retained
            // printed question by parentN, with an explicit audited region the
            // reader returns as-is. Its prompt and tariff live on the Mark Bank
            // card, not in the map.
            expect(subTasksOnly ? /^\d+$/.test(task.parentN) : parents.has(task.parentN), `${id} parent retained`).toBe(true);
            expect(typeof task.label === 'string' && task.label.trim().length > 0, `${id} label`).toBe(true);
            expect(task.paperRegion?.length, `${id} explicit paper region`).toBeGreaterThan(0);
            expect(paperRegionFor(map.q, task.n), `${id} usable paper region`).toEqual(task.paperRegion);
            continue;
          }
          // Rooted in a retained printed question, optionally through its
          // printed alternative (2021+ Q1A / Q1B → parent 1).
          expect(parents.has(task.n.match(/^(\d+)[A-Z]?\(/)?.[1] ?? ''), `${id} parent retained`).toBe(true);
          expect(typeof task.label === 'string' && task.label.trim().length > 0, `${id} label`).toBe(true);
          expect(task.practiceTask!.prompt.trim().length, `${id} prompt`).toBeGreaterThan(0);
          expect(task.practiceTask!.marks, `${id} marks`).toBeGreaterThan(0);
          expect(task.paperRegion?.length, `${id} explicit paper region`).toBeGreaterThan(0);
          expect(task.paperRegion![0].p, `${id} anchor page is the region's first page`).toBe(task.pP);
          // The reader accepts the audited region as-is (validity + page span).
          expect(paperRegionFor(map.q, task.n), `${id} usable paper region`).toEqual(task.paperRegion);
        }
        // A task's page reference must never shorten or extend a printed
        // question's crop: derived regions match the tasks-free map exactly.
        for (const question of printed) {
          expect(paperRegionFor(map.q, question.n), `${file} Q${question.n} crop unaffected by tasks`)
            .toEqual(paperRegionFor(printed, question.n));
        }
      }
    });
  }
});

describe('Paper Trail answer flag ↔ sidecar consistency', () => {
  it('every paper flagged answers:1 has a committed answer or paper-anchor sidecar', () => {
    const missing: string[] = [];
    for (const [subjectId, entries] of Object.entries(PAPER_TRAIL_INDEX)) {
      for (const entry of entries) {
        for (const item of entry.papers) {
          if (item.answers === 1) {
            const answer = path.join(ANSWERS_DIR, String(entry.year), `${item.doc.f}.json`);
            const anchor = path.join(ANCHORS_DIR, String(entry.year), `${item.doc.f}.json`);
            const preferred = preferredAnswersUrl(subjectId, entry.year, item.doc.f, 'storage');
            if (preferred.startsWith('/paper-answers/')) {
              // A committed override must exist at the URL the reader actually uses.
              const hosted = path.join(HOSTED_ANSWERS_DIR, String(entry.year), `${item.doc.f}.json`);
              if (!existsSync(hosted)) missing.push(`hosted:${entry.year}/${item.doc.f}`);
            } else if (!existsSync(answer) && !existsSync(anchor)) {
              missing.push(`${entry.year}/${item.doc.f}`);
            }
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
