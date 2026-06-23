/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Grammar of Grit — verified reference set ────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/grammar-of-grit.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 abramson1978 · 2 hofmann2012 · 3 neff2003
export const GRAMMAR_OF_GRIT_REFERENCE_LIST: Reference[] = [
  REF.abramson1978,
  REF.hofmann2012,
  REF.neff2003,
];
