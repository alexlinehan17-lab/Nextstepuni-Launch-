/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Mastering Mathematics (subject module) — verified source set ─────────────
//
// A Group B subject module. Paper structure and the show-your-work marking
// emphasis are grounded in the in-repo 2015 Maths Chief Examiner's Report; the
// HL Maths bonus in the CAO points grid; and two study-technique claims
// (retrieval practice, interleaving of maths problems) in the peer-reviewed
// learning-science library. See compliance/evidence/subject-mathematics.md.
// Ordered by first appearance — defines the inline {{cite:N}} numbering.
//   1 secMaths2015 · 2 caoPoints · 3 rk2006 · 4 rohrer2007
export const SUBJECT_MATHEMATICS_REFERENCE_LIST: Reference[] = [
  REF.secMaths2015,
  REF.caoPoints,
  REF.rk2006,
  REF.rohrer2007,
];
