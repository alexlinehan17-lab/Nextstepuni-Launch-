/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Economics (Ordinary Level).
 *
 * Sources of truth (both in examiner-reports/economics/):
 *  - 2025-ol-marking-scheme.md/.pdf — SEC Marking Scheme 2025, Economics Ordinary Level
 *  - 2023-ol-marking-scheme.md/.pdf — SEC Marking Scheme 2023, Economics Ordinary Level
 *
 * Honesty rules (see types.ts): every `notation` below is the scheme's own Max
 * Mark tokens VERBATIM (whitespace normalised only); `decoded` restates ONLY
 * what those marks allocate — no advice, no model answers. Every entry's parts
 * sum EXACTLY to its totalMarks (machine-checked in test/markingLens.test.ts).
 * The part↔mark binding was resolved by PyMuPDF table extraction of the marking
 * table (the printed Max Mark column), not from the flattened .md.
 *
 * No `pitfall` is attached: there is no filed Economics Chief Examiner's Report,
 * so nothing meets the documented-behaviour bar the honesty rules require.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2025 OL (LC034GLP000EV + IV mirror) Q1–16
 *  - 2023 OL (LC034GLP000EV + IV mirror) Q1–16
 * Both papers are a single booklet: Section A = Q1–Q10 (12 marks each),
 * Section B = Q11–Q16 (75 marks each = parts (a)+(b)+(c)). A Section A question
 * that reads "Answer either (a) or (b)" is ONE 12-mark part (you answer one
 * option), with the notation showing whichever option's mark pattern applies —
 * never listed as two summing 12-mark parts.
 */

import { type LensPart, type QuestionLens, type SubjectLens } from './types';

const EV_FILEID = 'LC034GLP000EV.pdf';
const IV_FILEID = 'LC034GLP000IV.pdf';

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

const CITE_2025 = (q: string) => `SEC Marking Scheme 2025, Economics Ordinary Level, ${q}`;
const CITE_2023 = (q: string) => `SEC Marking Scheme 2023, Economics Ordinary Level, ${q}`;

// A Section A short question: one 12-mark part, marked as the scheme shows.
const secA = (
  year: number,
  citeFn: (q: string) => string,
) => (n: string, headline: string, task: string, notation: string, decoded: string): QuestionLens => ({
  year,
  level: 'ordinary',
  lang: 'ev',
  fileid: EV_FILEID,
  n,
  totalMarks: 12,
  headline,
  parts: [{ part: '', task, notation, decoded, marks: 12 }],
  cite: citeFn(`Section A Q${n}`),
});

// A Section B long question: three parts (a)/(b)/(c) summing to 75.
const secB = (
  year: number,
  citeFn: (q: string) => string,
) => (n: string, headline: string, parts: LensPart[]): QuestionLens => ({
  year,
  level: 'ordinary',
  lang: 'ev',
  fileid: EV_FILEID,
  n,
  totalMarks: 75,
  headline,
  parts,
  cite: citeFn(`Section B Q${n}`),
});

const part = (p: string, task: string, notation: string, decoded: string, marks: number): LensPart =>
  ({ part: p, task, notation, decoded, marks });

// ════════════════════════════════════════════════════════════════════════════
// 2025 Ordinary Level — single booklet
// Source: examiner-reports/economics/2025-ol-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const A25 = secA(2025, CITE_2025);
const B25 = secB(2025, CITE_2025);

const SECTION_A_2025: QuestionLens[] = [
  A25('1',
    'A 12-mark Section A question, marked (i) two points at 4 · (ii) one point at 4.',
    'Short question on a CSO release: state what the initials CSO stand for, and outline one economic benefit for Irish consumers of lower electricity prices (parts (i) and (ii)).',
    '(i) 2 @ 4 · (ii) 4',
    'Part (i): two elements at 4 marks each (8). Part (ii): one element, 4 marks.'),
  A25('2',
    'A 12-mark Section A question — answer either (a) or (b); whichever you pick is marked out of 12.',
    'Answer either (a) or (b): decide whether the Budget 2025 education measure is an efficient use of scarce resources — tick a box and justify your answer (or the (b) alternative).',
    'Either (a) or (b): 12',
    'Whichever option is answered is marked as a whole out of 12.'),
  A25('3',
    'A 12-mark Section A question — answer either (a) or (b); whichever you pick is marked out of 12.',
    'Answer either (a) or (b): (a) outline one private benefit or social benefit of the increased use of public libraries (tick which); (b) agree/disagree, with justification, that the Government should keep supporting international sporting events.',
    'Either (a) or (b): 12',
    'Whichever option is answered is marked as a whole out of 12.'),
  A25('4',
    'A 12-mark Section A question — answer either (a) or (b); whichever you pick is marked out of 12.',
    'Answer either (a) or (b): outline one reason the government introduced the Budget 2025 tax-threshold/USC/cost-of-living measures (or the (b) alternative).',
    'Either (a) or (b): 12',
    'Whichever option is answered is marked as a whole out of 12.'),
  A25('5',
    'A 12-mark Section A question, marked (i) 4 · (ii) 8.',
    '(i) State what the initials GDP stand for; (ii) outline one advantage of an increasing GDP for citizens in Ireland.',
    '(i) 4 · (ii) 8',
    'Part (i): 4 marks. Part (ii): one point developed, 8 marks.'),
  A25('6',
    'A 12-mark Section A question, marked 1st point at 8 · 2nd point at 4.',
    'Outline one private cost to the individual and one social cost to society of the use of disposable vapes.',
    '1st x 8 · 2nd x 4',
    'Two points: the first 8 marks, the second 4.'),
  A25('7',
    'A 12-mark Section A question, marked (i) 4 · (ii) 8.',
    '(i) Calculate the percentage increase in the number of people aged 65 and over from 2014 to 2024 (show workings); (ii) outline one possible economic effect of this increase for the Irish Government.',
    '(i) 4 · (ii) 8',
    'Part (i): 4 marks. Part (ii): one point developed, 8 marks.'),
  A25('8',
    'A 12-mark Section A question, marked 1st point at 8 · 2nd point at 4.',
    'Identify with a tick which listed firm is a monopoly, then outline one possible barrier to entry in a monopoly market structure.',
    '1st x 8 · 2nd x 4',
    'Two points: the first 8 marks, the second 4.'),
  A25('9',
    'A 12-mark Section A question, marked as two items at 6 marks each.',
    'Indicate by a tick whether each listed good is a substitute or a complement for the Apple Watch Series 10, and explain the reason for each choice.',
    '2 @ 6',
    'Two items, 6 marks each.'),
  A25('10',
    'A 12-mark Section A question, marked (i) 8 · (ii) 4.',
    '(i) Outline one factor, other than ticket prices, that would affect a consumer’s demand for the concert; (ii) explain the reason for the shape of the ticket supply curve.',
    '(i) 8 · (ii) 4',
    'Part (i): 8 marks. Part (ii): 4 marks.'),
];

const SECTION_B_2025: QuestionLens[] = [
  B25('11', 'Three parts — (a) 20 · (b) 32 · (c) 23 — on perfect competition.', [
    part('(a)', 'Explain the economic term “homogenous product” and give one example; then outline points on firms operating in perfect competition.',
      '(i) 6 · (ii) 1st x 10 · 2nd x 4',
      'Part (i): 6 marks. Part (ii): two points, the first 10 marks, the second 4.', 20),
    part('(b)', 'Perfect-competition long-run equilibrium diagram: write out in full any three of the four diagram labels, mark the equilibrium point, and give the related short points.',
      '(i) 24 [3 @ 8] · (ii) 4 · (iii) 4',
      'Part (i): three items at 8 marks each (24). Part (ii): 4 marks. Part (iii): 4 marks.', 32),
    part('(c)', 'Dublin Airport passenger cap: outline one reason, in your opinion, for the limit, and the further points the scheme allocates.',
      '(i) 10 · (ii) 1st x 7 · 2nd x 3 · 3rd x 3',
      'Part (i): 10 marks. Part (ii): three points at 7, 3 and 3 marks.', 23),
  ]),
  B25('12', 'Three parts — (a) 21 · (b) 28 · (c) 26 — on public finance and national income.', [
    part('(a)', 'Government expenditure pie chart: calculate capital expenditure as a percentage of total government expenditure (show workings), plus the short related point.',
      '(i) 16 · (ii) 5',
      'Part (i): 16 marks. Part (ii): 5 marks.', 21),
    part('(b)', 'National Income: state what C, G and X stand for; calculate the multiplier for an open economy using MPS 0.2 and MPM 0.3; plus the short point.',
      '(i) 12 · (ii) 12 [4 @ 3] · (iii) 4',
      'Part (i): 12 marks. Part (ii): four elements at 3 marks each (12). Part (iii): 4 marks.', 28),
    part('(c)', 'European Central Bank: state what ECB stands for and outline its aim(s), then treat the effects of the ECB interest-rate cut.',
      '(i) 12 [3 @ 4] · (ii) 4 · (iii) 10 [1st x 6 · 2nd x 4]',
      'Part (i): three elements at 4 marks each (12). Part (ii): 4 marks. Part (iii): two points at 6 and 4 marks (10).', 26),
  ]),
  B25('13', 'Three parts — (a) 26 · (b) 23 · (c) 26 — on the labour market and MNCs.', [
    part('(a)', 'Labour and skills shortages: explain the factor of production labour; state and treat the sectors experiencing shortages; plus the further point.',
      '(i) 7 · (ii) 12 [1st @ 8 · 2nd @ 4] · (iii) 7',
      'Part (i): 7 marks. Part (ii): 12 marks (first point 8, second 4). Part (iii): 7 marks.', 26),
    part('(b)', 'Draw and label the AC, MC and MR curves for the firm from the given data (complete the axes); then explain the meaning of marginal cost or marginal revenue.',
      '(i) 17 [Axes · 2 @ 2 · MC: 5 · MC: 5 · MR: 3] · (ii) 6',
      'Part (i): 17 marks for the drawing — the axes (two at 2 marks) and the three marked cost/revenue lines (5, 5 and 3). Part (ii): 6 marks.', 23),
    part('(c)', 'Apple €14bn tax money: state two other MNCs operating in Ireland, and treat the further points the scheme allocates.',
      '(i) 12 [1st @ 8 · 2nd @ 4] · (ii) 14 [2 @ 7]',
      'Part (i): 12 marks (first point 8, second 4). Part (ii): two points at 7 marks each (14).', 26),
  ]),
  B25('14', 'Three parts — (a) 26 · (b) 26 · (c) 23 — on international trade and development.', [
    part('(a)', 'Customs duties: explain the economic term customs duties; outline two reasons imports are important to the Irish economy; plus the short point.',
      '(i) 6 · (ii) 16 [1st @ 10 · 2nd @ 6] · (iii) 4',
      'Part (i): 6 marks. Part (ii): two points at 10 and 6 marks (16). Part (iii): 4 marks.', 26),
    part('(b)', 'Overseas Development Assistance (ODA): comment on the overall trend of Irish ODA; suggest two actions LDC governments can take to improve citizens’ welfare.',
      '(i) 16 · (ii) 10 [1st @ 6 · 2nd @ 4]',
      'Part (i): 16 marks. Part (ii): two actions at 6 and 4 marks (10).', 26),
    part('(c)', 'Human Development Index data (2003 vs 2022): treat the data as the scheme sets out across parts (i) and (ii).',
      '(i) 13 · (ii) 10',
      'Part (i): 13 marks. Part (ii): 10 marks.', 23),
  ]),
  B25('15', 'Three parts — (a) 24 · (b) 30 · (c) 21 — on enterprise, the housing market and government debt.', [
    part('(a)', 'Entrepreneurs and the Irish economy: explain the term entrepreneur; tick agree/disagree on the statement; justify with the points the scheme allocates.',
      '(i) 10 · (ii) 4 · (iii) 10',
      'Part (i): 10 marks. Part (ii): 4 marks. Part (iii): 10 marks.', 24),
    part('(b)', 'Housing market diagram: show and explain the effect of the forecast population increase on the demand for housing; plus a further point; then outline one positive or negative effect of the Quays car restriction for Dublin residents (justify).',
      '(i) 14 [8 + 4 + 2] · (ii) 10 · (iii) 6',
      'Part (i): 14 marks (8 + 4 + 2). Part (ii): 10 marks. Part (iii): 6 marks.', 30),
    part('(c)', 'Government debt reduction: outline one economic benefit for the Irish government and one for citizens of the reduction, plus the further point.',
      '(i) 14 [1st @ 8 · 2nd @ 6] · (ii) 7',
      'Part (i): two benefits at 8 and 6 marks (14). Part (ii): 7 marks.', 21),
  ]),
  B25('16', 'Three parts — (a) 22 · (b) 29 · (c) 24 — on taxation, inflation and climate change.', [
    part('(a)', 'Excise duty & VAT on cigarettes: indicate whether they are a direct or indirect tax and explain; then outline one negative effect for the Irish economy of continuing to raise VAT on alcohol and tobacco.',
      '(i) 4 · (ii) 10 · (iii) 8',
      'Part (i): 4 marks. Part (ii): 10 marks. Part (iii): 8 marks.', 22),
    part('(b)', 'CPI inflation chart (May–Sep 2024): state what the letters CPI stand for and the related point; plus the further parts the scheme allocates.',
      '(i) 5 [1st @ 3 · 2nd @ 2] · (ii) 12 · (iii) 12 [1st @ 8 · 2nd @ 4]',
      'Part (i): 5 marks (3 + 2). Part (ii): 12 marks. Part (iii): two points at 8 and 4 marks (12).', 29),
    part('(c)', 'Climate change: identify one action each named sector of the economy could take to reduce climate-change effects (justify); then suggest one measure to promote Balanced Regional Development.',
      '(i) 18 [12 (2 @ 6) · 6] · (ii) 6',
      'Part (i): 18 marks (two points at 6, plus 6). Part (ii): 6 marks.', 24),
  ]),
];

// ════════════════════════════════════════════════════════════════════════════
// 2023 Ordinary Level — single booklet
// Source: examiner-reports/economics/2023-ol-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const A23 = secA(2023, CITE_2023);
const B23 = secB(2023, CITE_2023);

const SECTION_A_2023: QuestionLens[] = [
  A23('1',
    'A 12-mark Section A question, marked (i) 8 · (ii) 4.',
    'Unemployment-rate graph (Jul 2022–Jan 2023): identify the month unemployment was at its lowest, and comment on the unemployment rate over the period using figures from the chart.',
    '(i) 8 · (ii) 4',
    'Part (i): 8 marks. Part (ii): 4 marks.'),
  A23('2',
    'A 12-mark Section A question — answer either (a) or (b); each option is marked 1st point at 8 · 2nd point at 4.',
    'Answer either (a) or (b): outline two effects on the Irish consumer of KBC Bank and Ulster Bank leaving the Irish banking market (or the (b) alternative).',
    '(a) 1st @ 8 · 2nd @ 4  —or—  (b) 1st @ 8 · 2nd @ 4',
    'Whichever option is answered: two points, the first 8 marks, the second 4.'),
  A23('3',
    'A 12-mark Section A question — answer either (a) or (b); whichever you pick is marked out of 12.',
    'Answer either (a) or (b): (a)(i) identify one area of skills shortage in Ireland and (ii) outline one economic effect of a skilled-labour shortage; or the (b) alternative.',
    '(a) (i) 8 · (ii) 4  —or—  (b) 1st @ 8 · 2nd @ 4',
    'Option (a): (i) 8 marks, (ii) 4 marks. Option (b): two points at 8 and 4 marks.'),
  A23('4',
    'A 12-mark Section A question — answer either (a) or (b); whichever you pick is marked out of 12.',
    'Answer either (a) or (b): (a)(i) identify with a tick which listed firm is a monopoly and (ii) explain the term monopoly (or outline two characteristics); or the (b) alternative.',
    '(a) (i) 8 · (ii) 4  —or—  (b) 1st @ 8 · 2nd @ 4',
    'Option (a): (i) 8 marks, (ii) 4 marks. Option (b): two points at 8 and 4 marks.'),
  A23('5',
    'A 12-mark Section A question, marked as one answer out of 12.',
    'Rugby World Cup ticket supply diagram: explain the relationship between the price of tickets and the supply of tickets.',
    '12',
    'The explanation is marked as a whole out of 12.'),
  A23('6',
    'A 12-mark Section A question, marked (i) two points at 4 · (ii) one point at 4.',
    '(i) State what the initials GDP stand for; (ii) outline one advantage of increasing GDP for the Irish economy.',
    '(i) 2 @ 4 · (ii) 4',
    'Part (i): two elements at 4 marks each (8). Part (ii): one element, 4 marks.'),
  A23('7',
    'A 12-mark Section A question, marked 1st point at 8 · 2nd point at 4.',
    'Explain two reasons why the government in Ireland collects tax.',
    '1st @ 8 · 2nd @ 4',
    'Two reasons: the first 8 marks, the second 4.'),
  A23('8',
    'A 12-mark Section A question, marked (i) 4 + 2 · (ii) 4 + 2.',
    '(i) Name two of the three areas the Human Development Index measures; (ii) in your opinion, name one area of government expenditure that has helped Ireland’s HDI ranking and explain.',
    '(i) 1st @ 4 · 2nd @ 2 · (ii) 1st @ 4 · 2nd @ 2',
    'Part (i): two elements at 4 and 2 marks (6). Part (ii): 4 + 2 marks (6).'),
  A23('9',
    'A 12-mark Section A question, marked 1st point at 8 · 2nd point at 4.',
    '(i) Explain the term opportunity cost; (ii) outline one opportunity cost of the government’s €2.3bn spend on social and affordable housing.',
    '1st @ 8 · 2nd @ 4',
    'Two points: the first 8 marks, the second 4.'),
  A23('10',
    'A 12-mark Section A question, marked 1st point at 8 · 2nd point at 4.',
    'State one private benefit and one social benefit if the government’s intervention to reduce teenage vaping is successful.',
    '1st @ 8 · 2nd @ 4',
    'Two points: the first 8 marks, the second 4.'),
];

const SECTION_B_2023: QuestionLens[] = [
  B23('11', 'Three parts — (a) 20 · (b) 35 · (c) 20 — on monopolistic competition and the hidden economy.', [
    part('(a)', 'Outline two reasons the hair and beauty industries are an example of monopolistic competition; then outline two advantages for consumers of monopolistic competition.',
      '(i) 1st @ 6 · 2nd @ 4 · (ii) 1st @ 6 · 2nd @ 4',
      'Part (i): two reasons at 6 and 4 marks (10). Part (ii): two advantages at 6 and 4 marks (10).', 20),
    part('(b)', 'Long-run equilibrium diagram: write out in full the three numbered items; show and label the equilibrium; plus the short points the scheme allocates.',
      '(i) 3 @ 8 · (ii) 1st @ 4 · 2nd @ 4 · 3rd @ 1 · (iii) 1 · 1',
      'Part (i): three items at 8 marks each (24). Part (ii): three elements at 4, 4 and 1 marks (9). Part (iii): two 1-mark elements.', 35),
    part('(c)', 'Explain the term hidden economy and give one other example of a hidden-economy activity; then treat the further points the scheme allocates.',
      '(i) 6 · 4 · (ii) 1st @ 6 · 2nd @ 4',
      'Part (i): explanation 6 marks + example 4 marks (10). Part (ii): two points at 6 and 4 marks (10).', 20),
  ]),
  B23('12', 'Three parts — (a) 28 · (b) 20 · (c) 27 — on government revenue and a good tax system.', [
    part('(a)', 'Budget 2023 revenue pie chart: calculate the value(s) using the figures given, and treat the further points the scheme allocates.',
      '(i) 16 [6 @ 2 · Ans: 4] · (ii) 12 [4 @ 3]',
      'Part (i): 16 marks (six elements at 2, plus 4 for the answer). Part (ii): four elements at 3 marks each (12).', 28),
    part('(b)', 'Explain the term equity (a principle of a good tax system); then explain two other principles of a good tax system.',
      '(i) 8 · (ii) 1st @ 8 · 2nd @ 4',
      'Part (i): 8 marks. Part (ii): two principles at 8 and 4 marks (12).', 20),
    part('(c)', '€600 electricity credit: outline one benefit of the credit to the Irish household; plus the further points the scheme allocates.',
      '(i) 10 · (ii) 1st @ 10 · 2nd @ 4 · (iii) 3',
      'Part (i): 10 marks. Part (ii): two points at 10 and 4 marks (14). Part (iii): 3 marks.', 27),
  ]),
  B23('13', 'Three parts — (a) 22 · (b) 35 · (c) 18 — on exports, national income and interest rates.', [
    part('(a)', 'Food & drink exports bar chart: read and comment on the data as the scheme sets out across parts (i) and (ii).',
      '(i) 1st @ 8 · 2nd @ 4 · (ii) 1st @ 8 · 2nd @ 2',
      'Part (i): two points at 8 and 4 marks (12). Part (ii): two points at 8 and 2 marks (10).', 22),
    part('(b)', 'National Income formula: state what C and G represent; calculate the level of National Income for 2023 using the figures; plus the further points.',
      '(i) 2 @ 4 · (ii) 18 [6 @ 3] · (iii) 9 [3 @ 3]',
      'Part (i): two elements at 4 marks each (8). Part (ii): 18 marks (six elements at 3). Part (iii): three elements at 3 marks each (9).', 35),
    part('(c)', 'ECB interest-rate increase: explain how the increase affects consumers with Bank of Ireland mortgages; plus the further points the scheme allocates.',
      '(i) 8 · (ii) 8 · (iii) 2',
      'Part (i): 8 marks. Part (ii): 8 marks. Part (iii): 2 marks.', 18),
  ]),
  B23('14', 'Three parts — (a) 22 · (b) 30 · (c) 23 — on petrol prices, output/revenue and costs.', [
    part('(a)', 'Petrol prices (Apr–Sep 2022) line graph: comment on one key trend in the price of petrol, and treat the further points the scheme allocates.',
      '(i) 10 [6 + 4] · (ii) 1st @ 8 · 2nd @ 4',
      'Part (i): 10 marks (6 + 4). Part (ii): two points at 8 and 4 marks (12).', 22),
    part('(b)', 'Portable-chargers cost/revenue table: calculate the total revenue at the given output; plus the further points the scheme allocates.',
      '(i) 18 [3 @ 6] · (ii) 9 [3 @ 3] · (iii) 3',
      'Part (i): 18 marks (three elements at 6). Part (ii): 9 marks (three elements at 3). Part (iii): 3 marks.', 30),
    part('(c)', 'Explain the terms fixed costs and variable costs and state one example of each; plus the further point the scheme allocates.',
      '6 · 3 · 6 · 3 · 5',
      'Fixed costs 6 + example 3; variable costs 6 + example 3; plus a further point worth 5.', 23),
  ]),
  B23('15', 'Three parts — (a) 25 · (b) 30 · (c) 20 — on vehicle data and the market for electric cars.', [
    part('(a)', 'Vehicles licensed 2021 infographic: calculate private cars as a percentage of the total vehicles licensed, and treat the further points the scheme allocates.',
      '(i) 20 [5 @ 4] · (ii) 5',
      'Part (i): 20 marks (five elements at 4). Part (ii): 5 marks.', 25),
    part('(b)', 'Market for electric cars: draw and label the market demand curve (include the axes); show and explain the effect of a rise in consumer income; explain one other factor affecting demand.',
      '(i) 16 [4 @ 4] · (ii) 9 [6 + 3] · (iii) 5',
      'Part (i): 16 marks (four elements at 4). Part (ii): 9 marks (6 + 3). Part (iii): 5 marks.', 30),
    part('(c)', 'Electric vehicles by 2030: outline two ways the Irish government may influence consumers; plus the further point the scheme allocates.',
      '(i) 1st @ 8 · 2nd @ 4 · (ii) 8',
      'Part (i): two ways at 8 and 4 marks (12). Part (ii): 8 marks.', 20),
  ]),
  B23('16', 'Three parts — (a) 30 · (b) 21 · (c) 24 — on factors of production, economic goods and food waste.', [
    part('(a)', 'Keogh’s Crisps factors of production: complete the table (explanation + example) for the four factors; then, in your opinion, are entrepreneurs important to the development of the Irish economy — tick and explain.',
      '(i) 24 [6 @ 4] · (ii) 2 · 4',
      'Part (i): six table cells at 4 marks each (24). Part (ii): 2 marks + 4 marks (6).', 30),
    part('(b)', 'Economic goods: explain any two of the terms scarce, transferable and utility (with reference to Keogh’s Crisps); then explain the term economies of scale with reference to Keogh’s Crisps.',
      '(i) 2 @ 7 · (ii) 7',
      'Part (i): two terms at 7 marks each (14). Part (ii): 7 marks.', 21),
    part('(c)', 'Food waste: outline one cost to society of wasting food, and treat the further points the scheme allocates across parts (i)–(iii).',
      '(i) 8 · (ii) 8 · (iii) 8',
      'Part (i): 8 marks. Part (ii): 8 marks. Part (iii): 8 marks.', 24),
  ]),
];

const EV_ENTRIES: QuestionLens[] = [
  ...SECTION_A_2025,
  ...SECTION_B_2025,
  ...SECTION_A_2023,
  ...SECTION_B_2023,
];

const ECONOMICS_LENS: SubjectLens = {
  subjectId: 'economics',
  entries: [
    ...EV_ENTRIES,
    ...mirrorIV(EV_ENTRIES, IV_FILEID),
  ],
};

export default ECONOMICS_LENS;
