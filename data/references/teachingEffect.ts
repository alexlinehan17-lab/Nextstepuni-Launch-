/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Teaching Effect — verified reference set ────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/teaching-effect.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 nestojko2014 · 2 chi1989 · 3 dunlosky2013
export const TEACHING_EFFECT_REFERENCE_LIST: Reference[] = [
  REF.nestojko2014,
  REF.chi1989,
  REF.dunlosky2013,
];
