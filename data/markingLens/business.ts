/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Business (pilot / golden file).
 *
 * Source of truth: examiner-reports/business/2024-marking-scheme.md
 * (SEC Marking Scheme 2024, Business Higher Level). Every notation below is
 * verbatim from that document; every entry's parts sum to its Available Marks
 * line (machine-checked). Pitfalls cite the Chief Examiner's Report 2015
 * (Business HL) — the same sourced insights surfaced in examinerInsights.ts.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2024 HL Paper 1 (LC033ALP032EV) Q1–12 — Section 1 short answers, 10m each.
 *  - 2024 HL Paper 2 (LC033ALP041EV + IV mirror) Q1–8 — 60m long questions.
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE = (q: string) => `SEC Marking Scheme 2024, Business Higher Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

// ── Section 1 short-answer questions (Paper 1, 10 marks each) ───────────────

const short = (n: string, notation: string, decoded: string): QuestionLens => ({
  year: 2024,
  level: 'higher',
  lang: 'ev',
  fileid: 'LC033ALP032EV.pdf',
  n,
  totalMarks: 10,
  headline: 'A 10-mark short answer — the scheme allocates every mark on the grid below.',
  parts: [{ part: '', task: 'Short-answer question', notation, decoded, marks: 10 }],
  cite: CITE(`Section 1 Q${n}`),
});

const SHORTS: QuestionLens[] = [
  short('1', '3 + 2 + 2 + 2 + 1', 'Five scheme elements: 3 marks for the first, then 2m, 2m, 2m and 1m.'),
  short('2', '3 + 2 + 2 + 2 + 1', 'Five scheme elements: 3 marks for the first, then 2m, 2m, 2m and 1m.'),
  short('3', '(i) 4m (2+2) · (ii) 6m (3+3)', 'Part (i): two 2-mark elements. Part (ii): two 3-mark elements.'),
  short('4', '3 + 2 + 2 + 2 + 1', 'Five scheme elements: 3 marks for the first, then 2m, 2m, 2m and 1m.'),
  short('5', '2 @ 5m (3+2)', 'Two points, 5 marks each: 3m for the point, 2m for its development.'),
  short('6', '2 @ 5m (3+2)', 'Two points, 5 marks each: 3m for the point, 2m for its development.'),
  short('7', '3 + 2 + 2 + 2 + 1', 'Five scheme elements: 3 marks for the first, then 2m, 2m, 2m and 1m.'),
  short('8', '2 @ 5m (3+2)', 'Two points, 5 marks each: 3m for the point, 2m for its development.'),
  short('9', '(i) 6m (1+1+2+2) · (ii) 4m (2+2)', 'Part (i): four elements (1m, 1m, 2m, 2m). Part (ii): two 2-mark elements.'),
  short('10', '4m (2+2) + 3m (2+1) + 3m (2+1)', 'Three elements: one worth 4 (2+2) and two worth 3 (2+1 each).'),
  short('11', '10m (4 + 3 + 3)', 'One answer built of three elements: 4 marks, 3 marks, 3 marks.'),
  short('12', '(i) 4m (2+2) · (ii) 6m (2+2+1+1)', 'Part (i): two 2-mark elements. Part (ii): four elements (2m, 2m, 1m, 1m).'),
];

// ── Long questions (Paper 2, 60 marks each) ─────────────────────────────────

const LONGS_EV: QuestionLens[] = [
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '1',
    totalMarks: 60,
    headline: 'Three 20-mark parts (A–C); every point is marked on a state + develop grid.',
    parts: [
      { part: '(A)(i)', task: 'Explain the term breach of contract', notation: '6m (4+2)', decoded: '4 marks for the explanation, 2 for its development.', marks: 6 },
      { part: '(A)(ii)', task: 'Illustrate the remedies available for a breach of contract', notation: '2 @ 7m (2+2+3)', decoded: 'Two remedies, 7 marks each: state (2m) + develop (2m) + illustrate (3m).', marks: 14 },
      { part: '(B)(i)', task: 'Describe three features of the Small Claims Procedure', notation: '3 @ 5m (2+3)', decoded: 'Three features, 5 marks each: state (2m) + develop (3m).', marks: 15 },
      { part: '(B)(ii)', task: 'Recommend one improvement to the Small Claims Procedure, with a reason', notation: '5m (2+3)', decoded: 'Recommendation (2m) + supporting reason (3m).', marks: 5 },
      { part: '(C)(i)', task: 'List three grounds for unfair dismissal (Unfair Dismissals Act 1977/2015)', notation: '3 @ 2m', decoded: 'Three grounds, 2 marks each — listing is enough for a “List” cue.', marks: 6 },
      { part: '(C)(ii)', task: 'Outline three procedures an employer should follow when dismissing an employee', notation: '2 @ 5m (2+3) + 1 @ 4m (2+2)', decoded: 'Two procedures at 5m (state 2 + develop 3) and one at 4m (state 2 + develop 2).', marks: 14 },
    ],
    cite: CITE('Q1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '2',
    totalMarks: 60,
    headline: 'Three 20-mark parts (A–C); each point earns 5 marks on a 2+3 state + develop grid.',
    parts: [
      { part: '(A)(i)', task: 'Distinguish between economic growth and interest rates', notation: '2 @ 5m (2+3)', decoded: 'Both terms treated: state (2m) + develop (3m) each.', marks: 10 },
      { part: '(A)(ii)', task: 'Outline the impacts of an interest-rate increase on Irish businesses', notation: '2 @ 5m (2+3)', decoded: 'Two impacts, 5 marks each: state (2m) + develop (3m).', marks: 10 },
      { part: '(B)(i)', task: 'Illustrate your understanding of the primary sector', notation: '5m (2+3)', decoded: 'State (2m) + develop/illustrate (3m).', marks: 5 },
      { part: '(B)(ii)', task: 'Discuss current trends in the primary sector', notation: '3 @ 5m (2+3)', decoded: 'Three trends, 5 marks each: state (2m) + develop (3m).', marks: 15 },
      { part: '(C)(i)', task: 'Explain the term business ethics', notation: '5m (2+3)', decoded: 'State (2m) + develop (3m).', marks: 5 },
      { part: '(C)(ii)', task: 'Outline how a business may encourage employees to be ethical', notation: '3 @ 5m (2+3)', decoded: 'Three ways, 5 marks each: state (2m) + develop (3m).', marks: 15 },
    ],
    cite: CITE('Q2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '3',
    totalMarks: 60,
    headline: 'Three 20-mark parts; the calculation part awards workings, formula, € sign and the surplus/deficit call.',
    parts: [
      { part: '(A)(i)', task: 'Explain the term Balance of Payments', notation: '6m (3+3)', decoded: 'Two 3-mark elements of the explanation.', marks: 6 },
      { part: '(A)(ii)', task: 'Calculate the Balance of Trade and Balance of Payments; state surplus or deficit', notation: 'BOT 6m + BOP 8m', decoded: 'Formula 1m, each correct figure 1m, € sign 1m, surplus/deficit 1m — workings carry the marks.', marks: 14 },
      { part: '(B)', task: 'Discuss why multinationals locate in Ireland (apart from taxation)', notation: '4 @ 5m (2+3)', decoded: 'Four reasons, 5 marks each: state (2m) + develop (3m).', marks: 20 },
      { part: '(C)(i)', task: 'Distinguish standardised vs adapted marketing mix', notation: '2 @ 5m (2+3)', decoded: 'Both terms treated: state (2m) + develop (3m) each.', marks: 10 },
      { part: '(C)(ii)', task: 'Explain the importance for Ireland of one EU policy (CAP / Social / Competition)', notation: '2 @ 5m (2+3)', decoded: 'Two points on the chosen policy, 5 marks each: state (2m) + develop (3m).', marks: 10 },
    ],
    cite: CITE('Q3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '4',
    totalMarks: 60,
    headline: 'Three 20-mark parts; part (C) reserves 4 marks purely for the evaluation itself.',
    parts: [
      { part: '(A)(i)', task: 'Define trade dispute (Industrial Relations Act 1990)', notation: '8m (2+3+3)', decoded: 'Three elements of the statutory definition: 2m + 3m + 3m.', marks: 8 },
      { part: '(A)(ii)', task: 'Describe three types of official industrial action', notation: '3 @ 4m (2+2)', decoded: 'Three types, 4 marks each: state (2m) + develop (2m).', marks: 12 },
      { part: '(B)(i)', task: 'Illustrate the difference between lobbying and negotiation', notation: '2 @ 5m (3+2)', decoded: 'Both terms treated: 3m + 2m each.', marks: 10 },
      { part: '(B)(ii)', task: 'Outline two benefits of trade unions to an employee', notation: '2 @ 5m (3+2)', decoded: 'Two benefits, 5 marks each: state (3m) + develop (2m).', marks: 10 },
      { part: '(C)', task: 'Evaluate the role of the CCPC', notation: '4 @ 4m (2+2) + EV 2 + EV 2', decoded: 'Four points (state 2 + develop 2 each) — plus 4 marks ONLY for the evaluation: a judgement with justification.', marks: 20 },
    ],
    pitfall: {
      text: 'Evaluation that is superficial or absent is the consistently weakest skill — describing the point is not evaluating it, and caps the marks.',
      cite: "Chief Examiner's Report 2015 (Business HL), p.17",
    },
    cite: CITE('Q4'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '5',
    totalMarks: 60,
    headline: 'Applied question (IKEA): the third mark of each point is earned by tying it to the named business.',
    parts: [
      { part: '(A)', task: 'Explain reasons why an individual may become an entrepreneur', notation: '3 @ 5m (2+3)', decoded: 'Three reasons, 5 marks each: state (2m) + develop (3m).', marks: 15 },
      { part: '(B)(i)', task: 'Distinguish span of control vs chain of command', notation: '2 @ 5m (2+3)', decoded: 'Both terms treated: state (2m) + develop (3m) each.', marks: 10 },
      { part: '(B)(ii)', task: 'Discuss the benefits of a matrix structure for a business such as IKEA', notation: '3 @ 5m (2+2+1)', decoded: 'Three benefits: state (2m) + develop (2m) + link to the business (1m).', marks: 15 },
      { part: '(C)', task: 'Outline the impact of technology for management (design, manufacturing, marketing, HRM)', notation: '4 @ 5m (2+2+1)', decoded: 'One point per heading: state (2m) + develop (2m) + example/link (1m).', marks: 20 },
    ],
    pitfall: {
      text: 'Defining a term well but failing to apply it to the context asked for — recall did not match application, and the application marks are separate.',
      cite: "Chief Examiner's Report 2015 (Business HL), p.14",
    },
    cite: CITE('Q5'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '6',
    totalMarks: 60,
    headline: 'A 25-mark part (A) with a marked calculation, then two 15/20-mark discussion parts.',
    parts: [
      { part: '(A)(i)', task: 'Explain the reasons Jackson Ltd would prepare a cashflow forecast', notation: '2 @ 5m (2+3)', decoded: 'Two reasons, 5 marks each: state (2m) + develop (3m).', marks: 10 },
      { part: '(A)(ii)', task: 'Calculate the figures A, B and C on the cashflow forecast', notation: '7m (3+2+2)', decoded: 'The three figures carry 3m, 2m and 2m.', marks: 7 },
      { part: '(A)(iii)', task: 'Outline two ways to deal with a problem in the forecast', notation: '2 @ 4m (2+2)', decoded: 'Two ways, 4 marks each: state (2m) + develop (2m).', marks: 8 },
      { part: '(B)', task: 'Discuss household vs business management in relation to taxation', notation: '3 @ 5m (2+3)', decoded: 'Three points of contrast, 5 marks each: state (2m) + develop (3m).', marks: 15 },
      { part: '(C)(i)', task: 'Explain, with examples, three principles of insurance', notation: '3 @ 5m (2+3)', decoded: 'Each principle: state (2m) + develop/example (3m).', marks: 15 },
      { part: '(C)(ii)', task: 'Identify one insurance policy and explain why the risk might be uninsurable', notation: '5m (2+3)', decoded: 'Policy (2m) + explanation (3m).', marks: 5 },
    ],
    cite: CITE('Q6'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '7',
    totalMarks: 60,
    headline: 'Applied question (4th ARQ): headed contrast part (B) wants one 5-mark point per heading.',
    parts: [
      { part: '(A)(i)', task: 'Explain the term batch production', notation: '5m (2+3)', decoded: 'State (2m) + develop (3m).', marks: 5 },
      { part: '(A)(ii)', task: 'Discuss the implications of changing from batch to mass production', notation: '3 @ 5m (2+2+1)', decoded: 'Three implications: state (2m) + develop (2m) + link to the business (1m).', marks: 15 },
      { part: '(B)', task: 'Contrast a sole trader and a private limited company (formation, liability, finance, control)', notation: '4 @ 5m (2+3)', decoded: 'One contrast per heading, 5 marks each: state (2m) + develop (3m).', marks: 20 },
      { part: '(C)(i)', task: 'Explain three financial terms (liquidity, P&L, debtors, dividends)', notation: '3 @ 5m (2+3)', decoded: 'Three terms, 5 marks each: state (2m) + develop (3m).', marks: 15 },
      { part: '(C)(ii)', task: 'Outline one profitability ratio', notation: '5m (2+3)', decoded: 'Ratio (2m) + outline (3m).', marks: 5 },
    ],
    cite: CITE('Q7'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '8',
    totalMarks: 60,
    headline: 'Marketing question; part (B)(iii) marks each recommendation with its supporting reason.',
    parts: [
      { part: '(A)(i)', task: 'Explain the term premium pricing', notation: '5m (2+3)', decoded: 'State (2m) + develop (3m).', marks: 5 },
      { part: '(A)(ii)', task: 'Outline factors considered before pricing, with examples', notation: '3 @ 5m (2+2+1)', decoded: 'Three factors: state (2m) + develop (2m) + example (1m).', marks: 15 },
      { part: '(B)(i)', task: 'What do the letters ASAI stand for?', notation: '4m', decoded: 'The full name earns the 4 marks.', marks: 4 },
      { part: '(B)(ii)', task: 'Distinguish generic vs persuasive advertising', notation: '2 @ 5m (2+3)', decoded: 'Both terms treated: state (2m) + develop (3m) each.', marks: 10 },
      { part: '(B)(iii)', task: 'Recommend an advertising medium for two of the listed businesses, with reasons', notation: '1 @ 6m (3+3) + 1 @ 5m (3+2)', decoded: 'First recommendation 6m (medium 3 + reason 3); second 5m (medium 3 + reason 2).', marks: 11 },
      { part: '(C)', task: 'Describe sales promotion techniques, with examples', notation: '3 @ 5m (2+2+1)', decoded: 'Three techniques: state (2m) + develop (2m) + example (1m).', marks: 15 },
    ],
    cite: CITE('Q8'),
  },
];

const BUSINESS_LENS: SubjectLens = {
  subjectId: 'business',
  entries: [...SHORTS, ...LONGS_EV, ...mirrorIV(LONGS_EV, 'LC033ALP041IV.pdf')],
};

export default BUSINESS_LENS;
