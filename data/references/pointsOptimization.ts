/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The 625 Blueprint (Points Optimization) — verified source set ────────────
//
// A Group B exam/strategy module grounded in official Irish State exam &
// admissions documents, not peer-reviewed psychology journals. The CAO points
// grid and the SEC marking conventions are canonical published facts. The
// per-subject H1-rate figures derive from SEC annual examination statistics;
// those exact figures could not be re-verified this session (examinations.ie
// 403) and are surfaced as approximate / indicative — see the data-accuracy
// caveat in compliance/evidence/points-optimization.md.
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 caoPoints · 2 secExamStatistics · 3 secMarkingSchemes
export const POINTS_OPTIMIZATION_REFERENCE_LIST: Reference[] = [
  REF.caoPoints,
  REF.secExamStatistics,
  REF.secMarkingSchemes,
];
