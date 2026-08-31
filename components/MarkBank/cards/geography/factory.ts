/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Geography cards retain the SEC's Significant Relevant Point grammar. Exact
 * short answers and source questions carry their published allocation; longer
 * responses are placed against the full tariff with the scheme's SRP caps and
 * diagram/example directions visible. Indicative examples never become ticks.
 */

import type {
  CardSourceMaterial,
  GeographyCriterion,
  GeographyGuidanceKind,
  SecRubricCard,
} from '../../../../types/markBank';
import authored from './authored.json';

type GeographyLevel = 'higher' | 'ordinary';

interface AuthoredGeographyCard {
  id: string;
  year: number;
  level: GeographyLevel;
  part: 1 | 2;
  questionRef: string;
  stem: string;
  questionText: string;
  paperPage: number;
  paperFileid: string;
  totalMarks: number;
  schemePage: number;
  topicId: string;
  conceptId: string;
  taskRequirements: string[];
  guidanceKind: GeographyGuidanceKind;
  schemeGuidance: string[];
  sourceMaterial?: CardSourceMaterial;
  additionalSourceMaterials?: CardSourceMaterial[];
}

const DATA = authored.cards as AuthoredGeographyCard[];

const range = (from: number, to: number) =>
  Array.from({ length: to - from + 1 }, (_, index) => from + index);

const criterionFor = (card: AuthoredGeographyCard): GeographyCriterion => ({
  id: 'published-allocation',
  label: card.guidanceKind === 'exact'
    ? 'Published answers and allocation'
    : 'Complete response',
  maxMarks: card.totalMarks,
  permittedMarks: range(0, card.totalMarks),
  guidanceKind: card.guidanceKind,
  guidance: [...card.schemeGuidance],
});

const markingGuideNote = (card: AuthoredGeographyCard) =>
  card.guidanceKind === 'exact'
    ? 'Compare your response with the published answers and mark allocation. Where the scheme says “valid answer”, other correct responses remain creditable on their merits.'
    : 'The scheme’s suggestions and examples are not exhaustive. Count only valid Significant Relevant Points that emerge from a coherent response, then apply every published cap, named-example rule and diagram condition shown above.';

const makeCard = (card: AuthoredGeographyCard): SecRubricCard => ({
  id: card.id,
  subjectId: 'geography',
  level: card.level,
  topicId: card.topicId,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: card.paperFileid,
  section: String(card.part) as '1' | '2',
  questionRef: card.questionRef,
  stem: card.stem,
  questionText: card.questionText,
  sourceMaterial: card.sourceMaterial,
  additionalSourceMaterials: card.additionalSourceMaterials,
  totalMarks: card.totalMarks,
  schemeCitation:
    `SEC Geography ${card.level === 'higher' ? 'Higher' : 'Ordinary'} Level ` +
    `marking scheme ${card.year}, p.${card.schemePage} — © State Examinations Commission.`,
  specVersion: 'geography:outgoing',
  qa: {
    gates: [
      'verbatim-paper-prompt',
      'geography-srp-grammar',
      'required-source-complete',
      'finite-routes-expanded',
      'paper-census',
    ],
    humanReviewedBy: 'paper-and-scheme-census',
    humanReviewedAt: '2026-08-31',
  },
  rubric: {
    system: 'geography',
    taskRequirements: [...card.taskRequirements],
    criteria: [criterionFor(card)],
    srpMarks: card.guidanceKind === 'srp'
      ? (card.level === 'higher' ? 2 : 3)
      : undefined,
    markingGuideNote: markingGuideNote(card),
  },
});

export const generatedCardsForLevel = (level: GeographyLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const GEOGRAPHY_AUTHORED_CARD_COUNT = DATA.length;
