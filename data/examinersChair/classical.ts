/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Classical Studies (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the essay "unit of development" = point + evidence +
 * development, the narrative-caps-Overall-Quality rule, and the two-part
 * structural cap) is the real SEC system, cited to:
 *  - SEC LC Classical Studies HL marking scheme 2025 —
 *    examiner-reports/classical-studies/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Classical Studies HL marking scheme 2025, ${p}` });

// ─────────────── CL1 · A unit needs all three parts ───────────────

const CL1: GridSession = {
  mode: 'grid',
  id: 'cl-unit',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Point, evidence, development',
  cue: 'Essay',
  question: 'Section B essays score 15 marks per “unit of development”, and a full unit needs all three parts: a relevant point, relevant evidence, and development (analysis/elaboration). A candidate makes a strong point with good evidence — but never analyses or develops it. How much of the 15 does the unit earn?',
  questionNote:
    'Scenario authored for this exercise. A markable Classical Studies essay unit requires a relevant point, relevant evidence, AND development; a well-developed unit scores 15, a merely stated point-with-evidence sits far lower.',
  grid: {
    perPoint: [
      { id: 'point', label: 'Relevant point', marks: 4 },
      { id: 'evidence', label: 'Relevant evidence', marks: 4 },
      { id: 'development', label: 'Development (analysis)', marks: 7 },
    ],
    shorthand: '15 per unit: point + evidence + development',
    ruleNote:
      'All three parts are needed for a well-developed unit. The development — the analysis, elaboration or discussion — carries the most, and a point-plus-evidence that stops before analysing lands in the lower “basic/developed” bands, not the top.',
    cite: MS('p.11 (unit of development structure)'),
  },
  scripts: [
    {
      id: 'cl1-a',
      label: 'The unit',
      persona: 'Point + evidence, no analysis',
      attempts: [
        {
          id: 'cl1-a-1',
          text: 'A relevant point, backed by an accurate piece of evidence from the text — but the answer moves straight on without analysing what the evidence shows.',
          key: { point: 4, evidence: 4, development: 0 },
          keyNote: 'Point and evidence are there (8), but a full unit needs development — the analysis of what the evidence demonstrates about the point. Without it the unit stays in the lower bands. One sentence of “this shows that…” is what lifts a unit toward the full 15.',
        },
      ],
      embodies: {
        behaviour: 'States a point with evidence but never develops it — the unit stalls below full marks.',
        cite: MS('p.11'),
      },
    },
    {
      id: 'cl1-b',
      label: 'The unit',
      persona: 'All three parts',
      attempts: [
        {
          id: 'cl1-b-1',
          text: 'The same point and evidence, then a sentence analysing what the evidence reveals and why it matters to the question.',
          key: { point: 4, evidence: 4, development: 7 },
          keyNote: 'Point, evidence and development — a complete, well-developed unit. 15/15. The analysis is what turned an 8 into a 15.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cl1',
    rule: 'A unit isn’t complete until you analyse the evidence.',
    detail:
      'Classical Studies essay units score on point + evidence + development, and the development carries the most. A point backed by a quote still needs the “this shows that…” analysis to reach the top band. Always analyse your evidence.',
    cite: MS('p.11'),
  },
};

// ─────────────── CL2 · Answer both parts ───────────────

const CL2: ScaleSession = {
  mode: 'scale',
  id: 'cl-two-part',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Both parts, or a hard ceiling',
  cue: 'Essay',
  question: 'A Section B essay has two parts, (a) and (b). A candidate writes a rich answer with four well-developed units — but all of it addresses part (a); part (b) is ignored. The scheme caps a one-part answer’s Overall Quality in the Low range unless the full question is addressed. Roughly where does the 80-mark essay top out?',
  questionNote:
    'Scenario authored for this exercise. The scheme states the answer must address the full question (parts a and b) for more than three units of development to count and for Overall Quality to rise above the Low range — roughly a 57/80 ceiling for a one-sided answer.',
  scale: {
    name: 'Two-part essay ceiling · /80',
    levels: [
      { id: 'm57', label: 'Max ~57 (one part only)', annotation: '57', marks: 57 },
      { id: 'm80', label: 'Up to 80 (both parts)', annotation: '80', marks: 80 },
    ],
    notes: [
      'The essay must address the full question — both (a) and (b).',
      'A one-part answer: no more than three units count, and Overall Quality can’t rise above the Low range.',
      'That imposes a structural ceiling around 57/80, however good the one part is.',
    ],
    cite: MS('p.11 (full-question requirement)'),
  },
  scripts: [
    {
      id: 'cl2-a',
      label: 'The essay',
      persona: 'Brilliant — on part (a) only',
      work: [
        'Four well-developed units, all on part (a).',
        'Part (b) of the question is never addressed.',
      ],
      keyLevelId: 'm57',
      keyNote:
        'Capped around 57 of 80 — a one-part answer can’t have more than three units count, and its Overall Quality is held in the Low range, no matter how strong part (a) is. Even a short, weaker treatment of part (b) removes the ceiling. Always give both parts of the question real attention.',
      embodies: {
        behaviour: 'Answers only one part of a two-part essay — hitting the structural ceiling.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl2',
    rule: 'Address both parts, or you’re capped near 57/80.',
    detail:
      'A one-sided answer to a two-part Classical Studies essay caps its units and holds Overall Quality in the Low range — roughly 57/80. Give both parts genuine treatment; even a brief second part lifts the ceiling.',
    cite: MS('p.11'),
  },
};

// ─────────────── CL3 · Narrative caps Quality ───────────────

const CL3: ScaleSession = {
  mode: 'scale',
  id: 'cl-narrative',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Retelling isn’t arguing',
  cue: 'Essay (Overall Quality)',
  question: 'The essay’s Overall Quality is scored out of 20. A candidate retells the myth or the events accurately and vividly, but never builds an argument in response to the question. The Low Quality band is defined as “relies mostly on narrative”. Where does Overall Quality land?',
  questionNote:
    'Scenario authored for this exercise. Overall Quality (20 of the 80) is a separate holistic mark; its Low band is explicitly “relies mostly on narrative”, so a retelling can’t reach the High band.',
  scale: {
    name: 'Overall Quality · /20',
    levels: [
      { id: 'low', label: 'Low (1–12) — narrative', annotation: 'L', marks: 10 },
      { id: 'good', label: 'Good (13–17)', annotation: 'G', marks: 15 },
      { id: 'high', label: 'High (18–20)', annotation: 'H', marks: 19 },
    ],
    notes: [
      'Overall Quality is a separate 20 marks on top of the units.',
      'Low band (1–12): “relies mostly on narrative”.',
      'Higher bands need argument and analysis in response to the question, not retelling.',
    ],
    cite: MS('p.11 (Overall Quality bands)'),
  },
  scripts: [
    {
      id: 'cl3-a',
      label: 'The essay',
      persona: 'Vivid retelling',
      work: [
        'Accurate, vivid narration of the myth/events.',
        'No argument built in response to the question.',
      ],
      keyLevelId: 'low',
      keyNote:
        'Low Quality band — “relies mostly on narrative” is exactly this essay, so Overall Quality is held under 12 however vivid the storytelling. The higher bands are bought with argument: use the narrative as evidence for points that answer the question, don’t let it be the answer.',
      embodies: {
        behaviour: 'Retells the story instead of arguing — the named Low Quality descriptor.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl3',
    rule: 'Use the story as evidence, don’t just retell it.',
    detail:
      'Classical Studies Overall Quality caps in the Low band when an essay “relies mostly on narrative”. Turn the narrative into evidence for an argument that answers the question — retelling alone can’t reach the top.',
    cite: MS('p.11'),
  },
};

export const CLASSICAL_CHAIR: ChairSubject = {
  id: 'classical-studies',
  label: 'Classical Studies',
  tagline: 'Develop your units, answer both parts, argue not narrate.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CL1, CL2, CL3],
  sources: [
    { label: 'SEC LC Classical Studies HL marking scheme 2025 (examiner-reports/classical-studies/2025-marking-scheme)' },
  ],
  coverageNote:
    'Verified against the 2025 Higher Level scheme. The unit-of-development system and Overall Quality bands also structure Ordinary Level; OL-specific worked questions are being added.',
};
