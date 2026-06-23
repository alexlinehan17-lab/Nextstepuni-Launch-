/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Reframing Progress — verified reference set ─────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/reframing-progress.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 koriat2005 · 2 ericsson1993 · 3 dweckleggett1988
export const REFRAMING_PROGRESS_REFERENCE_LIST: Reference[] = [
  REF.koriat2005,
  REF.ericsson1993,
  REF.dweckleggett1988,
];
