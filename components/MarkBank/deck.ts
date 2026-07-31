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


/** The redeveloped Leaving Certificate Physics specification (NCCA, introduced
 *  September 2025, first examined June 2027), read from the specification PDF.
 *  Five strands, thirty units.
 *
 *  ONE DEPARTURE FROM THE DOCUMENT, and it is the document's error, not a
 *  reading of it: the spec prints "U4." twice — once for Modelling in Physics
 *  and again for Unit analysis — and contains no U5 anywhere. They are plainly
 *  separate units, with their own learning outcomes (generating and verifying
 *  models; dimensional analysis and order-of-magnitude estimates), so the second
 *  is numbered U5 here. Anything citing the printed code should expect U4. */
export const PHYSICS_STRANDS: StrandRef[] = [
  {
    id: 'pu', label: 'Unifying strand', title: 'The Nature of Science',
    topics: [
      { id: 'phys-u1', code: 'U1', title: 'Scientific knowledge' },
      { id: 'phys-u2', code: 'U2', title: 'Investigating in science' },
      { id: 'phys-u3', code: 'U3', title: 'Science in society' },
      { id: 'phys-u4', code: 'U4', title: 'Modelling in Physics' },
      { id: 'phys-u5', code: 'U5', title: 'Unit analysis' },
    ],
  },
  {
    id: 'ps1', label: 'Strand 1', title: 'Forces and Motion: Kinematics and Dynamics',
    topics: [
      { id: 'phys-1-1', code: '1.1', title: 'Particle motion in a straight line' },
      { id: 'phys-1-2', code: '1.2', title: 'Forces acting on a particle' },
      { id: 'phys-1-3', code: '1.3', title: 'Stretching and compressing objects' },
      { id: 'phys-1-4', code: '1.4', title: 'A work-energy model for analysing particle motion' },
      { id: 'phys-1-5', code: '1.5', title: 'Forces acting in a gravitational field' },
      { id: 'phys-1-6', code: '1.6', title: 'Uniform circular motion' },
    ],
  },
  {
    id: 'ps2', label: 'Strand 2', title: 'Wave Motion and Energy Transfer',
    topics: [
      { id: 'phys-2-1', code: '2.1', title: 'The transfer of heat energy and temperature change' },
      { id: 'phys-2-2', code: '2.2', title: 'Travelling waves as models of disturbances' },
      { id: 'phys-2-3', code: '2.3', title: 'Wave behaviour caused by interaction with the environment' },
      { id: 'phys-2-4', code: '2.4', title: 'Electromagnetic energy' },
      { id: 'phys-2-5', code: '2.5', title: 'Sound energy' },
      { id: 'phys-2-6', code: '2.6', title: 'Principle of superposition of waves' },
      { id: 'phys-2-7', code: '2.7', title: 'Wave effects' },
    ],
  },
  {
    id: 'ps3', label: 'Strand 3', title: 'Electric and Magnetic Fields and their Interactions',
    topics: [
      { id: 'phys-3-1', code: '3.1', title: 'Charge interactions' },
      { id: 'phys-3-2', code: '3.2', title: 'Modelling electric fields' },
      { id: 'phys-3-3', code: '3.3', title: 'Electric circuits' },
      { id: 'phys-3-4', code: '3.4', title: 'Magnetic fields around permanent and temporary magnets' },
      { id: 'phys-3-5', code: '3.5', title: 'The force on a current-carrying conductor in a magnetic field' },
      { id: 'phys-3-6', code: '3.6', title: 'Induced potential difference and the generator effect' },
    ],
  },
  {
    id: 'ps4', label: 'Strand 4', title: 'Modern Physics: Atomic and Nuclear',
    topics: [
      { id: 'phys-4-1', code: '4.1', title: 'The electron' },
      { id: 'phys-4-2', code: '4.2', title: 'Photoelectric emission and X-ray production' },
      { id: 'phys-4-3', code: '4.3', title: 'Early models of the atom' },
      { id: 'phys-4-4', code: '4.4', title: 'Radioactivity' },
      { id: 'phys-4-5', code: '4.5', title: 'Mass-energy equivalence' },
      { id: 'phys-4-6', code: '4.6', title: 'Harnessing energy from nuclear processes' },
    ],
  },
];

/** Agricultural Science, from the NCCA specification (the 2019 document, first
 *  examined 2021 — so every paper in the corpus sits on this one spec, with no
 *  syllabus change to straddle).
 *
 *  Four strands: a unifying Scientific practices strand whose outcomes permeate
 *  the other three, then Soils, Crops and Animals. Strands 2-4 each carry one
 *  topic that the spec itself subdivides a level deeper — Soil properties into
 *  chemical/physical/biological, and Production into its three stages — and
 *  those subdivisions are kept, because they are how the papers actually
 *  examine: a soil question is a chemistry question or a biology question, and
 *  filing both under "Properties" would hide the distinction the student needs.
 *
 *  The Individual Investigative Study is deliberately absent. It is 100 of the
 *  subject's 400 marks, but it is coursework marked on banded descriptors with
 *  no named answer, so it can never become a card. The deck covers the 300-mark
 *  written paper and the UI should not imply otherwise. */
export const AGRICULTURAL_SCIENCE_STRANDS: StrandRef[] = [
  {
    id: 'as1', label: 'Strand 1', title: 'Scientific practices',
    topics: [
      { id: 'agsci-1-1', code: '1.1', title: 'Hypothesising' },
      { id: 'agsci-1-2', code: '1.2', title: 'Experimenting' },
      { id: 'agsci-1-3', code: '1.3', title: 'Evaluating evidence' },
      { id: 'agsci-1-4', code: '1.4', title: 'Communicating' },
      { id: 'agsci-1-5', code: '1.5', title: 'Working safely' },
    ],
  },
  {
    id: 'as2', label: 'Strand 2', title: 'Soils',
    topics: [
      { id: 'agsci-2-1', code: '2.1', title: 'Formation and classification' },
      { id: 'agsci-2-2-1', code: '2.2.1', title: 'Properties — chemical' },
      { id: 'agsci-2-2-2', code: '2.2.2', title: 'Properties — physical' },
      { id: 'agsci-2-2-3', code: '2.2.3', title: 'Properties — biological' },
      { id: 'agsci-2-3', code: '2.3', title: 'Management' },
    ],
  },
  {
    id: 'as3', label: 'Strand 3', title: 'Crops',
    topics: [
      { id: 'agsci-3-1', code: '3.1', title: 'Plant physiology' },
      { id: 'agsci-3-2', code: '3.2', title: 'Classification/identification' },
      { id: 'agsci-3-3-1', code: '3.3.1', title: 'Production — establishment' },
      { id: 'agsci-3-3-2', code: '3.3.2', title: 'Production — management' },
      { id: 'agsci-3-3-3', code: '3.3.3', title: 'Production — harvesting' },
    ],
  },
  {
    id: 'as4', label: 'Strand 4', title: 'Animals',
    topics: [
      { id: 'agsci-4-1', code: '4.1', title: 'Animal physiology' },
      { id: 'agsci-4-2', code: '4.2', title: 'Classification/identification' },
      { id: 'agsci-4-3-1', code: '4.3.1', title: 'Production — system/enterprise' },
      { id: 'agsci-4-3-2', code: '4.3.2', title: 'Production — management' },
      { id: 'agsci-4-3-3', code: '4.3.3', title: 'Production — animal husbandry' },
    ],
  },
];

/** Every subject the deck covers, with the strand structure of its own
 *  specification. Card topicIds are namespaced by subject, so a card can only
 *  ever be filed under a unit of the subject it belongs to. */
export const SUBJECTS = [
  { id: 'biology', title: 'Biology', strands: STRANDS },
  { id: 'chemistry', title: 'Chemistry', strands: CHEMISTRY_STRANDS },
  { id: 'physics', title: 'Physics', strands: PHYSICS_STRANDS },
  { id: 'agricultural-science', title: 'Agricultural Science', strands: AGRICULTURAL_SCIENCE_STRANDS },
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
  physics: {
    higher: () => import('./cards/physics/higher'),
    ordinary: () => import('./cards/physics/ordinary'),
  },
  // agricultural-science has no entry yet: its cards are still being authored.
  // SUBJECTS lists it so the picker shows it as a deck being written, and
  // sizes.json has no row for it, so deckSize() is 0 and it is never openable.
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
