/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — LCVP Link Modules (Written Paper) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the point+expansion notation, the (0/2) all-or-nothing
 * items, the no-repetition rule on the 9-mark closers, and the apply-to-the-
 * case requirement) is the real SEC system, cited to:
 *  - SEC LCVP Link Modules Written Paper marking scheme 2024 (Common Level) —
 *    examiner-reports/lcvp/2024-marking-scheme.*
 * LCVP is examined at a single common level.
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC LCVP Link Modules marking scheme 2024, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── LC1 · The (0/2) cliff-edge ───────────────

const LC1: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-cliff',
  subject: 'lcvp',
  level: 'common',
  title: 'The all-or-nothing point',
  cue: 'Audio Visual',
  question: 'Two questions look identical — each “state a point” worth 2 marks. But one is marked (1+1) and the other (0/2), flagged “expansion needed”. A candidate writes a bare, undeveloped point for both. What does the (0/2) one score?',
  questionNote:
    'Scenario authored for this exercise. LCVP marks points either (1+1) — point 1 + expansion 1, partial credit available — or (0/2), all-or-nothing where an undeveloped point scores 0. The notation is the instruction.',
  scale: {
    name: '(0/2) item',
    levels: two(0, 2),
    notes: [
      'On a (1+1) item, a bare point still banks the 1 for the point.',
      'On a (0/2) item, there is no half credit — “expansion needed”.',
      'So an undeveloped point on a (0/2) item scores 0, not 1.',
    ],
    cite: MS('p.2 ((0/2) all-or-nothing items)'),
  },
  scripts: [
    {
      id: 'lc1-a',
      label: 'The answer',
      persona: 'Bare point, no expansion',
      work: ['States a valid point.', 'No expansion — on a (0/2) item flagged “expansion needed”.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — on a (0/2) item there’s no credit for the point alone; you only score by developing it. The identical-looking (1+1) item next to it would have given 1 for the same bare point. The habit that protects you everywhere: always add the “because…” expansion to a point.',
      embodies: {
        behaviour: 'Leaves a (0/2) point undeveloped, where there is no partial credit.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-lcvp1',
    rule: 'Always expand the point — some items give nothing without it.',
    detail:
      'LCVP marks some points (0/2): an undeveloped point scores 0, not a consolation 1. Add the “because…” expansion to every point and you’re safe whichever notation applies.',
    cite: MS('p.2'),
  },
};

// ─────────────── LC2 · No repetition on the 9-markers ───────────────

const LC2: GridSession = {
  mode: 'grid',
  id: 'lcvp-repetition',
  subject: 'lcvp',
  level: 'common',
  title: 'Three points, three ideas',
  cue: 'Explain three',
  question: 'A 9-mark closing question asks you to “explain three” things, marked 3 × (1+1+1), with the rule “no repetition of points/expansions”. A candidate gives one good idea, then two reworded versions of the same idea.',
  questionNote:
    'Scenario authored for this exercise. The 9-mark LCVP closers require three distinct points; the scheme states “no repetition of expansions/points”, so restated ideas earn nothing.',
  grid: {
    perPoint: [{ id: 'point', label: 'Distinct explained point', marks: 3 }],
    shorthand: '3 × 3m · no repetition',
    ruleNote:
      'Each of the three must be a different idea. The scheme forbids repetition, so a reworded restatement of a point already made scores nothing — you need three genuinely distinct explanations.',
    cite: MS('p.6, p.14 (no repetition on 9-markers)'),
  },
  scripts: [
    {
      id: 'lc2-a',
      label: 'The answer',
      persona: 'One idea, three ways',
      attempts: [
        {
          id: 'lc2-a-1',
          text: 'Point 1 — a genuine, well-explained idea.',
          key: { point: 3 },
          keyNote: 'The first idea, explained. 3 marks.',
        },
        {
          id: 'lc2-a-2',
          text: 'Point 2 — the same idea, reworded.',
          key: { point: 0 },
          keyNote: 'A restatement of point 1 — “no repetition” means it scores 0. A second, different idea was needed.',
        },
        {
          id: 'lc2-a-3',
          text: 'Point 3 — the same idea again, in new words.',
          key: { point: 0 },
          keyNote: 'Repetition again, 0. Only 3 of 9 — two-thirds lost to saying one thing three times. Three distinct ideas were the task.',
        },
      ],
      embodies: {
        behaviour: 'Repeats one idea across a “three distinct points” closer, where repetition scores 0.',
        cite: MS('p.6'),
      },
    },
    {
      id: 'lc2-b',
      label: 'The answer',
      persona: 'Three distinct ideas',
      attempts: [
        {
          id: 'lc2-b-1',
          text: 'Point 1 — first idea, explained.',
          key: { point: 3 },
          keyNote: 'Distinct idea, explained. 3.',
        },
        {
          id: 'lc2-b-2',
          text: 'Point 2 — a different idea, explained.',
          key: { point: 3 },
          keyNote: 'A second, genuinely different idea. 3.',
        },
        {
          id: 'lc2-b-3',
          text: 'Point 3 — a third, distinct idea, explained.',
          key: { point: 3 },
          keyNote: 'Three distinct explained ideas. 9/9.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp2',
    rule: 'On “explain three”, give three different ideas.',
    detail:
      'The 9-mark LCVP closers forbid repetition — a reworded restatement of a point already made scores 0. Plan three genuinely distinct points before you write.',
    cite: MS('p.6'),
  },
};

// ─────────────── LC3 · Apply it to the case ───────────────

const LC3: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-apply',
  subject: 'lcvp',
  level: 'common',
  title: 'Answer for this person',
  cue: 'Case Study',
  question: 'A Section B case-study question asks what a named person (Sandra) should do. A candidate writes a textbook-correct general answer — accurate, but never applied to Sandra or her situation. The scheme notes the answer “must be relevant to Sandra”. How does it fare?',
  questionNote:
    'Scenario authored for this exercise. In the Section B case study, credit is gated on relevance to the specific case/person — a generic, unapplied answer can fail even when it’s correct in the abstract.',
  scale: {
    name: 'Case study · applied',
    levels: two(0, 6),
    notes: [
      'The case study issues in advance and names specific people/situations.',
      'The scheme: the answer “must be relevant to Sandra” (the named person).',
      'A correct but generic, unapplied answer can score nothing here.',
    ],
    cite: MS('p.3 (relevance-to-the-case rule)'),
  },
  scripts: [
    {
      id: 'lc3-a',
      label: 'The answer',
      persona: 'Textbook, not applied',
      work: ['An accurate general answer.', 'Never applied to Sandra or her specific situation.'],
      keyLevelId: 'm0',
      keyNote:
        'It can score nothing — the case study rewards applying your knowledge to the named person, not reciting it in general. Tie every point back to Sandra’s situation (“for Sandra, this means…”) to unlock the marks. Application is the whole point of a case study.',
      embodies: {
        behaviour: 'Gives a generic, unapplied answer to a named case study — where credit needs relevance to the person.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-lcvp3',
    rule: 'In the case study, apply it to the named person.',
    detail:
      'Section B credit is gated on relevance to the specific case — a correct but generic answer can score nothing. Tie every point back to the named person and their situation.',
    cite: MS('p.3'),
  },
};

// ─────────────── LC4 · The compulsory item & the format mark ───────────────

const LC4: GridSession = {
  mode: 'grid',
  id: 'lcvp-compulsory',
  subject: 'lcvp',
  level: 'common',
  title: 'The compulsory item',
  cue: 'Prepare an agenda',
  question:
    'A Section C question worth 6 marks says “Prepare the agenda for the first meeting.” The scheme marks it: heading “AGENDA” = 1 mark, then 5 valid agenda items at 1 mark each — with the very first item, “Election of Officers”, flagged with an asterisk as a compulsory point. A candidate writes the heading and five perfectly valid items, but not Election of Officers. Full marks?',
  questionNote:
    'Scenario authored for this exercise. The mark split (heading 1m + 5 items 5@1m) and the asterisked “compulsory point” are the real SEC template — some structured-format questions reserve a mark for one named item, and a separate mark for the required heading.',
  grid: {
    perPoint: [
      { id: 'heading', label: 'AGENDA heading (format mark)', marks: 1 },
      { id: 'compulsory', label: 'Election of Officers (compulsory item)', marks: 1 },
      { id: 'others', label: 'Four other valid agenda items', marks: 4 },
    ],
    shorthand: 'Heading 1m + 5 items 5@1m · one item compulsory',
    ruleNote:
      'Two marks here are not “any valid point”. One is a format mark for writing the heading “AGENDA”. Another is reserved for the specific compulsory item the scheme asterisks (Election of Officers) — an extra valid item cannot substitute for it. You score that mark only by naming the exact required item.',
    cite: MS('p.8 (AGENDA: heading 1m, 5 items 5@1m, Election of Officers compulsory)'),
  },
  scripts: [
    {
      id: 'lc4-a',
      label: 'The answer',
      persona: 'Five valid items — but not the required one',
      attempts: [
        {
          id: 'lc4-a-1',
          text: 'Writes the heading “AGENDA”, then five valid items: Resources, Finance, Action steps, Date of the visit, and AOB. No “Election of Officers”.',
          key: { heading: 1, compulsory: 0, others: 4 },
          keyNote:
            '5/6. The heading banks its format mark, and four of the items are valid “other” points. But the fifth item mark is reserved for the compulsory point — Election of Officers — which the scheme asterisks. A sixth valid item can’t buy it back; you only earn that mark by naming the required item itself.',
        },
      ],
      embodies: {
        behaviour: 'Substitutes an extra valid agenda item for the point the scheme marks compulsory (asterisked).',
        cite: MS('p.8'),
      },
    },
    {
      id: 'lc4-b',
      label: 'The answer',
      persona: 'Leads with the compulsory item',
      attempts: [
        {
          id: 'lc4-b-1',
          text: 'Writes the heading “AGENDA”, opens with Election of Officers, then Resources, Finance, Action steps and AOB.',
          key: { heading: 1, compulsory: 1, others: 4 },
          keyNote:
            '6/6. The heading (1), the compulsory Election of Officers item (1), and four other valid items (4). Getting the format and the required item both banks every mark on offer.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp4',
    rule: 'Write the required heading, and the compulsory item.',
    detail:
      'Structured-format LCVP questions reserve marks for a named heading (a format mark) and for specific compulsory, asterisked points. An extra valid item never substitutes for the compulsory one — include the exact item, and write the heading, to bank those marks.',
    cite: MS('p.8'),
  },
};

export const LCVP_CHAIR: ChairSubject = {
  id: 'lcvp',
  label: 'LCVP Link Modules',
  tagline: 'Expand every point, three distinct ideas, apply it to the case, give the compulsory item.',
  offeredLevels: ['common'],
  sessions: [LC1, LC2, LC3, LC4],
  sources: [
    { label: 'SEC LCVP Link Modules Written Paper marking scheme 2024, Common Level (examiner-reports/lcvp/2024-marking-scheme)' },
  ],
  coverageNote:
    'LCVP Link Modules is examined at a single common level. These sessions teach the written-paper conventions — point+expansion notation, the (0/2) items, the no-repetition rule, the apply-to-the-case requirement and the compulsory-item/format marks — verified against the 2024 scheme. The portfolio (60% of the grade) is coursework and not covered here.',
};
