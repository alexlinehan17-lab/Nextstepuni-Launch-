/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Chemistry (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the exact-term demands, the "show your Mr addition" rule,
 * the per-occurrence calculation deduction, and the `//` mutually-exclusive
 * method rule) is the real SEC system, cited to:
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

export const CHEMISTRY_CHAIR: ChairSubject = {
  id: 'chemistry',
  label: 'Chemistry',
  tagline: 'Precise terms, shown workings and one method at a time.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CH1, CH2, CH3, CH4],
  sources: [
    { label: 'SEC LC Chemistry HL marking scheme 2024 (examiner-reports/chemistry/2024-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Chemistry 2013 (examiner-reports/chemistry/2013-chief-examiner)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — exact-term demands, the Mr rule, the calculation-deduction regime and the // method rule — which the scheme applies at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme; level-specific worked examples are being added.',
};
