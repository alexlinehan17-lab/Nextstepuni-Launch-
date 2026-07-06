/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Art (Visual Studies written paper, HL) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * marking grammar (descriptor-band marking; the four independent Section B/C
 * strands with Subject Knowledge rewarding analysis over recall; recognised
 * examples as a separable strand; Section A answers anchored to the given
 * headings) is the real SEC system, cited to:
 *  - SEC LC Art HL "Visual Studies" marking scheme 2024 (revised specification) —
 *    examiner-reports/art/2024-visual-studies-marking-scheme.*
 * This is the CURRENT spec (first examined 2023/24); the pre-2022 "History &
 * Appreciation" paper was marked differently (see the 2019 scheme in the same
 * folder). Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Art HL Visual Studies marking scheme 2024, ${p}` });

const bands = (marks: number[], labels: string[]): ScaleLevel[] =>
  marks.map((m, i) => ({ id: `b${i}`, label: labels[i], annotation: labels[i][0], marks: m }));

// ─────────────── ART1 · Analysis beats recall ───────────────

const ART1: ScaleSession = {
  mode: 'scale',
  id: 'art-analysis',
  subject: 'art',
  level: 'common',
  title: 'Analyse, don’t just recall',
  cue: 'Section B/C essay',
  question: 'The Subject Knowledge strand of a Section B/C answer is worth 20 marks, scored in Low/Moderate/High descriptor bands. A candidate recalls a large amount of accurate information about the artist and works — but never analyses or evaluates it. The High band demands “critical thinking to analyse and evaluate”. Which band applies?',
  questionNote:
    'Scenario authored for this exercise. Visual Studies is marked by descriptor bands; the 20-mark Subject Knowledge strand reserves its High band for critical analysis and evaluation, not recall.',
  scale: {
    name: 'Subject Knowledge · /20 bands',
    levels: bands([8, 14, 18], ['Low', 'Moderate — recall only', 'High — analysis']),
    notes: [
      'Marked in Low / Moderate / High descriptor bands.',
      'High band: “critical thinking to analyse and evaluate their knowledge”.',
      'Accurate recall alone sits in the Moderate band — analysis is what lifts it to High.',
    ],
    cite: MS('printed p.22 (Subject Knowledge strand)'),
  },
  scripts: [
    {
      id: 'art1-a',
      label: 'The answer',
      persona: 'Knows a lot, analyses none',
      work: [
        'Accurate, detailed recall of the artist and their works.',
        'No analysis or evaluation — it describes and lists.',
      ],
      keyLevelId: 'b1',
      keyNote:
        'Moderate band — the High band explicitly needs critical analysis and evaluation, and recall alone can’t reach it however much you know. Turn facts into analysis: why the artist made a choice, what it achieves, how works compare. That shift, not more facts, is what earns the top band.',
      embodies: {
        behaviour: 'Recalls knowledge without analysing it — capped in the Moderate band.',
        cite: MS('printed p.22'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art1',
    rule: 'The top band is analysis, not recall.',
    detail:
      'Visual Studies’ Subject Knowledge strand reserves its High band for critical analysis and evaluation. Don’t just recall facts about the art — explain choices, effects and comparisons. Analysis is what climbs out of the Moderate band.',
    cite: MS('printed p.22'),
  },
};

// ─────────────── ART2 · Recognised examples ───────────────

const ART2: ScaleSession = {
  mode: 'scale',
  id: 'art-examples',
  subject: 'art',
  level: 'common',
  title: 'Name the actual works',
  cue: 'Section B/C essay',
  question: 'Relevant Examples is its own 10-mark strand. A candidate discusses “a famous painting by the artist” and “another well-known sculpture” without ever naming or clearly identifying specific works. How does the Relevant Examples strand score?',
  questionNote:
    'Scenario authored for this exercise. In Visual Studies, recognised, specific examples are a separable 10-mark strand; vague or unidentified artworks cap it.',
  scale: {
    name: 'Relevant Examples · /10 bands',
    levels: bands([3, 6, 9], ['Low — vague', 'Moderate', 'High — recognised']),
    notes: [
      'Relevant Examples is an independent 10-mark strand.',
      'Vague or unrecognised references (“a famous painting”) cap this strand low.',
      'Named, specific, correctly-attributed works are what score in the High band.',
    ],
    cite: MS('printed p.23 (Relevant Examples strand)'),
  },
  scripts: [
    {
      id: 'art2-a',
      label: 'The answer',
      persona: 'Talks around the works',
      work: [
        '“A famous painting by the artist…”, “a well-known sculpture…”.',
        'No specific works named or clearly identified.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band for Relevant Examples — the strand rewards recognised, specific works, and “a famous painting” identifies nothing. Naming the actual titles (and where relevant dates or materials) turns vague references into scoring examples. This is its own 10 marks; specificity is what claims it.',
      embodies: {
        behaviour: 'Refers to works vaguely without naming them — capping the Relevant Examples strand.',
        cite: MS('printed p.23'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art2',
    rule: 'Name the specific works — examples are their own strand.',
    detail:
      'Visual Studies scores Relevant Examples as a separate 10-mark strand — vague references (“a famous painting”) sit low. Name specific, correctly-attributed works to earn it.',
    cite: MS('printed p.23'),
  },
};

// ─────────────── ART3 · Cover the given headings ───────────────

const ART3: ScaleSession = {
  mode: 'scale',
  id: 'art-headings',
  subject: 'art',
  level: 'common',
  title: 'Use the headings you’re given',
  cue: 'Section A',
  question: 'A Section A part (a) asks you to describe the illustrated work “using the given headings” — for example composition, perspective and colour. A candidate writes a fluent general description of the image but doesn’t address the named headings. How does that affect the mark?',
  questionNote:
    'Scenario authored for this exercise. Section A (a) answers are anchored to the paper’s given headings (named lenses); a description that ignores them can’t reach the top band.',
  scale: {
    name: 'Section A (a) · using given headings',
    levels: bands([2, 4, 6], ['Low', 'Moderate', 'High — headings covered']),
    notes: [
      'The question names the headings to use (e.g. composition, perspective, colour).',
      'These headings are the structure the marks are organised around.',
      'A general description that skips the named headings can’t reach the High band.',
    ],
    cite: MS('printed pp.17–19 (Section A, given headings)'),
  },
  scripts: [
    {
      id: 'art3-a',
      label: 'The answer',
      persona: 'Fluent, but ignores the headings',
      work: [
        'A fluent, general description of the illustrated work.',
        'Doesn’t address the named headings (composition / perspective / colour).',
      ],
      keyLevelId: 'b1',
      keyNote:
        'Held in the middle band — the given headings are the framework the marks follow, and a general description that doesn’t use them leaves marks unclaimed. Structure the answer around each named heading in turn; that’s what the part is actually asking for and how it reaches the top band.',
      embodies: {
        behaviour: 'Describes the work generally without addressing the given headings.',
        cite: MS('printed p.17'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art3',
    rule: 'Answer around the headings you’re given.',
    detail:
      'Section A parts tell you which headings to use (composition, perspective, colour…). They’re the structure the marks follow — address each named heading in turn rather than writing a general description.',
    cite: MS('printed p.17'),
  },
};

// ─────────────── ART4 · Coherence and Focus is its own strand ───────────────

const ART4: ScaleSession = {
  mode: 'scale',
  id: 'art-coherence',
  subject: 'art',
  level: 'common',
  title: 'Answer the question, in order',
  cue: 'Section B/C essay',
  question: 'Coherence and Focus is its own 10-mark strand in a Section B/C answer. A candidate pours in accurate, detailed knowledge — but as a disorganised info-dump that never builds a focused argument answering the question actually posed. Subject Knowledge is strong; where does Coherence and Focus land?',
  questionNote:
    'Scenario authored for this exercise. Coherence and Focus (10 marks) is a separate Section B/C strand rewarding understanding the demands of the question and building sequential, evidence-based arguments — independent of how much you know.',
  scale: {
    name: 'Coherence and Focus · /10 bands',
    levels: bands([2, 5, 9], ['Low — unfocused', 'Moderate', 'High — coherent & focused']),
    notes: [
      'Coherence and Focus is an independent 10-mark strand (Low 0–3 / Moderate 4–6 / High 7–10).',
      'It rewards understanding the demands of the question and forming sequential, logical, evidence-based arguments.',
      'A knowledge info-dump that doesn’t answer the question posed sits low here, however strong the knowledge.',
    ],
    cite: MS('printed p.21 (Coherence and Focus strand)'),
  },
  scripts: [
    {
      id: 'art4-a',
      label: 'The answer',
      persona: 'Knows a lot, answers nothing',
      work: [
        'Accurate, detailed knowledge throughout.',
        'But it’s an unstructured info-dump — no focused argument responding to the question posed.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band for Coherence and Focus — this strand marks whether you understood and answered the actual question in a structured way, and strong knowledge can’t rescue it. It’s a separate 10 marks from Subject Knowledge. Plan a focused argument that responds directly to the question, in a logical order; that structure is what the strand pays for.',
      embodies: {
        behaviour: 'Presents knowledge as an unfocused info-dump that doesn’t answer the question — capping the Coherence and Focus strand.',
        cite: MS('printed p.21'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art4',
    rule: 'Coherence and Focus is its own 10 marks — answer the question, in order.',
    detail:
      'Visual Studies scores Coherence and Focus as a separate 10-mark strand: it rewards understanding the demands of the question and building a sequential, evidence-based argument. A knowledge dump that doesn’t answer the question posed scores low here no matter how much you know — plan a focused response.',
    cite: MS('printed p.21'),
  },
};

// ─────────────── ART5 · Visual Language is its own strand ───────────────

const ART5: ScaleSession = {
  mode: 'scale',
  id: 'art-visual-language',
  subject: 'art',
  level: 'common',
  title: 'Use the vocabulary of art',
  cue: 'Section B/C essay',
  question: 'Visual Language is the fourth Section B/C strand, worth 10 marks for “terminology and/or sketches”. A candidate writes a fluent, confident answer entirely in everyday language — no visual-art terminology, and no sketches either. How does the Visual Language strand score?',
  questionNote:
    'Scenario authored for this exercise. Visual Language (10 marks) rewards accurate use of visual-art terminology; sketches are an OPTIONAL alternative route, gated by “If sketches are used”. Terminology alone can max the strand, but an answer with neither art vocabulary nor sketches forfeits it.',
  scale: {
    name: 'Visual Language · /10 bands',
    levels: bands([3, 6, 9], ['Low — plain language', 'Moderate', 'High — precise terminology']),
    notes: [
      'Visual Language (terminology and/or sketches) is an independent 10-mark strand (Low 0–3 / Moderate 4–6 / High 7–10).',
      'The High band needs “a thorough use and understanding of terminology which is accurate, relevant and supports the communication of ideas”.',
      'Sketches are optional — every band opens “If sketches are used” — so terminology alone can reach the High band, but an answer with neither caps low.',
    ],
    cite: MS('printed p.24 (Visual Language strand)'),
  },
  scripts: [
    {
      id: 'art5-a',
      label: 'The answer',
      persona: 'Fluent, but no art vocabulary',
      work: [
        'Confident, readable prose about the artist and the work.',
        'Everyday language throughout — no visual-art terminology, and no sketches.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band for Visual Language — this strand pays for accurate visual-art terminology, and plain description claims none of it. Naming what you see with the right vocabulary (composition, tone, contrast, medium, form…) is a separate 10 marks. Sketches are only an optional second route, so skipping them costs nothing — but writing with no art vocabulary at all leaves this whole strand on the table.',
      embodies: {
        behaviour: 'Answers in everyday language with no visual-art terminology (and no sketches) — capping the Visual Language strand.',
        cite: MS('printed p.24'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art5',
    rule: 'Visual Language is its own 10 marks — use the vocabulary of art.',
    detail:
      'Visual Studies scores Visual Language as a separate 10-mark strand: accurate, relevant use of visual-art terminology, with sketches only an optional alternative route (“if sketches are used”). A fluent answer written in everyday language, with no art vocabulary and no sketches, forfeits this strand — name what you see with the right terms.',
    cite: MS('printed p.24'),
  },
};

// ─────────────── ART6 · Back the opinion with reasons ───────────────

const ART6: ScaleSession = {
  mode: 'scale',
  id: 'art-section-a-justify',
  subject: 'art',
  level: 'common',
  title: 'Give reasons, not just an opinion',
  cue: 'Section A',
  question: 'A Section A part (b) asks for “a reasonable interpretation of… what the work is about. Reasons for the answer given” (other questions ask for “justification for the answer given”). A candidate states a confident opinion about the work — but gives no reasons or evidence for it. How does part (b) score?',
  questionNote:
    'Scenario authored for this exercise. Section A part (b) is worth 4 marks and always pairs an interpretation/opinion with a demand for reasons or justification; the descriptor credits arguments “based on evidence” and marks down those “based on little or no evidence”, so a bare opinion caps low.',
  scale: {
    name: 'Section A (b) · opinion + reasons · /4 bands',
    levels: bands([1, 3, 4], ['Low — bare opinion', 'Moderate', 'High — justified']),
    notes: [
      'Part (b) is worth 4 marks (Low 0–1 / Moderate 2–3 / High 4).',
      'The wording always pairs the opinion with “Reasons for the answer given” or “Justification for the answer given”.',
      'The descriptor credits arguments “based on evidence” and holds down those “based on little or no evidence” — so an unjustified opinion sits low.',
    ],
    cite: MS('printed p.17 (Section A, part (b))'),
  },
  scripts: [
    {
      id: 'art6-a',
      label: 'The answer',
      persona: 'States a view, defends nothing',
      work: [
        'A clear, confident opinion about what the work is / is about.',
        'No reasons, no evidence from the image — the opinion just sits there.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band — part (b) explicitly asks for the reasons behind the view, and an unbacked opinion answers only half the question. The marks are in the justification: point to what in the work leads you to that reading. The confident verdict is the easy part; the evidence for it is what the tariff pays for.',
      embodies: {
        behaviour: 'Offers an opinion with no reasons or evidence — capping the part (b) justification tariff.',
        cite: MS('printed p.17'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art6',
    rule: 'Part (b) wants the reasons, not just the verdict.',
    detail:
      'Every Section A part (b) pairs an interpretation or opinion with “reasons” or “justification for the answer given”. A confident view with nothing behind it caps low — the marks are in the evidence. Point to what in the work supports your reading.',
    cite: MS('printed p.17'),
  },
};

// ─────────────── ART7 · Today's world: apply, don't recite ───────────────

const ART7: ScaleSession = {
  mode: 'scale',
  id: 'art-todays-world',
  subject: 'art',
  level: 'common',
  title: 'Read the stimulus in front of you',
  cue: 'Section A',
  question: 'Section A is “Today’s world” — it shows an unfamiliar stimulus and asks you to “decode, decipher and make meaning” from it. A candidate barely engages the image shown and instead writes a memorised paragraph about a studied artist. The descriptor’s High band rewards “application… to new and unfamiliar situations” and “analysis… of any given stimulus material”. Where does the answer land?',
  questionNote:
    'Scenario authored for this exercise. Section A tests critical literacy applied to the unseen stimulus on the paper, not recall of prepared content; the descriptor rewards application “to new and unfamiliar situations” and analysis “of any given stimulus material”.',
  scale: {
    name: 'Section A · applying to the stimulus · /6 bands',
    levels: bands([2, 4, 6], ['Low — recites, ignores stimulus', 'Moderate', 'High — applies to the stimulus']),
    notes: [
      'Section A demands “skills of critical literacy and contextual inquiry to decode, decipher and make meaning from a range of stimuli/questions”.',
      'The High band rewards “application… to new and unfamiliar situations” and “analysis, interpretation and evaluation of any given stimulus material”.',
      'A prepared paragraph that doesn’t engage the stimulus shown answers a different question — it can’t reach the High band.',
    ],
    cite: MS('printed p.16 (Section A descriptor)'),
  },
  scripts: [
    {
      id: 'art7-a',
      label: 'The answer',
      persona: 'Recites the essay they prepared',
      work: [
        'A polished, memorised paragraph about a studied artist and movement.',
        'Barely references the unfamiliar stimulus actually shown on the paper.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band — “Today’s world” marks how well you read and interpret the stimulus in front of you, not how much prepared content you can reproduce. A pre-written paragraph that ignores the image is answering a question that wasn’t asked. Look hard at the given stimulus and apply your art thinking to it directly; that application to the unfamiliar is exactly what the band rewards.',
      embodies: {
        behaviour: 'Recites prepared content instead of decoding the given unfamiliar stimulus — capping the Section A descriptor.',
        cite: MS('printed p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art7',
    rule: 'Section A marks the stimulus in front of you, not the essay you prepared.',
    detail:
      '“Today’s world” tests critical literacy applied to an unfamiliar stimulus — decode, decipher and make meaning from the image on the paper. A memorised paragraph that ignores it answers a different question. Apply your art thinking to the actual stimulus; that application to the unfamiliar is what the High band rewards.',
    cite: MS('printed p.16'),
  },
};

export const ART_CHAIR: ChairSubject = {
  id: 'art',
  label: 'Art (Visual Studies)',
  tagline: 'Analyse over recall, name the works, use the vocabulary of art, and read the stimulus in front of you.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [ART1, ART2, ART3, ART4, ART5, ART6, ART7],
  sources: [
    { label: 'SEC LC Art HL Visual Studies marking scheme 2024 (examiner-reports/art/2024-visual-studies-marking-scheme)' },
    { label: 'SEC LC Art OL Visual Studies marking scheme 2024 (examiner-reports/art/2024-visual-studies-ol-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the CURRENT Visual Studies written-paper conventions (revised spec, first examined 2023/24). The written-paper descriptor bands are word-for-word identical at Higher and Ordinary level — differentiation is by the question paper, not the scheme — so these sessions apply at both levels (verified by comparing the 2024 HL and OL schemes directly). At OL the stimuli are everyday visual culture with simpler observable headings. The pre-2022 “History & Appreciation” paper was marked differently.',
};
