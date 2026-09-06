/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish reference-parity, complete SEC corpus and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import irishReference from '../data/examTopics/irish.json';
import irishCrosswalk from '../data/examTopics/irish-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/irish-curriculum-crosswalk.json';
import preservationBaseline from './fixtures/irishTopicQuestionBaseline.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { PAPER_TRAIL_INDEX } from '../paperTrailData';
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
  examQuestionTopicMappingsForSubject,
  examTopicIdsForQuestion,
  examTopicTaxonomyFor,
} from '../data/examTopics/registry';

type IrishLevel = 'higher' | 'ordinary' | 'foundation';
type Baseline = Array<{
  level: IrishLevel;
  lang: 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: Array<{ n: string; primary: string; secondary?: string }>;
}>;

const ROOT = process.cwd();
const baseline = preservationBaseline as Baseline;
const referenceVariants = Object.entries(irishReference.variants) as Array<[
  IrishLevel,
  (typeof irishReference.variants)[keyof typeof irishReference.variants],
]>;
const referenceTopics = referenceVariants.flatMap(([, variant]) => variant.topics);
const paperIdentity = (paper: { level: string; lang: string; year: number; fileid: string }) => (
  `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`
);

describe('Irish exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('irish')!;

  it('pins the exact three reference menus and appends only two labelled preservation shelves', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => ({ id: group.id, label: group.label, level: group.level })))
      .toEqual([
        { id: 'irish-higher', label: 'Higher Level', level: 'higher' },
        { id: 'irish-ordinary', label: 'Ordinary Level', level: 'ordinary' },
        { id: 'irish-foundation', label: 'Foundation Level', level: 'foundation' },
      ]);
    expect(taxonomy.topics.slice(0, 62).map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.slice(0, 62).map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.slice(0, 62).map(topic => topic.sourcePath))
      .toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(taxonomy.topics.slice(62).map(topic => ({ id: topic.id, label: topic.label })))
      .toEqual([
        {
          id: 'irish-higher-historic-additional-literature',
          label: 'Historic Additional Literature (NextStepUni archive)',
        },
        {
          id: 'irish-foundation-aural-cluastuiscint',
          label: 'Cluastuiscint (NextStepUni archive)',
        },
      ]);
    expect(taxonomy.groups.map(group => group.topicIds.length)).toEqual([26, 26, 12]);
    expect(strandsFor('irish', taxonomy.topics.map(topic => topic.id)).map(group => group.name))
      .toEqual(['Higher Level', 'Ordinary Level', 'Foundation Level']);
  });

  it('bridges every reference and preservation topic to official Irish curriculum nodes', () => {
    const canonicalIds = new Set(
      CURRICULUM
        .find(subject => subject.id === 'irish')!
        .strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(64);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids, topic.id).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles all 842 official headings at an explicit source boundary', () => {
    expect(irishCrosswalk.summary).toMatchObject({
      referenceTopics: 62,
      preservationExtensionTopics: 2,
      runtimeTopics: 64,
      referenceReportedAssociations: 1481,
      referenceOfficialAssociations: 842,
      referenceMockAssociations: 563,
      referenceProviderSampleAssociations: 76,
      matchedAssociations: 534,
      sourceBlockedAssociations: 308,
      sourceBlockedByReason: {
        deferred: 91,
        'pre-corpus': 129,
        sample: 28,
        'oral-material': 60,
      },
      matchedLocalCardLinks: 744,
    });
    expect(irishCrosswalk.policy.excludedContent).toContain('No commercial mock question');
    const blocked = irishCrosswalk.associations.filter(item => item.resolution === 'source-blocked');
    expect(blocked).toHaveLength(308);
    expect(blocked.every(item => 'reason' in item && item.reason.length > 0)).toBe(true);
  });

  it('retains every factual reference heading as part-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('irish');
    const expected = referenceVariants.flatMap(([, variant]) => variant.topics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    ))).sort();
    const actual = [...new Set(references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )))].sort();
    expect(references).toHaveLength(1052);
    expect(actual).toEqual(expected);
    expect(references.filter(reference => reference.sitting === 'deferred')).toHaveLength(91);
    expect(references.filter(reference => reference.sitting === 'sample')).toHaveLength(28);
  });

  it('preserves all 26 frozen variants and every original card and tag verbatim', () => {
    expect(baseline).toHaveLength(26);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(286);
    for (const expected of baseline) {
      const live = topicsForPaper('irish', expected.year, expected.level, expected.lang, expected.fileid);
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      for (const question of expected.questions) {
        expect(live!.q, `${paperIdentity(expected)} Q${question.n}`).toContainEqual(question);
      }
    }
  });

  it('adds every local paper component and every restored section card', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'irish');
    expect(irishCrosswalk.summary).toMatchObject({
      localPaperVariants: 91,
      localPhysicalMappings: 979,
      distinctStudentFacingQuestions: 979,
      referenceMappedLocalQuestions: 686,
      retainedLocalQuestions: 293,
      hostedPaperAnchorMaps: 91,
      preservedBaselineVariants: 26,
      preservedBaselineCards: 286,
      newlyAddedPaperVariants: 65,
      newlyAddedPhysicalMappings: 693,
    });
    expect(papers).toHaveLength(91);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(979);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    const indexPapers = PAPER_TRAIL_INDEX.irish.flatMap(entry => entry.papers);
    expect(indexPapers).toHaveLength(91);

    expect(topicsForPaper('irish', 2026, 'higher', 'iv', 'LC001ALP100IV.pdf')?.q.map(q => q.n))
      .toEqual(['1', '2', '3', '4', 'W-A', 'W-B', 'W-C']);
    expect(topicsForPaper('irish', 2026, 'foundation', 'iv', 'LC001BLP100IV.pdf')?.q.map(q => q.n))
      .toContain('R-3C');
    expect(topicsForPaper('irish', 2010, 'higher', 'iv', 'LC001ALP200IV.pdf')?.q.map(q => q.n))
      .toContain('X');
  });

  it('classifies every physical card into same-level practice buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'irish');
    expect(examQuestionTopicMappingsForSubject('irish').filter(mapping => mapping.lang === 'iv'))
      .toHaveLength(979);
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
        expect(examTopicIdsForQuestion(
          'irish', paper.level, paper.year, 'main', question.n,
          paper.paperKey, paper.lang, paper.fileid,
        )).toEqual(ids);
      }
    }
  });

  it('keeps aural, writing, grammar and preservation identities honest', () => {
    expect(examTopicIdsForQuestion(
      'irish', 'higher', 2026, 'main', '1', 'p1', 'iv', 'LC001ALP100IV.pdf',
    )).toEqual(['irish-higher-aural-fogra-announcement']);
    expect(examTopicIdsForQuestion(
      'irish', 'higher', 2026, 'main', 'W-C', 'p1', 'iv', 'LC001ALP100IV.pdf',
    )).toEqual(['irish-higher-write-a-debate']);
    expect(examTopicIdsForQuestion(
      'irish', 'higher', 2025, 'main', 'W-A', 'p1', 'iv', 'LC001ALP100IV.pdf',
    )).toEqual([
      'irish-higher-write-a-newsmagazine-article',
      'irish-higher-write-an-essay',
    ]);
    expect(examTopicIdsForQuestion(
      'irish', 'higher', 2025, 'main', '6', 'p2', 'iv', 'LC001ALP200IV.pdf',
    )).toEqual(['irish-higher-reading-comprehension', 'irish-higher-grammar']);
    expect(examTopicIdsForQuestion(
      'irish', 'higher', 2025, 'main', 'X', 'p2', 'iv', 'LC001ALP200IV.pdf',
    )).toEqual(['irish-higher-historic-additional-literature']);
    expect(examTopicIdsForQuestion(
      'irish', 'foundation', 2010, 'main', '1', 'single', 'iv', 'LC001BLPA00IV.pdf',
    )).toEqual(['irish-foundation-aural-cluastuiscint']);
    expect(examTopicIdsForQuestion(
      'irish', 'foundation', 2024, 'main', 'W-4B', 'single', 'iv', 'LC001BLP000IV.pdf',
    )).toEqual([
      'irish-foundation-write-a-letter',
      'irish-foundation-fill-in-a-form',
    ]);
  });

  it('ships a finite paper-only fallback for all 979 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'irish');
    expect(VAULT_PREFER_ANCHORS.get('irish')?.('LC001ALP100IV.pdf')).toBe(true);
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

  it('surfaces all 979 questions while keeping provider-only and oral buckets visibly empty', () => {
    expect(subjectAtlasStats('irish')).toMatchObject({
      questions: 979,
      topics: 64,
      yearMin: 2010,
      yearMax: 2026,
    });
    const empty = topicsForSubject('irish').filter(topic => topic.count === 0).map(topic => topic.subtopicId);
    expect(empty).toContain('irish-higher-oral-exam');
    expect(empty).toContain('irish-ordinary-oral-exam');
    expect(empty).toContain('irish-ordinary-write-a-debate');
    expect(empty).toContain('irish-higher-poetry-inion');
    expect(empty).not.toContain('irish-higher-historic-additional-literature');
    expect(empty).not.toContain('irish-foundation-aural-cluastuiscint');
  });
});
