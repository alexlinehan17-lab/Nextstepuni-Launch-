/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Controlling the Controllables — verified reference set ──────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/agency-architecture.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 weiner1985 · 2 abramson1978 · 3 wilsonLinville1982
export const AGENCY_ARCHITECTURE_REFERENCE_LIST: Reference[] = [
  REF.weiner1985,
  REF.abramson1978,
  REF.wilsonLinville1982,
];
