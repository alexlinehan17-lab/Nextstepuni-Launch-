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
 * rubric) is the real SEC system, cited to:
 *  - SEC LC Politics & Society HL marking scheme 2025 —
 *    examiner-reports/politics-society/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Politics & Society HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Politics & Society OL marking scheme 2025, ${p}` });

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

export const POLITICS_CHAIR: ChairSubject = {
  id: 'politics-society',
  label: 'Politics & Society',
  tagline: 'Insight over relevance, argument over summary, cite your sources.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [PS1, PS2, PS3, PS4],
  sources: [
    { label: 'SEC LC Politics & Society HL marking scheme 2025 (examiner-reports/politics-society/2025-marking-scheme)' },
    { label: 'SEC LC Politics & Society OL marking scheme 2025 (examiner-reports/politics-society/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The descriptor-band system applies at both levels, but the emphasis flips: HL rewards insight and evaluation; OL weights knowledge and structure heavily and makes analysis/evaluation the lightest criteria. The OL session is verified against the 2025 OL scheme.',
};
