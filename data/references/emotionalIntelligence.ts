/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Building Emotional Intelligence — verified reference set ────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/emotional-intelligence.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 lupien2009 · 2 saloveyMayer1990 · 3 damasio1996 · 4 brooks2014 ·
//   5 hofmann2012 · 6 balban2023 · 7 diekelmann2010
export const EMOTIONAL_INTELLIGENCE_REFERENCE_LIST: Reference[] = [
  REF.lupien2009,
  REF.saloveyMayer1990,
  REF.damasio1996,
  REF.brooks2014,
  REF.hofmann2012,
  REF.balban2023,
  REF.diekelmann2010,
];
