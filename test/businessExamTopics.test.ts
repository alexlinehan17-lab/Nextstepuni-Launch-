/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Business reference hierarchy, overlapping-specification bridge, complete
 * SEC corpus, crop, source-boundary, and task-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import businessReference from '../data/examTopics/business.json';
import businessEvidence from '../data/examTopics/business-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/business-curriculum-crosswalk.json';
import reviewedQuestions from '../data/examTopics/business-reviewed-question-topics.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { SUBJECTS as MARK_BANK_SUBJECTS } from '../components/MarkBank/deck';
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
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import preservationBaseline from './fixtures/businessTopicQuestionBaseline.json';

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
  variant => businessReference.variants[variant].topics,
);

describe('Business exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('business')!;

  it('pins the exact Higher/Ordinary × New/Old reference hierarchy', () => {
    expect(taxonomy).not.toBeNull();
    const expectedGroups = VARIANTS.flatMap((variant) => {
      const source = businessReference.variants[variant];
      const level = variant.startsWith('higher') ? 'higher' : 'ordinary';
      const course = variant.includes('new-course') ? 'new' : 'old';
      return source.groups.length
        ? source.groups.map(group => ({
            id: group.id,
            label: `${source.label} · ${group.label}`,
            level,
            course,
            topicIds: group.topicIds,
          }))
        : [{
            id: `business-${variant}`,
            label: source.label,
            level,
            course,
            topicIds: source.topics.map(topic => topic.id),
          }];
    });
    expect(taxonomy.groups).toEqual(expectedGroups);
    expect(taxonomy.groups).toHaveLength(12);
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(topicsForSubject('business')).toHaveLength(105);
  });

  it('keeps the official 2027 specification separate and bridges every practice bucket', () => {
    const outgoing = resolveCurriculumSpecification('Business', 2026)!;
    const redeveloped = resolveCurriculumSpecification('Business', 2027)!;
    const outgoingIds = new Set(
      outgoing.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    const redevelopedIds = new Set(
      redeveloped.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );

    expect(redeveloped.groups.map(group => group.title)).toEqual([
      'Unifying Strand: Investigating Business',
      'Strand 1: Exploring the Business Environment',
      'Strand 2: Understanding enterprise',
      'Strand 3: Leading in Business',
      'Strand 4: Being Informed and Making Informed Decisions',
    ]);
    expect(redevelopedIds.size).toBe(28);
    expect(redeveloped.recommendedClassHours).toBe(180);
    expect(redeveloped.assessmentComponents?.map(({ title, weighting }) => ({
      title,
      weighting,
    }))).toEqual([
      { title: 'Business Alive Investigative Study', weighting: 40 },
      { title: 'Written examination', weighting: 60 },
    ]);
    expect(MARK_BANK_SUBJECTS.find(subject => subject.id === 'business')?.spec)
      .toBe('outgoing 1999 syllabus');

    expect(Object.keys(curriculumCrosswalk)).toHaveLength(105);
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

  it('reconciles every listed item without importing commercial content', () => {
    expect(businessEvidence.summary).toMatchObject({
      referenceTopics: 105,
      referenceReportedAssociations: 5708,
      referenceOfficialAssociations: 3075,
      referenceMockAssociations: 2437,
      referenceProviderSampleAssociations: 196,
      matchedAssociations: 2008,
      sourceBlockedAssociations: 1067,
      matchedLogicalCards: 663,
      matchedQuestionTopicLinks: 1786,
      retainedLocalLogicalCards: 58,
    });
    expect(
      businessEvidence.summary.referenceOfficialAssociations
      + businessEvidence.summary.referenceMockAssociations
      + businessEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(businessEvidence.summary.referenceReportedAssociations);
    expect(businessEvidence.providerSamplePolicy).toContain('excluded');
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + (topic.providerSampleQuestionCount ?? 0),
      0,
    )).toBe(196);
    expect(businessEvidence.associations.filter(association => (
      association.resolution === 'source-blocked'
      && association.sitting === 'main'
    )).every(association => association.year < 2010)).toBe(true);
  });

  it('retains all 3,075 factual headings exactly as part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('business');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(3075);
    expect(references.filter(reference => reference.level === 'higher'))
      .toHaveLength(1547);
    expect(references.filter(reference => reference.level === 'ordinary'))
      .toHaveLength(1528);
    expect(actual).toEqual(expected);
    expect(new Set(references.map(reference => reference.paperKey)))
      .toEqual(new Set(['single', 'p1', 'p2']));
    expect(references).toContainEqual(expect.objectContaining({
      level: 'higher',
      year: 2025,
      paperKey: 'p2',
      n: 'ABQ',
      subdivision: '2025 - Section 2 - Question 1 - Part (a)',
    }));
  });

  it('preserves every one of the 523 frozen baseline cards', () => {
    expect(baseline).toHaveLength(50);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0))
      .toBe(523);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'business',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, paperIdentity(expected)).not.toBeNull();
      for (const number of expected.questions) {
        expect(
          live!.q.some(question => question.n === number),
          `${paperIdentity(expected)} Q${number}`,
        ).toBe(true);
      }
    }
  });

  it('exposes every official Business edition and top-level question through 2026', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'business');
    expect(businessEvidence.summary).toMatchObject({
      localPaperDocuments: 96,
      localPhysicalCards: 1442,
      localLogicalQuestions: 721,
      hostedAnchorMaps: 96,
      preservedBaselineVariants: 50,
      preservedBaselineCards: 523,
    });
    expect(papers).toHaveLength(96);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(1442);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    for (const paper of papers) {
      if (paper.level !== 'higher' && paper.level !== 'ordinary') {
        throw new Error(`Unexpected Business paper level: ${paper.level}`);
      }
      expect(paper.q.map(question => question.n)).toEqual(
        expectedQuestionNumbers(paper.level, paper.year, paper.paperKey),
      );
    }
  });

  it('classifies every physical card into same-level reference topics', () => {
    const topicLevel = new Map(
      taxonomy.topics.map(topic => [topic.id, topic.level]),
    );
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'business');
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

  it('retains every directly reviewed reference omission in both languages', () => {
    expect(Object.keys(reviewedQuestions.questions)).toHaveLength(58);
    expect(businessEvidence.retainedLocalCards).toHaveLength(58);
    for (const card of businessEvidence.retainedLocalCards) {
      if (card.level !== 'higher' && card.level !== 'ordinary') {
        throw new Error(`Unexpected retained Business card level: ${card.level}`);
      }
      for (const lang of ['ev', 'iv'] as const) {
        expect(examTopicIdsForQuestion(
          'business',
          card.level,
          card.year,
          'main',
          card.questionNumber,
          card.paperKey,
          lang,
        )).toEqual(card.topicIds);
      }
    }
    expect(businessEvidence.retainedLocalCards.every(card => (
      card.resolution === 'retained-local-reviewed'
    ))).toBe(true);
    expect(examTopicIdsForQuestion(
      'business', 'higher', 2026, 'main', 'ABQ', 'p2', 'ev',
    )).toEqual(expect.arrayContaining([
      'business-higher-old-course-abq-units-3-4-5',
      'business-higher-new-course-24-the-target-market',
    ]));
  });

  it('ships a valid finite paper crop for every physical card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'business');
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

  it('keeps every available scheme sidecar valid and falls back honestly where absent', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'business');
    let schemeMaps = 0;
    let paperOnlyVariants = 0;
    for (const paper of papers) {
      const answerPath = path.join(
        ROOT,
        'scripts',
        'paper-trail',
        'answers',
        String(paper.year),
        `${paper.fileid}.json`,
      );
      if (!fs.existsSync(answerPath)) {
        paperOnlyVariants += 1;
        continue;
      }
      schemeMaps += 1;
      const answerMap = JSON.parse(fs.readFileSync(answerPath, 'utf8'));
      expect(isAnswerMap(answerMap), answerPath).toBe(true);
      expect(answerMap.paperOnly).not.toBe(1);
      expect(answerMap.paperFileid).toBe(paper.fileid);
    }
    expect(schemeMaps).toBe(82);
    expect(paperOnlyVariants).toBe(14);
  });

  it('surfaces all 721 entitled questions through all 105 topic buckets', () => {
    expect(subjectAtlasStats('business')).toMatchObject({
      questions: 721,
      topics: 105,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + topic.mockQuestionCount,
      0,
    )).toBe(2437);
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + (topic.reportedQuestionCount ?? 0),
      0,
    )).toBe(5708);
  });
});

function expectedQuestionNumbers(
  level: 'higher' | 'ordinary',
  year: number,
  paperKey: string,
): string[] {
  if (year <= 2019) {
    return level === 'higher'
      ? [
          ...Array.from({ length: 10 }, (_, index) => String(index + 1)),
          'ABQ',
          ...Array.from({ length: 7 }, (_, index) => `S3Q${index + 1}`),
        ]
      : [
          ...Array.from({ length: 15 }, (_, index) => String(index + 1)),
          ...Array.from({ length: 8 }, (_, index) => `S2Q${index + 1}`),
        ];
  }
  if (level === 'higher') {
    return paperKey === 'p1'
      ? Array.from({ length: year === 2020 ? 10 : 12 }, (_, index) => String(index + 1))
      : [
          'ABQ',
          ...Array.from({ length: year === 2020 ? 7 : 8 }, (_, index) => String(index + 1)),
        ];
  }
  return paperKey === 'p1'
    ? Array.from({ length: 15 }, (_, index) => String(index + 1))
    : Array.from({ length: year === 2020 ? 8 : 9 }, (_, index) => String(index + 1));
}

function paperIdentity(paper: Baseline[number]): string {
  return [
    paper.level,
    paper.lang,
    paper.year,
    paper.paperKey,
    paper.fileid,
  ].join('|');
}
