/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Self Efficacy — verified reference set ──────────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/self-efficacy.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 bandura1977 · 2 schunk1987 · 3 gollwitzer1999
export const SELF_EFFICACY_REFERENCE_LIST: Reference[] = [
  REF.bandura1977,
  REF.schunk1987,
  REF.gollwitzer1999,
];
