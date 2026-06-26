/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Reframing Catastrophic Thoughts — verified reference set ────────────────
//
// DOIs confirmed via CrossRef (see compliance/evidence/catastrophic-thinking.md).
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 kuhlmann2005 · 2 hofmann2012 · 3 hayes2006
// Note: §1's acute-stress retrieval claim is cited to kuhlmann2005 (acute
// psychosocial stress impairs memory retrieval in healthy adults). It previously
// cited lupien2009, which is about CHRONIC lifespan stress, not the acute
// retrieval block — corrected after the verification pass.
export const CATASTROPHIC_THINKING_REFERENCE_LIST: Reference[] = [
  REF.kuhlmann2005,
  REF.hofmann2012,
  REF.hayes2006,
];
