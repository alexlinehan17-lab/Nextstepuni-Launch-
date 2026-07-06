/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Italian (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the two Content/Language axes with a graduated content cap,
 * the −50% wrong-language penalty, and the rote-off-the-point rule) is the real
 * SEC system, cited to:
 *  - SEC LC Italian HL marking scheme 2025 —
 *    examiner-reports/italian/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Italian HL marking scheme 2025, ${p}` });

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
  question: 'A comprehension question must be answered in English (it asks for your opinion in English). The candidate answers it well — but in Italian. The scheme applies a 50% deduction for answering in the wrong language. What happens?',
  questionNote:
    'Scenario authored for this exercise. Where the scheme requires an answer in English (e.g. the opinion question), answering in Italian triggers a −50% deduction — far harsher than the −1 for excess material.',
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
      'Italian comprehension sets the answer language per question — answering in Italian where English is required halves your marks. Check the required language on every question before you write.',
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

export const ITALIAN_CHAIR: ChairSubject = {
  id: 'italian',
  label: 'Italian',
  tagline: 'Two axes, the wrong-language penalty, and no rote off the point.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [IT1, IT2, IT3],
  sources: [
    { label: 'SEC LC Italian HL marking scheme 2025 (examiner-reports/italian/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the written-paper conventions — the two Content/Language axes with the graduated content cap, the wrong-language penalty and the rote-off-the-point rule — which apply at both Higher and Ordinary level (the oral is a separate scheme). Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
