/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Marking Lens — per-question "how the marks are given", grounded STRICTLY in
 * the SEC marking scheme for that exact paper (filed in /examiner-reports/).
 *
 * Content honesty rules (same register as the Examiner's Chair):
 *  - `notation` is the scheme's marking notation VERBATIM (e.g. "3 @ 5m (2+3)");
 *    `decoded` only restates what that notation allocates — it never adds
 *    advice, model answers or claims the scheme doesn't make.
 *  - Every entry cites the exact scheme document + question (`cite`).
 *  - `pitfall` is optional and only attached where a Chief Examiner's Report
 *    documents that behaviour for this question TYPE — with its own cite.
 *  - Marks integrity is machine-checked: the parts of every entry must sum to
 *    `totalMarks` (test/markingLens.test.ts). An entry that can't be made to
 *    sum honestly is not shipped.
 */

import { type PaperLang, type PaperLevel } from '../../types/paperTrail';

/** One row of the marks ladder — a question part as the scheme divides it. */
export interface LensPart {
  /** Part label as printed on the paper, e.g. "(A)(i)". Empty for one-part Qs. */
  part: string;
  /** What the part asks, abbreviated faithfully from the paper/scheme. */
  task: string;
  /** The scheme's marks notation, verbatim (normalised spacing only). */
  notation: string;
  /** What the notation allocates, in student terms — no more, no less. */
  decoded: string;
  /** Total marks this row carries. Rows must sum to `totalMarks`. */
  marks: number;
}

/** A documented examiner-flagged pitfall relevant to this question's type. */
export interface LensPitfall {
  text: string;
  /** e.g. "Chief Examiner's Report 2015 (Business HL), p.17" */
  cite: string;
}

/** The lens for ONE real past-paper question (keyed like a TopicSibling). */
export interface QuestionLens {
  year: number;
  level: PaperLevel;
  lang: PaperLang;
  fileid: string;
  /** Question number — must match the Topic Vault tag/sidecar `n`. */
  n: string;
  totalMarks: number;
  /** One-line marking model, e.g. "Three 20-mark parts, each on a state + develop grid." */
  headline: string;
  parts: LensPart[];
  pitfall?: LensPitfall;
  /** e.g. "SEC Marking Scheme 2024, Business Higher Level, Q1" */
  cite: string;
}

/** All lens entries for one subject. */
export interface SubjectLens {
  subjectId: string;
  entries: QuestionLens[];
}
