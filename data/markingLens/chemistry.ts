/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Chemistry.
 *
 * Sources of truth:
 *  - examiner-reports/chemistry/2024-marking-scheme.md
 *    (SEC Marking Scheme 2024, Chemistry Higher Level)
 *  - examiner-reports/chemistry/2025-marking-scheme.md
 *    (SEC Marking Scheme 2025, Chemistry Higher Level)
 * Every notation below is verbatim from those documents (the scheme prints a
 * bracketed mark after each markable element, e.g. "(3)", or a compound
 * bracket such as "(6 × 1)", "(4 + 2)", "(5 + 2 + 2)"); every entry's parts
 * sum to 50, the per-question total (machine-checked). Pitfalls cite the
 * Chief Examiner's Report 2013 (Chemistry) — the behaviours surfaced with
 * page refs in examiner-reports/chemistry/2024-insights.md.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2024 HL (LC022ALP000EV + IV mirror) Q1–9 — 50m each.
 *  - 2025 HL (LC022ALP000EV + IV mirror) Q1–9 — 50m each.
 * Q10 and Q11 (both years) are the option questions: each lettered part's
 * scheme marks sum to 25 and candidates answer two parts, but the
 * "answer any two parts" rubric is printed on the exam paper, not in the
 * filed scheme — so an honest 50-mark ladder cannot be built from the scheme
 * alone and those questions are deliberately omitted.
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE24 = (q: string) => `SEC Marking Scheme 2024, Chemistry Higher Level, ${q}`;
const CITE25 = (q: string) => `SEC Marking Scheme 2025, Chemistry Higher Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

// ── 2024 Higher Level (Q1–9; Q10/Q11 omitted — see header) ──────────────────

const ENTRIES_2024: QuestionLens[] = [
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '1',
    totalMarks: 50,
    headline: 'Vinegar titration: procedure elements at 3 marks each; the four calculation steps carry 4, 4, 2+2 and 2+3.',
    parts: [
      { part: '(a)(i)', task: 'Name the apparatus used to measure the 10.0 cm³ portion', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(ii)', task: 'Describe how this apparatus was rinsed before use', notation: '(3) + (3)', decoded: 'Two elements (with deionised water; with vinegar), 3 marks each.', marks: 6 },
      { part: '(a)(iii)', task: 'Describe a method to dilute the 10.0 cm³ portion to exactly 50.0 cm³', notation: '(3) + (3)', decoded: 'Two elements (vinegar into volumetric flask; to the mark with deionised water), 3 marks each.', marks: 6 },
      { part: '(b)(i)', task: 'Calculate the volume of undiluted vinegar needed to neutralise 25.0 cm³ of the NaOH', notation: '(3) + (3)', decoded: 'Two elements: reference to a factor of 5 (3m), then the result (3m).', marks: 6 },
      { part: '(b)(ii)', task: 'Outline an advantage of diluting the vinegar before titrating', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'Name a suitable indicator', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(ii)', task: 'State the colour change at the end point', notation: '(3) + (3)', decoded: 'Each colour carries 3 marks; the scheme adds "[award 3 marks for both correct colours reversed]".', marks: 6 },
      { part: '(d)(i)', task: 'Calculate the moles of NaOH in each 25.0 cm³ portion', notation: '(4)', decoded: 'The calculation carries 4 marks.', marks: 4 },
      { part: '(d)(ii)', task: 'Calculate the moles of ethanoic acid in each cm³ of diluted vinegar', notation: '(4)', decoded: 'The calculation carries 4 marks.', marks: 4 },
      { part: '(d)(iii)', task: 'Calculate the concentration of ethanoic acid in the original vinegar (mol/L)', notation: '(2) + (2)', decoded: 'Two calculation steps (×1000; ×5 to the result), 2 marks each.', marks: 4 },
      { part: '(d)(iv)', task: 'Calculate the concentration in % (w/v)', notation: '(2) + (3)', decoded: 'Mr = 60 earns 2 marks; the final percentage earns 3.', marks: 5 },
    ],
    pitfall: {
      text: 'Incorrect terminology loses marks — the 2013 Chief Examiner\'s Report flags "the use of \'clear\' instead of \'colourless\', \'lower meniscus\' instead of \'bottom of the meniscus\'" as mark-losing, and this scheme prints "do not accept clear" at exactly this end point.',
      cite: "Chief Examiner's Report 2013 (Chemistry), p.24",
    },
    cite: CITE24('Q1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '2',
    totalMarks: 50,
    headline: 'Three lab exercises: recrystallisation elements at 4/3 marks, then ethanal oxidation and soap preparation at 3 marks per element.',
    parts: [
      { part: '(a)(i)', task: 'Explain why water is a suitable recrystallisation solvent', notation: '(4)', decoded: 'One markable element — 4 marks.', marks: 4 },
      { part: '(a)(ii)', task: 'Explain the purpose of the first (hot) filtration', notation: '(4)', decoded: 'One markable element — 4 marks.', marks: 4 },
      { part: '(a)(iii)', task: 'Explain why fluted paper in a warm funnel suits hot filtration', notation: '(4)', decoded: 'One markable element — 4 marks.', marks: 4 },
      { part: '(a)(iv)', task: 'Explain why the second filtration follows a period of cooling', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(v)', task: 'What observation shows the recrystallised benzoic acid was pure?', notation: '(3) + (2)', decoded: 'Melting point earns 3 marks; its narrow range/sharpness earns 2.', marks: 5 },
      { part: '(b)(i)', task: 'Identify the reagent(s) to show ethanal is easily oxidised', notation: '(3)', decoded: 'One reagent route earns 3 marks — the // alternatives (acidified KMnO₄ // Fehling’s // Tollen’s) are mutually exclusive.', marks: 3 },
      { part: '(b)(ii)', task: 'State the colour change for the identified reagent(s)', notation: '(3) + (3)', decoded: 'Start and end colours earn 3 marks each, locked to the chosen // route; "[award 3 marks for both correct colours reversed]".', marks: 6 },
      { part: '(b)(iii)', task: 'Identify the organic product of the test', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(iv)', task: 'Write a half equation for the reduction of the inorganic reagent', notation: '(3)', decoded: 'The half equation earns 3 marks, locked to the chosen // route.', marks: 3 },
      { part: '(c)(i)', task: 'Identify the reactants used to prepare soap', notation: '(3) + (3)', decoded: 'Two elements (fat/oil; sodium/potassium hydroxide), 3 marks each.', marks: 6 },
      { part: '(c)(ii)', task: 'Identify the solvent used', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(iii)', task: 'Name the co-product and draw its structure', notation: '(3) + (3)', decoded: 'The name earns 3 marks and the drawn structure earns 3.', marks: 6 },
    ],
    cite: CITE24('Q2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '3',
    totalMarks: 50,
    headline: 'Thiosulfate rate experiment: the graph alone carries 11 marks (axes 3, points 6, line 2).',
    parts: [
      { part: '(a)(i)', task: 'Describe a method to know when the same mass of sulfur precipitated', notation: '(3) + (3)', decoded: 'Two elements (the arrangement; the endpoint criterion), 3 marks each — // routes are mutually exclusive.', marks: 6 },
      { part: '(a)(ii)', task: 'Describe preparing 100 cm³ of 0.09 M from 0.10 M solution', notation: '(3) + (3)', decoded: 'Two elements (90 cm³ of solution; made up with water), 3 marks each.', marks: 6 },
      { part: '(b)(i)', task: 'Complete the six missing rate values', notation: '(6 × 1)', decoded: 'Six values, 1 mark each.', marks: 6 },
      { part: '(b)(ii)', task: 'Draw the rate vs concentration graph', notation: '(3) + (6) + (2)', decoded: 'Axes labelled 3m; points plotted 6m ("[–1 for each incorrectly plotted point]", max 3 if not on graph paper); line of best fit 2m.', marks: 11 },
      { part: '(b)(iii)', task: 'What can be concluded from the graph?', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'Estimate the rate for 0.015 M solution from the graph', notation: '(4)', decoded: 'The estimate carries 4 marks.', marks: 4 },
      { part: '(c)(ii)', task: 'Calculate the time for sulfur to precipitate in that case', notation: '(4)', decoded: 'The calculation carries 4 marks.', marks: 4 },
      { part: '(d)(i)', task: 'Describe heating the reactants and measuring the temperature', notation: '(3) + (3)', decoded: 'Two elements (heat source; thermometer), 3 marks each.', marks: 6 },
      { part: '(d)(ii)', task: 'Which temperature was highest? Justify', notation: '(2) + (2)', decoded: 'The choice earns 2 marks; the justification earns 2.', marks: 4 },
    ],
    cite: CITE24('Q3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '4',
    totalMarks: 50,
    headline: 'Twelve short items (a)–(l); eight are answered at 6 marks each, with a 1-mark bonus on each of the first two attempted.',
    parts: [
      { part: '(a)–(l)', task: 'Any eight of the twelve short items', notation: 'Six marks to be allocated to each item', decoded: 'Eight items at 6 marks each (48). Within an item the 6 splits as printed — e.g. (4 + 2) for two elements, or (3 + 2 + 1) for an "[any three]" list.', marks: 48 },
      { part: '', task: 'The first two items attempted', notation: 'one additional mark to be added to each of the first two items attempted', decoded: 'A 1-mark bonus on each of the first two items attempted (2).', marks: 2 },
    ],
    cite: CITE24('Q4'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '5',
    totalMarks: 50,
    headline: 'Atomic theory: mostly paired 3-mark elements, two single 6-mark awards, and a 2-mark ionisation-energy element.',
    parts: [
      { part: '(a)(i)', task: 'Explain the term energy level', notation: '(3) + (3)', decoded: 'Two elements (fixed/quantised energy; of an electron), 3 marks each.', marks: 6 },
      { part: '(a)(ii)', task: 'Distinguish ground state from excited states', notation: '(6)', decoded: 'A single 6-mark award for the contrast — the // sides are mutually exclusive.', marks: 6 },
      { part: '(a)(iii)', task: 'Explain what happens when an electron moves from excited state to ground state', notation: '(3) + (3)', decoded: 'Two elements (energy released; as a photon/at a specific frequency), 3 marks each.', marks: 6 },
      { part: '(a)(iv)', task: 'Name the instrument used to examine a line spectrum', notation: '(3)', decoded: 'One element — 3 marks; "[do not accept mass spectrometer]".', marks: 3 },
      { part: '(b)(i)', task: 'Explain the Heisenberg uncertainty principle for an electron', notation: '(3) + (3)', decoded: 'Two elements (pairs of properties not both measurable; at the same time), 3 marks each.', marks: 6 },
      { part: '(b)(ii)', task: 'Write the full s, p configuration of neon per orbital', notation: '(3) + (3)', decoded: 'Two elements (1s² 2s²; 2px² 2py² 2pz²), 3 marks each.', marks: 6 },
      { part: '(b)(iii)', task: 'Distinguish an energy sublevel from an atomic orbital (via neon)', notation: '(3) + (3)', decoded: 'Each side of the distinction earns 3 marks; the // alternatives within each are mutually exclusive.', marks: 6 },
      { part: '(b)(iv)', task: 'Explain neon’s unreactivity from its configuration', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(v)', task: 'Explain how neon’s successive ionisation energies evidence energy levels', notation: '(2)', decoded: 'One markable element — 2 marks.', marks: 2 },
      { part: '(b)(vi)', task: 'Draw the shape of a p orbital', notation: '(6)', decoded: 'The correct dumb-bell shape earns 6 marks; "[award 3 marks for drawing that shows overlapping dumb-bell shapes]".', marks: 6 },
    ],
    cite: CITE24('Q5'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '6',
    totalMarks: 50,
    headline: 'Oil refining and thermochemistry: the isomer part carries 15 (names 3 × 2, structures 3 × 3) and the Hess-law calculation 11.',
    parts: [
      { part: '(a)(i)', task: 'Describe one property compound A shares with its naphtha fraction', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(ii)', task: 'State the IUPAC names of compounds A and B', notation: '(3 + 3)', decoded: 'Each name earns 3 marks.', marks: 6 },
      { part: '(a)(iii)', task: 'Explain why A and B are saturated alkanes', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(i)', task: 'Name the process converting A to B', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(ii)', task: 'Why is this conversion carried out?', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'Draw the structure of methylpropane', notation: '(3)', decoded: 'The drawn structure earns 3 marks.', marks: 3 },
      { part: '(c)(ii)', task: 'Name and draw three isomers of compound C', notation: '(3 × 2) + (3 × 3)', decoded: 'Three names at 2 marks each, then three drawn structures at 3 marks each.', marks: 15 },
      { part: '(d)(i)', task: 'Calculate the heat of combustion of compound A', notation: '(2 [multiplicative factor] + 1 [sign]) + (2 [multiplicative factor] + 1 [sign]) + (2 [multiplicative factor] + 1 [sign]) + (2)', decoded: 'Each of the three heat-of-formation terms earns 2 marks for its multiplicative factor and 1 for its sign; the final answer earns 2.', marks: 11 },
      { part: '(d)(ii)', task: 'Calculate the heat of reaction for converting A to B', notation: '(3)', decoded: 'The calculation carries 3 marks.', marks: 3 },
    ],
    cite: CITE24('Q6'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '7',
    totalMarks: 50,
    headline: 'Equilibrium: the Kc expression is a single 6-mark award, the ICE-table calculation carries 12, and each state-and-justify part splits 3 + 2.',
    parts: [
      { part: '(a)(i)', task: 'Explain chemical equilibrium', notation: '(3) + (2)', decoded: 'Two elements at 3 and 2 marks — the // sides are mutually exclusive.', marks: 5 },
      { part: '(a)(ii)', task: 'Write the Kc expression', notation: '(6)', decoded: 'The expression earns 6 marks; "[award 3 marks if round brackets are used]".', marks: 6 },
      { part: '(a)(iii)', task: 'Calculate Kc given 0.8 moles of H₂ at equilibrium', notation: '(3 × 2) + (3)', decoded: 'The three equilibrium concentrations earn 2 marks each; the evaluated Kc earns 3.', marks: 9 },
      { part: '(b)(i)', task: 'Explain why Kc would not change for the new mixture', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(ii)', task: 'Calculate the mass of CO₂ at equilibrium in case (b)(i)', notation: '(3) + (3) + (2) + (2) + (2)', decoded: 'Five steps: equilibrium table 3m; the Kc equation in x 3m; x = 1.25 2m; Mr = 44 2m; mass 2m.', marks: 12 },
      { part: '(c)(i)', task: 'Effect of decreasing pressure on % conversion — justify', notation: '(3) + (2)', decoded: 'The call ("no effect") earns 3 marks; the justification earns 2.', marks: 5 },
      { part: '(c)(ii)', task: 'How could Kc be increased? Justify', notation: '(3) + (2)', decoded: 'The change earns 3 marks; the justification earns 2.', marks: 5 },
      { part: '(c)(iii)', task: 'Effect of a catalyst on Kc — justify', notation: '(3) + (2)', decoded: 'The call ("no effect") earns 3 marks; the justification earns 2.', marks: 5 },
    ],
    cite: CITE24('Q7'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '8',
    totalMarks: 50,
    headline: 'Organic mechanisms and PVC: the free-radical mechanism carries 12 (four steps at 3 each); structures pair 3 + 3 with their marked bonds.',
    parts: [
      { part: '(a)', task: 'How does the carbon geometry change during reaction A?', notation: '(3) + (2)', decoded: 'The starting geometry earns 3 marks; the final geometry earns 2.', marks: 5 },
      { part: '(b)(i)', task: 'Classify reaction B (addition/substitution/elimination)', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(ii)', task: 'Describe the mechanism for reaction B', notation: '(3) + (3) + (3) + (3)', decoded: 'Four steps (initiation, two propagations, termination), 3 marks each.', marks: 12 },
      { part: '(b)(iii)', task: 'Explain how trace C₄H₁₀ evidences the mechanism', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(iv)', task: 'State one other piece of evidence for the mechanism', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'State the IUPAC name of compound X', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(ii)', task: 'Name the inorganic compound eliminated (X → Y)', notation: '(3)', decoded: 'One element — 3 marks; "[do not accept HCl or hydrochloric acid]".', marks: 3 },
      { part: '(c)(iii)', task: 'Draw X and indicate the bonds broken in the elimination', notation: '(3) + (3)', decoded: 'The structure earns 3 marks; indicating the broken C–Cl and C–H bonds earns 3.', marks: 6 },
      { part: '(c)(iv)', task: 'Draw Y and indicate the bond formed in the elimination', notation: '(3) + (3)', decoded: 'The structure earns 3 marks; indicating the C=C bond formed earns 3.', marks: 6 },
      { part: '(c)(v)', task: 'Draw two repeating units of PVC', notation: '(6)', decoded: 'The drawing earns 6 marks; "[award 3 marks two repeating units consistent with answer in part (iv)]".', marks: 6 },
    ],
    pitfall: {
      text: 'The Chief Examiner reports that "organic reaction mechanisms continue to be poorly answered" at Higher Level — the mechanism steps here carry 12 marks, the biggest single block in the question.',
      cite: "Chief Examiner's Report 2013 (Chemistry), p.23",
    },
    cite: CITE24('Q8'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '9',
    totalMarks: 50,
    headline: 'Acids and bases: 3-mark elements throughout, a 4 + 4 indicator part, and a combined 5 + 2 + 2 bracket on the titration-curve part.',
    parts: [
      { part: '(a)(i)', task: 'Why is NH₃ a Brønsted-Lowry base but not an Arrhenius base?', notation: '(3) + (3)', decoded: 'Two elements (proton acceptor; does not dissociate to give OH⁻), 3 marks each.', marks: 6 },
      { part: '(a)(ii)', task: 'Identify the conjugate acid of NH₃', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(iii)', task: 'Identify the conjugate base of NH₃', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(i)', task: 'Define pH', notation: '(3) + (3)', decoded: 'Two elements (–log₁₀; [H⁺]), 3 marks each.', marks: 6 },
      { part: '(b)(ii)', task: 'Explain why pure water’s pH is not 7 at 50 °C', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(iii)', task: 'State the pH change on diluting the strong acid ×10', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(iv)', task: 'Calculate the concentration of weak acid Y from Ka and pH', notation: '(3) + (3) + (3)', decoded: 'Three calculation steps, 3 marks each.', marks: 9 },
      { part: '(c)', task: 'Colour change of indicator HIn in 0.1 M KOH — justify', notation: '(4) + (4)', decoded: 'The colour call earns 4 marks; the justification earns 4.', marks: 8 },
      { part: '(d)', task: '(i) Evidence acid Z is strong; (ii) when the indicator changes colour — justify', notation: '(5 + 2 + 2)', decoded: 'Nine marks across (d)(i) and (d)(ii): the three printed answer elements are marked 5, 2 and 2.', marks: 9 },
    ],
    cite: CITE24('Q9'),
  },
];

// ── 2025 Higher Level (Q1–9; Q10/Q11 omitted — see header) ──────────────────

const ENTRIES_2025: QuestionLens[] = [
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '1',
    totalMarks: 50,
    headline: 'Iron-tablet KMnO₄ titration: procedure elements at 3 marks; the calculation chain runs 3, 2+2, 2+2 and a final 4.',
    parts: [
      { part: '(a)', task: 'Identify a primary standard for standardising KMnO₄', notation: '(5)', decoded: 'One markable element — 5 marks.', marks: 5 },
      { part: '(b)(i)', task: 'Outline bringing the volumetric-flask solution precisely to the mark', notation: '(3) + (3)', decoded: 'Two elements (drop by drop; bottom of meniscus on the mark), 3 marks each.', marks: 6 },
      { part: '(b)(ii)', task: 'Explain why using more than one tablet increases accuracy', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'Name the apparatus used to measure the 25.0 cm³ portion', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(ii)', task: 'Describe how it was rinsed before use', notation: '(3) + (3)', decoded: 'Two elements (with deionised water; with the iron(II) solution), 3 marks each.', marks: 6 },
      { part: '(d)(i)', task: 'Explain why no added indicator was required', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(d)(ii)', task: 'Describe the end-point observation', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(d)(iii)', task: 'What is observed if insufficient acid is present? Explain', notation: '(3) + (3)', decoded: 'The observation earns 3 marks; the explanation earns 3.', marks: 6 },
      { part: '(e)(i)', task: 'Calculate moles of MnO₄⁻ in 22.5 cm³ of 0.010 M solution', notation: '(3)', decoded: 'The calculation carries 3 marks.', marks: 3 },
      { part: '(e)(ii)', task: 'Calculate moles of iron(II) in the 250 cm³ flask', notation: '(2) + (2)', decoded: 'Two steps (×5 stoichiometry; ×10 scaling), 2 marks each.', marks: 4 },
      { part: '(e)(iii)', task: 'Calculate the average mass of iron(II) per tablet', notation: '(2) + (2)', decoded: 'Two steps (moles per tablet; ×56 to mass), 2 marks each.', marks: 4 },
      { part: '(e)(iv)', task: 'Calculate the % by mass of iron(II) in one tablet', notation: '(4)', decoded: 'The percentage earns 4 marks; "[Allow 3 marks for 0.2524]".', marks: 4 },
    ],
    pitfall: {
      text: 'In the same iron-tablet analysis, the Chief Examiner flagged "incorrect multiplying of interim answers by five" among "errors that were regularly observed" — the ×5 stoichiometric step here carries its own 2 marks.',
      cite: "Chief Examiner's Report 2013 (Chemistry), p.16",
    },
    cite: CITE25('Q1'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '2',
    totalMarks: 50,
    headline: 'Clove-oil steam distillation: the extraction procedure is a front-loaded 6 + 3 "any two" list; the eugenol structure alone carries 6.',
    parts: [
      { part: '(a)(i)', task: 'Identify substance A in the distillate', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(ii)', task: 'State and explain the appearance of the distillate', notation: '(3) + (3)', decoded: 'The appearance earns 3 marks; the explanation earns 3.', marks: 6 },
      { part: '(a)(iii)', task: 'State one advantage of steam distillation here', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(i)', task: 'Describe, with a labelled diagram, the liquid-liquid extraction procedure', notation: '(6 + 3)', decoded: 'Any two of the three listed elements: the first earns 6 marks, the second 3; "[maximum of 6 marks awarded if diagram not included]".', marks: 9 },
      { part: '(b)(ii)', task: 'State two properties making cyclohexane a suitable solvent', notation: '(2 × 3)', decoded: 'Any two of the listed properties, 3 marks each.', marks: 6 },
      { part: '(b)(iii)', task: 'State one precaution to maximise the eugenol yield', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(iv)', task: 'Describe isolating eugenol from the dried mixture', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'Suggest one use of eugenol', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(ii)', task: 'Draw the structure of a eugenol molecule', notation: '(6)', decoded: 'The drawn structure earns 6 marks.', marks: 6 },
      { part: '(c)(iii)', task: 'Name a spectroscopic technique to confirm identity', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(iv)', task: 'Calculate the volume of dry eugenol from 18.0 g of cloves at 7% yield', notation: '(3 + 2)', decoded: 'Two calculation steps: the mass earns 3 marks, the volume earns 2.', marks: 5 },
    ],
    cite: CITE25('Q2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '3',
    totalMarks: 50,
    headline: 'H₂O₂/MnO₂ rate experiment: the graph carries 12 (axes 3, points 7 × 1, curve 2); each predict-and-justify part splits 4 + 2.',
    parts: [
      { part: '(a)(i)', task: 'Plot the volume of oxygen vs time graph', notation: '(3) + (7 × 1) + (2)', decoded: 'Axes labelled 3m; seven points at 1 mark each (max 3 if not on graph paper); curve with good fit 2m.', marks: 12 },
      { part: '(a)(ii)', task: 'Find the instantaneous rate at 2.5 minutes from the graph', notation: '(3) + (3)', decoded: 'A good tangent at 2.5 minutes earns 3 marks; the value earns 3.', marks: 6 },
      { part: '(b)(i)', task: 'Find the average rate over the first 2.5 minutes', notation: '(3)', decoded: 'The value carries 3 marks.', marks: 3 },
      { part: '(b)(ii)', task: 'Effect of granular (not powdered) MnO₂ on the average rate — justify', notation: '(4 + 2)', decoded: 'Two elements: the call earns 4 marks, the justification 2.', marks: 6 },
      { part: '(b)(iii)', task: 'Effect of more concentrated H₂O₂ — justify', notation: '(4 + 2)', decoded: 'Two elements: the call earns 4 marks, the justification 2.', marks: 6 },
      { part: '(c)(i)', task: 'Determine the average rate over the first minute', notation: '(3)', decoded: 'The value carries 3 marks.', marks: 3 },
      { part: '(c)(ii)', task: 'Determine the average rate over the second minute', notation: '(3)', decoded: 'The value carries 3 marks.', marks: 3 },
      { part: '(c)(iii)', task: 'Account for the difference between the two average rates', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(d)', task: '(i) How a catalyst alters rate; (ii) type of catalysis here — justify', notation: '(4 + 2 + 2)', decoded: 'Eight marks across (d)(i) and (d)(ii): the printed answer elements are marked 4, 2 and 2.', marks: 8 },
    ],
    cite: CITE25('Q3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '4',
    totalMarks: 50,
    headline: 'Twelve short items (a)–(l); eight are answered at 6 marks each, with a 1-mark bonus on each of the first two attempted.',
    parts: [
      { part: '(a)–(l)', task: 'Any eight of the twelve short items', notation: 'Six marks to be allocated to each item', decoded: 'Eight items at 6 marks each (48). Within an item the 6 splits as printed — e.g. (3) + (3) for two elements, or (2 × 3) for two drawn isomers.', marks: 48 },
      { part: '', task: 'The first two items attempted', notation: 'one additional mark to be added to each of the first two items attempted', decoded: 'A 1-mark bonus on each of the first two items attempted (2).', marks: 2 },
    ],
    cite: CITE25('Q4'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '5',
    totalMarks: 50,
    headline: 'Isotopes and orbitals: paired 3-mark elements, a three-step 2+2+2 relative-atomic-mass calculation, and a combined 4 + 4 + 2 + 2 radius part.',
    parts: [
      { part: '(a)(i)', task: 'Name the instrument for measuring isotopic abundance', notation: '(2)', decoded: 'One markable element — 2 marks.', marks: 2 },
      { part: '(a)(ii)', task: 'Compare the nuclei of bromine-79 and bromine-81', notation: '(3) + (3)', decoded: 'Two elements (protons; neutrons of each isotope), 3 marks each.', marks: 6 },
      { part: '(a)(iii)', task: 'Explain relative atomic mass', notation: '(3) + (3)', decoded: 'Two elements (average mass; relative to one twelfth of carbon-12), 3 marks each.', marks: 6 },
      { part: '(a)(iv)', task: 'Calculate the relative atomic mass of bromine to two decimal places', notation: '(2) + (2) + (2)', decoded: 'Three calculation steps, 2 marks each.', marks: 6 },
      { part: '(b)(i)', task: 'What is an atomic orbital?', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(ii)', task: 'Draw the shape of the lowest-energy orbital in bromine', notation: '(3)', decoded: 'The drawn shape earns 3 marks.', marks: 3 },
      { part: '(b)(iii)', task: 'State the maximum electrons in a p-orbital', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(iv)', task: 'Describe how orbitals of equal energy fill', notation: '(3) + (3)', decoded: 'Two elements (occupy singly; then in pairs), 3 marks each.', marks: 6 },
      { part: '(b)(v)', task: 'When might an electron temporarily occupy a higher orbital?', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)', task: '(i) Atomic radius; (ii) why Br > Cl; (iii) why Br < Se', notation: '(4 + 4 + 2 + 2)', decoded: 'Twelve marks across (c)(i)–(iii): the four printed answer elements are marked 4, 4, 2 and 2.', marks: 12 },
    ],
    cite: CITE25('Q5'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '6',
    totalMarks: 50,
    headline: 'Oil refining and fuels: the distillation diagram carries 9 (three 3-mark elements, max 6 without the diagram); the hydrazine calculation 14.',
    parts: [
      { part: '(a)(i)', task: 'State what saturated means for hydrocarbons', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(ii)', task: 'Describe, with a labelled diagram, obtaining refinery gas by fractional distillation', notation: '(3) + (3) + (3)', decoded: 'Three elements (column with outlets; temperature gradient; feed and take-off), 3 marks each; "[maximum of 6 marks awarded if diagram not included]".', marks: 9 },
      { part: '(a)(iii)', task: 'Identify the two major hydrocarbon components of LPG', notation: '(3) + (3)', decoded: 'Two elements (propane; butane), 3 marks each.', marks: 6 },
      { part: '(a)(iv)', task: 'Name the process converting octane into 2,2,4-trimethylpentane', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(a)(v)', task: 'Identify the inorganic co-product of hexane → cyclohexane', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)', task: '(i) Heat of combustion; (ii) measuring instrument; (iii) two industrial H₂ production methods', notation: '(4 + 4 + 2 + 2)', decoded: 'Twelve marks across (b)(i)–(iii): the four printed answer elements are marked 4, 4, 2 and 2.', marks: 12 },
      { part: '(c)', task: 'Calculate the heat change for the hydrazine-forming reaction', notation: '(3) + (3) + (3) + (3) + (2)', decoded: 'Each of the four heat-of-formation terms earns 3 marks (printed as 2 for the multiplicative factor + 1 for the sign); the final answer earns 2.', marks: 14 },
    ],
    cite: CITE25('Q6'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '7',
    totalMarks: 50,
    headline: 'Acids and bases: definitions in 2 + 2 pairs, a single 6-mark Kw expression, and three-step calculations at 2/3 marks per step.',
    parts: [
      { part: '(a)(i)', task: 'How an acid differs from a base (Brønsted-Lowry)', notation: '(2) + (2)', decoded: 'Two elements (proton donor; proton acceptor), 2 marks each.', marks: 4 },
      { part: '(a)(ii)', task: 'How a strong acid differs from a weak acid (Brønsted-Lowry)', notation: '(2) + (2)', decoded: 'Two elements (good proton donor; poor proton donor), 2 marks each.', marks: 4 },
      { part: '(a)(iii)', task: 'What is a conjugate acid-base pair?', notation: '(2)', decoded: 'One markable element — 2 marks.', marks: 2 },
      { part: '(a)(iv)', task: 'Identify the conjugate pairs in the HCO₃⁻/H₂O reaction', notation: '(3)', decoded: 'Both pairs earn a single 3-mark award.', marks: 3 },
      { part: '(b)(i)', task: 'Explain what is meant by pH', notation: '(2) + (2)', decoded: 'Two elements (–log₁₀; [H⁺]), 2 marks each.', marks: 4 },
      { part: '(b)(ii)', task: 'Calculate [H₃O⁺] for a strong acid of pH 1.4', notation: '(2) + (2)', decoded: 'Two calculation steps, 2 marks each.', marks: 4 },
      { part: '(b)(iii)', task: 'Calculate the pH of a 0.015 M weak monobasic acid', notation: '(2) + (2) + (3)', decoded: 'Three steps: formula 2m, evaluation 2m, pH 3m.', marks: 7 },
      { part: '(c)(i)', task: 'Write the expression for the ionic product of water (Kw)', notation: '(6)', decoded: 'The expression earns a single 6-mark award.', marks: 6 },
      { part: '(c)(ii)', task: 'Calculate the pH of pure water at 60 °C', notation: '(3) + (3)', decoded: 'Two steps ([H⁺]; pH), 3 marks each.', marks: 6 },
      { part: '(d)(i)', task: 'Colour of indicator HA in a strong base — justify', notation: '(3) + (3)', decoded: 'The colour call earns 3 marks; the justification earns 3.', marks: 6 },
      { part: '(d)(ii)', task: 'Is HA suitable for the titration shown? Justify', notation: '(2) + (2)', decoded: 'The call earns 2 marks; the justification earns 2.', marks: 4 },
    ],
    cite: CITE25('Q7'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '8',
    totalMarks: 50,
    headline: 'Organic reaction scheme and the labelled ester: 2/3-mark elements, a 5-mark structure, and a 4 × 1 + 2 balanced equation.',
    parts: [
      { part: '(a)', task: 'Identify a substitution, an oxidation and a reduction reaction in the scheme', notation: '(2) + (2) + (2)', decoded: 'Three identifications, 2 marks each.', marks: 6 },
      { part: '(b)(i)', task: 'Name the homologous series of ethanal', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(b)(ii)', task: 'Colour change when ethanal is warmed with Fehling’s reagent', notation: '(3) + (3)', decoded: 'Start and end colours earn 3 marks each.', marks: 6 },
      { part: '(b)(iii)', task: 'Identify the reagent and catalyst converting ethanal to ethanol', notation: '(3) + (3)', decoded: 'Two elements (hydrogen; nickel), 3 marks each.', marks: 6 },
      { part: '(c)(i)', task: 'Draw the structure of ethyl ethanoate', notation: '(5)', decoded: 'The drawn structure earns 5 marks.', marks: 5 },
      { part: '(c)(ii)', task: 'Indicate the position of the O* atom', notation: '(3)', decoded: 'The indication earns 3 marks.', marks: 3 },
      { part: '(c)(iii)', task: 'Indicate the bond formed during esterification', notation: '(3)', decoded: 'The indication earns 3 marks.', marks: 3 },
      { part: '(c)(iv)', task: 'State the number of electrons in sigma bonds', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(v)', task: 'State the number of electrons in pi bonds', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(c)(vi)', task: 'State the number of lone pairs present', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
      { part: '(d)(i)', task: 'Write a balanced equation for ethanol reacting with sodium', notation: '(4 × 1 + 2)', decoded: 'Four species at 1 mark each, plus 2 marks for balancing.', marks: 6 },
      { part: '(d)(ii)', task: 'Why is ethanoate a weaker conjugate base than ethoxide?', notation: '(3)', decoded: 'One markable element — 3 marks.', marks: 3 },
    ],
    cite: CITE25('Q8'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC022ALP000EV.pdf', n: '9',
    totalMarks: 50,
    headline: 'NOBr equilibrium: single 4-mark definitions, a 10-mark Kc calculation, and three state-and-justify parts at 4 + 2 each.',
    parts: [
      { part: '(a)(i)', task: 'Explain a reversible reaction', notation: '(4)', decoded: 'One markable element — 4 marks.', marks: 4 },
      { part: '(a)(ii)', task: 'Explain why concentrations stay constant at dynamic equilibrium', notation: '(4)', decoded: 'One markable element — 4 marks.', marks: 4 },
      { part: '(b)(i)', task: 'Calculate the initial moles of NOBr', notation: '(2) + (2)', decoded: 'Two steps (Mr = 110; the moles), 2 marks each.', marks: 4 },
      { part: '(b)(ii)', task: 'Calculate the moles of NOBr at equilibrium', notation: '(2) + (2)', decoded: 'Two steps (moles decomposed; moles remaining), 2 marks each.', marks: 4 },
      { part: '(b)(iii)', task: 'Write the Kc expression', notation: '(6)', decoded: 'The expression earns 6 marks; "[award 3 marks if round brackets are used]".', marks: 6 },
      { part: '(b)(iv)', task: 'Calculate the value of Kc at temperature T', notation: '(2) + (2) + (3) + (3)', decoded: 'Four steps: moles of NO 2m; moles of Br₂ 2m; conversion to mol/L 3m; the evaluated Kc 3m.', marks: 10 },
      { part: '(c)(i)', task: 'State Le Châtelier’s principle', notation: '(4+2)', decoded: 'Two elements (system at equilibrium; opposes an applied stress) at 4 and 2 marks.', marks: 6 },
      { part: '(c)(ii)', task: 'Effect of increased pressure on moles of Br₂ — justify', notation: '(4+2)', decoded: 'The call earns 4 marks; the justification earns 2.', marks: 6 },
      { part: '(c)(iii)', task: 'Endothermic or exothermic? Justify from Kc rising with temperature', notation: '(4+2)', decoded: 'The call earns 4 marks; the justification earns 2.', marks: 6 },
    ],
    cite: CITE25('Q9'),
  },
];

const CHEMISTRY_LENS: SubjectLens = {
  subjectId: 'chemistry',
  entries: [
    ...ENTRIES_2024,
    ...mirrorIV(ENTRIES_2024, 'LC022ALP000IV.pdf'),
    ...ENTRIES_2025,
    ...mirrorIV(ENTRIES_2025, 'LC022ALP000IV.pdf'),
  ],
};

export default CHEMISTRY_LENS;
