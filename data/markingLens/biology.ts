/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Biology (Leaving Certificate 2025).
 *
 * Sources of truth (filed in /examiner-reports/biology/):
 *  - examiner-reports/biology/2025-hl-marking-scheme.md
 *    (SEC Marking Scheme 2025, Biology Higher Level — main sitting).
 *  - examiner-reports/biology/2025-ol-marking-scheme.md
 *    (SEC Marking Scheme 2025, Biology Ordinary Level — main sitting).
 * Pitfalls cite the Section-A surplus rule and the best-two-options rule as
 * printed verbatim in the filed 2025 HL and OL marking schemes (page-cited).
 *
 * Every notation below is transcribed from those schemes in the SEC `n(m)`
 * points grammar (e.g. "8(3)" = eight correct points, 3 marks each). Each
 * entry's parts sum to the scheme's printed question total (machine-checked).
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly. Biology
 * is filed as two booklets per sitting:
 *  - "Sections A and B" booklet → fileid …LP038… → n 1–10 = scheme Q1–Q10.
 *  - "Section C" booklet        → fileid …LP040… → n 1–7  = scheme Q11–Q17.
 * The IV (Irish) papers are the same exam under the same scheme — mirrored.
 *
 * NOT INCLUDED: 2023. The only 2023 scheme filed here is the *Deferred
 * Examinations* sitting, whose questions differ from the main-sitting paper the
 * 2023 tags key to (main Q1 = carbohydrates; deferred Q1 = fats). With no filed
 * scheme for the tagged main paper, 2023 is skipped rather than mis-mapped.
 */

import { type LensPitfall, type QuestionLens, type SubjectLens } from './types';

const CITE_HL = (q: string) => `SEC Marking Scheme 2025, Biology Higher Level, ${q}`;
const CITE_OL = (q: string) => `SEC Marking Scheme 2025, Biology Ordinary Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[]): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid: e.fileid.replace('EV.pdf', 'IV.pdf') }));

// ── Documented, page-cited pitfalls (question-type matches only) ─────────────

const SURPLUS_HL: LensPitfall = {
  text: 'In Section A a surplus wrong answer cancels a correct one — padding a part with an extra, incorrect item actively loses a mark you had already earned. The scheme’s own worked example: "Chitin, lignin" scores 4 − 4 = 0.',
  cite: 'SEC Marking Scheme 2025, Biology Higher Level, p.4 (Section A surplus rule)',
};
const SURPLUS_OL: LensPitfall = {
  text: 'In Section A a surplus wrong answer cancels a correct one — the scheme’s worked example drops a five-element list to 2(3) when "aluminium" is added ("Carbon, hydrogen, oxygen, calcium, aluminium"). Over-answering is penalised.',
  cite: 'SEC Marking Scheme 2025, Biology Ordinary Level, pp.4–5 (Section A surplus rule)',
};
const BEST2_OL: LensPitfall = {
  text: 'Q16/Q17 are "any two of (a)–(d)", 30 marks each — only your best two sub-parts score, so spreading effort thinly across all four wastes time the best-2 rule will not reward.',
  cite: 'SEC Marking Scheme 2025, Biology Ordinary Level, Q16–Q17 (any two of (a)–(d))',
};

// ════════════════════════════════════════════════════════════════════════════
// HIGHER LEVEL
// ════════════════════════════════════════════════════════════════════════════

const HL_AB = 'LC025ALP038EV.pdf';
const HL_C = 'LC025ALP040EV.pdf';

const hlBase = { year: 2025, level: 'higher' as const, lang: 'ev' as const };

// ── Section A (Q1–Q7, 20 marks each) ────────────────────────────────────────

const HL_SECTION_A: QuestionLens[] = [
  {
    ...hlBase, fileid: HL_AB, n: '1', totalMarks: 20,
    headline: 'Section A short question — best five of six one-line parts, 4 marks each.',
    parts: [
      { part: '(a)–(f)', task: 'Best five of the one-line parts (formula, elements, roles, subunits, vitamins, trace elements)', notation: '5(4)', decoded: 'Any five of the six parts score 4 marks each.', marks: 20 },
    ],
    pitfall: SURPLUS_HL,
    cite: CITE_HL('Q1'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '2', totalMarks: 20,
    headline: 'Section A — each named part earns its mark; the labelled drawing splits into a sketch mark plus label marks.',
    parts: [
      { part: '(a)', task: 'Name structure X and give its function', notation: '3 + 3', decoded: 'Name 3, function 3.', marks: 6 },
      { part: '(b)', task: 'Name tissue Y and give its function', notation: '3 + 3', decoded: 'Name 3, function 3.', marks: 6 },
      { part: '(c)', task: 'Name tissue Z where rapid mitosis occurs', notation: '3', decoded: 'One correct term, 3 marks.', marks: 3 },
      { part: '(d)', task: 'Draw and label a transverse section of the root', notation: '3 + 2(1)', decoded: 'Drawing 3, plus two labels at 1 mark each.', marks: 5 },
    ],
    cite: CITE_HL('Q2'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '3', totalMarks: 20,
    headline: 'Section A — a 2-mark opener then six 3-mark recall answers on respiration.',
    parts: [
      { part: '(a)', task: 'Name the cell organelle shown', notation: '2', decoded: 'One correct term, 2 marks.', marks: 2 },
      { part: '(b)', task: 'Name the cycle in stage 2 of aerobic respiration', notation: '3', decoded: 'One correct term, 3 marks.', marks: 3 },
      { part: '(c)', task: 'What does ATP stand for?', notation: '3', decoded: 'Correct expansion, 3 marks.', marks: 3 },
      { part: '(d)', task: 'Give the function of NAD+', notation: '3', decoded: 'Correct function, 3 marks.', marks: 3 },
      { part: '(e)', task: 'Suggest a condition for anaerobic respiration', notation: '3', decoded: 'Correct condition, 3 marks.', marks: 3 },
      { part: '(f)', task: 'State where anaerobic respiration occurs in the cell', notation: '3', decoded: 'Correct location, 3 marks.', marks: 3 },
      { part: '(g)', task: 'Name one product of anaerobic respiration', notation: '3', decoded: 'Correct product, 3 marks.', marks: 3 },
    ],
    cite: CITE_HL('Q3'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '4', totalMarks: 20,
    headline: 'Section A on the cell membrane — the labelled sketch carries a drawing mark plus 1 mark per named label.',
    parts: [
      { part: '(a)', task: 'Name the parts labelled X and Y', notation: '2 + 2', decoded: 'X 2, Y 2.', marks: 4 },
      { part: '(b)', task: 'Give a function of the cell membrane', notation: '3', decoded: 'Correct function, 3 marks.', marks: 3 },
      { part: '(c)', task: 'Terms for cells without / with membrane-bound organelles', notation: '3 + 3', decoded: 'Prokaryotic 3, eukaryotic 3.', marks: 6 },
      { part: '(d)', task: 'Sketch a plant cell (label membrane + wall); give a cell-wall function', notation: '3 + 1 + 1 + 2', decoded: 'Sketch 3, two labels at 1 each, function 2.', marks: 7 },
    ],
    cite: CITE_HL('Q4'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '5', totalMarks: 20,
    headline: 'Section A on microbial growth — a two-answer part scored 2(3), the rest single 3- and 2-mark answers.',
    parts: [
      { part: '(a)', task: 'Common name for the piece of equipment', notation: '3', decoded: 'One correct term, 3 marks.', marks: 3 },
      { part: '(b)', task: 'Two factors it controls that affect bacterial growth', notation: '2(3)', decoded: 'Any two factors, 3 marks each.', marks: 6 },
      { part: '(c)', task: 'Name stages X and Y on the growth curve', notation: '3 + 3', decoded: 'Stage X 3, stage Y 3.', marks: 6 },
      { part: '(d)', task: 'Which food-processing technique the curve shows', notation: '3', decoded: 'Correct term, 3 marks.', marks: 3 },
      { part: '(e)', task: 'Draw how the line continues if nutrients run out', notation: '2', decoded: 'Correct line, 2 marks.', marks: 2 },
    ],
    pitfall: SURPLUS_HL,
    cite: CITE_HL('Q5'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '6', totalMarks: 20,
    headline: 'Section A on the gut — the labelled villus drawing splits into a drawing mark plus 1 mark per label.',
    parts: [
      { part: '(a)', task: 'Name the parts labelled A and B', notation: '2 + 2', decoded: 'A 2, B 2.', marks: 4 },
      { part: '(b)', task: 'Name and describe how food travels through structure A', notation: '3 + 3', decoded: 'Name 3, description 3.', marks: 6 },
      { part: '(c)', task: 'How the pH of the food changes from A to B', notation: '2', decoded: 'Correct answer, 2 marks.', marks: 2 },
      { part: '(d)', task: 'Name the pancreatic enzyme that digests lipids', notation: '3', decoded: 'Correct enzyme, 3 marks.', marks: 3 },
      { part: '(e)', task: 'Draw and label the internal structure of a villus', notation: '3 + 2(1)', decoded: 'Drawing 3, plus two labels at 1 mark each.', marks: 5 },
    ],
    cite: CITE_HL('Q6'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '7', totalMarks: 20,
    headline: 'Section A on the scientific method — a 2-mark opener, a two-answer 2(3) part, and single 3-mark recalls.',
    parts: [
      { part: '(a)', task: 'A testable statement is known as a ___', notation: '2', decoded: 'Correct term, 2 marks.', marks: 2 },
      { part: '(b)', task: 'How the statement can be tested', notation: '3', decoded: 'Correct answer, 3 marks.', marks: 3 },
      { part: '(c)', task: 'Function of a scientific control', notation: '3', decoded: 'Correct function, 3 marks.', marks: 3 },
      { part: '(d)', task: 'Two limitations of the scientific method', notation: '2(3)', decoded: 'Any two limitations, 3 marks each.', marks: 6 },
      { part: '(e)', task: 'Where a biologist normally publishes results', notation: '3', decoded: 'Correct answer, 3 marks.', marks: 3 },
      { part: '(f)', task: 'What is meant by the term theory', notation: '3', decoded: 'Correct answer, 3 marks.', marks: 3 },
    ],
    cite: CITE_HL('Q7'),
  },
];

// ── Section B (Q8–Q10, 30 marks each) ───────────────────────────────────────

const HL_SECTION_B: QuestionLens[] = [
  {
    ...hlBase, fileid: HL_AB, n: '8', totalMarks: 30,
    headline: 'Section B experiment — a 6-mark opener (2 + 4) then eight 3-mark method/measurement points.',
    parts: [
      { part: '(a)', task: 'Ecosystem term (2) + what aids identifying organisms (4)', notation: '2 + 4', decoded: 'Ecosystem 2, key 4.', marks: 6 },
      { part: '(b)', task: 'Quantitative study of a named plant + two abiotic factors and how each was measured', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q8'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '9', totalMarks: 30,
    headline: 'Section B experiment — a 6-mark osmosis definition (2 + 4) then eight 3-mark practical points.',
    parts: [
      { part: '(a)', task: 'Explain the term osmosis', notation: '2 + 4', decoded: 'Movement of water 2, the full gradient statement 4.', marks: 6 },
      { part: '(b)', task: 'Named tissue/membrane + how the activity was carried out, including the result', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q9'),
  },
  {
    ...hlBase, fileid: HL_AB, n: '10', totalMarks: 30,
    headline: 'Section B experiment — a 6-mark opener (4 + 2) then eight 3-mark set-up/result points.',
    parts: [
      { part: '(a)', task: 'Kingdom of yeast (4) + explain the term sterility (2)', notation: '4 + 2', decoded: 'Fungi 4, sterility 2.', marks: 6 },
      { part: '(b)', task: 'Set-up (with one safety precaution) + result of the leaf-yeast investigation', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q10'),
  },
];

// ── Section C (Q11–Q17, 60 marks each) — n 1–7 in the LP040 booklet ──────────

const HL_SECTION_C: QuestionLens[] = [
  {
    ...hlBase, fileid: HL_C, n: '1', totalMarks: 60,
    headline: 'Section C long question worth 60 — parts (a)/(b)/(c) carry 3, 9 and 8 three-mark points.',
    parts: [
      { part: '(a)', task: 'Geotropism — define, name a part that responds, state the benefit', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Flower reproductive parts, embryo sac, and double-fertilisation parts P and Q', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Seed dispersal, advantages of dispersal and dormancy, asexual examples', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q11'),
  },
  {
    ...hlBase, fileid: HL_C, n: '2', totalMarks: 60,
    headline: 'Section C long question worth 60 — three-mark points split 3 / 9 / 8 across parts (a)/(b)/(c).',
    parts: [
      { part: '(a)', task: 'Mutation — define (3) + two causes', notation: '3 + 2(3)', decoded: 'Definition 3, plus two causes at 3 each.', marks: 9 },
      { part: '(b)', task: 'Gene vs allele; fruit-fly genotypes and offspring cross; linked genes', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'DNA meaning; purines/pyrimidines; DNA vs RNA; four steps of DNA profiling', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q12'),
  },
  {
    ...hlBase, fileid: HL_C, n: '3', totalMarks: 60,
    headline: 'Section C long question worth 60 — three-mark points split 3 / 9 / 8 across parts (a)/(b)/(c).',
    parts: [
      { part: '(a)', task: 'Photosynthesis as anabolic (3) + balanced equation', notation: '3 + 2(3)', decoded: 'Anabolic point 3, plus equation formulae 3 and balancing 3.', marks: 9 },
      { part: '(b)', task: 'Chloroplast; energised particles; the two pathways; products entering and regenerating the stages', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Enzyme nature and shape; where made; denaturation; a method of immobilisation', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q13'),
  },
  {
    ...hlBase, fileid: HL_C, n: '4', totalMarks: 60,
    headline: 'Section C long question worth 60 — part (b) mixes 3-, 1- and 2-mark answers; part (c) mixes 1-, 2- and 3-mark answers.',
    parts: [
      { part: '(a)', task: 'CNS vs PNS + how the nervous system is protected', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Roles in the eye and ear; which eye in low light (justify); a corrective measure', notation: '8(3) + 1(1) + 1(2)', decoded: 'Eight 3-mark points, plus a 1-mark choice and its 2-mark justification.', marks: 27 },
      { part: '(c)', task: 'Motor/sensory neuron (justify each); neurotransmitters; Schwann cell; a disorder cause and treatment', notation: '2(1) + 2(2) + 6(3)', decoded: 'Two 1-mark choices, two 2-mark justifications, six 3-mark points.', marks: 24 },
    ],
    cite: CITE_HL('Q14'),
  },
  {
    ...hlBase, fileid: HL_C, n: '5', totalMarks: 60,
    headline: 'Section C long question worth 60 — part (b) mixes seven 3-mark points with three 2-mark graph points.',
    parts: [
      { part: '(a)', task: 'Explain biosphere, niche and competition', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Predator vs prey; eagle adaptation and human impact; the predator–prey graph and its explanation; why food chains are short', notation: '7(3) + 3(2)', decoded: 'Seven 3-mark points plus three 2-mark graph-explanation points.', marks: 27 },
      { part: '(c)', task: 'Nitrogen-cycle processes; pollution; a named pollutant, its effect and its control', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_HL('Q15'),
  },
  {
    ...hlBase, fileid: HL_C, n: '6', totalMarks: 60,
    headline: 'Section C choice question — answer any two of options (a)–(d), each marked out of 30.',
    parts: [
      { part: '(a)–(d)', task: 'First of your two chosen options', notation: '30', decoded: 'One of the two options you answer from (a)–(d), marked out of 30.', marks: 30 },
      { part: '(a)–(d)', task: 'Second of your two chosen options', notation: '30', decoded: 'The other option you answer from (a)–(d), marked out of 30.', marks: 30 },
    ],
    cite: CITE_HL('Q16'),
  },
  {
    ...hlBase, fileid: HL_C, n: '7', totalMarks: 60,
    headline: 'Section C choice question — answer any two of options (a)–(d), each marked out of 30.',
    parts: [
      { part: '(a)–(d)', task: 'First of your two chosen options', notation: '30', decoded: 'One of the two options you answer from (a)–(d), marked out of 30.', marks: 30 },
      { part: '(a)–(d)', task: 'Second of your two chosen options', notation: '30', decoded: 'The other option you answer from (a)–(d), marked out of 30.', marks: 30 },
    ],
    cite: CITE_HL('Q17'),
  },
];

// ════════════════════════════════════════════════════════════════════════════
// ORDINARY LEVEL
// ════════════════════════════════════════════════════════════════════════════

const OL_AB = 'LC025GLP038EV.pdf';
const OL_C = 'LC025GLP040EV.pdf';

const olBase = { year: 2025, level: 'ordinary' as const, lang: 'ev' as const };

// ── Section A (Q1–Q7, 20 marks each) — each scored off a correct-count grid ──

const OL_SECTION_A: QuestionLens[] = [
  {
    ...olBase, fileid: OL_AB, n: '1', totalMarks: 20,
    headline: 'Section A — five one-line parts, 4 marks each, off a correct-count grid.',
    parts: [
      { part: '(a)–(e)', task: 'Five one-line parts (energy biomolecule, formula, triglyceride, water- and fat-soluble vitamins)', notation: '5(4)', decoded: 'Each of the five parts scores 4 marks (grid: 4/8/12/16/20).', marks: 20 },
    ],
    pitfall: SURPLUS_OL,
    cite: CITE_OL('Q1'),
  },
  {
    ...olBase, fileid: OL_AB, n: '2', totalMarks: 20,
    headline: 'Section A — match five ecology terms to descriptions, 4 marks each.',
    parts: [
      { part: '(a)–(e)', task: 'Match five terms (biosphere, ecosystem, conservation, habitat, pollution) to descriptions', notation: '5(4)', decoded: 'Each correct match scores 4 marks (grid: 4/8/12/16/20).', marks: 20 },
    ],
    pitfall: SURPLUS_OL,
    cite: CITE_OL('Q2'),
  },
  {
    ...olBase, fileid: OL_AB, n: '3', totalMarks: 20,
    headline: 'Section A — seven true/false statements scored on a 3-marks-per-correct grid.',
    parts: [
      { part: '(a)–(g)', task: 'Seven true/false statements', notation: '6(3) + 2', decoded: 'Six correct score 3 marks each; a seventh adds 2 (grid: 3/6/9/12/15/18/20).', marks: 20 },
    ],
    cite: CITE_OL('Q3'),
  },
  {
    ...olBase, fileid: OL_AB, n: '4', totalMarks: 20,
    headline: 'Section A on cells — identify, give reasons, and match components/functions off a grid.',
    parts: [
      { part: '(a)–(c)', task: 'Plant or animal cell + reasons; match cell components and functions to letters', notation: '6(3) + 2', decoded: 'Six correct answers at 3 marks; the seventh adds 2 (grid to 20).', marks: 20 },
    ],
    cite: CITE_OL('Q4'),
  },
  {
    ...olBase, fileid: OL_AB, n: '5', totalMarks: 20,
    headline: 'Section A on tropisms — match and short recall scored off a 3-per-correct grid.',
    parts: [
      { part: '(a)–(d)', task: 'Match tropisms to diagrams; importance; auxin transport; a commercial use of growth regulators', notation: '6(3) + 2', decoded: 'Six correct answers at 3 marks; the seventh adds 2 (grid to 20).', marks: 20 },
    ],
    cite: CITE_OL('Q5'),
  },
  {
    ...olBase, fileid: OL_AB, n: '6', totalMarks: 20,
    headline: 'Section A on nervous/endocrine systems — fill-the-blanks and eye recall off a grid.',
    parts: [
      { part: '(a)–(c)', task: 'Complete the endocrine/nervous passages; complete the CNS sentence; name eye parts by function', notation: '6(3) + 2', decoded: 'Six correct answers at 3 marks; the seventh adds 2 (grid to 20).', marks: 20 },
    ],
    cite: CITE_OL('Q6'),
  },
  {
    ...olBase, fileid: OL_AB, n: '7', totalMarks: 20,
    headline: 'Section A on mitosis — sequence-ordering (up to 6) plus short recall off a grid.',
    parts: [
      { part: '(a)–(e)', task: 'Order the mitosis sequence; name organelle X; spindle fibres; meiosis vs mitosis; uncontrolled division', notation: '6(3) + 2', decoded: 'Six correct answers at 3 marks; the seventh adds 2 (grid to 20). The ordering part earns 3 for any two correctly placed, 6 if fully correct.', marks: 20 },
    ],
    cite: CITE_OL('Q7'),
  },
];

// ── Section B (Q8–Q10, 30 marks each) ───────────────────────────────────────

const OL_SECTION_B: QuestionLens[] = [
  {
    ...olBase, fileid: OL_AB, n: '8', totalMarks: 30,
    headline: 'Section B experiment — a 6-mark recall opener (2 correct points) then eight 3-mark practical points.',
    parts: [
      { part: '(a)', task: 'Two one-line recall items (an element unique to protein; smallest carbohydrate unit)', notation: '2(3)', decoded: 'Two correct points, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Food tests for starch, reducing sugar, protein and lipid — reagent + observation each', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q8'),
  },
  {
    ...olBase, fileid: OL_AB, n: '9', totalMarks: 30,
    headline: 'Section B experiment — a 6-mark recall opener then eight 3-mark enzyme-activity points.',
    parts: [
      { part: '(a)', task: 'Two one-line recall items (biomolecule of enzymes; a factor other than pH)', notation: '2(3)', decoded: 'Two correct points, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Enzyme, substrate, varying pH, controlled factor and how kept constant, safety, axis labels', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q9'),
  },
  {
    ...olBase, fileid: OL_AB, n: '10', totalMarks: 30,
    headline: 'Section B experiment — a 6-mark recall opener then eight 3-mark germination points.',
    parts: [
      { part: '(a)', task: 'Two one-line recall items (period of inactivity; seed store of food)', notation: '2(3)', decoded: 'Two correct points, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'The germination investigation — control and justification, gas removed, factors, reliability', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q10'),
  },
];

// ── Section C (Q11–Q17, 60 marks each) — n 1–7 in the GLP040 booklet ─────────

const OL_SECTION_C: QuestionLens[] = [
  {
    ...olBase, fileid: OL_C, n: '1', totalMarks: 60,
    headline: 'Section C long question worth 60 — parts (a)/(b)/(c) carry 3, 9 and 8 three-mark points.',
    parts: [
      { part: '(a)', task: 'Energy source of ecosystems; why food chains are short; interconnected food chains', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Lesser horseshoe bat — adaptation, habitat, niche, protection, and a three-level food chain', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Nitrogen and carbon cycles — name each cycle and match the labelled processes', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q11'),
  },
  {
    ...olBase, fileid: OL_C, n: '2', totalMarks: 60,
    headline: 'Section C long question worth 60 — three-mark points split 3 / 9 / 8 across parts (a)/(b)/(c).',
    parts: [
      { part: '(a)', task: 'Match genotype/phenotype; chromosomes are DNA and ___', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Allele/recessive; tall and short genotypes; justify possible tall/short outcomes', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Transcription/replication/translation; DNA shape; an RNA base; uses of profiling and engineering', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q12'),
  },
  {
    ...olBase, fileid: OL_C, n: '3', totalMarks: 60,
    headline: 'Section C long question worth 60 — three-mark points split 3 / 9 / 8 across parts (a)/(b)/(c).',
    parts: [
      { part: '(a)', task: 'Metabolism; match photosynthesis/respiration to organelles', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Photosynthesis — pigment, gas, water source, oxygen outcomes, anabolic (justify), applications', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Respiration — muscle energy, stage-1 location, stage matching, anaerobic situation, fermentation', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q13'),
  },
  {
    ...olBase, fileid: OL_C, n: '4', totalMarks: 60,
    headline: 'Section C long question worth 60 — three-mark points split 3 / 9 / 8 across parts (a)/(b)/(c).',
    parts: [
      { part: '(a)', task: 'Root and shoot systems and a function for each', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Root transverse section; monocot/dicot (justify); match tissues; vascular tissue; xylem/phloem function', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Sexual vs asexual seed formation; dispersal types; vegetative propagation', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q14'),
  },
  {
    ...olBase, fileid: OL_C, n: '5', totalMarks: 60,
    headline: 'Section C long question worth 60 — three-mark points split 3 / 9 / 8 across parts (a)/(b)/(c).',
    parts: [
      { part: '(a)', task: 'Male hormone; hormones that build and maintain the endometrium', notation: '3(3)', decoded: 'Three correct points, 3 marks each.', marks: 9 },
      { part: '(b)', task: 'Menstruation, ovulation, fertilisation site, infertility and treatment, placenta/foetus, lactation', notation: '9(3)', decoded: 'Nine correct points, 3 marks each.', marks: 27 },
      { part: '(c)', task: 'Male reproductive parts, sperm production, contraception, and a labelled sperm-cell sketch', notation: '8(3)', decoded: 'Eight correct points, 3 marks each.', marks: 24 },
    ],
    cite: CITE_OL('Q15'),
  },
  {
    ...olBase, fileid: OL_C, n: '6', totalMarks: 60,
    headline: 'Section C choice question — answer any two of (a)–(d); each option is ten 3-mark points.',
    parts: [
      { part: '(a)–(d)', task: 'First of your two chosen options — ten 3-mark points', notation: '10(3)', decoded: 'Each option scores as ten correct points at 3 marks (grid to 30).', marks: 30 },
      { part: '(a)–(d)', task: 'Second of your two chosen options — ten 3-mark points', notation: '10(3)', decoded: 'Each option scores as ten correct points at 3 marks (grid to 30).', marks: 30 },
    ],
    pitfall: BEST2_OL,
    cite: CITE_OL('Q16'),
  },
  {
    ...olBase, fileid: OL_C, n: '7', totalMarks: 60,
    headline: 'Section C choice question — answer any two of (a)–(d); each option is ten 3-mark points.',
    parts: [
      { part: '(a)–(d)', task: 'First of your two chosen options — ten 3-mark points', notation: '10(3)', decoded: 'Each option scores as ten correct points at 3 marks (grid to 30).', marks: 30 },
      { part: '(a)–(d)', task: 'Second of your two chosen options — ten 3-mark points', notation: '10(3)', decoded: 'Each option scores as ten correct points at 3 marks (grid to 30).', marks: 30 },
    ],
    pitfall: BEST2_OL,
    cite: CITE_OL('Q17'),
  },
];

// ── Assembly ────────────────────────────────────────────────────────────────

const HL_EV: QuestionLens[] = [...HL_SECTION_A, ...HL_SECTION_B, ...HL_SECTION_C];
const OL_EV: QuestionLens[] = [...OL_SECTION_A, ...OL_SECTION_B, ...OL_SECTION_C];

const BIOLOGY_LENS: SubjectLens = {
  subjectId: 'biology',
  entries: [
    ...HL_EV, ...mirrorIV(HL_EV),
    ...OL_EV, ...mirrorIV(OL_EV),
  ],
};

export default BIOLOGY_LENS;
