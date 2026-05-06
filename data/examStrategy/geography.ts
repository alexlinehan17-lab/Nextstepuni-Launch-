/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Subject strategy preamble for Geography (Higher Level).
 */

import { type SubjectStrategy } from '../../types/examStrategiser';

export const geographyStrategy: SubjectStrategy = {
  subject: 'geography',
  headline: 'How Geography Higher Level is marked',
  intro:
    'Geography Paper 2 is marked in SRPs — Significant Relevant Points, each worth 2 marks. The marking scheme also embeds punitive caps ("Max X SRPs if…") that are easy to trigger and hard to recover from. Know the caps before you write.',
  rules: [
    {
      id: 'srp',
      title: 'The SRP system',
      body: 'Each Significant Relevant Point earns 2 marks. A 30-mark question awards roughly 14 SRPs of explanation plus 2 marks for naming a feature/landform. Aim for 15-16 distinct SRPs to leave headroom — the marking scheme rewards depth over breadth, but you need enough hooks for the examiner to land marks on.',
    },
    {
      id: 'max-srp-caps',
      title: '"Max X SRPs if…" — the killer caps',
      body: 'The single most punitive marking pattern. Examples: "Max 7 SRPs if only one factor examined" caps you at 14 of 30. "Max 2 SRPs if merely description without reference to formation" caps at 4 of 30. "Examination of erosion 0 marks" if the question asks about deposition. Read the marking-scheme caps BEFORE the indicative material — they\'re the difference between H1 and H4.',
      pinned: true,
    },
    {
      id: 'geographic-constraints',
      title: 'Geographic constraints — Ireland-tied vs not-Europe',
      body: 'Some questions tie you to Ireland; others explicitly forbid Ireland or Europe. Get this wrong and the entire answer scores 0 regardless of quality. Examples: "the Irish landscape" — Ireland-only. "Continental/Sub-Continental region (not in Europe)" — outside the EU. Pick your region BEFORE you start writing — switching mid-answer is a disaster.',
    },
    {
      id: 'diagram-labels',
      title: 'Diagram without labels = 0 marks',
      body: 'A universal rule across every Section 1 30-mark question. The diagram bonus (+1 SRP base, +2 SRPs for additional labelled info) only applies when the diagram is fully labelled. Arrows, named features, mantle/crust/ice layers, time markers — all need labels. An unlabelled diagram earns nothing.',
    },
    {
      id: 'two-features-two-examples',
      title: 'Bonus SRPs for second feature + named examples',
      body: 'Most physical-process questions reward "+1 SRP for a second feature/landform identified" and "+2 SRPs for two named examples" (Ireland-tied for Q1C, anywhere for Q2). These are easy SRPs if you know the pattern — name TWO different examples in different locations.',
    },
  ],
  marksToMinutes: {
    summary: 'HL Part Two: 320 marks across 140 minutes — roughly 0.44 minutes per mark.',
    examples: [
      '20-mark structured (Section A) → ~9 mins',
      '30-mark essay (Section B/C) → ~13 mins',
      '50-mark sketch-map question → ~22 mins',
      'Total Part Two budget for 4 questions × 80 marks = 140 mins',
    ],
  },
};
