/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * DCG reference-taxonomy parity, complete SEC drawing-task coverage, hosted
 * crop, canonical curriculum, and card-preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { CURRICULUM } from '../curriculum';
import dcgReference from '../data/examTopics/design-and-communication-graphics.json';
import dcgCrosswalk from '../data/examTopics/design-and-communication-graphics-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/design-and-communication-graphics-curriculum-crosswalk.json';
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
import preservationBaseline from './fixtures/designAndCommunicationGraphicsTopicQuestionBaseline.json';

const ROOT = process.cwd();

const higherLabels = [
  'Assemblies',
  'Axo / Di / Tri-Metric Projection',
  'Conic Sections',
  'Developments & Envelopments',
  'Dynamic Mechanisms',
  'Geological Geometry',
  'Interpenetration',
  'Intersecting Planes (Laminiar Planes)',
  'Orthographic & Auxiliary Projection +',
  'Perspective',
  'Skew Lines',
  'Solids in Contact',
  'Structural Forms',
  'Surface Geometry',
  'Tetrahedron',
  'The Oblique Plane',
];

const ordinaryLabels = [
  'Assemblies',
  'Axonometric Projection',
  'Conic Sections',
  'Dynamic Mechanisms',
  'Geological Geometry',
  'Interpenetration',
  'Orthographic & Auxillary Projection',
  'Perspective',
  'Rotation & Inclination of Solids',
  'Solids in Contact',
  'Structural Forms (Developments)',
  'Surface Geometry',
  'The Oblique Plane',
];

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

const baseline = preservationBaseline as Baseline;
const evidence = dcgCrosswalk;

describe('Design & Communication Graphics exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('design-and-communication-graphics')!;

  it('pins the exact flat reference hierarchy independently at each level', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups.map(group => [group.label, group.level])).toEqual([
      ['Higher Level', 'higher'],
      ['Ordinary Level', 'ordinary'],
    ]);
    expect(taxonomy.topics.filter(topic => topic.level === 'higher').map(topic => topic.label))
      .toEqual(higherLabels);
    expect(taxonomy.topics.filter(topic => topic.level === 'ordinary').map(topic => topic.label))
      .toEqual(ordinaryLabels);
    expect(topicsForSubject('design-and-communication-graphics')).toHaveLength(29);
  });

  it('bridges every practice bucket only to canonical NCCA DCG nodes', () => {
    const subject = CURRICULUM.find(item => item.id === 'design-and-communication-graphics')!;
    const canonicalIds = new Set(
      subject.strands.flatMap(strand => strand.subtopics.map(topic => topic.id)),
    );
    expect(canonicalIds.size).toBe(26);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(29);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), `${topic.id} has orphaned ids`).toEqual([]);
    }
  });

  it('reconciles every factual association and records each source boundary', () => {
    expect(evidence.summary).toMatchObject({
      referenceTopics: 29,
      referenceReportedAssociations: 787,
      referenceOfficialAssociations: 427,
      referenceMockAssociations: 360,
      matchedAssociations: 386,
      sourceBlockedAssociations: 41,
      matchedLogicalCards: 347,
      matchedQuestionTopicLinks: 373,
      retainedLocalLogicalCards: 49,
    });
    expect(evidence.policy.excludedCommercialContent).toContain('Question text');
    const blocked = evidence.associations.filter(association => association.resolution === 'source-blocked');
    expect(new Set(blocked.map(association => association.year))).toEqual(new Set([2009, 2022, 2023]));
    expect(new Set(blocked.map(association => association.sitting))).toEqual(new Set(['main', 'deferred']));
    expect(blocked.filter(association => association.year === 2009)).toHaveLength(17);
    expect(blocked.filter(association => association.year === 2022)).toHaveLength(13);
    expect(blocked.filter(association => association.year === 2023)).toHaveLength(11);
    expect(evidence.summary.emptyReferenceTopics).toEqual([
      'design-and-communication-graphics-higher-assemblies',
      'design-and-communication-graphics-ordinary-conic-sections',
    ]);
  });

  it('retains all 427 headings as level-, sitting-, and booklet-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('design-and-communication-graphics');
    expect(references).toHaveLength(427);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(249);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(178);
    expect(new Set(references.map(reference => reference.paperKey)))
      .toEqual(new Set(['single', 'section-a']));
    expect(new Set(references.map(reference => (
      `${reference.level}|${reference.topicId}|${reference.subdivision}`
    )))).toHaveLength(427);
  });

  it('preserves all 62 pre-migration variants and all 496 original cards', () => {
    expect(baseline).toHaveLength(62);
    expect(baseline.reduce((count, paper) => count + paper.questions.length, 0)).toBe(496);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'design-and-communication-graphics',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, `${expected.level}|${expected.lang}|${expected.year}|${expected.fileid}`)
        .not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('exposes every A-sheet quadrant and every B1-B3/C1-C5 drawing task', () => {
    expect(evidence.summary).toMatchObject({
      localPaperVariants: 132,
      localPhysicalMappings: 792,
      distinctStudentFacingQuestions: 396,
      hostedAnchorMaps: 132,
      preservedBaselineVariants: 62,
      preservedBaselineCards: 496,
    });
    const papers = PAPER_TOPIC_TAGS.filter(
      paper => paper.subjectId === 'design-and-communication-graphics',
    );
    expect(papers).toHaveLength(132);
    expect(papers.reduce((count, paper) => count + paper.q.length, 0)).toBe(792);
    expect(papers.filter(paper => paper.paperKey === 'section-a')).toHaveLength(66);
    expect(papers.filter(paper => paper.paperKey === 'single')).toHaveLength(66);
    for (const paper of papers) {
      expect(paper.q.map(question => question.n)).toEqual(
        paper.paperKey === 'section-a'
          ? ['1', '2', '3', '4']
          : ['1', '2', '3', '4', '5', '6', '7', '8'],
      );
    }
  });

  it('classifies every physical card into one or more same-level practice buckets', () => {
    const valid = new Map(taxonomy.topics.map(topic => [topic.id, topic.level]));
    const papers = PAPER_TOPIC_TAGS.filter(
      paper => paper.subjectId === 'design-and-communication-graphics',
    );
    for (const paper of papers) {
      for (const question of paper.q) {
        const topicIds = browseTopicIdsForQuestion(paper, question);
        expect(
          topicIds.length,
          `${paper.level}|${paper.lang}|${paper.year}|${paper.paperKey}|${question.n}`,
        ).toBeGreaterThan(0);
        expect(topicIds.every(topicId => valid.get(topicId) === paper.level)).toBe(true);
      }
    }
  });

  it('keeps A-sheet identities separate and retains exact multi-topic joins', () => {
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'higher', 2025, 'main', '1', 'section-a', 'ev',
    )).toEqual([
      'design-and-communication-graphics-higher-axo-di-tri-metric-projection',
      'design-and-communication-graphics-higher-developments-envelopments',
    ]);
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'higher', 2025, 'main', '1', 'single', 'ev',
    )).toEqual(['design-and-communication-graphics-higher-conic-sections']);
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'higher', 2025, 'main', '2', 'single', 'iv',
    )).toEqual([
      'design-and-communication-graphics-higher-intersecting-planes-laminiar-planes',
      'design-and-communication-graphics-higher-the-oblique-plane',
    ]);
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'higher', 2025, 'main', '6', 'single', 'ev',
    )).toEqual([
      'design-and-communication-graphics-higher-developments-envelopments',
      'design-and-communication-graphics-higher-intersecting-planes-laminiar-planes',
      'design-and-communication-graphics-higher-orthographic-auxiliary-projection-plus',
      'design-and-communication-graphics-higher-surface-geometry',
    ]);
  });

  it('keeps reference omissions visible under reviewed same-level topics', () => {
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'higher', 2025, 'main', '8', 'single', 'ev',
    )).toEqual(['design-and-communication-graphics-higher-assemblies']);
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'ordinary', 2025, 'main', '2', 'section-a', 'iv',
    )).toEqual(['design-and-communication-graphics-ordinary-conic-sections']);
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'ordinary', 2019, 'main', '4', 'section-a', 'ev',
    )).toEqual(['design-and-communication-graphics-ordinary-orthographic-auxillary-projection']);
    expect(examTopicIdsForQuestion(
      'design-and-communication-graphics', 'ordinary', 2024, 'main', '3', 'single', 'ev',
    )).toEqual(['design-and-communication-graphics-ordinary-interpenetration']);
  });

  it('ships a valid, finite crop for every one of the 792 physical cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(
      paper => paper.subjectId === 'design-and-communication-graphics',
    );
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
          paperRegionFor(anchorMap.q, question.n),
          `${anchorPath} Q${question.n}`,
        ).not.toBeNull();
      }
      if (paper.paperKey === 'section-a') {
        expect(anchorMap.q.every((question: { paperRegion?: Array<{ r?: number[] }> }) => (
          question.paperRegion?.length === 1
          && question.paperRegion[0].r?.[0] !== 0
          && question.paperRegion[0].r?.[2] !== 1
        ))).toBe(true);
      }
    }
  });

  it('surfaces all 396 entitled tasks through the 29-topic menu', () => {
    expect(subjectAtlasStats('design-and-communication-graphics')).toMatchObject({
      questions: 396,
      topics: 29,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(taxonomy.topics.reduce((count, topic) => count + topic.mockQuestionCount, 0))
      .toBe(360);
    expect(Object.values(dcgReference.levels)
      .flatMap(level => level.topics)
      .reduce((count, topic) => count + topic.officialQuestionHeadings.length, 0))
      .toBe(427);
  });
});
