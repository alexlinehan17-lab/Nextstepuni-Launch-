/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Italian reference-parity, complete SEC corpus and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import italianReference from '../data/examTopics/italian.json';
import italianCrosswalk from '../data/examTopics/italian-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/italian-curriculum-crosswalk.json';
import preservationBaseline from './fixtures/italianTopicQuestionBaseline.json';
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

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: Array<{ n: string; primary: string; secondary?: string }>;
}>;

const ROOT = process.cwd();
const baseline = preservationBaseline as Baseline;
const referenceTopics = Object.values(italianReference.variants).flatMap(variant => variant.topics);
const paperIdentity = (paper: { level: string; lang: string; year: number; fileid: string }) => (
  `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`
);

describe('Italian exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('italian')!;

  it('pins the exact flat Higher and Ordinary reference menus', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => ({ label: group.label, level: group.level }))).toEqual([
      { label: 'Higher Level', level: 'higher' },
      { label: 'Ordinary Level', level: 'ordinary' },
    ]);
    expect(taxonomy.groups.map(group => group.topicIds)).toEqual([
      italianReference.variants.higher.topics.map(topic => topic.id),
      italianReference.variants.ordinary.topics.map(topic => topic.id),
    ]);
    expect(taxonomy.topics.map(topic => topic.id)).toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label)).toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.map(topic => topic.sourcePath)).toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(topicsForSubject('italian')).toHaveLength(24);
  });

  it('bridges every practice topic to official Italian curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM
        .find(subject => subject.id === 'italian')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(24);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles all 340 factual associations at an explicit source boundary', () => {
    expect(italianCrosswalk.summary).toMatchObject({
      referenceTopics: 24,
      referenceReportedAssociations: 340,
      referenceOfficialAssociations: 340,
      referenceMockAssociations: 0,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 317,
      sourceBlockedAssociations: 23,
      matchedLocalCardLinks: 478,
    });
    expect(italianCrosswalk.policy.excludedContent).toContain('No commercial mock question');
    const blocked = italianCrosswalk.associations.filter(item => item.resolution === 'source-blocked');
    expect(blocked).toHaveLength(23);
    expect(blocked.every(item => item.year === 2009)).toBe(true);
    expect(blocked.every(item => 'reason' in item && item.reason.includes('begins in 2010'))).toBe(true);
  });

  it('retains every factual heading as part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('italian');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = [...new Set(references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )))].sort();
    expect(references).toHaveLength(501);
    expect(actual).toEqual(expected);
    expect(references.filter(reference => reference.paperKey === 'aural')).toHaveLength(119);
    expect(references.filter(reference => reference.paperKey === 'single')).toHaveLength(382);
  });

  it('preserves all 32 frozen variants and every original card and tag verbatim', () => {
    expect(baseline).toHaveLength(32);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(456);
    for (const expected of baseline) {
      const live = topicsForPaper('italian', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      for (const question of expected.questions) {
        expect(live!.q, `${paperIdentity(expected)} Q${question.n}`).toContainEqual(question);
      }
    }
  });

  it('adds every audited local answer map plus the verified 2026 written papers', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'italian');
    expect(italianCrosswalk.summary).toMatchObject({
      localPaperVariants: 98,
      localPhysicalMappings: 997,
      distinctStudentFacingQuestions: 730,
      referenceMappedLocalQuestions: 388,
      retainedLocalQuestions: 609,
      hostedPaperAnchorMaps: 98,
      preservedBaselineVariants: 32,
      preservedBaselineCards: 456,
      newlyAddedPaperVariants: 66,
      newlyAddedPhysicalMappings: 541,
    });
    expect(papers).toHaveLength(98);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(997);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));

    expect(topicsForPaper('italian', 2026, 'higher', 'ev', 'LC013ALP000BV.pdf')?.q)
      .toHaveLength(25);
    expect(topicsForPaper('italian', 2026, 'ordinary', 'ev', 'LC013GLP000BV.pdf')?.q)
      .toHaveLength(11);
    expect(topicsForPaper('italian', 2018, 'ordinary', 'ev', 'LC013GLP000EV.pdf')?.q)
      .toContainEqual({ n: 'B5', primary: 'italian-5-4' });
    expect(topicsForPaper('italian', 2025, 'higher', 'ev', 'LC013ALP000BV.pdf')?.q.map(q => q.n))
      .toEqual([...Array.from({ length: 20 }, (_, index) => String(index + 1)), 'C1', 'C2', 'C3']);
  });

  it('classifies every physical card into same-level reference buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'italian');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
        expect(examTopicIdsForQuestion(
          'italian', paper.level, paper.year, 'main', question.n,
          paper.paperKey, paper.lang, paper.fileid,
        )).toEqual(ids);
      }
    }
  });

  it('keeps current prescribed texts, legacy literature and writing semantics honest', () => {
    expect(examTopicIdsForQuestion('italian', 'higher', 2026, 'main', '11', 'single', 'ev'))
      .toEqual(['italian-higher-reading-comprehension-le-otto-montagne']);
    expect(examTopicIdsForQuestion('italian', 'higher', 2026, 'main', '16', 'single', 'ev'))
      .toEqual(['italian-higher-reading-comprehension-il-treno-dei-bambini']);
    expect(examTopicIdsForQuestion('italian', 'higher', 2026, 'main', '21', 'single', 'ev'))
      .toEqual(['italian-higher-essay-writing-le-otto-montagne']);
    expect(examTopicIdsForQuestion('italian', 'higher', 2018, 'main', '11', 'single', 'ev'))
      .toEqual(['italian-higher-reading-comprehension-literary-unseen']);
    expect(examTopicIdsForQuestion('italian', 'ordinary', 2018, 'main', 'B5', 'single', 'ev'))
      .toEqual(['italian-ordinary-ads-rulessafety-instructions']);
    expect(examTopicIdsForQuestion('italian', 'ordinary', 2026, 'main', '10', 'single', 'ev'))
      .toEqual(['italian-ordinary-writing-fill-in-a-form']);
  });

  it('ships a finite paper-only fallback for all 997 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'italian');
    for (const paper of papers) {
      const mapPath = path.join(
        ROOT, 'public', 'paper-anchors', String(paper.year), `${paper.fileid}.json`,
      );
      expect(fs.existsSync(mapPath), mapPath).toBe(true);
      const map = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
      expect(isAnswerMap(map), mapPath).toBe(true);
      expect(map.paperOnly, mapPath).toBe(1);
      expect(map.q.map((question: { n: string }) => question.n))
        .toEqual(paper.q.map(question => question.n));
      for (const question of map.q) {
        expect(
          paperRegionFor(map.q, question.n, map.maxCropPages ?? 3),
          `${mapPath} Q${question.n}`,
        ).not.toBeNull();
      }
    }
  });

  it('surfaces all 730 distinct cards and keeps only the unpublished Oral bucket empty', () => {
    expect(subjectAtlasStats('italian')).toMatchObject({
      questions: 730,
      topics: 24,
      yearMin: 2010,
      yearMax: 2026,
    });
    const topics = topicsForSubject('italian');
    const oral = topics.find(topic => topic.subtopicId === 'italian-higher-oral');
    expect(oral).toMatchObject({ count: 0, years: 0 });
    for (const id of italianCrosswalk.summary.emptyReferenceTopics.filter(id => id !== 'italian-higher-oral')) {
      expect(topics.find(topic => topic.subtopicId === id)?.count, id).toBeGreaterThan(0);
    }
  });
});
