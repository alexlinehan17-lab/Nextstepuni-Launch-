/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Construction Studies (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (drawings marked as a checklist of named elements with a
 * fixed draw+annotation split, the note+sketch split that halves text-only
 * answers, and per-step calculation marking) is the real SEC system, cited to:
 *  - SEC LC Construction Studies HL marking scheme 2025 —
 *    examiner-reports/construction-studies/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Construction Studies HL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── CS1 · Labels are a quarter of every element ───────────────

const CS1: GridSession = {
  mode: 'grid',
  id: 'cs-labels',
  subject: 'construction-studies',
  level: 'common',
  title: 'A quarter of the marks are labels',
  cue: 'Draw the detail',
  question: 'A sectional detail is marked element by element, and each element is worth 3 for the drawing plus 1 for its annotation. A candidate draws four elements beautifully and correctly — but labels none of them.',
  questionNote:
    'Scenario authored for this exercise. Construction Studies marks big drawings as a checklist of named elements, each split 3 (drawing) + 1 (annotation); rubric makes labelling mandatory.',
  grid: {
    perPoint: [
      { id: 'e1', label: 'Element 1 — annotation', marks: 1 },
      { id: 'e2', label: 'Element 2 — annotation', marks: 1 },
      { id: 'e3', label: 'Element 3 — annotation', marks: 1 },
      { id: 'e4', label: 'Element 4 — annotation', marks: 1 },
    ],
    shorthand: 'each element: draw 3 + annotate 1',
    ruleNote:
      'The annotation is a quarter of every element’s marks, and it’s marked separately from the line-work. A flawless but unlabelled section forfeits every annotation mark — a routine, avoidable loss on every drawing.',
    cite: MS('p.37, p.43 (draw + annotation split)'),
  },
  scripts: [
    {
      id: 'cs1-a',
      label: 'Script A',
      persona: 'Perfect drawing, no labels',
      attempts: [
        {
          id: 'cs1-a-1',
          text: 'Four elements drawn accurately and neatly — none labelled or annotated.',
          key: { e1: 0, e2: 0, e3: 0, e4: 0 },
          keyNote: 'The drawing marks are earned, but every annotation mark — a quarter of each element — is gone. Naming each element (DPC, insulation, wall tie, lintel) would have added them for a few seconds’ writing. Labelling is mandatory and it’s free marks.',
        },
      ],
      embodies: {
        behaviour: 'Draws elements well but leaves them unlabelled, forfeiting the separate annotation marks.',
        cite: MS('p.37'),
      },
    },
    {
      id: 'cs1-b',
      label: 'Script B',
      persona: 'Drawn and labelled',
      attempts: [
        {
          id: 'cs1-b-1',
          text: 'The same four elements, each clearly labelled — DPC, insulation, wall tie, lintel.',
          key: { e1: 1, e2: 1, e3: 1, e4: 1 },
          keyNote: 'Every annotation mark banked on top of the drawing marks. The labels cost seconds and are guaranteed marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs1',
    rule: 'Label every element — a quarter of the marks depend on it.',
    detail:
      'Construction Studies drawings split each element into drawing (3) and annotation (1). Unlabelled drawings forfeit every annotation mark however good the line-work. Name every component you draw.',
    cite: MS('p.37'),
  },
};

// ─────────────── CS2 · The sketch is half the marks ───────────────

const CS2: ScaleSession = {
  mode: 'scale',
  id: 'cs-sketch',
  subject: 'construction-studies',
  level: 'common',
  title: 'No sketch, half the marks',
  cue: 'Describe with the aid of a sketch',
  question: 'A “describe, with the aid of a sketch” sub-part is marked 3 for the note and 3 for the sketch. A candidate writes an excellent, detailed note — but draws no sketch. What’s the maximum they can score?',
  questionNote:
    'Scenario authored for this exercise. Construction Studies “describe with a sketch” parts default to a 3 (note) + 3 (sketch) split; a text-only answer forfeits the sketch half.',
  scale: {
    name: 'Note + sketch · /6',
    levels: ladder([3, 6]),
    notes: [
      'The default split is note 3 + sketch 3.',
      'The question explicitly asks for a sketch — the words “with the aid of a sketch” are a mark instruction.',
      'A text-only answer, however good, caps at 3 of 6.',
    ],
    cite: MS('p.38, p.40 (note + sketch split)'),
  },
  scripts: [
    {
      id: 'cs2-a',
      label: 'The answer',
      persona: 'Great note, no sketch',
      work: ['A detailed, accurate written description.', 'No sketch drawn.'],
      keyLevelId: 'm3',
      keyNote:
        'Capped at 3 of 6 — the sketch is half the marks, and “with the aid of a sketch” is a mark instruction, not a suggestion. A rough, labelled sketch alongside the note would have doubled the score. When a question asks for a sketch, always draw one, however quick.',
      embodies: {
        behaviour: 'Answers a “describe with a sketch” part in text only — capping at half marks.',
        cite: MS('p.38'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs2',
    rule: 'If it asks for a sketch, the sketch is half the marks.',
    detail:
      '“Describe with the aid of a sketch” splits 3 note + 3 sketch — a text-only answer forfeits half. Always draw the sketch, even a rough labelled one; the words are a mark instruction.',
    cite: MS('p.38'),
  },
};

// ─────────────── CS3 · Show the U-value working ───────────────

const CS3: ScaleSession = {
  mode: 'scale',
  id: 'cs-uvalue',
  subject: 'construction-studies',
  level: 'higher',
  title: 'Every layer is a mark',
  cue: 'Calculate the U-value',
  question: 'A U-value calculation is marked per step: each material layer’s thermal resistance is its own 3-mark tick, and each substitution scores separately — around 33 marks across the working. A candidate writes only the correct final U-value, with no working. Roughly what does it score?',
  questionNote:
    'Scenario authored for this exercise. The U-value question is marked step-by-step — each resistance and each substitution is its own tick — so a bare answer forfeits the bulk of the marks.',
  scale: {
    name: 'U-value · per-step',
    levels: ladder([3, 20, 33]),
    notes: [
      'Each material-layer resistance = its own 3-mark tick; each substitution scores separately.',
      'The marks are spread across ~11 steps, not attached to the final number.',
      'A correct final U-value with no working banks almost none of them.',
    ],
    cite: MS('p.41 (per-step U-value marking, Q5)'),
  },
  scripts: [
    {
      id: 'cs3-a',
      label: 'The answer',
      persona: 'Final answer only',
      work: ['U = 0.24 W/m²K', '(correct — but no working shown)'],
      keyLevelId: 'm3',
      keyNote:
        'Almost nothing — the marks live in each layer’s resistance and each substitution, and none are on the page. A correct final number can’t reclaim the ~33 marks spread across the steps that produced it. Lay out every layer’s resistance and every substitution; it’s where the marks are.',
      embodies: {
        behaviour: 'Writes only the final U-value with no working — forfeiting the per-step marks.',
        cite: MS('p.41'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs3',
    rule: 'Show every layer — the U-value marks are in the steps.',
    detail:
      'The U-value question ticks each material layer’s resistance and each substitution separately (~33 marks), not the final number. Set out every layer and every substitution; a bare answer banks almost nothing.',
    cite: MS('p.41'),
  },
};

// ─────────────── CS4 · One advantage AND one disadvantage — both required ───────────────

const CS4: GridSession = {
  mode: 'grid',
  id: 'cs-adv-dis',
  subject: 'construction-studies',
  level: 'higher',
  title: 'One advantage AND one disadvantage',
  cue: 'Discuss one advantage and one disadvantage',
  question: 'A part asks candidates to “discuss one advantage and one disadvantage” of each of two wall types — the grid splits it Advantage 3 + Disadvantage 3 per wall (12 marks). A candidate knows the topic well and writes two strong advantages for each wall — but no disadvantages.',
  questionNote:
    'Scenario authored for this exercise. In Construction Studies an “advantage and a disadvantage” part is marked with a separate tick for each side — the advantage and the disadvantage each carry their own marks, so a second advantage cannot pay for the missing disadvantage.',
  grid: {
    perPoint: [
      { id: 'w1adv', label: 'Wall 1 — advantage', marks: 3 },
      { id: 'w1dis', label: 'Wall 1 — disadvantage', marks: 3 },
      { id: 'w2adv', label: 'Wall 2 — advantage', marks: 3 },
      { id: 'w2dis', label: 'Wall 2 — disadvantage', marks: 3 },
    ],
    shorthand: 'each wall: advantage 3 + disadvantage 3',
    ruleNote:
      'The advantage and the disadvantage are marked as separate ticks, one each per wall. A second advantage lands in a box that’s already full — the disadvantage box stays empty and its marks are lost. Both sides are required.',
    cite: MS('p.17 (question wording), p.40 (Q4(c) advantage + disadvantage split)'),
  },
  scripts: [
    {
      id: 'cs4-a',
      label: 'Script A',
      persona: 'Two advantages, no disadvantage',
      attempts: [
        {
          id: 'cs4-a-1',
          text: 'For each wall type: two well-explained advantages, and no disadvantage.',
          key: { w1adv: 3, w1dis: 0, w2adv: 3, w2dis: 0 },
          keyNote: 'Half the marks gone. The extra advantage scores nothing — there’s only one advantage tick per wall — while the disadvantage tick sits unfilled on both walls. When a part names two things (an advantage AND a disadvantage), each is a separate mark; answer both.',
        },
      ],
      embodies: {
        behaviour: 'Gives two advantages instead of an advantage and a disadvantage — forfeiting the disadvantage marks.',
        cite: MS('p.40'),
      },
    },
    {
      id: 'cs4-b',
      label: 'Script B',
      persona: 'One of each, per wall',
      attempts: [
        {
          id: 'cs4-b-1',
          text: 'For each wall type: one advantage and one disadvantage, each briefly discussed.',
          key: { w1adv: 3, w1dis: 3, w2adv: 3, w2dis: 3 },
          keyNote: 'Full marks. Every tick has something to score against because the answer mirrors what the question asked for — one advantage and one disadvantage per wall.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs4',
    rule: 'If it asks for an advantage AND a disadvantage, both are separate marks.',
    detail:
      'When a part names two things — “one advantage and one disadvantage” — each is its own tick (here 3 + 3 per wall). A second advantage cannot fill the disadvantage box; answer every side the question names.',
    cite: MS('p.40'),
  },
};

// ─────────────── CS5 · Naming a point is only half — you must discuss it ───────────────

const CS5: GridSession = {
  mode: 'grid',
  id: 'cs-point-discussion',
  subject: 'construction-studies',
  level: 'higher',
  title: 'A named point is only half the mark',
  cue: 'Discuss two benefits',
  question: 'A “discuss two benefits” part is marked 3 for the point + 3 for the discussion, per benefit (12 marks). A candidate names two correct benefits crisply — “better airtightness”, “lower heating bills” — but writes nothing to develop or justify either.',
  questionNote:
    'Scenario authored for this exercise. On Construction Studies discuss/benefit parts each item splits into a mark for STATING the point and a separate, equal mark for DEVELOPING it — so a bare list of correct points forfeits the discussion half.',
  grid: {
    perPoint: [
      { id: 'b1point', label: 'Benefit 1 — point stated', marks: 3 },
      { id: 'b1disc', label: 'Benefit 1 — discussion', marks: 3 },
      { id: 'b2point', label: 'Benefit 2 — point stated', marks: 3 },
      { id: 'b2disc', label: 'Benefit 2 — discussion', marks: 3 },
    ],
    shorthand: 'each benefit: point 3 + discussion 3',
    ruleNote:
      'The point and its discussion are two separate ticks of equal weight. Naming a benefit banks the point mark but leaves the discussion mark empty — you claim it by explaining the mechanism, the “why”, the benefit to the homeowner. A list of bare points caps at half.',
    cite: MS('p.44 (Q8(a) — 3 for point, 3 for discussion)'),
  },
  scripts: [
    {
      id: 'cs5-a',
      label: 'Script A',
      persona: 'Names both, develops neither',
      attempts: [
        {
          id: 'cs5-a-1',
          text: 'Two correct benefits named in a line each — “better airtightness”, “lower heating bills” — with no explanation of how or why.',
          key: { b1point: 3, b1disc: 0, b2point: 3, b2disc: 0 },
          keyNote: 'Half the marks. Both points are correct and score their 3, but the discussion tick — an equal 3 per benefit — sits empty because nothing develops them. One sentence each on the mechanism (how airtightness cuts draughts, why that lowers the bill) would have banked the other half.',
        },
      ],
      embodies: {
        behaviour: 'Lists correct points but does not develop them — forfeiting the discussion half of each mark.',
        cite: MS('p.44'),
      },
    },
    {
      id: 'cs5-b',
      label: 'Script B',
      persona: 'Point then discussion',
      attempts: [
        {
          id: 'cs5-b-1',
          text: 'Each benefit named, then a sentence developing it — how the detail works and what it gives the homeowner.',
          key: { b1point: 3, b1disc: 3, b2point: 3, b2disc: 3 },
          keyNote: 'Full marks. Every point tick and every discussion tick has something to score against, because each benefit is both stated and explained.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs5',
    rule: 'Naming the point is half the mark — the discussion is the other half.',
    detail:
      'Discuss/benefit parts split each item into a point mark and an equal discussion mark (here 3 + 3). A correct bare list caps at 50%; develop every point — the mechanism, the “why”, the benefit — to claim the rest.',
    cite: MS('p.44'),
  },
};

// ─────────────── CS6 · The drawing’s scale & drafting is a separate graded band ───────────────

const CS6: ScaleSession = {
  mode: 'scale',
  id: 'cs-scale-drafting',
  subject: 'construction-studies',
  level: 'higher',
  title: 'Neatness is its own eight marks',
  cue: 'Draw to scale',
  question: 'On top of the per-element checklist, a big sectional drawing carries a separate 8-mark quality band — Scale 4 + Drafting 4 — graded Excellent 8, Good 6, Fair 4. A candidate shows every correct element but rushes the line-work: freehand, not to scale, cramped and untidy. Where does the quality band land?',
  questionNote:
    'Scenario authored for this exercise. Construction Studies major drawings carry a fixed presentation band (Scale 4 + Drafting 4) graded in three tiers on top of the element marks — so drawing quality is scored separately from whether the elements are correct.',
  scale: {
    name: 'Scale + Drafting · /8',
    levels: [
      { id: 'fair', label: 'Fair', annotation: '4', marks: 4 },
      { id: 'good', label: 'Good', annotation: '6', marks: 6 },
      { id: 'excellent', label: 'Excellent', annotation: '8', marks: 8 },
    ],
    notes: [
      'The band is separate from and additional to the element checklist — it scores the whole drawing’s scale and drafting.',
      'It is graded in three fixed tiers: Excellent 8, Good 6, Fair 4.',
      'A genuine attempt never drops below Fair 4 — but rushed, out-of-scale, untidy line-work stays there and forfeits the top four marks.',
    ],
    cite: MS('p.37, p.43 (Scale 4 + Drafting 4 — Excellent 8 / Good 6 / Fair 4)'),
  },
  scripts: [
    {
      id: 'cs6-a',
      label: 'The answer',
      persona: 'All elements, rushed drafting',
      work: ['Every credited element shown and labelled.', 'But freehand, not to scale, cramped and untidy.'],
      keyLevelId: 'fair',
      keyNote:
        'Fair — 4 of the 8. The element marks are earned, but the presentation band grades the drawing itself, and rushed, out-of-scale line-work sits at the bottom tier. Drawing to scale with a clean, ruled layout would have lifted the same content to Excellent and banked four more marks — for tidiness, not extra knowledge.',
      embodies: {
        behaviour: 'Earns the element marks but neglects scale and drafting — capping the separate quality band at its lowest tier.',
        cite: MS('p.37'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs6',
    rule: 'Drawing to scale and drafting neatly is a separate 8 marks.',
    detail:
      'Major drawings carry a Scale 4 + Drafting 4 band graded Excellent 8 / Good 6 / Fair 4, on top of the element checklist. Correct-but-rushed line-work caps at Fair 4; a scaled, clean drawing banks the full 8 for presentation alone.',
    cite: MS('p.37'),
  },
};

// ─────────────── CS7 · Every brief requirement is a discrete tick you must satisfy ───────────────

const CS7: GridSession = {
  mode: 'grid',
  id: 'cs-brief-requirements',
  subject: 'construction-studies',
  level: 'higher',
  title: 'The brief is a checklist',
  cue: 'Revise the layout',
  question: 'A “revise the layout” part lists explicit requirements the design must meet, each a 2-mark tick: include a downstairs bathroom (2), create an open-plan kitchen/dining/living area (2), optimise daylight (2). A candidate draws a polished revised layout — open-plan and well-lit — but never adds a downstairs bathroom.',
  questionNote:
    'Scenario authored for this exercise. Where a Construction Studies design/layout question lists explicit requirements, each named requirement is a discrete mark the examiner ticks against the brief — a good drawing that ignores one still forfeits that tick.',
  grid: {
    perPoint: [
      { id: 'bathroom', label: 'Downstairs bathroom included', marks: 2 },
      { id: 'openplan', label: 'Open-plan kitchen/dining/living created', marks: 2 },
      { id: 'daylight', label: 'Daylight optimised', marks: 2 },
    ],
    shorthand: 'each stated requirement: 2 (met / not met)',
    ruleNote:
      'These sit on top of the holistic mark for the drawing itself — each is a separate tick for visibly satisfying one line of the brief. A beautiful layout that skips a required feature loses that requirement’s marks outright; the examiner is ticking a checklist against what was asked for.',
    cite: MS('p.39 (Q3(a) — downstairs bathroom / open-plan / daylight, 2 each)'),
  },
  scripts: [
    {
      id: 'cs7-a',
      label: 'Script A',
      persona: 'Polished layout, one requirement missed',
      attempts: [
        {
          id: 'cs7-a-1',
          text: 'A clean, well-resolved open-plan layout with daylight optimised — but no downstairs bathroom anywhere on the plan.',
          key: { bathroom: 0, openplan: 2, daylight: 2 },
          keyNote: 'A tick lost for nothing. Open-plan and daylight are both satisfied and score, but the downstairs bathroom was named in the brief and isn’t on the drawing, so its 2 marks are gone however good the rest is. Every requirement the question lists is a mark you must visibly deliver.',
        },
      ],
      embodies: {
        behaviour: 'Produces a strong design but omits one explicitly required feature — forfeiting that requirement’s discrete mark.',
        cite: MS('p.39'),
      },
    },
    {
      id: 'cs7-b',
      label: 'Script B',
      persona: 'Every requirement met',
      attempts: [
        {
          id: 'cs7-b-1',
          text: 'The same layout, with a downstairs bathroom added, the open-plan area created, and daylight optimised — all three visible on the plan.',
          key: { bathroom: 2, openplan: 2, daylight: 2 },
          keyNote: 'Every requirement tick banked, because each named feature is actually on the drawing. Working straight down the brief’s list guarantees these marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs7',
    rule: 'When a question lists requirements, each is a mark you must visibly deliver.',
    detail:
      'On design/layout questions the stated brief is a checklist — every named requirement (here 2 marks each) is ticked separately against your drawing. A polished layout that omits a required feature forfeits its mark; satisfy every line of the brief.',
    cite: MS('p.39'),
  },
};

export const CONSTRUCTION_CHAIR: ChairSubject = {
  id: 'construction-studies',
  label: 'Construction Studies',
  tagline: 'Label every element, sketch when asked, show every layer, develop every point.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CS1, CS2, CS3, CS4, CS5, CS6, CS7],
  sources: [
    { label: 'SEC LC Construction Studies HL marking scheme 2025 (examiner-reports/construction-studies/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — the element draw+annotation split, the note+sketch split, per-step calculation marking, the point+discussion split, the separate scale/drafting quality band and the brief-as-checklist requirement ticks — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked questions are being added.',
};
