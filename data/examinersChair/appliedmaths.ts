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

export const APPLIED_MATHS_CHAIR: ChairSubject = {
  id: 'applied-maths',
  label: 'Applied Mathematics',
  tagline: 'Blunders, slips and the floor a real attempt always banks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AM1, AM2, AM3, AM4, AM5, AM6, AM7],
  sources: [
    { label: 'SEC LC Applied Mathematics HL marking scheme 2024 (examiner-reports/applied-maths/2024-marking-scheme)' },
    { label: 'SEC LC Applied Mathematics HL marking scheme 2023 (examiner-reports/applied-maths/2023-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general marking system — the blunder/slip/misreading tariff, the systemic-error scale floor, the name-the-method mark, the solidus = different-valid-attempts rule, the per-item “−1 for each incorrect part” listing deduction, and the standalone marks a labelled force diagram earns — which applies at both Higher and Ordinary level. Verified against the 2024 and 2023 Higher Level schemes; level-specific worked examples are being added.',
};
