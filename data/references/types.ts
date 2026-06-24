/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

// A single source backing a module claim.
//
// Two kinds of source are supported:
//
//  • 'paper'    — peer-reviewed literature, identified by a DOI verified against
//                 CrossRef (the Group A psychology modules). NEVER add one whose
//                 DOI has not been confirmed to resolve to a real paper that
//                 supports the specific claim.
//  • 'official' — examiner-authored / institutional sources that do not have a
//                 DOI: SEC Chief Examiner's Reports, SEC marking schemes, the CAO
//                 common points scale. Identified by a URL (and, where the source
//                 lives in this repo, mirrored under /examiner-reports/). These
//                 back the Group B exam/subject modules.
//
// Either way, the per-claim verification record lives in
// compliance/evidence/<module>.md (the dossier reviewed for accreditation).
export interface Reference {
  /** Short stable key, e.g. 'rk2006' or 'cao-points'. */
  id: string;
  /** Author / issuing body in citation form, e.g. "State Examinations Commission". */
  authors: string;
  year: number;
  /** Title (sentence case). */
  title: string;
  /** Journal / publication / issuing source (rendered italic). */
  source: string;
  /** 'paper' (default) for peer-reviewed DOI sources; 'official' for SEC/CAO sources. */
  kind?: 'paper' | 'official';
  /** Verified DOI (no URL prefix). Required for 'paper'; omitted for 'official'. */
  doi?: string;
  /** Canonical URL for an 'official' source (e.g. examinations.ie / cao.ie). */
  url?: string;
  /** Optional in-repo mirror path for an 'official' source, e.g. 'examiner-reports/business/2015-chief-examiner.pdf'. */
  repoPath?: string;
}
