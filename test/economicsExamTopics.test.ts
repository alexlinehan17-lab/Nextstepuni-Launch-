/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Economics reference-taxonomy parity, complete SEC task coverage, hosted
 * anchor, canonical curriculum, and card-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import economicsReference from '../data/examTopics/economics.json';
import economicsCrosswalk from '../data/examTopics/economics-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/economics-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { isAnswerMap } from '../components/PaperTrail/vaultResolve';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';
import preservationBaseline from './fixtures/economicsTopicQuestionBaseline.json';

const ROOT = process.cwd();

const higherLabels = [
  '1.1 Economic Concepts',
  '1.2 Sustainability',
  '2.1 The Market Economy',
  '2.2 Elasticity',
  '2.3 Costs of Production, Revenue & Profit',
  '2.4 Government Intervention',
  '3.1 Market Structures',
  '3.2 The Labour Market',
  '3.3 Market Failure',
  '4.1 National Income',
  '4.2 Fiscal Policy and the Budget Framework',
  '4.3 Employment',
  '4.4 Monetary Policy and Price Level',
  '4.5 The Financial Sector',
  '5.1 Economic Growth and Development',
  '5.2 Globalisation',
  '5.3 International Trade and Competitiveness',
  '6.1 Topical Questions and Statistics',
  'Research Project',
];

const ordinaryLabels = [
  '1.1 Economics as a Way of Thinking',
  '1.2 The Economic Concepts of Scarcity and Choice',
  '1.3 Sustainability',
  '2.1 The Market Economy',
  '2.2 Elasticity',
  '2.3 Costs of Production, Revenue & Profit',
  '2.4 Government Intervention',
  '3.1 Market Structures',
  '3.2 The Labour Market',
  '3.3 Market Failure',
  '4.1 National Income',
  '4.2 Fiscal Policy & the Budget Framework',
  '4.3 Employment',
  '4.4 Monetary Policy & the Price Level',
  '4.5 The Financial Sector',
  '5.1 Economic Growth & Development',
  '5.2 Globalisation',
  '5.3 International Trade & Competitiveness',
  'Acronyms',
  'Formulas',
  'Research Project',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

const baseline = preservationBaseline as Baseline;
const evidence = economicsCrosswalk;

describe('Economics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('economics')!;

  it('pins the exact flat reference hierarchy independently at each level', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [group.label, group.level])).toEqual([
      ['Higher Level', 'higher'],
      ['Ordinary Level', 'ordinary'],
    ]);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label))
      .toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label))
      .toEqual(ordinaryLabels);
    expect(topicsForSubject('economics')).toHaveLength(40);
  });

  it('bridges every practice bucket only to canonical NCCA Economics nodes', () => {
    const subject = CURRICULUM.find(item => item.id === 'economics')!;
    const canonicalIds = new Set(
      subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(canonicalIds.size).toBe(21);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(40);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
    }
  });

  it('reconciles every factual association and records each source boundary', () => {
    expect(evidence.summary).toMatchObject({
      referenceTopics: 40,
      referenceReportedAssociations: 1851,
      referenceOfficialAssociations: 1120,
      referenceMockAssociations: 731,
      matchedAssociations: 903,
      sourceBlockedAssociations: 217,
      matchedLogicalCards: 517,
      matchedQuestionTopicLinks: 816,
      retainedLocalLogicalCards: 32,
    });
    expect(evidence.policy.excludedCommercialContent).toContain('Question text');

    const blocked = evidence.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(
      new Set([2006, 2007, 2008, 2009, 2020, 2022]),
    );
    expect(new Set(blocked.map(association => association.sitting))).toEqual(
      new Set(['main', 'sample', 'deferred']),
    );
    expect(blocked.every(association => (
      'reason' in association && association.reason.includes('no StudyClix-hosted')
    ))).toBe(true);
    expect(evidence.summary.emptyReferenceTopics).toEqual([
      'economics-higher-research-project',
      'economics-ordinary-44-monetary-policy-the-price-level',
      'economics-ordinary-research-project',
    ]);
  });

  it('retains all 1,120 headings as level- and sitting-aware part metadata', () => {
    const references = examQuestionPartReferencesForSubject('economics');
    expect(references).toHaveLength(1120);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(602);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(518);
    expect(new Set(references.map(reference => (
      `${reference.level}|${reference.topicId}|${reference.subdivision}`
    )))).toHaveLength(1120);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
  });

  it('preserves all 26 pre-migration variants and all 304 original cards', () => {
    expect(baseline).toHaveLength(26);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(304);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'economics',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`)
        .not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expect.arrayContaining(expected.questions));
    }
  });

  it('exposes all old Section-B tasks and every new-format question', () => {
    expect(evidence.summary).toMatchObject({
      localPaperVariants: 66,
      localPhysicalMappings: 1098,
      distinctStudentFacingQuestions: 549,
      hostedAnchorMaps: 54,
      preservedBaselineVariants: 26,
      preservedBaselineCards: 304,
    });
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'economics');
    expect(papers).toHaveLength(66);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(1098);
    for (const paper of papers) {
      const expected = paper.year <= 2020
        ? [...Array.from({ length: 9 }, (_, i) => String(i + 1)), ...Array.from({ length: 8 }, (_, i) => `B${i + 1}`)]
        : Array.from({ length: 16 }, (_, i) => String(i + 1));
      expect(paper.q.map(question => question.n), `${paper.level}|${paper.lang}|${paper.year}`)
        .toEqual(expected);
    }
  });

  it('classifies every physical card into one or more same-level practice buckets', () => {
    const valid = new Map(taxonomy.topics.map(topic => [topic.id, topic.level]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'economics');
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(topicIds.length, `${paper.level}|${paper.lang}|${paper.year}|${question.n}`)
          .toBeGreaterThan(0);
        expect(topicIds.every(topicId => valid.get(topicId) === paper.level)).toBe(true);
      }
    }
  });

  it('keeps exact multi-topic joins and reviewed reference omissions', () => {
    expect(examTopicIdsForQuestion(
      'economics', 'higher', 2026, 'main', '1', 'single', 'ev',
    )).toEqual([
      'economics-higher-11-economic-concepts',
      'economics-higher-53-international-trade-and-competitiveness',
    ]);
    expect(examTopicIdsForQuestion(
      'economics', 'ordinary', 2025, 'main', '1', 'single', 'iv',
    )).toEqual(['economics-ordinary-11-economics-as-a-way-of-thinking']);
    expect(examTopicIdsForQuestion(
      'economics', 'higher', 2010, 'main', '1', 'single', 'ev',
    )).toEqual(['economics-higher-21-the-market-economy']);
    expect(examTopicIdsForQuestion(
      'economics', 'ordinary', 2010, 'main', 'B6', 'single', 'ev',
    )).toEqual([
      'economics-ordinary-45-the-financial-sector',
      'economics-ordinary-44-monetary-policy-the-price-level',
    ]);
    expect(examTopicIdsForQuestion(
      'economics', 'ordinary', 2019, 'main', 'B8', 'single', 'iv',
    )).toEqual([
      'economics-ordinary-51-economic-growth-development',
      'economics-ordinary-43-employment',
    ]);
  });

  it('ships complete hosted anchors wherever the classic map cannot address a card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => (
      paper.subjectId === 'economics' && (paper.year <= 2020 || (paper.year === 2025 && paper.level === 'higher'))
    ));
    expect(papers).toHaveLength(44);
    for (const paper of papers) {
      const anchorPath = path.join(
        ROOT,
        'public',
        'paper-anchors',
        String(paper.year),
        `${paper.fileid}.json`,
      );
      expect(fs.existsSync(anchorPath), anchorPath).toBe(true);
      const anchorMap = JSON.parse(fs.readFileSync(anchorPath, 'utf8'));
      expect(isAnswerMap(anchorMap), anchorPath).toBe(true);
      expect(anchorMap.paperOnly).toBe(1);
      expect(anchorMap.q.map((question: { n: string }) => question.n))
        .toEqual(paper.q.map(question => question.n));
      expect(anchorMap.q.every((question: { mode: string }) => question.mode === 'pagejump'))
        .toBe(true);
      for (const question of anchorMap.q) {
        expect(
          paperRegionFor(anchorMap.q, question.n, anchorMap.maxCropPages ?? 3),
          `${anchorPath} Q${question.n}`,
        ).not.toBeNull();
      }
    }
  });

  it('surfaces all 549 entitled tasks through the 40-topic menu', () => {
    expect(subjectAtlasStats('economics')).toMatchObject({
      questions: 549,
      topics: 40,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0))
      .toBe(731);
    expect(Object.values(economicsReference.levels)
      .flatMap(level => level.topics)
      .reduce((count, topic) => count + topic.officialQuestionHeadings.length, 0))
      .toBe(1120);
  });
});
