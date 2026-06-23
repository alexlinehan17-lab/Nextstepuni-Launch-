/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Bimodal Brain (Focused vs Diffuse Mode) — verified reference set ────
//
// DOIs confirmed via CrossRef (see compliance/evidence/bimodal-brain.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 raichle2001 · 2 baird2012 · 3 sio2009 · 4 lyons2012
export const BIMODAL_BRAIN_REFERENCE_LIST: Reference[] = [
  REF.raichle2001,
  REF.baird2012,
  REF.sio2009,
  REF.lyons2012,
];
