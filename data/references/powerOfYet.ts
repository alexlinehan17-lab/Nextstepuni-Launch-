/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Power of "Yet" — verified reference set ─────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/power-of-yet.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 moser2011 · 2 gollwitzer1999
export const POWER_OF_YET_REFERENCE_LIST: Reference[] = [
  REF.moser2011,
  REF.gollwitzer1999,
];
