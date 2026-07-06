/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Home Economics (S&S, Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the coarse 5:3:0 point ladder that pays nothing for a thin
 * point, the per-heading distribution rule, and the low all-or-nothing "name"
 * mark) is the real SEC system, cited to:
 *  - SEC LC Home Economics HL marking scheme 2025 —
 *    examiner-reports/home-economics/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Home Economics HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Home Economics OL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── HE1 · The 5:3:0 ladder ───────────────

const HE1: ScaleSession = {
  mode: 'scale',
  id: 'he-coarse-ladder',
  subject: 'home-economics',
  level: 'higher',
  title: 'Half a point scores nothing',
  cue: 'Discuss',
  question: 'A 20-mark “Discuss” part is marked as points on a 5:3:0 ladder — a well-developed point earns 5, a partial one earns 3, and a thin/undeveloped point earns 0. The candidate writes a correct but one-line, undeveloped point. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Many 20-mark Home Economics parts use a coarse 5:3:0 ladder — there is no 1 or 2 for a thin point; it is develop-it-or-score-nothing.',
  scale: {
    name: 'Point · 5:3:0 ladder',
    levels: ladder([0, 3, 5]),
    notes: [
      'This part marks each point 5 : 3 : 0 — no 1s or 2s.',
      '5 = a well-developed point; 3 = partially developed; 0 = a thin, undeveloped point.',
      'A correct but one-line point falls to 0 — there is no consolation mark.',
    ],
    cite: MS('p.13, p.16 (5:3:0 ladders on 20-mark parts)'),
  },
  scripts: [
    {
      id: 'he1-a',
      label: 'The answer',
      persona: 'Correct — but one line',
      work: ['A correct point, stated in a single undeveloped line.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the 5:3:0 ladder gives nothing for a thin point, and a bare correct statement is a thin point. One extra sentence of development (why it matters, an example) would jump it to 3 or 5. On these questions, a few developed points beat a long list of one-liners every time.',
      embodies: {
        behaviour: 'Writes correct but undeveloped one-line points, which the 5:3:0 ladder scores 0.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he1',
    rule: 'Develop the point, or it scores nothing.',
    detail:
      'Home Economics’ big “Discuss/Analyse” parts use a 5:3:0 ladder — a thin, one-line point earns 0, not a consolation mark. Develop each point (say why, give an example); a few developed points beat many bullet-listed ones.',
    cite: MS('p.13'),
  },
};

// ─────────────── HE2 · Spread across the headings ───────────────

const HE2: GridSession = {
  mode: 'grid',
  id: 'he-headings',
  subject: 'home-economics',
  level: 'higher',
  title: 'Spread across the headings',
  cue: 'Discuss (structured)',
  question: 'A part asks for points on food safety and requires: 1 point on storage, 1 on cooking/reheating, and 2 “other” points. A candidate writes four excellent points — but all four are about storage.',
  questionNote:
    'Scenario authored for this exercise. Structured Home Economics parts require points spread across named headings before free “other” points unlock; each named heading is capped independently.',
  grid: {
    perPoint: [
      { id: 'storage', label: 'Storage point', marks: 5 },
      { id: 'cooking', label: 'Cooking / reheating point', marks: 5 },
      { id: 'other1', label: '“Other” point', marks: 5 },
      { id: 'other2', label: '“Other” point', marks: 5 },
    ],
    shorthand: '1 storage, 1 cooking, 2 others',
    ruleNote:
      'The named headings are capped independently: only one storage point can score, no matter how many you write. Extra storage points don’t roll over to fill the cooking or “other” slots — those marks are simply lost.',
    cite: MS('p.16 (per-heading distribution rule)'),
  },
  scripts: [
    {
      id: 'he2-a',
      label: 'The answer',
      persona: 'Four points, all storage',
      attempts: [
        {
          id: 'he2-a-1',
          text: 'Four excellent, well-developed points — every one about safe storage of food.',
          key: { storage: 5, cooking: 0, other1: 0, other2: 0 },
          keyNote: 'Only the first storage point scores — the storage heading is capped at one, and the other three excellent points have nowhere to land. 5 of 20. Spreading them (one storage, one cooking, two others) would have scored all 20 for the same effort.',
        },
      ],
      embodies: {
        behaviour: 'Loads all points under one heading, forfeiting the independently-capped other headings.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he2',
    rule: 'Put a point under every named heading first.',
    detail:
      'Structured Home Economics parts cap each named heading independently — four points under one heading score once. Cover every heading the question names before adding “other” points, or the surplus marks are lost.',
    cite: MS('p.16'),
  },
};

// ─────────────── HE3 · Naming is cheap ───────────────

const HE3: GridSession = {
  mode: 'grid',
  id: 'he-name-describe',
  subject: 'home-economics',
  level: 'higher',
  title: 'The marks are in the describing',
  cue: 'Name and describe',
  question: 'A “Name and describe one method of heat transfer” part gives 2 marks for the name and 4 for the description. The candidate names conduction correctly, then writes only “it transfers heat”.',
  questionNote:
    'Scenario authored for this exercise. In Home Economics “name and describe/evaluate” parts, the name is a low, often all-or-nothing mark; the description or evaluation carries the marks.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the method', marks: 2 },
      { id: 'describe', label: 'Describe it (developed)', marks: 4 },
    ],
    shorthand: 'name 2 + describe 4',
    ruleNote:
      'Naming is the cheap part — 2 marks, and often all-or-nothing. The description carries most of the marks, and a vague one-liner earns little of it. Where a question says “describe” or “evaluate”, that is where the marks live.',
    cite: MS('p.8 (name + describe split)'),
  },
  scripts: [
    {
      id: 'he3-a',
      label: 'Script A',
      persona: 'Names it, barely describes',
      attempts: [
        {
          id: 'he3-a-1',
          text: 'Conduction. It transfers heat.',
          key: { name: 2, describe: 0 },
          keyNote: 'The name earns its 2, but “it transfers heat” describes nothing specific — the 4 description marks, where the question’s value sits, are untouched. 2 of 6. A sentence about heat passing through direct contact between particles would earn them.',
        },
      ],
      embodies: {
        behaviour: 'Nails the cheap “name” mark but leaves the description — where the marks are — undeveloped.',
        cite: MS('p.8'),
      },
    },
    {
      id: 'he3-b',
      label: 'Script B',
      persona: 'Names and describes',
      attempts: [
        {
          id: 'he3-b-1',
          text: 'Conduction: heat passes directly through a material by contact between particles — e.g. a metal saucepan base heating on a hob.',
          key: { name: 2, describe: 4 },
          keyNote: 'Name (2) plus a specific, developed description with an example (4). Full 6 — the description is what turned a 2 into a 6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-he3',
    rule: 'The marks are in the describing, not the naming.',
    detail:
      'In Home Economics “name and describe/evaluate” questions, the name is a small, often all-or-nothing mark; the real marks are in a developed description or evaluation. Spend your words there, not on the label.',
    cite: MS('p.8'),
  },
};

// ─────────────── HE4 · OL — never leave Section A blank ───────────────

const HE4: ScaleSession = {
  mode: 'scale',
  id: 'he-ol-section-a',
  subject: 'home-economics',
  level: 'ordinary',
  title: 'Guess it — never leave it blank',
  cue: 'Section A (OL)',
  question: 'An Ordinary Level Section A item (a true/false tick, or fill-the-blank) is marked all-or-nothing: 2 marks or 0, with no partial credit. A candidate isn’t sure of the answer and leaves it blank rather than guess. What’s the expected cost of leaving it blank versus guessing?',
  questionNote:
    'Scenario authored for this exercise. OL Section A items are graded 2:0 (all-or-nothing). Because a blank and a wrong guess both score 0, guessing on an unknown item is pure upside.',
  scale: {
    name: 'OL Section A · 2:0',
    levels: [
      { id: 'm0', label: '0 (blank or wrong)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (correct)', annotation: '2', marks: 2 },
    ],
    notes: [
      'OL Section A items score 2:0 — all-or-nothing, no partial credit.',
      'A blank scores 0. A wrong guess also scores 0. There is no penalty for a wrong answer.',
      'So on a true/false or fill-the-blank you don’t know, a guess can only help.',
    ],
    cite: MSOL('p.6–7 (Section A, graded 2:0)'),
  },
  scripts: [
    {
      id: 'he4-a',
      label: 'The decision',
      persona: 'Leaves it blank',
      work: ['Unsure of the answer.', 'Leaves the true/false item blank rather than guess.'],
      keyLevelId: 'm0',
      keyNote:
        'A guaranteed 0 — when a 50/50 guess would have scored 2 half the time for no downside. Section A is graded 2:0 with no penalty for a wrong answer, so leaving an item blank throws away free expected marks. Always put something down: on a true/false you can’t lose by guessing.',
      embodies: {
        behaviour: 'Leaves an all-or-nothing Section A item blank instead of guessing — forfeiting free expected marks.',
        cite: MSOL('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he4',
    rule: 'On OL Section A, always guess — never leave it blank.',
    detail:
      'Ordinary Level Section A items are graded 2:0 with no penalty for a wrong answer. A blank and a wrong guess both score 0, so guessing on a true/false or fill-the-blank you’re unsure of is pure upside. Never leave one blank.',
    cite: MSOL('p.6'),
  },
};

export const HOME_ECONOMICS_CHAIR: ChairSubject = {
  id: 'home-economics',
  label: 'Home Economics',
  tagline: 'Develop your points, spread the headings, describe don’t just name.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [HE1, HE2, HE3, HE4],
  sources: [
    { label: 'SEC LC Home Economics HL marking scheme 2025 (examiner-reports/home-economics/2025-marking-scheme)' },
    { label: 'SEC LC Home Economics OL marking scheme 2025 (examiner-reports/home-economics/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The point-ladder, per-heading and name-vs-describe sessions apply at both levels (OL ladders are even coarser — a half point often scores 0). The Ordinary session captures OL’s all-or-nothing Section A. Verified against the 2025 OL scheme.',
};
