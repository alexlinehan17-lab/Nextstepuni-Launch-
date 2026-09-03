/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Topic Vault — hosted paper-anchors fallback. Two contracts under test:
 *
 * 1. The pure resolution/validation logic in vaultResolve.ts: candidate URL
 *    ordering (verified Storage sidecar first, hosted anchors second) and the
 *    isAnswerMap shape guard. The guard is load-bearing: Firebase Hosting's
 *    SPA rewrite answers a MISSING /paper-anchors/... file with index.html
 *    and HTTP 200, so "miss" is detected by parse/shape, not status.
 *
 * 2. The committed pilot artifacts in public/paper-anchors/: every staged
 *    sidecar must be a valid, paper-only, monotonic map whose every question
 *    yields a confident paper-side crop via paperRegionFor. A wrong crop is
 *    worse than none — these files ship to the live app on push to main.
 */

import { existsSync, readdirSync, readFileSync } from 'fs';
import path from 'path';
import { describe, it, expect } from 'vitest';
import { answerMapUrls, hostedAnchorsUrl, isAnswerMap, resolveSibling, type ResolvedSibling } from '../components/PaperTrail/vaultResolve';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

const ANCHORS_DIR = path.resolve(__dirname, '../public/paper-anchors');

// ─── pure resolution logic ──────────────────────────────────────────────────

describe('hostedAnchorsUrl', () => {
  it('addresses the committed hosting path by year + fileid', () => {
    expect(hostedAnchorsUrl(2024, 'LC562ALP039EV.pdf'))
      .toBe('/paper-anchors/2024/LC562ALP039EV.pdf.json');
  });

  it('URL-encodes unusual fileids', () => {
    expect(hostedAnchorsUrl(2020, 'LC 01#.pdf')).toBe('/paper-anchors/2020/LC%2001%23.pdf.json');
  });
});

describe('answerMapUrls', () => {
  const base: ResolvedSibling = {
    paperUrl: 'https://storage/paper.pdf',
    schemeUrl: null,
    answersUrl: 'https://storage/answers/X.pdf.json',
    anchorsUrl: '/paper-anchors/2024/X.pdf.json',
    paperLabel: 'Exam Paper',
    preferAnchors: false,
  };

  it('tries the verified Storage sidecar before the hosted paper anchors', () => {
    expect(answerMapUrls(base)).toEqual([base.answersUrl, base.anchorsUrl]);
  });

  it('uses ONLY the hosted anchors for a numbering-conflict subject', () => {
    // Geography's Storage sidecar numbers Part-Two essays 1..12 while the vault
    // tags number Part-One short questions 1..12 — the Storage sidecar is wrong
    // for every tag, so it must never be served; a paper with no anchor falls
    // back honestly rather than showing a Part-Two crop under a Part-One topic.
    expect(answerMapUrls({ ...base, preferAnchors: true })).toEqual([base.anchorsUrl]);
  });

  it('geography resolves with preferAnchors set', () => {
    const geo = resolveSibling({ subjectId: 'geography', year: 2019, level: 'higher', lang: 'ev', fileid: 'LC005ALP000EV.pdf', paperKey: 'single', n: '1' });
    // Only assert the flag when the paper is in the committed index.
    if (geo) expect(geo.preferAnchors).toBe(true);
    const bio = resolveSibling({ subjectId: 'biology', year: 2019, level: 'higher', lang: 'ev', fileid: 'LC002ALP000EV.pdf', paperKey: 'single', n: '1' });
    if (bio) expect(bio.preferAnchors).toBe(false);
  });
});

describe('isAnswerMap', () => {
  const q = { n: '1', pP: 2, pY: [0.1, 1], region: [{ p: 1 }], mode: 'pagejump', conf: 0.5 };

  it('accepts a paper-only pagejump sidecar', () => {
    expect(isAnswerMap({ v: 1, paperFileid: 'X.pdf', schemeFileid: '', q: [q] })).toBe(true);
  });

  it('accepts a verified crop sidecar', () => {
    expect(isAnswerMap({
      v: 1, paperFileid: 'X.pdf', schemeFileid: 'S.pdf', component: '000', band: [1, 9],
      q: [{ ...q, region: [{ p: 3, r: [0, 0.2, 1, 0.9] }], mode: 'crop', conf: 1 }],
    })).toBe(true);
  });

  it.each([
    ['null', null],
    ['a string (index.html body would fail parse before this)', '<!doctype html>'],
    ['an empty object', {}],
    ['an empty question list', { paperFileid: 'X.pdf', q: [] }],
    ['q missing pP/pY', { paperFileid: 'X.pdf', q: [{ n: '1', region: [], mode: 'crop' }] }],
    ['q with a bad mode', { paperFileid: 'X.pdf', q: [{ ...q, mode: 'guess' }] }],
    ['q with a malformed pY', { paperFileid: 'X.pdf', q: [{ ...q, pY: [0.1] }] }],
    ['q with a non-numeric page', { paperFileid: 'X.pdf', q: [{ ...q, pP: '2' }] }],
  ])('rejects %s', (_label, v) => {
    expect(isAnswerMap(v)).toBe(false);
  });
});

// ─── committed pilot artifacts ──────────────────────────────────────────────

function stagedAnchors(): { year: string; file: string; map: PaperAnswerMap }[] {
  if (!existsSync(ANCHORS_DIR)) return [];
  const out: { year: string; file: string; map: PaperAnswerMap }[] = [];
  for (const year of readdirSync(ANCHORS_DIR)) {
    const ydir = path.join(ANCHORS_DIR, year);
    for (const file of readdirSync(ydir)) {
      if (!file.endsWith('.json')) continue;
      out.push({ year, file, map: JSON.parse(readFileSync(path.join(ydir, file), 'utf-8')) });
    }
  }
  return out;
}

const staged = stagedAnchors();

describe('public/paper-anchors — committed pilot sidecars', () => {
  it('the DCG pilot is present', () => {
    expect(staged.length).toBeGreaterThan(0);
  });

  it('every file passes the runtime shape guard and claims no scheme mapping', () => {
    for (const { year, file, map } of staged) {
      expect(isAnswerMap(map), `${year}/${file} shape`).toBe(true);
      expect(file, `${year}/${file} filename`).toBe(`${map.paperFileid}.json`);
      expect(map.schemeFileid, `${year}/${file} must not claim a scheme`).toBe('');
      for (const q of map.q) {
        expect(q.mode, `${year}/${file} Q${q.n} mode`).toBe('pagejump'); // no reveal claim
        expect(q.conf, `${year}/${file} Q${q.n} conf`).toBeLessThan(0.6);
      }
    }
  });

  it('question numbers are sequential and anchors are monotonic in print order', () => {
    for (const { year, file, map } of staged) {
      // Sequential run in PRINTED numbering — split-spec second booklets
      // continue the first paper's run (Biology Section C prints Q11-Q17),
      // so the run may start above 1 but must ascend without gaps.
      const first = Number(map.q[0]?.n ?? 1);
      map.q.forEach((q, i) => expect(q.n, `${year}/${file} q[${i}].n`).toBe(String(first + i)));
      for (let i = 1; i < map.q.length; i++) {
        const a = map.q[i - 1];
        const b = map.q[i];
        expect(
          b.pP > a.pP || (b.pP === a.pP && b.pY[0] > a.pY[0]),
          `${year}/${file} Q${b.n} out of print order`,
        ).toBe(true);
      }
    }
  });

  it('every anchored question yields a confident paper-side crop', () => {
    for (const { year, file, map } of staged) {
      for (const q of map.q) {
        const region = paperRegionFor(map.q, q.n);
        expect(region, `${year}/${file} Q${q.n} has no derivable crop`).not.toBeNull();
      }
    }
  });
});
