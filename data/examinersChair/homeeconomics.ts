/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Home Economics (S&S, Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the coarse 5:3:0 point ladder that pays nothing for a thin
 * point, the per-heading distribution rule, and the low all-or-nothing "name"
 * mark) is the real SEC system, cited to:
 *  - SEC LC Home Economics HL marking scheme 2025 —
 *    examiner-reports/home-economics/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Home Economics HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Home Economics OL marking scheme 2025, ${p}` });

const ladder = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── HE1 · The 5:3:0 ladder ───────────────

const HE1: ScaleSession = {
  mode: 'scale',
  id: 'he-coarse-ladder',
  subject: 'home-economics',
  level: 'higher',
  title: 'Half a point scores nothing',
  cue: 'Discuss',
  question: 'A 20-mark “Discuss” part is marked as points on a 5:3:0 ladder — a well-developed point earns 5, a partial one earns 3, and a thin/undeveloped point earns 0. The candidate writes a correct but one-line, undeveloped point. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Many 20-mark Home Economics parts use a coarse 5:3:0 ladder — there is no 1 or 2 for a thin point; it is develop-it-or-score-nothing.',
  scale: {
    name: 'Point · 5:3:0 ladder',
    levels: ladder([0, 3, 5]),
    notes: [
      'This part marks each point 5 : 3 : 0 — no 1s or 2s.',
      '5 = a well-developed point; 3 = partially developed; 0 = a thin, undeveloped point.',
      'A correct but one-line point falls to 0 — there is no consolation mark.',
    ],
    cite: MS('p.13, p.16 (5:3:0 ladders on 20-mark parts)'),
  },
  scripts: [
    {
      id: 'he1-a',
      label: 'The answer',
      persona: 'Correct — but one line',
      work: ['A correct point, stated in a single undeveloped line.'],
      keyLevelId: 'm0',
      keyNote:
        '0 — the 5:3:0 ladder gives nothing for a thin point, and a bare correct statement is a thin point. One extra sentence of development (why it matters, an example) would jump it to 3 or 5. On these questions, a few developed points beat a long list of one-liners every time.',
      embodies: {
        behaviour: 'Writes correct but undeveloped one-line points, which the 5:3:0 ladder scores 0.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he1',
    rule: 'Develop the point, or it scores nothing.',
    detail:
      'Home Economics’ big “Discuss/Analyse” parts use a 5:3:0 ladder — a thin, one-line point earns 0, not a consolation mark. Develop each point (say why, give an example); a few developed points beat many bullet-listed ones.',
    cite: MS('p.13'),
  },
};

// ─────────────── HE2 · Spread across the headings ───────────────

const HE2: GridSession = {
  mode: 'grid',
  id: 'he-headings',
  subject: 'home-economics',
  level: 'higher',
  title: 'Spread across the headings',
  cue: 'Discuss (structured)',
  question: 'A part asks for points on food safety and requires: 1 point on storage, 1 on cooking/reheating, and 2 “other” points. A candidate writes four excellent points — but all four are about storage.',
  questionNote:
    'Scenario authored for this exercise. Structured Home Economics parts require points spread across named headings before free “other” points unlock; each named heading is capped independently.',
  grid: {
    perPoint: [
      { id: 'storage', label: 'Storage point', marks: 5 },
      { id: 'cooking', label: 'Cooking / reheating point', marks: 5 },
      { id: 'other1', label: '“Other” point', marks: 5 },
      { id: 'other2', label: '“Other” point', marks: 5 },
    ],
    shorthand: '1 storage, 1 cooking, 2 others',
    ruleNote:
      'The named headings are capped independently: only one storage point can score, no matter how many you write. Extra storage points don’t roll over to fill the cooking or “other” slots — those marks are simply lost.',
    cite: MS('p.16 (per-heading distribution rule)'),
  },
  scripts: [
    {
      id: 'he2-a',
      label: 'The answer',
      persona: 'Four points, all storage',
      attempts: [
        {
          id: 'he2-a-1',
          text: 'Four excellent, well-developed points — every one about safe storage of food.',
          key: { storage: 5, cooking: 0, other1: 0, other2: 0 },
          keyNote: 'Only the first storage point scores — the storage heading is capped at one, and the other three excellent points have nowhere to land. 5 of 20. Spreading them (one storage, one cooking, two others) would have scored all 20 for the same effort.',
        },
      ],
      embodies: {
        behaviour: 'Loads all points under one heading, forfeiting the independently-capped other headings.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he2',
    rule: 'Put a point under every named heading first.',
    detail:
      'Structured Home Economics parts cap each named heading independently — four points under one heading score once. Cover every heading the question names before adding “other” points, or the surplus marks are lost.',
    cite: MS('p.16'),
  },
};

// ─────────────── HE3 · Naming is cheap ───────────────

const HE3: GridSession = {
  mode: 'grid',
  id: 'he-name-describe',
  subject: 'home-economics',
  level: 'higher',
  title: 'The marks are in the describing',
  cue: 'Name and describe',
  question: 'A “Name and describe one method of heat transfer” part gives 2 marks for the name and 4 for the description. The candidate names conduction correctly, then writes only “it transfers heat”.',
  questionNote:
    'Scenario authored for this exercise. In Home Economics “name and describe/evaluate” parts, the name is a low, often all-or-nothing mark; the description or evaluation carries the marks.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the method', marks: 2 },
      { id: 'describe', label: 'Describe it (developed)', marks: 4 },
    ],
    shorthand: 'name 2 + describe 4',
    ruleNote:
      'Naming is the cheap part — 2 marks, and often all-or-nothing. The description carries most of the marks, and a vague one-liner earns little of it. Where a question says “describe” or “evaluate”, that is where the marks live.',
    cite: MS('p.8 (name + describe split)'),
  },
  scripts: [
    {
      id: 'he3-a',
      label: 'Script A',
      persona: 'Names it, barely describes',
      attempts: [
        {
          id: 'he3-a-1',
          text: 'Conduction. It transfers heat.',
          key: { name: 2, describe: 0 },
          keyNote: 'The name earns its 2, but “it transfers heat” describes nothing specific — the 4 description marks, where the question’s value sits, are untouched. 2 of 6. A sentence about heat passing through direct contact between particles would earn them.',
        },
      ],
      embodies: {
        behaviour: 'Nails the cheap “name” mark but leaves the description — where the marks are — undeveloped.',
        cite: MS('p.8'),
      },
    },
    {
      id: 'he3-b',
      label: 'Script B',
      persona: 'Names and describes',
      attempts: [
        {
          id: 'he3-b-1',
          text: 'Conduction: heat passes directly through a material by contact between particles — e.g. a metal saucepan base heating on a hob.',
          key: { name: 2, describe: 4 },
          keyNote: 'Name (2) plus a specific, developed description with an example (4). Full 6 — the description is what turned a 2 into a 6.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-he3',
    rule: 'The marks are in the describing, not the naming.',
    detail:
      'In Home Economics “name and describe/evaluate” questions, the name is a small, often all-or-nothing mark; the real marks are in a developed description or evaluation. Spend your words there, not on the label.',
    cite: MS('p.8'),
  },
};

// ─────────────── HE4 · OL — never leave Section A blank ───────────────

const HE4: ScaleSession = {
  mode: 'scale',
  id: 'he-ol-section-a',
  subject: 'home-economics',
  level: 'ordinary',
  title: 'Guess it — never leave it blank',
  cue: 'Section A (OL)',
  question: 'An Ordinary Level Section A item (a true/false tick, or fill-the-blank) is marked all-or-nothing: 2 marks or 0, with no partial credit. A candidate isn’t sure of the answer and leaves it blank rather than guess. What’s the expected cost of leaving it blank versus guessing?',
  questionNote:
    'Scenario authored for this exercise. OL Section A items are graded 2:0 (all-or-nothing). Because a blank and a wrong guess both score 0, guessing on an unknown item is pure upside.',
  scale: {
    name: 'OL Section A · 2:0',
    levels: [
      { id: 'm0', label: '0 (blank or wrong)', annotation: '0', marks: 0 },
      { id: 'm2', label: '2 (correct)', annotation: '2', marks: 2 },
    ],
    notes: [
      'OL Section A items score 2:0 — all-or-nothing, no partial credit.',
      'A blank scores 0. A wrong guess also scores 0. There is no penalty for a wrong answer.',
      'So on a true/false or fill-the-blank you don’t know, a guess can only help.',
    ],
    cite: MSOL('p.6–7 (Section A, graded 2:0)'),
  },
  scripts: [
    {
      id: 'he4-a',
      label: 'The decision',
      persona: 'Leaves it blank',
      work: ['Unsure of the answer.', 'Leaves the true/false item blank rather than guess.'],
      keyLevelId: 'm0',
      keyNote:
        'A guaranteed 0 — when a 50/50 guess would have scored 2 half the time for no downside. Section A is graded 2:0 with no penalty for a wrong answer, so leaving an item blank throws away free expected marks. Always put something down: on a true/false you can’t lose by guessing.',
      embodies: {
        behaviour: 'Leaves an all-or-nothing Section A item blank instead of guessing — forfeiting free expected marks.',
        cite: MSOL('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he4',
    rule: 'On OL Section A, always guess — never leave it blank.',
    detail:
      'Ordinary Level Section A items are graded 2:0 with no penalty for a wrong answer. A blank and a wrong guess both score 0, so guessing on a true/false or fill-the-blank you’re unsure of is pure upside. Never leave one blank.',
    cite: MSOL('p.6'),
  },
};

// ─────────────── HE5 · The count is a cap ───────────────

const HE5: GridSession = {
  mode: 'grid',
  id: 'he-point-cap',
  subject: 'home-economics',
  level: 'higher',
  title: 'The count is a cap, not a target',
  cue: 'Discuss (fixed count)',
  question:
    'A 20-mark part is marked as “4 points @ 5 marks”. A candidate plays it safe and writes six points — three fully developed, one left as a thin one-liner, plus two more strong points beyond the four the question marks. How does it score?',
  questionNote:
    'Scenario authored for this exercise. Home Economics parts marked “N points @ M marks” mark only N points — the count is a cap. Surplus points earn nothing (barring the examiner’s discretionary “Excess point” credit), so effort past the count is wasted.',
  grid: {
    perPoint: [
      { id: 'p1', label: 'Marked point 1', marks: 5 },
      { id: 'p2', label: 'Marked point 2', marks: 5 },
      { id: 'p3', label: 'Marked point 3', marks: 5 },
      { id: 'p4', label: 'Marked point 4', marks: 5 },
    ],
    shorthand: '4 points @ 5 — only four are marked',
    ruleNote:
      'Only four points are scored, no matter how many are written. The two surplus points are unmarked even though they are strong; the fourth marked point was left thin and scored 0. The time spent on points five and six should have finished the fourth.',
    cite: MS('p.13 (“4 points @ 5 marks”); p.4 (“Excess point awarded …” annotation)'),
  },
  scripts: [
    {
      id: 'he5-a',
      label: 'The answer',
      persona: 'Writes six, develops three',
      attempts: [
        {
          id: 'he5-a-1',
          text: 'Six points attempted: three fully developed, the fourth a thin one-liner, plus two further strong points beyond the four the question marks.',
          key: { p1: 5, p2: 5, p3: 5, p4: 0 },
          keyNote:
            'Only four points are marked. Three developed points score 5 each; the fourth is a thin one-liner and scores 0 on the ladder; the two surplus points are unmarked however good they are. 15 of 20 — the effort spent on the two extras should have developed the fourth point to a 5.',
        },
      ],
      embodies: {
        behaviour: 'Over-answers past the fixed point count, leaving a marked point thin while surplus points earn nothing.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he5',
    rule: 'Stop at the count and develop what you have.',
    detail:
      'Home Economics parts marked “N points @ M marks” score only N points — surplus points earn nothing. Write exactly the number asked and develop each fully; time spent on extra points is time stolen from the ones that count.',
    cite: MS('p.13'),
  },
};

// ─────────────── HE6 · Contradiction voids the mark ───────────────

const HE6: ScaleSession = {
  mode: 'scale',
  id: 'he-contradiction',
  subject: 'home-economics',
  level: 'higher',
  title: 'Contradict yourself and the mark is gone',
  cue: 'Discuss / Explain',
  question:
    'A point is marked on the 5:3:0 ladder. The candidate makes a correct, well-developed point — then, a few lines later, states the opposite and contradicts it. The scheme’s general instructions say content “not … contradicted … the marks may not be awarded”. What does the point score?',
  questionNote:
    'Scenario authored for this exercise. The 2025 scheme’s general instructions (p.3) let the examiner withhold marks where an answer contradicts itself — a developed, correct point can collapse to 0.',
  scale: {
    name: 'Point · 5:3:0 with the contradiction rule',
    levels: ladder([0, 3, 5]),
    notes: [
      'The point is graded 5:3:0 — 5 developed, 3 partial, 0 thin.',
      'General instructions: content “must be correctly used in context and not contradicted”.',
      'Where the answer contradicts itself, “the marks may not be awarded” — a correct, developed point can fall to 0.',
    ],
    cite: MS('p.3 (general instructions — contradiction voids the mark)'),
  },
  scripts: [
    {
      id: 'he6-a',
      label: 'The answer',
      persona: 'Right, then wrong',
      work: [
        'States a correct, fully developed point.',
        'A few lines later, asserts the opposite and contradicts the earlier point.',
      ],
      keyLevelId: 'm0',
      keyNote:
        '0 — on its own the developed point was a clean 5, but the later contradiction triggers the general-instruction rule that contradicted content “may not be awarded”. Make a point once, correctly, and don’t walk it back later in the answer.',
      embodies: {
        behaviour: 'Makes a correct, developed point then contradicts it later, so the scheme withholds the mark.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he6',
    rule: 'Never contradict a point you’ve already made.',
    detail:
      'The 2025 scheme lets examiners withhold marks where an answer contradicts itself — a correct, developed point can collapse to 0 if a later line states the opposite. Make each point once, correctly, and don’t undo it.',
    cite: MS('p.3'),
  },
};

// ─────────────── HE7 · Label the diagram ───────────────

const HE7: ScaleSession = {
  mode: 'scale',
  id: 'he-diagram-labels',
  subject: 'home-economics',
  level: 'higher',
  title: 'An unlabelled diagram earns nothing',
  cue: 'Describe (diagram accepted)',
  question:
    'A description point is worth 3 marks, and the scheme says “Accept labelled diagram” — a diagram can earn the point instead of prose. The candidate draws a neat, accurate diagram but writes no labels on it. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The 2025 scheme credits diagrams only as a labelled alternative to prose (“Accept labelled diagram”, “Accept clear diagrams”); an unlabelled diagram satisfies no marking point and scores 0.',
  scale: {
    name: 'Diagram credit · labelled or nothing',
    levels: [
      { id: 'd0', label: '0 (unlabelled — no point satisfied)', annotation: '0', marks: 0 },
      { id: 'd3', label: '3 (labelled — full description point)', annotation: '3', marks: 3 },
    ],
    notes: [
      'A diagram is credited only as an accepted alternative to the prose point.',
      'The scheme’s diagram credit is always conditional: “Accept labelled diagram” / “Accept clear diagrams”.',
      'An unlabelled diagram maps to no marking point — it scores 0, however neat.',
    ],
    cite: MS('p.8 (“Accept labelled diagram”); p.12 (“Accept clear diagrams”)'),
  },
  scripts: [
    {
      id: 'he7-a',
      label: 'Script A',
      persona: 'Neat, but no labels',
      work: ['Draws a neat, accurate diagram.', 'Adds no labels to any part of it.'],
      keyLevelId: 'd0',
      keyNote:
        '0 — the diagram is credited only as a labelled alternative to the written point, and an unlabelled drawing satisfies no marking point. Neatness earns nothing; the labels are the marks.',
      embodies: {
        behaviour: 'Submits an accurate but unlabelled diagram, which maps to no marking point.',
        cite: MS('p.8'),
      },
    },
    {
      id: 'he7-b',
      label: 'Script B',
      persona: 'Labels every part',
      work: ['Draws the same diagram.', 'Labels each relevant part clearly.'],
      keyLevelId: 'd3',
      keyNote:
        'Full 3 — the labelled diagram is the accepted alternative to the prose point, so it earns the description mark in full. The only difference from Script A is the labels.',
    },
  ],
  takeaway: {
    id: 'codex-he7',
    rule: 'Label every diagram — the labels are the marks.',
    detail:
      'Home Economics credits a diagram only as a labelled alternative to prose (“Accept labelled diagram”). An accurate but unlabelled diagram satisfies no marking point and scores 0. Always label every relevant part.',
    cite: MS('p.8'),
  },
};

// ─────────────── HE8 · Fill every attribute row ───────────────

const HE8: GridSession = {
  mode: 'grid',
  id: 'he-attribute-table',
  subject: 'home-economics',
  level: 'higher',
  title: 'Fill every row — the count is per attribute',
  cue: 'Detailed account (itemised)',
  question:
    'An 18-mark “detailed account of one food-poisoning bacteria” is itemised: name (2), 1 source (2), 2 high-risk foods (2 each), 3 factors affecting growth (2 each), 2 symptoms (2 each). A candidate names the bacteria, lists six high-risk foods and five growth factors in detail — but writes nothing on source or symptoms.',
  questionNote:
    'Scenario authored for this exercise. Itemised Home Economics accounts fix a separate count for each attribute row; extra items in one row never fill an empty row.',
  grid: {
    perPoint: [
      { id: 'name', label: 'Name the bacteria', marks: 2 },
      { id: 'source', label: 'Source (1)', marks: 2 },
      { id: 'foods', label: 'High-risk foods (2)', marks: 4 },
      { id: 'factors', label: 'Factors affecting growth (3)', marks: 6 },
      { id: 'symptoms', label: 'Symptoms (2)', marks: 4 },
    ],
    shorthand: 'name 2 + source 2 + foods 2@2 + factors 3@2 + symptoms 2@2',
    ruleNote:
      'Each attribute row has its own fixed count and its own marks. Only two high-risk foods and three factors are ever scored, however many you list; the surplus earns nothing. And an empty row scores 0 — the extra foods and factors cannot roll over to cover the missing source and symptoms.',
    cite: MS('p.15 (itemised food-poisoning account: name + 1 source + 2 foods + 3 factors + 2 symptoms)'),
  },
  scripts: [
    {
      id: 'he8-a',
      label: 'The answer',
      persona: 'Loads two rows, leaves two blank',
      attempts: [
        {
          id: 'he8-a-1',
          text: 'Names the bacteria, then lists six high-risk foods and five growth factors in detail — but writes nothing about the source or the symptoms.',
          key: { name: 2, source: 0, foods: 4, factors: 6, symptoms: 0 },
          keyNote:
            'Name (2), the two capped food marks (4) and the three capped factor marks (6) all score — but the surplus foods and factors past the count earn nothing, and the empty source and symptoms rows score 0. 12 of 18. The minutes spent on foods five and six and factors four and five should have gone on one source and two symptoms — 6 marks left on the table.',
        },
      ],
      embodies: {
        behaviour: 'Over-fills two attribute rows past their count while leaving two rows blank, forfeiting the blank rows’ marks.',
        cite: MS('p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he8',
    rule: 'Give something to every attribute the question lists.',
    detail:
      'Itemised Home Economics accounts fix a separate count for each attribute (1 source, 2 foods, 3 factors, 2 symptoms). Each row is capped, and a blank row scores 0 — surplus items in one row never cover a missing one. Serve every row before deepening any.',
    cite: MS('p.15'),
  },
};

// ─────────────── HE9 · Answer one Section C question ───────────────

const HE9: ScaleSession = {
  mode: 'scale',
  id: 'he-section-c-discount',
  subject: 'home-economics',
  level: 'higher',
  title: 'A second Section C question is discounted',
  cue: 'Section C (elective choice)',
  question:
    'Section C is answered with exactly one question. A candidate who submitted Textiles coursework answers C2 (Textiles) as required, then — to be safe — also fully answers C4 (Core). The scheme applies a discount so only the greatest mark counts, and the C4 answer scores lower. What does the second answer add to the total?',
  questionNote:
    'Scenario authored for this exercise. The 2025 scheme’s Section C rule counts only the greatest mark when a candidate answers C2 and another Section C question — a discount (annotation A) wipes the lesser.',
  scale: {
    name: 'Section C · greatest-mark-only',
    levels: [
      { id: 'sc-disc', label: '0 (discounted — only the greatest counts)', annotation: 'A', marks: 0 },
      { id: 'sc-face', label: 'Its face value (if it counted)', annotation: '—', marks: 35 },
    ],
    notes: [
      'Section C is answered with one question only.',
      'Where a candidate answers C2 (Textiles) and another Section C question, “the examiner applies a discount mark so that only the greatest mark is counted”.',
      'The lesser answer is wiped (annotation A) — every mark earned on it adds 0 to the total, however good it is.',
    ],
    cite: MS('p.5 (Section C discount — only the greatest mark counted)'),
  },
  scripts: [
    {
      id: 'he9-a',
      label: 'The answer',
      persona: 'Answers two Section C questions',
      work: [
        'Submitted Textiles coursework, so answers C2 (Textiles) as required.',
        'Also fully answers C4 (Core) “to be safe”.',
        'The C4 answer scores lower than the C2 answer.',
      ],
      keyLevelId: 'sc-disc',
      keyNote:
        '0 added — only the greatest of the two Section C answers counts, and the weaker one is discounted (annotation A). A whole extra question’s effort earns nothing. Answer exactly one Section C question and spend the saved time on Sections A and B.',
      embodies: {
        behaviour: 'Answers a second Section C question, which the discount rule wipes to 0.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he9',
    rule: 'Answer exactly one Section C question.',
    detail:
      'Section C counts only your greatest single answer — a second Section C question is discounted to 0 (annotation A). Over-answering here is pure wasted time; pick one elective (or the core) and put the rest of your time into Sections A and B.',
    cite: MS('p.5'),
  },
};

// ─────────────── HE10 · A near-miss name scores nothing ───────────────

const HE10: ScaleSession = {
  mode: 'scale',
  id: 'he-name-gate',
  subject: 'home-economics',
  level: 'higher',
  title: 'A near-miss name scores nothing',
  cue: 'Name (all-or-nothing)',
  question:
    'A part asks to “name one design principle”, marked “1 point @ 4 marks (graded 4:0)” — all-or-nothing, no partial credit. A candidate writes that the outfit “looks well put together and stylish” instead of naming a recognised design principle. What does the name score?',
  questionNote:
    'Scenario authored for this exercise. Some Home Economics “name” gates carry real weight (4 marks) but are graded x:0 — a vague or wrong term scores 0, with no partial credit for being close.',
  scale: {
    name: 'Name · graded 4:0',
    levels: [
      { id: 'ng0', label: '0 (not a recognised principle)', annotation: '0', marks: 0 },
      { id: 'ng4', label: '4 (correctly named)', annotation: '4', marks: 4 },
    ],
    notes: [
      'The name is worth 4 marks but graded 4:0 — all-or-nothing.',
      'A precise, recognised term (Balance, Proportion, Emphasis, Rhythm, Harmony) earns the full 4.',
      'A vague description that never names a principle earns 0 — there is no partial credit for being close.',
    ],
    cite: MS('p.22 (“Name one design principle 1 point @ 4 marks (graded 4:0)”)'),
  },
  scripts: [
    {
      id: 'he10-a',
      label: 'Script A',
      persona: 'Describes instead of naming',
      work: [
        'Writes that the outfit “looks well put together and stylish”.',
        'Never names an actual design principle.',
      ],
      keyLevelId: 'ng0',
      keyNote:
        '0 — the gate is graded 4:0, so anything short of the precise term scores nothing. A description of the effect is not the name of the principle; “Balance” or “Proportion” would have earned the full 4.',
      embodies: {
        behaviour: 'Answers a 4:0 “name” gate with a description instead of the recognised term, scoring 0.',
        cite: MS('p.22'),
      },
    },
    {
      id: 'he10-b',
      label: 'Script B',
      persona: 'Names it precisely',
      work: ['Names “Balance” as the design principle.'],
      keyLevelId: 'ng4',
      keyNote:
        'Full 4 — a recognised design principle, named precisely, clears the all-or-nothing gate. The single word is the whole mark.',
    },
  ],
  takeaway: {
    id: 'codex-he10',
    rule: 'On a “name” gate, give the exact term — close scores 0.',
    detail:
      'Where a Home Economics “name” point is graded x:0, it is all-or-nothing: the precise recognised term earns the full marks and a near-miss or a description earns nothing. Commit the exact vocabulary; there is no consolation for being close.',
    cite: MS('p.22'),
  },
};

// ─────────────── HE11 · Fluent, relevant — and still zero ───────────────

const HE11: ScaleSession = {
  mode: 'scale',
  id: 'he-key-phrases',
  subject: 'home-economics',
  level: 'higher',
  title: 'Fluent, relevant — and still zero',
  cue: 'Explain / Describe',
  question:
    'The scheme’s general instructions say “only key phrases are given which contain information and ideas that must appear in the candidate’s answer in order to merit the assigned marks”. A candidate writes a fluent, on-topic paragraph that circles the subject but never states the specific key idea the point is looking for. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The 2025 scheme (p.3) awards a point only when the specific required idea appears — a relevant-sounding answer that never lands the key phrase satisfies no marking point.',
  scale: {
    name: 'Point · key idea present or absent',
    levels: [
      { id: 'kp0', label: '0 (key idea never stated)', annotation: '0', marks: 0 },
      { id: 'kp5', label: '5 (key idea clearly made)', annotation: '5', marks: 5 },
    ],
    notes: [
      'A point scores only when the specific information/idea the scheme lists “must appear in the candidate’s answer”.',
      'Fluency and relevance are not the test — landing the required idea is.',
      'An answer that talks around the topic without stating the key point maps to no marking point and scores 0.',
    ],
    cite: MS('p.3 (“…ideas that must appear in the candidate’s answer in order to merit the assigned marks”)'),
  },
  scripts: [
    {
      id: 'he11-a',
      label: 'The answer',
      persona: 'Talks around it',
      work: [
        'Writes a fluent, on-topic paragraph.',
        'Circles the subject but never states the specific key idea the point requires.',
      ],
      keyLevelId: 'kp0',
      keyNote:
        '0 — length and relevance do not earn the mark; the key idea has to actually appear. The examiner is looking for a specific information/idea, and it is not on the page. Name the point directly, then develop it — don’t hope a relevant-sounding sentence will be read as making it.',
      embodies: {
        behaviour: 'Writes a fluent, relevant answer that never states the required key idea, so no marking point is satisfied.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he11',
    rule: 'State the key idea outright — relevance isn’t the mark.',
    detail:
      'A point scores only when the specific idea the scheme is looking for actually appears in your answer. A fluent, on-topic paragraph that never lands the key phrase scores 0. Say the point directly, then develop it.',
    cite: MS('p.3'),
  },
};

// ─────────────── HE12 · Back the recommendation with the data ───────────────

const HE12: ScaleSession = {
  mode: 'scale',
  id: 'he-data-reasons',
  subject: 'home-economics',
  level: 'ordinary',
  title: 'Back the recommendation with the data',
  cue: 'Recommend (from a data table)',
  question:
    'Reading a nutrition-label table for two convenience soups, a candidate recommends one and gives a reason: “Soup A is the healthier, better choice.” The reasons are marked on a 5:3:2:0 ladder and the model reasons quote the table figures (lower in kcal, higher in protein/fibre …). What does this reason score?',
  questionNote:
    'Scenario authored for this exercise. The 2025 OL data-interpretation part credits reasons drawn from the figures in the table; a generic value judgement that cites no data satisfies no marking point.',
  scale: {
    name: 'Reason · 5:3:2:0 (data-grounded)',
    levels: [
      { id: 'dr0', label: '0 (no data — generic judgement)', annotation: '0', marks: 0 },
      { id: 'dr2', label: '2 (a figure, undeveloped)', annotation: '2', marks: 2 },
      { id: 'dr3', label: '3 (a figure, partly linked)', annotation: '3', marks: 3 },
      { id: 'dr5', label: '5 (figure linked to a nutritional reason)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Each reason is graded 5:3:2:0 — note there is no 4 and no 1.',
      'The scheme’s reasons all quote the table: “lower in kcal … higher in protein for growth/repair … higher in fibre for digestion”.',
      'A reason that names a figure and links it to a nutritional benefit earns 5; a bare value judgement with no data earns 0.',
    ],
    cite: MSOL('p.10 (“state which soup you would recommend … four reasons”; reasons @ 5 graded 5:3:2:0)'),
  },
  scripts: [
    {
      id: 'he12-a',
      label: 'The answer',
      persona: 'Opinion, no data',
      work: ['Recommends Soup A.', 'Reason given: “Soup A is the healthier, better choice.”'],
      keyLevelId: 'dr0',
      keyNote:
        '0 — the reason cites nothing from the table. “Healthier” is the conclusion, not a reason. “Soup A is lower in kcal, which helps prevent obesity” names a figure and links it to a benefit — that is the 5. On a data question, quote the number and say what it does.',
      embodies: {
        behaviour: 'Gives a generic value judgement instead of a reason drawn from the data table, scoring 0.',
        cite: MSOL('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he12',
    rule: 'On a data question, quote the figure and say what it does.',
    detail:
      'Data-interpretation parts credit reasons drawn from the table — a figure linked to a nutritional benefit. A generic “it’s healthier” cites no data and scores 0. Name the number, then explain why it matters.',
    cite: MSOL('p.10'),
  },
};

// ─────────────── HE13 · Coursework is banded on competence ───────────────

const HE13: ScaleSession = {
  mode: 'scale',
  id: 'he-coursework-bands',
  subject: 'home-economics',
  level: 'ordinary',
  title: 'Coursework is banded on competence, not fact-count',
  cue: 'Food Studies coursework — Investigation',
  question:
    'The 24-mark coursework Investigation is marked in competence bands, not point-by-point: Band A 19–24 (very good–excellent), B 13–18, C 7–12, D 0–6. Band A needs “thorough exploration and comprehensive analysis … uses evidence from research as basis for making relevant choices”. A candidate’s Investigation is an accurate but list-like set of facts with no analysis and no link to the dish chosen. Which band?',
  questionNote:
    'Scenario authored for this exercise. Coursework Investigation/Procedure/Evaluation blocks are graded on A/B/C/D competence bands, not the point-ladder used on the written paper.',
  scale: {
    name: 'Investigation · competence bands (/24)',
    levels: [
      { id: 'bd', label: 'Band D 0–6 (very basic – limited)', annotation: 'D', marks: 4 },
      { id: 'bc', label: 'Band C 7–12 (basic – competent)', annotation: 'C', marks: 10 },
      { id: 'bb', label: 'Band B 13–18 (very competent – good)', annotation: 'B', marks: 15 },
      { id: 'ba', label: 'Band A 19–24 (very good – excellent)', annotation: 'A', marks: 22 },
    ],
    notes: [
      'The Investigation is banded, not point-marked — the examiner places the whole piece in one band, then a mark within it.',
      'Band A needs thorough exploration AND comprehensive analysis AND research used to justify the menu/dish choices.',
      'A list of accurate facts with no analysis and no link to the chosen dish is exploration without analysis — Band C, not Band A.',
    ],
    cite: MSOL('p.26 (Investigation 24 marks; Bands A 19–24 / B 13–18 / C 7–12 / D 0–6)'),
  },
  scripts: [
    {
      id: 'he13-a',
      label: 'The answer',
      persona: 'Facts, no analysis',
      work: [
        'Presents accurate, relevant facts from a range of sources.',
        'Offers no analysis and never links the research to the dish chosen.',
      ],
      keyLevelId: 'bc',
      keyNote:
        'Band C (≈10 of 24) — the facts are accurate and sourced, but the jump to Band A/B needs analysis and research used to justify the choices, and neither is there. Accuracy alone is “exploration”; the marks are in analysing and applying it. Bands are decided by what you do with the facts, not how many you list.',
      embodies: {
        behaviour: 'Submits accurate facts with no analysis or application, capping the Investigation at the competent band.',
        cite: MSOL('p.26'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he13',
    rule: 'Coursework rewards analysis and application, not fact-count.',
    detail:
      'The coursework Investigation is banded on competence: accurate facts alone are only the “explored” band. Reaching the top band needs analysis of the facts and research used to justify your menu and dish choices. Do something with the information — don’t just list it.',
    cite: MSOL('p.26'),
  },
};

// ─────────────── HE14 · A wrong dish costs a flat −8 ───────────────

const HE14: ScaleSession = {
  mode: 'scale',
  id: 'he-coursework-sc',
  subject: 'home-economics',
  level: 'ordinary',
  title: 'A wrong dish costs a flat −8',
  cue: 'Food Studies coursework — practical',
  question:
    'The assignment specifies a cooked main course. A candidate prepares a beautifully executed dish — but it is a dessert, not a main course. The scheme’s SC (“Scenario applied”) annotation applies “an 8 mark deduction (−8 marks)” for a dish “not fully compliant with requirements”. How much does the non-compliance cost?',
  questionNote:
    'Scenario authored for this exercise. The SC deduction is a flat −8 for a non-compliant dish (wrong course, uncooked where cooked is required, over-use of convenience foods), applied on top of the practical marks after Advising-Examiner consultation.',
  scale: {
    name: 'Dish compliance · SC deduction',
    levels: [
      { id: 'sc-8', label: '−8 (SC — dish not compliant)', annotation: 'SC', marks: -8 },
      { id: 'sc-0', label: '0 (dish compliant — no deduction)', annotation: '—', marks: 0 },
    ],
    notes: [
      'SC is a flat penalty, not pro-rata: “this annotation applies an 8 mark deduction (−8 marks)”.',
      'It triggers when the dish is “not fully compliant with requirements” — wrong course, uncooked where cooked is specified, over-use of convenience foods.',
      'Execution quality does not soften it — a perfectly cooked dessert where a main course was required still loses the flat 8.',
    ],
    cite: MSOL('p.25 (“SC … applies an 8 mark deduction (−8 marks) … Dish selected not fully compliant with requirements”)'),
  },
  scripts: [
    {
      id: 'he14-a',
      label: 'The answer',
      persona: 'Great dish, wrong brief',
      work: [
        'The assignment specifies a cooked main course.',
        'Prepares a beautifully executed dessert instead.',
      ],
      keyLevelId: 'sc-8',
      keyNote:
        '−8, flat — the SC deduction is applied for a non-compliant dish regardless of how well it is cooked, and the practical marks earned are then reduced by the full 8. Read the brief’s requirements (course, cooked/uncooked, no convenience-food overload) before choosing the dish; skill can’t buy back an SC.',
      embodies: {
        behaviour: 'Prepares a well-executed but non-compliant dish, triggering the flat SC −8 deduction.',
        cite: MSOL('p.25'),
      },
    },
  ],
  takeaway: {
    id: 'codex-he14',
    rule: 'Match the dish to the brief — SC is a flat −8.',
    detail:
      'A coursework dish that breaks the brief (wrong course, uncooked where cooked is required, over-reliance on convenience foods) triggers a flat −8 SC deduction that execution quality cannot offset. Check the requirements before choosing the dish.',
    cite: MSOL('p.25'),
  },
};

// ─────────────── HE15 · The example can be worth double a detail ───────────────

const HE15: GridSession = {
  mode: 'grid',
  id: 'he-mark-weight',
  subject: 'home-economics',
  level: 'higher',
  title: 'The example can be worth double a detail',
  cue: 'Describe and give an example',
  question:
    'A “describe the structure and give one example” part is marked “4 points on structure @ 1 mark + 1 example @ 2 marks” (6 marks for the type). A candidate writes four solid structure points and, thinking the example is a throwaway, skips it.',
  questionNote:
    'Scenario authored for this exercise. Home Economics mark allocations are not uniform — here each structure detail is worth 1 but the single example is worth 2, so the “throwaway” example is worth double a detail.',
  grid: {
    perPoint: [
      { id: 's1', label: 'Structure point 1', marks: 1 },
      { id: 's2', label: 'Structure point 2', marks: 1 },
      { id: 's3', label: 'Structure point 3', marks: 1 },
      { id: 's4', label: 'Structure point 4', marks: 1 },
      { id: 'example', label: 'Example', marks: 2 },
    ],
    shorthand: '4 structure @ 1 + 1 example @ 2',
    ruleNote:
      'The marks are not spread evenly: each structure point is worth 1, but the single example is worth 2 — double any one detail. Skipping the example to add a fifth structure point is a bad trade (the fifth point is unmarked anyway; the example was worth two of the four you wrote).',
    cite: MS('p.12 (“4 points on structure @ 1 mark … 1 example @ 2 marks”)'),
  },
  scripts: [
    {
      id: 'he15-a',
      label: 'Script A',
      persona: 'Skips the “throwaway” example',
      attempts: [
        {
          id: 'he15-a-1',
          text: 'Four solid structure points; no example given.',
          key: { s1: 1, s2: 1, s3: 1, s4: 1, example: 0 },
          keyNote:
            '4 of 6 — every structure mark earned, but the example, worth 2, is missing. One named example (e.g. stearic acid) was worth as much as two of the structure points; leaving it out was the costliest omission on the part.',
        },
      ],
      embodies: {
        behaviour: 'Skips the highest-value single item (the example) assuming it is a throwaway.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'he15-b',
      label: 'Script B',
      persona: 'Includes the example',
      attempts: [
        {
          id: 'he15-b-1',
          text: 'Three structure points and one named example.',
          key: { s1: 1, s2: 1, s3: 1, s4: 0, example: 2 },
          keyNote:
            '5 of 6 from fewer items than Script A wrote — three structure points (3) plus the example (2). The one example outscored a structure point, so this shorter answer beats the longer one that skipped it.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-he15',
    rule: 'Read the allocation — the example may be worth most.',
    detail:
      'Home Economics does not spread marks evenly. When each detail is worth 1 but the example is worth 2, the example is the highest-value single item on the part. Never skip a required example as a “throwaway”; check where the marks actually sit.',
    cite: MS('p.12'),
  },
};

export const HOME_ECONOMICS_CHAIR: ChairSubject = {
  id: 'home-economics',
  label: 'Home Economics',
  tagline: 'Develop your points, spread the headings, describe don’t just name — and never contradict yourself.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [HE1, HE2, HE3, HE4, HE5, HE6, HE7, HE8, HE9, HE10, HE11, HE12, HE13, HE14, HE15],
  sources: [
    { label: 'SEC LC Home Economics HL marking scheme 2025 (examiner-reports/home-economics/2025-marking-scheme)' },
    { label: 'SEC LC Home Economics OL marking scheme 2025 (examiner-reports/home-economics/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The written-paper sessions — point-ladder, per-heading spread, itemised attribute counts, name-vs-describe, the all-or-nothing name gate, fixed-count cap, key-idea, contradiction, diagram-label, mark-allocation and the Section C one-question rule — are verified against the 2025 Higher Level scheme and apply at both levels (OL ladders are even coarser — a half point often scores 0). The Ordinary sessions pin OL-specific rules: all-or-nothing Section A, data-interpretation reasons on the 5:3:2:0 ladder, the coursework competence bands, and the flat −8 SC deduction for a non-compliant dish. All conventions were cross-checked against the 2025 OL scheme.',
};
