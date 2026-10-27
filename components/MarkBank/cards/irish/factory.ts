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
import { irishAnswersFor } from './answers';
import { irishTariffsFor } from './tariffs';

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
  conceptId: string;
  paperFileid: string;
  schemePage: number;
  taskRequirements: string[];
  criteria: IrishCriterion[];
  markingGuideNote: string;
  sourceMaterial?: CardSourceMaterial;
  audioMaterial?: CardAudioMaterial;
}

const DATA = authored.cards as AuthoredIrishCard[];

/** Listening and reading cards carry the scheme's exact answers; cut them
 *  into rows where the parts add up to the criterion (cards/irish/answers.ts). */
const EXACT_ANSWER_CARD = /Cluastuiscint|Léamhthuiscint/;

/** Literature cards price what the student must do rather than list answers;
 *  their Eolas tariff is cut into rows by cards/irish/tariffs.ts, as is the last
 *  reading question's composite tariff when the answer cutter cannot read it. */
const LITERATURE_CARD = /Prose|Poetry|Literature/;
const COMPOSITE_READING = /Léamhthuiscint .* Ceist 6/;
const PRICED = /\d+\s*m?h?arc\b/;

const allocationFor = (card: AuthoredIrishCard, criterion: AuthoredIrishCard['criteria'][number]) => {
  const source = { id: card.id, totalMarks: criterion.maxMarks, questionRef: card.questionRef, questionText: card.questionText, guidance: criterion.guidance };
  if (criterion.guidanceKind === 'exact' && EXACT_ANSWER_CARD.test(card.questionRef)) {
    return irishAnswersFor(source) ?? (COMPOSITE_READING.test(card.questionRef) ? irishTariffsFor(source) : undefined);
  }
  if (criterion.guidanceKind === 'indicative' && LITERATURE_CARD.test(card.questionRef) && criterion.guidance.some(line => PRICED.test(line))) {
    return irishTariffsFor(source);
  }
  return undefined;
};

const cloneCriteria = (card: AuthoredIrishCard): IrishCriterion[] =>
  card.criteria.map(criterion => {
    const allocation = allocationFor(card, criterion);
    return {
      ...criterion,
      permittedMarks: [...criterion.permittedMarks],
      guidance: [...criterion.guidance],
      ...(allocation ? { allocation } : {}),
    };
  });

const makeCard = (card: AuthoredIrishCard): SecRubricCard => ({
  id: card.id,
  subjectId: 'irish',
  level: card.level,
  topicId: card.topicId,
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
    `marking scheme ${card.year}, p.${card.schemePage} — © State Examinations Commission.`,
  specVersion: 'irish:outgoing',
  qa: {
    gates: [
      'verbatim-paper-prompt',
      'irish-published-rubric',
      'required-source-complete',
      'paper-census',
    ],
    humanReviewedBy: 'corpus-verified',
    humanReviewedAt: '2026-08-30',
  },
  rubric: {
    system: 'irish',
    taskRequirements: [...card.taskRequirements],
    criteria: cloneCriteria(card),
    markingGuideNote: card.markingGuideNote,
  },
});

export const generatedCardsForLevel = (level: IrishLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const IRISH_AUTHORED_CARD_COUNT = DATA.length;
