/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Driver's Manual (Agency) — verified reference set ───────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/agency-protocol.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 markus1986 · 2 husman1999 · 3 ryandeci2000 · 4 reeve2013 · 5 oyserman2010 · 6 moll1992
export const AGENCY_PROTOCOL_REFERENCE_LIST: Reference[] = [
  REF.markus1986,
  REF.husman1999,
  REF.ryandeci2000,
  REF.reeve2013,
  REF.oyserman2010,
  REF.moll1992,
];
