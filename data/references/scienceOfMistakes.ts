/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Science of Making Mistakes — verified reference set ─────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/science-of-mistakes.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 gehring1993 · 2 moser2011 · 3 arnsten2009
export const SCIENCE_OF_MISTAKES_REFERENCE_LIST: Reference[] = [
  REF.gehring1993,
  REF.moser2011,
  REF.arnsten2009,
];
