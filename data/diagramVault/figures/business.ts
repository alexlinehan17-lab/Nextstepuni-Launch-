/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — business figures extracted from SEC question papers. Written by
 * tools/dv_apply.py from agent-verified crops; do not hand-edit (re-run apply).
 */

import { nf } from '../nf';
import type { DiagramEntry } from '../index';

export const BUSINESS_FIGURES: DiagramEntry[] = [
  nf({
    subjectId: "business", subjectLabel: "Business",
    level: "ordinary", year: 2025,
    topicLabel: "Inflation rate forecast", questionRef: "2025 OL p4",
    src: "/exam-figures/business/business-2025-ol-inflation-rate-forecast.png",
    alt: "Bar chart titled \"Inflation rate forecast\" with a euro currency symbol on the left. Four bars of descending height labelled by year with values: 2022 8.1%, 2023 5.4%, 2024 3.2%, 2025 2.3%.",
    source: "SEC Leaving Certificate Business 2025 Ordinary Level — © State Examinations Commission",
  }),
  nf({
    subjectId: "business", subjectLabel: "Business",
    level: "ordinary", year: 2024,
    topicLabel: "Product Life Cycle", questionRef: "2024 OL p5",
    src: "/exam-figures/business/business-2024-ol-product-life-cycle.png",
    alt: "A product life cycle line graph. A single sales curve rises from the origin, peaks, then falls. The vertical axis is labelled SALES. Five stage boxes run across the top: Launch, Growth, Stage 3, Saturation and Decline, separated by vertical dashed lines. The Stage 3 box is shaded.",
    source: "SEC Leaving Certificate Business 2024 Ordinary Level — © State Examinations Commission",
  }),
  nf({
    subjectId: "business", subjectLabel: "Business",
    level: "ordinary", year: 2022,
    topicLabel: "International trade / imports", questionRef: "2022 OL p4",
    src: "/exam-figures/business/business-2022-ol-imports-pie-chart.png",
    alt: "A pie chart divided into several segments of differing sizes, shown in shades of grey with white borders between segments. Visible labels include a segment marked 19% and partial country labels including UK and USA.",
    source: "SEC Leaving Certificate Business 2022 Ordinary Level — © State Examinations Commission",
  }),
  nf({
    subjectId: "business", subjectLabel: "Business",
    level: "ordinary", year: 2021,
    topicLabel: "Maslow's Hierarchy of Needs", questionRef: "2021 OL p6",
    src: "/exam-figures/business/business-2021-ol-maslow-hierarchy-of-needs.png",
    alt: "A five-tier triangle diagram of Maslow's Hierarchy of Needs. From the base upward the tiers are labelled: Physiological, a blank tier marked 2, Social, a blank tier marked 4, and a blank tier marked 5 at the apex.",
    source: "SEC Leaving Certificate Business 2021 Ordinary Level — © State Examinations Commission",
  }),
];
