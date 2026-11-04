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
  PclmCapRule,
  PclmCriterion,
  PclmCriterionId,
  PclmGradeBand,
  PclmGradeLabel,
  PclmPrintedGrid,
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
  additionalSourceMaterials?: CardSourceMaterial[];
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
  // The COVID-adjusted 2021/2022 Ordinary Single Text schemes publish
  // P=11, C=11, L=11, M=2 for a 35-mark response. It is not a 30/30/30/10
  // percentage split; preserve the SEC's actual allocation.
  const main = total === 35 ? 11 : total * .3;
  const mechanics = total === 35 ? 2 : total * .1;
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
  additionalSourceMaterials: card.additionalSourceMaterials,
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

/**
 * Legacy runtime cards bundle separately marked leaf tasks. A reviewed
 * companion reader on one of those leaves (aggregated by english_publish.py)
 * must reach the bundled card, so it is merged here without changing its id.
 *
 * A bridged paper (scripts/markbank/authored/english-legacy-bridge.json) is
 * served by its published reviewed cards instead: each of its legacy ids is
 * either kept by the published card or registered as a progress alias, so the
 * legacy card itself is no longer generated.
 */
export const generatedCardsForLevel = (
  level: EnglishLevel,
  legacyAdditionalSources: Record<string, CardSourceMaterial[]> = {},
  bridgedLegacyIds: readonly string[] = [],
): SecRubricCard[] =>
  DATA.filter(card => card.level === level && !bridgedLegacyIds.includes(card.id)).map(card => {
    const extra = legacyAdditionalSources[card.id] ?? [];
    if (!extra.length) return makeCard(card);
    const own = card.additionalSourceMaterials ?? [];
    const merged = [...own, ...extra.filter(source =>
      !own.some(existing => JSON.stringify(existing) === JSON.stringify(source)))];
    return makeCard({ ...card, additionalSourceMaterials: merged });
  });

/* ------------------------------------------------ reviewed full corpus ---- */

/**
 * Cards from papers whose own independent review gate passed, generated by
 * scripts/markbank/authoring/english_publish.py. Each card is one separately
 * practicable task at its published mark boundary, or one route of a finite
 * printed choice. Its grid and cap rule are the year's own print, transcribed
 * in scripts/markbank/authored/english-marking-grids.json — never the modern
 * grid projected backwards.
 */
interface PrintedGridFamily {
  level: EnglishLevel;
  labels: PclmGradeLabel[];
  combinedLabels: PclmGradeLabel[];
  discrete: Record<string, Record<string, string[]>>;
  combined: Record<string, { total: string[]; split?: string }>;
}

interface PrintedGridSitting {
  family: string;
  gridPages: number[];
  capRule: { kind: 'none' | 'purpose-primacy' | 'language-at-d-band' };
  capRulePage: number;
}

interface PublishedEnglishCard {
  id: string;
  year: number;
  level: EnglishLevel;
  paper: 1 | 2;
  questionRef: string;
  questionText: string;
  totalMarks: number;
  topicId: string;
  conceptId: string;
  taskRequirements: string[];
  stem?: string;
  sourceMaterial?: CardSourceMaterial;
  additionalSourceMaterials?: CardSourceMaterial[];
  choiceParentId?: string;
  choiceLabel?: string;
  schemePages: number[];
  assessment: { mode: 'combined' | 'discrete'; grid: string; allocation?: Record<string, number> };
  paperFileid: string;
  atlas: { fileid: string; n: string };
  /** Indicative bullets lifted verbatim from the card's scheme page (bridge ledger). */
  indicativeMaterial?: string[];
}

export interface PublishedEnglishManifest {
  level: EnglishLevel;
  papers: Array<{ paperId: string; year: number; paper: 1 | 2; tasks: number; cards: number }>;
  grids: { families: Record<string, PrintedGridFamily>; sittings: Record<string, PrintedGridSitting> };
  legacyAdditionalSources: Record<string, CardSourceMaterial[]>;
  /** Legacy-served papers now published from their review (english-legacy-bridge.json). */
  bridgedPapers: string[];
  /** Every legacy id of those papers: kept by a published card or aliased. */
  bridgedLegacyIds: string[];
  /** Legacy id -> published card, mirrored in cardAliases.ts. */
  bridgeAliases: Record<string, string>;
  cardCount: number;
  cards: PublishedEnglishCard[];
}

/** Marks one printed cell permits: '30-26', '85-100', '7' or the 2026 '2/1'. */
export const printedCellMarks = (cell: string): number[] => {
  if (cell.includes('/')) return [...new Set(cell.split('/').map(Number))].sort((a, b) => a - b);
  if (cell.includes('-')) {
    const [low, high] = cell.split('-').map(Number).sort((a, b) => a - b);
    return range(low, high);
  }
  return [Number(cell)];
};

const unionOf = (cells: string[]) =>
  [...new Set(cells.flatMap(printedCellMarks))].sort((a, b) => a - b);

const pageList = (pages: number[]) => {
  const consecutive = pages.every((page, index) => index === 0 || page === pages[index - 1] + 1);
  if (pages.length === 1) return `p.${pages[0]}`;
  return consecutive ? `pp.${pages[0]}–${pages[pages.length - 1]}` : `pp.${pages.join(', ')}`;
};

const CRITERION_ROWS: Record<PclmCriterionId, [string, string]> = {
  // Higher Level and modern grids print one 30% row for P, C and L; the
  // 2010–2016 Ordinary grid prints each criterion on its own row.
  purpose: ['purpose', 'thirty'],
  coherence: ['coherence', 'thirty'],
  language: ['language', 'thirty'],
  mechanics: ['mechanics', 'ten'],
};

const ALLOCATION_KEY: Record<PclmCriterionId, string> = {
  purpose: 'P', coherence: 'C', language: 'L', mechanics: 'M',
};

const publishedAssessment = (
  card: PublishedEnglishCard,
  grids: PublishedEnglishManifest['grids'],
): PclmAssessment => {
  const sitting = grids.sittings[card.assessment.grid];
  const family = sitting && grids.families[sitting.family];
  if (!sitting || !family || family.level !== card.level) {
    throw new Error(`${card.id}: no printed ${card.level} grid ${card.assessment.grid}`);
  }
  const tariff = String(card.totalMarks);
  if (card.assessment.mode === 'combined') {
    const grid = family.combined[tariff];
    if (!grid) throw new Error(`${card.id}: no printed combined ${tariff}-mark grid`);
    const bands = grid.total.map((cell, index) => ({
      grade: family.combinedLabels[index], marks: printedCellMarks(cell),
    }));
    const marks = bands.flatMap(band => band.marks);
    const printedGrid: PclmPrintedGrid = { sitting: card.assessment.grid, schemePages: sitting.gridPages };
    if (new Set(marks).size !== marks.length) printedGrid.overlapping = true;
    if (Math.min(...marks) > 0) printedGrid.lowestMark = Math.min(...marks);
    const allocation = card.assessment.allocation;
    return {
      mode: 'combined',
      bands,
      criteria: allocation
        ? [...COMBINED_CRITERIA, `Printed split: Purpose and Coherence ${allocation['P+C']} · Language and Mechanics ${allocation['L+M']}`]
        : COMBINED_CRITERIA,
      printedGrid,
    };
  }
  const grid = family.discrete[tariff];
  if (!grid) throw new Error(`${card.id}: no printed discrete ${tariff}-mark grid`);
  const allocation = card.assessment.allocation ?? {};
  const row = (id: PclmCriterionId) => {
    const [named, shared] = CRITERION_ROWS[id];
    const cells = grid[named] ?? grid[shared];
    if (!cells) throw new Error(`${card.id}: printed ${tariff}-mark grid has no ${id} row`);
    return cells;
  };
  const template = discreteCriteria(card.totalMarks, card.taskRequirements);
  const criteria: PclmCriterion[] = template.map(criterion => {
    const permittedMarks = unionOf(row(criterion.id));
    const maxMarks = allocation[ALLOCATION_KEY[criterion.id]];
    if (maxMarks !== Math.max(...permittedMarks)) {
      throw new Error(`${card.id}: printed ${criterion.id} row does not reach the reviewed allocation`);
    }
    return { ...criterion, maxMarks, permittedMarks };
  });
  let capRule: PclmCapRule;
  if (sitting.capRule.kind === 'language-at-d-band') {
    const d = family.labels.indexOf('D');
    if (d < 0) throw new Error(`${card.id}: Language-at-D rule without a printed D band`);
    capRule = {
      kind: 'language-at-d-band',
      purposeBelow: Math.min(...printedCellMarks(row('purpose')[d])),
      coherenceBelow: Math.min(...printedCellMarks(row('coherence')[d])),
      languageMax: Math.max(...printedCellMarks(row('language')[d])),
    };
  } else {
    capRule = { kind: sitting.capRule.kind };
  }
  return {
    mode: 'discrete',
    bands: (grid.total ?? []).map((cell, index) => ({ grade: family.labels[index], marks: printedCellMarks(cell) })),
    criteria,
    ...(capRule.kind === 'purpose-primacy' ? { primacyOfPurpose: true as const } : {}),
    capRule,
    printedGrid: { sitting: card.assessment.grid, schemePages: sitting.gridPages },
  };
};

const makePublishedCard = (
  card: PublishedEnglishCard,
  grids: PublishedEnglishManifest['grids'],
): SecRubricCard => ({
  id: card.id,
  subjectId: 'english',
  level: card.level,
  topicId: card.topicId,
  conceptId: card.conceptId,
  source: 'sec',
  kind: 'rubric',
  year: card.year,
  paperFileid: card.paperFileid,
  section: card.paper === 1 ? '1' : '2',
  questionRef: card.questionRef,
  stem: card.stem,
  sourceMaterial: card.sourceMaterial,
  additionalSourceMaterials: card.additionalSourceMaterials,
  questionText: card.questionText,
  totalMarks: card.totalMarks,
  schemeCitation:
    `SEC English ${card.level === 'higher' ? 'Higher' : 'Ordinary'} Level marking scheme ` +
    `${card.year}, ${pageList(card.schemePages)} — © State Examinations Commission.`,
  specVersion: 'english:outgoing',
  qa: {
    gates: ['verbatim-paper-prompt', 'independent-paper-review', 'paper-gate', 'printed-year-grid', 'indicative-not-checklist'],
    humanReviewedBy: 'independent-paper-review',
    humanReviewedAt: '2026-10',
  },
  rubric: {
    system: 'pclm',
    taskRequirements: card.taskRequirements,
    assessment: publishedAssessment(card, grids),
    ...(card.indicativeMaterial?.length ? { indicativeMaterial: card.indicativeMaterial } : {}),
    indicativeMaterialNote: INDICATIVE_NOTE,
  },
});

/** Runtime cards for one level's published reviewed papers. */
export const publishedCards = (manifest: PublishedEnglishManifest): SecRubricCard[] => {
  if (manifest.cards.length !== manifest.cardCount) {
    throw new Error(`English published ${manifest.level} manifest count is stale`);
  }
  return manifest.cards.map(card => makePublishedCard(card, manifest.grids));
};

export const ENGLISH_AUTHORED_CARD_COUNT = DATA.length;
