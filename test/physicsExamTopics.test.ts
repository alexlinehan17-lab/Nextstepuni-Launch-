/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Physics reference hierarchy, overlapping-specification bridge, complete SEC
 * corpus, crop, source-boundary, and task-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import physicsReference from '../data/examTopics/physics.json';
import physicsEvidence from '../data/examTopics/physics-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/physics-curriculum-crosswalk.json';
import reviewed2026 from '../data/examTopics/physics-2026-exam-topic-map.json';
import reviewedOmissions from '../data/examTopics/physics-reference-omissions-topic-map.json';
import markBankCoverage from '../scripts/markbank/coverage-baseline.json';
import markBankExclusions from '../scripts/markbank/authoring/exclusions/physics.json';
import { CARDS as higherMarkBankCards } from '../components/MarkBank/cards/physics/higher';
import { CARDS as ordinaryMarkBankCards } from '../components/MarkBank/cards/physics/ordinary';
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
import preservationBaseline from './fixtures/physicsTopicQuestionBaseline.json';

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
  variant => physicsReference.variants[variant].topics,
);

describe('Physics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('physics')!;

  it('pins the exact Higher/Ordinary × New/Old reference hierarchy', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [
      group.label,
      group.level,
      group.course,
    ])).toEqual([
      [
        'Higher Level · New Course · Strand 1: Forces and Motion: Kinematics and Dynamics',
        'higher',
        'new',
      ],
      [
        'Higher Level · New Course · Strand 2: Wave Motion and Energy Transfer',
        'higher',
        'new',
      ],
      [
        'Higher Level · New Course · Strand 3: Electric and Magnetic Fields and Their Interactions',
        'higher',
        'new',
      ],
      [
        'Higher Level · New Course · Strand 4: Modern Physics Atomic and Nuclear',
        'higher',
        'new',
      ],
      ['Higher Level · Old Course', 'higher', 'old'],
      [
        'Ordinary Level · New Course · Strand 1: Forces and Motion: Kinematics and Dynamics',
        'ordinary',
        'new',
      ],
      [
        'Ordinary Level · New Course · Strand 2: Wave Motion and Energy Transfer',
        'ordinary',
        'new',
      ],
      [
        'Ordinary Level · New Course · Strand 3: Electric and Magnetic Fields and Their Interactions',
        'ordinary',
        'new',
      ],
      [
        'Ordinary Level · New Course · Strand 4: Modern Physics Atomic and Nuclear',
        'ordinary',
        'new',
      ],
      [
        'Ordinary Level · New Course · Unifying Strand: The Nature of Science',
        'ordinary',
        'new',
      ],
      ['Ordinary Level · Old Course', 'ordinary', 'old'],
    ]);
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(topicsForSubject('physics')).toHaveLength(113);
  });

  it('bridges every practice bucket to the correct canonical specification', () => {
    const outgoing = resolveCurriculumSpecification('Physics', 2026)!;
    const redeveloped = resolveCurriculumSpecification('Physics', 2027)!;
    const outgoingIds = new Set(
      outgoing.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    const redevelopedIds = new Set(
      redeveloped.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(113);
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
    expect(physicsEvidence.summary).toMatchObject({
      referenceTopics: 113,
      referenceReportedAssociations: 4701,
      referenceOfficialAssociations: 2482,
      referenceMockAssociations: 2051,
      referenceProviderSampleAssociations: 168,
      matchedAssociations: 1703,
      sourceBlockedAssociations: 779,
      matchedLogicalCards: 391,
      retainedLocalLogicalCards: 41,
    });
    expect(
      physicsEvidence.summary.referenceOfficialAssociations
      + physicsEvidence.summary.referenceMockAssociations
      + physicsEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(physicsEvidence.summary.referenceReportedAssociations);
    expect(physicsEvidence.providerSamplePolicy).toContain('excluded');
    expect(
      taxonomy.topics.reduce(
        (sum, topic) => sum + (topic.providerSampleQuestionCount ?? 0),
        0,
      ),
    ).toBe(168);
    expect(physicsEvidence.associations.filter(association => (
      association.resolution === 'source-blocked'
      && association.sitting === 'main'
    )).every(association => association.year < 2010)).toBe(true);
  });

  it('retains all 2,482 factual headings exactly as part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('physics');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(2482);
    expect(references.filter(reference => reference.level === 'higher'))
      .toHaveLength(1332);
    expect(references.filter(reference => reference.level === 'ordinary'))
      .toHaveLength(1150);
    expect(actual).toEqual(expected);
    expect(new Set(references.map(reference => reference.paperKey)))
      .toEqual(new Set(['single']));
    expect(references.filter(reference => (
      reference.subdivision === '2019 - Section 11 - Question b'
    ))).toHaveLength(2);
    expect(references.filter(reference => (
      reference.subdivision === '2019 - Section 11 - Question b'
    )).every(reference => reference.n === '11')).toBe(true);
  });

  it('preserves every one of the 790 frozen baseline cards', () => {
    expect(baseline).toHaveLength(63);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0))
      .toBe(790);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'physics',
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

  it('exposes every official Physics edition and question through 2026', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics');
    expect(physicsEvidence.summary).toMatchObject({
      localPaperVariants: 68,
      localPhysicalCards: 864,
      localLogicalQuestions: 432,
      preservedBaselineVariants: 63,
      preservedBaselineTasks: 790,
    });
    expect(papers).toHaveLength(68);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(864);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    for (const paper of papers) {
      const count = paper.year <= 2020 ? 12 : 14;
      expect(paper.q.map(question => question.n)).toEqual(
        Array.from({ length: count }, (_, index) => String(index + 1)),
      );
    }

    for (const year of [2011, 2012]) {
      for (const lang of ['ev', 'iv'] as const) {
        const paper = papers.find(candidate => (
          candidate.year === year
          && candidate.level === 'higher'
          && candidate.lang === lang
        ));
        expect(paper?.q.some(question => question.n === '12')).toBe(true);
      }
    }
    expect(papers.some(paper => (
      paper.year === 2025
      && paper.level === 'ordinary'
      && paper.lang === 'ev'
    ))).toBe(true);
  });

  it('classifies every physical card into same-level reference topics', () => {
    const topicLevel = new Map(
      taxonomy.topics.map(topic => [topic.id, topic.level]),
    );
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics');
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
    expect(Object.keys(reviewed2026.questions)).toHaveLength(28);
    expect(Object.keys(reviewedOmissions.questions)).toHaveLength(13);
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
        'physics', level, Number(year), 'main', n, 'single', 'ev',
      )).toEqual(expectedIds);
      expect(examTopicIdsForQuestion(
        'physics', level, Number(year), 'main', n, 'single', 'iv',
      )).toEqual(expectedIds);
    }
    expect(physicsEvidence.retainedLocalCards.every(card => (
      card.resolution === 'retained-local-reviewed'
    ))).toBe(true);
  });

  it('ships a valid finite paper crop for every physical card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics');
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

  it('keeps every available verified scheme map aligned to its paper', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'physics');
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
        .toEqual(paper.q.map(question => question.n));
    }
    expect(schemeMaps).toBe(67);
    expect(paperOnlyVariants).toEqual([
      { year: 2020, fileid: 'LC021GLP000IV.pdf' },
    ]);
    expect(fs.existsSync(path.join(
      ROOT,
      'paper-trail-corpus',
      'markingschemes',
      '2020',
      'LC021GLP000IV.pdf',
    ))).toBe(false);
  });

  it('keeps every shipped Mark Bank card linked to the exact old-course practice map', () => {
    const cards = [...higherMarkBankCards, ...ordinaryMarkBankCards];
    expect(cards).toHaveLength(1133);

    for (const card of cards) {
      const parsed = /^(\d{4})\s+(HL|OL)\s+Q(\d+)/.exec(card.questionRef);
      expect(parsed, `${card.id}: ${card.questionRef}`).not.toBeNull();
      const [, year, levelCode, question] = parsed!;
      const level = levelCode === 'HL' ? 'higher' : 'ordinary';
      expect(card.level).toBe(level);

      const topicIds = examTopicIdsForQuestion(
        'physics',
        level,
        Number(year),
        'main',
        question,
        'single',
        'ev',
      );
      expect(topicIds.length, card.id).toBeGreaterThan(0);
      expect(topicIds.every(topicId => {
        const topic = taxonomy.topics.find(candidate => candidate.id === topicId);
        return topic?.level === level;
      }), card.id).toBe(true);
      expect(topicIds.some(topicId => (
        taxonomy.topics.find(candidate => candidate.id === topicId)?.course === 'old'
      )), card.id).toBe(true);
    }
  });

  it('pins the independently measured Mark Bank remainder instead of hiding it', () => {
    expect(markBankCoverage.physics).toMatchObject({
      cards: 1133,
      leaves: 1224,
      covered: 1119,
      excluded: 46,
      open: 59,
      orphans: 6,
      coveragePct: 95.2,
    });
    expect(markBankExclusions).toHaveLength(46);
    expect(markBankExclusions.every(exclusion => (
      exclusion.ref && exclusion.reason && exclusion.evidence
    ))).toBe(true);
  });

  it('surfaces all 432 entitled questions through all 113 topic buckets', () => {
    expect(subjectAtlasStats('physics')).toMatchObject({
      questions: 432,
      topics: 113,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + topic.mockQuestionCount,
      0,
    )).toBe(2051);
    expect(taxonomy.topics.reduce(
      (sum, topic) => sum + (topic.reportedQuestionCount ?? 0),
      0,
    )).toBe(4701);
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
