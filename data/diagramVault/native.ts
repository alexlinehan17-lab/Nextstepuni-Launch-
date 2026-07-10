/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — NATIVE figures aggregate. Figures extracted straight from SEC
 * question papers by the extraction pipeline (tools/detect_exam_figures.py →
 * dv_prepare → agent-verify → dv_apply) land in one file per subject under
 * `./figures/`, and this module concatenates them. Each entry is a figure an
 * agent VIEWED and confirmed: a real diagram/graph/map/chart cropped from the
 * paper, with an alt describing only what the figure shows and an SEC `source`
 * naming the exact paper + question.
 *
 * INTEGRITY: every entry is covered by the same gate as the derived half
 * (test/diagramVault.test.ts) — the file at `src` must exist in public/, the
 * source must be SEC-attributed, ids unique. A `src` collision with a derived
 * figure is resolved in index.ts (native wins — it is the primary paper crop).
 *
 * Subject files are added to the imports + spread below as each wave lands.
 */

import type { DiagramEntry } from './index';
import { BIOLOGY_FIGURES } from './figures/biology';
import { GEOGRAPHY_FIGURES } from './figures/geography';
import { PHYSICS_FIGURES } from './figures/physics';
import { CHEMISTRY_FIGURES } from './figures/chemistry';
import { BUSINESS_FIGURES } from './figures/business';

export const NATIVE_FIGURES: DiagramEntry[] = [
  ...BIOLOGY_FIGURES,
  ...GEOGRAPHY_FIGURES,
  ...PHYSICS_FIGURES,
  ...CHEMISTRY_FIGURES,
  ...BUSINESS_FIGURES,
];
