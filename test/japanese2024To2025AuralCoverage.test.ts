/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Japanese listening papers restart numbering in every Part. These regressions
 * preserve the card identities shipped before the collision repair while
 * proving that every physically printed 2024–2025 question group is reachable.
 */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

type StableIdentity = readonly [string, number, readonly [number, number]];

const load = (year: number, fileid: string): PaperAnswerMap => JSON.parse(readFileSync(
  resolve(__dirname, `../scripts/paper-trail/answers/${year}/${fileid}.json`),
  'utf8',
));

const maps = {
  '2024 Higher': load(2024, 'LC058ALPA00BV.pdf'),
  '2024 Ordinary': load(2024, 'LC058GLPA00BV.pdf'),
  '2025 Higher': load(2025, 'LC058ALPA00BV.pdf'),
  '2025 Ordinary': load(2025, 'LC058GLPA00BV.pdf'),
} as const;

const stable: Record<keyof typeof maps, readonly StableIdentity[]> = {
  '2024 Higher': [
    ['1', 2, [0.3666, 0.5238]], ['2', 2, [0.5238, 0.681]],
    ['3', 2, [0.681, 1]], ['4', 3, [0.3729, 0.4308]],
    ['5', 3, [0.4308, 0.5236]], ['6', 3, [0.5236, 0.5816]],
    ['7', 3, [0.5816, 0.7092]], ['8', 3, [0.7092, 0.8368]],
    ['9', 3, [0.8368, 1]],
  ],
  '2024 Ordinary': [
    ['1', 2, [0.1144, 0.3629]], ['2', 2, [0.3629, 0.639]],
    ['3', 2, [0.639, 1]], ['4', 3, [0.4057, 0.4638]],
    ['5', 3, [0.4638, 0.6043]], ['6', 3, [0.6043, 0.7102]],
    ['7', 3, [0.7102, 0.7856]], ['8', 3, [0.7856, 1]],
  ],
  '2025 Higher': [
    ['1', 2, [0.2952, 0.4544]], ['2', 2, [0.4544, 0.6136]],
    ['3', 2, [0.6136, 1]], ['4', 4, [0.3807, 0.5112]],
    ['5', 4, [0.5112, 0.6678]], ['6', 4, [0.6678, 0.7548]],
    ['7', 4, [0.7548, 1]],
  ],
  '2025 Ordinary': [
    ['1', 2, [0.1481, 0.4464]], ['2', 2, [0.4464, 0.71]],
    ['3', 2, [0.71, 1]], ['4', 4, [0.5257, 0.694]],
    ['5', 4, [0.694, 0.7607]], ['6', 4, [0.7607, 0.8274]],
    ['7', 4, [0.8274, 1]],
  ],
};

const expected = {
  '2024 Higher': { total: 17, parts: { 'PART A': 3, 'PART B': 9, 'PART C': 2, 'PART D': 3 } },
  '2024 Ordinary': { total: 16, parts: { 'PART A': 3, 'PART B': 8, 'PART C': 2, 'PART D': 3 } },
  '2025 Higher': { total: 15, parts: { 'PART A': 3, 'PART B': 2, 'PART C': 7, 'PART D': 3 } },
  '2025 Ordinary': { total: 15, parts: { 'PART A': 3, 'PART B': 2, 'PART C': 7, 'PART D': 3 } },
} as const;

const partCounts = (map: PaperAnswerMap) => map.q.reduce<Record<string, number>>((out, q) => {
  const part = q.label?.match(/^PART [A-D]/)?.[0] ?? 'unlabelled';
  out[part] = (out[part] ?? 0) + 1;
  return out;
}, {});

describe('Japanese 2024–2025 listening answer coverage', () => {
  it.each(Object.entries(maps))('%s preserves every pre-repair card identity', (name, map) => {
    const actual = stable[name as keyof typeof maps].map(([n]) => {
      const question = map.q.find(q => q.n === n)!;
      return [question.n, question.pP, question.pY];
    });
    expect(actual).toEqual(stable[name as keyof typeof maps]);
  });

  it.each(Object.entries(maps))('%s covers every printed Part and question group', (name, map) => {
    const result = expected[name as keyof typeof maps];
    expect(map.q).toHaveLength(result.total);
    expect(partCounts(map)).toEqual(result.parts);
  });

  it.each(Object.entries(maps))('%s has stable IDs plus a complete physical order', (_name, map) => {
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

  it.each(Object.entries(maps))('%s yields bounded paper and scheme crops for every card', (_name, map) => {
    for (const q of map.q) {
      expect(paperRegionFor(map.q, q.n), `${q.label} paper crop`).not.toBeNull();
      expect(q.mode, `${q.label} scheme mode`).toBe('crop');
      expect(q.region.length, `${q.label} scheme crop`).toBeGreaterThan(0);
    }
  });
});
