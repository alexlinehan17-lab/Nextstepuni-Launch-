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

// ─────────────── ART8 · Match the detail to the marks ───────────────

const ART8: ScaleSession = {
  mode: 'scale',
  id: 'art-tariff-detail',
  subject: 'art',
  level: 'common',
  title: 'Match the detail to the marks',
  cue: 'Section A',
  question: 'Section A parts are worth 4, 5 or 6 marks, and the scheme says the depth expected scales with the tariff: “The detail required in any answer is determined by… the number of marks assigned”. A candidate gives a single thin sentence in answer to a 6-mark part (a) — the same length they’d give a 4-mark part. How does the 6-mark part score?',
  questionNote:
    'Scenario authored for this exercise. Section A uses one shared descriptor across 4/5/6-mark parts, with band boundaries that widen with the tariff (High is 4, 4–5, 5–6 respectively); the scheme ties the detail required to the marks available, so a thin answer under-serves a higher-tariff part.',
  scale: {
    name: 'Section A · detail vs 6-mark tariff',
    levels: bands([2, 4, 6], ['Low — thin for 6 marks', 'Moderate', 'High — detail matches tariff']),
    notes: [
      'A single descriptor covers 4-, 5- and 6-mark parts; the band ceilings widen with the tariff (High = 4 / 4–5 / 5–6).',
      '“The detail required in any answer is determined by the context and the manner in which the question is asked and by the number of marks assigned.”',
      'A one-line answer that would suit a 4-mark part leaves a 6-mark part short of its High band.',
    ],
    cite: MS('printed p.15 (detail determined by marks assigned)'),
  },
  scripts: [
    {
      id: 'art8-a',
      label: 'The answer',
      persona: 'One line, whatever the tariff',
      work: [
        'A single thin sentence answering a 6-mark part (a).',
        'The same length and depth it would give a 4-mark part.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band — the mark value tells you how much to write, and a 6-mark part expects more developed detail than a one-liner. Check the tariff before you answer: a 6-mark part wants fuller treatment of the given headings than a 4-mark part. Reading the marks and pacing your detail to them is a free way to climb the band.',
      embodies: {
        behaviour: 'Gives a low-tariff amount of detail to a high-tariff part — under-serving the marks available.',
        cite: MS('printed p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art8',
    rule: 'Let the marks tell you how much to write.',
    detail:
      'Section A parts run 4, 5 or 6 marks on one shared descriptor whose ceilings widen with the tariff. The scheme ties the detail required to the marks assigned — a one-line answer that suits a 4-mark part falls short of a 6-mark part’s High band. Read the tariff and pace your detail to it.',
    cite: MS('printed p.15'),
  },
};

// ─────────────── ART9 · Skilful brevity is protected ───────────────

const ART9: ScaleSession = {
  mode: 'scale',
  id: 'art-brevity',
  subject: 'art',
  level: 'common',
  title: 'Brevity is fine — padding isn’t',
  cue: 'Section A / B / C',
  question: 'The scheme instructs examiners twice: “Be careful not to penalise skilful brevity, nor to reward unwarranted length.” A candidate writes a short, precise, complete answer that fully addresses the question and then stops. Are they marked down for its length?',
  questionNote:
    'Scenario authored for this exercise. This general instruction appears in both the Section A and the Section B/C marking notes; it protects a concise, complete answer and refuses extra credit for padding.',
  scale: {
    name: 'Answer quality · substance not length',
    levels: bands([2, 4, 6], ['Low — padded, little said', 'Moderate', 'High — concise & complete']),
    notes: [
      '“Be careful not to penalise skilful brevity, nor to reward unwarranted length.”',
      'A short answer that fully meets the descriptor is not marked down for being short.',
      'Equally, filler and repetition earn nothing — length on its own is not a route to marks.',
    ],
    cite: MS('printed p.15 (repeated printed p.20)'),
  },
  scripts: [
    {
      id: 'art9-a',
      label: 'The answer',
      persona: 'Says it once, well, then stops',
      work: [
        'A short, precise answer that fully addresses the question and the given headings.',
        'No padding — it stops once the point is made.',
      ],
      keyLevelId: 'b2',
      keyNote:
        'High band — the scheme explicitly protects skilful brevity, so a complete, precise answer isn’t penalised for being short. Write to fully meet the descriptor, then stop; you don’t need to fill the space. The examiner is told not to reward unwarranted length either, so padding wouldn’t have lifted it — completeness does.',
      embodies: {
        behaviour: 'Answers completely and concisely — which the scheme protects rather than penalises.',
        cite: MS('printed p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art9',
    rule: 'A complete short answer beats a padded long one.',
    detail:
      'The scheme tells examiners not to penalise skilful brevity nor to reward unwarranted length. A concise answer that fully meets the descriptor scores full band — you don’t need to fill the page. Padding adds nothing, so make the point well and stop.',
    cite: MS('printed p.15'),
  },
};

// ─────────────── ART10 · Correct terms, no contradictions ───────────────

const ART10: ScaleSession = {
  mode: 'scale',
  id: 'art-term-accuracy',
  subject: 'art',
  level: 'common',
  title: 'Use terms correctly or lose the marks',
  cue: 'Section A / B / C',
  question: 'The scheme warns: “Words, expressions or phrases must be correctly used in context and not contradicted, and where there is evidence of incorrect use or contradictions the marks may not be awarded.” A candidate reaches for impressive-sounding art terms but misuses several and contradicts an earlier claim. How does that land?',
  questionNote:
    'Scenario authored for this exercise. This general marking instruction means terminology is only credited when used correctly and consistently — misused or self-contradicting terms can forfeit marks rather than gain them.',
  scale: {
    name: 'Terminology · correct use in context',
    levels: bands([3, 6, 9], ['Low — misused / contradicted', 'Moderate', 'High — accurate in context']),
    notes: [
      '“Words, expressions or phrases must be correctly used in context and not contradicted.”',
      '“Where there is evidence of incorrect use or contradictions the marks may not be awarded.”',
      'Reaching for jargon you don’t control can cost marks — a correctly used simpler term is safer.',
    ],
    cite: MS('printed p.15 (correct use of terminology)'),
  },
  scripts: [
    {
      id: 'art10-a',
      label: 'The answer',
      persona: 'Impressive words, wrong meanings',
      work: [
        'Sprinkles in advanced-sounding art terms to look fluent.',
        'Several are misused, and one claim contradicts an earlier one.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Low band — the scheme lets examiners withhold marks where terms are used incorrectly or the answer contradicts itself, so misfired jargon actively costs you. Only use a term you can apply correctly in context; a plainer word used accurately is worth more than an impressive one used wrongly. Keep your claims consistent so nothing cancels itself out.',
      embodies: {
        behaviour: 'Uses terminology incorrectly and contradicts an earlier claim — which the scheme says may forfeit marks.',
        cite: MS('printed p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art10',
    rule: 'A term only helps if it’s used correctly and consistently.',
    detail:
      'The scheme lets examiners withhold marks where words are used incorrectly in context or the answer contradicts itself. Impressive jargon you don’t control can cost marks — use only terms you can apply accurately, and keep your claims consistent.',
    cite: MS('printed p.15'),
  },
};

// ─────────────── ART11 · Your own valid example still counts ───────────────

const ART11: ScaleSession = {
  mode: 'scale',
  id: 'art-open-examples',
  subject: 'art',
  level: 'common',
  title: 'Bring the example you actually know',
  cue: 'Section B/C essay',
  question: 'The scheme is open: “Candidates may choose from a wide range of relevant examples and content… Relevant content must be credited,” and if an examiner doesn’t know the work they must “make yourself familiar… before you mark”. A candidate uses a specific, well-understood but less-famous artist rather than a textbook big name. Does that relevant, specific example score?',
  questionNote:
    'Scenario authored for this exercise. Visual Studies is not a closed answer key — any relevant, specific, correctly-identified content is credited and the examiner researches unfamiliar work, so a valid non-canonical example is not disadvantaged for being off the “expected” list.',
  scale: {
    name: 'Relevant Examples · open choice · /10 bands',
    levels: bands([3, 6, 9], ['Low — vague / irrelevant', 'Moderate', 'High — specific, relevant, understood']),
    notes: [
      '“Candidates may choose from a wide range of relevant examples and content… Relevant content must be credited.”',
      '“If you are not familiar with the artwork or artist… make yourself familiar… All valid points will be taken into consideration.”',
      'A specific, correctly-identified, well-understood example scores on its relevance — it doesn’t have to be a famous textbook name.',
    ],
    cite: MS('printed p.20 (wide range of relevant examples; printed p.15, examiner self-educates)'),
  },
  scripts: [
    {
      id: 'art11-a',
      label: 'The answer',
      persona: 'Uses the artist they genuinely know',
      work: [
        'A specific, less-famous artist and named works the candidate understands well.',
        'Directly relevant to the question, correctly identified and used to justify the response.',
      ],
      keyLevelId: 'b2',
      keyNote:
        'High band — the scheme credits any relevant content and has the examiner research unfamiliar work, so a specific, well-understood example scores on its merits whether or not it’s a canonical name. Don’t self-censor to only famous artists; the example you actually understand and can analyse will out-score a big name you can only describe vaguely. Relevance and understanding, not fame, are what the strand pays for.',
      embodies: {
        behaviour: 'Uses a valid, specific, well-understood non-canonical example — which the open-example rule credits fully.',
        cite: MS('printed p.20'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art11',
    rule: 'The example you truly understand beats a famous one you don’t.',
    detail:
      'Visual Studies is an open scheme — any relevant, specific, correctly-identified content is credited, and examiners research unfamiliar work. A well-understood, less-famous artist scores on relevance and understanding, so bring the example you can actually analyse rather than a big name you can only name.',
    cite: MS('printed p.20'),
  },
};

// ─────────────── ART12 · Over-answering: best answer counts ───────────────

const ART12: ScaleSession = {
  mode: 'scale',
  id: 'art-best-answer',
  subject: 'art',
  level: 'common',
  title: 'Answer one — but a spare doesn’t cost you',
  cue: 'Section B/C essay',
  question: 'You answer one question in Section B and one in Section C. A candidate, unsure, answers two Section B questions — one strong, one weak. The scheme says: “If candidates answer more than one question… per section then the question with the highest score is used to award marks.” Which one is credited?',
  questionNote:
    'Scenario authored for this exercise. Unlike some schemes that deduct for invalid extra answers, Visual Studies simply credits the highest-scoring answer per section — over-answering is not penalised, though the time spent is a real cost.',
  scale: {
    name: 'Section B/C · which answer is credited · /50',
    levels: bands([15, 30, 45], ['Low — the weak one', 'Moderate', 'High — the strong one counts']),
    notes: [
      '“If candidates answer more than one question etc. per section then the question with the highest score is used to award marks.”',
      'No deduction is applied for the extra answer — only the best one scores.',
      'The real cost of over-answering is time, not marks: two half-answers can beat neither.',
    ],
    cite: MS('printed p.20 (highest score used)'),
  },
  scripts: [
    {
      id: 'art12-a',
      label: 'The answer',
      persona: 'Hedged their bets, wrote two',
      work: [
        'Answered two Section B questions instead of one.',
        'One is strong; the other is weak and half-finished.',
      ],
      keyLevelId: 'b2',
      keyNote:
        'The strong answer is credited — the scheme takes the highest-scoring answer per section and applies no penalty for the extra one, so a spare attempt can’t lower your mark. The genuine risk is time: splitting effort across two questions can leave both under-developed. If you do change your mind, the better answer will count, so commit your time to making one of them strong.',
      embodies: {
        behaviour: 'Answers more than one question per section — credited on the highest-scoring one, with no deduction.',
        cite: MS('printed p.20'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art12',
    rule: 'The best answer per section counts — extras aren’t penalised, but they cost time.',
    detail:
      'If you answer more than one question in a section, Visual Studies credits the highest-scoring one and deducts nothing for the extra. A change of mind won’t sink you — but two half-answers help no one, so spend your time making one answer strong.',
    cite: MS('printed p.20'),
  },
};

// ─────────────── ART13 · Articulate a personal understanding ───────────────

const ART13: ScaleSession = {
  mode: 'scale',
  id: 'art-personal-understanding',
  subject: 'art',
  level: 'common',
  title: 'Show your own understanding',
  cue: 'Section B/C essay',
  question: 'The Coherence and Focus strand rewards, alongside answering the question, “the ability to articulate a personal understanding in the response”. A candidate reproduces an accurate, orderly, but entirely generic textbook answer — correct and well-sequenced, yet with no personal understanding or voice in it. Where does Coherence and Focus land?',
  questionNote:
    'Scenario authored for this exercise. Coherence and Focus (10 marks) lists articulating a personal understanding as one of the abilities it credits at each band; a competent but impersonal, memorised answer meets some of the strand but can’t reach its High band.',
  scale: {
    name: 'Coherence and Focus · personal understanding · /10 bands',
    levels: bands([2, 5, 9], ['Low', 'Moderate — orderly but generic', 'High — personal understanding']),
    notes: [
      'Each band pairs answering the question and sequential arguments with “a[n]… ability to articulate a personal understanding in the response”.',
      'The High band needs “a thorough ability to articulate a personal understanding”.',
      'An accurate but generic, memorised answer with no personal voice is held below the High band.',
    ],
    cite: MS('printed p.21 (Coherence and Focus, personal understanding)'),
  },
  scripts: [
    {
      id: 'art13-a',
      label: 'The answer',
      persona: 'Textbook-perfect, personally absent',
      work: [
        'An accurate, well-ordered, on-topic answer.',
        'Entirely generic — a reproduced textbook account with no personal understanding or view.',
      ],
      keyLevelId: 'b1',
      keyNote:
        'Moderate band — this strand credits articulating a personal understanding, and a flawless but impersonal reproduction meets the “answer the question” part while missing the personal voice the High band needs. Say what you make of the work: your reading, your judgement, your response to it. That personal engagement, on top of accuracy and order, is what lifts the strand.',
      embodies: {
        behaviour: 'Gives an accurate but generic answer with no personal understanding — capped below the strand’s High band.',
        cite: MS('printed p.21'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art13',
    rule: 'Coherence and Focus also rewards your personal understanding — put yourself in it.',
    detail:
      'The Coherence and Focus strand credits, at every band, “the ability to articulate a personal understanding in the response”. A correct but generic textbook answer meets the question but not the personal voice — reach the High band by saying what you make of the work: your reading, judgement and response.',
    cite: MS('printed p.21'),
  },
};

// ─────────────── ART14 · Four independent strands — serve all of them ───────────────

const ART14: ScaleSession = {
  mode: 'scale',
  id: 'art-four-strands',
  subject: 'art',
  level: 'common',
  title: 'Serve all four strands, not just one',
  cue: 'Section B/C essay',
  question: 'Each 50-mark Section B/C answer is marked on four separate band descriptors — Coherence and Focus (10), Subject Knowledge (20), Relevant Examples (10) and Visual Language (10) — scored independently and summed. A candidate writes a brilliant, High-band Subject Knowledge answer but names no recognised examples, wanders off the question and uses no art terminology. How high can the /50 total go?',
  questionNote:
    'Scenario authored for this exercise. The four Section B/C strands are separate band descriptors that add to 50; because they’re marked independently, a lopsided answer that maxes one strand and neglects the others is structurally capped — a top Subject Knowledge score is still only 20 of 50.',
  scale: {
    name: 'Section B/C · four strands summed · /50',
    levels: bands([18, 32, 45], ['Low — one strand only', 'Moderate', 'High — all four served']),
    notes: [
      'The answer is scored on four separate band descriptors: Coherence and Focus (10) + Subject Knowledge (20) + Relevant Examples (10) + Visual Language (10) = 50.',
      'The strands are marked independently and added — brilliance in one cannot pay for a blank in another.',
      'A top Subject Knowledge answer is still only 20 of 50; neglecting the other three strands caps the whole question.',
    ],
    cite: MS('printed pp.21–24 (four Section B/C band descriptors)'),
  },
  scripts: [
    {
      id: 'art14-a',
      label: 'The answer',
      persona: 'All knowledge, nothing else',
      work: [
        'A brilliant, High-band Subject Knowledge answer.',
        'But it names no recognised examples, drifts off the question, and uses no art terminology.',
      ],
      keyLevelId: 'b1',
      keyNote:
        'Held around the middle of /50 — Subject Knowledge is only 20 of the 50 marks, and the other three strands are scored and added separately, so neglecting them leaves roughly 30 marks unclaimed however strong the knowledge. Budget the answer across all four: stay on the question (Coherence and Focus), name recognised examples (Relevant Examples) and use art vocabulary (Visual Language). Spreading the effort, not deepening one strand, is what raises the total.',
      embodies: {
        behaviour: 'Maxes one strand and neglects the other three — structurally capping the four-strand total.',
        cite: MS('printed pp.21–24'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art14',
    rule: 'Four independent strands make 50 — a lopsided answer is capped.',
    detail:
      'Section B/C answers are scored on four separate band descriptors — Coherence and Focus (10), Subject Knowledge (20), Relevant Examples (10), Visual Language (10) — marked independently and summed. Brilliance in one can’t pay for a blank in another, so a top knowledge answer with no examples, focus or terminology is capped near 20 of 50. Budget your effort across all four.',
    cite: MS('printed pp.21–24'),
  },
};

// ─────────────── ART15 · Answer all five Section A questions ───────────────

const ART15: ScaleSession = {
  mode: 'scale',
  id: 'art-section-a-five',
  subject: 'art',
  level: 'common',
  title: 'Answer all five — and choose your five',
  cue: 'Section A',
  question: 'Section A instructs: “Candidates must answer any five questions in this section from Question 1 to Question 7. Each question is worth 10 marks.” A candidate answers only three — very well — and leaves two of the required five blank. Section A is 50 marks. What is the ceiling on their Section A total?',
  questionNote:
    'Scenario authored for this exercise. Section A is five free-choice 10-mark questions (5 × 10 = 50) out of seven; each unanswered required question is a full 10 marks forfeited, and the free choice lets a candidate skip their two weakest topics.',
  scale: {
    name: 'Section A · questions completed · /50',
    levels: bands([20, 35, 50], ['Low — left required questions blank', 'Moderate', 'High — all five answered']),
    notes: [
      '“Candidates must answer any five questions in this section from Question 1 to Question 7. Each question is worth 10 marks.”',
      'Five × 10 = 50: every unanswered required question forfeits a full 10 marks, whatever the quality of the rest.',
      'The choice is yours — pick your five strongest of the seven and skip the two you know least.',
    ],
    cite: MS('printed p.15 (answer any five, each 10 marks)'),
  },
  scripts: [
    {
      id: 'art15-a',
      label: 'The answer',
      persona: 'Three brilliant, two blank',
      work: [
        'Answers three Section A questions to a very high standard.',
        'Leaves two of the required five unanswered.',
      ],
      keyLevelId: 'b0',
      keyNote:
        'Capped at roughly 30 of 50 — each question is a separate 10 marks, so two blanks forfeit 20 no matter how good the three answers are. You choose any five of the seven, so there’s no need to attempt topics you fear: pick your five strongest and complete all of them. A modest fifth answer almost always beats a brilliant third-and-nothing-else, because it claims marks that would otherwise be lost.',
      embodies: {
        behaviour: 'Answers fewer than the required five questions — forfeiting a full 10 marks per blank.',
        cite: MS('printed p.15'),
      },
    },
  ],
  takeaway: {
    id: 'codex-art15',
    rule: 'Answer all five Section A questions — and choose your best five.',
    detail:
      'Section A is five free-choice 10-mark questions from seven (5 × 10 = 50). Each blank forfeits a full 10 marks regardless of how good the others are, so completing all five beats perfecting a few. You pick the five, so play to your strengths and skip your two weakest topics.',
    cite: MS('printed p.15'),
  },
};

export const ART_CHAIR: ChairSubject = {
  id: 'art',
  label: 'Art (Visual Studies)',
  tagline: 'Analyse over recall, name the works, use the vocabulary of art, budget all four strands, and read the stimulus in front of you.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [ART1, ART2, ART3, ART4, ART5, ART6, ART7, ART8, ART9, ART10, ART11, ART12, ART13, ART14, ART15],
  sources: [
    { label: 'SEC LC Art HL Visual Studies marking scheme 2024 (examiner-reports/art/2024-visual-studies-marking-scheme)' },
    { label: 'SEC LC Art OL Visual Studies marking scheme 2024 (examiner-reports/art/2024-visual-studies-ol-marking-scheme)' },
  ],
  coverageNote:
    'These sessions teach the CURRENT Visual Studies written-paper conventions (revised spec, first examined 2023/24). The written-paper descriptor bands are word-for-word identical at Higher and Ordinary level — differentiation is by the question paper, not the scheme — so these sessions apply at both levels (verified by comparing the 2024 HL and OL schemes directly). At OL the stimuli are everyday visual culture with simpler observable headings. The pre-2022 “History & Appreciation” paper was marked differently.',
};
