/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Geography cards retain the SEC's Significant Relevant Point grammar. Exact
 * short answers and source questions carry their published allocation; longer
 * responses are placed against the full tariff with the scheme's SRP caps and
 * diagram/example directions visible. Indicative examples never become ticks.
 *
 * Independently reviewed sittings (scripts/markbank/authored/
 * geography-reviewed-audit.json) carry one criterion per published allocation
 * line — an identification, a named example, an SRP explanation, a sketch
 * feature, an option's aspects and Overall Coherence — each limited to the
 * marks the scheme can award, plus the scheme's examiner directions. Each
 * criterion's lines are also cut into claimable rows (allocation.ts) wherever
 * they reconcile, so the reveal shows answers with their marks, not prose.
 */

import type {
  CardFigure,
  CardSourceMaterial,
  GeographyCriterion,
  GeographyGuidanceKind,
  SecRubricCard,
} from '../../../../types/markBank';
import authored from './authored.json';
import {
  geographyColumnLabels,
  geographyPointRoutes,
  geographyPointsProblem,
  parseGeographyAllocation,
  parseGeographyCriterionAllocation,
} from './allocation';

type GeographyLevel = 'higher' | 'ordinary';

interface AuthoredGeographyCriterion {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  guidanceKind: GeographyGuidanceKind;
  guidance: string[];
}

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
  /** Reviewed sittings only: the scheme's own allocation lines. */
  criteria?: AuthoredGeographyCriterion[];
  directions?: string[];
  atlasTopicIds?: string[];
  reviewed?: boolean;
  /** A crop of an official document (a map crop, or the scheme's labelled
   *  diagram as a solution figure held back until the reveal). */
  figure?: CardFigure;
  /** The paper's own print of the question (a diagram whose blanks are the
   *  ask), shown before the reveal in place of the typeset stem. */
  questionFigure?: CardFigure;
  /** A short factual note about the sitting's sources or allocation (no
   *  published legend; a scheme that prices less than the printed total). */
  note?: string;
  /** Printed marks the published scheme allocates to no line (2020 OL 9C:
   *  3 of 30). They stay in `totalMarks` and are never derived into a
   *  criterion; the card's `note` says so. */
  unpricedMarks?: number;
}

const DATA = authored.cards as AuthoredGeographyCard[];

const range = (from: number, to: number) =>
  Array.from({ length: to - from + 1 }, (_, index) => from + index);

/**
 * Each reviewed allocation line, and the same lines as claimable rows where
 * they reconcile to the criterion's maximum and its permitted marks
 * (allocation.ts, tryParseGeographyCriterionAllocation). A criterion they do
 * not reconcile for keeps its lines and mark control.
 *
 * Criteria that share printed lines are read together: a points table split
 * over several criteria ("Number of aspects", 2010–2013 Higher options) must
 * add up point by point across them, or none of them is structured; and
 * criteria the review gave identical lines take one addend each of a line
 * that prices them all ("Named · 4m + 3m + 3m").
 */
const reviewedCriteria = (card: AuthoredGeographyCard): GeographyCriterion[] => {
  const criteria = card.criteria ?? [];
  const columnLabels = geographyColumnLabels(criteria);
  const pointRoutes = geographyPointRoutes(criteria);
  const lineKeys = criteria.map(source => JSON.stringify(source.guidance));
  let previousRowText: string | undefined;
  const out = criteria.map((source, index) => {
    const criterion: GeographyCriterion = {
      ...source,
      permittedMarks: [...source.permittedMarks],
      guidance: [...source.guidance],
    };
    const siblings = lineKeys.filter(key => key === lineKeys[index]).length;
    const share = siblings > 1
      ? { index: lineKeys.slice(0, index).filter(key => key === lineKeys[index]).length, count: siblings }
      : undefined;
    const allocation = parseGeographyCriterionAllocation(
      { level: card.level, questionText: card.questionText, columnLabels, previousRowText, pointRoutes, share }, criterion);
    const rows = allocation?.groups.flatMap(group => group.rows) ?? [];
    previousRowText = rows.length ? rows[rows.length - 1].text : undefined;
    if (allocation) criterion.allocation = allocation;
    return criterion;
  });
  // A points table the criteria split between them is one table: they share
  // its pick (`follows`), and they must add up to its heading point by point.
  if (pointRoutes && out.some(criterion => criterion.allocation?.choice?.follows === pointRoutes.owner)
    && geographyPointsProblem(pointRoutes, out)) {
    for (const criterion of out) {
      if (criterion.id === pointRoutes.owner || criterion.allocation?.choice?.follows === pointRoutes.owner) delete criterion.allocation;
    }
  }
  return out;
};

const criterionFor = (card: AuthoredGeographyCard): GeographyCriterion => {
  const criterion: GeographyCriterion = {
    id: 'published-allocation',
    label: card.guidanceKind === 'exact'
      ? 'Published answers and allocation'
      : 'Complete response',
    maxMarks: card.totalMarks,
    permittedMarks: range(0, card.totalMarks),
    guidanceKind: card.guidanceKind,
    guidance: [...card.schemeGuidance],
  };
  // The same lines as claimable rows, where they add up to the printed total.
  const allocation = parseGeographyAllocation(card);
  if (allocation) criterion.allocation = allocation;
  return criterion;
};

const markingGuideNote = (card: AuthoredGeographyCard) =>
  card.guidanceKind === 'exact'
    ? 'Compare your response with the published answers and mark allocation. Where the scheme says “valid answer”, other correct responses remain creditable on their merits.'
    : 'The scheme’s suggestions and examples are not exhaustive. Count only valid Significant Relevant Points that emerge from a coherent response, then apply every published cap, named-example rule and diagram condition shown above.';

const guideNote = (card: AuthoredGeographyCard) =>
  card.note ? `${card.note} ${markingGuideNote(card)}` : markingGuideNote(card);

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
  ...(card.questionFigure
    ? { questionFigure: { ...card.questionFigure, lettersVisible: [...card.questionFigure.lettersVisible] } }
    : {}),
  ...(card.figure
    ? { figure: { ...card.figure, lettersVisible: [...card.figure.lettersVisible] } }
    : {}),
  totalMarks: card.totalMarks,
  schemeCitation:
    `SEC Geography ${card.level === 'higher' ? 'Higher' : 'Ordinary'} Level ` +
    `marking scheme ${card.year}, p.${card.schemePage} — © State Examinations Commission.`,
  specVersion: 'geography:outgoing',
  qa: card.reviewed
    ? {
      gates: [
        'visual-paper-sweep',
        'visual-scheme-allocation',
        'verbatim-paper-prompt',
        'published-mark-boundaries',
        'finite-routes-expanded',
        'required-source-complete',
        'canonical-topic',
      ],
      humanReviewedBy: 'independent-paper-and-scheme-review',
      humanReviewedAt: '2026-10-11',
    }
    : {
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
    criteria: card.criteria ? reviewedCriteria(card) : [criterionFor(card)],
    directions: card.directions?.length ? [...card.directions] : undefined,
    srpMarks: card.guidanceKind === 'srp'
      ? (card.level === 'higher' ? 2 : 3)
      : undefined,
    ...(card.unpricedMarks ? { unpricedMarks: card.unpricedMarks } : {}),
    markingGuideNote: guideNote(card),
  },
});

export const generatedCardsForLevel = (level: GeographyLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const GEOGRAPHY_AUTHORED_CARD_COUNT = DATA.length;
