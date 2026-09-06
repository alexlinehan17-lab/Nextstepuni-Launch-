/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Chemistry reference hierarchy, overlapping-specification bridge, complete
 * SEC corpus, crop, source-boundary, and task-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import chemistryReference from '../data/examTopics/chemistry.json';
import chemistryEvidence from '../data/examTopics/chemistry-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/chemistry-curriculum-crosswalk.json';
import reviewed2026 from '../data/examTopics/chemistry-2026-exam-topic-map.json';
import reviewedOmissions from '../data/examTopics/chemistry-reference-omissions-topic-map.json';
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
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import preservationBaseline from './fixtures/chemistryTopicQuestionBaseline.json';

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
  variant => chemistryReference.variants[variant].topics,
);
const expectedNumbers = Array.from({ length: 11 }, (_, index) => String(index + 1));

describe('Chemistry exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('chemistry')!;

  it('pins the exact Higher/Ordinary × New/Old reference hierarchy', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [
      group.label,
      group.level,
      group.course,
    ])).toEqual([
      ['Higher Level · New Course · Strand 1: Nature of Matter', 'higher', 'new'],
      ['Higher Level · New Course · Strand 2: Behaviour of Matter', 'higher', 'new'],
      ['Higher Level · New Course · Strand 3: Interactions of Matter', 'higher', 'new'],
      ['Higher Level · New Course · Strand 4: Matter in our World', 'higher', 'new'],
      ['Higher Level · Old Course', 'higher', 'old'],
      ['Ordinary Level · New Course · Strand 1: Nature of Matter', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Strand 2: Behaviour of Matter', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Strand 3: Interactions of Matter', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Strand 4: Matter in our World', 'ordinary', 'new'],
      ['Ordinary Level · New Course · Unifying Strand: The Nature of Science', 'ordinary', 'new'],
      ['Ordinary Level · Old Course', 'ordinary', 'old'],
    ]);
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(topicsForSubject('chemistry')).toHaveLength(76);
  });

  it('bridges every practice bucket to the correct canonical specification', () => {
    const outgoing = resolveCurriculumSpecification('Chemistry', 2026)!;
    const redeveloped = resolveCurriculumSpecification('Chemistry', 2027)!;
    const outgoingIds = new Set(
      outgoing.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    const redevelopedIds = new Set(
      redeveloped.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(76);
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
    expect(chemistryEvidence.summary).toMatchObject({
      referenceTopics: 76,
      referenceReportedAssociations: 4026,
      referenceOfficialAssociations: 2265,
      referenceMockAssociations: 1612,
      referenceProviderSampleAssociations: 149,
      matchedAssociations: 1406,
      sourceBlockedAssociations: 859,
      matchedLogicalCards: 342,
      retainedLocalLogicalCards: 32,
    });
    expect(
      chemistryEvidence.summary.referenceOfficialAssociations
      + chemistryEvidence.summary.referenceMockAssociations
      + chemistryEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(chemistryEvidence.summary.referenceReportedAssociations);
    expect(chemistryEvidence.providerSamplePolicy).toContain('excluded');
    expect(
      taxonomy.topics.reduce(
        (sum, topic) => sum + (topic.providerSampleQuestionCount ?? 0),
        0,
      ),
    ).toBe(149);
    expect(chemistryEvidence.associations.filter(association => (
      association.resolution === 'source-blocked'
      && association.sitting === 'main'
    )).every(association => association.year < 2010)).toBe(true);
  });

  it('retains all 2,265 factual headings exactly as part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('chemistry');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(2265);
    expect(references.filter(reference => reference.level === 'higher'))
      .toHaveLength(1398);
    expect(references.filter(reference => reference.level === 'ordinary'))
      .toHaveLength(867);
    expect(actual).toEqual(expected);
    expect(new Set(references.map(reference => reference.paperKey)))
      .toEqual(new Set(['single']));
    expect(references.find(reference => (
      reference.subdivision === '2013 - Section B - Question d'
    ))?.n).toBe('4');
    expect(references.find(reference => (
      reference.subdivision === '2017 - Section 11 - Question c - Part a'
    ))?.n).toBe('11');
  });

  it('preserves every one of the 704 frozen baseline cards', () => {
    expect(baseline).toHaveLength(64);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0))
      .toBe(704);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'chemistry',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('exposes every official Chemistry edition through 2026', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'chemistry');
    expect(chemistryEvidence.summary).toMatchObject({
      localPaperVariants: 68,
      localPhysicalCards: 748,
      localLogicalQuestions: 374,
      preservedBaselineVariants: 64,
      preservedBaselineTasks: 704,
    });
    expect(papers).toHaveLength(68);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(748);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    for (const paper of papers) {
      expect(paper.q.map(question => question.n)).toEqual(expectedNumbers);
    }
  });

  it('classifies every physical card into same-level reference topics', () => {
    const topicLevel = new Map(
      taxonomy.topics.map(topic => [topic.id, topic.level]),
    );
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'chemistry');
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
    expect(Object.keys(reviewed2026.questions)).toHaveLength(22);
    expect(Object.keys(reviewedOmissions.questions)).toHaveLength(10);
    const expectedMappings = [
      ...Object.entries(reviewed2026.questions).map(([key, ids]) => {
        const [level, n] = key.split('|');
        return [`${level}|2026|${n}`, ids] as const;
      }),
      ...Object.entries(reviewedOmissions.questions),
    ];
    for (const [key, expectedIds] of expectedMappings) {
      const [level, year, n] = key.split('|') as [
        'higher' | 'ordinary', string, string,
      ];
      expect(examTopicIdsForQuestion(
        'chemistry', level, Number(year), 'main', n, 'single', 'ev',
      )).toEqual(expectedIds);
      expect(examTopicIdsForQuestion(
        'chemistry', level, Number(year), 'main', n, 'single', 'iv',
      )).toEqual(expectedIds);
    }
    expect(chemistryEvidence.retainedLocalCards.every(card => (
      card.resolution === 'retained-local-reviewed'
    ))).toBe(true);
  });

  it('ships a valid finite paper crop for every physical card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'chemistry');
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

  it('keeps every available verified scheme map aligned to Q1-Q11', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'chemistry');
    let schemeMaps = 0;
    const paperOnlyVariants: Array<{ year: number; fileid: string }> = [];
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
        paperOnlyVariants.push({ year: paper.year, fileid: paper.fileid });
        continue;
      }
      schemeMaps += 1;
      const answerMap = JSON.parse(fs.readFileSync(answerPath, 'utf8'));
      expect(isAnswerMap(answerMap), answerPath).toBe(true);
      expect(answerMap.paperOnly).not.toBe(1);
      expect(answerMap.q.map((question: { n: string }) => question.n))
        .toEqual(expectedNumbers);
    }
    expect(schemeMaps).toBe(67);
    expect(paperOnlyVariants).toEqual([
      { year: 2020, fileid: 'LC022GLP000IV.pdf' },
    ]);
    expect(fs.existsSync(path.join(
      ROOT,
      'paper-trail-corpus',
      'markingschemes',
      '2020',
      'LC022GLP000IV.pdf',
    ))).toBe(false);
  });

  it('surfaces all 374 entitled questions through all 76 topic buckets', () => {
    expect(subjectAtlasStats('chemistry')).toMatchObject({
      questions: 374,
      topics: 76,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + topic.mockQuestionCount,
      0,
    )).toBe(1612);
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + (topic.reportedQuestionCount ?? 0),
      0,
    )).toBe(4026);
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
