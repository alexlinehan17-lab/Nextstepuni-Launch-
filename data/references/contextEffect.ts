/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Context Effect — verified reference set ─────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/context-effect.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 godden1975 · 2 smith1978 · 3 mehta2012 · 4 smithvela2001
export const CONTEXT_EFFECT_REFERENCE_LIST: Reference[] = [
  REF.godden1975,
  REF.smith1978,
  REF.mehta2012,
  REF.smithvela2001,
];
