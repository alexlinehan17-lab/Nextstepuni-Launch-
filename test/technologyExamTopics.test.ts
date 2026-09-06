/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Technology reference hierarchy, official-curriculum bridge, complete SEC
 * written-paper corpus, crop boundaries, and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import technologyReference from '../data/examTopics/technology.json';
import technologyEvidence from '../data/examTopics/technology-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/technology-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { SUBJECTS as MARK_BANK_SUBJECTS } from '../components/MarkBank/deck';
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
import { resolveCurriculumSpecification } from '../curriculumRegistry';
import preservationBaseline from './fixtures/technologyTopicQuestionBaseline.json';

const ROOT = process.cwd();
const LEVELS = ['higher', 'ordinary'] as const;

type Baseline = Array<{
  level: 'higher' | 'ordinary';
  lang: 'ev' | 'iv';
  year: number;
  fileid: string;
  paperKey: string;
  questions: string[];
}>;

const baseline = preservationBaseline as Baseline;
const referenceTopics = LEVELS.flatMap(level => technologyReference.variants[level].topics);
const paperIdentity = (paper: {
  level: string;
  lang: string;
  year: number;
  fileid: string;
}) => `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`;

describe('Technology exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('technology')!;

  it('pins the exact flat Higher and Ordinary reference hierarchy', () => {
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups).toEqual(LEVELS.map(level => ({
      id: `technology-${level}`,
      label: technologyReference.variants[level].label,
      level,
      topicIds: technologyReference.variants[level].topics.map(topic => topic.id),
    })));
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.map(topic => topic.sourcePath))
      .toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(topicsForSubject('technology')).toHaveLength(37);
  });

  it('bridges every practice bucket to real canonical Technology nodes', () => {
    const specification = resolveCurriculumSpecification('Technology', 2026)!;
    const canonicalIds = new Set(
      specification.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(specification.id).toBe('technology:current');
    expect(specification.selectionRules?.[0]).toMatchObject({ choose: 2 });
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(37);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
  });

  it('reconciles the complete factual count boundary without copying provider content', () => {
    expect(technologyEvidence.summary).toMatchObject({
      referenceTopics: 37,
      referenceGroups: 0,
      runtimeDisplayGroups: 2,
      referenceReportedAssociations: 2127,
      referenceOfficialAssociations: 1190,
      referenceMockAssociations: 937,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 1118,
      sourceBlockedAssociations: 72,
      sourceBlockedBreakdown: { beforeLocalCorpus: 72 },
      matchedLogicalCards: 580,
      matchedQuestionTopicLinks: 918,
      retainedLocalLogicalCards: 98,
    });
    expect(
      technologyEvidence.summary.referenceOfficialAssociations
      + technologyEvidence.summary.referenceMockAssociations
      + technologyEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(technologyEvidence.summary.referenceReportedAssociations);
    expect(technologyEvidence.policy.excludedCommercialContent).toContain('Question text');
    expect(technologyEvidence.associations.filter(item => (
      item.resolution === 'source-blocked'
    )).every(item => item.year === 2009)).toBe(true);
  });

  it('retains all 1,190 factual headings with level, sitting, and booklet metadata', () => {
    const references = examQuestionPartReferencesForSubject('technology');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(1190);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(632);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(558);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
    expect(references.filter(reference => reference.year >= 2010)
      .every(reference => Boolean(reference.fileid))).toBe(true);
    expect(references.filter(reference => reference.year === 2009)
      .every(reference => !reference.fileid)).toBe(true);
    expect(actual).toEqual(expected);
  });

  it('preserves all 56 frozen variants and every one of their 756 cards', () => {
    expect(baseline).toHaveLength(56);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(756);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'technology',
        expected.year,
        expected.level,
        expected.lang,
        expected.fileid,
      );
      expect(live, paperIdentity(expected)).not.toBeNull();
      expect(live!.paperKey).toBe(expected.paperKey);
      expect(live!.q.map(question => question.n)).toEqual(expected.questions);
    }
  });

  it('adds the omitted editions and every Section B/C booklet additively', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'technology');
    expect(technologyEvidence.summary).toMatchObject({
      localPaperVariants: 132,
      localPhysicalMappings: 1356,
      distinctStudentFacingQuestions: 678,
      newlyAddedPaperVariants: 76,
      newlyAddedPhysicalMappings: 600,
      verifiedSchemeMaps: 61,
      verifiedPaperOnlyMaps: 71,
      preservedBaselineVariants: 56,
      preservedBaselineCards: 756,
    });
    expect(papers).toHaveLength(132);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(1356);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    expect(papers.filter(paper => paper.fileid.includes('LP014'))).toHaveLength(66);
    expect(papers.filter(paper => /LP(?:015|039)/.test(paper.fileid))).toHaveLength(66);
    expect(papers.filter(paper => paper.year === 2020)).toHaveLength(4);
    expect(papers.filter(paper => paper.year === 2026)).toHaveLength(8);
  });

  it('classifies every physical card into same-level reference buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'technology');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
      }
    }
  });

  it('records the four directly reviewed SEC omissions and the reference typo safely', () => {
    const reviewed = technologyEvidence.retainedLocalCards.filter(card => (
      card.resolution === 'retained-local-reviewed'
    ));
    expect(reviewed).toHaveLength(4);
    expect(reviewed.map(card => `${card.level}|${card.year}|${card.questionNumber}`).sort())
      .toEqual(['higher|2022|3', 'higher|2022|4', 'higher|2026|15', 'higher|2026|8']);
    for (const card of reviewed) {
      const level = card.level as 'higher' | 'ordinary';
      expect(examTopicIdsForQuestion(
        'technology', level, card.year, 'main', card.questionNumber, 'single', 'ev',
      )).toEqual(card.topicIds);
      expect(examTopicIdsForQuestion(
        'technology', level, card.year, 'main', card.questionNumber, 'single', 'iv',
      )).toEqual(card.topicIds);
    }
    const typo = technologyEvidence.associations.find(item => (
      item.heading === '2016 - Paper A - Section A - Question 100'
    ));
    expect(typo).toMatchObject({ resolution: 'matched', n: '10' });
  });

  it('keeps Section A and B/C identities distinct and fills official option omissions', () => {
    const sectionA = topicsForPaper(
      'technology', 2025, 'higher', 'ev', 'LC065ALP014EV.pdf',
    )!;
    const sectionBC = topicsForPaper(
      'technology', 2025, 'higher', 'ev', 'LC065ALP039EV.pdf',
    )!;
    expect(sectionA.q.map(question => question.n)).toEqual(
      Array.from({ length: 15 }, (_, index) => `${index + 1}`),
    );
    expect(sectionBC.q.map(question => question.n))
      .toEqual(['B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'C5']);
    expect(examTopicIdsForQuestion(
      'technology', 'higher', 2025, 'main', 'C4', 'single', 'ev',
    )).toContain('technology-higher-option-manufacturing-systems');
    expect(examTopicIdsForQuestion(
      'technology', 'higher', 2025, 'main', 'C5', 'single', 'ev',
    )).toContain('technology-higher-option-materials-technology');
    expect(examTopicIdsForQuestion(
      'technology', 'ordinary', 2025, 'main', 'C3', 'single', 'ev',
    )).toContain('technology-ordinary-option-3-information-communications-technology');
    expect(examTopicIdsForQuestion(
      'technology', 'ordinary', 2025, 'main', 'C5', 'single', 'ev',
    )).toContain('technology-ordinary-option-5-materials-technology');
  });

  it('ships a finite paper crop and honest scheme boundary for all 1,356 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'technology');
    let schemeMaps = 0;
    let paperOnlyMaps = 0;
    for (const paper of papers) {
      const classicPath = path.join(
        ROOT, 'scripts', 'paper-trail', 'answers', String(paper.year), `${paper.fileid}.json`,
      );
      const hostedPath = path.join(
        ROOT, 'public', 'paper-anchors', String(paper.year), `${paper.fileid}.json`,
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
    expect({ schemeMaps, paperOnlyMaps }).toEqual({ schemeMaps: 61, paperOnlyMaps: 71 });

    const higherBC = JSON.parse(fs.readFileSync(
      path.join(ROOT, 'public/paper-anchors/2025/LC065ALP039EV.pdf.json'),
      'utf8',
    ));
    const ordinaryBC = JSON.parse(fs.readFileSync(
      path.join(ROOT, 'public/paper-anchors/2025/LC065GLP039EV.pdf.json'),
      'utf8',
    ));
    expect(paperRegionFor(higherBC.q, 'C4', higherBC.maxCropPages)).toHaveLength(2);
    expect(paperRegionFor(ordinaryBC.q, 'C5', ordinaryBC.maxCropPages)).toHaveLength(1);
  });

  it('surfaces 678 questions in Atlas and does not invent a Mark Bank deck', () => {
    expect(subjectAtlasStats('technology')).toMatchObject({
      questions: 678,
      topics: 37,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(MARK_BANK_SUBJECTS.map(subject => String(subject.id))).not.toContain('technology');
  });
});
