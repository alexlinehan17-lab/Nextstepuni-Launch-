/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Diagram Vault — physical-education figures extracted from SEC question papers. Written by
 * tools/dv_apply.py from agent-verified crops; do not hand-edit (re-run apply).
 */

import { nf } from '../nf';
import type { DiagramEntry } from '../index';

export const PHYSICAL_EDUCATION_FIGURES: DiagramEntry[] = [
  nf({
    subjectId: "physical-education", subjectLabel: "Physical Education",
    level: "higher", year: 2024,
    topicLabel: "WHO physical activity guidelines - daily moderate to vigorous activity", questionRef: "2024 HL Q10",
    src: "/exam-figures/physical-education/physical-education-2024-hl-q10-who-guidelines-daily-activity.png",
    alt: "Infographic stating that at least 60 minutes a day of moderate- to vigorous-intensity physical activity should be done across the week, with most of this physical activity being aerobic. Includes a clock icon, a silhouette of a child on a kick scooter, and an intensity scale of five dots with three filled.",
    source: "SEC Leaving Certificate Physical Education 2024 Higher Level, Q10 — © State Examinations Commission",
  }),
  nf({
    subjectId: "physical-education", subjectLabel: "Physical Education",
    level: "higher", year: 2024,
    topicLabel: "WHO physical activity guidelines - vigorous-intensity activity", questionRef: "2024 HL Q10",
    src: "/exam-figures/physical-education/physical-education-2024-hl-q10-who-guidelines-vigorous-activity.png",
    alt: "Infographic stating that on at least 3 days a week, vigorous-intensity aerobic activities, as well as those that strengthen muscle and bone, should be incorporated. Includes a calendar icon, silhouettes of two young people playing with a ball, and an intensity scale of five dots.",
    source: "SEC Leaving Certificate Physical Education 2024 Higher Level, Q10 — © State Examinations Commission",
  }),
  nf({
    subjectId: "physical-education", subjectLabel: "Physical Education",
    level: "higher", year: 2024,
    topicLabel: "Positive doping tests in cycling over time", questionRef: "2024 HL Q16",
    src: "/exam-figures/physical-education/physical-education-2024-hl-q16-doping-positive-tests-line-graph.png",
    alt: "Line graph labelled 'Positive tests' showing the number of positive tests per year from about 2003 to 2021. Values peak above 600 around 2007, fall sharply to under 400 by 2008, decline gradually to around 220-320 through the 2010s, drop below 100 around 2020, and rise to about 150 in 2021.",
    source: "SEC Leaving Certificate Physical Education 2024 Higher Level, Q16 — © State Examinations Commission",
  }),
  nf({
    subjectId: "physical-education", subjectLabel: "Physical Education",
    level: "ordinary", year: 2024,
    topicLabel: "Energy systems — percentage of total energy over time", questionRef: "2024 OL Q14",
    src: "/exam-figures/physical-education/physical-education-2024-ol-q14-energy-systems-graph.png",
    alt: "Line graph labelled 'percentage of total energy' on the vertical axis (0 to 100) with three curves labelled A, B and C. Curve A (red) peaks sharply near the start then falls to zero, curve B (yellow) peaks later before declining, and curve C (green) rises gradually and plateaus at the highest level.",
    source: "SEC Leaving Certificate Physical Education 2024 Ordinary Level, Q14 — © State Examinations Commission",
  }),
];
