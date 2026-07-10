/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — NATIVE figures. These are extracted directly from SEC question
 * papers by the extraction pipeline (tools/detect_exam_figures.py → crop →
 * agent-verify), independent of the catch-up-lane / command-word exhibits that
 * seed the derived half of the vault. Each entry is a figure an agent VIEWED and
 * confirmed: a real diagram/graph/map/chart cropped from the paper, with an alt
 * describing only what the figure shows and an SEC `source` naming the exact
 * paper + question.
 *
 * INTEGRITY: every entry here is covered by the same gate as the derived half
 * (test/diagramVault.test.ts) — the file at `src` must exist in public/, the
 * source must be SEC-attributed, ids unique. A `src` collision with a derived
 * figure is resolved in index.ts (native wins — it is the primary paper crop).
 *
 * Grows subject by subject; the `nf` helper stamps the id + subjectLabel so wave
 * authors write only the paper-specific fields. Ordered by subject then year.
 */

import type { DiagramEntry } from './index';

/** Build a native figure entry. `src` is the public path to the saved PNG. */
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

/**
 * Extracted figures, appended by extraction waves. Empty until the first wave
 * lands; the vault falls back to the derived exhibits until then.
 */
export const NATIVE_FIGURES: DiagramEntry[] = [
];
