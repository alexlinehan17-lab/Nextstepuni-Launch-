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
      // The 173 deferred headings (2022 and 2023 Higher) resolve to the
      // deferred papers since those joined the Atlas: 2287 + 173 matched.
      matchedAssociations: 2460,
      sourceBlockedAssociations: 461,
      sourceBlockedBreakdown: {
        beforeLocalCorpus: 363,
        deferred: 0,
        sample: 98,
      },
      matchedLogicalCards: 270,
      matchedQuestionTopicLinks: 1675,
      retainedLocalLogicalCards: 0,
      deferredMatchedAssociations: 173,
      deferredQuestionsFromReviewOnly: ['2022|2', '2022|7'],
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
    // A deferred heading names the deferred paper's question, never June's.
    const deferredHeadings = engineeringEvidence.associations.filter(item => item.sitting === 'deferred');
    expect(deferredHeadings).toHaveLength(173);
    for (const item of deferredHeadings) {
      expect(item.resolution, item.heading).toBe('matched');
      expect(item.target?.fileid, item.heading).toBe('LC027ALP000EV-deferred.pdf');
    }
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

  it('adds all four 2026 editions and the two deferred papers without replacing any existing paper', () => {
    const papers = PAPER_TOPIC_TAGS.filter(paper => paper.subjectId === 'engineering');
    expect(engineeringEvidence.summary).toMatchObject({
      localPaperVariants: 68,
      localPhysicalMappings: 526,
      distinctStudentFacingQuestions: 272,
      newlyAddedPaperVariants: 4,
      newlyAddedPhysicalMappings: 32,
      deferredPaperVariants: 2,
      deferredPhysicalMappings: 18,
      verifiedSchemeMaps: 64,
      verifiedPaperOnlyMaps: 4,
      preservedBaselineVariants: 62,
      preservedBaselineCards: 476,
    });
    expect(papers).toHaveLength(68);
    expect(papers.reduce((sum, paper) => sum + paper.q.length, 0)).toBe(526);
    // The SEC's deferred 2022 and 2023 Higher sittings, each its own paper.
    expect(papers.filter(paper => paper.fileid === 'LC027ALP000EV-deferred.pdf')
      .map(paper => `${paper.year}|${paper.level}|${paper.lang}|${paper.q.length}`).sort())
      .toEqual(['2022|higher|ev|9', '2023|higher|ev|9']);
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
        // A deferred paper's questions join on its own file id: without it
        // the lookup is June's question of the same number.
        expect(examTopicIdsForQuestion(
          'engineering', paper.level, paper.year, 'main', question.n,
          'single', paper.lang, paper.fileid.endsWith('-deferred.pdf') ? paper.fileid : undefined,
        )).toEqual(ids);
      }
    }
  });

  it('files each deferred question under its own topics, apart from June\'s', () => {
    const topicsOf = (fileid: string, year: number, n: string) => {
      const paper = topicsForPaper('engineering', year, 'higher', 'ev', fileid)!;
      return browseTopicIdsForQuestion(paper, paper.q.find(question => question.n === n)!);
    };
    // The reference heads no part of 2022's deferred Q7 (polymers): its card
    // review files it, apart from June 2022's Q7.
    expect(topicsOf('LC027ALP000EV-deferred.pdf', 2022, '7')).toEqual([
      'engineering-higher-polymers',
      'engineering-higher-the-structure-of-materials',
    ]);
    expect(topicsOf('LC027ALP000EV.pdf', 2022, '7')).not.toEqual(topicsOf('LC027ALP000EV-deferred.pdf', 2022, '7'));
    // Deferred 2023 Q2 (Extended Reality) carries its card review's Health and Safety.
    expect(topicsOf('LC027ALP000EV-deferred.pdf', 2023, '2')).toEqual([
      'engineering-higher-energy-electronics-robotics',
      'engineering-higher-health-and-safety',
    ]);
  });

  it('ships finite paper crops and honest scheme boundaries for all 526 cards', () => {
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
    expect({ schemeMaps, paperOnlyMaps }).toEqual({ schemeMaps: 64, paperOnlyMaps: 4 });
  });

  it('surfaces 272 written questions and preserves all 2269 Mark Bank cards', () => {
    // 254 June questions and the two deferred papers' 18.
    expect(subjectAtlasStats('engineering')).toMatchObject({
      questions: 272,
      topics: 74,
      yearMin: 2010,
      yearMax: 2026,
    });
    // 466 before the 2024 sittings were re-authored: fifteen asks the reader
    // had mis-keyed or mis-assembled, not fifteen new questions. 550 -> 554
    // when eng-e3/e4/e5's missing pieces landed: five added (2025 Higher
    // Q1(h), Q4(a)(i), Q4(b)(i); 2025 Ordinary Q7(a)(i); 2022 Ordinary
    // Q7(c)(i)) and eng-2025-ol-q2-c-i withdrawn.
    expect(ENGINEERING_HIGHER).toHaveLength(1452);
    expect(ENGINEERING_ORDINARY).toHaveLength(817);
    expect(new Set(
      [...ENGINEERING_HIGHER, ...ENGINEERING_ORDINARY].map(card => card.id),
    ).size).toBe(2269);
  });
});
