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
const MS24 = (p: string) => ({ label: `SEC Classical Studies HL marking scheme 2024, ${p}` });
const MS24OL = (p: string) => ({ label: `SEC Classical Studies OL marking scheme 2024, ${p}` });

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

// ─────────────── CL8 · Use your sources, don’t just list them ───────────────

const CL8: ScaleSession = {
  mode: 'scale',
  id: 'cl-rsr-sources',
  subject: 'classical-studies',
  level: 'higher',
  title: 'A source in the bibliography does no work',
  cue: 'Research Study Report (Evidence)',
  question:
    'The RSR’s Evidence/Research strand is worth 20 marks. A candidate lists a strong, well-chosen set of scholarly sources in the bibliography — but never brings any of them into the body of the essay to build a point. The descriptor for the bottom band is blunt: “sources included only in bibliography.” Where does the Evidence mark land?',
  questionNote:
    'Scenario authored for this exercise. The RSR Evidence/Research descriptor is a four-band grid; the lowest band is exactly “sources included only in bibliography”, so an unused reading list cannot climb out of it however impressive the titles are.',
  scale: {
    name: 'RSR Evidence/Research · /20',
    levels: [
      { id: 'cl8-biblio', label: 'Sources only in the bibliography', annotation: 'VB', marks: 4 },
      { id: 'cl8-referred', label: 'Sources referred to in the essay', annotation: 'B', marks: 8 },
      { id: 'cl8-discussed', label: 'Sources part of the discussion', annotation: 'T', marks: 13 },
      { id: 'cl8-analysed', label: 'Sources examined and used as evidence', annotation: 'VT', marks: 18 },
    ],
    notes: [
      'Top band: “active incorporation of sources… examined, analysed, used as evidence.”',
      'Bottom band: “sources included only in bibliography.”',
      'A source earns marks only once it does work inside a point — not by being cited at the end.',
    ],
    cite: MS('p.4 (RSR Evidence/Research descriptor)'),
  },
  scripts: [
    {
      id: 'cl8-a',
      label: 'The RSR',
      persona: 'Great reading list, unused',
      work: [
        'A strong, well-chosen bibliography of scholarly sources.',
        'None of them is brought into the essay to build or support a point.',
      ],
      keyLevelId: 'cl8-biblio',
      keyNote:
        'Bottom band — “sources included only in bibliography” describes this exactly, so the Evidence mark stays at the floor however good the reading list looks. The marks climb only as sources move off the reference page and into the argument: referred to, then discussed, then examined and used as evidence. Cite less; use more.',
      embodies: {
        behaviour: 'Lists sources in the bibliography but never incorporates them into the essay — the named bottom band.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl8',
    rule: 'A source only scores once it’s used in the argument.',
    detail:
      'The RSR Evidence strand puts “sources included only in bibliography” at the floor and “examined, analysed, used as evidence” at the top. Weave your reading into your points; a reference list on its own earns nothing.',
    cite: MS('p.4'),
  },
};

// ─────────────── CL9 · Go beyond the printed extract ───────────────

const CL9: ScaleSession = {
  mode: 'scale',
  id: 'cl-wider-evidence',
  subject: 'classical-studies',
  level: 'higher',
  title: 'The extract isn’t enough on its own',
  cue: 'Stimulus (discussion)',
  question:
    'A 12-mark stimulus question gives you an extract to discuss. A candidate writes a sharp, well-developed discussion — but draws only on the printed extract, never bringing in other material they studied. The scheme is explicit: “Must refer to specific points from the extract and other studied evidence for top band.” Where does an extract-only answer top out?',
  questionNote:
    'Scenario authored for this exercise. The top band on this stimulus type requires the printed extract AND other studied evidence; an answer resting on the extract alone is held in the incomplete band, however well argued.',
  scale: {
    name: 'Extract + studied evidence · /12',
    levels: [
      { id: 'cl9-basic', label: 'One valid point', annotation: '3', marks: 3 },
      { id: 'cl9-extract', label: 'Extract only — no wider study', annotation: '6', marks: 6 },
      { id: 'cl9-partial', label: 'Extract + studied evidence, good', annotation: '9', marks: 9 },
      { id: 'cl9-full', label: 'Extract + studied evidence, full', annotation: '12', marks: 12 },
    ],
    notes: [
      '“Must refer to specific points from the extract and other studied evidence for top band.”',
      'Top band (11–12): good discussion supported by the extract AND other studied evidence.',
      'Rest on the printed extract alone and the answer stalls in the incomplete band.',
    ],
    cite: MS('p.8 (Q6(a) discussion)'),
  },
  scripts: [
    {
      id: 'cl9-a',
      label: 'The answer',
      persona: 'All in on the extract',
      work: [
        'A specific, well-developed discussion built entirely on the printed extract.',
        'No other studied text or evidence is brought in.',
      ],
      keyLevelId: 'cl9-extract',
      keyNote:
        'Capped in the incomplete band. The top band explicitly needs the extract AND other studied evidence, so an extract-only answer — however sharp — can’t clear the middle. One line of “as we also see in…” from your wider study is what unlocks the top band. The extract is the starting point, not the whole case.',
      embodies: {
        behaviour: 'Discusses only the printed extract, never bringing in other studied evidence — capped below the top band.',
        cite: MS('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl9',
    rule: 'Back the extract with evidence from your wider study.',
    detail:
      'Top-band stimulus answers “refer to specific points from the extract and other studied evidence”. A brilliant reading of the printed passage alone is capped incomplete — always reach beyond it to the rest of your course.',
    cite: MS('p.8'),
  },
};

// ─────────────── CL10 · Cover both military AND political ───────────────

const CL10: ScaleSession = {
  mode: 'scale',
  id: 'cl-both-strategies',
  subject: 'classical-studies',
  level: 'higher',
  title: 'Three strategies — but all one type',
  cue: 'Stimulus (strategies)',
  question:
    'A 20-mark question asks for three strategies of a leader, with at least one example of each type — military and political. A candidate gives three excellent, well-explained strategies — but every one of them is military; the political side is never addressed. The scheme rules: “if military or political is not addressed, 14 marks max.” Where does it land?',
  questionNote:
    'Scenario authored for this exercise. This question requires both the military and the political dimension; leaving one out triggers a hard cap at 14 of 20, regardless of how strong the strategies covered are.',
  scale: {
    name: 'Strategies coverage cap · /20',
    levels: [
      { id: 'cl10-onetype', label: 'Only military (or only political)', annotation: '14', marks: 14 },
      { id: 'cl10-both', label: 'Both military and political', annotation: '20', marks: 20 },
    ],
    notes: [
      'Any three strategies for full marks, with at least one example of each type.',
      '“if military or political is not addressed, 14 marks max.”',
      'Three brilliant military strategies still cap at 14/20 while the political side is missing.',
    ],
    cite: MS('p.8 (Q7 strategies)'),
  },
  scripts: [
    {
      id: 'cl10-a',
      label: 'The answer',
      persona: 'Three strategies, all military',
      work: [
        'Three well-explained strategies, each showing what it was and why it mattered.',
        'All three are military; no political strategy is addressed.',
      ],
      keyLevelId: 'cl10-onetype',
      keyNote:
        'Capped at 14 of 20. The question needs both a military and a political dimension, so covering only one triggers the named cap however good the three strategies are. Swapping one military strategy for a political one — even a briefer one — lifts the ceiling. When a question names two categories, spend a point in each.',
      embodies: {
        behaviour: 'Addresses only the military strategies when both military and political are required — the named 14-mark cap.',
        cite: MS('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl10',
    rule: 'When a question names two categories, answer in both.',
    detail:
      'The strategies question caps at “14 marks max” if military or political is left out. Three excellent strategies of one type still hit the ceiling — always place at least one point in each named category.',
    cite: MS('p.8'),
  },
};

// ─────────────── CL11 · Depth can replace breadth ───────────────

const CL11: ScaleSession = {
  mode: 'scale',
  id: 'cl-depth-breadth',
  subject: 'classical-studies',
  level: 'higher',
  title: 'One deep point beats five shallow ones',
  cue: 'Stimulus (short answer)',
  question:
    'A 6-mark short-answer question can be answered, the scheme says, with “one well-developed point or two developed points for full marks.” One candidate writes a single, richly developed point and stops, sure they needed more. Another lists five quick, generic points. Who scores the full 6?',
  questionNote:
    'Scenario authored for this exercise. This band structure recurs across Section A: the scheme caps how many points count and lets depth substitute for breadth — one well-developed point reaches the full mark, while a pile of generic points sits in the basic band.',
  scale: {
    name: 'One well-developed point · /6',
    levels: [
      { id: 'cl11-basic', label: 'Generic points, none developed', annotation: '2', marks: 2 },
      { id: 'cl11-partial', label: 'One detailed point', annotation: '4', marks: 4 },
      { id: 'cl11-full', label: 'One well-developed (or two developed)', annotation: '6', marks: 6 },
    ],
    notes: [
      '“One well-developed point or two developed points for full marks.”',
      'Full 6: one very detailed answer; a partial detailed point earns 4.',
      'The scheme caps how many points count — extra generic points add nothing.',
    ],
    cite: MS('p.6 (Q3(b))'),
  },
  scripts: [
    {
      id: 'cl11-a',
      label: 'Answer A',
      persona: 'One deep point, worried it’s too few',
      work: [
        'A single point, developed in real detail with specific evidence.',
        'The candidate stops, anxious the examiner wanted more points.',
      ],
      keyLevelId: 'cl11-full',
      keyNote:
        'Full 6. “One well-developed point… for full marks” — this is exactly it, and nothing was lost by making one point instead of three. Depth is the currency here. When a short-answer is worth a handful of marks, develop one point fully rather than scattering several.',
    },
    {
      id: 'cl11-b',
      label: 'Answer B',
      persona: 'Five quick generic points',
      work: [
        'Five separate points, each a single generic sentence.',
        'None is developed or supported with specific detail.',
      ],
      keyLevelId: 'cl11-basic',
      keyNote:
        'Basic band — 2 of 6. The scheme caps how many points count and rewards development, so five generic points score no better than a couple; there’s simply nowhere for the extra ones to land. Trade three of those sentences for the detail that would develop the first two.',
      embodies: {
        behaviour: 'Lists many undeveloped points expecting quantity to score — but the scheme caps points and rewards depth.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl11',
    rule: 'Develop one point fully rather than list five.',
    detail:
      'Short-answers score on “one well-developed point or two developed points” — the scheme caps how many count. A single deep, evidenced point reaches full; a pile of generic points sits in the basic band.',
    cite: MS('p.6'),
  },
};

// ─────────────── CL12 · OL — a unit needs only “some development” ───────────────

const CL12: GridSession = {
  mode: 'grid',
  id: 'cl-ol-unit',
  subject: 'classical-studies',
  level: 'ordinary',
  title: 'At OL, a unit needs only “some development”',
  cue: 'Essay (OL)',
  question:
    'At Ordinary Level, an essay unit is worth 10 marks and needs a relevant point, relevant evidence, and — in the scheme’s words — “some development of the point”. That’s a gentler bar than Higher Level’s full analysis. A candidate makes a solid point with good evidence but adds no development at all. How much of the 10 does the unit earn?',
  questionNote:
    'Scenario authored for this exercise. The OL unit softens HL’s “develops the point” to “some development” and marks a developed point at the full 10 — but development is still required; point-plus-evidence alone stays a basic unit.',
  grid: {
    perPoint: [
      { id: 'point', label: 'Relevant point', marks: 3 },
      { id: 'evidence', label: 'Relevant evidence', marks: 3 },
      { id: 'development', label: 'Some development', marks: 4 },
    ],
    shorthand: '10 per OL unit: point + evidence + some development',
    ruleNote:
      'The OL third part is only “some development” — a lighter bar than HL’s full analysis — but it is still required. A developed point scores the full 10; a point-plus-evidence with no development is a basic unit.',
    cite: MSOL('p.12 (Q11b unit features)'),
  },
  scripts: [
    {
      id: 'cl12-a',
      label: 'The unit',
      persona: 'Point + evidence, no development',
      attempts: [
        {
          id: 'cl12-a-1',
          text: 'A relevant point backed by accurate evidence — but the answer moves on without any development of what the evidence shows.',
          key: { point: 3, evidence: 3, development: 0 },
          keyNote: 'Point and evidence are there (6), but even at OL a full unit needs “some development”. Without it the unit stays basic. You don’t need Higher-Level depth here — one line of “this shows that…” is enough to lift it to the full 10.',
        },
      ],
      embodies: {
        behaviour: 'Gives point and evidence but no development — a basic OL unit, short of the full 10.',
        cite: MSOL('p.12'),
      },
    },
    {
      id: 'cl12-b',
      label: 'The unit',
      persona: 'Point, evidence, and a line of development',
      attempts: [
        {
          id: 'cl12-b-1',
          text: 'The same point and evidence, plus one sentence developing what the evidence shows about the question.',
          key: { point: 3, evidence: 3, development: 4 },
          keyNote: 'A full OL unit — 10 of 10. The development needn’t be deep HL-style analysis; “some development” is the OL bar, and a single explaining sentence clears it.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-cl12',
    rule: 'At OL, one line of development completes a unit.',
    detail:
      'The OL unit asks for a point, evidence, and “some development” — a lighter bar than Higher Level. You don’t need deep analysis, but you do need a line that develops the point; point-plus-evidence alone stays a basic unit.',
    cite: MSOL('p.12'),
  },
};

// ─────────────── CL13 · OL — put it in your own words ───────────────

const CL13: ScaleSession = {
  mode: 'scale',
  id: 'cl-own-words',
  subject: 'classical-studies',
  level: 'ordinary',
  title: 'Copying the text back proves nothing',
  cue: 'Stimulus (OL)',
  question:
    'An OL question asks you to explain a line from the extract, for 6 marks, marked on level of understanding. A candidate simply copies the sentence straight out of the text as their “explanation”, word for word. The scheme sets a specific floor: “2 marks only repeating text as it appears (not in own words).” Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Where a question tests understanding, reproducing the extract verbatim is explicitly capped at 2 marks — understanding has to be shown in the candidate’s own words.',
  scale: {
    name: 'Own words · /6',
    levels: [
      { id: 'cl13-copy', label: 'Copies the text verbatim', annotation: '2', marks: 2 },
      { id: 'cl13-basic', label: 'Own words, basic', annotation: '4', marks: 4 },
      { id: 'cl13-full', label: 'Own words, shows understanding', annotation: '6', marks: 6 },
    ],
    notes: [
      '“2 marks only repeating text as it appears (not in own words).”',
      'Full 6 rewards understanding shown in your own words.',
      'The mark is for understanding — copying the extract back can’t demonstrate it.',
    ],
    cite: MSOL('p.9 (Q7(a))'),
  },
  scripts: [
    {
      id: 'cl13-a',
      label: 'The answer',
      persona: 'Copies the line out',
      work: [
        'The line from the extract, reproduced word for word.',
        'No paraphrase, no explanation in the candidate’s own words.',
      ],
      keyLevelId: 'cl13-copy',
      keyNote:
        'The copying floor — 2 of 6. Repeating the text as it appears triggers the named cap, because a question about understanding can only be answered by showing it in your own words. Rephrasing the same idea in your own phrasing, even simply, jumps this out of the floor immediately.',
      embodies: {
        behaviour: 'Reproduces the extract verbatim instead of explaining it — the named 2-mark copying floor.',
        cite: MSOL('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl13',
    rule: 'Explain in your own words, don’t copy the extract.',
    detail:
      'An OL understanding question caps at “2 marks only repeating text as it appears (not in own words)”. Lifting the sentence straight from the extract proves nothing — paraphrase it to show you understand it.',
    cite: MSOL('p.9'),
  },
};

// ─────────────── CL14 · Answer on the right myth ───────────────

const CL14: ScaleSession = {
  mode: 'scale',
  id: 'cl-wrong-myth',
  subject: 'classical-studies',
  level: 'higher',
  title: 'The wrong myth scores zero',
  cue: 'Essay (prescribed text)',
  question:
    'A 12-mark question asks you to discuss the nature of the gods using evidence from a specific myth on the course. A candidate writes a superb, well-developed, well-evidenced discussion — but about a different myth from the one the question specifies. The scheme’s bottom line is stark: “0: wrong myth.” What does this answer score?',
  questionNote:
    'Scenario authored for this exercise. The banded scheme runs from basic up to full, but carries an explicit “0: wrong myth” — answering on a myth other than the one set voids the answer regardless of its quality.',
  scale: {
    name: 'Right myth · /12',
    levels: [
      { id: 'cl14-wrong', label: 'Wrong myth', annotation: '0', marks: 0 },
      { id: 'cl14-basic', label: 'Right myth, one accurate point', annotation: '3', marks: 3 },
      { id: 'cl14-partial', label: 'Right myth, good development', annotation: '9', marks: 9 },
      { id: 'cl14-full', label: 'Right myth, full', annotation: '12', marks: 12 },
    ],
    notes: [
      'Bands run from basic (one accurate point) to full (very good reasons, high development).',
      '“0: wrong myth.”',
      'A superb discussion of the wrong myth scores nothing — the set text is non-negotiable.',
    ],
    cite: MS24('p.8 (Q7(c))'),
  },
  scripts: [
    {
      id: 'cl14-a',
      label: 'The essay',
      persona: 'Brilliant — on the wrong myth',
      work: [
        'A detailed, well-developed, well-evidenced discussion of the gods.',
        'But it draws on a different myth from the one the question names.',
      ],
      keyLevelId: 'cl14-wrong',
      keyNote:
        'Zero. However good the discussion, “0: wrong myth” overrides everything — the marks live only in the myth the question set. Before you write a line, check you’re answering on the exact prescribed text named. A brilliant answer to the question you wish had been asked scores nothing.',
      embodies: {
        behaviour: 'Writes a strong answer on a myth other than the one specified — triggering the “0: wrong myth” rule.',
        cite: MS24('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-cl14',
    rule: 'Check you’re answering on the myth the question actually set.',
    detail:
      'The scheme carries an explicit “0: wrong myth”. A superb, well-evidenced discussion of the wrong prescribed text scores nothing — read the question’s named text carefully before you commit.',
    cite: MS24('p.8'),
  },
};

// ─────────────── CL15 · OL — reference the text, quotation optional ───────────────

const CL15: ScaleSession = {
  mode: 'scale',
  id: 'cl-reference-not-quote',
  subject: 'classical-studies',
  level: 'ordinary',
  title: 'You don’t have to quote it word for word',
  cue: 'Stimulus (OL)',
  question:
    'An OL question asks you to discuss a poem you studied, for 10 marks. A candidate references specific scenes and messages from the poem accurately and in detail — but doesn’t reproduce any exact quotations, worried that will cost the top marks. The scheme says: “direct referencing needed for top marks but quotation not essential.” Where does the answer land?',
  questionNote:
    'Scenario authored for this exercise. The top band needs direct, specific reference to the text — but the scheme expressly states exact quotation is not essential; a precisely-referenced answer without word-for-word quotes can still reach full.',
  scale: {
    name: 'Reference the text · /10',
    levels: [
      { id: 'cl15-general', label: 'General points, no specific reference', annotation: 'basic', marks: 4 },
      { id: 'cl15-referenced', label: 'Direct reference (quotation optional)', annotation: 'full', marks: 10 },
    ],
    notes: [
      '“direct referencing needed for top marks but quotation not essential.”',
      'Top band: specific points and examples drawn directly from the text.',
      'Reference the scene or message precisely — you needn’t reproduce the exact words.',
    ],
    cite: MS24OL('p.8 (Q8(b))'),
  },
  scripts: [
    {
      id: 'cl15-a',
      label: 'The answer',
      persona: 'Specific, but no quotes',
      work: [
        'Accurate, detailed reference to named scenes and messages in the poem.',
        'No word-for-word quotations, out of fear that costs the top marks.',
      ],
      keyLevelId: 'cl15-referenced',
      keyNote:
        'Full marks — nothing was lost by not quoting. The scheme asks for direct referencing, not memorised quotation: naming the scene and its message precisely is what the top band rewards. Don’t burn revision time drilling exact wording; learn the text well enough to point to the right moment specifically.',
    },
  ],
  takeaway: {
    id: 'codex-cl15',
    rule: 'Reference the text precisely; you needn’t quote it word for word.',
    detail:
      'The scheme states “direct referencing needed for top marks but quotation not essential”. Specific, accurate reference to scenes and messages reaches the top band — exact quotation is optional, so learn the text, not a script.',
    cite: MS24OL('p.8'),
  },
};

export const CLASSICAL_CHAIR: ChairSubject = {
  id: 'classical-studies',
  label: 'Classical Studies',
  tagline: 'Develop your units, answer both parts, use your sources, argue not narrate.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [CL1, CL2, CL3, CL4, CL5, CL6, CL7, CL8, CL9, CL10, CL11, CL12, CL13, CL14, CL15],
  sources: [
    { label: 'SEC LC Classical Studies HL marking scheme 2025 (examiner-reports/classical-studies/2025-marking-scheme)' },
    { label: 'SEC LC Classical Studies OL marking scheme 2025 (examiner-reports/classical-studies/2025-ol-marking-scheme)' },
    { label: 'SEC LC Classical Studies HL marking scheme 2024 (examiner-reports/classical-studies/2024-marking-scheme)' },
    { label: 'SEC LC Classical Studies OL marking scheme 2024 (examiner-reports/classical-studies/2024-ol-marking-scheme)' },
  ],
  coverageNote:
    'The unit-of-development and Overall Quality sessions apply at both levels — the HL unit needs full development, while the OL unit softens this to “some development” and marks a developed point at full. The Section A sessions capture the stimulus-question marking grammar: engage both sources on picture questions, back the extract with wider studied evidence, cover both named categories (military and political), let depth replace breadth, and mind the yes/no floor, the Greek/Roman confusion cap, the “0: wrong myth” rule, the own-words copying floor, and the reference-not-quotation rule. RSR sessions cover using sources rather than just listing them, and the OL session captures OL’s inverted mark split — Section A 300 / essays 100. Verified against the 2025 and 2024 HL and OL schemes.',
};
