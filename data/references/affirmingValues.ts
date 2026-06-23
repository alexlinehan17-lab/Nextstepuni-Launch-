/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Affirming Values — verified reference set ───────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/affirming-values.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 steeleAronson1995 · 2 schmaderJohns2003 · 3 cohen2006 · 4 fredrickson2001 · 5 cohen2009
export const AFFIRMING_VALUES_REFERENCE_LIST: Reference[] = [
  REF.steeleAronson1995,
  REF.schmaderJohns2003,
  REF.cohen2006,
  REF.fredrickson2001,
  REF.cohen2009,
];
