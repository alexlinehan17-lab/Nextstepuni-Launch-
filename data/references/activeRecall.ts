/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Mastering Active Recall — verified reference set ────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/active-recall.md).
// Ordered by first appearance — the array order defines the superscript
// numbering used by the inline <Cite n={…}/> markers and the References modal.
//   1 rk2006 · 2 sb2015 · 3 kr2008 · 4 butler2010 · 5 kb2011 · 6 agarwal2014
export const ACTIVE_RECALL_REFERENCE_LIST: Reference[] = [
  REF.rk2006,
  REF.sb2015,
  REF.kr2008,
  REF.butler2010,
  REF.kb2011,
  REF.agarwal2014,
];
