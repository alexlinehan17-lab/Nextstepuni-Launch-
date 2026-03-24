/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// ─── Types ───────────────────────────────────────────────────────────────────

export interface PastPaperQuestion {
  year: number;
  paper: string;       // "Paper 1", "Paper 2", "Paper 1 & 2"
  question: string;    // "Q1", "Q6(b)", "Q7", "Section B Q5"
  marks: number;       // marks allocated to this question
  note?: string;       // optional extra context e.g. "Combined with Functions"
}

export interface TopicPaperTrail {
  subject: string;
  topic: string;
  questions: PastPaperQuestion[];
}

// ─── SEC Archive Link ────────────────────────────────────────────────────────

/** Returns a link to the SEC exam material archive for a given subject */
export function getSecArchiveUrl(): string {
  return 'https://www.examinations.ie/exammaterialarchive/';
}

// ─── Past Paper Data ─────────────────────────────────────────────────────────
//
// Question references for Leaving Certificate Higher Level papers.
// Source: SEC published exam papers 2019-2023.
// Format: { year, paper, question, marks, note? }

const PAST_PAPER_DATA: TopicPaperTrail[] = [

  // ═══════════════════════════════════════════════════════════════════════════
  // MATHEMATICS (Higher Level)
  // ═══════════════════════════════════════════════════════════════════════════

  { subject: 'Mathematics', topic: 'Algebra', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q1', marks: 25, note: 'Expressions & equations' },
    { year: 2023, paper: 'Paper 1', question: 'Q3', marks: 25, note: 'Simultaneous equations' },
    { year: 2022, paper: 'Paper 1', question: 'Q1', marks: 25 },
    { year: 2022, paper: 'Paper 1', question: 'Q2', marks: 25, note: 'Inequalities & logs' },
    { year: 2021, paper: 'Paper 1', question: 'Q1', marks: 25 },
    { year: 2020, paper: 'Paper 1', question: 'Q1', marks: 25 },
    { year: 2019, paper: 'Paper 1', question: 'Q1', marks: 25 },
  ]},
  { subject: 'Mathematics', topic: 'Complex Numbers', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q4', marks: 25, note: 'De Moivre\'s theorem' },
    { year: 2022, paper: 'Paper 1', question: 'Q3', marks: 25 },
    { year: 2021, paper: 'Paper 1', question: 'Q3', marks: 25, note: 'Argand diagram' },
    { year: 2020, paper: 'Paper 1', question: 'Q3', marks: 25 },
    { year: 2019, paper: 'Paper 1', question: 'Q3', marks: 50, note: 'Section B — extended question' },
  ]},
  { subject: 'Mathematics', topic: 'Sequences & Series', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q2', marks: 25 },
    { year: 2022, paper: 'Paper 1', question: 'Q4', marks: 25, note: 'Geometric series' },
    { year: 2021, paper: 'Paper 1', question: 'Q2', marks: 25 },
    { year: 2019, paper: 'Paper 1', question: 'Q2', marks: 25, note: 'Sum to infinity' },
  ]},
  { subject: 'Mathematics', topic: 'Functions', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q5', marks: 25, note: 'Graphing & transformations' },
    { year: 2022, paper: 'Paper 1', question: 'Q5', marks: 25 },
    { year: 2021, paper: 'Paper 1', question: 'Q5', marks: 25, note: 'Injective/surjective' },
    { year: 2020, paper: 'Paper 1', question: 'Q4', marks: 25 },
    { year: 2019, paper: 'Paper 1', question: 'Q4', marks: 25 },
  ]},
  { subject: 'Mathematics', topic: 'Calculus', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q7', marks: 50, note: 'Differentiation — max/min' },
    { year: 2023, paper: 'Paper 1', question: 'Q8', marks: 50, note: 'Integration — area' },
    { year: 2022, paper: 'Paper 1', question: 'Q7', marks: 50, note: 'Rates of change' },
    { year: 2022, paper: 'Paper 1', question: 'Q8', marks: 50, note: 'Integration — trapezoidal rule' },
    { year: 2021, paper: 'Paper 1', question: 'Q7', marks: 50, note: 'First principles + applications' },
    { year: 2021, paper: 'Paper 1', question: 'Q8', marks: 50, note: 'Integration' },
    { year: 2020, paper: 'Paper 1', question: 'Q7', marks: 50, note: 'Differentiation' },
    { year: 2020, paper: 'Paper 1', question: 'Q8', marks: 50, note: 'Integration' },
    { year: 2019, paper: 'Paper 1', question: 'Q7', marks: 50, note: 'Differentiation — rates of change' },
    { year: 2019, paper: 'Paper 1', question: 'Q8', marks: 50, note: 'Integration — area under curve' },
  ]},
  { subject: 'Mathematics', topic: 'Financial Maths', questions: [
    { year: 2022, paper: 'Paper 1', question: 'Q6(a)', marks: 15, note: 'Compound interest' },
    { year: 2020, paper: 'Paper 1', question: 'Q5', marks: 25, note: 'Present value & amortisation' },
    { year: 2019, paper: 'Paper 1', question: 'Q5', marks: 25 },
  ]},
  { subject: 'Mathematics', topic: 'Induction', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q6', marks: 25 },
    { year: 2022, paper: 'Paper 1', question: 'Q6(b)', marks: 10 },
    { year: 2021, paper: 'Paper 1', question: 'Q4', marks: 25 },
    { year: 2020, paper: 'Paper 1', question: 'Q6', marks: 25 },
  ]},
  { subject: 'Mathematics', topic: 'Coordinate Geometry', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Q1', marks: 25, note: 'Line' },
    { year: 2023, paper: 'Paper 2', question: 'Q3', marks: 25, note: 'Circle' },
    { year: 2022, paper: 'Paper 2', question: 'Q1', marks: 25, note: 'Line & slope' },
    { year: 2022, paper: 'Paper 2', question: 'Q2', marks: 25, note: 'Circle' },
    { year: 2021, paper: 'Paper 2', question: 'Q1', marks: 25, note: 'Line' },
    { year: 2021, paper: 'Paper 2', question: 'Q3', marks: 25, note: 'Circle — tangent' },
    { year: 2020, paper: 'Paper 2', question: 'Q1', marks: 25 },
    { year: 2019, paper: 'Paper 2', question: 'Q1', marks: 25 },
    { year: 2019, paper: 'Paper 2', question: 'Q2', marks: 25, note: 'Circle' },
  ]},
  { subject: 'Mathematics', topic: 'Trigonometry', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Q2', marks: 25, note: 'Trig identities' },
    { year: 2023, paper: 'Paper 2', question: 'Q7', marks: 50, note: 'Section B — 3D trig problem' },
    { year: 2022, paper: 'Paper 2', question: 'Q3', marks: 25, note: 'Trig equations' },
    { year: 2022, paper: 'Paper 2', question: 'Q7', marks: 50, note: 'Section B — sine/cosine rule' },
    { year: 2021, paper: 'Paper 2', question: 'Q2', marks: 25, note: 'Identities & proofs' },
    { year: 2020, paper: 'Paper 2', question: 'Q2', marks: 25 },
    { year: 2019, paper: 'Paper 2', question: 'Q3', marks: 25, note: 'Trig identities' },
  ]},
  { subject: 'Mathematics', topic: 'Probability & Statistics', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Q4', marks: 25, note: 'Probability — counting' },
    { year: 2023, paper: 'Paper 2', question: 'Q8', marks: 50, note: 'Section B — hypothesis testing' },
    { year: 2022, paper: 'Paper 2', question: 'Q4', marks: 25, note: 'Bernoulli trials' },
    { year: 2022, paper: 'Paper 2', question: 'Q8', marks: 50, note: 'Section B — normal distribution' },
    { year: 2021, paper: 'Paper 2', question: 'Q4', marks: 25, note: 'Probability' },
    { year: 2021, paper: 'Paper 2', question: 'Q8', marks: 50, note: 'Statistics — confidence intervals' },
    { year: 2020, paper: 'Paper 2', question: 'Q4', marks: 25 },
    { year: 2020, paper: 'Paper 2', question: 'Q8', marks: 50, note: 'Hypothesis testing' },
    { year: 2019, paper: 'Paper 2', question: 'Q4', marks: 25, note: 'Probability' },
    { year: 2019, paper: 'Paper 2', question: 'Q8', marks: 50, note: 'Normal distribution' },
  ]},
  { subject: 'Mathematics', topic: 'Geometry (Proofs)', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Q5', marks: 25, note: 'Theorem application' },
    { year: 2022, paper: 'Paper 2', question: 'Q5', marks: 25 },
    { year: 2021, paper: 'Paper 2', question: 'Q5', marks: 25, note: 'Proof + construction' },
    { year: 2019, paper: 'Paper 2', question: 'Q5', marks: 25 },
  ]},
  { subject: 'Mathematics', topic: 'Length, Area & Volume', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Q6', marks: 25, note: 'Combined with coordinate geometry' },
    { year: 2021, paper: 'Paper 2', question: 'Q6', marks: 25 },
    { year: 2020, paper: 'Paper 2', question: 'Q6', marks: 25 },
  ]},

  // ═══════════════════════════════════════════════════════════════════════════
  // ENGLISH (Higher Level)
  // ═══════════════════════════════════════════════════════════════════════════

  { subject: 'English', topic: 'Comprehension (Question A)', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q A', marks: 50, note: 'Two texts — 3 sub-questions each' },
    { year: 2022, paper: 'Paper 1', question: 'Q A', marks: 50 },
    { year: 2021, paper: 'Paper 1', question: 'Q A', marks: 50 },
    { year: 2020, paper: 'Paper 1', question: 'Q A', marks: 50 },
    { year: 2019, paper: 'Paper 1', question: 'Q A', marks: 50 },
  ]},
  { subject: 'English', topic: 'Functional Writing (Question B)', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Q B', marks: 50, note: 'Speech, article, or letter' },
    { year: 2022, paper: 'Paper 1', question: 'Q B', marks: 50, note: 'Blog post' },
    { year: 2021, paper: 'Paper 1', question: 'Q B', marks: 50, note: 'Speech' },
    { year: 2020, paper: 'Paper 1', question: 'Q B', marks: 50 },
    { year: 2019, paper: 'Paper 1', question: 'Q B', marks: 50, note: 'Letter to the editor' },
  ]},
  { subject: 'English', topic: 'Composing (Essay)', questions: [
    { year: 2023, paper: 'Paper 1', question: 'Section II', marks: 100, note: '7 title choices — personal essay appeared' },
    { year: 2022, paper: 'Paper 1', question: 'Section II', marks: 100, note: '7 titles including personal essay' },
    { year: 2021, paper: 'Paper 1', question: 'Section II', marks: 100, note: '7 titles' },
    { year: 2020, paper: 'Paper 1', question: 'Section II', marks: 100, note: '7 titles' },
    { year: 2019, paper: 'Paper 1', question: 'Section II', marks: 100, note: '7 titles — descriptive essay popular' },
  ]},
  { subject: 'English', topic: 'Single Text (Shakespeare)', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Section I', marks: 60, note: 'Mandatory since 2023 curriculum change' },
    { year: 2022, paper: 'Paper 2', question: 'Section I', marks: 60, note: 'Single text — choice of studied text' },
    { year: 2021, paper: 'Paper 2', question: 'Section I', marks: 60 },
    { year: 2020, paper: 'Paper 2', question: 'Section I', marks: 60 },
    { year: 2019, paper: 'Paper 2', question: 'Section I', marks: 60 },
  ]},
  { subject: 'English', topic: 'Comparative Study', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Section II', marks: 70, note: 'One mode — 3 texts compared' },
    { year: 2022, paper: 'Paper 2', question: 'Section II', marks: 70 },
    { year: 2021, paper: 'Paper 2', question: 'Section II', marks: 70 },
    { year: 2020, paper: 'Paper 2', question: 'Section II', marks: 70 },
    { year: 2019, paper: 'Paper 2', question: 'Section II', marks: 70 },
  ]},
  { subject: 'English', topic: 'Unseen Poetry', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Section III (A)', marks: 20 },
    { year: 2022, paper: 'Paper 2', question: 'Section III (A)', marks: 20 },
    { year: 2021, paper: 'Paper 2', question: 'Section III (A)', marks: 20 },
    { year: 2020, paper: 'Paper 2', question: 'Section III (A)', marks: 20 },
    { year: 2019, paper: 'Paper 2', question: 'Section III (A)', marks: 20 },
  ]},
  { subject: 'English', topic: 'Prescribed Poetry', questions: [
    { year: 2023, paper: 'Paper 2', question: 'Section III (B)', marks: 50, note: 'Choice of poets — Yeats, Bishop popular' },
    { year: 2022, paper: 'Paper 2', question: 'Section III (B)', marks: 50 },
    { year: 2021, paper: 'Paper 2', question: 'Section III (B)', marks: 50 },
    { year: 2020, paper: 'Paper 2', question: 'Section III (B)', marks: 50 },
    { year: 2019, paper: 'Paper 2', question: 'Section III (B)', marks: 50 },
  ]},

  // ═══════════════════════════════════════════════════════════════════════════
  // BIOLOGY (Higher Level)
  // ═══════════════════════════════════════════════════════════════════════════

  { subject: 'Biology', topic: 'Cell Biology', questions: [
    { year: 2023, paper: 'Paper', question: 'Q1', marks: 30, note: 'Cell structure & organelles' },
    { year: 2022, paper: 'Paper', question: 'Q1', marks: 30 },
    { year: 2021, paper: 'Paper', question: 'Q1', marks: 30 },
    { year: 2020, paper: 'Paper', question: 'Section A Q1-3', marks: 30 },
    { year: 2019, paper: 'Paper', question: 'Q1', marks: 30 },
  ]},
  { subject: 'Biology', topic: 'Genetics & DNA', questions: [
    { year: 2023, paper: 'Paper', question: 'Q14', marks: 60, note: 'Genetics long question' },
    { year: 2022, paper: 'Paper', question: 'Q14', marks: 60, note: 'DNA replication & protein synthesis' },
    { year: 2021, paper: 'Paper', question: 'Q14', marks: 60 },
    { year: 2020, paper: 'Paper', question: 'Q14', marks: 60, note: 'Genetic crosses' },
    { year: 2019, paper: 'Paper', question: 'Q14', marks: 60 },
  ]},
  { subject: 'Biology', topic: 'Ecology', questions: [
    { year: 2023, paper: 'Paper', question: 'Q15', marks: 60, note: 'Ecosystem study' },
    { year: 2022, paper: 'Paper', question: 'Q15', marks: 60 },
    { year: 2021, paper: 'Paper', question: 'Q15', marks: 60, note: 'Mandatory ecology experiment' },
    { year: 2020, paper: 'Paper', question: 'Q15', marks: 60 },
    { year: 2019, paper: 'Paper', question: 'Q15', marks: 60 },
  ]},
  { subject: 'Biology', topic: 'Human Biology', questions: [
    { year: 2023, paper: 'Paper', question: 'Q12', marks: 60, note: 'Circulatory or respiratory system' },
    { year: 2022, paper: 'Paper', question: 'Q12', marks: 60 },
    { year: 2021, paper: 'Paper', question: 'Q12', marks: 60, note: 'Digestive system' },
    { year: 2020, paper: 'Paper', question: 'Q12', marks: 60 },
    { year: 2019, paper: 'Paper', question: 'Q12', marks: 60, note: 'Nervous system' },
  ]},
  { subject: 'Biology', topic: 'Photosynthesis & Respiration', questions: [
    { year: 2023, paper: 'Paper', question: 'Q11', marks: 60, note: 'Biochemistry of photosynthesis' },
    { year: 2022, paper: 'Paper', question: 'Q11', marks: 60 },
    { year: 2021, paper: 'Paper', question: 'Q11', marks: 60, note: 'Krebs cycle & electron transport' },
    { year: 2020, paper: 'Paper', question: 'Q11', marks: 60 },
    { year: 2019, paper: 'Paper', question: 'Q11', marks: 60 },
  ]},
  { subject: 'Biology', topic: 'Experiments (Mandatory)', questions: [
    { year: 2023, paper: 'Paper', question: 'Section A Q1-3', marks: 30, note: 'Food tests, enzyme activity, osmosis' },
    { year: 2022, paper: 'Paper', question: 'Section A Q1-3', marks: 30 },
    { year: 2021, paper: 'Paper', question: 'Section A Q1-3', marks: 30 },
    { year: 2020, paper: 'Paper', question: 'Section A Q1-3', marks: 30 },
    { year: 2019, paper: 'Paper', question: 'Section A Q1-3', marks: 30 },
  ]},
];

// ─── Lookup ──────────────────────────────────────────────────────────────────

/** Get past paper questions for a specific subject + topic */
export function getPaperTrail(subject: string, topic: string): PastPaperQuestion[] {
  const entry = PAST_PAPER_DATA.find(
    d => d.subject === subject && d.topic === topic
  );
  return entry?.questions ?? [];
}

/** Get all subjects that have past paper data available */
export function getSubjectsWithPaperData(): string[] {
  const subjects = new Set(PAST_PAPER_DATA.map(d => d.subject));
  return [...subjects];
}

/** Check if a subject has any past paper data */
export function hasPaperData(subject: string): boolean {
  return PAST_PAPER_DATA.some(d => d.subject === subject);
}
