/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — English (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * PCLM marking grammar (the four criteria and their 30/30/30/10 split, the
 * primacy-of-Purpose cap, and the compulsory-section mark structure) is the
 * real SEC system, cited to:
 *  - SEC LC English HL marking scheme 2025 —
 *    examiner-reports/english/2025-marking-scheme.*
 *  - Chief Examiner's Report, English 2013 —
 *    examiner-reports/english/2013-chief-examiner.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC English HL marking scheme 2025, ${p}` });
const CER = (p: string) => ({ label: `Chief Examiner's Report, English 2013, ${p}` });
const MSOL = (p: string) => ({ label: `SEC English OL marking scheme 2025, ${p}` });

// ───────────────── Eng1 · Purpose caps everything ─────────────────

const capLevels: ScaleLevel[] = [
  { id: 'c9', label: '9 (capped to P)', annotation: '9', marks: 9 },
  { id: 'c14', label: '14', annotation: '14', marks: 14 },
  { id: 'c18', label: '18 (uncapped)', annotation: '18', marks: 18 },
];

const ENG1: ScaleSession = {
  mode: 'scale',
  id: 'eng-purpose-cap',
  subject: 'english',
  level: 'common',
  title: 'Purpose caps everything',
  cue: 'PCLM',
  question: 'A Single Text answer is written in gorgeous, fluent prose — but it barely engages with the actual question, drifting into a general character study. The examiner judges Clarity of Purpose as low (9/18). The language, taken alone, would be worth 18/18. What is the final mark for Coherence (out of 18)?',
  questionNote:
    'Scenario authored for this exercise. English is marked on PCLM — Purpose, Coherence, Language (each 30%) and Mechanics (10%). The primacy-of-Purpose cap is the SEC rule that the marks for Coherence or Language cannot exceed the mark for Clarity of Purpose.',
  scale: {
    name: 'PCLM · Coherence /18',
    levels: capLevels,
    notes: [
      'PCLM: Clarity of Purpose, Coherence of Delivery, Efficiency of Language — each 30% — plus Accuracy of Mechanics 10%.',
      'The rule: marks for Coherence or Language “cannot exceed the marks awarded for Clarity of Purpose.”',
      'Here Purpose is judged at 9/18, so Coherence is capped at 9 — no matter how fluent the writing is.',
    ],
    cite: MS('p.3 (PCLM weightings and the primacy-of-Purpose rule)'),
  },
  scripts: [
    {
      id: 'eng1-a',
      label: 'The answer',
      persona: 'Beautiful writing, off the question',
      work: [
        'Fluent, sophisticated prose throughout.',
        'But it answers a general “character” essay, not the specific question set.',
        'Examiner’s provisional judgement: Purpose 9/18, Language 18/18.',
      ],
      keyLevelId: 'c9',
      keyNote:
        'Because Coherence cannot exceed Purpose, a Purpose of 9 caps Coherence at 9 — even though the delivery, judged alone, was worth far more. Language is capped the same way. In English, answering the actual question (Purpose) is the mark that unlocks all the others. Style can’t rescue an off-question answer.',
      embodies: {
        behaviour: 'Writes fluently but does not engage the question, so a low Purpose caps the other criteria.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'eng1-b',
      label: 'The near-miss',
      persona: 'On the question, but only loosely',
      work: [
        'Clearly aware of the specific question and glances at it throughout.',
        'But the engagement stays loose — the exact terms of the question are touched, not driven.',
        'Examiner’s provisional judgement: Purpose 14/18, Language 18/18.',
      ],
      keyLevelId: 'c14',
      keyNote:
        'A middle-band mark. This answer isn’t off the question — it engages the task, just not tightly — so Purpose lands at 14, not 9. Because Coherence and Language can’t exceed Purpose, both are capped at 14: the fluent language that was worth 18 alone is pulled down to meet Purpose. The lesson isn’t “style is wasted” but “style is worth exactly as much as your engagement lets it be.” Tighten the answer onto the precise terms of the question and the cap rises with it.',
      embodies: {
        behaviour: 'Engages the question loosely, earning a mid-band Purpose that caps the fluent Language at the same level.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-eng1',
    rule: 'Purpose is the mark that unlocks the others.',
    detail:
      'In PCLM, Coherence and Language can never score higher than Clarity of Purpose. Answer the exact question first — no amount of beautiful writing lifts a mark that Purpose has capped.',
    cite: MS('p.3'),
  },
};

// ───────────────── Eng2 · The compulsory poem ─────────────────

const ENG2: ScaleSession = {
  mode: 'scale',
  id: 'eng-unseen-poem',
  subject: 'english',
  level: 'common',
  title: 'The section you can’t skip',
  cue: 'Strategy',
  question: 'A strong candidate is short on time in Paper 2 and decides to skip the Unseen Poem — “it’s only 20 marks and there’s no way to prepare for it.” What does that decision cost?',
  questionNote:
    'Scenario authored for this exercise. The Unseen Poem is a compulsory 20-mark section of the Paper 2 Poetry question; the Chief Examiner’s Report flags skipping it as a real and costly error.',
  scale: {
    name: 'Unseen Poem · /20',
    levels: [
      { id: 'm0', label: '0 (skipped)', annotation: '0', marks: 0 },
      { id: 'm12', label: '~12 (a fair attempt)', annotation: '12', marks: 12 },
      { id: 'm20', label: '20 (full)', annotation: '20', marks: 20 },
    ],
    notes: [
      'The Unseen Poem is compulsory and worth 20 marks (Poetry = Unseen 20 + Prescribed 50).',
      'There is no single “correct” reading — the scheme rewards a supported personal response, so any thoughtful attempt scores.',
      'Skipping it forfeits “up to twenty marks” — and it was the lowest-scoring element at HL, so a calm attempt beats most of the cohort.',
    ],
    cite: MS('p.42 (Unseen Poem, 20 marks, no correct reading)'),
  },
  scripts: [
    {
      id: 'eng2-a',
      label: 'The decision',
      persona: 'Skips it under time pressure',
      work: ['Leaves the Unseen Poem blank to spend the time elsewhere.'],
      keyLevelId: 'm0',
      keyNote:
        'Zero — a whole grade band’s worth of marks, forfeited. Because there is no “correct” reading, even a few supported observations about tone or an image would have scored; the section is HL’s lowest-scoring, so a modest attempt often beats the average. Never leave a compulsory section blank.',
      embodies: {
        behaviour: 'Does not attempt the compulsory Unseen Poem — a documented loss of up to twenty marks.',
        cite: CER('p.8–9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-eng2',
    rule: 'Never leave a compulsory section blank.',
    detail:
      'The Unseen Poem has no single right answer — a supported personal response always scores, and skipping it forfeits up to 20 marks on HL’s lowest-scoring element. A calm attempt beats a blank every time.',
    cite: MS('p.42'),
  },
};

// ───────────────── Eng3 · Evidence is the discriminator ─────────────────

const ENG3: GridSession = {
  mode: 'grid',
  id: 'eng-evidence',
  subject: 'english',
  level: 'common',
  title: 'The quote that pulls its weight',
  cue: 'Support your view',
  question: 'Two candidates make the same point about a comparative text: that the central relationship is built on control. Each backs it with a reference. Which references actually support the point?',
  questionNote:
    'Scenario authored for this exercise. The Chief Examiner’s Report identifies the quality of evidence cited as “a significant discriminator”, and careless quotation as an answer-underminer; this session trains that judgement.',
  grid: {
    perPoint: [{ id: 'evidence', label: 'Reference supports the point', marks: 3 }],
    shorthand: 'evidence quality · discriminator',
    ruleNote:
      'A point is only as strong as the evidence under it. A precise reference that actually shows the claim earns credit; a vague gesture, a misremembered “quote”, or a plot summary that doesn’t demonstrate the point does not — and careless quotation actively undermines the answer.',
    cite: MS('p.35 (Comparative, PCLM) and CER 2013 p.18 (evidence as discriminator)'),
  },
  scripts: [
    {
      id: 'eng3-a',
      label: 'Script A',
      persona: 'Gestures at the text',
      attempts: [
        {
          id: 'eng3-a-1',
          text: 'You can tell he’s controlling because of the way he acts towards her all the time throughout the whole text.',
          key: { evidence: 0 },
          keyNote: 'The claim is just restated, louder — no moment, no reference, nothing the examiner can weigh. Assertion without evidence doesn’t earn the support mark.',
        },
        {
          id: 'eng3-a-2',
          text: 'There’s a bit where he says something controlling to her, which proves it.',
          key: { evidence: 0 },
          keyNote: '“A bit where he says something” is a non-reference — vague and unverifiable. Careless, near-quotation like this undermines the answer rather than supporting it.',
        },
      ],
      embodies: {
        behaviour: 'Supports a point with vague, careless references — which the report says undermine the answer.',
        cite: CER('p.8'),
      },
    },
    {
      id: 'eng3-b',
      label: 'Script B',
      persona: 'Evidence that shows it',
      attempts: [
        {
          id: 'eng3-b-1',
          text: 'His control is quiet, not loud: he decides where she goes by “offering” to drive her everywhere, so she never travels alone.',
          key: { evidence: 3 },
          keyNote: 'A specific, accurately handled reference that actually demonstrates control. This is the evidence that discriminates a strong answer — it earns the support mark.',
        },
        {
          id: 'eng3-b-2',
          text: 'Even her choice of friends is filtered through his approval, shown when he vets each new name she mentions.',
          key: { evidence: 3 },
          keyNote: 'A second precise, relevant piece of evidence for the same claim. 3 marks — this is what “supported” means.',
        },
      ],
    },
    {
      id: 'eng3-c',
      label: 'Script C',
      persona: 'One that lands, one that doesn’t',
      attempts: [
        {
          id: 'eng3-c-1',
          text: 'He controls the money too — “he kept both bank cards in his own wallet”, so she has to ask him for everything.',
          key: { evidence: 3 },
          keyNote: 'A precise, accurately quoted reference that directly demonstrates financial control. Earns the support mark.',
        },
        {
          id: 'eng3-c-2',
          text: 'And he’s controlling in loads of other ways too, all through the book, you can really see it.',
          key: { evidence: 0 },
          keyNote: 'This is assertion, not evidence — “loads of other ways… all through the book” points to nothing the examiner can weigh. The same candidate can produce a marking reference and a non-reference in consecutive sentences; only the first scores. Make every supporting sentence a real, specific reference.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-eng3',
    rule: 'Evidence is the discriminator, not the point.',
    detail:
      'Everyone makes the obvious points; the marks separate on the evidence beneath them. Use precise, accurate references that actually show the claim — vague or careless quotation undermines the whole answer.',
    cite: CER('p.18'),
  },
};

// ───────────────── Eng4 · Different texts for QA and QB ─────────────────

const ENG4: ScaleSession = {
  mode: 'scale',
  id: 'eng-different-texts',
  subject: 'english',
  level: 'common',
  title: 'A and B on different texts',
  cue: 'Comprehending (Paper 1)',
  question: 'Paper 1 Comprehending has Question A (50) on one text and Question B (50) on a DIFFERENT text — the rule is “candidates may NOT answer a Question A and a Question B on the same text.” A candidate answers both A and B on Text 1. Both are good. What does the section score?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s anomaly procedure: if QA and QB are answered on the same text, mark both out of full marks and disallow the lower.',
  scale: {
    name: 'Comprehending · same-text answers',
    levels: [
      { id: 'm45', label: '45 (only the higher counts)', annotation: '45', marks: 45 },
      { id: 'm90', label: '90 (if on different texts)', annotation: '90', marks: 90 },
    ],
    notes: [
      'QA (50) and QB (50) must be on different texts.',
      'If both are on the same text, both are marked but the lower is disallowed.',
      'So one strong answer is thrown away — up to a whole 50-mark question lost.',
    ],
    cite: MS('p.4, p.169 (different-text rule and anomaly procedure)'),
  },
  scripts: [
    {
      id: 'eng4-a',
      label: 'The section',
      persona: 'Both answers on Text 1',
      work: ['Question A — a strong answer on Text 1.', 'Question B — another strong answer, also on Text 1.'],
      keyLevelId: 'm45',
      keyNote:
        'Only the higher of the two counts — the lower is disallowed because they’re on the same text, so a whole strong answer is thrown away. Half the section’s marks can vanish to a rule that has nothing to do with quality. Always take Question A and Question B from different texts.',
      embodies: {
        behaviour: 'Answers QA and QB on the same text, so the lower answer is disallowed.',
        cite: MS('p.169'),
      },
    },
  ],
  takeaway: {
    id: 'codex-eng4',
    rule: 'Question A and Question B must be on different texts.',
    detail:
      'On Paper 1 Comprehending, answering QA and QB on the same text gets the lower of the two disallowed — up to a whole 50-mark answer wasted. Pick your two texts before you start writing.',
    cite: MS('p.4'),
  },
};

// ───────────────── Eng5 · Mechanics is only 10% ─────────────────

const ENG5: ScaleSession = {
  mode: 'scale',
  id: 'eng-mechanics',
  subject: 'english',
  level: 'common',
  title: 'Neat, empty, and low',
  cue: 'PCLM',
  question: 'Accuracy of Mechanics (spelling and grammar) is only 10% of a task’s marks; Purpose, Coherence and Language are 30% each. A candidate hands in a mechanically flawless answer — perfect spelling and grammar — that barely engages the task and says little. On a 100-mark composition, roughly where does it land?',
  questionNote:
    'Scenario authored for this exercise. PCLM weights Mechanics at just 10%; flawless spelling and grammar can’t compensate for weak Purpose, Coherence and Language (90% between them).',
  scale: {
    name: 'PCLM · Mechanics 10%',
    levels: [
      { id: 'm20', label: '~20 (flawless mechanics, little else)', annotation: '20', marks: 20 },
      { id: 'm55', label: '~55 (mid all round)', annotation: '55', marks: 55 },
      { id: 'm85', label: '~85 (strong P/C/L + mechanics)', annotation: '85', marks: 85 },
    ],
    notes: [
      'Weightings: Purpose 30 + Coherence 30 + Language 30 + Mechanics 10.',
      'Perfect mechanics is worth at most 10 of 100 — it can’t carry an answer.',
      'The marks live in engaging the task (P), sustaining it (C) and controlling language (L).',
    ],
    cite: MS('p.3 (PCLM weightings)'),
  },
  scripts: [
    {
      id: 'eng5-a',
      label: 'The answer',
      persona: 'Immaculate spelling, empty content',
      work: [
        'Flawless spelling and grammar throughout.',
        'Barely engages the task; little to say, thinly sustained.',
      ],
      keyLevelId: 'm20',
      keyNote:
        'Low — perfect mechanics is only 10% of the marks, and Purpose, Coherence and Language (the other 90%) are all weak. Neatness can’t rescue an empty answer. Students who pour effort into tidy handwriting and spelling while neglecting what they actually say are optimising the smallest criterion. Engage the task first.',
      embodies: {
        behaviour: 'Relies on flawless mechanics while neglecting Purpose/Coherence/Language — optimising the 10% criterion.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-eng5',
    rule: 'Mechanics is only a tenth — engagement is the rest.',
    detail:
      'Spelling and grammar are 10% of an English task; Purpose, Coherence and Language are 90%. Flawless mechanics can’t carry a thin answer — spend your effort engaging the task and sustaining it, not just on neatness.',
    cite: MS('p.3'),
  },
};

// ───────────────── Eng6 · OL — Purpose & Coherence is 60% ─────────────────

const ENG6: ScaleSession = {
  mode: 'scale',
  id: 'eng-ol-pc-split',
  subject: 'english',
  level: 'ordinary',
  title: 'At OL, answering the task is 60%',
  cue: 'Combined criteria (OL)',
  question: 'On an Ordinary Level combined-criteria question, the marks split Purpose & Coherence = 60% and Language & Mechanics = 40%. A candidate writes in plain, simple English — nothing fancy — but genuinely answers the task, stays focused, and develops the point. Where can that land?',
  questionNote:
    'Scenario authored for this exercise. At OL, combined questions are marked in two blocks — P&C (60%) and L&M (40%) — so engaging and sustaining the task banks the majority even in plain language.',
  scale: {
    name: 'OL combined · P&C 60% / L&M 40%',
    levels: [
      { id: 'm40', label: '~40% (fancy language, off-task)', annotation: '40', marks: 40 },
      { id: 'm70', label: '~70% (plain, but on-task & developed)', annotation: '70', marks: 70 },
      { id: 'm90', label: '~90% (on-task + strong language)', annotation: '90', marks: 90 },
    ],
    notes: [
      'OL combined questions split Purpose & Coherence 60% + Language & Mechanics 40%.',
      'Answering the actual task, staying focused and developing it earns the 60% P&C block.',
      'So plain, simple English that genuinely engages the task scores well — you don’t need fancy writing.',
    ],
    cite: MSOL('p.73–74 (combined P&C 60 / L&M 40 split)'),
  },
  scripts: [
    {
      id: 'eng6-a',
      label: 'The answer',
      persona: 'Plain English, on the task',
      work: [
        'Simple, unfussy language — no ambitious vocabulary.',
        'But it answers exactly what was asked, stays focused, and develops the point.',
      ],
      keyLevelId: 'm70',
      keyNote:
        'It scores well — around 70% — because Purpose & Coherence is 60% of the mark, and this answer earns that block: it engages the task and sustains it. At OL you don’t need elaborate language to do well; you need to answer the question and develop it. Plain and on-task beats fancy and off-task every time.',
      embodies: {
        behaviour: 'Uses plain language but genuinely engages and sustains the task — banking the 60% P&C block.',
        cite: MSOL('p.73'),
      },
    },
  ],
  takeaway: {
    id: 'codex-eng6',
    rule: 'At OL, answering the task is 60% of the mark.',
    detail:
      'Ordinary Level combined questions split Purpose & Coherence (60%) and Language & Mechanics (40%). You don’t need fancy writing — engage the exact task, stay focused, and develop your points, and you bank the majority in plain English.',
    cite: MSOL('p.73'),
  },
};

// ───────────────── Eng7 · Question B — genre & register ─────────────────

const ENG7: ScaleSession = {
  mode: 'scale',
  id: 'eng-qb-register',
  subject: 'english',
  level: 'common',
  title: 'The essay that answered the wrong genre',
  cue: 'Comprehending Question B',
  question:
    'Paper 1 Question B is a functional-writing task — write the text of a captain’s pre-match team talk that (a) outlines the game plan, (b) reminds the team of the opponents’ strengths and weaknesses, and (c) motivates them. Purpose here is “Understanding of genre and register”. A candidate writes a fluent, third-person mini-essay ABOUT teamwork instead of a spoken team talk. How high can Purpose (out of 15) go?',
  questionNote:
    'Scenario authored for this exercise, modelled on the SEC Paper 1 Question B template. QB is a functional-writing task marked discretely P15/C15/L15/M5; its Clarity-of-Purpose descriptor is literally “Understanding of genre and register” of the specified task, and the rubric asks candidates to “engage with all aspects of the question, although not necessarily equally.”',
  scale: {
    name: 'QB · Purpose /15 (genre & register)',
    levels: [
      { id: 'p6', label: '6 (wrong genre/register)', annotation: '6', marks: 6 },
      { id: 'p11', label: '11 (right register, an aspect dropped)', annotation: '11', marks: 11 },
      { id: 'p14', label: '14 (right register + all aspects)', annotation: '14', marks: 14 },
    ],
    notes: [
      'QB is functional writing marked discretely P15/C15/L15/M5 — the P descriptor is “Understanding of genre and register” of the task set.',
      'The rubric: “Candidates should engage with all aspects of the question, although not necessarily equally.”',
      'Fluent prose in the wrong genre (an essay where a spoken talk was set) caps Purpose — and by primacy-of-P, a low Purpose then caps Coherence and Language too.',
    ],
    cite: MS('p.6 (Question B: register expected + “Understanding of genre and register” under P)'),
  },
  scripts: [
    {
      id: 'eng7-a',
      label: 'The essay',
      persona: 'Writes about the topic, in the wrong genre',
      work: [
        'Fluent, well-organised prose on the value of teamwork.',
        'But it is a third-person reflective essay — no direct address, no captain’s spoken voice, no talk being delivered.',
        'Right topic, wrong genre and register entirely.',
      ],
      keyLevelId: 'p6',
      keyNote:
        'Purpose is low — around 6 — because QB’s P is “Understanding of genre and register”, and this candidate produced an essay where a spoken team talk was required. The writing is fluent, but fluency lives in Language, and primacy-of-P means a low Purpose caps Language too. Match the genre the task actually sets before you polish a sentence.',
      embodies: {
        behaviour: 'Writes fluently in the wrong genre — ignoring the conventions of the task set, which examiners flag as decisive in functional and composition writing.',
        cite: CER('p.16 (genre conventions “imperative”)'),
      },
    },
    {
      id: 'eng7-b',
      label: 'The near-complete talk',
      persona: 'Right voice, one required aspect missing',
      work: [
        'Adopts the captain’s spoken, motivating register — direct address, rallying tone, the real genre.',
        'Covers the game plan and the motivation to win.',
        'But never mentions the opponents’ strengths and weaknesses — one of the three required aspects is simply absent.',
      ],
      keyLevelId: 'p11',
      keyNote:
        'A solid mid-band Purpose — around 11. The genre and register are right, which is the big win, but the rubric says engage with all aspects of the question, and a whole required aspect (the opponents) is missing. You don’t have to treat the three aspects equally, but you do have to touch each one. Dropping a third of the task holds Purpose below the top band.',
      embodies: {
        behaviour: 'Adopts the correct register but omits one of the question’s required aspects, capping Clarity of Purpose.',
        cite: MS('p.6 (“engage with all aspects of the question”)'),
      },
    },
    {
      id: 'eng7-c',
      label: 'The full talk',
      persona: 'Right genre, right register, all aspects',
      work: [
        'A rousing spoken team talk in the captain’s voice — direct address, urgency, belief.',
        'Outlines the game plan, sizes up the opponents’ strengths and weaknesses, and drives home the motivation to win.',
        'All three required aspects present, in the genre and register the task set.',
      ],
      keyLevelId: 'p14',
      keyNote:
        'Top-band Purpose — around 14. The candidate understood the genre and register (a captain’s spoken talk) and engaged every aspect the question named. With Purpose high, Coherence and Language are free to score to their own level. Genre first, all aspects covered — then the rest of PCLM can follow.',
    },
  ],
  takeaway: {
    id: 'codex-eng7',
    rule: 'Answer the genre that was set — then cover every aspect.',
    detail:
      'Functional writing is marked on “Understanding of genre and register”: an essay where a talk was set caps Purpose no matter how fluent it is. Match the genre, adopt the register, and touch every required aspect of the question — you needn’t weight them equally, but you can’t skip one.',
    cite: MS('p.6'),
  },
};

// ───────────────── Eng8 · Comparative — work through the mode ─────────────────

const ENG8: GridSession = {
  mode: 'grid',
  id: 'eng-comparative-mode',
  subject: 'english',
  level: 'higher',
  title: 'The mode is the lens, not the label',
  cue: 'The Comparative Study',
  question:
    'In the Comparative Study, Clarity of Purpose credits two things: “evidence of understanding of the mode” (Theme or Issue / Cultural Context / General Vision and Viewpoint) and “evidence of effective comparison within the mode”. Mark these points from three candidates’ answers on the same Theme-or-Issue question.',
  questionNote:
    'Scenario authored for this exercise, modelled on the SEC Paper 2 Comparative Study. On the single-question 70-mark format the P sub-mark (P21) explicitly rewards “understanding of the mode” and “effective comparison within the mode”; the GENERAL rubric asks for analysis “in the light of the modes for comparison”. Here each markable point is scored on those two P components.',
  grid: {
    perPoint: [
      { id: 'mode', label: 'Framed through the comparative mode', marks: 2 },
      { id: 'compare', label: 'Comparison sustained across texts', marks: 2 },
    ],
    shorthand: 'P (comparative): mode + comparison',
    ruleNote:
      'A comparative point only banks full Purpose when it does BOTH: reads the texts through the chosen mode (the theme/issue lens, not just plot) AND compares across texts. A prepared single-text character study does neither; a plot-level parallel compares but ignores the mode; only a point that works through the mode AND compares earns both marks.',
    cite: MS('p.35 (Comparative P: “understanding of the mode” + “effective comparison within the mode”) and p.32 (GENERAL: analysis “in the light of the modes for comparison”)'),
  },
  scripts: [
    {
      id: 'eng8-a',
      label: 'Script A',
      persona: 'A prepared single-text essay',
      attempts: [
        {
          id: 'eng8-a-1',
          text: 'Macbeth is consumed by ambition from the moment he hears the witches’ prophecy; his soliloquies chart a mind unravelling into guilt and paranoia.',
          key: { mode: 0, compare: 0 },
          keyNote:
            'A rich, accurate character study — but of one text, with no reference to the comparative mode and no second text in view. Nothing here shows “understanding of the mode”, and there is nothing to compare. Both Purpose components are unmet.',
        },
        {
          id: 'eng8-a-2',
          text: 'He deteriorates further after Duncan’s murder, and by the banquet scene his conscience has curdled into hallucination.',
          key: { mode: 0, compare: 0 },
          keyNote:
            'Still one text, still no mode, still no comparison. A prepared single-text essay ported into the Comparative Study scores nothing for the two P components the section is built on — however good the analysis is in isolation.',
        },
      ],
      embodies: {
        behaviour: 'Reproduces a prepared single-text character essay without working through the mode or comparing texts — the formulaic, off-task approach examiners flag as a loss of focus on the requirements of the task.',
        cite: CER('p.19–20 (formulaic approaches inhibit engagement with the task)'),
      },
    },
    {
      id: 'eng8-b',
      label: 'Script B',
      persona: 'Compares plots, forgets the lens',
      attempts: [
        {
          id: 'eng8-b-1',
          text: 'In both texts the central character dies at the end, and in both a loyal friend is left behind to tell the story.',
          key: { mode: 0, compare: 2 },
          keyNote:
            'This does compare across two texts — the comparison mark is earned. But it compares plot events, not the mode: nothing frames the parallel as, say, how each author explores the complexity of the theme. The mode component stays unmet.',
        },
        {
          id: 'eng8-b-2',
          text: 'Both texts are also set over a short span of time, and both open with a scene of conflict.',
          key: { mode: 0, compare: 2 },
          keyNote:
            'Another genuine cross-text comparison — comparison mark earned again — but still surface parallels, not the thematic mode’s lens. Comparison without the mode banks only half the Purpose available on the point.',
        },
      ],
      embodies: {
        behaviour: 'Compares texts at plot level without framing the comparison through the comparative mode, so only the comparison component of Purpose is met.',
        cite: MS('p.35'),
      },
    },
    {
      id: 'eng8-c',
      label: 'Script C',
      persona: 'Mode and comparison together',
      attempts: [
        {
          id: 'eng8-c-1',
          text: 'In the first text the author uses the protagonist’s guilt-ridden mindset to expose the complexity of ambition — how it corrodes as much as it drives.',
          key: { mode: 2, compare: 0 },
          keyNote:
            'Now the answer works through the mode: it reads the character explicitly as the author’s vehicle for the theme’s complexity. The mode component is earned. But it is still one text, so the comparison mark is not yet available on this point.',
        },
        {
          id: 'eng8-c-2',
          text: 'The second and third texts explore the same complexity from the opposite angle — where one character is destroyed by ambition, another is freed by renouncing it — so across the three, the authors’ differing treatments sharpen the theme.',
          key: { mode: 2, compare: 2 },
          keyNote:
            'Both components: the point is framed through the mode AND sustains comparison across texts. This is the full Purpose the Comparative Study is built to reward — the mode used as a lens, driving a comparison, not named and abandoned.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-eng8',
    rule: 'Work through the mode — don’t just retell a text.',
    detail:
      'Comparative Purpose credits two things: understanding of the mode (Theme or Issue / Cultural Context / General Vision and Viewpoint) and effective comparison within it. A prepared single-text essay earns neither; a plot-level parallel earns only half. Frame every point through the mode, and use it to compare across your texts.',
    cite: MS('p.35'),
  },
};

export const ENGLISH_CHAIR: ChairSubject = {
  id: 'english',
  label: 'English',
  tagline: 'PCLM — why answering the question beats writing beautifully.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [ENG1, ENG2, ENG3, ENG4, ENG5, ENG6, ENG7, ENG8],
  sources: [
    { label: 'SEC LC English HL marking scheme 2025 (examiner-reports/english/2025-marking-scheme)' },
    { label: 'SEC LC English OL marking scheme 2025 (examiner-reports/english/2025-ol-marking-scheme)' },
    { label: 'Chief Examiner’s Report, English 2013 (examiner-reports/english/2013-chief-examiner)' },
  ],
  coverageNote:
    'The PCLM sessions teach the criteria and primacy-of-Purpose rule the scheme applies to every task at both levels. Task-specific sessions are verified against the section they cite: Paper 1 Question B genre & register (common), and the Paper 2 Comparative Study “work through the mode” rule (Higher — the named modes are HL-specific). The Ordinary session is verified against the 2025 OL scheme (grades O1–O8; combined questions split P&C 60% / L&M 40%). More OL-specific worked examples are being added.',
};
