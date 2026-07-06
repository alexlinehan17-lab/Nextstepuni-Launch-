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
 *  - SEC LCVP Link Modules Written Paper marking scheme 2023 (Common Level) —
 *    examiner-reports/lcvp/2023-marking-scheme.* (the balance, itemised-slice,
 *    single-point-two-expansions, no-marks-for-headings, off-list and
 *    contradiction rules).
 * LCVP is examined at a single common level.
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC LCVP Link Modules marking scheme 2024, ${p}` });
const MS23 = (p: string) => ({ label: `SEC LCVP Link Modules marking scheme 2023, ${p}` });

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

// ─────────────── LC8 · No marks for headings (marketing mix) ───────────────

const LC8: GridSession = {
  mode: 'grid',
  id: 'lcvp-headings',
  subject: 'lcvp',
  level: 'common',
  title: 'Headings score nothing',
  cue: 'Apply the marketing mix',
  question:
    'A Section C question worth 8 marks says “Apply the marketing mix (Product, Price, Promotion, Place) to a business you are familiar with,” marked “4 P’s named and applied, 4 × 2m (1+1)” with the note “No marks for headings — 2 valid applications for each of the 4 Ps.” A candidate lays out a tidy answer: four bold headings — PRODUCT, PRICE, PROMOTION, PLACE — with nothing underneath. What does the structure earn?',
  questionNote:
    'Scenario authored for this exercise. The marketing-mix grid (4 P’s named and applied, 4 × 2m (1+1), “No marks for headings”, two applications per P) is the real SEC template — every mark is for applying an element, never for the heading that labels it.',
  grid: {
    perPoint: [
      { id: 'app1', label: 'First valid application of this P', marks: 1 },
      { id: 'app2', label: 'Second valid application of this P', marks: 1 },
    ],
    shorthand: '4 P’s 4@2m (1+1) · no marks for headings',
    ruleNote:
      'Each P is worth 2 marks — but only for applying it to the business, never for the heading. The scheme states “No marks for headings”: writing PRODUCT / PRICE / PROMOTION / PLACE earns nothing on its own. The two marks per P come from two valid applications (e.g. for Price: a stated price strategy, plus why it suits the market).',
    cite: MS23('p.15 (4 P’s named and applied, 4×2m (1+1), “No marks for headings”); p.7 (Section B “No marks for headings”)'),
  },
  scripts: [
    {
      id: 'lc8-a',
      label: 'The answer',
      persona: 'Neat headings, empty underneath',
      attempts: [
        {
          id: 'lc8-a-1',
          text: 'PRODUCT',
          key: { app1: 0, app2: 0 },
          keyNote:
            'The heading alone scores 0 — the scheme gives “No marks for headings.” Naming the P is not applying it. Two applications of Product to the business were needed (e.g. its USP, its packaging).',
        },
        {
          id: 'lc8-a-2',
          text: 'PRICE',
          key: { app1: 0, app2: 0 },
          keyNote:
            '0 again. The label “Price” tells the examiner nothing about your business. Two applications were needed — a price strategy, and why it fits the market.',
        },
        {
          id: 'lc8-a-3',
          text: 'PROMOTION',
          key: { app1: 0, app2: 0 },
          keyNote:
            '0. A heading is scaffolding, not an answer. Two promotion methods applied to the business would have banked the 2 marks.',
        },
        {
          id: 'lc8-a-4',
          text: 'PLACE',
          key: { app1: 0, app2: 0 },
          keyNote:
            '0/8 in total. Four perfect headings, no marks — because every mark on this question is for application, and none for the heading.',
        },
      ],
      embodies: {
        behaviour: 'Writes the required headings but no applied content, on a grid that awards “No marks for headings”.',
        cite: MS23('p.15'),
      },
    },
    {
      id: 'lc8-b',
      label: 'The answer',
      persona: 'Applies every P to the business',
      attempts: [
        {
          id: 'lc8-b-1',
          text: 'Product — “Our runners use recycled soles (USP); sold in minimalist recyclable boxes (packaging).”',
          key: { app1: 1, app2: 1 },
          keyNote: 'Two applications of Product to the actual business. 2/2.',
        },
        {
          id: 'lc8-b-2',
          text: 'Price — “A premium price of €120; set above rivals to signal quality to our target market.”',
          key: { app1: 1, app2: 1 },
          keyNote: 'A price strategy plus a reason it suits the market. 2/2.',
        },
        {
          id: 'lc8-b-3',
          text: 'Promotion — “Influencer posts on Instagram; and sponsorship of a local running club.”',
          key: { app1: 1, app2: 1 },
          keyNote: 'Two promotion methods applied. 2/2.',
        },
        {
          id: 'lc8-b-4',
          text: 'Place — “Sold through our own website; and stocked in two city-centre sports shops.”',
          key: { app1: 1, app2: 1 },
          keyNote: 'Two channels named for this business. 8/8 — the headings were free, the applications did the work.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp8',
    rule: 'Headings are free — write what goes under them.',
    detail:
      'Structured LCVP questions like the marketing mix give “No marks for headings.” The label (Product, Price…) earns nothing; every mark comes from applying it to your business. Spend no time on the heading — spend it on the two applications each mark needs.',
    cite: MS23('p.15'),
  },
};

// ─────────────── LC9 · Both sides, not three of one ───────────────

const LC9: GridSession = {
  mode: 'grid',
  id: 'lcvp-balance',
  subject: 'lcvp',
  level: 'common',
  title: 'One of each, not three of one',
  cue: 'Advantages and disadvantages',
  question:
    'A Section B question asks candidates to “outline the advantages and the disadvantages of remote working,” worth 6 marks, 3 × 2m (1+1). The scheme adds a rule: “Must have one advantage and one disadvantage and one other.” A candidate, strong on the upside, writes three well-developed advantages and no disadvantage. How does it score?',
  questionNote:
    'Scenario authored for this exercise. The balance rule (“Must have one advantage and one disadvantage and one other”) on an advantages-and-disadvantages question is the real SEC template — a mark slot is reserved for each side, so an all-one-sided answer forfeits the other side’s mark.',
  grid: {
    perPoint: [
      { id: 'point', label: 'Valid point', marks: 1 },
      { id: 'develop', label: 'Development', marks: 1 },
    ],
    shorthand: '3@2m (1+1) · one advantage + one disadvantage + one other',
    ruleNote:
      'When the question names both sides, the marks split across them: the scheme requires “one advantage and one disadvantage and one other.” A third advantage cannot fill the disadvantage’s reserved slot — however well developed, an unbalanced point on the missing side scores 0.',
    cite: MS23('p.6 (“Must have one advantage and one disadvantage and one other”, 3×2m (1+1))'),
  },
  scripts: [
    {
      id: 'lc9-a',
      label: 'The answer',
      persona: 'Three advantages, no disadvantage',
      attempts: [
        {
          id: 'lc9-a-1',
          text: 'Advantage — “Less time commuting, because there is no daily journey to the office.”',
          key: { point: 1, develop: 1 },
          keyNote: 'A valid, developed advantage — this fills the required “advantage” slot. 2/2.',
        },
        {
          id: 'lc9-a-2',
          text: 'Advantage — “Better work–life balance, as you can be at home for family.”',
          key: { point: 1, develop: 1 },
          keyNote: 'A second advantage, taken as the free “one other”. 2/2.',
        },
        {
          id: 'lc9-a-3',
          text: 'Advantage — “Cost savings, since you spend nothing on travel or lunches out.”',
          key: { point: 0, develop: 0 },
          keyNote:
            '0 — the third slot was reserved for a disadvantage, and this is a third advantage. The scheme requires one of each; a well-developed point on the wrong side earns nothing. 4/6 — one balanced sentence would have made it 6.',
        },
      ],
      embodies: {
        behaviour: 'Answers an advantages-and-disadvantages question all on one side, where the scheme reserves a mark for the other side.',
        cite: MS23('p.6'),
      },
    },
    {
      id: 'lc9-b',
      label: 'The answer',
      persona: 'One up, one down, one more',
      attempts: [
        {
          id: 'lc9-b-1',
          text: 'Advantage — “Less commuting, so more usable time in the day.”',
          key: { point: 1, develop: 1 },
          keyNote: 'The required advantage. 2/2.',
        },
        {
          id: 'lc9-b-2',
          text: 'Disadvantage — “Isolation, because you lose the informal contact of an office.”',
          key: { point: 1, develop: 1 },
          keyNote: 'The required disadvantage — the slot the all-advantages answer missed. 2/2.',
        },
        {
          id: 'lc9-b-3',
          text: 'Other — “Higher home energy costs, as you power light and heat all day.”',
          key: { point: 1, develop: 1 },
          keyNote: 'A valid third point (another disadvantage is fine as the “one other”). 6/6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp9',
    rule: 'Both sides asked? Give at least one of each.',
    detail:
      'When a question names advantages and disadvantages, the scheme reserves a mark for each side (“one advantage, one disadvantage, one other”). Three points all on one side lose the other side’s mark, no matter how good. Cover both, then add your third freely.',
    cite: MS23('p.6'),
  },
};

// ─────────────── LC10 · One point, developed twice ───────────────

const LC10: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-justify',
  subject: 'lcvp',
  level: 'common',
  title: 'One point, developed twice',
  cue: 'Justify your answer',
  question:
    'A Section B question asks, “Why, in your opinion, was it important for the committee to hold a public meeting? Justify your answer,” worth 3 marks, marked 1 × 3m (1+1+1): “Statement & two expansions.” A candidate gives a correct statement and one sentence of development, then stops. What does it score out of 3?',
  questionNote:
    'Scenario authored for this exercise. The single 3-mark “justify” point marked (1+1+1) — statement plus two expansions — is the real SEC template; here full credit needs the point developed twice, not a second and third separate point.',
  scale: {
    name: 'Justify · 1 point (1+1+1)',
    levels: [
      { id: 'j1', label: '1 mark', annotation: '1', marks: 1 },
      { id: 'j2', label: '2 marks', annotation: '2', marks: 2 },
      { id: 'j3', label: '3 marks', annotation: '3', marks: 3 },
    ],
    notes: [
      'This is one point worth 3, not three points worth 1.',
      'The scheme: “Statement & two expansions” — 1 for the statement, 1 for each of two developments.',
      'A statement with a single expansion is a 2-mark answer; the third mark needs a second, distinct expansion of the same point.',
    ],
    cite: MS23('p.8 (“1 x 3 marks (1+1+1) — Statement & two expansions”)'),
  },
  scripts: [
    {
      id: 'lc10-a',
      label: 'The answer',
      persona: 'Statement plus one line',
      work: [
        'Statement — “It let the committee inform locals of its plans.”',
        'One expansion — “so the community would know the hub existed.”',
        'Stops there.',
      ],
      keyLevelId: 'j2',
      keyNote:
        '2/3. The statement banks 1 and the single expansion banks 1, but this point is marked (1+1+1) — it needs a second, different development of the same idea (e.g. “…and it created awareness, so people were more likely to support and fund it”). On a 3-mark justify, go deeper on the one point; don’t reach for a new one.',
      embodies: {
        behaviour: 'Develops a single 3-mark (1+1+1) point only once, where two expansions are required for full credit.',
        cite: MS23('p.8'),
      },
    },
    {
      id: 'lc10-b',
      label: 'The answer',
      persona: 'Statement developed twice',
      work: [
        'Statement — “It let the committee inform locals of its plans,”',
        'Expansion 1 — “so the community understood what the hub would offer,”',
        'Expansion 2 — “which built ownership and made people more likely to support and fund it.”',
      ],
      keyLevelId: 'j3',
      keyNote:
        '3/3. One point, developed twice — exactly the (1+1+1) shape the scheme wants. Depth on a single idea, not breadth across three.',
    },
  ],
  takeaway: {
    id: 'codex-lcvp10',
    rule: 'A 3-mark point wants two expansions, not two new points.',
    detail:
      'Single “justify/why” points marked (1+1+1) score 1 for the statement and 1 for each of two developments. One line of development caps you at 2 of 3 — add a second, distinct expansion of the same point to bank the third mark.',
    cite: MS23('p.8'),
  },
};

// ─────────────── LC11 · Type, example, advantage ───────────────

const LC11: GridSession = {
  mode: 'grid',
  id: 'lcvp-components',
  subject: 'lcvp',
  level: 'common',
  title: 'Type, example, advantage',
  cue: 'Give an example of each',
  question:
    'A Section B question asks candidates to “identify two different types of research, give an example of each, and give an advantage of each,” worth 6 marks, 2 × 3m (1+1+1): “1m for type, 1m for example, 1m for advantage.” A candidate names two research methods with a good example for each — but both are primary methods, and neither has an advantage. How does it fare?',
  questionNote:
    'Scenario authored for this exercise. The itemised three-part point (1m for type + 1m for example + 1m for advantage) and the “two different types” requirement are the real SEC template — each named component carries its own mark, and the two types must be genuinely different (e.g. primary and secondary).',
  grid: {
    perPoint: [
      { id: 'type', label: 'A different research type', marks: 1 },
      { id: 'example', label: 'An example of it', marks: 1 },
      { id: 'advantage', label: 'An advantage of it', marks: 1 },
    ],
    shorthand: '2@3m (1+1+1) · type + example + advantage',
    ruleNote:
      'Each point breaks into three separately-marked slices: the type (1), an example (1), an advantage (1). Miss one slice and you lose that mark. And the two types must be different — a second method of the same kind (two primary methods) forfeits the “type” mark on the second point.',
    cite: MS23('p.7 (“2 x 3 mark (1+1+1) — 1m for type, 1m for example, 1m for advantage”, two different types)'),
  },
  scripts: [
    {
      id: 'lc11-a',
      label: 'The answer',
      persona: 'Two of the same type, no advantages',
      attempts: [
        {
          id: 'lc11-a-1',
          text: 'Primary research — example: a customer survey.',
          key: { type: 1, example: 1, advantage: 0 },
          keyNote: 'Type (1) and example (1), but no advantage given (0). 2/3 — the advantage was a free mark left on the table.',
        },
        {
          id: 'lc11-a-2',
          text: 'Primary research again — example: face-to-face interviews.',
          key: { type: 0, example: 1, advantage: 0 },
          keyNote:
            'The example scores (1), but the type mark is gone — the scheme wants two different types, and this is a second primary method. No advantage either. 1/3. Total 3/6.',
        },
      ],
      embodies: {
        behaviour: 'Repeats one research type and omits the advantage, on a grid that marks type, example and advantage separately and requires two different types.',
        cite: MS23('p.7'),
      },
    },
    {
      id: 'lc11-b',
      label: 'The answer',
      persona: 'Two different types, all three slices',
      attempts: [
        {
          id: 'lc11-b-1',
          text: 'Primary research — example: a survey — advantage: gives up-to-date, first-hand data specific to the committee’s needs.',
          key: { type: 1, example: 1, advantage: 1 },
          keyNote: 'Type, example and advantage all present. 3/3.',
        },
        {
          id: 'lc11-b-2',
          text: 'Secondary research — example: census data — advantage: cheap and quick, as it already exists.',
          key: { type: 1, example: 1, advantage: 1 },
          keyNote: 'A genuinely different type, with its own example and advantage. 6/6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp11',
    rule: 'When the mark is itemised, supply every item.',
    detail:
      'Some LCVP points are marked in named slices — “1m for type, 1m for example, 1m for advantage.” Each missing slice is a lost mark, and “two different types” means the second must be a genuinely different category. Read the breakdown and answer every part.',
    cite: MS23('p.7'),
  },
};

// ─────────────── LC12 · Stay on the one aspect ───────────────

const LC12: GridSession = {
  mode: 'grid',
  id: 'lcvp-oneaspect',
  subject: 'lcvp',
  level: 'common',
  title: 'Stay on the one aspect',
  cue: 'Design three questions',
  question:
    'Having named “employment” as an aspect of the local area in part (a), a candidate is asked to “design three suitable questions for a questionnaire investigating an aspect mentioned in (a),” worth 6 marks, 3 × 2m (0/2). The scheme adds: “No repetition of questions; need to be specific to the one aspect only.” The candidate writes one sharp employment question, then one about transport and one about local shops. How does it score?',
  questionNote:
    'Scenario authored for this exercise. The questionnaire grid — 3 × 2m (0/2), “No repetition of questions; need to be specific to the one aspect only” — is the real SEC template: all three questions must probe the single aspect chosen in (a), and each is all-or-nothing.',
  grid: {
    perPoint: [{ id: 'q', label: 'On-aspect, usable question', marks: 2 }],
    shorthand: '3@2m (0/2) · specific to the one aspect only',
    ruleNote:
      'Every one of the three questions must investigate the single aspect you named in (a) — the scheme says “specific to the one aspect only.” A question about a different aspect scores 0, and since each is (0/2) there is no half credit. Wandering onto other aspects (or repeating a question) throws marks away.',
    cite: MS('p.9 (“No repetition of questions; need to be specific to the one aspect only”, 3@2m (0/2))'),
  },
  scripts: [
    {
      id: 'lc12-a',
      label: 'The answer',
      persona: 'Drifts off the chosen aspect',
      attempts: [
        {
          id: 'lc12-a-1',
          text: '“What is the main type of employment in this area?” — on employment, the chosen aspect.',
          key: { q: 2 },
          keyNote: 'A usable question about the named aspect. 2/2.',
        },
        {
          id: 'lc12-a-2',
          text: '“How would you rate public transport here?” — about transport, a different aspect.',
          key: { q: 0 },
          keyNote:
            '0 — the scheme requires all three to be “specific to the one aspect only,” and this is about transport, not employment. It is (0/2), so no partial credit.',
        },
        {
          id: 'lc12-a-3',
          text: '“Are there enough local shops?” — about retail, a different aspect again.',
          key: { q: 0 },
          keyNote: '0 — off the aspect once more. 2/6, when three employment questions would have scored 6.',
        },
      ],
      embodies: {
        behaviour: 'Spreads questionnaire items across several aspects, where the scheme requires all three to stay on the one chosen aspect.',
        cite: MS('p.9'),
      },
    },
    {
      id: 'lc12-b',
      label: 'The answer',
      persona: 'Three questions, all on employment',
      attempts: [
        {
          id: 'lc12-b-1',
          text: '“What is the main type of employment in this area?”',
          key: { q: 2 },
          keyNote: 'On-aspect and usable. 2/2.',
        },
        {
          id: 'lc12-b-2',
          text: '“Is it easy to find full-time work locally?”',
          key: { q: 2 },
          keyNote: 'A different question, still on employment. 2/2.',
        },
        {
          id: 'lc12-b-3',
          text: '“Do most people commute out of the area for work?”',
          key: { q: 2 },
          keyNote: 'A third distinct employment question. 6/6 — all specific to the one aspect.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-lcvp12',
    rule: 'Design all three questions around the one aspect.',
    detail:
      'The questionnaire task is (0/2) and must stay “specific to the one aspect only” — every question probes the single aspect you named in (a). Questions on other aspects score nothing, with no half credit. Pick one aspect and drill into it three ways.',
    cite: MS('p.9'),
  },
};

// ─────────────── LC13 · A definition worth four marks ───────────────

const LC13: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-defineterm',
  subject: 'lcvp',
  level: 'common',
  title: 'A definition worth four marks',
  cue: 'Explain the term',
  question:
    'A Section C question says “Explain what is meant by ‘an inclusive workplace’,” worth 4 marks, marked 4 @ 1m — the scheme reads it as one point plus three expansions (“Mix of people (1m) + 3 expansions (3@1m)”). A candidate writes one tidy sentence: “An inclusive workplace is one where everyone feels welcome.” What does a single clean definition score out of 4?',
  questionNote:
    'Scenario authored for this exercise. The “explain the term” question marked 4 @ 1m — one point plus three creditable expansions (the 2023 scheme phrases the CSR version as “4 statements at 1 mark each”) — is the real SEC template: a 4-mark definition is scored as four separate creditable elements, not one sentence.',
  scale: {
    name: 'Explain the term · 4 @ 1m',
    levels: [
      { id: 't1', label: '1 mark', annotation: '1', marks: 1 },
      { id: 't2', label: '2 marks', annotation: '2', marks: 2 },
      { id: 't3', label: '3 marks', annotation: '3', marks: 3 },
      { id: 't4', label: '4 marks', annotation: '4', marks: 4 },
    ],
    notes: [
      'A 4-mark “explain the term” is marked 4 @ 1m — four separately creditable statements.',
      'The scheme reads it as one point (“mix of people”) plus three expansions.',
      'A single tidy sentence usually banks one or two of the four; the rest need spelling out.',
    ],
    cite: MS('p.14 (“4 marks 4@1m — Mix of people (1m) + 3 expansions (3@1m)”); 2023 scheme p.20 (“4 statements at 1 mark each”)'),
  },
  scripts: [
    {
      id: 'lc13-a',
      label: 'The answer',
      persona: 'One neat sentence',
      work: [
        '“An inclusive workplace is one where everyone feels welcome and can be themselves.”',
        'Stops there — one polished definition.',
      ],
      keyLevelId: 't2',
      keyNote:
        'About 2/4. The sentence carries a couple of creditable ideas (a mix of people; everyone feeling welcome), but the question is worth 4 @ 1m — it wants four elements. Spell out the rest: not discriminated against on grounds of age/gender/disability; everyone respected and equal; differences acknowledged. Each is a separate mark.',
      embodies: {
        behaviour: 'Answers a 4 @ 1m “explain the term” with a single sentence, where four separate creditable statements are marked.',
        cite: MS('p.14'),
      },
    },
    {
      id: 'lc13-b',
      label: 'The answer',
      persona: 'Four creditable elements',
      work: [
        'Point — “An inclusive workplace has a mix of people of all backgrounds and identities.”',
        'Expansion 1 — “No one is discriminated against on grounds such as age, gender or disability.”',
        'Expansion 2 — “Everyone is treated equally and with respect.”',
        'Expansion 3 — “Differences are acknowledged and people can be themselves.”',
      ],
      keyLevelId: 't4',
      keyNote:
        '4/4. One point plus three developments — exactly the four creditable statements the 4 @ 1m marking wants. Treat a 4-mark definition as four short points, not one sentence.',
    },
  ],
  takeaway: {
    id: 'codex-lcvp13',
    rule: 'A 4-mark definition is four points, not one sentence.',
    detail:
      '“Explain the term…” for 4 marks is marked 4 @ 1m — one point plus three expansions, or four creditable statements. A single tidy sentence banks only one or two. Break the definition into the number of marks on offer.',
    cite: MS('p.14'),
  },
};

// ─────────────── LC14 · Off the model list still counts ───────────────

const LC14: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-notexhaustive',
  subject: 'lcvp',
  level: 'common',
  title: 'Your own valid point counts',
  cue: 'Off the model list',
  question:
    'On a “(1+1)” point, a candidate gives a valid, well-developed answer that isn’t written anywhere in the marking scheme’s printed list of model answers. The scheme’s general instructions state the suggestions “are not exhaustive and alternative valid responses etc. are acceptable.” Does an answer that isn’t in the scheme score?',
  questionNote:
    'Scenario authored for this exercise. The SEC general instruction that model answers “are not exhaustive and alternative valid responses etc. are acceptable” is real — marks follow validity and relevance, not a match to the scheme’s wording.',
  scale: {
    name: 'Off-list · valid response',
    levels: two(0, 2),
    notes: [
      'The printed model answers are examples, not a closed list.',
      'The scheme: they “are not exhaustive and alternative valid responses etc. are acceptable.”',
      'A relevant, correctly-used, developed point scores full even if it isn’t in the scheme.',
    ],
    cite: MS23('p.3 (general instructions: model answers “not exhaustive … alternative valid responses … acceptable”)'),
  },
  scripts: [
    {
      id: 'lc14-a',
      label: 'The answer',
      persona: 'A good point that isn’t in the scheme',
      work: [
        'Gives a valid, relevant point not printed in the model answers.',
        'Develops it correctly and in context.',
      ],
      keyLevelId: 'm2',
      keyNote:
        'Full marks — the scheme’s list is “not exhaustive,” and “alternative valid responses are acceptable.” Examiners mark for validity and relevance, not for matching the printed wording. Don’t freeze because your point isn’t the “textbook” one; if it’s correct, in context, and developed, it scores. (The one gate is relevance — see the apply-to-the-case rule.)',
      embodies: {
        behaviour: 'Gives a valid developed point outside the scheme’s model list, which the general instructions accept in full.',
        cite: MS23('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-lcvp14',
    rule: 'Off the model list still scores — if it’s valid and relevant.',
    detail:
      'The scheme’s model answers are “not exhaustive”; “alternative valid responses are acceptable.” A correct, relevant, developed point banks its marks even when it isn’t printed. Write the best true answer, not the one you think the scheme wants.',
    cite: MS23('p.3'),
  },
};

// ─────────────── LC15 · The right word, used wrong ───────────────

const LC15: ScaleSession = {
  mode: 'scale',
  id: 'lcvp-contradiction',
  subject: 'lcvp',
  level: 'common',
  title: 'The right word, used wrong',
  cue: 'Correct use in context',
  question:
    'A candidate names the correct term the question is looking for, but the explanation that follows misuses it — or contradicts it. The scheme’s general instructions say words “must be correctly used in context and not contradicted, and where there is evidence of incorrect use or contradiction, the marks may not be awarded.” Does the right keyword still score?',
  questionNote:
    'Scenario authored for this exercise. The SEC general instruction that a term “must be correctly used in context and not contradicted” — with marks withheld where there is incorrect use or contradiction — is real: a correct keyword can be voided by the explanation around it.',
  scale: {
    name: 'Correct use · not contradicted',
    levels: two(0, 2),
    notes: [
      'A right keyword is not an automatic mark.',
      'The scheme: words “must be correctly used in context and not contradicted.”',
      '“Where there is evidence of incorrect use or contradiction, the marks may not be awarded.”',
    ],
    cite: MS23('p.3 (general instructions: correct use in context, not contradicted, or marks withheld)'),
  },
  scripts: [
    {
      id: 'lc15-a',
      label: 'The answer',
      persona: 'Correct term, self-contradicting explanation',
      work: [
        'Names the correct term the question asks for.',
        'Then explains it in a way that misuses or contradicts it (e.g. defines a “fixed cost” but says it “rises with output”).',
      ],
      keyLevelId: 'm0',
      keyNote:
        'It can score 0 — the scheme withholds marks “where there is evidence of incorrect use or contradiction.” The keyword alone isn’t the mark; the surrounding explanation has to use it correctly and not contradict it. A right term wrapped in a wrong explanation reads as not understood. Make sure your development supports the term, never fights it.',
      embodies: {
        behaviour: 'Pairs a correct term with an explanation that misuses or contradicts it, which the general instructions say may score nothing.',
        cite: MS23('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-lcvp15',
    rule: 'A right term used wrongly scores nothing.',
    detail:
      'The scheme withholds marks where a word is “incorrectly used… or contradicted.” The keyword isn’t an automatic mark — the explanation around it must use it correctly. Check that your development backs up the term rather than contradicting it.',
    cite: MS23('p.3'),
  },
};

export const LCVP_CHAIR: ChairSubject = {
  id: 'lcvp',
  label: 'LCVP Link Modules',
  tagline: 'Read the notation: expand every point, three distinct ideas, apply it to the case, list means list, name your choice, quote the figures, cover both sides, and headings are free.',
  offeredLevels: ['common'],
  sessions: [LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8, LC9, LC10, LC11, LC12, LC13, LC14, LC15],
  sources: [
    { label: 'SEC LCVP Link Modules Written Paper marking scheme 2024, Common Level (examiner-reports/lcvp/2024-marking-scheme)' },
    { label: 'SEC LCVP Link Modules Written Paper marking scheme 2023, Common Level (examiner-reports/lcvp/2023-marking-scheme)' },
  ],
  coverageNote:
    'LCVP Link Modules is examined at a single common level. These sessions teach the written-paper conventions — point+expansion notation, the (0/2) items, the no-repetition rule, the apply-to-the-case requirement, the compulsory-item/format marks, the `@1m` list/recall grid, the recommendation grid’s option mark, the data-table reference rule, the advantages-and-disadvantages balance rule, the single-point (1+1+1) “statement + two expansions” shape, the itemised type/example/advantage slices, the questionnaire’s one-aspect rule, the four-statement definition, the “no marks for headings” rule, the off-list “alternative valid responses” allowance and the correct-use/no-contradiction rule — verified against the 2024 and 2023 schemes. The portfolio (60% of the grade) is coursework and not covered here.',
};
