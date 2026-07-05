/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Oral Exam Trainer (Launchpad) — content types. The oral exams are a huge,
 * high-weight, underserved part of the Leaving Cert; this models one language's
 * oral so the trainer can render structure, preparation guidance and speaking
 * prompts. Every factual claim in the data files must trace to an official SEC /
 * NCCA source (verify-don't-guess) — recorded in the `sources` list.
 */

export interface OralPrompt {
  /** English prompt describing what to say/practise. */
  en: string;
  /** Optional Irish scaffold — only ever included when verified. */
  ga?: string;
}

export interface OralComponent {
  id: string;
  /** Component name in the target language. */
  nameGa: string;
  /** English gloss. */
  nameEn: string;
  /** Verified weighting (marks and/or %). */
  weight: string;
  /** One-line "what this part of the exam is". */
  whatItIs: string;
  /** Concrete, official-guidance-grounded preparation tips. */
  prepTips: string[];
  /** Speaking prompts to practise against (record + self-review). */
  prompts: OralPrompt[];
}

export interface OralExam {
  /** Display language, e.g. "Irish". */
  language: string;
  /** Total weighting of the oral within the subject. */
  totalWeight: string;
  /** Short intro shown at the top of the tool. */
  intro: string;
  /** Note on Higher vs Ordinary differences, if any. */
  levelNote?: string;
  components: OralComponent[];
  /** Official sources every fact above is grounded in. */
  sources: { label: string; url: string }[];
}
