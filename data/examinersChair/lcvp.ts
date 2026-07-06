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

// ─────────────── LC5 · List means list (@1m recall grid) ───────────────

const LC5: GridSession = {
  mode: 'grid',
  id: 'lcvp-list',
  subject: 'lcvp',
  level: 'common',
  title: 'When it says “list”, list',
  cue: 'List four',
  question:
    'A Section C question says “List four aspects of your local area,” marked 4 @ 1m — four marks, one per named item, no expansion read. A candidate treats it like an “explain” question, writes two richly-developed items with a paragraph each, and runs out of time before the third and fourth. What does all that development buy?',
  questionNote:
    'Scenario authored for this exercise. The `@1m` list/recall grid is the real SEC template — “List/Name/State four…” questions score one mark per item and read no expansion (e.g. “List four aspects” 4@1m, “List four careers” 4@1m).',
  grid: {
    perPoint: [
      { id: 'item1', label: 'First named item', marks: 1 },
      { id: 'item2', label: 'Second named item', marks: 1 },
      { id: 'item3', label: 'Third named item', marks: 1 },
      { id: 'item4', label: 'Fourth named item', marks: 1 },
    ],
    shorthand: '4 items 4@1m · no expansion read',
    ruleNote:
      'On a `@1m` list, each correct item scores exactly 1 — the mark is for naming it, and no expansion is read or rewarded. Four terse items is full marks; a paragraph on one item still scores only that one mark. The command word “List” (or “Name”/“State”) signals recall, not development.',
    cite: MS('p.9 (List four aspects … 4@1m); p.12 (List four careers … 4@1m)'),
  },
  scripts: [
    {
      id: 'lc5-a',
      label: 'The answer',
      persona: 'Over-develops two, runs out of time',
      attempts: [
        {
          id: 'lc5-a-1',
          text: 'Writes two aspects with a full explanatory paragraph each, then runs out of time before naming a third and fourth.',
          key: { item1: 1, item2: 1, item3: 0, item4: 0 },
          keyNote:
            '2/4. Each of the two aspects earns its single mark for being named — the paragraphs of development earn nothing extra, because a `@1m` list reads only the item. The time spent explaining two cost the two easy marks for simply naming a third and fourth.',
        },
      ],
      embodies: {
        behaviour: 'Writes developed paragraphs on a `@1m` list, where only the named item scores.',
        cite: MS('p.9'),
      },
    },
    {
      id: 'lc5-b',
      label: 'The answer',
      persona: 'Four terse, named items',
      attempts: [
        {
          id: 'lc5-b-1',
          text: 'Names four valid aspects in four short phrases: Employment, Transport, Education, Retail.',
          key: { item1: 1, item2: 1, item3: 1, item4: 1 },
          keyNote:
            '4/4. Four named items, full marks, in a fraction of the time. On a list, breadth beats depth — name the number asked and move on.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp5',
    rule: 'When it says “List”, list — don’t explain.',
    detail:
      'LCVP `@1m` list/recall grids (“List/Name/State four…”) score one mark per named item and read no expansion. Name the exact number asked in short phrases; save the development for the “Explain/Describe” grids that actually pay for it.',
    cite: MS('p.9'),
  },
};

// ─────────────── LC6 · Commit to the choice (recommendation grid) ───────────────

const LC6: GridSession = {
  mode: 'grid',
  id: 'lcvp-recommend',
  subject: 'lcvp',
  level: 'common',
  title: 'Name your recommendation',
  cue: 'Which would you recommend?',
  question:
    'A Section B question asks which option you would recommend for Sandra — sell the business or expand — and to give reasons. It’s marked “Option 1m + 3 valid reasons 3@1m”: one mark is reserved just for stating which option you pick. A candidate writes a balanced answer weighing both sides with three sharp reasons in play, but never actually says which one they recommend. How does it score?',
  questionNote:
    'Scenario authored for this exercise. The recommendation grid (Option 1m + 3 valid reasons 3@1m) is the real SEC template for “which option would you recommend?” questions — one mark for the choice itself, then three for the reasons.',
  grid: {
    perPoint: [
      { id: 'option', label: 'States the recommended option', marks: 1 },
      { id: 'reason1', label: 'First valid reason', marks: 1 },
      { id: 'reason2', label: 'Second valid reason', marks: 1 },
      { id: 'reason3', label: 'Third valid reason', marks: 1 },
    ],
    shorthand: 'Option 1m + 3 reasons 3@1m',
    ruleNote:
      'The first mark is not for a reason — it is for committing to a choice. Naming which option you recommend banks 1 mark on its own; then three valid reasons score 1 each. A fence-sitting answer that analyses both sides but never states a preference forfeits the free option mark, however good the analysis.',
    cite: MS('p.5 (Option 1m + 3 valid reasons 3@1m)'),
  },
  scripts: [
    {
      id: 'lc6-a',
      label: 'The answer',
      persona: 'Weighs both, commits to neither',
      attempts: [
        {
          id: 'lc6-a-1',
          text: 'Weighs selling against expanding with three sharp reasons in play, then closes without ever saying which option is recommended.',
          key: { option: 0, reason1: 1, reason2: 1, reason3: 1 },
          keyNote:
            '3/4. The three reasons land, but the one mark reserved for stating the option is gone — the scheme gives it for committing to a choice, and this answer never does. A single sentence (“I would recommend Sandra expands…”) would have banked it.',
        },
      ],
      embodies: {
        behaviour: 'Analyses both options without stating a recommendation, forfeiting the mark reserved for the choice.',
        cite: MS('p.5'),
      },
    },
    {
      id: 'lc6-b',
      label: 'The answer',
      persona: 'Commits first, then justifies',
      attempts: [
        {
          id: 'lc6-b-1',
          text: 'Opens “I recommend Sandra expands into the department store,” then gives three distinct reasons.',
          key: { option: 1, reason1: 1, reason2: 1, reason3: 1 },
          keyNote:
            '4/4. The choice banks its mark, and three valid reasons complete it. State the recommendation first, then justify.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp6',
    rule: 'On “which would you recommend?”, name your choice — it’s a free mark.',
    detail:
      'The recommendation grid reserves one mark for stating which option you pick, before any reasons. A balanced answer that never commits loses it. Say “I recommend…” outright, then give the three reasons.',
    cite: MS('p.5'),
  },
};

// ─────────────── LC7 · Cite the figures (data-table conclusion) ───────────────

const LC7: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-conclusion',
  subject: 'lcvp',
  level: 'common',
  title: 'Reading a table? Quote a figure',
  cue: 'Conclusion from the table',
  question:
    'A marketing question prints a table of forecast economic-growth figures (9.5% in 2022 falling to 2.3% in 2025) and asks for “one relevant conclusion from the table.” The scheme flags: the conclusion “must include reference to the table — years or %.” A candidate writes a true, sensible conclusion — “the economy is slowing” — but quotes no figure from the table. How does it fare?',
  questionNote:
    'Scenario authored for this exercise. The requirement that a conclusion drawn from a data table reference the table itself (a year or a percentage) is the real SEC instruction on this question type.',
  scale: {
    name: 'Data conclusion · reference the table',
    levels: two(0, 2),
    notes: [
      'The question hands you a data table and asks for a conclusion drawn from it.',
      'The scheme requires the conclusion to “include reference to the table — years or %”.',
      'A true-but-generic statement with no figure quoted can score nothing.',
    ],
    cite: MS('p.6 (conclusion “must include reference to the table – years or %”)'),
  },
  scripts: [
    {
      id: 'lc7-a',
      label: 'The answer',
      persona: 'Right idea, no numbers',
      work: [
        'States a valid conclusion — “the economy is slowing”.',
        'Quotes no year or percentage from the table.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'It can score 0 — the scheme requires the conclusion to reference the table (“years or %”). The idea is correct, but “the economy is slowing” reads as prior knowledge, not a reading of this data. Anchor it to the figures — “growth falls from 9.5% in 2022 to 2.3% in 2025” — and the same insight becomes a valid, evidenced conclusion.',
      embodies: {
        behaviour: 'Draws a conclusion from a data table without quoting any of its figures, where the scheme requires reference to the table.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-lcvp7',
    rule: 'Reading a table? Quote a figure.',
    detail:
      'When a question gives you data and asks for a conclusion, the scheme requires you to reference the table — a year or a percentage. A true-but-generic statement with no figure can score nothing. Name the numbers you’re reasoning from.',
    cite: MS('p.6'),
  },
};

export const LCVP_CHAIR: ChairSubject = {
  id: 'lcvp',
  label: 'LCVP Link Modules',
  tagline: 'Read the notation: expand every point, three distinct ideas, apply it to the case, list means list, name your choice, quote the figures.',
  offeredLevels: ['common'],
  sessions: [LC1, LC2, LC3, LC4, LC5, LC6, LC7],
  sources: [
    { label: 'SEC LCVP Link Modules Written Paper marking scheme 2024, Common Level (examiner-reports/lcvp/2024-marking-scheme)' },
  ],
  coverageNote:
    'LCVP Link Modules is examined at a single common level. These sessions teach the written-paper conventions — point+expansion notation, the (0/2) items, the no-repetition rule, the apply-to-the-case requirement, the compulsory-item/format marks, the `@1m` list/recall grid, the recommendation grid’s option mark and the data-table reference rule — verified against the 2024 scheme. The portfolio (60% of the grade) is coursework and not covered here.',
};
