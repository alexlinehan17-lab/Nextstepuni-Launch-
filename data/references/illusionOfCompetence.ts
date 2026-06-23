/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Overcoming Illusions of Competence — verified reference set ─────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/illusion-of-competence.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 koriat2005 · 2 dunlosky2013 · 3 murre2015 · 4 sb2015 · 5 rk2006
//   6 cepeda2006 · 7 rohrer2015 · 8 butler2010 · 9 agarwal2014
export const ILLUSION_OF_COMPETENCE_REFERENCE_LIST: Reference[] = [
  REF.koriat2005,
  REF.dunlosky2013,
  REF.murre2015,
  REF.sb2015,
  REF.rk2006,
  REF.cepeda2006,
  REF.rohrer2015,
  REF.butler2010,
  REF.agarwal2014,
];
