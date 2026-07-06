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

export const FRENCH_CHAIR: ChairSubject = {
  id: 'french',
  label: 'French',
  tagline: 'Two axes, manipulation, the one-answer rule — and the oral as conversation.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [FR1, FR2, FR3, FR4, FR5],
  sources: [
    { label: 'SEC LC French HL marking scheme 2025 (examiner-reports/french/2025-marking-scheme)' },
    { label: 'SEC LC French syllabus — oral assessment (examiner-reports/french/lc-french-syllabus)' },
  ],
  coverageNote:
    'These sessions teach the marking conventions the scheme applies across the written paper — the two Communication/Language axes, lift-vs-manipulation, and the one-answer rule — plus the oral (25% at Higher Level), which is a general conversation marked on transfer-of-meaning and accuracy. Verified against the 2025 Higher Level written scheme and the SEC LC French syllabus; level-specific worked examples are being added.',
};
