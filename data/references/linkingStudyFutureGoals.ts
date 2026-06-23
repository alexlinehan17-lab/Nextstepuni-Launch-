/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Linking Study to Future Goals — verified reference set ──────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/linking-study-future-goals.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 wigfield2000 · 2 husman1999 · 3 hulleman2009 · 4 cohen2006 ·
//   5 kappes2011 · 6 gollwitzer1999 · 7 ryandeci2000 · 8 oyserman2010
export const LINKING_STUDY_FUTURE_GOALS_REFERENCE_LIST: Reference[] = [
  REF.wigfield2000,
  REF.husman1999,
  REF.hulleman2009,
  REF.cohen2006,
  REF.kappes2011,
  REF.gollwitzer1999,
  REF.ryandeci2000,
  REF.oyserman2010,
];
