#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — compile authored cards into the deck modules.
 *
 * Input is the JSON produced by an authoring workflow. This script does the two
 * things an authoring agent is never allowed to do: bind a figure, and name a
 * paper. Agents name a figure by KEY only and never name a paper at all; the real
 * path, hash, attribution and SEC file id are resolved here from data on disk.
 * Both historical figure corruptions in this repo entered through a
 * hand-transcribed path, and the first Biology build pointed every card at the
 * marking scheme PDF instead of the question paper for the same reason.
 *
 * The subject is taken from the cards themselves, not a flag — a flag that
 * disagreed with the data would file a deck under the wrong subject silently.
 *
 *   node scripts/markbank/build-deck.mjs <cards.json>
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

import { resolvePaperFileid, resolveCompanionFileid, corpusSubjectFor } from './paperIndex.mjs';
import { normalise, comparableScheme, claimMatches } from './schemeText.mjs';
import { optionCapFor, MAX_LONG_OPTION_ROWS } from './optionCap.mjs';
import { isContentFreeRow } from './contentFree.mjs';
import { questionStandsAlone } from './questionText.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

/** Per-subject facts the generated module needs. Adding a subject means adding
 *  a row here, and nothing else in this script changes. */
const SUBJECTS = {
  engineering: {
    title: 'Engineering',
    /* The syllabus's section 2, "Materials and Technology", is what the
     * written examination covers -- 300 marks at Higher, 200 at Ordinary.
     * Its fourteen headings are the topics, plus the mechanisms heading from
     * section 1. See ENGINEERING_STRANDS in components/MarkBank/deck.ts. */
    specVersion: 'lc-engineering-materials-and-technology',
    specNote: 'Cards are tagged to the headings of the Engineering syllabus, section 2 Materials and Technology.\n * The written paper sets nine questions of 50 marks at Higher and seven at Ordinary; candidates answer six and four.',
    figureDir: 'public/exam-figures/engineering',
    blocked: new Set(),
  },
  technology: {
    title: 'Technology',
    /* The syllabus these papers were sat under -- seven core areas and five
     * options, of which a candidate studies two. Named by what it is rather
     * than by a year: no redeveloped Technology specification is examined
     * yet. See TECHNOLOGY_STRANDS in components/MarkBank/deck.ts. */
    specVersion: 'lc-technology-syllabus',
    specNote: 'Cards are tagged to the areas of the Leaving Certificate Technology syllabus:\n * seven core areas, examined in Sections A and B, and the five options, of which\n * Section C sets one question each and a candidate answers one.',
    figureDir: 'public/exam-figures/technology',
    blocked: new Set(),
  },
  'computer-science': {
    title: 'Computer Science',
    /* The specification first examined in 2020 -- the one these papers were
     * sat under, and the current one. Three strands: the practices and
     * principles, the five core concepts, and the four applied learning
     * tasks. Read from the specification PDF; see COMPUTER_SCIENCE_STRANDS
     * in components/MarkBank/deck.ts. */
    specVersion: 'lc-computer-science-2020',
    specNote: 'Cards are tagged to the strands of the Computer Science specification examined from 2020.\n * Sections A and B sit in one booklet and Section C, the programming task, in another.',
    figureDir: 'public/exam-figures/computer-science',
    blocked: new Set(),
  },
  maths: {
    title: 'Mathematics',
    /* The syllabus examined from 2015. Its redevelopment is scheduled but not
     * yet examined, so there is nothing later to tag against. */
    specVersion: 'lc-maths-2015',
    specNote: 'Cards are tagged to the strands of the Mathematics syllabus examined from 2015.\n * Higher and Ordinary sit two papers, and a citation names which.',
    figureDir: 'public/exam-figures/maths',
    blocked: new Set(),
  },
  'construction-studies': {
    title: 'Construction Studies',
    /* The syllabus these papers were actually sat under. Its replacement,
     * Construction Technology, is first examined 2028, so unlike the science
     * subjects there is no redeveloped specification to tag against and the
     * cards are filed where a student revising them is actually studying. */
    specVersion: 'lc-construction-studies-syllabus',
    specNote: 'Cards are tagged to the sections of the Construction Studies syllabus these\n * papers were sat under. Construction Technology replaces it from 2028.',
    figureDir: 'public/exam-figures/construction-studies',
    blocked: new Set(),
  },
  biology: {
    title: 'Biology',
    specVersion: 'lc-biology-2002',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Biology specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/biology',
    /** Crops that hold a neighbour's image, or truncate a label the question
     *  asks about. Never bindable. Mirrors BLOCKED_FIGURES in deck.ts. */
    blocked: new Set([
      'alveolus-gas-exchange', 'lymphocyte', 'shoulder-joint', 'neuron',
      'root-longitudinal-section', 'cell-membrane',
    ]),
  },
  physics: {
    title: 'Physics',
    /* The syllabus examined before the 2027 redevelopment, named by what it is
     * rather than by a year — its publication year is unverified here, and an
     * unverified date in a provenance field is worse than none. */
    specVersion: 'lc-physics-legacy',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Physics specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/physics',
    blocked: new Set(),
  },
  chemistry: {
    title: 'Chemistry',
    /* The syllabus examined before the 2027 redevelopment. Named by what it is
     * rather than by a year, because I have not verified its publication year
     * and an unverified date in a provenance field is worse than none. */
    specVersion: 'lc-chemistry-legacy',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Chemistry specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/chemistry',
    blocked: new Set(),
  },
  business: {
    title: 'Business',
    /* The 1999 syllabus, still examined. Named by year because it is verified:
     * every paper in the corpus (2021-2025) sits on it. */
    specVersion: 'lc-business-1999',
    specNote: 'Cards are tagged to the units of the REDEVELOPED Business specification, first\n * examined June 2027, not to the syllabus the 2021-2025 papers were sat under.',
    figureDir: 'public/exam-figures/business',
    blocked: new Set(),
  },
  'home-economics': {
    title: 'Home Economics',
    /* The syllabus examined before the 2027 redevelopment. Named by what it is
     * rather than by a year, because its publication year is unverified here. */
    specVersion: 'lc-home-economics-legacy',
    specNote: 'Cards are tagged to the areas of the Scientific and Social syllabus, which is the\n * one these papers were sat under and the one still being sat: the NCCA schedule\n * introduces a replacement in 2027 for first examination in 2029.',
    figureDir: 'public/exam-figures/home-economics',
    blocked: new Set(),
  },
  economics: {
    title: 'Economics',
    /* The NCCA specification published February 2019 and first examined in 2021
     * — dated because it IS verified: every paper in the corpus (2021-2025) sits
     * on it, with no syllabus change to straddle. */
    specVersion: 'lc-economics-2019',
    specNote: 'Cards are tagged to the strands of the specification the papers were actually sat\n * under. Economics was first examined on it in 2021, so the whole 2021-2025\n * corpus sits on one syllabus with nothing to straddle.',
    figureDir: 'public/exam-figures/economics',
    blocked: new Set(),
  },
  history: {
    title: 'History',
    /* The syllabus these papers were sat under. Its redevelopment is
     * introduced in 2027 for first examination in 2029, so there is nothing
     * later to tag against. Named by what it is rather than by a year: the
     * publication year is unverified here, and an unverified date in a
     * provenance field is worse than none. */
    specVersion: 'lc-history-syllabus',
    specNote: "Cards are tagged to the syllabus's four fields-and-areas and the six topics in\n * each. A candidate sits ONE field of study — Later Modern or Early Modern — which\n * the SEC prints as separate papers, so every citation names its field.",
    figureDir: 'public/exam-figures/history',
    blocked: new Set(),
  },
  'religious-education': {
    title: 'Religious Education',
    /* The syllabus published in 2003 and still examined — the whole
     * 2021-2025 corpus sits on it, with nothing to straddle. Named by year
     * because it is verified: the SEC's own scheme cites "the Leaving
     * Certificate Religious Education syllabus published by the Department of
     * Education and Skills in 2003" in its general introduction. */
    specVersion: 'lc-religious-education-2003',
    specNote: "Cards are tagged to the syllabus's own ten sections, A to J, which are the\n * sections the paper prints. A candidate answers Section A, two of B-D and one or\n * two of E-J; every section in the corpus is carded at both levels.",
    figureDir: 'public/exam-figures/religious-education',
    blocked: new Set(),
  },
  lcvp: {
    title: 'Link Modules',
    /* The LCVP programme statement, still examined: Life, Community and Work
     * replaces it from 2028, so the whole 2018-2025 corpus sits on this one.
     * Its two link modules and five units each are the topics; see
     * LCVP_STRANDS in components/MarkBank/deck.ts, which reads them from the
     * canonical curriculum rather than keeping a second list. */
    specVersion: 'lcvp-link-modules-programme-statement',
    specNote: 'Cards are tagged to the units of the LCVP Link Modules programme statement, which is\n * the one these papers were sat under. Life, Community and Work replaces it from 2028.\n * The paper is COMMON level: one paper, sat by everyone, cited "YYYY CL".',
    figureDir: 'public/exam-figures/lcvp',
    blocked: new Set(),
  },
  german: {
    title: 'German',
    /* The syllabus these papers were sat under and the one still being sat.
     * Named by what it is rather than by a year: the redeveloped Modern
     * Foreign Languages specifications are not examined yet, so there is
     * nothing later to tag against. */
    specVersion: 'lc-german-syllabus',
    specNote: 'Cards are tagged to the strands of the Leaving Certificate German syllabus.\n * A sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the TEXT it quotes,\n * bound to the pages of the question paper it was printed on. The answer\n * language differs WITHIN one comprehension, so each card states its own.',
    figureDir: 'public/exam-figures/german',
    blocked: new Set(),
  },
  french: {
    title: 'French',
    /* The syllabus these papers were sat under and the one still being sat.
     * Named by what it is rather than by a year: the redeveloped Modern
     * Foreign Languages specifications are not examined yet, so there is
     * nothing later to tag against. */
    specVersion: 'lc-french-syllabus',
    specNote: 'Cards are tagged to the strands of the Leaving Certificate French syllabus.\n * A sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the passage it quotes,\n * bound to the pages of the question paper it was printed on.',
    figureDir: 'public/exam-figures/french',
    blocked: new Set(),
  },
  polish: {
    title: 'Polish',
    /* The syllabus these papers were sat under. Polish is a NON-CURRICULAR EU
     * LANGUAGE: there is no Irish syllabus for it, and the SEC examines it
     * against the language itself. It was rebuilt in 2022 — before that one
     * 70-mark booklet at ONE level, since then Section A Reading and Section B
     * Written Production at two levels with a Listening Comprehension Test
     * beside them. See POLISH_STRANDS in components/MarkBank/deck.ts. */
    specVersion: 'lc-polish-non-curricular-eu-language',
    specNote: "Cards are tagged to the task types of the Leaving Certificate Polish examination.\n * From 2022 a sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the text it quotes, bound to\n * the pages of the question paper it was printed on. One comprehension is set in\n * two languages: the scheme awards HALF MARKS for an answer given in the wrong\n * one, so every card says which language its answer must be in.",
    figureDir: 'public/exam-figures/polish',
    blocked: new Set(),
  },
  lithuanian: {
    title: 'Lithuanian',
    /* The examination these papers were sat under. Lithuanian is a
     * NON-CURRICULAR EU LANGUAGE: there is no Irish syllabus for it, and the
     * SEC examines it against the language itself. The corpus holds three
     * printed shapes — I/II/III DALIS out of 100 to 2020, I/II DALIS out of 70
     * in 2021, and from 2022 Dalis A Skaitymas and Dalis B Rašymas at two
     * levels with a Listening Comprehension Test beside them. See
     * LITHUANIAN_STRANDS in components/MarkBank/deck.ts. */
    specVersion: 'lc-lithuanian-non-curricular-eu-language',
    specNote: "Cards are tagged to the task types of the Leaving Certificate Lithuanian examination.\n * From 2022 a sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the text it quotes, bound to\n * the pages of the question paper it was printed on. One comprehension is set in\n * two languages: the scheme awards HALF MARKS for an answer given in the wrong\n * one, so every card of those sittings says which language its answer must be in.",
    figureDir: 'public/exam-figures/lithuanian',
    blocked: new Set(),
  },
  latvian: {
    title: 'Latvian',
    /* Latvian never made the 2022 change Lithuanian and Polish did: every
     * sitting in the corpus, 2010 to 2026, is the old examination — one
     * Higher-only booklet, three parts, no Listening Comprehension Test. */
    specVersion: 'lc-latvian-non-curricular-eu-language',
    specNote: "Cards are tagged to the task types of the Leaving Certificate Latvian examination.\n * A sitting is ONE booklet at ONE level: an article, six questions on it, a\n * commentary and an essay. Every reading card carries the text it quotes, bound to\n * the pages of the question paper it was printed on.",
    figureDir: 'public/exam-figures/latvian',
    blocked: new Set(),
  },
  czech: {
    title: 'Czech',
    /* Czech, like Latvian, prints the old examination in every year of the
     * corpus. */
    specVersion: 'lc-czech-non-curricular-eu-language',
    specNote: "Cards are tagged to the task types of the Leaving Certificate Czech examination.\n * A sitting is ONE booklet at ONE level: an article, six questions on it, a\n * commentary and an essay. Every reading card carries the text it quotes, bound to\n * the pages of the question paper it was printed on.",
    figureDir: 'public/exam-figures/czech',
    blocked: new Set(),
  },
  russian: {
    title: 'Russian',
    /* The syllabus these papers were sat under and the one still being sat.
     * Named by what it is rather than by a year: the redeveloped Modern
     * Foreign Languages specifications are not examined yet, so there is
     * nothing later to tag against. */
    specVersion: 'lc-russian-syllabus',
    specNote: "Cards are tagged to the task types of the Leaving Certificate Russian syllabus.\n * A sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the text it quotes, bound\n * to the pages of the question paper it was printed on. Comprehension and\n * information retrieval are answered in English or Irish; the language-awareness\n * tasks are answered in RUSSIAN, and the scheme awards no marks for either in\n * the wrong language.",
    figureDir: 'public/exam-figures/russian',
    blocked: new Set(),
  },
  italian: {
    title: 'Italian',
    /* The syllabus these papers were sat under and the one still being sat.
     * Named by what it is rather than by a year: the redeveloped Modern
     * Foreign Languages specifications are not examined yet, so there is
     * nothing later to tag against. */
    specVersion: 'lc-italian-syllabus',
    specNote: 'Cards are tagged to the task types of the Leaving Certificate Italian syllabus.\n * A sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the passage, advertisement\n * or literary extract it quotes, bound to the page of the question paper facing\n * its own questions. Higher answers Sections A and B in ITALIAN except the last\n * ask of each comprehension; Ordinary answers everything in Irish or English.',
    figureDir: 'public/exam-figures/italian',
    blocked: new Set(),
  },
  japanese: {
    title: 'Japanese',
    /* The syllabus these papers were sat under and the one still being sat.
     * Named by what it is rather than by a year: the redeveloped Modern
     * Foreign Languages specifications are not examined yet, so there is
     * nothing later to tag against. */
    specVersion: 'lc-japanese-syllabus',
    specNote: 'Cards are tagged to the task types of the Leaving Certificate Japanese syllabus.\n * A sitting is TWO booklets — the written paper and a separate Listening\n * Comprehension Test — and every reading card carries the web page, article,\n * blog or e-mail it is answered from, bound to the pages of the question paper\n * it was printed on. The answer language changes INSIDE a question: 問題2 heads\n * its first items "Answer in English" and its third "Answer in Japanese", and\n * the scheme pays half marks for the wrong one, so every card says which is\n * wanted. Furigana — the kana reading the SEC sets ABOVE a kanji — is folded\n * into the line in brackets, 秋葉原（あきはばら）, and every card carrying\n * Japanese discloses the convention.',
    figureDir: 'public/exam-figures/japanese',
    blocked: new Set(),
  },
  latin: {
    title: 'Latin',
    /* The LEGACY written paper, which is what every sitting in the corpus is.
     * Latin's specification was redeveloped and its Strands 1 and 2 describe a
     * course assessed by a capstone text and a research study the SEC has not
     * examined yet; the syllabus strand these cards tag against is the legacy
     * paper's own seven task types. See LATIN_STRANDS in deck.ts. */
    specVersion: 'lc-latin-syllabus',
    specNote: 'Cards are tagged to the task types of the legacy Leaving Certificate Latin\n * written paper, which is the paper every sitting in the bank was sat on. Latin\n * is examined in ONE booklet with no listening test. Three of its five questions\n * print a CHOICE of routes a candidate answers one of — "Answer either Section A\n * or Section B" — so a card names the route it was set under. Every unseen\n * comprehension card carries the Latin passage, the English summary and the\n * vocabulary the SEC glossed it with, bound to the page of the question paper\n * they were printed on; a card whose ask names a photograph opens the plate\n * page at the back of the same booklet. Translation asks are NOT carded: the\n * scheme prices them by segment, but the segments are the source text and not\n * a model answer.',
    figureDir: 'public/exam-figures/latin',
    blocked: new Set(),
  },
  arabic: {
    title: 'Arabic',
    /* The syllabus these ten sittings were set on, which is examined to June
     * 2026; the redeveloped specification is examined from 2027 and no paper
     * exists to card against it yet. */
    specVersion: 'lc-arabic-syllabus',
    specNote: 'Cards are tagged to the task types of the Leaving Certificate Arabic syllabus\n * examined to June 2026. A sitting is ONE booklet — Arabic sets no Listening\n * Comprehension Test — numbered 1 to 15 straight through four printed parts, so\n * an ask is cited by its number and part letter alone. The paper is set in\n * Arabic and answered in Arabic, and every card says so, because Arabic reads\n * RIGHT TO LEFT and a card that does not say which language is wanted marks a\n * right answer wrong. The SEC letters its parts (أ) to (ه); a citation letters\n * them a to e, in that same abjad order.',
    figureDir: 'public/exam-figures/arabic',
    blocked: new Set(),
  },
  'classical-studies': {
    title: 'Classical Studies',
    /* TWO syllabuses, because the corpus straddles the change: 2021 and 2022
     * were sat on the ten-topic syllabus and 2023 onwards on the four-strand
     * specification. A card is filed under the course its own paper was set
     * on — the legacy strand in deck.ts holds the ten topics the old paper
     * prints over its own questions. */
    specVersion: 'lc-classical-studies-2020',
    specNote: 'Cards are tagged to the four strands of the Classical Studies specification\n * first examined in 2023, and to the ten topics of the syllabus the 2021 and 2022\n * papers were sat on. A sitting is TWO booklets — the question paper and the\n * accompanying Paper X of photographs and images — and a card whose ask names\n * one of those images opens Paper X at the page that booklet heads with it.',
    figureDir: 'public/exam-figures/classical-studies',
    blocked: new Set(),
  },
  'applied-maths': {
    title: 'Applied Maths',
    /* The specification first examined in 2023 — dated because it is verified
     * against the papers themselves: the 2023-2025 booklets head themselves
     * "Applied Mathematics – M32 2025" and set the graph theory, critical-path
     * analysis and difference equations the revised course added. The 2021 and
     * 2022 papers are the OUTGOING syllabus, which the specification kept whole
     * inside Strand 3, so both sides of the break tag against one taxonomy.
     * See APPLIED_MATHS_STRANDS in components/MarkBank/deck.ts, which reads the
     * four strands from the canonical curriculum. */
    specVersion: 'lc-applied-mathematics-2021',
    specNote: 'Cards are tagged to the four strands of the Applied Mathematics specification\n * first examined in 2023. The 2021 and 2022 papers were sat on the outgoing\n * mechanics syllabus, which Strand 3 of that specification contains whole.',
    figureDir: 'public/exam-figures/applied-maths',
    blocked: new Set(),
  },
  spanish: {
    title: 'Spanish',
    /* The syllabus these papers were sat under and the one still being sat.
     * Named by what it is rather than by a year: the redeveloped Modern
     * Foreign Languages specifications are not examined yet, so there is
     * nothing later to tag against. */
    specVersion: 'lc-spanish-syllabus',
    specNote: 'Cards are tagged to the strands of the Leaving Certificate Spanish syllabus.\n * A sitting is THREE booklets — the written paper, a separate Listening\n * Comprehension Test, and at Higher a two-page loose sheet carrying the Section B\n * article. Every reading card carries the text it quotes, bound to the pages of\n * the booklet that printed it; the Section B cards bind the loose sheet by its\n * own SEC file id, not the question paper\u2019s.',
    figureDir: 'public/exam-figures/spanish',
    blocked: new Set(),
  },
  'agricultural-science': {
    title: 'Agricultural Science',
    /* The NCCA specification published 2019 and first examined in 2021 — dated
     * here because it IS verified: every paper in the corpus (2021-2025) sits on
     * it, with no syllabus change to straddle. */
    specVersion: 'lc-agricultural-science-2019',
    specNote: 'Cards are tagged to the strands of the specification the papers were actually sat\n * under: this one has been the examined specification since 2021.',
    figureDir: 'public/exam-figures/agricultural-science',
    blocked: new Set(),
  },
};

/**
 * Alt text for the Biology figures actually looked at, from before the figure
 * manifest existed. A figure with no entry here has not been inspected, so it
 * cannot be bound — describing an image nobody opened is how Diagram Vault ended
 * up confidently captioning bread mould as an alveolus.
 */
const ALT = {
  "cell-membrane-labelled": "Cross-section of a cell membrane: a curved phospholipid bilayer with proteins embedded in and across it. A brace marks X at the bilayer itself on the left, and an arrow marks Y at a protein spanning the membrane.",
  "digestive-system": "Outline of a human torso showing the digestive tract. A leader line marks the tube running down the neck and chest; a second marks an organ below the liver. The pancreas and small intestine are named on the diagram.",
  "rhizopus": "Rhizopus growing on a substrate: rounded heads on upright stalks, a cluster of small spores being released at the right, and a horizontal filament running across the surface.",
  "cell-division": "A cell late in division: two daughter nuclei have formed, each with chromosomes drawn on a spindle, and the cell is pinching in at the middle.",
  "circulatory-system": "A whole-body circulatory diagram: the heart at the centre, lungs above, and vessels running to the liver, gut, kidneys and the capillary beds of the head and lower body.",
  "pupil-eyes": "Two eyes side by side, drawn identically except that the pupil is small in the left and much larger in the right.",
  "mitochondrion": "Cross-section of a mitochondrion: a smooth outer membrane and an inner membrane folded into long finger-like cristae, with small dots scattered through the interior.",
  "chloroplast": "Cross-section of a chloroplast: an outer envelope enclosing four stacks of disc-shaped compartments joined by flattened channels, with small dots in the surrounding fluid. No parts are lettered.",
  "embryo-sac": "A carpel in section on the left, with an arrow enlarging its ovule on the right. Inside the enlarged ovule, leader lines mark P at a pair of central nuclei and Q at a cell below them.",
  "neurons": "Two neurons drawn side by side. Neuron X has a branched cell body at the top and runs down to a block of muscle cells; Neuron Y runs from a patch of skin at the bottom up past its cell body. A brace marks Z at the fine branches at the top of Y, and arrows name the Schwann cells along both axons.",
  "sperm-sem": "Electron micrograph of a single sperm cell against a dark background, with a 2 micrometre scale bar. An arrow marks A at the rounded head and a second marks B partway along the tail.",
  "fermenter": "Photograph of an industrial stainless-steel fermenter: a sealed cylindrical vessel on a wheeled frame, with pipework, valves and gauges around it. No parts are lettered.",
};

/* ------------------------------------------------------- provenance gate ---- */

const schemeCache = new Map();

/** The level tokens a deck may carry.
 *
 * 'common' is not a third grade of difficulty: LCVP's Link Modules paper is
 * sat at ONE level by everyone, which is what the SEC's own file id says with
 * its level letter C (LC462CLP000EV.pdf) and what the canonical curriculum
 * already records. Filing it as 'higher' would have every card cite a Higher
 * Level paper that does not exist.
 */
const LEVELS = ['higher', 'ordinary', 'common'];
const LEVEL_TOKEN = { higher: 'hl', ordinary: 'ol', common: 'cl' };
const LEVEL_WORD = { higher: 'Higher', ordinary: 'Ordinary', common: 'Common' };

function schemeFor(subjectId, card) {
  const stem = `${card.year ?? 2025}-${LEVEL_TOKEN[card.level ?? 'higher'] ?? 'hl'}`;
  const file = resolve(ROOT, 'examiner-reports', subjectId, 'schemes', `${stem}.md`);
  if (!schemeCache.has(file)) {
    const raw = existsSync(file) ? readFileSync(file, 'utf8') : '';
    schemeCache.set(file, comparableScheme(raw));
  }
  return schemeCache.get(file);
}

/**
 * Row kinds the deck's own type accepts.
 *
 * Nothing validated this, and it showed: the authored Home Economics file had
 * drifted to kinds ("required", "explain") that are not in RowKind, which the
 * build happily emitted and typecheck then rejected — after the deck had been
 * written. Caught here the card is dropped with a reason instead.
 * Mirrors RowKind in types/markBank.ts.
 */
/** The glyph a broken subset font left behind, if the card still shows one.
 *
 * Word embeds its fonts as subsets whose ToUnicode map is wrong, so a scheme's
 * text layer spells "tan" in Oriya and "Certificate" as "CerƟficate".
 * derive_glyphs.py repairs what it can prove; this refuses to ship the rest.
 * A card that reads "h^(ᇱᇱ)(x)" where the scheme prints "h''(x)" is not a
 * smaller version of the right card, it is the wrong one, and it went out
 * looking poor because nothing was checking. Greek is genuinely Greek here,
 * and the two combining marks carry p-hat and z-bar. */
/* Greek is genuinely Greek, the two combining marks carry p-hat and z-bar,
 * and U+0152/U+0153 are the French OE ligature -- a letter of the language,
 * printed in 'sœur', 'cœur', 'nœud'. Refusing it dropped a correct French
 * card for containing a French letter. */
/* Characters inside BROKEN's range that a scheme really does print.
 * Greek and the hat and bar were here already; the DOT and DOUBLE DOT are
 * Newton's notation for a derivative — the 2022 Higher Applied Maths scheme
 * sets "ẋ = A ω cos(ωt + ε)" and "ẍ = −A ω² sin(ωt + ε)" — and U+1D62-U+1D6A
 * are the Unicode subscripts mathtext.subscripts() itself emits, so refusing
 * them threw away a card for spelling v_r the way the reader spelled it. */
/* Cyrillic (U+0400-U+04FF) is genuinely Cyrillic, for the same reason Greek is
 * genuinely Greek: it is the alphabet the Russian paper and its scheme are
 * printed in. Left inside BROKEN, every Russian marking point read as a page
 * of unreadable glyphs and the whole deck was refused. */
/* Latin Extended-A (U+0100-U+017F) is genuinely Latin Extended-A, for the same
 * reason Cyrillic is genuinely Cyrillic: ą ć ę ł ń ó ś ź ż are letters of the
 * POLISH alphabet, printed in every Polish paper and every Polish scheme, and
 * they reach the text layer intact. Left inside BROKEN, half the Polish deck
 * was refused for being written in Polish -- "Księgarnia była mała" counted as
 * four unreadable glyphs. The block also carries the French OE ligature and
 * the ligature glyphs LIGATURES already folds, which are handled before this
 * test is reached. */
const REAL = /[\u0100-\u017F\u0370-\u03FF\u0400-\u04FF\u0302\u0305\u0307\u0308\u02B0-\u02FF\u1D62-\u1D6A\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]/;
/* Script that is really script, inside the range the broken-subset test
 * sweeps. Arabic joins it because Arabic ships: 0600-06FF is the alphabet the
 * SEC sets its Arabic paper in, 0750-077F and 08A0-08FF the supplements. What
 * does NOT join it is the Arabic Presentation Forms — FB50-FDFF and FE70-FEFF
 * — because those are the SHAPED glyphs the text layer hands back and
 * ara_text.py folds them to their letters; one reaching a card means the fold
 * failed, which is exactly what this gate is for. */
const BROKEN = /[\u0100-\u1FFF\uE000-\uF8FF\uFB00-\uFB4F]/g;
/** Undo a subset font's broken ToUnicode map, using the table derived from the
 * schemes themselves by scripts/markbank/authoring/derive_glyphs.py. Applied
 * here as well as at authoring time so every subject benefits from a re-derived
 * table on its next build, without ten reader scripts each having to know. */
const GLYPHS = JSON.parse(readFileSync(
  resolve(ROOT, 'scripts/markbank/authoring/glyphmap.json'), 'utf8'));

/* CambriaMath text layers sometimes return each mathematical LETTER twice at
 * the same drawing origin. Collapsing letters is safe; doubled mathematical
 * digits are not, because the same font can map a different digit onto the
 * repeated glyph. Those are refused below instead of guessed. */
const DOUBLED_MATHS_LETTER = /([\u{1D400}-\u{1D7CD}])\1/gu;
const DOUBLED_MATHS_DIGIT = /([\u{1D7CE}-\u{1D7FF}])\1/u;

function repairText(text) {
  if (typeof text !== 'string') return text;
  let out = text;
  for (let i = 0; i < 4; i++) {
    const next = out.replace(DOUBLED_MATHS_LETTER, '$1');
    if (next === out) break;
    out = next;
  }
  if (!BROKEN.test(out)) return out;
  BROKEN.lastIndex = 0;
  return [...out].map(ch => GLYPHS[ch] ?? ch).join('');
}

/* Every string on the card, not a list of the fields that were mangled the
 * last time someone looked. Naming them missed contextNote, which is where the
 * business deck kept its "the word set as GiOen is often" asides -- text that
 * exists only because the mangling was not being repaired. Ids and keys are
 * ASCII, so walking them costs a failed regex test and changes nothing. */
function walkStrings(node, fn) {
  if (Array.isArray(node)) {
    node.forEach((v, i) => {
      if (typeof v === 'string') node[i] = fn(v);
      else if (v && typeof v === 'object') walkStrings(v, fn);
    });
  } else if (node && typeof node === 'object') {
    for (const k of Object.keys(node)) {
      const v = node[k];
      if (typeof v === 'string') node[k] = fn(v);
      else if (v && typeof v === 'object') walkStrings(v, fn);
    }
  }
}

function repairGlyphs(card) { walkStrings(card, repairText); }

function brokenGlyphs(text) {
  if (DOUBLED_MATHS_DIGIT.test(text)) {
    return 'a doubled maths digit whose value the text layer has lost — the font mis-maps some digits, so the pair cannot be collapsed';
  }
  const hits = (text.match(BROKEN) ?? []).filter(ch => !REAL.test(ch));
  if (!hits.length) return null;
  const uniq = [...new Set(hits)];
  return `${hits.length} unreadable glyph(s) from a broken font subset, e.g. `
    + uniq.slice(0, 4).map(ch => `U+${ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')}`).join(' ');
}

function mangledText(card) {
  const seen = [];
  // Author notes may quote a corrupt extraction specifically to document why
  // it was rejected; notes never ship, so police only the card students see.
  const { notes, ...shipped } = card;
  walkStrings(shipped, (v) => { seen.push(v); return v; });
  return brokenGlyphs(seen.join(' '));
}

const ROW_KINDS = new Set(['point', 'alt', 'allOf', 'anyN', 'criterion', 'gate']);

function badRowKind(c) {
  for (const r of c.rows) {
    if (!ROW_KINDS.has(r.kind)) {
      return `row "${r.id}" has kind "${r.kind}", which is not one of ${[...ROW_KINDS].join(', ')}`;
    }
  }
  return null;
}

/** Text that is a table fragment or a header rather than an answerable question. */
function badQuestion(text, card) {
  const t = String(text).trim();
  if (!questionStandsAlone(card)) return 'question text is too short to stand alone';
  if (/^section\s+[abc]\b/i.test(t)) return 'question text is a section header';
  if (/^question\s+\d+\.?$/i.test(t)) return 'question text is just a question number';
  if (/^\(?\d+\s*m(arks)?\)?\.?$/i.test(t)) return 'question text is a bare tariff';
  return null;
}

const cardsPath = process.argv[2];
if (!cardsPath) {
  console.error('usage: build-deck.mjs <cards.json>');
  process.exit(1);
}

const input = JSON.parse(readFileSync(cardsPath, 'utf8'));
const rawCards = Array.isArray(input) ? input : (input.accepted ?? input.cards ?? []);

/* The subject comes from the cards. Mixed input is a mistake, not a feature:
 * one run writes one subject's modules, so a stray card would vanish silently. */
const subjectIds = [...new Set(rawCards.map(c => c.subjectId ?? 'biology'))];
if (subjectIds.length !== 1) {
  console.error(`cards span ${subjectIds.length} subjects (${subjectIds.join(', ')}) — build one subject at a time`);
  process.exit(1);
}
const SUBJECT_ID = subjectIds[0];
const SUBJECT = SUBJECTS[SUBJECT_ID];
if (!SUBJECT) {
  console.error(`unknown subject "${SUBJECT_ID}" — add it to SUBJECTS in this script`);
  process.exit(1);
}

/**
 * Reviewed repairs that must survive regeneration of the authored JSON.
 *
 * Most subjects have accumulated several generations of authoring scripts. A
 * correction made only in a generated TypeScript deck disappears the next time
 * one of those scripts runs; changing a historical parser can, conversely,
 * rewrite hundreds of unrelated cards. This small declarative layer records an
 * independently checked exception at the card boundary: a duplicate can be
 * withdrawn, malformed OCR can be replaced, and official source pages can be
 * attached without obscuring the generator that produced the underlying card.
 */
const CORRECTIONS_PATH = resolve(ROOT, 'scripts/markbank/card-corrections.json');
const CORRECTIONS = existsSync(CORRECTIONS_PATH)
  ? JSON.parse(readFileSync(CORRECTIONS_PATH, 'utf8'))
  : {};
const SOURCE_BINDINGS_PATH = resolve(ROOT, 'scripts/markbank/card-source-bindings.json');
const SOURCE_BINDINGS = existsSync(SOURCE_BINDINGS_PATH)
  ? JSON.parse(readFileSync(SOURCE_BINDINGS_PATH, 'utf8'))
  : {};
const subjectCorrections = CORRECTIONS[SUBJECT_ID] ?? {};
const subjectSourceBindings = SOURCE_BINDINGS[SUBJECT_ID] ?? {};
const rawIds = new Set(rawCards.map(card => card.id));
for (const id of Object.keys(subjectCorrections)) {
  if (!rawIds.has(id)) {
    console.error(`stale correction for missing ${SUBJECT_ID} card "${id}"`);
    process.exit(1);
  }
}
for (const id of Object.keys(subjectSourceBindings)) {
  if (!rawIds.has(id)) {
    console.error(`stale source binding for missing ${SUBJECT_ID} card "${id}"`);
    process.exit(1);
  }
}

const appliedCorrections = [];
const cards = [];
for (const raw of rawCards) {
  const correction = subjectCorrections[raw.id];
  if (correction) {
    if (!String(correction.reason ?? '').trim()) {
      console.error(`${raw.id}: a correction must record why it is safe`);
      process.exit(1);
    }
    if (correction.drop) {
      if (!correction.replacementId || !rawIds.has(correction.replacementId)) {
        console.error(`${raw.id}: a withdrawn card must name an existing replacementId`);
        process.exit(1);
      }
      appliedCorrections.push(`${raw.id}: withdrawn; ${correction.reason}`);
      continue;
    }
  }
  const card = structuredClone(raw);
  for (const [key, value] of Object.entries(correction?.set ?? {})) {
    if (value === null) delete card[key];
    else card[key] = value;
  }
  if (correction?.answerVariantSources) {
    if (!Array.isArray(correction.answerVariantSources)) {
      console.error(`${raw.id}: answerVariantSources must be an array`);
      process.exit(1);
    }
    card.answerVariants = correction.answerVariantSources.map(source => {
      const sourceCard = rawCards.find(candidate => candidate.id === source.cardId);
      if (!sourceCard || !String(source.id ?? '').trim() || !String(source.label ?? '').trim()) {
        console.error(`${raw.id}: invalid answer variant source ${JSON.stringify(source)}`);
        process.exit(1);
      }
      if (sourceCard.year !== raw.year || sourceCard.level !== raw.level
          || sourceCard.questionText !== raw.questionText) {
        console.error(`${raw.id}: answer variant ${source.cardId} is not the same printed task`);
        process.exit(1);
      }
      return { id: source.id, label: source.label, rows: structuredClone(sourceCard.rows) };
    });
  }
  const binding = subjectSourceBindings[raw.id];
  if (binding) {
    const pages = Array.isArray(binding) ? binding : binding.pages;
    const sourceKind = !Array.isArray(binding) && binding.kind === 'text'
      ? 'source-text'
      : 'source-illustration';
    const sourceTitle = sourceKind === 'source-text' ? 'Source and question' : 'Official question page';
    card.sourceMaterial = {
      kind: sourceKind,
      label: sourceKind === 'source-text' ? 'OFFICIAL SOURCE' : 'OFFICIAL QUESTION PAGE',
      title: sourceTitle,
      pages,
      ...(!Array.isArray(binding) && binding.sourceFileid
        ? { sourceFileid: binding.sourceFileid }
        : {}),
      attribution: `SEC ${SUBJECT.title} ${card.year} ${LEVEL_WORD[card.level] ?? 'Higher'} Level examination paper — © State Examinations Commission.`,
      presentationNote: sourceKind === 'source-text'
        ? 'Read the exact source as it appeared in the examination paper, then answer the concise prompt above.'
        : 'Open the exact examination page to use its published chart, table, photograph or diagram.',
    };
    if (!Array.isArray(binding) && binding.stripStem) delete card.stem;
    if (!Array.isArray(binding) && binding.questionText) card.questionText = binding.questionText;
    appliedCorrections.push(`${raw.id}: attached its inspected official question-page source`);
  }
  cards.push(card);
  if (correction) appliedCorrections.push(`${raw.id}: ${correction.reason}`);
}

/**
 * Figures published by bind-figures.mjs: every one was OPENED by an inspecting
 * agent, and only those it marked complete and non-truncated are in here. Its id
 * is the extractor's own name, derived from the figure's page and index in the
 * PDF, so an authoring agent naming a figure cannot invent a path.
 */
const MANIFEST_PATH = resolve(ROOT, 'components/MarkBank/figures.json');
const SUBJECT_MANIFEST_PATH = resolve(
  ROOT, `components/MarkBank/figures-${SUBJECT_ID}.json`);
const MANIFEST = {
  ...(existsSync(MANIFEST_PATH) ? JSON.parse(readFileSync(MANIFEST_PATH, 'utf8')) : {}),
  ...(existsSync(SUBJECT_MANIFEST_PATH)
    ? JSON.parse(readFileSync(SUBJECT_MANIFEST_PATH, 'utf8')) : {}),
};

const figureRecord = (key) => {
  if (SUBJECT.blocked.has(key)) return { error: `figure "${key}" is on the blocklist` };

  const inspected = MANIFEST[key];
  if (inspected) {
    const abs = resolve(ROOT, 'public', inspected.src.replace(/^\//, ''));
    if (!existsSync(abs)) return { error: `figure file missing: ${inspected.src}` };
    const md5 = createHash('md5').update(readFileSync(abs)).digest('hex');
    if (md5 !== inspected.md5) return { error: `figure "${key}" changed on disk since it was inspected` };
    return {
      candId: key,
      src: inspected.src,
      srcHash: md5,
      alt: inspected.alt,
      attribution: inspected.attribution,
      ...(inspected.solution ? { solution: true } : {}),
    };
  }

  // Legacy 2025 Biology Higher Level crops, bound before the manifest existed.
  if (SUBJECT_ID !== 'biology' || !ALT[key]) {
    return { error: `figure "${key}" has not been inspected, so it has no verified alt text` };
  }
  const rel = `${SUBJECT.figureDir}/biology-2025-hl-${key}.png`;
  const abs = resolve(ROOT, rel);
  if (!existsSync(abs)) return { error: `figure file missing: ${rel}` };
  return {
    candId: `biology-2025-hl-${key}`,
    src: `/exam-figures/biology/biology-2025-hl-${key}.png`,
    srcHash: createHash('md5').update(readFileSync(abs)).digest('hex'),
    alt: ALT[key],
    attribution: 'SEC Leaving Certificate Biology 2025 Higher Level — © State Examinations Commission',
  };
};

/**
 * Early Maths question-crop descriptions were hard-cut after 220 characters.
 * Keep their useful verified context, mark the cut honestly with an ellipsis,
 * and append the complete card prompt so assistive technology never receives
 * a sentence ending halfway through a word. New crops are authored without a
 * fixed description limit; this repairs the already-inspected corpus at build.
 */
function accessibleQuestionFigureAlt(alt, card) {
  const repaired = repairText(alt ?? '').trim();
  if (SUBJECT_ID !== 'maths' || repaired.length !== 259) return repaired;
  const context = repaired.replace(/\s+\S*$/, '').trimEnd();
  const prompt = [card.stem, card.questionText]
    .filter(value => typeof value === 'string' && value.trim())
    .join(' ')
    .trim();
  return `${context}… Full card prompt: ${prompt}`;
}

const q = (s) => JSON.stringify(String(s));

/**
 * Whether a card's rows add up to the tariff the paper prints.
 *
 * Mirrors tariffReconciles in types/markBank.ts, including its handling of the
 * double solidus: mutually exclusive routes are counted ONCE and each must reach
 * the tariff alone, because a student takes one route or the other. Checked here
 * so a bad card is DROPPED with a reason rather than failing the whole suite.
 */
function tariffFault(c) {
  const t = c.tariffModel ?? { kind: 'fixed' };
  if (t.kind === 'orderedSplit' || t.kind === 'questionTotal') {
    return c.rows.every(r => r.marks === null || r.marks === undefined)
      ? null : `a ${t.kind} tariff cannot give rows their own marks`;
  }
  if (t.kind === 'bestNofParts') {
    return t.answer * t.perPart === c.totalMarks
      ? null : `best-of tariff ${t.answer}x${t.perPart} does not make ${c.totalMarks}`;
  }
  // Mirrors groupMarks() in types/markBank.ts: a descending tariff pays its
  // steps, not claimMax times one value.
  const worth = (r) => (r.kind === 'anyN' && r.group
    ? (r.group.perOptionSteps
        ? r.group.perOptionSteps.slice(0, r.group.claimMax).reduce((n, m) => n + m, 0)
        : r.group.claimMax * r.group.perOption)
    : (r.marks ?? 0));
  const byRoute = new Map();
  let common = 0;
  for (const r of c.rows) {
    if (!r.route) common += worth(r);
    else byRoute.set(r.route, (byRoute.get(r.route) ?? 0) + worth(r));
  }
  if (!byRoute.size) {
    return common === c.totalMarks ? null : `rows sum to ${common}, tariff is ${c.totalMarks}`;
  }
  const short = [...byRoute.entries()].filter(([, n]) => common + n !== c.totalMarks);
  return short.length
    ? `route ${short.map(([k, n]) => `"${k}" sums to ${common + n}`).join(', ')}, tariff is ${c.totalMarks}`
    : null;
}

/**
 * A tariff sentence standing where a marking point should be: "Any two rights,
 * 5 marks each (3 for the right + 2 for explaining it)".
 *
 * An anyN row's own verbatim is the one string the build does NOT check against
 * the scheme — the options carry the marking points, so the field looks free.
 * Twelve Business cards used it to restate the tariff, which the session never
 * renders, so the split it described reached nobody.
 */
const TARIFF_PROSE = /\bmarks? each\b|^\s*any (one|two|three|four|five|\d+)\b[^.]*\bmarks?\b/i;

/** Faults in a bounded pick-list that arithmetic can settle without an agent. */
function groupFault(c) {
  for (const r of c.rows) {
    if (r.kind !== 'anyN' || !r.group) continue;
    const g = r.group;
    if (g.options.length < g.claimMax) {
      return `row "${r.id}" lets a student claim ${g.claimMax} but lists ${g.options.length} option(s)`;
    }
    // The session prints "Any 2 of these — 7 marks each" from these two numbers,
    // so a group worth more than the question tells the student a false total.
    const groupWorth = g.perOptionSteps
      ? g.perOptionSteps.slice(0, g.claimMax).reduce((n, m) => n + m, 0)
      : g.claimMax * g.perOption;
    if (groupWorth > c.totalMarks) {
      return `row "${r.id}" offers ${groupWorth} marks on a ${c.totalMarks}-mark question`;
    }
    // A descending tariff must state exactly as many steps as it lets a student
    // claim, or the renderer pays the tail of a shorter list to nobody.
    if (g.perOptionSteps && g.perOptionSteps.length !== g.claimMax) {
      return `row "${r.id}" lists ${g.perOptionSteps.length} mark step(s) for ${g.claimMax} claimable option(s)`;
    }
    // Nothing enforced this before: rowCapFor() caps how many ROWS a card has,
    // and a menu's options live inside ONE row, so a group could list any number
    // at all. Ten Business groups had drifted past the cap unnoticed.
    //
    // Refused outright only past the LONG-question ceiling, which is a wall of
    // text on any paper. Between the short cap and that ceiling it is reported
    // instead of dropped: the count was only ever a proxy for reading load, and
    // ten one-word options ("pure", "solid", "soluble") are lighter than eight
    // paragraphs. Losing a working card to a proxy is the worse outcome.
    if (g.options.length > MAX_LONG_OPTION_ROWS) {
      return `row "${r.id}" shows ${g.options.length} options, past the ${MAX_LONG_OPTION_ROWS} any question may show`;
    }
    if (TARIFF_PROSE.test(r.verbatim ?? '')) {
      return `row "${r.id}" states its tariff where its marking point should be: "${r.verbatim}"`;
    }
  }
  return null;
}

function sourceMaterialFault(source, field = 'sourceMaterial') {
  if (!source || typeof source !== 'object') return `${field} is not an object`;
  if (!['source-text', 'source-illustration'].includes(source.kind)) {
    return `${field}.kind must be source-text or source-illustration`;
  }
  for (const key of ['label', 'title', 'attribution', 'presentationNote']) {
    if (!String(source[key] ?? '').trim()) return `${field}.${key} is empty`;
  }
  if (!Array.isArray(source.pages) || !source.pages.length
      || source.pages.some(page => !Number.isInteger(page) || page < 1)) {
    return `${field}.pages must contain one-based positive page numbers`;
  }
  if (new Set(source.pages).size !== source.pages.length) {
    return `${field}.pages repeats a page`;
  }
  return null;
}

function answerVariantsFault(card) {
  if (card.answerVariants === undefined) return null;
  if (!Array.isArray(card.answerVariants) || card.answerVariants.length < 2) {
    return 'answerVariants must contain at least two official routes';
  }
  const ids = new Set();
  for (const variant of card.answerVariants) {
    if (!String(variant?.id ?? '').trim() || !String(variant?.label ?? '').trim()) {
      return 'every answer variant needs a non-empty id and label';
    }
    if (ids.has(variant.id)) return `answer variant id "${variant.id}" appears twice`;
    ids.add(variant.id);
    if (!Array.isArray(variant.rows) || !variant.rows.length) {
      return `answer variant "${variant.id}" has no marking rows`;
    }
    const shadow = { ...card, rows: variant.rows };
    const tariff = tariffFault(shadow);
    if (tariff) return `answer variant "${variant.id}": ${tariff}`;
    const group = groupFault(shadow);
    if (group) return `answer variant "${variant.id}": ${group}`;
    const rowIds = new Set();
    for (const row of variant.rows) {
      if (rowIds.has(row.id)) return `answer variant "${variant.id}" repeats row id "${row.id}"`;
      rowIds.add(row.id);
      if (!ROW_KINDS.has(row.kind)) {
        return `answer variant "${variant.id}" row "${row.id}" has invalid kind "${row.kind}"`;
      }
      if (row.kind !== 'anyN' && isContentFreeRow(row.verbatim)) {
        return `answer variant "${variant.id}" contains content-free row "${row.verbatim}"`;
      }
    }
  }
  return null;
}

/**
 * On a MATCHING card, a label marked "asked" must be one of the answers.
 *
 * LabelKeyPanel deliberately shows only the labels the question leaves alone —
 * repeating one the student is self-marking would give the row away. On a card
 * whose rows ARE the letters ("1. Merger — D"), a letter marked asked but
 * claimed by no row is the distractor the paper warns about, and flagging it
 * asked hides the only decoding of it the student would ever see.
 *
 * Narrow on purpose. Where the question names the label itself — "Identify the
 * structure located at B", answer "Silage (pit)" — the label is genuinely asked
 * and no row repeats it, which is why this only speaks up once some OTHER label
 * has been found in the rows.
 */
function relabelDistractors(c) {
  const keys = Array.isArray(c.labelKey) ? c.labelKey : [];
  if (!keys.length) return null;
  const body = c.rows.map(r => `${r.verbatim ?? ''} ${(r.group?.options ?? []).join(' ')}`).join(' ');
  const claimed = (k) => new RegExp(`(^|[^A-Za-z0-9])${k.letter.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^A-Za-z0-9]|$)`).test(body);
  if (!keys.some(claimed)) return null;   // not a matching card; the letters live in the question
  const orphan = keys.filter(k => k.askedInThisQuestion && !claimed(k));
  if (!orphan.length) return null;
  // Corrected rather than dropped. No row self-marks this letter, so showing it
  // in the panel gives nothing away — and losing the whole card over one flag
  // costs the student far more than the flag ever did.
  for (const k of orphan) k.askedInThisQuestion = false;
  return `${c.id}: ${orphan.map(k => `"${k.letter}"`).join(', ')} claimed by no row — shown in the label key instead of hidden`;
}

/**
 * One card per question.
 *
 * A question first carded without its diagram, then re-carded once a verified
 * figure existed, would otherwise ship twice — and the figureless version is the
 * broken one: "Explain how you know the ventricles are contracting" cannot be
 * answered without seeing which diagram is meant. Where two cards claim the same
 * question, the one carrying a figure wins.
 */
const byQuestion = new Map();
for (const c of cards) {
  const prev = byQuestion.get(c.questionRef);
  if (!prev) { byQuestion.set(c.questionRef, c); continue; }
  const prevHasFigure = Boolean(prev.figureKey);
  const thisHasFigure = Boolean(c.figureKey);
  if (thisHasFigure && !prevHasFigure) byQuestion.set(c.questionRef, c);
}

const out = [];
const dropped = [];
const repaired = [];
const overCap = [];
const seenId = new Set();
const seenHash = new Map();
let unresolvedPapers = 0;

for (const c of cards) {
  if (byQuestion.get(c.questionRef) !== c) {
    dropped.push(`${c.id}: superseded for ${c.questionRef} by a card carrying its figure`);
    continue;
  }
  if (seenId.has(c.id)) { dropped.push(`${c.id}: duplicate id`); continue; }

  // A question-side crop already preserves the SEC's answer lines and page
  // layout exactly. Keep the accessible text prompt, but remove blank-rule
  // scaffolding and page furniture so students do not see a noisy OCR copy
  // above the official crop.
  if (c.questionFigureKey) {
    const originalQuestionText = c.questionText;
    c.questionText = String(c.questionText)
      .replace(/_{3,}/g, '')
      .replace(/\bThis question continues(?: on the next page)?\.?/gi, '')
      .replace(/\bSection B\s+Contexts and Applications\s+150 marks\b/gi, '')
      .replace(/\s+/g, ' ')
      .trim();
    if (c.questionText !== originalQuestionText) {
      repaired.push(`${c.id}: removed duplicated answer-line/page furniture from its question-crop prompt`);
    }
  }

  const contentFree = c.rows.filter(r => r.kind !== 'anyN' && isContentFreeRow(r.verbatim));
  if (contentFree.length) {
    dropped.push(`${c.id}: ${contentFree.length} content-free row(s), e.g. "${contentFree[0].verbatim}"`);
    continue;
  }

  const badQ = badQuestion(c.questionText, c);
  if (badQ) { dropped.push(`${c.id}: ${badQ} — "${c.questionText}"`); continue; }

  const badTariff = tariffFault(c);
  if (badTariff) { dropped.push(`${c.id}: ${badTariff}`); continue; }

  const badGroup = groupFault(c);
  if (badGroup) { dropped.push(`${c.id}: ${badGroup}`); continue; }

  const badVariants = answerVariantsFault(c);
  if (badVariants) { dropped.push(`${c.id}: ${badVariants}`); continue; }

  const sources = [c.sourceMaterial, ...(c.additionalSourceMaterials ?? [])]
    .filter(Boolean);
  /* A source printed in a SEPARATE official document names that document by
   * its Paper Trail label, and the id is resolved here rather than typed by an
   * author -- the same rule paperFileid has followed since a Biology build
   * defaulted it to the marking scheme's id. Spanish needs it: its Higher
   * Section B article is a two-page loose sheet (LC012ALP015EV) and the
   * questions about it are in the question paper, so a card that let
   * sourceFileid default would open the student on the questions and never
   * show them the article. Unresolvable means the card is DROPPED. */
  const unresolvedSource = sources.map((source) => {
    if (!source.sourceLabel) return null;
    const fileid = resolveCompanionFileid(
      corpusSubjectFor(SUBJECT_ID, c.questionRef), c.year ?? 2025,
      c.level ?? 'higher', source.sourceLabel);
    delete source.sourceLabel;
    if (!fileid) return `source document "${source.label}" is not in the Paper Trail index`;
    source.sourceFileid = fileid;
    return null;
  }).find(Boolean);
  if (unresolvedSource) { dropped.push(`${c.id}: ${unresolvedSource}`); continue; }
  const badSource = sources.map((source, index) => sourceMaterialFault(
    source,
    index === 0 ? 'sourceMaterial' : `additionalSourceMaterials[${index - 1}]`,
  )).find(Boolean);
  if (badSource) { dropped.push(`${c.id}: ${badSource}`); continue; }

  const relabelled = relabelDistractors(c);
  if (relabelled) repaired.push(relabelled);

  for (const r of [c.rows, ...(c.answerVariants ?? []).map(variant => variant.rows)].flat()) {
    const cap = optionCapFor(c.section);
    if (r.group && r.group.options.length > cap) {
      overCap.push(`${c.id}: row "${r.id}" shows ${r.group.options.length} options in section ${c.section}, over the ${cap} agreed for a short question`);
    }
  }

  /* A row id repeated inside one card is not cosmetic: rowId() keys the claims
   * map, so two rows sharing an id are one claim to the scorer — ticking either
   * credits both — and React collapses them to a single element. Seen in the
   * wild, so the build refuses it rather than the deck carrying it. */
  const rowIds = new Set();
  const dupeRow = c.rows.map(r => r.id).find(id => rowIds.has(id) || (rowIds.add(id), false));
  if (dupeRow) { dropped.push(`${c.id}: row id "${dupeRow}" appears twice`); continue; }

  // A question naming lettered parts is unanswerable without the figure.
  const invitesDrawing = /you may include a labelled/i.test(c.questionText);
  // CASE-SENSITIVE on the letter. The SEC indexes a diagram with CAPITALS --
  // "structure A", "the part labelled B" -- and those need a key decoding what
  // each points at. A lower-case letter is the thing's own name, not an index:
  // "three circles, labelled p, q, and r" and "the side labelled l" label
  // themselves on the printed diagram and have nothing to decode. The /i flag
  // conflated the two and refused four Maths cards whose crops show the labels.
  const namesLetters = !invitesDrawing
    && /\blabelled [A-Z]\b|\bstructures? [A-Z](,| and )|\bparts? [A-Z](,| and )|\blabelled\s+(parts|structures)\b/.test(c.questionText);
  // Not merely "has a figure": a question about labelled parts needs those
  // labels DECODED, so it must be a full diagram card with a label key.
  if (namesLetters && !(c.figureKey && Array.isArray(c.labelKey) && c.labelKey.length)) {
    dropped.push(`${c.id}: names lettered parts but carries no labelled figure`);
    continue;
  }

  const kindFault = badRowKind(c);
  if (kindFault) { dropped.push(`${c.id}: ${kindFault}`); continue; }

  // Every marking point must actually appear in its own scheme.
  const scheme = schemeFor(SUBJECT_ID, c);
  if (!scheme) { dropped.push(`${c.id}: no scheme on disk for ${c.year} ${c.level}`); continue; }
  const untraceable = [];
  for (const r of [c.rows, ...(c.answerVariants ?? []).map(variant => variant.rows)].flat()) {
    const claims = r.kind === 'anyN' && r.group ? r.group.options : [String(r.verbatim).split(/\s[—-]\s/).pop()];
    for (const claim of claims) {
      if (!claimMatches(scheme, claim)) untraceable.push(claim);
    }
  }
  if (untraceable.length) {
    dropped.push(`${c.id}: ${untraceable.length} marking point(s) not found in the ${c.year} ${c.level} scheme, e.g. "${String(untraceable[0]).slice(0, 60)}"`);
    continue;
  }

  /* Repaired after the provenance check, never before: the check reads the
   * scheme's own text layer, so a card matched against it must still be
   * spelled the way that layer spells things. What ships is the repaired
   * text, which is what the scheme actually PRINTS -- the mangling is the
   * PDF's broken ToUnicode map, not the examiner's writing. */
  repairGlyphs(c);
  const mangled = mangledText(c);
  if (mangled) { dropped.push(`${c.id}: ${mangled}`); continue; }

  let figure = null;
  let labelKey = null;
  if (c.figureKey) {
    const rec = figureRecord(c.figureKey);
    if (rec.error) { dropped.push(`${c.id}: ${rec.error}`); continue; }
    rec.alt = repairText(rec.alt ?? '');
    const figMangled = brokenGlyphs(rec.alt);
    if (figMangled) { dropped.push(`${c.id}: figure alt text — ${figMangled}`); continue; }
    // A lettered figure MUST decode its letters; an unlettered one has nothing
    // to decode and rides on a plain question card instead.
    const lettered = Array.isArray(c.labelKey) && c.labelKey.length > 0;
    const prev = seenHash.get(rec.srcHash);
    if (prev && prev !== c.figureKey) { dropped.push(`${c.id}: crop already bound as "${prev}"`); continue; }
    seenHash.set(rec.srcHash, c.figureKey);
    figure = { ...rec, lettersVisible: lettered ? c.labelKey.map(k => k.letter) : [] };
    labelKey = lettered ? c.labelKey : null;
  }

  /* The QUESTION-side crop: the SEC's own print of the ask and its setup,
   * shown before the reveal. Unlike an answer figure it may legitimately be
   * shared context across sibling cards, so it skips the one-crop-one-card
   * rule; and it must never be a solution crop, which would print the answer
   * in the question area. */
  let questionFigure = null;
  if (c.questionFigureKey) {
    const rec = figureRecord(c.questionFigureKey);
    if (rec.error) { dropped.push(`${c.id}: question figure — ${rec.error}`); continue; }
    if (rec.solution) { dropped.push(`${c.id}: question figure "${c.questionFigureKey}" is a solution crop`); continue; }
    questionFigure = { candId: rec.candId, src: rec.src, srcHash: rec.srcHash,
      alt: accessibleQuestionFigureAlt(rec.alt, c), lettersVisible: [], attribution: rec.attribution };
  }

  seenId.add(c.id);
  const rows = c.rows.map(r => {
    const parts = [`id: ${q(r.id)}`, `kind: ${q(r.kind)}`, `verbatim: ${q(r.verbatim)}`,
      `marks: ${r.marks === null || r.marks === undefined ? 'null' : r.marks}`];
    if (r.accepts?.length) parts.push(`accepts: ${JSON.stringify(r.accepts)}`);
    if (r.contextNote) parts.push(`contextNote: ${q(r.contextNote)}`);
    if (r.openList) parts.push('openList: true');
    if (r.exactTermRequired) parts.push('exactTermRequired: true');
    if (r.route) parts.push(`route: ${q(r.route)}`);
    if (r.dependsOn) parts.push(`dependsOn: ${q(r.dependsOn)}`);
    if (r.group) parts.push(`group: ${JSON.stringify(r.group)}`);
    return `    { ${parts.join(', ')} },`;
  }).join('\n');

  const year = c.year ?? 2025;
  const level = c.level ?? 'higher';
  const levelWord = LEVEL_WORD[level] ?? 'Higher';
  // Mathematics uses A/B as marking-scheme tariff sections, while its two
  // question documents are identified by Paper 1 / Paper 2 in questionRef.
  // Passing A/B to Paper Trail honestly resolves nothing, which previously
  // left every Maths card without its source-paper link despite all ten papers
  // being indexed. Read only the explicit paper number; never guess from a
  // question number or topic.
  const paperSection = SUBJECT_ID === 'maths'
    ? c.questionRef.match(/\bPaper\s+([12])\b/i)?.[1] ?? c.section
    : c.section;
  /* History is examined in two FIELDS OF STUDY, printed as separate papers a
   * candidate chooses between, and Paper Trail indexes them as two subjects.
   * corpusSubjectFor reads the field out of the citation; see paperIndex.mjs. */
  const fileid = resolvePaperFileid(
    corpusSubjectFor(SUBJECT_ID, c.questionRef), year, level, paperSection);
  if (!fileid) unresolvedPapers++;

  out.push({ level, code: `  {
    ...base, kind: ${q(labelKey ? 'diagram' : 'question')},
    year: ${year}, level: ${q(level)},
    paperFileid: ${fileid ? q(fileid) : 'null'},
    schemeCitation: ${q(`Marking points quoted from the SEC marking scheme, ${SUBJECT.title} ${year} ${levelWord} Level — © State Examinations Commission.`)},
    id: ${q(c.id)}, topicId: ${q(c.topicId)}, conceptId: ${q(c.conceptId)},
    section: ${q(c.section)}, questionRef: ${q(c.questionRef)},${c.stem ? `\n    stem: ${q(c.stem)},` : ''}
    questionText: ${q(c.questionText)},
    tariffModel: ${JSON.stringify(c.tariffModel)}, totalMarks: ${c.totalMarks},
    rows: [
${rows}
    ],${c.answerVariants ? `\n    answerVariants: ${JSON.stringify(c.answerVariants, null, 6).replace(/\n/g, '\n    ')},` : ''}${c.sourceMaterial ? `\n    sourceMaterial: ${JSON.stringify(c.sourceMaterial, null, 6).replace(/\n/g, '\n    ')},` : ''}${c.additionalSourceMaterials?.length ? `\n    additionalSourceMaterials: ${JSON.stringify(c.additionalSourceMaterials, null, 6).replace(/\n/g, '\n    ')},` : ''}${questionFigure ? `\n    questionFigure: ${JSON.stringify(questionFigure, null, 6).replace(/\n/g, '\n    ')},` : ''}${figure ? `\n    figure: ${JSON.stringify(figure, null, 6).replace(/\n/g, '\n    ')},` : ''}${labelKey ? `\n    labelKey: ${JSON.stringify(labelKey)},` : ''}
  } as SecCard,` });
}

process.stderr.write(`${SUBJECT.title}: built ${out.length} cards, dropped ${dropped.length}\n`);
/* Every build ends with the paper-anchored ledger, so nobody can ship a deck
 * without the coverage number in front of them — the class of failure where
 * "64 cards" was reported for a subject whose papers print 500 asks. Best
 * effort: a machine without python3 still builds. */
try {
  const { execSync } = await import('node:child_process');
  const led = execSync(
    `python3 ${resolve(ROOT, 'scripts/markbank/authoring/reconcile.py')} ${SUBJECT_ID}`,
    { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  process.stderr.write(`LEDGER ${led.split('\n')[0]}\n`);
} catch (e) {
  const first = String(e.stdout ?? '').split('\n')[0];
  process.stderr.write(first
    ? `LEDGER ${first}\n`
    : 'LEDGER unavailable (python3 missing?) — run reconcile.py by hand\n');
}
for (const d of dropped) process.stderr.write(`  DROPPED ${d}\n`);
for (const c of appliedCorrections) process.stderr.write(`  CORRECTED ${c}\n`);
for (const r of repaired) process.stderr.write(`  REPAIRED ${r}\n`);
for (const o of overCap) process.stderr.write(`  OVER CAP ${o}\n`);
if (unresolvedPapers) {
  process.stderr.write(`  ${unresolvedPapers} card(s) have no paper in the Paper Trail index; paperFileid is null rather than guessed\n`);
}

/**
 * One module per subject and level, not one for the whole deck.
 *
 * A student sits one subject at one level, so shipping everything in a single
 * chunk makes them download decks they will never open — and that cost grows with
 * every authoring wave. Splitting here lets the tool dynamic-import only what is
 * in front of the student.
 */
const OUT_DIR = resolve(ROOT, 'components/MarkBank/cards', SUBJECT_ID);
mkdirSync(OUT_DIR, { recursive: true });

const moduleFor = (level, cards) => `/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Mark Bank — authored ${SUBJECT.title} cards, ${LEVEL_WORD[level] ?? 'Higher'} Level.
 *
 * GENERATED by scripts/markbank/build-deck.mjs. Do not edit by hand.
 *
 * Every question, marking point and mark value is transcribed from the marking
 * scheme for that card's own year and level in examiner-reports/${SUBJECT_ID}/schemes/,
 * and the build drops any card whose content cannot be found there. Figure paths,
 * hashes and SEC paper file ids are resolved from data on disk by the build
 * script — never typed — because both historical figure corruptions in this repo
 * entered through a hand-transcribed path.
 *
 * ${SUBJECT.specNote}
 */

import type { SecCard } from '../../../../types/markBank';
${cards.length ? `
const base = {
  source: 'sec' as const,
  subjectId: ${q(SUBJECT_ID)},
  specVersion: ${q(SUBJECT.specVersion)},
  qa: { gates: ['verbatim', 'tariff', 'figure'], humanReviewedBy: 'agent-verified', humanReviewedAt: '2026-07-31' },
};
` : ''}
export const CARDS: SecCard[] = [
${cards.join('\n')}
];
`;

/* A level gets a module when the subject HAS that level, never as a matter of
 * course: LCVP is examined at one level and writing it an empty higher.ts and
 * ordinary.ts would put two dead decks in the picker. An existing file is
 * always rewritten, so a subject that loses every card at a level still ends
 * up with an honestly empty module rather than a stale one. */
const sizes = {};
for (const level of LEVELS) {
  const levelCards = out.filter(c => c.level === level).map(c => c.code);
  const path = resolve(OUT_DIR, `${level}.ts`);
  if (!levelCards.length && !existsSync(path)) continue;
  writeFileSync(path, moduleFor(level, levelCards));
  sizes[level] = levelCards.length;
  process.stderr.write(`  ${level}: ${levelCards.length} cards -> components/MarkBank/cards/${SUBJECT_ID}/${level}.ts\n`);
}

/**
 * How many cards each deck holds, so the tool can say which decks are ready
 * WITHOUT importing them. Knowing that Chemistry Ordinary is empty is exactly
 * the thing a student needs before they tap it, and finding out by downloading
 * the deck defeats the point of splitting the decks in the first place.
 *
 * Merged rather than overwritten: one run builds one subject, and clobbering the
 * file would erase every other subject's counts.
 */
const MANIFEST_OUT = resolve(ROOT, 'components/MarkBank/cards/sizes.json');
const existing = existsSync(MANIFEST_OUT) ? JSON.parse(readFileSync(MANIFEST_OUT, 'utf8')) : {};
writeFileSync(MANIFEST_OUT, `${JSON.stringify({ ...existing, [SUBJECT_ID]: sizes }, null, 1)}\n`);
