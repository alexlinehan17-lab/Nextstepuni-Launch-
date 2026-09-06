/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Art reference hierarchy, file-aware question joins, complete entitled SEC
 * coverage, crop/scheme boundaries, and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import artReference from '../data/examTopics/art.json';
import artEvidence from '../data/examTopics/art-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/art-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import authoredArt from '../components/MarkBank/cards/art/authored.json';
import { CARDS as ART_HIGHER } from '../components/MarkBank/cards/art/higher';
import { CARDS as ART_ORDINARY } from '../components/MarkBank/cards/art/ordinary';
import {
  browseTopicIdsForQuestion,
  subjectAtlasStats,
  topicsForPaper,
  topicsForSubject,
} from '../components/PaperTrail/topics';
import { paperRegionFor, schemeRegionFor } from '../components/PaperTrail/paperRegion';
import { isAnswerMap } from '../components/PaperTrail/vaultResolve';
import {
  curriculumNodeIdsForExamTopic,
  examQuestionPartReferencesForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';
import preservationBaseline from './fixtures/artTopicQuestionBaseline.json';

const ROOT = process.cwd();
const LEVELS = ['higher', 'ordinary'] as const;
const allReferenceTopics = LEVELS.flatMap(level => artReference.variants[level].topics);

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

const baseline = preservationBaseline as Baseline;
const paperIdentity = (paper: Pick<(typeof PAPER_TOPIC_TAGS)[number], 'level' | 'lang' | 'year' | 'fileid'>) =>
  `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`;

describe('Art exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('art')!;

  it('pins the exact level-aware reference hierarchy, including the flat Ordinary Section A', () => {
    const expectedGroups = [
      ...artReference.variants.higher.groups.map(group => ({
        id: group.id,
        label: group.label,
        level: 'higher' as const,
        topicIds: group.topicIds,
      })),
      {
        id: 'art-ordinary-section-a-todays-world',
        label: "Section A: Today's World",
        level: 'ordinary' as const,
        topicIds: ['art-ordinary-section-a-todays-world'],
      },
      ...artReference.variants.ordinary.groups.map(group => ({
        id: group.id,
        label: group.label,
        level: 'ordinary' as const,
        topicIds: group.topicIds,
      })),
    ];
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups).toEqual(expectedGroups);
    expect(taxonomy.groups).toHaveLength(6);
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(allReferenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(allReferenceTopics.map(topic => topic.label));
    expect(topicsForSubject('art')).toHaveLength(32);
  });

  it('bridges every practice bucket only to canonical NCCA Art nodes', () => {
    const subject = CURRICULUM.find(item => item.id === 'art')!;
    const canonicalIds = new Set(
      subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(canonicalIds.size).toBe(38);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(32);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
    }
  });

  it('reconciles every factual reference item without importing commercial content', () => {
    expect(artEvidence.summary).toMatchObject({
      referenceTopics: 32,
      referenceGroups: 5,
      runtimeDisplayGroups: 6,
      referenceReportedAssociations: 1299,
      referenceOfficialAssociations: 690,
      referenceMockAssociations: 609,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 592,
      sourceBlockedAssociations: 98,
      matchedLogicalCards: 541,
      matchedQuestionTopicLinks: 584,
      retainedLocalLogicalCards: 536,
      retainedWrittenLogicalCards: 144,
      retainedPracticalLogicalCards: 392,
    });
    expect(
      artEvidence.summary.referenceOfficialAssociations
      + artEvidence.summary.referenceMockAssociations
      + artEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(artEvidence.summary.referenceReportedAssociations);
    expect(artEvidence.policy.excludedCommercialContent).toContain('Question text');
    const blocked = artEvidence.associations.filter(item => item.resolution === 'source-blocked');
    expect(blocked.filter(item => item.sitting === 'main').every(item => item.year < 2010))
      .toBe(true);
    expect(blocked.filter(item => item.sitting === 'deferred')).toHaveLength(30);
    expect(blocked.filter(item => item.sitting === 'sample')).toHaveLength(18);
    expect(blocked.every(item => 'reason' in item && item.reason.includes('no StudyClix-hosted')))
      .toBe(true);
  });

  it('retains all 690 headings exactly as level-, sitting-, and file-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('art');
    const expected = allReferenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(690);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(378);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(312);
    expect(references.filter(reference => reference.fileid)).toHaveLength(592);
    expect(actual).toEqual(expected);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
  });

  it('preserves all 136 pre-migration variants and every one of their 1,850 cards', () => {
    expect(baseline).toHaveLength(136);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(1850);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'art',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expect.arrayContaining(expected.questions));
    }
  });

  it('adds every 2023–2026 written-paper edition and exposes all 2,154 physical cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'art');
    expect(artEvidence.summary).toMatchObject({
      localPaperVariants: 152,
      localPhysicalMappings: 2154,
      distinctStudentFacingQuestions: 1077,
      newlyAddedPaperVariants: 16,
      newlyAddedPhysicalMappings: 304,
      verifiedSchemeMaps: 65,
      verifiedPaperOnlyMaps: 87,
      preservedBaselineVariants: 136,
      preservedBaselineCards: 1850,
    });
    expect(papers).toHaveLength(152);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(2154);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    for (const year of [2023, 2024, 2025, 2026]) {
      const added = papers.filter(paper => paper.year === year);
      expect(added).toHaveLength(4);
      expect(added.every(paper => paper.q.length === 19)).toBe(true);
    }
  });

  it('classifies every physical card into one or more same-level reference buckets', () => {
    const valid = new Map(taxonomy.topics.map(topic => [topic.id, topic.level]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'art');
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(topicIds.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(topicIds.every(topicId => valid.get(topicId) === paper.level)).toBe(true);
      }
    }
  });

  it('keeps identically numbered practical and written cards distinct', () => {
    expect(examTopicIdsForQuestion(
      'art', 'higher', 2017, 'main', '1', 'single', 'ev', 'LC014ALP009EV.pdf',
    )).toEqual(['art-higher-artists-processes-and-media']);
    expect(examTopicIdsForQuestion(
      'art', 'higher', 2017, 'main', '1', 'single', 'ev', 'LC014ALP013EV.pdf',
    )).toEqual(['art-higher-pre-christian-ireland-c-4000bc-ad500']);
    expect(examTopicIdsForQuestion(
      'art', 'higher', 2023, 'main', '10', 'single', 'ev', 'LC014ALP000EV.pdf',
    )).toEqual(['art-higher-the-baroque-c-1600-1700s']);
    expect(examTopicIdsForQuestion(
      'art', 'ordinary', 2023, 'main', '1', 'single', 'iv', 'LC014GLP000IV.pdf',
    )).toEqual(['art-ordinary-section-a-todays-world']);
    expect(examTopicIdsForQuestion(
      'art', 'ordinary', 2023, 'main', '8', 'single', 'ev', 'LC014GLP000EV.pdf',
    )).toEqual(['art-ordinary-europe-romanesque-and-gothic']);
  });

  it('ships a valid finite paper boundary and honest scheme boundary for every card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'art');
    let schemeMaps = 0;
    let paperOnlyMaps = 0;
    for (const paper of papers) {
      const classicPath = path.join(
        ROOT,
        'scripts',
        'paper-trail',
        'answers',
        String(paper.year),
        `${paper.fileid}.json`,
      );
      const hostedPath = path.join(
        ROOT,
        'public',
        'paper-anchors',
        String(paper.year),
        `${paper.fileid}.json`,
      );
      const mapPath = fs.existsSync(classicPath) ? classicPath : hostedPath;
      expect(fs.existsSync(mapPath), mapPath).toBe(true);
      const map = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
      expect(isAnswerMap(map), mapPath).toBe(true);
      expect(map.q.map((question: { n: string }) => question.n))
        .toEqual(paper.q.map(question => question.n));
      if (map.paperOnly === 1) paperOnlyMaps += 1;
      else schemeMaps += 1;
      for (const question of map.q) {
        expect(
          paperRegionFor(map.q, question.n, map.maxCropPages ?? 3),
          `${mapPath} Q${question.n} paper`,
        ).not.toBeNull();
        if (question.mode === 'crop') {
          expect(schemeRegionFor(question).length, `${mapPath} Q${question.n} scheme`)
            .toBeGreaterThan(0);
        }
      }
    }
    expect({ schemeMaps, paperOnlyMaps }).toEqual({ schemeMaps: 65, paperOnlyMaps: 87 });
  });

  it('surfaces all 1,077 entitled questions while preserving all 462 authored Mark Bank cards', () => {
    expect(subjectAtlasStats('art')).toMatchObject({
      questions: 1077,
      topics: 32,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(authoredArt.cardCount).toBe(462);
    expect(ART_HIGHER).toHaveLength(222);
    expect(ART_ORDINARY).toHaveLength(240);
    expect(new Set([...ART_HIGHER, ...ART_ORDINARY].map(card => card.id)).size).toBe(462);
  });
});
