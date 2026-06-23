/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// A single peer-reviewed reference backing a module claim. Every reference here
// has had its DOI verified against CrossRef — see compliance/evidence/<module>.md
// for the per-claim verification record. NEVER add a reference whose DOI has not
// been confirmed to resolve to a real paper that supports the specific claim.
export interface Reference {
  /** Short stable key, e.g. 'rk2006'. */
  id: string;
  /** Author string in citation form, e.g. "Roediger, H. L., & Karpicke, J. D." */
  authors: string;
  year: number;
  /** Article title (sentence case). */
  title: string;
  /** Journal / source (rendered italic). */
  source: string;
  /** Verified DOI (no URL prefix). */
  doi: string;
}
