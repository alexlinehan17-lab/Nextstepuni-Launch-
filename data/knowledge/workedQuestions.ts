/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Worked questions for the Working-Shown Allocator (Stage 2).
 *
 * Each question shows a Maths/Science/Accounting answer broken into 5
 * steps. Marks accrue per step. Some questions include a "slip variant"
 * step — a wrong-direction version of one step that demonstrates how a
 * single mistake propagates.
 *
 * Per /CLAUDE.md content rule: question text paraphrased, never more
 * than 15 words verbatim from any SEC paper.
 *
 * Scoring grammar: 10D scale (0, 3, 5, 8, 10) per dossier § A2.
 *   - Attempt mark = 3 (writing the formula alone)
 *   - Mid-band      = 5 (formula + correct substitution)
 *   - Upper-mid     = 8 (substitution + correct manipulation)
 *   - Full          = 10 (correct final answer + verify)
 *
 * Penalty grammar (dossier § A2):
 *   - Slip (S)      = −1 (numerical / arithmetic mistake)
 *   - Blunder (B)   = −3 (mathematical error or omission)
 *   - Misreading(M) = −1 (provided the misread didn't oversimplify)
 *
 * Sources:
 * - 2015 Maths Chief Examiner Report
 * - Chemistry / Physics marking-scheme conventions per dossier § B4
 * - Accounting marking-scheme convention (calculator trap, W-references)
 *   per dossier § A2 / § B7
 */

import { type WorkingQuestion } from '../../types/knowledge';

export const WORKED_QUESTIONS: WorkingQuestion[] = [
  // ─── Q1 · Maths HL Algebra — Quadratic ────────────────────────────
  {
    id: 'maths-quadratic',
    subject: 'maths',
    topicLabel: 'Quadratic equation — find both roots',
    questionPrompt: 'Solve 2x² − 7x + 3 = 0. Find the values of x.',
    marksAvailable: 10,
    scaleLabel: '10D scale (0, 3, 5, 8, 10)',
    steps: [
      {
        id: 'q1-s1',
        label: 'Write the formula from the Tables booklet',
        contentLines: ['x = (−b ± √(b² − 4ac)) / 2a'],
        marksEarned: 3,
        annotation:
          'The attempt mark — 30% of the part. Writing the formula alone preserves three marks even if you go no further. The 2015 Maths CER explicitly notes: "if you write nothing, the examiner cannot award any marks."',
      },
      {
        id: 'q1-s2',
        label: 'Identify a, b, c and substitute',
        contentLines: ['a = 2, b = −7, c = 3', 'x = (7 ± √(49 − 24)) / 4'],
        marksEarned: 2,
        annotation:
          'Substitution. Notice −b becomes +7 because b = −7. This is the line where sign blunders begin — half of the slip-path examples in the marking scheme are sign mistakes here.',
      },
      {
        id: 'q1-s3',
        label: 'Evaluate the discriminant',
        contentLines: ['= (7 ± √25) / 4', '= (7 ± 5) / 4'],
        marksEarned: 3,
        annotation:
          'Discriminant = 25, so √25 = 5. Two real roots. +3 marks for correct manipulation.',
      },
      {
        id: 'q1-s3-blunder',
        label: 'Evaluate the discriminant — sign blunder',
        contentLines: ['= (7 ± √(49 + 24)) / 4   ←  + instead of −', '= (7 ± √73) / 4 ≈ (7 ± 8.54) / 4'],
        marksEarned: 3,
        penalty: { kind: 'blunder', amount: -3, reason: 'Sign error in b² − 4ac. Wrote + instead of −.' },
        annotation:
          'What feels like a "small slip" is what the marker calls a blunder — a mathematical error in working. Per the dossier penalty grammar: blunder = −3 marks. Three times the cost of a slip. The work-of-merit (+3) covers the algebraic effort, but the −3 blunder cancels it out.',
      },
      {
        id: 'q1-s4',
        label: 'Solve both roots',
        contentLines: ['x = (7 + 5) / 4 = 3', 'x = (7 − 5) / 4 = 0.5'],
        marksEarned: 2,
        annotation:
          '"Find the values of x" — plural — means both roots. Missing one root caps step 4 at +1. The plural cue is a Spot-the-Trap classic.',
      },
      {
        id: 'q1-s5',
        label: 'Verify by substitution',
        contentLines: ['2(3)² − 7(3) + 3 = 18 − 21 + 3 = 0  ✓', '2(0.5)² − 7(0.5) + 3 = 0.5 − 3.5 + 3 = 0  ✓'],
        marksEarned: 0,
        annotation:
          'No marks awarded for verification — but it\'s the cheapest insurance against the slip path. 30 seconds saves 3 marks. If your slip-path answer fails verification, you have time to go back.',
      },
    ],
    paths: [
      {
        id: 'blank',
        label: 'Nothing on the page',
        includedStepIds: [],
        finalScore: 0,
        characterisation: 'A panic blank. Even if the student knows the answer, the marker cannot award marks for what isn\'t written.',
      },
      {
        id: 'formula-only',
        label: 'Formula only',
        includedStepIds: ['q1-s1'],
        finalScore: 3,
        characterisation: 'The student wrote the formula from the Tables booklet and stopped. They earn the attempt mark — 30% of the part — for nothing more than recognition.',
      },
      {
        id: 'formula-sub',
        label: 'Formula + substitution',
        includedStepIds: ['q1-s1', 'q1-s2'],
        finalScore: 5,
        characterisation: 'Formula + correct identification of a, b, c. Mid-band. The student understood the structure but ran out of confidence before the discriminant.',
      },
      {
        id: 'full-with-slip',
        label: 'Full working — with one blunder',
        includedStepIds: ['q1-s1', 'q1-s2', 'q1-s3-blunder', 'q1-s4', 'q1-s5'],
        finalScore: 7,
        characterisation: 'All five steps are on the page, but a sign error in step 3 cancels three marks. The "slip you\'d never notice" — and the dossier explicitly calls this a blunder, not a slip.',
      },
      {
        id: 'full-correct',
        label: 'Full working, correct',
        includedStepIds: ['q1-s1', 'q1-s2', 'q1-s3', 'q1-s4', 'q1-s5'],
        finalScore: 10,
        characterisation: 'The complete answer with both roots and verification. Full marks.',
      },
    ],
    source: { section: 'A2', page: 3, cite: '2015 Maths Chief Examiner Report — partial credit grammar' },
  },

  // ─── Q2 · Maths HL Geometry — Pythagoras ──────────────────────────
  {
    id: 'maths-pythagoras',
    subject: 'maths',
    topicLabel: 'Right-angled triangle — find the third side',
    questionPrompt: 'A right-angled triangle has hypotenuse 13 cm and one side 5 cm. Find the length of the third side.',
    marksAvailable: 10,
    scaleLabel: '10D scale (0, 3, 5, 8, 10)',
    steps: [
      {
        id: 'q2-s1',
        label: 'State Pythagoras\' theorem',
        contentLines: ['a² + b² = c² where c is the hypotenuse'],
        marksEarned: 3,
        annotation:
          'Attempt mark — naming the relevant theorem and identifying that the hypotenuse is the longest side. The marking scheme explicitly accepts this as a relevant first step.',
      },
      {
        id: 'q2-s2',
        label: 'Identify the values',
        contentLines: ['c = 13 cm (hypotenuse), a = 5 cm', 'Find b'],
        marksEarned: 2,
        annotation:
          'Identification. The marker is checking that the student knows which side is the hypotenuse. A common blunder here: treating 13 as a leg and looking for the hypotenuse instead.',
      },
      {
        id: 'q2-s3',
        label: 'Substitute and rearrange',
        contentLines: ['5² + b² = 13²', '25 + b² = 169', 'b² = 169 − 25 = 144'],
        marksEarned: 3,
        annotation:
          'Correct rearrangement. b² is isolated by subtracting 25 from both sides.',
      },
      {
        id: 'q2-s3-blunder',
        label: 'Substitute and rearrange — formula misapplied',
        contentLines: ['5² + 13² = b²   ←  treated 13 as a leg', '25 + 169 = b²', 'b² = 194 → b ≈ 13.93 cm'],
        marksEarned: 3,
        penalty: { kind: 'blunder', amount: -3, reason: 'Treated the hypotenuse as a leg — a misapplication of Pythagoras.' },
        annotation:
          'The student wrote the formula correctly (+3 work of merit) but applied it as though 13 were a leg, not the hypotenuse. The marker reads this as a misapplication, which the dossier classifies as a blunder (−3). Net: +0 for this step.',
      },
      {
        id: 'q2-s4',
        label: 'Solve for b — include the unit',
        contentLines: ['b = √144', 'b = 12 cm'],
        marksEarned: 2,
        annotation:
          'Final answer with unit. Missing the "cm" is a slip in many marking schemes — −1 mark. In quantitative subjects, units are mark-bearing per dossier § A6.',
      },
      {
        id: 'q2-s5',
        label: 'Sanity check',
        contentLines: ['5–12–13 is a Pythagorean triple — the answer is plausible.'],
        marksEarned: 0,
        annotation:
          '0 marks for the check itself, but it\'s the catch-net for the blunder path. A student who treated 13 as a leg would notice the answer (≈13.93 cm) is longer than the hypotenuse, which is geometrically impossible.',
      },
    ],
    paths: [
      {
        id: 'blank',
        label: 'Nothing on the page',
        includedStepIds: [],
        finalScore: 0,
        characterisation: 'Recognition failure. The student didn\'t identify the question as a Pythagoras problem.',
      },
      {
        id: 'formula-only',
        label: 'Theorem stated only',
        includedStepIds: ['q2-s1'],
        finalScore: 3,
        characterisation: 'The student wrote a² + b² = c² and stopped. The attempt mark covers theorem recognition.',
      },
      {
        id: 'formula-sub',
        label: 'Theorem + values identified',
        includedStepIds: ['q2-s1', 'q2-s2'],
        finalScore: 5,
        characterisation: 'Identified the hypotenuse correctly but ran out of algebraic confidence to rearrange.',
      },
      {
        id: 'full-with-slip',
        label: 'Full working — formula misapplied',
        includedStepIds: ['q2-s1', 'q2-s2', 'q2-s3-blunder', 'q2-s4', 'q2-s5'],
        finalScore: 7,
        characterisation: 'Treated the hypotenuse as a leg. The misapplication is a blunder — −3 marks. The sanity check would have caught it: a leg cannot be longer than the hypotenuse.',
      },
      {
        id: 'full-correct',
        label: 'Full working, correct',
        includedStepIds: ['q2-s1', 'q2-s2', 'q2-s3', 'q2-s4', 'q2-s5'],
        finalScore: 10,
        characterisation: 'All steps complete. Hypotenuse identified, formula rearranged correctly, unit included, sanity check applied.',
      },
    ],
    source: { section: 'A2', page: 3, cite: 'Maths marking-scheme partial-credit convention; sanity check per dossier § C1' },
  },

  // ─── Q3 · Chemistry HL Mole Calc ──────────────────────────────────
  {
    id: 'chem-mole-calc',
    subject: 'chemistry',
    topicLabel: 'Mole calculation — moles in 250 cm³ of 0.1 M solution',
    questionPrompt: 'Calculate the number of moles in 250 cm³ of a 0.1 M sodium hydroxide solution.',
    marksAvailable: 10,
    scaleLabel: 'Chemistry mole-calc scheme (3 / 5 / 8 / 10 bands)',
    steps: [
      {
        id: 'q3-s1',
        label: 'Write the relationship',
        contentLines: ['n = c × V'],
        marksEarned: 3,
        annotation:
          'Attempt mark. The relationship between moles (n), concentration (c, in mol/dm³), and volume (V, in dm³) is the foundation of every mole-calc question. Writing this alone earns three marks.',
      },
      {
        id: 'q3-s2',
        label: 'Identify the values',
        contentLines: ['c = 0.1 mol/dm³', 'V = 250 cm³ = 0.250 dm³'],
        marksEarned: 2,
        annotation:
          'Volume must be in dm³. 1 dm³ = 1 litre = 1000 cm³. Per dossier § B4: the most common chemistry blunder is failing to convert cm³ to dm³ — and the marking scheme treats it as a blunder, not a slip.',
      },
      {
        id: 'q3-s3',
        label: 'Substitute and compute',
        contentLines: ['n = 0.1 × 0.250', 'n = 0.025 mol'],
        marksEarned: 3,
        annotation:
          'Correct multiplication. Note units throughout — the answer must be in mol.',
      },
      {
        id: 'q3-s3-blunder',
        label: 'Substitute and compute — failed unit conversion',
        contentLines: ['n = 0.1 × 250   ← V left in cm³', 'n = 25 mol'],
        marksEarned: 3,
        penalty: { kind: 'blunder', amount: -3, reason: 'Volume left in cm³. Failed to convert to dm³.' },
        annotation:
          '25 moles of NaOH would weigh a kilogram. The order-of-magnitude check would catch this in five seconds. Per the dossier, missed unit conversion is a blunder (−3) — not a slip.',
      },
      {
        id: 'q3-s4',
        label: 'State the final answer with units',
        contentLines: ['Number of moles = 0.025 mol'],
        marksEarned: 2,
        annotation:
          'Final-answer mark. Missing the unit "mol" costs a slip (−1) on most chemistry marking schemes.',
      },
      {
        id: 'q3-s5',
        label: 'Sanity check',
        contentLines: ['0.1 M means 0.1 mol per litre. We have a quarter-litre, so ~0.025 mol.', 'A solid handful of NaOH would be far more than 25 moles — implausible.'],
        marksEarned: 0,
        annotation:
          'No extra marks. But this 5-second mental check distinguishes 0.025 from 25 — a 1000× error. Order-of-magnitude is the fastest sanity check.',
      },
    ],
    paths: [
      {
        id: 'blank',
        label: 'Nothing on the page',
        includedStepIds: [],
        finalScore: 0,
        characterisation: 'No working. Even with a correct answer, no marks are awarded without a relevant first step.',
      },
      {
        id: 'formula-only',
        label: 'Relationship written',
        includedStepIds: ['q3-s1'],
        finalScore: 3,
        characterisation: 'Wrote n = c × V and stopped. Attempt mark earned. The formula is the gateway to every chemistry mole-calc.',
      },
      {
        id: 'formula-sub',
        label: 'Relationship + values',
        includedStepIds: ['q3-s1', 'q3-s2'],
        finalScore: 5,
        characterisation: 'Identified c and V but didn\'t complete the multiplication. The marker awards five marks for correct identification — including the cm³ → dm³ conversion.',
      },
      {
        id: 'full-with-slip',
        label: 'Full working — unit conversion blunder',
        includedStepIds: ['q3-s1', 'q3-s2', 'q3-s3-blunder', 'q3-s4', 'q3-s5'],
        finalScore: 7,
        characterisation: 'V left in cm³. The answer is 1000× too big. The marker reads this as a blunder (−3). The sanity check would have flagged the impossibility.',
      },
      {
        id: 'full-correct',
        label: 'Full working, correct',
        includedStepIds: ['q3-s1', 'q3-s2', 'q3-s3', 'q3-s4', 'q3-s5'],
        finalScore: 10,
        characterisation: 'Correct conversion, correct multiplication, correct units, sanity check applied. Full marks.',
      },
    ],
    source: { section: 'B4', page: 10, cite: 'Chemistry marking-scheme convention — mole calculations and unit conversions' },
  },

  // ─── Q4 · Physics HL Mechanics ────────────────────────────────────
  {
    id: 'phys-mechanics',
    subject: 'physics',
    topicLabel: 'Force on an accelerating object',
    questionPrompt: 'A 5 kg trolley accelerates at 2 m/s². Find the resultant force.',
    marksAvailable: 10,
    scaleLabel: 'Physics 10-mark band (3 / 5 / 8 / 10)',
    steps: [
      {
        id: 'q4-s1',
        label: 'Write Newton\'s second law',
        contentLines: ['F = ma'],
        marksEarned: 3,
        annotation:
          'Attempt mark. Newton\'s second law is one of the foundations of every mechanics question. Writing the formula alone is +3.',
      },
      {
        id: 'q4-s2',
        label: 'Identify the values with units',
        contentLines: ['m = 5 kg', 'a = 2 m/s²'],
        marksEarned: 2,
        annotation:
          'SI units throughout. Mass in kg, acceleration in m/s². Mismatched units (e.g. mass in grams) is one of the most common physics blunders.',
      },
      {
        id: 'q4-s3',
        label: 'Substitute and compute',
        contentLines: ['F = 5 × 2', 'F = 10'],
        marksEarned: 3,
        annotation:
          'Multiplication is correct. But the answer is incomplete without units — that\'s the slip path.',
      },
      {
        id: 'q4-s4',
        label: 'State the final answer with units',
        contentLines: ['F = 10 N (newtons)'],
        marksEarned: 2,
        annotation:
          'Per dossier § B4: the unit "newton" must be present. Missing units commonly costs the final mark in Physics. Lower-case for spelled-out units (newtons), capital for symbols (N).',
      },
      {
        id: 'q4-s4-slip',
        label: 'State the final answer — units missing',
        contentLines: ['F = 10'],
        marksEarned: 2,
        penalty: { kind: 'blunder', amount: -3, reason: 'Final answer with no units. Per Physics marking-scheme convention, missing units forfeits the final-answer mark and triggers the units-block penalty.' },
        annotation:
          'A bare "F = 10" with no units. The marker awards the working credit (+2) but penalises three marks because the final answer is incomplete and physically meaningless. Newtons? Pounds? Per dossier § B4 / § A6, units are mark-bearing.',
      },
      {
        id: 'q4-s5',
        label: 'Sanity check',
        contentLines: ['10 N is roughly the weight of a 1 kg bag of sugar.', 'A trolley accelerating gently — 10 N is plausible.'],
        marksEarned: 0,
        annotation:
          'No marks. But order-of-magnitude is the daily check that prevents 10⁹ N answers — the dossier\'s example of a "force to push a shopping trolley" sanity failure.',
      },
    ],
    paths: [
      {
        id: 'blank',
        label: 'Nothing on the page',
        includedStepIds: [],
        finalScore: 0,
        characterisation: 'Nothing written. Even one line of recognition would have earned three marks.',
      },
      {
        id: 'formula-only',
        label: 'F = ma only',
        includedStepIds: ['q4-s1'],
        finalScore: 3,
        characterisation: 'Newton\'s second law written and nothing more. Attempt mark earned for theorem recognition.',
      },
      {
        id: 'formula-sub',
        label: 'F = ma + values',
        includedStepIds: ['q4-s1', 'q4-s2'],
        finalScore: 5,
        characterisation: 'Identified m and a with units. Five marks. Mid-band.',
      },
      {
        id: 'full-with-slip',
        label: 'Full working — units missing',
        includedStepIds: ['q4-s1', 'q4-s2', 'q4-s3', 'q4-s4-slip', 'q4-s5'],
        finalScore: 7,
        characterisation: 'F = 10 with no units. Numerically right, physically meaningless. Three marks lost to the units-block penalty.',
      },
      {
        id: 'full-correct',
        label: 'Full working, correct',
        includedStepIds: ['q4-s1', 'q4-s2', 'q4-s3', 'q4-s4', 'q4-s5'],
        finalScore: 10,
        characterisation: 'F = 10 N. Sanity check applied. Full marks.',
      },
    ],
    source: { section: 'B4', page: 11, cite: 'Physics marking-scheme convention — units mark-bearing' },
  },

  // ─── Q5 · Accounting HL — Adjustment ──────────────────────────────
  {
    id: 'acc-depreciation',
    subject: 'accounting',
    topicLabel: 'Depreciation adjustment — cross-referenced workings',
    questionPrompt: 'A van costs €30,000 with a residual value of €5,000 and a useful life of 5 years. Calculate the annual depreciation charge and show how it appears in the Profit & Loss Account.',
    marksAvailable: 10,
    scaleLabel: 'Accounting 10-mark band; cross-reference rule per dossier § A2',
    steps: [
      {
        id: 'q5-s1',
        label: 'Open Workings note: W1',
        contentLines: ['W1 — Annual Depreciation'],
        marksEarned: 3,
        annotation:
          'Attempt mark. Per the dossier "calculator trap" rule, every adjustment must have a labelled W-note. Writing "W1 — Annual Depreciation" alone is the attempt mark — three marks for the discipline of showing.',
      },
      {
        id: 'q5-s2',
        label: 'State the formula',
        contentLines: ['Depreciation = (Cost − Residual) / Useful Life'],
        marksEarned: 2,
        annotation:
          'The straight-line depreciation formula. Stating it explicitly inside the W1 note is mark-bearing — markers can see the method and award method marks even if the arithmetic later fails.',
      },
      {
        id: 'q5-s3',
        label: 'Substitute and compute',
        contentLines: ['= (€30,000 − €5,000) / 5', '= €25,000 / 5', '= €5,000 per year'],
        marksEarned: 3,
        annotation:
          'Correct arithmetic with the € sign. Per dossier § A2: the € sign and unit are mark-bearing in Accounting. Numbers without € lose marks even when correct.',
      },
      {
        id: 'q5-s4',
        label: 'Cross-reference into the P&L',
        contentLines: ['Profit & Loss Account', 'For the year ended 31/12/20XX', '...', 'Depreciation: Vehicles  (W1)   €5,000'],
        marksEarned: 2,
        annotation:
          'Cross-reference (W1) appears beside the figure in the P&L. The marker can trace the figure back to its working. This is the rule that defeats the "calculator trap".',
      },
      {
        id: 'q5-s4-slip',
        label: 'Cross-reference into the P&L — figure only',
        contentLines: ['Profit & Loss Account', 'For the year ended 31/12/20XX', '...', 'Depreciation: €5,000   ← no (W1) reference'],
        marksEarned: 0,
        penalty: { kind: 'blunder', amount: -3, reason: 'No W1 reference. The "calculator trap" — partial credit for the working is forfeited because the marker cannot link the figure to its source.' },
        annotation:
          'The figure is correct, but with no (W1) the marker cannot connect it to the working. Per dossier § A2 / § B7: the calculator trap forfeits all partial credit for the adjustment if the figure is later shown to be wrong. Even with a correct figure, the lack of cross-reference loses three marks.',
      },
      {
        id: 'q5-s5',
        label: 'Verify column totals',
        contentLines: ['Check that the depreciation figure flows correctly to the P&L total and that any related fixed-asset note (W2) is consistent.'],
        marksEarned: 0,
        annotation:
          'No extra marks for the check itself. But Accounting is the fastest-paced LC paper at 27 seconds per mark — when an adjustment is wrong, every later figure built on it is wrong too.',
      },
    ],
    paths: [
      {
        id: 'blank',
        label: 'Nothing on the page',
        includedStepIds: [],
        finalScore: 0,
        characterisation: 'No working. The most expensive line in Accounting is the empty one.',
      },
      {
        id: 'formula-only',
        label: 'W1 note opened',
        includedStepIds: ['q5-s1'],
        finalScore: 3,
        characterisation: 'Just "W1 — Annual Depreciation" written. Attempt mark earned for opening a labelled working.',
      },
      {
        id: 'formula-sub',
        label: 'W1 + formula',
        includedStepIds: ['q5-s1', 'q5-s2'],
        finalScore: 5,
        characterisation: 'Method visible. Five marks for the W1 note + formula. The marker can see how the student intends to compute the figure.',
      },
      {
        id: 'full-with-slip',
        label: 'Full working — calculator trap',
        includedStepIds: ['q5-s1', 'q5-s2', 'q5-s3', 'q5-s4-slip', 'q5-s5'],
        finalScore: 7,
        characterisation: 'Working is on the page, but the P&L figure has no (W1) reference. The marker treats this as a calculator trap — three marks forfeited for breaking the cross-reference rule.',
      },
      {
        id: 'full-correct',
        label: 'Full working, cross-referenced',
        includedStepIds: ['q5-s1', 'q5-s2', 'q5-s3', 'q5-s4', 'q5-s5'],
        finalScore: 10,
        characterisation: 'W1 written, formula stated, arithmetic shown, € signs, and (W1) cross-reference into the P&L. Full marks.',
      },
    ],
    source: { section: 'A2', page: 5, cite: 'Accounting marking-scheme convention — W-references and headings; dossier § B7' },
  },
];
