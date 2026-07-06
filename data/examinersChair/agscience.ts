/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Agricultural Science (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the front-loaded points list, the surplus-answer penalty,
 * the calculation method mark, and the IIS coursework's holistic five-band
 * rubric) is the real SEC system,
 * cited to:
 *  - SEC LC Agricultural Science HL marking scheme 2024 —
 *    examiner-reports/agricultural-science/2024-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Agricultural Science HL marking scheme 2024, ${p}` });

const bandScale = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── Ag1 · Front-loaded points ───────────────

const AG1: GridSession = {
  mode: 'grid',
  id: 'ag-frontload',
  subject: 'agricultural-science',
  level: 'common',
  title: 'The first point pays most',
  cue: 'Name / list',
  question: 'Name four breeds of dairy cattle. The line is marked 4 + 2 + 2 + 2 — the first correct breed earns 4 marks, each of the next three earns 2.',
  questionNote:
    'Question authored for this exercise. Front-loaded points lists are a standard Ag Science pattern: the first correct answer is worth more, each subsequent correct answer worth less.',
  grid: {
    perPoint: [
      { id: 'b1', label: '1st correct breed', marks: 4 },
      { id: 'b2', label: '2nd correct breed', marks: 2 },
      { id: 'b3', label: '3rd correct breed', marks: 2 },
      { id: 'b4', label: '4th correct breed', marks: 2 },
    ],
    shorthand: '4 + 2 + 2 + 2',
    ruleNote:
      'The first correct answer carries the biggest mark; the rest taper. So getting at least one solid answer down banks the most valuable mark — and leaving the line blank forfeits the easiest 4 on the question.',
    cite: MS('p.4 (front-loaded points list)'),
  },
  scripts: [
    {
      id: 'ag1-a',
      label: 'Script A',
      persona: 'One breed, then blanks',
      attempts: [
        {
          id: 'ag1-a-1',
          text: 'Holstein-Friesian.  (no other breeds given)',
          key: { b1: 4, b2: 0, b3: 0, b4: 0 },
          keyNote: 'One correct breed banks the front-loaded 4 marks — nearly half the line for a single word. Three more names would have added 6, but even this one answer is worth more than any that follow it. Never leave a naming line blank.',
        },
      ],
      embodies: {
        behaviour: 'Gives only one answer on a front-loaded line — still banks the largest mark.',
        cite: MS('p.4'),
      },
    },
    {
      id: 'ag1-b',
      label: 'Script B',
      persona: 'All four',
      attempts: [
        {
          id: 'ag1-b-1',
          text: 'Holstein-Friesian, Jersey, Montbéliarde, Norwegian Red.',
          key: { b1: 4, b2: 2, b3: 2, b4: 2 },
          keyNote: 'Four correct breeds: 4 + 2 + 2 + 2 = 10. Full marks — and note the first was worth as much as the last two combined.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ag1',
    rule: 'On front-loaded lines, the first answer is worth most.',
    detail:
      'Ag Science lists often pay 4 + 2 + 2 + 2 — the first correct answer carries the biggest mark. Always get at least one solid answer down (it banks the most), then add the rest; never leave the line blank.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ag2 · Surplus penalty ───────────────

const AG2: ScaleSession = {
  mode: 'scale',
  id: 'ag-surplus',
  subject: 'agricultural-science',
  level: 'common',
  title: 'When an extra guess costs you',
  cue: 'Name',
  question: 'Name one breed of sheep. The candidate, hedging, writes two: “Texel, and also the Charolais.” One is a sheep breed; the other is a cattle breed. The line is worth 4 marks. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme applies a surplus-answer penalty: a surplus wrong answer cancels a correct one (worked in the scheme as 4 − 1 = 3 on a similar breed-ID line).',
  scale: {
    name: 'Surplus wrong answer',
    levels: bandScale([0, 4]),
    notes: [
      'The question asks for ONE breed; the candidate offers two.',
      'Texel is a sheep breed (correct); Charolais is a cattle breed (wrong here).',
      'Surplus-answer rule: a surplus wrong answer cancels a correct one.',
      'So the extra wrong breed cancels the right one — the line is dragged down.',
    ],
    cite: MS('p.4 (surplus wrong answer cancels a correct one)'),
  },
  scripts: [
    {
      id: 'ag2-a',
      label: 'The answer',
      persona: 'Adds a second, wrong',
      work: ['Texel, and also the Charolais.', '(Texel = sheep ✓, Charolais = cattle ✗)'],
      keyLevelId: 'm0',
      keyNote:
        'The surplus wrong answer cancels the correct one — hedging turned a 4-mark answer into a loss. When the question asks for one, give one: “Texel” alone scores full marks. An unsure extra is not free; it can wipe out the mark you had.',
      embodies: {
        behaviour: 'Adds an unsure extra answer where one was asked — the surplus wrong answer cancels the correct one.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag2',
    rule: 'Give the number asked — an extra guess can cancel a right answer.',
    detail:
      'Ag Science cancels a correct answer with a surplus wrong one. If the question asks for one breed, give one; padding with an unsure extra can wipe out the mark you’d earned.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ag3 · IIS holistic marking ───────────────

const AG3: ScaleSession = {
  mode: 'scale',
  id: 'ag-iis-brevity',
  subject: 'agricultural-science',
  level: 'higher',
  title: 'Length isn’t the mark',
  cue: 'Coursework (IIS)',
  question: 'An Individual Investigative Study (IIS) section is marked as ONE holistic band, not point-by-point. One candidate writes a long, padded section; another writes a shorter, sharper one that covers the same substance well. How does the padding affect the mark?',
  questionNote:
    'Scenario authored for this exercise. Each IIS section is awarded a single holistic band mark (Excellent/Very Good/Good/Fair/Weak); the scheme warns markers not to penalise skilful brevity nor reward unwarranted length.',
  scale: {
    name: 'IIS section · holistic band',
    levels: [
      { id: 'weak', label: 'Weak', annotation: 'W', marks: 6 },
      { id: 'good', label: 'Good', annotation: 'G', marks: 14 },
      { id: 'vgood', label: 'Very Good', annotation: 'VG', marks: 18 },
      { id: 'excellent', label: 'Excellent', annotation: 'E', marks: 22 },
    ],
    notes: [
      'Each IIS section gets one holistic band mark, not additive points.',
      'The scheme: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.”',
      'Padding a section doesn’t raise its band — quality and coverage do.',
    ],
    cite: MS('p.7 (IIS holistic banding; brevity/length note)'),
  },
  scripts: [
    {
      id: 'ag3-a',
      label: 'The section',
      persona: 'Padded for length',
      work: [
        'A long section with lots of filler and repetition.',
        'The actual substance matches a shorter, sharper answer.',
      ],
      keyLevelId: 'good',
      keyNote:
        'The padding earns nothing — the section is judged on one holistic band, and length isn’t a band criterion. A concise answer with the same substance lands in the same band, in a fraction of the words. Spend the effort on depth and coverage, not volume.',
      embodies: {
        behaviour: 'Pads a coursework section for length, which the holistic banding does not reward.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag3',
    rule: 'Coursework is banded on quality, not length.',
    detail:
      'Each IIS section is one holistic band mark — the scheme explicitly won’t reward padding or punish skilful brevity. Write concisely and cover the substance well; volume alone never lifts the band.',
    cite: MS('p.7'),
  },
};

// ─────────────── Ag4 · Calculation method mark ───────────────

const AG4: ScaleSession = {
  mode: 'scale',
  id: 'ag-method-mark',
  subject: 'agricultural-science',
  level: 'common',
  title: 'The formula banks marks on its own',
  cue: 'Calculate',
  question:
    'Calculate the % soil organic matter in a peat sample (mass lost 55.2 g from a 90 g sample). The line is worth 6 marks. A candidate writes the correct formula — “55.2 / 90 × 100” — but slips the arithmetic and lands on 51.3 % instead of 61.3 %. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Ag Science calculation lines carry a method mark: the scheme credits the correct formula on its own, worked here as “correct formula without correct answer, award 3m” on a 6-mark % organic matter calculation.',
  scale: {
    name: 'Calculation · method mark',
    levels: [
      { id: 'zero', label: 'No credit', annotation: '0', marks: 0 },
      { id: 'method', label: 'Method mark', annotation: 'M', marks: 3 },
      { id: 'full', label: 'Full marks', annotation: '6', marks: 6 },
    ],
    notes: [
      'The final answer (51.3 %) is wrong, so full marks are off the table.',
      'But the formula “55.2 / 90 × 100” is the correct method — the scheme credits it on its own.',
      'Scheme: correct formula without the correct answer scores 3 of 6.',
      '(A correct answer with no working still scores the full 6 — but a wrong answer with no formula shown scores nothing.)',
    ],
    cite: MS('p.24 (correct formula without correct answer, award 3m)'),
  },
  scripts: [
    {
      id: 'ag4-a',
      label: 'The answer',
      persona: 'Right method, wrong arithmetic',
      work: ['55.2 / 90 × 100', '= 51.3 %  (arithmetic slip; correct value is 61.3 %)'],
      keyLevelId: 'method',
      keyNote:
        'The final number is wrong, but the correct formula banks the method mark — 3 of the 6. Had this candidate written only “51.3 %” with no working, the examiner would have nothing to credit and it scores 0. Always put the formula on the page before the arithmetic: it is half the marks, and it survives a slip on the calculator.',
      embodies: {
        behaviour: 'Shows the correct formula but fumbles the arithmetic — the method mark still banks half.',
        cite: MS('p.24'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag4',
    rule: 'Show the formula — the method banks marks even if the answer is wrong.',
    detail:
      'Ag Science calculation lines credit the correct formula on its own: a right method with a wrong final number still scores the method mark (here 3 of 6), while a wrong answer with no working shown scores nothing. Always write the working before the arithmetic — it is the half of the marks a calculator slip can’t take.',
    cite: MS('p.24'),
  },
};

export const AG_SCIENCE_CHAIR: ChairSubject = {
  id: 'agricultural-science',
  label: 'Agricultural Science',
  tagline: 'Front-loaded points, surplus penalties, method marks and holistic coursework.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AG1, AG2, AG3, AG4],
  sources: [
    { label: 'SEC LC Agricultural Science HL marking scheme 2024 (examiner-reports/agricultural-science/2024-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — front-loaded points, the surplus-answer penalty, the calculation method mark and the IIS holistic banding — which apply at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme; level-specific worked examples are being added.',
};
