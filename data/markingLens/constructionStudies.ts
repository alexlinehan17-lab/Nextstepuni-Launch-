/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — Construction Studies (written Theory paper, Higher Level).
 *
 * Sources of truth (all in examiner-reports/construction-studies/):
 *  - 2024-marking-scheme.pdf/.md — SEC Marking Scheme 2024, Construction
 *    Studies Higher Level (theory grids on printed pp. 34–43).
 *  - 2025-marking-scheme.pdf/.md — SEC Marking Scheme 2025, Construction
 *    Studies Higher Level (theory grids on printed pp. 1–11 of the theory
 *    section, PDF pp. 37–47).
 * The .md extractions scramble some table columns, so every mark figure below
 * was cross-checked against the filed PDFs page by page. Every question is a
 * PERFORMANCE CRITERIA / MAXIMUM MARK table with named additive rows and a
 * printed TOTAL 60; every entry's parts sum to 60 (machine-checked).
 *
 * The big drawing questions carry a fixed 8-mark Scale/Drafting row printed as
 * a graded band — "Scale - 4 marks / Drafting - 4 marks: Excellent 8, Good 6,
 * Fair 4" — decoded here exactly as printed.
 *
 * Both years' schemes also print a "Question 10 (Alternative)" grid. The Topic
 * Vault stems for n=10 are the MAIN Q10 both years (2024: EnerPHit retrofit;
 * 2025: Passive House design), so only the main Q10 grids carry a lens.
 *
 * Keys (year/level/lang/fileid/n) match the Topic Vault tags exactly:
 *  - 2024 HL (LC029ALP000EV + IV mirror) Q1–10 — 60m each.
 *  - 2025 HL (LC029ALP000EV + IV mirror) Q1–10 — 60m each.
 * No Ordinary Level scheme is filed, so OL papers carry no lens. No Chief
 * Examiner's Report is filed for this subject, so no pitfalls are attached.
 */

import { type QuestionLens, type SubjectLens } from './types';

const CITE_2024 = (q: string) => `SEC Marking Scheme 2024, Construction Studies Higher Level, ${q}`;
const CITE_2025 = (q: string) => `SEC Marking Scheme 2025, Construction Studies Higher Level, ${q}`;

// The IV paper is the same exam marked by the same scheme — mirror EV entries.
const mirrorIV = (entries: QuestionLens[], fileid: string): QuestionLens[] =>
  entries.map(e => ({ ...e, lang: 'iv', fileid }));

// ════════════════════════════════════════════════════════════════════════════
// 2024 Higher Level — theory paper, 10 questions × 60 marks
// Source: examiner-reports/construction-studies/2024-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const HL_2024_EV: QuestionLens[] = [
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '1',
    totalMarks: 60,
    headline: 'A drawing checklist: 12 named elements × 4 marks (3 drawing + 1 annotation), plus a fixed 8-mark Scale/Drafting band and a 4-mark detail.',
    parts: [
      { part: '(a)', task: 'Vertical section through lean-to roof and external walls of a house', notation: 'External wall and eaves 4 × 4 marks · Roof 4 × 4 marks · Front wall of house and abutment 4 × 4 marks (3 for drawing, 1 for annotation)', decoded: 'Twelve named construction elements, 4 marks each: 3 for drawing the element, 1 for its annotation.', marks: 48 },
      { part: '', task: 'Scale and drafting of the drawing', notation: 'Scale - 4 marks · Drafting - 4 marks: Excellent 8, Good 6, Fair 4', decoded: 'A fixed 8-mark quality band for the whole drawing, graded Excellent 8, Good 6 or Fair 4.', marks: 8 },
      { part: '(b)', task: 'Typical design detailing that will ensure ventilation of the roof structure', notation: '(4 marks)', decoded: '4 marks for the identified ventilation design detailing.', marks: 4 },
    ],
    cite: CITE_2024('Q1'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '2',
    totalMarks: 60,
    headline: 'Every design detail is marked Notes 3 + Sketches 3; the en suite layout is credited element by element; each justification splits 1 + 2.',
    parts: [
      { part: '(a)', task: 'Two best practice guidelines when designing a room for lifetime use (kitchen and bedroom)', notation: 'Kitchen (2 details) + Bedroom (2 details): Notes (3) + Sketches (3) each', decoded: 'Four details in all (two kitchen, two bedroom), 6 marks each: 3 for the written note, 3 for the sketch.', marks: 24 },
      { part: '(b)', task: 'Preferred layout for en suite to ensure ease of use by a person with limited mobility', notation: 'Line diagram 4 · Access to en suite 3 · Shower area 3 · Water Closet (W.C.) 3 · Wash basin 3 · Grab rails 3 · Dimensions (any two) 2', decoded: '4 marks for the line diagram, 3 marks for each of the five located items on the annotated sketch, and 2 marks for any two dimensions.', marks: 21 },
      { part: '(c)', task: 'Justify the preferred location for each item at 2(b)', notation: '5 × 3 marks (1 for point, 2 for discussion)', decoded: 'Each of the five locations justified: 1 mark for the point, 2 for its discussion.', marks: 15 },
    ],
    cite: CITE_2024('Q2'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '3',
    totalMarks: 60,
    headline: 'A 26-mark revised layout (holistic 14 + a 3-mark tick per named requirement), a Notes 12 + Sketch 12 redesign, and two 5-mark advantages.',
    parts: [
      { part: '(a)', task: 'Revised internal layout for the proposed renovation', notation: 'Revised internal layout 14 · Linking existing kitchen to the forge 3 · Optimising natural daylight 3 · Maximising the views to the mountain 3 · Justification 3', decoded: '14 marks for the revised layout drawing itself, 3 marks for each of the three named design requirements it satisfies, and 3 for the justification.', marks: 26 },
      { part: '(b)', task: 'External design of forge that will respect and enhance the visual appearance of the house', notation: 'Notes 12 · Sketch 12', decoded: 'Two equal halves: 12 marks for the written notes, 12 for the sketch.', marks: 24 },
      { part: '(c)', task: 'Two advantages of respecting Irish vernacular architecture when renovating an old building', notation: '2 × 5 marks (2 for point, 3 for discussion)', decoded: 'Two advantages, 5 marks each: 2 for the point, 3 for its discussion.', marks: 10 },
    ],
    cite: CITE_2024('Q3'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '4',
    totalMarks: 60,
    headline: 'Two point + discussion parts where the discussion is double the point (2 + 4), then a 24-mark site sketch credited feature by feature.',
    parts: [
      { part: '(a)', task: 'Three reasons why local authorities regulate new dwellings', notation: '3 × 6 marks (2 for point, 4 for discussion)', decoded: 'Three reasons, 6 marks each: 2 for stating the reason, 4 for discussing it.', marks: 18 },
      { part: '(b)', task: 'Selection of preferred site and discuss three considerations for site selection', notation: '3 × 6 marks (2 for point, 4 for discussion)', decoded: 'Three considerations, 6 marks each: 2 for the point, 4 for the discussion.', marks: 18 },
      { part: '(c)', task: 'Sketch site showing house location and orientation, outdoor living space, road entrance and driveway', notation: 'Sketch of selected site 6 · House location and Orientation 5 · Outdoor living space 5 · Road entrance and Driveway 5 · Justification 3', decoded: '6 marks for the site sketch, 5 marks for each of the three required features shown on it, and 3 for the justification.', marks: 24 },
    ],
    cite: CITE_2024('Q4'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '5',
    totalMarks: 60,
    headline: 'A per-step calculation ladder: eleven 3-mark U-value steps, five 3-mark heat-loss-cost steps, then four 3-mark points (1 + 2).',
    parts: [
      { part: '(a)', task: 'U-value of external wall', notation: '(11 × 3 marks): Tabulation · External surface resistance · External render · External insulation · Concrete · Internal insulation · Internal plasterboard · Internal skim coat · Internal resistance · Total resistance · Calculation of U-value', decoded: 'Eleven 3-mark steps: the tabulation, each named layer resistance, the total resistance and the final U-value calculation — the working carries the marks.', marks: 33 },
      { part: '(b)', task: 'Cost of annual heat loss through external wall', notation: 'Heat loss formula and calculation 3 · Heating duration for one year 3 · k/Joules calculation for one year 3 · Kgs of wood pellets for one year 3 · Annual cost of heat loss 3', decoded: 'Five worked steps, 3 marks each.', marks: 15 },
      { part: '(c)', task: 'Two advantages and two disadvantages of incorporating a wood pellet boiler stove', notation: '4 x 3 marks (1 for point, 2 for discussion)', decoded: 'Two advantages and two disadvantages, 3 marks each: 1 for the point, 2 for its discussion.', marks: 12 },
    ],
    cite: CITE_2024('Q5'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '6',
    totalMarks: 60,
    headline: 'Notes + Sketches throughout: three features at 5 + 5, two features at 5 + 5, then two 5-mark advantages (2 + 3).',
    parts: [
      { part: '(a)', task: 'Three features of low environmental impact', notation: '(6 × 5 marks): Notes 5 + Sketches 5 per design feature', decoded: 'Three design features, 10 marks each: 5 for the notes, 5 for the sketches.', marks: 30 },
      { part: '(b)', task: 'Two features that could be added to the house to increase energy efficiency', notation: '(4 × 5 marks): Notes 5 + Sketches 5 per feature', decoded: 'Two features, 10 marks each: 5 for the notes, 5 for the sketches.', marks: 20 },
      { part: '(c)', task: 'Two advantages of designing energy efficient new homes', notation: '2 × 5 marks (2 for point, 3 for discussion)', decoded: 'Two advantages, 5 marks each: 2 for the point, 3 for its discussion.', marks: 10 },
    ],
    cite: CITE_2024('Q6'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '7',
    totalMarks: 60,
    headline: 'The drawing checklist again: 12 elements × 4 (3 drawing + 1 annotation) across wall, window head and floor, plus the 8-mark Scale/Drafting band.',
    parts: [
      { part: '(a)', task: 'Vertical section through timber frame wall, window frame and first floor joist', notation: 'External wall 5 × 4 marks · Head of the window 4 × 4 marks · First floor 3 × 4 marks (3 for drawing, 1 for annotation)', decoded: 'Twelve named construction elements, 4 marks each: 3 for drawing the element, 1 for its annotation.', marks: 48 },
      { part: '', task: 'Scale and drafting of the drawing', notation: 'Scale - 4 marks · Drafting - 4 marks: Excellent 8, Good 6, Fair 4', decoded: 'A fixed 8-mark quality band for the whole drawing, graded Excellent 8, Good 6 or Fair 4.', marks: 8 },
      { part: '(b)', task: 'Design details to ensure airtightness at junction of first floor and wall', notation: '(4 marks)', decoded: '4 marks for the identified design detail.', marks: 4 },
    ],
    cite: CITE_2024('Q7'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '8',
    totalMarks: 60,
    headline: 'A services layout credited per element (7 × 4 + 4), a Notes 6 + Sketches 6 method, and four 4-mark points weighted to the discussion (1 + 3).',
    parts: [
      { part: '(a)', task: 'Typical design layout to provide hot water and central heating', notation: '(7 × 4 marks) + 4 marks (Typical sizes of pipework - any two 4)', decoded: 'Seven credited elements of the hot water and central heating layout, 4 marks each, plus 4 marks for showing typical pipework sizes (any two).', marks: 32 },
      { part: '(b)', task: 'One onsite method of incorporating renewable technology into the hot water system', notation: 'Notes 6 · Sketches 6', decoded: 'Two equal halves: 6 marks for the notes, 6 for the sketches.', marks: 12 },
      { part: '(c)', task: 'Two advantages and two disadvantages of an underfloor heating system', notation: '4 × 4 marks (1 for point, 3 for discussion)', decoded: 'Two advantages and two disadvantages, 4 marks each: 1 for the point, 3 for its discussion.', marks: 16 },
    ],
    cite: CITE_2024('Q8'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '9',
    totalMarks: 60,
    headline: 'Sound question: two requirements at Notes 4 + Sketches 4, a 32-mark floor + stud-wall redesign (Notes 8 + Sketches 8 each), and two approach + principle pairs.',
    parts: [
      { part: '(a)', task: 'Two functional requirements of a home office space', notation: '(4 × 4 marks): Notes 4 + Sketches 4 per requirement', decoded: 'Two functional requirements, 8 marks each: 4 for the notes, 4 for the sketches.', marks: 16 },
      { part: '(b)', task: 'Revised design detailing that will reduce the transmission of sound', notation: 'Floor detail: Notes 8 + Sketches 8 · Stud wall detail: Notes 8 + Sketches 8', decoded: 'Both details marked in equal halves: 8 marks for notes and 8 for sketches on the floor detail, the same on the stud wall detail.', marks: 32 },
      { part: '(c)', task: 'Two approaches used to reduce transmission of sound and the associated principle', notation: 'Approach 4 + Associated sound principle 2 (× 2)', decoded: 'Two approaches: 4 marks for each approach, 2 for its associated sound principle.', marks: 12 },
    ],
    cite: CITE_2024('Q9'),
  },
  {
    year: 2024, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '10',
    totalMarks: 60,
    headline: 'EnerPHit retrofit question: every item is Notes 6 + Sketches 6, closing with two 6-mark advantages split 2 + 4.',
    parts: [
      { part: '(a)', task: 'Discuss the importance of any two in the EnerPHit design standard', notation: '(4 × 6 marks): Notes 6 + Sketches 6 per chosen item', decoded: 'Any two of the listed items, 12 marks each: 6 for the notes, 6 for the sketches.', marks: 24 },
      { part: '(b)', task: 'Improve indoor air quality and space heating when upgrading to meet the EnerPHit standard', notation: '(4 x 6 marks): Notes 6 + Sketches 6 per heading', decoded: 'Indoor air quality and space heating, 12 marks each: 6 for the notes, 6 for the sketches.', marks: 24 },
      { part: '(c)', task: 'Two advantages of using qualified skilled labour when retrofitting to the EnerPHit standard', notation: '2 × 6 marks (2 for point, 4 for discussion)', decoded: 'Two advantages, 6 marks each: 2 for the point, 4 for its discussion.', marks: 12 },
    ],
    cite: CITE_2024('Q10'),
  },
];

// ════════════════════════════════════════════════════════════════════════════
// 2025 Higher Level — theory paper, 10 questions × 60 marks
// Source: examiner-reports/construction-studies/2025-marking-scheme.pdf
// ════════════════════════════════════════════════════════════════════════════

const HL_2025_EV: QuestionLens[] = [
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '1',
    totalMarks: 60,
    headline: 'A drawing checklist: 12 named elements × 4 marks (3 drawing + 1 annotation), plus a fixed 8-mark Scale/Drafting band and a 4-mark detail.',
    parts: [
      { part: '(a)', task: 'Vertical section through foundation, solid ground floor, external wall and window', notation: 'Foundation + Solid ground floor 5 × 4 marks · External wall 4 × 4 marks · Window detail 3 × 4 marks (3 for drawing, 1 for annotation)', decoded: 'Twelve named construction elements, 4 marks each: 3 for drawing the element, 1 for its annotation.', marks: 48 },
      { part: '', task: 'Scale and drafting of the drawing', notation: 'Scale - 4 marks · Drafting - 4 marks: Excellent 8, Good 6, Fair 4', decoded: 'A fixed 8-mark quality band for the whole drawing, graded Excellent 8, Good 6 or Fair 4.', marks: 8 },
      { part: '(b)', task: 'Typical design detailing that will prevent the penetration of radon gas', notation: '(4 marks)', decoded: '4 marks for the identified radon design detailing.', marks: 4 },
    ],
    cite: CITE_2025('Q1'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '2',
    totalMarks: 60,
    headline: 'Safety question: two 6-mark discussions, three 4-mark risks, then six guidelines each split 3 for note + 3 for sketch.',
    parts: [
      { part: '(a)', task: 'The importance of any two in maintaining a positive health and safety culture', notation: '(12 marks): 6 + 6', decoded: 'Any two of safety training, health and safety officer, risk assessment audit — 6 marks each.', marks: 12 },
      { part: '(b)', task: 'One possible safety risk in each of the three scenarios', notation: '(12 marks): 4 + 4 + 4', decoded: 'One safety risk identified per scenario (deep trench, attic insulation, chimney capping), 4 marks each.', marks: 12 },
      { part: '(c)', task: 'Two best practice guidelines to reduce injury, per scenario', notation: '6 × 6 marks: Guideline (3 for note, 3 for sketch)', decoded: 'Two guidelines for each of the three scenarios — six guidelines, 6 marks each: 3 for the written note, 3 for the sketch.', marks: 36 },
    ],
    cite: CITE_2025('Q2'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '3',
    totalMarks: 60,
    headline: 'A 22-mark revised layout (holistic 16 + a 2-mark tick per stated requirement), three 6-mark reasons, and a Notes 10 + Sketch 10 redesign.',
    parts: [
      { part: '(a)', task: 'Revised internal layout for the ground floor and garage space', notation: 'Revised internal layout 16 · Include a downstairs bathroom 2 · Create an open-plan kitchen/dining and living area 2 · Optimising daylight into the ground floor 2', decoded: '16 marks for the revised layout drawing itself, plus a 2-mark tick for each of the three stated design requirements it satisfies.', marks: 22 },
      { part: '(b)', task: 'Three reasons for your proposed layout', notation: '(18 marks): 6 + 6 + 6', decoded: 'Three reasons, 6 marks each.', marks: 18 },
      { part: '(c)', task: 'External design of the garage to enhance the visual appearance', notation: 'Notes 10 · Sketch 10', decoded: 'Two equal halves: 10 marks for the written notes, 10 for the sketch.', marks: 20 },
    ],
    cite: CITE_2025('Q3'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '4',
    totalMarks: 60,
    headline: 'Wall question: requirements at Notes 3 + Sketches 3, wall constructions at 15 each with separate insulation-position and dimension ticks, then four 3-mark points.',
    parts: [
      { part: '(a)', task: 'Three functional requirements of an external wall', notation: '(18 marks): Notes 3 + Sketches 3 per requirement', decoded: 'Three functional requirements, 6 marks each: 3 for the notes, 3 for the sketches.', marks: 18 },
      { part: '(b)', task: 'Two high performance external wall constructions', notation: 'Per wall construction: Notes 5 · Sketches 6 · Position of Insulation 2 · Dimensions 2', decoded: 'Two wall constructions, 15 marks each: notes 5, sketches 6, plus separate 2-mark ticks for showing the position of the insulation and stating dimensions.', marks: 30 },
      { part: '(c)', task: 'One advantage and one disadvantage of each wall type shown in 4(b)', notation: '(12 marks): Advantage 3 + Disadvantage 3 per wall type', decoded: 'For each of the two wall constructions: one advantage (3 marks) and one disadvantage (3 marks).', marks: 12 },
    ],
    cite: CITE_2025('Q4'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '5',
    totalMarks: 60,
    headline: 'A per-step calculation ladder: eleven 3-mark U-value steps, five 3-mark heat-loss-cost steps, four 3-mark insulation-thickness steps.',
    parts: [
      { part: '(a)', task: 'U-value of external wall', notation: '(33 marks): External surface resistance 3 · Acrylic render 3 · External insulation 3 · External sand cement render 3 · Hollow concrete block 3 · Insulation 3 · Plasterboard 3 · Internal skim coat 3 · Internal surface resistance 3 · Total resistance 3 · Calculation of U-value 3', decoded: 'Eleven 3-mark steps: each named layer resistance, the total resistance and the final U-value calculation — the working carries the marks.', marks: 33 },
      { part: '(b)', task: 'Cost of annual heat loss through external wall', notation: 'Heat loss formula and calculation 3 · Heating duration for one year 3 · k/Joules calculation for one year 3 · Kgs of wood pellets for one year 3 · Annual cost of heat loss 3', decoded: 'Five worked steps, 3 marks each.', marks: 15 },
      { part: '(c)', task: 'Required thickness of additional insulation for U-value of 0.11 W/m²°C', notation: 'Resistance for U-value for 0.11 W/m²°C (using R=1/U) 3 · Difference in resistances (required resistance) 3 · Application of formula R = T/k 3 · Required thickness of insulation 3', decoded: 'Four worked steps, 3 marks each: target resistance, difference in resistances, applying R = T/k, and the required thickness.', marks: 12 },
    ],
    cite: CITE_2025('Q5'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '6',
    totalMarks: 60,
    headline: 'Three features at Notes 5 + Sketches 5, then five 6-mark discussion points each split 3 for point + 3 for discussion.',
    parts: [
      { part: '(a)', task: 'Three features of low environmental impact', notation: '(30 marks): Notes 5 + Sketches 5 per design feature', decoded: 'Three design features, 10 marks each: 5 for the notes, 5 for the sketches.', marks: 30 },
      { part: '(b)', task: 'How each of the following contributes to the creation of a healthy indoor environment', notation: '3 × 6 marks (3 for point, 3 for discussion)', decoded: 'Indoor air quality, natural light, and materials and finishes — 6 marks each: 3 for the point, 3 for its discussion.', marks: 18 },
      { part: '(c)', task: 'Two benefits of using locally sourced materials', notation: '2 × 6 marks (3 for point, 3 for discussion)', decoded: 'Two advantages, 6 marks each: 3 for the point, 3 for its discussion.', marks: 12 },
    ],
    cite: CITE_2025('Q6'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '7',
    totalMarks: 60,
    headline: 'Chimney/roof section: 10 elements × 4 (3 drawing + 1 annotation) + 6 for the slate courses, plus the 8-mark Scale/Drafting band and a 6-mark detail.',
    parts: [
      { part: '(a)', task: 'Vertical section through the centre of the chimney stack and roof structure', notation: '10 × 4 marks + 6 marks (3 for drawing, 1 for annotation) · Two courses of slate above and below the chimney stack 6', decoded: 'Ten named chimney/roof elements, 4 marks each (3 for drawing, 1 for annotation), plus 6 marks for showing two courses of slate above and below the chimney stack.', marks: 46 },
      { part: '', task: 'Scale and drafting of the drawing', notation: 'Scale - 4 marks · Drafting - 4 marks: Excellent 8, Good 6, Fair 4', decoded: 'A fixed 8-mark quality band for the whole drawing, graded Excellent 8, Good 6 or Fair 4.', marks: 8 },
      { part: '(b)', task: 'Design details to prevent the penetration of rainwater between the chimney stack and the adjoining roof surface', notation: '(6 marks)', decoded: '6 marks for the identified design detail.', marks: 6 },
    ],
    cite: CITE_2025('Q7'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '8',
    totalMarks: 60,
    headline: 'Two 6-mark benefits (3 + 3), then 48 marks on three airtightness details, each split Notes 8 + Sketches 8.',
    parts: [
      { part: '(a)', task: 'Discuss two benefits of preventing air leakage in a dwelling house', notation: '2 × 6 marks (3 for point, 3 for discussion)', decoded: 'Two benefits, 6 marks each: 3 for the point, 3 for its discussion.', marks: 12 },
      { part: '(b)', task: 'Best practice design detailing to prevent air leakage at any three of the locations circled', notation: '(48 marks): Notes 8 + Sketches 8 per detailing', decoded: 'Any three of the circled locations, 16 marks each: 8 for the notes, 8 for the sketches.', marks: 48 },
    ],
    cite: CITE_2025('Q8'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '9',
    totalMarks: 60,
    headline: 'Wiring layout credited per item (6 × 5, split 4 drawing + 1 annotation, + 4 for cable size and colour), then Notes + Sketches safety features and two 5-mark approaches.',
    parts: [
      { part: '(a)', task: 'Typical wiring layout for two light points controlled by a single switch', notation: '6 × 5 marks + 4 marks (4 for drawing, 1 for annotation) · Cable size (1) and colour (3) 4', decoded: 'Six credited items (distribution board, single switch, two light points, live/neutral/earth cabling), 5 marks each: 4 for drawing, 1 for annotation — plus 4 marks for cable size (1) and colour (3).', marks: 34 },
      { part: '(b)', task: 'Safety features incorporated in the design of the lighting circuit', notation: '(16 marks): Notes 4 + Sketches 4 per safety feature', decoded: 'Two safety features, 8 marks each: 4 for the notes, 4 for the sketches.', marks: 16 },
      { part: '(c)', task: 'Two approaches to reduce electrical consumption', notation: '2 × 5 marks (2 for point, 3 for discussion)', decoded: 'Two approaches, 5 marks each: 2 for the point, 3 for its discussion.', marks: 10 },
    ],
    cite: CITE_2025('Q9'),
  },
  {
    year: 2025, level: 'higher', lang: 'ev', fileid: 'LC029ALP000EV.pdf', n: '10',
    totalMarks: 60,
    headline: 'Passive House question: chosen items at Notes 5 + Sketches 5, a 28-mark orientation part (sketch 8 + two 4-mark features + two 6-mark benefits), and two methods at 3 + 3.',
    parts: [
      { part: '(a)', task: 'Discuss the importance of any two in Passive House design', notation: '(20 marks): Notes 5 + Sketches 5 per chosen item', decoded: 'Any two of building form, foundation design, space heating energy demand — 10 marks each: 5 for the notes, 5 for the sketches.', marks: 20 },
      { part: '(b)', task: 'Preferred orientation for the house and how this benefits the owner', notation: 'Sketch 8 · Orientation 4 · Sunpath 4 · Benefit 1 (3 for point, 3 for discussion) 6 · Benefit 2 (3 for point, 3 for discussion) 6', decoded: '8 marks for the sketch, 4 each for showing the orientation and the sun path, then two benefits at 6 marks each (3 for the point, 3 for its discussion).', marks: 28 },
      { part: '(c)', task: 'Two ways to reduce solar overheating while respecting the house design', notation: '(12 marks): Notes 3 + Sketches 3 per method', decoded: 'Two methods, 6 marks each: 3 for the notes, 3 for the sketches.', marks: 12 },
    ],
    cite: CITE_2025('Q10'),
  },
];

const CONSTRUCTION_STUDIES_LENS: SubjectLens = {
  subjectId: 'construction-studies',
  entries: [
    ...HL_2024_EV,
    ...mirrorIV(HL_2024_EV, 'LC029ALP000IV.pdf'),
    ...HL_2025_EV,
    ...mirrorIV(HL_2025_EV, 'LC029ALP000IV.pdf'),
  ],
};

export default CONSTRUCTION_STUDIES_LENS;
