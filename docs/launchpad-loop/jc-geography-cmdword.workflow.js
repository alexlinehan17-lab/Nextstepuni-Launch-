export const meta = {
  name: 'jc-geography-cmdword',
  description: 'Author + adversarially verify Junior Cycle Geography (Common Level) Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, geography sense, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_geography_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE GEOGRAPHY (Ireland, reformed NCCA spec, first examined 2022). The
student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue
demands and the marking trap behind it.

EXAM SHAPE: a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 360 marks, ~2h, map/photo/graph heavy. EVERY
stem's level MUST be 'common'. Marking: accepted answers per part, often "any X from a list", named landform/process
answers; skills parts (grid refs, distance, area) have a single right answer.

JC-GEOGRAPHY CUE GRAMMAR (ground demands/traps in it):
 - 'Name' / 'State' / 'Identify' / 'Give' / 'List': the exact short answer(s) / a named example — precise term, no
   explanation; count cues need that many. Trap: a vague description where a NAMED feature/place is needed; fewer than asked.
 - 'Describe': say WHAT it looks like / what happens (the appearance or sequence), with detail. Trap: an undeveloped
   one-liner; confusing describe (what) with explain (why).
 - 'Explain' / 'Account for' / 'Give a reason' / 'Why': the CAUSE/process — the reason it happens ("because ..."). Trap:
   describing the feature instead of giving the process/reason; the marks are the cause.
 - 'Calculate' / 'Work out' / 'Measure': a numeric map/data answer — distance (1:50,000 → map cm × 0.5 km), area in km²,
   temperature range, total/mean rainfall. Trap: scale-conversion slip; wrong units; reading the graph axis wrong.
 - 'Give the ... grid reference' / 'Match' / 'Draw' / 'Sketch' / 'Mark' / 'Label': the map/skills task — a six-figure grid
   reference (eastings before northings), matching items, a labelled sketch map/diagram. Trap: grid-ref digits reversed
   (northings before eastings); an unlabelled sketch; a feature in the wrong place.
 - 'Distinguish between' / 'Compare': the contrast on the SAME feature for BOTH items (e.g. erosion vs deposition,
   developed vs developing, nucleated vs dispersed settlement). Trap: only one side, or two non-contrasting facts.
 - 'Suggest' / 'Predict': a plausible geography-based answer with reasoning. Trap: a guess with no geography.

THE TYPE (one object per stem):
  id            kebab, prefix 'jcgeo-', unique (e.g. 'jcgeo-explain-volcano-common')
  subjectId     MUST be exactly 'jc-geography'
  subjectLabel  'Geography (Junior Cycle)'
  level         MUST be 'common'
  questionRef   e.g. '2024 CL · Q4(b)(ii)' or '2023 CL · Q1'
  stem          the question stem, faithful to the paper (summarise a long stimulus briefly; if it needs a map/photo/graph,
                describe the essential detail in words). MUST contain commandWord verbatim.
  commandWord   the cue ('Name', 'State', 'Identify', 'Give', 'List', 'Describe', 'Explain', 'Account for', 'Calculate',
                'Measure', 'Match', 'Draw', 'Sketch', 'Mark', 'Label', 'Distinguish', 'Compare', 'Suggest', 'Predict')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question.
  trap          the scheme-flagged mistake for THIS cue + the marks consequence.
  source        'SEC JC Geography {YEAR} CL marking scheme, Q… (…accepted answers…)'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Multi-word cues ('Distinguish between', 'Account for') must appear as that exact run.

GROUNDING (non-negotiable): every stem is a REAL SEC JC Geography question (2022-2025; exams cancelled 2020-2021). Papers +
schemes at ${TXT}/ — jc-geography-YYYY-CL-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme guidance. Do
NOT invent question numbers, marks, or scheme wording. Stay within JC scope.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'study the map'). trap = a real marking
pattern. Prefer cue DIVERSITY (especially the skills cues — grid reference, Calculate distance/area — and Explain vs
Describe). Plain text.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: { type: 'array', items: { type: 'object',
      required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
        stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
        trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'skills-map-data', cues: 'Calculate, Measure, Give (grid reference), Match, Mark, Label, Sketch, Draw',
    topics: 'the SKILLS cues (the most-examined area) — "Give the six-figure grid reference of ...", "Calculate the straight-line distance ... (1:50,000)", "Calculate the area of ...", "Match the photo to the map", "Draw a sketch map and mark/label ...", "Using the climate graph, calculate the annual temperature range". Demand: the exact skill method/answer. Trap: grid-ref digits reversed; scale-conversion slip; unlabelled sketch; misreading the graph axis.' },
  { key: 'name-state-identify', cues: 'Name, State, Identify, Give, List',
    topics: 'the short-answer/named-example cues across all groups — "Name the landform at X", "State one effect of the earthquake", "Identify the type of plate boundary", "Name a river you have studied". Demand: the exact named term / a real named example; count cues need that many. Trap: a vague description where a named feature/place is needed; a generic answer where a STUDIED example is required; fewer than asked.' },
  { key: 'describe-explain', cues: 'Describe, Explain, Account for, Give a reason',
    topics: 'the describe vs explain cues — "Describe the formation of a volcano", "Explain how a meander forms", "Account for the high population density", "Give a reason why ...". Demand: Describe = what it looks like / the sequence; Explain/Account-for = the process/cause ("because ..."). Trap: describing when asked to explain (and vice versa); an undeveloped one-liner; missing the process reason.' },
  { key: 'distinguish-suggest', cues: 'Distinguish between, Compare, Suggest, Predict',
    topics: 'the contrast + reasoned-suggestion cues — "Distinguish between erosion and deposition", "Compare a developed and a developing country", "Suggest one way to manage coastal erosion", "Predict an effect of climate change". Demand: the contrast on the SAME feature for both / a plausible geography-based suggestion with reasoning. Trap: only one side of a contrast; a guess with no geography.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems, each with a DIFFERENT cue where possible, across years and groups (all level 'common'). Ground every stem/demand/trap/marks/citation in the paper + scheme. Make demand+trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: {
      id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
      level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
      commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
      source: { type: 'string' }, marks: { type: 'integer' } } },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Geography (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase; multi-word cue = exact run)? If not → fix.\n` +
    `2. GROUNDING: real question near ${s.questionRef} (2022-2025 CL)? marks + the marking rule in demand/trap match the scheme? else grounded:false.\n` +
    `3. GEOGRAPHY SENSE + SCOPE: demand/trap correct and within JC scope? Is the cue the RIGHT command word for what the question asks? (For a skills stem, is the method right — grid ref eastings-then-northings, distance scale?) level exactly 'common'?\n` +
    `4. QUALITY: demand specific to this cue+question (no filler)? trap a real marking pattern (named-example, count, describe-vs-explain, grid-ref order, scale slip)?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id, level 'common'). If sound, accept. If fabricated, reject.\n\n` +
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
  `Completeness critic for a Junior Cycle Geography (Common Level) Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) cue diversity — Name/State/Identify/Give/List, Describe, Explain/Account for, Calculate/Measure, the grid-reference/Match/Draw/Sketch/Label skills cues, Distinguish/Compare, Suggest/Predict; flag missing cues, (2) coverage across the four groups (Geographical skills — should be well represented, Physical world, Interaction, People/place/change), (3) whether the signature traps are present: grid-ref order, scale conversion, named-example required, describe-vs-explain, one-sided contrast. List concrete gap slots (each: cue + topic/group). All stems are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
