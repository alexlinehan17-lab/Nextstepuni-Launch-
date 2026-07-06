/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Applied Mathematics (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the blunder −3 / slip −1 / misreading −1 penalty tariff, the
 * oversimplifying-slip upgrade, the systemic-error scale floor, and the mark
 * for naming a correct method) is the real SEC system, cited to:
 *  - SEC LC Applied Mathematics HL marking scheme 2024 —
 *    examiner-reports/applied-maths/2024-marking-scheme.*
 * Applied Maths uses neither the Maths A–D scales nor the Physics granule
 * ladder — it is the "blunders / slips / misreadings" subtractive system.
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Applied Mathematics HL marking scheme 2024, ${p}` });
const MS23 = (p: string) => ({ label: `SEC Applied Mathematics HL marking scheme 2023, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── AM1 · Blunder vs slip ───────────────

const AM1: ScaleSession = {
  mode: 'scale',
  id: 'am-blunder-slip',
  subject: 'applied-maths',
  level: 'common',
  title: 'A blunder costs three times a slip',
  cue: 'Solve',
  question: 'A 10-mark part is marked by the penalty system: a mathematical error (“blunder”) is −3, a numerical slip is −1. Two candidates each make one mistake — one a blunder (wrong equation of motion), one a slip (arithmetic). Otherwise both are correct. Where does the SLIP answer land?',
  questionNote:
    'Scenario authored for this exercise. Applied Maths uses a subtractive penalty tariff: blunder −3, slip −1, misreading −1 — applied down from full marks.',
  scale: {
    name: 'Penalty tariff · /10',
    levels: ladder([7, 9]),
    notes: [
      'Penalties are subtracted from full marks: blunder −3, slip −1, misreading −1.',
      'A single numerical slip on this 10-mark part → 10 − 1 = 9.',
      'The same answer with a blunder instead would be 10 − 3 = 7.',
      'The method you set up matters three times as much as the arithmetic.',
    ],
    cite: MS('p.3 (instruction 4, penalty tariff)'),
  },
  scripts: [
    {
      id: 'am1-a',
      label: 'The answer',
      persona: 'One arithmetic slip',
      work: ['Correct method and setup.', 'One arithmetic slip near the end.'],
      keyLevelId: 'm9',
      keyNote:
        '9 of 10 — a slip is only −1. Had the mistake been a blunder (a wrong equation of motion, a wrong principle), the same script would score 7. This is the key to Applied Maths: guard the method fiercely — a setup error costs three times what a number-crunching slip does.',
      embodies: {
        behaviour: 'Makes a numerical slip (−1), far cheaper than a method blunder (−3).',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am1',
    rule: 'Protect the method — a blunder costs 3× a slip.',
    detail:
      'Applied Maths subtracts penalties: a method blunder is −3, an arithmetic slip only −1. Spend your care on setting up the right equations and principles; a small number slip barely dents the mark, but a wrong method triples the loss.',
    cite: MS('p.3'),
  },
};

// ─────────────── AM2 · The scale floor ───────────────

const AM2: ScaleSession = {
  mode: 'scale',
  id: 'am-scale-floor',
  subject: 'applied-maths',
  level: 'common',
  title: 'A real attempt always banks something',
  cue: 'Solve',
  question: 'A 30-mark part is marked on a systemic-error scale: 27 / 24 / 16 / 8 for one error / two errors / more than two errors / a valid attempt. A candidate makes several errors but shows a genuine, relevant method throughout. What is the floor they can’t drop below?',
  questionNote:
    'Scenario authored for this exercise. On higher-value items Applied Maths uses a systemic-error scale, where any valid attempt banks the bottom rung and evident method with several errors still scores well above zero.',
  scale: {
    name: 'Systemic-error scale · /30',
    levels: ladder([8, 16, 24, 27]),
    notes: [
      'Scale: 27 (one error) / 24 (two) / 16 (more than two) / 8 (valid attempt).',
      'Even with more than two errors, evident relevant method scores 16.',
      'Any valid attempt banks the bottom rung — 8 of 30.',
      'So a genuine attempt is never worth zero on these items.',
    ],
    cite: MS('p.3, p.13 (systemic-error marking scales)'),
  },
  scripts: [
    {
      id: 'am2-a',
      label: 'The answer',
      persona: 'Messy, but a real attempt',
      work: [
        'A genuine, relevant method set up and pursued.',
        'Several errors along the way — more than two.',
      ],
      keyLevelId: 'm16',
      keyNote:
        'Still 16 of 30, because evident relevant method with more-than-two errors sits on that rung — and even a bare valid attempt would bank 8. The lesson: never scribble out a genuine attempt or leave the part blank. On the scale, a real try is worth well over half; nothing is worth nothing.',
      embodies: {
        behaviour: 'Shows a valid method with several errors — the systemic-error scale still banks a substantial floor.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am2',
    rule: 'A genuine attempt always banks a floor.',
    detail:
      'On Applied Maths scale items, any valid attempt scores the bottom rung and evident method with several errors still scores well above zero. Never blank a part or scrub out a real attempt — a messy try is worth far more than a clean blank.',
    cite: MS('p.3'),
  },
};

// ─────────────── AM3 · Name the method ───────────────

const AM3: ScaleSession = {
  mode: 'scale',
  id: 'am-name-method',
  subject: 'applied-maths',
  level: 'common',
  title: 'Name the method, bank the marks',
  cue: 'State the algorithm',
  question: 'A part asks the candidate to apply a named algorithm. Short on time, the candidate simply writes the correct name of the algorithm and does no further work. The scheme allows 3 marks for the name of a correct algorithm even with no other work. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme states: allow 3 marks for the name of a correct algorithm if no other work is presented (and its omission is a specific −3).',
  scale: {
    name: 'Name of algorithm',
    levels: ladder([0, 3]),
    notes: [
      '“Allow 3 marks for the name of a correct algorithm if no other work is presented.”',
      'So naming the right method banks marks even with nothing worked out.',
      'Conversely, omitting the name where it’s required is a specific −3.',
    ],
    cite: MS('p.6 (3 marks for naming a correct algorithm)'),
  },
  scripts: [
    {
      id: 'am3-a',
      label: 'The answer',
      persona: 'Just the name',
      work: ['Writes the correct name of the algorithm.', 'No further working (out of time).'],
      keyLevelId: 'm3',
      keyNote:
        '3 marks for the name alone — free marks banked under time pressure. Knowing what the method is called is worth writing down even when you can’t finish it, and forgetting the name where it’s required actually costs 3. When time is tight, name the method before you move on.',
      embodies: {
        behaviour: 'Writes only the correct algorithm name — which banks 3 marks on its own.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am3',
    rule: 'Naming the right method banks marks on its own.',
    detail:
      'Applied Maths gives 3 marks for naming a correct algorithm even with no working — and omitting the name where required costs 3. Under time pressure, always write down what the method is called before moving on.',
    cite: MS('p.6'),
  },
};

// ─────────────── AM4 · The slip that makes it easier ───────────────

const AM4: ScaleSession = {
  mode: 'scale',
  id: 'am-oversimplify',
  subject: 'applied-maths',
  level: 'common',
  title: 'A mistake that makes it easier is a blunder',
  cue: 'Solve',
  question: 'On a 10-mark part, a candidate drops a term early on. It looks like a one-mark slip — but losing that term makes the rest of the problem much easier to solve. The scheme says a slip or misreading that oversimplifies the question is treated as a blunder. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Instruction 5: “A misreading or slip or omission which oversimplifies the question may be regarded as equivalent to a mathematical error and is marked accordingly” — i.e. upgraded from −1 to −3.',
  scale: {
    name: 'Oversimplifying slip · /10',
    levels: ladder([7, 9]),
    notes: [
      'A normal slip is −1; a mathematical blunder is −3.',
      'But a slip, misreading or omission that OVERSIMPLIFIES the question is upgraded to a blunder.',
      'So dropping a term that makes the rest easier costs −3, not −1: 10 − 3 = 7.',
    ],
    cite: MS('p.3 (instruction 5, oversimplification upgrade)'),
  },
  scripts: [
    {
      id: 'am4-a',
      label: 'The answer',
      persona: 'Slip that simplifies the problem',
      work: ['One dropped term early in the working.', 'Losing it makes the remaining problem substantially easier.', 'The rest is carried through correctly.'],
      keyLevelId: 'm7',
      keyNote:
        'Only 7 of 10 — because the slip made the problem easier, it’s treated as a blunder, not a −1 slip. The examiner asks whether your mistake left the problem as hard as it was set: if it quietly removed the difficult part, you solved an easier question and are marked accordingly. When you drop or misread a term, check you haven’t cut out the hard bit.',
      embodies: {
        behaviour: 'Makes a slip that oversimplifies the question — upgraded from −1 to a −3 blunder.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am4',
    rule: 'A mistake that makes the problem easier is a blunder.',
    detail:
      'In Applied Maths a slip, misreading or omission that oversimplifies the question is upgraded from −1 to −3 — because you solved an easier problem than the one set. When you drop a term or misread, check you haven’t removed the difficulty; if you have, expect the bigger penalty.',
    cite: MS('p.3'),
  },
};

// ─────────────── AM5 · Different valid attempts (the solidus) ───────────────

const AM5: ScaleSession = {
  mode: 'scale',
  id: 'am-different-attempts',
  subject: 'applied-maths',
  level: 'common',
  title: 'Your method doesn’t have to match the model',
  cue: 'Solve',
  question: 'A 15-mark graph part asks for a minimum spanning tree. The scheme prints the model answer using Kruskal’s algorithm. A candidate builds the same tree correctly using Prim’s algorithm instead. Anxious it isn’t the “expected” method, they wonder if it’s docked. What does a fully-correct alternative method score?',
  questionNote:
    'Scenario authored for this exercise. Instruction 3: “A solidus (/) indicates different valid attempts”, and the scheme prints the model minimum-spanning-tree answer in two columns — Kruskal’s and Prim’s — as equally valid.',
  scale: {
    name: 'Valid alternative method · /15',
    levels: ladder([12, 15]),
    notes: [
      'Instruction 3: “A solidus (/) indicates different valid attempts.”',
      'The scheme shows one correct solution, but “alternative valid answers are acceptable”.',
      'A different but fully-correct method is NOT an error — it scores full marks (15), not the one-error rung (12).',
      'Using Prim’s where the model shows Kruskal’s loses nothing.',
    ],
    cite: MS('p.3 (instruction 3, solidus = different valid attempts); p.6 (MST shown as Kruskal / Prim)'),
  },
  scripts: [
    {
      id: 'am5-a',
      label: 'The answer',
      persona: 'Right tree, different algorithm',
      work: ['Builds the correct minimum spanning tree.', 'Uses Prim’s algorithm; the model solution used Kruskal’s.'],
      keyLevelId: 'm15',
      keyNote:
        'Full 15 — a valid alternative method is not a systemic error, so it never drops to the 12 rung. The scheme states plainly that it shows only one correct solution and that alternative valid answers are acceptable; the solidus in the model answers is there precisely because more than one route is right. Solve it the way you know cleanly; don’t burn time converting to the “expected” method.',
      embodies: {
        behaviour: 'Uses a valid alternative method to the model solution — which earns full marks, not a reduced scale.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am5',
    rule: 'A different valid method earns full marks.',
    detail:
      'The Applied Maths scheme shows one correct solution but states alternative valid answers are acceptable — the solidus (/) in the model answers marks genuinely different valid attempts. A fully-correct method that isn’t the “expected” one is not an error and loses nothing. Solve it your way; don’t convert to match the model.',
    cite: MS('p.3'),
  },
};

// ─────────────── AM6 · Per-item deduction on a listing question ───────────────

const AM6: ScaleSession = {
  mode: 'scale',
  id: 'am-per-item-deduction',
  subject: 'applied-maths',
  level: 'common',
  title: 'On a list, each wrong entry costs just one',
  cue: 'List',
  question: 'A 10-mark question asks the candidate to fill a dependency table with twelve entries (activities A to L). It is NOT marked on a systemic-error scale — the scheme deducts 1 mark for each incorrect entry. A candidate fills in all twelve rows and gets three of them wrong. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The 2023 scheme marks this listing item “10” with the instruction “–1 for each incorrect part A to L” — a linear per-entry deduction, not the banded systemic-error scale.',
  scale: {
    name: 'Per-item deduction · /10',
    levels: ladder([7, 9, 10]),
    notes: [
      'This listing item is marked “–1 for each incorrect part A to L”, not on the systemic-error scale.',
      'So each wrong entry costs exactly 1 mark: one wrong → 9, two wrong → 8, three wrong → 7.',
      'A blank row scores nothing and can never gain — a guessed row costs only 1 if wrong.',
      'Fill in every row: the expected value of attempting always beats leaving it blank.',
    ],
    cite: MS23('p.15 (Q9(i), “–1 for each incorrect part A to L”)'),
  },
  scripts: [
    {
      id: 'am6-a',
      label: 'The answer',
      persona: 'Full table, three slips',
      work: ['Fills in all twelve dependency rows, A to L.', 'Three of the entries are incorrect.'],
      keyLevelId: 'm7',
      keyNote:
        '7 of 10 — three wrong entries at −1 each. Because this item deducts per entry rather than banding on a scale, the arithmetic is simply full marks minus the number of wrong rows. That flips the usual instinct: never leave a row blank to “play safe”, because a blank banks nothing while a wrong guess costs only 1. On per-item listing questions, attempt every single row.',
      embodies: {
        behaviour: 'Attempts every entry on a per-item-deduction listing question, where each wrong entry costs only 1 mark.',
        cite: MS23('p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am6',
    rule: 'On per-item lists, fill every row — each wrong one costs only 1.',
    detail:
      'Some Applied Maths listing/table items are marked “–1 for each incorrect part”, not on the banded scale. Each wrong entry costs exactly one mark and a blank gains nothing, so the expected value of attempting every row always beats leaving gaps. Never leave a row blank to play safe.',
    cite: MS23('p.15'),
  },
};

// ─────────────── AM7 · The free-body diagram is worth marks ───────────────

const AM7: ScaleSession = {
  mode: 'scale',
  id: 'am-force-diagram',
  subject: 'applied-maths',
  level: 'common',
  title: 'The force diagram is a scoring part, not scaffolding',
  cue: 'Draw',
  question: 'The first part of a mechanics question, 2(a)(i), asks only for a labelled force diagram of the system — no equations. The scheme allocates it 10 marks. A candidate treats it as rough working and jumps straight to the equations of motion. What was on the table for the diagram alone?',
  questionNote:
    'Scenario authored for this exercise. In the 2024 scheme, part 2(a)(i) — a labelled force (free-body) diagram — is allocated 10 marks in its own right, before any equation is written.',
  scale: {
    name: 'Force diagram · /10',
    levels: ladder([0, 9, 10]),
    notes: [
      'The diagram-only part 2(a)(i) is worth 10 marks on its own.',
      'A complete, correctly-labelled force diagram banks all 10.',
      'One missing or mislabelled force is a slip: 10 − 1 = 9.',
      'Skipping the diagram to start on the equations forfeits the whole 10.',
    ],
    cite: MS('p.7 (Q2(a)(i), labelled force diagram allocated 10 marks)'),
  },
  scripts: [
    {
      id: 'am7-a',
      label: 'The answer',
      persona: 'Draws the full diagram first',
      work: ['Draws every force acting on the system.', 'Labels each — weights, tensions, reaction, friction — correctly.'],
      keyLevelId: 'm10',
      keyNote:
        'Full 10 — the diagram is its own marked part, not scaffolding for the equations. Every force present and correctly labelled banks the lot; a single missing or mislabelled force would be a −1 slip (9), and skipping the sketch to dive into the equations of motion forfeits all 10. Always draw the labelled force diagram first: it is often the easiest marks in the question.',
      embodies: {
        behaviour: 'Draws a complete, correctly-labelled force diagram — a standalone marked part worth 10.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am7',
    rule: 'Draw the labelled force diagram — it banks marks on its own.',
    detail:
      'In Applied Maths mechanics questions the labelled force (free-body) diagram is a scoring part in its own right — up to 10 marks before a single equation is written. Treat it as an answer, not rough scaffolding: draw every force and label it, and never skip it to jump to the equations.',
    cite: MS('p.7'),
  },
};

// ─────────────── AM8 · Box 2 — the partial-credit annotation ───────────────

const AM8: ScaleSession = {
  mode: 'scale',
  id: 'am-box-two',
  subject: 'applied-maths',
  level: 'common',
  title: 'A part-right step still banks two',
  cue: 'Solve',
  question: 'On a 5-mark step a candidate gets the idea partly right — the method is on the correct track but the element is not fully correct. The examiner’s annotation palette includes “Box 2 · Partially correct element — award 2 marks.” What does a partially-correct element score?',
  questionNote:
    'Scenario authored for this exercise. The 2024 scheme’s annotation table (instruction 8) lists a “Box 2” mark: “Partially correct element – award 2 marks.”',
  scale: {
    name: 'Partial-credit step · /5',
    levels: ladder([0, 2, 5]),
    notes: [
      'The annotation palette includes “Box 2 · Partially correct element – award 2 marks.”',
      'A fully-correct element on this step banks all 5.',
      'A partially-correct element is not zero — the examiner boxes a 2.',
      'Nothing creditable scores 0.',
    ],
    cite: MS('p.4 (instruction 8, “Box 2 · partially correct element – award 2 marks”)'),
  },
  scripts: [
    {
      id: 'am8-a',
      label: 'The answer',
      persona: 'Half-right step',
      work: ['Sets the step up on the right lines.', 'The element is only partially correct, not complete.'],
      keyLevelId: 'm2',
      keyNote:
        'The examiner boxes a 2 — a partially-correct element is explicitly worth 2 marks, not zero. That is why you write down the part you can do even when you can’t finish the step: “nearly right” is a scoring category with its own annotation, and a half-built step banks two marks a blank never would.',
      embodies: {
        behaviour: 'Presents a partially-correct element, which the “Box 2” annotation credits with 2 marks rather than 0.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am8',
    rule: 'A partially-correct step banks two marks — write it down.',
    detail:
      'The Applied Maths annotation palette has a “Box 2” mark: a partially-correct element earns 2 marks, not zero. Half-right work is a scoring category in its own right, so always put down the part of a step you can do rather than leaving it blank.',
    cite: MS('p.4'),
  },
};

// ─────────────── AM9 · The 10-mark scale collapses after one error ───────────────

const AM9: ScaleSession = {
  mode: 'scale',
  id: 'am-ten-scale-collapse',
  subject: 'applied-maths',
  level: 'common',
  title: 'On a 10-mark scale, the ladder collapses after one error',
  cue: 'Solve',
  question: 'A 10-mark item is marked on a systemic-error scale: 7 marks for one systemic error, and 4 marks for two systemic errors OR for a valid attempt that can’t score higher. A candidate makes two systemic errors. Where do they land — and how does that compare with someone who barely attempted it?',
  questionNote:
    'Scenario authored for this exercise. Instruction 6 gives the 10-mark scale as: “7 marks … one systemic error. 4 marks … two systemic errors or where a valid attempt is presented which cannot be awarded higher marks.”',
  scale: {
    name: '10-mark systemic-error scale',
    levels: ladder([4, 7, 10]),
    notes: [
      'Full marks (no systemic error) = 10.',
      'One systemic error drops it to 7.',
      'Two systemic errors → 4 — the SAME rung as a bare valid attempt.',
      'So after the first error, a second one costs no more than barely attempting: the ladder collapses.',
    ],
    cite: MS('p.3 (instruction 6, 10-mark scale 7/4); p.6 (Q1(a) “10 [0/4/7]”)'),
  },
  scripts: [
    {
      id: 'am9-a',
      label: 'The answer',
      persona: 'Two systemic errors',
      work: ['A recognisable method throughout.', 'Two systemic errors along the way.'],
      keyLevelId: 'm4',
      keyNote:
        '4 of 10 — because on the 10-mark scale “two systemic errors” and “a valid attempt” sit on the very same rung. Your first slip in the method is the expensive one (10 → 7); after that, a second error drops you to the floor a bare attempt already banks. The lesson: fight hardest to keep the first systemic error from happening — once you are past one, the marks fall away in a single step, not gradually.',
      embodies: {
        behaviour: 'Makes two systemic errors on a 10-mark scale item, landing on the same 4 rung as a bare valid attempt.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am9',
    rule: 'On a 10-mark scale, guard your first error — after it the ladder collapses.',
    detail:
      'The 10-mark systemic-error scale is 7 (one error) then 4 (two errors, or a bare valid attempt). The first systemic error is the costly one; a second drops you to the same floor a minimal attempt banks. Concentrate on getting the method through cleanly the first time.',
    cite: MS('p.3'),
  },
};

// ─────────────── AM10 · The 20-mark scale has no method-rescue rung ───────────────

const AM10: ScaleSession = {
  mode: 'scale',
  id: 'am-twenty-scale-cliff',
  subject: 'applied-maths',
  level: 'common',
  title: 'On a 20-mark scale there is no method-rescue rung',
  cue: 'Solve',
  question: 'A 20-mark item is marked on a systemic-error scale: 17 for one systemic error, 14 for two, and 8 for a valid attempt that can’t score higher. Unlike the 30-mark scale, there is NO middle rung for “more than two errors but method evident.” A candidate’s work shows a third systemic error. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Instruction 6 gives the 20-mark scale as 17 / 14 / 8 — with no “>2 errors with method” rung between 14 and the 8 floor.',
  scale: {
    name: '20-mark systemic-error scale',
    levels: ladder([8, 14, 17, 20]),
    notes: [
      'Full marks (no systemic error) = 20.',
      'One systemic error = 17; two systemic errors = 14.',
      'There is no rung between 14 and 8 — the 20-mark scale omits the “>2 errors, method evident” level the 30-mark scale keeps.',
      'So a third systemic error drops you straight from 14 to the 8 floor: a six-mark cliff.',
    ],
    cite: MS('p.3 (instruction 6, 20-mark scale 17/14/8); p.15 (Q10(a)(i) “20 [0/8/14/17]”)'),
  },
  scripts: [
    {
      id: 'am10-a',
      label: 'The answer',
      persona: 'A third systemic error',
      work: ['A valid method carried through.', 'Three systemic errors in the work.'],
      keyLevelId: 'm8',
      keyNote:
        '8 of 20 — the floor. On the 20-mark scale there is no cushioning rung between two errors (14) and the valid-attempt floor (8), so the third error costs a full six marks in one drop. This is the opposite of the 30-mark scale, which keeps a 16-mark rung for method-with-many-errors; on a 20-mark item you cannot rely on that rescue, so a clean two-error ceiling is worth defending hard.',
      embodies: {
        behaviour: 'Makes a third systemic error on a 20-mark scale item, which drops straight to the 8 floor because there is no intermediate rung.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am10',
    rule: 'The 20-mark scale has no method-rescue rung — a third error is a cliff.',
    detail:
      'The 20-mark systemic-error scale runs 17 / 14 / 8 with nothing between two errors and the valid-attempt floor. Unlike the 30-mark scale (which keeps a 16 rung for evident method with many errors), a third systemic error here drops you a full six marks in one step. Keep your error count to two on these items.',
    cite: MS('p.3'),
  },
};

// ─────────────── AM11 · Mark to the bracket printed beside the item ───────────────

const AM11: ScaleSession = {
  mode: 'scale',
  id: 'am-fifteen-bracket',
  subject: 'applied-maths',
  level: 'common',
  title: 'Mark to the bracket printed beside the item',
  cue: 'Solve',
  question: 'A 15-mark item is printed in the scheme as “15 [0/6/9/12].” But the general instructions’ 15-mark scale lists only two credit rungs — 12 and 6. A candidate’s work is rated one rung above the valid-attempt floor. On which ladder is it marked — the general table, or the bracket beside the item?',
  questionNote:
    'Scenario authored for this exercise. Instruction 6 gives a general 15-mark scale (12 / 6), but body items such as Q1(b)(i) are printed “15 [0/6/9/12]” — a finer ladder carrying a 9 rung the general table omits.',
  scale: {
    name: '15-mark item scale',
    levels: ladder([6, 9, 12, 15]),
    notes: [
      'The general 15-mark scale in instruction 6 lists only 12 and 6.',
      'But this item is printed “15 [0/6/9/12]” — it carries an extra 9 rung.',
      'The bracket beside the item is authoritative: it can be finer (more generous) than the general table.',
      'Work the examiner rates on that middle rung banks 9 — a level the general table doesn’t even offer.',
    ],
    cite: MS('p.6 (Q1(b)(i) “15 [0/6/9/12]”); p.3 (instruction 6, general 15-mark scale 12/6)'),
  },
  scripts: [
    {
      id: 'am11-a',
      label: 'The answer',
      persona: 'Rated on the printed 9 rung',
      work: ['A valid method with recognisable structure.', 'The examiner places it one rung above the valid-attempt floor — on the printed 9.'],
      keyLevelId: 'm9',
      keyNote:
        '9 of 15 — off the bracket printed beside the item, not the coarser general table (which would offer only 12 or 6). Applied Maths prints a per-item ladder wherever the standard scale doesn’t fit, and that bracket governs; here it carries a 9 rung the general instructions never list, quietly banking three extra marks. Always read the [ … ] beside the mark total: it is the ladder you are actually marked on.',
      embodies: {
        behaviour: 'Is marked on the per-item “[0/6/9/12]” bracket rather than the general 15-mark table, banking a 9 rung the general table omits.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am11',
    rule: 'The bracket beside the item is the ladder you’re marked on.',
    detail:
      'Where a scale item prints its own bracket (e.g. “15 [0/6/9/12]”), that per-item ladder — not the coarser general table in the instructions — governs the marking, and it can carry finer, more generous rungs. Read the bracket next to the mark total to know the real credit steps.',
    cite: MS('p.6'),
  },
};

// ─────────────── AM12 · The Irish-medium bonus rounds down ───────────────

const AM12: ScaleSession = {
  mode: 'scale',
  id: 'am-irish-bonus',
  subject: 'applied-maths',
  level: 'common',
  title: 'Answer through Irish, and the bonus rounds down',
  cue: 'Solve',
  question: 'A candidate answers the entire written paper through Irish and scores 290 of 400 (below 75%). The scheme awards a 5% bonus on marks obtained at this level — and states decimals are “always rounded down, not up.” 5% of 290 is 14.5. What bonus, and total, is recorded?',
  questionNote:
    'Scenario authored for this exercise. Instruction 9: a 5% bonus applies to a candidate answering entirely through Irish who obtains 75% or less; “decimals are always rounded down, not up ¬ e.g., 4.5 becomes 4; 4.9 becomes 4.”',
  scale: {
    name: 'Total with Irish bonus · /400',
    levels: ladder([290, 304, 305]),
    notes: [
      'Answering the paper entirely through Irish earns a 5% bonus at 75% or less.',
      '5% of 290 = 14.5.',
      'The scheme rounds bonus decimals DOWN: 14.5 → 14, not up to 15.',
      'So the recorded total is 290 + 14 = 304, not 305.',
    ],
    cite: MS('p.5 (instruction 9, 5% Irish-medium bonus, decimals rounded down)'),
  },
  scripts: [
    {
      id: 'am12-a',
      label: 'The answer',
      persona: 'Irish-medium script, 290 marks',
      work: ['Whole paper answered through Irish.', 'Base mark 290 of 400 (under 75%).', '5% of 290 = 14.5.'],
      keyLevelId: 'm304',
      keyNote:
        '304 — the 14.5 bonus rounds DOWN to 14, never up to 15. Two things are worth knowing here: sitting the paper entirely through Irish is worth a real 5% at this mark level, and the bonus is always truncated, not rounded to nearest. It is a free but modest lift — bank it if you work in Irish, but don’t expect the half-mark to round your way.',
      embodies: {
        behaviour: 'Earns the 5% Irish-medium bonus on a sub-75% script, with the 14.5 decimal rounded down to 14.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am12',
    rule: 'The Irish-medium bonus is 5%, always rounded down.',
    detail:
      'A candidate who answers the whole written paper through Irish and scores 75% or less gets a 5% bonus on marks obtained, with any decimal rounded down (4.5 → 4). It is a real but modest lift, and the fraction never rounds in your favour.',
    cite: MS('p.5'),
  },
};

// ─────────────── AM13 · The modelling project rewards judgement, not length ───────────────

const AM13: ScaleSession = {
  mode: 'scale',
  id: 'am-project-brevity',
  subject: 'applied-maths',
  level: 'common',
  title: 'The modelling project rewards judgement, not length',
  cue: 'Model',
  question: 'The 100-mark Mathematical Modelling Project’s “Introduction & Research” section is marked on descriptive bands: Very thorough 16–20, Thorough 11–15, Basic 6–10, Very basic 0–5. Examiners are told “not to penalise skilful brevity, nor to reward unwarranted length.” A candidate submits a concise, well-researched, fully-cited introduction. Which band?',
  questionNote:
    'Scenario authored for this exercise. The 2024 project rubric marks each section on four descriptive bands and instructs examiners: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.”',
  scale: {
    name: 'Introduction & Research band · /20',
    levels: [
      { id: 'am13-vb', label: 'Very basic (0–5)', annotation: 'VB', marks: 5 },
      { id: 'am13-b', label: 'Basic (6–10)', annotation: 'B', marks: 10 },
      { id: 'am13-t', label: 'Thorough (11–15)', annotation: 'T', marks: 15 },
      { id: 'am13-vt', label: 'Very thorough (16–20)', annotation: 'VT', marks: 20 },
    ],
    notes: [
      'Each project section is placed on a descriptive band, not marked per step.',
      '“Very thorough” = problem and variables identified, research presented and cited, data presented where relevant.',
      'Examiners are told not to penalise skilful brevity nor to reward unwarranted length.',
      'So a concise, complete, cited introduction reaches the top band — padding cannot lift it.',
    ],
    cite: MS('p.16 (project instruction, skilful brevity / unwarranted length); p.17 (Introduction & Research bands 16–20 / 11–15 / 6–10 / 0–5)'),
  },
  scripts: [
    {
      id: 'am13-a',
      label: 'The answer',
      persona: 'Concise but complete',
      work: ['Identifies the problem and its variables.', 'Presents and cites its research, with data where relevant.', 'Says it well and stops — no padding.'],
      keyLevelId: 'am13-vt',
      keyNote:
        'Very thorough — the top band — because it is the quality and completeness of the research that scores, not the word count. The rubric explicitly tells the examiner not to reward unwarranted length nor penalise skilful brevity, so a concise introduction that identifies the problem, cites its research and presents its data cleanly reaches the same band as a padded one. On the project, argue well and stop; padding cannot lift the band.',
      embodies: {
        behaviour: 'Submits a concise, complete, cited introduction that reaches the top band under the “do not reward unwarranted length” instruction.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am13',
    rule: 'On the modelling project, judgement sets the band — length does not.',
    detail:
      'Each section of the 100-mark modelling project is marked on descriptive bands, and examiners are told not to reward unwarranted length nor penalise skilful brevity. A concise, well-justified, fully-cited section reaches the top band; padding it out does not. Write to the point and stop.',
    cite: MS('p.16'),
  },
};

// ─────────────── AM14 · Communication & Innovation is read off the whole report ───────────────

const AM14: ScaleSession = {
  mode: 'scale',
  id: 'am-project-communication',
  subject: 'applied-maths',
  level: 'common',
  title: 'You can’t write a “communication and innovation” section',
  cue: 'Model',
  question: 'The modelling project awards 15 marks for “Communication & Innovation,” banded Very thorough 12–15 down to Very basic 0–3. But the rubric states this “is not a distinct section of the report” — it is judged across the whole project’s coherence and creativity. A candidate builds a coherent, imaginatively-approached report throughout, without a dedicated “communication” paragraph. Which band?',
  questionNote:
    'Scenario authored for this exercise. The 2024 project rubric states Communication & Innovation “is not a distinct section of the report,” marking it holistically on overall coherence and innovative/creative approach.',
  scale: {
    name: 'Communication & Innovation band · /15',
    levels: [
      { id: 'am14-vb', label: 'Very basic (0–3)', annotation: 'VB', marks: 3 },
      { id: 'am14-b', label: 'Basic (4–7)', annotation: 'B', marks: 7 },
      { id: 'am14-t', label: 'Thorough (8–11)', annotation: 'T', marks: 11 },
      { id: 'am14-vt', label: 'Very thorough (12–15)', annotation: 'VT', marks: 15 },
    ],
    notes: [
      'These 15 marks are explicitly “not a distinct section of the report.”',
      'They are read off the whole project’s overall coherence and innovative/creative approach.',
      'A report that is well-structured and imaginatively approached throughout reaches the top band.',
      'A bolt-on “communication” paragraph on an otherwise disjointed report cannot earn them.',
    ],
    cite: MS('p.16 (Communication & Innovation “not a distinct section of the report”); p.18 (band descriptors 12–15 / 8–11 / 4–7 / 0–3)'),
  },
  scripts: [
    {
      id: 'am14-a',
      label: 'The answer',
      persona: 'Coherent and creative throughout',
      work: ['Structures the whole report clearly and coherently.', 'Approaches the problem in an innovative, creative way.', 'Writes no separate “communication” paragraph.'],
      keyLevelId: 'am14-vt',
      keyNote:
        'Very thorough — but not because of any “communication” paragraph. These 15 marks are explicitly not a section you write; the examiner reads them off the coherence and creativity of the whole report. A project that is well-structured and imaginatively approached throughout banks the top band even with no dedicated paragraph, and a bolt-on paragraph cannot earn them on an otherwise disjointed report. You earn Communication & Innovation by how you build the whole thing, not by a closing note.',
      embodies: {
        behaviour: 'Earns the top Communication & Innovation band through whole-report coherence and creativity, with no dedicated section.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am14',
    rule: 'Communication & Innovation is read off the whole report, not a section you write.',
    detail:
      'The project’s 15 Communication & Innovation marks are “not a distinct section of the report” — they are judged holistically on overall coherence and creative approach. You cannot earn them with a tacked-on paragraph; they come from how the entire project is structured and presented.',
    cite: MS('p.16'),
  },
};

// ─────────────── AM15 · Units are policed per item, not by a blanket rule ───────────────

const AM15: ScaleSession = {
  mode: 'scale',
  id: 'am-units-per-item',
  subject: 'applied-maths',
  level: 'common',
  title: 'Units are policed per item — sometimes explicitly waived',
  cue: 'Solve',
  question: 'A vector part asks for the scalar (dot) product of two velocity vectors. A candidate computes it correctly as −376.71 but, unsure what unit a dot product carries, writes no units and fears a deduction. The scheme prints the answer with the note “[units not required].” What does it score?',
  questionNote:
    'Scenario authored for this exercise. Applied Maths has no blanket units penalty; units are policed per item, and the 2023 scheme marks the dot-product answer Q8(iv) as “−376.71 [units not required].”',
  scale: {
    name: 'Dot-product answer · /5',
    levels: ladder([0, 5]),
    notes: [
      'Applied Maths has no general units-deduction rule (unlike Physics).',
      'Units are handled per item, where they matter.',
      'On this scalar-product answer the scheme writes “[units not required].”',
      'So the correct value with no units banks full marks — there is nothing to deduct.',
    ],
    cite: MS23('p.14 (Q8(iv) “−376.71 [units not required]”)'),
  },
  scripts: [
    {
      id: 'am15-a',
      label: 'The answer',
      persona: 'Correct dot product, no units',
      work: ['Computes the scalar product correctly as −376.71.', 'Writes no units, unsure what a dot product carries.'],
      keyLevelId: 'm5',
      keyNote:
        'Full 5 — the scheme itself notes “[units not required]” on this answer, so there is no units mark to lose. Applied Maths does not run a blanket units penalty the way Physics does; it flags per item where units matter, and on a scalar like a dot product it explicitly waives them. Don’t manufacture a unit you are unsure of, and don’t fear a phantom deduction — give the correct value and move on.',
      embodies: {
        behaviour: 'Gives a correct scalar-product value without units, which the scheme marks in full because it notes “units not required.”',
        cite: MS23('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-am15',
    rule: 'There’s no blanket units penalty — units are policed per item.',
    detail:
      'Unlike Physics, Applied Maths applies no general units deduction; units are marked per item where they matter, and the scheme sometimes states “units not required” (e.g. on a scalar product). Give the correct value and don’t lose confidence over a unit the item doesn’t demand.',
    cite: MS23('p.14'),
  },
};

export const APPLIED_MATHS_CHAIR: ChairSubject = {
  id: 'applied-maths',
  label: 'Applied Mathematics',
  tagline: 'Blunders, slips and the floor a real attempt always banks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AM1, AM2, AM3, AM4, AM5, AM6, AM7, AM8, AM9, AM10, AM11, AM12, AM13, AM14, AM15],
  sources: [
    { label: 'SEC LC Applied Mathematics HL marking scheme 2024 (examiner-reports/applied-maths/2024-marking-scheme)' },
    { label: 'SEC LC Applied Mathematics HL marking scheme 2023 (examiner-reports/applied-maths/2023-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general marking system — the blunder/slip/misreading tariff, the systemic-error scale floor and its 10-/15-/20-mark variants, the “Box 2” partial-credit annotation, the name-the-method mark, the solidus = different-valid-attempts rule, the per-item “−1 for each incorrect part” listing deduction, the standalone marks a labelled force diagram earns, the per-item bracket that overrides the general scale, the 5% Irish-medium bonus (rounded down), the units-policed-per-item convention, and the modelling-project’s banded rubric — which applies at both Higher and Ordinary level. Verified against the 2024 and 2023 Higher Level schemes; level-specific worked examples are being added.',
};
