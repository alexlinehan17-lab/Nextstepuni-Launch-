/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — agricultural-economics figures extracted from SEC question papers. Written by
 * tools/dv_apply.py from agent-verified crops; do not hand-edit (re-run apply).
 */

import { nf } from '../nf';
import type { DiagramEntry } from '../index';

export const AGRICULTURAL_ECONOMICS_FIGURES: DiagramEntry[] = [
  nf({
    subjectId: "agricultural-economics", subjectLabel: "Agricultural Economics",
    level: "higher", year: 2019,
    topicLabel: "Price elasticity of supply — two supply curves", questionRef: null,
    src: "/exam-figures/agricultural-economics/agricultural-economics-2019-hl-supply-elasticity-graphs.png",
    alt: "Two side-by-side supply graphs, each with Price on the vertical axis and Quantity on the horizontal axis. The left graph shows a vertical supply curve labelled S1; the right graph shows an upward-sloping supply curve labelled S2.",
    source: "SEC Leaving Certificate Agricultural Economics 2019 Higher Level — © State Examinations Commission",
  }),
];
