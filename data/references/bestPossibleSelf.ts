/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Best Possible Self — verified reference set ─────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/best-possible-self.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 kappes2011 · 2 king2001 · 3 oettingenMayer2002 · 4 gollwitzer1999
export const BEST_POSSIBLE_SELF_REFERENCE_LIST: Reference[] = [
  REF.kappes2011,
  REF.king2001,
  REF.oettingenMayer2002,
  REF.gollwitzer1999,
];
