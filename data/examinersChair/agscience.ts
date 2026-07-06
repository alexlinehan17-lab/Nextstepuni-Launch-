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

export const AG_SCIENCE_CHAIR: ChairSubject = {
  id: 'agricultural-science',
  label: 'Agricultural Science',
  tagline: 'Front-loaded points, surplus penalties, method marks, the context rule and holistic coursework.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [AG1, AG2, AG3, AG4, AG5, AG6, AG7],
  sources: [
    { label: 'SEC LC Agricultural Science HL marking scheme 2024 (examiner-reports/agricultural-science/2024-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the general conventions — front-loaded points, the surplus-answer penalty, the calculation method mark, the IIS holistic banding, the context rule (a right term in a contradicted statement scores nothing), the two-versions "greater not sum" rule, and asterisked exact terms — which apply at both Higher and Ordinary level. Verified against the 2024 Higher Level scheme; level-specific worked examples are being added.',
};
