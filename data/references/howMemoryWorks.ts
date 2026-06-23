/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── How Your Memory Works — verified reference set ──────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/how-memory-works.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 atkinson1968 · 2 miller1956 · 3 cowan2001 · 4 peterson1959 · 5 squire2004
//   6 craik1972 · 7 diekelmann2010 · 8 dunlosky2013 · 9 lupien2009
export const HOW_MEMORY_WORKS_REFERENCE_LIST: Reference[] = [
  REF.atkinson1968,
  REF.miller1956,
  REF.cowan2001,
  REF.peterson1959,
  REF.squire2004,
  REF.craik1972,
  REF.diekelmann2010,
  REF.dunlosky2013,
  REF.lupien2009,
];
