/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — History (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (the Cumulative Mark + Overall Evaluation 60/40 system, the
 * paragraph-band CM, the holistic OE bands, the two-element CM cap, and the
 * DBQ comparison "one document only" cap) is the real SEC system, cited to:
 *  - SEC LC History HL marking scheme 2025 —
 *    examiner-reports/history/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC History HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC History OL marking scheme 2025, ${p}` });

// ─────────────── His1 · CM and OE ───────────────

const OE_BANDS: ScaleLevel[] = [
  { id: 'vweak', label: 'Very weak (0–9)', annotation: '5', marks: 5 },
  { id: 'weak', label: 'Weak (10–16)', annotation: '13', marks: 13 },
  { id: 'fair', label: 'Fair (17–23)', annotation: '20', marks: 20 },
  { id: 'good', label: 'Good (24–29)', annotation: '27', marks: 27 },
  { id: 'vgood', label: 'Very good (30–33)', annotation: '32', marks: 32 },
  { id: 'excellent', label: 'Excellent (34–40)', annotation: '37', marks: 37 },
];

const HIS1: ScaleSession = {
  mode: 'scale',
  id: 'his-cm-oe',
  subject: 'history',
  level: 'higher',
  title: 'Story vs argument',
  cue: 'Essay',
  question: 'An essay is packed with accurate, relevant facts, told as a flowing story from start to finish — but it never analyses, weighs evidence, or argues toward a conclusion. The Cumulative Mark for content is strong. Which OVERALL EVALUATION band (out of 40) does it earn?',
  questionNote:
    'Scenario authored for this exercise. Every History essay is marked under two headings that sum to the full mark: Cumulative Mark (content, /60) and Overall Evaluation (whole-answer quality, /40) — a fixed 60/40 split. This session is about the OE band.',
  scale: {
    name: 'Overall Evaluation · /40',
    levels: OE_BANDS,
    notes: [
      'Essays are marked 60/40: Cumulative Mark (content) + Overall Evaluation (quality).',
      'The OE criterion asks for “more than mere narrative” — analysis, marshalled evidence, and a conclusion.',
      'A purely narrative answer — however factually rich — caps in the lower OE bands.',
      'The facts still earn their CM; OE is the separate 40 marks a story leaves behind.',
    ],
    cite: MS('p.12, p.14–15 (CM/OE 60/40; OE bands; “more than mere narrative” criterion)'),
  },
  scripts: [
    {
      id: 'his1-a',
      label: 'The essay',
      persona: 'Great story, no argument',
      work: [
        'Accurate, relevant facts throughout.',
        'Told as a continuous narrative — “and then… and then…”.',
        'No analysis, no weighing of evidence, no conclusion.',
      ],
      keyLevelId: 'weak',
      keyNote:
        'Around the Weak OE band — narrative alone can’t climb higher, because OE explicitly pays for analysis, marshalled evidence and a conclusion. The same facts, reorganised into an argument that answers the question and reaches a judgement, could lift OE by 15–20 marks. The content was never the problem; the shaping was.',
      embodies: {
        behaviour: 'Writes narrative rather than analysis — capped in the lower OE bands.',
        cite: MS('p.14'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his1',
    rule: 'Facts earn CM; argument earns OE.',
    detail:
      'History essays are marked 60/40 — content and overall quality. A flowing story banks the content marks but caps the 40 Overall Evaluation marks. Analyse, weigh evidence, and argue to a conclusion to earn the other 40%.',
    cite: MS('p.14'),
  },
};

// ─────────────── His2 · The two-element cap ───────────────

const HIS2: ScaleSession = {
  mode: 'scale',
  id: 'his-two-element',
  subject: 'history',
  level: 'higher',
  title: 'Answer both halves',
  cue: 'Essay',
  question: 'An essay title asks about TWO elements (e.g. “the causes AND the consequences”). The candidate writes a superb answer — but only on the causes, ignoring the consequences entirely. What is the maximum Cumulative Mark (out of 60) now available?',
  questionNote:
    'Scenario authored for this exercise. Most two-element essay titles carry a scheme note: if only one element is addressed, the maximum Cumulative Mark is capped at 50 — a fixed 10-mark haircut.',
  scale: {
    name: 'Cumulative Mark cap · /60',
    levels: [
      { id: 'm50', label: 'Max 50 (one element)', annotation: '50', marks: 50 },
      { id: 'm60', label: 'Max 60 (both elements)', annotation: '60', marks: 60 },
    ],
    notes: [
      'Two-element titles carry the note: “If only ONE, Max. CM = 50.”',
      'It is a fixed cap, not a zero — a one-sided answer can still score up to 50.',
      'But the top 10 CM marks are locked behind addressing the second element.',
    ],
    cite: MS('p.15–18 (two-element CM cap)'),
  },
  scripts: [
    {
      id: 'his2-a',
      label: 'The essay',
      persona: 'Brilliant — on one half',
      work: [
        'A superb, detailed treatment of the causes.',
        'The consequences — the second required element — are not addressed at all.',
      ],
      keyLevelId: 'm50',
      keyNote:
        'Capped at 50 CM, no matter how good the causes are. The scheme’s “if only ONE, Max CM = 50” note means the last 10 content marks simply aren’t available until the second element is addressed. Even a short, weaker section on consequences would unlock them. Always cover every element the title names.',
      embodies: {
        behaviour: 'Answers only one element of a two-element question — the fixed CM cap applies.',
        cite: MS('p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his2',
    rule: 'A two-part title needs both parts.',
    detail:
      'If a History title names two elements and you address only one, the Cumulative Mark is capped at 50/60 — a flat 10-mark loss. Even a brief second section unlocks those marks. Underline every element in the title before you start.',
    cite: MS('p.15'),
  },
};

// ─────────────── His3 · DBQ comparison cap ───────────────

const HIS3: ScaleSession = {
  mode: 'scale',
  id: 'his-dbq-compare',
  subject: 'history',
  level: 'higher',
  title: 'Compare means both documents',
  cue: 'Documents question',
  question: 'A Documents-Based Question comparison part (worth 20) asks how two sources treat an issue. The candidate writes a thorough, insightful analysis — but only of Document A, never engaging Document B. What is the maximum mark?',
  questionNote:
    'Scenario authored for this exercise. In the DBQ comparison, the scheme states an answer referring to one document only is capped at 5 marks.',
  scale: {
    name: 'DBQ comparison · /20',
    levels: [
      { id: 'm5', label: 'Max 5 (one document)', annotation: '5', marks: 5 },
      { id: 'm14', label: '14 (both, partial)', annotation: '14', marks: 14 },
      { id: 'm20', label: '20 (full comparison)', annotation: '20', marks: 20 },
    ],
    notes: [
      'The comparison rule: “Answer referring to one document only = 5M max.”',
      'Comparison marks exist for the relationship between the two sources.',
      'However insightful, a single-document answer forfeits everything above 5.',
    ],
    cite: MS('p.8–9 (DBQ comparison, one-document cap)'),
  },
  scripts: [
    {
      id: 'his3-a',
      label: 'The answer',
      persona: 'Deep — on one source',
      work: [
        'A thorough, insightful analysis of Document A.',
        'Document B is never mentioned.',
      ],
      keyLevelId: 'm5',
      keyNote:
        'Capped at 5 of 20. A “comparison” question pays for the relationship between the sources — analysing one brilliantly still misses what the question rewards. Even a couple of lines linking B to A would break past the cap. Compare means both, side by side.',
      embodies: {
        behaviour: 'Answers a comparison using only one document — capped at 5 marks.',
        cite: MS('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his3',
    rule: 'A comparison must touch both sources.',
    detail:
      'In the DBQ, a comparison answer that engages only one document is capped at 5/20. The marks live in the relationship between the sources — always reference both and draw the link explicitly.',
    cite: MS('p.8'),
  },
};

// ─────────────── His4 · OL — count your Core Statements ───────────────

const HIS4: GridSession = {
  mode: 'grid',
  id: 'his-ol-core-statements',
  subject: 'history',
  level: 'ordinary',
  title: 'Count your Core Statements',
  cue: 'Part B (OL)',
  question: 'An Ordinary Level Part B answer is worth 20 for content (CM), marked as Core Statements at a flat 5 marks each — so it wants four distinct, completed, relevant points. A candidate writes three strong completed points, then pads the rest by restating the first point in new words.',
  questionNote:
    'Scenario authored for this exercise. Unlike Higher (banded paragraphs, 60/40 CM:OE), OL History marks long answers by counting Core Statements — each a flat 5 marks; Part B wants four, Part C wants six.',
  grid: {
    perPoint: [
      { id: 'cs1', label: 'Core Statement 1', marks: 5 },
      { id: 'cs2', label: 'Core Statement 2', marks: 5 },
      { id: 'cs3', label: 'Core Statement 3', marks: 5 },
      { id: 'cs4', label: 'Core Statement 4', marks: 5 },
    ],
    shorthand: '4 Core Statements @ 5m = 20 CM',
    ruleNote:
      'Each distinct, completed, relevant Core Statement is a flat 5 marks. Depth beyond “completed” isn’t rewarded, and repetition isn’t a new statement — so padding by restating a point earns nothing. You need four genuinely distinct points.',
    cite: MSOL('p.10, p.11 (Core Statement = 5 marks; Part B needs four)'),
  },
  scripts: [
    {
      id: 'his4-a',
      label: 'Script A',
      persona: 'Three points, then padding',
      attempts: [
        {
          id: 'his4-a-1',
          text: 'Core Statement 1 — a distinct, completed, relevant point.',
          key: { cs1: 5, cs2: 0, cs3: 0, cs4: 0 },
          keyNote: 'A completed relevant point — the flat 5 marks. No extra credit for writing more about it; the mark is for the point being made.',
        },
        {
          id: 'his4-a-2',
          text: 'Core Statement 2 — a second distinct completed point.',
          key: { cs1: 0, cs2: 5, cs3: 0, cs4: 0 },
          keyNote: 'A second distinct statement. 5.',
        },
        {
          id: 'his4-a-3',
          text: 'Core Statement 3 — a third distinct completed point.',
          key: { cs1: 0, cs2: 0, cs3: 5, cs4: 0 },
          keyNote: 'A third distinct statement. 5.',
        },
        {
          id: 'his4-a-4',
          text: 'The “fourth” — a reworded restatement of Core Statement 1, padding for length.',
          key: { cs1: 0, cs2: 0, cs3: 0, cs4: 0 },
          keyNote: 'Not a new Core Statement — it repeats the first, so it earns nothing. 15 of 20. A fourth distinct point, however brief, would have banked the last 5. At OL, count your statements: four distinct completed points, not three plus padding.',
        },
      ],
      embodies: {
        behaviour: 'Pads a Core-Statement answer by restating a point instead of giving a fourth distinct one.',
        cite: MSOL('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his4',
    rule: 'At OL, count distinct Core Statements — padding earns nothing.',
    detail:
      'Ordinary Level History marks long answers by counting Core Statements at a flat 5 marks each (Part B wants four, Part C six). Depth past “completed” isn’t rewarded and repetition isn’t a new point — give the number of distinct statements the part expects.',
    cite: MSOL('p.11'),
  },
};

// ─────────────── His5 · RSR — how a source citation earns its marks ───────────────

const HIS5: GridSession = {
  mode: 'grid',
  id: 'his-rsr-citation',
  subject: 'history',
  level: 'higher',
  title: 'Cite it, or lose the marks',
  cue: 'RSR Outline Plan',
  question:
    'In the Research Study Report Outline Plan, citing the sources is worth 6 of the 15 marks — three sources at 2 marks each, and each 2 splits into Author + title (1) and an extra validating detail like publisher or date (1). A candidate lists three items: (1) a full citation with author, title and year; (2) an author and title only; (3) the class textbook.',
  questionNote:
    'Scenario authored for this exercise. The RSR asks for three appropriate sources; the scheme awards each 2 marks as Author + title (1) + validating detail (1), and warns that standard school textbooks are not suitable sources.',
  grid: {
    perPoint: [
      { id: 'authortitle', label: 'Author + title', marks: 1 },
      { id: 'validating', label: 'Validating detail (e.g. publisher, date)', marks: 1 },
    ],
    shorthand: '3 sources @ (1 + 1) = max 6',
    ruleNote:
      'Each appropriate source is worth 2: one mark for author + title, one more for a validating detail (publisher, date). A standard school textbook is explicitly not a suitable source, so it earns nothing at all — not even the author + title mark.',
    cite: MS('p.4 (RSR Outline Plan — citation of sources; textbook exclusion)'),
  },
  scripts: [
    {
      id: 'his5-a',
      label: 'Script A',
      persona: 'Two clean, one careless',
      attempts: [
        {
          id: 'his5-a-1',
          text: 'Source 1 — full citation: author, title, and year of publication.',
          key: { authortitle: 1, validating: 1 },
          keyNote: 'Author + title banks the first mark; the year is the validating detail that banks the second. The full 2.',
        },
        {
          id: 'his5-a-2',
          text: 'Source 2 — author and title given, but no publisher, date or other validating detail.',
          key: { authortitle: 1, validating: 0 },
          keyNote: 'Author + title is there — 1 mark. With no validating detail, the second mark is simply not earned. A publisher or date would have completed the pair.',
        },
        {
          id: 'his5-a-3',
          text: 'Source 3 — the standard class textbook.',
          key: { authortitle: 0, validating: 0 },
          keyNote: 'Nothing. The scheme states standard school textbooks are not suitable sources, so this is not an appropriate source to cite — no author + title mark, no validating mark. 3 of the 6 citation marks in total; a second real source in place of the textbook would have added up to 2 more.',
        },
      ],
      embodies: {
        behaviour: 'Offers a standard school textbook as one of the three RSR sources, which the guidelines exclude.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his5',
    rule: 'A citation earns marks twice — name it, then validate it.',
    detail:
      'In the RSR each source is worth 2: author + title (1) and a validating detail such as publisher or date (1). Give both for all three sources — and never offer a standard school textbook, which the scheme rules out as a source entirely.',
    cite: MS('p.4'),
  },
};

// ─────────────── His6 · A conclusion that just repeats caps at 4 ───────────────

const HIS6: ScaleSession = {
  mode: 'scale',
  id: 'his-summation-repetition',
  subject: 'history',
  level: 'higher',
  title: 'A conclusion has to do work',
  cue: 'Concluding paragraph',
  question:
    'A candidate ends a strong essay with a final paragraph — but it just restates the introduction and the points already made, almost word for word. As a Cumulative Mark paragraph (a paragraph can score up to 12), what is the most that closing paragraph can earn?',
  questionNote:
    'Scenario authored for this exercise. A concluding paragraph counts as a markable "paragraph equivalent" — but the scheme attaches a note: a summation that is mere repetition is capped at 4 marks.',
  scale: {
    name: 'Concluding paragraph · CM',
    levels: [
      { id: 'rep', label: 'Mere repetition (max 4)', annotation: '4', marks: 4 },
      { id: 'fresh', label: 'Fresh summation — Good', annotation: '7', marks: 7 },
      { id: 'analytic', label: 'Analytic summation — Excellent', annotation: '12', marks: 12 },
    ],
    notes: [
      'A good concluding paragraph or summation counts as a full paragraph equivalent (up to 12).',
      'But the scheme adds: “Summation which is mere repetition = max 4 marks.”',
      'A conclusion that only re-states earlier material is capped — it has to add analysis, weigh the argument, or reach a judgement to score as a real paragraph.',
    ],
    cite: MS('p.13, p.11 (paragraph equivalent (vii); “Summation which is mere repetition = max 4 marks”)'),
  },
  scripts: [
    {
      id: 'his6-a',
      label: 'The conclusion',
      persona: 'Says it all again',
      work: [
        'Restates the introduction almost verbatim.',
        'Lists the same points already made in the body.',
        'Adds no new analysis, no weighing of the case, no judgement.',
      ],
      keyLevelId: 'rep',
      keyNote:
        'Capped at 4. However neat the wording, a summation that is mere repetition hits the scheme’s explicit ceiling — it is not treated as a fresh, markable paragraph. A conclusion that instead weighed the argument and reached a judgement could have scored as a Good or Excellent paragraph (up to 12). End by answering the question, not by echoing yourself.',
      embodies: {
        behaviour: 'Writes a concluding paragraph that only repeats earlier material — the mere-repetition cap applies.',
        cite: MS('p.13'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his6',
    rule: 'A conclusion that only repeats is capped at 4.',
    detail:
      'A concluding paragraph counts as a full CM paragraph (up to 12) only if it does something new — weighs the case, reaches a judgement. A summation that merely restates earlier material is capped at 4. Use the conclusion to answer the question, not to echo the essay.',
    cite: MS('p.13'),
  },
};

// ─────────────── His7 · Evaluate the source, don’t retell it ───────────────

const HIS7: ScaleSession = {
  mode: 'scale',
  id: 'his-source-value',
  subject: 'history',
  level: 'higher',
  title: 'Value, not summary',
  cue: 'DBQ Criticism (b)',
  question:
    'A DBQ Criticism question (worth 10) asks the candidate to “assess the value of this source” for a historian. The candidate accurately retells everything the document says — but never comments on who wrote it, when, its bias, its reliability, or what it leaves out. On the 0–10 sliding scale, which band does it earn?',
  questionNote:
    'Scenario authored for this exercise. The Criticism “value of the source” part is marked on a single sliding scale out of 10 (Excellent 9–10 … Weak 0–2). The scheme’s indicative points are all about evaluating the source — primary vs secondary, the author’s expertise, bias, and what the source omits — not about summarising its content.',
  scale: {
    name: 'Criticism (b) · value of the source · /10',
    levels: [
      { id: 'weak', label: 'Weak (0–2)', annotation: '1', marks: 1 },
      { id: 'fair', label: 'Fair (3–4)', annotation: '4', marks: 4 },
      { id: 'good', label: 'Good (5–6)', annotation: '6', marks: 6 },
      { id: 'vgood', label: 'Very good (7–8)', annotation: '8', marks: 8 },
      { id: 'excellent', label: 'Excellent (9–10)', annotation: '10', marks: 10 },
    ],
    notes: [
      'Marked on one sliding scale out of 10: Excellent 9–10, Very good 7–8, Good 5–6, Fair 3–4, Weak 0–2.',
      'The question is “value of the source” — the marks are for evaluation, not for retelling the content.',
      'The scheme’s model points weigh the source type, the author’s reliability and bias, and what the source omits.',
      'A pure content summary does not address the question asked, so it lands in the bottom band.',
    ],
    cite: MS('p.10 (Criticism (b), assess the value of the source; 0–10 sliding scale)'),
  },
  scripts: [
    {
      id: 'his7-a',
      label: 'The answer',
      persona: 'Retells, never evaluates',
      work: [
        'Accurately paraphrases everything the document states.',
        'Never says who wrote it, when, or from what standpoint.',
        'No comment on bias, reliability, or what the source leaves out.',
      ],
      keyLevelId: 'weak',
      keyNote:
        'Bottom band. The answer is accurate but it never does what the question asks — it summarises the source instead of evaluating its value. The marks here are for weighing the source: primary or secondary, the author’s expertise and bias, and the gaps it leaves. Even two lines — “this is a primary source, so… but the writer is biased because…” — would lift it several marks. Assess the source; don’t retell it.',
      embodies: {
        behaviour: 'Paraphrases a document’s content instead of evaluating it as a historical source.',
        cite: MS('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his7',
    rule: 'A “value of the source” question pays for evaluation, not summary.',
    detail:
      'When the DBQ asks you to assess a source’s value, the marks are for weighing it — primary vs secondary, the author’s expertise and bias, and what it omits. Retelling the content, however accurately, answers a different question and bands low. Judge the source; don’t summarise it.',
    cite: MS('p.10'),
  },
};

export const HISTORY_CHAIR: ChairSubject = {
  id: 'history',
  label: 'History',
  tagline: 'CM and OE — why the story is only 60% of the mark.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [HIS1, HIS2, HIS3, HIS4, HIS5, HIS6, HIS7],
  sources: [
    { label: 'SEC LC History HL marking scheme 2025 (examiner-reports/history/2025-marking-scheme)' },
    { label: 'SEC LC History OL marking scheme 2025 (examiner-reports/history/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'Higher sessions span the whole paper: the 60/40 CM:OE banded-paragraph essay system, the two-element CM cap, the DBQ comparison and source-value rules, the concluding-paragraph repetition cap, and the RSR citation grid. Ordinary Level is marked differently — by counting Core Statements at a flat 5 marks each, with no essay — so the OL session is verified separately against the 2025 OL scheme. More OL sessions are being added.',
};
