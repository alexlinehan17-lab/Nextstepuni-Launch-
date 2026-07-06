/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Italian marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the two Content/Language axes with a graduated content cap,
 * the −50% wrong-language penalty, the rote-off-the-point rule, and the
 * copy-vs-manipulate deduction on comprehension, the listening list rule where
 * one wrong item nullifies a correct one, and the separate 10-mark letter Format
 * block) is the real SEC system, cited to:
 *  - SEC LC Italian HL marking scheme 2025 —
 *    examiner-reports/italian/2025-marking-scheme.*
 *
 * The ORAL session (IT5) is cited to a DIFFERENT source — the official
 * SEC/NCCA Leaving Certificate Italian syllabus (examiner-reports/italian/
 * italian-syllabus.*), NOT the written marking scheme. SEC publishes NO
 * per-band oral marking grid, so the oral session teaches only what the
 * syllabus states — the Speaking weighting (25% HL / 20% OL), the oral format,
 * and the two Assessment Criteria (transfer of meaning; accuracy &
 * appropriateness) — and any band marks in its scale are labelled ILLUSTRATIVE.
 *
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel, type GridSession } from './types';

const MS = (p: string) => ({ label: `SEC Italian HL marking scheme 2025, ${p}` });
// Oral cite → the syllabus, NOT the written marking scheme.
const ORAL = (p: string) => ({ label: `SEC/NCCA LC Italian syllabus, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── IT1 · The graduated content cap ───────────────

const IT1: ScaleSession = {
  mode: 'scale',
  id: 'it-content-cap',
  subject: 'italian',
  level: 'common',
  title: 'Weak content, capped language',
  cue: 'Written production',
  question: 'A short written task is scored Content 15 + Language 10. A candidate writes accurate Italian, but the content barely addresses the task, scoring 7 or below. The scheme caps Language at 5 (out of 10) when content is 7 or less. What’s the most Language can score?',
  questionNote:
    'Scenario authored for this exercise. Italian marks writing on two axes (Content & Communication + Language); a graduated rule caps the Language mark when content is weak (content ≤7 → Language out of 5).',
  scale: {
    name: 'Language · graduated cap /10',
    levels: two(5, 10),
    notes: [
      'Writing is scored Content 15 + Language 10, summed.',
      'Graduated cap: if content is 7 or less, Language is marked out of 5.',
      'So accurate Italian on a weak-content answer can’t score more than 5 for Language.',
    ],
    cite: MS('p.26 (content-caps-Language rule)'),
  },
  scripts: [
    {
      id: 'it1-a',
      label: 'The answer',
      persona: 'Good Italian, thin content',
      work: ['Accurate Italian throughout.', 'Content barely addresses the task — scores ≤7.'],
      keyLevelId: 'm5',
      keyNote:
        'Language is capped at 5 of 10 — weak content drags the language mark down with it, though not to zero. Italian ties the axes loosely: you can’t bank full language marks on accurate-but-off-task writing. Address the task properly first; then your accuracy pays in full.',
      embodies: {
        behaviour: 'Writes accurate but thin-content Italian, triggering the graduated Language cap.',
        cite: MS('p.26'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it1',
    rule: 'Weak content caps your language mark.',
    detail:
      'Italian marks writing on two axes, but a content of 7 or less caps Language at 5/10. Accurate Italian can’t reach full language marks if the content doesn’t address the task — answer the task first.',
    cite: MS('p.26'),
  },
};

// ─────────────── IT2 · Wrong language = −50% ───────────────

const IT2: ScaleSession = {
  mode: 'scale',
  id: 'it-wrong-language',
  subject: 'italian',
  level: 'common',
  title: 'The wrong language halves it',
  cue: 'Comprehension',
  question: 'A comprehension question must be answered in English (it asks for your opinion in English). The candidate answers it well — but in Italian. The 2025 scheme applies a 50% deduction for answering in the wrong language. What happens?',
  questionNote:
    'Scenario authored for this exercise. The English-answer requirement for the opinion question is standing across years; the explicit −50% figure is stated in the 2025 scheme (it is not reproduced in 2023/2024). Answering in Italian where English is required triggers that −50% deduction — far harsher than the −1 for excess material.',
  scale: {
    name: 'Wrong-language penalty',
    levels: two(5, 10),
    notes: [
      'Some comprehension questions must be answered in English (the scheme states the language).',
      'Answering in Italian where English is required = −50% of the marks gained.',
      'This is much harsher than the −1 excess-material penalty.',
    ],
    cite: MS('p.11, p.13 (−50% wrong-language penalty)'),
  },
  scripts: [
    {
      id: 'it2-a',
      label: 'The answer',
      persona: 'Answers in Italian',
      work: ['A good answer to a 10-mark opinion question.', 'Written in Italian — but English was required.'],
      keyLevelId: 'm5',
      keyNote:
        'Halved — a strong answer in the wrong language loses 50%. Read the instruction for each question: some want Italian, some want English, and mixing them up is one of the most expensive avoidable errors on the paper. Check the required language before you write each answer.',
      embodies: {
        behaviour: 'Answers in Italian where English is required — the −50% penalty applies.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it2',
    rule: 'Answer in the language the question demands.',
    detail:
      'Italian comprehension sets the answer language per question — the opinion question must be answered in English, and in the 2025 scheme answering it in Italian halves your marks. Check the required language on every question before you write.',
    cite: MS('p.11'),
  },
};

// ─────────────── IT3 · Don't rote off the point ───────────────

const IT3: ScaleSession = {
  mode: 'scale',
  id: 'it-rote',
  subject: 'italian',
  level: 'common',
  title: 'Learnt off, off the point',
  cue: 'Written production',
  question: 'A candidate has memorised a polished paragraph about their summer holidays and drops it into a written task that actually asks about their future career plans. The Italian is flawless. The scheme warns candidates “must not produce something learnt off by heart and off the point.” How does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme explicitly targets rote material that doesn’t address the task — a memorised passage off the point scores on neither axis it fails.',
  scale: {
    name: 'Rote, off-task',
    levels: two(0, 25),
    notes: [
      'The scheme: candidates “must not produce something learnt off by heart and off the point.”',
      'A memorised passage that doesn’t address the task fails the Content axis.',
      'And with content failing, the graduated cap pulls the Language mark down too.',
    ],
    cite: MS('p.27 (rote-off-the-point rule)'),
  },
  scripts: [
    {
      id: 'it3-a',
      label: 'The answer',
      persona: 'Perfect rote, wrong topic',
      work: [
        'A flawless memorised paragraph about summer holidays.',
        'The task asked about future career plans.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'It scores at the bottom — the content doesn’t address the task, and the scheme names rote-off-the-point exactly. Memorised chunks only pay when they genuinely fit the question. Adapt what you’ve prepared to the actual task; a perfect answer to a question you weren’t asked is worth almost nothing.',
      embodies: {
        behaviour: 'Drops in a memorised passage that doesn’t address the task — the rote-off-the-point failure.',
        cite: MS('p.27'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it3',
    rule: 'Prepared material must fit the actual task.',
    detail:
      'Italian explicitly penalises something “learnt off by heart and off the point.” Rehearsed paragraphs only score when they answer the question asked — adapt what you’ve prepared to the specific task in front of you.',
    cite: MS('p.27'),
  },
};

// ─────────────── IT4 · Copy where you can, manipulate where you must ───────────────

const IT4: ScaleSession = {
  mode: 'scale',
  id: 'it-manipulation',
  subject: 'italian',
  level: 'common',
  title: 'Copy where you can, manipulate where you must',
  cue: 'Reading comprehension',
  question:
    'A reading-comprehension point is built on a line of direct speech in the passage. To answer it you have to turn that quote into reported form — switch the verbs and pronouns into the narrator’s voice. The candidate instead copies the sentence out word-for-word. The Italian is lifted perfectly. How does the point score out of 5?',
  questionNote:
    'Scenario authored for this exercise. Italian reading comprehension lets you copy straight from the text when no manipulation is needed, but when the answer requires manipulation (e.g. altering the verbs and pronouns of direct speech into narrator voice) and it is not done, 1 mark is deducted. This copy-vs-manipulate rule is standing across years — worded near-identically in the 2024 (Section A) and 2025 (Sections A & B) schemes; cited here to 2025.',
  scale: {
    name: 'Manipulation · −1 if required and not done /5',
    levels: two(4, 5),
    notes: [
      'Evidence is needed that the candidate has understood the text.',
      'When manipulation is NOT necessary, material can be copied straight from the text.',
      'When manipulation IS required and not done — e.g. direct-speech verbs and pronouns not altered to narrator voice — 1 mark is deducted.',
    ],
    cite: MS('p.11 & p.13 (copy-vs-manipulate rule, Sections A & B)'),
  },
  scripts: [
    {
      id: 'it4-a',
      label: 'The answer',
      persona: 'Lifts the quote verbatim',
      work: [
        'The point turns on a line of direct speech in the passage.',
        'Answering it needs the verbs and pronouns switched to reported / narrator voice.',
        'The candidate copies the sentence word-for-word instead — no manipulation done.',
      ],
      keyLevelId: 'm4',
      keyNote:
        'It drops to 4 of 5 — the −1 manipulation deduction. Copying is allowed only when the question doesn’t need reshaping; here it did, and lifting the quote unchanged doesn’t prove you understood it. Read what the question asks you to do with the line: if it must become reported speech, change the verbs and pronouns before you write it down.',
      embodies: {
        behaviour:
          'Copies a direct-speech line verbatim where the answer required manipulation into narrator voice — the −1 deduction applies.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it4',
    rule: 'Copy when you can; manipulate when the question makes you.',
    detail:
      'Italian comprehension lets you lift material straight from the text when no reshaping is needed — but when the answer requires manipulation (turning direct speech into reported voice, altering verbs and pronouns) and you just copy, you lose a mark. Do the manipulation the question asks for.',
    cite: MS('p.11'),
  },
};

// ─────────────── IT5 · The oral rewards transfer of meaning, not recital ───────────────

const IT5: ScaleSession = {
  mode: 'scale',
  id: 'it-oral-transfer',
  subject: 'italian',
  level: 'common',
  title: 'The oral marks talking, not reciting',
  cue: 'Oral · general conversation',
  question:
    'In the oral (worth 25% of the Higher paper, 20% at Ordinary), the examiner asks about your weekend. You deliver a flawless paragraph you memorised about your summer holidays instead — polished, accurate Italian, but not an answer to the question. The syllabus says the oral is judged on (i) your ability to transfer meaning and (ii) accuracy and appropriateness — and that assessment emphasises “language and communication skills rather than the information content.” Where does a memorised, off-question chunk land?',
  questionNote:
    'Scenario authored for this exercise. Grounded in the SEC/NCCA LC Italian syllabus: Speaking is 25% at Higher / 20% at Ordinary; the oral is a general conversation + role-play + picture sequence (15 min); and the two Assessment Criteria are (i) ability to transfer meaning and (ii) accuracy and appropriateness of language. SEC does NOT publish a per-band oral marking grid — the band marks below are ILLUSTRATIVE, used only to show the direction of travel, not real SEC oral marks.',
  scale: {
    name: 'Oral response · ILLUSTRATIVE bands (no official SEC oral grid exists)',
    levels: [
      { id: 'il-low', label: 'Recited, off the question', annotation: 'L', marks: 3 },
      { id: 'il-mid', label: 'On topic, limited transfer', annotation: 'M', marks: 7 },
      { id: 'il-high', label: 'Genuine transfer + accuracy', annotation: 'H', marks: 12 },
    ],
    notes: [
      'Speaking is worth 25% of the exam at Higher Level, 20% at Ordinary Level.',
      'The oral is scored on two criteria: (i) ability to transfer meaning, and (ii) accuracy and appropriateness of language (range of vocabulary and structures).',
      'The syllabus states assessment emphasises “language and communication skills rather than the information content” — so a rehearsed passage that doesn’t answer the question can’t satisfy criterion (i).',
      'The band marks here are ILLUSTRATIVE only — SEC publishes no per-band oral marking grid; they show direction of travel, not real oral marks.',
    ],
    cite: ORAL(
      'Assessment §4, p.25 (Speaking 25% HL / 20% OL; Assessment Criteria (i)–(ii)) & Oral Assessment, p.26',
    ),
  },
  scripts: [
    {
      id: 'it5-a',
      label: 'The answer',
      persona: 'Perfect recital, wrong question',
      work: [
        'Examiner asks a simple conversational question (about the weekend).',
        'Candidate delivers a memorised paragraph on a different topic (summer holidays).',
        'The Italian is accurate and fluent — but it does not respond to what was asked.',
      ],
      keyLevelId: 'il-low',
      keyNote:
        'It lands at the bottom — accurate Italian, but the primary criterion is the ability to transfer meaning, and a rehearsed chunk that ignores the question transfers none. The syllabus is explicit that the oral rewards language and communication skills rather than information content: you have to actually answer the examiner, in real time, not perform a prepared speech. Prepare vocabulary and structures, then use them to say something true in response to what you are asked. (Band mark ILLUSTRATIVE — SEC publishes no per-band oral grid.)',
      embodies: {
        behaviour:
          'Delivers a prepared, off-question paragraph, so criterion (i) — ability to transfer meaning in response to what was asked — is not met, however accurate the Italian.',
        cite: ORAL('Assessment §4, p.25 (Assessment Criteria (i) ability to transfer meaning)'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it5',
    rule: 'In the oral, answer the question — don’t recite.',
    detail:
      'The Italian oral (25% Higher, 20% Ordinary) is marked on your ability to transfer meaning and on accuracy — and the syllabus says it emphasises language and communication skills, not information content. A polished, memorised answer to a question you weren’t asked fails the first criterion. Prepare the language, then use it to respond, in real time, to what the examiner actually asks. (Any per-band oral marks are illustrative — SEC publishes no official oral grid.)',
    cite: ORAL('Assessment §4, p.25; Preamble, p.2 (language rather than information content)'),
  },
};

// ─────────────── IT6 · One wrong guess cancels a right one ───────────────

const IT6: ScaleSession = {
  mode: 'scale',
  id: 'it-list-nullify',
  subject: 'italian',
  level: 'common',
  title: 'One wrong guess cancels a right one',
  cue: 'Listening · list answer',
  question:
    'A listening question asks you to name two of the languages a company wants its staff to speak. You catch two correct ones — but you’re not certain, so you add a third for safety, and the third is wrong. The 2025 aural scheme states that where a list of vocabulary is required, one incorrect answer nullifies a correct one. The question is worth 2 marks (1+1). What do you score?',
  questionNote:
    'Scenario authored for this exercise. The rule is from the 2025 aural marking scheme (Listening, Section B): where a list of vocabulary is required, one incorrect answer nullifies a correct answer, and an inaccurate combination of points means full marks are not awarded. So padding a list with extra guesses can actively cost marks.',
  scale: {
    name: 'List answer · one wrong cancels one right /2',
    levels: two(1, 2),
    notes: [
      'Some listening answers require a list of vocabulary (e.g. two of four languages), each item worth a mark.',
      'The scheme: “Where a list of vocabulary is required, one incorrect answer nullifies a correct answer.”',
      'So two correct items plus one wrong one nets one mark, not two — the wrong guess cancels a right answer.',
    ],
    cite: MS('p.5 (Listening Section B — list rule: one incorrect answer nullifies a correct answer)'),
  },
  scripts: [
    {
      id: 'it6-a',
      label: 'The answer',
      persona: 'Hedges with an extra guess',
      work: [
        'The question needs two languages; two marks (1+1).',
        'The candidate writes three: two are correct, the third is wrong.',
        'The wrong one nullifies one of the correct ones.',
      ],
      keyLevelId: 'm1',
      keyNote:
        'It nets 1 of 2 — the wrong guess cancels a right answer. On a list question, don’t hedge: writing every option you can think of doesn’t insure you, it exposes you, because one wrong item wipes out a correct one. Give exactly the number asked for, and only items you’re sure of.',
      embodies: {
        behaviour:
          'Adds an extra, incorrect item to a required list, triggering the one-wrong-nullifies-a-right rule.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it6',
    rule: 'On a list answer, don’t hedge — one wrong item cancels a right one.',
    detail:
      'In the Italian listening test, where a question asks for a list of vocabulary, one incorrect answer nullifies a correct one. Adding extra guesses to be safe can cost you marks — give exactly the number asked for, and only items you’re sure of.',
    cite: MS('p.5'),
  },
};

// ─────────────── IT7 · The format marks you can bank first ───────────────

const IT7: GridSession = {
  mode: 'grid',
  id: 'it-letter-format',
  subject: 'italian',
  level: 'common',
  title: 'The format marks you can bank first',
  cue: 'Formal writing · letter',
  question:
    'The formal-writing task (50 marks) scores Format as its own 10-mark block: Date, Address, Greeting, Closing formula and Final salutation, in the correct register and spelt correctly. Two candidates write equally strong Italian in the body. Mark each one’s FORMAT block out of 10.',
  questionNote:
    'Scenario and letters authored for this exercise. The Format mark and its component values are the SEC 2025 HL scheme’s formal-writing breakdown (Section C, C3): Date 1m · Address 2m (3m if the candidate chooses email) · Greeting 2m · Closing formula 3m · Final salutation 2m — 10 marks, scored on top of Content & Communication and Language.',
  grid: {
    perPoint: [
      { id: 'date', label: 'Date', marks: 1 },
      { id: 'address', label: 'Address', marks: 2 },
      { id: 'greeting', label: 'Greeting', marks: 2 },
      { id: 'closing', label: 'Closing formula', marks: 3 },
      { id: 'salutation', label: 'Final salutation', marks: 2 },
    ],
    shorthand: 'Format 10 (1+2+2+3+2)',
    ruleNote:
      'Format is a separate 10-mark block on the formal-writing task, awarded for the letter’s furniture — date, address, greeting, closing formula and final salutation — in the correct register and spelt correctly. These marks don’t depend on the quality of your argument; they’re there to be banked before you write a sentence of content, and lost outright if you skip the conventions.',
    cite: MS('p.27 (Formal Writing — Format 10m breakdown & register/spelling requirement)'),
  },
  scripts: [
    {
      id: 'it7-a',
      label: 'Script A',
      persona: 'Strong Italian, skips the furniture',
      attempts: [
        {
          id: 'it7-a-1',
          text: 'Dives straight into the body of the letter. No date, no address. Opens with a bare “Ciao” and signs off with just a first name — no closing formula, no proper final salutation.',
          key: { date: 0, address: 0, greeting: 0, closing: 0, salutation: 0 },
          keyNote:
            'The Italian inside may be excellent, but the whole format block is missing or wrong register — “Ciao” is not an appropriate greeting for a formal letter, and there is no closing formula or salutation. 0 of 10 on Format, before Content and Language are even counted.',
        },
      ],
      embodies: {
        behaviour:
          'Omits the letter’s format furniture (date, address, greeting, closing, salutation), forfeiting the separate 10-mark Format block.',
        cite: MS('p.27'),
      },
    },
    {
      id: 'it7-b',
      label: 'Script B',
      persona: 'Models the format in full',
      attempts: [
        {
          id: 'it7-b-1',
          text: 'Dates the letter and lays out the address. Opens with a full, register-appropriate greeting, develops the body, then signs off with a correct closing formula and a proper final salutation — all spelt correctly.',
          key: { date: 1, address: 2, greeting: 2, closing: 3, salutation: 2 },
          keyNote:
            'Every format component is present, in the right register, spelt correctly — full 10 of 10 on Format. This candidate banked a tenth of the whole task before the examiner read a word of the argument.',
        },
      ],
      embodies: {
        behaviour:
          'Supplies every format component in the correct register and spelling, earning the full 10-mark Format block.',
        cite: MS('p.27'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it7',
    rule: 'Bank the letter’s format marks — they’re free and separate.',
    detail:
      'The Italian formal-writing task scores Format as its own 10-mark block: date, address, greeting, closing formula and final salutation, in the correct register and spelt correctly. These marks are independent of your argument — learn the conventions and bank all ten before you write a line of content.',
    cite: MS('p.27'),
  },
};

// ─────────────── IT8 · Excess material costs a mark ───────────────

const IT8: ScaleSession = {
  mode: 'scale',
  id: 'it-excess-material',
  subject: 'italian',
  level: 'common',
  title: 'The extra sentence that costs you',
  cue: 'Reading comprehension',
  question:
    'A reading point is worth 5 marks and the candidate gives the correct answer — then keeps going, copying out two further sentences from the passage that the question never asked for. The scheme deducts 1 mark for “excess and redundant material.” What does the point score?',
  questionNote:
    'Scenario authored for this exercise. The excess/redundant-material deduction is a standing reading-comprehension rule — printed on the Section A journalistic instructions (p.11) and repeated verbatim on the Section B literary instructions (p.13); cited here to 2025. Distinct from the copy-vs-manipulate rule: this penalises padding a correct answer, not failing to reshape it.',
  scale: {
    name: 'Excess material · −1 /5',
    levels: two(4, 5),
    notes: [
      'A correct reading point scores its full marks (here 5).',
      'The scheme: “Candidates may be penalised, and 1 mark will be deducted for excess and redundant material.”',
      'So burying the right answer inside extra, unasked-for material can cost a mark rather than add one.',
    ],
    cite: MS('p.11 & p.13 (excess and redundant material — 1 mark deducted)'),
  },
  scripts: [
    {
      id: 'it8-a',
      label: 'The answer',
      persona: 'Right answer, then keeps writing',
      work: [
        'Gives the correct answer to a 5-mark point.',
        'Then copies out two more sentences from the passage that weren’t asked for.',
        'The extra material is redundant to the point.',
      ],
      keyLevelId: 'm4',
      keyNote:
        'It drops to 4 of 5 — the excess-material deduction. Adding more than the question asked doesn’t insure the answer; it exposes it to a −1. Give exactly what the point requires and stop — a tight correct answer beats a padded one every time.',
      embodies: {
        behaviour: 'Pads a correct reading answer with extra, unasked-for material, triggering the excess-material −1.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it8',
    rule: 'Answer the point and stop — extra material costs a mark.',
    detail:
      'Italian reading comprehension deducts 1 mark for excess and redundant material. Copying out more of the passage than the question asked for can turn a full-mark answer into a −1 — give exactly what’s required and no more.',
    cite: MS('p.11'),
  },
};

// ─────────────── IT9 · The same answer only pays once ───────────────

const IT9: ScaleSession = {
  mode: 'scale',
  id: 'it-same-answer-once',
  subject: 'italian',
  level: 'common',
  title: 'One answer, marked once',
  cue: 'Reading comprehension',
  question:
    'Two separate reading questions can be answered from the passage, and a candidate spots one sentence that seems to satisfy both — so writes that same correct sentence for each. The scheme: where the same correct answer is given to two separate questions, full marks are awarded only once. The second question is worth 5. What does that SECOND question score?',
  questionNote:
    'Scenario authored for this exercise. The “same correct answer to two separate questions → full marks only once” rule is stated on both the Section A (p.11) and Section B (p.13) reading instructions; cited here to 2025. It means one sentence can’t be banked twice across the paper.',
  scale: {
    name: 'Recycled answer · credited once /5',
    levels: two(0, 5),
    notes: [
      'Some passages contain a line that looks like it answers two different questions.',
      'The scheme: “Where candidates provide the same correct answer to two separate questions, full marks will be awarded only once.”',
      'So the identical sentence, already credited once, earns nothing the second time.',
    ],
    cite: MS('p.11 & p.13 (same correct answer to two questions — credited only once)'),
  },
  scripts: [
    {
      id: 'it9-a',
      label: 'The answer',
      persona: 'Reuses one sentence for two questions',
      work: [
        'Question A is answered correctly with a sentence from the passage.',
        'Question B is answered with the SAME sentence — already credited under A.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The second question scores 0 — the answer was already banked once, and the scheme credits identical content only once. Each question is testing a different thing; if you find yourself writing the same line twice, one of the two questions is asking for something else. Go back and find the distinct point the second question actually wants.',
      embodies: {
        behaviour: 'Gives the identical correct sentence to two separate questions, so the repeat earns nothing under the credited-once rule.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it9',
    rule: 'Each question wants a distinct answer — the same line pays once.',
    detail:
      'In Italian reading comprehension, the same correct answer given to two separate questions is credited only once. If you’re tempted to reuse a sentence, the second question is asking for something different — find it, rather than banking on a repeat.',
    cite: MS('p.13'),
  },
};

// ─────────────── IT10 · The whole aural is answered in English ───────────────

const IT10: ScaleSession = {
  mode: 'scale',
  id: 'it-aural-english',
  subject: 'italian',
  level: 'common',
  title: 'The aural is answered in English',
  cue: 'Listening · answer language',
  question:
    'In the Listening test, every answer must be written in English — the whole test, not just one question. A candidate understands a dialogue perfectly and answers accurately, but writes the answers in Italian. The 2025 aural scheme: if a whole section is answered in Italian, mark it, then deduct 50% of the marks gained. A 16-mark section, answered correctly but in Italian — what survives?',
  questionNote:
    'Scenario authored for this exercise. The aural instructions (p.5) state “Responses must be written in English” and “If whole test / whole section answered in Italian: mark according to the Marking Scheme, then deduct 50% of marks gained.” The explicit −50% figure is pinned to the 2025 scheme (absent from 2024, per the cross-year verification). Distinct from the reading penalty (IT2): the reading requires English only on the opinion question, whereas the ENTIRE aural is answered in English.',
  scale: {
    name: 'Aural answered in Italian · −50%',
    levels: two(8, 16),
    notes: [
      'The Listening test is answered in English throughout — “Responses must be written in English.”',
      'Answering a whole section in Italian = mark as normal, then deduct 50% of the marks gained.',
      'So a fully-correct 16-mark section written in Italian keeps only 8.',
    ],
    cite: MS('p.5 (Listening — English answers required; whole section in Italian → −50%)'),
  },
  scripts: [
    {
      id: 'it10-a',
      label: 'The answer',
      persona: 'Understands it, answers in Italian',
      work: [
        'Catches every point in a 16-mark dialogue section.',
        'Writes all the answers in Italian.',
        'English was required for the whole test.',
      ],
      keyLevelId: 'm8',
      keyNote:
        'Halved to 8 of 16 — comprehension was perfect, but the aural is answered in English and a whole section in Italian loses 50%. Unlike the reading, there’s no part of the aural where Italian is wanted: write every listening answer in English, even when the Italian comes to you first.',
      embodies: {
        behaviour: 'Answers a whole aural section in Italian where English is required, triggering the −50% whole-section penalty.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it10',
    rule: 'Write every listening answer in English.',
    detail:
      'The Italian aural is answered in English from start to finish. In the 2025 scheme, a whole section answered in Italian is marked and then cut by 50%. Perfect comprehension in the wrong language keeps only half — answer the listening test in English throughout.',
    cite: MS('p.5'),
  },
};

// ─────────────── IT11 · Circle one, or lose the mark ───────────────

const IT11: ScaleSession = {
  mode: 'scale',
  id: 'it-mcq-double',
  subject: 'italian',
  level: 'common',
  title: 'Two circles, no marks',
  cue: 'Listening · multiple choice',
  question:
    'An aural multiple-choice item is worth 2 marks. Torn between (b) and (c), the candidate circles both and crosses out neither — and (c) was the correct option. The scheme: where two answers are circled and not cancelled, no marks are awarded. What does the item score?',
  questionNote:
    'Scenario authored for this exercise. The Section A multiple-choice rules (p.5) state: two answers circled and not cancelled = no marks; two circled with one cancelled = accept the non-cancelled answer; one circled and cancelled = accept it. Cited to 2025.',
  scale: {
    name: 'MCQ · two uncancelled circles = 0 /2',
    levels: two(0, 2),
    notes: [
      'Each aural multiple-choice item is worth 2 marks for the correct option.',
      'The scheme: “Where two answers are circled and not cancelled, no marks are awarded.”',
      'If you change your mind, cancel the wrong one clearly — “two circled and one cancelled, accept the non-cancelled answer.”',
    ],
    cite: MS('p.5 (Listening Section A — two answers circled and not cancelled: no marks)'),
  },
  scripts: [
    {
      id: 'it11-a',
      label: 'The answer',
      persona: 'Hedges between two options',
      work: [
        'Unsure, circles both (b) and (c).',
        'Cancels neither.',
        'Option (c) was correct.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Zero — even though the correct option is one of the two circled, leaving both standing scores nothing. Commit to one answer. If you truly change your mind, strike out the option you’re rejecting so exactly one clean choice remains; an uncancelled hedge throws the mark away.',
      embodies: {
        behaviour: 'Circles two multiple-choice options without cancelling either, so the no-marks rule applies despite one being correct.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it11',
    rule: 'Commit to one multiple-choice answer.',
    detail:
      'In the aural multiple choice, two options circled and not cancelled scores zero — even if one is right. If you change your mind, clearly cross out the option you’re rejecting so a single clean choice remains.',
    cite: MS('p.5'),
  },
};

// ─────────────── IT12 · Keep the Italian names Italian ───────────────

const IT12: ScaleSession = {
  mode: 'scale',
  id: 'it-italian-names',
  subject: 'italian',
  level: 'common',
  title: 'Keep the Italian names Italian',
  cue: 'Literature · prescribed-text essay',
  question:
    'In the prescribed-literature essay, a candidate argues well but Anglicises everything — renders the title in English and refers to the characters by translated or misspelled names throughout. The scheme: “Title and characters’ names translated into English will be penalised,” with “−1 overall for Italian title and names spelled incorrectly.” Take an essay sitting at the top of the 42–50 band. Where does the name-handling leave it?',
  questionNote:
    'Scenario authored for this exercise. The B3 prescribed-text essay instructions (p.21) state: “Title and characters’ names translated into English will be penalised” and “−1 overall for Italian title and names spelled incorrectly.” The 50 baseline is the top of the real Appendix 1 “42–50” band (p.29); the −1 is the scheme’s stated overall deduction. Cited to 2025.',
  scale: {
    name: 'Italian title & names · −1 overall',
    levels: two(49, 50),
    notes: [
      'The prescribed-text essay is graded in bands (Appendix 1); take a strong essay at the top of the 42–50 band.',
      'The scheme: translated titles and characters’ names “will be penalised,” with “−1 overall for Italian title and names spelled incorrectly.”',
      'So Anglicising or misspelling the Italian names shaves the overall mark — and the translation itself is separately penalised.',
    ],
    cite: MS('p.21 (B3 essay — translated / misspelled Italian title & names penalised) & p.29 (Appendix 1 bands)'),
  },
  scripts: [
    {
      id: 'it12-a',
      label: 'The answer',
      persona: 'Anglicises the title and names',
      work: [
        'A well-argued essay that would otherwise top the 42–50 band.',
        'Translates the novel’s title into English.',
        'Refers to the characters by translated / misspelled names throughout.',
      ],
      keyLevelId: 'm49',
      keyNote:
        'It takes the −1 overall for misspelling the Italian title and names — dropping from 50 to 49 — and the translation is separately penalised on top. Learn the title and the characters’ names exactly as they’re spelled in Italian and use them as they are. It’s free accuracy you control completely; don’t hand it back by Anglicising.',
      embodies: {
        behaviour: 'Translates and misspells the Italian title and characters’ names, triggering the −1 overall and the translation penalty.',
        cite: MS('p.21'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it12',
    rule: 'Spell the Italian title and names correctly — never translate them.',
    detail:
      'The Italian prescribed-text essay penalises titles and characters’ names translated into English, with a −1 overall for Italian titles and names spelled incorrectly. Memorise the exact Italian spellings and keep them Italian — it’s accuracy entirely within your control.',
    cite: MS('p.21'),
  },
};

// ─────────────── IT13 · Three points, well-argued, beat eight thin ones ───────────────

const IT13: ScaleSession = {
  mode: 'scale',
  id: 'it-literary-quality',
  subject: 'italian',
  level: 'common',
  title: 'Three deep points beat eight thin ones',
  cue: 'Literature · prescribed-text essay',
  question:
    'For the 60-mark prescribed-text essay, a candidate crams in eight points, each barely mentioned, with no quotation and a couple of plot errors — betting that volume wins marks. The scheme: “Quality and NOT quantity is important. Three relevant points, well-argued and supported from the text, are sufficient,” and “Factual errors will be penalised.” Where does a broad-but-shallow, error-dotted essay land?',
  questionNote:
    'Scenario authored for this exercise. The B3 essay instructions (p.21) state: “Reference to the text is important … Quality and NOT quantity is important. Three relevant points, well-argued and supported from the text, are sufficient … Factual errors will be penalised.” Band marks are from the real Appendix 1 grid (p.29): the 24–32 band is “some knowledge … little reference to the text … a lot of irrelevant material”; the 51–60 band is a full, text-supported answer. Cited to 2025.',
  scale: {
    name: 'Prescribed-text essay · Appendix 1 bands /60',
    levels: [
      { id: 'lit-shallow', label: 'Eight thin points, errors, no quotes', annotation: '28', marks: 28 },
      { id: 'lit-solid', label: 'Points covered, some textual support', annotation: '45', marks: 45 },
      { id: 'lit-developed', label: 'Three developed, accurate, text-anchored points', annotation: '55', marks: 55 },
    ],
    notes: [
      'The essay is graded on knowledge of the text, textual support and relevance (Appendix 1).',
      'The scheme: three relevant points, well-argued and supported from the text, are SUFFICIENT — quality over quantity.',
      'Factual errors are penalised, and unsupported, irrelevant material drags the band down.',
      'So eight barely-mentioned, error-dotted points sit far below three developed, accurate, quoted ones.',
    ],
    cite: MS('p.21 (B3 essay — quality not quantity; three points sufficient; factual errors penalised) & p.29 (Appendix 1 bands)'),
  },
  scripts: [
    {
      id: 'it13-a',
      label: 'The answer',
      persona: 'Breadth without depth',
      work: [
        'Lists eight points, each a single undeveloped sentence.',
        'No quotations or specific references to the text.',
        'Contains a couple of factual/plot errors.',
      ],
      keyLevelId: 'lit-shallow',
      keyNote:
        'It lands low — around the 24–32 band — despite covering the most ground. The essay rewards depth and accuracy, not a headcount of points: three points, each well-argued and anchored in the text, are explicitly enough for the top, while factual errors actively cost marks. Pick your three strongest points, develop each with a quotation, and get the facts right.',
      embodies: {
        behaviour: 'Trades depth for a long list of thin, unsupported, error-dotted points, landing in a low Appendix 1 band.',
        cite: MS('p.21'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it13',
    rule: 'Three developed, text-supported points — not a long list.',
    detail:
      'The Italian prescribed-text essay says three relevant points, well-argued and supported from the text, are sufficient, and it penalises factual errors. Depth and accuracy score; breadth without support doesn’t. Choose three strong points, quote the text for each, and get the facts right.',
    cite: MS('p.21'),
  },
};

// ─────────────── IT14 · A point earns on how well you develop it ───────────────

const IT14: ScaleSession = {
  mode: 'scale',
  id: 'it-point-tiers',
  subject: 'italian',
  level: 'common',
  title: 'A bare point is only a poor point',
  cue: 'Written production · per-point credit',
  question:
    'On the composition, each content point is worth up to 4 marks, scored 0-1-2-3-4. A candidate makes the required point — but in one bare sentence, no example, no expansion. The scheme’s per-point grid reads: 1m a poor point, 2m a sufficient point, 3m a good point, 4m a very good / excellent point. Where does a correct-but-undeveloped point land?',
  questionNote:
    'Scenario authored for this exercise. The per-point credit grid (p.28) scores 4-mark points as (0,1,2,3,4) with named quality tiers: “1m poor point · 2m sufficient point · 3m good point · 4m very good point / excellent point.” The formal-writing instructions add that “each point should be expanded and developed” (p.27). Cited to 2025.',
  scale: {
    name: 'Point out of 4 · quality tiers',
    levels: [
      { id: 'pt-none', label: 'No merit', annotation: '0', marks: 0 },
      { id: 'pt-poor', label: 'Poor point (bare / undeveloped)', annotation: '1', marks: 1 },
      { id: 'pt-suff', label: 'Sufficient point', annotation: '2', marks: 2 },
      { id: 'pt-good', label: 'Good point', annotation: '3', marks: 3 },
      { id: 'pt-exc', label: 'Very good / excellent point', annotation: '4', marks: 4 },
    ],
    notes: [
      'Content points aren’t all-or-nothing: a 4-mark point is scored 0,1,2,3,4 on quality.',
      'The grid: 1m poor point · 2m sufficient · 3m good · 4m very good / excellent.',
      'A correct point stated bare, without expansion, is only a “poor point” — 1 of 4.',
      'Each point should be expanded and developed to climb the tiers.',
    ],
    cite: MS('p.28 (per-point credit grid — poor / sufficient / good / excellent) & p.27 (each point expanded and developed)'),
  },
  scripts: [
    {
      id: 'it14-a',
      label: 'The answer',
      persona: 'Makes the point, leaves it bare',
      work: [
        'States the required point correctly.',
        'One short sentence — no example, no reason, no development.',
      ],
      keyLevelId: 'pt-poor',
      keyNote:
        'It scores 1 of 4 — a “poor point.” Being correct only gets you onto the ladder; the marks are in the development. The same point, expanded with a reason and an example, climbs to 3 or 4. Don’t just make each point — build it out.',
      embodies: {
        behaviour: 'Makes a correct point but leaves it undeveloped, scoring only the “poor point” tier on the per-point grid.',
        cite: MS('p.28'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it14',
    rule: 'Being right is 1 mark — developing the point is the other three.',
    detail:
      'Italian scores content points on quality, not just presence: a 4-mark point runs 1 (poor) to 4 (excellent), and a bare correct sentence is only a poor point. Expand each point with a reason and an example to climb from 1 toward 4.',
    cite: MS('p.28'),
  },
};

// ─────────────── IT15 · Verbs gate the Language band ───────────────

const IT15: ScaleSession = {
  mode: 'scale',
  id: 'it-verb-gate',
  subject: 'italian',
  level: 'common',
  title: 'Wrong verbs lock the top band',
  cue: 'Written production · Language mark',
  question:
    'A composition’s Language mark is out of 10. The candidate reaches for ambitious vocabulary and idiom — but conjugates several verbs wrong. The Language descriptors put “good grammatical accuracy” in the top band (7–10) and “some incorrect verbs and agreements” in the middle band (4–6). Where does rich-vocabulary-but-wrong-verbs land?',
  questionNote:
    'Scenario authored for this exercise. The Appendix 2 Language descriptors (p.32) band on verb accuracy: 7–10 “Idiomatic Italian, good vocabulary, good grammatical accuracy and few spelling mistakes”; 4–6 “Adequate vocabulary, some incorrect verbs and agreements”; 0–3 “most verbs incorrect.” Verbs are the named Language failure point. Cited to 2025.',
  scale: {
    name: 'Language descriptor bands /10',
    levels: [
      { id: 'lg-low', label: 'Most verbs incorrect', annotation: '3', marks: 3 },
      { id: 'lg-mid', label: 'Some incorrect verbs & agreements', annotation: '5', marks: 5 },
      { id: 'lg-high', label: 'Good grammatical accuracy', annotation: '9', marks: 9 },
    ],
    notes: [
      'The Language mark bands on grammatical accuracy, and verbs are the named failure point.',
      'Top band (7–10) requires “good grammatical accuracy”; middle band (4–6) is “some incorrect verbs and agreements.”',
      'So wrong verbs lock you out of the top band, however rich the vocabulary.',
    ],
    cite: MS('p.32 (Appendix 2 Language descriptors — verb accuracy bands)'),
  },
  scripts: [
    {
      id: 'it15-a',
      label: 'The answer',
      persona: 'Ambitious vocab, broken verbs',
      work: [
        'Reaches for rich vocabulary and idiomatic expressions.',
        'Conjugates several verbs incorrectly.',
      ],
      keyLevelId: 'lg-mid',
      keyNote:
        'It best-fits the middle band — 4–6 — because the top band requires good grammatical accuracy, and wrong verbs shut that door however impressive the vocabulary. Verbs are the language gate in Italian (and in French and Spanish). Reach for structures you can conjugate correctly; accuracy on the verbs you use beats ambition you can’t control.',
      embodies: {
        behaviour: 'Pairs ambitious vocabulary with incorrect verbs, so the Language mark is capped at the middle band by the accuracy requirement.',
        cite: MS('p.32'),
      },
    },
  ],
  takeaway: {
    id: 'codex-it15',
    rule: 'Verbs are the language gate — accuracy beats ambition.',
    detail:
      'The Italian Language mark bands on grammatical accuracy: the top band (7–10) needs good accuracy, while incorrect verbs pin you to the middle band (4–6), however rich the vocabulary. Choose structures you can conjugate correctly — getting your verbs right unlocks the top band.',
    cite: MS('p.32'),
  },
};

export const ITALIAN_CHAIR: ChairSubject = {
  id: 'italian',
  label: 'Italian',
  tagline: 'Two axes and the graduated cap, the wrong-language penalties, copy-vs-manipulate, excess-material and same-answer-once, no rote off the point, the list and multiple-choice hedging traps, verb-gated language, the letter’s free format marks, the literature essay’s rules — and an oral that marks talking, not reciting.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [IT1, IT2, IT3, IT4, IT5, IT6, IT7, IT8, IT9, IT10, IT11, IT12, IT13, IT14, IT15],
  sources: [
    { label: 'SEC LC Italian HL marking scheme 2025 (examiner-reports/italian/2025-marking-scheme)' },
    { label: 'SEC/NCCA Leaving Certificate Italian syllabus (examiner-reports/italian/italian-syllabus)' },
  ],
  coverageNote:
    'The written-paper sessions teach the conventions of the 2025 marking scheme — the two Content/Language axes with the graduated content cap, the wrong-language penalties (reading opinion question and whole-aural), the reading copy-vs-manipulate deduction, the excess/redundant-material −1, the same-answer-only-once rule, the rote-off-the-point rule, the per-point quality tiers, the verb-gated Language bands, the listening list rule and the multiple-choice two-circle rule, the separate 10-mark letter Format block, and the prescribed-literature essay’s rules (three points sufficient; keep Italian titles and names Italian) — which apply at both Higher and Ordinary level. The oral session is grounded in a different source: the official SEC/NCCA Italian syllabus (Speaking 25% Higher / 20% Ordinary; assessed on transfer of meaning + accuracy). SEC publishes NO per-band oral marking grid, so any band marks shown in the oral session are labelled illustrative. The explicit −50% wrong-language figure is pinned to the 2025 scheme (absent from 2024, per the cross-year verification). Verified against the 2025 HL scheme (copy-vs-manipulate and the content cap also corroborated against 2024) and the syllabus; level-specific worked examples are being added.',
};
