/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Agricultural Science reference-parity and non-destructive migration gates.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import agriculturalScienceBaselineJson from './fixtures/agriculturalScienceTopicQuestionBaseline.json';
import { subjectAtlasStats, topicsForPaper, topicsForSubject } from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
  retainedLocalExamTopicAssociations,
} from '../data/examTopics/registry';

const higherLabels = [
  'Animal Diseases',
  'Animal Physiology - Digestive System',
  'Animal Physiology - Reproductive Systems',
  'Beef Cattle',
  'Classification of Animals & Plants',
  'Coursework Project - 2025',
  'Coursework Project - 2026',
  'Crop Production',
  'Dairy Cattle',
  'Energy Crop & Catch Crop',
  'Fertilisers - Pollution - Environment - Cycles',
  'Genetics',
  'Grassland',
  'Innovation and Biotechnology in Agriculture',
  'Pigs',
  'Plant Physiology',
  'Scientific Practices - Experiments & Investigations',
  'Sheep',
  'Soil Science',
];

const ordinaryLabels = [
  'Animal Diseases',
  'Animal Physiology',
  'Animal Production',
  'Classification of Organisms',
  'Coursework Project - 2021',
  'COURSEWORK Project - 2022',
  'Coursework Project - 2023',
  'Crop Production',
  'Fertilisers, Pollution & the Environment',
  'Genetics',
  'Grassland',
  'Health & Safety',
  'Innovation and Biotechnology in Agriculture',
  'Plant Physiology',
  'Scientific Practices - Experiments & Investigations',
  'Soil Science',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: 'single';
  questions: string[];
}>;

describe('Agricultural Science exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('agricultural-science')!;
  const baseline = agriculturalScienceBaselineJson as Baseline;

  it('pins the exact 19 Higher and 16 Ordinary reference topics', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Higher Level', 'Ordinary Level']);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label)).toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label)).toEqual(ordinaryLabels);
    expect(topicsForSubject('agricultural-science')).toHaveLength(35);
  });

  it('crosswalks every browse topic to existing official-curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('retains every part-level reference heading as factual metadata', () => {
    const references = examQuestionPartReferencesForSubject('agricultural-science');
    expect(references).toHaveLength(1_027);
    expect(references.filter(reference => reference.sitting === 'main')).toHaveLength(923);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(45);
    expect(references.filter(reference => reference.sitting === 'sample')).toHaveLength(59);
    expect(references.some(reference => reference.n === '1' && reference.subdivision?.includes('Short question E'))).toBe(true);
    expect(references.every(reference => /^\d+$/.test(reference.n))).toBe(true);
  });

  it('covers all 458 local main-paper questions from 2010–2026', () => {
    for (let year = 2010; year <= 2020; year++) {
      for (let number = 1; number <= 9; number++) {
        expect(
          examTopicIdsForQuestion('agricultural-science', 'higher', year, 'main', String(number)),
          `higher|${year}|Q${number}`,
        ).not.toEqual([]);
      }
      for (let number = 1; number <= 13; number++) {
        expect(
          examTopicIdsForQuestion('agricultural-science', 'ordinary', year, 'main', String(number)),
          `ordinary|${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
    for (let year = 2021; year <= 2026; year++) {
      for (const level of ['higher', 'ordinary'] as const) {
        for (let number = 1; number <= 18; number++) {
          expect(
            examTopicIdsForQuestion('agricultural-science', level, year, 'main', String(number)),
            `${level}|${year}|Q${number}`,
          ).not.toEqual([]);
        }
      }
    }
  });

  it('records all 47 reference omissions explicitly', () => {
    const retained = retainedLocalExamTopicAssociations.filter(item => item.subjectId === 'agricultural-science');
    expect(retained).toHaveLength(47);
    expect(retained.some(item => item.level === 'higher' && item.year === 2021 && item.n === '4')).toBe(true);
    expect(retained.every(item => item.reason?.includes('omitted'))).toBe(true);
  });

  it('preserves every exact pre-migration paper/question identity', () => {
    expect(baseline).toHaveLength(55);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'agricultural-science',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('adds the previously untagged anchored papers without inflating translations', () => {
    expect(subjectAtlasStats('agricultural-science')).toMatchObject({
      questions: 458,
      topics: 35,
      yearMin: 2010,
      yearMax: 2026,
    });
  });

  it('stores mock counts but no commercial mock content', () => {
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0)).toBe(1_010);
    for (const topic of taxonomy.topics) {
      expect(Object.keys(topic).sort()).toEqual([
        'curriculumNodeIds',
        'id',
        'label',
        'level',
        'mockQuestionCount',
        'officialQuestionKeys',
        'sourcePath',
      ]);
    }
  });
});
