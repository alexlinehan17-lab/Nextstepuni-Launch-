/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Physics (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the numerical-answer granule ladder, the one-mark unit
 * deduction, per-occurrence slip deduction with error-carried-forward, and the
 * `//` mutually-exclusive-method rule) is the real SEC system, cited to:
 *  - SEC LC Physics HL marking scheme 2025 —
 *    examiner-reports/physics/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Physics HL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── Phy1 · Marked in granules ───────────────

const PHY1: GridSession = {
  mode: 'grid',
  id: 'phy-granules',
  subject: 'physics',
  level: 'common',
  title: 'The formula is worth a mark',
  cue: 'Calculate',
  question: 'Calculate the speed of a wave of frequency 512 Hz and wavelength 0.65 m. [The candidate wrote: “v = f λ” and then stopped — no numbers.]',
  questionNote:
    'Question authored for this exercise. Physics numerical answers are marked as a ladder of independent granules — formula, substitution, answer — each scoring separately, typically 3 marks each.',
  grid: {
    perPoint: [
      { id: 'formula', label: 'Relevant formula quoted', marks: 3 },
      { id: 'sub', label: 'Substitution / working', marks: 3 },
      { id: 'answer', label: 'Correct final answer', marks: 3 },
    ],
    shorthand: '3 granules × 3m',
    ruleNote:
      'Each granule is scored on its own. Quoting the right formula banks 3 marks even if you never plug in a number — so an “I don’t know where to start” blank and a written formula are worlds apart on the mark sheet.',
    cite: MS('p.6–8 (numerical granule ladder)'),
  },
  scripts: [
    {
      id: 'phy1-a',
      label: 'Script A',
      persona: 'Formula, then froze',
      attempts: [
        {
          id: 'phy1-a-1',
          text: 'v = f λ',
          key: { formula: 3, sub: 0, answer: 0 },
          keyNote: 'The relevant formula is its own granule — 3 marks banked, even with no numbers. A blank would have scored 0. Always write the equation first.',
        },
      ],
      embodies: {
        behaviour: 'Writes only the relevant formula — which banks its own granule.',
        cite: MS('p.6'),
      },
    },
    {
      id: 'phy1-b',
      label: 'Script B',
      persona: 'Full working',
      attempts: [
        {
          id: 'phy1-b-1',
          text: 'v = f λ = 512 × 0.65 = 332.8 m s⁻¹',
          key: { formula: 3, sub: 3, answer: 3 },
          keyNote: 'Formula, substitution and a correct answer with a unit — all three granules. 9/9.',
        },
      ],
    },
    {
      id: 'phy1-c',
      label: 'Script C',
      persona: 'Right formula, arithmetic slip',
      attempts: [
        {
          id: 'phy1-c-1',
          text: 'v = f λ = 512 × 0.65 = 233 m s⁻¹',
          key: { formula: 3, sub: 3, answer: 0 },
          keyNote: 'Formula and substitution granules are secure (6 marks); only the final arithmetic is wrong (512 × 0.65 = 332.8, not 233). You lose the answer granule, not the whole question — which is exactly why showing the substitution protects you.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-phy1',
    rule: 'Every numerical answer is a ladder — write each rung.',
    detail:
      'Physics calculations score in granules: formula, substitution, answer. Quoting the formula banks a mark on its own, and showing substitution protects those marks when the arithmetic slips. Never jump straight to a bare number.',
    cite: MS('p.6'),
  },
};

// ─────────────── Phy2 · The one-mark unit ───────────────

const PHY2: ScaleSession = {
  mode: 'scale',
  id: 'phy-unit',
  subject: 'physics',
  level: 'common',
  title: 'The mark you forget to write',
  cue: 'Calculate',
  question: 'A calculation is completely correct — right formula, right substitution, right number: 4.2. But the candidate writes no unit after it. The answer was worth 9 marks. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The general instructions state that omitting (or giving incorrect) units in a final answer costs one mark, unless otherwise indicated.',
  scale: {
    name: 'Unit omission',
    levels: ladder([8, 9]),
    notes: [
      'General rule: “For omission of appropriate units (or for incorrect units) in final answers, one mark is deducted.”',
      'It is a flat one-mark deduction — the rest of the working is untouched.',
      'So a flawless 9-mark answer with no unit scores 8, not 0.',
    ],
    cite: MS('p.3 (instruction 6, units)'),
  },
  scripts: [
    {
      id: 'phy2-a',
      label: 'The answer',
      persona: 'Right number, no unit',
      work: ['… = 4.2', '(no unit written)'],
      keyLevelId: 'm8',
      keyNote:
        '8 marks — a single mark deducted for the missing unit, not a wipeout. But it is a mark, and it is the easiest one on the paper to keep. Get into the habit of writing the unit the instant you write the number.',
      embodies: {
        behaviour: 'Omits the unit on a correct final answer — a one-mark deduction.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy2',
    rule: 'A missing unit is one mark — never zero, never free.',
    detail:
      'Omitting or mis-writing the unit on a final answer costs exactly one mark. It won’t sink the question, but it is the cheapest mark to protect — write the unit every single time.',
    cite: MS('p.3'),
  },
};

// ─────────────── Phy3 · A slip is one mark ───────────────

const PHY3: ScaleSession = {
  mode: 'scale',
  id: 'phy-slip',
  subject: 'physics',
  level: 'common',
  title: 'Slip once, carry on',
  cue: 'Calculate',
  question: 'Halfway through a multi-step calculation the candidate makes one arithmetic slip, then uses that wrong value correctly through every remaining step, reaching a consistent final answer. The full calculation is worth 12 marks. Roughly what should it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme deducts one mark each time an arithmetical slip occurs; downstream work built on the slipped value still earns its marks (error carried forward).',
  scale: {
    name: 'One slip, consistent finish',
    levels: ladder([4, 11, 12]),
    notes: [
      'Rule: “Each time an arithmetical slip occurs … one mark is deducted.”',
      'Error carried forward: steps that correctly use the slipped value still score.',
      'So one slip in an otherwise perfect 12-mark answer costs ~1 mark, not the question.',
      'Abandoning the answer after the slip forfeits all the method marks that follow.',
    ],
    cite: MS('p.3 (instruction 8, arithmetical slip / ECF)'),
  },
  scripts: [
    {
      id: 'phy3-a',
      label: 'The answer',
      persona: 'One slip, keeps going',
      work: [
        'Correct method throughout.',
        'One arithmetic slip in an intermediate step.',
        'Uses that value correctly to a consistent final answer.',
      ],
      keyLevelId: 'm11',
      keyNote:
        '~11 of 12 — one mark for the slip, everything after it credited by error-carried-forward. The worst thing you can do here is panic and scribble it all out: that forfeits the method marks you had already earned. A slip is one mark; a blank page is all of them.',
      embodies: {
        behaviour: 'Makes one slip but perseveres consistently — the marks-carried-forward case, not a wipeout.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy3',
    rule: 'A slip costs one mark — don’t abandon the answer.',
    detail:
      'One arithmetic slip is a single-mark deduction, and later steps that use the slipped value still score (error carried forward). Keep going to a consistent finish; restarting or scrubbing out forfeits marks you already banked.',
    cite: MS('p.3'),
  },
};

export const PHYSICS_CHAIR: ChairSubject = {
  id: 'physics',
  label: 'Physics',
  tagline: 'Granules, units and slips — how numerical marks are really built.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [PHY1, PHY2, PHY3],
  sources: [
    { label: 'SEC LC Physics HL marking scheme 2025 (examiner-reports/physics/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general numerical-marking conventions — the granule ladder, the one-mark unit deduction and error-carried-forward — which the scheme applies at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
