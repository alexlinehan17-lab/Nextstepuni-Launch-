/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How far the Irish archive review has reached, pinned once. Every reviewed paper (2026-11-04 batch 2: one commit
 * per paper) lowers the papers still pending a full review and adds the Atlas entries its per-question and
 * per-title cards give; the per-year tests import these instead of each pinning its own copy.
 */
/** Papers in scripts/markbank/authored/irish-archive-inventory.json still pending a full review. */
export const PAPERS_PENDING_FULL_REVIEW = 56;
/** Irish Topic Atlas entries (data/examTopics/irish-local-crosswalk.json summary). */
export const IRISH_ATLAS = { questions: 2550, retainedLocalQuestions: 1864, newlyAddedPhysicalMappings: 2264 } as const;
