/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Implementation Playbook — verified reference set ────────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/implementation-protocol.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 sheeran2002 · 2 gollwitzer1999 · 3 gollwitzerSheeran2006 ·
//   4 milkman2014 · 5 arielyWertenbroch2002
export const IMPLEMENTATION_PROTOCOL_REFERENCE_LIST: Reference[] = [
  REF.sheeran2002,
  REF.gollwitzer1999,
  REF.gollwitzerSheeran2006,
  REF.milkman2014,
  REF.arielyWertenbroch2002,
];
