/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * How far the Irish archive review has reached, pinned once. Every reviewed paper (2026-11-04 batch 2: one commit
 * per paper) lowers the papers still pending a full review and adds the Atlas entries its per-question and
 * per-title cards give; the per-year tests import these instead of each pinning its own copy.
 */
/** Papers in scripts/markbank/authored/irish-archive-inventory.json still pending a full review. */
export const PAPERS_PENDING_FULL_REVIEW = 35;
/** Irish Topic Atlas entries (data/examTopics/irish-local-crosswalk.json summary). */
export const IRISH_ATLAS = { questions: 3309, retainedLocalQuestions: 2623, newlyAddedPhysicalMappings: 3023 } as const;
/** Irish entries in HOSTED_ANSWER_OVERRIDES (components/PaperTrail/vaultResolve.ts): reviewed papers' hosted answer maps. */
export const IRISH_ANSWER_OVERRIDES = 56;
/** Cards the archive inventory indexes (Higher, Ordinary and Foundation). */
export const IRISH_INDEXED_CARDS = 2534;
