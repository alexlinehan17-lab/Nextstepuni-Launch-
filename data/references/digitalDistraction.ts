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
//   1 casey2008 · 2 mark2008 · 3 ward2017 · 4 gollwitzer1999
export const DIGITAL_DISTRACTION_REFERENCE_LIST: Reference[] = [
  REF.casey2008,
  REF.mark2008,
  REF.ward2017,
  REF.gollwitzer1999,
];
