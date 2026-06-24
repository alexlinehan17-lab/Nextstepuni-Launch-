/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Answer Engineering — verified source set ─────────────────────────────────
//
// A Group B exam/strategy module. The answer-structure frameworks (PEEL, S³S,
// the marks-shape decoder, the 60% rescue) are pedagogical scaffolds and carry
// no citation; the marking-convention claims they hang on (method/attempt/answer
// marks, mark-allocation signalling answer length, per-label diagram marks,
// developed vs one-word answers) are grounded in SEC sources.
// See compliance/evidence/answer-engineering.md.
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 secMarkingSchemes · 2 secBusiness2015
export const ANSWER_ENGINEERING_REFERENCE_LIST: Reference[] = [
  REF.secMarkingSchemes,
  REF.secBusiness2015,
];
