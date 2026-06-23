/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Cognitive Endurance — verified reference set ────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/cognitive-endurance.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 raichle2002 · 2 mcewen1998 · 3 walker2009 · 4 chambers2009
//   5 arnsten2009 · 6 balban2023
export const COGNITIVE_ENDURANCE_REFERENCE_LIST: Reference[] = [
  REF.raichle2002,
  REF.mcewen1998,
  REF.walker2009,
  REF.chambers2009,
  REF.arnsten2009,
  REF.balban2023,
];
