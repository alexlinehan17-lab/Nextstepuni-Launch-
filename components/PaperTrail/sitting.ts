/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — which sitting a paper belongs to.
 *
 * The SEC's deferred sitting (2022 onwards) is a paper of its own, numbered
 * like June's and filed under the same year, so a question from it read
 * "2022 · Higher · Question 3" exactly as June's Question 3 does. Every place
 * that names a question's paper names the deferred sitting with these words,
 * the ones the paper list already uses (PaperDocuments).
 */

/** The SEC files a deferred-sitting paper as "…-deferred.pdf"; nothing else is. */
export const isDeferredFileid = (fileid: string): boolean => /-deferred\.pdf$/i.test(fileid);

/** "Deferred sitting" for a deferred paper; null for June's, which says nothing. */
export const sittingLabel = (fileid: string): string | null =>
  isDeferredFileid(fileid) ? 'Deferred sitting' : null;
