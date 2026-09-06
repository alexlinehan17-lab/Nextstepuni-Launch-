/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The original Japanese 2019-2022 sidecars stopped before whole assessed
 * sections. These regressions enforce an additive repair: every old card keeps
 * its stable identity and crop, every recovered section is reachable in its
 * physical position, and the complete written paper has an intentional topic.
 */

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { paperRegionFor, questionsInDisplayOrder } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap, PaperAnswerQuestion } from '../types/paperTrail';

type Level = 'higher' | 'ordinary';

type MapSpec = {
  year: number;
  level: Level;
  fileid: string;
  base: number;
  total: number;
  baseHash: string;
  topics: readonly string[];
};

const repeat = (topic: string, count: number) => Array<string>(count).fill(topic);

const specs: readonly MapSpec[] = [
  {
    year: 2019,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    base: 26,
    total: 28,
    baseHash: 'fb0b80dc8d795f85c6e05cab38dfbddafc58447a6d036a9a50bed22ebfca950e',
    topics: [
      ...repeat('japanese-5-0', 8), ...repeat('japanese-5-2', 3), 'japanese-5-3',
      ...repeat('japanese-5-4', 2), ...repeat('japanese-5-5', 2),
      ...repeat('japanese-5-1', 8), 'japanese-5-4', 'japanese-5-5',
      ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2019,
    level: 'ordinary',
    fileid: 'LC058GLP000BV.pdf',
    base: 20,
    total: 23,
    baseHash: '883b4ed6a8be6fe1afed2c8000cd9b528a93796e60f499c73e2ee78eba8ac528',
    topics: [
      ...repeat('japanese-5-0', 6), ...repeat('japanese-5-2', 6), 'japanese-5-4',
      ...repeat('japanese-5-1', 5), ...repeat('japanese-5-5', 2),
      'japanese-5-6', ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2020,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    base: 20,
    total: 26,
    baseHash: '916febeedccfef0a8f025224ba002382fc2f3edd7b985de906f2a736c001fda5',
    topics: [
      ...repeat('japanese-5-0', 7), ...repeat('japanese-5-1', 3), 'japanese-5-3',
      ...repeat('japanese-5-2', 9), 'japanese-5-4', 'japanese-5-5',
      'japanese-5-4', 'japanese-5-5', ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2021,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    base: 23,
    total: 29,
    baseHash: '739a084d54b40f4cb51311c92470d995948d7c2b98b22397e0d518a37b8a862b',
    topics: [
      ...repeat('japanese-5-0', 10), ...repeat('japanese-5-2', 3), 'japanese-5-3',
      ...repeat('japanese-5-2', 9), 'japanese-5-4', 'japanese-5-5',
      'japanese-5-4', 'japanese-5-5', ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2021,
    level: 'ordinary',
    fileid: 'LC058GLP000BV.pdf',
    base: 21,
    total: 24,
    baseHash: '57a58f1975ebc8355264be7b7c1253e1fc968b591ef1cf99cc4cd35a05448215',
    topics: [
      ...repeat('japanese-5-0', 7), ...repeat('japanese-5-2', 6), 'japanese-5-4',
      ...repeat('japanese-5-1', 5), ...repeat('japanese-5-5', 2),
      'japanese-5-6', ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2022,
    level: 'higher',
    fileid: 'LC058ALP000BV.pdf',
    base: 22,
    total: 28,
    baseHash: '1e6bedc2bd51704e908b6273f669204ba7d0dbf11501afe0c23e229094d1ced1',
    topics: [
      ...repeat('japanese-5-0', 9), ...repeat('japanese-5-2', 3), 'japanese-5-3',
      ...repeat('japanese-5-2', 9), 'japanese-5-4', 'japanese-5-5',
      'japanese-5-4', 'japanese-5-5', ...repeat('japanese-5-7', 2),
    ],
  },
  {
    year: 2022,
    level: 'ordinary',
    fileid: 'LC058GLP000BV.pdf',
    base: 21,
    total: 24,
    baseHash: '227ec5478f8433f65f05d5af409494daad6948cdabfffd470b6f555d90a34774',
    topics: [
      ...repeat('japanese-5-0', 6), ...repeat('japanese-5-2', 7), 'japanese-5-4',
      ...repeat('japanese-5-2', 5), ...repeat('japanese-5-5', 2),
      'japanese-5-6', ...repeat('japanese-5-7', 2),
    ],
  },
];

const loadMap = ({ year, fileid }: MapSpec): PaperAnswerMap => JSON.parse(readFileSync(
  resolve(__dirname, `../scripts/paper-trail/answers/${year}/${fileid}.json`),
  'utf8',
));

const withoutPrintOrder = ({ printOrder: _printOrder, ...question }: PaperAnswerQuestion) => question;
const digest = (questions: PaperAnswerQuestion[]) => createHash('sha256')
  .update(JSON.stringify(questions.map(withoutPrintOrder)))
  .digest('hex');

type SourceTag = {
  year: number;
  level: Level;
  fileid: string;
  paperKey: string;
  q: { n: string; primary: string }[];
};

const sourceTags: SourceTag[] = JSON.parse(readFileSync(
  resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese-written-2019-2022.json'),
  'utf8',
));

const uploadManifest = readFileSync(
  resolve(__dirname, '../scripts/paper-trail/publish/audit-reupload.tsv'),
  'utf8',
);

describe('Japanese 2019-2022 written answer coverage', () => {
  it.each(specs)('$year $level preserves every original card and stable ID', spec => {
    const map = loadMap(spec);
    expect(map.q).toHaveLength(spec.total);
    expect(map.q.map(question => question.n)).toEqual(
      map.q.map((_, index) => String(index + 1)),
    );
    expect(digest(map.q.slice(0, spec.base))).toBe(spec.baseHash);
  });

  it.each(specs)('$year $level presents the stable IDs in physical paper order', spec => {
    const map = loadMap(spec);
    expect(map.q.map(question => question.printOrder).sort((a, b) => a! - b!))
      .toEqual(map.q.map((_, index) => index + 1));
    const displayed = questionsInDisplayOrder(map.q);
    for (let index = 1; index < displayed.length; index++) {
      const prior = displayed[index - 1];
      const current = displayed[index];
      expect(
        current.pP > prior.pP || (current.pP === prior.pP && current.pY[0] > prior.pY[0]),
        `${current.label} must follow ${prior.label}`,
      ).toBe(true);
    }
  });

  it.each(specs)('$year $level exposes bounded paper/scheme crops for every recovered card', spec => {
    const map = loadMap(spec);
    for (const question of map.q.slice(spec.base)) {
      expect(paperRegionFor(map.q, question.n), `${question.label} paper crop`).not.toBeNull();
      expect(question.endP, `${question.label} explicit paper end`).toBeGreaterThanOrEqual(question.pP);
      expect(question.region.length, `${question.label} scheme crop`).toBeGreaterThan(0);
      for (const region of question.region) {
        expect(region.p).toBeGreaterThanOrEqual(map.band[0]);
        expect(region.p).toBeLessThan(map.band[1]);
        expect(region.r?.[1]).toBeGreaterThanOrEqual(0);
        expect(region.r?.[3]).toBeLessThanOrEqual(1);
        expect(region.r?.[3]).toBeGreaterThan(region.r?.[1] ?? 1);
      }
    }
  });

  it.each(specs)('$year $level retains all five written-paper question families', spec => {
    const labels = loadMap(spec).q.map(question => question.label ?? '');
    for (const family of ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']) {
      expect(labels.some(label => label.startsWith(family)), `${family} missing`).toBe(true);
    }
  });

  it.each(specs)('$year $level has a complete source-type and skills crosswalk', spec => {
    const record = sourceTags.find(tag => (
      tag.year === spec.year
      && tag.level === spec.level
      && tag.fileid === spec.fileid
      && tag.paperKey === 'single'
    ));
    expect(record).toBeDefined();
    expect(record?.q.map(question => question.n)).toEqual(
      spec.topics.map((_, index) => String(index + 1)),
    );
    expect(record?.q.map(question => question.primary)).toEqual(spec.topics);
  });

  it.each(specs)('$year $level is included in the audited upload set', spec => {
    const local = `scripts/paper-trail/answers/${spec.year}/${spec.fileid}.json`;
    const remote = `papers/lc/japanese/${spec.year}/answers/${spec.fileid}.json`;
    expect(uploadManifest).toContain(`${local}\t${remote}`);
  });
});
