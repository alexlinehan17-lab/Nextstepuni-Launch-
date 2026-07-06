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

// ─────────────── EN8 · Capped list vs itemised split ───────────────

const EN8: GridSession = {
  mode: 'grid',
  id: 'en-itemised',
  subject: 'engineering',
  level: 'common',
  title: 'Know a capped list from an itemised split',
  cue: 'Name the three',
  question:
    'An “answer all parts” item asks you to identify three unit-cell structures, marked 2 + 2 + 2 — one mark-pair per structure. This is the opposite of an “Any N” list: there is no cap and no choice, so every correct structure adds marks. A candidate names two correctly and, running low on time, leaves the third blank. Mark it.',
  questionNote:
    'Scenario authored for this exercise. Based on Q5(a)(ii) in the 2025 HL scheme — three named structures marked 2 + 2 + 2. Unlike an “Any N @…” list (where only N answers are ever credited), an itemised 2 + 2 + 2 “answer all” part credits each required item separately, so a blank slot is a lost mark with nothing to offset it.',
  grid: {
    perPoint: [
      { id: 'structA', label: 'Structure A identified', marks: 2 },
      { id: 'structB', label: 'Structure B identified', marks: 2 },
      { id: 'structC', label: 'Structure C identified', marks: 2 },
    ],
    shorthand: '2 + 2 + 2 (three items, all credited)',
    ruleNote:
      'A 2 + 2 + 2 “answer all” part is the mirror image of an “Any N” cap: there is no cap, so every correct item earns its own pair — and every blank forfeits one. Read the shorthand to tell which situation you are in: “Any N @…” means give your best N and stop; “N + N + N” under “answer all parts” means fill every slot.',
    cite: MS('p.16 (Q5(a)(ii): Structure A/B/C @ 2 + 2 + 2)'),
  },
  scripts: [
    {
      id: 'en8-a',
      label: 'Script A',
      persona: 'Names two, leaves one blank',
      attempts: [
        {
          id: 'en8-a-1',
          text: 'Correctly identifies Structure A (BCC) and Structure B (FCC), but leaves Structure C blank after running low on time.',
          key: { structA: 2, structB: 2, structC: 0 },
          keyNote:
            'Two correct identifications bank 4, but the third slot is its own separate 2 and it is empty. There is no cap here to soak up the loss — every item is credited in its own right, so the missing structure is simply 2 marks gone. Naming the Close-Packed Hexagonal structure would have completed the 6.',
        },
      ],
      embodies: {
        behaviour:
          'Treats an itemised “answer all” 2 + 2 + 2 part as if extra items did not matter, leaving a separately-credited slot blank.',
        cite: MS('p.16'),
      },
    },
    {
      id: 'en8-b',
      label: 'Script B',
      persona: 'Fills all three slots',
      attempts: [
        {
          id: 'en8-b-1',
          text: 'Identifies all three structures — Structure A (BCC), Structure B (FCC) and Structure C (CPH).',
          key: { structA: 2, structB: 2, structC: 2 },
          keyNote:
            'Every slot filled, every pair earned. 6/6 — because in an itemised “answer all” split each correct item adds marks with no cap.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en8',
    rule: 'Tell a capped list from an itemised split.',
    detail:
      'An “Any N @…” list credits only N answers, so over-answering wastes time. An itemised “answer all” split (2 + 2 + 2, 1 + 1 + 1 + 1 + 1) credits every required item separately, so leaving a slot blank forfeits a standalone mark. Read the shorthand and the instruction: give your best N for a cap, but fill every slot for a split.',
    cite: MS('p.16'),
  },
};

// ─────────────── EN9 · Marking Out is credited before you cut ───────────────

const EN9: GridSession = {
  mode: 'grid',
  id: 'en-markingout',
  subject: 'engineering',
  level: 'common',
  title: 'Marking out scores before a single cut',
  cue: 'Practical',
  question:
    'In the Practical, each individual part is marked as four separate 5-mark concept marks. For Part 11 these are Marking Out (5), the 10 mm × 3 mm Slots (5), Length & Ø5.5 mm Holes (5) and the Top Profile (5). A candidate rushes the layout — measures by eye, skips the odd centre-punch — but then cuts the slots, holes and profile cleanly to those inaccurate lines. Mark the part.',
  questionNote:
    'Scenario authored for this exercise. The SEC Engineering Practical marks each part on separate 5-mark concept marks, and “Marking Out” is one of them in its own right (Part 11: Marking Out 5 + Slots 5 + Holes 5 + Profile 5).',
  grid: {
    perPoint: [
      { id: 'marking', label: 'Marking Out', marks: 5 },
      { id: 'slots', label: '10 mm × 3 mm Slots', marks: 5 },
      { id: 'holes', label: 'Length & Ø5.5 mm Holes', marks: 5 },
      { id: 'profile', label: 'Top Profile', marks: 5 },
    ],
    shorthand: 'Part 11: Marking Out 5 + Slots 5 + Holes 5 + Profile 5 (/20)',
    ruleNote:
      'Marking Out is a concept mark in its own right, scored separately from the cutting. Accurate layout is credited before any material is removed — so rushed, inaccurate marking out forfeits its 5 even when the subsequent cuts are clean. (Cutting neatly to inaccurate lines also lands the part off-dimension, putting the other marks at risk too.)',
    cite: MS('p.32 (Practical Part 11: Marking Out 5 + Slots 5 + Holes 5 + Top Profile 5)'),
  },
  scripts: [
    {
      id: 'en9-a',
      label: 'Script A',
      persona: 'Rushes the layout, cuts well',
      attempts: [
        {
          id: 'en9-a-1',
          text: 'Marks out by eye and skips centre-punching, then cuts the slots, drills the holes and files the top profile cleanly to the (inaccurate) lines.',
          key: { marking: 0, slots: 5, holes: 5, profile: 5 },
          keyNote:
            'The three cutting concept marks are earned, but Marking Out is a separate 5 and rushed layout loses it outright — a quarter of the part, gone before the first cut. Careful measuring and centre-punching would have banked it (and kept the cuts on dimension, protecting the rest).',
        },
      ],
      embodies: {
        behaviour:
          'Treats marking out as unmarked preparation and rushes it, dropping the separately-credited Marking Out concept mark.',
        cite: MS('p.32'),
      },
    },
    {
      id: 'en9-b',
      label: 'Script B',
      persona: 'Marks out accurately first',
      attempts: [
        {
          id: 'en9-b-1',
          text: 'Measures and marks out accurately, centre-punches every hole, then cuts the slots, holes and profile to those lines.',
          key: { marking: 5, slots: 5, holes: 5, profile: 5 },
          keyNote:
            'Accurate marking out banks its own 5 and sets up the cuts to land on dimension. Full 20 — the layout was worth a clean 5 in its own right.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en9',
    rule: 'Marking out is a mark, not just preparation.',
    detail:
      'In the Practical each part splits into separate 5-mark concept marks, and Marking Out is one of them — credited before any material is removed. Rushed layout forfeits its 5 and sends the dimensioned cuts off-target. Take the time to measure and centre-punch accurately: it scores in its own right and protects every mark after it.',
    cite: MS('p.32'),
  },
};

// ─────────────── EN10 · Open design briefs accept any workable solution ───────────────

const EN10: GridSession = {
  mode: 'grid',
  id: 'en-design',
  subject: 'engineering',
  level: 'common',
  title: 'On an open design brief, any workable answer scores',
  cue: 'Suggest a mechanism',
  question:
    'A design part asks for a mechanism to move a component, and the scheme prints one worked solution flagged “Suggested solution — other valid solutions accepted”, worth 8 as a single granule. One candidate proposes a completely different mechanism from the printed one — but it genuinely achieves the required motion and is clearly explained. Another freezes, sure they don’t know “the” answer, and leaves it blank. Mark both.',
  questionNote:
    'Scenario authored for this exercise. Several design parts in the 2025 HL scheme are flagged “Suggested solution – other valid solutions accepted” (e.g. Q9(a)(i), Q9(c)(i)) — the printed mechanism is one example, and any workable alternative that meets the brief is credited.',
  grid: {
    perPoint: [{ id: 'mech', label: 'A workable mechanism that meets the brief', marks: 8 }],
    shorthand: 'Single 8-mark granule — any valid mechanism',
    ruleNote:
      'On a design brief there is no single “correct” mechanism. The printed solution is flagged as suggested only, and any workable alternative that achieves the required motion scores full. The one answer that scores nothing is a blank — so a plausible, explained mechanism always beats leaving it empty.',
    cite: MS('p.28 (Q9(a)(i): “Suggested solution – other valid solutions accepted”)'),
  },
  scripts: [
    {
      id: 'en10-a',
      label: 'Script A',
      persona: 'Different mechanism, genuinely works',
      attempts: [
        {
          id: 'en10-a-1',
          text: 'Proposes a rack-and-pinion drive instead of the belt drive printed in the scheme, and explains how it produces the required movement.',
          key: { mech: 8 },
          keyNote:
            '“Other valid solutions accepted” means exactly this: a different mechanism that genuinely does the job earns full marks. 8/8. Don’t discard a workable idea just because it isn’t the one printed in the book.',
        },
      ],
    },
    {
      id: 'en10-b',
      label: 'Script B',
      persona: 'Freezes and leaves it blank',
      attempts: [
        {
          id: 'en10-b-1',
          text: 'Cannot recall a “standard” answer, worries anything else will be marked wrong, and leaves the part blank.',
          key: { mech: 0 },
          keyNote:
            'The only answer that cannot score is no answer. A blank is a guaranteed 0, whereas any explained mechanism that meets the brief would have been credited. On open design parts, always commit to a workable solution.',
        },
      ],
      embodies: {
        behaviour:
          'Leaves an open design part blank for fear of not matching the printed solution, on a part where any valid mechanism is accepted.',
        cite: MS('p.28'),
      },
    },
  ],
  takeaway: {
    id: 'codex-en10',
    rule: 'On an open design brief, commit to any workable solution.',
    detail:
      'Design parts print a “suggested solution” and accept any valid alternative that meets the brief, so there is no single answer to recall. A different-but-workable, clearly-explained mechanism scores full; only a blank scores nothing. Never leave a design part empty — sketch and explain a mechanism that does the job.',
    cite: MS('p.28'),
  },
};

// ─────────────── EN11 · Equal splits reward breadth, not depth ───────────────

const EN11: GridSession = {
  mode: 'grid',
  id: 'en-breadth',
  subject: 'engineering',
  level: 'common',
  title: 'An N + N split wants N points, not one deep one',
  cue: 'Give two reasons',
  question:
    'A part is marked 4 + 4: two separate points, four marks each. It is the opposite of the 3 + 2 “explain” pattern, which rewards developing one point in depth. A candidate makes a single excellent point and develops it over most of a page — but never offers a second. Mark it.',
  questionNote:
    'Scenario authored for this exercise. Based on Q4(a)(i) in the 2025 HL scheme — surface hardening giving “increased resistance to both fatigue failure and abrasive wear”, marked 4 + 4 (two distinct benefits, four marks each). An equal N + N split allocates one mark-block per required point; depth on a single point cannot reach into the second block.',
  grid: {
    perPoint: [
      { id: 'point1', label: 'First point (made and developed)', marks: 4 },
      { id: 'point2', label: 'Second point (made and developed)', marks: 4 },
    ],
    shorthand: '4 + 4 (two distinct points)',
    ruleNote:
      'An equal N + N split tells you how many separate points to give — one mark-block each. It is the mirror of the 3 + 2 pattern: 3 + 2 rewards developing one point in depth, but 4 + 4 (or 3 + 3) rewards breadth, two points of equal weight. A single point, however brilliant, can only ever fill its own block — the second block needs a second point.',
    cite: MS('p.14 (Q4(a)(i): resistance to both fatigue failure and abrasive wear @ 4 + 4)'),
  },
  scripts: [
    {
      id: 'en11-a',
      label: 'Script A',
      persona: 'One point, developed at length',
      attempts: [
        {
          id: 'en11-a-1',
          text: 'Explains one benefit of surface hardening — increased resistance to abrasive wear — thoroughly and at length, but never offers a second, distinct benefit.',
          key: { point1: 4, point2: 0 },
          keyNote:
            'The one developed point earns its 4, but the second 4-mark block needs a second, distinct point and there isn’t one — extra depth on the first cannot spill into it. Naming a second benefit (resistance to fatigue failure) in a line or two would have banked the other 4. In a 4 + 4, two solid points beat one exhaustive one.',
        },
      ],
      embodies: {
        behaviour:
          'Treats an equal 4 + 4 split like a 3 + 2 depth question, developing one point instead of giving the two the split calls for.',
        cite: MS('p.14'),
      },
    },
    {
      id: 'en11-b',
      label: 'Script B',
      persona: 'Two distinct points',
      attempts: [
        {
          id: 'en11-b-1',
          text: 'Gives two distinct benefits — resistance to abrasive wear and resistance to fatigue failure — each stated and briefly developed.',
          key: { point1: 4, point2: 4 },
          keyNote: 'Two points, one per block, each developed enough. Full 8 — the split asked for breadth and got it.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en11',
    rule: 'Let an equal split tell you how many points to give.',
    detail:
      'A 4 + 4 or 3 + 3 split allocates one mark-block per required point — it rewards breadth, unlike the 3 + 2 “explain” pattern that rewards depth on one point. Depth on a single point can only fill its own block. Count the blocks in the shorthand and give that many distinct points.',
    cite: MS('p.14'),
  },
};

// ─────────────── EN12 · Every practical section is worth 30 scaled marks ───────────────

const EN12: GridSession = {
  mode: 'grid',
  id: 'en-sections',
  subject: 'engineering',
  level: 'common',
  title: 'Finish every section — each is worth 30 scaled marks',
  cue: 'Practical',
  question:
    'The Practical is five sections of 20 marks — the assembled test-piece (Assembly/Function/Finish) plus four individual parts — totalling 100, which is then scaled ×1.5 to 150. A candidate finishes four sections to a high standard but runs out of time and never starts the fifth part. Mark the practical.',
  questionNote:
    'Scenario authored for this exercise. The 2025 HL Practical marking grid is five sections @ 20 marks = 100, scaled ×1.5 to 150. Each section is marked independently, so an unstarted section is a full 20 (30 after scaling) forfeited.',
  grid: {
    perPoint: [
      { id: 'sec1', label: 'Section 1 — test-piece (Assembly/Function/Finish)', marks: 20 },
      { id: 'sec2', label: 'Section 2 — Part 11', marks: 20 },
      { id: 'sec3', label: 'Section 3 — Parts 2', marks: 20 },
      { id: 'sec4', label: 'Section 4 — Parts 7 & 9', marks: 20 },
      { id: 'sec5', label: 'Section 5 — Part 10', marks: 20 },
    ],
    shorthand: '5 sections @ 20 = 100 (× 1.5 = 150)',
    ruleNote:
      'The five sections are marked independently and then the 100-mark total is scaled ×1.5 to 150 — so each 20-mark section is really worth 30. An unstarted section cannot be offset by polish elsewhere: it is a flat 20 (30 scaled) lost. Budgeting time to at least attempt all five beats perfecting four and running out.',
    cite: MS('p.32 (Practical: five sections @ 20 = 100 Marks × 1.5 = 150 Total)'),
  },
  scripts: [
    {
      id: 'en12-a',
      label: 'Script A',
      persona: 'Four sections perfect, fifth unstarted',
      attempts: [
        {
          id: 'en12-a-1',
          text: 'Completes the test-piece and three parts to a high standard, but runs out of time and never starts Part 10 (Section 5).',
          key: { sec1: 20, sec2: 20, sec3: 20, sec4: 20, sec5: 0 },
          keyNote:
            '80/100 before scaling — but that unstarted section is a full 20, which is 30 marks after the ×1.5 scaling. No amount of polish on the other four can reach into it. Even a rough attempt at Part 10 would have clawed back marks the finished parts simply cannot.',
        },
      ],
      embodies: {
        behaviour:
          'Perfects four practical sections at the cost of never attempting the fifth, forfeiting a full independent section worth 30 scaled marks.',
        cite: MS('p.32'),
      },
    },
    {
      id: 'en12-b',
      label: 'Script B',
      persona: 'Attempts all five sections',
      attempts: [
        {
          id: 'en12-b-1',
          text: 'Budgets time to attempt all five sections — four to a high standard and the fifth solidly, if less polished.',
          key: { sec1: 20, sec2: 20, sec3: 20, sec4: 20, sec5: 20 },
          keyNote:
            'Attempting every section banks marks the abandoned-section script left behind. Spreading the time to reach all five — even if the last is less refined — is worth more than perfecting four and stopping.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-en12',
    rule: 'Attempt every practical section — each is worth 30 scaled marks.',
    detail:
      'The Practical is five independent 20-mark sections scaled ×1.5, so each is really worth 30 and an unstarted section cannot be offset elsewhere. Budget your time to at least attempt all five; a rough fifth section scores more than extra polish on the other four.',
    cite: MS('p.32'),
  },
};

export const ENGINEERING_CHAIR: ChairSubject = {
  id: 'engineering',
  label: 'Engineering',
  tagline: 'Answer the number asked, match the mark split, label the diagram, unit the answer, finish every part.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [EN1, EN2, EN3, EN4, EN5, EN6, EN7, EN8, EN9, EN10, EN11, EN12],
  sources: [
    { label: 'SEC LC Engineering HL marking scheme 2025 (examiner-reports/engineering/2025-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general marking conventions — the “Any N” cap and its itemised “answer all” mirror, the point+development and equal-split (breadth) patterns, separately-credited labels, the single-granule calculation (formula → substitution → answer with unit), the “examples only / valid alternatives accepted” rule for both fixed answers and open design briefs, the Irish-language bonus, and the Practical’s concept marks (Assembly/Function/Finish, separately-credited Marking Out, and five independent ×1.5-scaled sections) — which apply at both Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked questions are being added.',
};
