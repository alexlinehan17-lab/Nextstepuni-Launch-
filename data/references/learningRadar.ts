/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Learning Radar — verified reference set ─────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/learning-radar.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 zell2014 · 2 kruger1999 · 3 nelson1991 · 4 dunlosky2013 · 5 koriat2005
export const LEARNING_RADAR_REFERENCE_LIST: Reference[] = [
  REF.zell2014,
  REF.kruger1999,
  REF.nelson1991,
  REF.dunlosky2013,
  REF.koriat2005,
];
