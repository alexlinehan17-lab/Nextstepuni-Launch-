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
  ],
  takeaway: {
    id: 'codex-eng3',
    rule: 'Evidence is the discriminator, not the point.',
    detail:
      'Everyone makes the obvious points; the marks separate on the evidence beneath them. Use precise, accurate references that actually show the claim — vague or careless quotation undermines the whole answer.',
    cite: CER('p.18'),
  },
};

export const ENGLISH_CHAIR: ChairSubject = {
  id: 'english',
  label: 'English',
  tagline: 'PCLM — why answering the question beats writing beautifully.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [ENG1, ENG2, ENG3],
  sources: [
    { label: 'SEC LC English HL marking scheme 2025 (examiner-reports/english/2025-marking-scheme)' },
    { label: 'Chief Examiner’s Report, English 2013 (examiner-reports/english/2013-chief-examiner)' },
  ],
  coverageNote:
    'These sessions teach the PCLM criteria and the primacy-of-Purpose rule, which the scheme applies to every task on both papers at Higher and Ordinary level. Verified against the 2025 Higher Level scheme; level-specific worked examples are being added.',
};
