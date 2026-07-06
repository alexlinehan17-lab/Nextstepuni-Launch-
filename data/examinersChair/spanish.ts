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
 * system. Most sessions cite the 2025 scheme, but several standing rules are
 * worded verbatim only in the earlier filed schemes, so those sessions are cited
 * to the year where the quoted line actually appears (with a verified page):
 *  - SEC LC Spanish HL marking scheme 2025 —
 *    examiner-reports/spanish/2025-marking-scheme.*
 *  - SEC LC Spanish HL marking scheme 2024 —
 *    examiner-reports/spanish/2024-marking-scheme.* (Content/Language band
 *    descriptors, the Q2 correct-tense rule, and the answer-both-only-higher rule)
 *  - SEC LC Spanish HL marking scheme 2023 —
 *    examiner-reports/spanish/2023-marking-scheme.* (the literature
 *    discuss-don't-quote rule and the note-vs-letter development contrast)
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
// Some standing rules are worded verbatim in the earlier filed schemes but NOT
// in the 2025 one — those sessions cite the year where the quoted line actually
// appears (see the header note), so the citation always resolves to a real page.
const MS23 = (p: string) => ({ label: `SEC Spanish HL marking scheme 2023, ${p}` });
const MS24 = (p: string) => ({ label: `SEC Spanish HL marking scheme 2024, ${p}` });
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

// ─────────────── Sp8 · Literature — discuss, don't quote ───────────────

const SP8: ScaleSession = {
  mode: 'scale',
  id: 'es-literature-discuss',
  subject: 'spanish',
  level: 'common',
  title: 'Discuss the literature — don’t quote it back',
  cue: 'Written comprehension (literature discussion)',
  question:
    'The prescribed-literature discussion (Q5, 12 marks) asks you to discuss three relevant points. A candidate makes three good points — but proves each one by quoting the lines straight from the extract. The item prints: “No marks awarded for answers supported by reference to the extract.” What does it score?',
  questionNote:
    'Scenario authored for this exercise. The literature discussion question carries a printed rule that answers supported by reference to the extract score nothing — verified verbatim in the 2023 scheme (p.5).',
  scale: {
    name: 'Literature Q5 · /12',
    levels: two(0, 12),
    notes: [
      'The prescribed-literature discussion is 4 + 4 + 4 = 12: discuss any three relevant points.',
      'The printed rule: “No marks awarded for answers supported by reference to the extract.”',
      'You must discuss in your own words — quoting the passage back to “prove” a point earns nothing.',
    ],
    cite: MS23('p.5 (literature Q5: no marks for answers supported by reference to the extract)'),
  },
  scripts: [
    {
      id: 'sp8-a',
      label: 'The discussion',
      persona: 'Good points, propped on quotes',
      work: [
        'Makes three relevant points about the extract.',
        'Backs each one up by quoting lines straight from the passage.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'It scores nothing — the rule voids answers supported by reference to the extract, however sound the points. This question tests whether you can discuss and analyse in your own words, not whether you can copy the passage back. Make the point, then explain it yourself instead of quoting the text to do the work.',
      embodies: {
        behaviour: 'Supports each discussion point by quoting the extract, which the scheme scores at zero.',
        cite: MS23('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es8',
    rule: 'Discuss the literature in your own words — quoting it back scores zero.',
    detail:
      'The Spanish literature discussion awards no marks for answers supported by reference to the extract. Make and explain your points yourself; copying the passage to prove them earns nothing on this question.',
    cite: MS23('p.5'),
  },
};

// ─────────────── Sp9 · The Content band — the Spanish-speaker test ───────────────

const SP9: ScaleSession = {
  mode: 'scale',
  id: 'es-content-band',
  subject: 'spanish',
  level: 'common',
  title: 'The Spanish-speaker test sets your Content band',
  cue: 'Written production (Q5 Content band)',
  question:
    'The Q5 Content/Communication axis (25 marks) is picked by band, then a mark within it. The line between the bottom and middle bands is one operational test: MIDDLE = “comprehensible to Spanish speaker”, BOTTOM = “Spanish speaker would have difficulty understanding”. A candidate’s essay is on-task and a Spanish reader can follow it, though there is some irrelevant padding. Which band?',
  questionNote:
    'Scenario authored for this exercise. The band descriptors and the “Spanish speaker” comprehensibility line are the real Q5 Content/Communication scale, printed identically in the 2023 and 2024 schemes (verified verbatim on p.9 of 2024).',
  scale: {
    name: 'Q5 Content · /25',
    levels: [
      { id: 'bottom', label: 'Bottom — a Spanish speaker would struggle', annotation: 'B', marks: 8 },
      { id: 'middle', label: 'Middle — comprehensible to a Spanish speaker', annotation: 'M', marks: 17 },
      { id: 'top', label: 'Top — coherent, clearly argued, on-point', annotation: 'T', marks: 25 },
    ],
    notes: [
      'The Content/Communication axis bands: BOTTOM 0–8, MIDDLE 9–17, TOP 18–25.',
      'The bottom/middle line is one test: MIDDLE = “comprehensible to Spanish speaker”; BOTTOM = “Spanish speaker would have difficulty understanding”.',
      'TOP adds high coherence, clear argumentation and “little or no irrelevant material”.',
    ],
    cite: MS24('p.9 (Q5 Content/Communication band descriptors)'),
  },
  scripts: [
    {
      id: 'sp9-a',
      label: 'The essay',
      persona: 'Followable, a bit padded',
      work: [
        'On-task and reasonably coherent — a Spanish reader follows the argument.',
        'Carries some irrelevant padding along the way.',
      ],
      keyLevelId: 'middle',
      keyNote:
        'It lands in the middle band: a Spanish speaker can follow it and the intention is more or less fulfilled, but the padding and looser coherence keep it off the top. To climb, cut the irrelevant material and tighten the argument — the top band wants clear argumentation and little or no filler. Write to be understood first; that alone lifts you out of the bottom band.',
      embodies: {
        behaviour: 'Writes on-task, comprehensible Spanish with some irrelevant padding — a middle-band Content answer.',
        cite: MS24('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es9',
    rule: 'Whether a Spanish speaker can follow you sets your Content band.',
    detail:
      'The Q5 Content axis is banded by comprehensibility: “comprehensible to Spanish speaker” is the middle band, difficulty understanding is the bottom. Write to be understood, then cut the irrelevant material — clarity and coherence carry you to the top.',
    cite: MS24('p.9'),
  },
};

// ─────────────── Sp10 · The Language band — verbs are the spine ───────────────

const SP10: ScaleSession = {
  mode: 'scale',
  id: 'es-language-band',
  subject: 'spanish',
  level: 'common',
  title: 'Verbs run down the middle of the Language band',
  cue: 'Written production (Q5 Language band)',
  question:
    'The Q5 Language axis (25 marks) is also banded, and verbs run down the spine of it: BOTTOM = “most verbs incorrect”, MIDDLE = “verbs generally correct”, TOP = “correct usage of tenses”. A candidate writes with a decent range of vocabulary and gets most verbs right, with a few slips. Which Language band?',
  questionNote:
    'Scenario authored for this exercise. The Language band descriptors — verbs as the operational marker across the three bands — are the real Q5 Language scale, printed identically in the 2023 and 2024 schemes (verified verbatim on p.9 of 2024).',
  scale: {
    name: 'Q5 Language · /25',
    levels: [
      { id: 'bottom', label: 'Bottom — most verbs incorrect', annotation: 'B', marks: 8 },
      { id: 'middle', label: 'Middle — verbs generally correct', annotation: 'M', marks: 17 },
      { id: 'top', label: 'Top — idiomatic, tenses correct', annotation: 'T', marks: 25 },
    ],
    notes: [
      'The Language axis bands: BOTTOM 0–8, MIDDLE 9–17, TOP 18–25.',
      'Verbs are the spine: BOTTOM = “most verbs incorrect”, MIDDLE = “verbs generally correct”, TOP = “correct usage of tenses”.',
      'The jump to the top band is idiomatic Spanish, a good range of vocabulary and correct tenses throughout.',
    ],
    cite: MS24('p.9 (Q5 Language band descriptors)'),
  },
  scripts: [
    {
      id: 'sp10-a',
      label: 'The essay',
      persona: 'Verbs mostly right',
      work: [
        'A decent range of vocabulary, generally adequate and appropriate.',
        'Most verbs correct, with a few slips and not too many spelling mistakes.',
      ],
      keyLevelId: 'middle',
      keyNote:
        'It sits in the middle Language band: “verbs generally correct” is the middle descriptor exactly. The top band needs correct usage of tenses throughout plus idiomatic Spanish, so those few verb slips are what hold it down. Drill your verb forms and tenses — they are the single marker that moves you up this axis.',
      embodies: {
        behaviour: 'Writes with good vocabulary and generally-correct verbs plus a few slips — a middle-band Language answer.',
        cite: MS24('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es10',
    rule: 'Your verb accuracy sets your Language band.',
    detail:
      'The Q5 Language axis is banded on verbs: “most verbs incorrect” is the bottom, “verbs generally correct” the middle, correct tenses the top. Tighten your verb forms and tenses — they are the marker that climbs this axis.',
    cite: MS24('p.9'),
  },
};

// ─────────────── Sp11 · The note needs the point made, not developed ───────────────

const SP11: ScaleSession = {
  mode: 'scale',
  id: 'es-note-development',
  subject: 'spanish',
  level: 'common',
  title: 'Develop the letter; the note just needs the point made',
  cue: 'Written production (Section C note/diary)',
  question:
    'The Section C note/diary is 20 marks: four points to communicate, max 5 each. Its instruction says “development of points not necessarily essential” — unlike the letter, where “each point should be developed and expanded”. A candidate communicates all four note points clearly, verbs correct, but each is short and undeveloped. What can each point score?',
  questionNote:
    'Scenario authored for this exercise. The note/diary’s “development not necessarily essential” rule (p.11) and the letter’s “developed and expanded” requirement (p.10) are printed in the Section C guidelines of the 2023 scheme.',
  scale: {
    name: 'Note point · /5',
    levels: two(0, 5),
    notes: [
      'The note/diary is four points × max 5, and its rule reads “Development of points not necessarily essential.”',
      'That is the opposite of the letter, where “each point should be developed and expanded”.',
      'A short, clear point with correct verbs can take full marks on the note — bareness is not penalised here.',
    ],
    cite: MS23('p.11 (note/diary: development not essential), p.10 (letter: developed and expanded)'),
  },
  scripts: [
    {
      id: 'sp11-a',
      label: 'The note',
      persona: 'Terse but correct',
      work: [
        'Communicates all four note points clearly.',
        'Each is short and undeveloped, verbs correct.',
      ],
      keyLevelId: 'm5',
      keyNote:
        'Each point can score full marks — the note explicitly does not require development, so clear communication with correct verbs is enough. Save the developing-and-expanding for the letter, where it is required; on the note, spending extra time padding points earns you nothing. Make the four points cleanly, get the verbs right, and move on.',
      embodies: {
        behaviour: 'Makes bare but clear note points with correct verbs, which score full where development is not required.',
        cite: MS23('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es11',
    rule: 'Develop the letter; the note just needs each point made.',
    detail:
      'Section C splits its two production rules: the letter’s points must be “developed and expanded”, but on the note/diary “development of points is not necessarily essential”. Develop where it’s required and keep the note clean and correct — extra padding there earns nothing.',
    cite: MS23('p.10'),
  },
};

// ─────────────── Sp12 · One correct point banks the biggest slice ───────────────

const SP12: ScaleSession = {
  mode: 'scale',
  id: 'es-first-correct',
  subject: 'spanish',
  level: 'common',
  title: 'One correct point still banks the biggest slice',
  cue: 'Written comprehension (4+3+3 items)',
  question:
    'A comprehension question wants three points and splits the marks 4 + 3 + 3 = 10, printed “First correct answer = 4m”. A candidate is sure of only one of the three points and writes just that one, correctly. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The “First correct answer = 4m” ordering rule on 4+3+3 items is printed across the comprehension sections of the 2023, 2024 and 2025 schemes.',
  scale: {
    name: '4+3+3 item · /10',
    levels: [
      { id: 'none', label: '0 — no correct point', annotation: '0', marks: 0 },
      { id: 'one', label: '4 — one correct point', annotation: '4', marks: 4 },
      { id: 'two', label: '7 — two correct points', annotation: '7', marks: 7 },
      { id: 'three', label: '10 — all three', annotation: '10', marks: 10 },
    ],
    notes: [
      'These items split 4 + 3 + 3 and print “First correct answer = 4m”.',
      'The credit is front-loaded: the first correct point earns 4, not a flat third of 10.',
      'So even a single correct point banks 4 marks — never leave one of these blank.',
    ],
    cite: MS('p.5 (4+3+3 comprehension items: first correct answer = 4m)'),
  },
  scripts: [
    {
      id: 'sp12-a',
      label: 'The item',
      persona: 'Sure of just one',
      work: [
        'Confident about only one of the three points wanted.',
        'Writes that single point, correctly, and leaves the rest.',
      ],
      keyLevelId: 'one',
      keyNote:
        'It scores 4 — the first correct point takes the biggest slice, not a flat third of the marks. That means attempting even one point you are sure of banks 4 out of 10 here, so these items should never be left blank. Write what you know; the marking rewards the first correct point disproportionately.',
      embodies: {
        behaviour: 'Answers only the one point they are sure of, banking the front-loaded 4 marks.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es12',
    rule: 'One correct point still banks the biggest slice — never leave these blank.',
    detail:
      'On 4+3+3 comprehension items the first correct point earns 4, not a flat third. Even a single point you are sure of banks 4 out of 10, so always write what you know rather than leaving the item empty.',
    cite: MS('p.5'),
  },
};

// ─────────────── Sp13 · Finish the idea — partial answers earn partial marks ───────────────

const SP13: ScaleSession = {
  mode: 'scale',
  id: 'es-graded-credit',
  subject: 'spanish',
  level: 'common',
  title: 'Finish the idea — half an answer earns half the marks',
  cue: 'Written comprehension (graded credit)',
  question:
    'A 4-mark comprehension point carries a printed breakdown: the complete idea (what makes Spain a unique, welcoming country that keeps attracting people) = 4m; “It makes Spain unique/welcoming” = 2m; “Spain is unique only” = 1m. A candidate writes only “Spain is unique.” What does it score?',
  questionNote:
    'Scenario authored for this exercise. The graded partial-credit ladder inside comprehension points (e.g. the 2025 Section A Q1(e) breakdown) is printed in the scheme — half an idea earns a fraction of the marks.',
  scale: {
    name: 'Graded point · /4',
    levels: [
      { id: 'wrong', label: '0 — not the idea', annotation: '0', marks: 0 },
      { id: 'part1', label: '1 — “Spain is unique” only', annotation: '1', marks: 1 },
      { id: 'part2', label: '2 — unique/welcoming', annotation: '2', marks: 2 },
      { id: 'full', label: '4 — the complete idea', annotation: '4', marks: 4 },
    ],
    notes: [
      'Some comprehension points carry a printed partial-credit ladder inside them.',
      'Here: the complete idea = 4m; “It makes Spain unique/welcoming” = 2m; “Spain is unique only” = 1m.',
      'Half an idea earns a fraction of the marks — completeness is scored, not just the right direction.',
    ],
    cite: MS('p.6 (Section A Q1(e) graded partial credit: unique/welcoming 2m, unique only 1m)'),
  },
  scripts: [
    {
      id: 'sp13-a',
      label: 'The point',
      persona: 'Half the idea',
      work: [
        'Heads in the right direction with “Spain is unique”.',
        'Stops there — leaves out the “welcoming, keeps attracting people” half.',
      ],
      keyLevelId: 'part1',
      keyNote:
        'It scores 1 of 4 — “Spain is unique only” is the lowest rung of the printed ladder. The examiner marks completeness, not just the right direction, so stopping halfway costs three of the four marks. When a comprehension point is worth several marks, finish the whole idea rather than the first clause of it.',
      embodies: {
        behaviour: 'Gives only the first clause of a graded point, earning the lowest rung of the printed ladder.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es13',
    rule: 'Finish the idea — partial answers earn partial marks.',
    detail:
      'Spanish comprehension points often carry a printed partial-credit ladder: half an idea scores a fraction of the marks. When a point is worth several marks, complete the whole idea rather than stopping at the first clause.',
    cite: MS('p.6'),
  },
};

// ─────────────── Sp14 · Get the tense right on the manipulation items ───────────────

const SP14: ScaleSession = {
  mode: 'scale',
  id: 'es-tense-manipulation',
  subject: 'spanish',
  level: 'common',
  title: 'The tense items: meaning alone won’t earn the mark',
  cue: 'Written comprehension (tense-manipulation items)',
  question:
    'The Section B Q2 items (5 marks each, awarded whole) ask you to render sentences from the text, and print “Correct tense required for full marks”. A candidate captures the meaning of the sentence but puts the verb in the wrong tense. What does the 5-mark item score?',
  questionNote:
    'Scenario authored for this exercise. The Section B Q2 items are single 5-mark blocks with the printed rule “Correct tense required for full marks”, verified verbatim in the 2023 and 2024 schemes (p.8 of 2024).',
  scale: {
    name: 'Q2 tense item · /5',
    levels: two(0, 5),
    notes: [
      'These 5-mark items are awarded whole and carry the rule “Correct tense required for full marks”.',
      'They test whether you can render the sentence in the right tense — capturing the meaning is not enough on its own.',
      'A right idea in the wrong tense fails the requirement, so the mark is withheld.',
    ],
    cite: MS24('p.8 (Section B Q2: correct tense required for full marks)'),
  },
  scripts: [
    {
      id: 'sp14-a',
      label: 'The item',
      persona: 'Right meaning, wrong tense',
      work: [
        'Captures the meaning of the sentence from the text.',
        'Renders the verb in the wrong tense.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The mark is withheld — these items require the correct tense for full marks, and there is no partial credit printed on a single 5-mark block. Getting the gist is not the task; rendering it in the right tense is. Read exactly which tense the text uses and match it before you commit the answer.',
      embodies: {
        behaviour: 'Renders a Q2 sentence with the right meaning but the wrong tense, failing the tense requirement.',
        cite: MS24('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es14',
    rule: 'On the tense items, get the tense right — meaning alone won’t earn the mark.',
    detail:
      'The Section B Q2 items are marked whole and require the correct tense for full marks. A right idea in the wrong tense fails the requirement — match the tense the text uses before committing your answer.',
    cite: MS24('p.8'),
  },
};

// ─────────────── Sp15 · Pick one Section C option and commit ───────────────

const SP15: ScaleSession = {
  mode: 'scale',
  id: 'es-both-parts',
  subject: 'spanish',
  level: 'common',
  title: 'Answer both options and only the higher one counts',
  cue: 'Written production (Section C choice)',
  question:
    'Section C asks you to attempt either Q1(a) or Q1(b) — one 30-mark task. A nervous candidate writes BOTH: a weaker dialogue and a stronger letter. The scheme says both are marked and “marks will be awarded only for the higher scoring of the two”. If the dialogue would score 20 and the letter 27, what is awarded?',
  questionNote:
    'Scenario authored for this exercise; the 20 and 27 are illustrative script marks. The rule — both attempts marked, only the higher counts — is printed in the Section C guidelines of the 2023 and 2024 schemes (p.10 of 2024).',
  scale: {
    name: 'Section C choice · /30',
    levels: two(20, 27),
    notes: [
      'You choose one of (a)/(b). If you answer both, “both must be marked and marks will be awarded only for the higher scoring of the two”.',
      'Doing both does not add up, and does not hurt — but it splits your time across two answers.',
      'You are better off committing to one task and making it your strongest.',
    ],
    cite: MS24('p.10 (Section C: if both attempted, only the higher scores)'),
  },
  scripts: [
    {
      id: 'sp15-a',
      label: 'The choice',
      persona: 'Hedges with both',
      work: [
        'Writes a weaker dialogue that would score 20.',
        'Also writes a stronger letter that would score 27.',
      ],
      keyLevelId: 'm27',
      keyNote:
        'You are awarded 27 — only the higher-scoring attempt counts, so the weaker dialogue earns nothing extra. Hedging by writing both does not add the marks together; it just spends the time you needed to make one answer excellent. Pick the option you are strongest at and put all of it there.',
      embodies: {
        behaviour: 'Attempts both Section C options, so only the higher-scoring answer is credited.',
        cite: MS24('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es15',
    rule: 'Pick one Section C option and commit — a second answer only costs you time.',
    detail:
      'If you attempt both (a) and (b) of a Section C question, both are marked but “only the higher scoring of the two” counts. Writing both never adds up — choose the task you are strongest at and spend all your time making that one answer excellent.',
    cite: MS24('p.10'),
  },
};

export const SPANISH_CHAIR: ChairSubject = {
  id: 'spanish',
  label: 'Spanish',
  tagline:
    'No lifting, content-before-language, the verb and tense gates, the two-axis bands, front-loaded partial credit, the right answer-language — and an oral that rewards real conversation.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [SP1, SP2, SP3, SP4, SP5, SP6, SP7, SP8, SP9, SP10, SP11, SP12, SP13, SP14, SP15],
  sources: [
    { label: 'SEC LC Spanish HL marking scheme 2025 (examiner-reports/spanish/2025-marking-scheme)' },
    { label: 'SEC LC Spanish HL marking scheme 2024 (examiner-reports/spanish/2024-marking-scheme)' },
    { label: 'SEC LC Spanish HL marking scheme 2023 (examiner-reports/spanish/2023-marking-scheme)' },
    { label: 'SEC/NCCA LC Spanish syllabus, Ordinary & Higher (examiner-reports/spanish/spanish-syllabus)' },
  ],
  coverageNote:
    'The fourteen written-paper sessions — no-lifting, content-gates-language, the Section C verb gate, exact transcription, the aural answer-in-English half-marks rule, the Spanish-only opinion item, the literature discuss-don’t-quote rule, the Q5 Content and Language band scales, the note-vs-letter development contrast, front-loaded and graded partial credit, the Q2 correct-tense gate, and the answer-both-only-higher-scores rule — are the real SEC marking grammar and apply at both Higher and Ordinary level. Most are cited to the 2025 Higher Level scheme; the standing rules worded verbatim only in the earlier filed schemes are cited to the year where the quoted line actually appears (the Q5 band scales, the Q2 correct-tense gate and the answer-both rule to 2024; the literature discuss-don’t-quote rule and the note-vs-letter contrast to 2023, both with verified pages). The oral session (Sp5) teaches the syllabus-defined weighting, format and assessment criteria of the Speaking component (SEC does not publish a per-band oral grid, so no internal cut-points are asserted). Level-specific worked examples are being added.',
};
