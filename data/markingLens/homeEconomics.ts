/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Home Economics (Scientific and Social).
 *
 * Sources of truth (all in examiner-reports/home-economics/):
 *  - 2025-marking-scheme.md/.pdf     — SEC Marking Scheme 2025, Home Economics S&S Higher Level
 *  - 2024-marking-scheme.md/.pdf     — SEC Marking Scheme 2024, Home Economics S&S Higher Level
 *  - 2025-ol-marking-scheme.md/.pdf  — SEC Marking Scheme 2025, Home Economics S&S Ordinary Level
 *  - 2024-ol-marking-scheme.md/.pdf  — SEC Marking Scheme 2024, Home Economics S&S Ordinary Level
 *
 * Honesty rules (see types.ts): every `notation` below is the scheme's own mark
 * tokens VERBATIM (whitespace normalised only, multiple printed notation lines
 * joined with " · "); `decoded` restates ONLY what those marks allocate — never
 * the model answer, never advice. Every entry's parts sum EXACTLY to its
 * totalMarks (machine-checked in test/markingLens.test.ts). The mark tokens were
 * read via PyMuPDF page-text extraction of each scheme PDF (the flattened .md
 * collapses the mark columns ambiguously), not from the .md.
 *
 * No `pitfall` is attached: there is no filed Home Economics Chief Examiner's
 * Report, so nothing meets the documented-behaviour bar the honesty rules require.
 *
 * ── SOLVED BOOKLET MAPPING (verified against the topic tags + the schemes) ──
 * Each sitting is served as TWO tagged booklets per level:
 *  - fileid  …LP014…  = Section A — the short questions. Every Section A question
 *    is worth 6 MARKS (the paper prints "Answer any ten questions … Each question
 *    carries 6 marks"; 14 questions are printed/tagged as n1..n14, and a candidate
 *    answers any ten). Each lens entry here is ONE 6-mark question.
 *  - fileid  …LP039…  = Section B — the long questions, tagged n1..n5.
 *    Q1 = 80 marks; Q2, Q3, Q4, Q5 = 50 marks each. Each long question is broken
 *    into its printed parts (a)/(b)/(c)/(d)/(e) with the part's own mark value.
 *  - Section C (electives) is NOT tagged in the vault and carries no lens.
 * HL fileids: LC098ALP014EV.pdf / LC098ALP039EV.pdf (+ …IV mirrors).
 * OL fileids: LC098GLP014EV.pdf / LC098GLP039EV.pdf (+ …IV mirrors).
 *
 * OL-vs-HL structure: identical here. Both 2025 OL and 2024 OL print "Each
 * question carries 6 marks" for Section A (same as HL — NOT a different OL value),
 * and the same Section B split (Q1=80, Q2–5=50). No structural divergence found.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2025 HL  Section A LC098ALP014EV Q1–14 · Section B LC098ALP039EV Q1–5  (+IV)
 *  - 2024 HL  Section A LC098ALP014EV Q1–14 · Section B LC098ALP039EV Q1–5  (+IV)
 *  - 2025 OL  Section A LC098GLP014EV Q1–14 · Section B LC098GLP039EV Q1–5  (+IV)
 *  - 2024 OL  Section A LC098GLP014EV Q1–14 · Section B LC098GLP039EV Q1–5  (+IV)
 * No questions skipped: every tagged n's parts reconcile exactly to its printed total.
 */

import { type LensPart, type QuestionLens, type SubjectLens } from './types';

// The IV paper is the same exam marked by the same scheme — mirror EV entries,
// deriving each IV fileid from its EV counterpart (…EV.pdf → …IV.pdf).
const mirrorIV = (entries: QuestionLens[]): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv' as const, fileid: e.fileid.replace('EV.pdf', 'IV.pdf') }));

const part = (p: string, task: string, notation: string, decoded: string, marks: number): LensPart =>
  ({ part: p, task, notation, decoded, marks });

type Level = 'higher' | 'ordinary';

// A Section A short question: one 6-mark part, marked as the scheme shows.
const secA = (year: number, level: Level, fileid: string, levelName: string) =>
  (n: string, headline: string, task: string, notation: string, decoded: string): QuestionLens => ({
    year,
    level,
    lang: 'ev',
    fileid,
    n,
    totalMarks: 6,
    headline,
    parts: [{ part: '', task, notation, decoded, marks: 6 }],
    cite: `SEC Marking Scheme ${year}, Home Economics – Scientific and Social ${levelName}, Section A Q${n}`,
  });

// A Section B long question: parts (a)/(b)/(c)… summing to totalMarks (80 for Q1,
// 50 for Q2–Q5).
const secB = (year: number, level: Level, fileid: string, levelName: string) =>
  (n: string, totalMarks: number, headline: string, parts: LensPart[]): QuestionLens => ({
    year,
    level,
    lang: 'ev',
    fileid,
    n,
    totalMarks,
    headline,
    parts,
    cite: `SEC Marking Scheme ${year}, Home Economics – Scientific and Social ${levelName}, Section B Q${n}`,
  });

// ════════════════════════════════════════════════════════════════════════════
// 2025 Higher Level
// Source: examiner-reports/home-economics/2025-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const A25H = secA(2025, 'higher', 'LC098ALP014EV.pdf', 'Higher Level');
const B25H = secB(2025, 'higher', 'LC098ALP039EV.pdf', 'Higher Level');

const SECTION_A_2025_HL: QuestionLens[] = [
  A25H('1', 'A 6-mark short question — two functions at 3 marks each.',
    'Describe two biological functions of carbohydrates.',
    '2 functions described @ 3 marks (graded 3:2:0)',
    'Two biological functions of carbohydrates, described, 3 marks each.'),
  A25H('2', 'A 6-mark short question — three table points at 2 marks each.',
    'Complete the table on the digestion of protein (organ, enzyme, substrate, product).',
    '3 points @ 2 marks (graded 2:1:0)',
    'Three completed table elements, 2 marks each.'),
  A25H('3', 'A 6-mark short question — two functions (4) plus two sources (2).',
    'State two biological functions of sodium; identify two dietary sources of sodium.',
    '2 functions @ 2 marks (graded 2:1:0) · 2 sources @ 1 mark (graded 1:0)',
    'Two functions of sodium at 2 marks each (4), plus two dietary sources at 1 mark each (2).'),
  A25H('4', 'A 6-mark short question — three vitamins at 2 marks each.',
    'Name one deficient vitamin for each named deficiency disease.',
    '3 correct vitamins @ 2 marks (graded 2:1:0)',
    'Three correct vitamins (one per deficiency), 2 marks each.'),
  A25H('5', 'A 6-mark short question — three guidelines at 2 marks each.',
    'Discuss three meal-planning guidelines for a person with coeliac disease.',
    '3 guidelines discussed @ 2 marks (graded 2:1:0)',
    'Three meal-planning guidelines, discussed, 2 marks each.'),
  A25H('6', 'A 6-mark short question — two methods at 3 marks each.',
    'Outline how each method of smoking fish (cold and hot) is carried out.',
    '2 methods outlined @ 3 marks (graded 3:2:1:0)',
    'Two smoking methods (cold, hot) outlined, 3 marks each.'),
  A25H('7', 'A 6-mark short question — two terms at 3 marks each.',
    'Explain the food-processing terms “added value foods” and “functional foods”.',
    '2 points explained @ 3 marks (graded 3:2:1:0)',
    'Two food-processing terms explained, 3 marks each.'),
  A25H('8', 'A 6-mark short question — name (2), description (3), example (1).',
    'Name and describe one method of heat transfer; give an example of a cooking method that shows it.',
    'Name @ 2 marks (graded 2:1:0) · Description 1 point @ 3 marks (graded 3:2:1:0) · Example 1 @ 1 mark (graded 1:0)',
    'The method named (2), a description point (3), and one cooking-method example (1).'),
  A25H('9', 'A 6-mark short question — two names (4) plus two functions (2).',
    'Name two physical conditioning agents (food additives) and give the function of each.',
    'Name @ 2 marks (graded 2:1:0) x 2 · Function @ 1 mark (graded 1:0) x 2',
    'Two agents named at 2 marks each (4), plus the function of each at 1 mark (2).'),
  A25H('10', 'A 6-mark short question — type named (3) plus one described point (3).',
    'Name and describe one type of life assurance.',
    '1 type @ 3 marks (graded 3:2:0) · 1 point @ 3 marks (graded 3:2:0)',
    'One type of life assurance named (3) and described in one point (3).'),
  A25H('11', 'A 6-mark short question — two points (4) plus two examples (2).',
    'Differentiate between essential and discretionary household expenditure; give one example of each.',
    '2 points @ 2 marks (graded 2:0) · 2 examples @ 1 mark (graded 1:0)',
    'Two differentiating points at 2 marks each (4), plus one example of each at 1 mark (2).'),
  A25H('12', 'A 6-mark short question — two types described at 3 marks each.',
    'Describe the types of consumer research (desk research, field research).',
    '2 points described @ 3 marks each (graded 3:2:1:0)',
    'Two types of consumer research described, 3 marks each.'),
  A25H('13', 'A 6-mark short question — two techniques described at 3 marks each.',
    'Describe how two supermarket merchandising techniques influence buying behaviour.',
    '2 described points @ 3 marks (graded 3:2:1:0)',
    'Two merchandising techniques described, 3 marks each.'),
  A25H('14', 'A 6-mark short question — two points discussed at 3 marks each.',
    'Discuss how a consumer is protected by the Consumer Credit Act 1995.',
    '2 discussed points @ 3 marks (graded 3:2:0)',
    'Two points on the Act’s protection, discussed, 3 marks each.'),
];

const SECTION_B_2025_HL: QuestionLens[] = [
  B25H('1', 80, 'Q1 (80 marks): (a) 20 · (b) 18 · (c) 12 · (d) 10 · (e) 20 — on energy sources and fatty acids.', [
    part('(a)', 'Comment and elaborate on four sources of energy in the diet of Irish adults, using the chart and healthy-eating guidelines.',
      '4 points @ 5 marks (graded 5:4:3:2:1:0)',
      'Four points, 5 marks each.', 20),
    part('(b)', 'Describe the structure and give one example of saturated, monounsaturated and polyunsaturated fatty acids.',
      '4 points on structure @ 1 mark (graded 1:0) x 3 · 1 example @ 2 marks (graded 2:0) x 3',
      'For each of the three fatty-acid types: up to four structure points at 1 mark (12 total) plus one example at 2 marks (6 total).', 18),
    part('(c)', 'Discuss the significance of fatty acids in the diet.',
      '3 points @ 4 marks (graded 4:3:2:1:0)',
      'Three points, 4 marks each.', 12),
    part('(d)', 'Give a detailed account of the formation of emulsions.',
      '5 points @ 2 marks (graded 2:1:0)',
      'Five points, 2 marks each.', 10),
    part('(e)', 'Analyse the factors that impact the food choices and eating habits of Irish adults.',
      '4 points @ 5 marks (graded 5:3:0)',
      'Four points, 5 marks each.', 20),
  ]),
  B25H('2', 50, 'Q2 (50 marks): (a) osteoporosis 18 + calcium absorption 15 · (b) cheese 17 — on bone health and dairy.', [
    part('(a)', 'Describe osteoporosis and discuss why a person might be at risk of developing it.',
      '2 points described @ 3 marks (graded 3:2:0) · 4 reasons discussed @ 3 marks (graded 3:2:0)',
      'Two description points at 3 marks (6) plus four risk reasons at 3 marks (12).', 18),
    part('(a)', 'Outline the factors that affect the absorption of calcium in the body.',
      '5 points @ 3 marks (graded 3:2:1:0)',
      'Five points, 3 marks each.', 15),
    part('(b)', 'Give a detailed account of the production of cheese (stages of production; packaging and labelling).',
      'Stages 6 points @ 2 marks (graded 2:1:0) · Packaging 2 points @ 1 mark (graded 1:0) · Labelling 3 points @ 1 mark (graded 1:0)',
      'Six production stages at 2 marks (12), two packaging points at 1 mark (2), three labelling points at 1 mark (3).', 17),
  ]),
  B25H('3', 50, 'Q3 (50 marks): (a) bacteria 18 · (b) storage/cooking 20 · (c) 2006 Regulations 12 — on food safety.', [
    part('(a)', 'Identify and give a detailed account of one food-poisoning bacteria (name, source, high-risk foods, factors affecting growth, symptoms).',
      'Name 1 @ 2 marks (graded 2:1:0) · Source 1 @ 2 marks (graded 2:1:0) · High-risk foods 2 @ 2 marks (graded 2:1:0) · Factors affecting growth 3 @ 2 marks (graded 2:1:0) · Symptoms 2 @ 2 marks (graded 2:1:0)',
      'Name (2), one source (2), two high-risk foods (4), three growth factors (6), two symptoms (4).', 18),
    part('(b)', 'Discuss the importance of correct food storage and cooking/reheating procedures in ensuring food is safe to eat.',
      '4 points @ 5 marks (graded 5:3:0)',
      'Four points, 5 marks each.', 20),
    part('(c)', 'Describe the protection provided by the European Communities (Hygiene of Foodstuffs) Regulations 2006 (amended 2009, 2010).',
      '3 points @ 4 marks (graded 4:2:0)',
      'Three points, 4 marks each.', 12),
  ]),
  B25H('4', 50, 'Q4 (50 marks): (a) 16 · (b) refrigeration study 22 · (c) 12 — on consumer behaviour and appliances.', [
    part('(a)', 'Discuss how consumers can be environmentally responsible when choosing, using and disposing of household appliances.',
      '4 points @ 4 marks (graded 4:2:0)',
      'Four points, 4 marks each.', 16),
    part('(b)', 'Set out details of a study on one refrigeration appliance (working principle; modern features).',
      'Working principle 5 points @ 3 marks (graded 3:2:1:0) · name @ 1 mark · Modern features 3 points @ 2 marks (graded 2:1:0)',
      'Working principle: five points at 3 marks plus 1 mark for naming the appliance (16); modern features: three points at 2 marks (6).', 22),
    part('(c)', 'Explain how the Sale of Goods and Supply of Services Act 1980 protects consumers buying electrical products.',
      '3 points @ 4 marks (graded 4:2:0)',
      'Three points, 4 marks each.', 12),
  ]),
  B25H('5', 50, 'Q5 (50 marks): (a) 20 · (b) functions + state support 18 · (c) 12 — on the family in society.', [
    part('(a)', 'Give an account of the historical development of the family in Ireland from the mid-twentieth century to today.',
      '4 points @ 5 marks (graded 5:3:0)',
      'Four points, 5 marks each.', 20),
    part('(b)', 'Describe three main functions of the family and outline how the State supports the family with each.',
      '3 functions and related state support @ 6 marks (graded 6:5:4:3:2:1:0)',
      'Three functions, each with its related State support, 6 marks each.', 18),
    part('(c)', 'Discuss the role of grandparents/older family members in modern family life.',
      '3 points @ 4 marks (graded 4:2:0)',
      'Three points, 4 marks each.', 12),
  ]),
];

// ════════════════════════════════════════════════════════════════════════════
// 2024 Higher Level
// Source: examiner-reports/home-economics/2024-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const A24H = secA(2024, 'higher', 'LC098ALP014EV.pdf', 'Higher Level');
const B24H = secB(2024, 'higher', 'LC098ALP039EV.pdf', 'Higher Level');

const SECTION_A_2024_HL: QuestionLens[] = [
  A24H('1', 'A 6-mark short question — three points at 2 marks each.',
    'In relation to protein, explain deamination.',
    '3 points @ 2 marks (graded 2:1:0)',
    'Three points, 2 marks each.'),
  A24H('2', 'A 6-mark short question — two functions (4) plus two sources (2).',
    'State two biological functions of Vitamin A; identify two dietary sources of Vitamin A.',
    '2 functions @ 2 marks (graded 2:1:0) · 2 sources @ 1 mark (graded 1:0)',
    'Two functions at 2 marks each (4), plus two dietary sources at 1 mark each (2).'),
  A24H('3', 'A 6-mark short question — descriptions (4) plus food sources (2).',
    'Describe the forms of iron (haem, non-haem) and give one food source of each.',
    'Description 2 points @ 2 marks (graded 2:0) · food source 1 point @ 1 mark (graded 1:0)',
    'For the two forms of iron: a description worth 2 marks each (4) and one food source each worth 1 mark (2).'),
  A24H('4', 'A 6-mark short question — two guidelines at 3 marks each.',
    'Outline two meal-planning guidelines for a person with osteoporosis.',
    '2 guidelines @ 3 marks (graded 3:2:0)',
    'Two guidelines, 3 marks each.'),
  A24H('5', 'A 6-mark short question — two sources (4) plus two products (2).',
    'Complete the table on alternative (novel) protein foods (source, product).',
    'Source @ 2 marks (graded 2:0) x 2 · Product @ 1 mark (graded 1:0) x 2',
    'Two sources at 2 marks each (4), plus two products at 1 mark each (2).'),
  A24H('6', 'A 6-mark short question — two points at 3 marks each.',
    'Explain the role of lactic acid bacteria and rennet in the production of cheese.',
    '2 points @ 3 marks (graded 3:2:0)',
    'Two points, 3 marks each.'),
  A24H('7', 'A 6-mark short question — contaminant, source and effect at 1 mark each.',
    'Identify two food-chain contaminants; state one source and one effect on the body of each.',
    'Contaminant 1 @ 1 mark (graded 1:0) x 2 · Source 1 @ 1 mark (graded 1:0) x 2 · Effect on the body 1 @ 1 mark (graded 1:0) x 2',
    'For two contaminants: the contaminant (1), a source (1) and an effect (1) each — six 1-mark elements.'),
  A24H('8', 'A 6-mark short question — two points at 3 marks each.',
    'Differentiate between infectious and toxic food poisoning.',
    '2 points @ 3 marks (graded 3:2:1:0)',
    'Two points, 3 marks each.'),
  A24H('9', 'A 6-mark short question — two principles at 3 marks each.',
    'Explain two underlying principles of jam making.',
    '2 underlying principles @ 3 marks (graded 3:2:1:0)',
    'Two underlying principles, 3 marks each.'),
  A24H('10', 'A 6-mark short question — two payments (4) plus two examples (2).',
    'Explain the two types of social welfare payment (social insurance, social assistance) and give one example of each.',
    '2 payments @ 2 marks (graded 2:1:0) · 2 examples @ 1 mark (graded 1:0)',
    'Two payment types at 2 marks each (4), plus one example of each at 1 mark (2).'),
  A24H('11', 'A 6-mark short question — name (3) plus one role point (3).',
    'Identify one voluntary consumer-protection agency and outline its role.',
    'Name 1 @ 3 marks (graded 3:2:0) · Role 1 point @ 3 marks (graded 3:2:0)',
    'The agency named (3) and one role point (3).'),
  A24H('12', 'A 6-mark short question — two functions at 3 marks each.',
    'Outline the function of the condenser and the evaporator of a refrigerator.',
    '2 functions @ 3 marks (graded 3:2:1:0)',
    'Two functions, 3 marks each.'),
  A24H('13', 'A 6-mark short question — two features at 3 marks each.',
    'Outline two features of the current Irish National Housing Policy (Housing for All).',
    '2 features @ 3 marks (graded 3:2:0)',
    'Two features, 3 marks each.'),
  A24H('14', 'A 6-mark short question — two points at 3 marks each.',
    'Describe two ways consumers can be more environmentally conscious when choosing electrical goods.',
    '2 points @ 3 marks (graded 3:2:0)',
    'Two points, 3 marks each.'),
];

const SECTION_B_2024_HL: QuestionLens[] = [
  B24H('1', 80, 'Q1 (80 marks): (a) 20 · (b) carbohydrates 22 · (c) sugar properties 18 · (d) 20 — on food purchasing and carbohydrates.', [
    part('(a)', 'Comment and elaborate on four factors that affect consumer decisions when purchasing food, using the chart.',
      '4 factors @ 5 marks each (graded 5:4:3:2:1:0)',
      'Four factors, 5 marks each.', 20),
    part('(b)', 'Give a detailed account of carbohydrates (monosaccharide structure; disaccharide formation; biological functions).',
      'Structure 1 point @ 8 marks (graded 8:…:0) · Disaccharides 4 points @ 2 marks (graded 2:1:0) · Functions 3 points @ 2 marks (graded 2:1:0)',
      'Monosaccharide structure one point (8), disaccharide formation four points at 2 marks (8), biological functions three points at 2 marks (6).', 22),
    part('(c)', 'Describe three properties of sugar and give one culinary example of each.',
      '3 properties @ 6 marks (graded 6:5:4:3:2:1:0) [Name 2 (2:0), Description 2 (2:1:0), Culinary application 2 (2:1:0)] x3',
      'Three properties at 6 marks each: name (2), description (2) and culinary application (2).', 18),
    part('(d)', 'Devise strategies to follow when purchasing and preparing food/drink to reduce a person’s sugar consumption.',
      '4 strategies @ 5 marks (graded 5:3:0)',
      'Four strategies, 5 marks each.', 20),
  ]),
  B24H('2', 50, 'Q2 (50 marks): (a) 20 · (b) Folic Acid 18 · (c) 12 — on pregnancy nutrition.', [
    part('(a)', 'Discuss the dietary guidelines to follow when planning and preparing meals for a woman during pregnancy.',
      '5 dietary guidelines @ 4 marks (graded 4:2:0)',
      'Five guidelines, 4 marks each.', 20),
    part('(b)', 'Give an account of Folic Acid/Folate (sources; biological functions; properties).',
      'Sources 3 @ 2 marks (graded 2:0) · Functions 3 @ 2 marks (graded 2:1:0) · Properties 3 @ 2 marks (graded 2:0)',
      'Three sources (6), three biological functions (6) and three properties (6), each at 2 marks.', 18),
    part('(c)', 'Evaluate food labelling as a source of consumer information for individuals with specific dietary requirements.',
      '3 points @ 4 marks (graded 4:2:0)',
      'Three points, 4 marks each.', 12),
  ]),
  B24H('3', 50, 'Q3 (50 marks): (a) 20 · (b) yogurt 20 · (c) 10 — on Irish food culture and manufacture.', [
    part('(a)', 'Discuss the changes that have evolved in Irish food and eating patterns in recent years.',
      '5 points @ 4 marks (graded 4:2:0)',
      'Five points, 4 marks each.', 20),
    part('(b)', 'Outline the stages involved in the manufacture of yogurt (production, packaging and labelling).',
      '10 points @ 2 marks (graded 2:1:0)',
      'Ten points, 2 marks each.', 20),
    part('(c)', 'Describe the protection provided by the Food Hygiene Regulations 1950–1989.',
      '2 points @ 5 marks (graded 5:3:0)',
      'Two points, 5 marks each.', 10),
  ]),
  B24H('4', 50, 'Q4 (50 marks): (a) 20 · (b) payment methods 18 · (c) 12 — on consumer shopping.', [
    part('(a)', 'Analyse the changes in consumer shopping patterns over the last decade.',
      '5 points @ 4 marks (graded 4:2:0)',
      'Five points, 4 marks each.', 20),
    part('(b)', 'Name and evaluate two methods of payment used for in-store purchases.',
      '[Name 3 marks (graded 3:2:0), 2 points @ 3 marks (graded 3:2:0)] x2',
      'For two payment methods: the method named (3) and two evaluation points at 3 marks (6) each — 9 each.', 18),
    part('(c)', 'Describe the protection provided by the Consumer Protection Act 2007.',
      '3 points @ 4 marks (graded 4:2:0)',
      'Three points, 4 marks each.', 12),
  ]),
  B24H('5', 50, 'Q5 (50 marks): (a) 20 · (b) 18 · (c) 12 — on the family.', [
    part('(a)', 'Discuss the role of the family in meeting the physical and psychological needs of young children.',
      '4 points @ 5 marks (graded 5:3:1:0)',
      'Four points, 5 marks each.', 20),
    part('(b)', 'Analyse the impact of social, economic and technological changes on contemporary family structures.',
      '3 points @ 6 marks (graded 6:4:2:0)',
      'Three points, 6 marks each.', 18),
    part('(c)', 'Describe two supports available to older family members and state how each helps them maintain independence.',
      '2 points @ 6 marks (graded 6:4:2:0)',
      'Two points, 6 marks each.', 12),
  ]),
];

// ════════════════════════════════════════════════════════════════════════════
// 2025 Ordinary Level
// Source: examiner-reports/home-economics/2025-ol-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const A25O = secA(2025, 'ordinary', 'LC098GLP014EV.pdf', 'Ordinary Level');
const B25O = secB(2025, 'ordinary', 'LC098GLP039EV.pdf', 'Ordinary Level');

const SECTION_A_2025_OL: QuestionLens[] = [
  A25O('1', 'A 6-mark short question — three true/false ticks at 2 marks each.',
    'Tick whether each of three statements (salt/blood pressure, ultra-processed foods, fat-soluble vitamins) is true or false.',
    '3 @ 2 marks (graded 2:0)',
    'Three true/false statements, 2 marks each.'),
  A25O('2', 'A 6-mark short question — two functions (4) plus one source (2).',
    'State two biological functions of protein; name one dietary source of protein.',
    '2 @ 2 marks (graded 2:1:0) · 1 @ 2 marks (graded 2:0)',
    'Two functions at 2 marks each (4), plus one dietary source at 2 marks (2).'),
  A25O('3', 'A 6-mark short question — three true/false ticks at 2 marks each.',
    'Tick whether each of three statements about fish is true or false.',
    '3 @ 2 marks (graded 2:0)',
    'Three true/false statements, 2 marks each.'),
  A25O('4', 'A 6-mark short question — three completions at 2 marks each.',
    'Complete three carbohydrate statements using the listed terms (dietary fibre, liver, energy).',
    '3 @ 2 marks (graded 2:0)',
    'Three completions, 2 marks each.'),
  A25O('5', 'A 6-mark short question — two effects at 3 marks each.',
    'Outline two effects of cooking on rice.',
    '2 effects @ 3 marks (graded 3:2:0)',
    'Two effects, 3 marks each.'),
  A25O('6', 'A 6-mark short question — three guidelines at 2 marks each.',
    'State three dietary guidelines for preparing meals for pre-school children.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three guidelines, 2 marks each.'),
  A25O('7', 'A 6-mark short question — three matches at 2 marks each.',
    'Name a cheese suitable for each of three dishes.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three cheese-to-dish matches, 2 marks each.'),
  A25O('8', 'A 6-mark short question — three benefits at 2 marks each.',
    'Explain three benefits of food labelling for a consumer.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three benefits, 2 marks each.'),
  A25O('9', 'A 6-mark short question — three factors at 2 marks each.',
    'Explain how money, time and equipment available influence family meal planning.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three factors, 2 marks each.'),
  A25O('10', 'A 6-mark short question — two types (4) plus one benefit (2).',
    'Name two types/sources of renewable energy; explain one benefit of renewable energy.',
    '2 @ 2 marks (graded 2:1:0) · 1 @ 2 marks (graded 2:1:0)',
    'Two types at 2 marks each (4), plus one benefit at 2 marks (2).'),
  A25O('11', 'A 6-mark short question — three factors at 2 marks each.',
    'State three factors to consider when buying goods on credit.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three factors, 2 marks each.'),
  A25O('12', 'A 6-mark short question — three uses at 2 marks each.',
    'Outline three uses of household textiles.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three uses, 2 marks each.'),
  A25O('13', 'A 6-mark short question — three disadvantages at 2 marks each.',
    'State three disadvantages of buying clothes online.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three disadvantages, 2 marks each.'),
  A25O('14', 'A 6-mark short question — two symbols at 3 marks each.',
    'State what each of two fabric-care symbols conveys to the consumer.',
    '2 @ 3 marks (graded 3:2:0)',
    'Two fabric-care symbols, 3 marks each.'),
];

const SECTION_B_2025_OL: QuestionLens[] = [
  B25O('1', 80, 'Q1 (80 marks): (a) recommendation 24 · (b) Vitamin C 24 · (c) 12 · (d) 20 — on convenience-food nutrition.', [
    part('(a)', 'Recommend which soup a consumer should buy (from the nutrition table) and give four reasons.',
      'Name 4 marks (graded 4:0) · Reasons 4 @ 5 marks (graded 5:3:2:0)',
      'The recommendation named (4) plus four reasons at 5 marks each (20).', 24),
    part('(b)', 'Give an account of Vitamin C (dietary sources; functions in the body; effect of deficiency).',
      'Sources 3 @ 4 marks (graded 4:2:0) · Functions 2 @ 4 marks (graded 4:2:0) · Deficiency 1 @ 4 marks (graded 4:2:0)',
      'Three sources (12), two functions (8) and one deficiency effect (4), each element at 4 marks.', 24),
    part('(c)', 'Outline three ways a teenager can include fruit and vegetables in their diet.',
      '3 ways @ 4 marks (graded 4:2:0)',
      'Three ways, 4 marks each.', 12),
    part('(d)', 'Describe four factors consumers should consider when selecting convenience food products.',
      '4 factors @ 5 marks (graded 5:3:0)',
      'Four factors, 5 marks each.', 20),
  ]),
  B25O('2', 50, 'Q2 (50 marks): (a) 20 · (b) menu 18 · (c) 12 — on eggs.', [
    part('(a)', 'Give an account of the nutritive value and dietetic value of eggs.',
      '4 points @ 5 marks (graded 5:4:3:2:0)',
      'Four points, 5 marks each.', 20),
    part('(b)', 'Set out a menu of three meals for one day (healthy-eating guidelines), including eggs in one meal.',
      '3 meals @ 6 marks (2 courses @ 2 (2:1:0) + beverage @ 1 (1:0)) x3 · egg component 1 @ 3 marks (graded 3:0)',
      'Three meals at 6 marks each — two courses at 2 marks plus a beverage at 1 mark (15) — plus the egg component (3).', 18),
    part('(c)', 'Outline the effects of heat on eggs.',
      '3 effects @ 4 marks (graded 4:2:0)',
      'Three effects, 4 marks each.', 12),
  ]),
  B25O('3', 50, 'Q3 (50 marks): (a) 15 · (b) preservation method 25 · (c) 10 — on food preservation and spoilage.', [
    part('(a)', 'Describe three main causes of food spoilage.',
      '3 causes @ 5 marks (graded 5:3:0)',
      'Three causes, 5 marks each.', 15),
    part('(b)', 'Name and give details of how one method of food preservation is carried out.',
      'Name 1 point @ 5 marks (graded 5:3:0) · Method 4 points @ 5 marks (graded 5:3:0)',
      'The method named (5) plus four method points at 5 marks each (20).', 25),
    part('(c)', 'Discuss two advantages of food preservation.',
      '2 advantages @ 5 marks (graded 5:3:0)',
      'Two advantages, 5 marks each.', 10),
  ]),
  B25O('4', 50, 'Q4 (50 marks): (a) 20 · (b) budget plan 20 · (c) 10 — on household budgeting.', [
    part('(a)', 'Discuss four advantages of budgeting.',
      '4 advantages @ 5 marks (graded 5:3:0)',
      'Four advantages, 5 marks each.', 20),
    part('(b)', 'Set out a weekly budget plan for a family of two adults and two children on €900 net a week.',
      '5 points @ 4 marks (graded 4:2:0)',
      'Five points, 4 marks each.', 20),
    part('(c)', 'Outline the role of the Money Advice and Budgeting Service (MABS).',
      '2 points @ 5 marks (graded 5:3:0)',
      'Two points, 5 marks each.', 10),
  ]),
  B25O('5', 50, 'Q5 (50 marks): (a) 20 · (b) 20 · (c) 10 — on marriage.', [
    part('(a)', 'Describe four ways marriage customs may differ between cultures.',
      '4 ways @ 5 marks (graded 5:3:0)',
      'Four ways, 5 marks each.', 20),
    part('(b)', 'Explain the rights and responsibilities of marriage partners.',
      '4 points @ 5 marks (graded 5:3:0)',
      'Four points, 5 marks each.', 20),
    part('(c)', 'Discuss how pre-marriage courses can help couples prepare for marriage.',
      '2 points @ 5 marks (graded 5:3:0)',
      'Two points, 5 marks each.', 10),
  ]),
];

// ════════════════════════════════════════════════════════════════════════════
// 2024 Ordinary Level
// Source: examiner-reports/home-economics/2024-ol-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const A24O = secA(2024, 'ordinary', 'LC098GLP014EV.pdf', 'Ordinary Level');
const B24O = secB(2024, 'ordinary', 'LC098GLP039EV.pdf', 'Ordinary Level');

const SECTION_A_2024_OL: QuestionLens[] = [
  A24O('1', 'A 6-mark short question — three true/false ticks at 2 marks each.',
    'Tick whether each of three statements (meat fibres, protein energy, egg biological value) is true or false.',
    '3 @ 2 marks (graded 2:0)',
    'Three true/false statements, 2 marks each.'),
  A24O('2', 'A 6-mark short question — two functions (4) plus one source (2).',
    'State two functions of Vitamin C in the body; name one dietary source of Vitamin C.',
    '2 @ 2 marks (graded 2:1:0) · 1 @ 2 marks (graded 2:0)',
    'Two functions at 2 marks each (4), plus one dietary source at 2 marks (2).'),
  A24O('3', 'A 6-mark short question — three completions at 2 marks each.',
    'Complete three statements about energy using the listed terms (empty kilocalories, energy balance, obesity).',
    '3 @ 2 marks (graded 2:0)',
    'Three completions, 2 marks each.'),
  A24O('4', 'A 6-mark short question — two factors (4) plus two ways (2).',
    'Outline two factors that affect the tenderness of meat; list two ways of tenderising meat.',
    '2 @ 2 marks (graded 2:1:0) · 2 ways @ 1 marks (graded 1:0)',
    'Two factors at 2 marks each (4), plus two tenderising ways at 1 mark each (2).'),
  A24O('5', 'A 6-mark short question — three true/false ticks at 2 marks each.',
    'Tick whether each of three statements (cereal bran, starch grains, roux sauce) is true or false.',
    '3 @ 2 marks (graded 2:0)',
    'Three true/false statements, 2 marks each.'),
  A24O('6', 'A 6-mark short question — three changes at 2 marks each.',
    'Outline three lifestyle changes recommended for an obese person trying to lose weight.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three lifestyle changes, 2 marks each.'),
  A24O('7', 'A 6-mark short question — two pastry types (4) plus two dishes (2).',
    'Name two types of pastry and a different dish made from each.',
    'Type of pastry 2 @ 2 marks (graded 2:0) · Dish 2 @ 1 mark (graded 1:0)',
    'Two pastry types at 2 marks each (4), plus one dish for each at 1 mark (2).'),
  A24O('8', 'A 6-mark short question — three guidelines at 2 marks each.',
    'Outline three guidelines to follow when freezing fresh food.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three guidelines, 2 marks each.'),
  A24O('9', 'A 6-mark short question — three matches at 2 marks each.',
    'Match the three methods of heat transfer (conduction, convection, radiation) with the correct definition.',
    '3 @ 2 marks (graded 2:0)',
    'Three matches, 2 marks each.'),
  A24O('10', 'A 6-mark short question — three rights at 2 marks each.',
    'Outline three consumer rights when buying goods.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three consumer rights, 2 marks each.'),
  A24O('11', 'A 6-mark short question — three advantages at 2 marks each.',
    'State three advantages of teenagers becoming regular savers.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three advantages, 2 marks each.'),
  A24O('12', 'A 6-mark short question — three criteria at 2 marks each.',
    'Explain how suitability for purpose, personal choice and cost influence the consumer selecting household textiles.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three criteria, 2 marks each.'),
  A24O('13', 'A 6-mark short question — two benefits at 3 marks each.',
    'State two benefits of life assurance.',
    '2 @ 3 marks (graded 3:2:0)',
    'Two benefits, 3 marks each.'),
  A24O('14', 'A 6-mark short question — three guidelines at 2 marks each.',
    'Describe three guidelines to follow when using a microwave oven.',
    '3 @ 2 marks (graded 2:1:0)',
    'Three guidelines, 2 marks each.'),
];

const SECTION_B_2024_OL: QuestionLens[] = [
  B24O('1', 80, 'Q1 (80 marks): (a) 20 · (b) carbohydrates 28 · (c) 12 · (d) 20 — on food choices and carbohydrates.', [
    part('(a)', 'Discuss five factors that affect a person’s food choices, using the table.',
      '5 @ 4 marks (graded 4:2:0)',
      'Five factors, 4 marks each.', 20),
    part('(b)', 'Give an account of carbohydrates (classification; functions in the body; dietary sources).',
      'Classification 3 classes @ 2 marks (graded 2:0) · Functions 2 @ 5 marks (graded 5:3:0) · Sources 3 @ 4 marks (graded 4:2:0)',
      'Three classes at 2 marks (6), two functions at 5 marks (10) and three sources at 4 marks (12).', 28),
    part('(c)', 'Outline three ways a person can increase the amount of fibre in their diet.',
      '3 points @ 4 marks (graded 4:2:0)',
      'Three points, 4 marks each.', 12),
    part('(d)', 'Describe four ways consumers can reduce food waste when planning meals and purchasing foods.',
      '4 ways @ 5 marks (graded 5:4:3:0)',
      'Four ways, 5 marks each.', 20),
  ]),
  B24O('2', 50, 'Q2 (50 marks): (a) 20 · (b) menu 18 · (c) 12 — on fruit and vegetables.', [
    part('(a)', 'Give an account of the nutritive value and dietetic value of fruit and vegetables.',
      '4 points @ 5 marks (graded 5:4:3:2:0)',
      'Four points, 5 marks each.', 20),
    part('(b)', 'Set out a menu of three meals for one day for a vegetarian (healthy-eating guidelines).',
      '3 meals @ 6 marks (2 courses @ 2 (2:1:0) + beverage @ 2 (2:0)) x3',
      'Three meals at 6 marks each — two courses at 2 marks plus a beverage at 2 marks.', 18),
    part('(c)', 'Describe three guidelines for storing fruit and vegetables to maintain their quality.',
      '3 ways @ 4 marks (graded 4:2:0)',
      'Three ways, 4 marks each.', 12),
  ]),
  B24O('3', 50, 'Q3 (50 marks): (a) 20 · (b) sectors 15 · (c) packaging 15 — on the processed-food industry.', [
    part('(a)', 'Describe four food additives used in the manufacture of processed foods.',
      '4 points @ 5 marks (graded 5:3:0)',
      'Four points, 5 marks each.', 20),
    part('(b)', 'Identify three major sectors of the Irish food industry and give one food product produced in each.',
      '3 sectors @ 3 marks (graded 3:2:0) · (1 food @ 2 marks (graded 2:1:0)) x3',
      'Three sectors at 3 marks (9), each with one food product at 2 marks (6).', 15),
    part('(c)', 'Evaluate the role of packaging (suitability for purpose; environmental impact; source of consumer information).',
      'Suitability 1 role @ 5 marks (graded 5:3:0) · Environmental impact 1 role @ 5 marks (graded 5:3:0) · Consumer information 1 role @ 5 marks (graded 5:3:0)',
      'One role under each of the three headings, 5 marks each.', 15),
  ]),
  B24O('4', 50, 'Q4 (50 marks): (a) 20 · (b) Small Claims Court 20 · (c) 10 — on consumer goods and services.', [
    part('(a)', 'Describe four factors that influence consumers when purchasing goods and services.',
      '4 factors @ 5 marks (graded 5:3:0)',
      'Four factors, 5 marks each.', 20),
    part('(b)', 'Give an account of the Small Claims Court procedure used to resolve a consumer dispute.',
      '4 points @ 5 marks (graded 5:3:0)',
      'Four points, 5 marks each.', 20),
    part('(c)', 'Explain how the Sale of Goods and Supply of Services Act 1980 protects the consumer.',
      '2 points @ 5 marks (graded 5:3:0)',
      'Two points, 5 marks each.', 10),
  ]),
  B24O('5', 50, 'Q5 (50 marks): (a) functions 20 · (b) 15 · (c) 15 — on the family.', [
    part('(a)', 'Describe the physical, emotional, social and economic functions of the family.',
      'Physical 1 point @ 5 marks (graded 5:3:0) · Emotional 1 point @ 5 marks (graded 5:3:0) · Social 1 point @ 5 marks (graded 5:3:0) · Economic 1 point @ 5 marks (graded 5:3:0)',
      'One point under each of the four functions, 5 marks each.', 20),
    part('(b)', 'Explain how the State assists the family in carrying out its physical, social and economic functions.',
      '3 points @ 5 marks (graded 5:3:0)',
      'Three points, 5 marks each.', 15),
    part('(c)', 'Discuss three advantages of a positive parent-child relationship within the family.',
      '3 points @ 5 marks (graded 5:3:0)',
      'Three points, 5 marks each.', 15),
  ]),
];

// ════════════════════════════════════════════════════════════════════════════

const EV_ENTRIES: QuestionLens[] = [
  ...SECTION_A_2025_HL, ...SECTION_B_2025_HL,
  ...SECTION_A_2024_HL, ...SECTION_B_2024_HL,
  ...SECTION_A_2025_OL, ...SECTION_B_2025_OL,
  ...SECTION_A_2024_OL, ...SECTION_B_2024_OL,
];

const HOME_ECONOMICS_LENS: SubjectLens = {
  subjectId: 'home-economics-s-and-s',
  entries: [
    ...EV_ENTRIES,
    ...mirrorIV(EV_ENTRIES),
  ],
};

export default HOME_ECONOMICS_LENS;
