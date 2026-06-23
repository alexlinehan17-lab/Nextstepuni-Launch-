/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Myelin Manual — verified reference set ──────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/myelin-manual.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 gibson2014 · 2 mckenzie2014 · 3 scholz2009 · 4 ericsson1993 · 5 sb2015
export const MYELIN_MANUAL_REFERENCE_LIST: Reference[] = [
  REF.gibson2014,
  REF.mckenzie2014,
  REF.scholz2009,
  REF.ericsson1993,
  REF.sb2015,
];
