/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * French reference-parity, complete SEC corpus and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import frenchReference from '../data/examTopics/french.json';
import frenchCrosswalk from '../data/examTopics/french-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/french-curriculum-crosswalk.json';
import preservationBaseline from './fixtures/frenchTopicQuestionBaseline.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  strandsFor,
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
const referenceTopics = Object.values(frenchReference.variants).flatMap(variant => variant.topics);
const paperIdentity = (paper: { level: string; lang: string; year: number; fileid: string }) => (
  `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`
);

describe('French exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('french')!;

  it('pins both exact flat reference menus', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => ({ label: group.label, level: group.level }))).toEqual([
      { label: 'Higher Level', level: 'higher' },
      { label: 'Ordinary Level', level: 'ordinary' },
    ]);
    expect(taxonomy.groups[0].topicIds).toEqual(frenchReference.variants.higher.topics.map(t => t.id));
    expect(taxonomy.groups[1].topicIds).toEqual(frenchReference.variants.ordinary.topics.map(t => t.id));
    expect(taxonomy.topics.map(topic => topic.id)).toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label)).toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.map(topic => topic.sourcePath)).toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(topicsForSubject('french')).toHaveLength(33);
    expect(strandsFor('french', taxonomy.topics.map(topic => topic.id)).map(group => group.name))
      .toEqual(['Higher Level', 'Ordinary Level']);
  });

  it('bridges every practice topic to official French curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM
        .find(subject => subject.id === 'french')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(33);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles all 739 official associations at an explicit source boundary', () => {
    expect(frenchCrosswalk.summary).toMatchObject({
      referenceTopics: 33,
      referenceReportedAssociations: 1244,
      referenceOfficialAssociations: 739,
      referenceMockAssociations: 505,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 505,
      sourceBlockedAssociations: 234,
      sourceBlockedByReason: { preCorpus: 170, deferred: 60, oralMaterial: 4 },
      matchedLocalCardLinks: 992,
    });
    expect(frenchCrosswalk.policy.excludedContent).toContain('No commercial mock question');
    const blocked = frenchCrosswalk.associations.filter(item => item.resolution === 'source-blocked');
    expect(blocked).toHaveLength(234);
    expect(blocked.every(item => 'reason' in item && item.reason.length > 0)).toBe(true);
  });

  it('retains every factual heading as part-aware reference metadata', () => {
    const references = examQuestionPartReferencesForSubject('french');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = [...new Set(references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )))].sort();
    expect(references).toHaveLength(1226);
    expect(actual).toEqual(expected);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(60);
    expect(references.filter(reference => reference.paperKey === 'oral')).toHaveLength(4);
  });

  it('preserves all 20 frozen variants and every original card and tag verbatim', () => {
    expect(baseline).toHaveLength(20);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(278);
    for (const expected of baseline) {
      const live = topicsForPaper('french', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      for (const question of expected.questions) {
        expect(live!.q, `${paperIdentity(expected)} Q${question.n}`).toContainEqual(question);
      }
    }
  });

  it('adds every reviewed sidecar and the verified missing reading and writing cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'french');
    expect(frenchCrosswalk.summary).toMatchObject({
      localPaperVariants: 98,
      localPhysicalMappings: 1423,
      distinctStudentFacingQuestions: 1003,
      referenceMappedLocalQuestions: 982,
      retainedLocalQuestions: 441,
      hostedPaperAnchorMaps: 98,
      preservedBaselineVariants: 20,
      preservedBaselineCards: 278,
      newlyAddedPaperVariants: 78,
      newlyAddedPhysicalMappings: 1145,
    });
    expect(papers).toHaveLength(98);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(1423);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));

    expect(topicsForPaper('french', 2015, 'ordinary', 'ev', 'LC010GLP000EV.pdf')?.q)
      .toContainEqual({ n: 'A4', primary: 'french-5-1' });
    expect(topicsForPaper('french', 2019, 'ordinary', 'ev', 'LC010GLP000BV.pdf')?.q.map(q => q.n))
      .toEqual(['A1', 'A2', 'A3', 'A4', 'B1A', 'B1B', 'B2A', 'B2B', 'B3A', 'B3B']);
  });

  it('classifies every physical card into same-level reference buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'french');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
        expect(examTopicIdsForQuestion(
          'french', paper.level, paper.year, 'main', question.n,
          paper.paperKey, paper.lang, paper.fileid,
        )).toEqual(ids);
      }
    }
  });

  it('keeps written, aural, restored and reference-omitted task identities honest', () => {
    expect(examTopicIdsForQuestion(
      'french', 'higher', 2026, 'main', '1', 'single', 'ev', 'LC010ALP000BV.pdf',
    )).toEqual(['french-higher-newspapermagazine-comprehension']);
    expect(examTopicIdsForQuestion(
      'french', 'higher', 2026, 'main', '1', 'aural', 'ev', 'LC010ALPA00BV.pdf',
    )).toEqual(['french-higher-aural-conversation']);
    expect(examTopicIdsForQuestion(
      'french', 'ordinary', 2019, 'main', 'A1', 'single', 'ev', 'LC010GLP000BV.pdf',
    )).toEqual(['french-ordinary-reading-comprehension-other-website-magazine-extracts']);
    expect(examTopicIdsForQuestion(
      'french', 'ordinary', 2026, 'main', 'B1B', 'single', 'ev', 'LC010GLP000BV.pdf',
    )).toEqual(['french-ordinary-fill-in-a-form']);
    expect(examTopicIdsForQuestion(
      'french', 'higher', 2010, 'main', 'B1A', 'single', 'ev', 'LC010ALP000EV.pdf',
    )).toEqual(['french-higher-written-production-recit']);
  });

  it('ships a finite paper-only fallback for all 1,423 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'french');
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

  it('surfaces all 1,003 distinct questions and only leaves oral buckets empty', () => {
    expect(subjectAtlasStats('french')).toMatchObject({
      questions: 1003,
      topics: 33,
      yearMin: 2010,
      yearMax: 2026,
    });
    const topics = topicsForSubject('french');
    expect(topics.filter(topic => topic.count === 0).map(topic => topic.subtopicId).sort())
      .toEqual(['french-higher-oral-exam', 'french-ordinary-oral-exam']);
    expect(topics.find(topic => (
      topic.subtopicId === 'french-higher-newspapermagazine-comprehension'
    ))?.count).toBeGreaterThan(0);
    expect(topics.find(topic => topic.subtopicId === 'french-ordinary-fill-in-a-form')?.count)
      .toBeGreaterThan(0);
  });
});
