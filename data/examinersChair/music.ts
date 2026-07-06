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

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

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

// ─────────────── MU8 · Repeated chord in adjacent boxes ───────────────

const MU8: ScaleSession = {
  mode: 'scale',
  id: 'mu-repeated-chord',
  subject: 'music',
  level: 'common',
  title: 'The same chord, twice',
  cue: 'Harmony',
  question:
    'In the harmony question a candidate is unsure of the next chord, so they simply repeat the chord already in the previous box — same chord, same bass, no 7th added. The scheme states a repeated chord in adjacent boxes is not accepted unless the bass has changed or a 7th has been added. What does the repeated box score?',
  questionNote:
    'Scenario authored for this exercise. In the harmony question a chord placed in a box adjacent to the same chord earns nothing on its own — the scheme accepts the repeat only if the bass note has changed or a 7th has been added.',
  scale: {
    name: 'Harmony · repeated chord',
    levels: two(0, 1),
    notes: [
      '“Same chord in adjacent boxes not accepted unless bass changed or 7th added.”',
      'A held/repeated chord with unchanged bass and no added 7th scores nothing in the second box.',
      'Repeating a chord to play safe is not a free box — it must earn its place by moving the bass or adding a 7th.',
    ],
    cite: MS('p.7 (Chord Progressions — General points; repeated chords)'),
  },
  scripts: [
    {
      id: 'mu8-a',
      label: 'The repeat',
      persona: 'Holds the chord to play safe',
      work: [
        'Unsure of the next chord, repeats the previous chord in the adjacent box.',
        'Same chord, same bass note, no 7th added.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — a repeated chord in an adjacent box is not accepted unless the bass has changed or a 7th has been added, and this repeat does neither. Holding a chord to fill a box earns nothing; move the bass or add a 7th, or choose a chord that actually progresses.',
      embodies: {
        behaviour: 'Repeats a chord in an adjacent box with unchanged bass and no added 7th, where the scheme rejects the repeat.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu8',
    rule: 'A repeated chord only counts if the bass moves or a 7th is added.',
    detail:
      'In the harmony question the scheme rejects the same chord in adjacent boxes unless the bass note changes or a 7th is added. Don’t fill an uncertain box by holding the previous chord — make it move.',
    cite: MS('p.7'),
  },
};

// ─────────────── MU9 · Accidental & suffix must be exact ───────────────

const MU9: ScaleSession = {
  mode: 'scale',
  id: 'mu-accidental-suffix',
  subject: 'music',
  level: 'common',
  title: 'Right chord, missing accidental',
  cue: 'Harmony',
  question:
    'In the harmony question a candidate chooses the correct chord in the correct place — but writes it with the wrong suffix (a plain triad where a 7th was needed) or omits a required accidental. The scheme says the accidental and suffix, where relevant, must be fully correct for the mark to be awarded. What does the chord score?',
  questionNote:
    'Scenario authored for this exercise. In the harmony question a chord’s accidental and suffix must be fully correct — the right chord function written with a wrong or missing accidental/suffix earns nothing, even where the progression is otherwise good.',
  scale: {
    name: 'Harmony · accidental & suffix',
    levels: two(0, 1),
    notes: [
      '“Accidental and suffix, where relevant, must be fully correct for mark to be awarded.”',
      'A correct chord function with a missing accidental or wrong suffix (e.g. triad where a 7th was required) fails the rule.',
      'Being right about which chord is not enough — the spelling on the page must be exact.',
    ],
    cite: MS('p.7 (Chord Progressions — General points; accidental and suffix)'),
  },
  scripts: [
    {
      id: 'mu9-a',
      label: 'The chord',
      persona: 'Right function, sloppy spelling',
      work: [
        'Chooses the correct chord in the correct place within a good progression.',
        'But omits a required accidental / writes the wrong suffix.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — the accidental and suffix must be fully correct for the mark, and this chord’s spelling is not. Knowing the right chord doesn’t bank the mark if the accidental is missing or the suffix is wrong. Write the exact accidental and suffix the chord needs.',
      embodies: {
        behaviour: 'Writes the correct chord function with a missing accidental or wrong suffix, which the precision rule denies.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu9',
    rule: 'A chord’s accidental and suffix must be exact, not just its function.',
    detail:
      'In the harmony question the accidental and suffix must be fully correct for the chord mark — the right chord written with a missing accidental or wrong suffix scores nothing. Spell every chord exactly, not just correctly in your head.',
    cite: MS('p.7'),
  },
};

// ─────────────── MU10 · Bass — pitch AND rhythmic place ───────────────

const MU10: ScaleSession = {
  mode: 'scale',
  id: 'mu-bass-placement',
  subject: 'music',
  level: 'common',
  title: 'Right bass note, wrong beat',
  cue: 'Harmony (bass)',
  question:
    'In the harmony question the bass line earns 0.5 for each correct bass note under a chord symbol — but the scheme specifies “correct pitch in correct place rhythmically”. A candidate writes the right bass pitch under the chord symbol, but places it on the wrong beat rhythmically. What does that note score?',
  questionNote:
    'Scenario authored for this exercise. Bass notes score 0.5 each, but only for the correct pitch in the correct rhythmic place — a right pitch dropped on the wrong beat earns nothing.',
  scale: {
    name: 'Bass · pitch and rhythmic place',
    levels: [
      { id: 'mu10-miss', label: '0 (wrong rhythmic place)', annotation: '0', marks: 0 },
      { id: 'mu10-full', label: '0.5 (right pitch, right place)', annotation: '0.5', marks: 0.5 },
    ],
    notes: [
      '“0.5 mark per correct bass note under each chord symbol … (Correct pitch in correct place rhythmically).”',
      'The 0.5 needs BOTH the right pitch AND the right rhythmic position — one without the other earns nothing.',
      'A correct bass pitch written on the wrong beat is not a “correct bass note” for this rule.',
    ],
    cite: MS('p.6 (Q4 Bass — correct pitch in correct place rhythmically)'),
  },
  scripts: [
    {
      id: 'mu10-a',
      label: 'The bass note',
      persona: 'Right pitch, wrong beat',
      work: [
        'Writes the correct bass pitch under the chord symbol.',
        'But places it on the wrong beat rhythmically.',
      ],
      keyLevelId: 'mu10-miss',
      keyNote:
        '0 — the 0.5 is for the correct pitch in the correct rhythmic place, and this note is on the wrong beat. Getting the note name right is only half the requirement; where it sits in the bar is the other half. Place each bass note on the right beat as well as at the right pitch.',
      embodies: {
        behaviour: 'Writes a correct bass pitch in the wrong rhythmic position, which the “correct place rhythmically” rule denies.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu10',
    rule: 'A bass note needs the right beat as well as the right pitch.',
    detail:
      'The bass line marks 0.5 for each correct bass note only when it is the “correct pitch in correct place rhythmically” — a right note on the wrong beat scores nothing. Fix both the pitch and its rhythmic position.',
    cite: MS('p.6'),
  },
};

// ─────────────── MU11 · Dance — modulation descriptor ───────────────

const MU11: ScaleSession = {
  mode: 'scale',
  id: 'mu-dance-modulation',
  subject: 'music',
  level: 'common',
  title: 'A modulation you never confirmed',
  cue: 'Composing (dance)',
  question:
    'The dance-melody question (Q3) is marked on a band grid that grades the modulation across its bands: “Successful modulation” in the top bands, “An unconfirmed modulation” in the Good band, “An unsuccessful modulation” lower, and “No attempt at modulation” at the foot. A candidate writes a strong dance melody that moves toward a new key but never confirms it with a cadence. Which modulation band does that pull toward?',
  questionNote:
    'Scenario authored for this exercise. Q3 (compose a dance) grades the modulation itself as a band descriptor — successful → unconfirmed → unsuccessful → no attempt — alongside rhythmic integrity of the dance and adherence to the given structure. The marks shown illustrate how the modulation descriptor pulls the band.',
  scale: {
    name: 'Dance · modulation descriptor',
    levels: [
      { id: 'mu11-none', label: 'No attempt at modulation', annotation: '≈14', marks: 14 },
      { id: 'mu11-unsucc', label: 'Unsuccessful modulation', annotation: '≈22', marks: 22 },
      { id: 'mu11-unconf', label: 'Unconfirmed modulation', annotation: '≈30', marks: 30 },
      { id: 'mu11-succ', label: 'Successful modulation', annotation: '≈46', marks: 46 },
    ],
    notes: [
      'The Q3 band grid grades modulation explicitly: “Successful modulation” (top) → “An unconfirmed modulation” (Good) → “An unsuccessful modulation” (Fair) → “No attempt at modulation” (Poor).',
      'A modulation that moves toward a new key but never confirms it (no cadence in the new key) is “unconfirmed” — the Good band, not the top.',
      'The dance grid also grades rhythmic integrity of the dance and adherence to the given structure — the modulation is only one of several descriptors.',
    ],
    cite: MS('p.5 (Q3 dance band grid — modulation descriptor)'),
  },
  scripts: [
    {
      id: 'mu11-a',
      label: 'The dance',
      persona: 'Moves key but never lands it',
      work: [
        'A strong dance melody with good rhythm and structure.',
        'It moves toward a new key but is never confirmed with a cadence there.',
      ],
      keyLevelId: 'mu11-unconf',
      keyNote:
        'An unconfirmed modulation lands in the Good band, not the top — the grid rates the modulation as “successful”, “unconfirmed”, “unsuccessful” or “not attempted”, and drifting toward a key without cadencing in it is “unconfirmed”. Confirm the new key with a cadence to lift the modulation descriptor into the top band.',
      embodies: {
        behaviour: 'Writes a modulation that moves toward a new key but never confirms it, landing on the “unconfirmed modulation” band.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu11',
    rule: 'In a dance, confirm the modulation or it only half-counts.',
    detail:
      'Q3’s band grid grades the modulation itself — successful, unconfirmed, unsuccessful or not attempted. A key change that is never confirmed with a cadence is “unconfirmed” and sits in the Good band. Cadence in the new key to make the modulation count.',
    cite: MS('p.5'),
  },
};

// ─────────────── MU12 · Melody to words — marriage of words & music ───────────────

const MU12: ScaleSession = {
  mode: 'scale',
  id: 'mu-words-music',
  subject: 'music',
  level: 'common',
  title: 'A good tune, clumsy word-setting',
  cue: 'Composing (words)',
  question:
    'In the melody-to-given-words question (Q2), every band descriptor is headed by the “marriage of words and music”. A candidate writes a singable tune, but the natural word stresses fall on weak beats and long syllables land on short notes. (The same grid ends with a hard floor: “No text inserted 0.”) With good notes but poor word-setting, which marriage-of-words band does it pull toward?',
  questionNote:
    'Scenario authored for this exercise. Q2 (melody to given words) puts “marriage of words and music” at the head of every band descriptor, and the grid’s hard floor is “No text inserted 0”. The marks shown illustrate how the marriage descriptor pulls the band; write the words under the notes and match stress to strong beats.',
  scale: {
    name: 'Words · marriage of words and music',
    levels: [
      { id: 'mu12-notext', label: 'No text inserted', annotation: '0', marks: 0 },
      { id: 'mu12-poor', label: 'Poor marriage of words and music', annotation: '≈17', marks: 17 },
      { id: 'mu12-good', label: 'Good marriage of words and music', annotation: '≈30', marks: 30 },
      { id: 'mu12-exc', label: 'Excellent marriage of words and music', annotation: '≈46', marks: 46 },
    ],
    notes: [
      'Every Q2 band is headed “marriage of words and music” — Excellent → Very good → Good → Fair → Poor.',
      'Word stresses on weak beats and long syllables on short notes are a poor “marriage”, whatever the tune’s quality.',
      'Hard floor at the foot of the grid: “No text inserted 0” — the words must actually be written under the notes.',
    ],
    cite: MS('p.4 (Q2 melody-to-words band grid — marriage of words and music; “No text inserted 0”)'),
  },
  scripts: [
    {
      id: 'mu12-a',
      label: 'The setting',
      persona: 'Singable tune, wrong stresses',
      work: [
        'A singable melody with a good sense of shape.',
        'But natural word stresses fall on weak beats and long syllables sit on short notes.',
      ],
      keyLevelId: 'mu12-poor',
      keyNote:
        'The tune may be good, but Q2 heads every band with the “marriage of words and music”, and stresses on weak beats read as a poor marriage — pulling the band down whatever the notes do. Match strong syllables to strong beats and give long syllables longer notes; and never forget the hard floor — “No text inserted” is 0.',
      embodies: {
        behaviour: 'Sets given words with stresses on weak beats and long syllables on short notes — a poor “marriage of words and music”.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu12',
    rule: 'In a words setting, marry stress to beat — and write the words in.',
    detail:
      'Q2 heads every band with the “marriage of words and music”: word stresses on weak beats and long syllables on short notes pull the band down however good the tune. And the grid’s floor is “No text inserted 0” — the words must be under the notes.',
    cite: MS('p.4'),
  },
};

// ─────────────── MU13 · Flat naming items are all-or-nothing ───────────────

const MU13: ScaleSession = {
  mode: 'scale',
  id: 'mu-flat-naming',
  subject: 'music',
  level: 'common',
  title: 'Name the cadence, or nothing',
  cue: 'Listening (identify)',
  question:
    'A listening item asks you to name the cadence you hear — worth a flat 2 marks. Unlike the description items, it carries no “partially correct = 1” line. A candidate hears it end on the dominant but writes “perfect” instead of “imperfect”. On a flat-mark naming item with no partial ladder, what does a near-miss score?',
  questionNote:
    'Scenario authored for this exercise. Flat identification items (name the cadence, name the section, name the key) carry a single flat mark with no “partially correct = 1” fallback — unlike the description items in MU2. They are all-or-nothing: the exact term or zero.',
  scale: {
    name: 'Identify · flat naming',
    levels: two(0, 2),
    notes: [
      'Naming items carry a flat mark and no partial ladder — e.g. “Perfect cadence 2”, “Recapitulation 1”.',
      'There is no “Partially correct answer = 1” line on these items — that fallback belongs to the description items (MU2).',
      'A near-miss (“perfect” for “imperfect”; “interrupted” for “perfect”) is wrong, and wrong scores 0 — not 1.',
    ],
    cite: MS('p.10 (flat identification marks — e.g. Perfect cadence = 2)'),
  },
  scripts: [
    {
      id: 'mu13-a',
      label: 'The answer',
      persona: 'Close, but the wrong term',
      work: [
        'Asked to name the cadence (flat 2-mark item).',
        'Writes “perfect” where the excerpt closes on an imperfect cadence.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0, not 1 — a flat naming item has no “partially correct” rung, so a near-miss term scores nothing. The mercy of the partially-correct cap (MU2) is only for description items; identification items are all-or-nothing. Commit to the exact cadence/section/key name, because close doesn’t travel here.',
      embodies: {
        behaviour: 'Gives a near-miss term on a flat naming item that carries no partial-credit fallback, scoring zero.',
        cite: MS('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu13',
    rule: 'On flat naming items, it’s the exact term or zero.',
    detail:
      'Identification items (name the cadence/section/key) carry a flat mark with no “partially correct = 1” fallback — that cushion is only for description items. A near-miss term scores 0, not 1, so name the exact thing.',
    cite: MS('p.10'),
  },
};

// ─────────────── MU14 · Identify AND describe (two marks) ───────────────

const MU14: GridSession = {
  mode: 'grid',
  id: 'mu-identify-describe',
  subject: 'music',
  level: 'common',
  title: 'Name it and describe it',
  cue: 'Listening (technique)',
  question:
    'A listening item asks you to identify a recording technique used in the excerpt AND to describe it — one mark for the identification, one mark for the description. How do three answers that do one, both, or neither score?',
  questionNote:
    'Scenario authored for this exercise. This two-part identify-and-describe pattern (e.g. a recording technique) splits the mark: one for naming the technique, one for describing it — so naming without describing earns half, and a vivid description that names no valid technique earns nothing.',
  grid: {
    perPoint: [
      { id: 'identify', label: 'Identify the technique', marks: 1 },
      { id: 'describe', label: 'Describe the technique', marks: 1 },
    ],
    shorthand: '1 + 1 (identify + describe)',
    ruleNote:
      'The identification and the description are marked separately — one mark each. Naming the technique but leaving it undescribed banks only the identify mark; describing an effect without pinning it to a valid, named technique banks neither.',
    cite: MS('p.12 (Q2(a) — identify a recording technique + describe it, 1 + 1)'),
  },
  scripts: [
    {
      id: 'mu14-a',
      label: 'Both parts',
      persona: 'Names it and describes it',
      attempts: [
        {
          id: 'mu14-a-1',
          text: 'Overdubbing — the vocal line has been recorded in a separate pass and layered over the backing so the singer appears to sing with themselves.',
          key: { identify: 1, describe: 1 },
          keyNote: 'The technique is named (overdubbing) and then described accurately — both marks land. 2/2.',
        },
      ],
    },
    {
      id: 'mu14-b',
      label: 'Names only',
      persona: 'Names it, stops there',
      attempts: [
        {
          id: 'mu14-b-1',
          text: 'Overdubbing.',
          key: { identify: 1, describe: 0 },
          keyNote:
            'The identify mark is earned, but there is no description of what overdubbing does, so the second mark is gone. 1/2 — half the item left on the table for want of a sentence.',
        },
      ],
      embodies: {
        behaviour: 'Names the technique but writes no description, banking only the identification mark on a two-part item.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'mu14-c',
      label: 'Describes, mislabels',
      persona: 'Vivid effect, wrong name',
      attempts: [
        {
          id: 'mu14-c-1',
          text: 'The voice sounds fuller and doubled, like there are two singers — a nice echo effect.',
          key: { identify: 0, describe: 0 },
          keyNote:
            'No valid technique is named (“echo effect” isn’t the technique heard), so the identify mark is lost — and because the description isn’t pinned to a correctly-named technique, it can’t bank the describe mark either. 0/2.',
        },
      ],
      embodies: {
        behaviour: 'Describes the audible effect but names no valid technique, so neither the identify nor the anchored-description mark is awarded.',
        cite: MS('p.12'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu14',
    rule: 'Identify AND describe — the two are separate marks.',
    detail:
      'On two-part listening items the identification and the description each carry their own mark. Name the technique to bank the first, then describe what it does to bank the second — one without the other is half marks or none.',
    cite: MS('p.12'),
  },
};

// ─────────────── MU15 · Paired category slots (classical + pop) ───────────────

const MU15: GridSession = {
  mode: 'grid',
  id: 'mu-category-slots',
  subject: 'music',
  level: 'common',
  title: 'One classical, one pop — two slots',
  cue: 'Listening (paired features)',
  question:
    'A listening item gives one mark for a valid classical feature AND one mark for a valid pop feature in the excerpt — two fixed category slots. How do three answers score: one of each, two of the same kind, or a vague classical plus a good pop?',
  questionNote:
    'Scenario authored for this exercise. This paired item reserves one mark for a classical feature and one for a pop feature — separate category slots. Two features of the same kind can only fill one slot; the empty slot earns nothing, and a slot only counts if its feature is valid.',
  grid: {
    perPoint: [
      { id: 'classical', label: 'Valid classical feature', marks: 1 },
      { id: 'pop', label: 'Valid pop feature', marks: 1 },
    ],
    shorthand: '1 + 1 (classical + pop)',
    ruleNote:
      'The two marks are reserved for two different categories — one classical feature, one pop feature. Giving two classical features fills only the classical slot; the pop mark stays unearned. Unlike a “name two features” item, doubling up on one category cannot cover the other.',
    cite: MS('p.12 (Q2(e) — one classical feature + one pop feature, 1 + 1)'),
  },
  scripts: [
    {
      id: 'mu15-a',
      label: 'One of each',
      persona: 'Reads both slots',
      attempts: [
        {
          id: 'mu15-a-1',
          text: 'Classical feature: the string nonet and harp play in instrumental counterpoint. Pop feature: relaxed, ballad-style storytelling vocals.',
          key: { classical: 1, pop: 1 },
          keyNote: 'One valid feature in each category — both slots filled. 2/2.',
        },
      ],
    },
    {
      id: 'mu15-b',
      label: 'Two classical',
      persona: 'Doubles up on one category',
      attempts: [
        {
          id: 'mu15-b-1',
          text: 'Classical strings play sustained legato chords, and there is instrumental counterpoint between the strings — both classical features of the arrangement.',
          key: { classical: 1, pop: 0 },
          keyNote:
            'Two valid classical features, but only one classical slot exists — the second can’t fill the pop slot. The pop mark is unearned. 1/2. On a paired item, doubling one category leaves the other blank.',
        },
      ],
      embodies: {
        behaviour: 'Answers a paired category item with two features of the same category, leaving the other slot’s mark unearned.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'mu15-c',
      label: 'Vague classical, good pop',
      persona: 'One slot vague, one solid',
      attempts: [
        {
          id: 'mu15-c-1',
          text: 'Classical feature: it sounds a bit orchestral and old-fashioned. Pop feature: relaxed ballad-style storytelling vocals.',
          key: { classical: 0, pop: 1 },
          keyNote:
            '“Sounds orchestral and old-fashioned” isn’t a valid, specific classical feature, so the classical slot stays empty — but the pop feature is valid and banks its mark. 1/2. Each slot needs a precise, correct feature, not an impression.',
        },
      ],
      embodies: {
        behaviour: 'Fills one category slot with a vague impression rather than a valid feature, losing that slot’s mark.',
        cite: MS('p.12'),
      },
    },
  ],
  takeaway: {
    id: 'codex-mu15',
    rule: 'Paired items are category slots — fill each with its own valid feature.',
    detail:
      'When an item gives one mark for a classical feature and one for a pop feature, the marks are reserved by category. Two of the same kind fill only one slot, and each slot needs a precise valid feature — an impression earns nothing.',
    cite: MS('p.12'),
  },
};

export const MUSIC_CHAIR: ChairSubject = {
  id: 'music',
  label: 'Music',
  tagline: 'Two over-answering regimes, precise descriptions, chords spelt and progressing in context, bass on the right beat, and what the composing band descriptors reward.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [MU1, MU2, MU3, MU4, MU5, MU6, MU7, MU8, MU9, MU10, MU11, MU12, MU13, MU14, MU15],
  sources: [
    { label: 'SEC LC Music HL marking scheme 2022, Deferred sitting (examiner-reports/music/2022-marking-scheme-deferred)' },
  ],
  coverageNote:
    'These sessions teach the marking grammar of the written papers — the two listening over-answering regimes, the precision cap on descriptions vs the all-or-nothing flat naming items, the 5B essay detail band, and the identify-and-describe / paired-category-slot listening patterns; the harmony chord-in-progression, cadential 6/4, chord-quality, repeated-chord and accidental/suffix rules plus the bass pitch-and-rhythmic-place credit; and the Section A composing band descriptors (performing directions & instrument choice, marriage of words and music, and the dance modulation grade). Verified against the 2022 Higher Level (Deferred) scheme, whose marking grammar matches the main sitting and is corroborated by the 2024 scheme. The practical performing component is not covered here.',
};
