/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Coursework Companion — the coursework/project/practical components, as the
 * filed SEC marking schemes actually mark them.
 *
 * AUTHORED-BUT-STRICTLY-CITED (the Oral Trainer register, not a projection):
 * there is no machine-readable coursework corpus to project from, so each
 * component below was extracted from the named filed SEC marking scheme in
 * /examiner-reports/ and every marks figure, criterion, grade band and printed
 * note traces to that document (the `filed` path is the re-verification trail;
 * see compliance/evidence/coursework-companion.md for the claim-by-claim
 * record). Where a scheme prints NO component total, `totalMarks` is null —
 * we never assert an unprinted total, even when the printed criteria happen to
 * sum to a round number. Where a scheme prints no percentage weighting or
 * deadline, none is stated. Subjects whose filed schemes carry no coursework
 * criteria (e.g. LCVP — its filed scheme covers the written paper only) are
 * simply absent.
 *
 * Marking schemes cite the SEC exam material archive, where every scheme is
 * published: https://www.examinations.ie/exammaterialarchive/
 */

import type { CourseworkComponent } from './types';

const ARCHIVE = 'https://www.examinations.ie/exammaterialarchive/';

export const COURSEWORK_COMPONENTS: CourseworkComponent[] = [
  // ── Home Economics — Food Studies Practical Coursework (2025 scheme) ──────
  {
    id: 'home-economics-s-and-s|food-studies-coursework',
    subjectId: 'home-economics-s-and-s',
    subjectLabel: 'Home Economics',
    name: 'Food Studies Practical Coursework',
    whatItIs:
      'A record of Food Studies assignments presented for examination — each assignment comprises an investigation, preparation and planning, implementation (the practical activity) and evaluation.',
    totalMarks: 160,
    criteria: [
      {
        name: 'Investigation: Analysis/Research',
        marks: 32,
        whatItRewards:
          'Exploration and analysis of the assignment’s key requirements (24, banded A–D), suitable menus/dishes/products chosen (4), two sources (4).',
      },
      {
        name: 'Preparation and Planning',
        marks: 8,
        whatItRewards:
          'Resources: quantities (2), ingredients (2), costing (2), equipment (2) — for the sensory-analysis area of practice: product/s (2) + equipment (6).',
      },
      {
        name: 'Implementation',
        marks: 28,
        whatItRewards:
          'Procedure in own words, correct sequence (16, banded A–D); two key factors explained (8); one safety and one hygiene issue (4).',
      },
      {
        name: 'Evaluation',
        marks: 12,
        whatItRewards:
          'Three points at 4 marks: evaluation of the implementation and of the specific requirements of the assignment.',
      },
    ],
    // The criteria describe ONE assignment (they sum to 80); the 160 total is
    // the grading table's scale across the assignments presented.
    criteriaComplete: false,
    gradeBands: [
      { grade: 1, markBand: '144–160' },
      { grade: 2, markBand: '128–143' },
      { grade: 3, markBand: '112–127' },
      { grade: 4, markBand: '96–111' },
      { grade: 5, markBand: '80–95' },
      { grade: 6, markBand: '64–79' },
      { grade: 7, markBand: '48–63' },
      { grade: 8, markBand: 'Less than 47' },
    ],
    structure:
      'Each assignment is marked out of 80 (32 + 8 + 28 + 12). The scheme states candidates present a record of assignments for examination — 2 assignments for 2025 “as a result of adjustments” — and each must include a different practical activity. The grading table marks the coursework out of 160.',
    source:
      'SEC Marking Scheme 2025, Home Economics (Scientific and Social) — Food Studies Coursework — © State Examinations Commission',
    filed: 'examiner-reports/home-economics/2025-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── Agricultural Science — Individual Investigative Study (2024 scheme) ───
  {
    id: 'agricultural-science|individual-investigative-study',
    subjectId: 'agricultural-science',
    subjectLabel: 'Agricultural Science',
    name: 'Individual Investigative Study (IIS)',
    whatItIs:
      'A candidate-conducted investigation based on an SEC brief theme, written up as a structured report and marked section by section against printed criteria.',
    // No overall IIS total or percentage weighting is printed in the filed scheme.
    totalMarks: null,
    criteria: [
      {
        name: 'Introduction and background research',
        marks: 20,
        whatItRewards:
          'Addressing and contextualising the brief theme; interrogating relevant, authoritative, credible sources with knowledge of the theme. Suggested 300–500 words.',
      },
      {
        name: 'The investigative process',
        marks: 25,
        whatItRewards:
          'A clear, valid hypothesis tested; the investigative design; how data was gathered. Suggested 500–800 words.',
      },
      {
        name: 'Results, analysis and conclusions',
        marks: 35,
        whatItRewards:
          'Relevant data analysed, interpreted, evaluated and presented; independent conclusions justifying the hypothesis. Suggested 600–1000 words.',
      },
      {
        name: 'Reflection on the study',
        marks: 10,
        whatItRewards:
          'Self-reflection on the completed study — learning gained, reliability, errors and possible changes, linked to the theme and hypothesis. Suggested 150–200 words.',
      },
      {
        name: 'Communication and innovation',
        marks: 10,
        whatItRewards:
          'Overall coherence, clarity and structure across the report, with individual innovative thinking (not a distinct report section).',
      },
    ],
    criteriaComplete: true,
    structure:
      'Each section is marked with a single mark using five band descriptors (Excellent / Very Good / Good / Fair / Weak). References carry no separate mark — they are checked within sections. The scheme prints no overall IIS total or percentage weighting.',
    source:
      'SEC Marking Scheme 2024, Agricultural Science Higher Level — Individual Investigative Study — © State Examinations Commission',
    filed: 'examiner-reports/agricultural-science/2024-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── Construction Studies — Practical Coursework (2025 scheme, Form A) ─────
  {
    id: 'construction-studies|practical-coursework',
    subjectId: 'construction-studies',
    subjectLabel: 'Construction Studies',
    name: 'Practical Coursework',
    whatItIs:
      'A candidate-produced coursework project comprising a design folio/report and a manufactured artefact, marked under four printed criteria headings (Form A).',
    totalMarks: 150,
    criteria: [
      {
        name: 'A. Planning of Project',
        marks: 40,
        whatItRewards:
          'Coursework selection, exploration and management planning; investigation and research; design development through annotated sketches, working drawing(s) and/or models.',
      },
      {
        name: 'B. Report',
        marks: 35,
        whatItRewards:
          'Sequence of manufacture with photographic evidence and/or sketches; critical appraisal and conclusions; quality of communication and presentation of the folio.',
      },
      {
        name: 'C. Manipulative Skills',
        marks: 40,
        whatItRewards:
          'Marking-out of materials; processing and assembly; range and depth of skills evident in the artefact.',
      },
      {
        name: 'D. Completion of Project',
        marks: 35,
        whatItRewards:
          'Artefact well finished; creativity and appropriateness; overall quality, coherence and presentation of the coursework.',
      },
    ],
    criteriaComplete: true,
    structure:
      'The scheme prints: “While the general headings and marks above will largely remain the same, breakdowns may vary for any given year.”',
    source:
      'SEC Marking Scheme 2025, Construction Studies — Practical Coursework — © State Examinations Commission',
    filed: 'examiner-reports/construction-studies/2025-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── Construction Studies — Practical Test (2025 scheme, Common Level) ─────
  {
    id: 'construction-studies|practical-test',
    subjectId: 'construction-studies',
    subjectLabel: 'Construction Studies',
    name: 'Practical Test (Common Level)',
    whatItIs:
      'A supervised hand-skills test in which candidates produce an artefact from a working drawing; marked on assembly, marking out and the processing of each joint.',
    totalMarks: 150,
    criteria: [
      { name: 'Overall Assembly', marks: 14, whatItRewards: 'Quality of the assembled artefact (10); design and applied shaping to edges (4).' },
      { name: 'Marking Out', marks: 51, whatItRewards: 'Marking out of all the joints, slopes, curves and chamfer across the piece.' },
      { name: 'Processing — Barefaced mortice and tenon joint', marks: 9, whatItRewards: 'Mortice (3) and tenon (6).' },
      { name: 'Processing — Notched housing joint', marks: 12, whatItRewards: 'Horizontal trench sawing/paring (4); vertical trenches (8).' },
      { name: 'Processing — Halving joint', marks: 8, whatItRewards: 'Sawing across the grain and paring of trenches to depth.' },
      { name: 'Processing — Dovetail joint', marks: 12, whatItRewards: 'Sawing and paring the tail (8) and the trench (4).' },
      { name: 'Processing — Housing joint (base)', marks: 4, whatItRewards: 'Sawing across the grain and paring of trench to depth.' },
      { name: 'Processing — Mortice and tenon joint', marks: 7, whatItRewards: 'Mortice (3) and tenon (4).' },
      { name: 'Processing — Box dovetail joint', marks: 16, whatItRewards: 'Tails (8); pins — sawing with the grain and paring across the grain (8).' },
      { name: 'Processing — Shaping and drilling', marks: 17, whatItRewards: 'Short slope (1), long slopes (4), curves (4), accurate drilling (6), chamfer (2).' },
    ],
    criteriaComplete: true,
    structure:
      'The artefact is hand produced without machinery (a battery-powered screwdriver is allowed); where machinery is used for a procedure, that procedure is marked out of 50% of its available marks. The scheme is printed in three versions (Day 1 / Day 2 / Day 3), each marked out of 150 with the same criteria.',
    source:
      'SEC Marking Scheme 2025, Construction Studies Common Level — Practical Test — © State Examinations Commission',
    filed: 'examiner-reports/construction-studies/2025-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── DCG — Student Assignment (2025 scheme, Higher Level) ──────────────────
  {
    id: 'design-and-communication-graphics|student-assignment',
    subjectId: 'design-and-communication-graphics',
    subjectLabel: 'Design & Communication Graphics',
    name: 'Student Assignment (Higher Level)',
    whatItIs:
      'A coursework project combining design research, freehand graphics and SolidWorks CAD modelling of a selected artefact and a design modification/concept, assessed against a printed assessment sheet.',
    // The assessment sheet prints no grand total (the total row is blank).
    totalMarks: null,
    criteria: [
      {
        name: 'Design Research & Design Feature Comparison',
        marks: 30,
        whatItRewards:
          'Exploring the brief, researching artefacts, selecting two, illustrating and comparing design features with effective sketches and layout.',
      },
      {
        name: 'Freehand Graphical Representation',
        marks: 20,
        whatItRewards:
          'Rendered 3D freehand drawing of the artefact — geometry, proportion/form/volume, tone/line rendering, effective layout.',
      },
      {
        name: 'SolidWorks Parts, Assembly, Drawing and eDrawing file',
        marks: 35,
        whatItRewards:
          'Filing structure (4), minimum 5 part files (2), part-modelling proficiency (15), design intent/difficulty (5), assembly and mating (7), eDrawing (2).',
      },
      {
        name: 'Hardcopy outputs from SolidWorks',
        marks: 15,
        whatItRewards:
          'Detailed orthographic views with dimensions/notes/symbols, rendered pictorial view, exploded view, section/detail views, effective sheet layout.',
      },
      {
        name: 'Graphical exploration of design solution',
        marks: 25,
        whatItRewards:
          'Analysing possible modifications or a concept design; developing and justifying a chosen solution with sketches, images and annotations.',
      },
      {
        name: 'Presentation of Modification/Concept Design',
        marks: 10,
        whatItRewards:
          'Rendered 3D freehand presentation of the modification/concept — proportion/form/volume, tone/line rendering, layout.',
      },
      {
        name: 'SolidWorks files and Hardcopy output (design solution)',
        marks: 25,
        whatItRewards:
          'Modelling the design solution with design intent/difficulty (13); orthographic views, rendered pictorial, photorealistic image, sheet layout (12).',
      },
    ],
    criteriaComplete: true,
    structure:
      'The assessment sheet prints a deduction row for pages in excess of the maximum, and prints no grand total — the seven printed criterion marks are listed as marked.',
    source:
      'SEC Marking Scheme 2025, Design and Communication Graphics Higher Level — Student Assignment — © State Examinations Commission',
    filed: 'examiner-reports/dcg/2025-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── Engineering — Practical Examination (2025 scheme, Higher Level) ───────
  {
    id: 'engineering|practical-examination',
    subjectId: 'engineering',
    subjectLabel: 'Engineering',
    name: 'Practical Examination',
    whatItIs:
      'A supervised test-piece manufacturing examination — candidates mark out, machine and assemble specified metal parts, marked against a per-section grid.',
    totalMarks: 100,
    criteria: [
      {
        name: 'All parts of test-piece',
        marks: 20,
        whatItRewards: 'Assembly (5), function (10) and finish (5) of the complete test-piece.',
      },
      {
        name: 'Part 11',
        marks: 20,
        whatItRewards: 'Marking out (5), 10 mm × 3 mm slots (5), length and holes (5), top profile (5).',
      },
      {
        name: 'Parts 2 (left and right)',
        marks: 20,
        whatItRewards: 'Per part (10 each): marking out with holes (5), external profile (5).',
      },
      {
        name: 'Parts 7 and 9',
        marks: 20,
        whatItRewards: 'Part 7 (5): marking out, hole, external profile. Part 9 (15): holes, locking slots, profile and recesses.',
      },
      {
        name: 'Part 10',
        marks: 20,
        whatItRewards: 'Marking out (5); drill and tap M5, drill and countersink (5); length and radii (5); 6 mm slots (5).',
      },
    ],
    criteriaComplete: true,
    structure:
      'The grid is marked out of 100 and the scheme prints “100 Marks (× 1.5 = 150 Total)”. Three marking grids are printed (Day 1 / Day 2 / Day 3) with the same five 20-mark sections, differing only in small part-dimension details.',
    source:
      'SEC Marking Scheme 2025, Engineering Higher Level — Practical Examination — © State Examinations Commission',
    filed: 'examiner-reports/engineering/2025-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── Art — Practical Coursework + Invigilated Practical (2024 scheme) ──────
  {
    id: 'art|practical-components',
    subjectId: 'art',
    subjectLabel: 'Art',
    name: 'Practical Coursework & Invigilated Practical Examination',
    whatItIs:
      'Two practical components based on a common brief and viewed as one project: a Visual Journal with development work leading to two artefacts (Practical Coursework), plus the realised Artefact B produced as the Invigilated Practical Examination.',
    // The scheme prints the components separately (250 and 100); it prints no
    // single combined practical total, so none is asserted here.
    totalMarks: null,
    criteria: [
      { name: 'Investigation of theme (per artefact)', marks: 10, whatItRewards: 'A sustained, meaningful, creative and varied investigation of the theme in the Visual Journal.' },
      { name: 'Primary sources (per artefact)', marks: 25, whatItRewards: 'Appropriate primary sources chosen (5) and analysed through drawing with a range of visual means, media and techniques (20).' },
      { name: 'Development (per artefact)', marks: 40, whatItRewards: 'Imaginative development of concepts with an annotated visual record (30); learning from Visual Studies informing the work (10).' },
      { name: 'Realised artefact (per artefact)', marks: 90, whatItRewards: 'Realisation of intentions (30); art elements and design principles (20); media, materials and techniques (30); overall impact (10).' },
      { name: 'Two distinctly different areas of practice (per artefact)', marks: 10, whatItRewards: 'Realising the two artefacts through distinctly different areas of practice, using different materials and techniques.' },
    ],
    criteriaComplete: false,
    structure:
      'The scheme prints the component table: Practical Coursework 250 marks (50%), Invigilated Practical Examination 100 marks (20%), Written Examination — Visual Studies 150 marks (30%). Criteria are printed per artefact (A and B alike), each marked by Low/Moderate/High band then a mark within it. Coursework marks apply to the Visual Journal, the development and realisation of Artefact A and the development of Artefact B; the Invigilated Practical marks apply to the realised Artefact B. The brief is a common examination paper — Higher and Ordinary candidates receive the same stimulus, with Ordinary marks converted from the common reference scale.',
    source:
      'SEC Marking Scheme 2024, Art — Practical Coursework and Invigilated Practical Examination — © State Examinations Commission',
    filed: 'examiner-reports/art/2024-visual-studies-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },

  // ── Geography — Geographical Investigation (2025 scheme) ──────────────────
  {
    id: 'geography|geographical-investigation',
    subjectId: 'geography',
    subjectLabel: 'Geography',
    name: 'Geographical Investigation',
    whatItIs:
      'A report on a fieldwork investigation, marked section by section in a reporting booklet.',
    // No component total is printed in the filed scheme.
    totalMarks: null,
    criteria: [
      { name: 'Introduction', marks: 5, whatItRewards: 'Aims that relate to the investigation, specific and qualified (4 SRPs @ 1; coherence 1).' },
      { name: 'Planning', marks: 5, whatItRewards: 'Identifying the information required and the methods of gathering it (4 SRPs @ 1; coherence 1).' },
      { name: 'Gathering of Data', marks: 40, whatItRewards: 'Two methods/tasks, activity-based and tied to the stated aims (SRPs @ 2; graded coherence marks).' },
      { name: 'Results, Conclusions, Evaluation', marks: 30, whatItRewards: 'Three headings @ 8 marks: results, conclusions and evaluations tied to the aims and gathering activities.' },
      { name: 'Organisation & Presentation of Results', marks: 20, whatItRewards: 'Two different presentation forms (graph, chart, map, table or sketch); overall coherence graded.' },
    ],
    criteriaComplete: true,
    structure:
      'Marks are only awarded for material in the appropriate section of the reporting booklet. The scheme prints the same section names and marks in the 2024 and 2025 schemes; no component total or deadline is printed.',
    source:
      'SEC Marking Scheme 2025, Geography — Geographical Investigation — © State Examinations Commission',
    filed: 'examiner-reports/geography/2025-marking-scheme.md',
    sourceUrl: ARCHIVE,
  },
];

export interface CourseworkSubject {
  id: string;
  label: string;
  count: number;
}

/** Subjects that have at least one grounded coursework component, with counts. */
export function courseworkSubjects(): CourseworkSubject[] {
  const m = new Map<string, CourseworkSubject>();
  for (const c of COURSEWORK_COMPONENTS) {
    const found = m.get(c.subjectId);
    if (found) found.count += 1;
    else m.set(c.subjectId, { id: c.subjectId, label: c.subjectLabel, count: 1 });
  }
  return [...m.values()].sort((a, b) => a.label.localeCompare(b.label));
}

/** The coursework components for one subject. */
export function componentsForSubject(subjectId: string): CourseworkComponent[] {
  return COURSEWORK_COMPONENTS.filter(c => c.subjectId === subjectId);
}

export type { CourseworkComponent, CourseworkCriterion, CourseworkGradeBand } from './types';
