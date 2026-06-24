/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── The Marking Scheme Decoder — verified source set ─────────────────────────
//
// A Group B exam/strategy module grounded almost entirely in documented SEC
// marking conventions (positive marking, attempt/method/answer marks, "or
// equivalent", "any N points", graduated partial credit, per-label diagram
// marks). The CAO points grid grounds the points-conversion claims in §5.
// See compliance/evidence/marking-scheme-decoder.md.
// Ordered by first appearance — defines the inline <Cite/> numbering.
//   1 secMarkingSchemes · 2 caoPoints
export const MARKING_SCHEME_DECODER_REFERENCE_LIST: Reference[] = [
  REF.secMarkingSchemes,
  REF.caoPoints,
];
