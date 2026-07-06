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

export const APPLIED_MATHS_CHAIR: ChairSubject = {
  id: 'applied-maths',
  label: 'Applied Mathematics',
  tagline: 'Blunders, slips and the floor a real attempt always banks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AM1, AM2, AM3, AM4],
  sources: [
    { label: 'SEC LC Applied Mathematics HL marking scheme 2024 (examiner-reports/applied-maths/2024-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general marking system — the blunder/slip/misreading tariff, the systemic-error scale floor and the name-the-method mark — which applies at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme; level-specific worked examples are being added.',
};
