/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Coursework Companion — content types. The coursework / project / practical
 * components carry a large share of the marks in many subjects and are
 * underserved by past-paper tools; this models one subject's coursework
 * component(s) so the tool can render what the component is, how the SEC scheme
 * marks it, and where every fact comes from.
 *
 * Content honesty rules (same register as the Oral Trainer / Marking Lens):
 *  - Every marks figure, criterion and grade band is stated ONLY where the filed
 *    SEC marking scheme prints it — extracted from the scheme, never inferred.
 *  - No percentages, deadlines or brief details are stated unless a resolvable
 *    SEC document states them.
 *  - Every component records its `source` (the filed scheme document) and the
 *    in-repo `filed` path where the extraction can be re-verified.
 *  - Marks integrity is machine-checked (test/courseworkCompanion.test.ts):
 *    where a component states both a total and per-criterion marks that the
 *    scheme presents as the full breakdown, they must reconcile; where the
 *    scheme's own breakdown is partial, the component says so in `structure`
 *    rather than inventing the remainder.
 */

/** One assessed criterion of the coursework, as the scheme prints it. */
export interface CourseworkCriterion {
  /** Criterion name as printed, e.g. "Investigation: Analysis/Research". */
  name: string;
  /** Marks the scheme prints for this criterion. */
  marks: number;
  /** What earns the marks — a short faithful paraphrase of the scheme band. */
  whatItRewards: string;
}

/** A printed grade band (where the scheme includes a grading table). */
export interface CourseworkGradeBand {
  grade: number;
  markBand: string;
}

/** One coursework/project/practical component of one subject. */
export interface CourseworkComponent {
  /** Stable id: `${subjectId}|${component-slug}`. */
  id: string;
  subjectId: string;
  subjectLabel: string;
  /** Component name as the scheme names it. */
  name: string;
  /** One neutral sentence: what the component is. */
  whatItIs: string;
  /** Total marks the component is marked out of, as printed — null when the
   *  scheme prints no component total (we never assert an unprinted total,
   *  even when the criteria happen to sum to a round number). */
  totalMarks: number | null;
  /** The assessed criteria with printed marks. May be a partial breakdown —
   *  `criteriaComplete` says whether the scheme presents it as the full total. */
  criteria: CourseworkCriterion[];
  /** True only when the scheme presents `criteria` as the complete breakdown of
   *  `totalMarks` (then the gate asserts the sum). */
  criteriaComplete: boolean;
  /** Grading table, where the scheme prints one. */
  gradeBands?: CourseworkGradeBand[];
  /** Submission structure / timing — only what the scheme states. */
  structure?: string;
  /** SEC attribution string, e.g.
   *  "SEC Marking Scheme 2025, Home Economics — Food Studies Coursework — © State Examinations Commission". */
  source: string;
  /** In-repo filed document the facts were extracted from (re-verification path). */
  filed: string;
  /** Resolvable archive for the cited scheme. */
  sourceUrl: string;
}
