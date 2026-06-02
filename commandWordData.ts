/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Command-Word Reflex content.
 *
 * FIRST SLICE: Leaving Cert Business (HL) — the subject where cue-word literacy
 * is the core exam skill. Demands and traps are source-grounded from the LC
 * Business Chief Examiner's Report 2015 and the 2025 marking scheme (see
 * examiner-reports/business/). Stems are faithful, representative LC Business
 * question stems that contain the real cue word; the marks-losing traps are the
 * exact patterns the examiners flag, with page citations.
 *
 * Scales subject-by-subject (the way Exam Reps did). Each cue word teaches a
 * transferable read-the-question skill.
 */

import { type CommandWordQuestion } from './types/commandWord';

export const COMMAND_WORD_QUESTIONS: CommandWordQuestion[] = [
  {
    id: 'biz-illustrate-specific-performance',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Business Law',
    stem: 'Illustrate, using an example, what is meant by ‘specific performance’ as a remedy for breach of contract.',
    commandWord: 'Illustrate',
    demand: 'Explain the term AND give a concrete example. With “Illustrate”, the example is not optional decoration — it earns marks in its own right (the marking grid gives separate marks for the example).',
    trap: 'Many candidates defined the term correctly but gave no example, “thereby losing marks.” The same requirement caught people out in Q3(B) and Q7(C).',
    source: 'LC Business Chief Examiner 2015, p.17',
    marks: 5,
  },
  {
    id: 'biz-list-discrimination-grounds',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Business Law',
    stem: 'List three grounds under which discrimination is prohibited by employment equality legislation.',
    commandWord: 'List',
    demand: 'Just name them — short, separate points. “List” rewards naming only; no explanation is needed or marked.',
    trap: 'Some candidates “wrote paragraphs to explain the protected grounds rather than just naming the grounds, as was required.” That extra writing earns nothing and burns time.',
    source: 'LC Business Chief Examiner 2015, p.17',
    marks: 6,
  },
  {
    id: 'biz-discuss-communication',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Managing',
    stem: 'Discuss the factors a business should consider when communicating with its stakeholders.',
    commandWord: 'Discuss',
    demand: 'Make several DISTINCT developed points (each typically Name + Explain). Range is the thing — different factors, not one idea reworded.',
    trap: '“Disproportionate focus on” one point — repeating variations of a single idea — limits the marks. Discussion questions reward distinct points.',
    source: 'LC Business Chief Examiner 2015, p.17',
    marks: 20,
  },
  {
    id: 'biz-evaluate-management-control',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Managing',
    stem: 'Evaluate the effectiveness of one method of management control used by a business.',
    commandWord: 'Evaluate',
    demand: 'Make a JUDGEMENT and justify it — say how effective it is and why. Evaluation is the most heavily weighted single component (3 of 7 marks in the 2025 grid).',
    trap: 'Candidates often name and explain the control, then stop. “Some evaluations continue to be very superficial and some candidates do not evaluate at all” — the highest-order, highest-mark step is the one most often skipped.',
    source: 'LC Business Chief Examiner 2015, p.17; 2025 marking scheme (B(i) weights evaluation 3/7)',
    marks: 7,
  },
  {
    id: 'biz-outline-entrepreneur-skills',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Enterprise',
    stem: 'Outline the main skills displayed by a successful entrepreneur.',
    commandWord: 'Outline',
    demand: 'Give DEVELOPED points (Name + Explain) — more than a bare list, but examples aren’t required.',
    trap: 'Cues like “outline” and “explain” are “often not addressed adequately.” Treating “Outline” like “List” (just naming) under-develops the answer and loses marks.',
    source: 'LC Business Chief Examiner 2015, p.20',
    marks: 20,
  },
  {
    id: 'biz-explain-utmost-good-faith',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Business in the Economy',
    stem: 'Explain the term ‘utmost good faith’ as a principle of insurance.',
    commandWord: 'Explain',
    demand: 'Give the precise business meaning — the exact technical sense, not a loose everyday paraphrase.',
    trap: 'Weaker answers explained it as “telling the truth” rather than “disclosing all material facts.” “Precision of language is required when explaining business concepts.”',
    source: 'LC Business Chief Examiner 2015, p.19',
    marks: 10,
  },
  {
    id: 'biz-distinguish-ltd-plc',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Business Ownership',
    stem: 'Distinguish between a private limited company and a public limited company as forms of business ownership.',
    commandWord: 'Distinguish',
    demand: 'Bring out the DIFFERENCE(S) — contrast the two directly (e.g. “whereas a private limited company…, a public limited company…”). The contrast is what’s marked.',
    trap: 'Describing each type separately, in isolation, without making the difference explicit, misses the comparison the cue demands.',
    source: 'LC Business Chief Examiner 2015, p.20 (compare/distinguish cues)',
    marks: 10,
  },
  {
    id: 'biz-define-delegation',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Managing',
    stem: 'Define the term ‘delegation’ as used in management.',
    commandWord: 'Define',
    demand: 'Give ONE precise sentence stating exactly what it means. “Define” wants brevity plus accuracy.',
    trap: 'A vague, roundabout or example-led sentence loses the mark — a definition must be tight and technically correct, not a story about it.',
    source: 'LC Business 2025 marking scheme (“Define” = a precise sentence)',
    marks: 5,
  },
  {
    id: 'biz-describe-recruitment',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Managing (HRM)',
    stem: 'Describe the stages a business goes through when recruiting a new employee.',
    commandWord: 'Describe',
    demand: 'Give an account of EACH stage — what happens and in what order. More than naming the stages.',
    trap: 'Just listing the stage names (treating “Describe” like “List”) under-answers it — the marks are in the account of what happens at each.',
    source: 'LC Business Chief Examiner 2015, p.20 (higher-order cues)',
    marks: 15,
  },
  {
    id: 'biz-analyse-exchange-rate',
    subjectId: 'business', subjectLabel: 'Business', level: 'higher',
    questionRef: 'HL · Business in the Economy',
    stem: 'Analyse the impact of a weakening exchange rate on an Irish business that exports to the UK.',
    commandWord: 'Analyse',
    demand: 'Break it down and show the cause-and-effect — explain HOW and WHY the change affects the business, with linked reasoning, not just a list of effects.',
    trap: 'Stating effects without showing the link back to the exporter (the “because… therefore…”) reads as description, and earns fewer marks than developed analysis.',
    source: 'LC Business Chief Examiner 2015, p.20 (higher-order skills)',
    marks: 15,
  },
];

/** Subject ids that currently have command-word content (drives the picker). */
export function commandSubjects(): { subjectId: string; subjectLabel: string; count: number }[] {
  const map = new Map<string, { subjectId: string; subjectLabel: string; count: number }>();
  for (const q of COMMAND_WORD_QUESTIONS) {
    const e = map.get(q.subjectId) ?? { subjectId: q.subjectId, subjectLabel: q.subjectLabel, count: 0 };
    e.count++;
    map.set(q.subjectId, e);
  }
  return [...map.values()];
}

export function questionsForSubject(subjectId: string): CommandWordQuestion[] {
  return COMMAND_WORD_QUESTIONS.filter(q => q.subjectId === subjectId);
}
