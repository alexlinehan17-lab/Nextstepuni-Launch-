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

// ─────────────── MU5 · Melody band — directions & instrument ───────────────

const MU5: ScaleSession = {
  mode: 'scale',
  id: 'mu-melody-directions',
  subject: 'music',
  level: 'common',
  title: 'Good notes, no directions',
  cue: 'Composing (melody)',
  question: 'In the melody-composition question a candidate writes a melody with good shape, structure and direction — but inserts no phrasing or dynamics and names no instrument. The band grid lists “appropriate performing directions (phrasing and dynamics) inserted” and “suitable instrument chosen” inside every band; the lower bands read “no performing directions inserted / no instrument chosen”. Which band does an otherwise-good melody with neither fall into?',
  questionNote:
    'Scenario authored for this exercise. Section A melody composition is marked on one holistic band grid, but two mechanical criteria — performing directions (phrasing/dynamics) and a chosen instrument — sit inside every band descriptor. A melody that omits both can only match the lower descriptor bands, whose text reads “no performing directions inserted / no instrument chosen”. The marks shown illustrate that band effect.',
  scale: {
    name: 'Melody · band descriptors',
    levels: [
      { id: 'mu5-omit', label: 'No performing directions / no instrument', annotation: '≈10', marks: 10 },
      { id: 'mu5-full', label: 'Good band · directions & instrument', annotation: '≈30', marks: 30 },
    ],
    notes: [
      'Every band lists “Appropriate performing directions (phrasing and dynamics) inserted” and “Suitable instrument chosen”.',
      'The upper-band descriptors REQUIRE both; a melody that omits them cannot match those bands.',
      'At the foot of the grid the same lines flip to “No performing directions (phrasing and dynamics) inserted / No instrument chosen”.',
      'Phrasing, dynamics and an instrument choice are marked descriptors here — not optional decoration on top of the notes.',
    ],
    cite: MS('p.3 (Section A melody band grid — performing-directions & instrument descriptors)'),
  },
  scripts: [
    {
      id: 'mu5-a',
      label: 'The melody',
      persona: 'Good shape, no markings',
      work: ['A melody with good sense of shape, structure and direction.', 'No phrasing or dynamics inserted; no instrument named.'],
      keyLevelId: 'mu5-omit',
      keyNote:
        'The notes may be good, but the top bands require “appropriate performing directions inserted” and “a suitable instrument chosen”. With neither, the script only matches the lower descriptor bands — the ones that literally read “no performing directions / no instrument chosen”. Two quick habits — mark in phrasing/dynamics and name an instrument — keep a good melody in the band its notes earned.',
      embodies: {
        behaviour: 'Submits a musically good melody with no performing directions and no instrument choice, dropping it into the lower descriptor bands.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu5',
    rule: 'Phrasing, dynamics and instrument choice are marked, not optional.',
    detail:
      'In Section A the melody band grid lists “appropriate performing directions inserted” and “suitable instrument chosen” inside every band — the top bands require them and the bottom ones read “no performing directions / no instrument chosen”. Always mark in phrasing/dynamics and name an instrument, or a good melody sinks a band.',
    cite: MS('p.3'),
  },
};

// ─────────────── MU6 · Chord quality mark ───────────────

const MU6: ScaleSession = {
  mode: 'scale',
  id: 'mu-chord-quality',
  subject: 'music',
  level: 'common',
  title: 'Chords that “worked” aren’t top marks',
  cue: 'Harmony (quality)',
  question: 'A candidate’s harmonisation is legal throughout — every chord is correct and part of a good progression, so the per-chord marks are earned. But the choices are safe and unadventurous; better chords were available at several points. On top of the per-chord marks sits a separate “Quality of Chord Progressions” band (Poor 0–1 … Excellent 9–10). Where do chords that merely “worked” land on it?',
  questionNote:
    'Scenario authored for this exercise. Beyond the per-chord marks (MU3/MU4), Q5 carries a separate holistic “Quality of Chord Progressions” band. The scheme states explicitly that chords which “worked” but weren’t the best choices are docked here.',
  scale: {
    name: 'Harmony · chord-quality band',
    levels: [
      { id: 'mu6-poor', label: 'Poor chord progressions', annotation: '0–1', marks: 1 },
      { id: 'mu6-good', label: 'Good chord progressions', annotation: '4–5', marks: 5 },
      { id: 'mu6-exc', label: 'Excellent chord progressions', annotation: '9–10', marks: 10 },
    ],
    notes: [
      '“While the candidate may have chosen chords that ‘worked’ at any point, there may have been better choices. If that is the case, this will be reflected in the chord quality mark.”',
      'The quality band is SEPARATE from the per-chord marks — legal chords still earn those.',
      'Safe, correct-but-unadventurous progressions sit mid-band, not at Excellent.',
      'Top quality marks reward the best choice at each point, not merely a working one.',
    ],
    cite: MS('p.7 (Chord quality; Quality of Chord Progressions band)'),
  },
  scripts: [
    {
      id: 'mu6-a',
      label: 'The harmonisation',
      persona: 'Legal but unadventurous',
      work: ['Every chord is correct and part of a good progression — the per-chord marks are earned.', 'But safer, weaker choices were made where stronger chords were available.'],
      keyLevelId: 'mu6-good',
      keyNote:
        'The per-chord marks are safe, but the separate quality band caps chords that only “worked”: better choices were available, so it lands around Good, not Excellent. Legality earns the per-chord marks; musical judgement earns the quality band. Reach for the strongest chord at each point, not just a defensible one.',
      embodies: {
        behaviour: 'Writes legal but unadventurous chords that earn per-chord marks yet are docked on the separate chord-quality band.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu6',
    rule: 'A legal chord and the best chord aren’t the same mark.',
    detail:
      'Q5 marks a separate “Quality of Chord Progressions” band on top of the per-chord marks: chords that “worked” but weren’t the best choices are docked there. Earn the per-chord marks with legal progressions, then chase the quality band by picking the strongest chord available at each point.',
    cite: MS('p.7'),
  },
};

// ─────────────── MU7 · 5B essay — detail moves the band ───────────────

const MU7: ScaleSession = {
  mode: 'scale',
  id: 'mu-essay-detail',
  subject: 'music',
  level: 'common',
  title: 'Correct, but lacking detail',
  cue: 'Listening (essay 5B)',
  question: 'The 10-mark extended essay (Q5B) is marked on its own band descriptor. A candidate’s answer is entirely correct and on-topic, but stays general — it names features of the chosen topic without the specific detail that fills out each point. The band reads “Excellent awareness and detailed knowledge … 10”, but “Good knowledge of topic, but lacking in detail 6–7”. Where does a correct-but-general essay land?',
  questionNote:
    'Scenario authored for this exercise. Unlike the per-item “partially correct = 1” cap (MU2), Q5B uses a seven-level essay band where DETAIL and specificity — not correctness alone — move you up the band.',
  scale: {
    name: 'Essay 5B · detail band',
    levels: [
      { id: 'mu7-general', label: 'Some general points · lacking detail', annotation: '4–5', marks: 5 },
      { id: 'mu7-good', label: 'Good knowledge · lacking in detail', annotation: '6–7', marks: 7 },
      { id: 'mu7-exc', label: 'Excellent · detailed knowledge', annotation: '10', marks: 10 },
    ],
    notes: [
      'Top of the band: “Excellent awareness and detailed knowledge of musical features of topic 10.”',
      'A correct answer that stays general is “Good knowledge of topic, but lacking in detail 6–7”.',
      'Thinner still: “Some general points on topic, but lacking sufficient detail 4–5.”',
      'Correctness gets you on the band; specific detail is what climbs it.',
    ],
    cite: MS('p.16 (Q5B essay band descriptor)'),
  },
  scripts: [
    {
      id: 'mu7-a',
      label: 'The essay',
      persona: 'Right, but general',
      work: ['An entirely correct, on-topic answer.', 'Names features of the topic but without the specific detail that develops each one.'],
      keyLevelId: 'mu7-good',
      keyNote:
        'Being correct isn’t the ceiling here — the band separates “detailed knowledge” (10) from “Good knowledge … but lacking in detail” (6–7). A right-but-general essay lands at 6–7, three marks short, purely for want of specifics. On the essay, back each named feature with a concrete musical detail — that’s what climbs the band.',
      embodies: {
        behaviour: 'Writes a correct but general essay that lands in the “lacking in detail” band rather than the detailed-knowledge top band.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu7',
    rule: 'On the essay, detail — not just correctness — moves the band.',
    detail:
      'Q5B’s band tops out at “Excellent awareness and detailed knowledge” (10) and puts a correct-but-general answer at “Good knowledge … lacking in detail” (6–7). Support every named feature with specific musical detail; a right answer without detail leaves marks on the table.',
    cite: MS('p.16'),
  },
};

export const MUSIC_CHAIR: ChairSubject = {
  id: 'music',
  label: 'Music',
  tagline: 'Two over-answering regimes, precise descriptions, chords in context, and what the band descriptors reward.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [MU1, MU2, MU3, MU4, MU5, MU6, MU7],
  sources: [
    { label: 'SEC LC Music HL marking scheme 2022, Deferred sitting (examiner-reports/music/2022-marking-scheme-deferred)' },
  ],
  coverageNote:
    'These sessions teach the marking grammar of the written papers — the two listening over-answering regimes, the precision cap and the 5B essay detail band; the harmony chord-in-progression, cadential 6/4, chord-quality rules; and the Section A melody band descriptors (performing directions & instrument choice). Verified against the 2022 Higher Level (Deferred) scheme, whose marking grammar matches the main sitting and is corroborated by the 2024 scheme. The practical performing component is not covered here.',
};
