/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — Firebase Storage addressing.
 *
 * The corpus is world-readable (storage.rules) so documents are fetched over
 * the plain Storage REST endpoint — no storage SDK in the bundle.
 *
 * Paths are versionless and stable: papers/{cycle}/{subjectId}/{year}/{kind}/{fileid}.
 * The {kind} segment is load-bearing: the SEC reuses the IDENTICAL fileid for a
 * paper and its marking scheme (~76% of pairs — e.g. LC032ALP000EV.pdf is both
 * the Accounting 2010 HL paper and its scheme), distinguishing them only by
 * archive directory. The upload pipeline (scripts/paper-trail/) mirrors this
 * exact layout.
 */

import { type PaperCycle } from '../../types/paperTrail';

const BUCKET = 'nextstepuni-app.firebasestorage.app';

export const paperStoragePath = (
  cycle: PaperCycle,
  subjectId: string,
  year: number,
  kind: 'paper' | 'scheme',
  fileid: string,
) => `papers/${cycle}/${subjectId}/${year}/${kind}/${fileid}`;

/** Public REST URL for a corpus document (range-request capable, CORS-open). */
export const paperUrl = (path: string) =>
  `https://firebasestorage.googleapis.com/v0/b/${BUCKET}/o/${encodeURIComponent(path)}?alt=media`;

export const prettyBytes = (b: number) => {
  if (!b) return '';
  if (b < 1024 * 1024) return `${Math.max(1, Math.round(b / 1024))} KB`;
  return `${(b / (1024 * 1024)).toFixed(1)} MB`;
};
