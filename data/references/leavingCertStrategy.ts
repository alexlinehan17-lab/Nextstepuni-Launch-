/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Points Playbook (Leaving Cert Strategy) — verified source set ───────
//
// Group B exam module: grounded in official Irish State exam / admissions
// documents, not psychology journals (see compliance/evidence/leaving-cert-strategy.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 caoPoints · 2 secMarkingSchemes · 3 secBusiness2015
export const LEAVING_CERT_STRATEGY_REFERENCE_LIST: Reference[] = [
  REF.caoPoints,
  REF.secMarkingSchemes,
  REF.secBusiness2015,
];
