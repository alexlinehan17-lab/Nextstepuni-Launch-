/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Classical Studies reference-parity and non-destructive migration gates.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import classicalStudiesBaselineJson from './fixtures/classicalStudiesTopicQuestionBaseline.json';
import { subjectAtlasStats, topicsForPaper, topicsForSubject } from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
  retainedLocalExamTopicAssociations,
} from '../data/examTopics/registry';

const topicLabels = [
  'Funerary Practices',
  'Greek Drama',
  'Mythology',
  'Philosophy',
  'Power and Identity',
  'Roman Spectacle',
  'Temples',
  'World of Heroes',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: 'single';
  questions: string[];
}>;

describe('Classical Studies exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('classical-studies')!;
  const baseline = classicalStudiesBaselineJson as Baseline;

  it('pins the exact eight-topic menu at both levels', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Higher Level', 'Ordinary Level']);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label)).toEqual(topicLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label)).toEqual(topicLabels);
    expect(topicsForSubject('classical-studies')).toHaveLength(16);
  });

  it('crosswalks every exam bucket to existing official-curriculum nodes', () => {
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
    const references = examQuestionPartReferencesForSubject('classical-studies');
    expect(references).toHaveLength(353);
    expect(references.filter(reference => reference.sitting === 'main')).toHaveLength(315);
    expect(references.filter(reference => reference.sitting === 'sample')).toHaveLength(38);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
  });

  it('covers every anchored main-paper question from 2010–2026', () => {
    for (const level of ['higher', 'ordinary'] as const) {
      for (let year = 2010; year <= 2026; year++) {
        if (level === 'ordinary' && year === 2020) continue;
        const questionCount = year >= 2023 ? 16 : 10;
        for (let number = 1; number <= questionCount; number++) {
          expect(
            examTopicIdsForQuestion('classical-studies', level, year, 'main', String(number)),
            `${level}|${year}|Q${number}`,
          ).not.toEqual([]);
        }
      }
    }
  });

  it('records all 153 reference omissions instead of dropping local questions', () => {
    const retained = retainedLocalExamTopicAssociations.filter(item => item.subjectId === 'classical-studies');
    expect(retained).toHaveLength(153);
    expect(retained.filter(item => item.year === 2026)).toHaveLength(32);
    expect(retained.every(item => item.reason?.includes('retained'))).toBe(true);
  });

  it('preserves every exact pre-migration paper/question identity', () => {
    expect(baseline).toHaveLength(11);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'classical-studies',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('surfaces all 378 distinct local questions without inflating translations', () => {
    expect(subjectAtlasStats('classical-studies')).toMatchObject({
      questions: 378,
      topics: 16,
      yearMin: 2010,
      yearMax: 2026,
    });
  });

  it('stores no commercial mock content', () => {
    expect(taxonomy.topics.every(topic => topic.mockQuestionCount === 0)).toBe(true);
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
