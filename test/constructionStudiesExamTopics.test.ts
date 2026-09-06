/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Construction Studies reference hierarchy, overlapping curriculum bridge,
 * complete written-paper corpus, answer boundaries, and preservation gates.
 */

import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import constructionReference from '../data/examTopics/construction-studies.json';
import constructionEvidence from '../data/examTopics/construction-studies-local-crosswalk.json';
import curriculumCrosswalk from '../data/examTopics/construction-studies-curriculum-crosswalk.json';
import reviewedQuestions from '../data/examTopics/construction-studies-reviewed-question-topics.json';
import { PAPER_TOPIC_TAGS } from '../data/paperTrail/topicTags';
import { CARDS as CONSTRUCTION_HIGHER } from '../components/MarkBank/cards/construction-studies/higher';
import { CARDS as CONSTRUCTION_ORDINARY } from '../components/MarkBank/cards/construction-studies/ordinary';
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
import preservationBaseline from './fixtures/constructionStudiesTopicQuestionBaseline.json';

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
  variant => constructionReference.variants[variant].topics,
);
const paperIdentity = (paper: {
  level: string;
  lang: string;
  year: number;
  fileid: string;
}) => `${paper.level}|${paper.lang}|${paper.year}|${paper.fileid}`;

describe('Construction Studies exam-topic registry', () => {
  const taxonomy = examTopicTaxonomyFor('construction-studies')!;

  it('pins the exact outgoing and new-course reference hierarchy', () => {
    const expectedGroups = VARIANTS.flatMap((variant) => {
      const source = constructionReference.variants[variant];
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
            id: `construction-studies-${variant}`,
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
    expect(topicsForSubject('construction-studies')).toHaveLength(103);
  });

  it('bridges each bucket only to the canonical specification for its course', () => {
    const outgoing = resolveCurriculumSpecification('Construction Studies', 2027)!;
    const redeveloped = resolveCurriculumSpecification('Construction Technology', 2028)!;
    const outgoingIds = new Set(
      outgoing.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    const redevelopedIds = new Set(
      redeveloped.groups.flatMap(group => group.topics.map(topic => topic.id)),
    );
    expect(outgoingIds.size).toBe(65);
    expect(redevelopedIds.size).toBe(31);
    expect(redeveloped.groups.map(group => group.title)).toEqual([
      'Built Environment',
      'Design, Materials, and Craft Skills',
      'Building Fabric',
      'Services and Control Technology',
    ]);
    expect(redeveloped.recommendedClassHours).toBe(180);
    expect(Object.keys(curriculumCrosswalk)).toHaveLength(103);
    for (const topic of taxonomy.topics) {
      const ids = curriculumNodeIdsForExamTopic(topic.id);
      expect(ids).toEqual(
        curriculumCrosswalk[topic.id as keyof typeof curriculumCrosswalk],
      );
      const canonicalIds = topic.course === 'new' ? redevelopedIds : outgoingIds;
      expect(ids.length, topic.id).toBeGreaterThan(0);
      expect(ids.filter(id => !canonicalIds.has(id)), topic.id).toEqual([]);
    }
    expect(MARK_BANK_SUBJECTS.find(subject => subject.id === 'construction-studies')?.spec)
      .toBe('outgoing Construction Studies syllabus');
  });

  it('reconciles every factual association with an explicit source boundary', () => {
    expect(constructionEvidence.summary).toMatchObject({
      referenceTopics: 103,
      referenceGroups: 8,
      runtimeDisplayGroups: 10,
      referenceReportedAssociations: 2336,
      referenceOfficialAssociations: 1396,
      referenceMockAssociations: 940,
      referenceProviderSampleAssociations: 0,
      matchedAssociations: 1031,
      sourceBlockedAssociations: 365,
      sourceBlockedBreakdown: {
        beforeLocalCorpus: 225,
        deferredSittings: 49,
        officialSamplePapers: 91,
      },
      matchedLogicalCards: 302,
      matchedQuestionTopicLinks: 1019,
      retainedLocalLogicalCards: 21,
    });
    expect(
      constructionEvidence.summary.referenceOfficialAssociations
      + constructionEvidence.summary.referenceMockAssociations
      + constructionEvidence.summary.referenceProviderSampleAssociations,
    ).toBe(constructionEvidence.summary.referenceReportedAssociations);
    expect(constructionEvidence.policy.excludedCommercialContent).toContain('Question text');
    expect(constructionEvidence.associations.filter(item => (
      item.resolution === 'source-blocked' && item.sitting === 'main'
    )).every(item => item.year < 2010)).toBe(true);
  });

  it('retains all 1,396 headings exactly as level- and sitting-aware metadata', () => {
    const references = examQuestionPartReferencesForSubject('construction-studies');
    const expected = referenceTopics.flatMap(topic => (
      topic.officialQuestionHeadings.map(heading => `${topic.id}|${heading}`)
    )).sort();
    const actual = references.map(reference => (
      `${reference.topicId}|${reference.subdivision}`
    )).sort();
    expect(references).toHaveLength(1396);
    expect(references.filter(reference => reference.level === 'higher')).toHaveLength(877);
    expect(references.filter(reference => reference.level === 'ordinary')).toHaveLength(519);
    expect(references.every(reference => reference.paperKey === 'single')).toBe(true);
    expect(actual).toEqual(expected);
  });

  it('preserves all 63 frozen variants and every one of their 598 cards', () => {
    expect(baseline).toHaveLength(63);
    expect(baseline.reduce((sum, paper) => sum + paper.questions.length, 0)).toBe(598);
    for (const expected of baseline) {
      const live = topicsForPaper(
        'construction-studies',
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

  it('adds the five missing editions without replacing any existing paper', () => {
    const papers = PAPER_TOPIC_TAGS.filter(
      paper => paper.subjectId === 'construction-studies',
    );
    expect(constructionEvidence.summary).toMatchObject({
      localPaperVariants: 68,
      localPhysicalMappings: 646,
      distinctStudentFacingQuestions: 323,
      newlyAddedPaperVariants: 5,
      newlyAddedPhysicalMappings: 48,
      verifiedSchemeMaps: 64,
      verifiedPaperOnlyMaps: 4,
      preservedBaselineVariants: 63,
      preservedBaselineCards: 598,
    });
    expect(papers).toHaveLength(68);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(646);
    expect(new Set(papers.map(paper => paper.year)))
      .toEqual(new Set(Array.from({ length: 17 }, (_, index) => 2010 + index)));
    expect(papers.filter(paper => paper.year === 2026)).toHaveLength(4);
    expect(papers.some(paper => (
      paper.year === 2014 && paper.level === 'higher' && paper.lang === 'ev'
    ))).toBe(true);
  });

  it('classifies every physical card into one or more same-level reference buckets', () => {
    const topics = new Map(taxonomy.topics.map(topic => [topic.id, topic]));
    const papers = PAPER_TOPIC_TAGS.filter(
      paper => paper.subjectId === 'construction-studies',
    );
    for (const paper of papers) {
      for (const question of paper.q) {
        const ids = browseTopicIdsForQuestion(paper, question);
        expect(ids.length, `${paperIdentity(paper)} Q${question.n}`).toBeGreaterThan(0);
        expect(ids.every((id) => {
          const topic = topics.get(id);
          return topic?.level === paper.level;
        }), `${paperIdentity(paper)} Q${question.n}: ${ids.join(', ')}`).toBe(true);
      }
    }
  });

  it('retains all 21 directly reviewed reference omissions in both languages', () => {
    expect(Object.keys(reviewedQuestions.questions)).toHaveLength(21);
    for (const [key, review] of Object.entries(reviewedQuestions.questions)) {
      const [level, year, n] = key.split('|') as [
        'higher' | 'ordinary', string, string,
      ];
      const expectedIds = review.topics.map((label) => {
        const topic = constructionReference.variants[level].topics.find(
          candidate => candidate.label === label,
        );
        expect(topic, `${key}: ${label}`).toBeDefined();
        return topic!.id;
      });
      expect(examTopicIdsForQuestion(
        'construction-studies', level, Number(year), 'main', n, 'single', 'ev',
      )).toEqual(expectedIds);
      expect(examTopicIdsForQuestion(
        'construction-studies', level, Number(year), 'main', n, 'single', 'iv',
      )).toEqual(expectedIds);
    }
    expect(constructionEvidence.retainedLocalCards.every(card => (
      card.resolution === 'retained-local-reviewed'
    ))).toBe(true);
  });

  it('ships a finite paper crop and honest scheme boundary for all 646 cards', () => {
    const papers = PAPER_TOPIC_TAGS.filter(
      paper => paper.subjectId === 'construction-studies',
    );
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
    expect({ schemeMaps, paperOnlyMaps }).toEqual({ schemeMaps: 64, paperOnlyMaps: 4 });
  });

  it('surfaces 323 written questions and preserves all 505 Mark Bank cards', () => {
    expect(subjectAtlasStats('construction-studies')).toMatchObject({
      questions: 323,
      topics: 103,
      yearMin: 2010,
      yearMax: 2026,
    });
    expect(CONSTRUCTION_HIGHER).toHaveLength(255);
    expect(CONSTRUCTION_ORDINARY).toHaveLength(250);
    expect(new Set(
      [...CONSTRUCTION_HIGHER, ...CONSTRUCTION_ORDINARY].map(card => card.id),
    ).size).toBe(505);
  });
});
