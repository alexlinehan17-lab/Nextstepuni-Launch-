/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Science of Hope — verified reference set ────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/hope-protocol.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 snyder1991 · 2 casey2008 · 3 petersbuchel2010 · 4 lupien2009 · 5 draganski2004
export const HOPE_PROTOCOL_REFERENCE_LIST: Reference[] = [
  REF.snyder1991,
  REF.casey2008,
  REF.petersbuchel2010,
  REF.lupien2009,
  REF.draganski2004,
];
