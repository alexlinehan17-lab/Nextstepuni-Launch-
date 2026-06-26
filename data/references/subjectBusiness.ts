/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Mastering Business (subject module) — verified source set ────────────────
//
// A Group B subject module grounded in official SEC sources: the in-repo 2025
// Business HL marking scheme (paper structure, weightings, ABQ Name/Explain/Link
// requirement) and the in-repo 2015 Business Chief Examiner's Report (developed
// vs one-word answers, action words, answering the question asked).
// See compliance/evidence/subject-business.md.
// Ordered by first appearance — defines the inline {{cite:N}} numbering.
//   1 secBusinessMarkingScheme2025 · 2 secBusiness2015
export const SUBJECT_BUSINESS_REFERENCE_LIST: Reference[] = [
  REF.secBusinessMarkingScheme2025,
  REF.secBusiness2015,
];
