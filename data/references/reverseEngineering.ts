/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Reverse Engineering the Exam — verified source set ──────────────────────
//
// Exam module, but its claims are study-planning psychology (see
// compliance/evidence/reverse-engineering.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 buehler1994 · 2 petersbuchel2010 · 3 cepeda2006 · 4 rk2006 · 5 rohrer2007
export const REVERSE_ENGINEERING_REFERENCE_LIST: Reference[] = [
  REF.buehler1994,
  REF.petersbuchel2010,
  REF.cepeda2006,
  REF.rk2006,
  REF.rohrer2007,
];
