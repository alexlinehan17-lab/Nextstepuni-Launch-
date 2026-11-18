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

// Recovered SEC schemes were absent from the Storage harvest. Ship these
// verified PDFs with Hosting so the corrected index never points at a 404.
const HOSTED_DOCUMENTS = new Set([
  'papers/lc/irish/2010/scheme/LC001ALP000EV.pdf',
  'papers/lc/irish/2010/scheme/LC001GLP000EV.pdf',
  'papers/lc/irish/2011/scheme/LC001BLP000EV.pdf',
]);

export const hostedPaperDocumentUrl = (path: string): string | null =>
  HOSTED_DOCUMENTS.has(path) ? `/paper-documents/${path}` : null;

export const paperStoragePath = (
  cycle: PaperCycle,
  subjectId: string,
  year: number,
  kind: 'paper' | 'scheme' | 'answers',
  fileid: string,
) => `papers/${cycle}/${subjectId}/${year}/${kind}/${fileid}`;

/** Storage path for a paper's answer-map sidecar JSON. The object name is the
 *  paper fileid + ".json" so the service-worker rule (answers.*\.json) and the
 *  upload pipeline agree. */
export const paperAnswersPath = (
  cycle: PaperCycle,
  subjectId: string,
  year: number,
  paperFileid: string,
) => `papers/${cycle}/${subjectId}/${year}/answers/${paperFileid}.json`;

/** Dev-only override: when VITE_PAPER_TRAIL_LOCAL is set (e.g. in .env.local),
 *  documents resolve against a local mirror server instead of Firebase Storage,
 *  so a new year can be previewed on localhost before its upload. The mirror
 *  serves the same `papers/...` layout and redirects misses to live Storage.
 *  Unset in production builds, leaving the plain Storage REST endpoint. */
const LOCAL_BASE = (import.meta as unknown as {
  env?: { VITE_PAPER_TRAIL_LOCAL?: string };
}).env?.VITE_PAPER_TRAIL_LOCAL;

/** Public REST URL for a corpus document (range-request capable, CORS-open). */
export const paperUrl = (path: string) =>
  LOCAL_BASE
    ? `${LOCAL_BASE}/${path}`
    : hostedPaperDocumentUrl(path)
      ?? `https://firebasestorage.googleapis.com/v0/b/${BUCKET}/o/${encodeURIComponent(path)}?alt=media`;

export const prettyBytes = (b: number) => {
  if (!b) return '';
  if (b < 1024 * 1024) return `${Math.max(1, Math.round(b / 1024))} KB`;
  return `${(b / (1024 * 1024)).toFixed(1)} MB`;
};
