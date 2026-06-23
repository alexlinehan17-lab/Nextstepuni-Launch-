/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Mental Modelling — verified reference set ───────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/mental-modelling.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 linn1985 · 2 shepard1971 · 3 rittlejohnson2001 · 4 uttal2013 · 5 sorby2009
export const MENTAL_MODELLING_REFERENCE_LIST: Reference[] = [
  REF.linn1985,
  REF.shepard1971,
  REF.rittlejohnson2001,
  REF.uttal2013,
  REF.sorby2009,
];
