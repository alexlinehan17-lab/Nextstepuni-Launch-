/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The generic language mapper historically stopped after Japanese reading
 * questions, so the 2024–2026 written papers shipped without answer sidecars.
 * These checks keep every audited SEC question/answer crop reachable and make
 * the curriculum-topic crosswalk part of the regression surface.
 */

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap } from '../types/paperTrail';

type Level = 'higher' | 'ordinary';

type MapSpec = {
  year: number;
  level: Level;
  fileid: string;
  total: number;
  topics: readonly string[];
};

const repeat = (topic: string, count: number) => Array<string>(count).fill(topic);

const specs: readonly MapSpec[] = [
  {
    year: 2024,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    total: 27,
    topics: [
      ...repeat('japanese-5-0', 9),
      ...repeat('japanese-5-4', 2),
      ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-1', 10),
      'japanese-5-4', 'japanese-5-5',
      ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2024,
    level: 'ordinary',
    fileid: 'LC058GLP000BV.pdf',
    total: 25,
    topics: [
      ...repeat('japanese-5-0', 7),
      ...repeat('japanese-5-2', 7),
      'japanese-5-4', 'japanese-5-6',
      ...repeat('japanese-5-1', 5),
      ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2025,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    total: 30,
    topics: [
      ...repeat('japanese-5-0', 10),
      ...repeat('japanese-5-2', 2),
      'japanese-5-3',
      ...repeat('japanese-5-4', 2),
      ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-1', 9),
      'japanese-5-4', 'japanese-5-5',
      ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2025,
    level: 'ordinary',
    fileid: 'LC058GLP000BV.pdf',
    total: 26,
    topics: [
      ...repeat('japanese-5-0', 6),
      ...repeat('japanese-5-2', 9),
      'japanese-5-4', 'japanese-5-6',
      ...repeat('japanese-5-1', 5),
      ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2026,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    total: 20,
    topics: [
      ...repeat('japanese-5-0', 7),
      ...repeat('japanese-5-2', 2),
      'japanese-5-3',
      ...repeat('japanese-5-4', 2),
      ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-1', 2),
      'japanese-5-4', 'japanese-5-5',
      ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2026,
    level: 'ordinary',
    fileid: 'LC058GLP000BV.pdf',
    total: 29,
    topics: [
      ...repeat('japanese-5-0', 6),
      ...repeat('japanese-5-2', 12),
      'japanese-5-4', 'japanese-5-6',
      ...repeat('japanese-5-2', 5),
      ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-7', 2),
    ],
  },
];

const loadMap = ({ year, fileid }: MapSpec): PaperAnswerMap => JSON.parse(readFileSync(
  resolve(__dirname, `../scripts/paper-trail/answers/${year}/${fileid}.json`),
  'utf8',
));

type SourceTag = {
  year: number;
  level: Level;
  fileid: string;
  paperKey: string;
  q: { n: string; primary: string }[];
};

const sourceTags: SourceTag[] = JSON.parse(readFileSync(
  resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'),
  'utf8',
));

const uploadManifest = readFileSync(
  resolve(__dirname, '../scripts/paper-trail/publish/audit-reupload.tsv'),
  'utf8',
);

describe('Japanese 2024–2026 written answer coverage', () => {
  it.each(specs)('$year $level exposes every audited card in physical order', spec => {
    const map = loadMap(spec);
    expect(map.q).toHaveLength(spec.total);
    expect(map.q.map(q => q.n)).toEqual(map.q.map((_, index) => String(index + 1)));

    for (let index = 1; index < map.q.length; index++) {
      const prior = map.q[index - 1];
      const current = map.q[index];
      expect(
        current.pP > prior.pP || (current.pP === prior.pP && current.pY[0] > prior.pY[0]),
        `${current.label} must follow ${prior.label}`,
      ).toBe(true);
    }
  });

  it.each(specs)('$year $level yields bounded paper and scheme crops for every card', spec => {
    const map = loadMap(spec);
    for (const q of map.q) {
      expect(paperRegionFor(map.q, q.n), `${q.label} paper crop`).not.toBeNull();
      expect(q.mode, `${q.label} scheme mode`).toBe('crop');
      expect(q.region.length, `${q.label} scheme crop`).toBeGreaterThan(0);
      for (const region of q.region) {
        expect(region.p, `${q.label} scheme page`).toBeGreaterThanOrEqual(map.band[0]);
        expect(region.p, `${q.label} scheme page`).toBeLessThan(map.band[1]);
        expect(region.r?.[1], `${q.label} scheme crop start`).toBeGreaterThanOrEqual(0);
        expect(region.r?.[3], `${q.label} scheme crop end`).toBeLessThanOrEqual(1);
        expect(region.r?.[3], `${q.label} scheme crop height`).toBeGreaterThan(region.r?.[1] ?? 1);
      }
    }
  });

  it.each(specs)('$year $level retains all five written-paper question families', spec => {
    const labels = loadMap(spec).q.map(q => q.label ?? '');
    for (const family of ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']) {
      expect(labels.some(label => label.startsWith(family)), `${family} missing`).toBe(true);
    }
  });

  it.each(specs)('$year $level has a complete, intentional topic crosswalk', spec => {
    const record = sourceTags.find(tag => (
      tag.year === spec.year
      && tag.level === spec.level
      && tag.fileid === spec.fileid
      && tag.paperKey === 'single'
    ));
    expect(record, `${spec.year} ${spec.level} source tags`).toBeDefined();
    expect(record?.q.map(q => q.n)).toEqual(spec.topics.map((_, index) => String(index + 1)));
    expect(record?.q.map(q => q.primary)).toEqual(spec.topics);
  });

  it.each(specs)('$year $level is included in the audited upload set', spec => {
    const local = `scripts/paper-trail/answers/${spec.year}/${spec.fileid}.json`;
    const remote = `papers/lc/japanese/${spec.year}/answers/${spec.fileid}.json`;
    expect(uploadManifest).toContain(`${local}\t${remote}`);
  });
});
