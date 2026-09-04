/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Student-facing exam-topic taxonomy.
 *
 * The canonical curriculum registry remains the authority for Syllabus X-Ray.
 * This layer records the flatter, level-aware question groupings students use
 * when browsing exam practice.  Keeping the two identities separate prevents
 * a commercial site's browse menu from erasing official syllabus nodes, while
 * the crosswalk lets the two surfaces link to each other.
 */

import type { PaperLang, PaperLevel } from '../../types/paperTrail';
import { PAPER_TOPIC_TAGS } from '../paperTrail/topicTags';
import accountingAuditJson from './accounting.json';
import agriculturalScienceAuditJson from './agricultural-science.json';
import appliedMathematicsAuditJson from './applied-mathematics.json';
import classicalStudiesAuditJson from './classical-studies.json';
import linkModulesAuditJson from './link-modules.json';
import politicsAndSocietyAuditJson from './politics-and-society.json';

export type ExamSitting = 'main' | 'deferred' | 'sample';

export interface ExamTopicDefinition {
  id: string;
  label: string;
  level: PaperLevel;
  /** Public page path used to re-audit the classification. */
  sourcePath: string;
  /** Official State-exam question identities; never commercial question text. */
  officialQuestionKeys: string[];
  /** Count only. Commercial mock content is deliberately excluded. */
  mockQuestionCount: number;
  /** Canonical curriculum nodes covered by this exam-practice bucket. */
  curriculumNodeIds: string[];
}

export interface ExamTopicGroup {
  id: string;
  label: string;
  level: PaperLevel;
  topicIds: string[];
}

export interface ExamTopicTaxonomy {
  subjectId: string;
  capturedAt: string;
  referenceProvider: string;
  groups: ExamTopicGroup[];
  topics: ExamTopicDefinition[];
}

export interface ExamQuestionPartReference {
  subjectId: string;
  level: PaperLevel;
  year: number;
  sitting: ExamSitting;
  /** Stable Paper Trail slot (`single`, `p1`, `p2`, `aural`, …). */
  paperKey: string;
  /** Top-level number printed on the official paper. */
  n: string;
  /** Factual heading only (section/part/roman-numeral range); never question text. */
  subdivision?: string;
  topicId: string;
}

interface AccountingAuditTopic {
  id: string;
  label: string;
  sourcePath: string;
  officialQuestions: string[];
  mockQuestionCount: number;
}

interface AccountingAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: Record<'higher' | 'ordinary', {
    label: string;
    topics: AccountingAuditTopic[];
  }>;
}

interface AppliedMathematicsAuditTopic {
  id: string;
  label: string;
  sourcePath: string;
  officialQuestionHeadings: string[];
  mockQuestionCount: number;
  empty?: boolean;
}

interface AppliedMathematicsAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: Record<'higher' | 'ordinary', {
    label: string;
    topics: AppliedMathematicsAuditTopic[];
  }>;
}

interface LinkModulesAudit {
  subjectId: string;
  capturedAt: string;
  reference: { provider: string };
  levels: {
    common: {
      label: string;
      topics: AppliedMathematicsAuditTopic[];
    };
  };
}

const accountingAudit = accountingAuditJson as AccountingAudit;
const agriculturalScienceAudit = agriculturalScienceAuditJson as AppliedMathematicsAudit;
const appliedMathematicsAudit = appliedMathematicsAuditJson as AppliedMathematicsAudit;
const classicalStudiesAudit = classicalStudiesAuditJson as AppliedMathematicsAudit;
const linkModulesAudit = linkModulesAuditJson as LinkModulesAudit;
const politicsAndSocietyAudit = politicsAndSocietyAuditJson as AppliedMathematicsAudit;

/**
 * Many-to-many bridge into the official Accounting syllabus.  The order is
 * not a primary/secondary ranking: a StudyClix-style exam bucket can span more
 * than one canonical node, while a question can sit in several exam buckets.
 */
const ACCOUNTING_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'accounting-higher-budgeting-cash': ['accounting-9-6'],
  'accounting-higher-budgeting-flexible': ['accounting-9-5'],
  'accounting-higher-budgeting-production': ['accounting-9-7'],
  'accounting-higher-cash-flow-statements': ['accounting-7-5'],
  'accounting-higher-club-accounts': ['accounting-5-2'],
  'accounting-higher-control-accounts': ['accounting-2-2'],
  'accounting-higher-correction-of-errorssuspense': ['accounting-2-3', 'accounting-2-4'],
  'accounting-higher-costing-job-product-stock-valuation-oh-apportionment': ['accounting-9-2', 'accounting-5-1', 'accounting-9-1'],
  'accounting-higher-costing-marginal': ['accounting-9-3'],
  'accounting-higher-depreciation-of-fixed-assets': ['accounting-2-5'],
  'accounting-higher-farm-accounts': ['accounting-5-4'],
  'accounting-higher-final-accounts-company': ['accounting-4-1'],
  'accounting-higher-final-accounts-manufacturing': ['accounting-5-0'],
  'accounting-higher-final-accounts-sole-trader': ['accounting-3-1'],
  'accounting-higher-fixed-assets-valuation': ['accounting-2-5'],
  'accounting-higher-incomplete-records-a': ['accounting-6-1', 'accounting-6-2', 'accounting-6-3', 'accounting-6-0'],
  'accounting-higher-incomplete-records-b': ['accounting-6-2', 'accounting-6-1', 'accounting-6-3', 'accounting-6-0'],
  'accounting-higher-interpretation-of-accounts': ['accounting-8-1', 'accounting-8-4', 'accounting-8-5', 'accounting-8-6', 'accounting-8-7', 'accounting-8-8', 'accounting-8-9', 'accounting-8-10'],
  'accounting-higher-published-accounts': ['accounting-4-2'],
  'accounting-higher-revaluation-of-fixed-assets': ['accounting-2-5'],
  'accounting-higher-service-firms': ['accounting-5-5'],
  'accounting-higher-tabular-statements': ['accounting-2-6'],

  'accounting-ordinary-bank-reconciliation-statement': ['accounting-2-1'],
  'accounting-ordinary-budgeting-cash': ['accounting-9-6'],
  'accounting-ordinary-budgeting-production': ['accounting-9-7'],
  'accounting-ordinary-cash-flow-statements': ['accounting-7-5'],
  'accounting-ordinary-club-accounts': ['accounting-5-2'],
  'accounting-ordinary-company-profit-loss': ['accounting-4-1'],
  'accounting-ordinary-control-accounts': ['accounting-2-2'],
  'accounting-ordinary-correction-of-errorssuspense': ['accounting-2-3', 'accounting-2-4'],
  'accounting-ordinary-costing-absorption': ['accounting-9-2', 'accounting-9-1'],
  'accounting-ordinary-costing-marginal': ['accounting-9-3'],
  'accounting-ordinary-farm-accounts': ['accounting-5-4'],
  'accounting-ordinary-final-accounts-company': ['accounting-4-1'],
  'accounting-ordinary-final-accounts-departmental': ['accounting-5-3'],
  'accounting-ordinary-final-accounts-manufacturing': ['accounting-5-0'],
  'accounting-ordinary-final-accounts-sole-trader': ['accounting-3-1'],
  'accounting-ordinary-fixed-assets-depreciation-revaluation': ['accounting-2-5'],
  'accounting-ordinary-incomplete-records-control-account': ['accounting-6-1'],
  'accounting-ordinary-incomplete-records-net-worth': ['accounting-6-2'],
  'accounting-ordinary-interpretation-of-accounts': ['accounting-8-1', 'accounting-8-4', 'accounting-8-5', 'accounting-8-6', 'accounting-8-7', 'accounting-8-9'],
  'accounting-ordinary-service-firms': ['accounting-5-5'],
  'accounting-ordinary-tabular-statements': ['accounting-2-6'],
};

const accountingLevels = ['higher', 'ordinary'] as const;
const accountingTopics: ExamTopicDefinition[] = accountingLevels.flatMap((level) =>
  accountingAudit.levels[level].topics.map((topic) => ({
    id: topic.id,
    label: topic.label,
    level,
    sourcePath: topic.sourcePath,
    officialQuestionKeys: topic.officialQuestions,
    mockQuestionCount: topic.mockQuestionCount,
    curriculumNodeIds: ACCOUNTING_CURRICULUM_CROSSWALK[topic.id] ?? [],
  })),
);

const ACCOUNTING_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: accountingAudit.subjectId,
  capturedAt: accountingAudit.capturedAt,
  referenceProvider: accountingAudit.reference.provider,
  groups: accountingLevels.map((level) => ({
    id: `accounting-${level}`,
    label: accountingAudit.levels[level].label,
    level,
    topicIds: accountingAudit.levels[level].topics.map((topic) => topic.id),
  })),
  topics: accountingTopics,
};

/**
 * The official specification remains the canonical mastery model. These links
 * only explain which syllabus ideas can surface inside each student-facing
 * exam-practice bucket. Several of the reference buckets intentionally overlap.
 */
const APPLIED_MATHEMATICS_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'applied-mathematics-higher-circular-motion': ['applied-mathematics-2-7'],
  'applied-mathematics-higher-difference-equations': ['applied-mathematics-3-0', 'applied-mathematics-3-1', 'applied-mathematics-3-2'],
  'applied-mathematics-higher-differential-equations': ['applied-mathematics-3-3', 'applied-mathematics-3-4'],
  'applied-mathematics-higher-further-integration-u-substitution-integration-by-parts': ['applied-mathematics-2-1', 'applied-mathematics-3-4'],
  'applied-mathematics-higher-hookes-law': ['applied-mathematics-2-13'],
  'applied-mathematics-higher-impacts-collisions': ['applied-mathematics-2-4'],
  'applied-mathematics-higher-integration': ['applied-mathematics-2-1', 'applied-mathematics-3-4'],
  'applied-mathematics-higher-mathematical-modelling-project': ['applied-mathematics-0-0', 'applied-mathematics-0-1', 'applied-mathematics-0-2', 'applied-mathematics-0-3', 'applied-mathematics-0-4'],
  'applied-mathematics-higher-networks-and-graphs': ['applied-mathematics-1-0', 'applied-mathematics-1-1', 'applied-mathematics-1-2', 'applied-mathematics-1-3', 'applied-mathematics-1-4'],
  'applied-mathematics-higher-newtons-laws-connected-particles': ['applied-mathematics-2-3', 'applied-mathematics-2-5', 'applied-mathematics-2-10', 'applied-mathematics-2-11'],
  'applied-mathematics-higher-optimal-critical-paths': ['applied-mathematics-1-3', 'applied-mathematics-1-4', 'applied-mathematics-1-5'],
  'applied-mathematics-higher-projectiles': ['applied-mathematics-2-2'],
  'applied-mathematics-higher-uniform-accelerated-motion': ['applied-mathematics-2-0', 'applied-mathematics-2-1'],
  'applied-mathematics-higher-vectors': ['applied-mathematics-2-2', 'applied-mathematics-2-9'],
  'applied-mathematics-higher-work-power-energy-momentum': ['applied-mathematics-2-4', 'applied-mathematics-2-6', 'applied-mathematics-2-12'],

  'applied-mathematics-ordinary-centre-of-gravity': ['applied-mathematics-2-10'],
  'applied-mathematics-ordinary-circular-motion': ['applied-mathematics-2-7'],
  'applied-mathematics-ordinary-difference-equations': ['applied-mathematics-3-0', 'applied-mathematics-3-1', 'applied-mathematics-3-2'],
  'applied-mathematics-ordinary-differential-equations': ['applied-mathematics-3-3', 'applied-mathematics-3-4'],
  'applied-mathematics-ordinary-dimensional-analysis': ['applied-mathematics-2-8'],
  'applied-mathematics-ordinary-hydrostatics': ['applied-mathematics-2-11'],
  'applied-mathematics-ordinary-impacts-collisions': ['applied-mathematics-2-4'],
  'applied-mathematics-ordinary-linear-motion': ['applied-mathematics-2-0', 'applied-mathematics-2-1'],
  'applied-mathematics-ordinary-mathematical-modelling-project': ['applied-mathematics-0-0', 'applied-mathematics-0-1', 'applied-mathematics-0-2', 'applied-mathematics-0-3', 'applied-mathematics-0-4'],
  'applied-mathematics-ordinary-networks-graphs': ['applied-mathematics-1-0', 'applied-mathematics-1-1', 'applied-mathematics-1-2', 'applied-mathematics-1-3', 'applied-mathematics-1-4'],
  'applied-mathematics-ordinary-newtons-laws-connected-particles': ['applied-mathematics-2-3', 'applied-mathematics-2-5'],
  'applied-mathematics-ordinary-optimal-critical-paths': ['applied-mathematics-1-3', 'applied-mathematics-1-4', 'applied-mathematics-1-5'],
  'applied-mathematics-ordinary-projectiles': ['applied-mathematics-2-2'],
  'applied-mathematics-ordinary-relative-velocity': ['applied-mathematics-2-9'],
  'applied-mathematics-ordinary-statics': ['applied-mathematics-2-10'],
  'applied-mathematics-ordinary-uniform-accelerated-motion': ['applied-mathematics-2-0', 'applied-mathematics-2-1'],
  'applied-mathematics-ordinary-vectors': ['applied-mathematics-2-2', 'applied-mathematics-2-9'],
  'applied-mathematics-ordinary-work-energy-power-momentum': ['applied-mathematics-2-4', 'applied-mathematics-2-6', 'applied-mathematics-2-12'],
};

const parseAppliedMathematicsHeading = (heading: string): {
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision?: string;
} => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const question = heading.match(/Question\s+(\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Applied Mathematics reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const afterQuestion = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim();
  const beforeQuestion = heading.slice(4, question.index)
    .replace(/(?:Sample Paper|Deferred Exam Paper|Paper)/gi, '')
    .replace(/^\s*-\s*|\s*-\s*$/g, '')
    .trim();
  const subdivision = [beforeQuestion, afterQuestion].filter(Boolean).join(' · ') || undefined;
  return { year, sitting, paperKey: 'single', n: question[1], subdivision };
};

const appliedMathematicsLevels = ['higher', 'ordinary'] as const;
const appliedMathematicsPartReferences: ExamQuestionPartReference[] = [];
const appliedMathematicsTopics: ExamTopicDefinition[] = appliedMathematicsLevels.flatMap((level) =>
  appliedMathematicsAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseAppliedMathematicsHeading(heading);
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      appliedMathematicsPartReferences.push({
        subjectId: appliedMathematicsAudit.subjectId,
        level,
        ...parsed,
        topicId: topic.id,
      });
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: APPLIED_MATHEMATICS_CURRICULUM_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const APPLIED_MATHEMATICS_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: appliedMathematicsAudit.subjectId,
  capturedAt: appliedMathematicsAudit.capturedAt,
  referenceProvider: appliedMathematicsAudit.reference.provider,
  groups: appliedMathematicsLevels.map((level) => ({
    id: `applied-mathematics-${level}`,
    label: appliedMathematicsAudit.levels[level].label,
    level,
    topicIds: appliedMathematicsAudit.levels[level].topics.map((topic) => topic.id),
  })),
  topics: appliedMathematicsTopics,
};

const AGRICULTURAL_SCIENCE_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'agricultural-science-higher-animal-diseases': ['agricultural-science-3-5'],
  'agricultural-science-higher-animal-physiology-digestive-system': ['agricultural-science-3-0'],
  'agricultural-science-higher-animal-physiology-reproductive-systems': ['agricultural-science-3-0', 'agricultural-science-3-6'],
  'agricultural-science-higher-beef-cattle': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-classification-of-animals-plants': ['agricultural-science-2-1', 'agricultural-science-3-1'],
  'agricultural-science-higher-coursework-project-2025': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-higher-coursework-project-2026': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-higher-crop-production': ['agricultural-science-2-2', 'agricultural-science-2-3', 'agricultural-science-2-4', 'agricultural-science-2-5'],
  'agricultural-science-higher-dairy-cattle': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-energy-crop-catch-crop': ['agricultural-science-2-2', 'agricultural-science-2-3', 'agricultural-science-2-4', 'agricultural-science-2-5'],
  'agricultural-science-higher-fertilisers-pollution-environment-cycles': ['agricultural-science-1-6'],
  'agricultural-science-higher-genetics': ['agricultural-science-3-6'],
  'agricultural-science-higher-grassland': ['agricultural-science-2-6'],
  'agricultural-science-higher-innovation-and-biotechnology-in-agriculture': ['agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-3-6'],
  'agricultural-science-higher-pigs': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-plant-physiology': ['agricultural-science-2-0'],
  'agricultural-science-higher-scientific-practices-experiments-investigations': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-higher-sheep': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-higher-soil-science': ['agricultural-science-1-0', 'agricultural-science-1-1', 'agricultural-science-1-2', 'agricultural-science-1-3', 'agricultural-science-1-4', 'agricultural-science-1-5', 'agricultural-science-1-6'],

  'agricultural-science-ordinary-animal-diseases': ['agricultural-science-3-5'],
  'agricultural-science-ordinary-animal-physiology': ['agricultural-science-3-0', 'agricultural-science-3-6'],
  'agricultural-science-ordinary-animal-production': ['agricultural-science-3-2', 'agricultural-science-3-3', 'agricultural-science-3-4', 'agricultural-science-3-5', 'agricultural-science-3-6'],
  'agricultural-science-ordinary-classification-of-organisms': ['agricultural-science-2-1', 'agricultural-science-3-1'],
  'agricultural-science-ordinary-coursework-project-2021': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-coursework-project-2022': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-coursework-project-2023': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-crop-production': ['agricultural-science-2-2', 'agricultural-science-2-3', 'agricultural-science-2-4', 'agricultural-science-2-5'],
  'agricultural-science-ordinary-fertilisers-pollution-the-environment': ['agricultural-science-1-6'],
  'agricultural-science-ordinary-genetics': ['agricultural-science-3-6'],
  'agricultural-science-ordinary-grassland': ['agricultural-science-2-6'],
  'agricultural-science-ordinary-health-safety': ['agricultural-science-0-4'],
  'agricultural-science-ordinary-innovation-and-biotechnology-in-agriculture': ['agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-3-6'],
  'agricultural-science-ordinary-plant-physiology': ['agricultural-science-2-0'],
  'agricultural-science-ordinary-scientific-practices-experiments-investigations': ['agricultural-science-0-0', 'agricultural-science-0-1', 'agricultural-science-0-2', 'agricultural-science-0-3', 'agricultural-science-0-4'],
  'agricultural-science-ordinary-soil-science': ['agricultural-science-1-0', 'agricultural-science-1-1', 'agricultural-science-1-2', 'agricultural-science-1-3', 'agricultural-science-1-4', 'agricultural-science-1-5', 'agricultural-science-1-6'],
};

const parseAgriculturalScienceHeading = (heading: string, level: PaperLevel): {
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision?: string;
} => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const question = heading.match(/Question\s+([A-Z]|\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Agricultural Science reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const printedQuestion = question[1];
  // Former-course Higher Section 1 printed its short items A–J inside the
  // single locally anchored Q1 region. Retain the letter as subdivision data.
  const isShortItem = level === 'higher' && /^[A-Z]$/i.test(printedQuestion);
  const n = isShortItem ? '1' : printedQuestion;
  const beforeQuestion = heading.slice(4, question.index)
    .replace(/(?:Sample Paper|Deferred Exam Paper|Paper)/gi, '')
    .replace(/^\s*-\s*|\s*-\s*$/g, '')
    .trim();
  const afterQuestion = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim();
  const subdivision = [
    beforeQuestion,
    isShortItem ? `Short question ${printedQuestion.toUpperCase()}` : '',
    afterQuestion,
  ].filter(Boolean).join(' · ') || undefined;
  return { year, sitting, paperKey: 'single', n, subdivision };
};

const agriculturalScienceLevels = ['higher', 'ordinary'] as const;
const agriculturalSciencePartReferences: ExamQuestionPartReference[] = [];
const agriculturalScienceTopics: ExamTopicDefinition[] = agriculturalScienceLevels.flatMap((level) =>
  agriculturalScienceAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseAgriculturalScienceHeading(heading, level);
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      agriculturalSciencePartReferences.push({
        subjectId: agriculturalScienceAudit.subjectId,
        level,
        ...parsed,
        topicId: topic.id,
      });
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: AGRICULTURAL_SCIENCE_CURRICULUM_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const AGRICULTURAL_SCIENCE_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: agriculturalScienceAudit.subjectId,
  capturedAt: agriculturalScienceAudit.capturedAt,
  referenceProvider: agriculturalScienceAudit.reference.provider,
  groups: agriculturalScienceLevels.map((level) => ({
    id: `agricultural-science-${level}`,
    label: agriculturalScienceAudit.levels[level].label,
    level,
    topicIds: agriculturalScienceAudit.levels[level].topics.map((topic) => topic.id),
  })),
  topics: agriculturalScienceTopics,
};

const LINK_MODULES_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'link-modules-common-1-career-investigation': ['lcvp-link-modules-0-2'],
  'link-modules-common-1-introduction-to-working-life': ['lcvp-link-modules-0-0'],
  'link-modules-common-1-job-seeking-skills': ['lcvp-link-modules-0-1', 'lcvp-link-modules-0-4'],
  'link-modules-common-1-work-placement': ['lcvp-link-modules-0-3', 'lcvp-link-modules-1-4'],
  'link-modules-common-2-an-enterprise-activity': ['lcvp-link-modules-1-3'],
  'link-modules-common-2-enterprise-skills': ['lcvp-link-modules-1-0'],
  'link-modules-common-2-local-business-enterprises': ['lcvp-link-modules-1-1'],
  'link-modules-common-2-local-voluntarycommunity-enterprises': ['lcvp-link-modules-1-2'],
  // These are assessment-format buckets whose source material can draw on any
  // unit; they are deliberately excluded from the inverse content fallback.
  'link-modules-common-audio-visual': [
    'lcvp-link-modules-0-0', 'lcvp-link-modules-0-1', 'lcvp-link-modules-0-2',
    'lcvp-link-modules-0-3', 'lcvp-link-modules-0-4', 'lcvp-link-modules-1-0',
    'lcvp-link-modules-1-1', 'lcvp-link-modules-1-2', 'lcvp-link-modules-1-3',
    'lcvp-link-modules-1-4',
  ],
  'link-modules-common-case-study': [
    'lcvp-link-modules-0-0', 'lcvp-link-modules-0-1', 'lcvp-link-modules-0-2',
    'lcvp-link-modules-0-3', 'lcvp-link-modules-0-4', 'lcvp-link-modules-1-0',
    'lcvp-link-modules-1-1', 'lcvp-link-modules-1-2', 'lcvp-link-modules-1-3',
    'lcvp-link-modules-1-4',
  ],
};

const parseLinkModulesHeading = (heading: string): Array<{
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision: string;
}> => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const section = heading.match(/Section\s+([ABC])/i)?.[1]?.toUpperCase();
  if (!year || !section) throw new Error(`Unparseable Link Modules reference heading: ${heading}`);
  const sitting: ExamSitting = /Deferred Exam Paper/i.test(heading) ? 'deferred' : 'main';
  const listed = heading.match(/Questions?\s+((?:\d+\s*,\s*)+\d+)/i);
  const range = heading.match(/Questions?\s+(\d+)(?:-(\d+))?/i);
  let printedNumbers: number[];
  if (listed) {
    printedNumbers = listed[1].split(',').map(value => Number(value.trim()));
  } else if (range) {
    const lo = Number(range[1]);
    const hi = Number(range[2] ?? range[1]);
    printedNumbers = Array.from({ length: hi - lo + 1 }, (_, index) => lo + index);
  } else if (section === 'A') {
    // The 2022 reference heading names the whole section rather than spelling
    // out its printed 1–8 range.
    printedNumbers = [1, 2, 3, 4, 5, 6, 7, 8];
  } else if (section === 'B') {
    printedNumbers = [1, 2, 3];
  } else {
    throw new Error(`Link Modules Section C heading has no question number: ${heading}`);
  }
  const offset = section === 'A' ? 0 : section === 'B' ? 8 : 11;
  const subdivision = heading.replace(/^\d{4}\s*-\s*/, '').trim();
  return printedNumbers.map(number => ({
    year,
    sitting,
    paperKey: 'single',
    n: String(offset + number),
    subdivision,
  }));
};

const linkModulesPartReferences: ExamQuestionPartReference[] = [];
const linkModulesTopics: ExamTopicDefinition[] = linkModulesAudit.levels.common.topics.map((topic) => {
  const officialQuestionKeys = new Set<string>();
  for (const heading of topic.officialQuestionHeadings) {
    for (const parsed of parseLinkModulesHeading(heading)) {
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      linkModulesPartReferences.push({
        subjectId: linkModulesAudit.subjectId,
        level: 'common',
        ...parsed,
        topicId: topic.id,
      });
    }
  }
  return {
    id: topic.id,
    label: topic.label,
    level: 'common',
    sourcePath: topic.sourcePath,
    officialQuestionKeys: [...officialQuestionKeys],
    mockQuestionCount: topic.mockQuestionCount,
    curriculumNodeIds: LINK_MODULES_CURRICULUM_CROSSWALK[topic.id] ?? [],
  };
});

const LINK_MODULES_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: linkModulesAudit.subjectId,
  capturedAt: linkModulesAudit.capturedAt,
  referenceProvider: linkModulesAudit.reference.provider,
  groups: [{
    id: 'link-modules-common',
    label: linkModulesAudit.levels.common.label,
    level: 'common',
    topicIds: linkModulesAudit.levels.common.topics.map(topic => topic.id),
  }],
  topics: linkModulesTopics,
};

const CLASSICAL_STUDIES_CURRICULUM_CROSSWALK: Record<string, string[]> = {
  'classical-studies-higher-funerary-practices': ['classical-studies-3-2'],
  'classical-studies-higher-greek-drama': ['classical-studies-1-0', 'classical-studies-1-1', 'classical-studies-1-2'],
  'classical-studies-higher-mythology': ['classical-studies-0-2', 'classical-studies-3-0'],
  'classical-studies-higher-philosophy': ['classical-studies-3-3'],
  'classical-studies-higher-power-and-identity': ['classical-studies-2-0', 'classical-studies-2-1', 'classical-studies-2-2', 'classical-studies-2-3', 'classical-studies-2-4'],
  'classical-studies-higher-roman-spectacle': ['classical-studies-1-3'],
  'classical-studies-higher-temples': ['classical-studies-3-1'],
  'classical-studies-higher-world-of-heroes': ['classical-studies-0-0', 'classical-studies-0-1', 'classical-studies-0-2', 'classical-studies-0-3', 'classical-studies-0-4'],

  'classical-studies-ordinary-funerary-practices': ['classical-studies-3-2'],
  'classical-studies-ordinary-greek-drama': ['classical-studies-1-0', 'classical-studies-1-1', 'classical-studies-1-2'],
  'classical-studies-ordinary-mythology': ['classical-studies-0-2', 'classical-studies-3-0'],
  'classical-studies-ordinary-philosophy': ['classical-studies-3-3'],
  'classical-studies-ordinary-power-and-identity': ['classical-studies-2-0', 'classical-studies-2-1', 'classical-studies-2-2', 'classical-studies-2-3', 'classical-studies-2-4'],
  'classical-studies-ordinary-roman-spectacle': ['classical-studies-1-3'],
  'classical-studies-ordinary-temples': ['classical-studies-3-1'],
  'classical-studies-ordinary-world-of-heroes': ['classical-studies-0-0', 'classical-studies-0-1', 'classical-studies-0-2', 'classical-studies-0-3', 'classical-studies-0-4'],
};

const parseClassicalStudiesHeading = (heading: string): {
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision?: string;
} => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const question = heading.match(/Question\s+(\d+)/i);
  if (!year || !question) throw new Error(`Unparseable Classical Studies reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  const subdivision = heading.slice((question.index ?? 0) + question[0].length)
    .replace(/^\s*-\s*/, '')
    .trim() || undefined;
  return { year, sitting, paperKey: 'single', n: question[1], subdivision };
};

const classicalStudiesLevels = ['higher', 'ordinary'] as const;
const classicalStudiesPartReferences: ExamQuestionPartReference[] = [];
const classicalStudiesTopics: ExamTopicDefinition[] = classicalStudiesLevels.flatMap((level) =>
  classicalStudiesAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      const parsed = parseClassicalStudiesHeading(heading);
      officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
      classicalStudiesPartReferences.push({
        subjectId: classicalStudiesAudit.subjectId,
        level,
        ...parsed,
        topicId: topic.id,
      });
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: CLASSICAL_STUDIES_CURRICULUM_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const CLASSICAL_STUDIES_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: classicalStudiesAudit.subjectId,
  capturedAt: classicalStudiesAudit.capturedAt,
  referenceProvider: classicalStudiesAudit.reference.provider,
  groups: classicalStudiesLevels.map((level) => ({
    id: `classical-studies-${level}`,
    label: classicalStudiesAudit.levels[level].label,
    level,
    topicIds: classicalStudiesAudit.levels[level].topics.map(topic => topic.id),
  })),
  topics: classicalStudiesTopics,
};

/**
 * Politics & Society has eight content themes plus two deliberately overlapping
 * assessment lenses. The official curriculum tree remains intact; these links
 * only power the simpler exam-practice menu students browse in Topic Atlas.
 */
const POLITICS_AND_SOCIETY_CONTENT_CROSSWALK: Record<string, string[]> = {
  '1-power-and-decision-making-at-national-and-european-level': [
    'politics-and-society-0-4', 'politics-and-society-0-5', 'politics-and-society-0-6',
    'politics-and-society-0-7', 'politics-and-society-0-8', 'politics-and-society-0-9',
    'politics-and-society-0-10', 'politics-and-society-0-12',
  ],
  '1-power-and-decision-making-in-the-school': [
    'politics-and-society-0-0', 'politics-and-society-0-1', 'politics-and-society-0-2',
    'politics-and-society-0-3', 'politics-and-society-0-11',
  ],
  '2-effectively-contributing-to-communities': [
    'politics-and-society-1-0', 'politics-and-society-1-1', 'politics-and-society-1-2',
    'politics-and-society-1-3', 'politics-and-society-1-4', 'politics-and-society-1-5',
    'politics-and-society-1-11',
  ],
  '2-rights-and-responsibilities-in-communication-with-others': [
    'politics-and-society-1-6', 'politics-and-society-1-7', 'politics-and-society-1-8',
    'politics-and-society-1-9', 'politics-and-society-1-10', 'politics-and-society-1-12',
  ],
  '3-human-rights-and-responsibilities-in-europe-and-the-wider-world': [
    'politics-and-society-2-7', 'politics-and-society-2-8', 'politics-and-society-2-9',
    'politics-and-society-2-11',
  ],
  '3-human-rights-and-responsibilities-in-ireland': [
    'politics-and-society-2-0', 'politics-and-society-2-1', 'politics-and-society-2-2',
    'politics-and-society-2-3', 'politics-and-society-2-4', 'politics-and-society-2-5',
    'politics-and-society-2-6', 'politics-and-society-2-10',
  ],
  '4-globalisation-and-identity': [
    'politics-and-society-3-0', 'politics-and-society-3-1', 'politics-and-society-3-2',
    'politics-and-society-3-3', 'politics-and-society-3-4', 'politics-and-society-3-5',
    'politics-and-society-3-6', 'politics-and-society-3-10',
  ],
  '4-sustainable-development': [
    'politics-and-society-3-7', 'politics-and-society-3-8', 'politics-and-society-3-9',
    'politics-and-society-3-11',
  ],
};

const POLITICS_AND_SOCIETY_ALL_CONTENT_NODES = [...new Set(
  Object.values(POLITICS_AND_SOCIETY_CONTENT_CROSSWALK).flat(),
)];
const POLITICS_AND_SOCIETY_CROSSWALK: Record<string, string[]> = {};
for (const level of ['higher', 'ordinary'] as const) {
  for (const [slug, ids] of Object.entries(POLITICS_AND_SOCIETY_CONTENT_CROSSWALK)) {
    POLITICS_AND_SOCIETY_CROSSWALK[`politics-and-society-${level}-${slug}`] = ids;
  }
  // Data-based questions are an assessment format which may draw on any of
  // the eight official themes, so the bridge is intentionally broad.
  POLITICS_AND_SOCIETY_CROSSWALK[`politics-and-society-${level}-data-based-questions`] =
    POLITICS_AND_SOCIETY_ALL_CONTENT_NODES;
  POLITICS_AND_SOCIETY_CROSSWALK[`politics-and-society-${level}-key-thinkers`] = [
    'politics-and-society-0-10',
    'politics-and-society-2-6',
    'politics-and-society-3-6',
    'politics-and-society-3-9',
  ];
}

const parsePoliticsAndSocietyHeading = (
  level: 'higher' | 'ordinary',
  heading: string,
): Array<{
  year: number;
  sitting: ExamSitting;
  paperKey: 'single';
  n: string;
  subdivision: string;
}> => {
  const year = Number(heading.match(/^(\d{4})/)?.[1]);
  const section = heading.match(/Section\s+([A-Za-z]\d?)/i)?.[1]?.toUpperCase();
  if (!year || !section) throw new Error(`Unparseable Politics and Society reference heading: ${heading}`);
  const sitting: ExamSitting = /Sample Paper/i.test(heading)
    ? 'sample'
    : /Deferred Exam Paper/i.test(heading)
      ? 'deferred'
      : 'main';
  let numbers: string[];
  if (section.startsWith('A')) {
    // The reference lists individual lettered short-answer parts while Paper
    // Trail deliberately exposes the complete Section A as one question card.
    numbers = ['1'];
  } else if (section === 'B') {
    // Higher exposes the complete DBQ as Q2. Ordinary exposes its three
    // printed questions as cards 2–4, even when the reference heading shortens
    // the whole section to just "Question 2".
    numbers = level === 'ordinary' ? ['2', '3', '4'] : ['2'];
  } else if (section === 'C') {
    const number = heading.match(/Question\s+(\d+)/i)?.[1];
    if (!number) throw new Error(`Politics and Society Section C heading has no question number: ${heading}`);
    numbers = [number];
  } else {
    throw new Error(`Unknown Politics and Society section in reference heading: ${heading}`);
  }
  const subdivision = heading.replace(/^\d{4}\s*-\s*/, '').trim();
  return numbers.map(n => ({ year, sitting, paperKey: 'single', n, subdivision }));
};

const politicsAndSocietyLevels = ['higher', 'ordinary'] as const;
const politicsAndSocietyPartReferences: ExamQuestionPartReference[] = [];
const politicsAndSocietyTopics: ExamTopicDefinition[] = politicsAndSocietyLevels.flatMap((level) =>
  politicsAndSocietyAudit.levels[level].topics.map((topic) => {
    const officialQuestionKeys = new Set<string>();
    for (const heading of topic.officialQuestionHeadings) {
      for (const parsed of parsePoliticsAndSocietyHeading(level, heading)) {
        officialQuestionKeys.add(`${parsed.year}|${parsed.sitting}|${parsed.n}`);
        politicsAndSocietyPartReferences.push({
          subjectId: politicsAndSocietyAudit.subjectId,
          level,
          ...parsed,
          topicId: topic.id,
        });
      }
    }
    return {
      id: topic.id,
      label: topic.label,
      level,
      sourcePath: topic.sourcePath,
      officialQuestionKeys: [...officialQuestionKeys],
      mockQuestionCount: topic.mockQuestionCount,
      curriculumNodeIds: POLITICS_AND_SOCIETY_CROSSWALK[topic.id] ?? [],
    };
  }),
);

const POLITICS_AND_SOCIETY_TAXONOMY: ExamTopicTaxonomy = {
  subjectId: politicsAndSocietyAudit.subjectId,
  capturedAt: politicsAndSocietyAudit.capturedAt,
  referenceProvider: politicsAndSocietyAudit.reference.provider,
  groups: politicsAndSocietyLevels.map(level => ({
    id: `politics-and-society-${level}`,
    label: politicsAndSocietyAudit.levels[level].label,
    level,
    topicIds: politicsAndSocietyAudit.levels[level].topics.map(topic => topic.id),
  })),
  topics: politicsAndSocietyTopics,
};

const TAXONOMIES = new Map<string, ExamTopicTaxonomy>([
  [ACCOUNTING_TAXONOMY.subjectId, ACCOUNTING_TAXONOMY],
  [AGRICULTURAL_SCIENCE_TAXONOMY.subjectId, AGRICULTURAL_SCIENCE_TAXONOMY],
  [APPLIED_MATHEMATICS_TAXONOMY.subjectId, APPLIED_MATHEMATICS_TAXONOMY],
  [CLASSICAL_STUDIES_TAXONOMY.subjectId, CLASSICAL_STUDIES_TAXONOMY],
  [LINK_MODULES_TAXONOMY.subjectId, LINK_MODULES_TAXONOMY],
  [POLITICS_AND_SOCIETY_TAXONOMY.subjectId, POLITICS_AND_SOCIETY_TAXONOMY],
]);

const TOPICS_BY_ID = new Map<string, ExamTopicDefinition>();
const QUESTION_TOPICS = new Map<string, string[]>();

const questionKey = (
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  n: string,
  paperKey = 'single',
  lang: PaperLang | 'any' = 'any',
) => `${subjectId}|${level}|${year}|${sitting}|${paperKey}|${lang}|${n}`;

for (const taxonomy of TAXONOMIES.values()) {
  for (const topic of taxonomy.topics) {
    TOPICS_BY_ID.set(topic.id, topic);
    for (const officialKey of topic.officialQuestionKeys) {
      const [year, sitting, ...identity] = officialKey.split('|');
      const paperKey = identity.length === 1 ? 'single' : identity[0];
      const n = identity.length === 1 ? identity[0] : identity[1];
      const key = questionKey(
        taxonomy.subjectId,
        topic.level,
        Number(year),
        sitting as ExamSitting,
        n,
        paperKey,
      );
      const ids = QUESTION_TOPICS.get(key) ?? [];
      if (!ids.includes(topic.id)) ids.push(topic.id);
      QUESTION_TOPICS.set(key, ids);
    }
  }
}

/**
 * Verified local questions omitted from the reference site's topic pages.
 * Retaining these explicit exceptions is safer than silently making a valid
 * SEC question disappear merely to make two headline counts agree.
 */
const RETAINED_LOCAL_ASSOCIATIONS: Array<{
  subjectId: string;
  level: PaperLevel;
  year: number;
  sitting: ExamSitting;
  paperKey?: string;
  /** Only needed where translated answer-map anchors are not structurally aligned. */
  lang?: PaperLang;
  n: string;
  topicIds: string[];
  reason?: string;
}> = [
  {
    subjectId: 'accounting',
    level: 'higher',
    year: 2017,
    sitting: 'main',
    n: '4',
    // The paper itself titles this "Departmental Final Accounts of a Sole
    // Trader". Higher has no separate Departmental bucket in the reference.
    topicIds: ['accounting-higher-final-accounts-sole-trader'],
  },
  {
    subjectId: 'accounting',
    level: 'ordinary',
    year: 2017,
    sitting: 'main',
    n: '5',
    topicIds: ['accounting-ordinary-interpretation-of-accounts'],
  },
];

/**
 * The reference pages omit 113 valid 2010–2022 questions from the former
 * Applied Mathematics course. Map only those omissions through their existing,
 * frozen canonical tags. This keeps the exact current reference menu while
 * retaining every local question; it never overwrites a reference association.
 */
const appliedTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of APPLIED_MATHEMATICS_TAXONOMY.topics) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = appliedTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    appliedTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

const agriculturalTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of AGRICULTURAL_SCIENCE_TAXONOMY.topics) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = agriculturalTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    agriculturalTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

const linkModuleContentTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of LINK_MODULES_TAXONOMY.topics.filter(topic =>
  !topic.id.endsWith('-audio-visual') && !topic.id.endsWith('-case-study'))) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const ids = linkModuleContentTopicsByCanonicalNode.get(curriculumNodeId) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    linkModuleContentTopicsByCanonicalNode.set(curriculumNodeId, ids);
  }
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'applied-mathematics') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => appliedTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    QUESTION_TOPICS.set(key, topicIds);
    if (!RETAINED_LOCAL_ASSOCIATIONS.some(item =>
      item.subjectId === paper.subjectId
      && item.level === paper.level
      && item.year === paper.year
      && item.sitting === 'main'
      && item.n === question.n)) {
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: paper.subjectId,
        level: paper.level,
        year: paper.year,
        sitting: 'main',
        n: question.n,
        topicIds,
        reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
      });
    }
  }
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'agricultural-science') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => agriculturalTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    QUESTION_TOPICS.set(key, topicIds);
    if (!RETAINED_LOCAL_ASSOCIATIONS.some(item =>
      item.subjectId === paper.subjectId
      && item.level === paper.level
      && item.year === paper.year
      && item.sitting === 'main'
      && item.n === question.n)) {
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: paper.subjectId,
        level: paper.level,
        year: paper.year,
        sitting: 'main',
        n: question.n,
        topicIds,
        reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
      });
    }
  }
}

// The 2021 Higher Q4 anchor predates the committed canonical tag wave and is
// also absent from the reference pages. Its official stem is about farm energy
// efficiency and environmental sustainability, so retain it explicitly in the
// environment bucket rather than allowing it to disappear from Topic Atlas.
if (!QUESTION_TOPICS.has(questionKey('agricultural-science', 'higher', 2021, 'main', '4'))) {
  RETAINED_LOCAL_ASSOCIATIONS.push({
    subjectId: 'agricultural-science',
    level: 'higher',
    year: 2021,
    sitting: 'main',
    n: '4',
    topicIds: ['agricultural-science-higher-fertilisers-pollution-environment-cycles'],
    reason: 'Valid local question omitted from both the reference topic pages and the earlier tag wave; retained from its official SEC stem.',
  });
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'link-modules') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const number = Number(question.n);
    const topicIds = number <= 8
      ? ['link-modules-common-audio-visual']
      : number <= 11
        ? ['link-modules-common-case-study']
        : [...new Set(
          [question.primary, question.secondary]
            .filter((id): id is string => Boolean(id))
            .flatMap(id => linkModuleContentTopicsByCanonicalNode.get(id) ?? []),
        )];
    if (!topicIds.length) continue;
    QUESTION_TOPICS.set(key, topicIds);
    if (!RETAINED_LOCAL_ASSOCIATIONS.some(item =>
      item.subjectId === paper.subjectId
      && item.year === paper.year
      && item.n === question.n)) {
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: paper.subjectId,
        level: paper.level,
        year: paper.year,
        sitting: 'main',
        n: question.n,
        topicIds,
        reason: 'Valid local question omitted from the reference topic pages; retained by assessment section and verified canonical tag.',
      });
    }
  }
}

const classicalTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of CLASSICAL_STUDIES_TAXONOMY.topics) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = classicalTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    classicalTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'classical-studies') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => classicalTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    RETAINED_LOCAL_ASSOCIATIONS.push({
      subjectId: paper.subjectId,
      level: paper.level,
      year: paper.year,
      sitting: 'main',
      n: question.n,
      topicIds,
      reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
    });
  }
}

const classicalTopicIds = (
  level: 'higher' | 'ordinary',
  slugs: string[],
) => slugs.map(slug => `classical-studies-${level}-${slug}`);

// The reference retains useful fragments of the retired ten-topic course but
// omits whole valid questions when their former topic has no exact modern
// equivalent. Keep the eight-bucket menu intact and conservatively cross-list
// those questions in the closest surviving practice buckets.
const CLASSICAL_LEGACY_FALLBACKS: Record<string, string[]> = {
  '1': ['power-and-identity'],
  '2': ['power-and-identity'],
  '3': ['power-and-identity', 'philosophy'],
  '4': ['power-and-identity'],
  '5': ['greek-drama'],
  '6': ['world-of-heroes'],
  '7': ['philosophy', 'world-of-heroes'],
  '8': ['temples', 'funerary-practices', 'mythology'],
  '9': ['philosophy'],
  '10': ['temples', 'roman-spectacle', 'funerary-practices'],
};

for (const level of classicalStudiesLevels) {
  for (let year = 2010; year <= 2022; year++) {
    if (level === 'ordinary' && year === 2020) continue;
    for (let n = 1; n <= 10; n++) {
      const number = String(n);
      const key = questionKey('classical-studies', level, year, 'main', number);
      if (QUESTION_TOPICS.has(key)) continue;
      RETAINED_LOCAL_ASSOCIATIONS.push({
        subjectId: 'classical-studies',
        level,
        year,
        sitting: 'main',
        n: number,
        topicIds: classicalTopicIds(level, CLASSICAL_LEGACY_FALLBACKS[number]),
        reason: 'Valid retired-course question omitted from the reference topic pages; retained in the closest surviving exam buckets from its official course topic.',
      });
    }
  }
}

const CLASSICAL_2026_TOPICS: Record<'higher' | 'ordinary', Record<string, string[]>> = {
  higher: {
    '1': ['temples'],
    '2': ['temples'],
    '3': ['mythology'],
    '4': ['world-of-heroes'],
    '5': ['greek-drama'],
    '6': ['greek-drama'],
    '7': ['power-and-identity'],
    '8': ['power-and-identity'],
    '9': ['funerary-practices'],
    '10': ['philosophy'],
    '11': ['world-of-heroes'],
    '12': ['philosophy'],
    '13': ['greek-drama'],
    '14': ['power-and-identity'],
    '15': ['temples'],
    '16': ['roman-spectacle'],
  },
  ordinary: {
    '1': ['mythology'],
    '2': ['world-of-heroes'],
    '3': ['temples'],
    '4': ['funerary-practices'],
    '5': ['philosophy'],
    '6': ['greek-drama'],
    '7': ['roman-spectacle'],
    '8': ['roman-spectacle'],
    '9': ['power-and-identity'],
    '10': ['power-and-identity'],
    '11': ['world-of-heroes'],
    '12': ['power-and-identity'],
    '13': ['temples'],
    '14': ['greek-drama'],
    '15': ['philosophy'],
    '16': ['funerary-practices'],
  },
};

for (const level of classicalStudiesLevels) {
  for (const [n, slugs] of Object.entries(CLASSICAL_2026_TOPICS[level])) {
    RETAINED_LOCAL_ASSOCIATIONS.push({
      subjectId: 'classical-studies',
      level,
      year: 2026,
      sitting: 'main',
      n,
      topicIds: classicalTopicIds(level, slugs),
      reason: 'Official 2026 SEC question published after the captured reference topic pages; retained from direct paper inspection.',
    });
  }
}

const politicsTopicsByCanonicalNode = new Map<string, string[]>();
for (const topic of POLITICS_AND_SOCIETY_TAXONOMY.topics.filter(topic =>
  !topic.id.endsWith('-data-based-questions'))) {
  for (const curriculumNodeId of topic.curriculumNodeIds) {
    const scopedKey = `${topic.level}|${curriculumNodeId}`;
    const ids = politicsTopicsByCanonicalNode.get(scopedKey) ?? [];
    if (!ids.includes(topic.id)) ids.push(topic.id);
    politicsTopicsByCanonicalNode.set(scopedKey, ids);
  }
}

// The reference menu omits Higher 2018 Q4. Retain it from the existing
// hand-verified canonical tag instead of sacrificing a valid SEC card for
// headline parity.
for (const paper of PAPER_TOPIC_TAGS) {
  if (paper.subjectId !== 'politics-and-society') continue;
  for (const question of paper.q) {
    const key = questionKey(paper.subjectId, paper.level, paper.year, 'main', question.n);
    if (QUESTION_TOPICS.has(key)) continue;
    const topicIds = [...new Set(
      [question.primary, question.secondary]
        .filter((id): id is string => Boolean(id))
        .flatMap(id => politicsTopicsByCanonicalNode.get(`${paper.level}|${id}`) ?? []),
    )];
    if (!topicIds.length) continue;
    RETAINED_LOCAL_ASSOCIATIONS.push({
      subjectId: paper.subjectId,
      level: paper.level,
      year: paper.year,
      sitting: 'main',
      n: question.n,
      topicIds,
      reason: 'Valid local question omitted from the reference topic pages; retained via its verified canonical tag.',
    });
  }
}

// The reference has no 2024 Higher data-based heading even though the SEC
// paper and our verified answer map both contain Q2. The documents concern
// women in Irish political representation and gender quotas, so preserve the
// assessment-format bucket plus the two directly relevant content themes.
if (!QUESTION_TOPICS.has(questionKey('politics-and-society', 'higher', 2024, 'main', '2'))) {
  RETAINED_LOCAL_ASSOCIATIONS.push({
    subjectId: 'politics-and-society',
    level: 'higher',
    year: 2024,
    sitting: 'main',
    n: '2',
    topicIds: [
      'politics-and-society-higher-data-based-questions',
      'politics-and-society-higher-1-power-and-decision-making-at-national-and-european-level',
      'politics-and-society-higher-3-human-rights-and-responsibilities-in-ireland',
    ],
    reason: 'Valid local data-based question omitted from the reference topic pages; retained from direct inspection of the official SEC paper.',
  });
}

for (const association of RETAINED_LOCAL_ASSOCIATIONS) {
  QUESTION_TOPICS.set(
    questionKey(
      association.subjectId,
      association.level,
      association.year,
      association.sitting,
      association.n,
      association.paperKey,
      association.lang,
    ),
    association.topicIds,
  );
}

export function examTopicTaxonomyFor(subjectId: string): ExamTopicTaxonomy | null {
  return TAXONOMIES.get(subjectId) ?? null;
}

export function examTopicDefinition(topicId: string): ExamTopicDefinition | null {
  return TOPICS_BY_ID.get(topicId) ?? null;
}

export function examTopicLabel(topicId: string): string | null {
  return TOPICS_BY_ID.get(topicId)?.label ?? null;
}

export function examTopicIdsForQuestion(
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  n: string,
  paperKey = 'single',
  lang?: PaperLang,
): string[] {
  const shared = QUESTION_TOPICS.get(questionKey(subjectId, level, year, sitting, n, paperKey)) ?? [];
  const localised = lang
    ? QUESTION_TOPICS.get(questionKey(subjectId, level, year, sitting, n, paperKey, lang)) ?? []
    : [];
  return [...new Set([...shared, ...localised])];
}

export function curriculumNodeIdsForExamTopic(topicId: string): string[] {
  return [...(TOPICS_BY_ID.get(topicId)?.curriculumNodeIds ?? [])];
}

/** Part-aware factual references retained for card-level Mark Bank mapping. */
export function examQuestionPartReferencesForSubject(subjectId: string): ExamQuestionPartReference[] {
  return [
    ...appliedMathematicsPartReferences,
    ...agriculturalSciencePartReferences,
    ...classicalStudiesPartReferences,
    ...linkModulesPartReferences,
    ...politicsAndSocietyPartReferences,
  ]
    .filter(reference => reference.subjectId === subjectId)
    .map(reference => ({ ...reference }));
}

export interface ExamQuestionTopicMapping {
  subjectId: string;
  level: PaperLevel;
  year: number;
  sitting: ExamSitting;
  paperKey: string;
  lang: PaperLang | 'any';
  n: string;
  topicIds: string[];
}

/** All audited question associations for a subject, newest first. */
export function examQuestionTopicMappingsForSubject(subjectId: string): ExamQuestionTopicMapping[] {
  const prefix = `${subjectId}|`;
  const mappings: ExamQuestionTopicMapping[] = [];
  for (const [key, topicIds] of QUESTION_TOPICS) {
    if (!key.startsWith(prefix)) continue;
    const [, level, year, sitting, paperKey, lang, n] = key.split('|');
    mappings.push({
      subjectId,
      level: level as PaperLevel,
      year: Number(year),
      sitting: sitting as ExamSitting,
      paperKey,
      lang: lang as PaperLang | 'any',
      n,
      topicIds: [...topicIds],
    });
  }
  return mappings.sort((a, b) =>
    b.year - a.year || a.level.localeCompare(b.level) || Number(a.n) - Number(b.n));
}

/** Canonical syllabus nodes touched by an audited exam question. */
export function curriculumNodeIdsForExamQuestion(
  subjectId: string,
  level: PaperLevel,
  year: number,
  sitting: ExamSitting,
  n: string,
  paperKey = 'single',
  lang?: PaperLang,
): string[] {
  const ids = examTopicIdsForQuestion(subjectId, level, year, sitting, n, paperKey, lang)
    .flatMap(topicId => curriculumNodeIdsForExamTopic(topicId));
  return [...new Set(ids)];
}

export const retainedLocalExamTopicAssociations = RETAINED_LOCAL_ASSOCIATIONS;
