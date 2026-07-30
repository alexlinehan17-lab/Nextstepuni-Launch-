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

export const ALL_TOPICS: TopicRef[] = STRANDS.flatMap(s => s.topics);
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
    { id: 'r-desc', kind: 'point', verbatim: 'Description — (involuntary) muscular contractions (that push food)', marks: 3, dependsOn: 'r-name' },
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
export const SAMPLE_CARDS: SecCard[] = [
  digestiveParts, peristalsis, rhizopus, rhizopusSexual, scientificMethod,
];

/** True while the deck is a sample slice rather than full coverage. */
export const IS_SAMPLE_DECK = true;

export const cardsForTopic = (topicId: string, cards: SecCard[] = SAMPLE_CARDS) =>
  cards.filter(c => c.topicId === topicId);

/** Total marks available in a topic — the denominator for "marks secure". */
export const topicMarks = (topicId: string, cards: SecCard[] = SAMPLE_CARDS) =>
  cardsForTopic(topicId, cards).reduce((n, c) => n + c.totalMarks, 0);
