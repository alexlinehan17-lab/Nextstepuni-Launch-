export const meta = {
  name: 'construction-cmdword',
  description: 'Author + adversarially verify Construction Studies Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, accuracy, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/construction_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert CONSTRUCTION STUDIES (Irish exam-technique tool) — the WRITTEN
THEORY paper. The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then
learns what that cue demands and the marking-scheme trap behind it.

EXAM SHAPE: Theory paper — HIGHER 300 marks, answer any FIVE (60 each); ORDINARY 200 marks, answer any FOUR (50 each).
The instructions state: drawings/sketches in PENCIL; "Neat freehand sketches to illustrate written descriptions should be
made"; "The name, sizes, dimensions and other necessary particulars of each material indicated must be noted on the
drawings." This is the key to the traps below.

CONSTRUCTION-STUDIES CUE GRAMMAR (ground demands/traps in it):
 - 'Discuss in detail, using notes and freehand sketches' / 'Describe' (the dominant cue): give DEVELOPED points WITH
   labelled freehand sketches — a text-only answer, or a bare list with no development/sketch, is capped. Depth + the
   sketch is what scores.
 - 'Draw … to a scale of 1:X' / 'Show … on your drawing' / 'Indicate': the answer is a DRAWN, LABELLED detail with the
   material names, sizes and dimensions noted; an unlabelled or undimensioned drawing loses the award points.
 - 'Calculate' (U-value etc.): use the formula (U = 1/ΣR), show the working, give the answer with UNITS (W/m²K); a missing
   formula/unit or wrong layer resistance loses marks even if part of the arithmetic is right.
 - 'State' / 'Name' / 'List' / 'Give (two reasons)': hand over the exact number of distinct, named points — the scheme
   awards per listed point; vague or fewer-than-asked answers cap the mark.
 - 'Explain' / 'Outline' / 'Recommend': give the reason/mechanism (or a justified recommendation), not just a name.

THE TYPE (one object per stem):
  id            kebab, prefix 'cons-', unique, includes cue + topic (e.g. 'cons-discuss-passive-house-hl')
  subjectId     MUST be exactly 'construction-studies'
  subjectLabel  'Construction Studies'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Q5(a)' or '2023 OL · Q3'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim. Keep it a stem (you may
                summarise the scenario briefly) — do not paste a whole multi-part question.
  commandWord   the cue (or multi-word cue like 'Discuss in detail', 'Calculate', 'Draw', 'Show', 'State', 'Give two')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (text-only where a sketch is required,
                unlabelled/undimensioned drawing, missing U-value formula/units, too few listed points). Point to the
                scheme's award structure where it bites.
  source        'LC Construction Studies {YEAR} {LEVEL} marking scheme, Q… ("…award points / scheme detail…")'
  marks         integer marks at stake (from the scheme; a whole question is 60 HL / 50 OL, a part is less)
  figureSpec    OPTIONAL — include ONLY if the cue genuinely depends on a diagram PRINTED in the question (e.g. "the
                detail shown", "the design shown"). Shape { year, level, questionRef, source ('paper'/'scheme'), describes,
                whyNeeded }. Most stems are self-contained from the text — do NOT force one. No real 'figure'/'src'.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem.

GROUNDING (non-negotiable): every stem is a REAL SEC LC Construction Studies question. Text of papers + schemes
(2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): construction-studies-YYYY-{HL,OL}-written.txt /
construction-studies-YYYY-{HL,OL}-marking-scheme.txt. grep/Read for the exact stem + scheme award. Do NOT invent question
numbers, marks, materials, or scheme wording. RECOMPUTE any U-value you cite.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'show your working',
'draw neatly'). trap = a real scheme-grounded rule. Prefer cue DIVERSITY: Discuss in detail, Describe, Draw, Show,
Indicate, Calculate, State, Name, List, Give two, Explain, Outline, Recommend. Plain text; unicode (×, °, ², ≤) fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
        properties: {
          id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
          level: { type: 'string', enum: ['higher', 'ordinary'] }, questionRef: { type: 'string' },
          stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
          trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'discuss-describe', cues: 'Discuss in detail, Describe',
    topics: 'the dominant essay-sketch cue — "Discuss in detail, using notes and freehand sketches…" on design-for-lifetime-use, sustainability/passive-house measures, condensation, services, best-practice detailing. Teach that the cue demands DEVELOPED points WITH labelled sketches; trap = text-only or an undeveloped list.' },
  { key: 'draw-show-indicate', cues: 'Draw, Show, Indicate',
    topics: 'the drawing cues — "Draw to a scale of 1:10 a vertical section through…", "Show on your drawing the typical detailing for…", "Indicate…". Teach the labelled, dimensioned detail (material names + sizes); trap = an unlabelled/undimensioned drawing. Add a figureSpec only if the question prints a detail the cue refers to.' },
  { key: 'calculate-state-give', cues: 'Calculate, State, Give, Name, List',
    topics: 'the technical/short cues — "Calculate the U-value of the wall" (U=1/ΣR, units W/m²K, RECOMPUTE), "State two functions of…", "Give two reasons why…", "Name…". Teach formula+units for Calculate and exact-number-of-named-points for State/Give; trap = missing units/formula or too few points.' },
  { key: 'explain-outline-recommend', cues: 'Explain, Outline, Recommend',
    topics: 'the reasoning cues — "Explain…", "Outline…", "Recommend…and give reasons" on thermal performance, insulation, ventilation, drainage, renewable energy, building science (timber decay, concrete). Teach reason/mechanism or justified recommendation, not a bare name; trap = naming without the why.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT command word where possible, spread across years 2021-2025. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation. Make the demand and trap specific to the exact question you cite.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Construction Studies Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + the scheme rule in demand/trap match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any construction error (wrong material/dimension, wrong U-value that does not recompute as U=1/ΣR, wrong detail)?\n` +
    `4. QUALITY: demand specific to cue+question (no banned filler)? trap a real scheme pattern (text-only where a sketch is required, unlabelled drawing, missing U-value units, too few points)?\n` +
    `5. FIGURE: if a figureSpec is present, is it real and does the cue truly need a printed diagram? else drop it. If the stem text already conveys the cue, no figure needed.\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated, reject.\n\n` +
    `THE STEM:\n${JSON.stringify(s, null, 2)}`,
    { label: `verify:${s.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ stem: s, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.stem)
  else if (r.v.verdict === 'fix' && r.v.fixedStem) kept.push({ ...r.stem, ...r.v.fixedStem })
}
log(`Verify: ${kept.length}/${stems.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a Construction Studies Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — Discuss dominates the real paper, but the set should ALSO cover Draw/Show, Calculate (U-value), State/Give, and Explain/Outline; flag if any of these is missing, (3) whether the signature "sketch-required" trap (Discuss/Show needs a labelled freehand sketch, text-only is capped) AND a U-value Calculate are both present, (4) duplicate cue+topic. List concrete gap slots to top up (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
