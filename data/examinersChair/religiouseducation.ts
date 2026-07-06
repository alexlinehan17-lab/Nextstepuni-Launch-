/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Religious Education (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (holistic six-band marking, and the "descriptive answer to a
 * higher-order command is capped at the top of Fair" rule) is the real SEC
 * system, cited to:
 *  - SEC LC Religious Education HL marking scheme 2025 —
 *    examiner-reports/religious-education/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Religious Education HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Religious Education OL marking scheme 2025, ${p}` });

// ─────────────── RE1 · Do the command word ───────────────

const RE1: ScaleSession = {
  mode: 'scale',
  id: 're-command',
  subject: 'religious-education',
  level: 'higher',
  title: 'Describe when it says assess',
  cue: 'Assess',
  question: 'A 40-mark question says “Assess”. The candidate writes a full, accurate, well-organised description of the topic — but never actually assesses anything. The scheme caps a descriptive answer to a higher-order command at the top of the Fair band (Max 21 on a 40-mark question). Where does it land?',
  questionNote:
    'Scenario authored for this exercise. RE marks holistically in six bands; a descriptive answer to a higher-order command word (Assess/Compare/Discuss) is ceilinged at the top of the Fair band.',
  scale: {
    name: 'Descriptive cap · /40',
    levels: [
      { id: 'fair', label: 'Max Fair (21) — descriptive', annotation: 'F', marks: 21 },
      { id: 'good', label: 'Good (22–27)', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'RE marks each answer holistically into one band, not by points.',
      'A description given for a higher-order command (Assess/Compare/Discuss) is capped at the top of Fair — Max 21 on a 40-mark question.',
      'Doing the command word is what unlocks the bands above Fair.',
    ],
    cite: MS('p.18 (descriptive-answer cap; band ranges p.6)'),
  },
  scripts: [
    {
      id: 're1-a',
      label: 'The answer',
      persona: 'Describes instead of assessing',
      work: [
        'Full, accurate, well-organised description of the topic.',
        'Never weighs, judges or assesses — the command word “Assess” isn’t performed.',
      ],
      keyLevelId: 'fair',
      keyNote:
        'Capped at 21 of 40 — the top of Fair — because the answer describes where the command asked it to assess. Accuracy and coverage can’t lift it past that cap; only doing the command word can. One evaluative thread (strengths, weaknesses, a judgement) would unlock the higher bands.',
      embodies: {
        behaviour: 'Describes rather than performing the higher-order command — the descriptive cap applies.',
        cite: MS('p.18'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re1',
    rule: 'Do the command word, or you’re capped at Fair.',
    detail:
      'RE ceilings a descriptive answer to “Assess/Compare/Discuss” at the top of the Fair band, regardless of accuracy. Perform the command — weigh, judge, compare — to reach the bands above.',
    cite: MS('p.18'),
  },
};

// ─────────────── RE2 · Holistic bands ───────────────

const RE2: ScaleSession = {
  mode: 'scale',
  id: 're-holistic',
  subject: 'religious-education',
  level: 'higher',
  title: 'One band for the whole answer',
  cue: 'Discuss',
  question: 'RE marks each answer as one holistic band judged on four things at once: evidence of the marking criteria, relevance, use of the skill, and factual accuracy. An answer is insightful and relevant — but contains a couple of clear factual errors. How does accuracy affect the band?',
  questionNote:
    'Scenario authored for this exercise. Each RE answer gets one holistic band; factual accuracy is one of the four descriptor dimensions, so errors lower the whole band rather than being a line-item deduction.',
  scale: {
    name: 'Holistic band /20',
    levels: [
      { id: 'good', label: 'Good (11–13)', annotation: 'G', marks: 12 },
      { id: 'vgood', label: 'Very Good (14–16)', annotation: 'VG', marks: 15 },
      { id: 'excellent', label: 'Excellent (17–20)', annotation: 'E', marks: 18 },
    ],
    notes: [
      'The answer is placed in one band on four dimensions at once: marking criteria, relevance, skill, factual accuracy.',
      'Accuracy isn’t a separate subtraction — it’s one of the things that sets the band.',
      'Clear factual errors pull an otherwise strong answer down a band.',
    ],
    cite: MS('p.2, p.4 (four-dimension holistic banding)'),
  },
  scripts: [
    {
      id: 're2-a',
      label: 'The answer',
      persona: 'Insightful, but with errors',
      work: [
        'Relevant and insightful discussion.',
        'But a couple of clear factual errors (wrong text, wrong figure).',
      ],
      keyLevelId: 'vgood',
      keyNote:
        'It settles a band lower than its insight alone would earn — accuracy is one of the four things the band weighs, so errors drag the whole judgement down rather than costing a fixed number of marks. Getting your facts right protects the band your analysis has earned. Precision and insight both set the ceiling.',
      embodies: {
        behaviour: 'Strong analysis undercut by factual errors, which lower the holistic band.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re2',
    rule: 'Accuracy sets the band, not a deduction.',
    detail:
      'RE judges each answer holistically on marking criteria, relevance, skill and accuracy together — factual errors lower the whole band rather than costing set marks. Keep your facts precise to protect the band your insight earns.',
    cite: MS('p.2'),
  },
};

// ─────────────── RE3 · OL — a strong description reaches the top ───────────────

const RE3: ScaleSession = {
  mode: 'scale',
  id: 're-ol-describe',
  subject: 'religious-education',
  level: 'ordinary',
  title: 'At OL, describing is enough',
  cue: 'Describe (OL)',
  question: 'At Higher Level, a purely descriptive answer to a higher-order command is capped at the top of Fair. At Ordinary Level there is NO such cap — the commands are Outline/Describe/Give an account, and a full, accurate, relevant description can reach the top band. A candidate writes exactly that. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Unlike HL, the OL scheme contains no descriptive-answer cap — its commands are lower-order (Describe/Outline), and a strong description is a top-band answer.',
  scale: {
    name: 'OL description · /40 bands',
    levels: [
      { id: 'fair', label: 'Fair (16–21)', annotation: 'F', marks: 19 },
      { id: 'good', label: 'Good (22–27)', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'OL centres on lower-order skills (Outline, Describe, Give an account); even where an OL question uses a higher-order stem, the scheme does not cap a description at Fair.',
      'There is no HL-style descriptive cap at OL: a description is not ceilinged at Fair for “not evaluating.” Where an OL note applies a “Max”, it caps a partial answer that omits a required element — not a description.',
      'A full, accurate, relevant description can reach the Excellent band.',
    ],
    cite: MSOL('p.5, p.20 (no descriptive cap at OL)'),
  },
  scripts: [
    {
      id: 're3-a',
      label: 'The answer',
      persona: 'Full, accurate description',
      work: [
        'A complete, accurate, relevant description of the topic.',
        'The command was “Describe” — and it describes thoroughly.',
      ],
      keyLevelId: 'excellent',
      keyNote:
        'It can reach the Excellent band — at OL there’s no descriptive cap, because the command asked you to describe, and you did it fully and accurately. This is the mirror image of Higher Level, where the same description would be capped at Fair. At OL, do exactly what the command word asks, thoroughly and accurately, and the top band is open.',
      embodies: {
        behaviour: 'Answers an OL “describe” command with a full accurate description — top band, no cap.',
        cite: MSOL('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re3',
    rule: 'At OL, a thorough accurate description is a top answer.',
    detail:
      'Ordinary Level RE has no descriptive cap — its commands are Describe/Outline/Give an account, and a full, accurate, relevant description can reach the Excellent band. Do exactly what the command asks, thoroughly and accurately.',
    cite: MSOL('p.5'),
  },
};

// ─────────────── RE4 · “Two” means two independent scores ───────────────

const RE4: ScaleSession = {
  mode: 'scale',
  id: 're-two-items',
  subject: 'religious-education',
  level: 'higher',
  title: 'When it says “two”, one brilliant answer isn’t enough',
  cue: 'Outline two',
  question: 'A 20-mark question says “Outline two images of God.” It’s marked as two separate 10-mark scores — the examiner codes “MC x 2” and bands each image independently. A candidate writes one flawless, Excellent account of God as Shepherd, and never gives a second image. Where does the whole answer land out of 20?',
  questionNote:
    'Scenario authored for this exercise. A “two-item” RE question (e.g. “Outline two images of God”, 10M × 2) is banded twice — the scheme instructs the examiner to “Code MC x 2” and mark each item on its own 10-mark grid; a missing item is coded MC X (no evidence).',
  scale: {
    name: 'Two-item split · /20',
    levels: [
      { id: 'half', label: 'One image only — Max 10 (second is MC X)', annotation: 'MC×1', marks: 10 },
      { id: 'onethin', label: 'One strong + one thin (≈13)', annotation: 'E+W', marks: 13 },
      { id: 'twosolid', label: 'Two solid images (≈16)', annotation: 'G+G', marks: 16 },
      { id: 'twotop', label: 'Two excellent images (20)', annotation: 'E+E', marks: 20 },
    ],
    notes: [
      'A “two-item” question is banded twice: the examiner codes “MC x 2” and marks each image on its own 10-mark grid (10–8 / 7 / 6–5 / 4 / 3–2 / 1–0).',
      'The two scores are independent — extra quality on one image cannot compensate for a missing one; a missing item is coded MC X (no evidence) and scores nothing.',
      'Doing one of two perfectly caps the whole answer at Max 10 — half the marks for half the task.',
    ],
    cite: MS('p.8 (Q2(b)(i) “Outline two images of God”, 10M × 2, “Code MC x 2”; MC X annotation p.3)'),
  },
  scripts: [
    {
      id: 're4-a',
      label: 'The answer',
      persona: 'One image, done perfectly',
      work: [
        'A flawless, accurate, Excellent-band account of God as Shepherd.',
        'No second image of God is ever given — the second half of the question is left blank.',
      ],
      keyLevelId: 'half',
      keyNote:
        'Capped at 10 of 20. The command asked for two images, so the examiner codes MC x 2 and bands each independently: image one earns a full Excellent 10, but image two is coded MC X — no evidence, no marks. The two scores don’t pool, so a perfect first image can’t cover a missing second. Half the task, half the marks. Two shorter, solid images would beat one flawless one here.',
      embodies: {
        behaviour: 'Answers only one of two required items — the second is coded MC X and the whole answer caps at half the marks.',
        cite: MS('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re4',
    rule: 'When it says “two”, give two — the scores don’t pool.',
    detail:
      'RE bands a “two-item” question twice (“Code MC x 2”), marking each item on its own grid; a missing item is coded MC X and scores zero. One flawless answer can’t make up for a missing second — cover every item the command lists.',
    cite: MS('p.8'),
  },
};

export const RE_CHAIR: ChairSubject = {
  id: 'religious-education',
  label: 'Religious Education',
  tagline: 'Holistic bands — do the command word and keep it accurate.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [RE1, RE2, RE3, RE4],
  sources: [
    { label: 'SEC LC Religious Education HL marking scheme 2025 (examiner-reports/religious-education/2025-marking-scheme)' },
    { label: 'SEC LC Religious Education OL marking scheme 2025 (examiner-reports/religious-education/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The holistic six-band system applies at both levels. But the descriptive cap is Higher-specific — at Ordinary Level the commands are lower-order and there is no cap, so a thorough description reaches the top band (verified against the 2025 OL scheme).',
};
