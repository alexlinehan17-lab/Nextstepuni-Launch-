/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Business (pilot / golden file).
 *
 * Sources of truth (all in examiner-reports/business/):
 *  - 2024-marking-scheme.md    — SEC Marking Scheme 2024, Business Higher Level
 *  - 2025-marking-scheme.md    — SEC Marking Scheme 2025, Business Higher Level
 *  - 2025-ol-marking-scheme.md — SEC Marking Scheme 2025, Business Ordinary Level
 * Every notation below is verbatim from the named document; every entry's
 * parts sum to its Available Marks line (machine-checked). Pitfalls cite the
 * Chief Examiner's Report 2015 (Business HL) — the same sourced insights
 * surfaced in examinerInsights.ts.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2024 HL Paper 1 (LC033ALP032EV) Q1–12 — Section 1 short answers, 10m each.
 *  - 2024 HL Paper 2 (LC033ALP041EV + IV mirror) Q1–8 — 60m long questions.
 *  - 2025 HL Paper 2 (LC033ALP041EV + IV mirror) Q1–8 — Section 3, 60m each.
 *    (2025 HL Section 1 / Section 2 ABQ are untagged, so carry no lens; Q1 is
 *    skipped — see note at LONGS_2025_HL_EV.)
 *  - 2025 OL Paper 2 (LC033GLP033EV + IV mirror) Q1–9 — Section 2, 75m each.
 *    (2025 OL Section 1 shorts are untagged, so carry no lens.)
 */

import { type LensPart, type QuestionLens, type SubjectLens } from './types';

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

// ════════════════════════════════════════════════════════════════════════════
// 2025 Higher Level — Section 3 long questions (Paper 2, 60 marks each)
// Source: examiner-reports/business/2025-marking-scheme.md
// ════════════════════════════════════════════════════════════════════════════

const CITE_2025_HL = (q: string) => `SEC Marking Scheme 2025, Business Higher Level, ${q}`;

// Q1 is deliberately SKIPPED: the scheme prints part (C) as "8+4 / 8marks
// (3+3+1+1)" against a 20-mark part total — the printed notation cannot be
// made to sum to 20 without guessing, so per the honesty rules it gets no lens.
const LONGS_2025_HL_EV: QuestionLens[] = [
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '2',
    totalMarks: 60,
    headline: 'Three 20-mark parts; the “Illustrate” part grades its four types on a sliding (4+1)/(3+2) grid.',
    parts: [
      { part: '(A)', task: 'Illustrate the types of business organisations (Partnership, Sole Trader, Franchise, Public Limited Company)', notation: '4@5 (4+1), (4+1), (3+2), (3+2)', decoded: 'Four types, 5 marks each: two marked explain 4 + example 1, two marked explain 3 + example 2.', marks: 20 },
      { part: '(B)', task: 'Discuss the benefits and challenges of increasing employment for Irish businesses', notation: '4@5 (2+3)', decoded: 'Four points, 5 marks each: name (2m) + explain (3m) — the scheme requires two benefits and two challenges.', marks: 20 },
      { part: '(C)', task: 'Outline how the Irish government could create a positive climate for business, with examples', notation: '4@5 (2+2+1)', decoded: 'Four ways: name (2m) + explain (2m) + example (1m).', marks: 20 },
    ],
    cite: CITE_2025_HL('Section 3 Q2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '3',
    totalMarks: 60,
    headline: 'Three 20-mark parts; part (A) splits 14/6 between the two EU forms of law and one explained impact.',
    parts: [
      { part: '(A)(i)', task: 'Describe, with examples, the difference between an EU directive and an EU regulation', notation: '2@7 (4+3)', decoded: 'Both forms of law treated, 7 marks each: feature (4m) + example (3m).', marks: 14 },
      { part: '(A)(ii)', task: 'Explain the impact of an established EU directive on Irish businesses', notation: '1@6 (3+3)', decoded: 'One impact explained, in two 3-mark elements.', marks: 6 },
      { part: '(B)', task: 'Outline the global marketing mix for a product of your choice', notation: '4@5 (2+2+1)', decoded: 'Four mix elements: element (2m) + explain (2m) + example (1m).', marks: 20 },
      { part: '(C)', task: 'Illustrate the barriers to free trade (Embargo, Quota, Subsidy, Tariff)', notation: '4@5 (4+1), (4+1), (3+2), (3+2)', decoded: 'Four barriers, 5 marks each: two marked explain 4 + example 1, two marked explain 3 + example 2.', marks: 20 },
    ],
    cite: CITE_2025_HL('Section 3 Q3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '4',
    totalMarks: 60,
    headline: 'Three 20-mark parts; the contract “Illustrate” grid pays (4+1) for the first two methods, (3+2) after.',
    parts: [
      { part: '(A)', task: 'Illustrate the methods of terminating a contract (Performance, Frustration, Breach of contract, Agreement)', notation: '4@5 (4+1), (4+1), (3+2), (3+2)', decoded: 'Four methods, 5 marks each: two marked explain 4 + example 1, two marked explain 3 + example 2.', marks: 20 },
      { part: '(B)', task: 'Explain, using an example, the grounds for fair dismissal (Unfair Dismissals Act 1977/2015)', notation: '4@5 (2+2+1)', decoded: 'Four grounds: ground (2m) + explain (2m) + example (1m).', marks: 20 },
      { part: '(C)(i)', task: 'Explain the term a competitive relationship', notation: '3+3', decoded: 'Two 3-mark elements of the explanation.', marks: 6 },
      { part: '(C)(ii)', task: 'Explain the benefits of competitive relationships between two suppliers and between two employees', notation: '2@7 (4+3)', decoded: 'Both relationships treated, 7 marks each: benefit (4m) + development (3m).', marks: 14 },
    ],
    cite: CITE_2025_HL('Section 3 Q4'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '5',
    totalMarks: 60,
    headline: 'Three 20-mark parts, every point on a 2+3 grid — including the SWOT, marked name + reference.',
    parts: [
      { part: '(A)', task: 'Discuss the factors to consider when choosing an effective communication medium', notation: '4@5 (2+3)', decoded: 'Four factors, 5 marks each: name (2m) + explain (3m).', marks: 20 },
      { part: '(B)', task: 'Conduct a SWOT analysis for a business of your choice', notation: '4@5 (2+3)', decoded: 'Four SWOT headings, 5 marks each: name (2m) + reference (3m).', marks: 20 },
      { part: '(C)(i)', task: 'Outline the implications of a manager adopting McGregor’s Theory X approach', notation: '2@5 (2+3)', decoded: 'Two implications, 5 marks each: name (2m) + explain (3m).', marks: 10 },
      { part: '(C)(ii)', task: 'Explain the factors that influence a manager to adopt a Theory X approach', notation: '2@5 (2+3)', decoded: 'Two factors, 5 marks each: name (2m) + explain (3m).', marks: 10 },
    ],
    cite: CITE_2025_HL('Section 3 Q5'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '6',
    totalMarks: 60,
    headline: 'Two 20-mark discussion parts, then a 20-mark tax calculation split 10/6/2/2 across PAYE, USC, PRSI and net pay.',
    parts: [
      { part: '(A)', task: 'Outline the types of insurance The Royal Oak Hotel should have in place', notation: '4@5 (4+1), (4+1), (3+2), (3+2)', decoded: 'Four types, 5 marks each: two marked name 4 + explain 1, two marked name 3 + explain 2.', marks: 20 },
      { part: '(B)', task: 'Discuss the strategies used to manage change in a business', notation: '4@5 (2+3)', decoded: 'Four strategies, 5 marks each: name (2m) + explain (3m).', marks: 20 },
      { part: '(C)(i)', task: 'Calculate the PAYE Gemma has to pay (show workings)', notation: '10 marks', decoded: 'Ten marks spread across the worked PAYE elements — workings carry the marks, and own figures earn marks.', marks: 10 },
      { part: '(C)(ii)', task: 'Calculate the total amount of USC paid', notation: '6 marks', decoded: 'Six marks across the worked USC elements.', marks: 6 },
      { part: '(C)(iii)', task: 'Calculate the total amount of PRSI paid', notation: '2 marks', decoded: 'Two marks for the PRSI calculation.', marks: 2 },
      { part: '(C)(iv)', task: 'Calculate Gemma’s net annual take-home pay', notation: '2 marks', decoded: 'Two marks: total deductions (1m) + net take-home figure (1m).', marks: 2 },
    ],
    cite: CITE_2025_HL('Section 3 Q6'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '7',
    totalMarks: 60,
    headline: 'Applied question (Glanbia / Anthem Transport): the third mark of each development stage is the link to the business.',
    parts: [
      { part: '(A)', task: 'Discuss the advantages and disadvantages of an acquisition (takeover) as a method of expansion', notation: '4@5 (2+3)', decoded: 'Four points, 5 marks each: name (2m) + explain (3m) — the scheme requires two of each.', marks: 20 },
      { part: '(B)', task: 'Illustrate four stages, apart from launch, that Glanbia may use for developing a new product', notation: '4@5 (2+2+1)', decoded: 'Four stages: name (2m) + explain (2m) + reference/example to the business (1m).', marks: 20 },
      { part: '(C)', task: 'Discuss how Anthem Transport Ltd could use different medium-term sources of finance', notation: '3@6 (3+3) + 2@1m', decoded: 'Three sources, 6 marks each (source 3m + explain 3m), plus 1 mark each for two uses of medium-term finance.', marks: 20 },
    ],
    pitfall: {
      text: 'Defining a term well but failing to apply it to the context asked for — recall did not match application, and the application marks are separate.',
      cite: "Chief Examiner's Report 2015 (Business HL), p.14",
    },
    cite: CITE_2025_HL('Section 3 Q7'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC033ALP041EV.pdf', n: '8',
    totalMarks: 60,
    headline: 'A 25-mark breakeven chart where the drawing itself carries 13 of the marks — calculations alone stop at 12.',
    parts: [
      { part: '(A)(i)', task: 'Explain the term product portfolio', notation: '6 (3+3)', decoded: 'Two 3-mark elements of the explanation.', marks: 6 },
      { part: '(A)(ii)', task: 'Illustrate the methods of market segmentation used by businesses such as Proctor and Gamble', notation: '2@7 (2+3+2)', decoded: 'Two methods, 7 marks each: method (2m) + explain (3m) + reference (2m).', marks: 14 },
      { part: '(B)', task: 'Describe the reasons for conducting market research', notation: '3@5 (3+2)', decoded: 'Three reasons, 5 marks each: name (3m) + explain (2m).', marks: 15 },
      { part: '(C)', task: 'Illustrate breakeven point, margin of safety and profit at forecast output by means of a breakeven chart', notation: 'Title 2m, Axis 1m, Axis 1m, FC 3m, TC 3m, TR 3m, BEP 4m, Profit at FO 4m, MoS 4m — OR Calculations only: BEP 4m, Profit at FO 4m, MoS 4m', decoded: 'The chart route pays title, both axes and the FC/TC/TR lines (13m) plus 4m each for BEP, profit at forecast output and margin of safety; calculations without the chart earn only those last three (12m).', marks: 25 },
    ],
    cite: CITE_2025_HL('Section 3 Q8'),
  },
];

// ════════════════════════════════════════════════════════════════════════════
// 2025 Ordinary Level — Section 2 long questions (Paper 2, 75 marks each)
// Source: examiner-reports/business/2025-ol-marking-scheme.md
// ════════════════════════════════════════════════════════════════════════════

const CITE_2025_OL = (q: string) => `SEC Marking Scheme 2025, Business Ordinary Level, ${q}`;

// The OL scheme's standard two-point part: first point 10 (7+3), second 5 (4+1).
const olTwo = (part: string, task: string): LensPart => ({
  part,
  task,
  notation: '10 Marks (7m + 3m) · 5 Marks (4m + 1m)',
  decoded: 'Two points: the first earns 10 marks (7 for the point + 3 development), the second earns 5 (4 + 1).',
  marks: 15,
});

const olQ = (n: string, headline: string, parts: LensPart[]): QuestionLens => ({
  year: 2025,
  level: 'ordinary',
  lang: 'ev',
  fileid: 'LC033GLP033EV.pdf',
  n,
  totalMarks: 75,
  headline,
  parts,
  cite: CITE_2025_OL(`Section 2 Q${n}`),
});

const LONGS_2025_OL_EV: QuestionLens[] = [
  olQ('1', 'Five 15-mark consumer-law parts; every two-point part pays 10 (7+3) for the first point and 5 (4+1) for the second.', [
    olTwo('(A)', 'Explain, using examples, two provisions of the Sale of Goods and Supply of Services Act 1980'),
    olTwo('(B)', 'Outline two forms of redress consumers are entitled to if the Act’s provisions are broken'),
    olTwo('(C)', 'Describe two advantages to a consumer of taking a case to the Small Claims Court'),
    olTwo('(D)', 'Outline two non-legislative steps a consumer might take to resolve the Ticketmaster overpricing issue'),
    olTwo('(E)', 'Outline two functions of the CCPC'),
  ]),
  olQ('2', 'Five 15-mark parts on the Wren Urban Nest text; part (C) splits 7/8 between the named sector and the other two.', [
    { part: '(A)', task: 'Outline one reward and one risk for Wren Urban Nest of being more environmentally friendly', notation: 'One reward: 10 Marks (7m + 3m) · One risk: 5 Marks (4m + 1m)', decoded: 'The reward earns 10 (7 + 3 development); the risk earns 5 (4 + 1).', marks: 15 },
    olTwo('(B)', 'Describe two benefits the hotel brings to the local economy'),
    { part: '(C)(i)', task: 'Name and explain the sector of the economy in which Wren Urban Nest operates', notation: '7 marks (4m + 3m)', decoded: 'Name (4m) + explanation (3m).', marks: 7 },
    { part: '(C)(ii)', task: 'List the other two sectors, giving an example of an occupation in each', notation: '8 marks (2m+2m) + (2m+2m)', decoded: 'Each of the two sectors: sector (2m) + example occupation (2m).', marks: 8 },
    olTwo('(D)', 'Explain two of the taxes mentioned in the diagram (Excise Duty, VAT, Carbon Tax)'),
    olTwo('(E)', 'Outline two ways in which the government helps Irish businesses'),
  ]),
  olQ('3', 'Five 15-mark parts; (C) hangs 14 of its 15 marks on the two explained effects after a 1-mark name.', [
    olTwo('(A)', 'Outline two reasons (other than corporation tax) why a multinational like Apple would locate in Ireland'),
    { part: '(B)', task: 'Outline one positive and one negative impact the EU’s top court ruling could have on the Irish economy', notation: 'One Positive: 10 Marks (7m + 3m) · One Negative: 5 Marks (4m + 1m)', decoded: 'The positive impact earns 10 (7 + 3 development); the negative earns 5 (4 + 1).', marks: 15 },
    { part: '(C)(i)', task: 'What is the official measure of inflation in Ireland?', notation: 'One Mark (1m)', decoded: 'One mark for naming the measure.', marks: 1 },
    { part: '(C)(ii)', task: 'Explain two effects a decrease in inflation would have on the consumer', notation: '@ 7 marks each (5m + 2m)', decoded: 'Two effects, 7 marks each: effect (5m) + development (2m).', marks: 14 },
    { part: '(D)(i)', task: 'Name three EU countries with which Ireland trades', notation: '7 marks (4m + 2m + 1m)', decoded: 'Three countries: the first 4m, then 2m and 1m.', marks: 7 },
    { part: '(D)(ii)', task: 'Outline two benefits to Ireland of exporting to EU countries', notation: '@ 4 Marks each (3m + 1m)', decoded: 'Two benefits, 4 marks each: benefit (3m) + development (1m).', marks: 8 },
    { part: '(E)', task: 'Explain the role of one EU institution (Parliament / Commission / Council)', notation: '10m + 5m', decoded: 'The explanation is marked in two elements: 10 marks + 5 marks.', marks: 15 },
  ]),
  olQ('4', 'Five 15-mark parts; the contract part pays 10 for the text-linked termination and 5 for the second way.', [
    olTwo('(A)', 'Outline two types of industrial action available to employees in a dispute'),
    olTwo('(B)', 'Outline the effects industrial action would have on any two stakeholders in the health service'),
    { part: '(C)(i)', task: 'Explain, with reference to the text, one way the McGrath family can terminate the contract', notation: '10 Marks (7m + 3m)', decoded: 'One way, tied to the text: 7 marks + 3 development.', marks: 10 },
    { part: '(C)(ii)', task: 'Explain one other way a contract can be terminated', notation: '5 Marks (4m + 1m)', decoded: 'One other way: 4 marks + 1 development.', marks: 5 },
    olTwo('(D)', 'Outline two grounds, other than race or sexual orientation, on which discrimination is outlawed (Employment Equality Acts)'),
    olTwo('(E)', 'Explain two functions of the Workplace Relations Commission (WRC)'),
  ]),
  olQ('5', 'Five 15-mark parts; (C) flattens to three 5-mark characteristics and (E) opens with a 3-mark definition.', [
    { part: '(A)', task: 'Outline one risk and one reward for Aimee of setting up her own business', notation: 'One risk: 10 Marks (7m + 3m) · One reward: 5 Marks (4m + 1m)', decoded: 'The risk earns 10 (7 + 3 development); the reward earns 5 (4 + 1).', marks: 15 },
    olTwo('(B)', 'Outline two other sources of new product/business ideas'),
    { part: '(C)', task: 'Outline three entrepreneurial characteristics/skills associated with entrepreneurs like Aimee', notation: '@ 5 marks each (4m + 1m)', decoded: 'Three characteristics, 5 marks each: 4m + 1m.', marks: 15 },
    olTwo('(D)', 'Outline two benefits for Aimee of using social media to communicate with her customers'),
    { part: '(E)(i)', task: 'Explain the term stock control', notation: '3 marks (3m)', decoded: 'Three marks for the explanation.', marks: 3 },
    { part: '(E)(ii)', task: 'Outline two reasons why stock control is important to a business like Sculpted', notation: '@ 6 marks each (5m + 1m)', decoded: 'Two reasons, 6 marks each: reason (5m) + development (1m).', marks: 12 },
  ]),
  olQ('6', 'Five 15-mark parts; the Notice-and-Agenda draft is marked element by element (4×1m + 5×2m + 1m).', [
    olTwo('(A)', 'State two advantages of meetings as a method of communication'),
    { part: '(B)(i)', task: 'Outline one duty of the Chairperson of a club', notation: '10 Marks (7m + 3m)', decoded: 'One duty: 7 marks + 3 development.', marks: 10 },
    { part: '(B)(ii)', task: 'Outline one duty of the Secretary of a club', notation: '5 Marks (4m + 1m)', decoded: 'One duty: 4 marks + 1 development.', marks: 5 },
    { part: '(C)', task: 'Draft the Notice and Agenda of the AGM of United Football Club (agenda: at least five items)', notation: 'Notice: 4 @1m each · Agenda: 5 @2marks each · Signed: 1 mark', decoded: 'Four 1-mark Notice elements, five 2-mark agenda items, and 1 mark for the signature.', marks: 15 },
    olTwo('(D)', 'Explain two reasons why a club should prepare a Cash Flow Forecast'),
    olTwo('(E)', 'Outline two sources the club could use to finance the building of a gym'),
  ]),
  olQ('7', 'Five 15-mark parts; the net-salary calculation is marked step by step (1m + 7×2m).', [
    { part: '(A)', task: 'Explain the terms ‘induction training’ and ‘on the job training’', notation: '10 Marks (7m + 3m) · 5 Marks (4m + 1m)', decoded: 'The first term earns 10 marks (7 + 3 development), the second 5 (4 + 1).', marks: 15 },
    olTwo('(B)', 'Explain two benefits for Dexcom of rewarding its employees'),
    olTwo('(C)', 'Outline any two steps in the recruitment and selection process before employing David Mulroy'),
    olTwo('(D)', 'Outline two differences between a salary and a wage'),
    { part: '(E)', task: 'Calculate David’s Annual Net Salary (show workings)', notation: '1m+2m+2m+2m+2m+2m+2m+2m', decoded: 'Eight worked elements: 1 mark, then seven 2-mark steps — the workings carry the marks.', marks: 15 },
  ]),
  olQ('8', 'Five 15-mark marketing parts; the Product Life Cycle diagram is marked element by element.', [
    olTwo('(A)', 'Outline two benefits to Cadbury of having a good brand name'),
    olTwo('(B)', 'Explain two factors a business should consider before setting the price of a product or service'),
    { part: '(C)(i)', task: 'Explain the term target market with reference to Cadbury', notation: '7 marks (4m+2m+1m)', decoded: 'Three elements: 4m + 2m + 1m.', marks: 7 },
    { part: '(C)(ii)', task: 'List two advertising media a business could use', notation: '8 marks (6m+2m)', decoded: 'Two media listed: 6m + 2m.', marks: 8 },
    olTwo('(D)', 'Name and explain two types of market research a business like Cadbury could have used'),
    { part: '(E)', task: 'Draw and label a Product Life Cycle diagram for a product such as Cadbury’s Dairy Milk', notation: 'Title 1m, Sales 1m, Time 1m, Curved line 2m, Labels (in order) 5 @2m each', decoded: 'Title and the Sales/Time axes 1m each, the curved line 2m, and the five stage labels in order 2m each.', marks: 15 },
  ]),
  olQ('9', 'Five 15-mark parts; (D) flattens to three 5-mark insurance terms.', [
    olTwo('(A)', 'Outline two reasons for a business like IKEA to expand its services'),
    olTwo('(B)', 'Outline two benefits to IKEA of completing a SWOT/SCOT analysis before its Click and Collect partnership'),
    olTwo('(C)', 'Explain two services that Enterprise Ireland provides to businesses'),
    { part: '(D)', task: 'Explain any three of the insurance terms underlined in the text', notation: '@ 5marks each (4m + 1m)', decoded: 'Three terms, 5 marks each: 4m + 1m.', marks: 15 },
    olTwo('(E)', 'Explain two of the insurance principles (insurable interest, indemnity, utmost good faith)'),
  ]),
];

const BUSINESS_LENS: SubjectLens = {
  subjectId: 'business',
  entries: [
    ...SHORTS,
    ...LONGS_EV,
    ...mirrorIV(LONGS_EV, 'LC033ALP041IV.pdf'),
    ...LONGS_2025_HL_EV,
    ...mirrorIV(LONGS_2025_HL_EV, 'LC033ALP041IV.pdf'),
    ...LONGS_2025_OL_EV,
    ...mirrorIV(LONGS_2025_OL_EV, 'LC033GLP033IV.pdf'),
  ],
};

export default BUSINESS_LENS;
