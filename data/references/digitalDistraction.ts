/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Creating Barriers for Digital Distractions — verified reference set ─────
//
// DOIs confirmed via CrossRef (see compliance/evidence/digital-distraction.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 casey2008 · 2 mark2005 · 3 ward2017 · 4 gollwitzer1999
// Note: the ~23-minute resumption figure is from Mark, Gonzalez & Harris (2005)
// "No task left behind?" (resumption of work), NOT Mark, Gudith & Klocke (2008)
// (which measures the speed/stress trade-off) — corrected after the verification pass.
export const DIGITAL_DISTRACTION_REFERENCE_LIST: Reference[] = [
  REF.casey2008,
  REF.mark2005,
  REF.ward2017,
  REF.gollwitzer1999,
];
