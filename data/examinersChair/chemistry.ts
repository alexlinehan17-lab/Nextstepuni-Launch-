/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Chemistry (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the exact-term demands, the "show your Mr addition" rule,
 * the per-occurrence calculation deduction, the units-in-final-answer rule, the
 * `//` mutually-exclusive method rule, the balanced-equation "(4 × 1 + 2)" split
 * and the organic structure-drawing deductions) is the real SEC system, cited to:
 *  - SEC LC Chemistry HL marking scheme 2024 —
 *    examiner-reports/chemistry/2024-marking-scheme.*
 *  - Chief Examiner's Report, Chemistry 2013 —
 *    examiner-reports/chemistry/2013-chief-examiner.*
 * Chemistry shares Biology's general conventions (the context rule, front-
 * loaded points lists); it adds a heavier calculation-deduction regime.
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Chemistry HL marking scheme 2024, ${p}` });
const CER = (p: string) => ({ label: `Chief Examiner's Report, Chemistry 2013, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── Ch1 · Exact-term demands ───────────────

const CH1: GridSession = {
  mode: 'grid',
  id: 'chem-exact-term',
  subject: 'chemistry',
  level: 'common',
  title: 'Colourless, not clear',
  cue: 'State observation',
  question: 'State what you would observe when the reaction is complete. The mark scheme requires the exact word “colourless” and prints “[do not accept clear]”.',
  questionNote:
    'Scenario authored for this exercise. Chemistry schemes enforce exact terms inline with “[do not accept …]” notes; the “clear” vs “colourless” distinction is a documented recurring error.',
  grid: {
    perPoint: [{ id: 'obs', label: 'Correct observation', marks: 3 }],
    shorthand: 'observation · 3m',
    ruleNote:
      'Where the scheme prints “[do not accept clear]”, near-synonyms fail: a clear solution can still be coloured, so it does not describe the observation. Chemistry rewards the precise scientific word, not the everyday one.',
    cite: MS('p.6 ([do not accept …] notes) and CER 2013 p.24'),
  },
  scripts: [
    {
      id: 'ch1-a',
      label: 'Script A',
      persona: 'Everyday word',
      attempts: [
        {
          id: 'ch1-a-1',
          text: 'The solution goes clear.',
          key: { obs: 0 },
          keyNote: '“Clear” is explicitly not accepted — a solution can be clear and still coloured, so it doesn’t report the observation. 0 marks. The examiner is checking for the precise term.',
        },
      ],
      embodies: {
        behaviour: 'Uses “clear” for “colourless” — a documented recurring error the scheme rejects.',
        cite: CER('p.24'),
      },
    },
    {
      id: 'ch1-b',
      label: 'Script B',
      persona: 'Precise term',
      attempts: [
        {
          id: 'ch1-b-1',
          text: 'The solution becomes colourless.',
          key: { obs: 3 },
          keyNote: 'The exact term the scheme requires. 3 marks. In Chemistry, precision of language is the difference between full marks and none.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-chem1',
    rule: 'Use the precise term, not the everyday one.',
    detail:
      'Chemistry schemes enforce exact words with “[do not accept …]” notes — “colourless” not “clear”, “effervescence” not “bubbles”. Learn the precise scientific term for observations; near-synonyms score zero.',
    cite: MS('p.6'),
  },
};

// ─────────────── Ch2 · Show your Mr addition ───────────────

const CH2: ScaleSession = {
  mode: 'scale',
  id: 'chem-mr',
  subject: 'chemistry',
  level: 'common',
  title: 'Show the addition',
  cue: 'Calculate',
  question: 'A calculation needs the relative molecular mass (Mr) of a compound. The candidate writes the Mr straight down as a single number — and it’s slightly wrong. The atomic-mass addition that builds it is not shown. How much does the Mr slip cost?',
  questionNote:
    'Scenario authored for this exercise. The scheme deducts one mark for an arithmetic slip in the Mr only if the atomic-mass addition is shown; if it isn’t, the full Mr marks are lost.',
  scale: {
    name: 'Mr with a slip',
    levels: two(0, 3),
    notes: [
      'General rule: an arithmetic slip is normally a one-mark deduction.',
      'For Mr specifically: the slip is only −1 IF the atomic-mass addition is shown.',
      'If the Mr is written as a bare (wrong) number, the full Mr marks are lost.',
    ],
    cite: MS('p.3 (point 7, Mr rule)'),
  },
  scripts: [
    {
      id: 'ch2-a',
      label: 'The answer',
      persona: 'Bare Mr, slightly wrong',
      work: ['Mr = 44  (written as a single number; the addition is not shown, and it should be 46)'],
      keyLevelId: 'm0',
      keyNote:
        'Full Mr marks lost — because the addition wasn’t shown, the examiner can’t see a one-mark slip; they see an unsupported wrong number. Had the candidate written “12 + (2 × 16) + …”, the same error would have cost just one mark. Always show the atomic-mass addition.',
      embodies: {
        behaviour: 'Writes a bare wrong Mr with no addition shown — forfeiting the protection of the one-mark slip rule.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-chem2',
    rule: 'Show the Mr addition to protect the mark.',
    detail:
      'A slip in the relative molecular mass is only a one-mark deduction if you show the atomic-mass addition. Write “12 + 2(16) + …” every time — a bare wrong Mr loses all its marks instead of one.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ch3 · // means one method ───────────────

const CH3: ScaleSession = {
  mode: 'scale',
  id: 'chem-solidus',
  subject: 'chemistry',
  level: 'common',
  title: 'Pick one method',
  cue: 'Calculate',
  question: 'A mark scheme offers two acceptable methods separated by “//” (mutually exclusive). The candidate does the first half of Method 1, then switches and does the second half of Method 2, hoping to stitch a full answer together. How does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s solidus rule: “//” separates mutually exclusive methods, and a partial answer from one side may not be combined with a partial answer from the other.',
  scale: {
    name: 'Mixed methods (//)',
    levels: [
      { id: 'm0', label: '0 (halves can’t combine)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (one method, partial)', annotation: '3', marks: 3 },
      { id: 'm6', label: '6 (one method, full)', annotation: '6', marks: 6 },
    ],
    notes: [
      '“//” marks two mutually exclusive methods.',
      '“A partial answer from one side of the // may not be taken in conjunction with a partial answer from the other side.”',
      'Stitching half of each method together scores only what one coherent method earns — often nothing.',
    ],
    cite: MS('p.3 (point 3, // rule)'),
  },
  scripts: [
    {
      id: 'ch3-a',
      label: 'The answer',
      persona: 'Half of each method',
      work: ['First half of Method 1.', 'Then switches: second half of Method 2.', 'Neither method is complete on its own.'],
      keyLevelId: 'm0',
      keyNote:
        'The two halves can’t be combined across the // , and neither method stands complete alone — so there’s nothing coherent to award. Committing to one method and finishing it, even partially, would have scored. Choose a method and see it through.',
      embodies: {
        behaviour: 'Combines partial work from two mutually-exclusive methods across a // — which cannot be credited together.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ch3-b',
      label: 'The answer',
      persona: 'One method, unfinished',
      work: ['Commits to Method 1 and stays on it throughout.', 'Sets it up and works the early steps correctly.', 'Runs out of time before the final step — incomplete, but coherent within the one method.'],
      keyLevelId: 'm3',
      keyNote:
        'Every mark here comes from a single coherent method, so the correct partial work is creditable — 3 of the 6 marks. This is the payoff of committing: unlike the stitched halves that scored nothing, one method carried as far as it goes still banks marks. Finishing it would have earned the full 6.',
      embodies: {
        behaviour: 'Commits to one method and earns partial credit for coherent work — the // rule doesn’t penalise an unfinished single method.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-chem3',
    rule: 'Commit to one method and finish it.',
    detail:
      'Where a scheme separates methods with “//”, you can’t stitch half of each together — partial work from opposite sides can’t be combined. Pick one route and carry it through; a complete-ish single method beats two abandoned halves.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ch4 · Explain needs a full sentence ───────────────

const CH4: GridSession = {
  mode: 'grid',
  id: 'chem-full-sentence',
  subject: 'chemistry',
  level: 'common',
  title: 'Explain wants a sentence',
  cue: 'Explain',
  question: 'A question says “Explain why the boiling point increases down the group.” A candidate answers with a bare phrase: “bigger molecules.” The Chief Examiner notes that on Describe/Explain cues a word or short phrase rarely earns full marks — the reasoning has to be stated.',
  questionNote:
    'Scenario authored for this exercise. The Chief Examiner’s Report flags that “Describe”/“Explain” cues need full sentences; a one-word or one-phrase answer rarely earns full marks.',
  grid: {
    perPoint: [
      { id: 'cause', label: 'States the cause', marks: 2 },
      { id: 'link', label: 'Links cause to effect (the “because”)', marks: 3 },
    ],
    shorthand: 'Explain = cause + reasoning',
    ruleNote:
      'On an “Explain” cue the marks are in the reasoning — the sentence that links a cause to the effect. A bare phrase names a factor but doesn’t explain anything, so it can’t earn the reasoning marks.',
    cite: MS('p.6 (Explain cues) and CER 2013 p.24 (full sentences)'),
  },
  scripts: [
    {
      id: 'ch4-a',
      label: 'Script A',
      persona: 'Bare phrase',
      attempts: [
        {
          id: 'ch4-a-1',
          text: '“Bigger molecules.”',
          key: { cause: 2, link: 0 },
          keyNote: 'Names a factor (2), but explains nothing — there’s no sentence linking bigger molecules to stronger forces to a higher boiling point. On “Explain”, the reasoning is where the marks are, and a two-word phrase leaves them behind.',
        },
      ],
      embodies: {
        behaviour: 'Answers an “Explain” cue with a bare phrase — which the report says rarely earns full marks.',
        cite: CER('p.24'),
      },
    },
    {
      id: 'ch4-b',
      label: 'Script B',
      persona: 'Full reasoning',
      attempts: [
        {
          id: 'ch4-b-1',
          text: '“Larger molecules have more electrons, so the van der Waals forces between them are stronger, and more energy is needed to separate them — so the boiling point is higher.”',
          key: { cause: 2, link: 3 },
          keyNote: 'A full explanation: cause (more electrons → stronger forces) linked all the way to the effect (higher boiling point). Full marks — the sentence is what earns the reasoning marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-chem4',
    rule: 'On “Explain”, write the reasoning as a sentence.',
    detail:
      'Describe/Explain cues rarely give full marks to a word or phrase — the marks are in the reasoning that links cause to effect. Write the full “because… so…” sentence, not just the factor’s name.',
    cite: CER('p.24'),
  },
};

// ─────────────── Ch5 · Right formulae, wrong balance ───────────────

const CH5: GridSession = {
  mode: 'grid',
  id: 'chem-balanced-equation',
  subject: 'chemistry',
  level: 'common',
  title: 'Right formulae, wrong balance',
  cue: 'Write a balanced equation',
  question:
    'Write a balanced chemical equation for the reaction of carbon monoxide with iron(III) oxide. The scheme marks it “(4 × 1 + 2)”: one mark for each of the four correct species formulae, plus two marks for correct balancing. A candidate writes “Fe2O3 + CO → Fe + CO2” — every formula right, but no coefficients, so the atoms don’t balance. What survives?',
  questionNote:
    'Scenario authored for this exercise. The mark split “(4 × 1 + 2)” on balanced-equation items is the real SEC shorthand: each species formula is credited on its own (4 × 1), and correct balancing is a separate 2-mark bloc.',
  grid: {
    perPoint: [
      { id: 'formulae', label: 'All four species formulae correct (4 × 1m)', marks: 4 },
      { id: 'balance', label: 'Correctly balanced (coefficients)', marks: 2 },
    ],
    shorthand: '(4 × 1 + 2)',
    ruleNote:
      'On a balanced-equation item the scheme splits the marks: each correct species formula scores one mark (here 4 × 1), and correct balancing is a separate two-mark bloc. Correct formulae bank those marks even when the equation is unbalanced — the balancing marks are the only thing an unbalanced equation forfeits. So a wrong equation is rarely a zero.',
    cite: MS('p.19 (blast-furnace equation, “(4 × 1 + 2)”)'),
  },
  scripts: [
    {
      id: 'ch5-a',
      label: 'Script A',
      persona: 'Correct formulae, unbalanced',
      attempts: [
        {
          id: 'ch5-a-1',
          text: 'Fe2O3 + CO → Fe + CO2  (all four formulae correct, but no coefficients — the atoms don’t balance).',
          key: { formulae: 4, balance: 0 },
          keyNote:
            'Every species formula is right, so the four formula marks are banked (4). The two balancing marks are lost because the coefficients are missing. 4 of 6 — not the zero many candidates fear from an “unbalanced” equation. The examiner credits the formulae you got right regardless of the balance.',
        },
      ],
      embodies: {
        behaviour: 'Writes the correct species formulae but leaves the equation unbalanced — a documented discriminator skill the report flags as often poorly done.',
        cite: CER('p.15'),
      },
    },
    {
      id: 'ch5-b',
      label: 'Script B',
      persona: 'Correct and balanced',
      attempts: [
        {
          id: 'ch5-b-1',
          text: 'Fe2O3 + 3CO → 2Fe + 3CO2  (formulae correct and fully balanced).',
          key: { formulae: 4, balance: 2 },
          keyNote:
            'Correct formulae (4) plus correct balancing (2) — the full 6. The two marks that separate this from Script A are purely the coefficients.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-chem5',
    rule: 'Write the correct formulae even if you can’t balance it.',
    detail:
      'Balanced-equation items are marked “(4 × 1 + 2)”: a mark for each correct species formula, then a separate bloc for balancing. Get the formulae down — they score on their own. An unbalanced equation with the right species forfeits only the balancing marks, not the lot.',
    cite: MS('p.19'),
  },
};

// ─────────────── Ch6 · Units in the final answer ───────────────

const CH6: ScaleSession = {
  mode: 'scale',
  id: 'chem-units',
  subject: 'chemistry',
  level: 'common',
  title: 'Don’t drop the units',
  cue: 'Calculate',
  question:
    'A calculation asks for a concentration. The candidate’s working is right and the final number is right — 0.061 — but they write it as a bare number with no units. The final-answer line is worth 3 marks. What does the missing “mol L–1” cost?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s general rule: omitting (or giving incorrect) units in a final answer is a one-mark deduction, unless otherwise indicated.',
  scale: {
    name: 'Units in the final answer',
    levels: [
      { id: 'm0', label: '0 (value wrong)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (value right, no units)', annotation: '2', marks: 2 },
      { id: 'm3', label: '3 (value + units)', annotation: '3', marks: 3 },
    ],
    notes: [
      '“For omission of appropriate units (or for incorrect units) in final answers, one mark is deducted, unless otherwise indicated.”',
      'The deduction is one mark, once — a correct value with no units still banks the rest.',
      'Incorrect units are treated the same as no units: still −1.',
    ],
    cite: MS('p.3 (point 9, units rule)'),
  },
  scripts: [
    {
      id: 'ch6-a',
      label: 'The answer',
      persona: 'Right number, no units',
      work: ['[Y] = 0.061  (correct value, but written with no units)'],
      keyLevelId: 'm2',
      keyNote:
        'The value is correct, so most of the marks stand — but a final answer with no units drops one mark under the units rule. 2 of 3. Writing “mol L–1” after the number is a free mark you’re throwing away.',
      embodies: {
        behaviour: 'Leaves the units off a correct final answer — the exact omission the units rule docks one mark for.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ch6-b',
      label: 'The answer',
      persona: 'Right number, with units',
      work: ['[Y] = 0.061 mol L–1  (correct value and correct units)'],
      keyLevelId: 'm3',
      keyNote:
        'Same working, same number — but the units are there. Full 3 marks. The only difference from the answer above is the unit, and it’s worth a mark every time.',
    },
  ],
  takeaway: {
    id: 'codex-chem6',
    rule: 'Always write the units on the final answer.',
    detail:
      'Omitting (or getting wrong) the units on a final answer is a one-mark deduction, every calculation, unless the paper says otherwise. The working can be flawless and the number correct — no units still costs a mark. Make writing the unit the last step of every calculation.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ch7 · Draw every atom and bond ───────────────

const CH7: ScaleSession = {
  mode: 'scale',
  id: 'chem-structure',
  subject: 'chemistry',
  level: 'common',
  title: 'Every atom and every bond',
  cue: 'Draw the structure',
  question:
    'A question says “Draw the molecular structure of methylpropane, including all atoms and bonds” — worth 3 marks. A candidate draws the carbon skeleton and every H atom, but leaves out the bonds to the H atoms throughout (a condensed sketch). The scheme deducts one mark for H atoms omitted in a systematic way, and one mark for bonds to H atoms omitted in a systematic way. Where does this land?',
  questionNote:
    'Scenario authored for this exercise. The scheme deducts one mark for systematically omitted H atoms and one mark for systematically omitted bonds to H atoms in organic structure drawings.',
  scale: {
    name: 'Structure: all atoms and bonds',
    levels: [
      { id: 'm1', label: '1 (H atoms and their bonds both omitted)', annotation: '1', marks: 1 },
      { id: 'm2', label: '2 (bonds to H omitted systematically)', annotation: '2', marks: 2 },
      { id: 'm3', label: '3 (all atoms and all bonds shown)', annotation: '3', marks: 3 },
    ],
    notes: [
      '“One mark is deducted if the H atoms are omitted in a systematic way and one mark is deducted if bonds to H atoms are omitted in a systematic way.”',
      'The two deductions are independent: miss the H atoms and miss the bonds to H and you lose two marks, not one.',
      'The question explicitly says “including all atoms and bonds” — a condensed sketch reads as a systematic omission.',
    ],
    cite: MS('p.3 (point 8, structure-drawing deductions)'),
  },
  scripts: [
    {
      id: 'ch7-a',
      label: 'The answer',
      persona: 'Skeleton with H atoms, no H bonds',
      work: [
        'Draws the four-carbon methylpropane skeleton correctly.',
        'Writes every H atom in the right place.',
        'But never draws the C–H bonds — the H atoms just sit beside the carbons throughout.',
      ],
      keyLevelId: 'm2',
      keyNote:
        'The skeleton and the H atoms are all there, so only one deduction applies: the bonds to H are omitted in a systematic way, −1. 2 of 3. Had the H atoms also been missing, it would be −2. Drawing every C–H bond — as the question literally asks — protects that mark.',
      embodies: {
        behaviour: 'Omits the bonds to H atoms systematically in a structure asked for with “all atoms and bonds” — the exact omission point 8 deducts for.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ch7-b',
      label: 'The answer',
      persona: 'Full displayed structure',
      work: [
        'Draws the four-carbon skeleton.',
        'Shows every H atom AND every C–H bond explicitly.',
      ],
      keyLevelId: 'm3',
      keyNote:
        'A fully displayed structure — all atoms, all bonds, nothing implied. Full 3 marks. When the question says “all atoms and bonds”, the displayed formula is the only version that scores everything.',
    },
  ],
  takeaway: {
    id: 'codex-chem7',
    rule: 'Draw the displayed structure — every atom, every bond.',
    detail:
      'When a structure question says “including all atoms and bonds”, condensed sketches lose marks: one deduction for systematically omitted H atoms, another for systematically omitted bonds to H. Draw the fully displayed formula every time, showing each C–H bond.',
    cite: MS('p.3'),
  },
};

export const CHEMISTRY_CHAIR: ChairSubject = {
  id: 'chemistry',
  label: 'Chemistry',
  tagline: 'Precise terms, shown workings and one method at a time.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CH1, CH2, CH3, CH4, CH5, CH6, CH7],
  sources: [
    { label: 'SEC LC Chemistry HL marking scheme 2024 (examiner-reports/chemistry/2024-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Chemistry 2013 (examiner-reports/chemistry/2013-chief-examiner)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — exact-term demands, the Mr rule, the calculation-deduction regime, the units rule, the // method rule, balanced-equation part-marking and organic structure-drawing deductions — which the scheme applies at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme (and re-confirmed in the 2025 scheme); level-specific worked examples are being added.',
};
