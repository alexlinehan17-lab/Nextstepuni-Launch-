/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Note-Taking Paradox — verified reference set ────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/note-taking-paradox.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 mueller2014 · 2 kiewra1989 · 3 craik1972 · 4 rk2006 · 5 nesbit2006
export const NOTE_TAKING_PARADOX_REFERENCE_LIST: Reference[] = [
  REF.mueller2014,
  REF.kiewra1989,
  REF.craik1972,
  REF.rk2006,
  REF.nesbit2006,
];
