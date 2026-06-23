/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Growth Playbook — verified reference set ────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/growth-mindset.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 dweckleggett1988 · 2 draganski2004 · 3 ericsson1993 · 4 hattie2007
export const GROWTH_MINDSET_REFERENCE_LIST: Reference[] = [
  REF.dweckleggett1988,
  REF.draganski2004,
  REF.ericsson1993,
  REF.hattie2007,
];
