/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Religious Education (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (holistic six-band marking, and the "descriptive answer to a
 * higher-order command is capped at the top of Fair" rule) is the real SEC
 * system, cited to:
 *  - SEC LC Religious Education HL marking scheme 2025 —
 *    examiner-reports/religious-education/2025-marking-scheme.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession } from './types';

const MS = (p: string) => ({ label: `SEC Religious Education HL marking scheme 2025, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Religious Education OL marking scheme 2025, ${p}` });

// ─────────────── RE1 · Do the command word ───────────────

const RE1: ScaleSession = {
  mode: 'scale',
  id: 're-command',
  subject: 'religious-education',
  level: 'higher',
  title: 'Describe when it says assess',
  cue: 'Assess',
  question: 'A 40-mark question says “Assess”. The candidate writes a full, accurate, well-organised description of the topic — but never actually assesses anything. The scheme caps a descriptive answer to a higher-order command at the top of the Fair band (Max 21 on a 40-mark question). Where does it land?',
  questionNote:
    'Scenario authored for this exercise. RE marks holistically in six bands; a descriptive answer to a higher-order command word (Assess/Compare/Discuss) is ceilinged at the top of the Fair band.',
  scale: {
    name: 'Descriptive cap · /40',
    levels: [
      { id: 'fair', label: 'Max Fair (21) — descriptive', annotation: 'F', marks: 21 },
      { id: 'good', label: 'Good (22–27)', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'RE marks each answer holistically into one band, not by points.',
      'A description given for a higher-order command (Assess/Compare/Discuss) is capped at the top of Fair — Max 21 on a 40-mark question.',
      'Doing the command word is what unlocks the bands above Fair.',
    ],
    cite: MS('p.18 (descriptive-answer cap; band ranges p.6)'),
  },
  scripts: [
    {
      id: 're1-a',
      label: 'The answer',
      persona: 'Describes instead of assessing',
      work: [
        'Full, accurate, well-organised description of the topic.',
        'Never weighs, judges or assesses — the command word “Assess” isn’t performed.',
      ],
      keyLevelId: 'fair',
      keyNote:
        'Capped at 21 of 40 — the top of Fair — because the answer describes where the command asked it to assess. Accuracy and coverage can’t lift it past that cap; only doing the command word can. One evaluative thread (strengths, weaknesses, a judgement) would unlock the higher bands.',
      embodies: {
        behaviour: 'Describes rather than performing the higher-order command — the descriptive cap applies.',
        cite: MS('p.18'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re1',
    rule: 'Do the command word, or you’re capped at Fair.',
    detail:
      'RE ceilings a descriptive answer to “Assess/Compare/Discuss” at the top of the Fair band, regardless of accuracy. Perform the command — weigh, judge, compare — to reach the bands above.',
    cite: MS('p.18'),
  },
};

// ─────────────── RE2 · Holistic bands ───────────────

const RE2: ScaleSession = {
  mode: 'scale',
  id: 're-holistic',
  subject: 'religious-education',
  level: 'higher',
  title: 'One band for the whole answer',
  cue: 'Discuss',
  question: 'RE marks each answer as one holistic band judged on four things at once: evidence of the marking criteria, relevance, use of the skill, and factual accuracy. An answer is insightful and relevant — but contains a couple of clear factual errors. How does accuracy affect the band?',
  questionNote:
    'Scenario authored for this exercise. Each RE answer gets one holistic band; factual accuracy is one of the four descriptor dimensions, so errors lower the whole band rather than being a line-item deduction.',
  scale: {
    name: 'Holistic band /20',
    levels: [
      { id: 'good', label: 'Good (11–13)', annotation: 'G', marks: 12 },
      { id: 'vgood', label: 'Very Good (14–16)', annotation: 'VG', marks: 15 },
      { id: 'excellent', label: 'Excellent (17–20)', annotation: 'E', marks: 18 },
    ],
    notes: [
      'The answer is placed in one band on four dimensions at once: marking criteria, relevance, skill, factual accuracy.',
      'Accuracy isn’t a separate subtraction — it’s one of the things that sets the band.',
      'Clear factual errors pull an otherwise strong answer down a band.',
    ],
    cite: MS('p.2, p.4 (four-dimension holistic banding)'),
  },
  scripts: [
    {
      id: 're2-a',
      label: 'The answer',
      persona: 'Insightful, but with errors',
      work: [
        'Relevant and insightful discussion.',
        'But a couple of clear factual errors (wrong text, wrong figure).',
      ],
      keyLevelId: 'vgood',
      keyNote:
        'It settles a band lower than its insight alone would earn — accuracy is one of the four things the band weighs, so errors drag the whole judgement down rather than costing a fixed number of marks. Getting your facts right protects the band your analysis has earned. Precision and insight both set the ceiling.',
      embodies: {
        behaviour: 'Strong analysis undercut by factual errors, which lower the holistic band.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re2',
    rule: 'Accuracy sets the band, not a deduction.',
    detail:
      'RE judges each answer holistically on marking criteria, relevance, skill and accuracy together — factual errors lower the whole band rather than costing set marks. Keep your facts precise to protect the band your insight earns.',
    cite: MS('p.2'),
  },
};

// ─────────────── RE3 · OL — a strong description reaches the top ───────────────

const RE3: ScaleSession = {
  mode: 'scale',
  id: 're-ol-describe',
  subject: 'religious-education',
  level: 'ordinary',
  title: 'At OL, describing is enough',
  cue: 'Describe (OL)',
  question: 'At Higher Level, a purely descriptive answer to a higher-order command is capped at the top of Fair. At Ordinary Level there is NO such cap — the commands are Outline/Describe/Give an account, and a full, accurate, relevant description can reach the top band. A candidate writes exactly that. Where does it land?',
  questionNote:
    'Scenario authored for this exercise. Unlike HL, the OL scheme contains no descriptive-answer cap — its commands are lower-order (Describe/Outline), and a strong description is a top-band answer.',
  scale: {
    name: 'OL description · /40 bands',
    levels: [
      { id: 'fair', label: 'Fair (16–21)', annotation: 'F', marks: 19 },
      { id: 'good', label: 'Good (22–27)', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'OL centres on lower-order skills (Outline, Describe, Give an account); even where an OL question uses a higher-order stem, the scheme does not cap a description at Fair.',
      'There is no HL-style descriptive cap at OL: a description is not ceilinged at Fair for “not evaluating.” Where an OL note applies a “Max”, it caps a partial answer that omits a required element — not a description.',
      'A full, accurate, relevant description can reach the Excellent band.',
    ],
    cite: MSOL('p.5, p.20 (no descriptive cap at OL)'),
  },
  scripts: [
    {
      id: 're3-a',
      label: 'The answer',
      persona: 'Full, accurate description',
      work: [
        'A complete, accurate, relevant description of the topic.',
        'The command was “Describe” — and it describes thoroughly.',
      ],
      keyLevelId: 'excellent',
      keyNote:
        'It can reach the Excellent band — at OL there’s no descriptive cap, because the command asked you to describe, and you did it fully and accurately. This is the mirror image of Higher Level, where the same description would be capped at Fair. At OL, do exactly what the command word asks, thoroughly and accurately, and the top band is open.',
      embodies: {
        behaviour: 'Answers an OL “describe” command with a full accurate description — top band, no cap.',
        cite: MSOL('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re3',
    rule: 'At OL, a thorough accurate description is a top answer.',
    detail:
      'Ordinary Level RE has no descriptive cap — its commands are Describe/Outline/Give an account, and a full, accurate, relevant description can reach the Excellent band. Do exactly what the command asks, thoroughly and accurately.',
    cite: MSOL('p.5'),
  },
};

// ─────────────── RE4 · “Two” means two independent scores ───────────────

const RE4: ScaleSession = {
  mode: 'scale',
  id: 're-two-items',
  subject: 'religious-education',
  level: 'higher',
  title: 'When it says “two”, one brilliant answer isn’t enough',
  cue: 'Outline two',
  question: 'A 20-mark question says “Outline two images of God.” It’s marked as two separate 10-mark scores — the examiner codes “MC x 2” and bands each image independently. A candidate writes one flawless, Excellent account of God as Shepherd, and never gives a second image. Where does the whole answer land out of 20?',
  questionNote:
    'Scenario authored for this exercise. A “two-item” RE question (e.g. “Outline two images of God”, 10M × 2) is banded twice — the scheme instructs the examiner to “Code MC x 2” and mark each item on its own 10-mark grid; a missing item is coded MC X (no evidence).',
  scale: {
    name: 'Two-item split · /20',
    levels: [
      { id: 'half', label: 'One image only — Max 10 (second is MC X)', annotation: 'MC×1', marks: 10 },
      { id: 'onethin', label: 'One strong + one thin (≈13)', annotation: 'E+W', marks: 13 },
      { id: 'twosolid', label: 'Two solid images (≈16)', annotation: 'G+G', marks: 16 },
      { id: 'twotop', label: 'Two excellent images (20)', annotation: 'E+E', marks: 20 },
    ],
    notes: [
      'A “two-item” question is banded twice: the examiner codes “MC x 2” and marks each image on its own 10-mark grid (10–8 / 7 / 6–5 / 4 / 3–2 / 1–0).',
      'The two scores are independent — extra quality on one image cannot compensate for a missing one; a missing item is coded MC X (no evidence) and scores nothing.',
      'Doing one of two perfectly caps the whole answer at Max 10 — half the marks for half the task.',
    ],
    cite: MS('p.8 (Q2(b)(i) “Outline two images of God”, 10M × 2, “Code MC x 2”; MC X annotation p.3)'),
  },
  scripts: [
    {
      id: 're4-a',
      label: 'The answer',
      persona: 'One image, done perfectly',
      work: [
        'A flawless, accurate, Excellent-band account of God as Shepherd.',
        'No second image of God is ever given — the second half of the question is left blank.',
      ],
      keyLevelId: 'half',
      keyNote:
        'Capped at 10 of 20. The command asked for two images, so the examiner codes MC x 2 and bands each independently: image one earns a full Excellent 10, but image two is coded MC X — no evidence, no marks. The two scores don’t pool, so a perfect first image can’t cover a missing second. Half the task, half the marks. Two shorter, solid images would beat one flawless one here.',
      embodies: {
        behaviour: 'Answers only one of two required items — the second is coded MC X and the whole answer caps at half the marks.',
        cite: MS('p.8'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re4',
    rule: 'When it says “two”, give two — the scores don’t pool.',
    detail:
      'RE bands a “two-item” question twice (“Code MC x 2”), marking each item on its own grid; a missing item is coded MC X and scores zero. One flawless answer can’t make up for a missing second — cover every item the command lists.',
    cite: MS('p.8'),
  },
};

// ─────────────── RE5 · Contradict yourself and the mark is voided ───────────────

const RE5: ScaleSession = {
  mode: 'scale',
  id: 're-contradiction',
  subject: 'religious-education',
  level: 'common',
  title: 'Contradict yourself and the mark is voided',
  cue: 'Explain',
  question: 'A 20-mark answer states a term correctly and clearly — enough, on its own, to reach the Good band. But a later sentence flatly contradicts that same term. The scheme’s General Introduction says a word “must be correctly used in context and not contradicted” — where there is contradiction, “the marks may not be awarded.” Where does the answer land?',
  questionNote:
    'Scenario authored for this exercise. This is not the general “errors lower the band” rule (that is a separate session): here the candidate cancels its OWN correct point by contradicting it, and the scheme voids the credit for the contradicted material rather than just softening the band.',
  scale: {
    name: 'Self-contradiction /20',
    levels: [
      { id: 'poor', label: 'Poor (0–4)', annotation: 'P', marks: 3 },
      { id: 'weak', label: 'Weak (5–7)', annotation: 'W', marks: 6 },
      { id: 'fair', label: 'Fair (8–10)', annotation: 'F', marks: 9 },
      { id: 'good', label: 'Good (11–13)', annotation: 'G', marks: 12 },
    ],
    notes: [
      'A word, expression or phrase “must be correctly used in context and not contradicted” — where there is contradiction, “the marks may not be awarded.” (General Introduction, stated identically in the HL and OL schemes.)',
      'This is not a fixed deduction and not merely a band softened for an error: the credit for the contradicted point is actively voided, so the material you were relying on for the band no longer counts.',
      'A self-contradiction also registers on the Factual Accuracy descriptor row, so it pulls the surviving answer down as well.',
    ],
    cite: MS('p.2 (General Introduction — contradiction/incorrect use voids the mark)'),
  },
  scripts: [
    {
      id: 're5-a',
      label: 'The answer',
      persona: 'States it right, then unsays it',
      work: [
        'States the key term correctly and clearly — on its own, Good-band material.',
        'A later sentence flatly contradicts the same term, using it incorrectly in context.',
      ],
      keyLevelId: 'weak',
      keyNote:
        'It had enough correct material to reach Good — but the contradiction means “the marks may not be awarded” for that central point, so the credit it was resting on is voided, not merely trimmed. The contradiction also counts against Factual Accuracy, so what survives lands at Weak. You cancelled your own best point. Say it once, correctly, and leave it standing — don’t undo it two sentences later.',
      embodies: {
        behaviour: 'Correctly states a point then contradicts it, so the scheme voids the credit for the contradicted material.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re5',
    rule: 'Contradict your own point and its marks are voided.',
    detail:
      'RE requires terms to be “correctly used in context and not contradicted”; where a candidate contradicts itself, “the marks may not be awarded” for that point. This is a voiding, not a soft deduction — make your point once, correctly, and don’t undermine it later in the answer.',
    cite: MS('p.2'),
  },
};

// ─────────────── RE6 · Answering twice earns it once ───────────────

const RE6: ScaleSession = {
  mode: 'scale',
  id: 're-duplicate',
  subject: 'religious-education',
  level: 'common',
  title: 'Answer it twice and only the first counts',
  cue: 'Outline',
  question: 'A candidate answers a 20-mark question early in the booklet — a thin, Fair-band effort. Later, with time to spare, they re-answer the same question far more fully, hoping the better version will be marked instead. The examiner brackets the second attempt “[ … ]” as a duplicate “for which marks are already awarded” and ignores it. What does the candidate score?',
  questionNote:
    'Scenario authored for this exercise. The online-marking annotation table defines “[ … ]” as the beginning/end of a duplicate answer to a question for which marks are already awarded — RE’s anti-double-credit rule. The FIRST answer marked is the one that stands; a fuller re-write is discarded.',
  scale: {
    name: 'Duplicate answer /20',
    levels: [
      { id: 'weak', label: 'Weak (5–7)', annotation: 'W', marks: 6 },
      { id: 'fair', label: 'Fair — first answer (8–10)', annotation: 'F', marks: 9 },
      { id: 'good', label: 'Good (11–13)', annotation: 'G', marks: 12 },
      { id: 'vgood', label: 'Very Good — the ignored re-write (14–16)', annotation: 'VG', marks: 15 },
    ],
    notes: [
      'The examiner brackets a second answer to an already-marked question — “[ … ] Beginning … End of duplicate answer to a question for which marks are already awarded” — and awards it nothing.',
      'The mark is fixed by the first answer the examiner marks, not by the candidate’s best attempt.',
      'A fuller re-write of the same question cannot replace or top up the first — it is discarded, however good it is.',
    ],
    cite: MS('p.3 (online annotation “[ … ] duplicate answer to a question for which marks are already awarded”)'),
  },
  scripts: [
    {
      id: 're6-a',
      label: 'The answer',
      persona: 'Re-answers hoping the better one counts',
      work: [
        'First attempt: a thin, Fair-band outline early in the booklet.',
        'Second attempt: the same question re-answered far more fully later on.',
        'The examiner brackets the second as a duplicate and marks only the first.',
      ],
      keyLevelId: 'fair',
      keyNote:
        'The candidate is stuck with the first answer’s Fair band. The polished Very-Good re-write they were counting on is bracketed “[ … ]” as a duplicate and earns nothing — marks are already awarded on the first. Redoing a question you’ve answered doesn’t upgrade it; it just burns time. If you want the fuller answer to count, cross out the first cleanly and write one answer — or get it right the first time.',
      embodies: {
        behaviour: 'Re-answers an already-answered question; the duplicate is bracketed and ignored, so only the weaker first answer scores.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re6',
    rule: 'Answer each question once — the second attempt is discarded.',
    detail:
      'RE brackets a second answer to an already-marked question (“[ … ] duplicate answer … for which marks are already awarded”) and scores it zero. The first answer marked is the one that stands, however much better the re-write is — so commit to one answer per question.',
    cite: MS('p.3'),
  },
};

// ─────────────── RE7 · Coursework — identify AND balance perspectives ───────────────

const RE7: ScaleSession = {
  mode: 'scale',
  id: 're-coursework-balance',
  subject: 'religious-education',
  level: 'higher',
  title: 'A reflection that balances two views, not one',
  cue: 'Reflect (coursework)',
  question: 'The 40-mark Part B coursework reflection is banded on, among other rows, the “different perspectives” descriptor. The top bands require “identification AND balancing different perspectives.” A candidate’s reflection identifies one viewpoint vividly and personally — but never sets a second viewpoint against it. Where can that reflection band on the perspectives dimension?',
  questionNote:
    'Scenario authored for this exercise. The Part B (Personal Reflection) descriptor grid bands the “What different perspectives were encountered?” row: Excellent = “SUBSTANTIAL IDENTIFICATION AND BALANCING DIFFERENT PERSPECTIVES”, down to lower bands. Identifying one view without balancing it against another cannot satisfy the top-band descriptor.',
  scale: {
    name: 'Part B perspectives /40',
    levels: [
      { id: 'fair', label: 'Fair (16–21)', annotation: 'F', marks: 19 },
      { id: 'good', label: 'Good (22–27) — identifies, doesn’t balance', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'The Part B perspectives row reads “IDENTIFICATION AND BALANCING DIFFERENT PERSPECTIVES” at Excellent and Very Good — both verbs are required for the top bands.',
      'A reflection that identifies one perspective but never balances it against another meets only the “identification” half, so on this row it sits below the balancing bands.',
      'Reporting a single viewpoint is a mid-band ceiling on the perspectives dimension — the higher bands need a second view weighed against the first.',
    ],
    cite: MS('p.36 (Part B descriptor — “identification AND balancing different perspectives”; band marks 40>34 … 15>0)'),
  },
  scripts: [
    {
      id: 're7-a',
      label: 'The reflection',
      persona: 'One viewpoint, deeply felt',
      work: [
        'Identifies one perspective on the title vividly and with genuine personal engagement.',
        'Never sets a second, contrasting viewpoint against it — nothing is balanced or weighed.',
      ],
      keyLevelId: 'good',
      keyNote:
        'It bands at Good on the perspectives row, not higher — the Excellent and Very Good descriptors both demand “identification AND balancing different perspectives,” and a single viewpoint, however heartfelt, only does the identifying. Name a second perspective and weigh it against the first — that balancing is what opens the top bands. Depth on one view can’t substitute for contrast between two.',
      embodies: {
        behaviour: 'Identifies one perspective without balancing it against another — meets only half the top-band descriptor.',
        cite: MS('p.36'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re7',
    rule: 'Identify AND balance — one viewpoint caps the reflection.',
    detail:
      'The Part B coursework reflection reserves its top bands for “identification AND balancing different perspectives.” A single viewpoint, however deeply felt, meets only half the descriptor — name a second perspective and weigh it against the first to reach Very Good and Excellent.',
    cite: MS('p.36'),
  },
};

export const RE_CHAIR: ChairSubject = {
  id: 'religious-education',
  label: 'Religious Education',
  tagline: 'Holistic bands — do the command word, keep it accurate, and don’t undo your own answer.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [RE1, RE2, RE3, RE4, RE5, RE6, RE7],
  sources: [
    { label: 'SEC LC Religious Education HL marking scheme 2025 (examiner-reports/religious-education/2025-marking-scheme)' },
    { label: 'SEC LC Religious Education OL marking scheme 2025 (examiner-reports/religious-education/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The holistic six-band system applies at both levels, as do the General-Introduction rules shown as “all levels” (self-contradiction voids the mark; a duplicate answer is bracketed and ignored). The descriptive cap is Higher-specific — at Ordinary Level the commands are lower-order and there is no cap, so a thorough description reaches the top band (verified against the 2025 OL scheme). The coursework “identify AND balance perspectives” session uses the Higher-Level Part B grid.',
};
