/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Engineering reference hierarchy, outgoing/replacement curriculum bridge,
 * complete written-paper corpus, crop boundaries, and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import engineeringReference from '../data/examTopics/engineering.json';
import engineeringEvidence from '../data/examTopics/engineering-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/engineering-curriculum-crosswalk.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { CARDS as ENGINEERING_HIGHER } from '../components/MarkBank/cards/engineering/higher';
import { CARDS as ENGINEERING_ORDINARY } from '../components/MarkBank/cards/engineering/ordinary';
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
import preservationBaseline from './fixtures/engineeringTopicQuestionBaseline.json';

const ROOT = process.cwd();
const VARIANTS = [
  'higher',
  'ordinary',
  'higher-new-course',
  'ordinary-new-course',
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
  variant => engineeringReference.variants[variant].topics,
);
const paperIdentity = (paper: {
  level: string;
  lang: string;
  year: number;
  fileid: string;
}) => `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`;

describe('Engineering exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('engineering')!;

  it('pins the exact outgoing and four-strand replacement hierarchy', () => {
    const expectedGroups = VARIANTS.flatMap((variant) => {
      const source = engineeringReference.variants[variant];
      const level = variant.startsWith('higher') ? 'higher' : 'ordinary';
      const course = variant.endsWith('new-course') ? 'new' : 'old';
      return source.groups.length
        ? source.groups.map(group => ({
            id: group.id,
            label: `${source.label} · ${group.label}`,
            level,
            course,
            topicIds: group.topicIds,
          }))
        : [{
            id: `engineering-${variant}`,
            label: source.label,
            level,
            course,
            topicIds: source.topics.map(topic => topic.id),
          }];
    });
    expect(taxonomy).not.toBeNull();
    expect(taxonomy.groups).toEqual(expectedGroups);
    expect(taxonomy.groups).toHaveLength(10);
    expect(taxonomy.topics.map(topic => topic.id))
      .toEqual(referenceTopics.map(topic => topic.id));
    expect(taxonomy.topics.map(topic => topic.label))
      .toEqual(referenceTopics.map(topic => topic.label));
    expect(taxonomy.topics.map(topic => topic.sourcePath))
      .toEqual(referenceTopics.map(topic => topic.sourcePath));
    expect(topicsForSubject('engineering')).toHaveLength(74);
  });

  it('bridges each practice bucket only to its applicable curriculum', () => {
    const outgoing = resolveCurriculumSpecification('Engineering', 2027)!;
    const replacement = resolveCurriculumSpecification('Engineering', 2028)!;
    const outgoingIds = new Set(
      outgoing.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    const replacementIds = new Set(
      replacement.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(outgoing.id).toBe('engineering:materials-and-technology');
    expect(outgoingIds.size).toBe(16);
    expect(replacement.id).toBe('engineering:2028');
    expect(replacement.coverageNodeLevel).toBe('topic');
    expect(replacementIds.size).toBe(19);
    expect(replacement.groups.map(group => group.title)).toEqual([
      'Engineering Processes',
      'Automation and Control Systems',
      'Design Capability',
      'Engineering Principles and Energy',
    ]);
    expect(replacement.recommendedClassHours).toBe(180);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(74);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk]);
      const canonicalIds = topic.course === 'new' ? replacementIds : outgoingIds;
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
    expect(MARK_BANK_SUBJECTS.find(subject => subject.id === 'engineering')?.spec)
      .toBe('Materials and Technology syllabus');
  });

  it('reconciles all 4,681 listed associations at an explicit source boundary', () => {
    expect(engineeringEvidence.summary).toMatchObject({
      referenceTopics: 74,
      referenceGroups: 8,
      runtimeDisplayGroups: 10,
      referenceReportedAssociations: 4681,
      referenceOfficialAssociations: 2921,
      referenceMockAssociations: 1760,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 2287,
      sourceBlockedAssociations: 634,
      sourceBlockedBreakdown: {
        beforeLocalCorpus: 363,
        deferred: 173,
        sample: 98,
      },
      matchedLogicalCards: 254,
      matchedQuestionTopicLinks: 1568,
      retainedLocalLogicalCards: 0,
    });
    expect(
      engineeringEvidence.summary.referenceOfficialAssociations
      + engineeringEvidence.summary.referenceMockAssociations
      + engineeringEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(engineeringEvidence.summary.referenceReportedAssociations);
    expect(engineeringEvidence.policy.excludedCommercialContent).toContain('Question text');
    expect(engineeringEvidence.associations.filter(item => (
      item.resolution === 'source-blocked' && item.sitting === 'main'
    )).every(item => item.year < 2010)).toBe(true);
    expect(engineeringEvidence.summary.emptyReferenceTopics).toEqual([
      'engineering-higher-practical-exam',
      'engineering-higher-project',
      'engineering-higher-new-course-project-planning-and-evaluation',
      'engineering-ordinary-new-course-control-system-design',
    ]);
  });

  it('retains all 2,921 factual headings exactly and parses the 2016 typo safely', () => {
    const references = examQuestionPartReferencesForSubject('engineering');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(2921);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(1596);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(1325);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
    expect(actual).toEqual(expected);
    const typoRows = engineeringEvidence.associations.filter(item => (
      /^2016 - Section 1 - Question A - Part [bkd]$/.test(item.heading)
    ));
    expect(typoRows).toHaveLength(6);
    expect(typoRows.every(item => item.resolution === 'matched' && item.n === '1')).toBe(true);
  });

  it('preserves all 62 frozen variants and every one of their 476 cards', () => {
    expect(baseline).toHaveLength(62);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(476);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'engineering',
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

  it('adds all four 2026 editions without replacing any existing paper', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'engineering');
    expect(engineeringEvidence.summary).toMatchObject({
      localPaperVariants: 66,
      localPhysicalMappings: 508,
      distinctStudentFacingQuestions: 254,
      newlyAddedPaperVariants: 4,
      newlyAddedPhysicalMappings: 32,
      verifiedSchemeMaps: 64,
      verifiedPaperOnlyMaps: 2,
      preservedBaselineVariants: 62,
      preservedBaselineCards: 476,
    });
    expect(papers).toHaveLength(66);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(508);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    expect(papers.filter(paper => paper.year === 2026)).toHaveLength(4);
    expect(papers.filter(paper => paper.year === 2020)).toHaveLength(2);
  });

  it('classifies every physical card into same-level reference buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'engineering');
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every(id => topics.get(id)?.level === paper.level), (
          `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`
        )).toBe(true);
        expect(examTopicIdsForQuestion(
          'engineering', paper.level, paper.year, 'main', question.n,
          'single', paper.lang,
        )).toEqual(ids);
      }
    }
  });

  it('ships finite paper crops and honest scheme boundaries for all 508 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'engineering');
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
    expect({ schemeMaps, paperOnlyMaps }).toEqual({ schemeMaps: 64, paperOnlyMaps: 2 });
  });

  it('surfaces 254 written questions and preserves all 466 Mark Bank cards', () => {
    expect(subjectAtlasStats('engineering')).toMatchObject({
      questions: 254,
      topics: 74,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(ENGINEERING_HIGHER).toHaveLength(313);
    expect(ENGINEERING_ORDINARY).toHaveLength(153);
    expect(new Set(
      [...ENGINEERING_HIGHER, ...ENGINEERING_ORDINARY].map(card => card.id),
    ).size).toBe(466);
  });
});
