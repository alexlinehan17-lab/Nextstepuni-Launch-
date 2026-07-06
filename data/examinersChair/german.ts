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
 * The oral session (Ge5) is instead cited to the official SEC/NCCA LC German
 * syllabus (Oral Assessment, criteria and weighting) —
 * examiner-reports/german/german-syllabus.* — because SEC does not publish a
 * per-mark oral marking scheme. Its refs use the syllabus's printed page numbers.
 * Page refs use the PDF page number (runs ~2 ahead of the printed page).
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel, type GridSession } from './types';

const MS = (p: string) => ({ label: `SEC German HL marking scheme 2025, ${p}` });

// The oral is NOT covered by the written marking scheme (SEC issues the oral
// interviewers' instructions confidentially). Its assessment structure, criteria
// and mark weighting are set out in the official SEC/NCCA LC German syllabus —
// this is the verifiable public source for the oral, filed at
// examiner-reports/german/german-syllabus.*. Do NOT relabel this as the written
// marking scheme. Page refs are the syllabus's printed page numbers.
const ORAL = (p: string) => ({ label: `SEC LC German syllabus (Ordinary & Higher), ${p}` });

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

// ─────────────── Ge5 · The oral marks language, not information ───────────────

const GE5: ScaleSession = {
  mode: 'scale',
  id: 'de-oral-criteria',
  subject: 'german',
  level: 'common',
  title: 'They mark how you say it, not what you know',
  cue: 'Mündliche Prüfung',
  question:
    'In the general conversation, the examiner asks about your summer. You reel off an impressive amount of information — places, dates, names — but in halting German with lots of errors and a narrow range of vocabulary. The oral is worth a big slice of the grade. Does packing in the facts protect your mark?',
  questionNote:
    'Scenario authored for this exercise. The real SEC system: the oral is worth 25% at Higher Level (20% at Ordinary) and is assessed on language and communication — the ability to transfer meaning and the accuracy, appropriateness and range of vocabulary and structures — NOT on the information content of what you say.',
  scale: {
    name: 'Oral · what earns the marks',
    levels: [
      { id: 'content', label: 'Information content of the answer', annotation: '✗', marks: 0 },
      { id: 'language', label: 'Transfer of meaning + accuracy & range', annotation: '✓', marks: 25 },
    ],
    notes: [
      'The oral (speaking) is worth 25% of the grade at Higher Level and 20% at Ordinary Level — more marks go to productive skills at Higher Level.',
      'The syllabus states assessment "will emphasise language and communication skills rather than the information content of any particular section".',
      'The oral assessment criteria take account of (i) ability to transfer meaning and (ii) degrees of accuracy and appropriateness of language, including the range of vocabulary and structures used.',
      'Structure: general conversation + one of {project / picture sequence} + a role-play; fifteen minutes per candidate.',
    ],
    cite: ORAL('printed p.25 (Mark Allocation; Assessment Criteria) & p.26 (Oral Assessment)'),
  },
  scripts: [
    {
      id: 'ge5-a',
      label: 'The answer',
      persona: 'Facts-heavy, language-thin',
      work: [
        'Delivers lots of information — places, dates, names.',
        'German is halting and error-filled, with a narrow range of vocabulary.',
      ],
      keyLevelId: 'content',
      keyNote:
        'The pile of facts earns nothing on its own — the oral marks language and communication, not the information content. What scores is transferring meaning clearly and showing accurate, appropriate, wide-ranging vocabulary and structures. A simpler answer said in good German beats an information-packed one said badly. Prepare range and accuracy, not just things to say.',
      embodies: {
        behaviour:
          'Answers with rich information but weak, narrow language, where the oral credits language/communication over information content.',
        cite: ORAL('p.2 (language over information content) & p.25 (Assessment Criteria)'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de5',
    rule: 'The oral marks how you speak, not what you know.',
    detail:
      'German’s oral is 25% of the grade at Higher Level (20% at Ordinary) and is assessed on transfer of meaning and the accuracy, appropriateness and range of your vocabulary and structures — not on the information content. Build range and accuracy; a simpler point said in good German outscores a fact-dump said badly.',
    cite: ORAL('p.25 (Assessment Criteria) & p.2 (language over information content)'),
  },
};

// ─────────────── Ge6 · Applied Grammar — the verb splits three ways ───────────────

const GE6: GridSession = {
  mode: 'grid',
  id: 'de-applied-grammar',
  subject: 'german',
  level: 'higher',
  title: 'The verb splits three ways',
  cue: 'Angewandte Grammatik (Verben)',
  question:
    'In the Applied Grammar task (Verben option), each gap gives you an infinitive to put into the tense and number the text requires. Two of the items: (1) versuchen — Perfekt, singular; (2) verstehen — Perfekt, plural. Each item is worth 5 marks. Mark the three scripts below.',
  questionNote:
    'Answers authored for this exercise; the verb items and the mark split are the real SEC template. Each 5-mark verb item is scored: correct verb stem/lexis (2) + correct tense (2) + correct number (1) — e.g. the scheme’s key “versuchen (2), Perfekt (2), Singular (1)”.',
  grid: {
    perPoint: [
      { id: 'verb', label: 'Verb — correct stem/lexis', marks: 2 },
      { id: 'tense', label: 'Correct tense', marks: 2 },
      { id: 'number', label: 'Correct number (sing./plural)', marks: 1 },
    ],
    shorthand: '5×5 (2+2+1)',
    ruleNote:
      'Each verb is worth 5, split verb (2) + tense (2) + number (1). The three parts are scored independently, so the right verb in the wrong tense still forfeits its 2 tense marks, and a wrong verb takes the whole 5 — there is nothing left to award the tense or number to.',
    cite: MS('p.[9] (Angewandte Grammatik: “versuchen (2), Perfekt (2), Singular (1)”)'),
  },
  scripts: [
    {
      id: 'ge6-a',
      label: 'Script A',
      persona: 'Lexis solid, tense adrift',
      attempts: [
        {
          id: 'ge6-a-1',
          text: 'Item 1 (versuchen → Perfekt, sing.): schreibt „versuchte“.',
          key: { verb: 2, tense: 0, number: 1 },
          keyNote:
            'Right verb, singular is right — but „versuchte“ is Imperfekt, and the item fixed Perfekt („hat versucht“). The 2 tense marks are gone. 3/5.',
        },
        {
          id: 'ge6-a-2',
          text: 'Item 2 (verstehen → Perfekt, pl.): schreibt „verstehen“.',
          key: { verb: 2, tense: 0, number: 1 },
          keyNote:
            'Same failure: correct verb, plural is fine, but this is a plain present-tense form where Perfekt („haben verstanden“) was required. Tense marks lost again. 3/5.',
        },
      ],
      embodies: {
        behaviour:
          'Supplies the correct verb in the wrong tense, forfeiting the tense sub-marks in the atomised Applied Grammar scoring.',
        cite: MS('p.[9]'),
      },
    },
    {
      id: 'ge6-b',
      label: 'Script B',
      persona: 'Form and all',
      attempts: [
        {
          id: 'ge6-b-1',
          text: 'Item 1 (versuchen → Perfekt, sing.): schreibt „hat versucht“.',
          key: { verb: 2, tense: 2, number: 1 },
          keyNote: 'Correct verb, Perfekt, singular — all three parts land. Full 5/5.',
        },
        {
          id: 'ge6-b-2',
          text: 'Item 2 (verstehen → Perfekt, pl.): schreibt „haben verstanden“.',
          key: { verb: 2, tense: 2, number: 1 },
          keyNote: 'Verb, tense and plural agreement all correct. 5/5.',
        },
      ],
      embodies: {
        behaviour: 'Produces the required verb, tense and number, earning each of the three sub-marks.',
        cite: MS('p.[9]'),
      },
    },
    {
      id: 'ge6-c',
      label: 'Script C',
      persona: 'Two different ways to bleed marks',
      attempts: [
        {
          id: 'ge6-c-1',
          text: 'Item 2 (verstehen → Perfekt, pl.): schreibt „hat verstanden“.',
          key: { verb: 2, tense: 2, number: 0 },
          keyNote:
            'Verb right, Perfekt right — but the auxiliary is singular („hat“) where the text needed the plural „haben verstanden“. Only the 1 number mark is lost. 4/5.',
        },
        {
          id: 'ge6-c-2',
          text: 'Item 1 (versuchen → Perfekt, sing.): schreibt „hat gemacht“.',
          key: { verb: 0, tense: 0, number: 0 },
          keyNote:
            'Wrong verb entirely — machen, not versuchen. Once the lexis is wrong there is nothing to attach the tense or number marks to, so the whole item scores 0/5, even though the Perfekt and singular are “correct” in isolation.',
        },
      ],
      embodies: {
        behaviour:
          'Shows a number-agreement slip (loses 1) and a wrong-verb choice (loses all 5) — the two poles of the split-mark scoring.',
        cite: MS('p.[9]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de6',
    rule: 'The Applied Grammar verb splits three ways — verb, tense, number.',
    detail:
      'Each Angewandte Grammatik verb is 5 marks: 2 for the verb, 2 for the tense, 1 for the number, scored independently. The right verb in the wrong tense still drops 2; a wrong verb drops all 5. Nail all three parts, not just the word.',
    cite: MS('p.[9]'),
  },
};

// ─────────────── Ge7 · Near-right is wrong ───────────────

const GE7: ScaleSession = {
  mode: 'scale',
  id: 'de-precision',
  subject: 'german',
  level: 'common',
  title: 'Near-right is wrong',
  cue: 'Aural / Comprehension',
  question:
    'The News section asks for today’s weather forecast. The forecast said cloudy. The candidate has the gist and writes “overcast”. It’s close — near-synonymous, even. What does the point score?',
  questionNote:
    'Scenario authored for this exercise. German marking repeatedly zeroes an almost-right word rather than giving partial credit: the scheme prints “cloudy (overcast=0)” beside this very detail.',
  scale: {
    name: 'Detail · precise vs approximate',
    levels: two(0, 1),
    notes: [
      'Detail questions want the exact word the text used, not a near-synonym.',
      'The scheme writes the near-miss straight into the key and zeroes it: “cloudy (overcast=0)”, “women eat more healthily … (Are healthier = 0)”, “Playground/play area (Plural = 0)”.',
      'The same rigour runs through the reading texts: a person who “smiles” is not one who laughs — “(Laugh=0)”.',
      'There is no half credit for “close”: the approximate word forfeits the whole point.',
    ],
    cite: MS('p.[28] (“cloudy (overcast=0)”); p.[27] (“Are healthier = 0”, “Plural = 0”); p.[7] (“Laugh=0”)'),
  },
  scripts: [
    {
      id: 'ge7-a',
      label: 'The answer',
      persona: 'Close, but not the word',
      work: ['The forecast was “cloudy”.', 'Writes “overcast” — near-synonymous, but not what the text said.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the scheme literally prints “overcast=0” next to this answer. German detail-marking wants the precise word the speaker used, and gives no partial credit for an approximation. “Are healthier” for “eat more healthily”, a singular where a plural was needed, “laugh” for “smile” — all zeroed the same way. Hear the exact word and write the exact word.',
      embodies: {
        behaviour: 'Gives a near-synonym where the exact detail was required — zeroed, not part-credited.',
        cite: MS('p.[28] & p.[27]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de7',
    rule: 'A near-right answer scores zero, not half.',
    detail:
      'German detail questions credit the exact word only — “overcast” for cloudy, “are healthier” for eat more healthily, “laugh” for smile, a singular for a plural all score 0. There is no partial credit for “close”; capture the precise word the text uses.',
    cite: MS('p.[27] & p.[28]'),
  },
};

export const GERMAN_CHAIR: ChairSubject = {
  id: 'german',
  label: 'German',
  tagline:
    'The length gate, half-mark lifts, tense-critical answers, the three-way Applied Grammar split — and why near-right scores zero.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [GE1, GE2, GE3, GE4, GE5, GE6, GE7],
  sources: [
    { label: 'SEC LC German HL marking scheme 2025 (examiner-reports/german/2025-marking-scheme)' },
    { label: 'SEC LC German syllabus, Oral Assessment (examiner-reports/german/german-syllabus)' },
  ],
  coverageNote:
    'These sessions teach the written-paper conventions — the Lower-E length gate, the half-mark rule for unmanipulated lifts, tense-critical comprehension and the zero-for-approximation detail rule — plus the oral (25% at Higher, 20% at Ordinary), assessed on language and communication rather than information content. Most apply at both levels; the Applied Grammar (Angewandte Grammatik) verb-scoring session is Higher-Level-specific and shows only under the Higher tab. Written rules verified against the 2025 Higher Level scheme (Lower-E, unmanipulated-lift and aural-language rules cross-checked against the 2024 scheme); the oral against the SEC German syllabus. Level-specific worked examples are being added.',
};
