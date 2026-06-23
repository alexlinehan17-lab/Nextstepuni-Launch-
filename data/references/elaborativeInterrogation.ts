/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Elaborative Interrogation — verified reference set ──────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/elaborative-interrogation.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 stein1979 · 2 pressley1987 · 3 dunlosky2013
export const ELABORATIVE_INTERROGATION_REFERENCE_LIST: Reference[] = [
  REF.stein1979,
  REF.pressley1987,
  REF.dunlosky2013,
];
