/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The Examiner's Chair — Geography (Higher Level) marking sessions.
 *
 * Questions and scripts are AUTHORED for this exercise (labelled in each
 * `questionNote`) — they are not real SEC questions or candidate scripts. The
 * SRP marking grammar (the definition of a Significant Relevant Point, the
 * diagram rule, the answer-the-question caps and the graded Overall Coherence
 * mark) is the real SEC system, cited to:
 *  - SEC LC Geography HL marking scheme 2025 —
 *    examiner-reports/geography/2025-marking-scheme.*
 *  - Chief Examiner's Report, Geography 2012 —
 *    examiner-reports/geography/2012-chief-examiner.*
 * Claim-by-claim record: compliance/evidence/examiners-chair.md.
 */

import { type ChairSubject, type GridSession, type ScaleSession, type ScaleLevel } from './types';

const MS = (p: string) => ({ label: `SEC Geography HL marking scheme 2025, ${p}` });
const CER = (p: string) => ({ label: `Chief Examiner's Report, Geography 2012, ${p}` });
const MSOL = (p: string) => ({ label: `SEC Geography OL marking scheme 2025, ${p}` });

const srpScale = (marks: number[]): ScaleLevel[] =>
  marks.map(m => ({ id: `m${m}`, label: m === 0 ? 'No marks' : `${m} marks`, annotation: `${m}m`, marks: m }));

// ───────────────── Geo1 · What counts as an SRP ─────────────────

const GEO1: GridSession = {
  mode: 'grid',
  id: 'geo-srp',
  subject: 'geography',
  level: 'higher',
  title: 'SRP, or just words?',
  cue: 'Examine',
  question: 'Examine how one Irish landform was formed by the process of deposition.',
  questionNote:
    'Question authored for this exercise. Marked on the SEC SRP system — each Significant Relevant Point is worth 2 marks; a landform-formation part is typically “Landform named 2 marks / Examination 14 × SRPs”.',
  grid: {
    perPoint: [{ id: 'srp', label: 'SRP', marks: 2 }],
    shorthand: 'each SRP · 2m',
    ruleNote:
      'An SRP is “a single piece of factual information” that advances a coherent answer. A sentence that adds a real fact scores 2; a sentence that just restates, waffles, or repeats an earlier point adds nothing — the examiner counts points of substance, not lines of writing.',
    cite: MS('p.3 (SRP definition) and p.9 (landform grid)'),
  },
  scripts: [
    {
      id: 'geo1-a',
      label: 'Script A',
      persona: 'Writes a lot, says little',
      attempts: [
        {
          id: 'geo1-a-1',
          text: 'A beach is a very common landform that you see in Ireland and lots of people visit beaches on their holidays.',
          key: { srp: 0 },
          keyNote: 'True, but not a piece of formation information — nothing here explains deposition. 0 SRPs. Examiners see a lot of this warm-up sentence; it scores nothing.',
        },
        {
          id: 'geo1-a-2',
          text: 'Beaches are really important and they are a beautiful part of our coastline.',
          key: { srp: 0 },
          keyNote: 'Opinion and repetition, no new fact about how the landform formed. 0 SRPs.',
        },
      ],
      embodies: {
        behaviour: 'Fills the page with relevant-sounding but non-factual sentences that carry no SRP.',
        cite: MS('p.3'),
      },
    },
    {
      id: 'geo1-b',
      label: 'Script B',
      persona: 'Every sentence earns',
      attempts: [
        {
          id: 'geo1-b-1',
          text: 'Waves carry sand and shingle along the coast by longshore drift.',
          key: { srp: 2 },
          keyNote: 'A single, specific factual step in the formation process. 2 marks — one SRP.',
        },
        {
          id: 'geo1-b-2',
          text: 'Where the coastline curves into a bay, the waves lose energy and drop this material.',
          key: { srp: 2 },
          keyNote: 'A distinct next fact — energy loss causing deposition. Another SRP, 2 marks.',
        },
      ],
    },
    {
      id: 'geo1-c',
      label: 'Script C',
      persona: 'Knows it — but says it twice',
      attempts: [
        {
          id: 'geo1-c-1',
          text: 'Longshore drift transports sand and shingle along the coast.',
          key: { srp: 2 },
          keyNote: 'A genuine SRP — a real step in the process, clearly stated. 2 marks.',
        },
        {
          id: 'geo1-c-2',
          text: 'The material is moved down the coastline by the drifting of the waves.',
          key: { srp: 0 },
          keyNote: 'This is the SAME point as the last sentence, just reworded — no new fact. The examiner credits a point once, so a restatement scores 0. This is the middle performer’s trap: a solid answer padded with rephrasings of points already made. Two sentences, one SRP.',
        },
      ],
      embodies: {
        behaviour: 'Earns a real SRP, then re-states it in different words — the restatement carries no new fact, so it scores nothing.',
        cite: MS('p.3'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo1',
    rule: 'Marks are SRPs, not sentences.',
    detail:
      'Geography pays 2 marks per Significant Relevant Point — a single piece of factual information. Warm-up lines, opinions and repetition score nothing. Make every sentence carry one new fact.',
    cite: MS('p.3'),
  },
};

// ───────────────── Geo2 · The diagram rule ─────────────────

const GEO2: ScaleSession = {
  mode: 'scale',
  id: 'geo-diagram',
  subject: 'geography',
  level: 'higher',
  title: 'Label it or lose it',
  cue: 'Diagram',
  question: 'A candidate draws a clear, accurate diagram of a river’s course to support a landform answer — but writes no labels on it at all.',
  questionNote:
    'Scenario authored for this exercise. The diagram rule is stated across the SEC scheme’s landform questions: a labelled diagram earns 1 SRP; an unlabelled diagram earns nothing.',
  scale: {
    name: 'Diagram · SRP credit',
    levels: srpScale([0, 2]),
    notes: [
      'A relevant, labelled diagram is worth 1 SRP (2 marks).',
      'The scheme’s recurring rule: “Diagram without labelling 0 marks.”',
      'Accuracy and neatness don’t substitute for labels — the labels are what the SRP pays for.',
    ],
    cite: MS('p.6–14 (diagram rule, recurring)'),
  },
  scripts: [
    {
      id: 'geo2-a',
      label: 'The diagram',
      persona: 'Beautiful — and unlabelled',
      work: ['[ A clear, accurate river diagram ]', 'No labels written on it.'],
      keyLevelId: 'm0',
      keyNote:
        'However good the drawing, an unlabelled diagram scores 0 — the SEC rule is explicit. Two or three labels (source, meander, mouth) would have turned this into an SRP. Labels are the cheapest marks a diagram can earn, and they are routinely left off.',
      embodies: {
        behaviour: 'Submits an accurate but unlabelled diagram, which the scheme scores at 0.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo2',
    rule: 'An unlabelled diagram is worth nothing.',
    detail:
      'The scheme says it plainly: “Diagram without labelling 0 marks.” A labelled diagram earns an SRP. Always add labels — they are free marks most candidates leave on the table.',
    cite: MS('p.6'),
  },
};

// ───────────────── Geo3 · Answer the question asked ─────────────────

const GEO3: ScaleSession = {
  mode: 'scale',
  id: 'geo-wrong-process',
  subject: 'geography',
  level: 'higher',
  title: 'The waterfall trap',
  cue: 'Examine',
  question: 'The question asks how a landform of DEPOSITION was formed. The candidate writes a detailed, accurate two-page account of how a waterfall (a landform of EROSION) is formed.',
  questionNote:
    'Scenario authored for this exercise. The behaviour is documented in the 2012 Chief Examiner’s Report; the 2025 scheme states “Examination of processes of erosion 0 marks” where deposition was required.',
  scale: {
    name: 'Off-process answer',
    levels: srpScale([0, 14, 28]),
    notes: [
      'The examination part is worth up to 14 SRPs (28 marks) — when it answers the question set.',
      'This answer examines erosion where deposition was required.',
      'The scheme’s rule for exactly this: “Examination of processes of erosion 0 marks.”',
      'So a perfect answer to the wrong question scores 0 for the examination.',
    ],
    cite: MS('p.9 (wrong-process rule)'),
  },
  scripts: [
    {
      id: 'geo3-a',
      label: 'The script',
      persona: 'Excellent answer — to the wrong question',
      work: [
        'Two pages on a waterfall: hard and soft rock, undercutting, the plunge pool, retreat upstream forming a gorge.',
        'Accurate, well-sequenced, fully labelled diagram.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Every fact is correct — about erosion. The question asked for deposition, and the scheme awards the examination of the wrong process 0 marks. This is the single most expensive mistake in Geography: brilliant work, zero credit, because it answered a question that wasn’t asked. Read the process word before you write.',
      embodies: {
        behaviour: 'Writes a detailed answer on the wrong process (erosion for a deposition question) — flagged in the Chief Examiner’s Report.',
        cite: CER('p.25'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo3',
    rule: 'A perfect answer to the wrong question scores zero.',
    detail:
      'Geography questions pin a specific process, landform or region. Answer a different one — erosion for deposition — and even flawless work earns nothing. Underline the key nouns in the question first.',
    cite: MS('p.9'),
  },
};

// ───────────────── Geo4 · Overall Coherence (essays) ─────────────────

const GEO4: ScaleSession = {
  mode: 'scale',
  id: 'geo-coherence',
  subject: 'geography',
  level: 'higher',
  title: 'The 20 marks for coherence',
  cue: 'Options essay',
  question: 'An Options essay is packed with accurate facts, but they are dumped in no clear order and much of the material is about the general topic rather than the specific question asked. How is the graded Overall Coherence mark awarded?',
  questionNote:
    'Scenario authored for this exercise. Options essays carry a graded Overall Coherence mark of 20; the descriptor bands are quoted from the 2025 scheme.',
  scale: {
    name: 'Overall Coherence · graded /20',
    levels: [
      { id: 'poor', label: 'Poor', annotation: '0', marks: 0 },
      { id: 'weak', label: 'Weak', annotation: '6', marks: 6 },
      { id: 'fair', label: 'Fair', annotation: '10', marks: 10 },
      { id: 'good', label: 'Good', annotation: '14', marks: 14 },
      { id: 'vgood', label: 'Very Good', annotation: '17', marks: 17 },
      { id: 'excellent', label: 'Excellent', annotation: '20', marks: 20 },
    ],
    notes: [
      'Overall Coherence is graded: Excellent 20 / Very Good 17 / Good 14 / Fair 10 / Weak 6 / Poor 0.',
      'It rewards a structured answer that addresses the specific question — not the amount of knowledge.',
      'Facts dumped in no order, much of it topic-not-question, is the classic “Weak” profile.',
    ],
    cite: MS('p.47 (Overall Coherence descriptors)'),
  },
  scripts: [
    {
      id: 'geo4-a',
      label: 'The essay',
      persona: 'Knowledge bank, no shape',
      work: [
        'Lots of accurate facts about the topic.',
        'No clear structure; jumps between ideas.',
        'Much of the material is about the general topic, not the question set.',
      ],
      keyLevelId: 'weak',
      keyNote:
        'The facts might score their SRPs, but Overall Coherence is a separate, graded 20 marks for structure and relevance to the question. Unordered, topic-not-question writing lands around “Weak” (6). The same knowledge, organised into an argument that answers the question, reaches Very Good or Excellent — a 11-to-14-mark swing on coherence alone.',
      embodies: {
        behaviour: 'Provides “banks of knowledge” about the topic without shaping it to the specific question — the Overall Coherence killer.',
        cite: CER('p.30'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo4',
    rule: 'Structure is worth its own 20 marks.',
    detail:
      'In Options essays, Overall Coherence is graded separately from your facts. A shaped answer that addresses the exact question can gain 11–14 marks over the same facts dumped at random. Plan the essay before you write it.',
    cite: MS('p.47'),
  },
};

// ───────────────── Geo5 · OL — an SRP is worth 3 marks ─────────────────

const GEO5: GridSession = {
  mode: 'grid',
  id: 'geo-ol-srp',
  subject: 'geography',
  level: 'ordinary',
  title: 'At Ordinary Level, an SRP is 3 marks',
  cue: 'Explain (OL)',
  question: 'An Ordinary Level part ends “Explain briefly” and is marked “2 SRPs @ 3 marks each = 6m”. At OL each Significant Relevant Point is worth 3 marks (not 2 as at Higher). A candidate writes one developed point, then stops.',
  questionNote:
    'Scenario authored for this exercise. At Ordinary Level an SRP is worth 3 marks (Higher is 2), and “explain briefly” closers typically want two developed points (2 SRPs @ 3m).',
  grid: {
    perPoint: [
      { id: 'srp1', label: '1st SRP (developed point)', marks: 3 },
      { id: 'srp2', label: '2nd SRP (developed point)', marks: 3 },
    ],
    shorthand: '2 SRPs @ 3m = 6m',
    ruleNote:
      'Each developed point is worth 3 marks at OL. A “brief explanation” closer wants two of them — one developed sentence banks 3, but the second 3-mark SRP is left behind unless you give a second point.',
    cite: MSOL('p.12, p.18 (2 SRPs @ 3m closers; SRP = 3 marks at OL)'),
  },
  scripts: [
    {
      id: 'geo5-a',
      label: 'Script A',
      persona: 'One point, then stops',
      attempts: [
        {
          id: 'geo5-a-1',
          text: 'One developed, factual point explaining the cause — then the answer ends.',
          key: { srp1: 3, srp2: 0 },
          keyNote: 'One SRP banked (3 of 6). The closer wanted two developed points, and the second 3-mark SRP is simply unclaimed. At OL the marks are bigger per point (3, not 2) — but you still have to give the number the question asks for.',
        },
      ],
      embodies: {
        behaviour: 'Gives one developed point on a two-SRP closer — forfeiting the second 3-mark SRP.',
        cite: MSOL('p.12'),
      },
    },
    {
      id: 'geo5-b',
      label: 'Script B',
      persona: 'Two developed points',
      attempts: [
        {
          id: 'geo5-b-1',
          text: 'Two distinct developed points, each a clear factual statement explaining the cause.',
          key: { srp1: 3, srp2: 3 },
          keyNote: 'Two SRPs at 3 marks each. Full 6/6 — the “brief explanation” was really an instruction to give two developed points.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-geo5',
    rule: 'At OL, each SRP is 3 marks — give the number the closer asks for.',
    detail:
      'Ordinary Level Geography pays 3 marks per Significant Relevant Point (Higher pays 2), and “explain briefly” closers usually want two. One point banks 3; a second developed point banks the other 3. Match the SRP count the part expects.',
    cite: MSOL('p.12'),
  },
};

// ───────────────── Geo6 · OS sketch-map skills marks ─────────────────

const GEO6: GridSession = {
  mode: 'grid',
  id: 'geo-sketch-map',
  subject: 'geography',
  level: 'higher',
  title: 'Show it AND label it',
  cue: 'OS map (Part A)',
  question:
    'On the 20-mark Ordnance Survey question, a candidate must draw a half-scale sketch and “correctly show and label” four features. Each feature is worth 4 marks: Shown 3 (graded) + Label 1. How do three ways of drawing the same feature score?',
  questionNote:
    'Question authored for this exercise. The Part A OS sketch grid is real: “Sketch Outline 4 marks; 4 features @ 4 marks each — Shown 3 marks (graded 3/1/0), Label 1 mark”, with the showing/labelling interdependence rules quoted from the 2025 scheme.',
  grid: {
    perPoint: [
      { id: 'shown', label: 'Shown (feature located on the sketch)', marks: 3 },
      { id: 'label', label: 'Label', marks: 1 },
    ],
    shorthand: 'per feature · Shown 3 + Label 1',
    ruleNote:
      'Showing and labelling are locked together. “If not labelled, 0 marks for showing” — so an unlabelled feature scores nothing, however accurately it is drawn. But a labelled feature that was traced (or drawn from only a section of the map) keeps its label mark: “lose … 3 marks for showing per item. Allow labelling marks only.” Using the aerial photograph instead of the OS map scores 0 for the whole sketch.',
    cite: MS('p.5 (Part A OS sketch grid and rules)'),
  },
  scripts: [
    {
      id: 'geo6-a',
      label: 'Script A',
      persona: 'Perfectly placed — no label',
      attempts: [
        {
          id: 'geo6-a-1',
          text: 'Draws the river’s course in exactly the right place on the sketch, accurate and proportionate — but never writes its name beside it or in a key.',
          key: { shown: 0, label: 0 },
          keyNote:
            'The scheme is blunt: “If not labelled, 0 marks for showing.” No label means the 3 showing marks vanish too — an accurate, well-placed feature scores 0/4. The single word of the label was carrying three marks behind it.',
        },
      ],
      embodies: {
        behaviour: 'Locates a feature accurately but leaves it unlabelled — which zeroes the showing marks as well as the label.',
        cite: MS('p.5'),
      },
    },
    {
      id: 'geo6-b',
      label: 'Script B',
      persona: 'Shown and labelled',
      attempts: [
        {
          id: 'geo6-b-1',
          text: 'Shows the feature in roughly the right location and proportion, and labels it clearly on the sketch.',
          key: { shown: 3, label: 1 },
          keyNote:
            '“Reasonable accuracy (location and proportion) for full showing marks”, plus the label — the full 4/4. Note the bar is reasonable accuracy, not perfection.',
        },
      ],
    },
    {
      id: 'geo6-c',
      label: 'Script C',
      persona: 'Traced it',
      attempts: [
        {
          id: 'geo6-c-1',
          text: 'Traces the OS map rather than drawing a sketch, but labels each of the four features correctly.',
          key: { shown: 0, label: 1 },
          keyNote:
            'Tracing forfeits the showing marks — “lose … 3 marks for showing per item. Allow labelling marks only.” The correct labels still bank 1 mark each; the showing marks are gone. Draw the sketch; don’t trace it.',
        },
      ],
      embodies: {
        behaviour: 'Traces the map instead of sketching it, keeping only the labelling marks per feature.',
        cite: MS('p.5'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo6',
    rule: 'On the OS sketch, a feature has to be shown AND labelled.',
    detail:
      'Each feature is 4 marks — 3 for showing, 1 for the label — but they are linked: “If not labelled, 0 marks for showing.” An unlabelled feature scores nothing; a traced sketch keeps only the label marks. Label every feature, and draw rather than trace.',
    cite: MS('p.5'),
  },
};

// ───────────────── Geo7 · Describe vs develop — the SRP cap ─────────────────

const GEO7: ScaleSession = {
  mode: 'scale',
  id: 'geo-describe-cap',
  subject: 'geography',
  level: 'higher',
  title: 'Description isn’t formation',
  cue: 'Examine',
  question:
    'The question asks how a landform of deposition was FORMED. The candidate writes a long, accurate description of what the landform looks like — its shape, size and setting — but never explains the process that built it. The examination part is worth 14 SRPs (28 marks). How far can this go?',
  questionNote:
    'Scenario authored for this exercise. The cap is the scheme’s recurring rule for the landform-formation part: a description of the landform that never reaches its formation is capped at 2 SRPs.',
  scale: {
    name: 'Description-only · SRP cap',
    levels: srpScale([0, 4, 28]),
    notes: [
      'The examination is worth up to 14 SRPs (28 marks) when it explains formation.',
      'A right-landform answer that only DESCRIBES the landform, never its formation, is capped: “Max of 2 x SRPs if there is merely a description of landform without a reference to formation.”',
      'That cap is 4 marks — a hard ceiling, not a slow bleed. Pages of accurate description cannot pass it.',
      'This is different from answering the wrong process (0 marks): here the landform is right, but description is not explanation.',
    ],
    cite: MS('p.9 (description-without-formation cap)'),
  },
  scripts: [
    {
      id: 'geo7-a',
      label: 'The script',
      persona: 'Describes the postcard, not the process',
      work: [
        'Two paragraphs on how the spit looks: its length, its curved end, the lagoon behind it, where it sits on the coast.',
        'Vivid, accurate, well written.',
        'Never says how deposition built it — no longshore drift, no loss of energy, no material dropped.',
      ],
      keyLevelId: 'm4',
      keyNote:
        'Everything is correct and relevant to the landform — but it is description, not formation. The scheme caps “merely a description of landform without a reference to formation” at 2 SRPs, so the whole account tops out at 4 marks of the 28 available. The fix is one word repeated: because. Every feature described has to be tied to the process that made it.',
      embodies: {
        behaviour: 'Describes the finished landform in detail but never explains the process of formation the question asked for — hitting the 2-SRP cap.',
        cite: MS('p.9'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo7',
    rule: 'Describing the landform is not explaining how it formed.',
    detail:
      'A “how was it formed” part pays for the process, not the postcard. “Merely a description of landform without a reference to formation” is capped at 2 SRPs (4 marks) — however long and accurate the description. Tie every feature back to the process that built it.',
    cite: MS('p.9'),
  },
};

// ───────────────── Geo8 · Half a question halves the ceiling ─────────────────

const GEO8: ScaleSession = {
  mode: 'scale',
  id: 'geo-rock-ceiling',
  subject: 'geography',
  level: 'higher',
  title: 'Half the question, half the marks',
  cue: 'Examine',
  question:
    'The question asks how DIFFERENT rock types produce distinctive landscapes — plural, at least two. The candidate examines only ONE rock type (limestone) and its karst landscape, in real depth, for two full pages. The examination is worth 11 SRPs. How far can a one-rock answer go?',
  questionNote:
    'Scenario authored for this exercise. The cap is the scheme’s explicit half-question ceiling on the Rocks and Landscapes part: examine only one rock type and the whole examination is capped at 6 SRPs, however good it is.',
  scale: {
    name: 'One-rock answer · SRP cap',
    levels: srpScale([0, 12, 22]),
    notes: [
      'The examination is worth up to 11 SRPs (22 marks) when it examines two or more rock types.',
      'A question set on “different rock types” (plural) needs at least two examined.',
      'The scheme caps a one-rock answer: “Max 6 x SRPs if there is only one rock type and landscape examined.”',
      'That cap is 12 marks — reached at one rock. The 11th SRP the answer never earns is not lost to weakness; it is walled off because only half the question was attempted.',
      'This ceiling recurs across the paper (e.g. “Max 7 x SRPs if only one factor examined”). A plural question always wants both halves.',
    ],
    cite: MS('p.6 (one-rock-type SRP cap)'),
  },
  scripts: [
    {
      id: 'geo8-a',
      label: 'The script',
      persona: 'One rock, examined beautifully',
      work: [
        'Two pages on limestone and karst: solution, joints and bedding planes, swallow holes, limestone pavement, caverns.',
        'Accurate, well-sequenced, correctly labelled diagram.',
        'Only one rock type is ever examined — no second rock and landscape.',
      ],
      keyLevelId: 'm12',
      keyNote:
        'The work is easily strong enough for 11 SRPs — but the scheme caps a one-rock answer at 6 SRPs (12 marks). The question said “rock types”, plural, and half of it went unanswered. A second, thinner rock-and-landscape (say granite uplands) would have unlocked the top half of the marks. Depth in one place cannot substitute for the breadth the question demanded.',
      embodies: {
        behaviour: 'Examines only one rock type on a plural “rock types” question, hitting the scheme’s 6-SRP one-rock ceiling.',
        cite: MS('p.6'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo8',
    rule: 'A plural question wants both halves — one half is capped.',
    detail:
      'When a question names two things (two rock types, two factors, two challenges), the scheme caps a one-sided answer — “Max 6 x SRPs if there is only one rock type and landscape examined.” Give the second half, even briefly; depth in one half cannot pass the ceiling.',
    cite: MS('p.6'),
  },
};

// ───────────────── Geo9 · Anchor it to a named region ─────────────────

const GEO9: ScaleSession = {
  mode: 'scale',
  id: 'geo-region-anchor',
  subject: 'geography',
  level: 'higher',
  title: 'No region, no marks',
  cue: 'Examine',
  question:
    'The question asks the candidate to examine factors influencing an economic activity IN A REGION they have studied. The answer is a fluent, accurate account of the factors in general — but it never names or clearly points to a specific region. The examination is worth 13 SRPs. What does it score?',
  questionNote:
    'Scenario authored for this exercise. The scheme’s regional questions carry an explicit zero rule: examination not anchored to a named or clearly inferred region scores nothing, regardless of quality.',
  scale: {
    name: 'Region-less answer · credit',
    levels: srpScale([0, 26]),
    notes: [
      'The examination is worth up to 13 SRPs (26 marks) when it is anchored to a region.',
      'The scheme is absolute: “Examination without link to a named or clearly inferred region 0 marks.”',
      'The region can be named outright or “clearly inferred” — but a purely general account anchors to nowhere.',
      'This is different from the wrong-process zero: here the content is fine, but with no place to attach it, the examiner has nothing to credit.',
    ],
    cite: MS('p.16 (region-anchor zero rule)'),
  },
  scripts: [
    {
      id: 'geo9-a',
      label: 'The script',
      persona: 'Textbook-perfect, placeless',
      work: [
        'A well-organised account of the factors — climate, relief, markets, labour — influencing the activity.',
        'Every statement is geographically accurate.',
        'No region is ever named, and none can be clearly inferred from the detail given.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Everything is correct in the abstract, but the scheme awards a region-less examination 0 marks. One named region in the opening line — and detail specific enough to infer it — would have turned the same 13 SRPs live. In Regional Geography the region is not decoration; it is the thing the marks attach to.',
      embodies: {
        behaviour: 'Examines the factors in general without linking them to a named or clearly inferred region — the scheme’s automatic zero.',
        cite: MS('p.16'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo9',
    rule: 'A regional answer with no region scores zero.',
    detail:
      'Regional questions demand a place: “Examination without link to a named or clearly inferred region 0 marks.” Correct, general geography earns nothing until it is pinned to a specific region. Name the region early and keep the detail specific enough to prove it.',
    cite: MS('p.16'),
  },
};

// ───────────────── Geo10 · The graph that names itself ─────────────────

const GEO10: GridSession = {
  mode: 'grid',
  id: 'geo-graph-skills',
  subject: 'geography',
  level: 'higher',
  title: 'A title is not the chart’s name',
  cue: 'Draw a suitable graph',
  question:
    'On the 16-mark “draw a suitable graph” task, the marks are Title 2, each axis named 1, and each data item plotted (graded 2/1/0). A candidate draws a neat, accurate bar chart. How do the title and axis marks fall for three versions of the same chart?',
  questionNote:
    'Question authored for this exercise. The graph grid is real: “Title 2 marks; Vertical axis named 1; Horizontal axis named 1; 6 items illustrated graded 2/1/0”, with the title and graph-paper rules quoted from the 2025 scheme.',
  grid: {
    perPoint: [
      { id: 'title', label: 'Title (refers to chart content)', marks: 2 },
      { id: 'axes', label: 'Both axes named', marks: 2 },
    ],
    shorthand: 'Title 2 · Axes 1 + 1',
    ruleNote:
      'The title marks pay for content, not the chart’s category: “Naming of graph/chart type not sufficient for title mark. The title must have reference to chart content.” Writing “Bar Chart” across the top earns nothing; “Life expectancy by continent, 2023” earns the 2. A separate, invisible rule: “If graph paper is not used deduct 2 marks from total” — so an otherwise-perfect graph drawn on blank paper loses 2 before marking even starts.',
    cite: MS('p.31 (graph grid, title and graph-paper rules)'),
  },
  scripts: [
    {
      id: 'geo10-a',
      label: 'Script A',
      persona: 'Labels it “Bar Chart”',
      attempts: [
        {
          id: 'geo10-a-1',
          text: 'Writes “Bar Chart” as the title. Names both axes correctly (“Continent” / “Life expectancy in years”).',
          key: { title: 0, axes: 2 },
          keyNote:
            'The axes are named, so those 2 marks are safe — but “Bar Chart” names the chart type, not its content. The scheme: “Naming of graph/chart type not sufficient for title mark.” The title mark is simply forfeited. A title describing what the data shows would have banked it.',
        },
      ],
      embodies: {
        behaviour: 'Uses the chart type (“Bar Chart”) as the title, which the scheme rules insufficient for the title mark.',
        cite: MS('p.31'),
      },
    },
    {
      id: 'geo10-b',
      label: 'Script B',
      persona: 'Titled it, forgot the axes',
      attempts: [
        {
          id: 'geo10-b-1',
          text: 'Titles it “Average life expectancy by continent, 2023”. Draws and plots the bars accurately but never writes what either axis represents.',
          key: { title: 2, axes: 0 },
          keyNote:
            'A content title banks the 2 title marks. But unnamed axes score 0 for naming — the examiner cannot assume the reader knows what the numbers or categories are. The two axis marks are the cheapest on the page and they were left blank.',
        },
      ],
    },
    {
      id: 'geo10-c',
      label: 'Script C',
      persona: 'Title and axes, both there',
      attempts: [
        {
          id: 'geo10-c-1',
          text: 'Titles it “Average life expectancy by continent, 2023” and names both axes clearly.',
          key: { title: 2, axes: 2 },
          keyNote:
            'A content-bearing title (2) and both axes named (1 + 1). The full 4 marks of the frame, before a single bar is even graded. These are the marks that vanish for nothing when a candidate rushes the labelling.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-geo10',
    rule: 'Title the data, name the axes, use the graph paper.',
    detail:
      'On graph questions, “naming of graph/chart type is not sufficient for the title mark” — the title must describe the content. Name both axes, and draw on graph paper (blank paper is a flat −2). These framing marks are free and routinely dropped.',
    cite: MS('p.31'),
  },
};

// ───────────────── Geo11 · The Investigation must be yours ─────────────────

const GEO11: ScaleSession = {
  mode: 'scale',
  id: 'geo-gi-teacher',
  subject: 'geography',
  level: 'higher',
  title: 'The teacher can’t do it for you',
  cue: 'Geographical Investigation',
  question:
    'In the Planning section of the Geographical Investigation (5 marks), a candidate writes up a plan that describes, accurately, the arrangements the teacher made — the teacher chose the site, booked the trip, prepared the equipment and set the tasks. How does the Planning section score?',
  questionNote:
    'Scenario authored for this exercise. The GI marking rules state the Planning marks reward the candidate’s own planning; work done solely by the teacher scores nothing, and aims/plans must be specific and qualified.',
  scale: {
    name: 'Planning section · credit',
    levels: srpScale([0, 5]),
    notes: [
      'Planning is worth 5 marks: 4 SRPs @ 1 mark plus 1 Coherence/Linkage mark.',
      'The scheme: “Work completed solely by the teacher = 0 marks.”',
      'Statements must be the candidate’s own and qualified — “All statements must be qualified e.g. practicing equipment where/how/why?”',
      'Aims elsewhere “must relate to investigation and must be specific and qualified.”',
    ],
    cite: MS('p.62 (GI Planning rules)'),
  },
  scripts: [
    {
      id: 'geo11-a',
      label: 'The script',
      persona: 'Reports the teacher’s plan',
      work: [
        'Describes how the teacher selected the location and the route.',
        'Notes that the teacher assembled and tested the equipment.',
        'Lists the tasks the teacher assigned to the class.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Every line is true — and every line is the teacher’s planning, not the candidate’s. The scheme awards work “completed solely by the teacher” 0 marks. The Planning section rewards what YOU did to plan: what you decided to gather, how you would gather it, how you prepared — each stated specifically. Written in the first person and qualified, this same trip yields the full 5.',
      embodies: {
        behaviour: 'Reports planning done entirely by the teacher, which the GI scheme scores at 0.',
        cite: MS('p.62'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo11',
    rule: 'Investigation marks reward YOUR planning, not the teacher’s.',
    detail:
      'In the Geographical Investigation, “work completed solely by the teacher = 0 marks.” Write the Planning and Gathering as your own decisions and actions, specific and qualified (where / how / why) — not a report of what the teacher arranged.',
    cite: MS('p.62'),
  },
};

// ───────────────── Geo12 · Qualify the activity statement ─────────────────

const GEO12: GridSession = {
  mode: 'grid',
  id: 'geo-gi-qualify',
  subject: 'geography',
  level: 'higher',
  title: '“I recorded the results” — and?',
  cue: 'Geographical Investigation',
  question:
    'In the Gathering of Data section (9 SRPs @ 2 marks per method), an SRP is earned by an activity statement that says HOW or WHERE the work was done. A bare statement of the activity is not enough. How do two write-ups of the same fieldwork step score?',
  questionNote:
    'Question authored for this exercise. The GI Gathering rules state that simple activity statements are insufficient and must be qualified (how / where) to earn an SRP.',
  grid: {
    perPoint: [{ id: 'srp', label: 'SRP (qualified activity statement)', marks: 2 }],
    shorthand: 'each SRP · 2m',
    ruleNote:
      'The scheme lists the trap by name: “Simple statements are not sufficient e.g. I observed the features, I recorded the results, I sketched the landform etc.” To score, “there must be some qualification of the statement e.g. how/where?” The gathering section is activity-based reporting — the marks are for the method, and a method is only a method once you say how and where it was carried out.',
    cite: MS('p.63 (GI Gathering — qualification rule)'),
  },
  scripts: [
    {
      id: 'geo12-a',
      label: 'Script A',
      persona: 'Bare activity statements',
      attempts: [
        {
          id: 'geo12-a-1',
          text: 'I measured the width of the river. I recorded the results in a table.',
          key: { srp: 0 },
          keyNote:
            'This is exactly the scheme’s worked example of what does NOT score: “I recorded the results” with no qualification. Which point on the river? With what? How? The examiner needs a method, not an announcement that a method existed. 0 SRPs.',
        },
      ],
      embodies: {
        behaviour: 'Gives bare activity statements (“I recorded the results”) that the GI scheme names as insufficient for an SRP.',
        cite: MS('p.63'),
      },
    },
    {
      id: 'geo12-b',
      label: 'Script B',
      persona: 'Qualified — how and where',
      attempts: [
        {
          id: 'geo12-b-1',
          text: 'At three cross-sections 50 m apart, I measured river width by stretching a tape from bank to bank at the water’s edge and reading it to the nearest 10 cm.',
          key: { srp: 2 },
          keyNote:
            'Same activity, now qualified: where (three cross-sections, 50 m apart), how (tape bank to bank, read to 10 cm). That is a method the examiner can picture and credit. 2 marks — one SRP — and every gathering sentence can be built this way.',
        },
      ],
    },
  ],
  takeaway: {
    id: 'codex-geo12',
    rule: 'In the Investigation, say HOW and WHERE — not just what.',
    detail:
      'Gathering-of-data SRPs reward qualified method: “simple statements are not sufficient (I observed…, I recorded…)” — “there must be some qualification e.g. how/where?” Turn every “I measured X” into “I measured X, at …, using …, by …”.',
    cite: MS('p.63'),
  },
};

// ───────────────── Geo13 · Right answer, wrong section ─────────────────

const GEO13: ScaleSession = {
  mode: 'scale',
  id: 'geo-gi-section',
  subject: 'geography',
  level: 'higher',
  title: 'Right answer, wrong section',
  cue: 'Geographical Investigation',
  question:
    'A candidate writes excellent conclusions and evaluations — but writes them inside the Gathering-of-Data section of the reporting booklet, not in the Results / Conclusions / Evaluation section. The Results section is worth 30 marks. How much of that can the misplaced material earn?',
  questionNote:
    'Scenario authored for this exercise. The GI scheme restricts credit to material that appears in the correct section of the reporting booklet, and bars double-marking of gathering material as results.',
  scale: {
    name: 'Misplaced conclusions · credit',
    levels: srpScale([0, 30]),
    notes: [
      'Results, Conclusions and Evaluation carry 30 marks — three headings, marked only where they belong.',
      'The scheme: “Marks only awarded for Results / Conclusions / Evaluations if in the appropriate section of the reporting booklet.”',
      'The Gathering section states plainly: “No marks for results in this written section.”',
      'And material is credited once: “No double marking of information relating to issues mentioned in Section 3.”',
    ],
    cite: MS('p.63–64 (GI section-placement rules)'),
  },
  scripts: [
    {
      id: 'geo13-a',
      label: 'The script',
      persona: 'Good work, filed in the wrong box',
      work: [
        'The Gathering section contains a strong set of conclusions and a thoughtful evaluation.',
        'The Results / Conclusions / Evaluation section is left thin — the analysis is all back in Gathering.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'The thinking is genuinely good, but it is in the wrong section, and the scheme awards Results / Conclusions / Evaluation marks only where they belong. Gathering is for how you gathered — “no marks for results in this written section.” The 30-mark section stays empty of credit. The booklet’s headings are not suggestions; they tell the examiner where to look for each type of mark.',
      embodies: {
        behaviour: 'Places conclusions and evaluation in the Gathering section, where the scheme awards them no marks.',
        cite: MS('p.64'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo13',
    rule: 'Marks live in their section of the booklet.',
    detail:
      'The Investigation is marked section by section: “marks only awarded for Results / Conclusions / Evaluations if in the appropriate section,” and “no marks for results” in the Gathering section. Put each type of content under its own heading — right answer, wrong box, scores nothing.',
    cite: MS('p.64'),
  },
};

// ───────────────── Geo14 · Two different ways to show results ─────────────────

const GEO14: ScaleSession = {
  mode: 'scale',
  id: 'geo-gi-presentation',
  subject: 'geography',
  level: 'higher',
  title: 'Two charts, one method',
  cue: 'Geographical Investigation',
  question:
    'The Organisation & Presentation section (20 marks) needs TWO different forms of presentation and awards a 4-mark Overall Coherence mark on top. A candidate presents their results as two bar charts — same method twice. How does the Overall Coherence mark fall?',
  questionNote:
    'Scenario authored for this exercise. The GI Presentation rules require two different forms of presentation, and bar the Overall Coherence mark where only one method is evident.',
  scale: {
    name: 'Presentation Overall Coherence · /4',
    levels: srpScale([0, 4]),
    notes: [
      'Presentation is 20 marks: up to 4 SRPs per method @ 2 marks, plus a 4-mark graded Overall Coherence.',
      'The scheme: “There must be two different forms of presentation of results e.g. graphs, chart, map, table, sketch.”',
      'And the Coherence gate: “Cannot be awarded Overall Coherence marks if only one method of presentation is evident.”',
      'Two bar charts count as one method — so the 4 Coherence marks are locked out (the SRPs for the one method still stand).',
    ],
    cite: MS('p.65 (GI Presentation rules)'),
  },
  scripts: [
    {
      id: 'geo14-a',
      label: 'The script',
      persona: 'Same method, drawn twice',
      work: [
        'Results shown as a bar chart.',
        'Then shown again as a second bar chart.',
        'No table, map, pie chart or sketch — only bar charts.',
      ],
      keyLevelId: 'm0',
      keyNote:
        'Two graphs, but one method — and the scheme cannot award Overall Coherence “if only one method of presentation is evident.” The 4 Coherence marks are gone. Swapping the second bar chart for a table or a pie chart (a genuinely different form) both satisfies the two-methods rule and reopens the Coherence mark. Variety of form, not quantity, is what this section pays for.',
      embodies: {
        behaviour: 'Uses the same presentation method twice, forfeiting the Overall Coherence mark that requires two different forms.',
        cite: MS('p.65'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo14',
    rule: 'Present results two DIFFERENT ways.',
    detail:
      'The Presentation section needs “two different forms of presentation” and “cannot be awarded Overall Coherence marks if only one method of presentation is evident.” Pair a graph with a table or a map — not two of the same — to claim the coherence marks.',
    cite: MS('p.65'),
  },
};

// ───────────────── Geo15 · Depth over breadth in Options ─────────────────

const GEO15: ScaleSession = {
  mode: 'scale',
  id: 'geo-options-aspects',
  subject: 'geography',
  level: 'higher',
  title: 'Three aspects deep, not ten shallow',
  cue: 'Options essay',
  question:
    'An 80-mark Options essay is marked as 3 aspects @ 20 marks (identify 4 + discussion 8 SRPs) or 4 aspects @ 15. A candidate races through eight aspects, giving each a single thin sentence. How does one of those thin aspects score against a fully developed one?',
  questionNote:
    'Scenario authored for this exercise. The Options marking scheme structures the essay as 3 or 4 developed aspects and advises depth over a superficial treatment of many points.',
  scale: {
    name: 'One aspect · marks',
    levels: srpScale([0, 6, 20]),
    notes: [
      'Each aspect is worth up to 20 marks: 4 for identifying it, 16 (8 SRPs) for the discussion.',
      'Only 3 (or 4) aspects are marked — the scheme selects the 3-aspect or 4-aspect grid to the candidate’s benefit; a 5th, 6th, 7th aspect earns nothing.',
      'The scheme’s explicit steer: “It is better to discuss three or four aspects of the theme in some detail, rather than to give a superficial treatment of a large number of points.”',
      'A one-sentence aspect scores its 4-mark identification plus perhaps a single SRP (≈6); the same effort spent developing it reaches 20.',
    ],
    cite: MS('p.46–47 (Options structure and depth note)'),
  },
  scripts: [
    {
      id: 'geo15-a',
      label: 'The script',
      persona: 'Breadth without depth',
      work: [
        'Names eight aspects of the theme.',
        'Gives each a single, thin sentence — the point is identified but never developed.',
        'Only the strongest three or four aspects will be marked at all.',
      ],
      keyLevelId: 'm6',
      keyNote:
        'Each thin aspect scores its identification (4) and maybe one SRP — around 6 of a possible 20 — and the extra aspects beyond the marked three or four score nothing at all. The scheme says it outright: better to take “three or four aspects in some detail” than “a superficial treatment of a large number of points.” The same page-count, poured into three developed aspects, is the difference between a mid-grade and a top-grade essay.',
      embodies: {
        behaviour: 'Treats many aspects superficially instead of developing three or four — the approach the scheme advises against.',
        cite: MS('p.46'),
      },
    },
  ],
  takeaway: {
    id: 'codex-geo15',
    rule: 'Develop three or four aspects — don’t list ten.',
    detail:
      'Options essays mark 3 aspects @ 20 or 4 @ 15; extra aspects score nothing. “It is better to discuss three or four aspects in some detail, rather than a superficial treatment of a large number of points.” Pick your strongest few and go deep.',
    cite: MS('p.46'),
  },
};

export const GEOGRAPHY_CHAIR: ChairSubject = {
  id: 'geography',
  label: 'Geography',
  tagline: 'SRPs, diagrams and coherence — the anatomy of a Geography mark.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [GEO1, GEO2, GEO3, GEO4, GEO5, GEO6, GEO7, GEO8, GEO9, GEO10, GEO11, GEO12, GEO13, GEO14, GEO15],
  sources: [
    { label: 'SEC LC Geography HL marking scheme 2025 (examiner-reports/geography/2025-marking-scheme)' },
    { label: 'SEC LC Geography OL marking scheme 2025 (examiner-reports/geography/2025-ol-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Geography 2012 (examiner-reports/geography/2012-chief-examiner)' },
  ],
  coverageNote:
    'Higher sessions are verified against the 2025 HL scheme; the Ordinary session against the 2025 OL scheme. They span the SRP grammar, the diagram rule, the wrong-process zero, the description-without-formation SRP cap, the half-question SRP ceiling, the named-region zero, Part A Ordnance Survey and graph-drawing skills, the Options Overall Coherence and three-or-four-aspects rules, and the Geographical Investigation marks (own-work, qualified activity statements, correct-section placement and two-methods presentation). Note the SRP is worth 3 marks at OL (2 at HL), and OL has no Options essay / Overall Coherence grid. More OL sessions are being added.',
};
