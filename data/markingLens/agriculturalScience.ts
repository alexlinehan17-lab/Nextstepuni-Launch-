/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Agricultural Science (Higher Level).
 *
 * Sources of truth (both filed in /examiner-reports/agricultural-science/):
 *  - SEC Marking Scheme 2023, Agricultural Science (Higher Level) —
 *    examiner-reports/agricultural-science/2023-marking-scheme.md
 *  - SEC Marking Scheme 2024, Agricultural Science Higher Level —
 *    examiner-reports/agricultural-science/2024-marking-scheme.md
 *
 * Every `notation` below is verbatim from those documents (spacing normalised
 * only); every entry's parts sum to the printed question total (Section A = 10,
 * Section B = 50), machine-checked in test/markingLens.test.ts.
 *
 * SEC notation used in these schemes:
 *  - "N(M)"  = N separate elements, each worth M marks (e.g. "3(2)" = 6).
 *  - "X+Y…"  = the first correct point earns X, the next Y, and so on.
 *  - "D = …" / "L = …" = marks reserved for a Diagram / its Labels.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly — both
 * papers are 2023 / 2024 Higher Level, English (ev), fileid LC024ALP000EV.pdf,
 * Q1–18. Only the Higher Level scheme is filed for each year, so only HL/ev is
 * authored. Where a question offers alternative parts ("Or"), the ladder shows
 * one complete answer path (noted in the headline); its parts sum to the total.
 *
 * Skipped: 2024 HL Q18 — its printed sub-part marks sum to 54, not the 50 on
 * the paper, and the extraction cannot be reconciled to the printed total
 * without inventing an allocation. Omitted rather than shipped wrong.
 */

import { type QuestionLens, type SubjectLens } from './types';

const FILE = 'LC024ALP000EV.pdf';
const CITE23 = (q: string) => `SEC Marking Scheme 2023, Agricultural Science Higher Level, ${q}`;
const CITE24 = (q: string) => `SEC Marking Scheme 2024, Agricultural Science Higher Level, ${q}`;

// ── 2023 Higher Level ───────────────────────────────────────────────────────

const HL_2023: QuestionLens[] = [
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '1', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)(i)', task: 'Identify the breeds of animals A, B and C', notation: '3(2)', decoded: 'Three breeds, 2 marks each.', marks: 6 },
      { part: '(a)(ii)', task: 'Explain dual purpose breed', notation: '2', decoded: 'The explanation earns 2 marks.', marks: 2 },
      { part: '(a)(iii)', task: 'Explain the importance of using a purebred sire in a beef herd', notation: '2', decoded: 'The explanation earns 2 marks.', marks: 2 },
    ],
    cite: CITE23('Section A Q1'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '2', totalMarks: 10,
    headline: 'Section A short answer (10m); two elements per part.',
    parts: [
      { part: '(a)', task: 'Explain what happens at any two stages in a named plant', notation: '2(3)', decoded: 'Two stages, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Identify any two weeds found in Irish fields', notation: '2(2)', decoded: 'Two weeds, 2 marks each.', marks: 4 },
    ],
    cite: CITE23('Section A Q2'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '3', totalMarks: 10,
    headline: 'Section A short answer (10m); the deficiency part splits into a name and a symptom.',
    parts: [
      { part: '(a)', task: 'State one source of calcium for either plants or animals', notation: '2', decoded: 'The stated source earns 2 marks.', marks: 2 },
      { part: '(b)', task: 'Outline one process by which calcium becomes available to plants', notation: '2', decoded: 'The outlined process earns 2 marks.', marks: 2 },
      { part: '(c)', task: 'Explain the symptoms of a named calcium deficiency in cattle', notation: 'Name = 3 + Symptom = 3', decoded: 'Naming the deficiency (3m) + a symptom (3m).', marks: 6 },
    ],
    cite: CITE23('Section A Q3'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '4', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Suggest one reason for any three treatments', notation: '3(2)', decoded: 'Three treatments, 2 marks each.', marks: 6 },
      { part: '(b)', task: 'Outline the importance of performance testing to the beef or dairy industry', notation: '4', decoded: 'The outlined importance earns 4 marks.', marks: 4 },
    ],
    cite: CITE23('Section A Q4'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '5', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Briefly describe how to collect soil samples for soil testing', notation: '2(3)', decoded: 'Two points, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Describe a reason for the 3–5 year / October–February recommendations', notation: '2', decoded: 'The reason earns 2 marks.', marks: 2 },
      { part: '(c)', task: 'Outline how soil testing can improve economic sustainability', notation: '2', decoded: 'The outlined point earns 2 marks.', marks: 2 },
    ],
    cite: CITE23('Section A Q5'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '6', totalMarks: 10,
    headline: 'Section A short answer (10m); one mark block per part.',
    parts: [
      { part: '(a)', task: 'State a cause of lameness in sheep', notation: '4', decoded: 'The stated cause earns 4 marks.', marks: 4 },
      { part: '(b)', task: 'Briefly describe the symptoms of the disease stated in part (a)', notation: '2', decoded: 'The symptoms earn 2 marks.', marks: 2 },
      { part: '(c)', task: 'Outline the treatment for the disease in part (a)', notation: '2', decoded: 'The treatment earns 2 marks.', marks: 2 },
      { part: '(d)', task: 'Briefly describe one negative financial implication of lameness', notation: '2', decoded: 'The implication earns 2 marks.', marks: 2 },
    ],
    cite: CITE23('Section A Q6'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '7', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)', task: 'Complete the table comparing goat dairy farming to cow dairy farming', notation: '3+3+2+2', decoded: 'Four table entries worth 3, 3, 2 and 2 marks.', marks: 10 },
    ],
    cite: CITE23('Section A Q7'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '8', totalMarks: 10,
    headline: 'Section A short answer (10m); the two variables are marked separately.',
    parts: [
      { part: '(a)', task: 'State the dependent and independent variable in this investigation', notation: '2 + 2', decoded: 'Independent variable (2m) + dependent variable (2m).', marks: 4 },
      { part: '(b)', task: 'Outline why it was important to carry out the test 3 times for each fertiliser', notation: '3', decoded: 'The outlined reason earns 3 marks.', marks: 3 },
      { part: '(c)', task: 'Briefly describe the conclusion the student made', notation: '3', decoded: 'The conclusion earns 3 marks.', marks: 3 },
    ],
    cite: CITE23('Section A Q8'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '9', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)(i)', task: 'Explain pre-emergence hoeing', notation: '2', decoded: 'The explanation earns 2 marks.', marks: 2 },
      { part: '(a)(ii)', task: 'Explain how the Farmdroid can benefit the environment and farmer', notation: '2(3)', decoded: 'Two benefits, 3 marks each.', marks: 6 },
      { part: '(a)(iii)', task: 'Outline one other piece of technology benefiting farmer and environment', notation: '2', decoded: 'The outlined technology earns 2 marks.', marks: 2 },
    ],
    cite: CITE23('Section A Q9'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '10', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)(i)', task: 'Label the diagram of the monogastric digestive system (A, B, C)', notation: '3(2)', decoded: 'Three labels, 2 marks each.', marks: 6 },
      { part: '(a)(ii)', task: 'Outline the role of microorganisms in the monogastric digestive system', notation: '4', decoded: 'The outlined role earns 4 marks.', marks: 4 },
    ],
    cite: CITE23('Section A Q10'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '11', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Outline ways Tim can achieve the target of 0.95', notation: '2(3)', decoded: 'Two ways, 3 marks each.', marks: 6 },
      { part: '(b)', task: 'Briefly explain ways to achieve the 6-week calving rate target of 80%', notation: '2(2)', decoded: 'Two ways, 2 marks each.', marks: 4 },
    ],
    cite: CITE23('Section A Q11'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '12', totalMarks: 10,
    headline: 'Section A short answer (10m); one mark block per part.',
    parts: [
      { part: '(a)', task: 'State the N content of this slurry sample', notation: '3', decoded: 'The stated value earns 3 marks.', marks: 3 },
      { part: '(b)', task: 'Suggest one reason for a DM content of 2% in a slurry sample', notation: '3', decoded: 'The reason earns 3 marks.', marks: 3 },
      { part: '(c)', task: 'Briefly explain why nutrient content is higher in the 7% DM slurry', notation: '2', decoded: 'The explanation earns 2 marks.', marks: 2 },
      { part: '(d)', task: 'Outline a safety precaution taken when sampling slurry', notation: '2', decoded: 'The precaution earns 2 marks.', marks: 2 },
    ],
    cite: CITE23('Section A Q12'),
  },

  // Section B — 50 marks each.
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '13', totalMarks: 50,
    headline: 'Section B long question (50m). Parts (a) and (b) are answered, then part (c) OR the (d) alternative — (c) is shown.',
    parts: [
      { part: '(a)(i)', task: 'Describe two factors involved in the formation of soil', notation: '5+5+2+2', decoded: 'Four scored elements worth 5, 5, 2 and 2 marks.', marks: 14 },
      { part: '(a)(ii)', task: 'Draw a labelled diagram of a Podzol soil profile', notation: 'D = 0, 3, 6 + L = 3(2)', decoded: 'Diagram scored 0, 3 or 6 by elements present + three labels at 2 marks each.', marks: 12 },
      { part: '(b)(i)', task: 'Identify the soil water content level for each diagram', notation: '3(3)', decoded: 'Three identifications, 3 marks each.', marks: 9 },
      { part: '(b)(ii)', task: 'Briefly describe the implications for a farmer of any two', notation: '2+1', decoded: 'Two implications worth 2 and 1 marks.', marks: 3 },
      { part: '(c)', task: 'Describe with a labelled diagram an investigation comparing the drainage rate of a podzol and a brown earth soil', notation: '3(4)', decoded: 'Three points, 4 marks each.', marks: 12 },
    ],
    cite: CITE23('Section B Q13'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '14', totalMarks: 50,
    headline: 'Section B long question (50m); every part answered.',
    parts: [
      { part: '(a)', task: 'Explain direct drilling and outline one advantage', notation: '2+1', decoded: 'Explanation (2m) + one advantage (1m).', marks: 3 },
      { part: '(b)(i)', task: 'Briefly describe why he chose three varieties of oilseed rape', notation: '5', decoded: 'The reason earns 5 marks.', marks: 5 },
      { part: '(b)(ii)', task: 'Explain undersowing', notation: '3', decoded: 'The explanation earns 3 marks.', marks: 3 },
      { part: '(b)(iii)', task: 'Outline the advantages of sowing clover with the oilseed rape', notation: '5+1', decoded: 'Two advantages worth 5 and 1 marks.', marks: 6 },
      { part: '(b)(iv)', task: 'Explain annual plant', notation: '3', decoded: 'The explanation earns 3 marks.', marks: 3 },
      { part: '(b)(v)', task: 'Give another example of an annual plant', notation: '3', decoded: 'The example earns 3 marks.', marks: 3 },
      { part: '(c)(i)', task: 'Describe how to carry out a plant count in a 2 hectare field', notation: '3(4)', decoded: 'Three points, 4 marks each.', marks: 12 },
      { part: '(c)(ii)', task: 'Briefly explain advantages of a plant count in a reseeded field', notation: '5+1', decoded: 'Two advantages worth 5 and 1 marks.', marks: 6 },
      { part: '(c)(iii)', task: 'Explain why counting is difficult at the tillering stage', notation: '4', decoded: 'The explanation earns 4 marks.', marks: 4 },
      { part: '(c)(iv)', task: 'Describe a scientific reason for the higher seeding rate', notation: '5', decoded: 'The reason earns 5 marks.', marks: 5 },
    ],
    cite: CITE23('Section B Q14'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '15', totalMarks: 50,
    headline: 'Section B long question (50m); every part answered.',
    parts: [
      { part: '(a)', task: 'Describe how to determine the soil texture', notation: '3(4)', decoded: 'Three points, 4 marks each.', marks: 12 },
      { part: '(b)(i)', task: 'State the optimum pH of a soil for crop growth', notation: '6', decoded: 'The stated range earns 6 marks.', marks: 6 },
      { part: '(b)(ii)', task: 'Suggest a more accurate way to determine the pH of the soil filtrate', notation: '3', decoded: 'The suggestion earns 3 marks.', marks: 3 },
      { part: '(b)(iii)', task: 'Briefly describe other benefits of liming the soil', notation: '5+2', decoded: 'Two benefits worth 5 and 2 marks.', marks: 7 },
      { part: '(c)(i)', task: 'State the soil pH that produces the least N2O emissions', notation: '6', decoded: 'The stated value earns 6 marks.', marks: 6 },
      { part: '(c)(ii)', task: 'Discuss the pH–N2O relationship and its implications for farming', notation: '5 + 3', decoded: 'The relationship (5m) + its implication (3m).', marks: 8 },
      { part: '(d)', task: 'For a named food crop, describe seedbed preparation and disease prevention', notation: '4+4', decoded: 'Two headings worth 4 marks each.', marks: 8 },
    ],
    cite: CITE23('Section B Q15'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '16', totalMarks: 50,
    headline: 'Section B long question (50m). Parts (a) and (b) are answered, then part (c) OR the (d) alternative — (c) is shown.',
    parts: [
      { part: '(a)(i)', task: 'Identify the main source of carbon emissions on the farm', notation: '5', decoded: 'The identification earns 5 marks.', marks: 5 },
      { part: '(a)(ii)', task: 'State with reason if emissions are above or below the national average', notation: '5+1', decoded: 'The statement (5m) + reason (1m).', marks: 6 },
      { part: '(a)(iii)', task: 'Comment on overall emissions since joining the scheme and justify', notation: '2(3)', decoded: 'Two points, 3 marks each.', marks: 6 },
      { part: '(b)(i)', task: 'Describe advice — one action for each source of carbon emissions', notation: '4+4+2+2', decoded: 'Four actions worth 4, 4, 2 and 2 marks.', marks: 12 },
      { part: '(b)(ii)', task: 'List two other potential sources of carbon emissions', notation: '5+1', decoded: 'Two sources worth 5 and 1 marks.', marks: 6 },
      { part: '(c)', task: 'Draw a labelled diagram of the carbon cycle', notation: '5(3)', decoded: 'Five scored elements of the cycle, 3 marks each.', marks: 15 },
    ],
    cite: CITE23('Section B Q16'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '17', totalMarks: 50,
    headline: 'Section B long question (50m); every part answered.',
    parts: [
      { part: '(a)(i)', task: 'Describe the management of the reseeded land at each of the stages', notation: '4(4)', decoded: 'Four stages, 4 marks each.', marks: 16 },
      { part: '(a)(ii)', task: 'Explain ways plants can be encouraged to tiller', notation: '6+2', decoded: 'Two ways worth 6 and 2 marks.', marks: 8 },
      { part: '(b)(i)', task: 'Describe the reasons for including a hybrid seed mixture', notation: '2(6)', decoded: 'Two reasons, 6 marks each.', marks: 12 },
      { part: '(b)(ii)', task: 'Outline reasons for a variety of heading-out dates in the seed mixture', notation: '2(2)', decoded: 'Two reasons, 2 marks each.', marks: 4 },
      { part: '(b)(iii)', task: 'Identify any two plant varieties in Irish multi-species seed mixtures', notation: '2(2)', decoded: 'Two varieties, 2 marks each.', marks: 4 },
      { part: '(c)', task: 'Explain, with a labelled diagram, how a grass plant reproduces sexually or asexually', notation: '5+1', decoded: 'Two points worth 5 and 1 marks.', marks: 6 },
    ],
    cite: CITE23('Section B Q17'),
  },
  {
    year: 2023, level: 'higher', lang: 'ev', fileid: FILE, n: '18', totalMarks: 50,
    headline: 'Section B long question (50m); the milk-quality part reserves marks for factor + description.',
    parts: [
      { part: '(a)(i)', task: 'Label any three parts of the structure of the udder', notation: '3(1)', decoded: 'Three labels, 1 mark each.', marks: 3 },
      { part: '(a)(ii)', task: 'Briefly describe the symptoms of mastitis in cows', notation: '4+3', decoded: 'Two symptoms worth 4 and 3 marks.', marks: 7 },
      { part: '(a)(iii)', task: 'Explain the treatment of mastitis in cows', notation: '4', decoded: 'The treatment earns 4 marks.', marks: 4 },
      { part: '(a)(iv)', task: 'Briefly describe ways farmers can reduce mastitis in cows', notation: '2(3)', decoded: 'Two ways, 3 marks each.', marks: 6 },
      { part: '(a)(v)', task: 'Place each step in the correct order (match letter to number)', notation: '4(2)', decoded: 'Four matches, 2 marks each.', marks: 8 },
      { part: '(b)(i)', task: 'Analyse the table and outline the reasons for the difference', notation: '3+1', decoded: 'Two points worth 3 and 1 marks.', marks: 4 },
      { part: '(b)(ii)', task: 'Describe the factors affecting milk quality', notation: 'F:3(3) + D:3(3)', decoded: 'Three factors at 3m each + three descriptions at 3m each.', marks: 18 },
    ],
    cite: CITE23('Section B Q18'),
  },
];

// ── 2024 Higher Level ───────────────────────────────────────────────────────

const HL_2024: QuestionLens[] = [
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '1', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Identify the items of farm machinery / equipment in A, B and C', notation: '3(2)', decoded: 'Three items, 2 marks each.', marks: 6 },
      { part: '(b)', task: 'Briefly describe how equipment B is used on a sheep farm', notation: '4', decoded: 'The description earns 4 marks.', marks: 4 },
    ],
    cite: CITE24('Section A Q1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '2', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)(i)', task: 'Identify any two of the breeds A, B and C', notation: '2(2)', decoded: 'Two breeds, 2 marks each.', marks: 4 },
      { part: '(a)(ii)', task: 'Explain the term prolificacy', notation: '2', decoded: 'The explanation earns 2 marks.', marks: 2 },
      { part: '(a)(iii)', task: 'Briefly explain characteristics making bull C suitable as a terminal sire', notation: '2(2)', decoded: 'Two characteristics, 2 marks each.', marks: 4 },
    ],
    cite: CITE24('Section A Q2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '3', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)(i)', task: 'Identify the best grazing period for post-grazing recovery', notation: '1', decoded: 'The identification earns 1 mark.', marks: 1 },
      { part: '(a)(ii)', task: 'Outline one reason for root development in continuously grazed fields', notation: '1', decoded: 'The outlined reason earns 1 mark.', marks: 1 },
      { part: '(a)(iii)', task: 'State which grazing system is associated with each description', notation: '2(4)', decoded: 'Two matches, 4 marks each.', marks: 8 },
    ],
    cite: CITE24('Section A Q3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '4', totalMarks: 10,
    headline: 'Section A short answer (10m); a single grid on compaction and organic-matter loss.',
    parts: [
      { part: '', task: 'Describe the impact of compaction and organic matter loss on the productivity of farmland (effect + ways of reducing)', notation: '2(3) + 2(2)', decoded: 'Two points at 3 marks each + two points at 2 marks each.', marks: 10 },
    ],
    cite: CITE24('Section A Q4'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '5', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Identify the crops A, B and C', notation: '5+2(1)', decoded: 'First identification 5 marks, then two at 1 mark each.', marks: 7 },
      { part: '(b)', task: 'Outline the advice on keeping and re-sowing the seed', notation: '3', decoded: 'The advice earns 3 marks.', marks: 3 },
    ],
    cite: CITE24('Section A Q5'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '6', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)', task: 'Name flock-management features and briefly describe the benefit of each', notation: '2(3) + 2(2)', decoded: 'Two points at 3 marks each + two points at 2 marks each.', marks: 10 },
    ],
    cite: CITE24('Section A Q6'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '7', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Explain agroforestry', notation: '4', decoded: 'The explanation earns 4 marks.', marks: 4 },
      { part: '(b)', task: 'Outline the possible benefits of agroforestry', notation: '2(3)', decoded: 'Two benefits, 3 marks each.', marks: 6 },
    ],
    cite: CITE24('Section A Q7'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '8', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Explain natural predators', notation: '2', decoded: 'The explanation earns 2 marks.', marks: 2 },
      { part: '(b)', task: 'Briefly describe how the dock beetle controls dock leaves', notation: '2', decoded: 'The description earns 2 marks.', marks: 2 },
      { part: '(c)', task: 'Provide an example of a biological control and state its target', notation: '2(3)', decoded: 'Two example-and-target rows, 3 marks each.', marks: 6 },
    ],
    cite: CITE24('Section A Q8'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '9', totalMarks: 10,
    headline: 'Section A short answer (10m). Answer part (a) OR the (b) alternative — the (a) ladder is shown.',
    parts: [
      { part: '(a)', task: 'Compare soil mineral particles (Gravel/Sand vs Silt/Clay) on drainage, fertility and ion exchange', notation: '4(2) + 2(1)', decoded: 'Four points at 2 marks each + two points at 1 mark each.', marks: 10 },
    ],
    cite: CITE24('Section A Q9'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '10', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Identify which picture (A or B) is more likely a multi-species sward', notation: '4', decoded: 'The identification earns 4 marks.', marks: 4 },
      { part: '(b)', task: 'List two plants that could be included on the multi-species sward', notation: '2(2)', decoded: 'Two plants, 2 marks each.', marks: 4 },
      { part: '(c)', task: 'Briefly describe how plant diversity impacts soil biology', notation: '2', decoded: 'The description earns 2 marks.', marks: 2 },
    ],
    cite: CITE24('Section A Q10'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '11', totalMarks: 10,
    headline: 'Section A short answer (10m); the cull part marks the choice and its reason separately.',
    parts: [
      { part: '(a)', task: 'Calculate the average calving interval for Cow 1', notation: '4', decoded: 'The calculation earns 4 marks.', marks: 4 },
      { part: '(b)', task: 'Briefly describe how the calving interval reduced between lactation 3 and 4', notation: '2', decoded: 'The description earns 2 marks.', marks: 2 },
      { part: '(c)', task: 'State with reason which cow should be culled', notation: '2 + 2', decoded: 'Naming the cow (2m) + the reason (2m).', marks: 4 },
    ],
    cite: CITE24('Section A Q11'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '12', totalMarks: 10,
    headline: 'Section A short answer (10m).',
    parts: [
      { part: '(a)', task: 'Outline actions farmers can take to reduce runoff from the fields and roadway', notation: '4+2', decoded: 'Two actions worth 4 and 2 marks.', marks: 6 },
      { part: '(b)', task: 'Outline other potential sources of water pollution from agriculture', notation: '2(2)', decoded: 'Two sources, 2 marks each.', marks: 4 },
    ],
    cite: CITE24('Section A Q12'),
  },

  // Section B — 50 marks each.
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '13', totalMarks: 50,
    headline: 'Section B long question (50m). Parts (a) and (b) are answered, then part (c) OR the (d) alternative — (c) is shown.',
    parts: [
      { part: '(a)(i)', task: 'Describe how the botanical-composition investigation was carried out', notation: '3(4)', decoded: 'Three points, 4 marks each.', marks: 12 },
      { part: '(a)(ii)', task: 'Identify the plants A–D', notation: '4(2)', decoded: 'Four plants, 2 marks each.', marks: 8 },
      { part: '(a)(iii)', task: 'Explain advice to create positive grassland for plant biodiversity', notation: '6+2', decoded: 'Two points worth 6 and 2 marks.', marks: 8 },
      { part: '(b)(i)', task: 'Describe with a labelled diagram how a peat soil is formed', notation: '6+2', decoded: 'Two points worth 6 and 2 marks.', marks: 8 },
      { part: '(b)(ii)', task: 'State two locations in Ireland where you would find a peat soil', notation: '3+3', decoded: 'Two locations worth 3 marks each.', marks: 6 },
      { part: '(c)', task: 'Outline advice on the importance of preserving peat bogs', notation: '6+2', decoded: 'Two points worth 6 and 2 marks.', marks: 8 },
    ],
    cite: CITE24('Section B Q13'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '14', totalMarks: 50,
    headline: 'Section B long question (50m). Parts (a) and (b) are answered, then part (d) OR the (c) diagram alternative — (d) is shown.',
    parts: [
      { part: '(a)(i)', task: 'Identify the bacteria required for good-quality silage (tick)', notation: '6', decoded: 'The correct tick earns 6 marks.', marks: 6 },
      { part: '(a)(ii)', task: 'Describe the chemical / biological processes producing good-quality silage', notation: '3(4)', decoded: 'Three points, 4 marks each.', marks: 12 },
      { part: '(a)(iii)', task: 'Identify the ideal DM % of good-quality silage (tick)', notation: '6', decoded: 'The correct tick earns 6 marks.', marks: 6 },
      { part: '(b)(i)', task: 'Describe a lab investigation to measure the DM content of silage', notation: '3(4)', decoded: 'Three points, 4 marks each.', marks: 12 },
      { part: '(b)(ii)', task: 'Outline factors affecting silage quality apart from DM', notation: '6+2', decoded: 'Two factors worth 6 and 2 marks.', marks: 8 },
      { part: '(d)', task: 'Outline the characteristics of grass most desirable for grazing', notation: '5+1', decoded: 'Two characteristics worth 5 and 1 marks.', marks: 6 },
    ],
    cite: CITE24('Section B Q14'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '15', totalMarks: 50,
    headline: 'Section B long question (50m); every part answered.',
    parts: [
      { part: '(a)(i)', task: 'Explain the animal’s phenotype', notation: '3', decoded: 'The explanation earns 3 marks.', marks: 3 },
      { part: '(a)(ii)', task: 'Briefly explain the function of protein, vitamins and water', notation: '6+2+1', decoded: 'Three nutrients worth 6, 2 and 1 marks.', marks: 9 },
      { part: '(a)(iii)', task: 'State two animal-related factors or two environmental conditions', notation: '2(2)', decoded: 'Two points, 2 marks each.', marks: 4 },
      { part: '(a)(iv)', task: 'Describe the energy requirement of a breeding cow at each stage', notation: '3(1)', decoded: 'Three stages, 1 mark each.', marks: 3 },
      { part: '(a)(v)', task: 'Briefly describe the symptoms and prevention of a named mineral deficiency', notation: '3(2)', decoded: 'Three points, 2 marks each.', marks: 6 },
      { part: '(b)(i)', task: 'Outline benefits of weighing cattle on beef farms', notation: '5+1', decoded: 'Two benefits worth 5 and 1 marks.', marks: 6 },
      { part: '(b)(ii)', task: 'Briefly describe two safety considerations when weighing beef animals', notation: '5+4', decoded: 'Two considerations worth 5 and 4 marks.', marks: 9 },
      { part: '(c)(i)', task: 'Calculate the average daily liveweight gain of the calves', notation: '6', decoded: 'The calculation earns 6 marks.', marks: 6 },
      { part: '(c)(ii)', task: 'Calculate the value of the scheme to Paul', notation: '4', decoded: 'The calculation earns 4 marks.', marks: 4 },
    ],
    cite: CITE24('Section B Q15'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '16', totalMarks: 50,
    headline: 'Section B long question (50m); every part answered.',
    parts: [
      { part: '(a)(i)', task: 'Outline a hypothesis for this investigation', notation: '2', decoded: 'The hypothesis earns 2 marks.', marks: 2 },
      { part: '(a)(ii)', task: 'Outline with reason if this investigation is a fair test', notation: '4 + 3', decoded: 'The judgement (4m) + reason (3m).', marks: 7 },
      { part: '(a)(iii)', task: 'State the independent, dependent and control variables', notation: '4+4+3', decoded: 'Three variables worth 4, 4 and 3 marks.', marks: 11 },
      { part: '(a)(iv)', task: 'Outline two possible sources of error', notation: '3+1', decoded: 'Two sources worth 3 and 1 marks.', marks: 4 },
      { part: '(b)(i)', task: 'State if there is any difference in colostrum quality when pooled', notation: '4', decoded: 'The statement earns 4 marks.', marks: 4 },
      { part: '(b)(ii)', task: 'Outline the advice to farmers based on the results', notation: '4', decoded: 'The advice earns 4 marks.', marks: 4 },
      { part: '(c)', task: 'Explain how diet change from birth to weaning affects ruminant stomach development', notation: '5+1', decoded: 'Two points worth 5 and 1 marks.', marks: 6 },
      { part: '(d)', task: 'Discuss the importance of feeding colostrum (timing, amount, hygiene)', notation: '6+2(3)', decoded: 'One point at 6 marks + two points at 3 marks each.', marks: 12 },
    ],
    cite: CITE24('Section B Q16'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: FILE, n: '17', totalMarks: 50,
    headline: 'Section B long question (50m); every part answered.',
    parts: [
      { part: '(a)', task: 'Briefly describe how a named abiotic factor affects Irish agriculture', notation: '5 + 1', decoded: 'The factor (5m) + its description (1m).', marks: 6 },
      { part: '(b)(i)', task: 'Draw a labelled diagram of the rhizosphere', notation: 'D = 3, 0 + L = 2(1)', decoded: 'Diagram scored 3 or 0 + two labels at 1 mark each.', marks: 5 },
      { part: '(b)(ii)', task: 'Describe the relationship between plant roots and rhizosphere microorganisms', notation: '3', decoded: 'The description earns 3 marks.', marks: 3 },
      { part: '(b)(iii)', task: 'Identify the key fungi in the rhizosphere (tick)', notation: '6', decoded: 'The correct tick earns 6 marks.', marks: 6 },
      { part: '(b)(iv)', task: 'Describe advantages of the fungi on soil productivity', notation: '5+1', decoded: 'Two advantages worth 5 and 1 marks.', marks: 6 },
      { part: '(b)(v)', task: 'Outline ways to increase the fungi in soil apart from organic matter', notation: '5+1', decoded: 'Two ways worth 5 and 1 marks.', marks: 6 },
      { part: '(c)(i)', task: 'Predict with reason which soil (loam or peat) has the higher % organic matter', notation: '5+1', decoded: 'The prediction (5m) + reason (1m).', marks: 6 },
      { part: '(c)(ii)', task: 'Calculate A, the % soil organic matter in the peat sample', notation: '6', decoded: 'The calculation earns 6 marks.', marks: 6 },
      { part: '(c)(iii)', task: 'Calculate B, the % soil organic carbon in the peat sample', notation: '6', decoded: 'The calculation earns 6 marks.', marks: 6 },
    ],
    cite: CITE24('Section B Q17'),
  },
];

const AGRICULTURAL_SCIENCE_LENS: SubjectLens = {
  subjectId: 'agricultural-science',
  entries: [...HL_2023, ...HL_2024],
};

export default AGRICULTURAL_SCIENCE_LENS;
