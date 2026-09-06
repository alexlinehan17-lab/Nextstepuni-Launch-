/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * LCVP Link Modules reference-parity and preservation gates.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import linkModulesBaselineJson from './fixtures/linkModulesTopicQuestionBaseline.json';
import { subjectAtlasStats, topicsForPaper, topicsForSubject } from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
  retainedLocalExamTopicAssociations,
} from '../data/examTopics/registry';

const topicLabels = [
  '1. Career Investigation',
  '1. Introduction to Working Life',
  '1. Job Seeking Skills',
  '1. Work Placement',
  '2. An Enterprise Activity',
  '2. Enterprise Skills',
  '2. Local Business Enterprises',
  '2. Local Voluntary/Community Enterprises',
  'Audio Visual',
  'Case Study',
];

type Baseline = Array<{
  level: 'common';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: 'single';
  questions: string[];
}>;

describe('LCVP Link Modules exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('link-modules')!;
  const baseline = linkModulesBaselineJson as Baseline;

  it('pins the exact ten-topic common-level reference menu', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Common Level']);
    expect(taxonomy.topics.map(topic => topic.label)).toEqual(topicLabels);
    expect(taxonomy.topics.every(topic => topic.level === 'common')).toBe(true);
    expect(topicsForSubject('link-modules')).toHaveLength(10);
  });

  it('crosswalks all content and assessment-format buckets to real curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('normalises section-restarting question numbers to Paper Trail identities', () => {
    const references = examQuestionPartReferencesForSubject('link-modules');
    expect(references).toHaveLength(348);
    expect(references.filter(reference => reference.sitting === 'main')).toHaveLength(318);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(30);
    expect(references.some(reference => reference.n === '1' && reference.subdivision.includes('Question 1-8'))).toBe(true);
    expect(references.some(reference => reference.n === '8' && reference.subdivision.includes('Question 1-8'))).toBe(true);
    expect(references.some(reference => reference.n === '9' && reference.subdivision.includes('Question 1-3'))).toBe(true);
    expect(references.some(reference => reference.n === '11' && reference.subdivision.includes('Question 1-3'))).toBe(true);
    expect(references.some(reference => reference.n === '12' && reference.subdivision.includes('Section C'))).toBe(true);
  });

  it('covers all 295 local main-paper question identities through 2026', () => {
    for (let year = 2010; year <= 2020; year++) {
      for (let number = 1; number <= 17; number++) {
        expect(
          examTopicIdsForQuestion('link-modules', 'common', year, 'main', String(number)),
          `${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
    for (let year = 2021; year <= 2026; year++) {
      for (let number = 1; number <= 18; number++) {
        expect(
          examTopicIdsForQuestion('link-modules', 'common', year, 'main', String(number)),
          `${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
  });

  it('records all reference omissions without dropping a local question', () => {
    const retained = retainedLocalExamTopicAssociations.filter(item => item.subjectId === 'link-modules');
    expect(retained).toHaveLength(25);
    expect(retained.every(item => item.reason?.includes('omitted'))).toBe(true);
  });

  it('preserves every exact pre-migration paper/question identity', () => {
    expect(baseline).toHaveLength(16);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'link-modules',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('adds the anchored 2026 paper and keeps printed-question counts distinct', () => {
    expect(subjectAtlasStats('link-modules')).toMatchObject({
      questions: 295,
      topics: 10,
      yearMin: 2010,
      yearMax: 2026,
    });
  });

  it('stores mock counts only, never commercial mock content', () => {
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0)).toBe(120);
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
