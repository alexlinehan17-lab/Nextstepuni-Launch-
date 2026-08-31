/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Art cards use the SEC's own Art assessment grammar. The outgoing 2021–2022
 * papers allocate a 50-mark response across named components. Visual Studies
 * Section A places each compulsory part in a low/moderate/high descriptor band;
 * Sections B and C use four published criteria totalling 50. None is PCLM and
 * none is converted into a fabricated model-answer checklist.
 */

import type {
  ArtBand,
  ArtCriterion,
  CardSourceMaterial,
  SecRubricCard,
} from '../../../../types/markBank';
import authored from './authored.json';

type ArtLevel = 'higher' | 'ordinary';
type AssessmentKind =
  | 'legacy-components'
  | 'current-short-descriptors'
  | 'current-long-descriptors';

interface AuthoredCriterion {
  id: string;
  label: string;
  maxMarks: number;
  permittedMarks: number[];
  guidance: string[];
  bandMarks?: Record<'low' | 'moderate' | 'high', number[]>;
}

interface AuthoredArtCard {
  id: string;
  year: number;
  level: ArtLevel;
  section: 'A' | 'B' | 'C' | '1' | '2' | '3';
  questionRef: string;
  stem?: string;
  questionText: string;
  paperPage: number;
  paperFileid: string;
  totalMarks: number;
  schemePage: number | number[];
  topicId: string;
  conceptId: string;
  taskRequirements: string[];
  assessment: AssessmentKind;
  criteria?: AuthoredCriterion[];
  sourceMaterial?: CardSourceMaterial;
}

const DATA = authored.cards as AuthoredArtCard[];

const SHORT_BAND_GUIDANCE: Record<ArtBand['level'], string[]> = {
  low: [
    'Limited understanding of the task and limited application of relevant knowledge.',
    'Limited analysis or interpretation of stimulus material and little supporting evidence.',
    'Limited coherence, focus, visual-art terminology and/or relevant sketches.',
  ],
  moderate: [
    'Good understanding of the task and good application of relevant knowledge.',
    'Good analysis or interpretation of stimulus material with evidence-based ideas.',
    'A coherent, focused answer using accurate visual-art terminology and/or relevant sketches.',
  ],
  high: [
    'Thorough understanding of the task and thorough application of well-informed knowledge.',
    'Consistent analysis or interpretation of stimulus material with well-supported ideas.',
    'A thoroughly coherent answer using accurate visual-art terminology and/or relevant sketches.',
  ],
};

const bandsFrom = (criterion: AuthoredCriterion): ArtBand[] | undefined => {
  if (!criterion.bandMarks) return undefined;
  return (['low', 'moderate', 'high'] as const).map(level => ({
    level,
    marks: criterion.bandMarks![level],
    guidance: SHORT_BAND_GUIDANCE[level],
  }));
};

const authoredCriteria = (card: AuthoredArtCard): ArtCriterion[] => {
  if (!card.criteria) throw new Error(`${card.id}: missing Art scheme criteria`);
  return card.criteria.map(criterion => ({
    id: criterion.id,
    label: criterion.label,
    maxMarks: criterion.maxMarks,
    permittedMarks: criterion.permittedMarks,
    guidance: criterion.guidance,
    bands: bandsFrom(criterion),
  }));
};

const range = (from: number, to: number) =>
  Array.from({ length: to - from + 1 }, (_, index) => from + index);

const band = (
  level: ArtBand['level'], from: number, to: number, guidance: string[],
): ArtBand => ({ level, marks: range(from, to), guidance });

/** The four descriptor tables printed for every current Section B/C answer. */
const LONG_CRITERIA: ArtCriterion[] = [
  {
    id: 'coherence-focus',
    label: 'Coherence and Focus',
    maxMarks: 10,
    permittedMarks: range(0, 10),
    guidance: ['Understand the demands of the chosen question and build the response around it.'],
    bands: [
      band('low', 0, 3, [
        'Limited understanding of the question and limited ability to create an answer from it.',
        'Arguments or ideas have limited sequence, logic or evidence; personal understanding is limited.',
      ]),
      band('moderate', 4, 6, [
        'Good understanding of the question and an appropriate answer based on it.',
        'Mostly evidenced, reasonable and sequential ideas with a good personal understanding.',
      ]),
      band('high', 7, 10, [
        'Thorough understanding of the question and a high-level answer based on it.',
        'Clearly evidenced, logical ideas with a thorough personal understanding.',
      ]),
    ],
  },
  {
    id: 'subject-knowledge',
    label: 'Subject Knowledge',
    maxMarks: 20,
    permittedMarks: range(0, 20),
    guidance: ['Recall, analyse and apply knowledge of the content area to the chosen question.'],
    bands: [
      band('low', 0, 7, [
        'Limited recall, knowledge and understanding of the area of focus.',
        'Limited analysis, evaluation and use of knowledge to support the response.',
      ]),
      band('moderate', 8, 13, [
        'Good recall, knowledge and understanding of the area of focus.',
        'Good analysis, evaluation and perceptive use of knowledge to support the response.',
      ]),
      band('high', 14, 20, [
        'Thorough recall, knowledge and understanding of the area of focus.',
        'Thorough analysis, evaluation and perceptive use of knowledge to support the response.',
      ]),
    ],
  },
  {
    id: 'relevant-examples',
    label: 'Relevant Examples',
    maxMarks: 10,
    permittedMarks: range(0, 10),
    guidance: ['Choose recognised, relevant artists and artworks or artefacts that support the response.'],
    bands: [
      band('low', 0, 3, [
        'Examples have limited relevance or recognition and support only a limited response.',
        'Limited understanding of the selected artists and examples.',
      ]),
      band('moderate', 4, 6, [
        'Mostly relevant, recognised examples support a mostly accurate response.',
        'Good understanding of the selected artists and examples.',
      ]),
      band('high', 7, 10, [
        'Highly relevant, recognised examples support a highly accurate response.',
        'Thorough understanding of the selected artists and examples.',
      ]),
    ],
  },
  {
    id: 'visual-language',
    label: 'Visual Language',
    maxMarks: 10,
    permittedMarks: range(0, 10),
    guidance: ['Use visual-art terminology and, where used, sketches to communicate and support ideas.'],
    bands: [
      band('low', 0, 3, [
        'Limited use and understanding of terminology.',
        'Any sketches show limited ability to support or communicate ideas.',
      ]),
      band('moderate', 4, 6, [
        'Good, accurate and relevant terminology adds to the communication of ideas.',
        'Any sketches are mostly accurate, relevant and supportive.',
      ]),
      band('high', 7, 10, [
        'Thorough, accurate and relevant terminology supports the communication of ideas.',
        'Any sketches are thorough, accurate, relevant and strongly supportive.',
      ]),
    ],
  },
];

const criteriaFor = (card: AuthoredArtCard): ArtCriterion[] =>
  card.assessment === 'current-long-descriptors'
    ? LONG_CRITERIA.map(criterion => ({
        ...criterion,
        permittedMarks: [...criterion.permittedMarks],
        guidance: [...criterion.guidance],
        bands: criterion.bands?.map(entry => ({
          ...entry, marks: [...entry.marks], guidance: [...entry.guidance],
        })),
      }))
    : authoredCriteria(card);

const guideNote = (assessment: AssessmentKind) => {
  if (assessment === 'legacy-components') {
    return 'The SEC allocates the marks for this printed task across these named components. Judge each component against what the task asks; the scheme does not publish low/moderate/high bands for these papers.';
  }
  if (assessment === 'current-short-descriptors') {
    return 'Judge this published part on its own. First identify the low, moderate or high descriptor that best fits, then select a mark inside that band.';
  }
  return 'Judge the complete response once against each of the four published descriptors. Relevant content outside any examples you revised must still be credited on its merits.';
};

const schemeCitation = (card: AuthoredArtCard) => {
  const pages = Array.isArray(card.schemePage)
    ? `pp.${card.schemePage[0]}–${card.schemePage.at(-1)}`
    : `p.${card.schemePage}`;
  return `SEC Art ${card.level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme ${card.year}, ${pages} — © State Examinations Commission.`;
};

const makeCard = (card: AuthoredArtCard): SecRubricCard => ({
  id: card.id,
  subjectId: 'art',
  level: card.level,
  topicId: card.topicId,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: card.paperFileid,
  section: card.section,
  questionRef: card.questionRef,
  sourceMaterial: card.sourceMaterial,
  stem: card.stem,
  questionText: card.questionText,
  totalMarks: card.totalMarks,
  schemeCitation: schemeCitation(card),
  specVersion: card.year <= 2022 ? 'art:history-and-appreciation' : 'art:current',
  qa: {
    gates: ['verbatim-paper-prompt', 'art-scheme-grammar', 'official-illustration', 'paper-census'],
    humanReviewedBy: 'corpus-verified',
    humanReviewedAt: '2026-08-30',
  },
  rubric: {
    system: 'art',
    taskRequirements: card.taskRequirements,
    criteria: criteriaFor(card),
    markingGuideNote: guideNote(card.assessment),
  },
});

export const generatedCardsForLevel = (level: ArtLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const ART_AUTHORED_CARD_COUNT = DATA.length;
