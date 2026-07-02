/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — Formulae & Tables quick-jump.
 *
 * The SEC "Formulae and Tables" booklet is the only reference candidates may use
 * in Maths and the sciences. This feature surfaces a quick-jump list inside the
 * viewer for the subjects that use it, so a student can flick to the right table
 * without leaving the paper.
 *
 * GATED, BY DESIGN. The tool only appears once BOTH are true:
 *   1. FORMULAE_BOOKLET_LIVE === true, and
 *   2. the booklet PDF has been uploaded to Storage at FORMULAE_BOOKLET_PATH.
 * Until the founder uploads the (public-domain) SEC booklet and flips the flag,
 * nothing renders — no dead button, no 404. See scripts/paper-trail/FORMULAE.md.
 *
 * Section → PDF-page numbers are NOT hard-coded here on purpose: printed page
 * numbers and PDF page numbers differ by the booklet's front matter, and a wrong
 * jump reads as a bug. Pages come from a founder-generated sidecar
 * (FORMULAE_INDEX_PATH) built from the actual uploaded PDF; a section with no
 * page entry simply opens the booklet at the front. Labels + subject mapping
 * below are stable and safe to ship.
 */

/** Master switch — stays false until the booklet is live in Storage. */
export const FORMULAE_BOOKLET_LIVE = false;

/** Storage object paths (world-readable corpus bucket). */
export const FORMULAE_BOOKLET_PATH = 'formulae/formulae-and-tables.pdf';
export const FORMULAE_INDEX_PATH = 'formulae/formulae-and-tables.index.json';

/** Paper-Trail subjectIds whose candidates use the booklet in the exam. */
export const FORMULAE_SUBJECTS: Record<string, true> = {
  mathematics: true,
  'applied-mathematics': true,
  physics: true,
  chemistry: true,
  'physics-and-chemistry': true,
  biology: true,
  engineering: true,
  'construction-studies': true,
  'agricultural-science': true,
};

export interface FormulaeSection {
  /** Stable id — the key the Storage page-index sidecar is keyed by. */
  id: string;
  label: string;
  /** SubjectIds this section is most relevant to (used to order + group). */
  subjects: string[];
}

/** The booklet's stable table-of-contents entries. Page numbers are resolved at
 *  runtime from the Storage sidecar (see file header) — never from here. */
export const FORMULAE_SECTIONS: FormulaeSection[] = [
  { id: 'algebra', label: 'Algebra', subjects: ['mathematics', 'applied-mathematics', 'engineering'] },
  { id: 'geometry', label: 'Geometry & Co-ordinate Geometry', subjects: ['mathematics', 'applied-mathematics'] },
  { id: 'trigonometry', label: 'Trigonometry', subjects: ['mathematics', 'applied-mathematics'] },
  { id: 'differentiation', label: 'Differential Calculus', subjects: ['mathematics', 'applied-mathematics', 'physics'] },
  { id: 'integration', label: 'Integral Calculus', subjects: ['mathematics', 'applied-mathematics'] },
  { id: 'sequences-series', label: 'Sequences & Series', subjects: ['mathematics'] },
  { id: 'financial-maths', label: 'Financial Maths', subjects: ['mathematics'] },
  { id: 'area-volume', label: 'Area & Volume', subjects: ['mathematics', 'construction-studies', 'engineering'] },
  { id: 'statistics', label: 'Statistics & Probability', subjects: ['mathematics'] },
  { id: 'physical-constants', label: 'Physical Constants', subjects: ['physics', 'physics-and-chemistry', 'applied-mathematics'] },
  { id: 'mechanics', label: 'Mechanics & Motion', subjects: ['physics', 'applied-mathematics'] },
  { id: 'electricity', label: 'Electricity & Magnetism', subjects: ['physics', 'physics-and-chemistry'] },
  { id: 'waves-optics', label: 'Waves, Light & Sound', subjects: ['physics'] },
  { id: 'periodic-table', label: 'Periodic Table', subjects: ['chemistry', 'physics-and-chemistry', 'biology', 'agricultural-science'] },
  { id: 'reduction-potentials', label: 'Standard Reduction Potentials', subjects: ['chemistry'] },
  { id: 'thermodynamic-data', label: 'Thermodynamic Data', subjects: ['chemistry', 'physics-and-chemistry'] },
];

/** Storage sidecar shape: sectionId → 1-based PDF page in the uploaded booklet. */
export type FormulaePageIndex = Record<string, number>;

/** Descriptor handed to the viewer only when the feature is live for a subject. */
export interface FormulaeHandle {
  bookletUrl: string;
  indexUrl: string;
  sections: FormulaeSection[];
}
