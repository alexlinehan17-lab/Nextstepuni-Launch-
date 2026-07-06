/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Engineering (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the "Any N @…" best-N cap, the 3+2 point+development split,
 * separately-credited diagram labels, and the Practical's Assembly/Function/Finish
 * concept marks) is the real SEC system, cited to:
 *  - SEC LC Engineering HL marking scheme 2025 —
 *    examiner-reports/engineering/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Engineering HL marking scheme 2025, ${p}` });

// ─────────────── EN1 · The "Any N" cap ───────────────

const EN1: GridSession = {
  mode: 'grid',
  id: 'en-anyn',
  subject: 'engineering',
  level: 'common',
  title: 'Answer exactly the number asked',
  cue: 'Any three',
  question: 'A part says “Discuss any three properties”, marked 6 + 6 + 6. Only three answers are credited, and each 6 is earned only if the property is properly discussed. A candidate plays safe and writes five properties — but rushes them all, so each is a bare mention with no real discussion. Mark it.',
  questionNote:
    'Scenario authored for this exercise. In “Any N @…” parts only N answers are credited (extras earn nothing), and each counted mark is earned only if the point is properly discussed. Writing more, thinner answers does not beat writing N developed ones.',
  grid: {
    perPoint: [{ id: 'prop', label: 'Property properly discussed', marks: 6 }],
    shorthand: 'Any three @ 6 + 6 + 6 (three credited)',
    ruleNote:
      'Only three answers are credited — extra answers earn nothing, so over-answering just costs time. And each 6 is earned only by proper discussion, not a bare mention. Fewer, developed points beat more, thin ones.',
    cite: MS('p.20 (Any three @ 6+6+6 cap)'),
  },
  scripts: [
    {
      id: 'en1-a',
      label: 'Script A',
      persona: 'Writes five, all thin',
      attempts: [
        {
          id: 'en1-a-1',
          text: 'Property 1 — named only, no discussion.',
          key: { prop: 0 },
          keyNote: 'A bare mention with no discussion, so it doesn’t earn the 6. Naming a property is not discussing it.',
        },
        {
          id: 'en1-a-2',
          text: 'Property 2 — again just named.',
          key: { prop: 0 },
          keyNote: 'The same problem — a label, not a discussion. No mark.',
        },
        {
          id: 'en1-a-3',
          text: 'Property 3 — another bare mention. (Two more properties were written too, but only three are credited and none of the five is actually discussed.)',
          key: { prop: 0 },
          keyNote: 'Writing five didn’t help: only three are ever credited, so the extra two were wasted effort — and because nothing was properly discussed, even the counted three earn nothing. 0 of 18. Three developed points would have scored full marks.',
        },
      ],
      embodies: {
        behaviour: 'Over-answers an “Any N” part with thin points, trusting quantity — but only N are credited and each needs proper discussion.',
        cite: MS('p.20'),
      },
    },
    {
      id: 'en1-b',
      label: 'Script B',
      persona: 'Three, each developed',
      attempts: [
        {
          id: 'en1-b-1',
          text: 'Property 1 — stated, then developed with a point and its consequence.',
          key: { prop: 6 },
          keyNote: 'A properly discussed property — point plus consequence. 6.',
        },
        {
          id: 'en1-b-2',
          text: 'Property 2 — a second property, developed.',
          key: { prop: 6 },
          keyNote: 'Another developed point. 6.',
        },
        {
          id: 'en1-b-3',
          text: 'Property 3 — a third property, developed.',
          key: { prop: 6 },
          keyNote: 'Exactly three, each developed. 18/18 — and less writing than Script A.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en1',
    rule: 'Fewer developed points beat more thin ones.',
    detail:
      'In “Any N @…” parts only N answers are credited — extra answers earn nothing, so over-answering only costs you time. And each mark is earned by proper discussion, not a bare mention. Pick your strongest N and develop them.',
    cite: MS('p.20'),
  },
};

// ─────────────── EN2 · Headline before development ───────────────

const EN2: GridSession = {
  mode: 'grid',
  id: 'en-headline',
  subject: 'engineering',
  level: 'common',
  title: 'State the point, then develop it',
  cue: 'Explain',
  question: 'An “explain” point is marked 3 + 2: 3 for stating the point clearly, 2 for developing it. A candidate writes a flowing paragraph that circles the idea and eventually implies it, but never states it plainly.',
  questionNote:
    'Scenario authored for this exercise. The dominant Engineering “explain” pattern is 3 (state the point) + 2 (develop it); the clear headline banks the larger mark.',
  grid: {
    perPoint: [
      { id: 'point', label: 'State the point clearly', marks: 3 },
      { id: 'develop', label: 'Develop it', marks: 2 },
    ],
    shorthand: '3 + 2 (point + development)',
    ruleNote:
      'The headline is the bigger mark, and it has to be stated, not implied. A paragraph that circles the idea without naming it risks the 3, even if the development is good. Say the point in a plain sentence first, then develop it.',
    cite: MS('p.7–9 (3+2 point + development split)'),
  },
  scripts: [
    {
      id: 'en2-a',
      label: 'Script A',
      persona: 'Circles the point',
      attempts: [
        {
          id: 'en2-a-1',
          text: 'A flowing paragraph that hints at the idea and implies it by the end — but never states it in a plain sentence.',
          key: { point: 0, develop: 2 },
          keyNote: 'The development marks are there, but the 3-mark headline needs the point stated plainly — an implied point is a risked point. A single clear opening sentence naming the property or principle would have banked the 3. State it, then develop it.',
        },
      ],
      embodies: {
        behaviour: 'Implies the point instead of stating it, risking the larger headline mark.',
        cite: MS('p.7'),
      },
    },
    {
      id: 'en2-b',
      label: 'Script B',
      persona: 'Headline then development',
      attempts: [
        {
          id: 'en2-b-1',
          text: 'States the point in a plain opening sentence, then develops it with a reason and an example.',
          key: { point: 3, develop: 2 },
          keyNote: 'Clear headline (3) plus development (2). Full 5 — and the plain first sentence is what secured the bigger mark.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en2',
    rule: 'State the point before you develop it.',
    detail:
      'Engineering “explain” marks split 3 (state the point) + 2 (develop) — and the headline is the bigger, must-be-stated mark. Open with a plain sentence naming the point, then develop it; don’t leave it implied.',
    cite: MS('p.7'),
  },
};

// ─────────────── EN3 · Labels are their own marks ───────────────

const EN3: GridSession = {
  mode: 'grid',
  id: 'en-labels',
  subject: 'engineering',
  level: 'common',
  title: 'The labels score too',
  cue: 'Draw a diagram',
  question: 'A diagram part is marked 8 + 1 + 1: 8 for the diagram, and two required labels credited separately at 1 mark each. A candidate draws an excellent diagram but leaves both labels off.',
  questionNote:
    'Scenario authored for this exercise. Engineering diagrams credit required labels separately from the drawing (e.g. 8 + 1 + 1).',
  grid: {
    perPoint: [
      { id: 'diagram', label: 'Diagram', marks: 8 },
      { id: 'label1', label: 'Label 1', marks: 1 },
      { id: 'label2', label: 'Label 2', marks: 1 },
    ],
    shorthand: '8 + 1 + 1 (diagram + 2 labels)',
    ruleNote:
      'The labels are their own marks, separate from the drawing. A flawless but unlabelled diagram forfeits them — small marks, but free ones, and routinely dropped.',
    cite: MS('p.16–17 (diagram + separate label marks)'),
  },
  scripts: [
    {
      id: 'en3-a',
      label: 'The diagram',
      persona: 'Great diagram, no labels',
      attempts: [
        {
          id: 'en3-a-1',
          text: 'A clear, correct diagram — but the two required parts are not labelled.',
          key: { diagram: 8, label1: 0, label2: 0 },
          keyNote: 'The diagram earns its 8, but the two label marks are separate and unearned. Two words would have added them. Whenever a diagram names parts, label them — the marks are itemised.',
        },
      ],
      embodies: {
        behaviour: 'Draws well but omits the separately-credited labels.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-en3',
    rule: 'Label the diagram — those are separate marks.',
    detail:
      'Engineering diagrams credit required labels separately from the drawing (8 + 1 + 1). A perfect unlabelled diagram forfeits them. Add every required label — they’re small, free, and easy to drop.',
    cite: MS('p.16'),
  },
};

// ─────────────── EN4 · The practical is marked on Finish too ───────────────

const EN4: GridSession = {
  mode: 'grid',
  id: 'en-finish',
  subject: 'engineering',
  level: 'common',
  title: 'A working piece is not a finished piece',
  cue: 'Practical',
  question: 'In the Practical Examination, Section 1 (the whole test-piece) is marked 20 across three concept marks: Assembly (5), Function (10) and Finish (5). A candidate’s piece assembles correctly and works perfectly — but is handed up rough: file marks left on, sharp edges undeburred, surfaces unpolished. Mark Section 1.',
  questionNote:
    'Scenario authored for this exercise. The SEC Engineering Practical marks the assembled test-piece on three separate concept marks — Assembly, Function and Finish — and the whole practical (100 marks) is scaled ×1.5 to 150.',
  grid: {
    perPoint: [
      { id: 'assembly', label: 'Assembly', marks: 5 },
      { id: 'function', label: 'Function', marks: 10 },
      { id: 'finish', label: 'Finish', marks: 5 },
    ],
    shorthand: 'Section 1: Assembly 5 + Function 10 + Finish 5 (/20)',
    ruleNote:
      'Finish is its own concept mark, scored separately from whether the piece assembles or works. A piece that functions flawlessly but is left rough forfeits the Finish 5 — a full quarter of Section 1 — no matter how well it performs.',
    cite: MS('p.32 (Practical Section 1: Assembly 5 + Function 10 + Finish 5)'),
  },
  scripts: [
    {
      id: 'en4-a',
      label: 'Script A',
      persona: 'Works, handed up rough',
      attempts: [
        {
          id: 'en4-a-1',
          text: 'The test-piece assembles correctly and functions exactly as intended — but file marks are left on the surfaces, edges are sharp and undeburred, and nothing is polished.',
          key: { assembly: 5, function: 10, finish: 0 },
          keyNote: 'Assembly and Function are fully earned (15), but Finish is a separate 5-mark concept and it is gone — a quarter of Section 1 lost to rough surfaces. A few minutes deburring and cleaning up the finish would have banked it. The piece working does not carry the Finish mark.',
        },
      ],
      embodies: {
        behaviour: 'Builds a piece that assembles and functions perfectly but leaves the finish rough, dropping the separately-credited Finish concept mark.',
        cite: MS('p.32'),
      },
    },
    {
      id: 'en4-b',
      label: 'Script B',
      persona: 'Same piece, finished properly',
      attempts: [
        {
          id: 'en4-b-1',
          text: 'The same working, correctly-assembled test-piece — but surfaces are cleaned up, edges deburred and the piece finished before it is handed up.',
          key: { assembly: 5, function: 10, finish: 5 },
          keyNote: 'Assembly (5), Function (10) and Finish (5) all earned. Full 20 — the only difference from Script A is the finishing pass, and it was worth a clean 5 marks.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en4',
    rule: 'Finish is marked, even when the piece works.',
    detail:
      'In the Engineering Practical, Section 1 splits into Assembly (5), Function (10) and Finish (5) — and the whole 100-mark practical is scaled ×1.5 to 150. Finish is credited in its own right, so a working piece left rough still drops those marks. Leave time to deburr, clean up and finish the test-piece.',
    cite: MS('p.32'),
  },
};

// ─────────────── EN5 · A calculation is one all-or-nothing granule ───────────────

const EN5: GridSession = {
  mode: 'grid',
  id: 'en-calc',
  subject: 'engineering',
  level: 'common',
  title: 'Show the chain, and put the unit on the answer',
  cue: 'Calculate',
  question:
    'A calculation part — ultimate tensile strength — is worth 4 marks as a single granule: the formula, the substituted values and the final answer *with its unit* all sit under one mark value. A candidate does the arithmetic correctly on a calculator and writes only “= 1.6” — no formula, no substitution, no unit. Mark it.',
  questionNote:
    'Scenario authored for this exercise. Based on Q3(b)(iii) (ultimate tensile strength) in the 2025 HL scheme — a numerical answer marked as one 4-mark granule covering formula → substitution → answer, with the unit carried into the accepted answer (kN/mm²). There is no separate “unit mark” and no partial-credit ladder.',
  grid: {
    perPoint: [{ id: 'calc', label: 'Calculation shown, answer with its unit', marks: 4 }],
    shorthand: 'Single 4-mark granule (formula → substitution → answer + unit)',
    ruleNote:
      'The whole chain — formula, substituted values and the final answer with its unit — sits under one 4-mark value. There is no part-marks ladder to catch a stray step and no separate unit mark to fall back on, so a bare number, or a right answer with the unit dropped, risks the entire granule. Show the working and carry the unit into the answer.',
    cite: MS('p.13 (Q3(b)(iii): UTS = 181 kN / 113.1 mm² = 1.6 kN/mm², 4 marks)'),
  },
  scripts: [
    {
      id: 'en5-a',
      label: 'Script A',
      persona: 'Right value, no working or unit',
      attempts: [
        {
          id: 'en5-a-1',
          text: 'Writes only “= 1.6” as the final answer. The arithmetic was done on a calculator, but no formula or substitution is shown and no unit is given.',
          key: { calc: 0 },
          keyNote:
            'The value is right, but the granule pays for the shown chain with its unit — and there is no separate unit mark to rescue a bare “1.6”. One line — Max Load / C.S.A = 181 kN / 113.1 mm² = 1.6 kN/mm² — banks the 4. As written it risks all of it.',
        },
      ],
      embodies: {
        behaviour:
          'Gives a correct numerical value with no working and no unit, where the mark is a single all-or-nothing granule.',
        cite: MS('p.13'),
      },
    },
    {
      id: 'en5-b',
      label: 'Script B',
      persona: 'Formula, substitution, unit',
      attempts: [
        {
          id: 'en5-b-1',
          text: 'Writes the formula, substitutes the values and gives the answer with its unit: UTS = Max Load / C.S.A = 181 kN / 113.1 mm² = 1.6 kN/mm².',
          key: { calc: 4 },
          keyNote: 'Formula, substitution and a united answer — exactly the granule. Full 4.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en5',
    rule: 'Show the chain, and put the unit on the answer.',
    detail:
      'Engineering calculations are marked as a single granule — formula → substitution → answer with its unit under one value, with no separate unit mark and no partial ladder. A bare or unitless number risks the whole thing. Write the formula, substitute, and carry the unit into the final line.',
    cite: MS('p.13'),
  },
};

// ─────────────── EN6 · The model answer is an example, not a script ───────────────

const EN6: GridSession = {
  mode: 'grid',
  id: 'en-valid',
  subject: 'engineering',
  level: 'common',
  title: 'Marks follow correct content, not the model’s exact words',
  cue: 'State the function',
  question:
    'A defined 5-mark item — “state the function of…” — is marked as a single granule. One candidate gives the correct function in plain, everyday wording, nothing like the formal sentence printed in the scheme. Another reproduces a fluent, well-memorised textbook sentence — but it describes the wrong component. Mark both.',
  questionNote:
    'Scenario authored for this exercise. General instruction 1 (p.4), repeated at the head of the marking (p.7): “The solutions presented are examples only. All other valid solutions are acceptable and are marked accordingly.” Several Q1 parts are single undivided 5-mark granules (e.g. Q1(b), Q1(g)).',
  grid: {
    perPoint: [{ id: 'content', label: 'Correct technical content (any valid wording)', marks: 5 }],
    shorthand: 'Single 5-mark granule — content, not wording',
    ruleNote:
      'The printed model answer is an example, not a required script. Correct technical content in any valid wording earns the marks; polished wording around wrong content earns nothing. The examiner marks what you say, not whether you matched their phrasing.',
    cite: MS('p.4 (instruction 1) & p.7 (repeated note): “solutions presented are examples only … all other valid solutions are acceptable”'),
  },
  scripts: [
    {
      id: 'en6-a',
      label: 'Script A',
      persona: 'Different phrasing, right content',
      attempts: [
        {
          id: 'en6-a-1',
          text: 'Explains the component’s function correctly, but in plain everyday wording — nothing like the formal sentence in the marking scheme.',
          key: { content: 5 },
          keyNote:
            '“Examples only” means exactly this: the content is right, so the different wording is fully accepted. 5. Don’t rewrite your answer to chase the model’s phrasing.',
        },
      ],
    },
    {
      id: 'en6-b',
      label: 'Script B',
      persona: 'Polished wording, wrong content',
      attempts: [
        {
          id: 'en6-b-1',
          text: 'Reproduces a fluent, well-memorised textbook sentence — but it describes the wrong component, so the technical content is incorrect.',
          key: { content: 0 },
          keyNote:
            'Fluent phrasing can’t rescue wrong content — the granule pays for a correct answer, in any words. 0. Matching a revision-book sentence isn’t the goal; being technically right is.',
        },
      ],
      embodies: {
        behaviour:
          'Relies on polished, memorised wording over correct technical content, where the scheme credits content and treats its own model as an example only.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-en6',
    rule: 'Marks follow correct content, not the model’s exact words.',
    detail:
      'The scheme states its solutions “are examples only — all other valid solutions are acceptable.” A correct answer in your own words scores full; a fluent answer with wrong content scores nothing. Write what’s technically true; don’t fear phrasing that differs from a revision book.',
    cite: MS('p.4'),
  },
};

// ─────────────── EN7 · The Irish-language bonus (read the right band) ───────────────

const EN7: ScaleSession = {
  mode: 'scale',
  id: 'en-irish-bonus',
  subject: 'engineering',
  level: 'common',
  title: 'The Irish-language bonus is real, free marks',
  cue: 'Apply the bonus',
  question:
    'A candidate answered the entire written paper entirely through Irish and comes in with a provisional mark of 264 / 300 (88%) before the language bonus. Because that is above 75%, the tapered “Tábla 300 @ 5%” applies, not the flat 5%. Read the table and award the bonus band.',
  questionNote:
    'Scenario authored for this exercise. Applies general instruction 3 (p.4) and the published bonus table “Tábla 300 @ 5%” (p.5). The levels below are the real, adjacent table bands; the candidate’s band is the one to select.',
  scale: {
    name: 'Tábla 300 @ 5% (Irish-language bonus)',
    levels: [
      { id: 'en7-b4', label: 'Base 267–273 → +4', annotation: '+4', marks: 4 },
      { id: 'en7-b5', label: 'Base 261–266 → +5', annotation: '+5', marks: 5 },
      { id: 'en7-b6', label: 'Base 254–260 → +6', annotation: '+6', marks: 6 },
      { id: 'en7-b7', label: 'Base 247–253 → +7', annotation: '+7', marks: 7 },
    ],
    notes: [
      'Instruction 3 (p.4): a 5% bonus is given to a candidate who answers “entirely through Irish” and obtains less than 75% of the total marks; in calculating it “decimals are always rounded down, not up e.g., 4.5 becomes 4; 4.9 becomes 4”.',
      'Above 75%, the tapered “Tábla 300 @ 5%” (p.5) applies instead: the bonus slides from +11 (base 226) down to 0 (base 294–300). At 264/300 the candidate sits in the 261–266 band → +5.',
      'The bonus is added on top of the earned mark — it rewards committing to answering the whole paper as Gaeilge, and it is always rounded down, never up.',
    ],
    cite: MS('p.5 (Tábla 300 @ 5% bands) & p.4 (instruction 3: “rounded down, not up … 4.5 becomes 4”)'),
  },
  scripts: [
    {
      id: 'en7-a',
      label: 'The band',
      persona: 'Answered entirely through Irish, base 264/300',
      work: [
        'Candidate answered the entire written examination through Irish (as Gaeilge).',
        'Provisional mark before the language bonus: 264 / 300 (88%).',
        'Above 75%, so the tapered Tábla 300 @ 5% applies — not the flat 5% of the mark obtained.',
      ],
      keyLevelId: 'en7-b5',
      keyNote:
        '264 falls in the 261–266 band → +5 bonus (final 269). Above 75% the tapered table applies; below 75% it is a flat 5% of the mark obtained, always rounded DOWN (4.5 → 4, 4.9 → 4). Either way the bonus is real, free marks — but only for a candidate who actually answers the whole paper entirely through Irish.',
    },
  ],
  takeaway: {
    id: 'codex-en7',
    rule: 'Answering entirely through Irish earns a bonus — always rounded down.',
    detail:
      'A candidate who answers the whole written paper as Gaeilge earns a language bonus: a flat 5% of the mark obtained below 75%, or the tapered “Tábla 300 @ 5%” band above 75%. The bonus is always rounded down (4.5 → 4). It is free marks on top of the earned score — worth knowing if your Irish is strong enough to commit to the whole answer.',
    cite: MS('p.4'),
  },
};

export const ENGINEERING_CHAIR: ChairSubject = {
  id: 'engineering',
  label: 'Engineering',
  tagline: 'Answer the number asked, state the point, label the diagram, unit the answer, finish the piece.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [EN1, EN2, EN3, EN4, EN5, EN6, EN7],
  sources: [
    { label: 'SEC LC Engineering HL marking scheme 2025 (examiner-reports/engineering/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — the “Any N” cap, the point+development split, separately-credited labels, the single-granule calculation (formula → substitution → answer with unit), the “examples only / valid alternatives accepted” rule, the Irish-language bonus, and the Practical’s Assembly/Function/Finish concept marks — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked questions are being added.',
};
