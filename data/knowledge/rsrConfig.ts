/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * RSR Section Allocator — section specs, source-evaluation checks,
 * Review-of-Process slop patterns (Stage 3.2).
 *
 * Sources:
 * - Dossier § A2 (RSR mark allocation), § B5 (2017 History CER —
 *   "vague Review of Process", "only 2 sources at HL when 3 required",
 *   "weak chronological control")
 * - PDST History RSR guidance
 *
 * Word ranges per section are derived from the dossier's published
 * total ranges (HL 1,200–1,500; OL 600–800) split proportionally to
 * each section's mark weight. Specific per-section targets are
 * approximations that schemes accept.
 */

import { type RsrSectionSpec, type SourceEvalCheckSpec, type SlopPattern } from '../../types/knowledge';

// ─── Section specifications ────────────────────────────────────────────

export const RSR_SECTIONS: RsrSectionSpec[] = [
  {
    id: 'outline-plan',
    label: 'Outline Plan',
    marksOf100: 15,
    hlMin: 150,
    hlMax: 225,
    olMin: 75,
    olMax: 120,
    guidance: 'Title, research question, key sub-questions, and the rationale for the topic. Examiners look for a precise question — not a topic name.',
  },
  {
    id: 'evaluation-sources',
    label: 'Evaluation of Sources',
    marksOf100: 25,
    hlMin: 300,
    hlMax: 375,
    olMin: 150,
    olMax: 200,
    guidance: '3 sources at HL (2 at OL). Each source must be evaluated against Origin / Purpose / Value / Limitations. The 2017 CER specifically flagged weak source criticism.',
  },
  {
    id: 'extended-essay',
    label: 'Extended Essay',
    marksOf100: 50,
    hlMin: 600,
    hlMax: 750,
    olMin: 300,
    olMax: 400,
    guidance: 'The body of your research. Chronological control, named events with dates, integration of source material. Half the marks live here.',
  },
  {
    id: 'review-process',
    label: 'Review of Process',
    marksOf100: 10,
    hlMin: 100,
    hlMax: 150,
    olMin: 60,
    olMax: 80,
    guidance: 'Specific decisions you made, sources you abandoned, methods that did and did not work. Examiners hunt for specifics — not "I researched on the internet".',
  },
];

// ─── Source evaluation checks ─────────────────────────────────────────

export const SOURCE_EVAL_CHECKS: SourceEvalCheckSpec[] = [
  {
    id: 'origin',
    label: 'Origin',
    promptQuestion: 'Who created this source, when, and where?',
    signalPatterns: [
      'written by', 'authored by', 'published in', 'the author',
      'composed in', 'first appeared', 'commissioned by', 'issued in',
      'in [yY]ear', 'this source was', 'the document was',
      'originated in', 'recorded in', 'broadcast in',
      'this primary source', 'this secondary source',
      'a memoir', 'a newspaper', 'a speech', 'a letter', 'a treaty',
      'a propaganda poster', 'a pamphlet',
    ],
    prescription: 'Open the evaluation with author + date + form. The marker scans the first sentence for these. "Written by Erich Maria Remarque in 1929" beats "this novel was about WWI".',
  },
  {
    id: 'purpose',
    label: 'Purpose',
    promptQuestion: 'Why was the source created? Who was it for?',
    signalPatterns: [
      'in order to', 'aim was', 'aimed to', 'intended to', 'intended audience',
      'the purpose was', 'this was meant to', 'to persuade',
      'to inform', 'to record', 'to commemorate', 'to argue',
      'audience for this', 'the readership',
      'a target audience', 'the writer wanted to',
      'designed to', 'created to',
    ],
    prescription: 'Name the audience and the function. "Aimed at the British home front to maintain morale" is a purpose; "this was about war" is not.',
  },
  {
    id: 'value',
    label: 'Value',
    promptQuestion: 'What does this source tell us about the period that other sources cannot?',
    signalPatterns: [
      'this source tells us', 'useful for', 'valuable for',
      'first-hand account', 'primary source provides',
      'reveals', 'demonstrates', 'shows that',
      'this source is valuable', 'gives insight', 'unique perspective',
      'eyewitness', 'lived experience',
    ],
    prescription: 'Name what only this source tells us. "Reveals the everyday domestic experience of rationing" is a value claim; "this is a useful source" is not.',
  },
  {
    id: 'limitations',
    label: 'Limitations',
    promptQuestion: 'What are the source\'s biases, gaps, or weaknesses?',
    signalPatterns: [
      'however', 'although', 'limitation', 'limited',
      'biased', 'one-sided', 'subjective', 'partial',
      'omits', 'does not address', 'fails to', 'silent on',
      'propaganda', 'agenda', 'should be treated with caution',
      'the source\'s perspective', 'must be weighed against',
      'cannot be relied upon', 'lacks', 'no mention of',
    ],
    prescription: 'Per the 2017 History CER: "few were able to use quotations to show weaknesses". Name the bias and quote the giveaway phrase.',
  },
];

// ─── Slop patterns for Review of Process ──────────────────────────────

export const SLOP_PATTERNS: SlopPattern[] = [
  {
    id: 'researched-on-internet',
    pattern: 'I (researched|did research|searched|looked) (on the )?(internet|google|online|web)',
    flag: 'Generic research method. The marker has read this sentence ten thousand times.',
    prescription: 'Name the specific archive, journal, or database. "JSTOR\'s collection of inter-war pamphlets" beats "the internet".',
  },
  {
    id: 'books-and-websites',
    pattern: 'I used (books and websites|websites and books|various sources|different sources|many sources)',
    flag: 'Vague enumeration of source types.',
    prescription: 'Name 2-3 specific sources by author and date. "Foster\'s Modern Ireland (1988), Townshend\'s Easter 1916 (2005), and a 1916 Catholic Bulletin issue" is what the marker is hunting.',
  },
  {
    id: 'challenging-at-times',
    pattern: '(it was|was) (challenging|difficult|hard) (at times|sometimes|occasionally)',
    flag: 'Filler reflection without a specific challenge named.',
    prescription: 'Name the specific decision that was hard and what you did. "Choosing between three biographies of Carson — I picked the most recent because…" is a real reflection.',
  },
  {
    id: 'learned-a-lot',
    pattern: 'I (learned|learnt) (a lot|so much|new things|much)',
    flag: 'Generic outcome statement. Examiners want what changed in your understanding.',
    prescription: 'Name what you believed before vs after. "I had assumed Pearse spoke for the IRB; reading Foster, I revised that view" is specific.',
  },
  {
    id: 'worked-hard',
    pattern: 'I (worked hard|tried my best|put in the effort|did my best)',
    flag: 'Praise for yourself, not analysis.',
    prescription: 'Cut entirely. Effort is assumed; specific decisions are not.',
  },
  {
    id: 'time-management',
    pattern: '(time management|managing my time|finding time) (was|is) (important|essential|crucial)',
    flag: 'Generic platitude. Every RSR contains this sentence.',
    prescription: 'Name the specific scheduling decision: "I set aside two hours each Sunday for source review and three for writing" is a real method.',
  },
  {
    id: 'enjoyed-this-topic',
    pattern: 'I (really )?(enjoyed|loved|liked|found interesting) (this topic|the topic|my research|this project)',
    flag: 'Personal preference, not research method.',
    prescription: 'Cut. The marker is checking decisions, not enthusiasm.',
  },
  {
    id: 'i-found-out',
    pattern: 'I (found out|discovered|realised) that',
    flag: 'Generic hedge before a specific claim.',
    prescription: 'State the claim directly. "Pearse\'s 1916 oration drew on Wolfe Tone\'s 1798 vocabulary" is firmer than "I found out that…".',
  },
  {
    id: 'overall',
    pattern: 'overall,? I',
    flag: 'Filler conjunction at sentence start.',
    prescription: 'Cut "overall,". Lead with the actual conclusion.',
  },
  {
    id: 'in-conclusion',
    pattern: '(in conclusion|to conclude|to sum up),? ',
    flag: 'Word-count padding.',
    prescription: 'Cut. The sentence after this phrase is your real conclusion — make it land.',
  },
  {
    id: 'good-experience',
    pattern: '(it was|was|has been) a (good|valuable|useful|positive) experience',
    flag: 'Vague positive reflection.',
    prescription: 'Name what specifically changed about how you research. "Next time I\'d start with the bibliography of a recent academic monograph" is concrete.',
  },
  {
    id: 'helped-me',
    pattern: '(this|the project|the research) helped me',
    flag: 'Generic benefit statement.',
    prescription: 'Name the specific skill that improved or the method you adopted. "Reading critical biographies side by side taught me to triangulate" is concrete.',
  },
];
