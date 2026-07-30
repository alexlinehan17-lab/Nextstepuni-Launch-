/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — deck structure and SAMPLE content.
 *
 * These five cards are a SAMPLE SLICE, not full coverage — but they are real.
 * Every question, every marking point and every mark value is transcribed from
 * `examiner-reports/biology/2025-hl-marking-scheme.md`, and both figures are real
 * crops from the 2025 Higher Level paper, opened and checked by eye before being
 * bound (the Biology corpus has four known duplicate-crop pairs, and the alveolus
 * file is one of them — it holds the Rhizopus crop, so it is not used here).
 * Nothing is drawn, approximated or invented. Topics without cards report
 * themselves as not built yet rather than being padded.
 *
 * The taxonomy IS real: these are the twelve units of the redeveloped Leaving
 * Certificate Biology specification (NCCA, introduced September 2025, first
 * examined June 2027), extracted from the specification PDF itself. The old
 * Unit One / Two / Three syllabus was examined for the last time in June 2026,
 * so there is no cohort left for whom the old taxonomy is correct.
 */

import type { SecCard, SecDiagramCard } from '../../types/markBank';
import DECK_SIZES from './cards/sizes.json';


export interface TopicRef {
  id: string;
  code: string;
  title: string;
}

export interface StrandRef {
  id: string;
  label: string;
  title: string;
  topics: TopicRef[];
}

/** The redeveloped specification's own structure, verbatim from the spec. */
export const STRANDS: StrandRef[] = [
  {
    id: 'u', label: 'Unifying strand', title: 'Nature of Science',
    topics: [
      { id: 'bio-u1', code: 'U1', title: 'Scientific knowledge' },
      { id: 'bio-u2', code: 'U2', title: 'Investigating in Science' },
      { id: 'bio-u3', code: 'U3', title: 'Science in society' },
      { id: 'bio-u4', code: 'U4', title: 'Biological reasoning' },
    ],
  },
  {
    id: 's1', label: 'Strand 1', title: 'Organisation of Life',
    topics: [
      { id: 'bio-1-1', code: '1.1', title: 'Characteristics of life' },
      { id: 'bio-1-2', code: '1.2', title: 'Chemicals of life — biomolecules' },
      { id: 'bio-1-3', code: '1.3', title: 'Unit of life — cells' },
      { id: 'bio-1-4', code: '1.4', title: 'Information of life — genetic inheritance' },
      { id: 'bio-1-5', code: '1.5', title: 'Origins of life — evolution' },
    ],
  },
  {
    id: 's2', label: 'Strand 2', title: 'Structures and Processes of Life',
    topics: [
      { id: 'bio-2-1', code: '2.1', title: 'Enzymes' },
      { id: 'bio-2-2', code: '2.2', title: 'Cellular processes — photosynthesis and respiration' },
      { id: 'bio-2-3', code: '2.3', title: 'Information of life — cell division, protein synthesis' },
      { id: 'bio-2-4', code: '2.4', title: 'Response' },
      { id: 'bio-2-5', code: '2.5', title: 'Reproduction' },
      { id: 'bio-2-6', code: '2.6', title: 'Transport and transfer (physiological processes)' },
    ],
  },
  {
    id: 's3', label: 'Strand 3', title: 'Interactions of Life',
    topics: [
      { id: 'bio-3-1', code: '3.1', title: 'Ecology, ecosystems, biodiversity' },
      { id: 'bio-3-2', code: '3.2', title: 'Microorganisms and nutrient cycling' },
      { id: 'bio-3-3', code: '3.3', title: 'Information of life — genetic engineering' },
    ],
  },
];


/** The redeveloped Leaving Certificate Chemistry specification (NCCA, introduced
 *  September 2025, first examined June 2027), read from the specification PDF.
 *  Five strands, twenty units. Note the spec numbers its units with a trailing
 *  dot ("1.1.") — the codes here drop it for display consistency with Biology. */
export const CHEMISTRY_STRANDS: StrandRef[] = [
  {
    id: 'cu', label: 'Unifying strand', title: 'The Nature of Science',
    topics: [
      { id: 'chem-u1', code: 'U1', title: 'Understanding about chemistry' },
      { id: 'chem-u2', code: 'U2', title: 'Investigating in chemistry' },
      { id: 'chem-u3', code: 'U3', title: 'Chemistry in society' },
      { id: 'chem-u4', code: 'U4', title: 'Abstraction to representation' },
    ],
  },
  {
    id: 'cs1', label: 'Strand 1', title: 'Nature of Matter',
    topics: [
      { id: 'chem-1-1', code: '1.1', title: 'Matter' },
      { id: 'chem-1-2', code: '1.2', title: 'Atomic structure' },
      { id: 'chem-1-3', code: '1.3', title: 'The periodic table' },
      { id: 'chem-1-4', code: '1.4', title: 'Quantifying matter' },
    ],
  },
  {
    id: 'cs2', label: 'Strand 2', title: 'Behaviour of Matter',
    topics: [
      { id: 'chem-2-1', code: '2.1', title: 'Chemical bonding' },
      { id: 'chem-2-2', code: '2.2', title: 'Intermolecular forces and molecular shapes' },
      { id: 'chem-2-3', code: '2.3', title: 'Behaviour of gases' },
      { id: 'chem-2-4', code: '2.4', title: 'Hydrocarbons' },
    ],
  },
  {
    id: 'cs3', label: 'Strand 3', title: 'Interactions of Matter',
    topics: [
      { id: 'chem-3-1', code: '3.1', title: 'Thermochemistry' },
      { id: 'chem-3-2', code: '3.2', title: 'Rates of reaction' },
      { id: 'chem-3-3', code: '3.3', title: 'Chemical equilibrium' },
      { id: 'chem-3-4', code: '3.4', title: 'Acid-base systems' },
      { id: 'chem-3-5', code: '3.5', title: 'Electrochemistry' },
    ],
  },
  {
    id: 'cs4', label: 'Strand 4', title: 'Matter in our World',
    topics: [
      { id: 'chem-4-1', code: '4.1', title: 'Volumetric analysis' },
      { id: 'chem-4-2', code: '4.2', title: 'Reactivity of organic compounds' },
      { id: 'chem-4-3', code: '4.3', title: 'Our chemical environment' },
    ],
  },
];

/** Every subject the deck covers, with the strand structure of its own
 *  specification. Card topicIds are namespaced by subject, so a card can only
 *  ever be filed under a unit of the subject it belongs to. */
export const SUBJECTS = [
  { id: 'biology', title: 'Biology', strands: STRANDS },
  { id: 'chemistry', title: 'Chemistry', strands: CHEMISTRY_STRANDS },
] as const;

export type SubjectId = (typeof SUBJECTS)[number]['id'];

export const strandsFor = (subjectId: string) =>
  SUBJECTS.find(s => s.id === subjectId)?.strands ?? STRANDS;

export const ALL_TOPICS: TopicRef[] = SUBJECTS.flatMap(s => s.strands).flatMap(s => s.topics);
export const topicById = (id: string) => ALL_TOPICS.find(t => t.id === id);

/**
 * Figure files that hold the WRONG image and must never be bound to a card.
 *
 * The Biology corpus contains four byte-identical pairs. In each pair one name
 * matches its content and the other inherited its neighbour's crop, because a
 * verifying agent hand-transcribed the crop path and the apply script deduped on
 * destination filename rather than source hash. I opened all four and resolved
 * which side is which: the file named for what it actually shows is kept, its
 * twin is blocked here. The four figures those blocked names should have held
 * were never shipped at all and need re-cropping from the paper.
 */
export const BLOCKED_FIGURES: readonly string[] = [
  'biology-2025-hl-alveolus-gas-exchange', // holds the Rhizopus crop
  'biology-2025-hl-lymphocyte',            // holds the cell-division crop
  'biology-2025-hl-shoulder-joint',        // holds the circulatory-system crop
  'biology-2025-hl-neuron',                // holds the pupil-eyes crop
  'biology-2025-hl-root-longitudinal-section', // crop truncates labels the question asks for
];

const SCHEME_2025 = 'Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission.';

const shared = {
  subjectId: 'biology',
  level: 'higher' as const,
  year: 2025,
  paperFileid: 'LC025ALP038EV',
  /* Sourced from the final old-syllabus papers. Retained because the SEC will
   * publish no marking scheme for the new specification until roughly August
   * 2027, which makes the 2010–2026 schemes the only official marking-point
   * corpus in existence. Re-tagged to the new units above. */
  specVersion: 'lc-biology-2002',
  qa: { gates: ['verbatim', 'tariff', 'figure'], humanReviewedBy: 'agent-verified', humanReviewedAt: '2026-07-30' },
};

/** Real cropped figures from the 2025 Higher Level paper, verified by eye against
 *  the paper before binding. Both were checked for the duplicate-crop defect. */
const DIGESTIVE = {
  candId: 'biology-2025-hl-digestive-system',
  src: '/exam-figures/biology/biology-2025-hl-digestive-system.png',
  srcHash: '471fe80f7312c2c5a68413fb3494428c',
  alt: 'Outline of a human torso showing the digestive tract. A leader line marks the tube running down the neck and chest; a second marks an organ below the liver. The pancreas and small intestine are named on the diagram.',
  lettersVisible: ['A', 'B'],
  attribution: 'SEC Leaving Certificate Biology 2025 Higher Level, Q6 — © State Examinations Commission',
};

const RHIZOPUS = {
  candId: 'biology-2025-hl-rhizopus',
  src: '/exam-figures/biology/biology-2025-hl-rhizopus.png',
  srcHash: 'c12e3971d83734db54a96bd67ecd3b7f',
  alt: 'Rhizopus growing on a substrate: rounded heads on upright stalks, a cluster of small spores being released at the right, and a horizontal filament running across the surface.',
  lettersVisible: ['A', 'B', 'C'],
  attribution: 'SEC Leaving Certificate Biology 2025 Higher Level, Q16 — © State Examinations Commission',
};

/** Q6(a). Scheme: "A: Oesophagus 2 / B: Stomach 2". */
const digestiveParts: SecDiagramCard = {
  ...shared, source: 'sec', kind: 'diagram',
  id: 'bio-2025-hl-q6-a', topicId: 'bio-2-6', conceptId: 'digestive-parts',
  section: 'A', questionRef: '2025 HL Q6(a)',
  questionText: 'Name the parts labelled A and B.',
  tariffModel: { kind: 'fixed' }, totalMarks: 4,
  rows: [
    { id: 'r-a', kind: 'point', verbatim: 'A — Oesophagus', marks: 2 },
    { id: 'r-b', kind: 'point', verbatim: 'B — Stomach', marks: 2 },
  ],
  figure: DIGESTIVE,
  labelKey: [
    { letter: 'A', meaning: 'Oesophagus', askedInThisQuestion: true },
    { letter: 'B', meaning: 'Stomach', askedInThisQuestion: true },
  ],
  schemeCitation: SCHEME_2025,
};

/** Q6(b)–(c). Scheme: "Name: Peristalsis 3 / Description: (involuntary) muscular
 *  contractions (that push food) 3" and "Lowers 2". */
const peristalsis: SecDiagramCard = {
  ...shared, source: 'sec', kind: 'diagram',
  id: 'bio-2025-hl-q6-bc', topicId: 'bio-2-6', conceptId: 'peristalsis',
  section: 'A', questionRef: '2025 HL Q6(b)–(c)',
  questionText: 'Name and describe briefly the method by which food travels through structure A. How does the pH of the food material change as it travels from A to B?',
  tariffModel: { kind: 'fixed' }, totalMarks: 8,
  rows: [
    { id: 'r-name', kind: 'point', verbatim: 'Name — Peristalsis', marks: 3 },
    // No dependsOn: the scheme awards the name and the description as two
    // independent marks. Gating one on the other would deny a student a mark the
    // examiner would have given them.
    { id: 'r-desc', kind: 'point', verbatim: 'Description — (involuntary) muscular contractions (that push food)', marks: 3 },
    { id: 'r-ph', kind: 'point', verbatim: 'pH — Lowers', marks: 2 },
  ],
  figure: DIGESTIVE,
  labelKey: [
    { letter: 'A', meaning: 'Oesophagus', askedInThisQuestion: true },
    { letter: 'B', meaning: 'Stomach', askedInThisQuestion: true },
  ],
  schemeCitation: SCHEME_2025,
};

/** Q16(a)(i)–(iii). Scheme: "A: *Sporangium 1 / B: *Spore 1 / C: *Stolon 1",
 *  "Spread the fungus 3", "Saprophytic or heterotrophic 3". The asterisks mean
 *  the exact term is required — they do NOT mean the row is worth nothing. */
const rhizopus: SecDiagramCard = {
  ...shared, source: 'sec', kind: 'diagram',
  id: 'bio-2025-hl-q16a-i', topicId: 'bio-3-2', conceptId: 'rhizopus-structure',
  paperFileid: 'LC025ALP040EV', section: 'C', questionRef: '2025 HL Q16(a)(i)–(iii)',
  stem: 'The diagram shows Rhizopus growing on bread.',
  questionText: 'Name the structures A, B and C. Give one function of structure C, and name the method of nutrition used by Rhizopus.',
  tariffModel: { kind: 'fixed' }, totalMarks: 9,
  rows: [
    { id: 'g-a', kind: 'gate', verbatim: 'A — Sporangium', marks: 1, exactTermRequired: true },
    { id: 'g-b', kind: 'gate', verbatim: 'B — Spore', marks: 1, exactTermRequired: true },
    { id: 'g-c', kind: 'gate', verbatim: 'C — Stolon', marks: 1, exactTermRequired: true },
    { id: 'r-fn', kind: 'point', verbatim: 'One function of C — spread the fungus', marks: 3 },
    { id: 'r-nut', kind: 'alt', verbatim: 'Method of nutrition — saprophytic', accepts: ['heterotrophic'], marks: 3 },
  ],
  figure: RHIZOPUS,
  labelKey: [
    { letter: 'A', meaning: 'Sporangium', askedInThisQuestion: true },
    { letter: 'B', meaning: 'Spore', askedInThisQuestion: true },
    { letter: 'C', meaning: 'Stolon', askedInThisQuestion: true },
  ],
  schemeCitation: SCHEME_2025,
};

/** Q16(a)(iv)2. Scheme lists nine points, "Any four 4(3)" — a bounded group. */
const rhizopusSexual: SecCard = {
  ...shared, source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q16a-iv', topicId: 'bio-3-2', conceptId: 'rhizopus-sexual-reproduction',
  paperFileid: 'LC025ALP040EV', section: 'C', questionRef: '2025 HL Q16(a)(iv)',
  questionText: 'Describe the process of sexual reproduction in Rhizopus.',
  tariffModel: { kind: 'fixed' }, totalMarks: 12,
  rows: [
    {
      id: 'r-group', kind: 'anyN', verbatim: 'Any four of the following', marks: null,
      group: {
        claimMax: 4, perOption: 3,
        options: [
          '+ and − strains grow close together',
          'swellings form (opposite each other)',
          'progametangia are formed',
          'gametangium formed',
          'fertilisations of haploid nuclei occur',
          'diploid nuclei formed',
          'zygospore formed',
          'survives adverse conditions',
          'germinates by meiosis when suitable conditions are present',
        ],
      },
    },
  ],
  schemeCitation: SCHEME_2025,
};

/** Q7(a)–(c). Scheme: "Hypothesis 2", "Conducting an experiment 3",
 *  "A comparison to the experiment 3". */
const scientificMethod: SecCard = {
  ...shared, source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q7-abc', topicId: 'bio-u2', conceptId: 'scientific-method',
  section: 'A', questionRef: '2025 HL Q7(a)–(c)',
  questionText: 'In the scientific method, a testable statement is known as a ______. How can this statement be tested, and what is the function of a scientific control?',
  tariffModel: { kind: 'fixed' }, totalMarks: 8,
  rows: [
    { id: 'r-hyp', kind: 'point', verbatim: 'Hypothesis', marks: 2 },
    { id: 'r-test', kind: 'point', verbatim: 'Conducting an experiment', marks: 3 },
    { id: 'r-ctrl', kind: 'point', verbatim: 'A comparison to the experiment', marks: 3 },
  ],
  schemeCitation: SCHEME_2025,
};

/** Sample deck: five real cards, every marking point and mark value transcribed
 *  from the 2025 Higher Level scheme on disk, every figure a real crop from the
 *  paper. Real authoring extends this; it does not replace its provenance. */
/**
 * The deck. The five hand-built cards below were the first, written by hand while
 * the card model was being settled; the rest are compiled from the same 2025
 * Higher Level scheme by scripts/markbank/build-deck.mjs. Cards whose question
 * reference collides with a generated one are dropped in favour of the generated
 * version, which went through independent verification.
 */
const HAND_BUILT: SecCard[] = [
  digestiveParts, peristalsis, rhizopus, rhizopusSexual, scientificMethod,
];

/**
 * Cards for one subject at one level, loaded on demand.
 *
 * A student sits one subject at one level, so each pairing is its own module and
 * only the one in front of them is fetched. Shipping the whole deck in a single
 * chunk would make every student download decks they will never open, and that
 * cost grows with every subject and every authoring wave.
 *
 * The imports are spelled out rather than built from a template because the
 * bundler has to see each one to split it; a computed specifier either fails to
 * resolve or drags every deck into one chunk, which is the thing this avoids.
 */
const DECKS: Record<string, Record<Level, () => Promise<{ CARDS: SecCard[] }>>> = {
  biology: {
    higher: () => import('./cards/biology/higher'),
    ordinary: () => import('./cards/biology/ordinary'),
  },
  chemistry: {
    higher: () => import('./cards/chemistry/higher'),
    ordinary: () => import('./cards/chemistry/ordinary'),
  },
};

export type Level = 'higher' | 'ordinary';

/**
 * How many cards each deck holds, written by the build script.
 *
 * Read eagerly, unlike the decks themselves, because the tool has to say which
 * decks are ready BEFORE a student taps one — and answering that by downloading
 * every deck would defeat the splitting above. A subject absent here has nothing
 * built yet.
 */
export const deckSize = (subjectId: string, level: Level): number =>
  (DECK_SIZES as Record<string, Partial<Record<Level, number>>>)[subjectId]?.[level] ?? 0;

/** Decks with cards in them, as "Biology Higher"-style labels. */
export const builtDecks = (): { subjectId: string; level: Level; label: string }[] =>
  SUBJECTS.flatMap(s => (['higher', 'ordinary'] as Level[])
    .filter(l => deckSize(s.id, l) > 0)
    .map(l => ({ subjectId: s.id, level: l, label: `${s.title} ${l === 'higher' ? 'Higher' : 'Ordinary'}` })));

export async function loadCards(subjectId: string, level: Level): Promise<SecCard[]> {
  const load = DECKS[subjectId]?.[level];
  if (!load) return [];
  const mod = await load();
  if (subjectId !== 'biology') return mod.CARDS;
  // The five hand-built Biology cards predate the build script. A generated card
  // for the same question supersedes one, because that one went through
  // independent verification and these were written while the model was settling.
  const refs = new Set(mod.CARDS.map(c => c.questionRef));
  return [...mod.CARDS, ...HAND_BUILT.filter(c => c.level === level && !refs.has(c.questionRef))];
}

export const cardsForTopic = (topicId: string, cards: SecCard[]) =>
  cards.filter(c => c.topicId === topicId);

/** Total marks available in a topic — the denominator for "marks secure". */
export const topicMarks = (topicId: string, cards: SecCard[]) =>
  cardsForTopic(topicId, cards).reduce((n, c) => n + c.totalMarks, 0);
