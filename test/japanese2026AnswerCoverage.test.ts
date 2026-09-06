/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Japanese 2026 listening is a section-restart paper: Parts A, B, C and D
 * each print their own Q1. The first generated sidecars silently collapsed
 * those duplicate printed numbers, leaving all of B/C and D1-3 inaccessible.
 * This locks the recovered cards in place without renumbering any shipped ID.
 */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

const load = (fileid: string): PaperAnswerMap => JSON.parse(readFileSync(
  resolve(__dirname, `../scripts/paper-trail/answers/2026/${fileid}.json`),
  'utf8',
));

const higher = load('LC058ALPA00BV.pdf');
const ordinary = load('LC058GLPA00BV.pdf');

const stableHigher = [
  ['1', 2, [0.3165, 0.4737]],
  ['2', 2, [0.4737, 0.6309]],
  ['3', 2, [0.6309, 1.0]],
  ['4', 5, [0.5257, 0.6243]],
  ['5', 5, [0.6243, 0.7055]],
  ['6', 5, [0.7055, 0.7751]],
  ['7', 5, [0.7751, 0.8563]],
  ['8', 5, [0.8563, 1.0]],
] as const;

const stableOrdinary = [
  ['1', 2, [0.1484, 0.379]],
  ['2', 2, [0.379, 0.6558]],
  ['3', 2, [0.6558, 1.0]],
  ['4', 5, [0.5017, 0.5713]],
  ['5', 5, [0.5713, 0.6829]],
  ['6', 5, [0.6829, 0.819]],
  ['7', 5, [0.819, 1.0]],
] as const;

const identity = (map: PaperAnswerMap, ids: readonly (readonly [string, number, readonly number[]])[]) =>
  ids.map(([n]) => {
    const q = map.q.find(question => question.n === n)!;
    return [q.n, q.pP, q.pY];
  });

const partCounts = (map: PaperAnswerMap) => map.q.reduce<Record<string, number>>((out, q) => {
  const part = q.label?.match(/^PART [A-D]/)?.[0] ?? 'unlabelled';
  out[part] = (out[part] ?? 0) + 1;
  return out;
}, {});

describe('Japanese 2026 listening answer coverage', () => {
  it('preserves every original Higher and Ordinary card identity', () => {
    expect(identity(higher, stableHigher)).toEqual(stableHigher);
    expect(identity(ordinary, stableOrdinary)).toEqual(stableOrdinary);
  });

  it('covers every printed section and question group', () => {
    expect(higher.q).toHaveLength(16);
    expect(partCounts(higher)).toEqual({ 'PART A': 3, 'PART D': 8, 'PART B': 3, 'PART C': 2 });
    expect(ordinary.q).toHaveLength(15);
    expect(partCounts(ordinary)).toEqual({ 'PART A': 3, 'PART D': 7, 'PART B': 3, 'PART C': 2 });
  });

  it.each([
    ['Higher', higher],
    ['Ordinary', ordinary],
  ] as const)('%s cards have unique stable IDs and an explicit physical order', (_level, map) => {
    expect(map.q.map(q => q.n)).toEqual(map.q.map((_, i) => String(i + 1)));
    expect(map.q.map(q => q.printOrder).sort((a, b) => a! - b!))
      .toEqual(map.q.map((_, i) => i + 1));

    const physical = [...map.q].sort((a, b) => a.printOrder! - b.printOrder!);
    for (let i = 1; i < physical.length; i++) {
      const prior = physical[i - 1];
      const current = physical[i];
      expect(
        current.pP > prior.pP || (current.pP === prior.pP && current.pY[0] > prior.pY[0]),
        `${current.label} must follow ${prior.label}`,
      ).toBe(true);
    }
  });

  it.each([
    ['Higher', higher],
    ['Ordinary', ordinary],
  ] as const)('%s cards all yield bounded paper crops and scheme crops', (_level, map) => {
    for (const q of map.q) {
      expect(paperRegionFor(map.q, q.n), `${q.label} paper crop`).not.toBeNull();
      expect(q.mode, `${q.label} scheme mode`).toBe('crop');
      expect(q.region.length, `${q.label} scheme crop`).toBeGreaterThan(0);
    }
  });

  it('uses explicit section ends so restart headers cannot bleed into the prior card', () => {
    for (const [map, ids] of [
      [higher, ['3', '11', '13']],
      [ordinary, ['3', '10', '12']],
    ] as const) {
      for (const n of ids) {
        const q = map.q.find(question => question.n === n)!;
        expect(q.endP).toBe(q.pP);
        expect(q.endY).toBe(q.pY[1]);
        expect(paperRegionFor(map.q, n)).toHaveLength(1);
      }
    }
  });
});
