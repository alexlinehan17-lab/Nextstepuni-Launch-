/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Spanish (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the no-lifting rule on the written essay, the Content-gates-
 * Language rule on Q5, and the verbs-must-be-correct cap on production units)
 * is the real SEC system, cited to:
 *  - SEC LC Spanish HL marking scheme 2025 —
 *    examiner-reports/spanish/2025-marking-scheme.*
 * (The oral is a separate scheme, not covered here.)
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Spanish HL marking scheme 2025, ${p}` });

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

// ─────────────── Sp4 · The aural — one wrong extra cancels a right one ───────────────

const SP4: ScaleSession = {
  mode: 'scale',
  id: 'es-aural-hedge',
  subject: 'spanish',
  level: 'common',
  title: 'Don’t hedge the aural list',
  cue: 'Aural',
  question: 'A listening item asks for one detail. The candidate, unsure, writes two — one right, one wrong — hoping the extra covers them. In the aural vocabulary-list items, a wrong extra answer cancels a correct one. What does it score?',
  questionNote:
    'Scenario authored for this exercise. In the Spanish aural, hedging with an extra wrong answer in a list item cancels a correct one — the same trap as over-answering elsewhere.',
  scale: {
    name: 'Aural item · hedged',
    levels: [
      { id: 'm0', label: '0 (wrong extra cancels)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (single correct)', annotation: '3', marks: 3 },
    ],
    notes: [
      'The item asks for one detail; the candidate offers two.',
      'In the aural list items, a wrong extra answer cancels a correct one.',
      'So the hedge voids the mark you had — commit to one answer.',
    ],
    cite: MS('p.5 (aural: wrong extra cancels a correct answer)'),
  },
  scripts: [
    {
      id: 'sp4-a',
      label: 'The item',
      persona: 'Hedges with a second guess',
      work: ['Heard one detail clearly; unsure, writes it plus a second guess.', 'One is right, the other wrong.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the wrong extra cancels the correct answer, so hedging turned a mark into nothing. The aural list items punish over-answering just like the written paper: write the single answer you’re most sure of. A confident single answer protects the mark a hedge throws away.',
      embodies: {
        behaviour: 'Hedges a single-answer aural item with an extra wrong answer, which cancels the correct one.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-es4',
    rule: 'In the aural, one answer — don’t hedge the list.',
    detail:
      'Spanish aural list items cancel a correct answer with a wrong extra. When an item asks for one detail, write the single answer you’re surest of; a hedged second guess can void the mark.',
    cite: MS('p.5'),
  },
};

export const SPANISH_CHAIR: ChairSubject = {
  id: 'spanish',
  label: 'Spanish',
  tagline: 'No lifting, content-before-language, and the verb gate.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [SP1, SP2, SP3, SP4],
  sources: [
    { label: 'SEC LC Spanish HL marking scheme 2025 (examiner-reports/spanish/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the written-paper conventions — the no-lifting rule, the content-gates-language rule and the verb gate — which apply at both Higher and Ordinary level (the oral is a separate scheme). Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
