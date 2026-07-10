/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — the `nf` helper for native (paper-extracted) figures. Lives in
 * its own module so per-subject figure files and native.ts can both import it
 * without an initialisation cycle.
 */

import type { DiagramEntry } from './index';

/** Build a native figure entry. `src` is the public path to the saved PNG; the
 *  id is derived from it. Wave authors pass only the paper-specific fields. */
export const nf = (e: {
  subjectId: string;
  subjectLabel: string;
  topicLabel?: string | null;
  level?: string | null;
  year?: number | null;
  questionRef?: string | null;
  src: string;
  alt: string;
  source: string;
}): DiagramEntry => ({
  id: e.src.replace(/^.*\/exam-figures\//, '').replace(/\.png$/i, '').replace(/[/\s]+/g, '-'),
  subjectId: e.subjectId,
  subjectLabel: e.subjectLabel,
  topicLabel: e.topicLabel ?? null,
  level: e.level ?? null,
  year: e.year ?? null,
  questionRef: e.questionRef ?? null,
  src: e.src,
  alt: e.alt,
  source: e.source,
});
