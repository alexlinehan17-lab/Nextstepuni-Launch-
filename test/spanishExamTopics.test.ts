/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Spanish reference-parity, complete SEC corpus and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import spanishReference from '../data/examTopics/spanish.json';
import spanishCrosswalk from '../data/examTopics/spanish-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/spanish-curriculum-crosswalk.json';
import preservationBaseline from './fixtures/spanishTopicQuestionBaseline.json';
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
const referenceTopics = Object.values(spanishReference.variants).flatMap(variant => variant.topics);
const historicLiteratureId = 'spanish-higher-prescribed-literature-historic-texts';
const paperIdentity = (paper: { level: string; lang: string; year: number; fileid: string }) => (
  `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`
);

describe('Spanish exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('spanish')!;

  it('pins all six exact reference shelves plus one preservation-only literature bucket', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => ({ id: group.id, label: group.label, level: group.level })))
      .toEqual(Object.entries(spanishReference.variants).flatMap(([level, variant]) => (
        variant.groups.map(group => ({
          id: `spanish-${level}-${group.id}`,
          label: group.label,
          level,
        }))
      )));

    for (const [level, variant] of Object.entries(spanishReference.variants)) {
      for (const group of variant.groups) {
        const expected = variant.topics
          .filter(topic => topic.groupId === group.id)
          .map(topic => topic.id);
        if (level === 'higher' && group.id === 'written') expected.push(historicLiteratureId);
        expect(taxonomy.groups.find(item => item.id === `spanish-${level}-${group.id}`)?.topicIds)
          .toEqual(expected);
      }
    }

    expect(taxonomy.topics.slice(0, 33).map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.slice(0, 33).map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.slice(0, 33).map(topic => topic.sourcePath))
      .toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(taxonomy.topics.at(-1)).toMatchObject({
      id: historicLiteratureId,
      label: 'Prescribed Literature (Historic Texts)',
      level: 'higher',
    });
    expect(topicsForSubject('spanish')).toHaveLength(34);
    expect(strandsFor('spanish', taxonomy.topics.map(topic => topic.id)).map(group => group.name))
      .toEqual([
        'Higher Level · Aural',
        'Higher Level · Oral',
        'Higher Level · Written',
        'Ordinary Level · Aural',
        'Ordinary Level · Oral',
        'Ordinary Level · Written',
      ]);
  });

  it('bridges every practice topic to official Spanish curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM
        .find(subject => subject.id === 'spanish')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(34);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles all 471 official associations at an explicit source boundary', () => {
    expect(spanishCrosswalk.summary).toMatchObject({
      referenceTopics: 33,
      runtimeTopics: 34,
      localExtensionTopics: 1,
      referenceReportedAssociations: 822,
      referenceOfficialAssociations: 471,
      referenceMockAssociations: 351,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 397,
      sourceBlockedAssociations: 74,
      sourceBlockedByReason: { preCorpus: 51, deferred: 14, oralBooklet: 9 },
      matchedLocalCardLinks: 559,
    });
    expect(spanishCrosswalk.policy.excludedContent).toContain('No commercial mock question');
    const blocked = spanishCrosswalk.associations.filter(item => item.resolution === 'source-blocked');
    expect(blocked).toHaveLength(74);
    expect(blocked.every(item => 'reason' in item && item.reason.length > 0)).toBe(true);
  });

  it('retains every factual heading as file-aware part metadata', () => {
    const references = examQuestionPartReferencesForSubject('spanish');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = [...new Set(references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )))].sort();
    expect(references).toHaveLength(633);
    expect(actual).toEqual(expected);
    expect(references.filter(reference => reference.fileid)).toHaveLength(559);
    expect(references.filter(reference => reference.paperKey === 'single')).toHaveLength(624);
    expect(references.filter(reference => reference.paperKey === 'oral')).toHaveLength(9);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(14);
  });

  it('preserves all 124 frozen variants and every original card and tag verbatim', () => {
    expect(baseline).toHaveLength(124);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(909);
    for (const expected of baseline) {
      const live = topicsForPaper('spanish', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      for (const question of expected.questions) {
        expect(live!.q, `${paperIdentity(expected)} Q${question.n}`).toContainEqual(question);
      }
    }
  });

  it('adds every reviewed sidecar, 2026 and the missing Ordinary writing choices', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'spanish');
    expect(spanishCrosswalk.summary).toMatchObject({
      localPaperVariants: 136,
      // +8 (2026-11-12): Higher B5 and C2 for 2020 and 2026, both editions;
      // +2: 2020 Higher A1b4 (journalistic Q4), both editions.
      // +5: 2019 Higher B5 and C2, both editions, and A1b4 (English edition).
      // +6: 2018 Higher B5, C2 and A1b4, both editions.
      // +6: 2017 Higher B5, C2 and A1b4, both editions.
      // +5: 2016 Higher B5 and C2, both editions, and A1b4 (English edition).
      // +5: 2015 Higher B5 and C2, both editions, and A1b4 (English edition).
      // +6: 2014 Higher B5, C2 and A1b4, both editions.
      // +5: 2013 Higher B5 and C2, both editions, and A1b4 (English edition).
      localPhysicalMappings: 1229,
      distinctStudentFacingQuestions: 657,
      referenceMappedLocalQuestions: 459,
      retainedLocalQuestions: 770,
      hostedPaperAnchorMaps: 136,
      preservedBaselineVariants: 124,
      preservedBaselineCards: 909,
      newlyAddedPaperVariants: 12,
      newlyAddedPhysicalMappings: 320,
    });
    expect(papers).toHaveLength(136);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(1229);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));

    expect(topicsForPaper('spanish', 2020, 'ordinary', 'iv', 'LC012GLP000IV.pdf')?.q.map(q => q.n))
      .toEqual(['1', '2', '3', '4', '5', 'B1', 'B2A', 'B2B']);
    // Higher Section B Q5 and Section C Q2 are cards of their own wherever
    // the Mark Bank has carded the sitting (es_atlas.py files them there).
    for (const year of [2020, 2026, 2025, 2024, 2023, 2022, 2021, 2019, 2018, 2017, 2016, 2015, 2014, 2013]) {
      expect(topicsForPaper('spanish', year, 'higher', 'ev', 'LC012ALP000EV.pdf')?.q)
        .toEqual(expect.arrayContaining([
          { n: 'B5', primary: 'spanish-6-0' },
          { n: 'C2', primary: 'spanish-6-3', secondary: 'spanish-6-4' },
        ]));
    }
    expect(topicsForPaper('spanish', 2026, 'ordinary', 'ev', 'LC012GLP000EV.pdf')?.q)
      .toEqual(expect.arrayContaining([
        { n: 'B1', primary: 'spanish-6-2' },
        { n: 'B2A', primary: 'spanish-6-4' },
        { n: 'B2B', primary: 'spanish-6-3' },
      ]));
  });

  it('classifies every physical card into same-level reference or preservation buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'spanish');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
        expect(examTopicIdsForQuestion(
          'spanish', paper.level, paper.year, 'main', question.n,
          paper.paperKey, paper.lang, paper.fileid,
        )).toEqual(ids);
      }
    }
  });

  it('keeps written, aural, current literature and historic literature identities honest', () => {
    const written = examTopicIdsForQuestion(
      'spanish', 'higher', 2026, 'main', '1', 'single', 'ev', 'LC012ALP000EV.pdf',
    );
    const aural = examTopicIdsForQuestion(
      'spanish', 'higher', 2026, 'main', '1', 'single', 'ev', 'LC012ALPA00EV.pdf',
    );
    expect(written).toEqual(['spanish-higher-prescribed-literature-ana-alcolea-el-medallon-perdido']);
    expect(aural).toEqual(['spanish-higher-aural-anuncio-announcement']);
    expect(written).not.toEqual(aural);
    expect(examTopicIdsForQuestion(
      'spanish', 'higher', 2025, 'main', '1', 'single', 'ev', 'LC012ALP000EV.pdf',
    )).toEqual([historicLiteratureId]);
    expect(examTopicIdsForQuestion(
      'spanish', 'ordinary', 2020, 'main', 'B1', 'single', 'iv', 'LC012GLP000IV.pdf',
    )).toEqual(['spanish-ordinary-write-a-letteremail']);
    expect(examTopicIdsForQuestion(
      'spanish', 'ordinary', 2020, 'main', 'B2A', 'single', 'iv', 'LC012GLP000IV.pdf',
    )).toEqual(['spanish-ordinary-write-a-note']);
    expect(examTopicIdsForQuestion(
      'spanish', 'ordinary', 2020, 'main', 'B2B', 'single', 'iv', 'LC012GLP000IV.pdf',
    )).toEqual(['spanish-ordinary-write-a-diary-entry']);
  });

  it('ships a finite paper-only fallback for all 1,229 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'spanish');
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

  it('surfaces all 657 distinct questions and only leaves unavailable oral buckets empty', () => {
    expect(subjectAtlasStats('spanish')).toMatchObject({
      questions: 657,
      topics: 34,
      yearMin: 2010,
      yearMax: 2026,
    });
    const topics = topicsForSubject('spanish');
    const empty = topics.filter(topic => topic.count === 0).map(topic => topic.subtopicId).sort();
    expect(empty).toEqual([
      'spanish-higher-oral-exam',
      'spanish-higher-role-play-1-alojamiento',
      'spanish-higher-role-play-2-el-portatil-roto',
      'spanish-higher-role-play-3-una-autocaravanacamper',
      'spanish-higher-role-play-4-el-medio-ambiente',
      'spanish-higher-role-play-5-averia-de-coche',
      'spanish-ordinary-oral-exam',
      'spanish-ordinary-role-play-1-alojamiento',
      'spanish-ordinary-role-play-2-el-portatil-roto',
      'spanish-ordinary-role-play-3-una-autocaravanacamper',
      'spanish-ordinary-role-play-4-el-medio-ambiente',
      'spanish-ordinary-role-play-5-averia-de-coche',
    ].sort());
    expect(topics.find(topic => topic.subtopicId === 'spanish-higher-write-a-dialogue')?.count)
      .toBeGreaterThan(0);
    expect(topics.find(topic => topic.subtopicId === 'spanish-ordinary-comprehension')?.count)
      .toBeGreaterThan(0);
  });
});
