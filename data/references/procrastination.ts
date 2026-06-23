/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Understanding Procrastination — verified reference set ──────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/procrastination.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 siroisPychyl2013 · 2 casey2008 · 3 steel2007 · 4 berglasJones1978 ·
//   5 wohl2010 · 6 gollwitzer1999
export const PROCRASTINATION_REFERENCE_LIST: Reference[] = [
  REF.siroisPychyl2013,
  REF.casey2008,
  REF.steel2007,
  REF.berglasJones1978,
  REF.wohl2010,
  REF.gollwitzer1999,
];
