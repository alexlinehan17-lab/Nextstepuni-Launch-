/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — applied-mathematics figures extracted from SEC question papers. Written by
 * tools/dv_apply.py from agent-verified crops; do not hand-edit (re-run apply).
 */

import { nf } from '../nf';
import type { DiagramEntry } from '../index';

export const APPLIED_MATHEMATICS_FIGURES: DiagramEntry[] = [
  nf({
    subjectId: "applied-mathematics", subjectLabel: "Applied Mathematics",
    level: "ordinary", year: 2021,
    topicLabel: "Connected particles and pulleys", questionRef: "2021 OL p3",
    src: "/exam-figures/applied-mathematics/applied-mathematics-2021-ol-connected-particles-pulleys.png",
    alt: "Two mechanics diagrams. Top: a pulley fixed to a horizontal support with a string over it, a block labelled 5 kg hanging on the left and a block labelled 3 kg hanging on the right. Bottom: an inclined plane at angle theta with a block labelled 5.2 kg on the incline, connected by a string over a pulley at the top of the incline to a block labelled 4 kg hanging vertically.",
    source: "SEC Leaving Certificate Applied Mathematics 2021 Ordinary Level — © State Examinations Commission",
  }),
];
