/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Spanish (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the no-lifting rule on the written essay, the Content-gates-
 * Language rule on Q5, the verbs-must-be-correct cap on production units, and
 * the exact-transcription rule on finding-a-phrase items) is the real SEC
 * system, cited to:
 *  - SEC LC Spanish HL marking scheme 2025 —
 *    examiner-reports/spanish/2025-marking-scheme.*
 * The oral (Sp5) is a separate component; SEC does NOT publish a per-band oral
 * marking grid, so that session teaches only what the authoritative public
 * syllabus states — the oral's weighting, format and assessment criteria —
 * cited to:
 *  - SEC/NCCA LC Spanish syllabus (Ordinary & Higher) —
 *    examiner-reports/spanish/spanish-syllabus.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Spanish HL marking scheme 2025, ${p}` });
// Oral criteria come from the SEC/NCCA syllabus, NOT the written marking scheme —
// kept on its own helper so the two sources never blur.
const ORAL = (p: string) => ({ label: `SEC/NCCA LC Spanish syllabus, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── Sp1 · No lifting on the essay ───────────────

const SP1: ScaleSession = {
  mode: 'scale',
  id: 'es-no-lift',
  subject: 'spanish',
  level: 'common',
  title: 'Copied phrases score zero',
  cue: 'Written production (Q5)',
  question: 'In the 50-mark written question, a candidate builds paragraphs largely from phrases copied straight out of the reading text. Those copied phrases are relevant and accurate. How are they marked?',
  questionNote:
    'Scenario authored for this exercise. The scheme states plainly for the written question: no marks are awarded for phrases taken directly from the text.',
  scale: {
    name: 'Q5 · lifted phrases',
    levels: two(0, 25),
    notes: [
      'Written-production rule: “No marks will be awarded for phrases taken directly from the text.”',
      'Copying is not producing language — it shows nothing about the candidate’s own Spanish.',
      'Only phrases the candidate constructs themselves can score.',
    ],
    cite: MS('p.9 (no marks for lifted phrases)'),
  },
  scripts: [
    {
      id: 'sp1-a',
      label: 'The essay',
      persona: 'Builds it from the text',
      work: ['Paragraphs assembled largely from phrases lifted out of the reading passage.'],
      keyLevelId: 'm0',
      keyNote:
        'Those lifted phrases score nothing — the rule is explicit and absolute. The written question tests the Spanish you can produce yourself, so recycled text is invisible to it. Rework every idea into your own sentences before it can earn a mark.',
      embodies: {
        behaviour: 'Builds the written answer from phrases copied out of the text — which score no marks.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es1',
    rule: 'On the written question, copied text is worth nothing.',
    detail:
      'Spanish awards no marks for phrases taken directly from the reading text. The essay tests the language you produce yourself — rework every borrowed idea into your own sentences.',
    cite: MS('p.9'),
  },
};

// ─────────────── Sp2 · Content gates Language ───────────────

const SP2: ScaleSession = {
  mode: 'scale',
  id: 'es-content-gates',
  subject: 'spanish',
  level: 'common',
  title: 'Off-topic sinks both scores',
  cue: 'Written production (Q5)',
  question: 'The 50-mark written question is marked on two axes: Content-Communication (25) and Language (25). A candidate writes accurate, elegant Spanish — but it does not address the task at all, so Content scores 0. What is the maximum Language mark?',
  questionNote:
    'Scenario authored for this exercise. On this question the scheme ties the axes: where no marks are awarded for Content, no marks are awarded for Language either.',
  scale: {
    name: 'Q5 · Language /25',
    levels: two(0, 25),
    notes: [
      'The written question is scored Content-Communication 25 + Language 25.',
      'Unlike some languages, here the axes are tied: “Where no marks are awarded for Content, no marks will be awarded for Language.”',
      'So accurate Spanish that ignores the task scores 0 on BOTH axes.',
    ],
    cite: MS('p.9 (Content gates Language)'),
  },
  scripts: [
    {
      id: 'sp2-a',
      label: 'The essay',
      persona: 'Lovely Spanish, wrong task',
      work: [
        'Accurate, elegant Spanish throughout.',
        'But it never addresses the question set — Content = 0.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Language is capped at 0 too — Spanish ties the axes, so a Content of zero drags Language down with it. You cannot bank language marks on beautiful but irrelevant writing here. Address the actual task first; only then does your accuracy start to pay.',
      embodies: {
        behaviour: 'Writes accurate but off-task Spanish, where a zero Content also zeroes Language.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es2',
    rule: 'No content, no language marks.',
    detail:
      'On the Spanish written question the two axes are tied: if your answer doesn’t address the task, Content scores 0 and Language is dragged to 0 with it. Answer the question first — accuracy only counts once the content does.',
    cite: MS('p.9'),
  },
};

// ─────────────── Sp3 · Verbs must be correct ───────────────

const SP3: ScaleSession = {
  mode: 'scale',
  id: 'es-verbs',
  subject: 'spanish',
  level: 'common',
  title: 'Verbs gate full marks',
  cue: 'Written production (Section C)',
  question: 'A Section C production unit (a dialogue turn) is worth 6 marks. The candidate communicates the intended message clearly — but the verb is in the wrong form. What is the maximum this unit can score?',
  questionNote:
    'Scenario authored for this exercise. In Section C, each production unit’s top band states the communicative intention must be fulfilled AND the verbs must be correct for full marks.',
  scale: {
    name: 'Section C unit · /6',
    levels: [
      { id: 'm0', label: '0', annotation: '0', marks: 0 },
      { id: 'm4', label: '4 (message clear, verb wrong)', annotation: '4', marks: 4 },
      { id: 'm6', label: '6 (message + correct verb)', annotation: '6', marks: 6 },
    ],
    notes: [
      'Top band: “Communicative intention fulfilled. Verbs must be correct for full marks.”',
      'A clear message with a wrong verb communicates, but can’t reach the top band.',
      'Verb accuracy is the single most repeated gate in the scheme.',
    ],
    cite: MS('p.10–11 (Section C band scales, verb rule)'),
  },
  scripts: [
    {
      id: 'sp3-a',
      label: 'The unit',
      persona: 'Message clear, verb wrong',
      work: ['The dialogue turn gets the message across clearly.', 'But the verb is in the wrong form.'],
      keyLevelId: 'm4',
      keyNote:
        'Full marks are gated on a correct verb, so a clear message with a wrong verb lands below the top band. Communication earns you most of the way; the verb earns you the last step. Nail the verb form and the tense — it is the gate the scheme checks on every unit.',
      embodies: {
        behaviour: 'Communicates clearly but with an incorrect verb — capped below full marks by the verb gate.',
        cite: MS('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es3',
    rule: 'Correct verbs unlock full marks.',
    detail:
      'Every Spanish production unit gates its top band on a correct verb: a clear message with a wrong verb form can’t reach full marks. Get the verb and tense right — it’s the accuracy check the scheme applies on every unit.',
    cite: MS('p.10'),
  },
};

// ─────────────── Sp4 · Transcription — copy the exact phrase ───────────────

const SP4: ScaleSession = {
  mode: 'scale',
  id: 'es-transcription',
  subject: 'spanish',
  level: 'common',
  title: 'Copy the phrase exactly',
  cue: 'Written comprehension (transcription)',
  question: 'A finding-a-phrase question asks the candidate to copy from the text the exact words that mean “X”. They locate the right phrase — but pad it with a couple of extra words to be safe. The item prints: “No marks awarded if extra words are added. Exact transcription required.” What does it score?',
  questionNote:
    'Scenario authored for this exercise. Spanish comprehension transcription items carry a printed exact-transcription rule; adding extra words voids the item. Verified present in the 2023, 2024 and 2025 schemes.',
  scale: {
    name: 'Transcription · exact',
    levels: two(0, 4),
    notes: [
      'These finding-a-phrase items require the exact phrase copied from the text.',
      'The printed rule: “No marks awarded if extra words are added. Exact transcription required.”',
      'Padding the correct phrase with extra words voids the whole item — it is all-or-nothing.',
    ],
    cite: MS('p.5 (exact transcription: no marks if extra words added)'),
  },
  scripts: [
    {
      id: 'sp4-a',
      label: 'The item',
      persona: 'Right phrase, padded',
      work: ['Finds and copies the correct phrase from the text.', 'Adds a couple of extra words “to be safe”.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the extra words void the item, because exact transcription is all-or-nothing here. The correct phrase was already worth full marks; the padding threw them away. On these items, copy only the words the question asks for and stop.',
      embodies: {
        behaviour: 'Pads a correct transcription with extra words, which the exact-transcription rule voids entirely.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es4',
    rule: 'On transcription items, copy the exact phrase — nothing extra.',
    detail:
      'Spanish finding-a-phrase questions require exact transcription: adding extra words scores no marks, even when the right phrase is in there. Copy only the words the question asks for — padding “to be safe” voids the item.',
    cite: MS('p.5'),
  },
};

// ─────────────── Sp5 · The oral — converse, don't recite ───────────────

const SP5: ScaleSession = {
  mode: 'scale',
  id: 'es-oral',
  subject: 'spanish',
  level: 'common',
  title: 'The oral: converse, don’t recite',
  cue: 'Oral',
  question: 'The Spanish oral (25% of the marks at Higher Level, 20% at Ordinary) is a general conversation plus a role-play, marked on two criteria: (i) your ability to transfer meaning and (ii) the accuracy and appropriateness of your language. A candidate delivers a flawless, memorised speech about their hobbies — but it doesn’t answer what the examiner actually asked. How does that land?',
  questionNote:
    'Scenario authored for this exercise. The band marks below are ILLUSTRATIVE — SEC does not publish per-band oral cut-points. The load-bearing, cited facts are the syllabus’s weighting (Speaking 25% HL / 20% OL), the general-conversation + role-play format, the two assessment criteria, and the principle that assessment emphasises language and communication rather than information content.',
  scale: {
    name: 'Oral · communication (illustrative)',
    levels: [
      { id: 'recite', label: 'Low — recited, off-question', annotation: 'L', marks: 8 },
      { id: 'partial', label: 'Moderate', annotation: 'M', marks: 14 },
      { id: 'converse', label: 'High — genuine, accurate exchange', annotation: 'H', marks: 20 },
    ],
    notes: [
      'The oral is Speaking 25% (Higher) / 20% (Ordinary): a general conversation plus a role-play, 15 minutes.',
      'Assessment criteria: “(i) ability to transfer meaning and (ii) degrees of accuracy and appropriateness of language, including the range of vocabulary and structures used.”',
      'Assessment “will emphasise language and communication skills rather than the information content” — so a recited, off-question speech fails criterion (i), however polished.',
    ],
    cite: ORAL('p.24 (Speaking 25%/20%, assessment criteria), p.25 (oral format), p.2 (language over information content)'),
  },
  scripts: [
    {
      id: 'sp5-a',
      label: 'The oral',
      persona: 'Perfect speech, wrong question',
      work: [
        'A flawless, memorised paragraph about hobbies.',
        'But it doesn’t engage with what the examiner actually asked.',
      ],
      keyLevelId: 'recite',
      keyNote:
        'It lands low — the first criterion is your ability to transfer meaning in a real exchange, and reciting past the question doesn’t do that, however clean the Spanish. The oral rewards communication over rehearsed content: listen, answer what’s asked, and let the conversation move. A simpler point that genuinely responds beats a perfect speech aimed at the wrong question.',
      embodies: {
        behaviour: 'Recites a memorised passage instead of conversing — failing the transfer-of-meaning criterion the oral is built on.',
        cite: ORAL('p.24'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es5',
    rule: 'The oral rewards conversation, not recitation.',
    detail:
      'Spanish oral marks (25% HL / 20% OL) reward your ability to transfer meaning and the accuracy of your language — not memorised content. Listen and answer what’s actually asked; a real, accurate exchange beats a polished speech aimed at the wrong question.',
    cite: ORAL('p.24'),
  },
};

// ─────────────── Sp6 · Answer the aural in English ───────────────

const SP6: ScaleSession = {
  mode: 'scale',
  id: 'es-aural-language',
  subject: 'spanish',
  level: 'common',
  title: 'Answer the aural in English',
  cue: 'Listening comprehension (aural)',
  question:
    'The Listening test is worth 80 marks and must be answered in English. A strong candidate hears everything correctly and writes answers that would earn full marks — but writes them in Spanish. How does that score?',
  questionNote:
    'Scenario authored for this exercise. The aural carries a printed language rule: answers must be in English, and a whole test/section answered in Spanish is marked as normal and then halved.',
  scale: {
    name: 'Aural · /80',
    levels: two(40, 80),
    notes: [
      'Aural general rule: “All answers must be in English.”',
      'Wrong-language penalty: “If the entire test/section is answered in Spanish: mark as per Marking Scheme and award half of the marks gained.”',
      'So correct content written in Spanish is first marked normally, then cut in half — an 80 becomes 40.',
    ],
    cite: MS('p.12 (aural: answer in English; Spanish answers marked then halved)'),
  },
  scripts: [
    {
      id: 'sp6-a',
      label: 'The aural',
      persona: 'Right answers, wrong language',
      work: [
        'Hears every item correctly.',
        'Writes answers that would earn full marks — but writes them in Spanish, not English.',
      ],
      keyLevelId: 'm40',
      keyNote:
        'The content is marked as normal and then halved, because the aural must be answered in English. Perfect comprehension in the wrong language throws away half the section for nothing. Read the instruction: the Listening answers go in English — it costs you nothing to comply and half the marks to forget.',
      embodies: {
        behaviour: 'Answers the aural correctly but in Spanish, triggering the half-marks language penalty.',
        cite: MS('p.12'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es6',
    rule: 'The aural is answered in English — Spanish answers are halved.',
    detail:
      'The Spanish Listening test must be answered in English; a whole section answered in Spanish is marked and then cut to half the marks gained. Correct answers in the wrong language lose half the section — write your aural answers in English.',
    cite: MS('p.12'),
  },
};

// ─────────────── Sp7 · The opinion question must be in Spanish ───────────────

const SP7: ScaleSession = {
  mode: 'scale',
  id: 'es-opinion-spanish',
  subject: 'spanish',
  level: 'common',
  title: 'The opinion question must be in Spanish',
  cue: 'Written comprehension (opinion item)',
  question:
    'Most comprehension answers are written in English — but the short 6-mark opinion question at the end of a reading text is different. A candidate gives a thoughtful, on-point opinion — written in English. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The comprehension opinion item is the one reading answer that must be given in Spanish; the scheme prints that English answers score nothing on it.',
  scale: {
    name: 'Opinion item · /6',
    levels: two(0, 6),
    notes: [
      'Comprehension answers are written in English — except this opinion item.',
      'The printed rule: “Any mark from 0 to 6 may be awarded for this question. No marks for answers in English.”',
      'So a good opinion written in English scores 0 — the language, not the idea, is the gate.',
    ],
    cite: MS('p.6 (opinion item: no marks for answers in English)'),
  },
  scripts: [
    {
      id: 'sp7-a',
      label: 'The opinion',
      persona: 'Good point, wrong language',
      work: [
        'Gives a thoughtful, relevant opinion on the text.',
        'Writes it in English — like the rest of the comprehension answers.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — the opinion item awards no marks for answers in English, however good the point. This is the one reading answer that flips to Spanish, so the reflex of answering comprehension in English costs you the whole item here. Spot the “answer in Spanish” instruction and switch languages for it.',
      embodies: {
        behaviour: 'Answers the Spanish-only opinion item in English, which the scheme scores at zero.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es7',
    rule: 'Answer the opinion question in Spanish, not English.',
    detail:
      'Most Spanish comprehension answers are written in English, but the short opinion item is the exception: it awards no marks for answers in English. Watch for the “answer in Spanish” instruction — the one reading question where writing in English scores zero.',
    cite: MS('p.6'),
  },
};

export const SPANISH_CHAIR: ChairSubject = {
  id: 'spanish',
  label: 'Spanish',
  tagline:
    'No lifting, content-before-language, the verb gate, the right answer-language — and an oral that rewards real conversation.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [SP1, SP2, SP3, SP4, SP5, SP6, SP7],
  sources: [
    { label: 'SEC LC Spanish HL marking scheme 2025 (examiner-reports/spanish/2025-marking-scheme)' },
    { label: 'SEC/NCCA LC Spanish syllabus, Ordinary & Higher (examiner-reports/spanish/spanish-syllabus)' },
  ],
  coverageNote:
    'The written-paper sessions (no-lifting, content-gates-language, verb gate, exact transcription, the aural answer-in-English half-marks rule, and the Spanish-only opinion item) apply at both Higher and Ordinary level, verified against the 2025 Higher Level scheme. The oral session (Sp5) teaches the syllabus-defined weighting, format and assessment criteria of the Speaking component (SEC does not publish a per-band oral grid, so no internal cut-points are asserted). Level-specific worked examples are being added.',
};
