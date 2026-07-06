/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Classical Studies (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the essay "unit of development" = point + evidence +
 * development, the narrative-caps-Overall-Quality rule, and the two-part
 * structural cap) is the real SEC system, cited to:
 *  - SEC LC Classical Studies HL marking scheme 2025 —
 *    examiner-reports/classical-studies/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Classical Studies HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Classical Studies OL marking scheme 2025, ${p}` });

// ─────────────── CL1 · A unit needs all three parts ───────────────

const CL1: GridSession = {
  mode: 'grid',
  id: 'cl-unit',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Point, evidence, development',
  cue: 'Essay',
  question: 'Section B essays score 15 marks per “unit of development”, and a full unit needs all three parts: a relevant point, relevant evidence, and development (analysis/elaboration). A candidate makes a strong point with good evidence — but never analyses or develops it. How much of the 15 does the unit earn?',
  questionNote:
    'Scenario authored for this exercise. A markable Classical Studies essay unit requires a relevant point, relevant evidence, AND development; a well-developed unit scores 15, a merely stated point-with-evidence sits far lower.',
  grid: {
    perPoint: [
      { id: 'point', label: 'Relevant point', marks: 4 },
      { id: 'evidence', label: 'Relevant evidence', marks: 4 },
      { id: 'development', label: 'Development (analysis)', marks: 7 },
    ],
    shorthand: '15 per unit: point + evidence + development',
    ruleNote:
      'All three parts are needed for a well-developed unit. The development — the analysis, elaboration or discussion — carries the most, and a point-plus-evidence that stops before analysing lands in the lower “basic/developed” bands, not the top.',
    cite: MS('p.11 (unit of development structure)'),
  },
  scripts: [
    {
      id: 'cl1-a',
      label: 'The unit',
      persona: 'Point + evidence, no analysis',
      attempts: [
        {
          id: 'cl1-a-1',
          text: 'A relevant point, backed by an accurate piece of evidence from the text — but the answer moves straight on without analysing what the evidence shows.',
          key: { point: 4, evidence: 4, development: 0 },
          keyNote: 'Point and evidence are there (8), but a full unit needs development — the analysis of what the evidence demonstrates about the point. Without it the unit stays in the lower bands. One sentence of “this shows that…” is what lifts a unit toward the full 15.',
        },
      ],
      embodies: {
        behaviour: 'States a point with evidence but never develops it — the unit stalls below full marks.',
        cite: MS('p.11'),
      },
    },
    {
      id: 'cl1-b',
      label: 'The unit',
      persona: 'All three parts',
      attempts: [
        {
          id: 'cl1-b-1',
          text: 'The same point and evidence, then a sentence analysing what the evidence reveals and why it matters to the question.',
          key: { point: 4, evidence: 4, development: 7 },
          keyNote: 'Point, evidence and development — a complete, well-developed unit. 15/15. The analysis is what turned an 8 into a 15.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cl1',
    rule: 'A unit isn’t complete until you analyse the evidence.',
    detail:
      'Classical Studies essay units score on point + evidence + development, and the development carries the most. A point backed by a quote still needs the “this shows that…” analysis to reach the top band. Always analyse your evidence.',
    cite: MS('p.11'),
  },
};

// ─────────────── CL2 · Answer both parts ───────────────

const CL2: ScaleSession = {
  mode: 'scale',
  id: 'cl-two-part',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Both parts, or a hard ceiling',
  cue: 'Essay',
  question: 'A Section B essay has two parts, (a) and (b). A candidate writes a rich answer with four well-developed units — but all of it addresses part (a); part (b) is ignored. The scheme caps a one-part answer’s Overall Quality in the Low range unless the full question is addressed. Roughly where does the 80-mark essay top out?',
  questionNote:
    'Scenario authored for this exercise. The scheme states the answer must address the full question (parts a and b) for more than three units of development to count and for Overall Quality to rise above the Low range — a mid-50s/80 ceiling for a one-sided answer (three units ≈ 45 plus a Low-range quality mark).',
  scale: {
    name: 'Two-part essay ceiling · /80',
    levels: [
      { id: 'm57', label: 'Max ~mid-50s (one part only)', annotation: '~55', marks: 56 },
      { id: 'm80', label: 'Up to 80 (both parts)', annotation: '80', marks: 80 },
    ],
    notes: [
      'The essay must address the full question — both (a) and (b).',
      'A one-part answer: no more than three units count, and Overall Quality can’t rise above the Low range.',
      'That imposes a structural ceiling in the mid-50s/80 (three units max ≈ 45, plus a Low-range quality mark), however good the one part is.',
    ],
    cite: MS('p.11 (full-question requirement)'),
  },
  scripts: [
    {
      id: 'cl2-a',
      label: 'The essay',
      persona: 'Brilliant — on part (a) only',
      work: [
        'Four well-developed units, all on part (a).',
        'Part (b) of the question is never addressed.',
      ],
      keyLevelId: 'm57',
      keyNote:
        'Capped in the mid-50s of 80 — a one-part answer can’t have more than three units count, and its Overall Quality is held in the Low range, no matter how strong part (a) is. Even a short, weaker treatment of part (b) removes the ceiling. Always give both parts of the question real attention.',
      embodies: {
        behaviour: 'Answers only one part of a two-part essay — hitting the structural ceiling.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl2',
    rule: 'Address both parts, or you’re capped in the mid-50s/80.',
    detail:
      'A one-sided answer to a two-part Classical Studies essay caps its units and holds Overall Quality in the Low range — the mid-50s out of 80. Give both parts genuine treatment; even a brief second part lifts the ceiling.',
    cite: MS('p.11'),
  },
};

// ─────────────── CL3 · Narrative caps Quality ───────────────

const CL3: ScaleSession = {
  mode: 'scale',
  id: 'cl-narrative',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Retelling isn’t arguing',
  cue: 'Essay (Overall Quality)',
  question: 'The essay’s Overall Quality is scored out of 20. A candidate retells the myth or the events accurately and vividly, but never builds an argument in response to the question. The Low Quality band is defined as “relies mostly on narrative”. Where does Overall Quality land?',
  questionNote:
    'Scenario authored for this exercise. Overall Quality (20 of the 80) is a separate holistic mark; its Low band is explicitly “relies mostly on narrative”, so a retelling can’t reach the High band.',
  scale: {
    name: 'Overall Quality · /20',
    levels: [
      { id: 'low', label: 'Low — narrative', annotation: 'L', marks: 10 },
      { id: 'good', label: 'Good', annotation: 'G', marks: 15 },
      { id: 'high', label: 'High', annotation: 'H', marks: 19 },
    ],
    notes: [
      'Overall Quality is a separate 20 marks on top of the units.',
      'Low band: “relies mostly on narrative”.',
      'Higher bands need argument and analysis in response to the question, not retelling.',
    ],
    cite: MS('p.11 (Overall Quality bands)'),
  },
  scripts: [
    {
      id: 'cl3-a',
      label: 'The essay',
      persona: 'Vivid retelling',
      work: [
        'Accurate, vivid narration of the myth/events.',
        'No argument built in response to the question.',
      ],
      keyLevelId: 'low',
      keyNote:
        'Low Quality band — “relies mostly on narrative” is exactly this essay, so Overall Quality is held in the Low band however vivid the storytelling. The higher bands are bought with argument: use the narrative as evidence for points that answer the question, don’t let it be the answer.',
      embodies: {
        behaviour: 'Retells the story instead of arguing — the named Low Quality descriptor.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl3',
    rule: 'Use the story as evidence, don’t just retell it.',
    detail:
      'Classical Studies Overall Quality caps in the Low band when an essay “relies mostly on narrative”. Turn the narrative into evidence for an argument that answers the question — retelling alone can’t reach the top.',
    cite: MS('p.11'),
  },
};

// ─────────────── CL4 · OL — Section A is the mark bank ───────────────

const CL4: ScaleSession = {
  mode: 'scale',
  id: 'cl-ol-section-a',
  subject: 'classical-studies',
  level: 'ordinary',
  title: 'At OL, the short answers are the marks',
  cue: 'Exam strategy (OL)',
  question: 'At Ordinary Level, Section A (the stimulus short-answer questions) is worth 300 marks and Section B (the essays) only 100 — the reverse of Higher, where the essays dominate. A candidate rushes the Section A short answers to leave lots of time for a long essay. Is that the right allocation?',
  questionNote:
    'Scenario authored for this exercise. At OL the mark split is inverted versus HL: Section A = 300, Section B = 100. Short-answer accuracy is where the marks are; the essays are worth far less.',
  scale: {
    name: 'OL time allocation',
    levels: [
      { id: 'wrong', label: 'Rush A, pour time into the essay', annotation: '✗', marks: 30 },
      { id: 'right', label: 'Bank Section A carefully first', annotation: '✓', marks: 90 },
    ],
    notes: [
      'OL Section A = 300 marks; Section B (essays) = 100. HL is the reverse (200/200, essays heavy).',
      'The stimulus short-answers are the mark bank — accuracy and coverage there decide the grade.',
      'Rushing Section A to write a long essay chases the smaller pot.',
    ],
    cite: MSOL('p.6, p.12 (Section A 300 / Section B 100)'),
  },
  scripts: [
    {
      id: 'cl4-a',
      label: 'The strategy',
      persona: 'Rushes A for a big essay',
      work: ['Hurries through the Section A short answers.', 'Spends the saved time on one long Section B essay.'],
      keyLevelId: 'wrong',
      keyNote:
        'Backwards for OL — Section A holds 300 of the 400 marks, so rushing it to write a longer essay chases the 100-mark pot at the expense of the 300-mark one. At Ordinary Level, give the stimulus short-answers your care and time first; the essay matters far less than it does at Higher. Spend your minutes where the marks are.',
      embodies: {
        behaviour: 'Under-invests in the 300-mark Section A to write a longer 100-mark essay — the wrong OL allocation.',
        cite: MSOL('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl4',
    rule: 'At OL, Section A holds most of the marks — spend your time there.',
    detail:
      'Ordinary Level Classical Studies inverts the HL split: Section A short-answers are 300 marks, the essays only 100. Give the stimulus questions your care and time; the essay is worth far less than at Higher.',
    cite: MSOL('p.6'),
  },
};

// ─────────────── CL5 · The picture question needs both sources ───────────────

const CL5: ScaleSession = {
  mode: 'scale',
  id: 'cl-picture',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Read the picture AND the text',
  cue: 'Stimulus (picture question)',
  question:
    'A Section A picture question gives you an image and an extract from the Aeneid and asks you to agree or disagree with a claim, for 7 marks. A candidate writes a sharp, specific reading of the image — but never once engages the Aeneid text. The scheme says “Discussion of both the text and the image for full marks.” Where does the answer top out?',
  questionNote:
    'Scenario authored for this exercise. The 7-mark picture question’s top band requires engaging both the image and the accompanying text; an answer that discusses only one source cannot reach full marks, however good that half is.',
  scale: {
    name: 'Picture question · /7',
    levels: [
      { id: 'cl5-yn', label: 'Yes/no only', annotation: '1', marks: 1 },
      { id: 'cl5-basic', label: 'Basic, generic', annotation: '2', marks: 2 },
      { id: 'cl5-partial', label: 'Partial — one source', annotation: '4', marks: 4 },
      { id: 'cl5-full', label: 'Full — image and text', annotation: '7', marks: 7 },
    ],
    notes: [
      '“Discussion of both the text and the image for full marks.”',
      'Full 7: “full, detailed answer, specific points, refers to image and Aeneid.”',
      'Engage only one source, however well, and the answer can’t clear the partial band.',
    ],
    cite: MS('p.6 (Q1(b) picture question)'),
  },
  scripts: [
    {
      id: 'cl5-a',
      label: 'The answer',
      persona: 'Brilliant on the image, silent on the text',
      work: [
        'A specific, detailed reading of the image, with a clear stance.',
        'The Aeneid extract beside it is never discussed.',
      ],
      keyLevelId: 'cl5-partial',
      keyNote:
        'Capped at partial (4 of 7). Full marks explicitly require discussing both the text and the image, so a one-source answer — however sharp — can’t reach the top band. On a picture question, always turn to the accompanying passage and tie the two sources together; that second source is what unlocks the full 7.',
      embodies: {
        behaviour: 'Discusses only one of the two required sources on a picture question — capped below full marks.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl5',
    rule: 'On a picture question, discuss both the image and the text.',
    detail:
      'Classical Studies picture questions award full marks only for “discussion of both the text and the image”. A brilliant reading of just one source is capped at partial. Always engage both, and connect them.',
    cite: MS('p.6'),
  },
};

// ─────────────── CL6 · A bare “yes” scores one mark ───────────────

const CL6: ScaleSession = {
  mode: 'scale',
  id: 'cl-yesno',
  subject: 'classical-studies',
  level: 'higher',
  title: 'A bare “yes” scores one mark',
  cue: 'Stimulus (personal response)',
  question:
    'A 15-mark personal-response question asks you to agree or disagree and explain, with reference to the poetry. A candidate writes “Yes, I agree” — a clear stance — and stops there, with no explanation. The scheme’s floor is explicit: “1 mark – only answers yes or no, no other valid point made.” Where does it land, and what lifts it?',
  questionNote:
    'Scenario authored for this exercise. This yes/no floor recurs across the paper: the stance is free, but with no supporting explanation the answer scores the absolute minimum.',
  scale: {
    name: 'Personal response · /15',
    levels: [
      { id: 'cl6-yn', label: 'Yes/no, nothing more', annotation: '1', marks: 1 },
      { id: 'cl6-basic', label: 'Basic — limited explanation', annotation: '5', marks: 5 },
      { id: 'cl6-partial', label: 'Partial — specific points', annotation: '10', marks: 10 },
      { id: 'cl6-full', label: 'Full — fully developed', annotation: '15', marks: 15 },
    ],
    notes: [
      'Full 15: “opinion given and explanation fully developed.”',
      'Floor: “1 mark – only answers yes or no, no other valid point made.”',
      'The stance itself earns nothing — every mark is in the justification.',
    ],
    cite: MS('p.10 (Q11(a)(ii) personal response)'),
  },
  scripts: [
    {
      id: 'cl6-a',
      label: 'The answer',
      persona: 'States a view, justifies nothing',
      work: ['“Yes, I agree.”', 'No explanation, evidence or reference to the poetry follows.'],
      keyLevelId: 'cl6-yn',
      keyNote:
        'The yes/no floor: 1 of 15. A stance with no justification triggers the named minimum, and the same rule appears on other stimulus parts too. Deciding your view is worth nothing on its own — the marks live entirely in the “because…”. Even a couple of specific reasons jump this from 1 to the partial band.',
      embodies: {
        behaviour: 'Gives a bare yes/no stance with no supporting explanation — the named yes/no floor.',
        cite: MS('p.10 (also p.6, p.8)'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl6',
    rule: 'The stance is free; the marks are in the “because”.',
    detail:
      'A bare “yes” or “no” with no explanation scores just 1 mark — the named floor across Classical Studies stimulus questions. Never stop at your view; the justification is the entire answer.',
    cite: MS('p.10'),
  },
};

// ─────────────── CL7 · Don’t confuse Greek and Roman ───────────────

const CL7: ScaleSession = {
  mode: 'scale',
  id: 'cl-confusion',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Confuse Greek and Roman, lose the marks',
  cue: 'Stimulus (short answer)',
  question:
    'A 6-mark question asks for one developed point on ancient Greek funerary practices. A candidate writes a genuinely well-developed point — but describes Roman practices as if they were Greek, mixing the two cultures. The scheme rules: “max 3 marks if Greek and Roman roles/practices are confused.” Where does this otherwise-strong answer land?',
  questionNote:
    'Scenario authored for this exercise. Development normally carries the full 6, but conflating the two cultures triggers a hard cap at 3 — a content-accuracy ceiling, not a development one.',
  scale: {
    name: 'Confusion cap · /6',
    levels: [
      { id: 'cl7-basic', label: 'Basic, generic', annotation: '2', marks: 2 },
      { id: 'cl7-confused', label: 'Developed but confused — capped', annotation: '3', marks: 3 },
      { id: 'cl7-full', label: 'Full — developed and accurate', annotation: '6', marks: 6 },
    ],
    notes: [
      'One developed point earns the full 6 — when the culture is right.',
      '“max 3 marks if Greek and Roman roles/practices are confused.”',
      'Conflating the two cultures pulls even a well-developed point down to 3.',
    ],
    cite: MS('p.9 (Q9(c) funerary practices)'),
  },
  scripts: [
    {
      id: 'cl7-a',
      label: 'The answer',
      persona: 'Well-developed, wrong culture',
      work: [
        'A developed, detailed point about funerary practices.',
        'But it attributes Roman customs to the Greeks, blurring the two.',
      ],
      keyLevelId: 'cl7-confused',
      keyNote:
        'Capped at 3 of 6. The development is real, but the confusion cap overrides it — mixing Greek and Roman practices halves what a clean answer would have scored. Keep the two cultures firmly apart: on Classical Studies short answers, factual precision about which world you’re describing is worth as much as the development itself.',
      embodies: {
        behaviour: 'Develops a point but attributes Roman practices to Greek culture — triggering the confusion cap.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl7',
    rule: 'Keep Greek and Roman apart, or the mark is capped.',
    detail:
      'A well-developed funerary-practices answer is capped at “max 3 marks if Greek and Roman roles/practices are confused”. Content accuracy about which culture you’re describing can override development — don’t blur the two worlds.',
    cite: MS('p.9'),
  },
};

export const CLASSICAL_CHAIR: ChairSubject = {
  id: 'classical-studies',
  label: 'Classical Studies',
  tagline: 'Develop your units, answer both parts, argue not narrate.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CL1, CL2, CL3, CL4, CL5, CL6, CL7],
  sources: [
    { label: 'SEC LC Classical Studies HL marking scheme 2025 (examiner-reports/classical-studies/2025-marking-scheme)' },
    { label: 'SEC LC Classical Studies OL marking scheme 2025 (examiner-reports/classical-studies/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The unit-of-development and Overall Quality sessions apply at both levels (OL softens “develops” to “some development” and drops the top quality tier). The Section A sessions capture the stimulus-question marking grammar — engage both sources on picture questions, the yes/no floor, and the Greek/Roman confusion cap. The Ordinary session captures OL’s inverted mark split — Section A 300 / essays 100. Verified against the 2025 HL and OL schemes.',
};
