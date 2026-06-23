/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Cognitive Load — verified reference set ─────────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/cognitive-load.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 miller1956 · 2 cowan2001 · 3 sweller1988 · 4 sweller1998
//   5 chandlersweller1992 · 6 kalyuga2003
export const COGNITIVE_LOAD_REFERENCE_LIST: Reference[] = [
  REF.miller1956,
  REF.cowan2001,
  REF.sweller1988,
  REF.sweller1998,
  REF.chandlersweller1992,
  REF.kalyuga2003,
];
