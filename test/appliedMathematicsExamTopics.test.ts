/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Applied Mathematics parity and preservation gates. Reference data contains
 * factual headings only; commercial question text and solutions stay excluded.
 */

import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
import appliedMathematicsBaselineJson from './fixtures/appliedMathematicsTopicQuestionBaseline.json';
import {
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
  retainedLocalExamTopicAssociations,
} from '../data/examTopics/registry';

const higherLabels = [
  'Circular Motion',
  'Difference Equations',
  'Differential Equations',
  'Further Integration (u-substitution, integration by parts)',
  "Hooke's Law",
  'Impacts & Collisions',
  'Integration',
  'Mathematical Modelling Project',
  'Networks and Graphs',
  "Newton's laws & Connected Particles",
  'Optimal & Critical Paths',
  'Projectiles',
  'Uniform Accelerated Motion',
  'Vectors',
  'Work, Power, Energy & Momentum',
];

const ordinaryLabels = [
  'Centre of Gravity',
  'Circular Motion',
  'Difference Equations',
  'Differential Equations',
  'Dimensional Analysis',
  'Hydrostatics',
  'Impacts & Collisions',
  'Linear Motion',
  'Mathematical Modelling Project',
  'Networks & Graphs',
  "Newton's Laws & Connected Particles",
  'Optimal & Critical Paths',
  'Projectiles',
  'Relative Velocity',
  'Statics',
  'Uniform Accelerated Motion',
  'Vectors',
  'Work, Energy, Power & Momentum',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: 'single';
  questions: string[];
}>;

describe('Applied Mathematics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('applied-mathematics')!;
  const baseline = appliedMathematicsBaselineJson as Baseline;

  it('pins the exact level-aware reference menu, including empty buckets', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => group.label)).toEqual(['Higher Level', 'Ordinary Level']);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label)).toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label)).toEqual(ordinaryLabels);
    expect(topicsForSubject('applied-mathematics')).toHaveLength(33);
  });

  it('crosswalks every exam topic to real official-curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM.flatMap(subject => subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id))),
    );
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids.length, `${topic.id} has no curriculum crosswalk`).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned curriculum ids`).toEqual([]);
    }
  });

  it('retains part-level reference provenance without copying question text', () => {
    const references = examQuestionPartReferencesForSubject('applied-mathematics');
    expect(references).toHaveLength(369);
    expect(references.filter(reference => reference.sitting === 'main')).toHaveLength(308);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(26);
    expect(references.filter(reference => reference.sitting === 'sample')).toHaveLength(35);
    expect(references.every(reference => /^\d+$/.test(reference.n))).toBe(true);
    expect(references.every(reference => Object.keys(reference).every(key => [
      'subjectId', 'level', 'year', 'sitting', 'paperKey', 'n', 'subdivision', 'topicId',
    ].includes(key)))).toBe(true);
  });

  it('covers every local main-paper question from 2010–2026', () => {
    for (let year = 2010; year <= 2026; year++) {
      for (let number = 1; number <= 10; number++) {
        expect(
          examTopicIdsForQuestion('applied-mathematics', 'higher', year, 'main', String(number)),
          `higher|${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
    for (const year of [...Array.from({ length: 10 }, (_, index) => 2010 + index), 2021, 2022]) {
      for (let number = 1; number <= 9; number++) {
        expect(
          examTopicIdsForQuestion('applied-mathematics', 'ordinary', year, 'main', String(number)),
          `ordinary|${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
    for (let year = 2023; year <= 2026; year++) {
      for (let number = 1; number <= 10; number++) {
        expect(
          examTopicIdsForQuestion('applied-mathematics', 'ordinary', year, 'main', String(number)),
          `ordinary|${year}|Q${number}`,
        ).not.toEqual([]);
      }
    }
  });

  it('records all 113 reference omissions as explicit preservation associations', () => {
    const retained = retainedLocalExamTopicAssociations.filter(item => item.subjectId === 'applied-mathematics');
    expect(retained).toHaveLength(113);
    expect(retained.every(item => item.reason?.includes('omitted from the reference'))).toBe(true);
  });

  it('preserves every exact pre-migration paper/question identity', () => {
    expect(baseline).toHaveLength(50);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'applied-mathematics',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`).not.toBeNull();
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('adds all anchored 2023–2026 questions and reports distinct printed totals', () => {
    for (const entry of PAPER_TRAIL_INDEX['applied-mathematics'].filter(entry => entry.year >= 2023)) {
      for (const paper of entry.papers.filter(paper => paper.answers === 1)) {
        const live = topicsForPaper('applied-mathematics', entry.year, entry.level, entry.lang, paper.doc.f);
        expect(live, `${entry.level}|${entry.lang}|${entry.year}`).not.toBeNull();
        expect(live!.q).toHaveLength(10);
      }
    }
    expect(subjectAtlasStats('applied-mathematics')).toMatchObject({
      questions: 318,
      topics: 33,
      yearMin: 2010,
      yearMax: 2026,
    });
  });
});
