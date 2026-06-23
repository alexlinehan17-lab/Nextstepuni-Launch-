/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Neuroplasticity — verified reference set ────────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/neuroplasticity.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 draganski2004 · 2 casey2008 · 3 scholz2009 · 4 bliss1973
//   5 cepeda2006 · 6 rk2006 · 7 diekelmann2010 · 8 lupien2009
export const NEUROPLASTICITY_REFERENCE_LIST: Reference[] = [
  REF.draganski2004,
  REF.casey2008,
  REF.scholz2009,
  REF.bliss1973,
  REF.cepeda2006,
  REF.rk2006,
  REF.diekelmann2010,
  REF.lupien2009,
];
