/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Agricultural Science (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the front-loaded points list, the surplus-answer penalty,
 * the calculation method mark, and the IIS coursework's holistic five-band
 * rubric) is the real SEC system,
 * cited to:
 *  - SEC LC Agricultural Science HL marking scheme 2024 —
 *    examiner-reports/agricultural-science/2024-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Agricultural Science HL marking scheme 2024, ${p}` });

const bandScale = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: `${m} marks`, annotation: `${m}`, marks: m }));

// ─────────────── Ag1 · Front-loaded points ───────────────

const AG1: GridSession = {
  mode: 'grid',
  id: 'ag-frontload',
  subject: 'agricultural-science',
  level: 'common',
  title: 'The first point pays most',
  cue: 'Name / list',
  question: 'Name four breeds of dairy cattle. The line is marked 4 + 2 + 2 + 2 — the first correct breed earns 4 marks, each of the next three earns 2.',
  questionNote:
    'Question authored for this exercise. Front-loaded points lists are a standard Ag Science pattern: the first correct answer is worth more, each subsequent correct answer worth less.',
  grid: {
    perPoint: [
      { id: 'b1', label: '1st correct breed', marks: 4 },
      { id: 'b2', label: '2nd correct breed', marks: 2 },
      { id: 'b3', label: '3rd correct breed', marks: 2 },
      { id: 'b4', label: '4th correct breed', marks: 2 },
    ],
    shorthand: '4 + 2 + 2 + 2',
    ruleNote:
      'The first correct answer carries the biggest mark; the rest taper. So getting at least one solid answer down banks the most valuable mark — and leaving the line blank forfeits the easiest 4 on the question.',
    cite: MS('p.4 (front-loaded points list)'),
  },
  scripts: [
    {
      id: 'ag1-a',
      label: 'Script A',
      persona: 'One breed, then blanks',
      attempts: [
        {
          id: 'ag1-a-1',
          text: 'Holstein-Friesian.  (no other breeds given)',
          key: { b1: 4, b2: 0, b3: 0, b4: 0 },
          keyNote: 'One correct breed banks the front-loaded 4 marks — nearly half the line for a single word. Three more names would have added 6, but even this one answer is worth more than any that follow it. Never leave a naming line blank.',
        },
      ],
      embodies: {
        behaviour: 'Gives only one answer on a front-loaded line — still banks the largest mark.',
        cite: MS('p.4'),
      },
    },
    {
      id: 'ag1-b',
      label: 'Script B',
      persona: 'All four',
      attempts: [
        {
          id: 'ag1-b-1',
          text: 'Holstein-Friesian, Jersey, Montbéliarde, Norwegian Red.',
          key: { b1: 4, b2: 2, b3: 2, b4: 2 },
          keyNote: 'Four correct breeds: 4 + 2 + 2 + 2 = 10. Full marks — and note the first was worth as much as the last two combined.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ag1',
    rule: 'On front-loaded lines, the first answer is worth most.',
    detail:
      'Ag Science lists often pay 4 + 2 + 2 + 2 — the first correct answer carries the biggest mark. Always get at least one solid answer down (it banks the most), then add the rest; never leave the line blank.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ag2 · Surplus penalty ───────────────

const AG2: ScaleSession = {
  mode: 'scale',
  id: 'ag-surplus',
  subject: 'agricultural-science',
  level: 'common',
  title: 'When an extra guess costs you',
  cue: 'Name',
  question: 'Name one breed of sheep. The candidate, hedging, writes two: “Texel, and also the Charolais.” One is a sheep breed; the other is a cattle breed. The line is worth 4 marks. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme applies a surplus-answer penalty: a surplus wrong answer cancels a correct one (worked in the scheme as 4 − 1 = 3 on a similar breed-ID line).',
  scale: {
    name: 'Surplus wrong answer',
    levels: bandScale([0, 4]),
    notes: [
      'The question asks for ONE breed; the candidate offers two.',
      'Texel is a sheep breed (correct); Charolais is a cattle breed (wrong here).',
      'Surplus-answer rule: a surplus wrong answer cancels a correct one.',
      'So the extra wrong breed cancels the right one — the line is dragged down.',
    ],
    cite: MS('p.4 (surplus wrong answer cancels a correct one)'),
  },
  scripts: [
    {
      id: 'ag2-a',
      label: 'The answer',
      persona: 'Adds a second, wrong',
      work: ['Texel, and also the Charolais.', '(Texel = sheep ✓, Charolais = cattle ✗)'],
      keyLevelId: 'm0',
      keyNote:
        'The surplus wrong answer cancels the correct one — hedging turned a 4-mark answer into a loss. When the question asks for one, give one: “Texel” alone scores full marks. An unsure extra is not free; it can wipe out the mark you had.',
      embodies: {
        behaviour: 'Adds an unsure extra answer where one was asked — the surplus wrong answer cancels the correct one.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag2',
    rule: 'Give the number asked — an extra guess can cancel a right answer.',
    detail:
      'Ag Science cancels a correct answer with a surplus wrong one. If the question asks for one breed, give one; padding with an unsure extra can wipe out the mark you’d earned.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ag3 · IIS holistic marking ───────────────

const AG3: ScaleSession = {
  mode: 'scale',
  id: 'ag-iis-brevity',
  subject: 'agricultural-science',
  level: 'higher',
  title: 'Length isn’t the mark',
  cue: 'Coursework (IIS)',
  question: 'An Individual Investigative Study (IIS) section is marked as ONE holistic band, not point-by-point. One candidate writes a long, padded section; another writes a shorter, sharper one that covers the same substance well. How does the padding affect the mark?',
  questionNote:
    'Scenario authored for this exercise. Each IIS section is awarded a single holistic band mark (Excellent/Very Good/Good/Fair/Weak); the scheme warns markers not to penalise skilful brevity nor reward unwarranted length.',
  scale: {
    name: 'IIS section · holistic band',
    levels: [
      { id: 'weak', label: 'Weak', annotation: 'W', marks: 6 },
      { id: 'good', label: 'Good', annotation: 'G', marks: 14 },
      { id: 'vgood', label: 'Very Good', annotation: 'VG', marks: 18 },
      { id: 'excellent', label: 'Excellent', annotation: 'E', marks: 22 },
    ],
    notes: [
      'Each IIS section gets one holistic band mark, not additive points.',
      'The scheme: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.”',
      'Padding a section doesn’t raise its band — quality and coverage do.',
    ],
    cite: MS('p.7 (IIS holistic banding; brevity/length note)'),
  },
  scripts: [
    {
      id: 'ag3-a',
      label: 'The section',
      persona: 'Padded for length',
      work: [
        'A long section with lots of filler and repetition.',
        'The actual substance matches a shorter, sharper answer.',
      ],
      keyLevelId: 'good',
      keyNote:
        'The padding earns nothing — the section is judged on one holistic band, and length isn’t a band criterion. A concise answer with the same substance lands in the same band, in a fraction of the words. Spend the effort on depth and coverage, not volume.',
      embodies: {
        behaviour: 'Pads a coursework section for length, which the holistic banding does not reward.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag3',
    rule: 'Coursework is banded on quality, not length.',
    detail:
      'Each IIS section is one holistic band mark — the scheme explicitly won’t reward padding or punish skilful brevity. Write concisely and cover the substance well; volume alone never lifts the band.',
    cite: MS('p.7'),
  },
};

// ─────────────── Ag4 · Calculation method mark ───────────────

const AG4: ScaleSession = {
  mode: 'scale',
  id: 'ag-method-mark',
  subject: 'agricultural-science',
  level: 'common',
  title: 'The formula banks marks on its own',
  cue: 'Calculate',
  question:
    'Calculate the % soil organic matter in a peat sample (mass lost 55.2 g from a 90 g sample). The line is worth 6 marks. A candidate writes the correct formula — “55.2 / 90 × 100” — but slips the arithmetic and lands on 51.3 % instead of 61.3 %. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Ag Science calculation lines carry a method mark: the scheme credits the correct formula on its own, worked here as “correct formula without correct answer, award 3m” on a 6-mark % organic matter calculation.',
  scale: {
    name: 'Calculation · method mark',
    levels: [
      { id: 'zero', label: 'No credit', annotation: '0', marks: 0 },
      { id: 'method', label: 'Method mark', annotation: 'M', marks: 3 },
      { id: 'full', label: 'Full marks', annotation: '6', marks: 6 },
    ],
    notes: [
      'The final answer (51.3 %) is wrong, so full marks are off the table.',
      'But the formula “55.2 / 90 × 100” is the correct method — the scheme credits it on its own.',
      'Scheme: correct formula without the correct answer scores 3 of 6.',
      '(A correct answer with no working still scores the full 6 — but a wrong answer with no formula shown scores nothing.)',
    ],
    cite: MS('p.24 (correct formula without correct answer, award 3m)'),
  },
  scripts: [
    {
      id: 'ag4-a',
      label: 'The answer',
      persona: 'Right method, wrong arithmetic',
      work: ['55.2 / 90 × 100', '= 51.3 %  (arithmetic slip; correct value is 61.3 %)'],
      keyLevelId: 'method',
      keyNote:
        'The final number is wrong, but the correct formula banks the method mark — 3 of the 6. Had this candidate written only “51.3 %” with no working, the examiner would have nothing to credit and it scores 0. Always put the formula on the page before the arithmetic: it is half the marks, and it survives a slip on the calculator.',
      embodies: {
        behaviour: 'Shows the correct formula but fumbles the arithmetic — the method mark still banks half.',
        cite: MS('p.24'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag4',
    rule: 'Show the formula — the method banks marks even if the answer is wrong.',
    detail:
      'Ag Science calculation lines credit the correct formula on its own: a right method with a wrong final number still scores the method mark (here 3 of 6), while a wrong answer with no working shown scores nothing. Always write the working before the arithmetic — it is the half of the marks a calculator slip can’t take.',
    cite: MS('p.24'),
  },
};

// ─────────────── Ag5 · The context rule ───────────────

const AG5: ScaleSession = {
  mode: 'scale',
  id: 'ag-context',
  subject: 'agricultural-science',
  level: 'common',
  title: 'Right word, wrong statement',
  cue: 'Explain',
  question:
    'Explain one way earthworms improve soil structure. The line is worth 6 marks. A candidate writes: “Earthworms improve soil structure by compacting the soil so that air and water cannot pass through.” The key term “soil structure” is on the page — but does it score?',
  questionNote:
    'Scenario authored for this exercise. The context rule is real: a correct term embedded in a contradicted or incorrect statement is not credited — the scheme withholds the marks where there is evidence of incorrect use or contradiction.',
  scale: {
    name: 'Term used in context',
    levels: bandScale([0, 6]),
    notes: [
      'The keywords “soil structure” and “air and water” are all present.',
      'But the mechanism is contradicted: earthworms improve structure by burrowing and aerating, not by compacting so air and water cannot pass.',
      'Context rule: “words, expressions or phrases must be correctly used in context and not contradicted … the marks may not be awarded.”',
      'The right words in a contradicted statement earn nothing — this is not keyword-spotting.',
    ],
    cite: MS('p.3 (correctly used in context and not contradicted)'),
  },
  scripts: [
    {
      id: 'ag5-a',
      label: 'The answer',
      persona: 'Keywords present, mechanism wrong',
      work: [
        'Earthworms improve soil structure by compacting the soil',
        'so that air and water cannot pass through.',
        '(right terms — but the mechanism is the opposite of the truth)',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The term “soil structure” is on the page, but it sits inside a statement that contradicts the science — so the marks are withheld entirely. Examiners do not scan for keywords; the surrounding sentence has to be correct. Learn the mechanism, not just the vocabulary: “earthworms burrow and aerate the soil, improving structure” scores; the same words wrapped around the wrong process score nothing.',
      embodies: {
        behaviour: 'Uses the correct term inside a contradicted statement — the scheme withholds the marks.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag5',
    rule: 'A right term in a wrong statement scores nothing.',
    detail:
      'Ag Science only credits terms “correctly used in context and not contradicted”. Naming the keyword is not enough — if the surrounding sentence is wrong or self-contradicting, the marks are withheld. Get the mechanism right, then the vocabulary pays.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ag6 · Two versions, no manufactured total ───────────────

const AG6: ScaleSession = {
  mode: 'scale',
  id: 'ag-two-versions',
  subject: 'agricultural-science',
  level: 'common',
  title: 'You get the better version, not the sum',
  cue: 'Two versions of an answer',
  question:
    'Give three roles of water in a plant — the line is worth 6 marks (three points at 2). Unsure, the candidate answers twice without crossing anything out. Version 1: “transport of dissolved minerals; raw material for photosynthesis.” Version 2: “used in photosynthesis; keeps cells turgid for support.” Between them that is three distinct roles. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The rule is real: where two un-cancelled versions of an answer are given, the examiner marks both and accepts the greater — but may not combine points from both versions to arrive at a manufactured total.',
  scale: {
    name: 'Two un-cancelled versions',
    levels: bandScale([0, 4, 6]),
    notes: [
      'Version 1 scores two roles = 4; Version 2 scores two roles = 4 (photosynthesis overlaps).',
      'Rule: “mark both and accept the answer that yields the greater number of marks.”',
      '“You may not, however, combine points from both versions to arrive at a manufactured total.”',
      'So the distinct third role across the two versions cannot be added in — the line takes the better single version, 4, not 6.',
    ],
    cite: MS('p.4 (mark both, accept the greater; no manufactured total)'),
  },
  scripts: [
    {
      id: 'ag6-a',
      label: 'The answer',
      persona: 'Hedges with two versions',
      work: [
        'V1: transport of dissolved minerals; raw material for photosynthesis.',
        'V2: used in photosynthesis; keeps cells turgid for support.',
        '(three distinct roles across the two — but only within one version each)',
      ],
      keyLevelId: 'm4',
      keyNote:
        'The examiner marks both versions and keeps the better one — here each is worth 4 — but cannot stitch the unique point from each together into 6. Writing the answer twice does not bank more; it just picks your strongest single attempt. Put all three roles in one clear answer and the full 6 is there. Hedging with a second version caps you at the better of the two.',
      embodies: {
        behaviour: 'Splits the answer across two un-cancelled versions, hoping the points sum — the scheme takes the greater single version.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag6',
    rule: 'Two versions get you the better one, never the sum.',
    detail:
      'When a candidate leaves two un-cancelled answers, Ag Science marks both and awards the greater — it will not combine points from both into a manufactured total. Commit to one complete answer; splitting your points across two attempts caps you at your strongest single version.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ag7 · The asterisked exact term ───────────────

const AG7: ScaleSession = {
  mode: 'scale',
  id: 'ag-asterisk',
  subject: 'agricultural-science',
  level: 'common',
  title: 'When only the exact word will do',
  cue: 'Name (exact term)',
  question:
    'Name the plant tissue that transports water from the roots up to the leaves. In the scheme this term is asterisked — the only acceptable answer is the specific word. The candidate writes “the water-carrying tubes”. The line is worth 4 marks. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The asterisk rule is real: synonyms are generally accepted, but where the scheme marks a term with an asterisk the only acceptable answer is that specific word or term, and near-misses or descriptions are refused.',
  scale: {
    name: 'Asterisked exact term',
    levels: bandScale([0, 4]),
    notes: [
      'Normally synonyms are fine — but an asterisk overrides that.',
      'Asterisk rule: “the only acceptable answer is a specific word or term.”',
      '“Xylem” scores; a description like “the water-carrying tubes” is not the exact term, so it earns nothing.',
      'On an asterisked line, a paraphrase is worth zero — the specific scientific word is the whole mark.',
    ],
    cite: MS('p.3 (asterisk: only acceptable answer is a specific word or term)'),
  },
  scripts: [
    {
      id: 'ag7-a',
      label: 'The answer',
      persona: 'Describes instead of naming',
      work: [
        'The water-carrying tubes.',
        '(the idea is right — but the exact term “xylem” is what the asterisk demands)',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The candidate clearly knows what the tissue does, but an asterisked line will only accept the precise term — “xylem” — and a description scores nothing. Most Ag Science lines take synonyms; the asterisk is the exception where the exact scientific word is the whole mark. When a question asks you to name a specific term, name it: don’t paraphrase your way around a word you half-remember.',
      embodies: {
        behaviour: 'Gives a correct description instead of the exact asterisked term — which the scheme refuses.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag7',
    rule: 'On an asterisked term, only the exact word scores.',
    detail:
      'Ag Science accepts synonyms on most lines, but an asterisk marks a term where “the only acceptable answer is a specific word or term”. A description or near-synonym earns zero there. When a line asks you to name a precise scientific term, write that term — not a paraphrase of it.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ag8 · Multi-step calculation ladder ───────────────

const AG8: ScaleSession = {
  mode: 'scale',
  id: 'ag-calc-ladder',
  subject: 'agricultural-science',
  level: 'common',
  title: 'Every correct step banks a mark',
  cue: 'Calculate',
  question:
    'Calculate the average daily liveweight gain of calves from birth to 15 weeks: start 40 kg, finish 125 kg. The full method is 125 − 40 = 85, then 15 × 7 = 105 days, then 85 ÷ 105 = 0.81 kg/day. The line is worth 6 marks. A candidate gets the first two steps right but stalls on the final division. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Ag Science multi-step calculations are marked as a ladder: the scheme credits partial progress — “If the candidate completes two correct calculations, award 5m. If the candidate gives the correct calculation, award 4m.”',
  scale: {
    name: 'Calculation · partial-credit ladder',
    levels: [
      { id: 'zero', label: 'No credit', annotation: '0', marks: 0 },
      { id: 'one', label: 'One correct calculation', annotation: 'C1', marks: 4 },
      { id: 'two', label: 'Two correct calculations', annotation: 'C2', marks: 5 },
      { id: 'full', label: 'Full marks', annotation: '6', marks: 6 },
    ],
    notes: [
      'The final answer is missing, so the full 6 is off the table.',
      'But each correct intermediate calculation banks a mark on the ladder.',
      'Scheme: “If a candidate gives 0.81 without showing calculation, award 6m. If the candidate completes two correct calculations, award 5m. If the candidate gives the correct calculation, award 4m.”',
      'Two right steps (85 kg gain, 105 days) = 5 of 6 — one mark short, not zero.',
    ],
    cite: MS('p.21 (two correct calculations, award 5m; one, award 4m)'),
  },
  scripts: [
    {
      id: 'ag8-a',
      label: 'The answer',
      persona: 'Two steps in, then stalls',
      work: [
        '125 − 40 = 85  (liveweight gain, kg)',
        '15 × 7 = 105  (days)',
        '…stuck on 85 ÷ 105 — final value left blank.',
      ],
      keyLevelId: 'two',
      keyNote:
        'Two correct calculations bank 5 of the 6 — one mark short of full, and a world away from the zero many students fear a half-finished sum will score. On a multi-step line the marks are a ladder: get the weight gain and the day count down, and you have banked most of the marks even if the final division defeats you. Never abandon a calculation because you can’t finish it — write every step you can.',
      embodies: {
        behaviour: 'Completes the intermediate steps of a multi-step calculation but not the final one — the ladder still banks most of the marks.',
        cite: MS('p.21'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag8',
    rule: 'Multi-step sums are a ladder — every correct step banks a mark.',
    detail:
      'Ag Science credits partial progress on multi-step calculations: two correct steps here score 5 of 6, one step scores 4, even with no final answer. Write out every stage you can rather than giving up — you bank marks rung by rung, and an unfinished calculation is worth far more than a blank.',
    cite: MS('p.21'),
  },
};

// ─────────────── Ag9 · Right answer, no working ───────────────

const AG9: ScaleSession = {
  mode: 'scale',
  id: 'ag-answer-only',
  subject: 'agricultural-science',
  level: 'common',
  title: 'A right answer needs no working',
  cue: 'Calculate',
  question:
    'Calculate the average calving interval for a cow over her lactations. The correct value is 375 days and the line is worth 4 marks. A confident candidate writes only “375 days” — no formula, no working shown. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme confirms a correct final answer is not penalised for missing working: “If a candidate gives 375.25 or 375 without showing calculation, award 4m. If the candidate gives the correct formula without correct answer, award 2m.”',
  scale: {
    name: 'Answer shown, working omitted',
    levels: [
      { id: 'zero', label: 'No credit', annotation: '0', marks: 0 },
      { id: 'formula', label: 'Formula only, wrong answer', annotation: 'F', marks: 2 },
      { id: 'full', label: 'Full marks', annotation: '4', marks: 4 },
    ],
    notes: [
      'The final answer (375 days) is correct.',
      'Scheme: “If a candidate gives 375.25 or 375 without showing calculation, award 4m.”',
      'A right answer is NOT docked for showing no working — it scores the full 4.',
      '(The mirror rule: a correct formula with the wrong answer still salvages 2 — so working is your insurance when the number goes wrong.)',
    ],
    cite: MS('p.24 (375 without showing calculation, award 4m)'),
  },
  scripts: [
    {
      id: 'ag9-a',
      label: 'The answer',
      persona: 'Answer only, no working',
      work: [
        '375 days.',
        '(no formula or working shown — but the value is correct)',
      ],
      keyLevelId: 'full',
      keyNote:
        'A correct final answer scores full marks even with no working on the page — the scheme awards the whole 4 for “375 without showing calculation”. You are not penalised for a bare right answer. The reason to write the working anyway is insurance, not compliance: if your number turns out wrong, a correct formula salvages half (2 of 4), whereas a wrong answer with nothing shown scores zero. Show working to protect yourself, not because a right answer needs it.',
      embodies: {
        behaviour: 'Gives the correct final answer with no working shown — which the scheme awards in full.',
        cite: MS('p.24'),
      },
    },
    {
      id: 'ag9-border',
      label: 'The borderline',
      persona: 'Right formula, wrong number',
      work: [
        '(397 + 345 + 397 + 362) / 4',
        '= 385 days  (arithmetic slip; the correct value is 375)',
        '(the method is right — only the final number is wrong)',
      ],
      keyLevelId: 'formula',
      keyNote:
        'This is the mirror of the bare right answer: the correct formula is on the page, but the arithmetic slips, so the line lands on the method mark — 2 of the 4, neither the full mark nor zero. A careless marker is pulled both ways: seeing a wrong final number they may strike the whole line out, or seeing a page of correct working they may wave it up to full. The scheme pins it precisely in the middle — a correct formula without the correct answer scores 2. This is exactly why working earns its keep: the formula shown here salvages half the marks a wrong number would otherwise have cost.',
      embodies: {
        behaviour: 'Shows the correct formula but slips the arithmetic — the method salvages the middle mark, neither full nor zero.',
        cite: MS('p.24'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag9',
    rule: 'A correct answer is never docked for missing working.',
    detail:
      'Ag Science awards full marks for a correct final answer even when no calculation is shown. Working earns its keep as insurance — a right formula salvages partial credit if the number comes out wrong — not as a requirement for a correct answer. Show it to protect a slip, but know a bare right answer still scores full.',
    cite: MS('p.24'),
  },
};

// ─────────────── Ag10 · Diagram quality ladder ───────────────

const AG10: ScaleSession = {
  mode: 'scale',
  id: 'ag-diagram-quality',
  subject: 'agricultural-science',
  level: 'higher',
  title: 'One wrong feature caps the diagram',
  cue: 'Draw a diagram',
  question:
    'Draw a diagram of a grass plant at the ideal growth stage for harvesting (the vegetative stage). The diagram mark is worth 2, awarded 2/1/0 on what it shows. A candidate draws a healthy plant with several leaves — but adds a seed head. What does the diagram score?',
  questionNote:
    'Scenario authored for this exercise. The scheme grades a diagram on a short quality ladder: “To show at least 3 leaves or tillers, and no seed head for 2m; Seed head present or less than 3 leaves for 1m; No elements listed present 0m.”',
  scale: {
    name: 'Diagram · quality ladder (D = 2, 1, 0)',
    levels: [
      { id: 'zero', label: 'No creditable elements', annotation: '0', marks: 0 },
      { id: 'partial', label: 'Wrong feature present', annotation: '1', marks: 1 },
      { id: 'full', label: 'Correct stage shown', annotation: '2', marks: 2 },
    ],
    notes: [
      'The vegetative stage means at least 3 leaves/tillers and NO seed head.',
      'Scheme: “To show at least 3 leaves or tillers, and no seed head for 2m; Seed head present or less than 3 leaves for 1m; No elements listed present 0m.”',
      'The extra seed head contradicts the vegetative stage, so the diagram caps at 1, not 2.',
      'A neat drawing does not rescue the mark — the wrong feature is what the scheme keys on.',
    ],
    cite: MS('p.19 (grass plant diagram: 2m / 1m / 0m)'),
  },
  scripts: [
    {
      id: 'ag10-a',
      label: 'The diagram',
      persona: 'Good drawing, wrong stage',
      work: [
        'Grass plant with several leaves — drawn clearly and neatly.',
        'But a seed head is included.',
        '(a seed head means the plant is past the vegetative harvesting stage)',
      ],
      keyLevelId: 'partial',
      keyNote:
        'The seed head drops the diagram from 2 to 1 — the scheme grades the drawing on what it shows, not how neatly it is drawn, and a seed head contradicts the vegetative stage the question named. Read exactly what stage or state is being asked for before you draw, and leave out the features that belong to a different stage. One wrong element can halve a diagram mark.',
      embodies: {
        behaviour: 'Adds a feature (seed head) that belongs to the wrong growth stage — the scheme caps the diagram at the partial mark.',
        cite: MS('p.19'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag10',
    rule: 'Diagrams are graded on correctness, not neatness.',
    detail:
      'Ag Science marks a diagram on a short quality ladder (2 / 1 / 0) keyed to the features it shows. Adding a feature that belongs to the wrong stage — a seed head on a “vegetative stage” grass plant — caps the mark. Draw exactly the stage or state named, and leave out anything that contradicts it.',
    cite: MS('p.19'),
  },
};

// ─────────────── Ag11 · Draw AND label are separate marks ───────────────

const AG11: GridSession = {
  mode: 'grid',
  id: 'ag-draw-label',
  subject: 'agricultural-science',
  level: 'higher',
  title: 'Draw and label are two mark pools',
  cue: 'Draw a labelled diagram',
  question:
    'Draw a labelled diagram of the rhizosphere. The scheme marks it as two separate pools: the diagram itself (must show a root with a rhizosphere zone around it) is worth 3, and the labels are worth 2 — two labels at 1 mark each.',
  questionNote:
    'Question authored for this exercise. The draw-and-label split is the real SEC pattern: the scheme records the diagram and the labels as separate mark allocations, here “D = 3, 0 / L = 2(1)”.',
  grid: {
    perPoint: [
      { id: 'diagram', label: 'Diagram (root + rhizosphere zone)', marks: 3 },
      { id: 'labelA', label: '1st correct label', marks: 1 },
      { id: 'labelB', label: '2nd correct label', marks: 1 },
    ],
    shorthand: 'D:3 + L:2(1)',
    ruleNote:
      'The diagram and the labels are marked independently. A perfect drawing with nothing labelled still forfeits the 2 label marks — and correct labels still score even if the drawing itself misses the mark. Do both: they are separate pools of marks.',
    cite: MS('p.23 (D = 3, 0 / L = 2(1))'),
  },
  scripts: [
    {
      id: 'ag11-a',
      label: 'Script A',
      persona: 'Draws it, forgets to label',
      attempts: [
        {
          id: 'ag11-a-1',
          text: 'A clear drawing of a root with the rhizosphere zone around it — but no labels added.',
          key: { diagram: 3, labelA: 0, labelB: 0 },
          keyNote: 'The drawing banks its full 3, but the two label marks are simply left on the table — labels are a separate pool, and a diagram without them cannot claim them. Two words (e.g. “rhizoplane”, “bulk soil”) were worth a mark each. Always label a “labelled diagram”: the instruction is telling you where 2 of the marks live.',
        },
      ],
      embodies: {
        behaviour: 'Draws the diagram well but adds no labels — forfeiting the separately-allocated label marks.',
        cite: MS('p.23'),
      },
    },
    {
      id: 'ag11-b',
      label: 'Script B',
      persona: 'Labels land, drawing weak',
      attempts: [
        {
          id: 'ag11-b-1',
          text: 'A rough sketch that never clearly shows the rhizosphere zone — but two labels (“rhizosphere soil”, “microorganism”) are correct.',
          key: { diagram: 0, labelA: 1, labelB: 1 },
          keyNote: 'The drawing misses the required rhizosphere zone, so the 3 diagram marks are gone — but the two correct labels still score 1 each, because labels are marked in their own pool. Even when a diagram lets you down, name every part you can: those label marks are independent of the drawing’s quality.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ag11',
    rule: 'On a labelled diagram, the drawing and the labels score separately.',
    detail:
      'Ag Science splits a labelled-diagram question into two independent mark pools — the diagram and the labels. A flawless drawing with no labels forfeits the label marks; correct labels score even when the drawing is weak. Always do both: the word “labelled” is telling you a share of the marks lives in the labels.',
    cite: MS('p.23'),
  },
};

// ─────────────── Ag12 · Points can be found on the diagram ───────────────

const AG12: ScaleSession = {
  mode: 'scale',
  id: 'ag-diagram-points',
  subject: 'agricultural-science',
  level: 'higher',
  title: 'Your diagram is part of your answer',
  cue: 'Describe (with diagram)',
  question:
    'Describe how an investigation into the botanical composition of a field was carried out. The line is worth 12 marks — any three creditable points at 4 marks each. A candidate writes two steps in prose and shows a third (“place a quadrat”) only as a label on their diagram. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme states credit can come from the candidate’s diagram, not only the prose: on this describe-the-investigation line it notes “Points can be found on the diagram.”',
  scale: {
    name: 'Points credited from prose OR diagram',
    levels: [
      { id: 'zero', label: 'No creditable points', annotation: '0', marks: 0 },
      { id: 'one', label: 'One point', annotation: '4', marks: 4 },
      { id: 'two', label: 'Two points', annotation: '8', marks: 8 },
      { id: 'three', label: 'Three points', annotation: '12', marks: 12 },
    ],
    notes: [
      'The line pays any three points at 4 marks each (3 × 4 = 12).',
      'Scheme: “Points can be found on the diagram.”',
      'A step shown only as a labelled diagram feature counts the same as a step written in prose.',
      'Two prose steps + one from the diagram = three points = full 12.',
    ],
    cite: MS('p.18 (Points can be found on the diagram)'),
  },
  scripts: [
    {
      id: 'ag12-a',
      label: 'The answer',
      persona: 'Third point lives in the diagram',
      work: [
        'Prose: “Identify plants using a key… record the results.”',
        'Diagram: a labelled sketch showing a quadrat placed on the ground.',
        '(the quadrat step appears only as a diagram label, not in the prose)',
      ],
      keyLevelId: 'three',
      keyNote:
        'The third point — placing the quadrat — is credited even though it appears only on the diagram, because the scheme takes points “found on the diagram” just as it takes them from prose. Your labelled sketch is not decoration; it is markable answer content. When a describe-the-method question invites a diagram, put real steps into the labels — they earn the same marks as a written sentence, and a good diagram can complete an answer your prose left short.',
      embodies: {
        behaviour: 'Places a creditable step only in the labelled diagram — which the scheme credits as an answer point.',
        cite: MS('p.18'),
      },
    },
    {
      id: 'ag12-border',
      label: 'The borderline',
      persona: 'Two points land, the third too vague',
      work: [
        'Prose: “Identify the plant species present using a key.”  (one clear method step)',
        'Diagram: a labelled sketch showing a quadrat placed on the ground.  (a second step, in the diagram)',
        'Prose: “Then decide which area of the field was the best.”  (too vague to credit as a method step)',
      ],
      keyLevelId: 'two',
      keyNote:
        'Two genuine method steps are credited — one written in prose, one taken from the labelled diagram — so the line banks 8 of the 12. The third statement names no real step, so it earns nothing, and the answer stops at two points of the three. A careless marker can be pushed either way: seeing a full-looking answer with a diagram they may round up to the full 12, or discounting the sketch they may drop to a single prose point and 4. The scheme pins it at two — it credits the step found on the diagram exactly like a prose step, but it still needs a genuine third step this script never gives.',
      embodies: {
        behaviour: 'Earns two creditable points, one of them from the diagram, but offers no genuine third step — the line lands two of three.',
        cite: MS('p.18'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag12',
    rule: 'A labelled diagram earns the same marks as prose.',
    detail:
      'Ag Science credits points “found on the diagram”, not only in the written answer. A step shown as a diagram label scores exactly like a step written out. Treat your sketch as markable content: label it with real method steps, and it can complete an answer your prose left short.',
    cite: MS('p.18'),
  },
};

// ─────────────── Ag13 · Name AND describe are split marks ───────────────

const AG13: GridSession = {
  mode: 'grid',
  id: 'ag-name-describe',
  subject: 'agricultural-science',
  level: 'common',
  title: 'Naming it isn’t describing it',
  cue: 'Describe a characteristic',
  question:
    'Describe one characteristic of the Irish Moiled breed that makes it a sustainable choice on Irish farms. The line is marked 2 + 2 — 2 marks for naming a valid characteristic, and a separate 2 marks for the description that explains it.',
  questionNote:
    'Question authored for this exercise. The name-plus-describe split is the real SEC pattern: this line is scored “characteristic - 2 / description - 2”, with the naming and the explanation marked separately.',
  grid: {
    perPoint: [
      { id: 'char', label: 'Names a valid characteristic', marks: 2 },
      { id: 'desc', label: 'Describes / explains it', marks: 2 },
    ],
    shorthand: '2 + 2 (characteristic + description)',
    ruleNote:
      'Naming the characteristic is only half the marks; the description that unpacks it is a separate 2. A one-word answer scores 2 of 4 — the “describe” command is asking for the explanation, and the scheme has already reserved marks for it.',
    cite: MS('p.12 (characteristic - 2 / description - 2)'),
  },
  scripts: [
    {
      id: 'ag13-a',
      label: 'Script A',
      persona: 'Names it, stops there',
      attempts: [
        {
          id: 'ag13-a-1',
          text: '“Early maturing.”  (no further detail)',
          key: { char: 2, desc: 0 },
          keyNote: 'A correct characteristic banks its 2 marks — but the line said “describe”, and the description carries its own 2. “Early maturing” names the trait without explaining it, so half the marks go unclaimed. The command word is the instruction: “describe” means the naming alone is never the full answer.',
        },
      ],
      embodies: {
        behaviour: 'Names a characteristic without describing it — forfeiting the separately-allocated description marks.',
        cite: MS('p.12'),
      },
    },
    {
      id: 'ag13-b',
      label: 'Script B',
      persona: 'Names and unpacks',
      attempts: [
        {
          id: 'ag13-b-1',
          text: '“Early maturing — steers finish between 20 and 24 months, so the animal is off the farm sooner.”',
          key: { char: 2, desc: 2 },
          keyNote: 'The characteristic (2) plus a description that explains what it means in practice (2) = the full 4. The naming earns its marks and the explanation earns its own — this is what “describe” is asking for.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-ag13',
    rule: 'When asked to describe, naming is only half the marks.',
    detail:
      'Ag Science splits “describe a characteristic” lines into name (2) and description (2). A one-word answer scores half; the command word “describe” is reserving marks for the explanation. Name the feature, then unpack what it means in practice — the two are marked separately.',
    cite: MS('p.12'),
  },
};

// ─────────────── Ag14 · Cancelled answers ───────────────

const AG14: ScaleSession = {
  mode: 'scale',
  id: 'ag-cancelled',
  subject: 'agricultural-science',
  level: 'common',
  title: 'Cross it out and it’s gone',
  cue: 'Explain (two attempts)',
  question:
    'Give three roles of water in a plant — 3 points at 2 marks. A candidate first writes a strong answer worth all three roles (6 marks), then strikes it through and replaces it with a rushed second version that covers only two roles (4 marks). Which one does the examiner mark?',
  questionNote:
    'Scenario authored for this exercise. The rule is real: “If an answer is cancelled and a second version of the answer is given, you should accept the cancellation and award marks, where merited, for the un-cancelled version only.”',
  scale: {
    name: 'Cancelled first version, replaced',
    levels: bandScale([0, 4, 6]),
    notes: [
      'The first version — all three roles — was worth the full 6.',
      'But the candidate cancelled it and wrote a weaker second version worth 4.',
      'Rule: award marks “for the un-cancelled version only.”',
      'So the crossed-out 6-mark answer is ignored; only the un-cancelled 4 is marked.',
    ],
    cite: MS('p.4 (award marks for the un-cancelled version only)'),
  },
  scripts: [
    {
      id: 'ag14-a',
      label: 'The answer',
      persona: 'Cancels the better version',
      work: [
        'V1 (struck through): transport of minerals; raw material for photosynthesis; turgor for support.  — three roles, 6 marks.',
        'V2 (kept): used in photosynthesis; keeps cells turgid.  — two roles, 4 marks.',
      ],
      keyLevelId: 'm4',
      keyNote:
        'The examiner marks the un-cancelled version only — so the stronger first answer, crossed out, scores nothing, and the line takes the weaker replacement’s 4. This is the mirror of the two-versions rule: leave both standing and you get the better one; cancel the better one and you are stuck with what remains. Never strike through an answer unless you are certain the replacement is an improvement — and if you change your mind, the scheme says an un-cancelled answer is treated as if it were never crossed out, so a hasty line through good work is the real risk.',
      embodies: {
        behaviour: 'Cancels a stronger answer and replaces it with a weaker one — the scheme marks only the un-cancelled version.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag14',
    rule: 'A cancelled answer is gone — only the un-cancelled version is marked.',
    detail:
      'When a candidate cancels one answer and writes another, Ag Science marks the un-cancelled version only. Strike through your best work and its marks vanish, even if the replacement is worse. Don’t cross anything out unless you are sure the new version is better.',
    cite: MS('p.4'),
  },
};

// ─────────────── Ag15 · Tick-box identification is all-or-nothing ───────────────

const AG15: ScaleSession = {
  mode: 'scale',
  id: 'ag-tickbox',
  subject: 'agricultural-science',
  level: 'common',
  title: 'A hedged tick is no tick',
  cue: 'Identify (tick the box)',
  question:
    'Identify the bacterium required for good-quality silage by ticking one box: Lactobacillus, Clostridia, or Staphylococcus aureus. The item is worth 6 marks — all or nothing. Unsure, the candidate ticks two boxes, including the correct one. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Tick-box identification items are scored as a single all-or-nothing block (here 6 marks); a second, wrong tick is a surplus incorrect answer, which “cancels the marks awarded for a correct answer.”',
  scale: {
    name: 'Tick-box identification (all-or-nothing)',
    levels: bandScale([0, 6]),
    notes: [
      'A tick-box identification carries no partial credit — it is the full 6 or nothing.',
      'One correct tick alone scores the full 6.',
      'Ticking a second, wrong box adds a surplus incorrect answer.',
      'Surplus rule: “A surplus wrong answer cancels the marks awarded for a correct answer” — so the hedged double-tick scores 0.',
    ],
    cite: MS('p.19 (tick-box identification, 6 marks) with p.4 (surplus wrong answer cancels)'),
  },
  scripts: [
    {
      id: 'ag15-a',
      label: 'The answer',
      persona: 'Ticks two to be safe',
      work: [
        '✓ Lactobacillus  (correct)',
        '✓ Clostridia  (wrong — added as a hedge)',
        '(the extra tick is a surplus incorrect answer)',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The correct box is ticked — but so is a wrong one, and the surplus wrong tick cancels the correct one, dropping a certain 6 to 0. Tick-box items are all-or-nothing and offer no reward for hedging: a single confident tick on Lactobacillus banks the full 6. When a question says tick one box, tick exactly one. A second “just in case” tick is not a safety net; it is the thing that loses you the mark.',
      embodies: {
        behaviour: 'Ticks a second box as a hedge — the surplus wrong tick cancels the correct one to zero.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ag15',
    rule: 'Tick exactly one box — a hedged second tick cancels the first.',
    detail:
      'Ag Science tick-box identifications are all-or-nothing, and a surplus wrong tick cancels a correct one. Ticking two boxes to be safe turns a certain full mark into zero. Commit to a single tick; the “just in case” second box is what costs you the marks.',
    cite: MS('p.4'),
  },
};

export const AG_SCIENCE_CHAIR: ChairSubject = {
  id: 'agricultural-science',
  label: 'Agricultural Science',
  tagline: 'Front-loaded points, surplus penalties, the calculation ladder, diagram marking, split name/describe lines and holistic coursework.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AG1, AG2, AG3, AG4, AG5, AG6, AG7, AG8, AG9, AG10, AG11, AG12, AG13, AG14, AG15],
  sources: [
    { label: 'SEC LC Agricultural Science HL marking scheme 2024 (examiner-reports/agricultural-science/2024-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — front-loaded points, the surplus-answer penalty, the calculation method mark and multi-step ladder, the rule that a correct answer needs no working, diagram marking (the quality ladder, the draw/label split, and points credited from the diagram), the split name-and-describe line, the IIS holistic banding, the context rule, the two-versions "greater not sum" rule, the cancelled-answer rule, asterisked exact terms and all-or-nothing tick-box items — which apply at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme; level-specific worked examples are being added.',
};
