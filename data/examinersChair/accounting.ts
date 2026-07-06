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

export const ACCOUNTING_CHAIR: ChairSubject = {
  id: 'accounting',
  label: 'Accounting',
  tagline: 'Workmarks, balancing, own-figure marking and format marks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AC1, AC2, AC3, AC4, AC5, AC6, AC7],
  sources: [
    { label: 'SEC LC Accounting HL marking scheme 2024 (examiner-reports/accounting/2024-marking-scheme)' },
    { label: 'SEC LC Accounting OL marking scheme 2024 (examiner-reports/accounting/2024-ol-marking-scheme)' },
  ],
  coverageNote:
    'The workmark, own-figure, sequence, journal-narration and statement-heading sessions apply at both levels (note: OL has no “both totals correct” balance-sheet mark). The Ordinary session is verified against the 2024 OL scheme. More OL sessions are being added.',
};
