/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The original 2012-2018 Japanese written sidecars stopped after Question 3.
 * These regressions keep that repair additive: every original card retains its
 * stable ID and crop, while Q4/Q5 and granular Kanji/grammar/culture cards
 * remain reachable, tagged, physically ordered and publishable.
 */

import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { paperRegionFor, questionsInDisplayOrder } from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap, PaperAnswerQuestion } from '../types/paperTrail';

type LevelCode = 'A' | 'G';
type LanguageCode = 'E' | 'I';
type SkillTopic = 'japanese-5-4' | 'japanese-5-5' | 'japanese-5-6';
type SkillSpec = readonly [after: number, topic: SkillTopic];

type MapSpec = {
  year: number;
  levelCode: LevelCode;
  languageCode: LanguageCode;
  base: number;
  baseHash: string;
  skills: readonly SkillSpec[];
};

const KANJI = 'japanese-5-4' as const;
const GRAMMAR = 'japanese-5-5' as const;
const CULTURE = 'japanese-5-6' as const;

const specs: readonly MapSpec[] = [
  { year: 2012, levelCode: 'A', languageCode: 'E', base: 21, baseHash: '5ce0d30c996e8b43ac836e34c6cf022337775a7a2db92b64fdb66cd09e810c34', skills: [] },
  { year: 2012, levelCode: 'A', languageCode: 'I', base: 20, baseHash: '946767b1433f5e031c18d8850c1d8db8294c922c4f00394b74a2b2bb8f9273b7', skills: [] },
  { year: 2012, levelCode: 'G', languageCode: 'E', base: 14, baseHash: '7ae198df309ab7649134be6f46fcb070ebcb90d1541c14846aa9f97a27b39319', skills: [[14, KANJI], [14, GRAMMAR], [14, CULTURE]] },
  { year: 2012, levelCode: 'G', languageCode: 'I', base: 13, baseHash: '3954e2962a13c4103cfa71c88a8a6b9571d45e9b872b0e4289037da11ece62c6', skills: [[13, KANJI], [13, GRAMMAR], [13, CULTURE]] },
  { year: 2013, levelCode: 'A', languageCode: 'E', base: 3, baseHash: '1843db424c37b1a87718d2c5db4c46ee6e7e9840892242d241d15e59d49eeae6', skills: [[2, KANJI], [2, GRAMMAR], [3, KANJI]] },
  { year: 2013, levelCode: 'A', languageCode: 'I', base: 6, baseHash: '97c8135fa8b724303e9b57be76d05d735e0a2942260eff65cb65ed57899125a6', skills: [[5, KANJI], [5, GRAMMAR], [6, KANJI]] },
  { year: 2013, levelCode: 'G', languageCode: 'E', base: 3, baseHash: '91ea1a8a668e7b31ea4f30ad0534d497939137973d2f558afea0b376ea16a1b2', skills: [[2, CULTURE], [3, KANJI], [3, GRAMMAR], [3, GRAMMAR]] },
  { year: 2013, levelCode: 'G', languageCode: 'I', base: 8, baseHash: 'c1890fa6f0a97a1a7423f5c3c268805dcee389024cf0325e3860f4004b9e5c2e', skills: [[4, CULTURE]] },
  { year: 2014, levelCode: 'A', languageCode: 'E', base: 5, baseHash: '54f57f25106743fb7478c31cb4d37c56f03f36672f79058c7affdc610ec5247b', skills: [[3, KANJI], [3, GRAMMAR], [5, KANJI], [5, GRAMMAR]] },
  { year: 2014, levelCode: 'A', languageCode: 'I', base: 18, baseHash: '2c7f0372b3fd7ef2b7d0eec89052f81551051608050e162c020a2fbbc7323b96', skills: [[13, KANJI], [13, GRAMMAR], [18, KANJI], [18, GRAMMAR]] },
  { year: 2014, levelCode: 'G', languageCode: 'E', base: 13, baseHash: '9f0f5dabcd34910c027915610b11f3ca9033efa7caf7d217693d348c496a0abe', skills: [[9, CULTURE]] },
  { year: 2014, levelCode: 'G', languageCode: 'I', base: 12, baseHash: '0eda887a5d49a61a7938a5ba5b4a6a72634a116db63cf52d081cc234e61ada77', skills: [[8, KANJI], [8, GRAMMAR], [8, CULTURE]] },
  { year: 2015, levelCode: 'A', languageCode: 'E', base: 17, baseHash: '9c6173cb8983693f387346ce66b06f0fae007f7be9fb8927a43f53637e095941', skills: [[12, KANJI], [12, GRAMMAR], [17, KANJI], [17, GRAMMAR]] },
  { year: 2015, levelCode: 'A', languageCode: 'I', base: 8, baseHash: '286e395e2d5e3c279d01ae9800a463873b7a792d82c5cd2c17d8f9d2de0a94ae', skills: [[6, KANJI], [6, GRAMMAR], [8, KANJI], [8, GRAMMAR]] },
  { year: 2015, levelCode: 'G', languageCode: 'E', base: 16, baseHash: 'b6f4640702a8b9f478f482cfb095add85fa291a146c2bea2c7e88b2fb4187355', skills: [[10, CULTURE]] },
  { year: 2015, levelCode: 'G', languageCode: 'I', base: 12, baseHash: '51b733c58012cb1eeb2339f8fe0b8e90e5bd80e5a064d664b98be6e1aa16c2b0', skills: [[9, KANJI], [9, CULTURE], [12, GRAMMAR], [12, GRAMMAR]] },
  { year: 2016, levelCode: 'A', languageCode: 'E', base: 22, baseHash: 'd7a167cfad5755af3b5a45dc021cbd181940b759080b87d398fd37630d8a332f', skills: [] },
  { year: 2016, levelCode: 'A', languageCode: 'I', base: 19, baseHash: 'f9429d622e510744912cb9c4d320c4046c20993df4f4316e86a8a5e052d36239', skills: [[13, KANJI], [13, GRAMMAR], [19, KANJI], [19, GRAMMAR]] },
  { year: 2016, levelCode: 'G', languageCode: 'E', base: 14, baseHash: '8b31e5936dae7179376cb96fce2c545edb8ff729774237f3e4b0a2d1c6997308', skills: [[10, GRAMMAR], [10, KANJI], [14, CULTURE]] },
  { year: 2016, levelCode: 'G', languageCode: 'I', base: 14, baseHash: '7b4176b271cbf107c8a410bf3baae58f67ebaefdeae2902f1a8546950c8624a7', skills: [[10, GRAMMAR], [10, KANJI], [14, CULTURE]] },
  { year: 2017, levelCode: 'A', languageCode: 'E', base: 14, baseHash: '7f093510fdf597fc05ac2ff743d2de2e4ab947022ed3f146455bee5f63cc9117', skills: [[12, KANJI], [12, GRAMMAR], [14, KANJI], [14, GRAMMAR]] },
  { year: 2017, levelCode: 'A', languageCode: 'I', base: 20, baseHash: '400dbfde22bf1e385bd5564af5380237c4d9c75e68c033fbf50af87171a536ad', skills: [[12, KANJI], [12, GRAMMAR], [20, KANJI], [20, GRAMMAR]] },
  { year: 2017, levelCode: 'G', languageCode: 'E', base: 17, baseHash: '5cfca6640c6363574973cc285f4e6b419889fd21cb963675fc272ee147989c4b', skills: [[11, CULTURE]] },
  { year: 2017, levelCode: 'G', languageCode: 'I', base: 11, baseHash: '746693b93dc30eb06628fd3027d3d8dcfbf92301a8125a9d280015d17901bfd0', skills: [] },
  { year: 2018, levelCode: 'A', languageCode: 'E', base: 23, baseHash: '4b2983b53402794616fe910b591b9654c7b0880590b33a14bb996408dba26212', skills: [[14, KANJI], [14, GRAMMAR], [23, KANJI], [23, GRAMMAR]] },
  { year: 2018, levelCode: 'A', languageCode: 'I', base: 21, baseHash: '2b314421ff93a42911d2c8e6d72f5ba6508a98904d6f38d43397d518edf19858', skills: [[14, KANJI], [14, GRAMMAR], [21, KANJI], [21, GRAMMAR]] },
  { year: 2018, levelCode: 'G', languageCode: 'E', base: 3, baseHash: '66f5b4b2d4ebed903e5970fa82fa40c6b7f192494661009e04be46fbeb7e81f1', skills: [[2, KANJI], [2, CULTURE], [3, GRAMMAR]] },
  { year: 2018, levelCode: 'G', languageCode: 'I', base: 18, baseHash: 'f151c1f3c9432425e164b309e584b8c6e428e41226feebdf353f596c73940045', skills: [[11, KANJI], [11, CULTURE], [18, GRAMMAR]] },
];

const fileidFor = (spec: MapSpec) =>
  `LC058${spec.levelCode}LP000${spec.languageCode}V.pdf`;

const loadMap = (spec: MapSpec): PaperAnswerMap => JSON.parse(readFileSync(
  resolve(__dirname, `../scripts/paper-trail/answers/${spec.year}/${fileidFor(spec)}.json`),
  'utf8',
));

const withoutPrintOrder = (question: PaperAnswerQuestion) => {
  const preserved = { ...question };
  delete preserved.printOrder;
  return preserved;
};

const digest = (questions: PaperAnswerQuestion[]) => createHash('sha256')
  .update(JSON.stringify(questions.map(withoutPrintOrder)))
  .digest('hex');

const expectedDisplayIds = (spec: MapSpec) => {
  const inserted = new Map<number, string[]>();
  spec.skills.forEach(([after], index) => {
    const stableId = String(spec.base + 3 + index);
    inserted.set(after, [...(inserted.get(after) ?? []), stableId]);
  });
  const ids: string[] = [];
  for (let stableId = 1; stableId <= spec.base; stableId += 1) {
    ids.push(String(stableId), ...(inserted.get(stableId) ?? []));
  }
  ids.push(String(spec.base + 1), String(spec.base + 2));
  return ids;
};

type SourceTag = {
  year: number;
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  fileid: string;
  paperKey: string;
  q: { n: string; primary: string }[];
};

const sourceTags: SourceTag[] = JSON.parse(readFileSync(
  resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'),
  'utf8',
));

const aggregateTags: SourceTag[] = JSON.parse(readFileSync(
  resolve(__dirname, '../data/paperTrail/paperTopicTags.json'),
  'utf8',
));

const uploadManifest = readFileSync(
  resolve(__dirname, '../scripts/paper-trail/publish/audit-reupload.tsv'),
  'utf8',
);

const tagFor = (tags: SourceTag[], spec: MapSpec) => tags.find(tag =>
  tag.year === spec.year && tag.fileid === fileidFor(spec) && tag.paperKey === 'single');

describe('Japanese 2012-2018 written answer coverage', () => {
  it.each(specs)('$year $levelCode $languageCode preserves every original card and stable ID', spec => {
    const map = loadMap(spec);
    expect(map.q).toHaveLength(spec.base + 2 + spec.skills.length);
    expect(map.q.map(question => question.n)).toEqual(
      map.q.map((_, index) => String(index + 1)),
    );
    expect(digest(map.q.slice(0, spec.base))).toBe(spec.baseHash);
    expect(map.q.slice(spec.base, spec.base + 2).map(question => question.label)).toEqual([
      expect.stringMatching(/^Q4 · /),
      expect.stringMatching(/^Q5 · /),
    ]);
  });

  it.each(specs)('$year $levelCode $languageCode exposes the intended physical display order', spec => {
    const map = loadMap(spec);
    const displayed = questionsInDisplayOrder(map.q);
    const ranks = map.q.map(question => question.printOrder);
    expect([...ranks].sort((a, b) => Number(a) - Number(b))).toEqual(
      map.q.map((_, index) => index + 1),
    );
    expect(displayed.map(question => question.n)).toEqual(expectedDisplayIds(spec));
  });

  it.each(specs)('$year $levelCode $languageCode exposes bounded recovered paper and scheme crops', spec => {
    const map = loadMap(spec);
    for (const question of map.q.slice(spec.base)) {
      const paperRegions = paperRegionFor(map.q, question.n);
      expect(paperRegions).not.toBeNull();
      expect(paperRegions?.[0].p).toBe(question.pP);
      expect(paperRegions?.at(-1)?.p).toBe(question.endP);
      expect(question.endP! - question.pP).toBeLessThanOrEqual(3);
      expect(question.region.length).toBeGreaterThan(0);
      expect(question.region.map(region => region.p)).toEqual(
        [...question.region.map(region => region.p)].sort((a, b) => a - b),
      );
      for (const region of question.region) {
        expect(region.r[1]).toBeGreaterThanOrEqual(0);
        expect(region.r[3]).toBeLessThanOrEqual(1);
        expect(region.r[3]).toBeGreaterThan(region.r[1]);
      }
    }
  });

  it.each(specs)('$year $levelCode $languageCode tags every retained and recovered card', spec => {
    const map = loadMap(spec);
    for (const tags of [sourceTags, aggregateTags]) {
      const record = tagFor(tags, spec);
      expect(record, `${spec.year} ${fileidFor(spec)} tag record`).toBeDefined();
      expect(record?.q.map(question => question.n)).toEqual(map.q.map(question => question.n));
      expect(record?.q.slice(spec.base)).toEqual([
        { n: String(spec.base + 1), primary: 'japanese-5-7' },
        { n: String(spec.base + 2), primary: 'japanese-5-7' },
        ...spec.skills.map(([, topic], index) => ({
          n: String(spec.base + 3 + index),
          primary: topic,
        })),
      ]);
    }
  });

  it.each(specs)('$year $levelCode $languageCode is listed exactly once for audited upload', spec => {
    const fileid = fileidFor(spec);
    const expected = `scripts/paper-trail/answers/${spec.year}/${fileid}.json\t` +
      `papers/lc/japanese/${spec.year}/answers/${fileid}.json`;
    expect(uploadManifest.split('\n').filter(line => line === expected)).toHaveLength(1);
  });
});
