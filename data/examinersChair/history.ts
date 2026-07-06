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
    {
      id: 'his3-border',
      label: 'The comparison',
      persona: 'Both sources — one thinly',
      work: [
        'A full, well-developed analysis of Document A.',
        'A single sentence noting that Document B “says something similar”.',
        'No real development of B, and no sustained link drawn between the two.',
      ],
      keyLevelId: 'm14',
      keyNote:
        'Lands at 14 — not the 5-mark cap, not the full 20. The one line on Document B is a genuine reference to the second source, so the “one document only = 5M” cap is cleared: a harsh marker who ignores that sentence and pins it at 5 is wrong. But a bare mention is not a developed comparison, so the top band — a sustained, two-sided treatment — stays out of reach, and the generous marker who rewards the strong A section with full marks is wrong too. Both documents touched, the relationship only half-built: exactly the middle rung.',
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
    {
      id: 'his6-border',
      label: 'The conclusion',
      persona: 'Half-fresh, half-echo',
      work: [
        'Opens by re-stating two points already made in the body.',
        'Then briefly weighs them and offers a genuine, if thin, judgement on the question.',
        'The new analysis is real but undeveloped.',
      ],
      keyLevelId: 'fresh',
      keyNote:
        'A Good paragraph — about 7 — not the 4-mark cap and not the Excellent ceiling. Because it does weigh the case and reach a judgement, it is more than mere repetition, so the “summation which is mere repetition = max 4” cap does not bite: the marker who sees the opening echo and pins it at 4 is too harsh. But the fresh work is thin and undeveloped, so it cannot score as an analytic, Excellent summation; the marker who rewards the mere presence of a conclusion with 12 is too generous. Part fresh, part echo — the middle rung is where it belongs.',
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
    {
      id: 'his7-border',
      label: 'The answer',
      persona: 'Half-evaluates, half-retells',
      work: [
        'Correctly identifies the document as a primary source, written by an eye-witness.',
        'Notes that this makes it useful first-hand evidence of the events.',
        'But then slips back into retelling the content, never weighing the author’s bias or what the source leaves out.',
      ],
      keyLevelId: 'good',
      keyNote:
        'A Good answer — 5 to 6 — neither the bottom band nor the top. It genuinely evaluates: naming the source type and the author’s closeness to the events are real “value” points, so it clears the Weak band a pure summary would earn, and the marker who dismisses it as retelling is too harsh. But the evaluation stops half-way — nothing on bias, reliability or omission — so it cannot climb to Very good or Excellent, and the marker who rewards the strong opening with 8-plus is too generous. Half the source weighed, half only retold: the middle of the scale.',
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

// ─────────────── His8 · RSR — the sources you skip cap the ones you keep ───────────────

const HIS8: ScaleSession = {
  mode: 'scale',
  id: 'his-rsr-evaluation',
  subject: 'history',
  level: 'higher',
  title: 'Two sources cap you at 17',
  cue: 'RSR Evaluation of the Sources',
  question:
    'The Research Study Report Evaluation of the Sources is worth 25. A candidate evaluates only two of the three sources — but does it brilliantly, with sharp comment on strengths, weaknesses and relevance. On the scheme’s graduated ceiling, what is the most those 25 marks can now become?',
  questionNote:
    'Scenario authored for this exercise. The Evaluation of the Sources scale is graduated by how many sources the candidate engages: reference to ALL THREE tops out at 25; only TWO tops out at 17; only ONE tops out at 9 — a hard ceiling, not a quality judgement.',
  scale: {
    name: 'Evaluation of the Sources · /25',
    levels: [
      { id: 'one', label: 'One source only (max 9)', annotation: '9', marks: 9 },
      { id: 'two', label: 'Two sources only (max 17)', annotation: '17', marks: 17 },
      { id: 'three', label: 'All three sources (max 25)', annotation: '25', marks: 25 },
    ],
    notes: [
      'The scheme sets a ceiling by coverage: “Reference to ALL THREE sources — Excellent 22-25.”',
      '“Reference to only TWO sources — Excellent 15-17.”  “Reference to only ONE source — Excellent 8-9.”',
      'The ceiling is about how many sources you engage, not how well — brilliance on two still caps at 17.',
      'The whole top band (18-25) is locked behind referencing all three sources.',
    ],
    cite: MS('p.5 (Evaluation of the Sources; graduated ceiling by number of sources)'),
  },
  scripts: [
    {
      id: 'his8-a',
      label: 'The evaluation',
      persona: 'Brilliant — on two of three',
      work: [
        'Sharp comment on the strengths and weaknesses of source 1.',
        'Equally strong evaluation of source 2, tied to the subject.',
        'Source 3 is never evaluated — it drops out of the discussion.',
      ],
      keyLevelId: 'two',
      keyNote:
        'Capped at 17, however good the analysis of the two sources is. The Evaluation scale is graduated by coverage, and “only TWO sources” tops out at 17 — the eight marks above that are reserved for candidates who engage all three. A few lines evaluating the third source would have unlocked the 25-mark band. Reference every source you cited.',
      embodies: {
        behaviour: 'Evaluates only two of three cited sources — the graduated coverage ceiling applies.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his8',
    rule: 'In the RSR, the number of sources you evaluate sets the ceiling.',
    detail:
      'The Evaluation of the Sources scale is graduated: all three sources tops out at 25, two only at 17, one only at 9. Quality cannot lift you past the coverage ceiling — engage every source you cited, even briefly, to keep the top band open.',
    cite: MS('p.5'),
  },
};

// ─────────────── His9 · Past the CM cap, extra paragraphs are worth zero ───────────────

const HIS9: ScaleSession = {
  mode: 'scale',
  id: 'his-excess-paragraph',
  subject: 'history',
  level: 'higher',
  title: 'Writing past the cap',
  cue: 'Section 2/3 essay',
  question:
    'A candidate has already written enough excellent paragraphs to reach the maximum Cumulative Mark of 60 for a Section 2 essay. With time to spare, they write one more genuinely excellent paragraph of accurate, relevant content. How much Cumulative Mark does that extra paragraph add?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s marking annotations include an “excess paragraph” rule: once an answer has scored the maximum CMs allowable, further material is given notional marks with zero value attached.',
  scale: {
    name: 'Excess paragraph · CM value',
    levels: [
      { id: 'excess', label: 'Excess paragraph — notional, zero value', annotation: '0', marks: 0 },
      { id: 'within', label: 'Within the cap — counts in full', annotation: '12', marks: 12 },
    ],
    notes: [
      'The annotation rule: “Where an answer has already scored the maximum CMs allowable, any remaining material will be awarded notional marks with zero value attached.”',
      'An excellent paragraph is worth up to 12 CM — but only until the 60-mark cap is reached.',
      'Beyond the cap, the examiner may write a notional “5” beside it, but it adds nothing to the total.',
      'The time is not wasted only if it is spent on the Overall Evaluation quality, or on another question.',
    ],
    cite: MS('p.3 (Excess paragraph marks — notional marks, zero value)'),
  },
  scripts: [
    {
      id: 'his9-a',
      label: 'The extra paragraph',
      persona: 'Already at 60, still writing',
      work: [
        'The essay has already banked the maximum 60 CM.',
        'A further paragraph of accurate, relevant, well-expressed content is added.',
        'On its own it would be an Excellent paragraph.',
      ],
      keyLevelId: 'excess',
      keyNote:
        'Zero value. Once the answer has scored the maximum CM allowable, the scheme awards remaining material only notional marks — the extra paragraph, however good, cannot lift the CM past 60. The same minutes spent sharpening the argument (OE) or on a thinner answer elsewhere would have earned real marks. Know when a question is full.',
      embodies: {
        behaviour: 'Keeps adding content paragraphs after the CM cap is reached — the excess-paragraph rule applies.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his9',
    rule: 'Once the CM is maxed, extra paragraphs are worth zero.',
    detail:
      'Content marks cap at 60 per essay. The scheme gives any material beyond the cap notional marks with zero value. Piling on more paragraphs after you have reached it earns nothing — bank the marks by moving to the Overall Evaluation quality or the next question.',
    cite: MS('p.3'),
  },
};

// ─────────────── His10 · An invalid combination costs you the lowest answer ───────────────

const HIS10: ScaleSession = {
  mode: 'scale',
  id: 'his-invalid-combination',
  subject: 'history',
  level: 'higher',
  title: 'The combination you attempt',
  cue: 'Question choice',
  question:
    'A candidate attempts an invalid combination — three questions from a single topic where the rules allow only two to count. The examiner marks all three; the lowest-scoring of them is worth 10. What does that lowest answer do to the total mark?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s annotations cover invalid combinations (e.g. three questions from one topic): the lowest-scoring invalid answer(s) are deducted from the total using minus-mark annotations, entered on the Adjustment (ADJ) line.',
  scale: {
    name: 'Invalid combination · net effect',
    levels: [
      { id: 'deducted', label: 'Lowest invalid answer deducted (ADJ)', annotation: '−10', marks: -10 },
      { id: 'ignored', label: 'Simply not counted (0)', annotation: '0', marks: 0 },
      { id: 'valid', label: 'Counts toward the total (+10)', annotation: '10', marks: 10 },
    ],
    notes: [
      'The scheme: “If an invalid combination of questions was attempted the lowest scoring invalid answer(s) will be deducted from the total mark using minus-mark annotations (e.g. -10 marks).”',
      '“Invalid” is flagged where, for example, three questions are attempted from one topic.',
      'The deduction is entered on the Adjustment (ADJ) line at the bottom of the panel.',
      'So an over-attempted answer is worse than wasted effort — it actively pulls the total down.',
    ],
    cite: MS('p.3 (Invalid combination; minus-mark ADJ deduction)'),
  },
  scripts: [
    {
      id: 'his10-a',
      label: 'The extra answer',
      persona: 'Three from one topic',
      work: [
        'The rules allow two questions to count from the topic.',
        'The candidate answers a third from the same topic — an invalid combination.',
        'It is the lowest-scoring of the three, worth 10 on its own.',
      ],
      keyLevelId: 'deducted',
      keyNote:
        'Deducted. An invalid combination triggers a minus-mark ADJ: the lowest-scoring invalid answer is taken off the total, not quietly ignored. The extra answer cost time to write and then subtracted marks. Read the rubric first and answer the required spread of topics — an over-attempt from one topic can only hurt you.',
      embodies: {
        behaviour: 'Attempts an invalid combination (three questions from one topic) — the ADJ minus-mark deduction applies.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'his10-border',
      label: 'The extra answer',
      persona: 'Over-attempts — but validly',
      work: [
        'The rules let the candidate answer across the required spread of topics.',
        'They answer one question more than they need — but from an allowed topic, so the combination is valid.',
        'The examiner marks them all and counts the best; this surplus answer is the lowest.',
      ],
      keyLevelId: 'ignored',
      keyNote:
        'Net zero — neither deducted nor counted. Because the combination is valid, the minus-mark ADJ rule for invalid combinations never triggers: the marker who deducts it, as if it were three questions from one topic, is wrong. But it is a surplus answer, so only the best required answers count and it adds nothing to the total either — the marker who lets it lift the score is wrong too. A valid over-attempt is simply set aside: the middle outcome between a deduction and a credit.',
    },
  ],
  takeaway: {
    id: 'codex-his10',
    rule: 'An invalid combination is deducted, not ignored.',
    detail:
      'Answering more than the allowed number from one topic is an invalid combination: the scheme deducts the lowest-scoring invalid answer via a minus-mark on the Adjustment line. Extra answers from the wrong place actively cost marks — always answer the required spread of questions.',
    cite: MS('p.3'),
  },
};

// ─────────────── His11 · The DBQ essay is capped at 24, not 60 ───────────────

const HIS11: ScaleSession = {
  mode: 'scale',
  id: 'his-dbq-contextualisation',
  subject: 'history',
  level: 'higher',
  title: 'A mini-essay, not a full one',
  cue: 'DBQ Contextualisation (Q4)',
  question:
    'The DBQ Contextualisation (Q4) is a short essay worth 40, marked by paragraph like the big essays. A candidate, treating it like a Section 2 question, writes five excellent paragraphs of content. What is the maximum Cumulative Mark those paragraphs can earn here?',
  questionNote:
    'Scenario authored for this exercise. Q4 is marked by paragraph (CM + OE), but its split is fixed at CM = max 24 and OE = max 16 — not the 60/40 of the Section 2 and 3 essays.',
  scale: {
    name: 'Contextualisation content · CM cap',
    levels: [
      { id: 'dbq', label: 'DBQ Q4 (CM max 24)', annotation: '24', marks: 24 },
      { id: 'essay', label: 'Section 2/3 essay (CM max 60)', annotation: '60', marks: 60 },
    ],
    notes: [
      'For Q4 the scheme states: “Cumulative Mark = Max. 24 marks   Overall Evaluation = Max 16 marks.”',
      'A paragraph still tops out at 12 CM — so about two excellent paragraphs already reach the 24 cap.',
      'The Section 2/3 essays are the ones marked to CM 60; Q4 is a quarter-length answer.',
      'Extra content paragraphs in Q4 hit the excess-paragraph rule fast — the marks move to OE and to the argument.',
    ],
    cite: MS('p.11 (Contextualisation — CM max 24, OE max 16)'),
  },
  scripts: [
    {
      id: 'his11-a',
      label: 'The Q4 answer',
      persona: 'Writes it like a full essay',
      work: [
        'Five excellent paragraphs of accurate, relevant content.',
        'Enough material for a strong Section 2 essay.',
        'All of it aimed at the 40-mark Contextualisation question.',
      ],
      keyLevelId: 'dbq',
      keyNote:
        'Capped at 24 CM. Q4 is a mini-essay: its content mark maxes at 24, which about two excellent paragraphs already reach. The remaining three paragraphs are excess — the marks left in Q4 are the 16 Overall Evaluation marks, earned by arguing the case, not by more content. Size the answer to the 40, not to a 100-mark essay.',
      embodies: {
        behaviour: 'Writes a full Section-length essay for the DBQ Q4, whose CM caps at 24.',
        cite: MS('p.11'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his11',
    rule: 'The DBQ Q4 is a mini-essay — content caps at 24.',
    detail:
      'Contextualisation is marked by paragraph like the big essays, but its split is fixed at CM 24 / OE 16. Two excellent paragraphs reach the content cap; the rest of the marks are for arguing the case (OE). Size it to the 40 and spend the surplus on the argument, not more facts.',
    cite: MS('p.11'),
  },
};

// ─────────────── His12 · OL Part A — a two-part answer needs both parts ───────────────

const HIS12: GridSession = {
  mode: 'grid',
  id: 'his-ol-part-a-elements',
  subject: 'history',
  level: 'ordinary',
  title: 'Both halves of a short answer',
  cue: 'Part A (OL)',
  question:
    'An Ordinary Level Part A stimulus question is worth 6 marks, and the scheme answer names two required elements — awarding 3 marks for each, and stating explicitly that giving one element only earns 3. A candidate answers three such questions with different levels of completeness.',
  questionNote:
    'Scenario authored for this exercise. OL Section 2/3 Part A short questions are typically 6 marks each; where the answer has two parts, the scheme splits it 3m + 3m and notes “one element only = 3m”.',
  grid: {
    perPoint: [
      { id: 'pa-el1', label: 'First required element', marks: 3 },
      { id: 'pa-el2', label: 'Second required element', marks: 3 },
    ],
    shorthand: '2 elements @ 3m = 6 (one element only = 3m)',
    ruleNote:
      'A two-part Part A answer is worth 3 marks for each named element. Give one and you get 3; give both and you get the full 6. There is no bonus for elaborating a single correct element — the second 3 marks are only unlocked by the second element.',
    cite: MSOL('p.12 (Part A short questions — two elements, “one element only = 3m”)'),
  },
  scripts: [
    {
      id: 'his12-a',
      label: 'Script A',
      persona: 'Sometimes one half, sometimes both',
      attempts: [
        {
          id: 'his12-a-1',
          text: 'Names both required elements the scheme asks for (e.g. both towns / both bodies).',
          key: { 'pa-el1': 3, 'pa-el2': 3 },
          keyNote: 'Both elements present — 3 + 3 = the full 6. Exactly what the two-part answer wants.',
        },
        {
          id: 'his12-a-2',
          text: 'Names only one of the two required elements, but describes it in extra detail.',
          key: { 'pa-el1': 3, 'pa-el2': 0 },
          keyNote: 'One element only — 3 marks. The extra detail adds nothing; the missing second 3 is not for depth, it is for the second element. Naming it would have doubled the mark.',
        },
        {
          id: 'his12-a-3',
          text: 'Gives a vague or incorrect answer that matches neither required element.',
          key: { 'pa-el1': 0, 'pa-el2': 0 },
          keyNote: 'Nothing earned — neither required element is there. 9 of a possible 18 across the three questions; the middle answer alone left 3 marks on the table for want of a second word.',
        },
      ],
      embodies: {
        behaviour: 'Answers a two-part OL short question with one element only, earning half.',
        cite: MSOL('p.12'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his12',
    rule: 'At OL, a two-part short answer needs both parts.',
    detail:
      'Where an OL Part A question splits 3m + 3m, one element earns 3 and both earn 6. Depth on a single element does not buy the other three marks — only the second element does. When a question names two things, give two things.',
    cite: MSOL('p.12'),
  },
};

// ─────────────── His13 · OL RSR citation — title and author are separate marks ───────────────

const HIS13: GridSession = {
  mode: 'grid',
  id: 'his-ol-rsr-citation',
  subject: 'history',
  level: 'ordinary',
  title: 'Title, author, and one more',
  cue: 'RSR Outline Plan (OL)',
  question:
    'At Ordinary Level the RSR Outline Plan asks for two sources, each worth 3 marks: 1 for the title, 1 for the author, and 1 for a further piece of validating information such as the publisher or date. A candidate lists a source three different ways.',
  questionNote:
    'Scenario authored for this exercise. Unlike Higher (three sources, author + title bundled as one mark), the OL scheme asks for TWO sources and splits each 3-mark citation into Title (1), Author (1) and one validating detail (1).',
  grid: {
    perPoint: [
      { id: 'olcite-title', label: 'Title', marks: 1 },
      { id: 'olcite-author', label: 'Author', marks: 1 },
      { id: 'olcite-valid', label: 'Validating detail (e.g. publisher, date, website)', marks: 1 },
    ],
    shorthand: '2 sources @ (1 + 1 + 1) = max 6',
    ruleNote:
      'Each OL source is worth 3 marks, one each for the title, the author, and a validating detail like the publisher, date or website. They are three separate marks — dropping the author, or leaving off any validating detail, simply loses that one mark.',
    cite: MSOL('p.4 (OL RSR Outline Plan — Title 1 + Author 1 + validating 1; two sources)'),
  },
  scripts: [
    {
      id: 'his13-a',
      label: 'Script A',
      persona: 'Fuller each time — or not',
      attempts: [
        {
          id: 'his13-a-1',
          text: 'Source 1 — full citation: title, author, and year of publication.',
          key: { 'olcite-title': 1, 'olcite-author': 1, 'olcite-valid': 1 },
          keyNote: 'Title, author and a validating detail (the year) — all three marks. The complete 3.',
        },
        {
          id: 'his13-a-2',
          text: 'Source 2 — title and author given, but no publisher, date or website.',
          key: { 'olcite-title': 1, 'olcite-author': 1, 'olcite-valid': 0 },
          keyNote: 'Title and author bank 2; with no validating detail the third mark is simply not earned. Any publisher or date would have completed the citation.',
        },
        {
          id: 'his13-a-3',
          text: 'Source 3 — the title of a book only, with no author and no other detail.',
          key: { 'olcite-title': 1, 'olcite-author': 0, 'olcite-valid': 0 },
          keyNote: 'Title alone — 1 mark. At OL the author is a separate mark, so leaving it off costs a mark all by itself. Two easy marks were sitting in the author line and one validating detail.',
        },
      ],
      embodies: {
        behaviour: 'Gives incomplete OL citations, dropping the separately-marked author and validating detail.',
        cite: MSOL('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his13',
    rule: 'At OL a citation earns three marks — title, author, and one more.',
    detail:
      'The OL RSR asks for two sources, each worth 3: title (1), author (1), and one validating detail such as publisher, date or website (1). They are separate marks — write all three for both sources rather than a bare title.',
    cite: MSOL('p.4'),
  },
};

// ─────────────── His14 · OL Criticism — name the source type AND justify it ───────────────

const HIS14: GridSession = {
  mode: 'grid',
  id: 'his-ol-criticism-source',
  subject: 'history',
  level: 'ordinary',
  title: 'Primary or secondary — and why',
  cue: 'DBQ Criticism (a) (OL)',
  question:
    'An Ordinary Level DBQ Criticism part (worth 10) asks whether a document is a primary or secondary source. The scheme marks it 5M + 5M: 5 for correctly classifying the source and 5 for a valid supporting reason. A candidate answers three ways.',
  questionNote:
    'Scenario authored for this exercise. At OL the Criticism source-type question is a discrete 5 + 5: the correct classification (primary/secondary) earns 5, and a valid explanation earns a separate 5 — unlike the HL 0–10 sliding scale for “value of the source”.',
  grid: {
    perPoint: [
      { id: 'crit-classify', label: 'Correct classification (primary / secondary)', marks: 5 },
      { id: 'crit-reason', label: 'Valid supporting reason', marks: 5 },
    ],
    shorthand: 'Source type (5) + valid reason (5) = 10',
    ruleNote:
      'The mark is split: 5 for calling the source correctly primary or secondary, and 5 for a reason that actually justifies it (who wrote it, when, whether they were an eye-witness). A bare classification with no reason gets 5; a reason attached to the wrong classification earns neither.',
    cite: MSOL('p.9 (OL DBQ Criticism (a) — source type + valid reason, 5M + 5M)'),
  },
  scripts: [
    {
      id: 'his14-a',
      label: 'Script A',
      persona: 'Names it, sometimes explains it',
      attempts: [
        {
          id: 'his14-a-1',
          text: 'Calls Document A a primary source and explains: it was written by a participant in the events, published within a few years.',
          key: { 'crit-classify': 5, 'crit-reason': 5 },
          keyNote: 'Correct classification (5) and a valid reason that justifies it — written by a participant, close to the events (5). The full 10.',
        },
        {
          id: 'his14-a-2',
          text: 'Correctly calls it a primary source, then just retells what the document says.',
          key: { 'crit-classify': 5, 'crit-reason': 0 },
          keyNote: 'The classification is right — 5. But the “reason” is a content summary, not a justification of the source type, so the second 5 is not earned. Saying who wrote it and when would have banked it.',
        },
        {
          id: 'his14-a-3',
          text: 'Calls it a secondary source (wrong) and offers no reason.',
          key: { 'crit-classify': 0, 'crit-reason': 0 },
          keyNote: 'Wrong classification and nothing to support it — 0. 15 of a possible 30 across the three: the reason mark is only ever earned by explaining the source type, never by summarising the source.',
        },
      ],
      embodies: {
        behaviour: 'Names a source type without justifying it, or misclassifies it — losing the reason mark.',
        cite: MSOL('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his14',
    rule: 'Name the source type — then say why.',
    detail:
      'The OL Criticism source-type question is 5 + 5: 5 for correctly calling it primary or secondary, 5 for a reason that justifies the call (who wrote it, when, were they there). Retelling the document is not a reason — classify it, then explain the classification.',
    cite: MSOL('p.9'),
  },
};

// ─────────────── His15 · OL — a finished statement is worth 5, an unfinished one 1–4 ───────────────

const HIS15: ScaleSession = {
  mode: 'scale',
  id: 'his-ol-incomplete-statement',
  subject: 'history',
  level: 'ordinary',
  title: 'Finish the statement',
  cue: 'Core Statement (OL)',
  question:
    'At Ordinary Level, long answers are marked by Core Statement — each completed one worth a flat 5. A candidate, running out of time, begins a final statement with a relevant fact but never completes it into a full, relevant point. How is that last statement marked?',
  questionNote:
    'Scenario authored for this exercise. The OL Core Statement rule awards 5 for each completed statement, but adds that an incomplete Core Statement at the end of an answer may merit 1–4 marks — partial, not the full 5.',
  scale: {
    name: 'Final Core Statement · marks',
    levels: [
      { id: 'incomplete', label: 'Incomplete Core Statement (1–4)', annotation: '3', marks: 3 },
      { id: 'complete', label: 'Completed Core Statement (5)', annotation: '5', marks: 5 },
    ],
    notes: [
      'The scheme: “Each completed Core Statement is awarded 5 marks.”',
      '“An incomplete Core Statement at the end of an answer may merit 1-4 marks.”',
      'So a started-but-unfinished point earns partial credit — never the full 5.',
      'Four completed statements beat five where the last is a fragment.',
    ],
    cite: MSOL('p.10 (Core Statement — completed = 5; incomplete at end = 1–4 marks)'),
  },
  scripts: [
    {
      id: 'his15-a',
      label: 'The last statement',
      persona: 'Out of time, trails off',
      work: [
        'The answer ends mid-thought — a relevant fact is named.',
        'But it is never developed into a complete, relevant point.',
        'The pen stops before the statement is finished.',
      ],
      keyLevelId: 'incomplete',
      keyNote:
        'Partial — 1 to 4, not 5. The scheme gives full marks only to a completed Core Statement; an unfinished one at the end merits 1–4. The gap between a fragment and a finished point can be a couple of marks per statement. Better to write fewer statements and complete each than to trail off in the last one.',
      embodies: {
        behaviour: 'Leaves the final Core Statement incomplete, earning partial rather than the full 5.',
        cite: MSOL('p.10'),
      },
    },
  ],
  takeaway: {
    id: 'codex-his15',
    rule: 'A finished statement is 5; an unfinished one is 1–4.',
    detail:
      'OL long answers score 5 for each completed Core Statement, but only 1–4 for one left incomplete at the end. Complete every point you start — four finished statements outscore five where the last is a fragment.',
    cite: MSOL('p.10'),
  },
};

export const HISTORY_CHAIR: ChairSubject = {
  id: 'history',
  label: 'History',
  tagline: 'CM and OE — why the story is only 60% of the mark.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [HIS1, HIS2, HIS3, HIS4, HIS5, HIS6, HIS7, HIS8, HIS9, HIS10, HIS11, HIS12, HIS13, HIS14, HIS15],
  sources: [
    { label: 'SEC LC History HL marking scheme 2025 (examiner-reports/history/2025-marking-scheme)' },
    { label: 'SEC LC History OL marking scheme 2025 (examiner-reports/history/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'Higher sessions span the whole paper: the 60/40 CM:OE banded-paragraph essay system, the two-element CM cap, the DBQ comparison, source-value and Contextualisation (CM 24 / OE 16) rules, the concluding-paragraph repetition cap, the excess-paragraph and invalid-combination annotations, and the RSR citation and graduated Evaluation-of-Sources ceilings. Ordinary Level is marked differently — by Core Statements at a flat 5 marks each and short two-part Part A answers — so the OL sessions (Core Statements, incomplete-statement partial credit, the two-element Part A split, the OL RSR citation, and the OL source-type Criticism) are verified separately against the 2025 OL scheme.',
};
