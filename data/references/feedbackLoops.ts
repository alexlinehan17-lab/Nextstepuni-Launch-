/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Using Feedback Loops — verified reference set ───────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/feedback-loops.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 ericsson1993 · 2 hattie2007 · 3 metcalfe2017 · 4 sweller1988 · 5 chi1989
export const FEEDBACK_LOOPS_REFERENCE_LIST: Reference[] = [
  REF.ericsson1993,
  REF.hattie2007,
  REF.metcalfe2017,
  REF.sweller1988,
  REF.chi1989,
];
