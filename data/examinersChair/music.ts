/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Music (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the two opposite over-answering regimes, the "partially
 * correct = 1" precision cap on descriptions, chords credited only within a
 * good progression, and the cadential 6/4 placement rule) is the real SEC
 * system, cited to:
 *  - SEC LC Music HL marking scheme 2022 (Deferred sitting) —
 *    examiner-reports/music/2022-marking-scheme-deferred.*
 * The deferred scheme's marking grammar is identical to the main sitting; only
 * per-question detail may differ (SEC note, p.2).
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Music HL marking scheme 2022, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── MU1 · Two opposite regimes ───────────────

const MU1: ScaleSession = {
  mode: 'scale',
  id: 'mu-regimes',
  subject: 'music',
  level: 'common',
  title: 'When an extra answer cancels',
  cue: 'Listening',
  question: 'A listening question asks you to name two features you hear. The candidate names three — two right, one wrong — hoping the extra covers them. On this kind of question, each extra incorrect answer cancels a correct one. On a 4-mark item (2 features × 2), what does that score?',
  questionNote:
    'Scenario authored for this exercise. Music applies two opposite over-answering regimes: on “name/identify” items an extra wrong answer cancels a correct one; on explicit choice questions examiners mark all and take the best. Knowing which applies is the skill.',
  scale: {
    name: 'Name features · cancelling regime',
    levels: two(2, 4),
    notes: [
      'On “name/identify N features” items: “each extra incorrect answer cancels a correct one.”',
      'Two correct + one wrong → the wrong one cancels a right one → 2 of 4.',
      'On EXPLICIT choice questions the opposite holds — mark all, take the best — so extras are safe there.',
      'The skill is knowing which regime the question is under.',
    ],
    cite: MS('p.9 (General Notes to Examiners, over-answering)'),
  },
  scripts: [
    {
      id: 'mu1-a',
      label: 'The answer',
      persona: 'Names a third to be safe',
      work: ['Names three features where two were asked.', 'Two are correct; the third is wrong.'],
      keyLevelId: 'm2',
      keyNote:
        'The extra wrong feature cancels a correct one — 2 of 4, not 4. On “name” items, an unsure extra is not insurance; it’s a liability. (On an explicit choice question it would be safe — examiners take your best there.) Name exactly what’s asked unless the question invites a choice.',
      embodies: {
        behaviour: 'Adds an extra wrong answer on a “name” item, where it cancels a correct one.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu1',
    rule: 'Know which over-answering regime you’re under.',
    detail:
      'On Music “name/identify” items an extra wrong answer cancels a correct one; on explicit choice questions examiners take your best, so extras are safe. Give exactly the number asked unless the question invites a choice.',
    cite: MS('p.9'),
  },
};

// ─────────────── MU2 · Partially correct = 1 ───────────────

const MU2: ScaleSession = {
  mode: 'scale',
  id: 'mu-precision',
  subject: 'music',
  level: 'common',
  title: 'Vague description, one mark',
  cue: 'Listening (describe)',
  question: 'A “describe the texture” item is worth up to 3 marks. The candidate writes a long, general answer that is broadly in the right area but never pins down a precise, correct musical statement. The scheme caps a partially-correct answer at 1 mark. What does it score?',
  questionNote:
    'Scenario authored for this exercise. In the listening paper, full marks need a fully-correct statement; a partially-correct or vague answer is capped at 1 mark regardless of length.',
  scale: {
    name: 'Describe · precision cap',
    levels: [
      { id: 'm1', label: '1 (partially correct)', annotation: '1', marks: 1 },
      { id: 'm3', label: '3 (fully correct)', annotation: '3', marks: 3 },
    ],
    notes: [
      'Full marks require a fully-correct musical statement.',
      'A “partially correct answer = 1” — the cap doesn’t rise with length.',
      'One precise term (homophonic, imitative, monophonic) beats a paragraph of vague description.',
    ],
    cite: MS('p.11–18 (partially-correct = 1 cap)'),
  },
  scripts: [
    {
      id: 'mu2-a',
      label: 'The answer',
      persona: 'Long, vague, broadly right',
      work: ['A long description in roughly the right area.', 'No precise, correct musical statement pinned down.'],
      keyLevelId: 'm1',
      keyNote:
        'Capped at 1 — length doesn’t lift a partially-correct answer, and vagueness is exactly what the cap targets. One precise, correct term earns the full 3 where a paragraph of hedging earns 1. In the listening paper, name the exact musical feature; don’t circle it.',
      embodies: {
        behaviour: 'Writes a long but imprecise description — capped at 1 mark by the precision rule.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu2',
    rule: 'Precision beats length in the listening paper.',
    detail:
      'Music caps a partially-correct description at 1 mark however long it is — full marks need a fully-correct statement. Name the exact feature (texture, cadence, device) precisely rather than describing around it.',
    cite: MS('p.11'),
  },
};

// ─────────────── MU3 · Chords in progression ───────────────

const MU3: ScaleSession = {
  mode: 'scale',
  id: 'mu-chords',
  subject: 'music',
  level: 'common',
  title: 'A chord scores only in context',
  cue: 'Harmony',
  question: 'In the harmony question, a candidate boxes in a chord that is correct in isolation — but it doesn’t form a good progression with the chords around it (it creates a rejected V7–V move). Chords earn 1 mark only when part of a good progression. What does this chord score?',
  questionNote:
    'Scenario authored for this exercise. In the harmony question a chord earns its mark only as part of a good progression, and specific voice-leading moves (e.g. V7–V) are rejected.',
  scale: {
    name: 'Harmony · chord in progression',
    levels: two(0, 1),
    notes: [
      '“1 mark for each chord that is part of a good progression.”',
      'A chord correct in isolation but creating a rejected move (e.g. V7–V) scores nothing.',
      'Harmony is marked on the line of chords, not each chord alone.',
    ],
    cite: MS('p.7 (chord-in-progression rule; rejected moves)'),
  },
  scripts: [
    {
      id: 'mu3-a',
      label: 'The chord',
      persona: 'Right chord, wrong progression',
      work: ['A chord that is valid in isolation.', 'But it forms a rejected V7–V progression with its neighbours.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — a chord earns its mark only as part of a good progression, and the V7–V move here is explicitly rejected. Harmony marks reward the flow of chords, not each one alone. Choose each chord for how it connects to the ones on either side.',
      embodies: {
        behaviour: 'Writes a chord that’s valid alone but forms a rejected progression, scoring nothing.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu3',
    rule: 'Chords score as progressions, not in isolation.',
    detail:
      'In the harmony question a chord earns its mark only within a good progression, and moves like V7–V are rejected. Choose each chord for how it connects to its neighbours, not just whether it’s correct alone.',
    cite: MS('p.7'),
  },
};

// ─────────────── MU4 · Cadential 6/4 placement ───────────────

const MU4: ScaleSession = {
  mode: 'scale',
  id: 'mu-cadential',
  subject: 'music',
  level: 'common',
  title: 'The 6/4 on the wrong beat',
  cue: 'Harmony',
  question: 'In the harmony question a candidate boxes a cadential 6/4 (Ic) approaching the final cadence — the right chord, correctly spelt. But it lands on the weaker of the two beats rather than the stronger one. The scheme credits a cadential 6/4 only when it’s on the stronger of the two beats AND at a cadence point. What does this chord score?',
  questionNote:
    'Scenario authored for this exercise. In the harmony question the cadential 6/4 (Ic) has a placement rule: it must sit on the stronger of the two beats and fall at a cadence point. A correctly-spelt Ic in the wrong metric position earns nothing.',
  scale: {
    name: 'Harmony · cadential 6/4 placement',
    levels: two(0, 1),
    notes: [
      '“Cadential 6/4 must be on the stronger of the two beats and at a cadence point.”',
      'A correctly-spelt Ic on the weaker beat fails the placement rule, so the chord earns nothing.',
      'Here “correct” includes WHERE the chord sits in the bar, not just which notes it contains.',
      'It is also the one context where iib–i (ii–I) is accepted — but only as the approach to that Ic.',
    ],
    cite: MS('p.7 (Chord Progressions — General points; cadential 6/4 placement)'),
  },
  scripts: [
    {
      id: 'mu4-a',
      label: 'The chord',
      persona: 'Right 6/4, weak beat',
      work: ['Boxes a cadential 6/4 (Ic) into the approach to the final cadence.', 'The chord is correctly spelt — but it lands on the weaker of the two beats.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the cadential 6/4 must be on the stronger of the two beats and at a cadence point, and this one is on the weaker beat. Spelling the Ic correctly isn’t enough; its metric position is part of being right. Place the 6/4 on the strong beat leading into V–I, and the mark follows.',
      embodies: {
        behaviour: 'Places a correctly-spelt cadential 6/4 on the weaker beat, where the placement rule denies the mark.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu4',
    rule: 'A cadential 6/4 only counts on the strong beat at a cadence.',
    detail:
      'In the harmony question the cadential 6/4 (Ic) must sit on the stronger of the two beats and fall at a cadence point — a correctly-spelt Ic in the wrong metric position scores nothing. For this chord, position is part of correctness.',
    cite: MS('p.7'),
  },
};

export const MUSIC_CHAIR: ChairSubject = {
  id: 'music',
  label: 'Music',
  tagline: 'Two over-answering regimes, precise descriptions, chords in context.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [MU1, MU2, MU3, MU4],
  sources: [
    { label: 'SEC LC Music HL marking scheme 2022, Deferred sitting (examiner-reports/music/2022-marking-scheme-deferred)' },
  ],
  coverageNote:
    'These sessions teach the written/listening-paper conventions — the two over-answering regimes, the precision cap, chord-in-progression marking and the cadential 6/4 placement rule — which apply across levels. Verified against the 2022 Higher Level (Deferred) scheme, whose marking grammar matches the main sitting; the composing and performing components are practical and not covered here.',
};
