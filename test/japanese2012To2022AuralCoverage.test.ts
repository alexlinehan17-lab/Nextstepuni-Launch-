/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Japanese listening papers use four independently numbered Parts. These
 * regressions preserve the stable identities that shipped before repair,
 * retain every available 2012-2022 variant, and lock its StudyClix-reference
 * Part-to-topic crosswalk to the official SEC paper and marking scheme.
 */

import { createHash } from 'node:crypto';
import { readFileSync, readdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import {
  paperRegionFor,
  questionsInDisplayOrder,
  schemeRegionFor,
} from '../components/PaperTrail/paperRegion';
import type { PaperAnswerMap, PaperAnswerQuestion } from '../types/paperTrail';

type LevelCode = 'A' | 'G';
type LanguageCode = 'E' | 'I' | 'B';
type ListeningTopic = 'japanese-6-0' | 'japanese-6-1' | 'japanese-6-2';

type MapSpec = {
  year: number;
  levelCode: LevelCode;
  languageCode: LanguageCode;
};

type RepairSpec = MapSpec & {
  base: number;
  total: number;
  baseHash: string;
  parts: Record<string, number>;
};

type TopicTag = {
  subjectId: string;
  year: number;
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  fileid: string;
  paperKey: string;
  q: { n: string; primary: string }[];
};

const CONVERSATION = 'japanese-6-0' as const;
const INTERVIEW = 'japanese-6-1' as const;
const RADIO = 'japanese-6-2' as const;

const topicsByPart: Record<number, readonly ListeningTopic[]> = {
  2012: [CONVERSATION, CONVERSATION, RADIO, INTERVIEW],
  2013: [CONVERSATION, RADIO, CONVERSATION, INTERVIEW],
  2014: [CONVERSATION, RADIO, CONVERSATION, CONVERSATION],
  2015: [INTERVIEW, RADIO, CONVERSATION, CONVERSATION],
  2016: [INTERVIEW, CONVERSATION, RADIO, CONVERSATION],
  2017: [INTERVIEW, RADIO, CONVERSATION, CONVERSATION],
  2018: [CONVERSATION, RADIO, CONVERSATION, CONVERSATION],
  2019: [INTERVIEW, RADIO, CONVERSATION, CONVERSATION],
  2020: [INTERVIEW, INTERVIEW, RADIO, CONVERSATION],
  2021: [INTERVIEW, RADIO, INTERVIEW, CONVERSATION],
  2022: [INTERVIEW, RADIO, CONVERSATION, CONVERSATION],
};

const codesByYear: Record<number, readonly string[]> = {
  2012: ['AE', 'AI', 'GE', 'GI'],
  2013: ['AE', 'AI', 'GE', 'GI'],
  2014: ['AE', 'AI', 'GE', 'GI'],
  2015: ['AE', 'AI', 'GE', 'GI'],
  2016: ['AE', 'AI', 'GE', 'GI'],
  2017: ['AE', 'GE', 'GI'],
  2018: ['AE', 'AI', 'GE', 'GI'],
  2019: ['AB', 'GB'],
  2020: ['AB'],
  2021: ['AB', 'GB'],
  2022: ['AB', 'GB'],
};

const allSpecs: readonly MapSpec[] = Object.entries(codesByYear).flatMap(([year, codes]) =>
  codes.map(code => ({
    year: Number(year),
    levelCode: code[0] as LevelCode,
    languageCode: code[1] as LanguageCode,
  })),
);

const repairs: readonly RepairSpec[] = [
  {
    year: 2013, levelCode: 'G', languageCode: 'E', base: 9, total: 18,
    baseHash: '1119584f6536d40cded230c355facb50a9a2d3985a6d64a49c03ea7f3153531b',
    parts: { 'PART A': 4, 'PART B': 2, 'PART C': 3, 'PART D': 9 },
  },
  {
    year: 2013, levelCode: 'G', languageCode: 'I', base: 9, total: 18,
    baseHash: '9170d7b1e53ae79543d4bbf7244290f77b580af87258ef44bd642f60f0a4cb1d',
    parts: { 'PART A': 4, 'PART B': 2, 'PART C': 3, 'PART D': 9 },
  },
  {
    year: 2014, levelCode: 'G', languageCode: 'E', base: 6, total: 14,
    baseHash: '2d83970cf32d80661e37152bf872fe7f6ef4d73cbb4c63b46e9e4612bbc0f7fd',
    parts: { 'PART A': 3, 'PART B': 3, 'PART C': 2, 'PART D': 6 },
  },
  {
    year: 2014, levelCode: 'G', languageCode: 'I', base: 6, total: 14,
    baseHash: 'ad7e9df92fdf1c86d53962af72bf920aa18d082def63c2a4608014bcdf935dd5',
    parts: { 'PART A': 3, 'PART B': 3, 'PART C': 2, 'PART D': 6 },
  },
  {
    year: 2015, levelCode: 'A', languageCode: 'E', base: 7, total: 15,
    baseHash: '7704e03fd80b174d6ae62adb72c1fbb6ad15216d521f21a0749555cd77ce210d',
    parts: { 'PART A': 3, 'PART B': 3, 'PART C': 2, 'PART D': 7 },
  },
  {
    year: 2015, levelCode: 'A', languageCode: 'I', base: 7, total: 15,
    baseHash: 'ae20358ac41a17fba64a050608beec55fb1a400fdba7ae876d74d28a8f0ade60',
    parts: { 'PART A': 3, 'PART B': 3, 'PART C': 2, 'PART D': 7 },
  },
  {
    year: 2015, levelCode: 'G', languageCode: 'E', base: 6, total: 14,
    baseHash: 'f28ba1114abd6291b61868405510f2455924a72193e62b3715848a6ea81993cc',
    parts: { 'PART A': 3, 'PART B': 3, 'PART C': 2, 'PART D': 6 },
  },
  {
    year: 2015, levelCode: 'G', languageCode: 'I', base: 6, total: 14,
    baseHash: 'fcf4a529dbb63d377ea01c0f6cb0cb69b35527f0f64a94f2541e64450c0b045b',
    parts: { 'PART A': 3, 'PART B': 3, 'PART C': 2, 'PART D': 6 },
  },
  {
    year: 2016, levelCode: 'G', languageCode: 'E', base: 6, total: 14,
    baseHash: 'aa3a8b53367648be49fabb5a25ba9885d15144257bfafef75c3543a76c36eb09',
    parts: { 'PART A': 3, 'PART B': 2, 'PART C': 3, 'PART D': 6 },
  },
  {
    year: 2016, levelCode: 'G', languageCode: 'I', base: 6, total: 14,
    baseHash: '26ba3793ed0e561f2952f5554ea6cabe334fe208c1f534df37138b13f2a96dc6',
    parts: { 'PART A': 3, 'PART B': 2, 'PART C': 3, 'PART D': 6 },
  },
];

const fileidFor = (spec: MapSpec) =>
  `LC058${spec.levelCode}LPA00${spec.languageCode}V.pdf`;

const loadMap = (spec: MapSpec): PaperAnswerMap => JSON.parse(readFileSync(
  resolve(__dirname, `../scripts/paper-trail/answers/${spec.year}/${fileidFor(spec)}.json`),
  'utf8',
));

const levelFor = (spec: MapSpec) => spec.levelCode === 'A' ? 'higher' : 'ordinary';
const languageFor = (spec: MapSpec) => spec.languageCode === 'I' ? 'iv' : 'ev';

const partFor = (question: PaperAnswerQuestion) => {
  const match = question.label?.match(/(?:PART|CUID)\s*([A-D])/i);
  if (!match) throw new Error(`Card ${question.n} has no Japanese listening Part label`);
  return match[1].toUpperCase().charCodeAt(0) - 65;
};

const expectedTopics = (spec: MapSpec, map: PaperAnswerMap) =>
  map.q.map(question => topicsByPart[spec.year][partFor(question)]);

const protectedQuestion = ({
  label: _label,
  printOrder: _printOrder,
  schemeRegion: _schemeRegion,
  paperRegion: _paperRegion,
  endP: _endP,
  endY: _endY,
  ...question
}: PaperAnswerQuestion) => question;

const digest = (questions: PaperAnswerQuestion[]) => createHash('sha256')
  .update(JSON.stringify(questions.map(protectedQuestion)))
  .digest('hex');

const sourceTags: TopicTag[] = JSON.parse(readFileSync(
  resolve(__dirname, '../scripts/paper-trail/topic-tags/tags/japanese.json'),
  'utf8',
));

const aggregateTags: TopicTag[] = JSON.parse(readFileSync(
  resolve(__dirname, '../data/paperTrail/paperTopicTags.json'),
  'utf8',
));

const uploadManifest = readFileSync(
  resolve(__dirname, '../scripts/paper-trail/publish/audit-reupload.tsv'),
  'utf8',
);

const matchingTags = (tags: TopicTag[], spec: MapSpec) => tags.filter(tag =>
  tag.subjectId === 'japanese'
  && tag.year === spec.year
  && tag.level === levelFor(spec)
  && tag.lang === languageFor(spec)
  && tag.fileid === fileidFor(spec)
  && tag.paperKey === 'aural');

const partCounts = (map: PaperAnswerMap) => map.q.reduce<Record<string, number>>((out, q) => {
  const part = q.label?.match(/PART [A-D]/i)?.[0].toUpperCase() ?? 'unlabelled';
  out[part] = (out[part] ?? 0) + 1;
  return out;
}, {});

describe('Japanese 2012-2022 listening answer coverage', () => {
  it('covers exactly all 34 locally available paper variants', () => {
    const discovered = Object.keys(codesByYear).flatMap(year =>
      readdirSync(resolve(__dirname, `../scripts/paper-trail/answers/${year}`))
        .filter(name => /^LC058[AG]LPA00[EIB]V\.pdf\.json$/.test(name))
        .map(name => `${year}/${name}`),
    ).sort();
    const expected = allSpecs.map(spec => `${spec.year}/${fileidFor(spec)}.json`).sort();
    expect(allSpecs).toHaveLength(34);
    expect(discovered).toEqual(expected);
  });

  it.each(allSpecs)('$year $levelCode $languageCode keeps every card reachable and bounded', spec => {
    const map = loadMap(spec);
    const repair = repairs.find(candidate => fileidFor(candidate) === fileidFor(spec)
      && candidate.year === spec.year);
    expect(map.q).toHaveLength(repair?.total ?? 4);
    expect(map.q.map(question => question.n)).toEqual(
      map.q.map((_, index) => String(index + 1)),
    );
    for (const question of map.q) {
      expect(paperRegionFor(map.q, question.n), `${question.label} paper crop`).not.toBeNull();
      expect(question.mode, `${question.label} scheme mode`).toBe('crop');
      const schemeRegion = schemeRegionFor(question);
      expect(schemeRegion.length, `${question.label} scheme crop`).toBeGreaterThan(0);
      for (const region of schemeRegion) {
        expect(region.r[1]).toBeGreaterThanOrEqual(0);
        expect(region.r[3]).toBeLessThanOrEqual(1);
        expect(region.r[3]).toBeGreaterThan(region.r[1]);
      }
    }
  });

  it.each(allSpecs)('$year $levelCode $languageCode has one exact source and aggregate topic map', spec => {
    const map = loadMap(spec);
    for (const tags of [sourceTags, aggregateTags]) {
      const matches = matchingTags(tags, spec);
      expect(matches, `${spec.year} ${fileidFor(spec)} tag identity`).toHaveLength(1);
      expect(matches[0].q.map(question => question.n)).toEqual(
        map.q.map(question => question.n),
      );
      expect(matches[0].q.map(question => question.primary)).toEqual(
        expectedTopics(spec, map),
      );
    }
  });

  it.each(repairs)('$year $levelCode $languageCode preserves every pre-repair card', spec => {
    const map = loadMap(spec);
    expect(digest(map.q.slice(0, spec.base))).toBe(spec.baseHash);
    expect(partCounts(map)).toEqual(spec.parts);
  });

  it.each(repairs)('$year $levelCode $languageCode has a complete physical order', spec => {
    const map = loadMap(spec);
    expect(map.q.map(question => question.printOrder).sort((a, b) => a! - b!))
      .toEqual(map.q.map((_, index) => index + 1));
    const displayed = questionsInDisplayOrder(map.q);
    for (let index = 1; index < displayed.length; index += 1) {
      const prior = displayed[index - 1];
      const current = displayed[index];
      expect(
        current.pP > prior.pP || (current.pP === prior.pP && current.pY[0] > prior.pY[0]),
        `${current.label} must follow ${prior.label}`,
      ).toBe(true);
    }
  });

  it.each(repairs)('$year $levelCode $languageCode caps Part A before the recovered Part B', spec => {
    const map = loadMap(spec);
    const lastPartA = questionsInDisplayOrder(map.q)
      .filter(question => question.label?.startsWith('PART A'))
      .at(-1)!;
    expect(lastPartA.endP).toBe(lastPartA.pP);
    expect(lastPartA.endY).toBe(lastPartA.pY[1]);
    expect(paperRegionFor(map.q, lastPartA.n)?.at(-1)?.p).toBe(lastPartA.pP);
  });

  it('uses audited additive display corrections without mutating legacy identities', () => {
    const maps = repairs.map(spec => loadMap(spec));
    const schemeCorrected = maps.flatMap(map => map.q.filter(question => question.schemeRegion));
    const paperCorrected = maps.flatMap(map => map.q.filter(question => question.paperRegion));
    expect(schemeCorrected).toHaveLength(13);
    expect(paperCorrected).toHaveLength(6);
    for (const question of schemeCorrected) {
      expect(schemeRegionFor(question)).toEqual(question.schemeRegion);
      expect(schemeRegionFor(question).every(region => region.p === 3)).toBe(true);
    }
    for (const question of paperCorrected) {
      expect(question.label).toMatch(/^PART A · [1-3]$/);
      expect(paperRegionFor([question], question.n)).toEqual(question.paperRegion);
    }
  });

  it.each(repairs)('$year $levelCode $languageCode is listed exactly once for audited upload', spec => {
    const fileid = fileidFor(spec);
    const expected = `scripts/paper-trail/answers/${spec.year}/${fileid}.json\t`
      + `papers/lc/japanese/${spec.year}/answers/${fileid}.json`;
    expect(uploadManifest.split('\n').filter(line => line === expected)).toHaveLength(1);
  });
});
