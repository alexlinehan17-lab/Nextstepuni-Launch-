/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Computer Science reference-taxonomy parity, complete SEC booklet coverage,
 * hosted crop, canonical curriculum, and card-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import computerScienceReference from '../data/examTopics/computer-science.json';
import computerScienceEvidence from '../data/examTopics/computer-science-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/computer-science-curriculum-crosswalk.json';
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
import preservationBaseline from './fixtures/computerScienceTopicQuestionBaseline.json';

const ROOT = process.cwd();

const higherLabels = [
  'Algorithms',
  'Communication Protocols',
  'Communication Protocols, World Wide Web & the Internet',
  'Computational Thinking',
  'Computer Systems',
  'Computers and Society',
  'Data Analysis',
  'Data Representation',
  'Databases',
  'Digital and Analogue Input',
  'Embedded Systems',
  'History of Computing',
  'HTML/CSS',
  'JavaScript',
  'Logic Gates',
  'Machine Learning and Artificial Intelligence',
  'Modelling and Simulation',
  'Pseudocode and Flowcharts',
  'Python',
  'Software Design and Development',
  'User Experience and User Interface',
];

const ordinaryLabels = [
  'Algorithms',
  'Communication Protocols',
  'Communication Protocols, World Wide Web & the Internet',
  'Computational Thinking',
  'Computer Systems',
  'Computers and Society',
  'Data Analysis',
  'Data Representation',
  'Databases',
  'Decomposition',
  'Digital and Analogue Input',
  'Embedded Systems',
  'History of Computing',
  'HTML / CSS',
  'JavaScript',
  'Logic Gates',
  'Machine Learning and Artificial Intelligence',
  'Modelling and Simulation',
  'Number Systems',
  'Pseudocode and Flowcharts',
  'Python',
  'Software',
  'Software Design and Development',
  'User Experience and User Interface',
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
const evidence = computerScienceEvidence;

describe('Computer Science exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('computer-science')!;

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
    expect(topicsForSubject('computer-science')).toHaveLength(45);
  });

  it('bridges every practice bucket only to canonical NCCA Computer Science nodes', () => {
    const subject = CURRICULUM.find(item => item.id === 'computer-science')!;
    const canonicalIds = new Set(
      subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(canonicalIds.size).toBe(61);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(45);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
    }
  });

  it('reconciles every factual association and records the sample-paper boundary', () => {
    expect(evidence.summary).toMatchObject({
      referenceTopics: 45,
      referenceReportedAssociations: 420,
      referenceOfficialAssociations: 302,
      referenceMockAssociations: 118,
      matchedAssociations: 253,
      sourceBlockedAssociations: 49,
      matchedLogicalCards: 203,
      matchedQuestionTopicLinks: 240,
      retainedLocalLogicalCards: 5,
    });
    expect(evidence.policy.excludedCommercialContent).toContain('Question text');
    const blocked = evidence.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(new Set([2020]));
    expect(new Set(blocked.map(association => association.sitting))).toEqual(new Set(['sample']));
    expect(evidence.summary.emptyReferenceTopics).toEqual([
      'computer-science-higher-data-analysis',
      'computer-science-ordinary-databases',
      'computer-science-ordinary-decomposition',
      'computer-science-ordinary-html-css',
      'computer-science-ordinary-number-systems',
    ]);
  });

  it('retains all 302 headings as level-, sitting-, and part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('computer-science');
    expect(references).toHaveLength(302);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(153);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(149);
    expect(new Set(references.map(reference => reference.paperKey))).toEqual(new Set(['single']));
    expect(new Set(references.map(reference => (
      `${reference.level}|${reference.topicId}|${reference.subdivision}`
    )))).toHaveLength(302);
  });

  it('preserves all 23 pre-migration variants and all 317 original cards', () => {
    expect(baseline).toHaveLength(23);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(317);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'computer-science',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`)
        .not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('exposes every A/B and C booklet through 2026 in both official languages', () => {
    expect(evidence.summary).toMatchObject({
      localPaperVariants: 52,
      localPhysicalMappings: 416,
      distinctStudentFacingQuestions: 208,
      hostedAnchorMaps: 52,
      preservedBaselineVariants: 23,
      preservedBaselineCards: 317,
    });
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'computer-science');
    expect(papers).toHaveLength(52);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(416);
    expect(papers.filter(paper => paper.fileid.includes('P038'))).toHaveLength(26);
    expect(papers.filter(paper => paper.fileid.includes('P040'))).toHaveLength(26);
    for (const paper of papers) {
      expect(paper.q.map(question => question.n)).toEqual(
        paper.fileid.includes('P038')
          ? Array.from({ length: 15 }, (_, index) => String(index + 1))
          : ['16'],
      );
    }
  });

  it('classifies every physical card into one or more same-level practice buckets', () => {
    const valid = new Map(taxonomy.topics.map(topic => [topic.id, topic.level]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'computer-science');
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(
          topicIds.length,
          `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}|${question.n}`,
        ).toBeGreaterThan(0);
        expect(topicIds.every(topicId => valid.get(topicId) === paper.level)).toBe(true);
      }
    }
  });

  it('retains exact multi-topic joins across both official languages', () => {
    expect(examTopicIdsForQuestion(
      'computer-science', 'higher', 2026, 'main', '14', 'single', 'ev',
    )).toEqual([
      'computer-science-higher-computational-thinking',
      'computer-science-higher-computers-and-society',
    ]);
    expect(examTopicIdsForQuestion(
      'computer-science', 'higher', 2025, 'main', '14', 'single', 'iv',
    )).toEqual([
      'computer-science-higher-algorithms',
      'computer-science-higher-python',
    ]);
    expect(examTopicIdsForQuestion(
      'computer-science', 'ordinary', 2026, 'main', '16', 'single', 'ev',
    )).toEqual(['computer-science-ordinary-python']);
  });

  it('keeps all five reference omissions visible under reviewed same-level topics', () => {
    expect(examTopicIdsForQuestion(
      'computer-science', 'higher', 2020, 'main', '9', 'single', 'ev',
    )).toEqual([
      'computer-science-higher-data-analysis',
      'computer-science-higher-data-representation',
    ]);
    expect(examTopicIdsForQuestion(
      'computer-science', 'higher', 2021, 'main', '2', 'single', 'iv',
    )).toEqual(['computer-science-higher-data-representation']);
    expect(examTopicIdsForQuestion(
      'computer-science', 'higher', 2023, 'main', '1', 'single', 'ev',
    )).toEqual(['computer-science-higher-data-representation']);
    expect(examTopicIdsForQuestion(
      'computer-science', 'higher', 2023, 'main', '9', 'single', 'iv',
    )).toEqual([
      'computer-science-higher-computational-thinking',
      'computer-science-higher-pseudocode-and-flowcharts',
    ]);
    expect(examTopicIdsForQuestion(
      'computer-science', 'ordinary', 2025, 'main', '12', 'single', 'ev',
    )).toEqual([
      'computer-science-ordinary-software-design-and-development',
      'computer-science-ordinary-data-representation',
    ]);
  });

  it('ships a valid, finite crop for every one of the 416 physical cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'computer-science');
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
      for (const question of anchorMap.q) {
        expect(
          paperRegionFor(anchorMap.q, question.n, anchorMap.maxCropPages ?? 3),
          `${anchorPath} Q${question.n}`,
        ).not.toBeNull();
      }
    }
  });

  it('surfaces all 208 entitled questions through the 45-topic menu', () => {
    expect(subjectAtlasStats('computer-science')).toMatchObject({
      questions: 208,
      topics: 45,
      yearMin: 2020,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0))
      .toBe(118);
    expect(Object.values(computerScienceReference.levels)
      .flatMap(level => level.topics)
      .reduce((count, topic) => count + topic.officialQuestionHeadings.length, 0))
      .toBe(302);
  });
});
