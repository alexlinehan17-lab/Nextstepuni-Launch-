/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { type Reference } from './types';
import { REF } from './library';

// ─── Mastering English (subject module) — verified source set ─────────────────
//
// A Group B subject module grounded in official SEC sources: the in-repo 2025
// English HL marking scheme (PCLM criteria + 30/30/30/10 weightings, primacy of
// Clarity of Purpose, paper structure and section mark allocations, the
// unseen-poetry marking stance) and the in-repo 2013 English Chief Examiner's
// Report (loss of task focus, formulaic comparative answers, brief undeveloped
// compositions, section averages). The 2024 HL scheme was used as a second-year
// stability check (examiner-reports/english/2024-verification.md).
// See compliance/evidence/subject-english.md.
// Ordered by first appearance — defines the inline {{cite:N}} numbering.
//   1 secEnglishMarkingScheme2025 · 2 secEnglish2013
export const SUBJECT_ENGLISH_REFERENCE_LIST: Reference[] = [
  REF.secEnglishMarkingScheme2025,
  REF.secEnglish2013,
];
