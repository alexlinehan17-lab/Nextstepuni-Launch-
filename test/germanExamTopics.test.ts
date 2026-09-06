/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * German reference-parity, complete SEC corpus and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import germanReference from '../data/examTopics/german.json';
import germanCrosswalk from '../data/examTopics/german-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/german-curriculum-crosswalk.json';
import preservationBaseline from './fixtures/germanTopicQuestionBaseline.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import {
  browseTopicIdsForQuestion,
  strandsFor,
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import { paperRegionFor } from '../components/PaperTrail/paperRegion';
import { isAnswerMap, VAULT_PREFER_ANCHORS } from '../components/PaperTrail/vaultResolve';
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
const referenceVariants = Object.values(germanReference.variants);
const referenceTopics = referenceVariants.flatMap(variant => variant.topics);
const referenceGroups = referenceVariants.flatMap(variant => variant.groups);
const paperIdentity = (paper: { level: string; lang: string; year: number; fileid: string }) => (
  `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`
);

describe('German exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('german')!;

  it('pins the exact four reference menus and all 25 topics', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => ({ label: group.label, level: group.level }))).toEqual([
      { label: 'Aural', level: 'higher' },
      { label: 'Written', level: 'higher' },
      { label: 'Aural', level: 'ordinary' },
      { label: 'Written', level: 'ordinary' },
    ]);
    expect(taxonomy.groups.map(group => group.topicIds)).toEqual(
      referenceGroups.map(group => group.topicIds.map(id => {
        const level = group === germanReference.variants.higher.groups[0]
          || group === germanReference.variants.higher.groups[1]
          ? 'higher'
          : 'ordinary';
        return `german-${level}-${id}`;
      })),
    );
    expect(taxonomy.topics.map(topic => topic.id)).toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label)).toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.map(topic => topic.sourcePath)).toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(topicsForSubject('german')).toHaveLength(25);
    expect(strandsFor('german', taxonomy.topics.map(topic => topic.id)).map(group => group.name))
      .toEqual([
        'Higher Level · Aural',
        'Higher Level · Written',
        'Ordinary Level · Aural',
        'Ordinary Level · Written',
      ]);
  });

  it('bridges every practice topic to official German curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM
        .find(subject => subject.id === 'german')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(25);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles all 479 official associations at an explicit source boundary', () => {
    expect(germanCrosswalk.summary).toMatchObject({
      referenceTopics: 25,
      referenceReportedAssociations: 820,
      referenceOfficialAssociations: 479,
      referenceMockAssociations: 341,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 379,
      sourceBlockedAssociations: 100,
      sourceBlockedByReason: { preCorpus: 90, deferred: 10 },
      matchedLocalCardLinks: 652,
    });
    expect(germanCrosswalk.policy.excludedContent).toContain('No commercial mock question');
    const blocked = germanCrosswalk.associations.filter(item => item.resolution === 'source-blocked');
    expect(blocked).toHaveLength(100);
    expect(blocked.every(item => 'reason' in item && item.reason.length > 0)).toBe(true);
  });

  it('retains every factual heading as part-aware reference metadata', () => {
    const references = examQuestionPartReferencesForSubject('german');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = [...new Set(references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )))].sort();
    expect(references).toHaveLength(752);
    expect(actual).toEqual(expected);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(10);
  });

  it('preserves all 20 frozen variants and every original card and tag verbatim', () => {
    expect(baseline).toHaveLength(20);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(220);
    for (const expected of baseline) {
      const live = topicsForPaper('german', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      for (const question of expected.questions) {
        expect(live!.q, `${paperIdentity(expected)} Q${question.n}`).toContainEqual(question);
      }
    }
  });

  it('adds every reviewed sidecar and all verified writing choices', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'german');
    expect(germanCrosswalk.summary).toMatchObject({
      localPaperVariants: 100,
      localPhysicalMappings: 970,
      distinctStudentFacingQuestions: 664,
      referenceMappedLocalQuestions: 631,
      retainedLocalQuestions: 339,
      hostedPaperAnchorMaps: 100,
      preservedBaselineVariants: 20,
      preservedBaselineCards: 220,
      newlyAddedPaperVariants: 80,
      newlyAddedPhysicalMappings: 750,
      emptyOfficialReferenceTopics: ['german-ordinary-write-a-blog'],
    });
    expect(papers).toHaveLength(100);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(970);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));

    expect(topicsForPaper('german', 2026, 'higher', 'ev', 'LC011ALP000BV.pdf')?.q.map(q => q.n))
      .toContain('P-B');
    expect(topicsForPaper('german', 2026, 'ordinary', 'ev', 'LC011GLP000BV.pdf')?.q.map(q => q.n))
      .toEqual([
        'I1', 'I2', 'I3', 'I4', 'II1', 'II2', 'II3', 'II4',
        'III1', 'III2', 'III3', 'III4', 'III5', 'G', 'T-A', 'T-B', 'P-A', 'P-B',
      ]);
    expect(topicsForPaper('german', 2013, 'ordinary', 'iv', 'LC011GLP000IV.pdf')?.q.map(q => q.n))
      .toContain('13');
  });

  it('classifies every physical card into same-level reference buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'german');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
        expect(examTopicIdsForQuestion(
          'german', paper.level, paper.year, 'main', question.n,
          paper.paperKey, paper.lang, paper.fileid,
        )).toEqual(ids);
      }
    }
  });

  it('keeps written, aural, multi-topic and retained task identities honest', () => {
    expect(examTopicIdsForQuestion(
      'german', 'higher', 2026, 'main', '1', 'aural', 'ev', 'LC011ALPA00BV.pdf',
    )).toEqual(['german-higher-aural-interview']);
    expect(examTopicIdsForQuestion(
      'german', 'higher', 2026, 'main', 'G', 'single', 'ev', 'LC011ALP000BV.pdf',
    )).toEqual(['german-higher-grammatik-grammar']);
    expect(examTopicIdsForQuestion(
      'german', 'higher', 2026, 'main', 'P-A', 'single', 'ev', 'LC011ALP000BV.pdf',
    )).toEqual(['german-higher-schriftliche-produktion-write-a-letter']);
    expect(examTopicIdsForQuestion(
      'german', 'higher', 2026, 'main', 'P-B', 'single', 'ev', 'LC011ALP000BV.pdf',
    )).toEqual(['german-higher-schriftliche-produktion-picture']);
    expect(examTopicIdsForQuestion(
      'german', 'ordinary', 2026, 'main', 'T-A', 'single', 'ev', 'LC011GLP000BV.pdf',
    )).toEqual([
      'german-ordinary-finish-the-dialogue',
      'german-ordinary-write-on-a-theme-thema',
    ]);
    expect(examTopicIdsForQuestion(
      'german', 'ordinary', 2026, 'main', 'T-B', 'single', 'ev', 'LC011GLP000BV.pdf',
    )).toEqual([
      'german-ordinary-write-an-application',
      'german-ordinary-write-on-a-theme-thema',
    ]);
    expect(examTopicIdsForQuestion(
      'german', 'ordinary', 2025, 'main', 'P-B', 'single', 'ev', 'LC011GLP000BV.pdf',
    )).toEqual([
      'german-ordinary-write-a-story',
      'german-ordinary-write-on-a-topicgive-your-opinion',
    ]);
    expect(examTopicIdsForQuestion(
      'german', 'ordinary', 2013, 'main', '13', 'single', 'iv', 'LC011GLP000IV.pdf',
    )).toEqual(['german-ordinary-comprehension-magazine-or-newspaper']);
  });

  it('ships a finite paper-only fallback for all 970 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'german');
    expect(VAULT_PREFER_ANCHORS.get('german')?.('LC011ALP000BV.pdf')).toBe(true);
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

  it('surfaces all 664 distinct questions and only leaves the mock-only blog bucket empty', () => {
    expect(subjectAtlasStats('german')).toMatchObject({
      questions: 664,
      topics: 25,
      yearMin: 2010,
      yearMax: 2026,
    });
    const topics = topicsForSubject('german');
    expect(topics.filter(topic => topic.count === 0).map(topic => topic.subtopicId).sort())
      .toEqual(['german-ordinary-write-a-blog']);
    expect(topics.find(topic => topic.subtopicId === 'german-higher-aural-dialogue')?.count)
      .toBeGreaterThan(0);
    expect(topics.find(topic => topic.subtopicId === 'german-ordinary-write-an-application')?.count)
      .toBeGreaterThan(0);
  });
});
