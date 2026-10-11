/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Irish cards retain the marking grammar printed by the SEC.  Exact listening
 * and reading answers, indicative literature material, composition quality
 * criteria and Ordinary-Level language deductions are deliberately distinct.
 */

import type {
  CardAudioMaterial,
  CardSourceMaterial,
  IrishCriterion,
  SecRubricCard,
} from '../../../../types/markBank';
import authored from './authored.json';
import higher2026P1 from './higher-2026-p1-authored.json';
import higher2026P2 from './higher-2026-p2-authored.json';
import { resolveCurriculumSpecification } from '../../../../curriculumRegistry';

type IrishLevel = 'higher' | 'ordinary';

interface AuthoredIrishCard {
  id: string;
  year: number;
  level: IrishLevel;
  paper: 1 | 2;
  section: '1' | '2';
  questionRef: string;
  questionText: string;
  totalMarks: number;
  topicId: string;
  additionalTopicIds?: string[];
  conceptId: string;
  paperFileid: string;
  schemePage: number;
  schemePages?: number[];
  reviewedAt?: string;
  taskRequirements: string[];
  criteria: IrishCriterion[];
  markingGuideNote: string;
  sourceMaterial?: CardSourceMaterial;
  audioMaterial?: CardAudioMaterial;
}

// Paper-reviewed components ship as their own files beside the legacy census output.
const DATA = [...authored.cards, ...higher2026P1.cards, ...higher2026P2.cards] as AuthoredIrishCard[];

const cloneCriteria = (criteria: IrishCriterion[]): IrishCriterion[] =>
  criteria.map(criterion => ({
    ...criterion,
    permittedMarks: [...criterion.permittedMarks],
    guidance: [...criterion.guidance],
  }));

const makeCard = (card: AuthoredIrishCard): SecRubricCard => ({
  id: card.id,
  subjectId: 'irish',
  level: card.level,
  topicId: card.topicId,
  additionalTopicIds: card.additionalTopicIds ? [...card.additionalTopicIds] : undefined,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: card.paperFileid,
  section: card.section,
  questionRef: card.questionRef,
  questionText: card.questionText,
  sourceMaterial: card.sourceMaterial,
  audioMaterial: card.audioMaterial,
  totalMarks: card.totalMarks,
  schemeCitation:
    `SEC Gaeilge ${card.level === 'higher' ? 'Ardleibhéal' : 'Gnáthleibhéal'} ` +
    `marking scheme ${card.year}, p.${card.schemePage}` +
    (card.schemePages && card.schemePages.length > 1 ? `–${card.schemePages.at(-1)}` : '') +
    ' — © State Examinations Commission.',
  specVersion: resolveCurriculumSpecification('irish', card.year)!.id,
  qa: {
    gates: [
      'verbatim-paper-prompt',
      'irish-published-rubric',
      'required-source-complete',
      'paper-census',
    ],
    humanReviewedBy: 'corpus-verified',
    humanReviewedAt: card.reviewedAt ?? '2026-08-30',
  },
  rubric: {
    system: 'irish',
    taskRequirements: [...card.taskRequirements],
    criteria: cloneCriteria(card.criteria),
    markingGuideNote: card.markingGuideNote,
  },
});

export const generatedCardsForLevel = (level: IrishLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const IRISH_AUTHORED_CARD_COUNT = DATA.length;
