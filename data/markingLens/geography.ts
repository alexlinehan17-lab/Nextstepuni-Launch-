/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Geography.
 *
 * Sources of truth:
 *  - examiner-reports/geography/2024-marking-scheme.md
 *    (SEC Marking Scheme 2024, Geography Higher Level — Part One, p.4)
 *  - examiner-reports/geography/2025-marking-scheme.md
 *    (SEC Marking Scheme 2025, Geography Higher Level — Part One, p.4)
 *  - examiner-reports/geography/2025-ol-marking-scheme.md
 *    (SEC Marking Scheme 2025, Geography Ordinary Level — Part One, pp.6–7)
 * Every notation below is verbatim from those documents (the Part One grids
 * print each markable answer with its mark, e.g. "Rejuvenation 2m",
 * "Valid answer 2 + 2 marks"); every entry's parts sum to the per-question
 * total from the scheme's own Part One header (HL: "Any 10 questions @ 8
 * marks each"; OL: "ANY TEN QUESTIONS @ 10 MARKS EACH" with a printed
 * "Total 10m" per question) — machine-checked. Pitfalls cite the Chief
 * Examiner's Report 2012 (Geography HL) Part One commentary — the behaviours
 * surfaced with page refs in examiner-reports/geography/2012-insights.md.
 *
 * Geography numbering note (repo audit; see VAULT_PREFER_ANCHORS in
 * components/PaperTrail/vaultResolve.ts): the paper carries two "Q1..12" runs —
 * the vault tags' n = 1..12 are the PART ONE short-answer questions, not the
 * Part Two structured questions. This lens therefore covers ONLY Part One.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2024 HL (LC005ALP043EV + IV mirror) Q1–12 — Part One shorts, 8m each.
 *  - 2025 HL (LC005ALP043EV + IV mirror) Q1–12 — Part One shorts, 8m each.
 *  - 2025 OL (LC005GLP042EV, no IV tag) Q1–12 — Part One shorts, 10m each.
 * Deliberately omitted: the 2025 OL LC005GLP043EV tag run (its 12 questions
 * are the Part Two structured questions — out of this lens's Part One scope),
 * and 2024 OL / earlier years (no marking scheme filed in examiner-reports/).
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE24 = (q: string) => `SEC Marking Scheme 2024, Geography Higher Level, ${q}`;
const CITE25 = (q: string) => `SEC Marking Scheme 2025, Geography Higher Level, ${q}`;
const CITE25OL = (q: string) => `SEC Marking Scheme 2025, Geography Ordinary Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

const HL_HEADLINE =
  'An 8-mark Part One short answer — the scheme marks every question attempted and awards the 10 with the highest marks (Any 10 questions @ 8 marks each; no grading).';
const OL_HEADLINE =
  'A 10-mark Part One short answer — the scheme marks every question attempted and awards the ten with the highest marks (ANY TEN QUESTIONS @ 10 MARKS EACH).';

// ── 2024 Higher Level — Part One (12 short answers, 8 marks each) ────────────

const hl24 = (n: string, notation: string, decoded: string): QuestionLens => ({
  year: 2024,
  level: 'higher',
  lang: 'ev',
  fileid: 'LC005ALP043EV.pdf',
  n,
  totalMarks: 8,
  headline: HL_HEADLINE,
  parts: [{ part: '', task: 'Short-answer question', notation, decoded, marks: 8 }],
  cite: CITE24(`Part One Q${n}`),
});

const HL_2024: QuestionLens[] = [
  {
    ...hl24(
      '1',
      'River Confluence 2m · Headland 2m · Ox bow lake 2m · Tarn 2m',
      'Four features identified, 2 marks each.'
    ),
    pitfall: {
      text: 'Identification slips are the documented Part One weakness — the Chief Examiner flags candidates confusing an arête, a pyramidal peak and a lateral moraine on the equivalent landform-identification short question.',
      cite: "Chief Examiner's Report 2012 (Geography HL), p.23",
    },
  },
  hl24(
    '2',
    '(i) C 1m · A 1m · B 1m · D 1m · (ii) Chemical 1m · Physical/Mechanical 1m · Physical/Mechanical 1m · Chemical 1m',
    'Part (i): four letters, 1 mark each. Part (ii): four classifications, 1 mark each.'
  ),
  hl24(
    '3',
    '(i) D 1m · B 1m · A 1m · C 1m · (ii) Rejuvenation 2m · (iii) Valid reason 2m',
    'Part (i): four letters, 1 mark each. Part (ii): the term, 2 marks. Part (iii): a valid reason, 2 marks.'
  ),
  hl24(
    '4',
    '(i) C 1m · D 1m · B 1m · A 1m · (ii) (a) True 2m · (b) True 2m',
    'Part (i): four letters, 1 mark each. Part (ii): two true/false answers, 2 marks each.'
  ),
  hl24(
    '5',
    '(i) C 1m · E 1m · F 1m · D 1m · B 1m · A 1m · (ii) True 2m',
    'Part (i): six letters, 1 mark each. Part (ii): one true/false answer, 2 marks.'
  ),
  {
    ...hl24(
      '6',
      '(i) Urban 1m · Geomorphological 1m · Climatic 1m · Administrative 1m · (ii) Berlin 1m · The Burren 1m · Hot Desert 1m · Co. Leitrim 1m',
      'Part (i): four answers, 1 mark each. Part (ii): four examples, 1 mark each.'
    ),
    pitfall: {
      text: 'On the equivalent regions short question the Chief Examiner reports that brief definitions of regions were poorly done — each region answer and example here carries its own mark.',
      cite: "Chief Examiner's Report 2012 (Geography HL), p.23",
    },
  },
  hl24(
    '7',
    '(i) W 006 533 2m · (ii) 8.5 (km) 2m · (iii) Star Shaped Fort 2m · (iv) 18 (km²) 2m',
    'Four answers, 2 marks each.'
  ),
  hl24(
    '8',
    'B Centre Middleground 2m · C Right Foreground 2m · D Right Background 2m · E Left Middleground 2m',
    'Four photograph positions, 2 marks each.'
  ),
  hl24(
    '9',
    '(i) Mealagh River 2m · (ii) Even 2m · (iii) Glanaclougha Loop 2m · (iv) Coniferous (Plantation) 2m',
    'Four answers, 2 marks each.'
  ),
  hl24(
    '10',
    '(i) Mayo 2m · (ii) Four 2m · (iii) 146 2m · (iv) Isohels 2m',
    'Four answers, 2 marks each.'
  ),
  hl24(
    '11',
    '(i) 1070 2m · (ii) 2020 2m · (iii) 1314 2m · (iv) Valid explanation 1 + 1m',
    'Parts (i)–(iii): 2 marks each. Part (iv): an explanation marked 1 + 1.'
  ),
  hl24('12', 'C 2m · B 2m · A 2m · D 2m', 'Four letters, 2 marks each.'),
];

// ── 2025 Higher Level — Part One (12 short answers, 8 marks each) ────────────

const hl25 = (n: string, notation: string, decoded: string): QuestionLens => ({
  year: 2025,
  level: 'higher',
  lang: 'ev',
  fileid: 'LC005ALP043EV.pdf',
  n,
  totalMarks: 8,
  headline: HL_HEADLINE,
  parts: [{ part: '', task: 'Short-answer question', notation, decoded, marks: 8 }],
  cite: CITE25(`Part One Q${n}`),
});

const HL_2025: QuestionLens[] = [
  {
    ...hl25(
      '1',
      '(i) Convection Current 2 marks · (ii) Subduction 2 marks · (iii) Ocean Trench 2 marks · (iv) Lithosphere 2 marks',
      'Four terms identified, 2 marks each.'
    ),
    pitfall: {
      text: 'On the equivalent plate-tectonics short question the Chief Examiner reports candidates had difficulty identifying the asthenosphere — each named feature here carries its own 2 marks.',
      cite: "Chief Examiner's Report 2012 (Geography HL), p.23",
    },
  },
  hl25(
    '2',
    '(i) B 1 mark · D 1 mark · A 1 mark · C 1 mark · (ii) (a) True 2 marks · (b) True 2 marks',
    'Part (i): four letters, 1 mark each. Part (ii): two true/false answers, 2 marks each.'
  ),
  hl25(
    '3',
    '(i) A 1 mark · D 1 mark · B 1 mark · C 1 mark · (ii) Valid answer 2 marks · (iii) Valid answer 2 marks',
    'Part (i): four letters, 1 mark each. Parts (ii) and (iii): a valid answer, 2 marks each.'
  ),
  hl25(
    '4',
    '(i) @ 1 mark each — table: Sand · Sandstone · Quartzite · Molten Rock · Basalt · Schist · (ii) Valid answer 1 + 1 mark',
    'Part (i): the six table entries, 1 mark each. Part (ii): a valid answer marked 1 + 1.'
  ),
  hl25(
    '5',
    '(i) D 1 mark · A 1 mark · B 1 mark · C 1 mark · (ii) Valid answer 2 + 2 marks',
    'Part (i): four letters, 1 mark each. Part (ii): a valid answer marked 2 + 2.'
  ),
  hl25(
    '6',
    '@ 1 mark each — table: Dingle · Co. Kerry · Ruhr Valley · Germany · Wicklow Mountains · Leinster · Paris Basin · France',
    'The eight table entries, 1 mark each.'
  ),
  hl25(
    '7',
    '(i) M 123 432 2 marks · (ii) 6 - 7 (km²) 2 marks · (iii) 7.8 (km) 2 marks · (iv) Irish Speaking Area 2 marks',
    'Four answers, 2 marks each.'
  ),
  hl25(
    '8',
    '(i) Owenriff river 2 marks · (ii) M 122 427 2 marks · (iii) N59 2 marks · (iv) North East 2 marks',
    'Four answers, 2 marks each.'
  ),
  hl25(
    '9',
    'A Centre foreground 2 marks · B Right background 2 marks · C Left foreground 2 marks · D Left middleground 2 marks',
    'Four photograph positions, 2 marks each.'
  ),
  hl25(
    '10',
    '(i) 1013 2 marks · (ii) False 2 marks · (iii) Isobars 2 marks · (iv) Occluded 2 marks',
    'Four answers, 2 marks each.'
  ),
  hl25(
    '11',
    '(i) Australian 2 marks · (ii) 1,034,132 2 marks · (iii) 34.4 (%) 2 marks · (iv) Valid answer 2 marks',
    'Four answers, 2 marks each.'
  ),
  hl25(
    '12',
    '(i) 3 (%) 2 marks · (ii) 13 (%) 2 marks · (iii) True 2 marks · (iv) Valid answer 1 + 1 mark',
    'Parts (i)–(iii): 2 marks each. Part (iv): a valid answer marked 1 + 1.'
  ),
];

// ── 2025 Ordinary Level — Part One (12 short answers, 10 marks each) ─────────

const ol25 = (n: string, notation: string, decoded: string): QuestionLens => ({
  year: 2025,
  level: 'ordinary',
  lang: 'ev',
  fileid: 'LC005GLP042EV.pdf',
  n,
  totalMarks: 10,
  headline: OL_HEADLINE,
  parts: [{ part: '', task: 'Short-answer question', notation, decoded, marks: 10 }],
  cite: CITE25OL(`Part One Q${n}`),
});

const OL_2025: QuestionLens[] = [
  ol25('1', 'B 2m · E 2m · A 2m · D 2m · C 2m', 'Five letters, 2 marks each.'),
  ol25(
    '2',
    '(i) C 2m · B 2m · A 2m · (ii)(a) False 2m · (ii)(b) True 2m',
    'Part (i): three letters, 2 marks each. Part (ii): two true/false answers, 2 marks each.'
  ),
  ol25(
    '3',
    '(i) C 2m · A 2m · B 2m · D 2m · (ii) Erosion 2m',
    'Part (i): four letters, 2 marks each. Part (ii): the term, 2 marks.'
  ),
  ol25(
    '4',
    '(i) B 2m · C 2m · (ii) Sedimentary 2m · Metamorphic 2m · Igneous 2m',
    'Part (i): two letters, 2 marks each. Part (ii): three rock types, 2 marks each.'
  ),
  ol25('5', '(i) North east 5m · (ii) 7 km² 5m', 'Two answers, 5 marks each.'),
  ol25(
    '6',
    '(i) 18hole golf 2m · Cycle route 2m · Cillin 2m · (ii) National (secondary) 2m · (iii) Correctly drawn symbol 2m',
    'Part (i): three answers, 2 marks each. Part (ii): 2 marks. Part (iii): a correctly drawn symbol, 2 marks.'
  ),
  ol25(
    '7',
    '(i) False 2m · (ii) False 2m · (iii) True 2m · (iv) True 2m · (v) True 2m',
    'Five true/false answers, 2 marks each.'
  ),
  ol25('8', 'B 2m · E 2m · A 2m · D 2m · C 2m', 'Five letters, 2 marks each.'),
  ol25(
    '9',
    '(i) 1973 2m · (ii) 3 2m · (iii) Croatia 2m · (iv) 2004 2m · (v) Valid advantage 2m',
    'Parts (i)–(iv): 2 marks each. Part (v): a valid advantage, 2 marks.'
  ),
  ol25(
    '10',
    '(i) C 2m · D 2m · A 2m · B 2m · (ii) Anticyclone 2m',
    'Part (i): four letters, 2 marks each. Part (ii): the term, 2 marks.'
  ),
  ol25(
    '11',
    '(i) 32 (%) 2m · (ii) Monaghan & Longford 2m · (iii) Car 2m · (iv) 2,320,297 2m · (v) Valid impact 2m',
    'Parts (i)–(iv): 2 marks each. Part (v): a valid impact, 2 marks.'
  ),
  ol25(
    '12',
    '(i) D 2m · A 2m · C 2m · B 2m · (ii) Dormant 2m',
    'Part (i): four letters, 2 marks each. Part (ii): the term, 2 marks.'
  ),
];

const GEOGRAPHY_LENS: SubjectLens = {
  subjectId: 'geography',
  entries: [
    ...HL_2024,
    ...mirrorIV(HL_2024, 'LC005ALP043IV.pdf'),
    ...HL_2025,
    ...mirrorIV(HL_2025, 'LC005ALP043IV.pdf'),
    ...OL_2025,
  ],
};

export default GEOGRAPHY_LENS;
