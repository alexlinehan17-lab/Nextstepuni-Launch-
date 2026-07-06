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

// ─────────────── CS8 · The point+discussion split isn’t always 50/50 ───────────────

const CS8: GridSession = {
  mode: 'grid',
  id: 'cs-discussion-outweighs',
  subject: 'construction-studies',
  level: 'higher',
  title: 'Sometimes the discussion is worth more than the point',
  cue: 'Discuss two approaches',
  question: 'A “two approaches to reduce electrical consumption” part is marked 2 for the point + 3 for the discussion, per approach (10 marks). A candidate names two correct approaches — “LED lighting”, “occupancy sensors” — but writes nothing to develop either.',
  questionNote:
    'Scenario authored for this exercise. On this Construction Studies part the split is uneven — the point is worth 2 and the discussion 3 — so on some questions the development is worth MORE than naming the point, not just as much.',
  grid: {
    perPoint: [
      { id: 'a1point', label: 'Approach 1 — point stated', marks: 2 },
      { id: 'a1disc', label: 'Approach 1 — discussion', marks: 3 },
      { id: 'a2point', label: 'Approach 2 — point stated', marks: 2 },
      { id: 'a2disc', label: 'Approach 2 — discussion', marks: 3 },
    ],
    shorthand: 'each approach: point 2 + discussion 3',
    ruleNote:
      'The point and the discussion are separate ticks — but here they are NOT equal: the point is 2, the discussion 3. A bare list of correct approaches banks only 4 of the 10; the larger share lives in the development. Where the split is uneven, the discussion is the bigger prize, so develop it.',
    cite: MS('p.45 (Q9(c) — 2 for point, 3 for discussion)'),
  },
  scripts: [
    {
      id: 'cs8-a',
      label: 'Script A',
      persona: 'Names both, develops neither',
      attempts: [
        {
          id: 'cs8-a-1',
          text: 'Two correct approaches named — “LED lighting”, “occupancy sensors” — with no explanation of how either cuts consumption.',
          key: { a1point: 2, a1disc: 0, a2point: 2, a2disc: 0 },
          keyNote: 'Only 4 of 10. Both points are right and bank their 2, but the discussion tick — worth 3, more than the point itself — sits empty on both. A sentence each on the mechanism (how a sensor kills standby draw, how LEDs cut watts per lumen) would have added the larger half.',
        },
      ],
      embodies: {
        behaviour: 'Lists correct approaches without developing them — forfeiting the discussion tranche, which here outweighs the point.',
        cite: MS('p.45'),
      },
    },
    {
      id: 'cs8-b',
      label: 'Script B',
      persona: 'Point then fuller discussion',
      attempts: [
        {
          id: 'cs8-b-1',
          text: 'Each approach named, then explained — how it works and why it lowers the electricity bill.',
          key: { a1point: 2, a1disc: 3, a2point: 2, a2disc: 3 },
          keyNote: 'Full marks. Each approach is both named and developed, so both the point tick and the larger discussion tick score.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs8',
    rule: 'The split isn’t always 50/50 — sometimes the discussion is worth more than the point.',
    detail:
      'On some discuss parts the point is 2 and the discussion 3, so naming alone banks under half. Read the tariff: where the discussion outweighs the point, the development is the bigger prize — always explain the mechanism.',
    cite: MS('p.45'),
  },
};

// ─────────────── CS9 · Dimensions & insulation position are their own ticks ───────────────

const CS9: GridSession = {
  mode: 'grid',
  id: 'cs-dimensions-insulation',
  subject: 'construction-studies',
  level: 'higher',
  title: 'Dimensions and insulation position are their own marks',
  cue: 'Detail a wall construction',
  question: 'A high-performance wall construction is marked Notes 5 + Sketches 6 + Position of insulation 2 + Dimensions 2 (15 marks). A candidate writes strong notes and draws a clear sketch — but marks no dimensions on it and never shows where the insulation sits.',
  questionNote:
    'Scenario authored for this exercise. On this Construction Studies wall-detail part, stating the dimensions and showing the position of the insulation are separately tariffed ticks — not folded into the note or the sketch — so a good drawing that omits them still loses those marks.',
  grid: {
    perPoint: [
      { id: 'notes', label: 'Notes', marks: 5 },
      { id: 'sketch', label: 'Sketch', marks: 6 },
      { id: 'inspos', label: 'Position of insulation shown', marks: 2 },
      { id: 'dims', label: 'Dimensions stated', marks: 2 },
    ],
    shorthand: 'notes 5 + sketch 6 + insulation position 2 + dimensions 2',
    ruleNote:
      'The dimensions and the position of the insulation are their own ticks, scored separately from the notes and the sketch. A clear labelled sketch with no dimensions marked and no insulation location shown forfeits those 4 marks — and the rubric already requires sizes and dimensions on every drawing. Put the numbers and the insulation on the page.',
    cite: MS('p.40 (Q4(b) — Notes 5, Sketches 6, Position of Insulation 2, Dimensions 2)'),
  },
  scripts: [
    {
      id: 'cs9-a',
      label: 'Script A',
      persona: 'Good detail, no dimensions or insulation position',
      attempts: [
        {
          id: 'cs9-a-1',
          text: 'Strong written notes and a clear sketch of the wall build-up — but no dimensions marked and no indication of where the insulation sits.',
          key: { notes: 5, sketch: 6, inspos: 0, dims: 0 },
          keyNote: 'Eleven of fifteen. The notes and sketch score in full, but the dimensions tick and the insulation-position tick are separate marks and both are empty. Adding leader-line dimensions and hatching the insulation layer — seconds of work the drawing already invites — banks the last four.',
        },
      ],
      embodies: {
        behaviour: 'Details a wall well but omits dimensions and insulation position — forfeiting their separate ticks.',
        cite: MS('p.40'),
      },
    },
    {
      id: 'cs9-b',
      label: 'Script B',
      persona: 'Everything on the drawing',
      attempts: [
        {
          id: 'cs9-b-1',
          text: 'The same notes and sketch, now with dimensions marked and the insulation clearly positioned in the build-up.',
          key: { notes: 5, sketch: 6, inspos: 2, dims: 2 },
          keyNote: 'Full marks. Every tick — including the separately-marked dimensions and insulation position — has something to score against.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs9',
    rule: 'Dimensions and the position of the insulation are marked separately — put them on the drawing.',
    detail:
      'On wall-detail parts, stating dimensions and showing where the insulation sits are their own ticks (here 2 + 2), not part of the note or sketch marks. A good drawing that omits them loses those marks; always dimension the detail and locate the insulation.',
    cite: MS('p.40'),
  },
};

// ─────────────── CS10 · On the wiring layout, colour is 3/4 of the annotation ───────────────

const CS10: GridSession = {
  mode: 'grid',
  id: 'cs-cable-colour',
  subject: 'construction-studies',
  level: 'higher',
  title: 'On a wiring layout, colour is three-quarters of the annotation',
  cue: 'Draw the wiring layout',
  question: 'A wiring-layout question annotates the cabling with a 4-mark tick split Cable size (1) + colour (3). A candidate draws the live, neutral and earth runs correctly and notes the cable size — but colour-codes nothing.',
  questionNote:
    'Scenario authored for this exercise. On the Construction Studies wiring layout the cabling’s annotation mark is split cable size (1) and colour (3) — so the colour-coding of the conductors carries three times the marks of the size note.',
  grid: {
    perPoint: [
      { id: 'size', label: 'Cable size noted', marks: 1 },
      { id: 'colour', label: 'Cable colours shown (live / neutral / earth)', marks: 3 },
    ],
    shorthand: 'cable annotation: size 1 + colour 3',
    ruleNote:
      'The cabling annotation isn’t one mark — it’s split, and the colour-coding is worth three times the size note. Drawing the runs and writing the cable size banks 1 of the 4; identifying each conductor by colour (brown live, blue neutral, green/yellow earth) banks the other 3. Colour the conductors.',
    cite: MS('p.45 (Q9(a) — Cable size (1) and colour (3))'),
  },
  scripts: [
    {
      id: 'cs10-a',
      label: 'Script A',
      persona: 'Runs drawn, no colour-coding',
      attempts: [
        {
          id: 'cs10-a-1',
          text: 'Live, neutral and earth runs drawn correctly and the cable size noted — but no colours identified on the conductors.',
          key: { size: 1, colour: 0 },
          keyNote: 'One of four on the annotation. The size note scores, but the colour tick — three times as valuable — is empty. Labelling brown/blue/green-yellow against the three conductors is a few words for three marks.',
        },
      ],
      embodies: {
        behaviour: 'Notes cable size but omits the colour-coding — losing the larger three-quarters of the annotation mark.',
        cite: MS('p.45'),
      },
    },
    {
      id: 'cs10-b',
      label: 'Script B',
      persona: 'Size and colours both given',
      attempts: [
        {
          id: 'cs10-b-1',
          text: 'The same layout with the cable size noted and each conductor colour-identified — brown live, blue neutral, green/yellow earth.',
          key: { size: 1, colour: 3 },
          keyNote: 'Full annotation marks. Size and colour are separate ticks and both are satisfied.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs10',
    rule: 'On the wiring layout, colour-coding the conductors is worth three times the cable size.',
    detail:
      'The cabling annotation splits cable size (1) + colour (3): identifying each conductor by colour carries three-quarters of the mark. Always colour-code live, neutral and earth — it’s the bigger, easily-won share.',
    cite: MS('p.45'),
  },
};

// ─────────────── CS11 · The scheme is illustrative, not a closed answer key ───────────────

const CS11: GridSession = {
  mode: 'grid',
  id: 'cs-not-exhaustive',
  subject: 'construction-studies',
  level: 'common',
  title: 'You’re not matching a fixed answer key',
  cue: 'State two relevant points',
  question: 'A “state two relevant points” part carries a model list in the scheme — but every list ends “Any other relevant points”, and the scheme’s standing note says model answers are “not exclusive or exhaustive”. A candidate gives two correct, relevant points that don’t appear word-for-word on the model list. Do they score?',
  questionNote:
    'Scenario authored for this exercise. The Construction Studies scheme states its model notes are illustrative, not a closed key — a valid, relevant point that isn’t on the printed list is credited; only irrelevant or wrong points score nothing.',
  grid: {
    perPoint: [
      { id: 'p1', label: 'Point 1 — relevant and correct', marks: 3 },
      { id: 'p2', label: 'Point 2 — relevant and correct', marks: 3 },
    ],
    shorthand: 'each relevant point: 3 (on-list or not)',
    ruleNote:
      'The examiner marks on merit against the scheme’s standing note, not against a closed list. A correct, relevant point that isn’t printed still earns its mark; what fails is a point that’s irrelevant or wrong. So never bin a good point because you’re unsure it’s “the” answer — and never pad with waffle hoping it lands.',
    cite: MS('p.3 (standing note — model answers not exclusive or exhaustive; “Any other relevant points”)'),
  },
  scripts: [
    {
      id: 'cs11-a',
      label: 'Script A',
      persona: 'Valid points, not on the printed list',
      attempts: [
        {
          id: 'cs11-a-1',
          text: 'Two correct, on-topic points that happen not to appear verbatim in the scheme’s model answer.',
          key: { p1: 3, p2: 3 },
          keyNote: 'Full marks. The scheme’s model notes are explicitly illustrative, not a closed key — a relevant, correct point is credited whether or not it’s printed. Don’t self-censor a good answer for fear it isn’t “on the list”.',
        },
      ],
      embodies: {
        behaviour: 'Gives valid points absent from the model list — which the scheme still credits on merit.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'cs11-b',
      label: 'Script B',
      persona: 'Off-topic filler',
      attempts: [
        {
          id: 'cs11-b-1',
          text: 'Two vague, off-topic statements that don’t actually answer what was asked.',
          key: { p1: 0, p2: 0 },
          keyNote: 'Nothing. “Not exhaustive” credits relevant alternatives — it does not rescue irrelevant filler. The test is relevance and correctness, not whether the words match the scheme.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs11',
    rule: 'The scheme is illustrative, not a closed key — any relevant, correct point scores.',
    detail:
      'Model answers are “not exclusive or exhaustive” and every list ends “any other relevant points”. A valid point that isn’t printed still earns its mark; only irrelevant or wrong answers score nothing. Answer on merit — don’t bin good points, don’t pad with filler.',
    cite: MS('p.3'),
  },
};

// ─────────────── CS12 · Any valid calculation method is accepted ───────────────

const CS12: ScaleSession = {
  mode: 'scale',
  id: 'cs-alt-method',
  subject: 'construction-studies',
  level: 'higher',
  title: 'Your own valid method is fine',
  cue: 'Calculate — any valid method',
  question: 'The 15-mark “cost of annual heat loss” calculation has a model step layout, but the scheme prints a single-formula “Alternative method” reaching the same €76.34 and states “Alternative calculation methods acceptable”. A candidate ignores the scheme’s step layout and works the whole thing through one combined formula, fully shown, landing on the right figure. What can they score?',
  questionNote:
    'Scenario authored for this exercise. The Construction Studies scheme explicitly accepts alternative calculation methods and even prints a one-formula route to the same answer — so a valid method, fully worked, is not penalised for not matching the scheme’s layout.',
  scale: {
    name: 'Heat-loss cost · /15',
    levels: ladder([3, 9, 15]),
    notes: [
      'The scheme prints a step layout AND a single-formula alternative, both reaching €76.34.',
      '“Alternative calculation methods acceptable” — the method is not prescribed.',
      'What’s marked is a valid route, fully shown, to the correct answer — not conformity to the scheme’s steps.',
    ],
    cite: MS('p.20 (Q5(b) alternative single-formula method), p.21 (“Alternative calculation methods acceptable”)'),
  },
  scripts: [
    {
      id: 'cs12-a',
      label: 'The answer',
      persona: 'Non-scheme method, fully shown',
      work: ['One combined formula: U-value × Area × ΔT × Time × Cost ÷ (calorific value × 1000)', '= €76.34 — every substitution written out'],
      keyLevelId: 'm15',
      keyNote:
        'Full marks. The scheme accepts alternative methods and prints this very route; because every substitution is on the page and the answer is right, the non-standard method loses nothing. The rule that bites is showing the working (as in the per-step U-value) — not which valid method you choose.',
      embodies: {
        behaviour: 'Uses a valid non-scheme method, fully worked — which the scheme explicitly credits.',
        cite: MS('p.21'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs12',
    rule: 'Any valid method scores — as long as you show every substitution.',
    detail:
      'The scheme states “alternative calculation methods acceptable” and prints more than one route to the same answer. A non-standard but valid method, fully worked to the right figure, is not penalised. Don’t panic about matching the scheme’s layout — show your working and the method is yours to choose.',
    cite: MS('p.21'),
  },
};

// ─────────────── CS13 · “Three reasons” means three whole mark-blocks ───────────────

const CS13: GridSession = {
  mode: 'grid',
  id: 'cs-reasons-count',
  subject: 'construction-studies',
  level: 'higher',
  title: '“Three reasons” means three whole mark-blocks',
  cue: 'Give three reasons',
  question: 'A “give three reasons for your proposed layout” part is marked Reason 1 (6) + Reason 2 (6) + Reason 3 (6) — 18 marks. A candidate justifies the layout with two strong, well-argued reasons and stops there.',
  questionNote:
    'Scenario authored for this exercise. Where a Construction Studies part asks for a set number of reasons, each reason is a full, equally-weighted mark-block — so giving fewer than asked forfeits a whole block however good the ones given are.',
  grid: {
    perPoint: [
      { id: 'r1', label: 'Reason 1', marks: 6 },
      { id: 'r2', label: 'Reason 2', marks: 6 },
      { id: 'r3', label: 'Reason 3', marks: 6 },
    ],
    shorthand: 'three reasons × 6 each',
    ruleNote:
      'Each reason is its own 6-mark block and the question fixes the count at three. Two brilliant reasons cannot overflow into the third block — there is no bonus for depth on reason two. Stopping at two caps the part at 12 of 18; the third reason, even a modest one, is a whole extra six.',
    cite: MS('p.39 (Q3(b) — Reason 1 / 2 / 3, 6 each)'),
  },
  scripts: [
    {
      id: 'cs13-a',
      label: 'Script A',
      persona: 'Two strong reasons, stops short',
      attempts: [
        {
          id: 'cs13-a-1',
          text: 'Two well-argued reasons for the layout — and no third.',
          key: { r1: 6, r2: 6, r3: 0 },
          keyNote: 'Twelve of eighteen. The two reasons score in full, but the third block is empty and nothing the first two do can fill it. A third reason — daylight, circulation, privacy, anything relevant — banks another six for a line of writing.',
        },
      ],
      embodies: {
        behaviour: 'Gives fewer reasons than the question asks for — forfeiting a whole mark-block.',
        cite: MS('p.39'),
      },
    },
    {
      id: 'cs13-b',
      label: 'Script B',
      persona: 'Three reasons, as asked',
      attempts: [
        {
          id: 'cs13-b-1',
          text: 'Three distinct reasons for the layout, each briefly justified.',
          key: { r1: 6, r2: 6, r3: 6 },
          keyNote: 'Full marks. The answer supplies exactly the count the question fixed, so all three blocks score.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs13',
    rule: 'When a question asks for N reasons, each is a full mark-block — give all N.',
    detail:
      '“Three reasons” is three separate 6-mark blocks; extra depth on one cannot pay for a missing one. Always produce the exact count the question names — the last item is a whole block of marks for a line of writing.',
    cite: MS('p.39'),
  },
};

// ─────────────── CS14 · Half the coursework marks are the folio ───────────────

const CS14: GridSession = {
  mode: 'grid',
  id: 'cs-coursework-folio',
  subject: 'construction-studies',
  level: 'common',
  title: 'Half the coursework marks are the folio, not the making',
  cue: 'Submit the coursework',
  question: 'The Practical Coursework (150 marks) is marked under four headings — A Planning 40, B Report 35, C Manipulative Skills 40, D Completion 35. A candidate builds a superb artefact and finishes it beautifully, but submits almost no planning documentation and no report folio.',
  questionNote:
    'Scenario authored for this exercise. Construction Studies coursework splits across four headings where the written folio — Planning plus Report — is worth 75 of the 150 marks, as much as the making itself.',
  grid: {
    perPoint: [
      { id: 'planning', label: 'A · Planning of Project', marks: 40 },
      { id: 'report', label: 'B · Report', marks: 35 },
      { id: 'skills', label: 'C · Manipulative Skills', marks: 40 },
      { id: 'completion', label: 'D · Completion of Project', marks: 35 },
    ],
    shorthand: 'Planning 40 + Report 35 + Manipulative 40 + Completion 35 = 150',
    ruleNote:
      'The folio — Planning (40) and Report (35) — is 75 of the 150 marks, exactly half, and it is scored independently of the artefact. A brilliant object with no research, no design development and no written report banks only the making half; the planning and report headings score against documents, not the piece.',
    cite: MS('p.63 (Practical Coursework Form A — A Planning 40, B Report 35, C Manipulative Skills 40, D Completion 35)'),
  },
  scripts: [
    {
      id: 'cs14-a',
      label: 'Script A',
      persona: 'Great maker, no folio',
      attempts: [
        {
          id: 'cs14-a-1',
          text: 'An excellently made and well-finished artefact — but no planning research or design development submitted, and no written report.',
          key: { planning: 0, report: 0, skills: 40, completion: 35 },
          keyNote: 'Seventy-five of 150. The making headings score in full, but Planning and Report are marked against a folio that isn’t there, so half the marks are gone. The write-up — research, annotated design development, sequence of manufacture, appraisal — is worth as much as the object.',
        },
      ],
      embodies: {
        behaviour: 'Makes a strong artefact but neglects the planning and report folio — forfeiting half the coursework marks.',
        cite: MS('p.63'),
      },
    },
    {
      id: 'cs14-b',
      label: 'Script B',
      persona: 'Folio and artefact both delivered',
      attempts: [
        {
          id: 'cs14-b-1',
          text: 'The same artefact, with a full planning and design-development folio and a complete written report.',
          key: { planning: 40, report: 35, skills: 40, completion: 35 },
          keyNote: 'Full marks. Every heading has something to score against because the folio is delivered alongside the making.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cs14',
    rule: 'Half the coursework marks are the folio — plan and report as hard as you make.',
    detail:
      'Coursework splits Planning 40 + Report 35 + Manipulative 40 + Completion 35; the written folio is 75 of 150, scored against documents not the object. A great artefact with no folio caps at half — invest equally in research, design development and the report.',
    cite: MS('p.63'),
  },
};

// ─────────────── CS15 · The practical must be hand-made — machinery halves the procedure ───────────────

const CS15: ScaleSession = {
  mode: 'scale',
  id: 'cs-machinery-penalty',
  subject: 'construction-studies',
  level: 'common',
  title: 'Use a machine, lose half the procedure',
  cue: 'Hand-produce the artefact',
  question: 'The Practical Test artefact “is to be hand produced by candidates without the assistance of machinery”. Where an examiner sees evidence of machine work on a procedure, that component “is marked out of 50% of the marks available for that procedure”. A candidate cuts a 12-mark box-dovetail joint cleanly — but with clear evidence of machine assistance. What is the ceiling for that joint?',
  questionNote:
    'Scenario authored for this exercise. The Construction Studies Practical Test requires hand production; a machinery penalty caps any machine-assisted procedure at 50% of its marks (a battery screwdriver being the one allowed exception).',
  scale: {
    name: 'Box-dovetail joint · /12',
    levels: [
      { id: 'penalised', label: 'Machine-assisted — capped at 50%', annotation: '6', marks: 6 },
      { id: 'hand', label: 'Hand-produced — full', annotation: '12', marks: 12 },
    ],
    notes: [
      'The artefact must be hand produced; a battery-powered screwdriver is the only allowed machine.',
      'Evidence of machinery on a procedure caps that procedure at 50% of its marks.',
      'The penalty is on the procedure, not the whole artefact — but a clean machine-cut joint still loses half.',
    ],
    cite: MS('p.49 (Practical Test note — hand-produced; machine-assisted procedure marked out of 50%)'),
  },
  scripts: [
    {
      id: 'cs15-a',
      label: 'The joint',
      persona: 'Clean cut, machine-assisted',
      work: ['A well-fitting box-dovetail joint', 'Clear evidence of machine assistance in cutting it'],
      keyLevelId: 'penalised',
      keyNote:
        'Six of twelve. Quality doesn’t rescue it — the artefact must be hand produced, and any procedure showing machine work is capped at 50% however clean the result. Only the same joint cut by hand reaches the full 12. Leave the machines (bar the allowed battery screwdriver) and work it by hand.',
      embodies: {
        behaviour: 'Produces a clean joint with machine assistance — capping the procedure at half its marks.',
        cite: MS('p.49'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cs15',
    rule: 'The practical must be hand-made — machine evidence caps that procedure at 50%.',
    detail:
      'The Practical Test artefact is “to be hand produced… without the assistance of machinery”; a machine-assisted procedure is “marked out of 50% of the marks available for that procedure”. Only a battery screwdriver is allowed. A clean but machine-cut component still loses half — work by hand.',
    cite: MS('p.49'),
  },
};

export const CONSTRUCTION_CHAIR: ChairSubject = {
  id: 'construction-studies',
  label: 'Construction Studies',
  tagline: 'Label every element, sketch when asked, show every layer, develop every point — and give the exact count asked.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CS1, CS2, CS3, CS4, CS5, CS6, CS7, CS8, CS9, CS10, CS11, CS12, CS13, CS14, CS15],
  sources: [
    { label: 'SEC LC Construction Studies HL marking scheme 2025 (examiner-reports/construction-studies/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — the element draw+annotation split, the note+sketch split, per-step calculation marking, the point+discussion split (including where the discussion outweighs the point), separately-tariffed dimensions/insulation/cable-colour ticks, the scale/drafting quality band, the brief-as-checklist and required-count rules, the illustrative-not-exhaustive credit and acceptance of alternative methods, plus the Practical Test hand-production penalty and the coursework folio weighting — which apply at both Higher and Ordinary level (the practical/coursework rules are Common Level). Verified against the 2025 Higher Level scheme; level-specific worked questions are being added.',
};
