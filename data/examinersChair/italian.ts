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

export const ITALIAN_CHAIR: ChairSubject = {
  id: 'italian',
  label: 'Italian',
  tagline: 'Two axes, the wrong-language penalty, copy-vs-manipulate, no rote off the point, the list-hedging trap, the letter’s free format marks — and an oral that marks talking, not reciting.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [IT1, IT2, IT3, IT4, IT5, IT6, IT7],
  sources: [
    { label: 'SEC LC Italian HL marking scheme 2025 (examiner-reports/italian/2025-marking-scheme)' },
    { label: 'SEC/NCCA Leaving Certificate Italian syllabus (examiner-reports/italian/italian-syllabus)' },
  ],
  coverageNote:
    'The written-paper sessions teach the conventions of the 2025 marking scheme — the two Content/Language axes with the graduated content cap, the wrong-language penalty, the reading-comprehension copy-vs-manipulate deduction, the rote-off-the-point rule, the listening list rule (one wrong item nullifies a correct one) and the separate 10-mark letter Format block — which apply at both Higher and Ordinary level. The oral session is grounded in a different source: the official SEC/NCCA Italian syllabus (Speaking 25% Higher / 20% Ordinary; assessed on transfer of meaning + accuracy). SEC publishes NO per-band oral marking grid, so any band marks shown in the oral session are labelled illustrative. Verified against the 2025 HL scheme (copy-vs-manipulate also corroborated against 2024) and the syllabus; level-specific worked examples are being added.',
};
