/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * English cards use one shared implementation of the SEC's PCLM grammar.  The
 * generated manifest contains only paper-specific facts: exact prompt, source
 * pages, topic, marks and scheme citation.  It deliberately contains no model
 * answers and no binary marking rows.
 */

import type {
  CardSourceMaterial,
  PclmAssessment,
  PclmCriterion,
  PclmGradeBand,
  SecRubricCard,
} from '../../../../types/markBank';
import authored from './authored.json';

type EnglishLevel = 'higher' | 'ordinary';

interface AuthoredEnglishCard {
  id: string;
  year: number;
  level: EnglishLevel;
  paper: 1 | 2;
  section: string;
  questionRef: string;
  questionText: string;
  totalMarks: number;
  printedParts: string[];
  schemePage: number;
  topicId: string;
  conceptId: string;
  taskRequirements: string[];
  stem?: string;
  sourceMaterial?: CardSourceMaterial;
}

const DATA = authored.cards as AuthoredEnglishCard[];

const range = (from: number, to: number) =>
  from > to ? [] : Array.from({ length: to - from + 1 }, (_, index) => from + index);

const grade = (level: EnglishLevel, number: number): PclmGradeBand['grade'] =>
  `${level === 'higher' ? 'H' : 'O'}${number}` as PclmGradeBand['grade'];

/** The anchor-style grid printed for a single combined-criteria response. */
const combinedBands = (total: number, level: EnglishLevel): PclmGradeBand[] => {
  const anchors = [.9, .8, .7, .6, .5, .4, .3].map(value => Math.ceil(total * value));
  return [
    { grade: grade(level, 1), marks: range(anchors[0], total) },
    ...anchors.slice(1).map((mark, index) => ({
      grade: grade(level, index + 2), marks: [mark],
    })),
    { grade: grade(level, 8), marks: range(0, anchors[6] - 1) },
  ];
};

/** The continuous total-mark bands printed beside a discrete PCLM grid. */
const discreteBands = (total: number, level: EnglishLevel): PclmGradeBand[] => {
  const floors = [.9, .8, .7, .6, .5, .4, .3].map(value => Math.ceil(total * value));
  return floors.map((floor, index) => ({
    grade: grade(level, index + 1),
    marks: range(floor, (index === 0 ? total + 1 : floors[index - 1]) - 1),
  })).concat({ grade: grade(level, 8), marks: range(0, floors[6] - 1) });
};

/** Marks the SEC permits on one P, C, L or M row of the grade grid. */
const criterionMarks = (maximum: number): number[] => {
  const anchors = [.9, .8, .7, .6, .5, .4, .3].map(value => Math.ceil(maximum * value));
  return [...new Set([
    ...range(0, anchors[6] - 1),
    ...anchors.slice(1).reverse(),
    ...range(anchors[0], maximum),
  ])].sort((a, b) => a - b);
};

const COMBINED_CRITERIA = [
  'Clear, purposeful engagement with the exact task',
  'A sustained and coherently developed response',
  'Language managed and controlled for the task',
  'Spelling and grammar appropriate to the register',
];

const discreteCriteria = (total: number, requirements: string[]): PclmCriterion[] => {
  const main = total * .3;
  const mechanics = total * .1;
  if (!Number.isInteger(main) || !Number.isInteger(mechanics)) {
    throw new Error(`English discrete PCLM total ${total} cannot be divided 30/30/30/10`);
  }
  return [
    {
      id: 'purpose', label: 'Clarity of Purpose', maxMarks: main,
      guidance: requirements,
      permittedMarks: criterionMarks(main),
    },
    {
      id: 'coherence', label: 'Coherence of Delivery', maxMarks: main,
      guidance: ['Sustain focus and relevance throughout', 'Shape, sequence and manage ideas effectively'],
      permittedMarks: criterionMarks(main),
    },
    {
      id: 'language', label: 'Efficiency of Language Use', maxMarks: main,
      guidance: ['Manage language to communicate clearly', 'Control expression, vocabulary, style and fluency'],
      permittedMarks: criterionMarks(main),
    },
    {
      id: 'mechanics', label: 'Accuracy of Mechanics', maxMarks: mechanics,
      guidance: ['Use spelling and grammar accurately for the chosen register'],
      permittedMarks: criterionMarks(mechanics),
    },
  ];
};

const part = (printed: string) => {
  const match = printed.match(/^(.*?)\s+(\d+)\s+marks?$/i);
  if (!match) throw new Error(`Invalid English printed part: ${printed}`);
  const label = match[1].trim();
  return {
    id: label.replace(/[()]/g, '-').replace(/^-|-$/g, '').replace(/--+/g, '-'),
    label: `Part ${label}`,
    totalMarks: Number(match[2]),
  };
};

const assessmentFor = (card: AuthoredEnglishCard): PclmAssessment => {
  if (card.printedParts.length) {
    return {
      mode: 'composite',
      components: card.printedParts.map(print => {
        const component = part(print);
        // Across the complete 2021–2025 corpus, the schemes put linked parts
        // worth 20 marks or fewer on a combined grid.  The 30/40-mark linked
        // Comparative parts receive their own discrete P, C, L and M grids.
        // Keeping the distinction at component level is essential: an OL
        // Comparative card is deliberately mixed (15 combined + 15 combined
        // + 40 discrete), while the question remains one selectable response.
        return component.totalMarks <= 20
          ? {
              ...component,
              mode: 'combined' as const,
              bands: combinedBands(component.totalMarks, card.level),
              criteria: COMBINED_CRITERIA,
            }
          : {
              ...component,
              mode: 'discrete' as const,
              bands: discreteBands(component.totalMarks, card.level),
              criteria: discreteCriteria(component.totalMarks, card.taskRequirements),
              primacyOfPurpose: true as const,
            };
      }),
    };
  }
  if (card.totalMarks <= 20) {
    return {
      mode: 'combined',
      bands: combinedBands(card.totalMarks, card.level),
      criteria: COMBINED_CRITERIA,
    };
  }
  return {
    mode: 'discrete',
    bands: discreteBands(card.totalMarks, card.level),
    criteria: discreteCriteria(card.totalMarks, card.taskRequirements),
    primacyOfPurpose: true,
  };
};

const INDICATIVE_NOTE =
  'SEC examples are broad, non-exhaustive directions for examiners. Valid alternatives must be judged on their merits; none is a required answer.';

const paperFileid = (card: AuthoredEnglishCard) =>
  `LC002${card.level === 'higher' ? 'A' : 'G'}LP${card.paper === 1 ? '100' : '200'}EV`;

const makeCard = (card: AuthoredEnglishCard): SecRubricCard => ({
  id: card.id,
  subjectId: 'english',
  level: card.level,
  topicId: card.topicId,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: paperFileid(card),
  section: card.paper === 1 ? '1' : '2',
  questionRef: card.questionRef,
  stem: card.stem,
  sourceMaterial: card.sourceMaterial,
  questionText: card.questionText,
  totalMarks: card.totalMarks,
  schemeCitation:
    `SEC English ${card.level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme ` +
    `${card.year}, p.${card.schemePage} — © State Examinations Commission.`,
  specVersion: 'english:outgoing',
  qa: {
    gates: ['verbatim-paper-prompt', 'pclm-grid', 'indicative-not-checklist', 'paper-census'],
    humanReviewedBy: 'corpus-verified',
    humanReviewedAt: '2026-08-30',
  },
  rubric: {
    system: 'pclm',
    taskRequirements: card.taskRequirements,
    assessment: assessmentFor(card),
    indicativeMaterialNote: INDICATIVE_NOTE,
  },
});

export const generatedCardsForLevel = (level: EnglishLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const ENGLISH_AUTHORED_CARD_COUNT = DATA.length;
