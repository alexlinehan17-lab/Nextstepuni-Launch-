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

// ─────────────── Ge8 · Accept the first answer only ───────────────

const GE8: ScaleSession = {
  mode: 'scale',
  id: 'de-first-answer',
  subject: 'german',
  level: 'common',
  title: 'Hedging costs you the point',
  cue: 'Comprehension',
  question:
    'A comprehension question has one right answer. Unsure, the candidate writes two — the first one wrong, the second one correct — hoping the right one will be spotted and credited. On a 2-mark point, what does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s global rule: where a candidate answers a question more than once, the examiner accepts the first answer only — a right second answer behind a wrong first one is never reached.',
  scale: {
    name: 'Comprehension · first answer only',
    levels: two(0, 2),
    notes: [
      'Global rule: “Where the candidate answers a question more than once, accept the first answer only.”',
      'The examiner does not scan both answers and pick the correct one — only answer #1 is marked.',
      'Cancelled answers are re-read only “where no other answer has been given”.',
      'So hedging with a second answer cannot bank the mark; a wrong first answer stands.',
    ],
    cite: MS('p.[3] (“accept the first answer only”)'),
  },
  scripts: [
    {
      id: 'ge8-a',
      label: 'The answer',
      persona: 'Two answers, wrong one first',
      work: ['Gives two answers to a single-answer question.', 'First answer is wrong; the correct one is written second.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the examiner marks the first answer only, and the first one is wrong, so the correct second answer is never reached. Hedging does not bank the mark; it throws it away when you lead with the weaker option. Commit to one answer, and make it your best one.',
      embodies: {
        behaviour: 'Offers a wrong first answer and a right second one, where only the first is marked — scored on the wrong one.',
        cite: MS('p.[3]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de8',
    rule: 'Only your first answer is marked.',
    detail:
      'German comprehension accepts the first answer only where a question is answered more than once. A correct answer written second, behind a wrong first one, scores nothing. Decide on one answer and lead with it — never hedge.',
    cite: MS('p.[3]'),
  },
};

// ─────────────── Ge9 · Over-answering is safe ───────────────

const GE9: ScaleSession = {
  mode: 'scale',
  id: 'de-over-answer',
  subject: 'german',
  level: 'common',
  title: 'One weak extra can’t drag you down',
  cue: 'Schriftliche Produktion',
  question:
    'The letter task says answer any four of the five bullet points. A candidate answers all five — but the fifth is thin and half-relevant. Does attempting that weak fifth point pull the Content mark down?',
  questionNote:
    'Scenario authored for this exercise. The scheme instructs examiners to mark all attempted points and select the best four (letter) or five (photo) — over-answering is not penalised.',
  scale: {
    name: 'Content · best-of selected',
    levels: [
      { id: 'capped', label: 'Weak extra drags Content down', annotation: '✗', marks: 20 },
      { id: 'best', label: 'Best four kept, extra ignored', annotation: '✓', marks: 25 },
    ],
    notes: [
      'Letter: answer any four of five points; photo: any five of six.',
      'Rule: “Where a candidate has answered more than four, mark all and pick the best four for final mark.”',
      'The examiner scores every attempted point and keeps the strongest four (or five) — the weak extra is simply dropped, not subtracted.',
      'So a spare attempt can only help: if it beats one of your four, it replaces it; if not, it costs nothing.',
    ],
    cite: MS('p.[16] (“mark all and pick the best four”); p.[17] (best five)'),
  },
  scripts: [
    {
      id: 'ge9-a',
      label: 'The answer',
      persona: 'Answers all five, one is thin',
      work: ['Answers all five bullet points where four were required.', 'The fifth is thin and only half-relevant.'],
      keyLevelId: 'best',
      keyNote:
        'Full — the examiner marks all five and keeps the best four, so the thin fifth is dropped, never subtracted. Over-answering is a free option: a spare point can only replace a weaker one or be ignored. If you have time and a fifth idea, write it; it cannot cost you.',
      embodies: {
        behaviour: 'Attempts more points than required, where the scheme selects the best four — the weak extra is discarded, not penalised.',
        cite: MS('p.[16]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de9',
    rule: 'Extra points are marked and the best kept.',
    detail:
      'German written production marks every point you attempt and keeps the best four (letter) or five (photo). A weak extra is dropped, never subtracted — so over-answering can only help. If you have a spare idea and time, add it.',
    cite: MS('p.[16]'),
  },
};

// ─────────────── Ge10 · The letter frame is worth four marks ───────────────

const GE10: GridSession = {
  mode: 'grid',
  id: 'de-letter-frame',
  subject: 'german',
  level: 'common',
  title: 'The letter’s frame is four marks a photo-answer never earns',
  cue: 'Schriftliche Produktion (Brief)',
  question:
    'In the letter option, the opening is worth 2 marks and the closing 2 marks — 4 marks of “frame” before any content. Each is split: a required structural element (1) plus a development (1). Mark the openings and closings below.',
  questionNote:
    'Answers authored for this exercise; the mark split is the real SEC template. Op. (2) = suitable opening / bare minimum (1) + appropriate elaboration OR reference to the letter (1); Cl. (2) = suitable transition to ending (1) + appropriate closing formula (1).',
  grid: {
    perPoint: [
      { id: 'marker', label: 'Structural marker (greeting / transition to ending)', marks: 1 },
      { id: 'develop', label: 'Development (opening elaboration or reference / closing formula)', marks: 1 },
    ],
    shorthand: '2×2 (1+1)',
    ruleNote:
      'The opening and closing are each 2 marks, split 1 (the structural marker) + 1 (the development). A bare greeting with no reference to the letter earns 1 of 2; a sign-off with no transition sentence earns 1 of 2. Skip the frame entirely — as a photo-response candidate can — and you forfeit 4 marks the letter demands.',
    cite: MS('p.[16] (“Op. (2)” / “Cl. (2)” splits)'),
  },
  scripts: [
    {
      id: 'ge10-a',
      label: 'Script A',
      persona: 'Straight to business',
      attempts: [
        {
          id: 'ge10-a-1',
          text: 'Opening: „Liebe Andrea,“ — then straight into answering point A.',
          key: { marker: 1, develop: 0 },
          keyNote:
            'The greeting is there (bare minimum, 1) but there is no elaboration and no reference to Andrea’s letter, so the second mark is lost. 1/2.',
        },
        {
          id: 'ge10-a-2',
          text: 'Closing: ends with just „Tschüss, deine Sarah“.',
          key: { marker: 0, develop: 1 },
          keyNote:
            'A closing formula is present („deine Sarah“, 1) but there is no transition sentence easing into the ending, so the transition mark is lost. 1/2.',
        },
      ],
      embodies: {
        behaviour: 'Supplies half of each frame element — greeting without reference, sign-off without transition.',
        cite: MS('p.[16]'),
      },
    },
    {
      id: 'ge10-b',
      label: 'Script B',
      persona: 'Frames it properly',
      attempts: [
        {
          id: 'ge10-b-1',
          text: 'Opening: „Liebe Andrea, vielen Dank für deinen Brief! Schön, von dir zu hören.“',
          key: { marker: 1, develop: 1 },
          keyNote: 'Greeting present (1) and a genuine reference back to Andrea’s letter (1). Full 2/2.',
        },
        {
          id: 'ge10-b-2',
          text: 'Closing: „Ich muss jetzt leider Schluss machen. Schreib mir bald zurück! Deine Sarah“',
          key: { marker: 1, develop: 1 },
          keyNote: 'A transition sentence eases into the ending (1) and a proper closing formula signs off (1). 2/2.',
        },
      ],
      embodies: {
        behaviour: 'Provides both the structural marker and the development in each of the opening and closing.',
        cite: MS('p.[16]'),
      },
    },
    {
      id: 'ge10-c',
      label: 'Script C',
      persona: 'Writes it like a photo response',
      attempts: [
        {
          id: 'ge10-c-1',
          text: 'Opening: no greeting at all — begins „Ich trainiere jeden Tag Breaking …“.',
          key: { marker: 0, develop: 0 },
          keyNote:
            'No greeting and no reference to the letter — the whole 2-mark opening is forfeited. This is the photo-response habit: diving straight into content. 0/2.',
        },
        {
          id: 'ge10-c-2',
          text: 'Closing: the letter simply stops after the last point — no ending.',
          key: { marker: 0, develop: 0 },
          keyNote:
            'No transition and no closing formula, so both closing marks are gone. The frame the letter task demands is missing entirely. 0/2.',
        },
      ],
      embodies: {
        behaviour: 'Omits the opening and closing frame entirely, forfeiting the 4 structural marks unique to the letter option.',
        cite: MS('p.[16]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de10',
    rule: 'The letter’s opening and closing are 4 marks — earn them.',
    detail:
      'The letter option scores Op. (2) and Cl. (2) before any content: a greeting plus a reference to the letter, and a transition sentence plus a closing formula. Each is 1+1. Skip the frame — as a photo response can — and you drop four marks the letter demands.',
    cite: MS('p.[16]'),
  },
};

// ─────────────── Ge11 · Quote the phrase, not the mood ───────────────

const GE11: ScaleSession = {
  mode: 'scale',
  id: 'de-language-spotting',
  subject: 'german',
  level: 'common',
  title: 'Name the phrase, not the tone',
  cue: 'Aural',
  question:
    'The phone-call section asks for three examples of the language used that show the caller is happy. The candidate writes “he sounds cheerful and enthusiastic” — an accurate reading of his tone. On a 2-mark example, what does it score?',
  questionNote:
    'Scenario authored for this exercise. This aural sub-task credits cited expressions and phrases only — there are no marks for describing tone of voice or intonation without quoting specific language.',
  scale: {
    name: 'Aural · language evidence',
    levels: two(0, 2),
    notes: [
      'The task asks for “examples of the language used (= expressions and phrases)” that show the caller is happy.',
      'Rule: “no marks for tone of voice / intonation without reference to specific expressions and phrases.”',
      'You must cite the actual words — an accurate exact phrase or an accurate paraphrase in translation is accepted.',
      'Describing the mood (“he sounds happy”) is not evidence of language; it scores nothing.',
    ],
    cite: MS('p.[24] (“no marks for tone of voice / intonation …”)'),
  },
  scripts: [
    {
      id: 'ge11-a',
      label: 'The answer',
      persona: 'Describes the mood, quotes nothing',
      work: ['Writes “he sounds cheerful and enthusiastic”.', 'Cites no actual expression or phrase from the call.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the task wants the language, not the mood. “He sounds happy” describes tone of voice, which earns nothing here; the marks attach to a cited phrase like „einfach toll!“ or „eine wunderbare Aussicht“. Write down the words the speaker actually used, or a faithful paraphrase of them.',
      embodies: {
        behaviour: 'Reports the speaker’s tone rather than quoting a specific expression — awarded no marks under the language-evidence rule.',
        cite: MS('p.[24]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de11',
    rule: 'Evidence means a phrase, not a mood.',
    detail:
      'Where the aural asks for language that shows an attitude, only a cited expression or phrase (or a faithful paraphrase) scores — “he sounds happy” earns nothing. Note the actual words the speaker uses, not your reading of their tone.',
    cite: MS('p.[24]'),
  },
};

// ─────────────── Ge12 · All-or-nothing items ───────────────

const GE12: ScaleSession = {
  mode: 'scale',
  id: 'de-all-or-nothing',
  subject: 'german',
  level: 'common',
  title: 'One digit wrong, the whole item gone',
  cue: 'Aural',
  question:
    'The phone-message section asks the candidate to note the caller’s contact number, worth 2 marks and marked all-or-nothing. The candidate hears it almost perfectly but transposes one digit. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Certain aural items — a phone number, an age range — are marked all-or-nothing: every element must be right, with no part-marks for “nearly”.',
  scale: {
    name: 'Aural · all-or-nothing item',
    levels: two(0, 2),
    notes: [
      'The scheme flags certain items “All or nothing”: e.g. the contact number “0171 63 72 9 1 0” (2 marks) and the age range “16 to 80” (2 marks).',
      'Every digit / element must be correct — one wrong digit zeroes the whole item.',
      'There is no partial credit for getting most of it; the item is scored as a single unit.',
      'These are the items to double-check on the final playing.',
    ],
    cite: MS('p.[23] (“All or nothing: Kontaktnummer …”); p.[27] (“16 to 80 … all or nothing”)'),
  },
  scripts: [
    {
      id: 'ge12-a',
      label: 'The answer',
      persona: 'One digit off',
      work: ['Notes the contact number almost perfectly.', 'Transposes a single digit within it.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — this item is all-or-nothing, so a single wrong digit zeroes the full 2 marks, however close the rest is. There is no “most of it” credit for a phone number or an age range. Treat these items as unforgiving and confirm every digit on the last playing before you commit.',
      embodies: {
        behaviour: 'Gets an all-or-nothing item nearly right with one wrong digit — scored 0, with no partial credit.',
        cite: MS('p.[23]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de12',
    rule: 'All-or-nothing items give no part-marks.',
    detail:
      'Numbers and ranges in the German aural — a phone number, an age band — are marked all-or-nothing: one wrong element zeroes the whole item. “Nearly right” earns nothing. Verify every digit of these items on the final playing.',
    cite: MS('p.[23]'),
  },
};

// ─────────────── Ge13 · A quote without explanation ───────────────

const GE13: ScaleSession = {
  mode: 'scale',
  id: 'de-explain-quote',
  subject: 'german',
  level: 'common',
  title: 'A German quote alone proves nothing',
  cue: 'Comprehension',
  question:
    'A 5-mark question asks the candidate to give an example of change in the text, allowing either content or language use as evidence. The candidate copies a German phrase from the text and stops — no explanation of why it shows change. How does it score?',
  questionNote:
    'Scenario authored for this exercise. Where a question invites a quotation as evidence, the scheme flags that a German quote given with no explanation scores 0 — the candidate must show what it demonstrates.',
  scale: {
    name: 'Comprehension · quote + explanation',
    levels: two(0, 5),
    notes: [
      'The question allows language use and/or content as the example of change.',
      'Rule printed on the item: “German only without explanation = 0”.',
      'A lifted German phrase with no comment does not show the candidate has understood why it demonstrates the point.',
      'Explain what the quotation shows — the explanation is what earns the marks.',
    ],
    cite: MS('p.[8] (“German only without explanation =0”)'),
  },
  scripts: [
    {
      id: 'ge13-a',
      label: 'The answer',
      persona: 'Quotes and stops',
      work: ['Copies a German phrase from the text as the example.', 'Gives no explanation of why it shows change.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — “German only without explanation = 0”. The bare quote may point at the right line, but without saying what it demonstrates it shows no understanding, so the item scores nothing. Pair every quotation with a sentence explaining the change it illustrates; the explanation is where the marks live.',
      embodies: {
        behaviour: 'Provides a German quotation with no explanation where explanation is required — scored 0.',
        cite: MS('p.[8]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de13',
    rule: 'A quote needs an explanation to score.',
    detail:
      'Where a German question invites a quotation as evidence, “German only without explanation = 0”. A lifted phrase alone proves nothing — you must explain what it shows. Always follow the quote with the point it demonstrates.',
    cite: MS('p.[8]'),
  },
};

// ─────────────── Ge14 · The wrong referent ───────────────

const GE14: ScaleSession = {
  mode: 'scale',
  id: 'de-referent',
  subject: 'german',
  level: 'common',
  title: 'Right detail, wrong person',
  cue: 'Comprehension',
  question:
    'A question asks about Till’s first encounter with a girl, Feli. The candidate reports a correct detail but refers to Feli as “he” throughout, having misread who the character is. On a 2-mark point, what happens?',
  questionNote:
    'Scenario authored for this exercise. The scheme zeroes a content point pinned to the wrong referent — “Reference to Feli as ‘he’ = 0” — but applies the penalty once only across the answer.',
  scale: {
    name: 'Comprehension · referential accuracy',
    levels: two(0, 2),
    notes: [
      'Rule printed on the item: “Reference to Feli as ‘he’ = 0. Penalise once only.”',
      'A detail attached to the wrong person shows the text was misread, so the point scores 0.',
      '“Penalise once only” — the referent error is docked a single time, not on every subsequent point.',
      'Track who is who in the text before you write the detail down.',
    ],
    cite: MS('p.[7] (“Reference to Feli as ‘he’=0. Penalise once only”)'),
  },
  scripts: [
    {
      id: 'ge14-a',
      label: 'The answer',
      persona: 'Correct detail, wrong gender/referent',
      work: ['Reports a correct detail about the encounter.', 'Calls Feli “he” throughout, having misread the character.'],
      keyLevelId: 'm0',
      keyNote:
        '0 on this point — the detail is right, but pinning it to the wrong person (“he” for Feli) shows the text was misread, so the scheme zeroes it. The saving grace is “penalise once only”: the referent slip is docked a single time, not on every following answer. Get clear on who each character is before you commit a detail.',
      embodies: {
        behaviour: 'Attaches a correct detail to a mis-identified referent — scored 0, penalised once only.',
        cite: MS('p.[7]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de14',
    rule: 'A detail on the wrong person scores zero.',
    detail:
      'German comprehension zeroes a content point tied to the wrong referent — a correct detail said of the wrong character scores 0 (“penalise once only”). Fix who is who in the text before you write, so your details land on the right person.',
    cite: MS('p.[7]'),
  },
};

// ─────────────── Ge15 · Discretionary marks reward elaboration ───────────────

const GE15: ScaleSession = {
  mode: 'scale',
  id: 'de-discretionary',
  subject: 'german',
  level: 'common',
  title: 'Elaboration earns the discretionary mark',
  cue: 'Schriftliche Produktion',
  question:
    'Two candidates make the same required point in the letter. One states it plainly and moves on; the other adds a relevant reason and a personal detail. Beyond the point’s own mark, what extra is on offer for the elaboration?',
  questionNote:
    'Scenario authored for this exercise. On top of the fixed content points, the scheme reserves discretionary marks (five in Schriftliche Produktion, two in Äußerung) for additional relevant elaboration or comment.',
  scale: {
    name: 'Content · point + discretionary',
    levels: [
      { id: 'bare', label: 'Bare point only', annotation: '1', marks: 1 },
      { id: 'elaborated', label: 'Point + relevant elaboration', annotation: '2', marks: 2 },
    ],
    notes: [
      'Each fixed content point earns its stated mark (e.g. 1) for being made.',
      'On top, “Five discretionary marks are available … for additional relevant elaboration or comment” (two in Äußerung).',
      'The discretionary mark rewards developing a point — a reason, an example, a personal detail — beyond the bare statement.',
      'So the same point, elaborated, can out-score the same point stated flat.',
    ],
    cite: MS('p.[16] (“Five discretionary marks … for additional relevant elaboration or comment”); p.[13] (2 in Äußerung)'),
  },
  scripts: [
    {
      id: 'ge15-a',
      label: 'The answer',
      persona: 'Develops the point',
      work: ['Makes the required point.', 'Adds a relevant reason and a personal detail — genuine elaboration.'],
      keyLevelId: 'elaborated',
      keyNote:
        'The point earns its own mark, and the relevant elaboration earns a discretionary mark on top — 2 where the flat version scored 1. The scheme banks up to five such marks across the letter for developing your points. Don’t just tick the box: give a reason, an example, a personal angle, and let the discretionary marks add up.',
      embodies: {
        behaviour: 'Elaborates a required point with relevant detail, earning a discretionary mark beyond the point’s own value.',
        cite: MS('p.[16]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-de15',
    rule: 'Elaboration wins discretionary marks.',
    detail:
      'Beyond the fixed content points, German reserves discretionary marks — five in Schriftliche Produktion, two in Äußerung — for relevant elaboration or comment. Developing a point with a reason or personal detail out-scores stating it flat. Elaborate every point you can.',
    cite: MS('p.[16]'),
  },
};

export const GERMAN_CHAIR: ChairSubject = {
  id: 'german',
  label: 'German',
  tagline:
    'The length gate, half-mark lifts, tense-critical answers, the three-way Applied Grammar split, the letter frame, all-or-nothing items — and why near-right scores zero.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [GE1, GE2, GE3, GE4, GE5, GE6, GE7, GE8, GE9, GE10, GE11, GE12, GE13, GE14, GE15],
  sources: [
    { label: 'SEC LC German HL marking scheme 2025 (examiner-reports/german/2025-marking-scheme)' },
    { label: 'SEC LC German syllabus, Oral Assessment (examiner-reports/german/german-syllabus)' },
  ],
  coverageNote:
    'These sessions teach the written-paper conventions — the Lower-E length gate, the half-mark rule for unmanipulated lifts, first-answer-only marking, over-answer safety, the letter’s opening/closing frame, tense-critical and referential comprehension, the quote-needs-explanation and zero-for-approximation detail rules, the aural language-evidence and all-or-nothing items, and the discretionary marks for elaboration — plus the oral (25% at Higher, 20% at Ordinary), assessed on language and communication rather than information content. Most apply at both levels; the Applied Grammar (Angewandte Grammatik) verb-scoring session is Higher-Level-specific and shows only under the Higher tab. Written rules verified against the 2025 Higher Level scheme (Lower-E, unmanipulated-lift, aural-language, all-or-nothing and discretionary-mark rules cross-checked against the 2024 scheme); the oral against the SEC German syllabus. Level-specific worked examples are being added.',
};
