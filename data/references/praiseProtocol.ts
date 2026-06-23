/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Power of Praise — verified reference set ────────────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/praise-protocol.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 mueller1998 · 2 moser2011 · 3 gunderson2013 · 4 gunderson2018
// Note: Sisk 2018 (the balancing meta-analysis) is discussed in the dossier as
// reviewer context; it is not cited inline because the module makes the
// study-specific praise/error-signal claims, not the broad "mindset
// intervention raises grades" claim that meta-analysis qualifies.
export const PRAISE_PROTOCOL_REFERENCE_LIST: Reference[] = [
  REF.mueller1998,
  REF.moser2011,
  REF.gunderson2013,
  REF.gunderson2018,
];
