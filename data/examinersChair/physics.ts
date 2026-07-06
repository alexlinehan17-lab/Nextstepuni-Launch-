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

export const PHYSICS_CHAIR: ChairSubject = {
  id: 'physics',
  label: 'Physics',
  tagline: 'Granules, units, graphs and diagrams — how physics marks are really built.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [PHY1, PHY2, PHY3, PHY4, PHY5, PHY6, PHY7],
  sources: [
    { label: 'SEC LC Physics HL marking scheme 2025 (examiner-reports/physics/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general marking conventions the scheme applies across levels — the numerical granule ladder, the one-mark unit deduction, error-carried-forward, part-marked definitions, “state N”-from-a-list marking, the graph granules (with the inappropriate-scale deduction) and the labelled-diagram rules. Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
