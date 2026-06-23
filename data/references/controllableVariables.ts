/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Using Controllable Variables to Grow — verified reference set ───────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/controllable-variables.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 casey2008 · 2 yoo2007 · 3 diekelmann2010 · 4 vandongen2003 ·
//   5 dawson1997 · 6 raichle2002 · 7 cotman2007 · 8 spiegel2004
export const CONTROLLABLE_VARIABLES_REFERENCE_LIST: Reference[] = [
  REF.casey2008,
  REF.yoo2007,
  REF.diekelmann2010,
  REF.vandongen2003,
  REF.dawson1997,
  REF.raichle2002,
  REF.cotman2007,
  REF.spiegel2004,
];
