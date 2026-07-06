/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Irish / Gaeilge (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the composition's Stíl + Ionramháil + Cumas Gaeilge split
 * with language as 80 of 100, the wrong-genre Stíl-zero rule, and the
 * comprehension "own words" gate) is the real SEC system, cited to:
 *  - SEC LC Irish HL marking scheme 2025 (An Ardteistiméireacht, Scéim
 *    Mharcála, Ardleibhéal, Gaeilge) — examiner-reports/irish/2025-marking-scheme.*
 * The oral / Béaltriail is a SEPARATE assessment. Its 240-mark / 40% component
 * allocation (session Ir6) is cited to the SEC's own assessment-structure
 * document, NOT the written marking scheme:
 *  - SEC LC Assessment Arrangements 2026 (An Bhéaltriail Chomónta) —
 *    examiner-reports/irish/2026-assessment-arrangements-oral.*
 * The per-question oral marking grid (how each component is scored internally)
 * is not sourced here and is not asserted.
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Irish HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Irish OL marking scheme 2025, ${p}` });
// Oral: cited to the SEC assessment-structure document, NOT the written scheme.
const ORAL = (p: string) => ({ label: `SEC LC Assessment Arrangements 2026 (An Bhéaltriail Chomónta), ${p}` });

// ─────────────── Ir1 · Language is the mark ───────────────

const GAEILGE_BANDS: ScaleLevel[] = [
  { id: 'iseal', label: 'Íseal (low)', annotation: '25', marks: 25 },
  { id: 'mean', label: 'Meánach (middle)', annotation: '48', marks: 48 },
  { id: 'ard', label: 'Ard (high)', annotation: '72', marks: 72 },
];

const IR1: ScaleSession = {
  mode: 'scale',
  id: 'ir-cumas-gaeilge',
  subject: 'irish',
  level: 'common',
  title: 'Great ideas, shaky Irish',
  cue: 'Ceapadóireacht',
  question: 'A composition has genuinely interesting, well-organised ideas — but the Irish itself is error-strewn: wrong verb tenses, shaky syntax, misused prepositions. Of the 100 composition marks, 80 are for Cumas Gaeilge (command of Irish). Which Cumas Gaeilge band does it land in?',
  questionNote:
    'Scenario authored for this exercise. The composition is marked Stíl 5 + Ionramháil Ábhair 15 + Cumas Gaeilge 80 — so command of the language is 80 of the 100 marks, driven by vocabulary range and accuracy.',
  scale: {
    name: 'Cumas Gaeilge · /80 · bands',
    levels: GAEILGE_BANDS,
    notes: [
      'Composition = Stíl 5 + Ionramháil Ábhair 15 + Cumas Gaeilge 80.',
      'Cumas Gaeilge (80 marks) is judged on richness AND accuracy of the Irish.',
      'Repeated errors in tense, syntax and prepositions hold the answer in the lower band, however good the ideas.',
      'Ideas are rewarded under Ionramháil (15) — but they can’t rescue the 80-mark language band.',
    ],
    cite: MS('p.13 (Cumas Gaeilge weighting and bands)'),
  },
  scripts: [
    {
      id: 'ir1-a',
      label: 'The composition',
      persona: 'Ideas strong, Irish weak',
      work: [
        'Interesting, well-structured ideas.',
        'But frequent errors: wrong tenses, weak syntax, misused prepositions.',
      ],
      keyLevelId: 'iseal',
      keyNote:
        'Lower Cumas Gaeilge band — because 80 of the 100 marks reward command of Irish, and repeated accuracy errors are exactly what that band measures. The ideas earn their marks under Ionramháil (15), but they can’t lift the language score. In Irish composition, the surest marks come from writing accurate Irish you control, not ambitious Irish you don’t.',
      embodies: {
        behaviour: 'Strong ideas undermined by weak language accuracy — where 80% of the mark lives.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir1',
    rule: 'In Irish composition, the language is the mark.',
    detail:
      'Cumas Gaeilge is 80 of the 100 composition marks — accuracy and range of Irish. Write Irish you control: reliable tenses, syntax and prepositions beat ambitious sentences riddled with errors. Ideas alone can’t lift the language band.',
    cite: MS('p.13'),
  },
};

// ─────────────── Ir2 · Wrong genre = Style 0 ───────────────

const IR2: ScaleSession = {
  mode: 'scale',
  id: 'ir-genre',
  subject: 'irish',
  level: 'common',
  title: 'Right title, wrong form',
  cue: 'Ceapadóireacht',
  question: 'The chosen composition title asks for a speech (óráid). The candidate writes a fluent, accurate piece — but as a personal essay (aiste), with none of the features of a speech (no address to an audience, no rhetorical opening). What does the Stíl (Style) mark, out of 5, become?',
  questionNote:
    'Scenario authored for this exercise. Style marks genre discipline, not quality: writing the wrong genre for the chosen title scores Stíl 0.',
  scale: {
    name: 'Stíl · /5',
    levels: [
      { id: 'm0', label: '0 (wrong genre)', annotation: '0', marks: 0 },
      { id: 'm5', label: '5 (correct genre)', annotation: '5', marks: 5 },
    ],
    notes: [
      'Stíl (5 marks) rewards using the right genre for the chosen title — not the quality of writing.',
      'A speech title needs the features of a speech; written as an essay, Stíl = 0.',
      'The Cumas Gaeilge and Ionramháil marks are judged separately.',
    ],
    cite: MS('p.14 (Stíl / genre rule)'),
  },
  scripts: [
    {
      id: 'ir2-a',
      label: 'The composition',
      persona: 'Fluent — wrong form',
      work: [
        'Fluent, accurate Irish.',
        'Title asked for a speech (óráid); written as a personal essay (aiste).',
        'No audience address, no rhetorical features.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Stíl 0 — the genre is wrong for the title, and Style marks the form, not the fluency. The language marks may still be strong, but 5 easy marks are gone for want of a speech’s opening and audience address. Match the form the title asks for: speech, letter, diary, debate, essay.',
      embodies: {
        behaviour: 'Writes the wrong genre for the chosen title — Stíl scores 0.',
        cite: MS('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir2',
    rule: 'Write the genre the title asks for.',
    detail:
      'Stíl rewards using the correct form — speech, letter, diary, debate — not how well you write. Pick a title whose genre you can produce, and build in that genre’s features. Wrong form is an automatic Stíl 0.',
    cite: MS('p.14'),
  },
};

// ─────────────── Ir3 · Own words gate ───────────────

const IR3: ScaleSession = {
  mode: 'scale',
  id: 'ir-own-words',
  subject: 'irish',
  level: 'higher',
  title: 'In your own words',
  cue: 'Léamhthuiscint',
  question: 'A reading-comprehension question (worth 12 marks) explicitly requires the answer in the candidate’s own words. The relevant idea is clearly in the passage, and the candidate copies the sentence out word for word. What does it score?',
  questionNote:
    'Scenario authored for this exercise. Comprehension Q6(b) is worth 12 marks and must be in the candidate’s own words; lifting the passage verbatim there scores nothing.',
  scale: {
    name: 'Comprehension (own words) · /12',
    levels: [
      { id: 'm0', label: '0 (copied)', annotation: '0', marks: 0 },
      { id: 'm7', label: '7 (partly reworded)', annotation: '7', marks: 7 },
      { id: 'm12', label: '12 (own words)', annotation: '12', marks: 12 },
    ],
    notes: [
      'This 12-mark question requires the answer in the candidate’s own words.',
      'Copying the passage verbatim does not demonstrate understanding — it scores nothing here.',
      'Rewording the idea in controlled Irish is what unlocks the marks.',
    ],
    cite: MS('p.16 (Q6(b), own words, 12 marks)'),
  },
  scripts: [
    {
      id: 'ir3-a',
      label: 'The answer',
      persona: 'Copies the passage',
      work: ['Lifts the relevant sentence from the text, word for word.'],
      keyLevelId: 'm0',
      keyNote:
        '0 of 12 — the question is gated behind “own words”, and a verbatim lift shows nothing about understanding. Even a simple reworded version in accurate Irish would score. On “own words” questions, never copy: paraphrase the idea in language you control.',
      embodies: {
        behaviour: 'Copies the passage on an “own words” question — which scores 0.',
        cite: MS('p.16'),
      },
    },
    {
      id: 'ir3-b',
      label: 'The answer',
      persona: 'Half-rewords, half-lifts',
      work: [
        'Recasts the opening of the idea in the candidate’s own words.',
        'Then falls back and copies the rest of the passage sentence verbatim.',
      ],
      keyLevelId: 'm7',
      keyNote:
        '7 of 12 — a partial reward. Where the idea is genuinely reworded, understanding is shown and credited; where the answer lapses back into a verbatim lift, those marks are withheld. The examiner isn’t looking for perfect paraphrase, but the whole idea has to be in your own Irish. Carry the rewording all the way through — don’t start in your own words and coast home on the passage.',
      embodies: {
        behaviour: 'Rewords part of the idea but lifts the rest verbatim on an “own words” question — partial credit only.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir3',
    rule: 'On “own words” questions, never copy.',
    detail:
      'Irish comprehension gates some marks behind answering in your own words — a verbatim lift scores 0 there. Reword the idea in accurate, controlled Irish; understanding shown is what the marks reward.',
    cite: MS('p.16'),
  },
};

// ─────────────── Ir4 · OL — reword the poem, or lose half ───────────────

const IR4: ScaleSession = {
  mode: 'scale',
  id: 'ir-ol-poetry',
  subject: 'irish',
  level: 'ordinary',
  title: 'Reword the poem, or lose half',
  cue: 'Filíocht (OL)',
  question: 'An Ordinary Level poetry question asks about an image or theme “i d’fhocail féin” (in your own words). The candidate answers correctly — but by quoting the verse lines verbatim. The scheme halves a verbatim answer. On a 5-mark part, what does it score?',
  questionNote:
    'Scenario authored for this exercise. At OL, comprehension answers are direct passage lifts (there is no “own words” gate there), but the poetry “i d’fhocail féin” parts halve a verbatim-lifted answer.',
  scale: {
    name: 'OL poetry · own words',
    levels: [
      { id: 'm2', label: '2 (verbatim, halved)', annotation: '2', marks: 2 },
      { id: 'm5', label: '5 (reworded)', annotation: '5', marks: 5 },
    ],
    notes: [
      'OL poetry “i d’fhocail féin” parts require the idea in your own words.',
      'A verbatim-lifted verse line is halved — the scheme collapses it (e.g. to 2+2).',
      'This is the opposite of OL comprehension, where lifting the passage is fine.',
    ],
    cite: MSOL('p.25–27 (poetry “i d’fhocail féin” halving)'),
  },
  scripts: [
    {
      id: 'ir4-a',
      label: 'The answer',
      persona: 'Quotes the verse',
      work: ['Answers the image/theme correctly — but by copying the poem’s lines word for word.'],
      keyLevelId: 'm2',
      keyNote:
        'Halved — the verbatim verse lines earn only 2 of 5, because this part wanted the idea in your own words. Note the split from comprehension: at OL you CAN copy the prose passage, but in poetry “i d’fhocail féin” you must reword. Put the poet’s idea into your own simple Irish.',
      embodies: {
        behaviour: 'Quotes verse lines verbatim on an OL “own words” poetry part — halved.',
        cite: MSOL('p.25'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir4',
    rule: 'At OL, copy the prose passage — but reword the poem.',
    detail:
      'Ordinary Level comprehension answers can lift the passage directly, but poetry “i d’fhocail féin” parts halve a verbatim answer. Know which is which: reword the poem’s idea in your own Irish; you can copy the prose.',
    cite: MSOL('p.25'),
  },
};

// ─────────────── Ir5 · Your Irish is marked in the aural ───────────────

const CLUAS_GAEILGE: ScaleLevel[] = [
  { id: 'm0', label: '0 (structure broken)', annotation: '0', marks: 0 },
  { id: 'm2', label: '2 (minor slips)', annotation: '2', marks: 2 },
  { id: 'm3', label: '3 (sound Irish)', annotation: '3', marks: 3 },
];

const IR5: ScaleSession = {
  mode: 'scale',
  id: 'ir-aural-gaeilge',
  subject: 'irish',
  level: 'common',
  title: 'Your Irish counts in the aural',
  cue: 'Cluastuiscint',
  question: 'A candidate hears the Cluastuiscint clearly and gives the right information in every answer — but writes it in Irish riddled with major syntax errors (wrong copula, wrong verb tenses). The Cluastuiscint deducts 0 to 3 marks for the standard of Irish (caighdeán na Gaeilge). Where does that Irish mark land?',
  questionNote:
    'Scenario authored for this exercise. The 0–3 deduction for the standard of Irish across the Cluastuiscint is the real SEC rule (“Bainfear ó 0 go 3 ar chaighdeán na Gaeilge”): major syntax errors — the copula, verb tenses, prepositions — are penalised; spelling is not counted.',
  scale: {
    name: 'Cluastuiscint · caighdeán na Gaeilge (0–3)',
    levels: CLUAS_GAEILGE,
    notes: [
      'The Cluastuiscint deducts 0 to 3 marks for the standard of your Irish — separate from the comprehension marks.',
      'What’s penalised: major syntax errors that distort the structure — the copula, verb tenses, prepositions.',
      'Spelling is not counted; but broken sentences are, even when the content is right.',
    ],
    cite: MS('p.3 (Cluastuiscint: “Bainfear ó 0 go 3 ar chaighdeán na Gaeilge”)'),
  },
  scripts: [
    {
      id: 'ir5-a',
      label: 'The answers',
      persona: 'Right content, broken Irish',
      work: [
        'Every answer has the correct information from the recording.',
        'But the Irish is full of major syntax errors — the copula and verb tenses are wrong throughout.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The comprehension content earns its own marks — but the full 3-mark Gaeilge deduction applies, because the syntax is broken. Your Irish is marked even in a listening test. Write short, correct sentences: mind the copula, the tenses and the prepositions. Spelling itself won’t cost you here, so don’t let fear of it push you into garbled structures.',
      embodies: {
        behaviour: 'Answers the aural correctly but in structurally broken Irish — forfeiting the 0–3 standard-of-Irish marks.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir5',
    rule: 'Your Irish is marked even in the aural.',
    detail:
      'The Cluastuiscint deducts up to 3 marks for the standard of your Irish. Right answers in broken Irish still lose those marks — write short, grammatically sound sentences (watch the copula, verb tenses and prepositions). Spelling itself isn’t counted, so don’t let it scare you into worse structures.',
    cite: MS('p.3'),
  },
};

// ─────────────── Ir6 · The oral is 40% — and the Comhrá is half of it ───────────────

const BEALTRIAIL_COMPONENTS: ScaleLevel[] = [
  { id: 'failtiu', label: 'An Fáiltiú (greeting)', annotation: '5', marks: 5 },
  { id: 'filiocht', label: 'Léamh na Filíochta (poetry)', annotation: '35', marks: 35 },
  { id: 'sraith', label: 'An tSraith Pictiúr (picture sequence)', annotation: '80', marks: 80 },
  { id: 'comhra', label: 'An Comhrá (general conversation)', annotation: '120', marks: 120 },
];

const IR6: ScaleSession = {
  mode: 'scale',
  id: 'ir-oral-weighting',
  subject: 'irish',
  level: 'common',
  title: 'The oral is 40% — and the Comhrá is half of it',
  cue: 'An Bhéaltriail',
  question:
    'The Leaving Cert Irish oral (An Bhéaltriail Chomónta) is worth 240 marks — 40% of your entire Irish grade — and is common to Higher and Ordinary. It has four parts: An Fáiltiú (the greeting), Léamh na Filíochta (reading named poetry), An tSraith Pictiúr (describing a picture sequence), and An Comhrá (the general conversation). A candidate polishes the poems and learns off the picture sequences, but treats the general conversation as something to wing on the day. Which single part carries the MOST marks — the part they are gambling with?',
  questionNote:
    'Scenario authored for this exercise. The four-part split of the 240-mark common oral — An Fáiltiú 5, Léamh na Filíochta 35, An tSraith Pictiúr 80, An Comhrá 120 — is the real SEC allocation.',
  scale: {
    name: 'An Bhéaltriail Chomónta · na comhpháirteanna (as 240)',
    levels: BEALTRIAIL_COMPONENTS,
    notes: [
      'The oral is 240 marks — 40% of the whole LC Irish grade (out of 600), common to Higher and Ordinary.',
      'An Fáiltiú (greeting) 5 · Léamh na Filíochta (poetry) 35 · An tSraith Pictiúr 80 · An Comhrá 120.',
      'The general conversation alone is 120 — half of the oral, and 20% of your entire Irish result.',
      'That 120 is more than the written composition (An Cheapadóireacht, 100) — the single biggest chunk of LC Irish.',
    ],
    cite: ORAL('p.39 (240 marc: Fáiltiú 5 / Filíocht 35 / Sraith Pictiúr 80 / Comhrá 120)'),
  },
  scripts: [
    {
      id: 'ir6-a',
      label: 'The gamble',
      persona: 'Polishes the set-pieces, wings the chat',
      work: [
        'Poems read fluently; the picture sequences learned off by heart.',
        'But the general conversation is left to chance — no prepared ground on family, hobbies, area or future plans.',
      ],
      keyLevelId: 'comhra',
      keyNote:
        'The Comhrá — 120 marks. It is the single largest part of the oral: half of the 240, and 20% of the entire LC Irish grade — more than the whole written composition (100). Winging it puts more marks at risk than the poems (35) and the picture sequences (80) they polished, combined. Prepare the conversation hardest: stock the predictable ground you will actually be asked about — teaghlach, caitheamh aimsire, ceantar, an todhchaí — in Irish you control.',
      embodies: {
        behaviour:
          'Under-prepares the highest-value oral component (An Comhrá, 120 marks) while over-preparing lower-value set-pieces.',
        cite: ORAL('p.39'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir6',
    rule: 'Prepare the conversation hardest — it is half the oral.',
    detail:
      'The Irish oral is 240 marks (40% of the subject), common to both levels. Within it the general Comhrá is 120 — half the oral and 20% of your whole grade, more than the written composition. The greeting (5), poetry (35) and even the picture sequences (80) carry less. Bank the Comhrá by preparing the predictable ground in Irish you control.',
    cite: ORAL('p.39'),
  },
};

// ─────────────── Ir7 · The Irish is marked in the literature too ───────────────

const LIT_GAEILGE: ScaleLevel[] = [
  { id: 'g1', label: '1 (Cumas lag/an-lag)', annotation: '1', marks: 1 },
  { id: 'g3', label: '3 (Cumas maith)', annotation: '3', marks: 3 },
  { id: 'g5', label: '5 (Sárchumas)', annotation: '5', marks: 5 },
];

const IR7: ScaleSession = {
  mode: 'scale',
  id: 'ir-litriocht-gaeilge',
  subject: 'irish',
  level: 'higher',
  title: 'The Irish is marked in the literature too',
  cue: 'Prós / Filíocht',
  question:
    'A Prós answer discusses the statement well, with rich textual reference — but the Irish itself is error-strewn: wrong verb tenses, broken syntax, misused prepositions. Every literature question (Prós, Filíocht, Litríocht Bhreise) awards a SEPARATE 5 marks for the standard of the Irish, on top of the content (Eolas) mark — Prós is 25 Eolas + 5 Gaeilge = 30. Where does that 5-mark language award land?',
  questionNote:
    'Scenario authored for this exercise. The separate 5-mark Gaeilge award on each literature answer is the real SEC rule ("beidh 5 mharc le bronnadh i ngach cás ar chaighdeán na Gaeilge"): it is judged on the príomhghnéithe de cheart na teanga — gramadach, comhréir, struchtúr, deilbhíocht.',
  scale: {
    name: 'Litríocht · Gaeilge · /5',
    levels: LIT_GAEILGE,
    notes: [
      'Each literature answer is Eolas (content) + a separate 5-mark Gaeilge (language) award — Prós/Filíocht 25 + 5 = 30, Litríocht Bhreise 35 + 5 = 40.',
      'The 5-mark Gaeilge scale runs 5 Sárchumas · 4 Cumas an-mhaith · 3 Cumas maith · 2 Cumas measartha · 1 Cumas lag/an-lag.',
      'It is judged on the príomhghnéithe de cheart na teanga: grammar, syntax, structure, morphology (gramadach, comhréir, struchtúr, deilbhíocht).',
      'Strong content earns its Eolas marks — but broken Irish keeps this separate 5-mark award in the low band.',
    ],
    cite: MS('p.27 (literature 5-mark Gaeilge award: "25 ar Eolas agus 5 ar Ghaeilge")'),
  },
  scripts: [
    {
      id: 'ir7-a',
      label: 'The answer',
      persona: 'Fine points, broken Irish',
      work: [
        'Discusses the statement well, with strong, apt textual reference.',
        'But the Irish is error-strewn: wrong verb tenses, broken syntax, misused prepositions.',
      ],
      keyLevelId: 'g1',
      keyNote:
        'The Eolas marks (25) are judged separately and the discussion can still score there — but the 5-mark Gaeilge award lands in the low band, because it measures ceart na teanga and the syntax is broken. Even in a literature answer that is "about" a text, 5 of every 30 marks reward the Irish itself. Write the discussion in accurate Irish you control.',
      embodies: {
        behaviour: 'Strong literary content undermined by error-strewn Irish — forfeiting the separate 5-mark Gaeilge award.',
        cite: MS('p.27'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir7',
    rule: 'Even in the literature answers, the Irish itself is marked.',
    detail:
      'Prós, Filíocht and Litríocht Bhreise each carry a separate 5-mark Gaeilge award on top of the content (Eolas) mark — 25 Eolas + 5 Gaeilge = 30. Excellent points in broken Irish still lose those 5 marks. Write the discussion in accurate, controlled Irish.',
    cite: MS('p.27'),
  },
};

// ─────────────── Ir8 · The precise detail buys the second mark ───────────────

const AURAL_PRECISION: ScaleLevel[] = [
  { id: 'm0', label: '0 (wrong)', annotation: '0', marks: 0 },
  { id: 'm1', label: '1 (vague / partly named)', annotation: '1', marks: 1 },
  { id: 'm2', label: '2 (precise / fully named)', annotation: '2', marks: 2 },
];

const IR8: ScaleSession = {
  mode: 'scale',
  id: 'ir-aural-precision',
  subject: 'irish',
  level: 'common',
  title: 'The precise detail buys the second mark',
  cue: 'Cluastuiscint',
  question:
    'A Cluastuiscint item worth 2 marks asks who broadcast a notice. The recording names "RTÉ Raidió na Gaeltachta". The candidate hears it but writes only "RTÉ". The scheme awards the full 2 marks for the fully-named detail and 1 mark for the vague, partly-named version. What does "RTÉ" score?',
  questionNote:
    'Scenario authored for this exercise, but the mark values are the real SEC scheme\'s: "RTÉ Raidió na Gaeltachta = 2 mharc … RTÉ = 1 mharc"; likewise "Ceol beo = 2 mharc … Ceol = 1 mharc". Most aural items are worth 2 marks, and precision of the retrieved detail is what buys the second one.',
  scale: {
    name: 'Cluastuiscint · precision · /2',
    levels: AURAL_PRECISION,
    notes: [
      'Most Cluastuiscint items are worth 2 marks each.',
      'The full 2 marks need the precise, fully-named detail; a vague or partly-named answer is capped at 1.',
      '"RTÉ Raidió na Gaeltachta" = 2, "RTÉ" = 1; "Ceol beo" = 2, "Ceol" = 1; "Agallaimh spéisiúla" = 2, "Agallaimh" = 1.',
      'This is separate from the 0–3 standard-of-Irish deduction — it is about how completely you named the thing you heard.',
    ],
    cite: MS('p.7 ("RTÉ Raidió na Gaeltachta = 2 mharc … RTÉ = 1 mharc")'),
  },
  scripts: [
    {
      id: 'ir8-a',
      label: 'The answer',
      persona: 'Heard it, half-named it',
      work: ['Writes "RTÉ" for who broadcast the notice — when the recording said "RTÉ Raidió na Gaeltachta".'],
      keyLevelId: 'm1',
      keyNote:
        '1 of 2 — the answer is not wrong, but it is vague. The second mark is reserved for the precise, fully-named detail ("RTÉ Raidió na Gaeltachta"), and a general "RTÉ" only earns half. The listening was fine; the loss is in the writing-down. Note the exact, full name you hear.',
      embodies: {
        behaviour: 'Gives a vague, partly-named aural answer where the full name was heard — capped at half the item\'s marks.',
        cite: MS('p.7'),
      },
    },
    {
      id: 'ir8-b',
      label: 'The answer',
      persona: 'Names it in full',
      work: ['Writes "RTÉ Raidió na Gaeltachta" in full for who broadcast the notice.'],
      keyLevelId: 'm2',
      keyNote:
        'Full 2 marks — the detail is named completely and specifically, which is exactly what the second mark rewards. The difference between 1 and 2 here is not understanding but precision: the whole name, the whole phrase, written down as heard.',
      embodies: {
        behaviour: 'Gives the precise, fully-named aural answer — earning the full 2 marks.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ir8',
    rule: 'In the aural, the precise detail buys the second mark.',
    detail:
      'Most Cluastuiscint items are worth 2 marks, and a vague or partly-named answer scores only 1: "RTÉ" earns 1, "RTÉ Raidió na Gaeltachta" earns 2. Write the full, specific detail you heard — the exact name, the whole phrase — not an approximation.',
    cite: MS('p.7'),
  },
};

export const IRISH_CHAIR: ChairSubject = {
  id: 'irish',
  label: 'Irish',
  tagline: 'Where language accuracy, genre, “own words”, precise detail — and the 40% oral — win the marks.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [IR1, IR2, IR3, IR4, IR5, IR6, IR7, IR8],
  sources: [
    { label: 'SEC LC Irish HL marking scheme 2025 (examiner-reports/irish/2025-marking-scheme)' },
    { label: 'SEC LC Irish OL marking scheme 2025 (examiner-reports/irish/2025-ol-marking-scheme)' },
    {
      label:
        'SEC LC Assessment Arrangements 2026 — An Bhéaltriail Chomónta (examiner-reports/irish/2026-assessment-arrangements-oral)',
    },
  ],
  coverageNote:
    'The composition (language is ~80% of the mark), genre, and Cluastuiscint (aural) sessions apply at both levels — the aural sessions teach the 0–3 standard-of-Irish deduction and the 2-mark precision rule (vague retrieval scores half) that apply even in the listening comprehension. The “own words” comprehension rule is Higher-specific (OL comprehension has no own-words gate); the Ordinary session covers OL poetry’s “i d’fhocail féin” halving; the literature 5-mark Gaeilge award (a separate language mark on each Prós/Filíocht/Litríocht Bhreise answer) is verified against the Higher scheme. The oral session teaches the 240-mark / 40% component split of the common Béaltriail (Fáiltiú 5 / Filíocht 35 / Sraith Pictiúr 80 / Comhrá 120), verified against the SEC Assessment Arrangements 2026; the internal per-component oral marking grid is a separate scheme and is not asserted here. The written rules are verified against the 2025 HL and OL schemes.',
};
