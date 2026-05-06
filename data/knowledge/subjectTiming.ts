/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Per-subject timing data for the Time-Allocation Calculator.
 * Source: /docs/leaving-cert-knowledge-dossier.md § A3.
 *
 * Note: where marking-scheme totals appear to differ from the dossier,
 * the dossier's figures are kept verbatim — the dossier is the cited
 * authority per the Necessary Knowledge content guarantee.
 */

import { type SubjectTiming } from '../../types/knowledge';

export const SUBJECT_TIMING: SubjectTiming[] = [
  {
    id: 'english-p1',
    subjectLabel: 'English — Paper 1 (Higher)',
    totalMarks: 200,
    totalMinutes: 170,
    breakdown: [
      { section: 'Composition (1 of 7)', marks: 100, minutes: 85 },
      { section: 'Comprehension Question A', marks: 50, minutes: 42 },
      { section: 'Comprehension Question B (different text)', marks: 50, minutes: 42 },
    ],
    source: { section: 'A3', page: 6 },
  },
  {
    id: 'english-p2',
    subjectLabel: 'English — Paper 2 (Higher)',
    totalMarks: 200,
    totalMinutes: 200,
    breakdown: [
      { section: 'Single Text', marks: 60, minutes: 50 },
      { section: 'Comparative Studies', marks: 70, minutes: 70 },
      { section: 'Poetry — prescribed + unseen', marks: 70, minutes: 65 },
    ],
    source: { section: 'A3', page: 6 },
  },
  {
    id: 'maths',
    subjectLabel: 'Maths — both papers (Higher / Ordinary)',
    totalMarks: 300,
    totalMinutes: 150,
    breakdown: [
      { section: 'Section A — Concepts and Skills', marks: 150, minutes: 75 },
      { section: 'Section B — Contexts and Applications', marks: 150, minutes: 75 },
    ],
    source: { section: 'A3', page: 6 },
  },
  {
    id: 'geography',
    subjectLabel: 'Geography (Higher)',
    totalMarks: 400,
    totalMinutes: 170,
    breakdown: [
      { section: 'Short questions (10 of 12 × 8m)', marks: 80, minutes: 25 },
      { section: 'Section 2 — Patterns and Processes', marks: 80, minutes: 35 },
      { section: 'Section 3 — Regional Geography', marks: 80, minutes: 35 },
      { section: 'Section 4 — Elective', marks: 80, minutes: 35 },
      { section: 'Section 5 — Option (HL only)', marks: 80, minutes: 40 },
    ],
    source: { section: 'A3', page: 6 },
  },
  {
    id: 'business',
    subjectLabel: 'Business (Higher)',
    totalMarks: 400,
    totalMinutes: 180,
    breakdown: [
      { section: 'Section 1 — Short Response (8 questions)', marks: 80, minutes: 36 },
      { section: 'Section 2 — Applied Business Question (ABQ)', marks: 80, minutes: 36 },
      { section: 'Section 3 — Long questions (4 × 60m)', marks: 240, minutes: 108 },
    ],
    source: { section: 'A3', page: 6 },
  },
  {
    id: 'accounting',
    subjectLabel: 'Accounting (Higher)',
    totalMarks: 400,
    totalMinutes: 180,
    breakdown: [
      { section: 'Section 1 — Financial accounting (1 of 3)', marks: 120, minutes: 54 },
      { section: 'Section 2 — Financial accounting (2 of 4)', marks: 200, minutes: 90 },
      { section: 'Section 3 — Management accounting (1 of 2)', marks: 80, minutes: 36 },
    ],
    source: { section: 'A3', page: 6, cite: '0.45 mins/mark — 27 seconds. The fastest-paced LC paper.' },
  },
  {
    id: 'biology',
    subjectLabel: 'Biology (Higher)',
    totalMarks: 400,
    totalMinutes: 180,
    breakdown: [
      { section: 'Section A — short questions', marks: 100, minutes: 45 },
      { section: 'Section B — experiments (2 of 4)', marks: 60, minutes: 27 },
      { section: 'Section C — long questions (4 of 6)', marks: 240, minutes: 108 },
    ],
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'chemistry',
    subjectLabel: 'Chemistry (Higher)',
    totalMarks: 400,
    totalMinutes: 180,
    breakdown: [
      { section: 'Section A — experiments (2 of 3)', marks: 100, minutes: 45 },
      { section: 'Section B — long questions (5 of 8)', marks: 300, minutes: 135 },
    ],
    source: { section: 'B4', page: 10 },
  },
  {
    id: 'physics',
    subjectLabel: 'Physics (Higher)',
    totalMarks: 400,
    totalMinutes: 180,
    breakdown: [
      { section: 'Section A — mandatory experiments (3 of 4)', marks: 120, minutes: 54 },
      { section: 'Section B — long questions (5 of 8)', marks: 280, minutes: 126 },
    ],
    source: { section: 'B4', page: 11 },
  },
  {
    id: 'history',
    subjectLabel: 'History (Higher)',
    totalMarks: 500,
    totalMinutes: 170,
    breakdown: [
      { section: 'Documents-Based Question (DBQ)', marks: 100, minutes: 35 },
      { section: 'Long Questions — Ireland (2 essays)', marks: 200, minutes: 70 },
      { section: 'Long Questions — Europe / Wider World (2 essays)', marks: 200, minutes: 65 },
    ],
    source: { section: 'B5', page: 11 },
  },
  {
    id: 'irish-p2',
    subjectLabel: 'Irish — Paper 2 (Higher)',
    totalMarks: 220,
    totalMinutes: 165,
    breakdown: [
      { section: 'Léamhthuiscint — comprehension (2 × 50m)', marks: 100, minutes: 75 },
      { section: 'Prós + Filíocht (literature)', marks: 120, minutes: 90 },
    ],
    source: { section: 'B3', page: 9 },
  },
  {
    id: 'mfl',
    subjectLabel: 'Modern Foreign Languages — written paper',
    totalMarks: 220,
    totalMinutes: 150,
    breakdown: [
      { section: 'Listening (separate audio)', marks: 60, minutes: 40 },
      { section: 'Reading comprehension', marks: 80, minutes: 55 },
      { section: 'Written production (opinion + functional)', marks: 80, minutes: 55 },
    ],
    source: { section: 'B8', page: 13 },
  },
];
