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

import { type ChairSubject, type GridSession, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Chemistry HL marking scheme 2024, ${p}` });
const CER = (p: string) => ({ label: `Chief Examiner's Report, Chemistry 2013, ${p}` });

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
    {
      id: 'ch1-border',
      label: 'Script C',
      persona: 'One precise term, one everyday',
      attempts: [
        {
          id: 'ch1-border-1',
          text: 'Effervescence is observed…',
          key: { obs: 3 },
          keyNote: 'The precise term for the gas evolved — “effervescence”, not “bubbles”. This observation earns its full 3 marks: exactly the scientific word the scheme wants.',
        },
        {
          id: 'ch1-border-2',
          text: '…and the solution goes clear.',
          key: { obs: 0 },
          keyNote:
            '“Clear” is the explicitly-rejected everyday word for the second observation — a solution can be clear and still coloured, so it doesn’t report what was seen. This observation scores 0. One precise term, one everyday one: the script lands on exactly 3 of the 6, and it sits on the boundary — a marker swayed by the confident “effervescence” might round it up to full, one snagged by the rejected “clear” might round it down to nothing, but the scheme pins it at the mid mark.',
        },
      ],
      embodies: {
        behaviour: 'Gets one exact term right (“effervescence”) but uses the rejected everyday word (“clear”) for the other — the documented near-synonym error.',
        cite: CER('p.24'),
      },
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
    levels: [
      { id: 'm0', label: '0 (bare wrong Mr, no addition shown)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (addition shown, one-mark slip)', annotation: '2', marks: 2 },
      { id: 'm3', label: '3 (Mr correct)', annotation: '3', marks: 3 },
    ],
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
    {
      id: 'ch2-border',
      label: 'The answer',
      persona: 'Addition shown, one slip',
      work: ['Mr = 12 + (2 × 16) + 2 = 44  (the atomic-mass addition is written out in full; the sum should be 46 — a single arithmetic slip).'],
      keyLevelId: 'm2',
      keyNote:
        'The atomic-mass addition is on the page, so the examiner can see exactly where the arithmetic went astray — that turns the error into a one-mark slip rather than a lost answer. 2 of 3. It sits precisely on the middle rung: the working is right enough to protect two marks, wrong enough to cost one. A marker who reads “46 was intended” could be tempted up to full, and one who sees “44” could be tempted down to zero — but the shown addition pins it at 2, the exact mark the bare-number answer above forfeited.',
      embodies: {
        behaviour: 'Shows the atomic-mass addition but slips in the sum — the one-mark-slip case the Mr rule protects.',
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

// ─────────────── Ch8 · Round the way the question asks ───────────────

const CH8: ScaleSession = {
  mode: 'scale',
  id: 'chem-rounding',
  subject: 'chemistry',
  level: 'common',
  title: 'Round the way it asks',
  cue: 'Calculate',
  question:
    'A rate calculation asks for the answer “correct to three decimal places”. The candidate’s value is arithmetically right — 0.016 — but they write it as 0.02, rounded to two places instead of three. The final-answer line is worth 3 marks. What does the wrong rounding cost?',
  questionNote:
    'Scenario authored for this exercise. Point 7 makes incorrect or inappropriate rounding a one-mark deduction, exactly like an arithmetic slip; Q3(b)(i) demands the rate values “correct to three decimal places”.',
  scale: {
    name: 'Rounding as the question specifies',
    levels: [
      { id: 'm0', label: '0 (value wrong)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (value right, rounded wrong)', annotation: '2', marks: 2 },
      { id: 'm3', label: '3 (value + correct rounding)', annotation: '3', marks: 3 },
    ],
    notes: [
      '“Each time an arithmetical error occurs in a calculation, one mark is deducted; this also applies to inappropriate or incorrect rounding of numerical answers.”',
      'Rounding to the wrong number of places is treated exactly like an arithmetic slip: −1.',
      'Where the question says “correct to three decimal places”, that instruction is part of the mark.',
    ],
    cite: MS('p.3 (point 7, rounding) and p.8 (Q3(b)(i), “correct to three decimal places”)'),
  },
  scripts: [
    {
      id: 'ch8-a',
      label: 'The answer',
      persona: 'Right value, wrong rounding',
      work: ['Rate = 0.016  → writes 0.02 (rounded to two decimal places, when three were asked for)'],
      keyLevelId: 'm2',
      keyNote:
        'The underlying value is correct, so most of the marks stand — but rounding to the wrong number of places is a one-mark deduction under the rounding rule, just like an arithmetic slip. 2 of 3. Reading “correct to three decimal places” as part of the answer, not a suggestion, keeps that mark.',
      embodies: {
        behaviour: 'Rounds a correct value to the wrong number of decimal places — the exact deduction point 7 attaches to “inappropriate or incorrect rounding”.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ch8-b',
      label: 'The answer',
      persona: 'Right value, rounded as asked',
      work: ['Rate = 0.016  (correct value, three decimal places, exactly as the question specifies)'],
      keyLevelId: 'm3',
      keyNote:
        'Same value — but rounded to the three decimal places the question demanded. Full 3 marks. The only difference from the answer above is honouring the “three decimal places” instruction.',
    },
  ],
  takeaway: {
    id: 'codex-chem8',
    rule: 'Round to the precision the question names.',
    detail:
      'Incorrect or inappropriate rounding costs a mark, exactly like an arithmetic slip. When a question says “correct to three decimal places” (or two, or a given significant figure), that instruction is part of the answer — give the value to the precision asked, no more and no less.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ch9 · Answer the number asked, no extras ───────────────

const CH9: ScaleSession = {
  mode: 'scale',
  id: 'chem-cancellation',
  subject: 'chemistry',
  level: 'common',
  title: 'Two asked, three given',
  cue: 'State',
  question:
    'A question says “State two reasons why real gases deviate from ideal behaviour” — 6 marks, 3 per reason. The candidate hedges and writes three reasons: two correct, one wrong. Surely the extra one is harmless? How does cancellation score it?',
  questionNote:
    'Scenario authored for this exercise. Point 1’s cancellation rule: when a candidate gives more than the required number of responses, or a list of correct and incorrect answers, a wrong extra can cancel a correct one.',
  scale: {
    name: 'Cancellation on an over-long list',
    levels: [
      { id: 'm0', label: '0 (no correct reasons stand)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (a correct reason cancelled by the wrong extra)', annotation: '3', marks: 3 },
      { id: 'm6', label: '6 (exactly two correct, no extras)', annotation: '6', marks: 6 },
    ],
    notes: [
      '“Cancellation may apply when a candidate gives more than the required number of responses, or a list of correct and incorrect answers.”',
      'Two reasons were asked for; a third, wrong, reason is an extra response — and it can cancel one of the correct ones.',
      'Writing more than the number asked is not free insurance: it can cost you marks you had already earned.',
    ],
    cite: MS('p.3 (point 1, cancellation) and p.10 (Q4, “[any two]”/“[any three]” lists)'),
  },
  scripts: [
    {
      id: 'ch9-a',
      label: 'The answer',
      persona: 'Hedges with a third reason',
      work: [
        '“Particles have volume.” (correct)',
        '“There are intermolecular forces.” (correct)',
        '“Collisions transfer energy to the walls.” (wrong — an extra, third reason)',
      ],
      keyLevelId: 'm3',
      keyNote:
        'Only two reasons were asked for. The wrong third response triggers cancellation, striking out one of the two correct reasons — so two correct answers net just 3 marks. Stopping at the two the candidate was sure of would have banked the full 6. More is not safer.',
      embodies: {
        behaviour: 'Gives more than the required number of responses, mixing a wrong one in — the exact situation point 1 says cancellation applies to.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ch9-b',
      label: 'The answer',
      persona: 'Two, and only two',
      work: [
        '“Particles have volume.” (correct)',
        '“There are intermolecular forces.” (correct)',
      ],
      keyLevelId: 'm6',
      keyNote:
        'Exactly the two reasons asked for, both correct, nothing extra to cancel. Full 6 marks. The discipline of answering the number asked — not one more — is what protects the score.',
    },
  ],
  takeaway: {
    id: 'codex-chem9',
    rule: 'Give the number of answers asked — no bonus extras.',
    detail:
      'When a question asks for two (or three) things, give exactly that many. A wrong extra doesn’t sit harmlessly beside your right answers — under cancellation it can strike one of them out. Pick your best answers and stop at the number requested.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ch10 · Use the graph paper ───────────────

const CH10: ScaleSession = {
  mode: 'scale',
  id: 'chem-graph-paper',
  subject: 'chemistry',
  level: 'common',
  title: 'Use the graph paper',
  cue: 'Draw a graph',
  question:
    'A question asks for a graph; the plotting is worth 6 marks. One candidate plots every point perfectly — but on ordinary lined paper, not graph paper. Another uses graph paper but misplots a single point. Where does each land?',
  questionNote:
    'Scenario authored for this exercise. Q3(b)(ii) marks the plotting “[–1 for each incorrectly plotted point]” with a hard cap: “[maximum of 3 marks for points plotted on paper other than graph paper]”.',
  scale: {
    name: 'Plotting (6 marks)',
    levels: [
      { id: 'm3', label: '3 (perfect plot, wrong paper — capped)', annotation: '3', marks: 3 },
      { id: 'm5', label: '5 (graph paper, one point misplotted)', annotation: '5', marks: 5 },
      { id: 'm6', label: '6 (graph paper, all points correct)', annotation: '6', marks: 6 },
    ],
    notes: [
      '“Points plotted [–1 for each incorrectly plotted point]” — each stray point is a one-mark deduction, not a wipe-out.',
      '“Maximum of 3 marks for points plotted on paper other than graph paper.” — the cap bites however neat the plot.',
      'Perfect points on the wrong paper score less than a flawed plot on the right paper.',
    ],
    cite: MS('p.8 (Q3(b)(ii), plotting deductions and graph-paper cap)'),
  },
  scripts: [
    {
      id: 'ch10-a',
      label: 'Script A',
      persona: 'Perfect plot, lined paper',
      work: [
        'Plots all six points correctly and neatly.',
        'But draws the whole graph on ordinary lined paper, not the graph paper provided.',
      ],
      keyLevelId: 'm3',
      keyNote:
        'Every point is right, yet the plotting is capped at 3 of 6 because it isn’t on graph paper. The cap is blind to how careful the plot is — using the graph paper provided is worth as much as plotting accurately. Half the marks gone for a choice of paper.',
      embodies: {
        behaviour: 'Plots on paper other than graph paper — hitting the explicit 3-mark cap in the scheme.',
        cite: MS('p.8'),
      },
    },
    {
      id: 'ch10-b',
      label: 'Script B',
      persona: 'Graph paper, one stray point',
      work: [
        'Uses the graph paper provided.',
        'Plots five points correctly; one point is placed slightly wrong.',
      ],
      keyLevelId: 'm5',
      keyNote:
        'On graph paper the per-point rule applies gently: −1 for the single misplotted point, so 5 of 6. One slip is one mark — nothing like the flat cap that the wrong paper triggers. The paper choice mattered more than the stray point.',
    },
  ],
  takeaway: {
    id: 'codex-chem10',
    rule: 'Draw graphs on the graph paper — every point counts, one at a time.',
    detail:
      'A single misplotted point costs one mark. But plotting on anything other than graph paper caps the whole plotting block at 3 — a harsher loss than several stray points. Always use the graph paper provided, and plot each point with care.',
    cite: MS('p.8'),
  },
};

// ─────────────── Ch11 · The sign carries its own mark ───────────────

const CH11: GridSession = {
  mode: 'grid',
  id: 'chem-thermo-sign',
  subject: 'chemistry',
  level: 'common',
  title: 'The sign is worth a mark',
  cue: 'Calculate',
  question:
    'A heat-of-combustion calculation multiplies a heat of formation by a coefficient: 8 × (–393.5) for the CO₂ term. The scheme marks each such term “(2 [multiplicative factor] + 1 [sign])” — two marks for the right factor, a separate mark for the right sign. A candidate computes “8 × 393.5 = 3148” and writes it as +3148, dropping the negative. What survives?',
  questionNote:
    'Scenario authored for this exercise. The “(2 [multiplicative factor] + 1 [sign])” split on Hess-cycle terms is the real SEC shorthand: the arithmetic factor and the sign are marked separately.',
  grid: {
    perPoint: [
      { id: 'factor', label: 'Correct multiplicative factor (coefficient × ΔHf)', marks: 2 },
      { id: 'sign', label: 'Correct sign on the term', marks: 1 },
    ],
    shorthand: '(2 [factor] + 1 [sign])',
    ruleNote:
      'On a Hess-cycle term the scheme splits the marks: two for the right multiplicative factor, one just for the sign. Getting the magnitude right but the sign wrong forfeits only the sign mark — but forfeit it you do. The minus signs on exothermic values are not decoration; each one is worth a mark.',
    cite: MS('p.12 (Q6(d)(i), “(2 [multiplicative factor] + 1 [sign])”)'),
  },
  scripts: [
    {
      id: 'ch11-a',
      label: 'Script A',
      persona: 'Right magnitude, dropped sign',
      attempts: [
        {
          id: 'ch11-a-1',
          text: '8 × 393.5 = 3148  (writes +3148 — the negative sign on the heat of formation is dropped).',
          key: { factor: 2, sign: 0 },
          keyNote:
            'The multiplicative factor is right, so those two marks are banked (2). But the term should be –3148: dropping the sign forfeits the separate sign mark. 2 of 3. Carrying the minus through every exothermic term is a mark per term.',
        },
      ],
      embodies: {
        behaviour: 'Computes the correct magnitude but loses the sign — the exact split the “(2 [factor] + 1 [sign])” marking isolates.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'ch11-b',
      label: 'Script B',
      persona: 'Factor and sign both right',
      attempts: [
        {
          id: 'ch11-b-1',
          text: '8 × (–393.5) = –3148  (correct factor, negative sign carried through).',
          key: { factor: 2, sign: 1 },
          keyNote:
            'Correct factor (2) and the sign carried through (1) — the full 3 for the term. The only difference from Script A is the minus sign, and it is worth a mark on its own.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-chem11',
    rule: 'Carry the sign — it is marked separately.',
    detail:
      'In heat-of-reaction and Hess-cycle calculations, each term is marked “(2 [factor] + 1 [sign])”: the arithmetic and the sign score independently. A right number with the wrong (or missing) sign still drops the sign mark. Write the minus on every exothermic value.',
    cite: MS('p.12'),
  },
};

// ─────────────── Ch12 · Charges are part of the ion ───────────────

const CH12: GridSession = {
  mode: 'grid',
  id: 'chem-ion-charges',
  subject: 'chemistry',
  level: 'common',
  title: 'The charge is the answer',
  cue: 'Write the formula',
  question:
    'A question asks for the chemical formulae of the two metal ions that cause water hardness. The scheme prints the answer “Ca²⁺, Mg²⁺ [charges required] (3 + 3)”. A candidate writes “Ca” and “Mg” — right elements, no charges. How is each marked?',
  questionNote:
    'Scenario authored for this exercise. Where the scheme prints “[charges required]”, the ionic charge is not optional — the neutral-atom symbol does not answer a question that asks for the ion.',
  grid: {
    perPoint: [{ id: 'ion', label: 'Correct ion with its charge', marks: 3 }],
    shorthand: 'ion + charge · 3m each',
    ruleNote:
      'When a question asks for an ion and the scheme prints “[charges required]”, the charge is part of the answer, not a flourish. “Ca” is a neutral atom; “Ca²⁺” is the ion the question asked for. Each ion is marked on its own — leave the charge off one and you lose that ion’s marks while the other still scores.',
    cite: MS('p.18 (Q11(c)(i), “[charges required]”)'),
  },
  scripts: [
    {
      id: 'ch12-a',
      label: 'Script A',
      persona: 'Charge on one ion, not the other',
      attempts: [
        {
          id: 'ch12-a-1',
          text: 'Ca²⁺  (correct ion, charge shown).',
          key: { ion: 3 },
          keyNote: 'The ion is written with its charge — exactly what “[charges required]” demands. 3 marks.',
        },
        {
          id: 'ch12-a-2',
          text: 'Mg  (right element, but no charge).',
          key: { ion: 0 },
          keyNote:
            '“Mg” is the neutral atom, not the ion the question asked for; with “[charges required]” printed, the missing charge costs the whole 3 for this ion. Each ion is marked independently, so this one falls even though the calcium ion scored.',
        },
      ],
      embodies: {
        behaviour: 'Omits the charge on an ion the scheme marks “[charges required]” — writing the atom where the ion was asked for.',
        cite: MS('p.18'),
      },
    },
    {
      id: 'ch12-b',
      label: 'Script B',
      persona: 'Both ions, both charged',
      attempts: [
        {
          id: 'ch12-b-1',
          text: 'Ca²⁺  (correct ion with charge).',
          key: { ion: 3 },
          keyNote: 'Ion and charge both present. 3 marks.',
        },
        {
          id: 'ch12-b-2',
          text: 'Mg²⁺  (correct ion with charge).',
          key: { ion: 3 },
          keyNote: 'The charge that Script A dropped is here. 3 marks — the full 6 across both ions.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-chem12',
    rule: 'When asked for an ion, write the charge.',
    detail:
      'An ion’s charge is part of its formula, and schemes print “[charges required]” to say so. “Na” and “Na⁺” are different species — one is an atom, one is the ion the question asked for. Write the superscript charge every time you name an ion.',
    cite: MS('p.18'),
  },
};

// ─────────────── Ch13 · Square brackets mean concentration ───────────────

const CH13: ScaleSession = {
  mode: 'scale',
  id: 'chem-kc-brackets',
  subject: 'chemistry',
  level: 'common',
  title: 'Square brackets, not round',
  cue: 'Write an expression',
  question:
    'A question asks for the equilibrium-constant expression Kc — worth 6 marks. The candidate gets the ratio exactly right (products over reactants, each raised to the right power) but writes every term in round brackets, ( ), instead of the square brackets, [ ], that mean molar concentration. How does the scheme treat it?',
  questionNote:
    'Scenario authored for this exercise. On the Kc expression the scheme prints “[award 3 marks if round brackets are used]”: square brackets denote concentration, so round brackets score only half.',
  scale: {
    name: 'Kc expression (6 marks)',
    levels: [
      { id: 'm0', label: '0 (ratio wrong)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (right ratio, round brackets)', annotation: '3', marks: 3 },
      { id: 'm6', label: '6 (right ratio, square brackets)', annotation: '6', marks: 6 },
    ],
    notes: [
      '“[award 3 marks if round brackets are used]” — half the marks for the right ratio in the wrong brackets.',
      'Square brackets [X] are the notation for molar concentration; round brackets (X) are not.',
      'The chemistry of the expression is right either way — the notation alone is worth 3 of the 6 marks.',
    ],
    cite: MS('p.13 (Q7(a)(ii), “[award 3 marks if round brackets are used]”)'),
  },
  scripts: [
    {
      id: 'ch13-a',
      label: 'The answer',
      persona: 'Right ratio, round brackets',
      work: ['Kc = (H₂)(CO₂) / (H₂O)(CO)   — correct ratio, but round brackets throughout.'],
      keyLevelId: 'm3',
      keyNote:
        'The ratio is completely correct — products over reactants, right terms — but round brackets aren’t the notation for concentration, so the scheme awards only 3 of 6. Swapping ( ) for [ ] would have doubled the mark for no extra chemistry.',
      embodies: {
        behaviour: 'Writes a correct Kc ratio in round brackets — the exact case the scheme halves to 3 marks.',
        cite: MS('p.13'),
      },
    },
    {
      id: 'ch13-b',
      label: 'The answer',
      persona: 'Right ratio, square brackets',
      work: ['Kc = [H₂][CO₂] / [H₂O][CO]   — correct ratio in square brackets.'],
      keyLevelId: 'm6',
      keyNote:
        'Same ratio, but written with square brackets — the notation for molar concentration. Full 6 marks. The only difference from the answer above is the shape of the brackets, and it is worth 3 marks.',
    },
  ],
  takeaway: {
    id: 'codex-chem13',
    rule: 'Write concentrations in square brackets.',
    detail:
      'In equilibrium-constant expressions, [X] means the molar concentration of X — round brackets do not. A correct Kc ratio in round brackets scores only half. Use square brackets for every concentration term.',
    cite: MS('p.13'),
  },
};

// ─────────────── Ch14 · Colour change has a direction ───────────────

const CH14: ScaleSession = {
  mode: 'scale',
  id: 'chem-colour-direction',
  subject: 'chemistry',
  level: 'common',
  title: 'Which way the colour changes',
  cue: 'State the colour change',
  question:
    'A question asks for the colour change at the end point — marked as two colours, 3 for the starting colour and 3 for the final colour. A candidate names both correct colours but states the change the wrong way round (final → starting). The scheme prints “[award 3 marks for both correct colours reversed]”. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. A colour change is marked as a from-colour and a to-colour; the scheme’s “[award 3 marks for both correct colours reversed]” note halves the marks when the direction is reversed.',
  scale: {
    name: 'Colour change (6 marks)',
    levels: [
      { id: 'm0', label: '0 (colours wrong or vague)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (both colours right, direction reversed)', annotation: '3', marks: 3 },
      { id: 'm6', label: '6 (both colours right, correct direction)', annotation: '6', marks: 6 },
    ],
    notes: [
      'A colour change is two marks-blocs: the starting colour and the final colour, 3 each.',
      '“[award 3 marks for both correct colours reversed]” — right colours, wrong direction, scores only half.',
      'Knowing the two colours isn’t enough; the from → to direction is half the marks.',
    ],
    cite: MS('p.6 (Q1(c)(ii), “[award 3 marks for both correct colours reversed]”)'),
  },
  scripts: [
    {
      id: 'ch14-a',
      label: 'The answer',
      persona: 'Right colours, wrong way round',
      work: ['“Colourless to pink.”  (both colours correct, but the change actually runs pink → colourless).'],
      keyLevelId: 'm3',
      keyNote:
        'Both colours are right, so the candidate clearly knows the chemistry — but the direction is reversed, and the scheme awards just 3 of 6 for correct colours the wrong way round. Stating the change in the order it actually happens is the other half of the mark.',
      embodies: {
        behaviour: 'Names both correct colours but reverses the direction — the exact case the “colours reversed” note halves.',
        cite: MS('p.6'),
      },
    },
    {
      id: 'ch14-b',
      label: 'The answer',
      persona: 'Right colours, right direction',
      work: ['“Pink to colourless.”  (both colours correct, in the direction the change actually occurs).'],
      keyLevelId: 'm6',
      keyNote:
        'The same two colours, stated in the right order. Full 6 marks. The direction — from-colour then to-colour — is worth as much as knowing the colours at all.',
    },
  ],
  takeaway: {
    id: 'codex-chem14',
    rule: 'State a colour change in the right direction.',
    detail:
      'A colour change is marked as “from X to Y” — the starting colour and the final colour each carry marks. Naming both correct colours but reversing the direction scores only half. Always state the change in the order it happens: original colour first, final colour second.',
    cite: MS('p.6'),
  },
};

// ─────────────── Ch15 · When only the name will do ───────────────

const CH15: GridSession = {
  mode: 'grid',
  id: 'chem-name-not-formula',
  subject: 'chemistry',
  level: 'common',
  title: 'When only the name counts',
  cue: 'Name the compound',
  question:
    'A question says “Name the inorganic compound eliminated.” Generally a scheme accepts either the name or the formula — but here it prints the answer “hydrogen chloride [do not accept HCl or hydrochloric acid]”. A candidate writes “HCl”. How does it score?',
  questionNote:
    'Scenario authored for this exercise. Point 6 lets a name or formula answer an identification “unless otherwise indicated” — and Q8(c)(ii) indicates otherwise, rejecting the formula when the cue is “Name”.',
  grid: {
    perPoint: [{ id: 'name', label: 'Correct name (as the question demands)', marks: 3 }],
    shorthand: 'name only · 3m',
    ruleNote:
      'Point 6 usually lets you answer an identification with either the name or the formula. But that holds only “unless otherwise indicated” — and a “Name …” cue with “[do not accept HCl …]” printed is exactly that indication. When the question asks you to name a compound and rejects the formula, the formula scores zero however correct it is.',
    cite: MS('p.3 (point 6, name/formula) and p.14 (Q8(c)(ii), “[do not accept HCl …]”)'),
  },
  scripts: [
    {
      id: 'ch15-a',
      label: 'Script A',
      persona: 'Gives the formula',
      attempts: [
        {
          id: 'ch15-a-1',
          text: '“HCl.”',
          key: { name: 0 },
          keyNote:
            'The formula is chemically right, but the cue was “Name …” and the scheme prints “[do not accept HCl or hydrochloric acid]”. That is the “unless otherwise indicated” exception to the name-or-formula rule — so the formula scores 0. Reading the cue tells you which form is wanted.',
        },
      ],
      embodies: {
        behaviour: 'Answers a “Name …” cue with a formula the scheme explicitly refuses — missing the “unless otherwise indicated” limit on the name-or-formula rule.',
        cite: MS('p.14'),
      },
    },
    {
      id: 'ch15-b',
      label: 'Script B',
      persona: 'Gives the name',
      attempts: [
        {
          id: 'ch15-b-1',
          text: '“Hydrogen chloride.”',
          key: { name: 3 },
          keyNote: 'The name the “Name …” cue asked for — and the one form the scheme accepts here. 3 marks.',
        },
      ],
    },
    {
      id: 'ch15-border',
      label: 'Script C',
      persona: 'Names one, formula-s the other',
      attempts: [
        {
          id: 'ch15-border-1',
          text: '“Water.”',
          key: { name: 3 },
          keyNote: 'The compound written as its name — the form a “Name …” cue asks for, and here nothing bars it. This identification earns its full 3 marks.',
        },
        {
          id: 'ch15-border-2',
          text: '“HCl.”',
          key: { name: 0 },
          keyNote:
            'For the second eliminated compound the candidate reverts to the formula — and this is where the scheme prints “[do not accept HCl]”. A “Name …” cue plus that note is the “unless otherwise indicated” exception to the name-or-formula rule, so the formula scores 0. One named, one formula-d: 3 of the 6, and the script balances on the edge — the marker who credits the chemically-correct “HCl” pushes it up to full, the one who reads a stray formula as spoiling the answer pushes it down to zero, but the scheme fixes it at the middle.',
        },
      ],
      embodies: {
        behaviour: 'Names one eliminated compound but gives the other as a formula the scheme explicitly refuses — the “unless otherwise indicated” limit on the name-or-formula rule.',
        cite: MS('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-chem15',
    rule: 'Read the cue: “Name” can mean the formula won’t do.',
    detail:
      'You may usually identify a substance by name or formula — but only “unless otherwise indicated”. A “Name the compound …” cue can reject the formula outright (e.g. “[do not accept HCl]”). When the question says name, write the word, not the symbols.',
    cite: MS('p.3'),
  },
};

export const CHEMISTRY_CHAIR: ChairSubject = {
  id: 'chemistry',
  label: 'Chemistry',
  tagline: 'Precise terms, shown workings, the right notation and one method at a time.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15],
  sources: [
    { label: 'SEC LC Chemistry HL marking scheme 2024 (examiner-reports/chemistry/2024-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Chemistry 2013 (examiner-reports/chemistry/2013-chief-examiner)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — exact-term demands, the Mr rule, the calculation-deduction regime (arithmetic slips, rounding and precision), the units rule, the // method rule, cancellation on over-long lists, balanced-equation part-marking, organic structure-drawing deductions, the multiplicative-factor-plus-sign split in thermochemistry, ionic charges, square-bracket concentration notation, colour-change direction, graph-plotting deductions and the name-vs-formula rule — which the scheme applies at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme (with cancellation, the rounding clause, the factor-plus-sign split and the round-brackets rule re-confirmed in the 2025 scheme); level-specific worked examples are being added.',
};
