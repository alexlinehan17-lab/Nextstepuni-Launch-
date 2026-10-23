/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Art cards use the SEC's own Art assessment grammar. The outgoing 2021–2022
 * papers allocate a 50-mark response across named components. Visual Studies
 * Section A places each compulsory part in a low/moderate/high descriptor band;
 * Sections B and C use four published criteria totalling 50. None is PCLM and
 * none is converted into a fabricated model-answer checklist.
 *
 * Every card shows only the scheme's printed wording under the SEC's name:
 * the 2023+ descriptor bullets, criterion labels and marking notes come from
 * authored.descriptors, and the 2021-2022 component rows, marks and notes
 * from each card's criteria, all lifted page by page by
 * scripts/markbank/authoring/art_printed.py and art_cards.py. There is no
 * written fallback: a card without its printed descriptors fails to build.
 * Our own guidance is kept apart as practice notes on every card.
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
  rowMarks?: number[];
  rowNotes?: string[];
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

interface PrintedLongCriterion {
  id: string;
  label: string;
  maxMarks: number;
  page: number;
  lead: string;
  bands: Record<ArtBand['level'], { marks: number[]; guidance: string[] }>;
}

/** One audited year and level's descriptors and notes, as the scheme prints them. */
interface PrintedScheme {
  short: { page: number; lead: string; bands: Record<ArtBand['level'], string[]> };
  long: PrintedLongCriterion[];
  notes: Record<Exclude<AssessmentKind, 'legacy-components'>, { page: number; text: string[] }>;
}

const DATA = authored.cards as AuthoredArtCard[];
const PRINTED = authored.descriptors as Record<string, PrintedScheme>;
const AUDITED_YEARS = new Set<number>(authored.auditedYears);

/** The printed descriptors a 2023+ card shows; legacy cards have none. */
const printedFor = (card: AuthoredArtCard): PrintedScheme | undefined => {
  if (card.assessment === 'legacy-components') return undefined;
  const printed = AUDITED_YEARS.has(card.year) ? PRINTED[`${card.year}-${card.level}`] : undefined;
  if (!printed) throw new Error(`${card.id}: no printed descriptors lifted for ${card.year} ${card.level}`);
  return printed;
};

const bandsFrom = (
  criterion: AuthoredCriterion, printed: PrintedScheme | undefined,
): ArtBand[] | undefined => {
  if (!criterion.bandMarks) return undefined;
  return (['low', 'moderate', 'high'] as const).map(level => ({
    level,
    marks: criterion.bandMarks![level],
    lead: printed!.short.lead,
    guidance: [...printed!.short.bands[level]],
  }));
};

const authoredCriteria = (card: AuthoredArtCard): ArtCriterion[] => {
  if (!card.criteria) throw new Error(`${card.id}: missing Art scheme criteria`);
  const printed = printedFor(card);
  return card.criteria.map(criterion => ({
    id: criterion.id,
    label: criterion.label,
    maxMarks: criterion.maxMarks,
    permittedMarks: criterion.permittedMarks,
    guidance: criterion.guidance,
    ...(criterion.rowMarks ? { rowMarks: [...criterion.rowMarks] } : {}),
    ...(criterion.rowNotes ? { rowNotes: [...criterion.rowNotes] } : {}),
    bands: bandsFrom(criterion, printed),
  }));
};

/** The four Section B/C criteria exactly as an audited scheme prints them. */
const printedLongCriteria = (printed: PrintedScheme): ArtCriterion[] =>
  printed.long.map(criterion => ({
    id: criterion.id,
    label: criterion.label,
    maxMarks: criterion.maxMarks,
    permittedMarks: range(0, criterion.maxMarks),
    guidance: [],
    bands: (['low', 'moderate', 'high'] as const).map(level => ({
      level,
      marks: [...criterion.bands[level].marks],
      lead: criterion.lead,
      guidance: [...criterion.bands[level].guidance],
    })),
  }));

const range = (from: number, to: number) =>
  Array.from({ length: to - from + 1 }, (_, index) => from + index);

const criteriaFor = (card: AuthoredArtCard): ArtCriterion[] =>
  card.assessment === 'current-long-descriptors'
    ? printedLongCriteria(printedFor(card)!)
    : authoredCriteria(card);

/** NextStepUni's own guidance for using the card; never shown as the SEC's. */
const practiceNotes = (assessment: AssessmentKind): string[] => {
  const scoring = 'Score each independently awarded component once. Descriptor guidance is evidence for a band, never a model-answer checklist.';
  if (assessment === 'legacy-components') {
    return [
      'The SEC allocates the marks for this printed task across these named components. Judge each component against what the task asks; the scheme does not publish low/moderate/high bands for these papers.',
      'Score each independently awarded component once.',
    ];
  }
  if (assessment === 'current-short-descriptors') {
    return [
      'Judge this published part on its own. First identify the low, moderate or high descriptor that best fits, then select a mark inside that band.',
      scoring,
    ];
  }
  return [
    'Judge the complete response once against each of the four published descriptors.',
    scoring,
  ];
};

/** The scheme's own note on applying the descriptors; empty until audited. */
const schemeNote = (card: AuthoredArtCard): string => {
  const printed = printedFor(card);
  if (!printed || card.assessment === 'legacy-components') return '';
  return printed.notes[card.assessment].text.join(' ');
};

const contiguous = (pages: number[]) => pages.every((page, index) => index === 0 || page === pages[index - 1] + 1);

const schemeCitation = (card: AuthoredArtCard) => {
  const pages = !Array.isArray(card.schemePage)
    ? `p.${card.schemePage}`
    : contiguous(card.schemePage)
      ? `pp.${card.schemePage[0]}–${card.schemePage.at(-1)}`
      : `pp.${card.schemePage.join(', ')}`;
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
    gates: [
      'verbatim-paper-prompt', 'art-scheme-grammar', 'official-illustration', 'paper-census',
      ...(AUDITED_YEARS.has(card.year) ? ['sec-printed-wording'] : []),
    ],
    humanReviewedBy: 'corpus-verified',
    humanReviewedAt: '2026-08-30',
  },
  rubric: {
    system: 'art',
    taskRequirements: card.taskRequirements,
    criteria: criteriaFor(card),
    markingGuideNote: schemeNote(card),
    practiceNotes: practiceNotes(card.assessment),
  },
});

export const generatedCardsForLevel = (level: ArtLevel): SecRubricCard[] =>
  DATA.filter(card => card.level === level).map(makeCard);

export const ART_AUTHORED_CARD_COUNT = DATA.length;
