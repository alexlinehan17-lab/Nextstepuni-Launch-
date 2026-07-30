/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — deck structure and SAMPLE content.
 *
 * ⚠️ THE CARDS IN THIS FILE ARE SAMPLES, not the authored deck. They exist so the
 * tool's shape can be walked through end to end before any real authoring
 * begins. Every sample card's marking points are quoted from a real SEC scheme
 * that was read directly; nothing here is invented. Topics without sample cards
 * report themselves honestly as not built yet rather than being padded.
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

const SCHEME_2025 = 'Marking points quoted from the SEC marking scheme, Biology 2025 Higher Level — © State Examinations Commission.';
const SCHEME_2023 = 'Marking points quoted from the SEC marking scheme, Biology 2023 Higher Level — © State Examinations Commission.';

const shared = {
  subjectId: 'biology',
  level: 'higher' as const,
  /* Sourced from the final old-syllabus papers. Retained because the SEC will
   * publish no marking scheme for the new specification until roughly August
   * 2027, which makes the 2010–2026 schemes the only official marking-point
   * corpus in existence. Re-tagged to the new units above. */
  specVersion: 'lc-biology-2002',
  qa: { gates: ['verbatim', 'tariff'], humanReviewedBy: 'sample', humanReviewedAt: '2026-07-30' },
};

/** A stand-in illustration, clearly labelled. Real cards bind a cropped SEC
 *  figure by machine-emitted candidate id; drawing over a primary source is the
 *  failure this tool exists to prevent. */
const placeholderFungus = 'data:image/svg+xml;utf8,' + encodeURIComponent(`
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200">
    <rect x="0" y="150" width="300" height="50" fill="#9a9a9a"/>
    <g stroke="#c4c4c4" stroke-width="4" fill="none">
      <path d="M60 150 V95"/><path d="M110 150 V70"/><path d="M160 150 V60"/><path d="M210 150 V85"/>
      <path d="M60 150 C 95 140, 130 140, 160 150"/>
    </g>
    <circle cx="60" cy="88" r="13" fill="#9a9a9a"/><circle cx="110" cy="63" r="15" fill="#9a9a9a"/>
    <circle cx="160" cy="52" r="16" fill="#9a9a9a"/><circle cx="210" cy="78" r="13" fill="#9a9a9a"/>
    <g fill="#9a9a9a"><circle cx="238" cy="70" r="3"/><circle cx="250" cy="62" r="3"/><circle cx="246" cy="80" r="3"/><circle cx="258" cy="74" r="3"/></g>
    <g font-family="Georgia" font-size="17" font-weight="bold" fill="#111">
      <text x="150" y="26">A</text><text x="252" y="46">B</text><text x="92" y="140">C</text>
    </g>
    <g stroke="#111" stroke-width="1.6" fill="none">
      <path d="M155 30 L 160 36"/><path d="M250 50 L 246 58"/><path d="M97 136 L 104 146"/>
    </g>
  </svg>`);

const rhizopus: SecDiagramCard = {
  ...shared, source: 'sec', kind: 'diagram',
  id: 'bio-2025-hl-q16a', topicId: 'bio-3-2', conceptId: 'rhizopus-structure',
  year: 2025, paperFileid: 'LC025ALP040EV', section: 'C', questionRef: '2025 HL Q16(a)',
  stem: 'The diagram shows a fungus grown on bread.',
  questionText: 'Name the structures labelled A, B and C, and give one function of C.',
  tariffModel: { kind: 'fixed' }, totalMarks: 9,
  rows: [
    { id: 'g-a', kind: 'gate', verbatim: 'A — Sporangium', marks: 0, exactTermRequired: true },
    { id: 'g-b', kind: 'gate', verbatim: 'B — Spore', marks: 0, exactTermRequired: true },
    { id: 'g-c', kind: 'gate', verbatim: 'C — Stolon', marks: 0, exactTermRequired: true },
    { id: 'r-fn', kind: 'point', verbatim: 'One function of C — spreads the fungus (to a new food source)', marks: 3 },
    { id: 'r-nut', kind: 'alt', verbatim: 'Method of nutrition — saprophytic', accepts: ['heterotrophic'], openList: true, marks: 6 },
  ],
  figure: {
    candId: 'sample-placeholder', src: placeholderFungus, srcHash: 'sample',
    alt: 'Placeholder illustration: rounded heads on upright stalks, spores dispersing to the right, and a filament running along the surface',
    lettersVisible: ['A', 'B', 'C'],
    attribution: 'Placeholder illustration — not the SEC figure',
  },
  labelKey: [
    { letter: 'A', meaning: 'Sporangium', askedInThisQuestion: true },
    { letter: 'B', meaning: 'Spore', askedInThisQuestion: true },
    { letter: 'C', meaning: 'Stolon', askedInThisQuestion: true },
  ],
  schemeCitation: SCHEME_2025,
};

const digestive: SecCard = {
  ...shared, source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q6-ab', topicId: 'bio-2-6', conceptId: 'digestive-parts',
  year: 2025, paperFileid: 'LC025ALP038EV', section: 'A', questionRef: '2025 HL Q6(a)',
  questionText: 'Name the parts labelled A and B.',
  tariffModel: { kind: 'fixed' }, totalMarks: 4,
  rows: [
    { id: 'r-a', kind: 'point', verbatim: 'A — Oesophagus', marks: 2 },
    { id: 'r-b', kind: 'point', verbatim: 'B — Stomach', marks: 2 },
  ],
  schemeCitation: SCHEME_2025,
};

const peristalsis: SecCard = {
  ...shared, source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q6-bc', topicId: 'bio-2-6', conceptId: 'peristalsis',
  year: 2025, paperFileid: 'LC025ALP038EV', section: 'A', questionRef: '2025 HL Q6(b)–(c)',
  questionText: 'Name and describe briefly the method by which food travels through structure A.',
  tariffModel: { kind: 'fixed' }, totalMarks: 8,
  rows: [
    { id: 'r-name', kind: 'point', verbatim: 'Name — Peristalsis', marks: 3 },
    { id: 'r-desc', kind: 'point', verbatim: '(involuntary) muscular contractions that push food along', marks: 3, dependsOn: 'r-name' },
    { id: 'r-ph', kind: 'point', verbatim: 'The pH lowers as food travels from A to B', marks: 2 },
  ],
  schemeCitation: SCHEME_2025,
};

const waterUptake: SecCard = {
  ...shared, source: 'sec', kind: 'question',
  id: 'bio-2023-hl-q3', topicId: 'bio-2-6', conceptId: 'water-transport',
  year: 2023, paperFileid: 'LC025ALP038EV', section: 'A', questionRef: '2023 HL Q3',
  questionText: 'Outline how water from the soil reaches the leaf of a plant.',
  tariffModel: { kind: 'orderedSplit', notation: '2(5) + 5(2)' }, totalMarks: 20,
  rows: [
    { id: 'w1', kind: 'point', verbatim: 'Root hair', marks: null },
    { id: 'w2', kind: 'point', verbatim: 'Osmosis', marks: null, contextNote: 'The word alone scores nothing — it must be stated as the mechanism of uptake.' },
    { id: 'w3', kind: 'point', verbatim: 'Xylem', marks: null, contextNote: 'Named as the vessel the water travels up.' },
    { id: 'w4', kind: 'point', verbatim: 'Transpiration (pull)', marks: null },
    { id: 'w5', kind: 'point', verbatim: 'Cohesion / adhesion of water molecules', marks: null, openList: true },
  ],
  schemeCitation: SCHEME_2023,
};

const enzymeTemp: SecCard = {
  ...shared, source: 'sec', kind: 'question',
  id: 'bio-2025-hl-q10a', topicId: 'bio-2-1', conceptId: 'enzyme-temperature',
  year: 2025, paperFileid: 'LC025ALP038EV', section: 'B', questionRef: '2025 HL Q10(a)',
  questionText: 'Describe the effect of increasing temperature on the rate of an enzyme-controlled reaction.',
  tariffModel: { kind: 'fixed' }, totalMarks: 12,
  rows: [
    { id: 'e1', kind: 'point', verbatim: 'Rate increases up to the optimum', marks: 3 },
    { id: 'e2', kind: 'point', verbatim: 'Optimum temperature is approximately 37 °C in humans', marks: 3 },
    { id: 'e3', kind: 'point', verbatim: 'Above the optimum the enzyme denatures', marks: 3 },
    { id: 'e4', kind: 'point', verbatim: 'The shape of the active site changes, so substrate no longer fits', marks: 3 },
  ],
  schemeCitation: SCHEME_2025,
};

/** Sample deck. Real authoring replaces this wholesale. */
export const SAMPLE_CARDS: SecCard[] = [rhizopus, digestive, peristalsis, waterUptake, enzymeTemp];

/** True while the deck is sample content, so the UI can say so plainly. */
export const IS_SAMPLE_DECK = true;

export const cardsForTopic = (topicId: string, cards: SecCard[] = SAMPLE_CARDS) =>
  cards.filter(c => c.topicId === topicId);

/** Total marks available in a topic — the denominator for "marks secure". */
export const topicMarks = (topicId: string, cards: SecCard[] = SAMPLE_CARDS) =>
  cardsForTopic(topicId, cards).reduce((n, c) => n + c.totalMarks, 0);
