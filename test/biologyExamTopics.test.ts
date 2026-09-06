/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Biology reference hierarchy, overlapping-specification bridge, complete SEC
 * booklet coverage, crop, source-boundary, and task-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import biologyReference from '../data/examTopics/biology.json';
import biologyEvidence from '../data/examTopics/biology-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/biology-curriculum-crosswalk.json';
import reviewed2026 from '../data/examTopics/biology-2026-exam-topic-map.json';
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
import {
  resolveCurriculumSpecification,
} from '../curriculumRegistry';
import preservationBaseline from './fixtures/biologyTopicQuestionBaseline.json';

const ROOT = process.cwd();
const VARIANTS = [
  'higher-new-course',
  'higher-old-course',
  'ordinary-new-course',
  'ordinary-old-course',
] as const;

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

const baseline = preservationBaseline as Baseline;
const referenceTopics = VARIANTS.flatMap(
  variant => biologyReference.variants[variant].topics,
);

const expectedNumbers = (year: number, fileid: string): string[] => {
  if (fileid.includes('P000')) {
    return Array.from({ length: 15 }, (_, index) => String(index + 1));
  }
  if (fileid.includes('P038')) {
    const count = year <= 2020 ? 9 : 10;
    return Array.from({ length: count }, (_, index) => String(index + 1));
  }
  const first = year <= 2020 ? 10 : 11;
  const last = year <= 2020 ? 15 : 17;
  return Array.from({ length: last - first + 1 }, (_, index) => String(first + index));
};

describe('Biology exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('biology')!;

  it('pins the exact Higher/Ordinary × New/Old reference hierarchy', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [
      group.label,
      group.level,
      group.course,
    ])).toEqual([
      ['Higher Level · New Course · Strand 1: Organisation of Life', 'higher', 'new'],
      ['Higher Level · New Course · Strand 2: Structures and Processes of Life', 'higher', 'new'],
      ['Higher Level · New Course · Strand 3: Interactions of Life', 'higher', 'new'],
      ['Higher Level · New Course · Unifying Strand: Nature of Science', 'higher', 'new'],
      ['Higher Level · Old Course', 'higher', 'old'],
      ['Ordinary Level · New Course · Strand 1: Organisation of Life', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Strand 2: Structures and Processes of Life', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Strand 3: Interactions of Life', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Unifying Strand: Nature of Science', 'ordinary', 'new'],
      ['Ordinary Level · Old Course', 'ordinary', 'old'],
    ]);
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(topicsForSubject('biology')).toHaveLength(122);
  });

  it('bridges every practice bucket to the correct canonical specification', () => {
    const outgoing = resolveCurriculumSpecification('Biology', 2026)!;
    const redeveloped = resolveCurriculumSpecification('Biology', 2027)!;
    const outgoingIds = new Set(
      outgoing.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    const redevelopedIds = new Set(
      redeveloped.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(122);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(
        curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk],
      );
      const canonicalIds = topic.course === 'new' ? redevelopedIds : outgoingIds;
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles every listed item without importing provider-owned samples', () => {
    expect(biologyEvidence.summary).toMatchObject({
      referenceTopics: 122,
      referenceReportedAssociations: 4891,
      referenceOfficialAssociations: 2419,
      referenceMockAssociations: 2333,
      referenceProviderSampleAssociations: 139,
      matchedAssociations: 1561,
      sourceBlockedAssociations: 858,
      matchedLogicalCards: 485,
      retainedLocalLogicalCards: 49,
    });
    expect(
      biologyEvidence.summary.referenceOfficialAssociations
      + biologyEvidence.summary.referenceMockAssociations
      + biologyEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(biologyEvidence.summary.referenceReportedAssociations);
    expect(biologyEvidence.providerSamplePolicy).toContain('excluded');
    expect(
      taxonomy.topics.reduce(
        (sum, topic) => sum + (topic.providerSampleQuestionCount ?? 0),
        0,
      ),
    ).toBe(139);
  });

  it('retains all 2,419 factual headings exactly as part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('biology');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(2419);
    expect(references.filter(reference => reference.level === 'higher'))
      .toHaveLength(1370);
    expect(references.filter(reference => reference.level === 'ordinary'))
      .toHaveLength(1049);
    expect(actual).toEqual(expected);
    expect(new Set(references.map(reference => reference.paperKey)))
      .toEqual(new Set(['single']));
  });

  it('preserves all 971 baseline tasks while correcting the verified 48 IDs', () => {
    expect(baseline).toHaveLength(89);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0))
      .toBe(971);
    let corrected = 0;
    for (const expected of baseline) {
      const live = topicsForPaper(
        'biology',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, paperIdentity(expected)).not.toBeNull();
      const shifts = (
        (expected.year === 2019 || expected.year === 2020)
        && expected.fileid.includes('P040')
      );
      const wanted = expected.questions.map(number => {
        if (!shifts) return number;
        corrected += 1;
        return String(Number(number) - 1);
      });
      expect(live!.q.map(question => question.n)).toEqual(wanted);
    }
    expect(corrected).toBe(48);
  });

  it('exposes every official paper edition through 2026', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'biology');
    expect(biologyEvidence.summary).toMatchObject({
      localPaperVariants: 100,
      localPhysicalCards: 1068,
      localLogicalQuestions: 534,
      preservedBaselineVariants: 89,
      preservedBaselineTasks: 971,
      corrected2019To2020SectionCCardIds: 48,
    });
    expect(papers).toHaveLength(100);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(1068);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    for (const paper of papers) {
      expect(paper.q.map(question => question.n))
        .toEqual(expectedNumbers(paper.year, paper.fileid));
    }
  });

  it('corrects 2019-2020 Section C against the printed SEC numbering', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => (
      paper.subjectId === 'biology'
      && (paper.year === 2019 || paper.year === 2020)
      && paper.fileid.includes('P040')
    ));
    expect(papers).toHaveLength(8);
    for (const paper of papers) {
      expect(paper.q.map(question => question.n))
        .toEqual(['10', '11', '12', '13', '14', '15']);
      const anchorPath = path.join(
        ROOT, 'public/paper-anchors', String(paper.year), `${paper.fileid}.json`,
      );
      const anchorMap = JSON.parse(fs.readFileSync(anchorPath, 'utf8'));
      expect(anchorMap.q.map((question: { n: string }) => question.n))
        .toEqual(['10', '11', '12', '13', '14', '15']);
    }
  });

  it('classifies every physical card into same-level reference topics', () => {
    const topicLevel = new Map(
      taxonomy.topics.map(topic => [topic.id, topic.level]),
    );
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'biology');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(
          ids.length,
          `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}|${question.n}`,
        ).toBeGreaterThan(0);
        expect(ids.every(id => topicLevel.get(id) === paper.level)).toBe(true);
      }
    }
  });

  it('retains all 34 post-snapshot 2026 questions under reviewed topics', () => {
    expect(Object.keys(reviewed2026.questions)).toHaveLength(34);
    for (const [key, expectedIds] of Object.entries(reviewed2026.questions)) {
      const [level, n] = key.split('|') as ['higher' | 'ordinary', string];
      expect(examTopicIdsForQuestion(
        'biology', level, 2026, 'main', n, 'single', 'ev',
      )).toEqual(expectedIds);
      expect(examTopicIdsForQuestion(
        'biology', level, 2026, 'main', n, 'single', 'iv',
      )).toEqual(expectedIds);
    }
  });

  it('ships a valid finite paper crop for every physical card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'biology');
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

  it('surfaces all 534 entitled questions through all 122 topic buckets', () => {
    expect(subjectAtlasStats('biology')).toMatchObject({
      questions: 534,
      topics: 122,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + topic.mockQuestionCount,
      0,
    )).toBe(2333);
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + (topic.reportedQuestionCount ?? 0),
      0,
    )).toBe(4891);
  });
});

function paperIdentity(paper: Baseline[number]): string {
  return [
    paper.level,
    paper.lang,
    paper.year,
    paper.paperKey,
    paper.fileid,
  ].join('|');
}
