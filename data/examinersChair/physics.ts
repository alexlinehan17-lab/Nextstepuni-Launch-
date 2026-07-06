/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Physics (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the numerical-answer granule ladder, the one-mark unit
 * deduction, per-occurrence slip deduction with error-carried-forward, the
 * `//` mutually-exclusive-method rule, and the part-marked-definition
 * convention) is the real SEC system, cited to:
 *  - SEC LC Physics HL marking scheme 2025 —
 *    examiner-reports/physics/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Physics HL marking scheme 2025, ${p}` });
const MS23 = (p: string) => ({ label: `SEC Physics HL marking scheme 2023, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── Phy1 · Marked in granules ───────────────

const PHY1: GridSession = {
  mode: 'grid',
  id: 'phy-granules',
  subject: 'physics',
  level: 'common',
  title: 'The formula is worth a mark',
  cue: 'Calculate',
  question: 'Calculate the speed of a wave of frequency 512 Hz and wavelength 0.65 m. [The candidate wrote: “v = f λ” and then stopped — no numbers.]',
  questionNote:
    'Question authored for this exercise. Physics numerical answers are marked as a ladder of independent granules — formula, substitution, answer — each scoring separately, typically 3 marks each.',
  grid: {
    perPoint: [
      { id: 'formula', label: 'Relevant formula quoted', marks: 3 },
      { id: 'sub', label: 'Substitution / working', marks: 3 },
      { id: 'answer', label: 'Correct final answer', marks: 3 },
    ],
    shorthand: '3 granules × 3m',
    ruleNote:
      'Each granule is scored on its own. Quoting the right formula banks 3 marks even if you never plug in a number — so an “I don’t know where to start” blank and a written formula are worlds apart on the mark sheet.',
    cite: MS('p.6–8 (numerical granule ladder)'),
  },
  scripts: [
    {
      id: 'phy1-a',
      label: 'Script A',
      persona: 'Formula, then froze',
      attempts: [
        {
          id: 'phy1-a-1',
          text: 'v = f λ',
          key: { formula: 3, sub: 0, answer: 0 },
          keyNote: 'The relevant formula is its own granule — 3 marks banked, even with no numbers. A blank would have scored 0. Always write the equation first.',
        },
      ],
      embodies: {
        behaviour: 'Writes only the relevant formula — which banks its own granule.',
        cite: MS('p.6'),
      },
    },
    {
      id: 'phy1-b',
      label: 'Script B',
      persona: 'Full working',
      attempts: [
        {
          id: 'phy1-b-1',
          text: 'v = f λ = 512 × 0.65 = 332.8 m s⁻¹',
          key: { formula: 3, sub: 3, answer: 3 },
          keyNote: 'Formula, substitution and a correct answer with a unit — all three granules. 9/9.',
        },
      ],
    },
    {
      id: 'phy1-c',
      label: 'Script C',
      persona: 'Right formula, arithmetic slip',
      attempts: [
        {
          id: 'phy1-c-1',
          text: 'v = f λ = 512 × 0.65 = 233 m s⁻¹',
          key: { formula: 3, sub: 3, answer: 0 },
          keyNote: 'Formula and substitution granules are secure (6 marks); only the final arithmetic is wrong (512 × 0.65 = 332.8, not 233). You lose the answer granule, not the whole question — which is exactly why showing the substitution protects you.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-phy1',
    rule: 'Every numerical answer is a ladder — write each rung.',
    detail:
      'Physics calculations score in granules: formula, substitution, answer. Quoting the formula banks a mark on its own, and showing substitution protects those marks when the arithmetic slips. Never jump straight to a bare number.',
    cite: MS('p.6'),
  },
};

// ─────────────── Phy2 · The one-mark unit ───────────────

const PHY2: ScaleSession = {
  mode: 'scale',
  id: 'phy-unit',
  subject: 'physics',
  level: 'common',
  title: 'The mark you forget to write',
  cue: 'Calculate',
  question: 'A calculation is completely correct — right formula, right substitution, right number: 4.2. But the candidate writes no unit after it. The answer was worth 9 marks. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The general instructions state that omitting (or giving incorrect) units in a final answer costs one mark, unless otherwise indicated.',
  scale: {
    name: 'Unit omission',
    levels: ladder([8, 9]),
    notes: [
      'General rule: “For omission of appropriate units (or for incorrect units) in final answers, one mark is deducted.”',
      'It is a flat one-mark deduction — the rest of the working is untouched.',
      'So a flawless 9-mark answer with no unit scores 8, not 0.',
    ],
    cite: MS('p.3 (instruction 6, units)'),
  },
  scripts: [
    {
      id: 'phy2-a',
      label: 'The answer',
      persona: 'Right number, no unit',
      work: ['… = 4.2', '(no unit written)'],
      keyLevelId: 'm8',
      keyNote:
        '8 marks — a single mark deducted for the missing unit, not a wipeout. But it is a mark, and it is the easiest one on the paper to keep. Get into the habit of writing the unit the instant you write the number.',
      embodies: {
        behaviour: 'Omits the unit on a correct final answer — a one-mark deduction.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy2',
    rule: 'A missing unit is one mark — never zero, never free.',
    detail:
      'Omitting or mis-writing the unit on a final answer costs exactly one mark. It won’t sink the question, but it is the cheapest mark to protect — write the unit every single time.',
    cite: MS('p.3'),
  },
};

// ─────────────── Phy3 · A slip is one mark ───────────────

const PHY3: ScaleSession = {
  mode: 'scale',
  id: 'phy-slip',
  subject: 'physics',
  level: 'common',
  title: 'Slip once, carry on',
  cue: 'Calculate',
  question: 'Halfway through a multi-step calculation the candidate makes one arithmetic slip, then uses that wrong value correctly through every remaining step, reaching a consistent final answer. The full calculation is worth 12 marks. Roughly what should it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme deducts one mark each time an arithmetical slip occurs; downstream work built on the slipped value still earns its marks (error carried forward).',
  scale: {
    name: 'One slip, consistent finish',
    levels: ladder([4, 11, 12]),
    notes: [
      'Rule: “Each time an arithmetical slip occurs … one mark is deducted.”',
      'Error carried forward: steps that correctly use the slipped value still score.',
      'So one slip in an otherwise perfect 12-mark answer costs ~1 mark, not the question.',
      'Abandoning the answer after the slip forfeits all the method marks that follow.',
    ],
    cite: MS('p.3 (instruction 8, arithmetical slip / ECF)'),
  },
  scripts: [
    {
      id: 'phy3-a',
      label: 'The answer',
      persona: 'One slip, keeps going',
      work: [
        'Correct method throughout.',
        'One arithmetic slip in an intermediate step.',
        'Uses that value correctly to a consistent final answer.',
      ],
      keyLevelId: 'm11',
      keyNote:
        '~11 of 12 — one mark for the slip, everything after it credited by error-carried-forward. The worst thing you can do here is panic and scribble it all out: that forfeits the method marks you had already earned. A slip is one mark; a blank page is all of them.',
      embodies: {
        behaviour: 'Makes one slip but perseveres consistently — the marks-carried-forward case, not a wipeout.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy3',
    rule: 'A slip costs one mark — don’t abandon the answer.',
    detail:
      'One arithmetic slip is a single-mark deduction, and later steps that use the slipped value still score (error carried forward). Keep going to a consistent finish; restarting or scrubbing out forfeits marks you already banked.',
    cite: MS('p.3'),
  },
};

// ─────────────── Phy4 · A definition is marked in parts ───────────────

const PHY4: GridSession = {
  mode: 'grid',
  id: 'phy-definition-parts',
  subject: 'physics',
  level: 'common',
  title: 'The “per unit” is worth marks',
  cue: 'Explain / Define',
  question:
    'Explain what is meant by resistance. The scheme marks this definition as “[4 + 2]”: the core relationship (voltage, or R = V/I) is worth 4, and the qualifying phrase “per unit current” is a separate 2. A candidate writes “Resistance is the voltage across a component” and stops.',
  questionNote:
    'Question authored for this exercise. The part-marked definition is the real SEC convention — the resistance definition is printed as “voltage // R = V/I” + “per unit current // notation [4 + 2]”, so the qualifier carries its own marks.',
  grid: {
    perPoint: [
      { id: 'core', label: 'Core relationship (voltage / R = V/I)', marks: 4 },
      { id: 'perunit', label: 'The “per unit current” qualifier', marks: 2 },
    ],
    shorthand: 'definition · [4 + 2]',
    ruleNote:
      'Physics definitions are marked in parts. Naming the quantities scores the core marks, but the “per unit …” phrase (or the ratio it implies) is a separate, forfeitable component. Drop it and you leave those marks behind — a definition is not complete until the qualifier is there.',
    cite: MS('p.16–17 (definition part-marking, [4 + 2])'),
  },
  scripts: [
    {
      id: 'phy4-a',
      label: 'Script A',
      persona: 'Half the definition',
      attempts: [
        {
          id: 'phy4-a-1',
          text: '“Resistance is the voltage across a component.”',
          key: { core: 4, perunit: 0 },
          keyNote:
            'The core quantity is there (4), but the definition is only half-built — “per unit current” (the ratio to the current) is a separate 2-mark component and it’s missing. 4 of 6. The qualifier is not optional colour; it is where the last marks live.',
        },
      ],
      embodies: {
        behaviour: 'Gives the core of a definition but omits the separately-marked “per unit” qualifier.',
        cite: MS('p.16'),
      },
    },
    {
      id: 'phy4-b',
      label: 'Script B',
      persona: 'Full definition',
      attempts: [
        {
          id: 'phy4-b-1',
          text: '“Resistance is the voltage across a component per unit current through it (R = V/I).”',
          key: { core: 4, perunit: 2 },
          keyNote:
            'Both parts: the core relationship and the “per unit current” qualifier. Full 6 marks. The ratio form (R = V/I) carries the same meaning — either way, the complete definition is what scores.',
        },
      ],
    },
    {
      id: 'phy4-c',
      label: 'Script C',
      persona: 'Vague at the qualifier',
      attempts: [
        {
          id: 'phy4-c-1',
          text: '“Resistance is the voltage across a component, and it depends on the current.”',
          key: { core: 4, perunit: 0 },
          keyNote:
            'The core quantity scores (4), and this time there’s a gesture at the current — but “depends on the current” is not the “per unit current” ratio, so the 2-mark qualifier is still unearned. That component is all-or-nothing: attempting it vaguely scores the same as leaving it out. 4 of 6. Name the ratio (per unit current, or R = V/I) or the marks stay on the table.',
        },
      ],
      embodies: {
        behaviour: 'Gestures at the qualifier vaguely (“depends on the current”) without stating the ratio — the all-or-nothing part scores 0.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy4',
    rule: 'Finish the definition — the “per unit” carries its own marks.',
    detail:
      'Physics definitions are part-marked: the core quantities score some marks, and the qualifier — “per unit …”, or the ratio it implies — scores the rest. Always state the full relationship; a half-definition banks only half the marks.',
    cite: MS('p.16'),
  },
};

// ─────────────── Phy5 · “Any two” from a list ───────────────

const PHY5: GridSession = {
  mode: 'grid',
  id: 'phy-any-two',
  subject: 'physics',
  level: 'common',
  title: 'Give the number they asked for',
  cue: 'State two',
  question:
    'State two principal external forces that should be minimised in a momentum experiment. The scheme marks this “frictional, gravitational [3 + 3]” — each valid force is its own 3-mark granule, and only two are asked for.',
  questionNote:
    'Question authored for this exercise. “State two …” list items are marked as independent granules drawn from a set of acceptable answers — you earn a granule for each valid, DISTINCT point up to the number the question asks for.',
  grid: {
    perPoint: [
      { id: 'point1', label: 'First valid force', marks: 3 },
      { id: 'point2', label: 'Second valid (distinct) force', marks: 3 },
    ],
    shorthand: 'any two · [3 + 3]',
    ruleNote:
      'Each valid point banks its own granule, up to the two asked for. A wrong point earns nothing — on a plain “state two” list there is no deduction for it — but it cannot rescue a missing right one, and repeating the same point in different words never earns the second granule.',
    cite: MS('p.7 (Q2 “state two … [3 + 3]”)'),
  },
  scripts: [
    {
      id: 'phy5-a',
      label: 'Script A',
      persona: 'Two clean points',
      attempts: [
        {
          id: 'phy5-a-1',
          text: 'Frictional force and gravitational force.',
          key: { point1: 3, point2: 3 },
          keyNote: 'Two valid, distinct forces — both granules. 6/6. Exactly two were asked for and exactly two were given.',
        },
      ],
    },
    {
      id: 'phy5-b',
      label: 'Script B',
      persona: 'One right, one wrong',
      attempts: [
        {
          id: 'phy5-b-1',
          text: 'Frictional force and magnetic force.',
          key: { point1: 3, point2: 0 },
          keyNote:
            'Friction is valid (3); “magnetic force” is not one of the forces acting, so it scores nothing. 3/6. The wrong answer does not cost you a mark here, but it does not earn one either — one good point is worth one granule, not two.',
        },
      ],
      embodies: {
        behaviour: 'Pads a “state two” with an invalid extra point — which earns nothing (no deduction, but no credit).',
        cite: MS('p.7'),
      },
    },
    {
      id: 'phy5-c',
      label: 'Script C',
      persona: 'Same point twice',
      attempts: [
        {
          id: 'phy5-c-1',
          text: 'Friction between the wheels and the track, and the frictional drag on the trolley.',
          key: { point1: 3, point2: 0 },
          keyNote:
            'Both halves are the same point — friction — reworded. The examiner credits it once (3); the second granule needs a DISTINCT force. 3/6. “Two” means two different things, not one thing said twice.',
        },
      ],
      embodies: {
        behaviour: 'Restates a single valid point in two forms, hoping to earn both granules — the duplicate scores 0.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy5',
    rule: 'Answer the number asked — with that many DISTINCT points.',
    detail:
      '“State two” is two granules: each valid, distinct point banks its own marks up to the number requested. A wrong extra earns nothing (though a plain list won’t deduct for it), and repeating one point in new words never fills the second slot. Give exactly as many genuinely different points as the question asks.',
    cite: MS('p.7'),
  },
};

// ─────────────── Phy6 · A graph is marked in granules ───────────────

const PHY6: GridSession = {
  mode: 'grid',
  id: 'phy-graph',
  subject: 'physics',
  level: 'common',
  title: 'The line of best fit is its own mark',
  cue: 'Draw a graph',
  question:
    'Draw a suitable graph from a table of readings. The scheme marks the graph in separate granules — “values … [3] / axes labelled [3] / points plotted [3] / line of best fit [3]” — and a separate general rule deducts one mark for an inappropriate scale.',
  questionNote:
    'Question authored for this exercise. Graphs are marked as independent granules (values, labelled axes, plotted points, line of best fit); the general instructions add a one-mark deduction for an inappropriate scale, and any slope taken afterwards must be read from the best-fit line, not a pair of raw data points.',
  grid: {
    perPoint: [
      { id: 'values', label: 'Derived values calculated', marks: 3 },
      { id: 'axes', label: 'Axes labelled (with a suitable scale)', marks: 3 },
      { id: 'points', label: 'Points plotted', marks: 3 },
      { id: 'bestfit', label: 'Line of best fit drawn', marks: 3 },
    ],
    shorthand: 'graph · [3 + 3 + 3 + 3]',
    ruleNote:
      'The line of best fit is a granule in its own right — joining the dots dot-to-dot, or plotting points and stopping, forfeits it. A separate general rule docks one mark for an inappropriate scale, and when a later part asks for a slope it must be taken from the best-fit line, not two raw readings.',
    cite: MS('p.9 (Q4 graph granules); p.3 (instruction 7, inappropriate scale)'),
  },
  scripts: [
    {
      id: 'phy6-a',
      label: 'Script A',
      persona: 'Textbook graph',
      attempts: [
        {
          id: 'phy6-a-1',
          text: 'Calculates sin i and sin r, labels both axes on a sensible scale, plots every point, then draws a single straight line of best fit through them.',
          key: { values: 3, axes: 3, points: 3, bestfit: 3 },
          keyNote: 'All four granules — values, labelled axes, plotted points, best-fit line. 12/12, and the scale is sensible so there is no deduction.',
        },
      ],
    },
    {
      id: 'phy6-b',
      label: 'Script B',
      persona: 'Joins the dots',
      attempts: [
        {
          id: 'phy6-b-1',
          text: 'Values, labelled axes and all points correct — then connects the points with short straight segments dot-to-dot instead of one best-fit line.',
          key: { values: 3, axes: 3, points: 3, bestfit: 0 },
          keyNote:
            'Values, axes and points are all there (9), but a dot-to-dot zig-zag is not a line of best fit, so that granule is lost. 9/12. The best-fit line is a separate mark — draw one straight line that balances the scatter, never join the points.',
        },
      ],
      embodies: {
        behaviour: 'Plots correctly but joins the points dot-to-dot rather than drawing a line of best fit — forfeiting that granule.',
        cite: MS('p.9'),
      },
    },
    {
      id: 'phy6-c',
      label: 'Script C',
      persona: 'Unlabelled axes',
      attempts: [
        {
          id: 'phy6-c-1',
          text: 'Correct values, points plotted and a good line of best fit — but neither axis carries a label or quantity.',
          key: { values: 3, axes: 0, points: 3, bestfit: 3 },
          keyNote:
            'The plotting and the best-fit line are fine (9), but unlabelled axes forfeit their own granule — the examiner cannot tell what was plotted against what. 9/12. Label both axes with the quantity every single time.',
        },
      ],
      embodies: {
        behaviour: 'Draws a correct graph but leaves the axes unlabelled — losing the labelled-axes granule.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy6',
    rule: 'A graph is four marks, not one — and the line of best fit is one of them.',
    detail:
      'Graphs are marked in granules: derived values, labelled axes, plotted points and a line of best fit each score separately. Joining the dots or leaving axes unlabelled forfeits a whole granule, an inappropriate scale costs a further mark, and any slope must come from the best-fit line, not two raw points.',
    cite: MS('p.9'),
  },
};

// ─────────────── Phy7 · Diagrams: label everything, invent nothing ───────────────

const PHY7: ScaleSession = {
  mode: 'scale',
  id: 'phy-diagram',
  subject: 'physics',
  level: 'common',
  title: 'Label everything, invent nothing',
  cue: 'Draw a labelled diagram',
  question:
    'Draw a labelled vector diagram of the four forces on a car driving up a hill. The scheme scores the four forces “[2 + 2 + 2 + 1]”, then adds “[–1 mark if no label present on diagram]” and “[–1 mark for additional incorrect forces]”. A perfect diagram is worth 7. How do the two deductions bite?',
  questionNote:
    'Scenario authored for this exercise. The vector-diagram convention is real: each correct force is a granule, an unlabelled diagram loses one mark overall, and each additional incorrect force loses a mark — so guessing extra forces can actively cost you.',
  scale: {
    name: 'Vector diagram [2 + 2 + 2 + 1]',
    levels: ladder([5, 6, 7]),
    notes: [
      'Rule: four correct forces score “[2 + 2 + 2 + 1]” = 7 marks.',
      '“[–1 mark if no label present on diagram]” — an unlabelled diagram loses one mark overall.',
      '“[–1 mark for additional incorrect forces]” — each invented extra force costs a mark.',
      'So a correct-but-unlabelled diagram scores 6; a fully-labelled diagram padded with one made-up force also scores 6; do both and it drops to 5.',
    ],
    cite: MS('p.11 (Q6(b) vector diagram, label / extra-force deductions)'),
  },
  scripts: [
    {
      id: 'phy7-a',
      label: 'Script A',
      persona: 'All four, labelled, nothing extra',
      work: [
        'Applied force, frictional force, gravitational force and normal/reaction force.',
        'Every arrow labelled. No other forces drawn.',
      ],
      keyLevelId: 'm7',
      keyNote:
        '7/7 — four correct forces, all labelled, nothing invented. This is the whole diagram: the right forces, named, and not one arrow more.',
    },
    {
      id: 'phy7-b',
      label: 'Script B',
      persona: 'Right forces, no labels',
      work: [
        'All four correct forces drawn as arrows.',
        'No label on any arrow.',
      ],
      keyLevelId: 'm6',
      keyNote:
        '6/7 — the forces are all correct, but with no labels the diagram loses one mark overall. The cheapest mark on any diagram question is the label; write the name beside every arrow.',
      embodies: {
        behaviour: 'Draws the correct forces but leaves them unlabelled — the flat “–1 if no label” deduction.',
        cite: MS('p.11'),
      },
    },
    {
      id: 'phy7-c',
      label: 'Script C',
      persona: 'Hedges with an extra force',
      work: [
        'All four correct forces, each labelled.',
        'Adds a fifth arrow — a made-up “forward driving force of the air” — that is not acting.',
      ],
      keyLevelId: 'm6',
      keyNote:
        '6/7 — the four real forces are perfect, but the invented fifth force triggers “–1 for additional incorrect forces”. Unlike a list, where a wrong extra is harmless, on a diagram every extra wrong arrow costs a mark. Draw only the forces you can justify.',
      embodies: {
        behaviour: 'Pads the diagram with an invented extra force — the “–1 for additional incorrect forces” deduction.',
        cite: MS('p.11'),
      },
    },
    {
      id: 'phy7-d',
      label: 'Script D',
      persona: 'Unlabelled AND padded',
      work: [
        'All four correct forces drawn — but no labels …',
        '… and a made-up extra force added on top.',
      ],
      keyLevelId: 'm5',
      keyNote:
        '5/7 — both deductions land at once: –1 for no labels and –1 for the invented force. The two rules stack, so a diagram carrying “more” drawing scores less than a clean, labelled one.',
    },
  ],
  takeaway: {
    id: 'codex-phy7',
    rule: 'On a diagram: label every arrow, draw nothing you can’t justify.',
    detail:
      'Vector and labelled diagrams score each correct element as a granule, then dock one mark for an unlabelled diagram and one for each additional incorrect element. Padding a diagram with extra forces is the opposite of a list — here a wrong extra actively costs a mark. Draw exactly the elements that belong, and label all of them.',
    cite: MS('p.11'),
  },
};

// ─────────────── Phy8 · The double solidus is a fork, not a buffet ───────────────

const PHY8: ScaleSession = {
  mode: 'scale',
  id: 'phy-mutex',
  subject: 'physics',
  level: 'common',
  title: 'One method or the other — never half of each',
  cue: 'Describe / Method',
  question:
    'A 6-mark answer can be reached by either of two methods, printed in the scheme as “Method A // Method B” — the double solidus means the two are mutually exclusive. A candidate writes the first half of Method A, then switches and writes the second half of Method B, hoping to bank a partial from each side. How is it marked?',
  questionNote:
    'Scenario authored for this exercise. Instruction 3 of the scheme states that answers separated by a double solidus // are mutually exclusive — a partial answer from one side may not be combined with a partial answer from the other.',
  scale: {
    name: 'Mutually-exclusive methods (//)',
    levels: ladder([0, 3, 6]),
    notes: [
      'Rule (instruction 3): “Answers that are separated by a double solidus, //, are answers which are mutually exclusive.”',
      '“A partial answer from one side of the // may not be taken in conjunction with a partial answer from the other side.”',
      'So half of Method A plus half of Method B is not 3 + 3 — the examiner credits only the better single side.',
      'Choose one method and carry it all the way through; blending two throws away the marks that don’t line up.',
    ],
    cite: MS('p.3 (instruction 3, // mutually exclusive)'),
  },
  scripts: [
    {
      id: 'phy8-a',
      label: 'Script A',
      persona: 'Half of each method',
      work: [
        'Writes the first step of Method A correctly (one valid partial).',
        'Then abandons it and writes the second step of Method B (a partial from the other side).',
      ],
      keyLevelId: 'm3',
      keyNote:
        '3/6 — the two sides of a // cannot be combined, so the examiner takes the better single partial and stops. Two half-methods do not add up to one whole; commit to one route and finish it.',
      embodies: {
        behaviour: 'Cherry-picks a partial from each side of a // pair, which instruction 3 forbids combining.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'phy8-b',
      label: 'Script B',
      persona: 'One coherent method',
      work: [
        'Picks Method A and writes both of its steps correctly.',
        'Does not touch Method B at all.',
      ],
      keyLevelId: 'm6',
      keyNote:
        '6/6 — one method, carried right through. That is what the scheme rewards: a complete answer from a single side of the //.',
    },
  ],
  takeaway: {
    id: 'codex-phy8',
    rule: 'A // is a fork, not a buffet — pick one method and finish it.',
    detail:
      'Where the scheme separates two answers with a double solidus, they are mutually exclusive: a partial from one side cannot be added to a partial from the other. Choose the method you know best and complete it — blending two routes forfeits every mark that doesn’t belong to a single coherent answer.',
    cite: MS('p.3'),
  },
};

// ─────────────── Phy9 · Every experiment is apparatus + method + observation ───────────────

const PHY9: GridSession = {
  mode: 'grid',
  id: 'phy-experiment',
  subject: 'physics',
  level: 'common',
  title: 'The result is a whole mark',
  cue: 'Describe an experiment',
  question:
    'Describe an experiment to demonstrate that light waves are transverse. The scheme marks it in three granules — “apparatus [3] / method [3] / result [3]”. A candidate names two polaroids and a light source and says to rotate one relative to the other, then stops.',
  questionNote:
    'Question authored for this exercise. “Describe a laboratory experiment” answers are marked as three independent granules — apparatus, method and observation/result — a structure the scheme applies across experiment questions (e.g. 2025 Q8(ii), 2023 Q8(ii)).',
  grid: {
    perPoint: [
      { id: 'apparatus', label: 'Apparatus named', marks: 3 },
      { id: 'method', label: 'Method described', marks: 3 },
      { id: 'observation', label: 'Observation / result stated', marks: 3 },
    ],
    shorthand: 'experiment · [3 + 3 + 3]',
    ruleNote:
      'A “describe an experiment” answer is three independent granules — name the apparatus, describe the method, and state what you observe. The observation is the one candidates skip, and it is a whole granule: an experiment write-up with no result stops a third short.',
    cite: MS('p.14 (Q8(ii) apparatus / method / result)'),
  },
  scripts: [
    {
      id: 'phy9-a',
      label: 'Script A',
      persona: 'Forgets the result',
      attempts: [
        {
          id: 'phy9-a-1',
          text: 'Two pieces of polaroid and a light source; rotate one polaroid relative to the other. (Nothing said about what is seen.)',
          key: { apparatus: 3, method: 3, observation: 0 },
          keyNote:
            'Apparatus and method are both there (6), but the answer never says what happens — the “light intensity decreases” observation is its own 3-mark granule and it’s missing. 6/9. Always finish an experiment with what you would actually see.',
        },
      ],
      embodies: {
        behaviour: 'Describes apparatus and method but omits the observation — forfeiting that granule.',
        cite: MS('p.14'),
      },
    },
    {
      id: 'phy9-b',
      label: 'Script B',
      persona: 'Full write-up',
      attempts: [
        {
          id: 'phy9-b-1',
          text: 'Two polaroids and a light source; rotate one polaroid relative to the other; the transmitted light intensity falls to a minimum.',
          key: { apparatus: 3, method: 3, observation: 3 },
          keyNote: 'Apparatus, method and the observed result — all three granules. 9/9.',
        },
      ],
    },
    {
      id: 'phy9-c',
      label: 'Script C',
      persona: 'No kit named',
      attempts: [
        {
          id: 'phy9-c-1',
          text: 'Rotate one polariser relative to the other and watch the light dim to a minimum — but never states what apparatus is set up.',
          key: { apparatus: 0, method: 3, observation: 3 },
          keyNote:
            'Method and observation are credited (6), but the apparatus granule needs the kit named — two polaroids and a light source. 6/9. Name the equipment before you describe what to do with it.',
        },
      ],
      embodies: {
        behaviour: 'States method and observation but never names the apparatus — losing the apparatus granule.',
        cite: MS('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy9',
    rule: 'An experiment is apparatus + method + observation — write all three.',
    detail:
      '“Describe an experiment” is marked as three independent granules: name the apparatus, describe the method, and state the observation or result. The result is the one most often left off, and it is a whole granule — never end a write-up without saying what you would see.',
    cite: MS('p.14'),
  },
};

// ─────────────── Phy10 · A law is stated in clauses ───────────────

const PHY10: GridSession = {
  mode: 'grid',
  id: 'phy-law',
  subject: 'physics',
  level: 'common',
  title: 'Half a law is half the marks',
  cue: 'State the law',
  question:
    'State Newton’s law of universal gravitation. The scheme marks it “[3 + 3]”: the force is proportional to the product of the two masses [3], and inversely proportional to the square of the distance between them [3]. A candidate writes only “the force is proportional to the product of the two masses”.',
  questionNote:
    'Question authored for this exercise. A “state the law” answer with two proportionality clauses is marked one granule per clause — the SEC scheme prints Newton’s law of universal gravitation (and Coulomb’s law) as “[3 + 3]”.',
  grid: {
    perPoint: [
      { id: 'direct', label: 'Direct-proportion clause (∝ product of masses)', marks: 3 },
      { id: 'inverse', label: 'Inverse-square clause (∝ 1/d²)', marks: 3 },
    ],
    shorthand: 'state the law · [3 + 3]',
    ruleNote:
      'A law with two proportionalities is marked in two halves. Newton’s law needs BOTH “proportional to the product of the masses” AND “inversely proportional to the square of the distance” — each is its own 3-mark granule. Give one clause and you bank half the law; the missing inverse-square part is not a detail, it is a mark.',
    cite: MS('p.13 (Q7(ii) law stated in two clauses)'),
  },
  scripts: [
    {
      id: 'phy10-a',
      label: 'Script A',
      persona: 'Only the first clause',
      attempts: [
        {
          id: 'phy10-a-1',
          text: '“The gravitational force is proportional to the product of the two masses.”',
          key: { direct: 3, inverse: 0 },
          keyNote:
            'The first clause is there (3), but the inverse-square clause is a separate 3-mark granule and it’s missing. 3/6. A law stated halfway banks half its marks.',
        },
      ],
      embodies: {
        behaviour: 'States only the direct-proportion half of a two-clause law.',
        cite: MS('p.13'),
      },
    },
    {
      id: 'phy10-b',
      label: 'Script B',
      persona: 'The whole law',
      attempts: [
        {
          id: 'phy10-b-1',
          text: '“The gravitational force between two masses is proportional to the product of the masses and inversely proportional to the square of the distance between them.”',
          key: { direct: 3, inverse: 3 },
          keyNote: 'Both clauses — the product of the masses and the inverse square of the distance. Full 6 marks.',
        },
      ],
    },
    {
      id: 'phy10-c',
      label: 'Script C',
      persona: 'Vague on the distance',
      attempts: [
        {
          id: 'phy10-c-1',
          text: '“The force is proportional to the product of the masses and depends on the distance between them.”',
          key: { direct: 3, inverse: 0 },
          keyNote:
            'The first clause is secure (3), but “depends on the distance” is not “inversely proportional to the square of the distance” — the second granule needs the exact relationship. 3/6. Name the inverse-square, or the marks stay on the table.',
        },
      ],
      embodies: {
        behaviour: 'Gestures at the distance dependence without stating the inverse-square law — the second clause scores 0.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy10',
    rule: 'State every clause of the law — each proportionality is its own mark.',
    detail:
      'A law with two proportionalities is marked one granule per clause. Newton’s law of universal gravitation and Coulomb’s law both need the direct-proportion clause AND the inverse-square clause — state both, exactly, or you bank only half the law.',
    cite: MS('p.13'),
  },
};

// ─────────────── Phy11 · A derivation is graded on its working ───────────────

const PHY11: GridSession = {
  mode: 'grid',
  id: 'phy-derivation',
  subject: 'physics',
  level: 'common',
  title: 'In a derivation the answer is the cheap part',
  cue: 'Derive an expression',
  question:
    'Derive an equation for the angular velocity ω of an object in terms of its linear velocity v when it moves in a circle. The scheme marks it “[2 + 2 + 2]”: a starting relationship (θ = s/r or v = s/t or ω = θ/t) [2], the combination of two of them [2], and the result ω = v/r [2]. A candidate simply writes “ω = v/r”.',
  questionNote:
    'Question authored for this exercise. A “derive” answer is marked in granules — the starting formulae, the combination step, and the final expression — and because the target result is printed in the question, the marks live in the working.',
  grid: {
    perPoint: [
      { id: 'start', label: 'Starting relationship(s) quoted', marks: 2 },
      { id: 'combine', label: 'Combination step shown', marks: 2 },
      { id: 'result', label: 'Correct final expression reached', marks: 2 },
    ],
    shorthand: 'derivation · [2 + 2 + 2]',
    ruleNote:
      'A “derive” is not a “state”. The target expression is already printed in the question, so writing it down alone proves nothing — the marks are in the starting relationships and, above all, the “combination of two formulae” step. Show the algebra that gets you from start to finish.',
    cite: MS('p.13 (Q7(iii) derivation: formulae / combination / result)'),
  },
  scripts: [
    {
      id: 'phy11-a',
      label: 'Script A',
      persona: 'Just writes the target',
      attempts: [
        {
          id: 'phy11-a-1',
          text: '“ω = v/r.” (No starting formulae, no working.)',
          key: { start: 0, combine: 0, result: 0 },
          keyNote:
            '0/6 — the target ω = v/r is printed in the question, so restating it derives nothing. With no starting relationships and no combination step, there is no working to credit. In a “derive”, the answer is given; the marks are the journey.',
        },
      ],
      embodies: {
        behaviour: 'Restates the given target expression with no derivation — which earns nothing in a “derive” question.',
        cite: MS('p.13'),
      },
    },
    {
      id: 'phy11-b',
      label: 'Script B',
      persona: 'Full derivation',
      attempts: [
        {
          id: 'phy11-b-1',
          text: '“v = s/t, ω = θ/t and θ = s/r; combining, ω = θ/t = (s/r)/t = (s/t)/r = v/r.”',
          key: { start: 2, combine: 2, result: 2 },
          keyNote: 'Starting relationships, the combination step, and the result — all three granules. 6/6.',
        },
      ],
    },
    {
      id: 'phy11-c',
      label: 'Script C',
      persona: 'Formulae, then a leap',
      attempts: [
        {
          id: 'phy11-c-1',
          text: '“v = s/t, ω = θ/t, θ = s/r — therefore ω = v/r.”',
          key: { start: 2, combine: 0, result: 2 },
          keyNote:
            'The starting formulae are quoted (2) and the result is right (2), but “therefore” jumps the gap — the combination of the formulae is its own 2-mark granule and it isn’t shown. 4/6. Write the algebra, don’t assert it.',
        },
      ],
      embodies: {
        behaviour: 'Quotes the starting formulae and the result but skips the combination step that links them.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy11',
    rule: 'In a derivation, show the combination — the result is already given.',
    detail:
      'A “derive” is marked in granules: the starting relationships, the combination step, and the final expression. The target is printed in the question, so restating it scores nothing — the marks are in the formulae you start from and the algebra that combines them. Show every step.',
    cite: MS('p.13'),
  },
};

// ─────────────── Phy12 · The scheme pre-pays the near-miss ───────────────

const PHY12: ScaleSession = {
  mode: 'scale',
  id: 'phy-partial-credit',
  subject: 'physics',
  level: 'common',
  title: 'The near-miss is worth marks',
  cue: 'Explain the principle',
  question:
    'Explain the principle of the source of the Sun’s energy. The scheme gives “fusion [7]” and adds “[award 4 marks for reference to nuclear reactions / E = mc²]”. A candidate never writes “fusion”, but writes “the energy comes from nuclear reactions in the core, where mass is converted to energy (E = mc²)”. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme routinely prints a fallback credit in square brackets — “[award N marks for …]” or “[accept … for N marks]” — so a near-miss answer scores a stated partial, not zero.',
  scale: {
    name: 'Pre-set partial credit',
    levels: ladder([0, 4, 7]),
    notes: [
      'Full answer: “fusion [7]”.',
      'Fallback printed in the scheme: “[award 4 marks for reference to nuclear reactions / E = mc²]”.',
      'So the near-miss is not zero — it banks the pre-set 4 marks.',
      'These bracketed fallbacks appear throughout the scheme (e.g. amplitude “[accept … for 3 marks]”, Celsius equation “[accept reference to 273(.15) for 3 marks]”). If you can’t land the exact key word, write the nearest real physics — it is often worth half.',
    ],
    cite: MS('p.12 (Q6(k) fusion, “[award 4 marks for …]”)'),
  },
  scripts: [
    {
      id: 'phy12-a',
      label: 'Script A',
      persona: 'Near miss with real physics',
      work: [
        'Never uses the word “fusion”.',
        'States the energy comes from nuclear reactions converting mass to energy, E = mc².',
      ],
      keyLevelId: 'm4',
      keyNote:
        '4/7 — the exact key word “fusion” is the full-mark answer, but the scheme pre-authorises 4 marks for “nuclear reactions / E = mc²”. A near-miss carrying real physics is worth far more than a blank; write what you do know.',
      embodies: {
        behaviour: 'Gives the pre-authorised fallback answer rather than the exact key word — earning the stated partial credit.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'phy12-b',
      label: 'Script B',
      persona: 'Exact key word',
      work: ['States the source is nuclear fusion (of hydrogen into helium).'],
      keyLevelId: 'm7',
      keyNote: '7/7 — the key word “fusion” is the full-mark answer.',
    },
  ],
  takeaway: {
    id: 'codex-phy12',
    rule: 'Can’t hit the key word? Write the nearest real physics — the scheme often pre-pays a partial.',
    detail:
      'Schemes print bracketed fallbacks — “[award N marks for …]”, “[accept … for N marks]” — so a near-miss answer earns a specified partial rather than zero. Never leave an “explain the principle” blank because you’re unsure of the one word; the related physics you can state is usually worth marks.',
    cite: MS('p.12'),
  },
};

// ─────────────── Phy13 · Right word, wrong context ───────────────

const PHY13: ScaleSession = {
  mode: 'scale',
  id: 'phy-context',
  subject: 'physics',
  level: 'common',
  title: 'A true statement in the wrong place scores zero',
  cue: 'State one improvement',
  question:
    'State one other way to improve the accuracy of the momentum experiment. The scheme accepts “e.g. repeat the experiment / reduce the error of parallax / a more accurate balance or timer [3]”, but instruction 1 says key words only score “in the correct context”. A candidate writes “use a bigger spring so the trolleys move faster”. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Instruction 1 of the scheme states that key words must appear “in the correct context” to merit the marks — a true statement that does not answer the question as asked scores nothing.',
  scale: {
    name: 'Right word, right context',
    levels: ladder([0, 3]),
    notes: [
      'Rule (instruction 1): key words “must appear in the correct context in the candidate’s answer in order to merit the assigned marks”.',
      'The accepted answers are about accuracy: repeat the experiment, reduce parallax error, use a more accurate balance/timer.',
      '“Use a bigger spring” is a true statement, but it changes the speed of the trolleys, not the accuracy — wrong context, no marks.',
      'Answer the question actually asked: a correct physics fact aimed at the wrong question is worth nothing.',
    ],
    cite: MS('p.3 (instruction 1, correct context); p.7 (Q2(vii) accuracy)'),
  },
  scripts: [
    {
      id: 'phy13-a',
      label: 'Script A',
      persona: 'True but off-topic',
      work: ['“Use a bigger spring so the trolleys move faster.”'],
      keyLevelId: 'm0',
      keyNote:
        '0/3 — a correct statement, but it improves nothing about the accuracy the question asked for. The scheme wanted a precaution against error (repeat runs, reduce parallax, better instruments). A right fact in the wrong context scores zero.',
      embodies: {
        behaviour: 'Answers with a true statement in the wrong context, which instruction 1 gives no credit for.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'phy13-b',
      label: 'Script B',
      persona: 'On-target precaution',
      work: ['“Repeat the experiment several times and average, and read the scale at eye level to reduce parallax error.”'],
      keyLevelId: 'm3',
      keyNote: '3/3 — a genuine accuracy improvement, squarely in the context the question set.',
    },
  ],
  takeaway: {
    id: 'codex-phy13',
    rule: 'Answer the question asked — a right fact in the wrong context scores zero.',
    detail:
      'Instruction 1 credits key words only when they appear “in the correct context”. A statement can be perfectly true and still earn nothing if it doesn’t answer the question as set. Read what is actually being asked, and aim your answer at it.',
    cite: MS('p.3'),
  },
};

// ─────────────── Phy14 · Nuclear equations: balance it, add nothing ───────────────

const PHY14: ScaleSession = {
  mode: 'scale',
  id: 'phy-nuclear-eqn',
  subject: 'physics',
  level: 'common',
  title: 'Balance the equation, invent no particles',
  cue: 'Write the nuclear equation',
  question:
    'State the nuclear equation for the Cockcroft–Walton reaction — a proton striking lithium-7 to give two alpha particles. The scheme marks the species “[4 × 2]” — each correct nuclide, with its mass and atomic numbers, is worth 2 — and adds “[–2 additional incorrect species]”. A candidate writes the fully correct equation but tacks on a stray gamma-ray photon that is not part of it. What does it score?',
  questionNote:
    'Scenario authored for this exercise. A nuclear equation is marked per species (each nuclide with its correct mass and atomic numbers), and the scheme deducts marks for each additional incorrect species written in (2025 Q12(a)(i); 2023 Q9(i)).',
  scale: {
    name: 'Nuclear equation [4 × 2]',
    levels: ladder([4, 6, 8]),
    notes: [
      'Rule: each correct species scores — here “[4 × 2]”, 2 marks per nuclide, for a maximum of 8.',
      'Penalty printed in the scheme: “[–2 additional incorrect species]”.',
      'So a fully correct equation padded with one spurious particle scores 8 – 2 = 6, not 8.',
      'A nuclide only earns its 2 marks if its mass and atomic numbers balance across the arrow — wrong numbers, no granule.',
      'Like the extra-force rule on a diagram, an invented species actively costs marks: write only the particles that are really there.',
    ],
    cite: MS('p.18 (Q12(a)(i) “[4 × 2]” & “[–2 additional incorrect species]”)'),
  },
  scripts: [
    {
      id: 'phy14-a',
      label: 'Script A',
      persona: 'Correct, but padded',
      work: [
        'Proton + lithium-7 → two alpha particles; every nuclide and every mass/atomic number correct.',
        'Adds a spurious γ photon to the products “to be safe”.',
      ],
      keyLevelId: 'm6',
      keyNote:
        '6/8 — the four real species are all correct (8), but the invented gamma photon triggers “–2 additional incorrect species”. An extra particle you can’t justify is not free insurance; it costs. Write only what is actually produced.',
      embodies: {
        behaviour: 'Adds a spurious extra species to a correct equation — the “–2 additional incorrect species” deduction.',
        cite: MS('p.18'),
      },
    },
    {
      id: 'phy14-b',
      label: 'Script B',
      persona: 'Clean and balanced',
      work: ['Proton + lithium-7 → two alpha particles; every mass and atomic number balanced; nothing extra added.'],
      keyLevelId: 'm8',
      keyNote: '8/8 — four correct species, correctly numbered, and not one spurious particle.',
    },
    {
      id: 'phy14-c',
      label: 'Script C',
      persona: 'Numbers don’t balance',
      work: [
        'Names the right particles — proton, lithium, alpha — but the mass/atomic numbers on one side don’t balance the other.',
      ],
      keyLevelId: 'm4',
      keyNote:
        '4/8 — some species score, but nuclides carrying wrong mass or atomic numbers don’t earn their 2 marks. The top and bottom numbers must balance across the arrow before a species counts.',
      embodies: {
        behaviour: 'Writes the species but leaves the mass/atomic numbers unbalanced, forfeiting those per-species granules.',
        cite: MS('p.18'),
      },
    },
  ],
  takeaway: {
    id: 'codex-phy14',
    rule: 'Balance the equation and add nothing extra — each species is marked, and spurious ones cost.',
    detail:
      'A nuclear equation scores per species, each nuclide worth marks only when its mass and atomic numbers balance across the arrow. An additional incorrect species is penalised, exactly like an invented extra force on a diagram. Write only the particles that are really there, and balance the top and bottom numbers.',
    cite: MS('p.18'),
  },
};

// ─────────────── Phy15 · Define every symbol, even the obvious ones ───────────────

const PHY15: GridSession = {
  mode: 'grid',
  id: 'phy-symbols',
  subject: 'physics',
  level: 'common',
  title: 'The “obvious” symbol still carries marks',
  cue: 'Explain the symbols',
  question:
    'The emission-line equation is hf = E₂ – E₁. Explain what each symbol stands for. The scheme marks it “[2 + 2 + 2 + 1]”: h = Planck constant, f = frequency, E₂ = higher energy, E₁ = lower energy. A candidate carefully defines E₂ and E₁ but writes nothing for h and f, assuming they’re too obvious to bother with.',
  questionNote:
    'Question authored for this exercise (SEC 2023 Q6(l)). When a question asks you to explain each symbol in an equation, every symbol is a separate granule — including the “obvious” constants.',
  grid: {
    perPoint: [
      { id: 'h', label: 'h = Planck constant', marks: 2 },
      { id: 'f', label: 'f = frequency', marks: 2 },
      { id: 'e2', label: 'E₂ = higher energy level', marks: 2 },
      { id: 'e1', label: 'E₁ = lower energy level', marks: 1 },
    ],
    shorthand: 'define each symbol · [2 + 2 + 2 + 1]',
    ruleNote:
      'When a question says “explain what each symbol stands for”, every symbol is its own granule — even the ones that feel too basic to write. Skipping h or f because they seem obvious throws away 2 marks apiece. Define all of them.',
    cite: MS23('p.12 (Q6(l) symbols defined [2 + 2 + 2 + 1])'),
  },
  scripts: [
    {
      id: 'phy15-a',
      label: 'Script A',
      persona: 'Skips the obvious',
      attempts: [
        {
          id: 'phy15-a-1',
          text: '“E₂ is the higher energy level and E₁ is the lower energy level.” (Nothing written for h or f.)',
          key: { h: 0, f: 0, e2: 2, e1: 1 },
          keyNote:
            'The two energy terms are defined (3), but h and f are left blank because they “seemed obvious” — and each was a 2-mark granule. 3/7. The scheme rewards defining every symbol, however basic; never skip one.',
        },
      ],
      embodies: {
        behaviour: 'Leaves the “obvious” symbols (h, f) undefined, forfeiting their granules.',
        cite: MS23('p.12'),
      },
    },
    {
      id: 'phy15-b',
      label: 'Script B',
      persona: 'Every symbol defined',
      attempts: [
        {
          id: 'phy15-b-1',
          text: '“h = the Planck constant, f = the frequency of the photon, E₂ = the higher energy level, E₁ = the lower energy level.”',
          key: { h: 2, f: 2, e2: 2, e1: 1 },
          keyNote: 'All four symbols defined — full 7 marks. The two “obvious” constants carried 4 of the 7 marks between them.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-phy15',
    rule: 'Define every symbol — even the obvious constants each carry marks.',
    detail:
      'When asked to explain the symbols in an equation, every symbol is a separate granule, including constants like h and frequencies like f that feel too basic to state. Define all of them — the “obvious” ones are often worth as much as the rest.',
    cite: MS23('p.12'),
  },
};

export const PHYSICS_CHAIR: ChairSubject = {
  id: 'physics',
  label: 'Physics',
  tagline: 'Granules, units, laws, derivations and diagrams — how physics marks are really built.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [PHY1, PHY2, PHY3, PHY4, PHY5, PHY6, PHY7, PHY8, PHY9, PHY10, PHY11, PHY12, PHY13, PHY14, PHY15],
  sources: [
    { label: 'SEC LC Physics HL marking scheme 2025 (examiner-reports/physics/2025-marking-scheme)' },
    { label: 'SEC LC Physics HL marking scheme 2023 (examiner-reports/physics/2023-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general marking conventions the scheme applies across levels — the numerical granule ladder, the one-mark unit deduction, error-carried-forward, part-marked definitions, “state N”-from-a-list marking, the graph granules (with the inappropriate-scale deduction), the labelled-diagram rules, the double-solidus mutually-exclusive-method rule, the apparatus/method/observation structure of experiment questions, stating a law clause-by-clause, derivation granules (the combination step), the scheme’s pre-set partial credit, the correct-context requirement, per-species nuclear-equation marking, and defining every symbol. Verified against the 2025 and 2023 Higher Level schemes; level-specific worked examples are being added.',
};
