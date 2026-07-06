/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Politics & Society (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (quality descriptor bands where insight beats relevance,
 * the summary-isn't-discussion essay trap, and the split documents-question
 * rubric — plus the both-documents band cap, the floating 3M-slot note, the
 * length/brevity instruction and the discrete project-reference scale) is the
 * real SEC system, cited to:
 *  - SEC LC Politics & Society HL marking scheme 2025 —
 *    examiner-reports/politics-society/2025-marking-scheme.*
 *  - SEC LC Politics & Society OL marking scheme 2025 —
 *    examiner-reports/politics-society/2025-ol-marking-scheme.*
 *  - SEC LC Politics & Society HL marking scheme 2024 —
 *    examiner-reports/politics-society/2024-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Politics & Society HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Politics & Society OL marking scheme 2025, ${p}` });
const MS24 = (p: string) => ({ label: `SEC Politics & Society HL marking scheme 2024, ${p}` });

// ─────────────── PS1 · Insight beats relevance ───────────────

const PS1: ScaleSession = {
  mode: 'scale',
  id: 'ps-insight',
  subject: 'politics-society',
  level: 'higher',
  title: 'Relevant isn’t enough',
  cue: 'Data question',
  question: 'A 20-mark data-question response is accurate and clearly relevant to the question — but it stays descriptive, offering no independent interpretation. The band descriptors reserve the top band (16–20) for answers that are “independent and insightful”, with “relevant but lacking insight” sitting a band lower. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Politics & Society scores by quality descriptor bands, not points-per-fact; on 20-mark data items the top band requires independent insight, and merely relevant answers sit in the Good band.',
  scale: {
    name: 'Data item · descriptor bands /20',
    levels: [
      { id: 'fair', label: 'Fair (0–10)', annotation: 'F', marks: 8 },
      { id: 'good', label: 'Good — relevant, no insight (11–15)', annotation: 'G', marks: 14 },
      { id: 'vgood', label: 'Very good — insightful (16–20)', annotation: 'VG', marks: 18 },
    ],
    notes: [
      'Marked by descriptor band, not a point tariff.',
      'Good band (11–15): “relevant but lacking insight”.',
      'Very good band (16–20): “independent and insightful”.',
      'Accurate, relevant description caps in the Good band — insight is what lifts it.',
    ],
    cite: MS('p.11 (20-mark data-item bands)'),
  },
  scripts: [
    {
      id: 'ps1-a',
      label: 'The answer',
      persona: 'Accurate, relevant, descriptive',
      work: [
        'Reads the data correctly and stays on the question.',
        'But offers no interpretation of its own — just describes what’s there.',
      ],
      keyLevelId: 'good',
      keyNote:
        'The Good band — “relevant but lacking insight” is exactly this answer. Relevance and accuracy get you to the middle; the top band needs a line of your own interpretation (what the data implies, why it matters, what it doesn’t show). Add the “so what”, and the same content jumps a band.',
      embodies: {
        behaviour: 'Gives a relevant but non-insightful answer — capped in the Good band by the descriptors.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps1',
    rule: 'Relevance reaches the middle; insight reaches the top.',
    detail:
      'Politics & Society bands reserve the top marks for “independent and insightful”, not merely “relevant”. Always add your own interpretation — what the evidence implies and why — to climb out of the Good band.',
    cite: MS('p.11'),
  },
};

// ─────────────── PS2 · Summary isn't discussion ───────────────

const PS2: ScaleSession = {
  mode: 'scale',
  id: 'ps-summary',
  subject: 'politics-society',
  level: 'higher',
  title: 'Summary isn’t argument',
  cue: 'Discursive essay',
  question: 'A 100-mark essay is knowledgeable and well-written, but it summarises each viewpoint in turn and never builds an argument or compares them. The holistic grade descriptors flag that “summary and repetition often take the place of discussion” at the lower bands. Where does it sit?',
  questionNote:
    'Scenario authored for this exercise. Section C essays are marked on analytic criteria then reconciled to H1–H8 holistic bands; a descriptive, summarising essay is structurally held in the lower bands.',
  scale: {
    name: 'Essay · holistic band',
    levels: [
      { id: 'h6', label: 'Lower (summary in place of discussion)', annotation: 'H6', marks: 55 },
      { id: 'h4', label: 'Mid (points stand alone)', annotation: 'H4', marks: 68 },
      { id: 'h2', label: 'Upper (comparative, integrated)', annotation: 'H2', marks: 85 },
    ],
    notes: [
      'Essays reconcile to H1–H8 holistic bands after analytic marking.',
      'Lower band descriptor: “summary and repetition often take the place of discussion”.',
      'Higher bands need comparison, integration and independent conclusions.',
      'A well-written but summarising essay can’t reach the top bands.',
    ],
    cite: MS('p.14–15 (analytic criteria + holistic band descriptors)'),
  },
  scripts: [
    {
      id: 'ps2-a',
      label: 'The essay',
      persona: 'Summarises each side',
      work: [
        'Knowledgeable and fluent.',
        'Sets out each viewpoint in turn — but never argues, compares or concludes.',
      ],
      keyLevelId: 'h6',
      keyNote:
        'It lands in the lower band, where “summary takes the place of discussion” — the exact profile of this essay. Knowledge and fluency aren’t the ceiling; the ceiling is set by whether you argue. Compare the viewpoints, weigh them, and reach your own conclusion to move up the bands.',
      embodies: {
        behaviour: 'Summarises viewpoints instead of arguing between them — the lower-band essay trap.',
        cite: MS('p.15'),
      },
    },
    {
      id: 'ps2-border',
      label: 'The essay (near miss)',
      persona: 'Starts to compare, then lists',
      work: [
        'Opens by setting two viewpoints against each other and genuinely weighs them for a paragraph.',
        'But after that first comparison it reverts to taking each remaining point in turn — the argument isn’t sustained and there’s no integrated conclusion.',
      ],
      keyLevelId: 'h4',
      keyNote:
        'This is the borderline a hurried marker misplaces. It does more than summarise — there’s a real comparison early on — so it clears the lower band; but the argument isn’t carried through, the later points stand alone, and there’s no independent conclusion. That’s the mid band, not the integrated, comparative top band. One sustained line of argument to a conclusion of your own is the difference between mid and upper.',
    },
  ],
  takeaway: {
    id: 'codex-ps2',
    rule: 'Argue, don’t summarise.',
    detail:
      'Politics & Society essays cap in the lower bands when summary replaces discussion. Knowledge alone won’t lift the grade — compare the perspectives, weigh the evidence, and reach an independent conclusion.',
    cite: MS('p.15'),
  },
};

// ─────────────── PS3 · Conclude AND cite ───────────────

const PS3: GridSession = {
  mode: 'grid',
  id: 'ps-documents',
  subject: 'politics-society',
  level: 'higher',
  title: 'Conclude and cite',
  cue: 'Documents question',
  question: 'The 50-mark capstone of the documents question is marked on a split rubric: Conclusions /30 and Use of documents /20. A candidate writes a strong, well-argued conclusion — but never refers to the provided documents at all.',
  questionNote:
    'Scenario authored for this exercise. The documents-question capstone awards Conclusions and Use of documents on two separate scales that must both be satisfied.',
  grid: {
    perPoint: [
      { id: 'conclusions', label: 'Conclusions (argued)', marks: 30 },
      { id: 'documents', label: 'Use of the documents', marks: 20 },
    ],
    shorthand: 'Conclusions 30 + Use of documents 20',
    ruleNote:
      'The two scales are marked separately, so each must be earned in its own right. A brilliant argument that ignores the documents forfeits up to 20; heavy quoting with weak conclusions forfeits up to 30. You need both.',
    cite: MS('p.12 (split Conclusions/Use-of-documents rubric)'),
  },
  scripts: [
    {
      id: 'ps3-a',
      label: 'The answer',
      persona: 'Great argument, ignores the documents',
      attempts: [
        {
          id: 'ps3-a-1',
          text: 'A strong, well-structured conclusion drawn entirely from the candidate’s own knowledge — the provided documents are never referenced.',
          key: { conclusions: 30, documents: 0 },
          keyNote: 'The conclusions score well, but “Use of documents” is a separate 20-mark scale and nothing here engages the sources — so 20 marks are simply unearned. 30 of 50. Weave the documents in (quote, interpret, agree or challenge them) to claim the other scale.',
        },
      ],
      embodies: {
        behaviour: 'Argues well but ignores the documents — forfeiting the separate Use-of-documents scale.',
        cite: MS('p.12'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps3',
    rule: 'The documents question needs both halves.',
    detail:
      'The capstone marks Conclusions and Use of documents on separate scales — a great argument that ignores the sources loses 20, and heavy quoting with thin conclusions loses 30. Build your argument and anchor it in the documents.',
    cite: MS('p.12'),
  },
};

// ─────────────── PS4 · OL — knowledge and structure carry the essay ───────────────

const PS4: ScaleSession = {
  mode: 'scale',
  id: 'ps-ol-knowledge',
  subject: 'politics-society',
  level: 'ordinary',
  title: 'At OL, knowledge carries the essay',
  cue: 'Essay (OL)',
  question: 'An Ordinary Level essay (50 marks) is scored on six criteria: Introduction 10, Knowledge 10, Evidence 10, Analysis 5, Evaluation 5, Cohesion 10. A candidate writes a well-introduced, knowledgeable, well-structured essay with solid evidence — but light on deep analysis and evaluation. How does it fare?',
  questionNote:
    'Scenario authored for this exercise. At OL the higher-order criteria (Analysis, Evaluation) are the lightest at 5 marks each; Introduction, Knowledge, Evidence and Cohesion carry 10 each — the opposite emphasis to Higher Level, where insight and evaluation dominate.',
  scale: {
    name: 'OL essay · /50',
    levels: [
      { id: 'm20', label: '~20 (thin all round)', annotation: '20', marks: 20 },
      { id: 'm40', label: '~40 (strong K/E/structure, light analysis)', annotation: '40', marks: 40 },
      { id: 'm48', label: '~48 (strong throughout)', annotation: '48', marks: 48 },
    ],
    notes: [
      'OL essay criteria: Introduction 10, Knowledge 10, Evidence 10, Analysis 5, Evaluation 5, Cohesion 10.',
      'Analysis and Evaluation are the LIGHTEST criteria at OL (5 each) — the reverse of HL.',
      'A knowledgeable, well-structured, well-evidenced essay banks 40 of the 50 marks.',
    ],
    cite: MSOL('p.15 (OL essay criteria weightings)'),
  },
  scripts: [
    {
      id: 'ps4-a',
      label: 'The essay',
      persona: 'Knowledgeable and structured',
      work: [
        'Clear introduction, strong knowledge, solid evidence, well organised.',
        'But light on deep analysis and evaluation.',
      ],
      keyLevelId: 'm40',
      keyNote:
        'It scores well — around 40 of 50 — because at OL, Introduction, Knowledge, Evidence and Cohesion carry 10 marks each and Analysis/Evaluation only 5 each. This is the opposite of Higher Level, where insight and evaluation win the marks. At OL, a knowledgeable, well-structured, well-evidenced essay is most of the way there; the analysis is the smaller top-up.',
      embodies: {
        behaviour: 'Delivers strong knowledge and structure with light analysis — which at OL banks the majority.',
        cite: MSOL('p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps4',
    rule: 'At OL, knowledge and structure carry the essay.',
    detail:
      'Ordinary Level Politics & Society weights Introduction, Knowledge, Evidence and Cohesion at 10 each and Analysis/Evaluation at only 5 — the reverse of Higher. A well-introduced, knowledgeable, well-organised, evidenced essay banks the majority; analysis is the top-up.',
    cite: MSOL('p.15'),
  },
};

// ─────────────── PS5 · Name the name — it's a separate mark ───────────────

const PS5: GridSession = {
  mode: 'grid',
  id: 'ps-name-explain',
  subject: 'politics-society',
  level: 'higher',
  title: 'Name the name',
  cue: 'Short data question',
  question:
    'A Section A short question is worth 5 marks: “Name the Key Thinker associated with The Capabilities Approach. Briefly explain this theory.” The scheme splits it 2 marks + 3 marks — the naming is a specific-fact tariff (Martha Nussbaum, 2M) and the explanation is banded (up to 3M). One answer explains the theory well but never names the thinker; another names the thinker but never explains it.',
  questionNote:
    'Scenario authored for this exercise. Section A two-part “name/identify + explain” items mark the named fact and the explanation on separate tariffs — modelled on the 2025 HL Q1(o) template.',
  grid: {
    perPoint: [
      { id: 'ps5-name', label: 'Name the thinker (specific fact)', marks: 2 },
      { id: 'ps5-explain', label: 'Explain the theory (banded)', marks: 3 },
    ],
    shorthand: 'Name 2M + Explain 3M',
    ruleNote:
      'The two parts are marked on separate scales. The naming mark is a specific fact — you earn it by writing “Martha Nussbaum”, not by describing the idea. Explaining the theory beautifully banks nothing from the naming tariff; naming without explaining caps at 2. Both parts, or you leave marks on the table.',
    cite: MS('p.9 (Q1(o) — “Name: Martha Nussbaum 2M” + banded explanation 3M)'),
  },
  scripts: [
    {
      id: 'ps5-a',
      label: 'The answers',
      persona: 'Half the two-part question, each time',
      attempts: [
        {
          id: 'ps5-a-1',
          text: 'Sets out the Capabilities Approach clearly — people need real freedoms and capabilities (life, health, bodily integrity) to flourish — but never says who devised it.',
          key: { 'ps5-name': 0, 'ps5-explain': 3 },
          keyNote:
            'The explanation is very good and banks the full 3M banded tariff. But the paper asked you to name the Key Thinker, and that is a separate 2-mark fact — Martha Nussbaum. Describing the theory does not earn the naming mark. No name, no 2 marks: 3 of 5.',
        },
        {
          id: 'ps5-a-2',
          text: 'Writes “Martha Nussbaum” and stops — no account of what the theory actually claims.',
          key: { 'ps5-name': 2, 'ps5-explain': 0 },
          keyNote:
            'The name banks the 2M fact cleanly, but with no explanation the 3M banded scale is empty. 2 of 5. The name and the explanation sit on separate scales — you have to feed both.',
        },
      ],
      embodies: {
        behaviour: 'Answers one tariff of a two-part “name + explain” item and forfeits the other.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps5',
    rule: 'Name the name — it’s a separate mark.',
    detail:
      'When a Politics & Society question says “name the key thinker / social scientist”, the name is a specific fact worth its own marks — describing the theory won’t earn it, and naming without explaining leaves the banded marks empty. Answer both halves.',
    cite: MS('p.9'),
  },
};

// ─────────────── PS6 · Answer the number the question asks ───────────────

const PS6: GridSession = {
  mode: 'grid',
  id: 'ps-two-items',
  subject: 'politics-society',
  level: 'higher',
  title: 'Two means two',
  cue: 'Short data question',
  question:
    'A 5-mark Section A question reads “Describe two functions of the President of Ireland (3M + 2M).” The two required functions are marked on an asymmetric split — the first worth 3M, the second worth 2M — and each is credited in its own right. A candidate describes one function superbly and never gives a second.',
  questionNote:
    'Scenario authored for this exercise. Section A “describe two …” items split the marks across the required number of points (here 3M + 2M) and mark each separately — modelled on the 2025 HL Q1(i) template.',
  grid: {
    perPoint: [
      { id: 'ps6-first', label: 'First function (3M slot)', marks: 3 },
      { id: 'ps6-second', label: 'Second function (2M slot)', marks: 2 },
    ],
    shorthand: '2 functions · 3M + 2M',
    ruleNote:
      'The scheme splits the marks 3 + 2 across the two required items and marks each in its own slot. One brilliant function can’t spill into the second slot — an unanswered second function is a straight 2-mark loss. The instruction “two” is a mark-bearing quantity, not a suggestion.',
    cite: MS('p.7 (Q1(i) — “Describe two functions … (3M+2M)”, each banded separately)'),
  },
  scripts: [
    {
      id: 'ps6-a',
      label: 'The answers',
      persona: 'Counts to one, then to two',
      attempts: [
        {
          id: 'ps6-a-1',
          text: 'Describes one function — Supreme Commander of the Defence Forces — in rich, well-explained detail, and stops there.',
          key: { 'ps6-first': 3, 'ps6-second': 0 },
          keyNote:
            'The single function is very good and banks the 3M first slot. But the second-function slot (2M) is marked separately and it’s empty — you can’t earn it by over-writing the first. 3 of 5. “Two” means two.',
        },
        {
          id: 'ps6-a-2',
          text: 'Gives two solid functions — Supreme Commander of the Defence Forces, and signing legislation into law or referring bills to the Supreme Court.',
          key: { 'ps6-first': 3, 'ps6-second': 2 },
          keyNote:
            'Both slots filled: 3M + 2M = full marks. Note the second only needs to be solid, not spectacular — its ceiling is 2M — so once the first is strong, the fastest marks are in simply adding the second point.',
        },
      ],
      embodies: {
        behaviour: 'Gives one item when two are asked — forfeiting the separately-marked second slot.',
        cite: MS('p.7'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps6',
    rule: 'Answer the number the question asks.',
    detail:
      'When a Politics & Society question says “two” and splits the marks (e.g. 3M + 2M), each item is marked in its own slot. A superb single answer caps at the first slot; the missing item is a clean loss. Give exactly as many points as the question names.',
    cite: MS('p.7'),
  },
};

// ─────────────── PS7 · A contradiction can void the marks ───────────────

const PS7: ScaleSession = {
  mode: 'scale',
  id: 'ps-contradiction',
  subject: 'politics-society',
  level: 'higher',
  title: 'Right, then wrong',
  cue: 'Short data question',
  question:
    'A 5-mark Section A explanation opens with an accurate point that would sit in the top band — but midway it misuses the key term and states the opposite of its own definition. The scheme’s general instruction is explicit: “Words, expressions or phrases must be correctly used in context and not contradicted … the marks may not be awarded.” Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Section A 5-mark items band Very good 4–5 / Good 2–3 / Fair 0–1; the scheme’s general marking instructions withhold marks where a term is misused or the answer contradicts itself.',
  scale: {
    name: 'Section A item · /5 (correct-use rule)',
    levels: [
      { id: 'ps7-forfeit', label: 'Contradicted — not credited', annotation: 'X', marks: 0 },
      { id: 'ps7-fair', label: 'Fair (0–1)', annotation: 'F', marks: 1 },
      { id: 'ps7-good', label: 'Good (2–3)', annotation: 'G', marks: 3 },
      { id: 'ps7-vgood', label: 'Very good (4–5)', annotation: 'VG', marks: 5 },
    ],
    notes: [
      'Section A 5-mark items band Very good 4–5, Good 2–3, Fair 0–1.',
      'General rule: terms must be “correctly used in context and not contradicted”, or the marks may not be awarded.',
      'A correct point later contradicted can’t be credited — the contradiction voids the very claim the marks rested on.',
    ],
    cite: MS('p.3 (correct-use / no-contradiction rule) + p.4 (5-mark bands)'),
  },
  scripts: [
    {
      id: 'ps7-a',
      label: 'The answer',
      persona: 'Right, then contradicts itself',
      work: [
        'Opens with an accurate explanation of the key term — top-band on its own.',
        'Then misuses the same term and asserts the opposite of the definition it just gave.',
      ],
      keyLevelId: 'ps7-forfeit',
      keyNote:
        'Read in isolation the opening is very-good. But the scheme is explicit: where a term is misused or the answer contradicts itself, “the marks may not be awarded”. The contradiction cancels the very claim the marks rested on, so the credit falls away — accuracy you then undo isn’t accuracy. One contradicted key term can cost the whole item; say it once, correctly, and leave it consistent.',
      embodies: {
        behaviour: 'Makes a correct point then contradicts it — triggering the correct-use rule that withholds the marks.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'ps7-border',
      label: 'The answer (near miss)',
      persona: 'Correct and consistent — but thin',
      work: [
        'Uses the key term correctly and never contradicts itself.',
        'But the explanation stops at a bare, accurate definition — no development, no worked context.',
      ],
      keyLevelId: 'ps7-good',
      keyNote:
        'The correct-use rule is satisfied — nothing is misused or contradicted, so none of the credit falls away; that clears the forfeit and lifts it above Fair. But a correct term left undeveloped is a Good-band answer, not Very good: the top band wants the term used in context and explained, not merely stated. Because it’s accurate as far as it goes, a generous marker drifts up and a harsh one down — the scheme pins it in the middle: right, but thin. Develop the point in context and the same term reaches the top band.',
    },
  ],
  takeaway: {
    id: 'codex-ps7',
    rule: 'A contradiction can void the marks it rested on.',
    detail:
      'Politics & Society requires terms to be used correctly and consistently; where an answer misuses a term or contradicts itself, the scheme says the marks may not be awarded. Make the point once, correctly — don’t undo a good point two lines later.',
    cite: MS('p.3'),
  },
};

// ─────────────── PS8 · Both documents, or capped ───────────────

const PS8: ScaleSession = {
  mode: 'scale',
  id: 'ps-both-documents',
  subject: 'politics-society',
  level: 'higher',
  title: 'Both documents, or capped',
  cue: 'Documents question',
  question:
    'A 20-mark Section B question asks you to comment on an issue “according to both documents”. A candidate writes an insightful, well-argued comment — but draws it entirely from Document A and never engages Document B. The top band is reserved for comment “using both documents”, while “reference to one document only” is written straight into the Good band. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Section B 20-mark synthesis items band Very good 16–20 (independent, insightful, using both documents) / Good 11–15 (relevant, one document only) / Fair 6–10 / Weak 0–5 — modelled on the 2024 HL Q2(c) template.',
  scale: {
    name: 'Both-documents item · /20',
    levels: [
      { id: 'ps8-weak', label: 'Weak — contradictory or confused (0–5)', annotation: 'W', marks: 4 },
      { id: 'ps8-fair', label: 'Fair — limited, lacking clarity (6–10)', annotation: 'F', marks: 8 },
      { id: 'ps8-good', label: 'Good — insightful but one document only (11–15)', annotation: 'G', marks: 13 },
      { id: 'ps8-vgood', label: 'Very good — insightful, both documents (16–20)', annotation: 'VG', marks: 18 },
    ],
    notes: [
      'Top band (16–20): “independent, insightful comment using both documents”.',
      'Good band (11–15): “relevant comment but lacking insight, reference to one document only”.',
      'Using only one document is written into the Good band — insight alone can’t lift a one-document answer past it.',
    ],
    cite: MS24('p.9 (Q2(c) — “reference to one document only” pins the Good band)'),
  },
  scripts: [
    {
      id: 'ps8-a',
      label: 'The answer',
      persona: 'Insightful, but one document',
      work: [
        'Reads Document A closely and builds a genuinely insightful comment on it.',
        'Never turns to Document B — the second source is left untouched.',
      ],
      keyLevelId: 'ps8-good',
      keyNote:
        'The comment is insightful, which normally reaches for the top band — but the descriptor pins a one-document answer in the Good band no matter how sharp it is (“reference to one document only” is the Good-band wording). The scale doesn’t just reward insight; it requires you to work across both documents. Bring Document B in, even briefly, and the same insight can climb to Very good.',
      embodies: {
        behaviour: 'Comments insightfully on a single document when the band demands both — capped at Good.',
        cite: MS24('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps8',
    rule: 'Both documents means both, or you cap at Good.',
    detail:
      'On Section B synthesis questions the top band requires comment “using both documents”; the scheme writes “reference to one document only” into the Good band. However insightful, a one-document answer is held below the top — always engage the second source.',
    cite: MS24('p.9'),
  },
};

// ─────────────── PS9 · Presentation means the packaging ───────────────

const PS9: ScaleSession = {
  mode: 'scale',
  id: 'ps-data-presentation',
  subject: 'politics-society',
  level: 'ordinary',
  title: 'Presentation means the packaging',
  cue: 'Data-presentation question',
  question:
    'A 5-mark OL question asks you to “comment on the presentation of data in Document A”. The scheme credits comment on how the data is displayed — “effective visuals and use of colour”, “simple box with figures”, “easy to read / easily understood”. A candidate instead re-states what the figures say (the numbers and the trend) and never mentions how they are shown. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. OL Section B “presentation of data” items band Very good 4–5 / Good 2–3 / Fair 0–1 and reward comment on the visual format, not a summary of the content — modelled on the 2025 OL Q3(a) template.',
  scale: {
    name: 'Presentation item · /5',
    levels: [
      { id: 'ps9-fair', label: 'Fair — off-question / content summary (0–1)', annotation: 'F', marks: 1 },
      { id: 'ps9-good', label: 'Good — some comment on the display (2–3)', annotation: 'G', marks: 3 },
      { id: 'ps9-vgood', label: 'Very good — clear comment on the display (4–5)', annotation: 'VG', marks: 5 },
    ],
    notes: [
      'The question is about how the data is presented, not what the data says.',
      'Model references: “effective visuals and use of colour”, “simple box with figures”, “easy to read”.',
      'Summarising the figures instead of judging their display misses the question.',
    ],
    cite: MSOL('p.12 (Q3(a) — presentation-of-data reference points)'),
  },
  scripts: [
    {
      id: 'ps9-a',
      label: 'The answer',
      persona: 'Answers the wrong question',
      work: [
        'Accurately restates the figures and the trend they show.',
        'Says nothing about the layout, colour, chart type or readability of the display.',
      ],
      keyLevelId: 'ps9-fair',
      keyNote:
        'The figures are read correctly, but “presentation” asks about the packaging — the visuals, colour, layout and readability — not the content. A content summary simply doesn’t answer a presentation question, so it sits in Fair. Comment on whether the display is clear, well-labelled, easy to read or effectively colour-coded and the same 5 marks open up.',
      embodies: {
        behaviour: 'Summarises the data’s content when asked to judge its presentation — off-question.',
        cite: MSOL('p.12'),
      },
    },
    {
      id: 'ps9-border',
      label: 'The answer (near miss)',
      persona: 'Half display, half content',
      work: [
        'Notes that the document uses a simple box of figures and is easy to read.',
        'But then spends the rest of the answer restating the figures and the trend, adding nothing further about the design.',
      ],
      keyLevelId: 'ps9-good',
      keyNote:
        'One real observation about the display — “a simple box, easy to read” is exactly the kind of comment the scheme credits — lifts this clear of Fair. But it’s a single, undeveloped point wrapped in a content summary, so it can’t reach the clear, sustained comment the top band wants. It lands in Good: on-question, but only just. Build the presentation comment out — colour, labelling, chart type, what the format does for the reader — instead of drifting back to the numbers.',
    },
  ],
  takeaway: {
    id: 'codex-ps9',
    rule: 'A “presentation” question is about the packaging, not the payload.',
    detail:
      '“Comment on the presentation of data” credits how the data is displayed — visuals, colour, layout, readability — not a restatement of the figures. Describe the design choices and their effect on the reader, not the numbers themselves.',
    cite: MSOL('p.12'),
  },
};

// ─────────────── PS10 · Your best point isn't penalised for coming second ───────────────

const PS10: GridSession = {
  mode: 'grid',
  id: 'ps-floating-slot',
  subject: 'politics-society',
  level: 'higher',
  title: 'Best point, either order',
  cue: 'Short data question',
  question:
    'A 5-mark Section A item splits 3M + 2M across two required points. Students worry: what if my stronger point is the second one I write? The scheme’s note is explicit — “If the first point is awarded 2M or less, mark the second point out of 3M.” The 3-mark ceiling follows your better point, whichever order you wrote them in.',
  questionNote:
    'Scenario authored for this exercise. Several 2024 HL Section A two-point items carry a note reallocating the 3M ceiling to the stronger point regardless of order — modelled on the Q1(a) / Q1(i) template.',
  grid: {
    perPoint: [
      { id: 'ps10-strong', label: 'Stronger point → 3M slot', marks: 3 },
      { id: 'ps10-other', label: 'Other point → 2M slot', marks: 2 },
    ],
    shorthand: '2 points · 3M + 2M (best point takes the 3M)',
    ruleNote:
      'The examiner doesn’t lock the 3M to whatever you happened to write first. If the first point scores 2M or less, the scheme moves the 3M ceiling onto your stronger second point. So order never costs you — but you still need two points to fill both slots.',
    cite: MS24('p.4 (Q1(a) note — “If the first point is awarded 2M or less, mark the second point out of 3M”)'),
  },
  scripts: [
    {
      id: 'ps10-a',
      label: 'The answers',
      persona: 'Writes the strong point second',
      attempts: [
        {
          id: 'ps10-a-1',
          text: 'Opens with a modest, partly-developed point, then follows it with a second point that is clearly the stronger, fuller answer.',
          key: { 'ps10-strong': 3, 'ps10-other': 2 },
          keyNote:
            'Because the first point is weak (2M or less), the scheme moves the 3M ceiling onto the stronger second point — so the good point still earns 3M and the modest one fills the 2M slot. Full 5. You are never punished for saving your best point for second.',
        },
        {
          id: 'ps10-a-2',
          text: 'Gives one strong, well-developed point and stops — no second point at all.',
          key: { 'ps10-strong': 3, 'ps10-other': 0 },
          keyNote:
            'The strong point banks the 3M slot, but the reallocation note can only move the ceiling between points you actually wrote — it can’t conjure a second point. With the 2M slot empty, this is 3 of 5. Order is free; the second point is not.',
        },
      ],
      embodies: {
        behaviour: 'Places the stronger point second (rewarded by the reallocation note) and, separately, omits the second point.',
        cite: MS24('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps10',
    rule: 'Your best point isn’t penalised for coming second.',
    detail:
      'On two-point Section A items the 3M ceiling reallocates to your stronger point regardless of the order you wrote them (“if the first point is awarded 2M or less, mark the second out of 3M”). Don’t agonise over sequence — but you still need both points to fill both slots.',
    cite: MS24('p.4'),
  },
};

// ─────────────── PS11 · Length isn't a mark ───────────────

const PS11: ScaleSession = {
  mode: 'scale',
  id: 'ps-length',
  subject: 'politics-society',
  level: 'higher',
  title: 'Length isn’t a mark',
  cue: 'Discursive essay',
  question:
    'A 100-mark essay is long — it fills every page — but much of that length is padding and repetition circling the same few points. A shorter, sharper essay would make those points once and stop. The examiner’s explicit instruction on the grade-band page: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.” Where does the padded essay land?',
  questionNote:
    'Scenario authored for this exercise. The essay grade-band page carries an explicit instruction that length is not itself credited and concise answers are not penalised.',
  scale: {
    name: 'Essay · quality, not length',
    levels: [
      { id: 'ps11-weak', label: 'Weak — few real points (0–39)', annotation: 'H7–8', marks: 30 },
      { id: 'ps11-mid', label: 'Mid — the points it actually makes (50–59)', annotation: 'H5', marks: 55 },
      { id: 'ps11-top', label: 'Upper — range and depth (80–89)', annotation: 'H2', marks: 85 },
    ],
    notes: [
      'Explicit instruction: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.”',
      'Marks track the quality and range of distinct points, not word count.',
      'A concise essay making the same points well scores the same as the padded version.',
    ],
    cite: MS('p.15 (essay grade bands — brevity/length instruction)'),
  },
  scripts: [
    {
      id: 'ps11-a',
      label: 'The essay',
      persona: 'Long, but padded',
      work: [
        'Fills the whole answer book and reads as a big, effortful essay.',
        'But the distinct points are middling and few — the length is repetition and restatement.',
      ],
      keyLevelId: 'ps11-mid',
      keyNote:
        'The examiner is told not to reward unwarranted length, so the padding earns nothing — the essay lands on the quality and range of the points it actually makes, which is mid-band. The same points made in half the words would score the same. And since brevity isn’t penalised, the padding wasn’t even insurance: better to make more distinct, well-evidenced points than to restate a few at length.',
      embodies: {
        behaviour: 'Pads a thin argument to great length, expecting length to lift the grade.',
        cite: MS('p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps11',
    rule: 'Length isn’t a mark; distinct points are.',
    detail:
      'The essay bands are applied with an explicit instruction not to reward unwarranted length nor penalise skilful brevity. Padding and repetition earn nothing — spend the words on more distinct, well-evidenced points, not on restating the same ones.',
    cite: MS('p.15'),
  },
};

// ─────────────── PS12 · The intro is worth ten ───────────────

const PS12: ScaleSession = {
  mode: 'scale',
  id: 'ps-introduction',
  subject: 'politics-society',
  level: 'higher',
  title: 'The intro is worth ten',
  cue: 'Discursive essay',
  question:
    'The essay Introduction is a marked criterion worth 10. The top bands need the issue “directly addressed and contextualised”; “issue is vaguely addressed with no contextualisation” is written into the Fair band (3–4). A candidate opens by restating the question in their own words and immediately launches into arguments — no context, no framing of why the issue matters. How does the introduction score?',
  questionNote:
    'Scenario authored for this exercise. The essay Introduction criterion is marked /10 across Excellent 9–10 / Very good 7–8 / Good 5–6 / Fair 3–4 / Weak 0–2, keyed on how fully the issue is addressed and contextualised.',
  scale: {
    name: 'Introduction criterion · /10',
    levels: [
      { id: 'ps12-weak', label: 'Weak — vague or misunderstood (0–2)', annotation: 'W', marks: 1 },
      { id: 'ps12-fair', label: 'Fair — addressed, no contextualisation (3–4)', annotation: 'F', marks: 3 },
      { id: 'ps12-good', label: 'Good — reasonably addressed, limited context (5–6)', annotation: 'G', marks: 5 },
      { id: 'ps12-vgood', label: 'Very good — addresses and contextualises (7–8)', annotation: 'VG', marks: 7 },
      { id: 'ps12-exc', label: 'Excellent — addresses, clarifies, contextualises (9–10)', annotation: 'E', marks: 9 },
    ],
    notes: [
      'Introduction is a standalone 10-mark criterion, not a throwaway opener.',
      'Fair band (3–4): “issue is vaguely addressed with no contextualisation”.',
      'Restating the question isn’t contextualising it — you have to frame the issue and why it matters.',
    ],
    cite: MS('p.14 (Introduction criterion bands)'),
  },
  scripts: [
    {
      id: 'ps12-a',
      label: 'The introduction',
      persona: 'Restates and dives in',
      work: [
        'Rewords the question as an opening sentence.',
        'Goes straight into the first argument — no background, no framing of the issue.',
      ],
      keyLevelId: 'ps12-fair',
      keyNote:
        'Rewording the question addresses the issue but doesn’t contextualise it, which is the exact Fair-band descriptor (“vaguely addressed with no contextualisation”). A whole 10-mark criterion is sitting at 3–4 for want of two or three sentences of framing — what the issue is, why it’s contested, what’s at stake. Contextualise before you argue and this criterion nearly doubles.',
      embodies: {
        behaviour: 'Opens by restating the question with no contextualisation — the Fair-band introduction.',
        cite: MS('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps12',
    rule: 'The introduction is a 10-mark criterion — contextualise, don’t just restate.',
    detail:
      'The essay Introduction is marked /10 on how well you address and contextualise the issue; restating the question with no context sits in the Fair band (3–4). Frame the issue — what it is, why it’s contested, what’s at stake — before arguing.',
    cite: MS('p.14'),
  },
};

// ─────────────── PS13 · References: nothing, half, or full ───────────────

const PS13: ScaleSession = {
  mode: 'scale',
  id: 'ps-references',
  subject: 'politics-society',
  level: 'higher',
  title: 'Nothing, half, or full',
  cue: 'Citizenship project',
  question:
    'In the Citizenship Project report, References and Bibliography is scored on a blunt three-step scale — the scheme literally marks it “(0/2/4)”. There is no 1 and no 3. A report with a partial, sloppy reference list doesn’t get “most of the 4”; it gets 2 or 0, and the examiner is directed to “check the back of the booklet”. What does a half-done reference list score?',
  questionNote:
    'Scenario authored for this exercise. The project’s References and Bibliography component is marked on a discrete 0/2/4 scale (4 marks), checked against the references at the back of the booklet.',
  scale: {
    name: 'References & Bibliography · 0/2/4',
    levels: [
      { id: 'ps13-none', label: 'None — no references (0)', annotation: '0', marks: 0 },
      { id: 'ps13-partial', label: 'Partial — present but incomplete (2)', annotation: '2', marks: 2 },
      { id: 'ps13-full', label: 'Full — complete, proper list (4)', annotation: '4', marks: 4 },
    ],
    notes: [
      'Scored “(0/2/4)” — a discrete step scale, with no in-between marks.',
      'Examiner is directed to “check the back of the booklet” for the references.',
      'A partial or sloppy list scores 2, not “nearly 4”; only a complete, proper list earns the full 4.',
    ],
    cite: MS('p.17 (Citizenship Project — “References and Bibliography … (0/2/4) (4 marks)”)'),
  },
  scripts: [
    {
      id: 'ps13-a',
      label: 'The report',
      persona: 'A few references thrown in',
      work: [
        'Lists a couple of websites at the back, without full detail, and misses several sources used in the report.',
        'Assumes a partial effort earns most of the marks.',
      ],
      keyLevelId: 'ps13-partial',
      keyNote:
        'The reference scale has only three stops — 0, 2 or 4. An incomplete list isn’t marked “almost full”; it drops to the 2 step. There is no reward for being close, and no penalty short of a step — so completing the list to a proper standard is a clean, low-effort 2 marks that many candidates leave behind. Full references, every source, checked at the back of the booklet.',
      embodies: {
        behaviour: 'Submits a partial reference list expecting proportional credit on a discrete 0/2/4 scale.',
        cite: MS('p.17'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps13',
    rule: 'Project references are 0, 2 or 4 — there is no “nearly”.',
    detail:
      'References and Bibliography is marked on a discrete 0/2/4 scale and checked at the back of the booklet. A partial list scores 2, not most of the 4 — so finish it properly; the last 2 marks are the easiest on the project.',
    cite: MS('p.17'),
  },
};

// ─────────────── PS14 · The example is its own mark ───────────────

const PS14: GridSession = {
  mode: 'grid',
  id: 'ps-example-mark',
  subject: 'politics-society',
  level: 'ordinary',
  title: 'The example is its own mark',
  cue: 'Short question (OL)',
  question:
    'A 10-mark OL item reads “Describe what a duty bearer is and give an example of one.” The scheme splits it: the description is banded up to 8 marks, and the example is a separate fixed 2-mark tariff. One answer describes a duty bearer perfectly but gives no example; another names an example but supplies no real description.',
  questionNote:
    'Scenario authored for this exercise. Several OL Section A items reserve a fixed 2-mark tariff for a required example alongside a banded description — modelled on the 2025 OL Q1(r) “duty bearer” template.',
  grid: {
    perPoint: [
      { id: 'ps14-describe', label: 'Describe the concept (banded)', marks: 8 },
      { id: 'ps14-example', label: 'Give an example (fixed 2M)', marks: 2 },
    ],
    shorthand: 'Describe /8 + Example 2M',
    ruleNote:
      'The description is banded up to 8; the example is a separate 2-mark fact. A flawless description with no example caps at 8; a named example on its own props up almost nothing. The word “example” in the question is a mark instruction, not a suggestion.',
    cite: MSOL('p.10 (Q1(r) — “Very good description 6–8M … Example: 2 marks”)'),
  },
  scripts: [
    {
      id: 'ps14-a',
      label: 'The answers',
      persona: 'Describes, or exemplifies — not both',
      attempts: [
        {
          id: 'ps14-a-1',
          text: 'Explains fully what a duty bearer is — an individual or body with an obligation to respect, protect and fulfil rights — but never names an actual example.',
          key: { 'ps14-describe': 8, 'ps14-example': 0 },
          keyNote:
            'The description is very good and banks the full banded 8. But the question also asked for an example, and that is a separate fixed 2-mark fact — naming, say, the government or the Gardaí. No example, no 2 marks: 8 of 10. The word “example” was worth marks on its own.',
        },
        {
          id: 'ps14-a-2',
          text: 'Writes “an example is the government” and stops — no account of what a duty bearer actually is or does.',
          key: { 'ps14-describe': 0, 'ps14-example': 2 },
          keyNote:
            'The example banks its fixed 2M cleanly, but with no real description the banded 8-mark scale is empty. 2 of 10. The example is a top-up, not the answer — you still owe the description that carries the marks.',
        },
      ],
      embodies: {
        behaviour: 'Answers one half of a “describe + give an example” item and forfeits the other tariff.',
        cite: MSOL('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps14',
    rule: 'When it says “give an example”, the example is its own mark.',
    detail:
      'On OL “describe + give an example” items the description is banded and the example is a separate fixed tariff (often 2M). A perfect description with no example caps below full; an example with no description earns almost nothing. Do both.',
    cite: MSOL('p.10'),
  },
};

// ─────────────── PS15 · Say "I", not just "we" ───────────────

const PS15: ScaleSession = {
  mode: 'scale',
  id: 'ps-we-i',
  subject: 'politics-society',
  level: 'higher',
  title: 'Say “I”, not just “we”',
  cue: 'Citizenship project',
  question:
    'The Citizenship Project’s “Summary of the actions undertaken” row is marked, in the scheme’s own words, “(We / I)”, and candidates are told to “distinguish clearly between group actions and your individual actions by using ‘we’ or ‘I’ as appropriate”. In a group project, a candidate writes the whole summary as “we did X, we organised Y” — the examiner can’t see what this candidate actually did. How does the actions row fare?',
  questionNote:
    'Scenario authored for this exercise. In the project’s Execution section the actions row is assessed on the We/I distinction across Excellent 12–15 / Very good 8–11 / Good 4–7 / Fair 0–3 — modelled on the 2025 HL project criteria.',
  scale: {
    name: 'Actions-undertaken row · /15 (We/I)',
    levels: [
      { id: 'ps15-fair', label: 'Fair — actions unclear (0–3)', annotation: 'F', marks: 2 },
      { id: 'ps15-good', label: 'Good — group actions, individual role blurred (4–7)', annotation: 'G', marks: 6 },
      { id: 'ps15-vgood', label: 'Very good — group and individual distinguished (8–11)', annotation: 'VG', marks: 10 },
      { id: 'ps15-exc', label: 'Excellent — clear, full We/I account (12–15)', annotation: 'E', marks: 13 },
    ],
    notes: [
      'The row is marked “(We / I)” — the group/individual distinction is part of what’s assessed.',
      'Candidates are told to “distinguish clearly between group actions and your individual actions by using ‘we’ or ‘I’”.',
      'An all-“we” account hides the individual contribution the examiner is trying to credit.',
    ],
    cite: MS('p.16–17 (project instruction “we/I” + “Summary of the actions undertaken (We / I)” row)'),
  },
  scripts: [
    {
      id: 'ps15-a',
      label: 'The report',
      persona: 'All “we”, never “I”',
      work: [
        'Describes the group’s actions fully and clearly, start to finish.',
        'Writes “we” throughout — never separates out what this candidate personally did.',
      ],
      keyLevelId: 'ps15-good',
      keyNote:
        'The account is clear, but the row is explicitly marked on the We/I distinction, and an all-“we” write-up leaves the examiner with no individual contribution to credit. The group work is visible; the candidate’s own role is not, so it can’t reach the top bands. Mark your personal actions with “I” — “I contacted…”, “I designed…”, “we then…” — and the same activity becomes individually creditable.',
      embodies: {
        behaviour: 'Writes a group project entirely as “we”, hiding the individual role the scheme asks to be distinguished.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-ps15',
    rule: 'In a group project, say “I”, not just “we”.',
    detail:
      'The project’s actions row is marked on the We/I distinction and candidates are told to separate group actions from their own using “we” or “I”. An all-“we” account hides your individual contribution and holds the row below the top bands — flag your personal actions explicitly with “I”.',
    cite: MS('p.16'),
  },
};

export const POLITICS_CHAIR: ChairSubject = {
  id: 'politics-society',
  label: 'Politics & Society',
  tagline: 'Insight over relevance, argument over summary, both documents, answer the exact question asked.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [PS1, PS2, PS3, PS4, PS5, PS6, PS7, PS8, PS9, PS10, PS11, PS12, PS13, PS14, PS15],
  sources: [
    { label: 'SEC LC Politics & Society HL marking scheme 2025 (examiner-reports/politics-society/2025-marking-scheme)' },
    { label: 'SEC LC Politics & Society OL marking scheme 2025 (examiner-reports/politics-society/2025-ol-marking-scheme)' },
    { label: 'SEC LC Politics & Society HL marking scheme 2024 (examiner-reports/politics-society/2024-marking-scheme)' },
  ],
  coverageNote:
    'The descriptor-band system applies at both levels, but the emphasis flips: HL rewards insight and evaluation; OL weights knowledge and structure heavily and makes analysis/evaluation the lightest criteria. Alongside the long-question grammar (insight over relevance, argument over summary, the split documents rubric, the both-documents band cap, and the length/brevity instruction) the Section A short-question mechanics are covered — the separate naming tariff, the asymmetric two-point split, the floating 3M slot that follows your stronger point, the fixed example tariff, the presentation-of-data question, and the correct-use rule. The Citizenship Project adds the discrete 0/2/4 reference scale and the We/I distinction. OL sessions (PS4, PS9, PS14) are verified against the 2025 OL scheme; the both-documents cap and floating-slot note against the 2024 HL scheme; all others against the 2025 HL scheme.',
};
