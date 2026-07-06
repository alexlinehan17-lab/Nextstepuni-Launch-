/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — German (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the two Content/Expression components, the "Lower-E"
 * length/content gate on the Expression mark, the half-marks penalty for
 * unmanipulated lifting, and tense-critical comprehension) is the real SEC
 * system, cited to:
 *  - SEC LC German HL marking scheme 2025 —
 *    examiner-reports/german/2025-marking-scheme.*
 * Page refs use the PDF page number (runs ~2 ahead of the printed page).
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC German HL marking scheme 2025, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── Ge1 · The length gate ───────────────

const GE1: ScaleSession = {
  mode: 'scale',
  id: 'de-length-gate',
  subject: 'german',
  level: 'common',
  title: 'Too short to score full',
  cue: 'Schriftliche Produktion',
  question: 'The written production is marked Content 25 + Expression 25. A candidate writes flawless German — but only about 80 words, under the 100-word expectation. What is the maximum EXPRESSION mark now available?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s “Lower-E” rule: if the content mark is 12 or less, OR the answer is under 100 words, expression is marked out of 18 instead of 25.',
  scale: {
    name: 'Expression · Lower-E gate',
    levels: [
      { id: 'm18', label: 'Max 18 (short/thin)', annotation: '18', marks: 18 },
      { id: 'm25', label: 'Max 25 (full length)', annotation: '25', marks: 25 },
    ],
    notes: [
      'Written production = Content 25 + Expression 25.',
      'Lower-E rule: “If the content mark is 12 or less, or the answer is too short (less than 100 words), mark expression out of 18.”',
      'So a short script has its language mark structurally capped, however accurate.',
    ],
    cite: MS('p.[20] (Lower-E gate, Schriftliche Produktion)'),
  },
  scripts: [
    {
      id: 'ge1-a',
      label: 'The answer',
      persona: 'Flawless — but too short',
      work: ['Accurate, well-written German.', 'Only ~80 words — under the 100-word expectation.'],
      keyLevelId: 'm18',
      keyNote:
        'Expression is capped at 18, not 25 — the Lower-E rule caps the language mark for short or thin scripts before quality is even judged. Perfect German can’t beat the cap; reaching the expected length is what unlocks the full 25. Watch the word count as closely as the grammar.',
      embodies: {
        behaviour: 'Writes accurate but under-length German, triggering the Lower-E cap on Expression.',
        cite: MS('p.[20]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de1',
    rule: 'Under-length caps your language mark.',
    detail:
      'German’s Lower-E rule marks Expression out of 18 (not 25) if the answer is under 100 words or content is weak — regardless of accuracy. Hit the expected length; flawless German that’s too short can’t reach full marks.',
    cite: MS('p.[20]'),
  },
};

// ─────────────── Ge2 · Copying = half marks ───────────────

const GE2: ScaleSession = {
  mode: 'scale',
  id: 'de-half-lift',
  subject: 'german',
  level: 'common',
  title: 'Lift it, halve it',
  cue: 'Comprehension',
  question: 'A comprehension question requires the answer to be manipulated (reworked), but the candidate quotes the sentence from the text unchanged. The point is correct. On a 4-mark question, what does it score?',
  questionNote:
    'Scenario authored for this exercise. In German comprehension, a quotation given without the required manipulation (or with extraneous material) is awarded half marks.',
  scale: {
    name: 'Comprehension · unmanipulated lift',
    levels: two(2, 4),
    notes: [
      'German comprehension needs evidence the candidate understood the text.',
      'Quotation without the required manipulation → half marks.',
      'Adding extraneous material around the answer → half marks too.',
    ],
    cite: MS('p.[10] (half marks for unmanipulated quotation)'),
  },
  scripts: [
    {
      id: 'ge2-a',
      label: 'The answer',
      persona: 'Quotes it unchanged',
      work: ['Copies the sentence from the text verbatim, where manipulation was required.'],
      keyLevelId: 'm2',
      keyNote:
        'Half marks — 2 of 4. The lift shows you found the right place, but not that you understood it enough to rework it, so the scheme halves the award. Manipulate the quotation (change the person/tense as needed) to earn the full mark. Half is better than zero, but it’s still half.',
      embodies: {
        behaviour: 'Quotes the text without the required manipulation — awarded half marks.',
        cite: MS('p.[10]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de2',
    rule: 'An unmanipulated quote is worth half.',
    detail:
      'German comprehension halves the marks for a quotation given without the required manipulation, or padded with extraneous material. Rework the answer into your own form and keep it tight to earn full marks.',
    cite: MS('p.[10]'),
  },
};

// ─────────────── Ge3 · Wrong tense = 0 ───────────────

const GE3: ScaleSession = {
  mode: 'scale',
  id: 'de-tense',
  subject: 'german',
  level: 'common',
  title: 'Right fact, wrong tense',
  cue: 'Comprehension',
  question: 'A comprehension question asks about something that already happened. The candidate finds the correct information but writes it in the present tense, where the past was required. How does it score?',
  questionNote:
    'Scenario authored for this exercise. German comprehension can make tense mark-critical: for a past-events question, an answer in the present tense scores 0.',
  scale: {
    name: 'Comprehension · tense-critical',
    levels: two(0, 4),
    notes: [
      'Some comprehension answers are tense-critical.',
      'For a past-events question, the scheme marks a present-tense answer as “Present Tense = 0”.',
      'Finding the right information isn’t enough — the tense must match what the question asks.',
    ],
    cite: MS('p.[5] (tense-critical marking, Present Tense = 0)'),
  },
  scripts: [
    {
      id: 'ge3-a',
      label: 'The answer',
      persona: 'Correct fact, present tense',
      work: ['Finds the correct information.', 'Writes it in the present tense — the question was about the past.'],
      keyLevelId: 'm0',
      keyNote:
        '0 marks — where the scheme flags a question as tense-critical, a present-tense answer to a past-events question scores nothing, even with the right content. Read what the question is asking about in time, and match your verb tense to it. The fact was there; the tense threw it away.',
      embodies: {
        behaviour: 'Answers a past-events question in the present tense — scored 0 where tense is mark-critical.',
        cite: MS('p.[5]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de3',
    rule: 'Match the tense the question asks about.',
    detail:
      'German comprehension can make tense decisive — the right fact in the wrong tense (present for a past-events question) scores 0. Check the time frame of the question and put your verb in the matching tense.',
    cite: MS('p.[5]'),
  },
};

// ─────────────── Ge4 · The aural — check the language per section ───────────────

const GE4: ScaleSession = {
  mode: 'scale',
  id: 'de-aural-language',
  subject: 'german',
  level: 'common',
  title: 'The aural switches languages on you',
  cue: 'Aural',
  question: 'In the German listening test, the required answer language changes by section — one section is answered in English (the interview), another requires German (a phone-message note). A candidate answers the German-required section in English, out of habit. What happens?',
  questionNote:
    'Scenario authored for this exercise. The German aural requires answers in different languages by section, and a section answered in the wrong language is halved.',
  scale: {
    name: 'Aural · language per section',
    levels: [
      { id: 'half', label: 'Half marks (wrong language)', annotation: '½', marks: 4 },
      { id: 'full', label: 'Full (right language)', annotation: '✓', marks: 8 },
    ],
    notes: [
      'The aural sets the answer language per section — some English, some German.',
      'A whole section answered in the wrong language is halved.',
      'Read the instruction at the top of each section before you write.',
    ],
    cite: MS('p.[23] (aural: language flips per section; half-marks penalty)'),
  },
  scripts: [
    {
      id: 'ge4-a',
      label: 'The section',
      persona: 'Answers in English out of habit',
      work: ['A section that required answers in German.', 'Answered in English by habit — the previous section was English.'],
      keyLevelId: 'half',
      keyNote:
        'Halved — the section required German and got English. The German aural deliberately switches the required language between sections, so a habit carried over from the last section costs half the marks. Check the instruction line at the start of each section and answer in the language it names.',
      embodies: {
        behaviour: 'Answers an aural section in the wrong language, where the requirement flips per section — halved.',
        cite: MS('p.[23]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de4',
    rule: 'The aural sets the language per section — check each one.',
    detail:
      'The German listening test requires different answer languages in different sections; a section in the wrong language is halved. Read the instruction at the top of every section and answer in the language it specifies.',
    cite: MS('p.[23]'),
  },
};

export const GERMAN_CHAIR: ChairSubject = {
  id: 'german',
  label: 'German',
  tagline: 'The length gate, half-mark lifts and tense-critical answers.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [GE1, GE2, GE3, GE4],
  sources: [
    { label: 'SEC LC German HL marking scheme 2025 (examiner-reports/german/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the written-paper conventions — the Lower-E length gate, the half-mark rule for unmanipulated lifts and tense-critical comprehension — which apply at both Higher and Ordinary level (the oral is a separate scheme). Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
