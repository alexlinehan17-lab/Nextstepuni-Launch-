/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Politics & Society reference-parity and preservation gates.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import politicsAndSocietyBaselineJson from './fixtures/politicsAndSocietyTopicQuestionBaseline.json';
import { subjectAtlasStats, topicsForPaper, topicsForSubject } from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
  retainedLocalExamTopicAssociations,
} from '../data/examTopics/registry';

const topicLabels = [
  '1. Power and Decision-Making at National and European Level',
  '1. Power and Decision-Making in the School',
  '2. Effectively Contributing to Communities',
  '2. Rights and Responsibilities in Communication with Others',
  '3. Human Rights and Responsibilities in Europe and the Wider World',
  '3. Human Rights and Responsibilities in Ireland',
  '4. Globalisation and Identity',
  '4. Sustainable Development',
  'Data-Based Questions',
  'Key Thinkers',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: 'single';
  questions: string[];
}>;

describe('Politics and Society exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('politics-and-society')!;
  const baseline = politicsAndSocietyBaselineJson as Baseline;

  it('pins the exact ten-topic reference menu at both levels', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Higher Level', 'Ordinary Level']);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label)).toEqual(topicLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label)).toEqual(topicLabels);
    expect(topicsForSubject('politics-and-society')).toHaveLength(20);
  });

  it('crosswalks all content and assessment-lens buckets to real curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('normalises lettered and data-based sections to Paper Trail card identities', () => {
    const references = examQuestionPartReferencesForSubject('politics-and-society');
    expect(references).toHaveLength(550);
    expect(references.filter(reference => reference.sitting === 'main')).toHaveLength(467);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(27);
    expect(references.filter(reference => reference.sitting === 'sample')).toHaveLength(56);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);

    const ordinary2026Dbq = references.filter(reference =>
      reference.level === 'ordinary'
      && reference.year === 2026
      && reference.sitting === 'main'
      && reference.topicId === 'politics-and-society-ordinary-data-based-questions');
    expect([...new Set(ordinary2026Dbq.map(reference => reference.n))]).toEqual(['2', '3', '4']);
  });

  it('covers every anchored main-paper question from 2018–2026', () => {
    for (let year = 2018; year <= 2026; year++) {
      const higherCount = year <= 2020 ? 6 : 7;
      for (let number = 1; number <= higherCount; number++) {
        expect(
          examTopicIdsForQuestion('politics-and-society', 'higher', year, 'main', String(number)),
          `higher|${year}|Q${number}`,
        ).not.toEqual([]);
      }
      if (year === 2020) continue;
      for (let number = 1; number <= 10; number++) {
        expect(
          examTopicIdsForQuestion('politics-and-society', 'ordinary', year, 'main', String(number)),
          `ordinary|${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
  });

  it('records the two reference omissions instead of dropping valid local cards', () => {
    const retained = retainedLocalExamTopicAssociations.filter(item => item.subjectId === 'politics-and-society');
    expect(retained).toHaveLength(2);
    expect(retained.map(item => `${item.level}|${item.year}|${item.n}`).sort()).toEqual([
      'higher|2018|4',
      'higher|2024|2',
    ]);
    expect(retained.every(item => item.reason?.includes('retained'))).toBe(true);
  });

  it('preserves every exact pre-migration paper/question identity', () => {
    expect(baseline).toHaveLength(9);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'politics-and-society',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('surfaces all 140 distinct local cards without inflating translations', () => {
    expect(subjectAtlasStats('politics-and-society')).toMatchObject({
      questions: 140,
      topics: 20,
      yearMin: 2018,
      yearMax: 2026,
    });
  });

  it('stores mock counts only, never commercial mock content', () => {
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0)).toBe(471);
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
