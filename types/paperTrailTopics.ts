/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — per-question topic tags (Tier 2). Each anchored question is
 * tagged with a curriculum subtopic id (from curriculum.ts), verified against
 * the actual question text with the same verify-don't-guess discipline as the
 * answer maps. Tags power the frequency chips ("Calculus — appeared in 4 of 5
 * tagged years") and cross-year jumping ("drill every Calculus question").
 *
 * Tags are committed in-repo (small) rather than fetched, so the frequency
 * aggregation is available client-side with no extra round-trip. Positions come
 * from the answer-map anchors (question `n` is the join key).
 */

import { type PaperLang, type PaperLevel } from './paperTrail';

export interface QuestionTopicTag {
  /** Question number — matches PaperAnswerQuestion.n on the answer map. */
  n: string;
  /** Primary curriculum subtopic id (from curriculum.ts). */
  primary: string;
  /** Optional second subtopic when the question genuinely spans two. */
  secondary?: string;
}

export interface PaperTopicTags {
  subjectId: string;
  level: PaperLevel;
  lang: PaperLang;
  year: number;
  /** The paper's fileid (join key with the index + Storage). */
  fileid: string;
  /** Normalised paper slot — 'p1' | 'p2' | 'single' — so P1 and P2 topic pools
   *  don't blur together in the frequency counts. */
  paperKey: string;
  q: QuestionTopicTag[];
}
