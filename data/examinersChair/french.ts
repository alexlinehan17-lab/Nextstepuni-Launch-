/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — French (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the two independent Communication/Language axes for written
 * production, the lift-vs-manipulation rule, the hedging-scores-zero rule and
 * the wrong-language penalties) is the real SEC system, cited to:
 *  - SEC LC French HL marking scheme 2025 —
 *    examiner-reports/french/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC French HL marking scheme 2025, ${p}` });

// The oral is a different document from the written marking scheme: SEC does not
// publish per-band oral cut-points, but the LC French syllabus (SEC/NCCA) sets out
// the oral's assessment criteria, weighting and format. Cite it under its own label
// so it is never confused with the written scheme above.
//   examiner-reports/french/lc-french-syllabus.*
const ORAL = (p: string) => ({ label: `SEC LC French syllabus — oral assessment, ${p}` });

const commBands: ScaleLevel[] = [
  { id: 'bottom', label: 'Bottom band', annotation: 'B', marks: 6 },
  { id: 'middle', label: 'Middle band', annotation: 'M', marks: 13 },
  { id: 'top', label: 'Top band', annotation: 'T', marks: 18 },
];

const twoOutcome = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── Fr1 · Two axes (perfect French, off topic) ───────────────

const FR1: ScaleSession = {
  mode: 'scale',
  id: 'fr-two-axes',
  subject: 'french',
  level: 'common',
  title: 'Perfect French, wrong answer',
  cue: 'Written production',
  question: 'A written-production answer (Communication out of 20) is in flawless, elegant French — but it mostly copies phrases straight from the stimulus and never really addresses the task. Where does its COMMUNICATION mark land?',
  questionNote:
    'Scenario authored for this exercise. Written production is marked on two independent, equally weighted axes — Communication and Language — that are summed; this session is about the Communication axis (out of 20 for a 40-mark question).',
  scale: {
    name: 'Communication · /20 · bands',
    levels: commBands,
    notes: [
      'Every written answer is scored on two independent axes: Communication and Language, equally weighted, then summed.',
      'Language accuracy does NOT lift Communication — they are marked separately.',
      '“Mere transcription or very poor treatment of the stimulus material” is the Bottom-band Communication descriptor.',
      'So copied-but-flawless French sits in the Bottom Communication band, however good the grammar.',
    ],
    cite: MS('p.[15]–[16] (Communication/Language bands)'),
  },
  scripts: [
    {
      id: 'fr1-a',
      label: 'The answer',
      persona: 'Beautiful French, lifted content',
      work: [
        'Elegant, accurate French throughout — no grammar errors.',
        'But it recycles phrases from the stimulus and barely treats the task.',
      ],
      keyLevelId: 'bottom',
      keyNote:
        'Bottom band for Communication — “mere transcription” is the explicit descriptor. The Language axis might score well, but Communication is judged on whether the candidate actually addresses the task in their own words. Two axes: you have to earn both. Grammar can’t buy Communication marks.',
      embodies: {
        behaviour: 'Transcribes the stimulus in accurate French — the Bottom-band Communication descriptor.',
        cite: MS('p.[16]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr1',
    rule: 'Communication and Language are marked separately.',
    detail:
      'In French written production, accuracy and content are two independent axes summed together. Flawless French that copies the prompt or dodges the task scores at the bottom for Communication — address the task in your own words to earn that half.',
    cite: MS('p.[15]'),
  },
};

// ─────────────── Fr2 · Manipulation required ───────────────

const FR2: ScaleSession = {
  mode: 'scale',
  id: 'fr-manipulation',
  subject: 'french',
  level: 'common',
  title: 'Lift it, and lose a mark',
  cue: 'Comprehension',
  question: 'A comprehension question is tagged “correct manipulation required”. The answer in the text is «il a parlé à sa mère». The candidate copies it out unchanged. The full answer needed the verb changed to the first person. What does the raw lift score (out of 5)?',
  questionNote:
    'Scenario authored for this exercise. In reading comprehension the scheme tags each question either “direct quotation OR manipulation acceptable” or “correct manipulation required”; where manipulation is required, an uncorrected lift is docked on the 5/4/3/2/1/0 ladder.',
  scale: {
    name: 'Comprehension · /5',
    levels: [
      { id: 'm0', label: '0', annotation: '0', marks: 0 },
      { id: 'm4', label: '4 (lift, not manipulated)', annotation: '4', marks: 4 },
      { id: 'm5', label: '5 (correctly manipulated)', annotation: '5', marks: 5 },
    ],
    notes: [
      'This question is tagged “correct manipulation required”.',
      'Copying «il a parlé» unchanged is a raw lift — the scheme docks it one mark.',
      'Changing it to the first person («j’ai parlé…») is the manipulation that earns full marks.',
      'A single stray word with no manipulation would score 0.',
    ],
    cite: MS('p.[13] (lift vs manipulation ladder, Q.5(a))'),
  },
  scripts: [
    {
      id: 'fr2-a',
      label: 'The answer',
      persona: 'Copies the sentence out',
      work: ['«il a parlé à sa mère»  (copied straight from the text)'],
      keyLevelId: 'm4',
      keyNote:
        'The lift is on-target, so it scores 4 — but the question required manipulation to the first person, and leaving «il a» uncorrected drops the fifth mark. On “manipulation required” questions, copying is never full marks; transform the person/tense the answer needs.',
      embodies: {
        behaviour: 'Lifts the text verbatim where the question requires manipulation — docked on the ladder.',
        cite: MS('p.[13]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr2',
    rule: 'When manipulation is required, copying costs a mark.',
    detail:
      'French comprehension flags some questions “manipulation required” — you must transform the verb/pronoun (e.g. third to first person), not just lift the sentence. A raw quote there is capped below full marks.',
    cite: MS('p.[13]'),
  },
};

// ─────────────── Fr3 · Don't hedge ───────────────

const FR3: ScaleSession = {
  mode: 'scale',
  id: 'fr-hedge',
  subject: 'french',
  level: 'common',
  title: 'Two answers, zero marks',
  cue: 'Comprehension',
  question: 'A comprehension question has one correct answer. Unsure, the candidate writes two possible answers, hoping one is right. One of them IS correct. What does the question score?',
  questionNote:
    'Scenario authored for this exercise. The scheme states plainly for comprehension: if more than one answer is offered, the question scores 0.',
  scale: {
    name: 'Comprehension · one answer only',
    levels: twoOutcome(0, 5),
    notes: [
      'Comprehension rule: “If more than one answer offered = 0 Marks.”',
      'It does not matter that one of the two is correct — offering two voids the question.',
      'The examiner will not choose the right one for you.',
    ],
    cite: MS('p.[6], p.[12] (more than one answer = 0)'),
  },
  scripts: [
    {
      id: 'fr3-a',
      label: 'The answer',
      persona: 'Hedges the bet',
      work: ['Answer 1 (correct) … / … Answer 2 (wrong)', 'Both offered, hoping one lands.'],
      keyLevelId: 'm0',
      keyNote:
        '0 marks — even though one answer was right. Offering two answers voids the question outright; the examiner will not pick the correct one for you. Commit to a single answer. A confident wrong answer at least can’t cost you a right one this way.',
      embodies: {
        behaviour: 'Offers more than one answer to a single-answer question, which the scheme scores 0.',
        cite: MS('p.[6]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr3',
    rule: 'One question, one answer.',
    detail:
      'In French comprehension, offering two answers scores 0 — even if one is correct. Decide, commit, and write a single answer. Hedging guarantees the loss it was meant to avoid.',
    cite: MS('p.[6]'),
  },
};

// ─────────────── Fr4 · The aural rewards the information ───────────────

const FR4: ScaleSession = {
  mode: 'scale',
  id: 'fr-aural',
  subject: 'french',
  level: 'common',
  title: 'The aural: get the fact down',
  cue: 'Aural',
  question: 'In the listening test, the scheme is lenient on phrasing: “accept any formulation which communicates the information sought”, with no penalty for excess and points need not be on separate lines. A candidate hears the answer but, unsure how to word it neatly, leaves it blank. What does that cost — and how should the aural be approached?',
  questionNote:
    'Scenario authored for this exercise. The listening test is marked on the information communicated, not the neatness of the phrasing — but a whole section answered in French (where English is required) is halved.',
  scale: {
    name: 'Aural · information communicated',
    levels: [
      { id: 'm0', label: '0 (left blank)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (rough but clear)', annotation: '3', marks: 3 },
    ],
    notes: [
      'The aural accepts “any formulation which communicates the information sought”.',
      'No excess penalty, and points need not be on separate lines — the fact is what scores.',
      'Answer in the required language (usually English); a whole section in French is halved.',
    ],
    cite: MS('p.[17] (aural: any formulation; 50% wrong-language penalty)'),
  },
  scripts: [
    {
      id: 'fr4-a',
      label: 'The answer',
      persona: 'Heard it, left it blank',
      work: ['Heard and understood the answer.', 'Left it blank, unsure how to phrase it neatly.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — for information the candidate actually had. The aural rewards the fact communicated, not tidy phrasing: a rough note that gets the information across scores. Never leave an aural answer blank because you can’t word it perfectly — jot down what you heard, in the required language (usually English).',
      embodies: {
        behaviour: 'Leaves an aural answer blank over phrasing, where any clear formulation would score.',
        cite: MS('p.[17]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr4',
    rule: 'In the aural, the fact scores — not the phrasing.',
    detail:
      'The listening test accepts any formulation that communicates the information, with no excess penalty. Write down what you heard, however roughly, in the required language — never leave it blank over wording. (A whole section in French is halved.)',
    cite: MS('p.[17]'),
  },
};

// ─────────────── Fr5 · The oral rewards conversation, not recitation ───────────────

const FR5: ScaleSession = {
  mode: 'scale',
  id: 'fr-oral',
  subject: 'french',
  level: 'common',
  title: 'The oral: converse, don’t recite',
  cue: 'Oral',
  question:
    'The oral is worth 25% of French at Higher Level. A candidate has memorised a fluent, grammatically flawless two-minute speech about their summer job — and delivers it almost word-for-word no matter what the examiner actually asks. The French is perfect. Where does the performance land?',
  questionNote:
    'Scenario authored for this exercise. The oral is assessed as a “general conversation, based on the syllabus content”, on two criteria: (i) ability to transfer meaning and (ii) accuracy and appropriateness of language, including vocabulary and structures. SEC does not publish per-band cut-points, so the mark bands below are illustrative positions on the 100-mark oral — the marking grammar (two criteria + genuine conversation) is the cited syllabus system, not the exact numbers.',
  scale: {
    name: 'Oral · communicative bands (/100, illustrative)',
    levels: [
      { id: 'recite', label: 'Recited, off-question', annotation: 'B', marks: 40 },
      { id: 'partial', label: 'Partly responds', annotation: 'M', marks: 65 },
      { id: 'converse', label: 'Genuine conversation', annotation: 'T', marks: 85 },
    ],
    notes: [
      'The oral is “general conversation, based on the syllabus content” — a conversation, not a recital.',
      'It is assessed on “(i) ability to transfer meaning and (ii) degrees of accuracy and appropriateness of language, including the range of vocabulary and structures used”.',
      'Speaking is 25% of the exam at Higher Level (20% at Ordinary); fifteen minutes per candidate.',
      'A memorised speech that ignores the examiner’s actual question transfers little meaning — it forfeits the first criterion however accurate its French, keeping only some of the second.',
      'SEC does not publish oral band cut-points; these marks illustrate the criterion, they are not official sub-marks.',
    ],
    cite: ORAL('p.[25]–[26] (oral assessment: general conversation; criteria (i)/(ii); 25% weighting)'),
  },
  scripts: [
    {
      id: 'fr5-a',
      label: 'The performance',
      persona: 'Perfect French, deaf to the question',
      work: [
        'Fluent, error-free delivery — clearly well rehearsed.',
        'Recites the prepared “summer job” speech whatever the examiner asks.',
        'Never actually answers the question put, so no real information is exchanged.',
      ],
      keyLevelId: 'recite',
      keyNote:
        'Bottom band — because the oral marks “ability to transfer meaning” first, and a speech that ignores the question transfers almost none. The accuracy criterion (vocabulary and structures) keeps it off the floor, but flawless French cannot rescue a monologue that isn’t a conversation. Listen to the actual question and answer it in your own words; a rougher answer that genuinely responds outscores a perfect one that doesn’t.',
      embodies: {
        behaviour:
          'Recites a memorised, off-question speech in a component defined as “general conversation” — high on accuracy, low on the transfer-of-meaning criterion.',
        cite: ORAL('p.[25]–[26]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr5',
    rule: 'The oral is a conversation — transfer meaning, don’t recite.',
    detail:
      'The French oral (25% at Higher Level) is marked on two criteria: ability to transfer meaning, and accuracy/appropriateness of vocabulary and structures. A memorised speech delivered regardless of the question is accurate but transfers little — it loses the primary criterion. Answer what is actually asked, in your own words.',
    cite: ORAL('p.[25] (assessment criteria & 25% weighting)'),
  },
};

// ─────────────── Fr6 · The Language axis is a verb gate ───────────────

const langBands: ScaleLevel[] = [
  { id: 'bottom', label: 'Bottom band', annotation: 'B', marks: 6 },
  { id: 'middle', label: 'Middle band', annotation: 'M', marks: 10 },
  { id: 'top', label: 'Top band', annotation: 'T', marks: 17 },
];

const FR6: ScaleSession = {
  mode: 'scale',
  id: 'fr-language-axis',
  subject: 'french',
  level: 'common',
  title: 'Great ideas, broken verbs',
  cue: 'Written production',
  question:
    'A written-production answer (Language out of 20) argues its point clearly and a French reader follows it easily — but most of the verbs are wrong and agreement keeps breaking down. Where does its LANGUAGE mark land?',
  questionNote:
    'Scenario authored for this exercise. This is the mirror of the two-axes session: written production is scored on two independent axes — Communication and Language — summed. Fr1 held Language fixed and moved Communication; here the content communicates well but the LANGUAGE axis is judged on verbs, agreement and spelling.',
  scale: {
    name: 'Language · /20 · bands',
    levels: langBands,
    notes: [
      'Communication and Language are two independent axes, equally weighted, then summed.',
      'The Language axis is judged on verbs, agreement and spelling — not on ideas.',
      'Bottom Language band descriptor: “Problems with vocabulary / Most verbs incorrect / Basic rule of agreement not respected / Many mistakes in spelling.”',
      'Middle band needs verbs “generally correct” and agreement “generally respected”; Top band is idiomatic French with “few mistakes in verbs, agreement or spelling”.',
      'So a well-argued answer whose verbs are mostly wrong sits in the Bottom Language band, however good the content — that content earns the Communication half, not this one.',
    ],
    cite: MS('p.[16] (Language grid: verbs / agreement / spelling)'),
  },
  scripts: [
    {
      id: 'fr6-a',
      label: 'The answer',
      persona: 'Clear argument, wrong verbs',
      work: [
        'Ideas land — a French reader follows the argument without trouble.',
        'But most verb forms are wrong and adjective/past-participle agreement keeps failing.',
      ],
      keyLevelId: 'bottom',
      keyNote:
        'Bottom band for Language — “most verbs incorrect” and “basic rule of agreement not respected” are the explicit bottom-band descriptors. The strong content scores on the Communication axis, but it cannot lift Language: the two axes are marked and summed separately. Get the verbs and agreements right to earn this half — it is a mechanical gate, not an ideas contest.',
      embodies: {
        behaviour:
          'Communicates the argument but with most verbs incorrect and agreement broken — the bottom-band Language descriptors.',
        cite: MS('p.[16]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr6',
    rule: 'The Language axis is a verb-and-agreement gate.',
    detail:
      'In French written production, Language is scored separately from content — on verbs, agreement and spelling. A clear, well-argued answer whose verbs are mostly wrong lands in the bottom Language band; strong ideas earn the Communication half, not this one. Drill verb forms and agreement to unlock the other twenty marks.',
    cite: MS('p.[16]'),
  },
};

// ─────────────── Fr7 · Excess material is docked ───────────────

const FR7: ScaleSession = {
  mode: 'scale',
  id: 'fr-excess',
  subject: 'french',
  level: 'common',
  title: 'Right word, extra baggage',
  cue: 'Comprehension',
  question:
    'A reading-comprehension question asks for the single word meaning « troubler ». The answer is «  Déranger  » (5 marks). The candidate writes «  Déranger quelqu’un  » — the correct word plus one extra word that wasn’t asked for. What does it score (out of 5)?',
  questionNote:
    'Scenario authored for this exercise. In the Reading Comprehensions the scheme docks excess material: “Excess material: -1 or -2 Marks”, and single-word/precise answers carry the note “Minus 1 Mark for each extraneous element”. (This is the opposite of the aural, which has no excess penalty.)',
  scale: {
    name: 'Comprehension · /5 · excess docked',
    levels: [
      { id: 'm3', label: '3 (buried in a full clause, −2)', annotation: '3', marks: 3 },
      { id: 'm4', label: '4 (one extraneous word, −1)', annotation: '4', marks: 4 },
      { id: 'm5', label: '5 (clean, exact answer)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Reading Comprehension penalty: “Excess material: -1 or -2 Marks.”',
      'On precise/single-word answers the note is explicit: “Minus 1 Mark for each extraneous element.”',
      '«  Déranger  » alone is the full-mark answer; «  Déranger quelqu’un  » adds one extraneous element — docked one mark to 4.',
      'Burying the word inside a whole lifted clause drops it further, to 3.',
      'Unlike the aural (“no penalty for excess”), the written comprehension penalises padding — quote only what is asked.',
    ],
    cite: MS('p.[11] (single-word answer; “Minus 1 Mark for each extraneous element”), p.[4] (excess penalty)'),
  },
  scripts: [
    {
      id: 'fr7-a',
      label: 'The answer',
      persona: 'Right word, one word too many',
      work: ['«  Déranger quelqu’un  »', 'The exact answer was «  Déranger  » — the extra word wasn’t asked for.'],
      keyLevelId: 'm4',
      keyNote:
        '4 marks — the correct word is there, but the extra «  quelqu’un  » is one extraneous element, and the scheme docks a mark for each. Excess never adds credit and can only cost you: when a question wants one word or one precise expression, give exactly that and stop. (The aural is the exception — there, excess is free.)',
      embodies: {
        behaviour:
          'Adds an extraneous element to an otherwise correct single-word answer, triggering the “minus 1 per extraneous element” deduction.',
        cite: MS('p.[11]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr7',
    rule: 'In the written comprehension, quote only what is asked.',
    detail:
      'French reading comprehension docks excess material (−1 or −2), and precise answers lose a mark for each extraneous element. The right word smuggled in with extra baggage scores below full marks; padding can only cost you. Isolate the exact word or expression and stop. (The aural is the one place excess is free.)',
    cite: MS('p.[4]'),
  },
};

// ─────────────── Fr8 · Wrong language in the reading comprehension ───────────────

const FR8: ScaleSession = {
  mode: 'scale',
  id: 'fr-wrong-language-read',
  subject: 'french',
  level: 'common',
  title: 'Right answer, wrong language',
  cue: 'Comprehension',
  question:
    'A Compréhension Écrite question must be answered in French. The candidate locates exactly the right information in the text — but writes the answer out in English. What does it score (out of 5)?',
  questionNote:
    'Scenario authored for this exercise. The reading-comprehension penalty list names “Answers given in the wrong language” — answers in Irish/English where French is required — and caps “all other errors” at a maximum of minus 1 Mark per question/segment. (Contrast the aural, where a whole section in the wrong language is halved, not docked a mark.)',
  scale: {
    name: 'Comprehension · /5 · wrong-language dock',
    levels: [
      { id: 'm0', label: '0 (wrong information)', annotation: '0', marks: 0 },
      { id: 'm4', label: '4 (right info, wrong language)', annotation: '4', marks: 4 },
      { id: 'm5', label: '5 (right info, in French)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Reading-comprehension penalty list: “Answers given in the wrong language … answers in Irish/English when French required as in Compréhension Écrite.”',
      'It sits under “all other errors … a maximum of minus 1 Mark per question/segment” — so a fully-correct answer in English is docked one mark to 4, not zeroed.',
      'The information still has to be right; wrong content scores 0 whatever the language.',
      'This is the written paper. In the aural, a whole section in the wrong language is instead halved (−50% of marks gained) — a different, harsher mechanism.',
    ],
    cite: MS('p.[4] (wrong-language penalty, −1 per segment)'),
  },
  scripts: [
    {
      id: 'fr8-a',
      label: 'The answer',
      persona: 'Found it, wrote it in English',
      work: [
        'Pinpoints exactly the right phrase in the French text.',
        'Writes the answer out in English rather than in French.',
      ],
      keyLevelId: 'm4',
      keyNote:
        '4 marks — the information is dead right, but the Compréhension Écrite must be answered in French, and answering in the wrong language is a −1 error. It only costs one mark here (the reading penalty caps at −1 per segment), but it is a mark you never needed to lose: answer the French comprehension in French. Note the aural plays by different rules — there a whole section in the wrong language is halved.',
      embodies: {
        behaviour: 'Answers a French-required comprehension question in English — the named wrong-language error, docked one mark.',
        cite: MS('p.[4]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr8',
    rule: 'Answer the French comprehension in French.',
    detail:
      'The reading comprehension docks a mark for answers given in the wrong language (English/Irish where French is required) — the right information in English scores 4, not 5. It is only −1, but a needless one. (The aural is stricter still: a whole section in the wrong language loses 50%.)',
    cite: MS('p.[4]'),
  },
};

// ─────────────── Fr9 · The opinion question flips to English ───────────────

const FR9: ScaleSession = {
  mode: 'scale',
  id: 'fr-opinion-english',
  subject: 'french',
  level: 'common',
  title: 'The one answer you write in English',
  cue: 'Comprehension',
  question:
    'The last part of each reading comprehension (Q.6, 5+5 marks) is an opinion question — posed in English, asking the candidate to agree/disagree and “refer to the text in support”. Wanting to show off, the candidate answers it in elegant French. What happens to one 5-mark segment?',
  questionNote:
    'Scenario authored for this exercise. Q.6 in each Compréhension Écrite is set in English and expects an English answer supported by reference to the text; the penalty list explicitly names “q.6 segments answered in French” as a wrong-language error, capped at −1 per segment.',
  scale: {
    name: 'Comprehension · Q.6 · /5 per segment',
    levels: [
      { id: 'm0', label: '0 (no valid point / no text support)', annotation: '0', marks: 0 },
      { id: 'm4', label: '4 (valid point, but in French)', annotation: '4', marks: 4 },
      { id: 'm5', label: '5 (valid point, in English)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Q.6 is the exception inside a French comprehension: the question is posed in English and answered in English.',
      'The penalty list names “q.6 segments answered in French” as a wrong-language error — the same −1 cap per segment.',
      'The task is “Refer to the text in support of your answer” (two points, ~50 words) — an opinion grounded in the text, not a free essay.',
      'So a valid, text-supported point written in French is docked to 4; the same point in English scores the full 5.',
    ],
    cite: MS('p.[9], p.[14] (Q.6 posed in English; “refer to the text”), p.[4] (q.6 in French penalised)'),
  },
  scripts: [
    {
      id: 'fr9-a',
      label: 'The answer',
      persona: 'Shows off in French on the English question',
      work: [
        'Makes a genuine, text-supported point agreeing with the statement.',
        'Writes it in fluent French — but Q.6 is answered in English.',
      ],
      keyLevelId: 'm4',
      keyNote:
        '4, not 5 — the point is valid and grounded in the text, but Q.6 is the one place in the French comprehension you write in English, and a French segment is a named wrong-language error. The rest of the paper rewards French; this question inverts that. Read the rubric: an English question with “refer to the text” wants an English answer.',
      embodies: {
        behaviour: 'Answers the English-medium Q.6 opinion question in French — the specifically named “q.6 segments answered in French” error.',
        cite: MS('p.[4]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr9',
    rule: 'The opinion question is answered in English.',
    detail:
      'Q.6 of each French reading comprehension is set in English and answered in English, supported by reference to the text — the one place the paper flips language. A point written in French there is docked to 4. Match the language the rubric is written in.',
    cite: MS('p.[9]'),
  },
};

// ─────────────── Fr10 · The aural fact must be exactly right ───────────────

const FR10: ScaleSession = {
  mode: 'scale',
  id: 'fr-aural-accuracy',
  subject: 'french',
  level: 'common',
  title: 'The aural: the number has to be exact',
  cue: 'Aural',
  question:
    'In the listening test a speaker says she works “three and a half hours” each morning. The candidate clearly understood the shape of the answer and writes “two and a half hours”. The phrasing is fine — only the number is wrong. What does the 3-mark item score?',
  questionNote:
    'Scenario authored for this exercise. The aural is lenient on wording but not on the datum: the scheme prints “Incorrect amount of time = 0 Marks” and “Incorrect amount of money = 0 Marks”, and “Wrong person = -1 Mark” — key facts must be exact.',
  scale: {
    name: 'Aural · /3 · detail accuracy',
    levels: [
      { id: 'm0', label: '0 (wrong amount)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (exact detail)', annotation: '3', marks: 3 },
    ],
    notes: [
      'The aural accepts any formulation that communicates the information — but the information itself must be correct.',
      'On quantities the scheme is absolute: “Incorrect amount of time = 0 Marks”; “Incorrect amount of money = 0 Marks.”',
      'Identity errors are docked but not fatal: “Wrong person = -1 Mark”; a wrong source is capped low (e.g. “paid for by ‘incorrect source’ = 1 Mark”).',
      'So a wrong number zeroes an item you otherwise understood — there is no partial credit for a near-miss figure.',
    ],
    cite: MS('p.[18] (Incorrect amount of time = 0), p.[22] (Incorrect amount of money = 0), p.[24] (Wrong person = -1)'),
  },
  scripts: [
    {
      id: 'fr10-a',
      label: 'The answer',
      persona: 'Right structure, wrong number',
      work: ['“She works two and a half hours in the morning.”', 'The recording said three and a half hours.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — even though the sentence is well-formed and clearly on the right track. On amounts of time and money the scheme is unforgiving: an incorrect figure scores nothing, with no partial credit for being close. The aural forgives clumsy phrasing (Fr4) but never a wrong fact. When the answer is a number, double-check the number — a wrong person only costs −1, but a wrong amount costs everything.',
      embodies: {
        behaviour: 'Reports a wrong quantity for a number-based aural item, which the scheme scores 0 regardless of phrasing.',
        cite: MS('p.[18]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr10',
    rule: 'In the aural, wrong numbers score zero.',
    detail:
      'The listening test forgives rough phrasing but not wrong facts: “Incorrect amount of time = 0 Marks”, “Incorrect amount of money = 0 Marks”, with no partial credit for a near-miss figure (a wrong person is only −1). When the answer is a quantity, get the quantity exactly right.',
    cite: MS('p.[18]'),
  },
};

// ─────────────── Fr11 · Don't manipulate when a clean quote will do ───────────────

const FR11: ScaleSession = {
  mode: 'scale',
  id: 'fr-over-manipulate',
  subject: 'french',
  level: 'common',
  title: 'Manipulation you didn’t need',
  cue: 'Comprehension',
  question:
    'A comprehension question is tagged “appropriate direct quotation OR correct manipulation acceptable” — a clean lift would score full marks. The candidate instead rephrases the sentence into their own words and, doing so, breaks a verb form. What does it score (out of 5)?',
  questionNote:
    'Scenario authored for this exercise. This is the mirror of Fr2. Where manipulation is required, a raw lift is docked; but where direct quotation is acceptable, an unforced manipulation that introduces a grammar error is docked instead — the penalty list names “Language/grammar errors in manipulation” and “Manipulation when not required”.',
  scale: {
    name: 'Comprehension · /5 · unforced manipulation',
    levels: [
      { id: 'm0', label: '0 (answer lost in the rephrase)', annotation: '0', marks: 0 },
      { id: 'm4', label: '4 (manipulated, grammar broken)', annotation: '4', marks: 4 },
      { id: 'm5', label: '5 (clean direct quotation)', annotation: '5', marks: 5 },
    ],
    notes: [
      'This question allows “appropriate direct quotation OR correct manipulation” — so a clean lift is worth the full 5.',
      'The penalty list docks “Language/grammar errors in manipulation” and “Manipulation when not required” — max −1 per segment.',
      'Rephrasing into your own words and breaking a verb form takes on risk the question never asked for — one mark gone, to 4.',
      'The safe play when quotation is acceptable: quote cleanly and stop. Save manipulation for the questions that demand it.',
    ],
    cite: MS('p.[4] (Language/grammar errors in manipulation; manipulation when not required), p.[5] (Q.1(a): direct quotation OR manipulation acceptable)'),
  },
  scripts: [
    {
      id: 'fr11-a',
      label: 'The answer',
      persona: 'Rephrases and slips a verb',
      work: [
        'The exact text sentence would have scored 5 as a direct quotation.',
        'Rewrites it in their own words — and mangles a verb form in the process.',
      ],
      keyLevelId: 'm4',
      keyNote:
        '4 — the meaning survives, but the self-imposed rewrite introduced a grammar error, and “language/grammar errors in manipulation” costs a mark. The question offered a free full-mark route: lift the sentence cleanly. Manipulation is a tool for questions that require it, not a way to decorate an answer that was already correct. Don’t take on grammar risk you weren’t asked to carry.',
      embodies: {
        behaviour: 'Manipulates where a direct quotation was acceptable and introduces a grammar error — the docked “errors in manipulation” case.',
        cite: MS('p.[4]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr11',
    rule: 'When quotation is allowed, quote cleanly.',
    detail:
      'Some comprehension questions accept a direct lift OR a manipulation. If a clean quote scores full marks, rephrasing only creates a chance to break grammar — and “language/grammar errors in manipulation” is docked. Manipulate only where the question requires it; otherwise take the safe full-mark lift.',
    cite: MS('p.[4]'),
  },
};

// ─────────────── Fr12 · To change an answer, cancel the old one ───────────────

const FR12: ScaleSession = {
  mode: 'scale',
  id: 'fr-cancel-to-retry',
  subject: 'french',
  level: 'common',
  title: 'The better answer that never counted',
  cue: 'Comprehension',
  question:
    'A candidate writes an answer, then has a better idea and writes a second answer below it — without striking out the first. The first answer is wrong; the second is correct. The first was left standing. What does the question score?',
  questionNote:
    'Scenario authored for this exercise. The comprehension rules state that “any extra sub-division is rewarded only if one of the previous answers to the question is cancelled”, and that two answers on one line are “regarded as one answer and marked accordingly” — the examiner marks what stands, not what you meant to replace.',
  scale: {
    name: 'Comprehension · /5 · replace by cancelling',
    levels: [
      { id: 'm0', label: '0 (first answer stands, it was wrong)', annotation: '0', marks: 0 },
      { id: 'm5', label: '5 (first struck out, correct answer stands)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Rule: “Any extra sub-division is rewarded only if one of the previous answers to the question is cancelled.”',
      'Leave the first answer standing and the improved second one is not rewarded — the original is marked as it is.',
      'Two answers crammed on one line are “regarded as one answer and marked accordingly”.',
      'The fix is one pen-stroke: cross out the answer you are abandoning, clearly, before writing its replacement.',
    ],
    cite: MS('p.[4] (extra sub-division rewarded only if a previous answer is cancelled)'),
  },
  scripts: [
    {
      id: 'fr12-a',
      label: 'The answer',
      persona: 'Rethinks but doesn’t cross out',
      work: [
        'First answer (wrong) — left in place.',
        'Second answer (correct), written just below, first not struck out.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — the correct answer is sitting right there on the page, but the extra attempt is only rewarded if the earlier answer is cancelled, and it wasn’t. The examiner marks the first answer as it stands: wrong. This is a purely mechanical loss and a one-stroke fix — when you change your mind, strike a clean line through the answer you’re replacing so it’s obvious which one to mark.',
      embodies: {
        behaviour: 'Adds a corrected second answer without cancelling the first, so the (wrong) original is the one marked.',
        cite: MS('p.[4]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr12',
    rule: 'To change an answer, strike out the old one.',
    detail:
      'In French comprehension a second attempt is rewarded only if a previous answer is cancelled — an uncancelled correction is ignored and the original stands. When you rethink an answer, draw a clean line through the one you’re abandoning before writing its replacement.',
    cite: MS('p.[4]'),
  },
};

// ─────────────── Fr13 · Register is scored under Communication ───────────────

const FR13: ScaleSession = {
  mode: 'scale',
  id: 'fr-register-communication',
  subject: 'french',
  level: 'common',
  title: 'Perfect grammar, wrong tone',
  cue: 'Written production',
  question:
    'A written-production task is a formal letter. The candidate’s French is grammatically flawless — but the tone is casual throughout (chatty phrasing, tu where vous is expected). Grammar can’t be faulted. Which axis pays for the register, and where does its COMMUNICATION mark land?',
  questionNote:
    'Scenario authored for this exercise. Register is scored on the Communication grid, not the Language grid: the Communication descriptors include “Few mistakes in register” (top) and “Mistakes in register” (bottom). So mismatched register costs Communication marks even when the Language axis is clean.',
  scale: {
    name: 'Communication · /20 · register lives here',
    levels: commBands,
    notes: [
      'The Communication grid lists register explicitly: TOP = “Few mistakes in register”; BOTTOM = “Mistakes in register”.',
      'Register is therefore a Communication matter — flawless grammar (the Language axis) cannot buy it back.',
      'A formal task answered in casual register keeps its content and coherence but forfeits the register descriptor, so it cannot reach the top Communication band.',
      'Match the register the task sets — formal letter vs diary vs opinion piece each carry their own expected tone.',
    ],
    cite: MS('p.[16] (register listed under the Communication grid)'),
  },
  scripts: [
    {
      id: 'fr13-a',
      label: 'The answer',
      persona: 'Immaculate French, casual tone',
      work: [
        'A formal letter, argued clearly and coherently.',
        'But the tone is chatty throughout — casual phrasing, tu where vous belongs.',
      ],
      keyLevelId: 'middle',
      keyNote:
        'Middle band for Communication — the content is coherent and communicative, but register is a Communication descriptor, and casual tone in a formal task keeps it out of the top band. Crucially, the spotless grammar sits on the Language axis and can’t rescue this half: register is judged with content, not accuracy. Read what the task is (letter, diary, opinion) and pitch the tone to match.',
      embodies: {
        behaviour: 'Writes a formal task in casual register — a Communication-grid “mistakes in register” fault that accuracy cannot offset.',
        cite: MS('p.[16]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr13',
    rule: 'Register is a Communication mark, not a Language one.',
    detail:
      'The written-production grid scores register on the Communication axis (“few mistakes in register” at the top, “mistakes in register” at the bottom). A formal task written in casual tone loses Communication marks however perfect the grammar — accuracy can’t buy register back. Pitch the tone to the task: letter, diary, and opinion piece each expect their own.',
    cite: MS('p.[16]'),
  },
};

// ─────────────── Fr14 · The Modified Marking Scheme spelling waiver ───────────────

const FR14: ScaleSession = {
  mode: 'scale',
  id: 'fr-modified-scheme',
  subject: 'french',
  level: 'common',
  title: 'The spelling waiver: would you hear it?',
  cue: 'Written production',
  question:
    'A candidate granted the spelling/grammar waiver (Modified Marking Scheme) writes: «J’ai organisée une fête á mon maisone…» — strewn with accent and spelling slips, but grammatically sound to the ear apart from a couple of audible errors. How does the LANGUAGE axis treat all those visible mistakes?',
  questionNote:
    'Scenario authored for this exercise. Under the Modified Marking Scheme (for candidates with a spelling/grammar waiver, scribe, spell-check or recorded answer), spelling errors and incorrect/missing accents are NOT penalised; grammar is penalised only where the error “would be picked up when listening” — imagine hearing the answer as a recording.',
  scale: {
    name: 'Language · /20 · under the MMS waiver',
    levels: langBands,
    notes: [
      'MMS spelling rule: “do not underline words that are misspelt, or which have missing or incorrect accents” — “incorrect accents [are] spelling errors which are not to be penalised”.',
      'MMS grammar test: “imagine that you are hearing the answer as a recording. Only mistakes that would be picked up when listening should be penalised.”',
      '«Elle a allée» — wrong auxiliary avoir is audible, so it is penalised; «Elle est allé» — the missing agreement is silent, so it is not.',
      'A visually messy answer that is audibly sound therefore lands high on Language: the accents and spelling simply don’t count.',
    ],
    cite: MS('p.[25] (Modified Marking Scheme: accents/spelling not penalised; audible-grammar test)'),
  },
  scripts: [
    {
      id: 'fr14-a',
      label: 'The answer',
      persona: 'Waiver candidate, messy on paper',
      work: [
        '«J’ai organisée une fête á mon maisone pour demain…» — accents and spelling all over the place.',
        'Read aloud, though, it is almost entirely correct: only a couple of errors would actually be heard.',
      ],
      keyLevelId: 'top',
      keyNote:
        'Top band for Language — because under the Modified Marking Scheme the accents and misspellings are struck out from consideration entirely, and only the handful of audible grammar errors count. The page looks error-strewn but the ear hears sound French. This is an access provision, not a loophole: the test is always “would this be picked up on a recording?” — if not, it isn’t penalised.',
      embodies: {
        behaviour: 'Presents an MMS answer whose visible errors are accents/spelling (waived) with only minor audible grammar faults — scored on the audible layer only.',
        cite: MS('p.[25]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr14',
    rule: 'Under the Modified Marking Scheme, only audible errors count.',
    detail:
      'For candidates with a spelling/grammar waiver, the French scheme does not penalise spelling or incorrect/missing accents, and penalises grammar only where the error “would be picked up when listening”. A visually messy but audibly-sound answer scores high on Language — the examiner marks what the ear would catch, not what the eye sees.',
    cite: MS('p.[25]'),
  },
};

// ─────────────── Fr15 · The two-segment higher-mark rule (aural) ───────────────

const FR15: ScaleSession = {
  mode: 'scale',
  id: 'fr-two-segment-lift',
  subject: 'french',
  level: 'common',
  title: 'One strong half lifts the other',
  cue: 'Aural',
  question:
    'A two-detail listening item (worth 3+3) is one of the questions flagged for the “D” rule. The candidate nails the first detail (3 marks) but only half-catches the second (worth 2 on its own). Because of the rule, what is the item total?',
  questionNote:
    'Scenario authored for this exercise. On the flagged two-segment items (A-2, C-2, D-1), the scheme states: “where less than full marks is achieved in either segment, the higher mark is to be awarded to each segment” — a candidate-favouring rule, marked with the annotation “D”.',
  scale: {
    name: 'Aural · two-segment item · /6',
    levels: twoOutcome(5, 6),
    notes: [
      'The rule (annotation “D”, items A-2 / C-2 / D-1): “where less than full marks is achieved in either segment, the higher mark is to be awarded to each segment.”',
      'Segment 1 = 3 (full), segment 2 = 2 (partial): naively that is 5.',
      'The higher segment mark (3) is instead awarded to each segment — so 3 + 3 = 6.',
      'The rule rewards nailing at least one half outright: a single airtight segment lifts a weaker partner on these flagged items.',
    ],
    cite: MS('p.[17] (two-segment rule: higher mark awarded to each segment)'),
  },
  scripts: [
    {
      id: 'fr15-a',
      label: 'The answer',
      persona: 'One detail perfect, one partial',
      work: [
        'Detail 1: fully correct — 3 marks.',
        'Detail 2: only half-caught — would be 2 marks on its own.',
      ],
      keyLevelId: 'm6',
      keyNote:
        '6, not 5 — on these flagged two-segment items the higher of your two segment marks is awarded to BOTH segments, so a perfect first detail (3) pulls the partial second one up from 2 to 3. This is the rare rule that pays you back: on a two-part listening question, make at least one half airtight and it will carry the weaker half. Always attempt both segments — a strong one is never wasted.',
      embodies: {
        behaviour: 'Scores full on one segment and partial on the other of a “D”-flagged item, triggering the higher-mark-to-each-segment lift.',
        cite: MS('p.[17]'),
      },
    },
  ],
  takeaway: {
    id: 'codex-fr15',
    rule: 'On flagged two-part aural items, your best half carries the other.',
    detail:
      'For certain two-segment listening questions (annotation “D”: A-2, C-2, D-1), if either segment falls short of full marks the higher segment mark is awarded to each — so 3+2 becomes 3+3. Attempt both parts and make at least one airtight; a single strong segment lifts its partner.',
    cite: MS('p.[17]'),
  },
};

export const FRENCH_CHAIR: ChairSubject = {
  id: 'french',
  label: 'French',
  tagline: 'Both axes, manipulation, excess, register, the language map — and the oral as conversation.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR11, FR12, FR13, FR14, FR15],
  sources: [
    { label: 'SEC LC French HL marking scheme 2025 (examiner-reports/french/2025-marking-scheme)' },
    { label: 'SEC LC French syllabus — oral assessment (examiner-reports/french/lc-french-syllabus)' },
  ],
  coverageNote:
    'These sessions teach the marking conventions the scheme applies across the whole paper — both Communication and Language axes (the Language axis being a verbs/agreement/spelling gate; register scored on the Communication side), lift-vs-manipulation in both directions, the excess-material deduction, the one-answer and cancel-to-retry rules, the paper’s language map (French in the comprehension, English on the Q.6 opinion, the wrong-language docks), aural detail-accuracy and the two-segment lift, and the Modified Marking Scheme spelling waiver — plus the oral (25% at Higher Level), a general conversation marked on transfer-of-meaning and accuracy. Verified against the 2025 Higher Level written scheme (cross-checked to 2024) and the SEC LC French syllabus; level-specific worked examples are being added.',
};
