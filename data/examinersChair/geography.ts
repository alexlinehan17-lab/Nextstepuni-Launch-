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

export const GEOGRAPHY_CHAIR: ChairSubject = {
  id: 'geography',
  label: 'Geography',
  tagline: 'SRPs, diagrams and coherence — the anatomy of a Geography mark.',
  offeredLevels: ['higher', 'ordinary'],
  sessions: [GEO1, GEO2, GEO3, GEO4, GEO5],
  sources: [
    { label: 'SEC LC Geography HL marking scheme 2025 (examiner-reports/geography/2025-marking-scheme)' },
    { label: 'SEC LC Geography OL marking scheme 2025 (examiner-reports/geography/2025-ol-marking-scheme)' },
    { label: 'Chief Examiner’s Report, Geography 2012 (examiner-reports/geography/2012-chief-examiner)' },
  ],
  coverageNote:
    'Higher sessions are verified against the 2025 HL scheme; the Ordinary session against the 2025 OL scheme. Note the SRP is worth 3 marks at OL (2 at HL), and OL has no Options essay / Overall Coherence grid. More OL sessions are being added.',
};
