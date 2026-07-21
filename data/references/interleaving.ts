/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Mix It Up (Interleaving) — verified reference set ───────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/interleaving.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 rohrer2007 · 2 rohrer2015 · 3 sb2015 · 4 kornell2008
export const INTERLEAVING_REFERENCE_LIST: Reference[] = [
  REF.rohrer2007,
  REF.rohrer2015,
  REF.sb2015,
  REF.kornell2008,
];
