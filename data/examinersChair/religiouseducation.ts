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

// ─────────────── RE8 · A valid answer that isn’t in the scheme still scores ───────────────

const RE8: ScaleSession = {
  mode: 'scale',
  id: 're-alt-valid',
  subject: 'religious-education',
  level: 'common',
  title: 'Your answer isn’t in the scheme — and still tops the band',
  cue: 'Outline',
  question: 'A 20-mark answer is accurate, relevant and well-made — but the specific example it uses is NOT one of the bulleted “e.g.” exemplars printed under the question. The scheme’s General Introduction says the listed points “are not exhaustive and alternative valid answers are acceptable.” Where does it land?',
  questionNote:
    'Scenario authored for this exercise. The bulleted exemplars under each RE question are illustrative, not a checklist: the General Introduction states the points are “not exhaustive and alternative valid answers are acceptable” — a valid answer outside the list is marked on its merits.',
  scale: {
    name: 'Alternative valid answer /20',
    levels: [
      { id: 'fair', label: 'Fair (8–10)', annotation: 'F', marks: 9 },
      { id: 'good', label: 'Good (11–13)', annotation: 'G', marks: 12 },
      { id: 'vgood', label: 'Very Good (14–16)', annotation: 'VG', marks: 15 },
      { id: 'excellent', label: 'Excellent (17–20) — valid, though off-list', annotation: 'E', marks: 18 },
    ],
    notes: [
      'The scheme’s exemplars are illustrative only: “The descriptions, definitions and points in the scheme are not exhaustive and alternative valid answers are acceptable.”',
      'An accurate, relevant answer that never appears in the printed “e.g.” list is marked on its merits — it can reach Excellent.',
      'You are not being marked for matching the scheme’s wording; you are being marked against the question’s Marking Criteria.',
    ],
    cite: MS('p.2 (General Introduction — scheme “not exhaustive … alternative valid answers are acceptable”; band ranges p.4)'),
  },
  scripts: [
    {
      id: 're8-a',
      label: 'The answer',
      persona: 'Right answer, off the printed list',
      work: [
        'An accurate, relevant, well-organised answer that fully meets the question’s Marking Criteria.',
        'Its central example is a valid one — but it is not among the bulleted exemplars the scheme prints under the question.',
      ],
      keyLevelId: 'excellent',
      keyNote:
        'It reaches Excellent. The scheme’s bullet points are “not exhaustive,” so a valid answer that isn’t on the printed list is marked on its merits, not penalised for being off-script. Never abandon a correct, well-argued point just because it isn’t the “textbook” example — the examiner marks it against the Marking Criteria, not against a word-list.',
      embodies: {
        behaviour: 'Gives a valid answer absent from the scheme’s exemplars — accepted on merit, not capped for being off-list.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re8',
    rule: 'A valid answer off the scheme’s list still scores full band.',
    detail:
      'RE’s exemplars are “not exhaustive and alternative valid answers are acceptable.” You are marked against the question’s Marking Criteria, not for matching the printed wording — so back a correct, well-argued point even when it isn’t the textbook example.',
    cite: MS('p.2'),
  },
};

// ─────────────── RE9 · Relevance is its own descriptor row ───────────────

const RE9: ScaleSession = {
  mode: 'scale',
  id: 're-relevance',
  subject: 'religious-education',
  level: 'common',
  title: 'Padding drags the whole band down',
  cue: 'Outline',
  question: 'Relevance is one of the four descriptor rows scored on every RE answer — “completely & clearly relevant” at the top, sliding to “generally relevant”, “limited relevance”, “not relevant.” A candidate writes an accurate core but pads it out with a page of tangential material that doesn’t address the question. What does the padding do to the band?',
  questionNote:
    'Scenario authored for this exercise. “Relevance” is a distinct descriptor row on every RE marking grid — separate from Factual Accuracy — so off-topic padding is not simply ignored; it moves the answer down the Relevance row and lowers the single holistic band.',
  scale: {
    name: 'Relevance row /20',
    levels: [
      { id: 'fair', label: 'Fair (8–10)', annotation: 'F', marks: 9 },
      { id: 'good', label: 'Good (11–13) — “generally relevant”', annotation: 'G', marks: 12 },
      { id: 'vgood', label: 'Very Good (14–16)', annotation: 'VG', marks: 15 },
      { id: 'excellent', label: 'Excellent (17–20)', annotation: 'E', marks: 18 },
    ],
    notes: [
      'Every RE grid scores a “Relevance” row: completely & clearly relevant → clearly → generally → limited → little → not relevant.',
      'Tangential padding isn’t neutral — it makes the answer only “generally relevant,” which is a Good-band descriptor, not the “completely & clearly relevant” of the top bands.',
      'Because there’s one holistic band across four rows, a weakened Relevance row pulls the whole answer down — accuracy alone can’t hold the band up.',
    ],
    cite: MS('p.4 (Relevance descriptor row — “completely & clearly relevant” → “generally relevant” → “Not relevant”)'),
  },
  scripts: [
    {
      id: 're9-a',
      label: 'The answer',
      persona: 'Accurate core, buried in padding',
      work: [
        'An accurate, correct core that addresses the question.',
        'But a page of tangential material — related to the topic, not to the question asked — padded around it.',
      ],
      keyLevelId: 'good',
      keyNote:
        'The padding pulls it to Good. Its accurate core might have reached Very Good or Excellent, but the tangents make the answer only “generally relevant,” and Relevance is one of the four rows the single band is judged on — so the whole answer drops. Off-topic material never adds marks and can cost them. Cut the padding; keep every sentence pointed at the exact question.',
      embodies: {
        behaviour: 'Surrounds an accurate core with off-question padding, lowering the Relevance row and the whole band.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re9',
    rule: 'Relevance is scored — padding costs marks, never adds them.',
    detail:
      'RE grades a distinct “Relevance” row on every answer. Tangential material makes an answer only “generally relevant,” pulling the holistic band down even when the facts are right. Keep every sentence aimed at the exact question asked.',
    cite: MS('p.4'),
  },
};

// ─────────────── RE10 · Coursework Part A — a second source is required ───────────────

const RE10: ScaleSession = {
  mode: 'scale',
  id: 're-coursework-source',
  subject: 'religious-education',
  level: 'higher',
  title: 'One source can’t reach the top of the sources row',
  cue: 'Investigate (coursework)',
  question: 'The 40-mark Part A coursework summary is banded on, among other rows, a “Sources of information” descriptor that codes the SECOND source (SI) and reserves its top band for “substantial information” drawn from more than one source. A candidate writes a thorough, well-organised summary — but built entirely on ONE source. Where can it band on the sources row?',
  questionNote:
    'Scenario authored for this exercise. The Part A (Summary of the Investigation) grid scores a distinct “Sources of information” row whose examiner code, SI, marks a SECOND source; a summary resting on a single source cannot satisfy the top-band descriptor on that row.',
  scale: {
    name: 'Part A sources /40',
    levels: [
      { id: 'fair', label: 'Fair (16–21)', annotation: 'F', marks: 19 },
      { id: 'good', label: 'Good (22–27) — one source, well used', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'The Part A “Sources of information” row codes the second source SI and tops out at “substantial information” — which needs more than one source.',
      'A summary built on a single source, however thorough, meets the lower descriptors on this row; it cannot reach the “2nd source” top band.',
      'The coursework grid bands 40>34 / 33>28 / 27>22 / 21>16 / 15>0 — one source caps the sources row in the middle of that range.',
    ],
    cite: MS('p.35 (Part A — “Sources of information … 2nd source Code SI”; coursework band marks 40>34 … 15>0)'),
  },
  scripts: [
    {
      id: 're10-a',
      label: 'The summary',
      persona: 'Thorough, but single-source',
      work: [
        'A thorough, accurate, well-organised summary of the investigation.',
        'Every point is drawn from one source — no second source is used or referenced.',
      ],
      keyLevelId: 'good',
      keyNote:
        'On the sources row it bands at Good, not higher — the descriptor reserves its top band for “substantial information” with a second source (coded SI), and a single source, however well used, can’t meet it. Depth on one source doesn’t substitute for breadth across two. Bring in a second, contrasting source and show what it added to reach the top of that row.',
      embodies: {
        behaviour: 'Builds the Part A summary on a single source, capping the “Sources of information” row below its second-source top band.',
        cite: MS('p.35'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re10',
    rule: 'Part A needs a second source — one source caps the sources row.',
    detail:
      'The coursework Part A grid scores a “Sources of information” row that codes and rewards a SECOND source (SI). A summary resting on one source, however thorough, can’t reach the top of that row — use and reference more than one source.',
    cite: MS('p.35'),
  },
};

// ─────────────── RE11 · Coursework Part B — distinguish fact from opinion ───────────────

const RE11: ScaleSession = {
  mode: 'scale',
  id: 're-fact-opinion',
  subject: 'religious-education',
  level: 'higher',
  title: 'State opinion as fact and the reflection bands lower',
  cue: 'Reflect (coursework)',
  question: 'The 40-mark Part B reflection is banded partly on a “What questions arose?” row (coded Q) whose descriptor rewards “the ability to question the authority of different sources of information & distinguish between fact and opinion.” A candidate’s reflection is engaged and personal but presents its opinions as settled facts and never separates the two. Where can it band on that row?',
  questionNote:
    'Scenario authored for this exercise. The Part B “What questions arose?” descriptor (code Q) explicitly rewards distinguishing fact from opinion; a reflection that treats opinion as fact meets the lower descriptors on that row even when it is otherwise engaged.',
  scale: {
    name: 'Part B fact/opinion /40',
    levels: [
      { id: 'fair', label: 'Fair (16–21)', annotation: 'F', marks: 19 },
      { id: 'good', label: 'Good (22–27) — engaged, but no fact/opinion split', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'The Part B “What questions arose?” row (Q) rewards “the ability to question the authority of different sources … & distinguish between fact and opinion.”',
      'A reflection that states its opinions as facts never performs that distinction, so it meets only the lower descriptors on this row.',
      'Personal engagement can’t substitute for the skill the row names — the higher bands need fact and opinion visibly separated.',
    ],
    cite: MS('p.36 (Part B — “What questions arose?” Q row: “distinguish between fact and opinion”)'),
  },
  scripts: [
    {
      id: 're11-a',
      label: 'The reflection',
      persona: 'Heartfelt, but opinion dressed as fact',
      work: [
        'An engaged, personal reflection on the coursework title.',
        'Presents its own opinions as settled facts and never separates what is fact from what is opinion.',
      ],
      keyLevelId: 'good',
      keyNote:
        'On the questions row it bands at Good — the descriptor rewards distinguishing fact from opinion, and this reflection does the opposite, stating opinion as fact. Feeling strongly about the title can’t stand in for the skill the row names. Signal explicitly which claims are established fact and which are your view — that visible distinction is what opens the top bands here.',
      embodies: {
        behaviour: 'Presents opinion as fact in the Part B reflection, missing the “distinguish fact from opinion” descriptor.',
        cite: MS('p.36'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re11',
    rule: 'Separate fact from opinion — the Part B Q row scores it.',
    detail:
      'The coursework Part B “What questions arose?” row rewards questioning sources and distinguishing fact from opinion. Stating opinion as fact caps that row — mark clearly which claims are established and which are your own view.',
    cite: MS('p.36'),
  },
};

// ─────────────── RE12 · Answering through Irish — the bonus tapers ───────────────

const RE12: ScaleSession = {
  mode: 'scale',
  id: 're-irish-bonus',
  subject: 'religious-education',
  level: 'common',
  title: 'The Irish-language bonus isn’t a flat 10%',
  cue: 'Trí Ghaeilge',
  question: 'A candidate answers the RE paper through Irish and scores a raw 300 out of 320. The scheme awards a bonus for answering as Gaeilge — the normal rate is 10%, but only up to 75% of the marks (240/320); above that a taper table applies. How much bonus does a raw 300 earn?',
  questionNote:
    'Scenario authored for this exercise. The bonus mechanism is the real SEC rule: 10% at the normal rate up to 75% of the total, then the published taper table (“Tábla 320 @ 10%”) reduces the bonus as the base mark rises — so a very high raw mark earns far less than a flat 10% would suggest.',
  scale: {
    name: 'Irish bonus on 300/320',
    levels: [
      { id: 'none', label: 'No bonus — “over 75%, so nothing”', annotation: '+0', marks: 0 },
      { id: 'actual', label: 'Tapered: the 297–300 band → +6', annotation: '+6', marks: 6 },
      { id: 'mid', label: '+15 (that’s the 267–270 band)', annotation: '+15', marks: 15 },
      { id: 'flat', label: 'Flat 10% of the score → +30', annotation: '+30', marks: 30 },
    ],
    notes: [
      'The bonus is 10% at the normal rate only up to 75% of the total (240 of 320); above that the taper table applies.',
      'On the taper table a base of 297–300 earns +6, and a base of 317–320 earns +0 — the closer to full marks, the smaller the bonus.',
      'A raw 300 therefore gains +6, not the +30 a flat 10% would imply; bonus marks are rounded down.',
    ],
    cite: MS('p.32 (“Tábla 320 @ 10%” taper: base 297–300 → +6; base 317–320 → +0; normal rate up to 75%)'),
  },
  scripts: [
    {
      id: 're12-a',
      label: 'The script',
      persona: 'Top marks, answered as Gaeilge',
      work: [
        'Answered the whole paper through Irish.',
        'Scored a raw 300 out of 320 before any language bonus.',
      ],
      keyLevelId: 'actual',
      keyNote:
        'It earns +6, not +30. The 10% rate applies only up to 75% of the marks; above that the taper table takes over, and a base of 297–300 sits at +6 (a perfect 320 would earn +0). The bonus rewards reaching the 75% threshold, not exceeding it — so a strong candidate answering through Irish shouldn’t bank on a flat tenth of their whole score.',
      embodies: {
        behaviour: 'A high raw mark answered through Irish, where the taper table gives far less than a flat 10%.',
        cite: MS('p.32'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re12',
    rule: 'The Irish bonus tapers above 75% — it isn’t a flat 10%.',
    detail:
      'RE gives 10% for answering through Irish only up to 75% of the total; above that a taper table shrinks the bonus (base 297–300 → +6; 317–320 → +0). Expect the reward for the marks up to 75%, not a flat tenth of a top score.',
    cite: MS('p.32'),
  },
};

// ─────────────── RE13 · Band-not-count — length isn’t a lever ───────────────

const RE13: ScaleSession = {
  mode: 'scale',
  id: 're-band-not-count',
  subject: 'religious-education',
  level: 'common',
  title: 'Writing more doesn’t raise the band',
  cue: 'Discuss',
  question: 'RE marks each answer as one holistic band, not by adding up points — “the mark for the candidate’s answer is awarded within a range from excellent … to no grade.” A candidate writes three pages of accurate, generally-relevant, competently-skilled material, believing more writing means more marks. If the quality never rises above the Good descriptors, what does the extra length buy?',
  questionNote:
    'Scenario authored for this exercise. RE has no point tally: the whole answer gets a single band judged on quality (marking criteria, relevance, skill, accuracy). Adding more material of the same quality cannot move the band; only higher-quality material can.',
  scale: {
    name: 'Band-not-count /20',
    levels: [
      { id: 'fair', label: 'Fair (8–10)', annotation: 'F', marks: 9 },
      { id: 'good', label: 'Good (11–13) — long, but Good-quality throughout', annotation: 'G', marks: 12 },
      { id: 'vgood', label: 'Very Good (14–16)', annotation: 'VG', marks: 15 },
      { id: 'excellent', label: 'Excellent (17–20)', annotation: 'E', marks: 18 },
    ],
    notes: [
      'There is no adding-up of points in RE: the whole answer is placed in one band on its quality across four descriptor rows.',
      'Three pages of Good-quality material band exactly where one focused page of Good-quality material bands — length is not a marking dimension.',
      'To climb a band you need sharper relevance, better use of the skill, or more precise accuracy — not more of the same.',
    ],
    cite: MS('p.2 (band-not-count — mark “awarded within a range from excellent … to no grade”; one band per answer)'),
  },
  scripts: [
    {
      id: 're13-a',
      label: 'The answer',
      persona: 'Long, and thinks length is marks',
      work: [
        'Three pages of accurate, generally-relevant, competently-argued material.',
        'The quality never sharpens beyond the Good descriptors — it’s just more of the same.',
      ],
      keyLevelId: 'good',
      keyNote:
        'The extra length buys nothing — it bands at Good, exactly where one tight Good-quality page would. RE awards one holistic band on quality, with no point tally to accumulate, so volume can’t lift the band. What moves it is a jump in quality: crisper relevance, a fuller performance of the command skill, cleaner accuracy. Write less, but better.',
      embodies: {
        behaviour: 'Pads to great length at one quality level, expecting volume to raise a band that only rises on quality.',
        cite: MS('p.2'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re13',
    rule: 'One band on quality — length doesn’t accumulate marks.',
    detail:
      'RE bands the whole answer on quality with no point tally, so writing more at the same quality can’t raise the band. Climb by sharpening relevance, skill and accuracy — not by adding length.',
    cite: MS('p.2'),
  },
};

// ─────────────── RE14 · Make the Marking Criteria evident ───────────────

const RE14: ScaleSession = {
  mode: 'scale',
  id: 're-mc-evident',
  subject: 'religious-education',
  level: 'common',
  title: 'If the examiner can’t find your point, it isn’t there',
  cue: 'Outline',
  question: 'The examiner codes “MC” in the margin at the first place the answer clearly meets the question’s Marking Criteria — and codes “MC X” (no evidence) if it never does. A candidate knows the required point but writes around it, only ever implying it, never stating it plainly. How does that read on the grid?',
  questionNote:
    'Scenario authored for this exercise. The MC / MC X annotation is the mechanical heart of RE marking: the examiner marks where the Marking Criteria is FIRST evident; an answer that only implies the required point gives the examiner no clear MC and bands low on Evidence of MC.',
  scale: {
    name: 'MC evident /20',
    levels: [
      { id: 'poor', label: 'Poor (0–4)', annotation: 'P', marks: 3 },
      { id: 'weak', label: 'Weak (5–7) — criteria only implied', annotation: 'W', marks: 6 },
      { id: 'fair', label: 'Fair (8–10)', annotation: 'F', marks: 9 },
      { id: 'good', label: 'Good (11–13)', annotation: 'G', marks: 12 },
    ],
    notes: [
      'The examiner codes MC “where the Marking Criteria is first evident in the candidate’s answer,” and MC X where there is “no evidence” of it.',
      'An answer that only implies the required point never gives the examiner a clear MC, so it bands low on the Evidence-of-MC row.',
      'Writing around a point you actually know throws away marks — state the required point explicitly and early so it is unmistakably evident.',
    ],
    cite: MS('p.4 (“Code MC … where the Marking Criteria is first evident”); MC X “No evidence of … Marking Criteria” p.3'),
  },
  scripts: [
    {
      id: 're14-a',
      label: 'The answer',
      persona: 'Knows it, but never says it',
      work: [
        'Clearly knows the required point — the surrounding material circles it.',
        'But never states it plainly; the Marking Criteria is left implicit throughout.',
      ],
      keyLevelId: 'weak',
      keyNote:
        'It bands at Weak, because the examiner never finds a clear MC to code — the required point is implied, not stated, so it reads as little evidence of the Marking Criteria. Knowing the answer isn’t the same as showing it. Put the required point in a plain, explicit sentence, early — don’t make the examiner infer it from material that only gestures at it.',
      embodies: {
        behaviour: 'Leaves the required point implicit, so the examiner finds no clear MC and the Evidence-of-MC row bands low.',
        cite: MS('p.4'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re14',
    rule: 'State the required point explicitly — implied isn’t evident.',
    detail:
      'The examiner codes MC at the first clear evidence of the Marking Criteria and MC X where there is none. An answer that only implies its point gives no clear MC and bands low — say the required point plainly and early.',
    cite: MS('p.4'),
  },
};

// ─────────────── RE15 · Coursework Part A — back your conclusions ───────────────

const RE15: ScaleSession = {
  mode: 'scale',
  id: 're-coursework-evidence',
  subject: 'religious-education',
  level: 'higher',
  title: 'A conclusion with nothing behind it',
  cue: 'Conclude (coursework)',
  question: 'The 40-mark Part A summary is banded on, among other rows, a “Supporting evidence for conclusions drawn” descriptor whose top band needs “substantial supporting evidence.” A candidate states clear, confident conclusions — but offers no evidence from the investigation to support them. Where can it band on that row?',
  questionNote:
    'Scenario authored for this exercise. The Part A grid scores a distinct “Supporting evidence for conclusions drawn” row; conclusions asserted without evidence from the investigation meet only the lower descriptors on that row, however well-phrased.',
  scale: {
    name: 'Part A evidence /40',
    levels: [
      { id: 'fair', label: 'Fair (16–21)', annotation: 'F', marks: 19 },
      { id: 'good', label: 'Good (22–27) — conclusions asserted, not evidenced', annotation: 'G', marks: 25 },
      { id: 'vgood', label: 'Very Good (28–33)', annotation: 'VG', marks: 31 },
      { id: 'excellent', label: 'Excellent (34–40)', annotation: 'E', marks: 37 },
    ],
    notes: [
      'The Part A grid scores a “Supporting evidence for conclusions drawn” row, topping out at “substantial supporting evidence for conclusions.”',
      'A confident conclusion with no evidence behind it meets only the lower descriptors on this row — assertion is not evidence.',
      'The coursework bands run 40>34 / 33>28 / 27>22 / 21>16 / 15>0 — unsupported conclusions cap this row in the middle of that range.',
    ],
    cite: MS('p.35 (Part A — “Supporting evidence for conclusions drawn” descriptor row; coursework band marks 40>34 … 15>0)'),
  },
  scripts: [
    {
      id: 're15-a',
      label: 'The summary',
      persona: 'Confident conclusions, no backing',
      work: [
        'States clear, confident conclusions to the investigation.',
        'Offers no evidence from the investigation to support any of them.',
      ],
      keyLevelId: 'good',
      keyNote:
        'On the evidence row it bands at Good, not higher — the descriptor’s top band needs “substantial supporting evidence for conclusions,” and a bare assertion, however confident, doesn’t supply it. A conclusion is only as strong as what stands behind it. Tie each conclusion back to specific findings from the investigation to reach the top of this row.',
      embodies: {
        behaviour: 'Asserts conclusions without supporting evidence, capping the Part A “supporting evidence” row.',
        cite: MS('p.35'),
      },
    },
  ],
  takeaway: {
    id: 'codex-re15',
    rule: 'Back every conclusion — assertion isn’t evidence.',
    detail:
      'The coursework Part A grid scores a “Supporting evidence for conclusions drawn” row. Confident conclusions with nothing behind them cap that row — tie each conclusion to specific evidence from your investigation.',
    cite: MS('p.35'),
  },
};

export const RE_CHAIR: ChairSubject = {
  id: 'religious-education',
  label: 'Religious Education',
  tagline: 'Holistic bands — do the command word, keep it accurate, and don’t undo your own answer.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [RE1, RE2, RE3, RE4, RE5, RE6, RE7, RE8, RE9, RE10, RE11, RE12, RE13, RE14, RE15],
  sources: [
    { label: 'SEC LC Religious Education HL marking scheme 2025 (examiner-reports/religious-education/2025-marking-scheme)' },
    { label: 'SEC LC Religious Education OL marking scheme 2025 (examiner-reports/religious-education/2025-ol-marking-scheme)' },
  ],
  coverageNote:
    'The holistic six-band system applies at both levels, as do the General-Introduction rules shown as “all levels” (self-contradiction voids the mark; a duplicate answer is bracketed and ignored; a valid answer off the scheme’s exemplar list still scores; Relevance is its own descriptor row; the whole answer gets one band, so length isn’t a lever; the examiner codes MC where the Marking Criteria is first evident; the Irish-language bonus tapers above 75%). The descriptive cap is Higher-specific — at Ordinary Level the commands are lower-order and there is no cap, so a thorough description reaches the top band (verified against the 2025 OL scheme). The four coursework sessions (identify AND balance perspectives; a second source; distinguish fact from opinion; back conclusions with evidence) use the Higher-Level Part A/B grids.',
};
