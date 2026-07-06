/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Accounting (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the per-line workmark system, the discrete "both totals
 * correct" presentation mark, own-figure / transfer marking, the
 * incorrect-sequence penalty, the statement-heading mark, and the General
 * Journal "Being…" narration mark) is the real SEC system, cited to:
 *  - SEC LC Accounting HL marking scheme 2024 —
 *    examiner-reports/accounting/2024-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Accounting HL marking scheme 2024, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Accounting OL marking scheme 2024, ${p}` });

const two = (a: number, b: number): ScaleLevel[] => [
  { id: `m${a}`, label: `${a} marks`, annotation: `${a}`, marks: a },
  { id: `m${b}`, label: `${b} marks`, annotation: `${b}`, marks: b },
];

// ─────────────── Ac1 · The workings are the marks ───────────────

const AC1: GridSession = {
  mode: 'grid',
  id: 'acc-workings',
  subject: 'accounting',
  level: 'higher',
  title: 'Show the working, bank the marks',
  cue: 'Prepare accounts',
  question: 'A Closing Stock figure needs two adjustments before it goes into the accounts. The line is worth 7 marks, awarded through the numbered working (N-note) that derives it. Two candidates each get the final figure slightly wrong.',
  questionNote:
    'Scenario authored for this exercise. Accounting is marked line-by-line (the “workmark” system): each adjusted figure is justified by a numbered working, and the marks live in that working — not in the final figure alone.',
  grid: {
    perPoint: [
      { id: 'base', label: 'Base figure identified', marks: 2 },
      { id: 'adj1', label: 'First adjustment shown', marks: 3 },
      { id: 'adj2', label: 'Second adjustment shown', marks: 2 },
    ],
    shorthand: 'Numbered working · 7m',
    ruleNote:
      'The mark sheet awards each step of the working, not the final number. A bare wrong figure with no working can’t part-score — but a shown working banks every correct step even when the final total is off.',
    cite: MS('p.3, p.5 (workmark system, numbered workings)'),
  },
  scripts: [
    {
      id: 'ac1-a',
      label: 'Script A',
      persona: 'Final figure only',
      attempts: [
        {
          id: 'ac1-a-1',
          text: 'Closing stock: €18,400  (no working shown — and the figure is wrong)',
          key: { base: 0, adj1: 0, adj2: 0 },
          keyNote: 'A wrong figure with nothing behind it. There is no working for the examiner to award, so the line scores 0. In Accounting, a bare answer is all-or-nothing — and here it’s nothing.',
        },
      ],
      embodies: {
        behaviour: 'Writes only the final figure — with no working to part-score when it’s wrong.',
        cite: MS('p.5'),
      },
    },
    {
      id: 'ac1-b',
      label: 'Script B',
      persona: 'Full working, small slip',
      attempts: [
        {
          id: 'ac1-b-1',
          text: 'W: Stock per count €20,000; less goods on sale-or-return €2,000; less damaged stock write-down €600 → but adds instead of subtracting the €600, giving €17,400.',
          key: { base: 2, adj1: 3, adj2: 0 },
          keyNote: 'The base figure and the first adjustment are shown correctly — 5 of 7 banked — even though the second adjustment is mishandled and the final total is wrong. This is exactly why you show every step: the working protects the marks the answer would have lost.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-acc1',
    rule: 'The workings are where the marks live.',
    detail:
      'Accounting is marked line-by-line through the numbered working, not the final figure. Show every adjustment — a shown working banks each correct step even when the total is wrong, while a bare wrong figure scores nothing.',
    cite: MS('p.5'),
  },
};

// ─────────────── Ac2 · Both totals correct* ───────────────

const AC2: ScaleSession = {
  mode: 'scale',
  id: 'acc-balance',
  subject: 'accounting',
  level: 'higher',
  title: 'The mark for balancing',
  cue: 'Balance Sheet',
  question: 'A Balance Sheet carries a discrete mark for both totals agreeing — a presentation mark separate from the line figures. The candidate’s figures are mostly right, but a single misplaced entry means the two totals don’t match. What happens to that presentation mark?',
  questionNote:
    'Scenario authored for this exercise. The Balance Sheet awards a discrete mark for both totals agreeing, separate from the individual line figures (the 2024 scheme flags it with a * annotation; the 2023 scheme marks the same agreeing-totals mark with an examiner arrow — the mark itself is the standing convention).',
  scale: {
    name: 'Both totals correct',
    levels: two(0, 3),
    notes: [
      'The mark for both balance-sheet totals agreeing is its own losable mark, independent of the line entries.',
      'If the two Balance Sheet totals don’t agree, that mark is gone — even if most figures are right.',
      'It rewards a statement that actually balances, not just correct components.',
    ],
    cite: MS('p.4, p.27 (Both totals correct mark)'),
  },
  scripts: [
    {
      id: 'ac2-a',
      label: 'The Balance Sheet',
      persona: 'Doesn’t quite balance',
      work: ['Most figures correct.', 'One misplaced entry → the two totals don’t agree.'],
      keyLevelId: 'm0',
      keyNote:
        'The discrete “both totals correct” mark is lost — it exists precisely to reward a statement that balances, and this one doesn’t. It’s independent of the line marks, so it’s a clean, avoidable loss. Always cross-check that your totals agree before moving on.',
      embodies: {
        behaviour: 'Submits a Balance Sheet whose totals don’t agree — forfeiting the discrete balancing mark.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-acc2',
    rule: 'Balancing is its own mark.',
    detail:
      'The Balance Sheet gives a discrete mark for both totals agreeing, separate from the figures. A single misplaced entry that breaks the balance forfeits it. Check your totals match before you move on — it’s a free, losable mark.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ac3 · Own-figure / transfer discipline ───────────────

const AC3: ScaleSession = {
  mode: 'scale',
  id: 'acc-transfer',
  subject: 'accounting',
  level: 'higher',
  title: 'One error, marked once',
  cue: 'Prepare accounts',
  question: 'A candidate calculates a net profit figure that is wrong (an earlier slip), then transfers that same figure correctly into the next statement. The transfer is worth marks. Does the earlier error cost the transfer marks too?',
  questionNote:
    'Scenario authored for this exercise. Accounting uses own-figure marking: a figure carried forward is penalised once; a correct transfer of the candidate’s own (wrong) figure still earns the transfer marks, while a non-transfer earns half marks.',
  scale: {
    name: 'Transfer of own figure',
    levels: [
      { id: 'm0', label: '0 (no transfer)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (non-transfer, half)', annotation: '2', marks: 2 },
      { id: 'm4', label: '4 (correct transfer)', annotation: '4', marks: 4 },
    ],
    notes: [
      'Own-figure marking: an error is penalised where it happens, once.',
      'Correctly transferring your own (even wrong) figure earns the full transfer marks.',
      'A non-transfer (leaving it out) earns half marks; an incorrect transfer is penalised.',
    ],
    cite: MS('p.18, p.34 (own-figure / transfer rules)'),
  },
  scripts: [
    {
      id: 'ac3-a',
      label: 'The transfer',
      persona: 'Carries the figure correctly',
      work: ['Net profit figure is wrong (earlier slip).', 'That same figure is transferred correctly to the next statement.'],
      keyLevelId: 'm4',
      keyNote:
        'Full transfer marks — the earlier error was already penalised where it happened, and own-figure marking credits a correct transfer of your own number. So don’t stop at a wrong subtotal: carry it through correctly and keep earning. Leaving it out entirely would have scored only half.',
      embodies: {
        behaviour: 'Correctly transfers an own (wrong) figure — earning the transfer marks under own-figure marking.',
        cite: MS('p.34'),
      },
    },
    {
      id: 'ac3-border',
      label: 'The non-transfer',
      persona: 'Computes the figure but never carries it forward',
      work: ['Net profit figure is calculated and left in the first statement.', 'The next statement is prepared, but the profit line is left blank — the figure is never transferred in.'],
      keyLevelId: 'm2',
      keyNote:
        'Half marks — not zero, not full — and this is the rung careless markers get wrong in both directions. Own-figure marking pays half for a non-transfer: the figure was never carried into the next statement, so the transfer marks weren’t earned, but simply leaving it out is treated more gently than transferring a wrong number. A marker skimming for a figure on the line is tempted to award nothing; one crediting the correct subtotal above is tempted to wave the transfer through. The scheme pins it at half. Carry the figure through and it would have been the full four.',
    },
  ],
  takeaway: {
    id: 'codex-acc3',
    rule: 'One error is marked once — carry your figure through.',
    detail:
      'Accounting uses own-figure marking: a slip is penalised where it happens, not again downstream. Transfer your own figure correctly to keep the transfer marks; abandoning it or leaving it out costs more than the original error did.',
    cite: MS('p.34'),
  },
};

// ─────────────── AC4 · OL — the theory mark bank ───────────────

const AC4: ScaleSession = {
  mode: 'scale',
  id: 'acc-ol-theory',
  subject: 'accounting',
  level: 'ordinary',
  title: 'The theory is a mark bank',
  cue: 'Explain / define (OL)',
  question: 'An Ordinary Level paper carries written theory parts worth big flat marks — e.g. explaining a ratio for 10 marks, or giving two benefits of a cash budget for 5 each. A candidate who finds the accounts hard skips these written parts to spend more time on the figures. What does that cost?',
  questionNote:
    'Scenario authored for this exercise. At OL, written theory parts are free-standing flat-mark awards (definitions/benefits at 5–10 marks each) — reachable even by a candidate weak on the computational questions.',
  scale: {
    name: 'OL theory parts',
    levels: [
      { id: 'm0', label: '0 (skipped)', annotation: '0', marks: 0 },
      { id: 'm10', label: '10 (a definition answered)', annotation: '10', marks: 10 },
      { id: 'm20', label: '20 (theory parts done)', annotation: '20', marks: 20 },
    ],
    notes: [
      'OL awards written theory in big flat blocks — a ratio explained is 10 marks; each cash-budget benefit is 5.',
      'These marks don’t depend on getting the accounts right.',
      'Skipping them to chase figures forfeits the easiest, most reliable marks on the paper.',
    ],
    cite: MSOL('p.13, p.17, p.18 (theory definitions/benefits, flat marks)'),
  },
  scripts: [
    {
      id: 'ac4-a',
      label: 'The decision',
      persona: 'Skips theory for the figures',
      work: ['Struggles with the computational questions.', 'Skips the written definition/benefit parts to spend more time on the accounts.'],
      keyLevelId: 'm0',
      keyNote:
        'Zero from the theory — and these were the surest marks on the paper. A ratio definition is a flat 10 whether or not your accounts balance; two cash-budget benefits are 5 each. A candidate weak on figures should bank every theory mark first, then return to the computations. Never leave the written parts blank.',
      embodies: {
        behaviour: 'Skips flat-mark theory parts to chase computational marks — forfeiting the easiest marks.',
        cite: MSOL('p.13'),
      },
    },
    {
      id: 'ac4-border',
      label: 'The half-answer',
      persona: 'Explains the ratio, skips the benefits',
      work: ['Explains the ratio in full for its flat 10 marks.', 'Runs low on time and leaves the two cash-budget benefits (5 each) blank.'],
      keyLevelId: 'm10',
      keyNote:
        'Ten marks banked, ten left behind — exactly the middle. The ratio explanation is a clean flat 10 and it is secure; but the two cash-budget benefits were never written, so those marks are simply gone. A marker glancing at a well-answered theory block is tempted to credit the lot; one seeing an unfinished section is tempted to dock the ratio too. Each theory part stands alone: the ratio keeps its 10, the missing benefits score nothing. Answer every written part, not just the first that comes to mind.',
    },
  ],
  takeaway: {
    id: 'codex-ac4',
    rule: 'At OL, bank the theory marks first.',
    detail:
      'Ordinary Level Accounting pays big flat marks for written definitions and benefits (5–10 each), independent of your figures. Answer every theory part — they’re the surest marks on the paper, especially if the accounts are giving you trouble.',
    cite: MSOL('p.13'),
  },
};

// ─────────────── Ac5 · Published-accounts sequence penalty ───────────────

const AC5: ScaleSession = {
  mode: 'scale',
  id: 'acc-sequence',
  subject: 'accounting',
  level: 'higher',
  title: 'Right figures, wrong order',
  cue: 'Published accounts',
  question:
    'Published (statutory) accounts follow a fixed, prescribed sequence of entries. A candidate computes every figure in a Published Profit & Loss section correctly, but lists three of the entries in the wrong place in that sequence. The arithmetic is perfect. Is anything lost?',
  questionNote:
    'Scenario authored for this exercise. The published-accounts format sequence is itself examinable: the 2024 scheme opens Q2 (Published Accounts) with a standing note that penalties apply where entries are in incorrect sequence, and the annotation legend prices a misplaced entry at −1.',
  scale: {
    name: 'Correct sequence',
    levels: [
      { id: 'm0', label: '0 (statutory order abandoned)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (three entries out of sequence, −1 each)', annotation: '−3', marks: 2 },
      { id: 'm5', label: '5 (correct statutory sequence)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Published accounts follow a fixed statutory sequence — the order of the entries is marked, not just the figures.',
      'Right figures in the wrong order are penalised: −1 for each entry out of sequence, even when every number is arithmetically correct.',
      'Learn the layout cold so the marks your figures earn aren’t chipped away by presentation penalties.',
    ],
    cite: MS('p.10 (incorrect-sequence penalty), p.34 (−1 penalty: misplaced figure)'),
  },
  scripts: [
    {
      id: 'ac5-a',
      label: 'The Published P&L',
      persona: 'Correct figures, jumbled order',
      work: ['Every figure is arithmetically correct.', 'Three entries sit in the wrong place in the statutory sequence.'],
      keyLevelId: 'm2',
      keyNote:
        'Three marks gone to −1 penalties — the figures were all right, but published accounts are marked on layout as well as arithmetic. In the statutory format the order is examinable: “Penalties are applied where entries are in incorrect sequence.” Memorise the prescribed sequence so correct figures actually keep the marks they earn.',
      embodies: {
        behaviour: 'Places arithmetically-correct entries in the wrong statutory sequence — incurring the incorrect-sequence penalty.',
        cite: MS('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ac5',
    rule: 'In published accounts, the order is marked too.',
    detail:
      'Statutory published accounts follow a prescribed sequence, and entries in the wrong order are penalised −1 each — even when every figure is correct. Learn the layout so presentation penalties don’t chip away the marks your arithmetic earned.',
    cite: MS('p.10'),
  },
};

// ─────────────── Ac6 · The General Journal narration mark ───────────────

const AC6: GridSession = {
  mode: 'grid',
  id: 'acc-journal',
  subject: 'accounting',
  level: 'higher',
  title: 'The narration is a mark',
  cue: 'General Journal',
  question:
    'A General Journal entry (correction of errors) earns marks for the debit line, the credit line, AND the one-line “Being…” narration that explains it. One candidate posts the figures perfectly but writes no narration; another adds the narration line.',
  questionNote:
    'Scenario authored for this exercise; figures simplified. In the General Journal the marking is real: each entry awards the debit, the credit, and a discrete mark for the “Being the correction of…” narration — a mark candidates routinely leave on the table.',
  grid: {
    perPoint: [
      { id: 'debit', label: 'Debit entry correct', marks: 2 },
      { id: 'credit', label: 'Credit entry correct', marks: 2 },
      { id: 'narration', label: '“Being…” narration', marks: 1 },
    ],
    shorthand: 'Dr 2 · Cr 2 · Being… 1',
    ruleNote:
      'The narration (“Being the posting of…”) is a separately-awarded mark, not decoration. A correctly-posted entry with no narration banks the debit and credit but forfeits the narration mark on every single entry.',
    cite: MS('p.25 (General Journal — “Being…” narration [1])'),
  },
  scripts: [
    {
      id: 'ac6-a',
      label: 'Script A',
      persona: 'Figures only, no narration',
      attempts: [
        {
          id: 'ac6-a-1',
          text: 'Dr Bank €900; Cr Bad debt recovered €900. (No “Being…” line written.)',
          key: { debit: 2, credit: 2, narration: 0 },
          keyNote:
            'Debit and credit are both correct — 4 of 5 banked — but the narration mark is gone because no “Being…” line was written. Multiply that by every journal entry on the paper and the skipped narrations add up to a real block of marks. The narration is quick and it is marked: always write it.',
        },
      ],
      embodies: {
        behaviour: 'Posts a correct journal entry but omits the “Being…” narration — forfeiting the narration mark on every entry.',
        cite: MS('p.25'),
      },
    },
    {
      id: 'ac6-b',
      label: 'Script B',
      persona: 'Full entry, narration included',
      attempts: [
        {
          id: 'ac6-b-1',
          text: 'Dr Bank €900; Cr Bad debt recovered €900; “Being the posting of a bad debt recovered which had been omitted from the accounts.”',
          key: { debit: 2, credit: 2, narration: 1 },
          keyNote:
            'Full marks — the same correct posting, plus the one-line narration that the first script skipped. The narration takes seconds and secures a mark on every entry; it is the cheapest habit to build in the Correction-of-Errors question.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ac6',
    rule: 'Write the “Being…” — the narration is a mark.',
    detail:
      'Every General Journal entry awards a discrete mark for the “Being the correction of…” narration, on top of the debit and credit. Skipping it forfeits a mark on every single entry — always write the one-line narration.',
    cite: MS('p.25'),
  },
};

// ─────────────── Ac7 · The statement-heading mark ───────────────

const AC7: ScaleSession = {
  mode: 'scale',
  id: 'acc-heading',
  subject: 'accounting',
  level: 'higher',
  title: 'The heading is worth a mark',
  cue: 'Prepare accounts',
  question:
    'Every financial statement earns a mark for a correct, fully-dated heading — the business name, the statement type, and the period it covers. A candidate under time pressure dives straight into the figures with a bare, undated heading. What does that cost?',
  questionNote:
    'Scenario authored for this exercise. The 2024 scheme awards [1] for a correctly-titled, dated statement heading — e.g. “Trading Profit and Loss Account of Yeats Ltd for the year ended 31/12/2023 [1]” and “Manufacturing account for Sexton Ltd for year ended 31/12/2023 [1]”.',
  scale: {
    name: 'Statement heading',
    levels: [
      { id: 'm0', label: '0 (no proper heading)', annotation: '0', marks: 0 },
      { id: 'm1', label: '1 (full dated heading)', annotation: '1', marks: 1 },
    ],
    notes: [
      'Every statement earns a mark for a correct heading: the business name, the statement type, and the period it covers.',
      'A bare, undated, or mislabelled heading forfeits that mark — however good the figures beneath it are.',
      'Write the full dated title first, every time — it is among the cheapest marks on the paper.',
    ],
    cite: MS('p.3, p.6 (statement heading [1])'),
  },
  scripts: [
    {
      id: 'ac7-a',
      label: 'The statement',
      persona: 'Straight into the figures',
      work: ['Starts writing figures immediately under a one-word label.', 'No business name and no period/date on the heading.'],
      keyLevelId: 'm0',
      keyNote:
        'The heading mark is forfeited — the scheme awards [1] for a properly named and dated title, and this heading has neither the business name nor the period. It’s a free, independent mark that costs nothing but the discipline of writing the full title before the first figure. Head every statement in full.',
      embodies: {
        behaviour: 'Submits a statement with no properly named, dated heading — forfeiting the heading mark.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ac7',
    rule: 'Head every statement in full — it’s a mark.',
    detail:
      'Each statement awards a mark for a correct heading: business name, statement type, and period. A bare or undated title forfeits it regardless of the figures below. Write the full dated title first, every time — it’s one of the cheapest marks on the paper.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ac8 · OL — surplus answers earn nothing ───────────────

const AC8: ScaleSession = {
  mode: 'scale',
  id: 'acc-surplus',
  subject: 'accounting',
  level: 'ordinary',
  title: 'Extra answers don’t earn extra',
  cue: 'State / list (OL)',
  question:
    'A written part asks for TWO benefits of a cash budget, worth a fixed block of marks. A candidate who knows the topic writes FOUR benefits, all correct, hoping the extras earn more. Do the two extra benefits add anything?',
  questionNote:
    'Scenario authored for this exercise; the part’s mark split is simplified. The rule is real: the SEC annotation legend marks anything beyond the required answer as a “surplus answer … marks awarded elsewhere” — extra correct material earns nothing above the part’s ceiling.',
  scale: {
    name: 'Marks for the part',
    levels: [
      { id: 'm0', label: '0 (part skipped)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (one benefit)', annotation: '3', marks: 3 },
      { id: 'm5', label: '5 (two benefits — the ceiling)', annotation: '5', marks: 5 },
    ],
    notes: [
      'The part asks for a set number of points and carries a fixed maximum — here, two benefits for the full block.',
      'Correct material beyond the number asked for is annotated “surplus answer … marks awarded elsewhere” — it scores nothing above the ceiling.',
      'The two extra benefits are pure time cost: the same marks were already secured by the first two.',
    ],
    cite: MSOL('p.18 (two benefits of a cash budget [5]), p.19 (surplus-answer annotation)'),
  },
  scripts: [
    {
      id: 'ac8-a',
      label: 'The over-answerer',
      persona: 'Writes four benefits when two are asked',
      work: ['Question asks for TWO benefits.', 'Writes four correct benefits, expecting the extras to score.'],
      keyLevelId: 'm5',
      keyNote:
        'Full marks for the part — but only two of the four benefits actually scored; the other two are annotated “surplus … marks awarded elsewhere” and earn nothing. Answer the number asked for, well, then move on: extra correct writing cannot lift you above the part’s ceiling and the time is better spent on an unattempted item.',
      embodies: {
        behaviour: 'Writes more correct points than the question asks for — the surplus earns nothing beyond the ceiling.',
        cite: MSOL('p.19'),
      },
    },
    {
      id: 'ac8-border',
      label: 'The under-answerer',
      persona: 'Gives one benefit when two are asked',
      work: ['The part asks for TWO benefits of a cash budget.', 'Writes one clearly-correct benefit, then leaves the second blank.'],
      keyLevelId: 'm3',
      keyNote:
        'Three of the five — one benefit answered well, the second never attempted. This is the rung the scheme fixes precisely. A generous marker reads the single strong point as “clearly knows it” and is tempted to award the whole block; a strict one wants both points before crediting anything. Neither is right: the part is marked per point, so one benefit earns its 3 and the absent second earns nothing. A good single point is not the two the question asked for — give the number required, then move on.',
    },
  ],
  takeaway: {
    id: 'codex-acc8',
    rule: 'Answer the number asked — no more.',
    detail:
      'A written part has a fixed ceiling; correct material beyond the number of points required is marked “surplus … marks awarded elsewhere” and earns nothing. Give exactly what’s asked, do it well, and spend the saved time on parts you haven’t reached.',
    cite: MSOL('p.19'),
  },
};

// ─────────────── Ac9 · The ledger balancing figure ───────────────

const AC9: GridSession = {
  mode: 'grid',
  id: 'acc-ledger-balance',
  subject: 'accounting',
  level: 'higher',
  title: 'Balance the account off',
  cue: 'Ledger / T-account',
  question:
    'A Provision for Depreciation account is built from several correct entries. The account is only finished when it is ruled off with a Balance c/d and re-opened with a Balance b/d — and that balancing figure is itself a marked line. One candidate posts every entry but never strikes a balance.',
  questionNote:
    'Scenario authored for this exercise; figures simplified. In the 2024 scheme the ledger balancing figure is a discrete award — the Provision for Depreciation account credits the closing “Balance c/d [3]” as its own marked line, separate from the entries above it.',
  grid: {
    perPoint: [
      { id: 'entries', label: 'Individual entries correct', marks: 4 },
      { id: 'balc', label: 'Balance c/d struck & carried down', marks: 3 },
    ],
    shorthand: 'Entries 4 · Balance c/d 3',
    ruleNote:
      'In a T-account the closing balance is not bookkeeping housekeeping — it is a separately-awarded figure. Leaving the account unruled (no Balance c/d, no Balance b/d) banks the entries but forfeits the balancing-figure mark on every account you leave open.',
    cite: MS('p.16 (Provision for Depreciation A/c — closing Balance c/d [3])'),
  },
  scripts: [
    {
      id: 'ac9-a',
      label: 'Script A',
      persona: 'Posts entries, never balances',
      attempts: [
        {
          id: 'ac9-a-1',
          text: 'Posts the disposal, the P&L charge and the opening balance correctly, then moves on — no Balance c/d struck, the account left open.',
          key: { entries: 4, balc: 0 },
          keyNote:
            'The individual entries all score — but the account was never ruled off, so the discrete “Balance c/d” figure is gone. That balancing figure is a marked line in its own right; leaving even one T-account open on the paper is a clean, avoidable loss. Always close and re-open your ledger accounts.',
        },
      ],
      embodies: {
        behaviour: 'Leaves a ledger account unbalanced — forfeiting the discrete Balance c/d mark.',
        cite: MS('p.16'),
      },
    },
    {
      id: 'ac9-b',
      label: 'Script B',
      persona: 'Rules the account off',
      attempts: [
        {
          id: 'ac9-b-1',
          text: 'Same correct entries, then rules the account off: totals both sides, strikes Balance c/d, and brings the Balance b/d down below.',
          key: { entries: 4, balc: 3 },
          keyNote:
            'Full marks — the entries plus the balancing figure. Striking the Balance c/d and carrying the b/d down takes seconds and secures a marked line on every account. It also proves the account agrees, which is exactly what the examiner is looking to award.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-acc9',
    rule: 'The closing balance is a marked figure.',
    detail:
      'A ledger/T-account is finished only when it is ruled off — the Balance c/d (and the Balance b/d brought down) is a discrete award, not housekeeping. Close and re-open every account; an unbalanced account forfeits that figure however good the entries above it are.',
    cite: MS('p.16'),
  },
};

// ─────────────── Ac10 · The Notes to the Accounts ───────────────

const AC10: ScaleSession = {
  mode: 'scale',
  id: 'acc-notes',
  subject: 'accounting',
  level: 'higher',
  title: 'Don’t skip the Notes',
  cue: 'Published accounts',
  question:
    'In Published Accounts, the Notes to the Accounts (Accounting Policy, Operating Profit, Dividends, Tangible Fixed Assets) sit after the main statement and carry a heavy block of marks in their own right. A candidate who runs short on time finishes the face of the Profit & Loss but leaves the Notes blank. What does that cost?',
  questionNote:
    'Scenario authored for this exercise. The 2024 scheme prices the Notes to the Accounts as a large discrete block — Accounting Policy Notes [4], Operating Profit [4], Dividends [2] and Tangible Fixed Assets [7] — roughly 17 marks that live entirely in the notes, not in the statement above.',
  scale: {
    name: 'Notes to the Accounts',
    levels: [
      { id: 'm0', label: '0 (notes left blank)', annotation: '0', marks: 0 },
      { id: 'm7', label: '7 (TFA note only)', annotation: '7', marks: 7 },
      { id: 'm17', label: '17 (all four notes)', annotation: '17', marks: 17 },
    ],
    notes: [
      'The Notes to the Accounts are a separately-marked block: Accounting Policy [4], Operating Profit [4], Dividends [2], Tangible Fixed Assets [7].',
      'The Tangible Fixed Assets note alone is worth [7] — as much as the heaviest single line on the face of the accounts.',
      'These marks are gone if the notes are skipped, no matter how complete the statement above them is.',
    ],
    cite: MS('p.11 (Notes to the Accounts — Accounting Policy [4], Operating Profit [4], Dividends [2], Tangible Fixed Assets [7])'),
  },
  scripts: [
    {
      id: 'ac10-a',
      label: 'The Published Accounts',
      persona: 'Finishes the face, skips the notes',
      work: ['Completes the Published Profit & Loss account.', 'Runs low on time and leaves the Notes to the Accounts blank.'],
      keyLevelId: 'm0',
      keyNote:
        'A large block forfeited — the notes carry roughly 17 marks the statement above doesn’t, and the Tangible Fixed Assets note alone is [7]. Because the notes are a reliable, structured layout you can learn cold, budget time to attempt them: even the accounting-policy note is [4] of near-guaranteed marks. Never leave the Notes empty.',
      embodies: {
        behaviour: 'Leaves the Notes to the Accounts blank — forfeiting a large, self-contained block of marks.',
        cite: MS('p.11'),
      },
    },
    {
      id: 'ac10-border',
      label: 'The part-finished notes',
      persona: 'Does the big note, skips the rest',
      work: ['Completes the Tangible Fixed Assets note in full [7].', 'Leaves the Accounting Policy [4], Operating Profit [4] and Dividends [2] notes blank.'],
      keyLevelId: 'm7',
      keyNote:
        'Seven marks — the Tangible Fixed Assets note, done properly, is worth exactly that and it is banked in full. But the other three notes are untouched, so ten more marks are still on the table. The middle rung is real because the notes are separately marked: a part-done notes section neither collapses to zero nor rounds up to the full block. A marker who sees a strong TFA note may assume the section is “done”; the scheme credits only what is written. Attempt all four — even the two-mark Dividends note is quick, guaranteed marks.',
    },
  ],
  takeaway: {
    id: 'codex-acc10',
    rule: 'The Notes carry their own block of marks.',
    detail:
      'In Published Accounts the Notes to the Accounts (Accounting Policy, Operating Profit, Dividends, Tangible Fixed Assets) are worth a large block on top of the statement — the TFA note alone is [7]. They’re a learnable layout: budget time to attempt them and never leave them blank.',
    cite: MS('p.11'),
  },
};

// ─────────────── Ac11 · Cash-flow section headings ───────────────

const AC11: GridSession = {
  mode: 'grid',
  id: 'acc-cashflow-headings',
  subject: 'accounting',
  level: 'higher',
  title: 'Label every cash-flow section',
  cue: 'Cash Flow Statement',
  question:
    'A Cash Flow Statement is organised under standard section headings — Operating Activities, Return on Investments & Servicing of Finance, Taxation, Capital Expenditure, Equity Dividends Paid, Financing. Each heading is a mark. One candidate lists the movements with correct figures but writes no section headings.',
  questionNote:
    'Scenario authored for this exercise; figures omitted. In the 2024 scheme each cash-flow section heading earns a discrete mark — “Operating Activities [1]”, “Taxation [1]”, “Financing [1]”, and so on — on top of the figures grouped beneath it.',
  grid: {
    perPoint: [
      { id: 'figures', label: 'Section figures correct', marks: 6 },
      { id: 'headings', label: 'Section headings present', marks: 6 },
    ],
    shorthand: 'Figures 6 · Headings 6 (≈[1] each)',
    ruleNote:
      'The standard cash-flow section headings are marked lines, not layout decoration — each is worth about [1]. A statement with correct figures but no headings banks the figures and quietly forfeits a mark for every missing heading.',
    cite: MS('p.23 (Cash Flow Statement — section headings each [1])'),
  },
  scripts: [
    {
      id: 'ac11-a',
      label: 'Script A',
      persona: 'Correct figures, no headings',
      attempts: [
        {
          id: 'ac11-a-1',
          text: 'Lists the cash movements with correct figures in the right order, but under no section headings — a bare column of numbers.',
          key: { figures: 6, headings: 0 },
          keyNote:
            'Every figure scores — but each of the six standard section headings is a separate [1] mark that was left unwritten. That is a whole block of easy marks lost to omission. The headings are fixed and identical every year: learn them and write them.',
        },
      ],
      embodies: {
        behaviour: 'Omits the standard cash-flow section headings — forfeiting the mark on each one.',
        cite: MS('p.23'),
      },
    },
    {
      id: 'ac11-b',
      label: 'Script B',
      persona: 'Figures grouped under headings',
      attempts: [
        {
          id: 'ac11-b-1',
          text: 'Groups the same correct figures under the standard headings — Operating Activities, Taxation, Capital Expenditure, Financing, and the rest.',
          key: { figures: 6, headings: 6 },
          keyNote:
            'Full marks — the same figures, now under the standard section headings that each carry a mark. The headings are a rote, guaranteed block; writing them as you build the statement costs nothing and secures marks the first script simply gave away.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-acc11',
    rule: 'Every cash-flow heading is a mark.',
    detail:
      'The Cash Flow Statement’s standard section headings (Operating Activities, Taxation, Capital Expenditure, Financing, …) each earn a discrete mark on top of the figures. They’re fixed every year — write them all, and don’t hand back a block of guaranteed marks by listing bare numbers.',
    cite: MS('p.23'),
  },
};

// ─────────────── Ac12 · The interpretation report rewards developed comment ───────────────

const AC12: GridSession = {
  mode: 'grid',
  id: 'acc-report-comments',
  subject: 'accounting',
  level: 'higher',
  title: 'A ratio isn’t a comment',
  cue: 'Interpretation report',
  question:
    'In the Interpretation report, marks are awarded for developed analysis under each heading, not for the bare ratio — a good comment quotes the figure, notes the trend against last year, and interprets it against a benchmark. One candidate writes only “ROCE is 17.3%.” Another develops it fully.',
  questionNote:
    'Scenario authored for this exercise; the per-comment split is simplified. The 2024 report scheme awards big analytical blocks — Profitability [7], Gearing [9], Security [7] — plus a discrete Conclusion [1]; the marks reward developed comment (figure + trend + interpretation), not a re-stated ratio.',
  grid: {
    perPoint: [
      { id: 'figure', label: 'Ratio value quoted', marks: 2 },
      { id: 'trend', label: 'Trend vs prior year', marks: 2 },
      { id: 'interp', label: 'Interpretation / benchmark', marks: 3 },
    ],
    shorthand: 'Figure 2 · Trend 2 · Interpret 3',
    ruleNote:
      'The report question is not the ratio calculation — the analytical marks sit in the comment. A developed point states the figure, compares it to last year, and reads it against a benchmark (the ideal ratio, the cost of borrowing, the risk-free return). A bare ratio scores only the figure.',
    cite: MS('p.19, p.20 (Interpretation report — Profitability [7], Gearing [9], Conclusion [1])'),
  },
  scripts: [
    {
      id: 'ac12-a',
      label: 'Script A',
      persona: 'States the ratio, stops',
      attempts: [
        {
          id: 'ac12-a-1',
          text: '“The return on capital employed is 17.3%.” (No comparison, no interpretation.)',
          key: { figure: 2, trend: 0, interp: 0 },
          keyNote:
            'Only the figure scores — the report is asking for analysis, and there is none here. Quoting a ratio you already calculated earlier is close to a surplus answer; the marks live in the trend and the interpretation the candidate never wrote. In the report, a number without a comment is barely worth anything.',
        },
      ],
      embodies: {
        behaviour: 'Restates a computed ratio without developing a trend or interpretation — the analytical marks go unearned.',
        cite: MS('p.19'),
      },
    },
    {
      id: 'ac12-b',
      label: 'Script B',
      persona: 'Develops the comment',
      attempts: [
        {
          id: 'ac12-b-1',
          text: '“ROCE is 17.3%, up from 15% last year — an improving trend. It is well above the 8% cost of borrowing, so the company is using its resources efficiently.”',
          key: { figure: 2, trend: 2, interp: 3 },
          keyNote:
            'Full marks — figure, trend and interpretation, exactly what the report heading rewards. Notice the shape you can reuse for every ratio: state it, compare it to last year, then judge it against a benchmark. And finish the report with a clear Conclusion — that recommendation is its own [1].',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-acc12',
    rule: 'In the report, comment beats calculation.',
    detail:
      'The Interpretation report awards developed analysis, not the bare ratio: quote the figure, note the trend against last year, interpret it against a benchmark. Restating a number scores almost nothing. Build every comment to that shape — and end with a clear Conclusion, which carries its own mark.',
    cite: MS('p.20'),
  },
};

// ─────────────── Ac13 · HL — the theory tail is still marks ───────────────

const AC13: ScaleSession = {
  mode: 'scale',
  id: 'acc-hl-theory',
  subject: 'accounting',
  level: 'higher',
  title: 'The theory part at the end',
  cue: 'Explain / define (HL)',
  question:
    'Even the big Higher Level computational questions end with a written theory part — define FIFO and name alternatives, explain controllable costs, explain why the suspense account closes to zero. A strong computational candidate, low on time, skips this final written part to check figures. What does that cost?',
  questionNote:
    'Scenario authored for this exercise. At HL the written tail of a computational question is a flat-mark block independent of the figures — e.g. the suspense-account explanation [2], “Controllable costs …” [4], and defining FIFO with alternatives [6] in the 2024 scheme.',
  scale: {
    name: 'HL written-theory part',
    levels: [
      { id: 'm0', label: '0 (part skipped)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (definition only)', annotation: '2', marks: 2 },
      { id: 'm6', label: '6 (definition + alternatives)', annotation: '6', marks: 6 },
    ],
    notes: [
      'HL computational questions carry a written theory tail worth a flat block — FIFO + alternatives [6], controllable costs [4], the suspense explanation [2].',
      'These marks are independent of the figures: they’re there whether or not your accounts balanced.',
      'They are among the most reliable marks in the question, yet the first thing rushed candidates drop.',
    ],
    cite: MS('p.26 (suspense-account explanation [2]), p.29 (controllable costs [4]), p.30 (FIFO + alternative methods [6])'),
  },
  scripts: [
    {
      id: 'ac13-a',
      label: 'The final part',
      persona: 'Skips the written tail',
      work: ['Completes the computational parts.', 'Leaves the closing written-theory part blank to re-check figures.'],
      keyLevelId: 'm0',
      keyNote:
        'A flat, reliable block forfeited — the theory tail is worth its marks regardless of the figures, and defining FIFO with two alternatives is a straight [6]. HL is not “all computation”: budget a couple of minutes for the written part of every big question, because a rote definition is safer than one more re-check of an account that already balances.',
      embodies: {
        behaviour: 'Skips the written-theory tail of an HL computational question — forfeiting flat, figure-independent marks.',
        cite: MS('p.30'),
      },
    },
    {
      id: 'ac13-border',
      label: 'The half-written tail',
      persona: 'Defines the term, omits the alternatives',
      work: ['Defines FIFO correctly.', 'Does not name or outline the alternative methods the same part also asks for.'],
      keyLevelId: 'm2',
      keyNote:
        'Two of the six — the definition is right and earns its marks, but the part also asks for the alternative methods and none are given. The scheme fixes this at the middle: the definition stands on its own, while the alternatives are a separate, unwritten chunk of the same allocation. A hurried marker credits the whole part for a confident opening line, or skips a “half-done” answer entirely; here the definition banks its 2 and the missing alternatives cost the other 4. Finish the part — naming the alternatives is as rote as the definition itself.',
    },
  ],
  takeaway: {
    id: 'codex-acc13',
    rule: 'Answer the theory tail — even at HL.',
    detail:
      'Higher Level computational questions end with a written part (define FIFO, explain controllable costs, why the suspense closes to zero) worth a flat block independent of the figures. It’s among the surest marks in the question — always attempt it, rather than re-checking accounts that already balance.',
    cite: MS('p.30'),
  },
};

// ─────────────── Ac14 · A valid alternative method scores full ───────────────

const AC14: ScaleSession = {
  mode: 'scale',
  id: 'acc-alternatives',
  subject: 'accounting',
  level: 'higher',
  title: 'A valid alternative still scores',
  cue: 'Interpretation / ratios',
  question:
    'Gearing can be expressed as Debt to Capital Employed or as Debt to Equity — two different formulas giving two different percentages. A candidate uses Debt to Equity instead of the layout in the model answer and reaches the correct alternative figure. Full marks, or marked down for “wrong method”?',
  questionNote:
    'Scenario authored for this exercise. The 2024 scheme explicitly accepts the alternative: for Q5 gearing it notes Debt to Equity “is fully acceptable” and that the student “should arrive at an answer of 36.89% for full marks” — a legitimate alternative that reaches the correct target is not penalised.',
  scale: {
    name: 'Alternative method',
    levels: [
      { id: 'm0', label: '0 (alternative, wrong target)', annotation: '0', marks: 0 },
      { id: 'm3', label: '3 (right method, figure slips)', annotation: '3', marks: 3 },
      { id: 'm6', label: '6 (valid alternative, correct target)', annotation: '6', marks: 6 },
    ],
    notes: [
      'A legitimate alternative approach is accepted provided it reaches the correct target figure — the scheme names Debt to Equity as fully acceptable for gearing.',
      'The award follows the correct alternative answer, not the particular layout in the model solution.',
      'What is still required is the right target figure: an alternative that lands on the wrong number does not rescue the marks.',
    ],
    cite: MS('p.18 (Q5 gearing — Debt to Equity accepted, 36.89% for full marks)'),
  },
  scripts: [
    {
      id: 'ac14-a',
      label: 'The alternative',
      persona: 'Uses Debt to Equity, lands the figure',
      work: ['Uses Debt to Equity instead of Debt to Capital Employed.', 'Reaches the accepted alternative figure of 36.89%.'],
      keyLevelId: 'm6',
      keyNote:
        'Full marks — the scheme explicitly accepts Debt to Equity and prints 36.89% as the alternative target. Don’t abandon a method you know well because it isn’t the one in your notes: a valid alternative that reaches the correct figure scores in full. The one thing that is non-negotiable is landing on the right target.',
      embodies: {
        behaviour: 'Uses a scheme-accepted alternative method and reaches the correct alternative target — scoring full marks.',
        cite: MS('p.18'),
      },
    },
    {
      id: 'ac14-border',
      label: 'The slipped alternative',
      persona: 'Right method, wrong final figure',
      work: ['Uses Debt to Equity — a method the scheme accepts.', 'Slips in the arithmetic and reports a figure other than the 36.89% target.'],
      keyLevelId: 'm3',
      keyNote:
        'The middle rung, and the easiest to mis-mark. The method is legitimate — Debt to Equity is fully accepted — so the workmarks for the correct approach are earned; but the final figure is wrong, so the marks that ride on landing 36.89% are not. A marker who spots an accepted method is tempted to award full; one who spots the wrong final number is tempted to award nothing. The scheme splits it: right method, wrong target. A valid alternative only pays in full when it actually reaches the correct figure.',
    },
  ],
  takeaway: {
    id: 'codex-acc14',
    rule: 'A valid alternative that hits the target scores full.',
    detail:
      'The scheme accepts legitimate alternative methods — e.g. Debt to Equity for gearing (36.89%) — provided they reach the correct target figure. Use the approach you know best without fear of a “wrong format”; just make sure it lands on the right number.',
    cite: MS('p.18'),
  },
};

// ─────────────── Ac15 · Corrected Net Profit — add or deduct ───────────────

const AC15: GridSession = {
  mode: 'grid',
  id: 'acc-corrected-profit',
  subject: 'accounting',
  level: 'higher',
  title: 'Add it or take it away',
  cue: 'Correction of errors',
  question:
    'In the Statement of Corrected Net Profit, each correction has to be classified as an addition to profit or a deduction from it. Identifying the adjustment isn’t enough — putting it on the wrong side loses the mark. A candidate identifies every adjustment but adds one back that should have been deducted.',
  questionNote:
    'Scenario authored for this exercise; figures simplified. The 2024 Statement of Corrected Net Profit (Q7) marks each adjustment by its side — items under “Add” raise the profit and items under “Less” reduce it, and the correct classification is what earns the mark.',
  grid: {
    perPoint: [
      { id: 'identify', label: 'Adjustment identified', marks: 2 },
      { id: 'direction', label: 'Correct side (add vs less)', marks: 2 },
    ],
    shorthand: 'Identify 2 · Correct side 2',
    ruleNote:
      'The Statement of Corrected Net Profit is a directional statement: an item that overstated profit must be deducted, one that understated it must be added back. Naming the right item on the wrong side scores the identification but not the classification — and the wrong sign feeds into a wrong corrected figure.',
    cite: MS('p.26 (Statement of Corrected Net Profit — Add / Less classification)'),
  },
  scripts: [
    {
      id: 'ac15-a',
      label: 'Script A',
      persona: 'Right item, wrong side',
      attempts: [
        {
          id: 'ac15-a-1',
          text: 'Lists an overstatement of profit under “Add” instead of “Less”, so it increases the corrected profit rather than reducing it.',
          key: { identify: 2, direction: 0 },
          keyNote:
            'The adjustment is correctly identified, but it’s on the wrong side — an item that overstated profit has to be deducted, not added. The classification mark is lost, and the wrong sign also pushes the final corrected profit off. Before writing each line, ask: did this error make profit too high or too low?',
        },
      ],
      embodies: {
        behaviour: 'Places a correction on the wrong side of the Corrected Net Profit statement — losing the classification mark.',
        cite: MS('p.26'),
      },
    },
    {
      id: 'ac15-b',
      label: 'Script B',
      persona: 'Right item, right side',
      attempts: [
        {
          id: 'ac15-b-1',
          text: 'Puts each overstatement under “Less” and each understatement under “Add”, so every correction moves profit in the right direction.',
          key: { identify: 2, direction: 2 },
          keyNote:
            'Full marks — each adjustment identified and classified on the correct side. Deciding “too high, so deduct / too low, so add back” for every item both banks the classification mark and keeps the corrected profit figure right. The direction is half the marks on this statement.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-acc15',
    rule: 'Get each correction on the right side.',
    detail:
      'In the Statement of Corrected Net Profit, classification is marked as well as identification: an item that overstated profit must be deducted, one that understated it added back. Ask “too high or too low?” for each adjustment — the wrong side loses the mark and corrupts the final figure.',
    cite: MS('p.26'),
  },
};

export const ACCOUNTING_CHAIR: ChairSubject = {
  id: 'accounting',
  label: 'Accounting',
  tagline: 'Workmarks, balancing, own-figure marking, format marks and the marks candidates leave on the table.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15],
  sources: [
    { label: 'SEC LC Accounting HL marking scheme 2024 (examiner-reports/accounting/2024-marking-scheme)' },
    { label: 'SEC LC Accounting OL marking scheme 2024 (examiner-reports/accounting/2024-ol-marking-scheme)' },
  ],
  coverageNote:
    'The workmark, own-figure, sequence, journal-narration, statement-heading, ledger-balance, notes, cash-flow-heading, report-comment, theory-tail, alternative-method and corrected-profit sessions are verified against the 2024 HL scheme; most apply at both levels (note: OL has no “both totals correct” balance-sheet mark and no incorrect-sequence penalty). The two Ordinary sessions (flat-mark theory, surplus answers) are verified against the 2024 OL scheme. More OL sessions are being added.',
};
