export const meta = {
  name: 'jc-geography-cmdword-topup',
  description: 'Targeted top-up of critic-identified cue gaps (Distinguish, Measure, Identify, Suggest, Label, Account for) in the JC Geography Command-Word set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic per stem' } ],
}

const TXT = '/tmp/jc_geography_txt'

const SHARED = `
You author ONE Command-Word Reflex stem for JUNIOR CYCLE GEOGRAPHY (reformed NCCA spec, first examined 2022). COMMON LEVEL
only — every stem level MUST be 'common'. Single terminal paper, 360 marks, map/photo/graph heavy. The student taps the
COMMAND WORD then learns the demand + the marking trap.

CUE GRAMMAR: Name/State/Identify/Give/List = exact named term/example; count cues need that many. Describe = what it looks
like / the sequence. Explain/Account for/Give a reason = the cause/process. Calculate/Measure = a numeric map/data answer
(distance on 1:50,000 = map cm x 0.5 km; area in km2; temperature range; mean rainfall). Give the six-figure grid
reference / Match / Draw / Sketch / Mark / Label = the map skill (grid ref = eastings before northings; Label = add names
to a supplied diagram/sketch). Distinguish between / Compare = the contrast on the SAME feature for BOTH items. Suggest/
Predict = a plausible geography-based answer with reasoning.

THE TYPE: { id (kebab, prefix 'jcgeo-'), subjectId:'jc-geography', subjectLabel:'Geography (Junior Cycle)', level:'common',
questionRef ('2024 CL · Q5(c)'), stem (faithful to the paper; MUST contain commandWord verbatim; describe any map/photo/
graph in words), commandWord, demand (what THIS cue requires here), trap (the scheme-flagged mistake + marks consequence),
source ('SEC JC Geography {YEAR} CL marking scheme, Q… (…accepted answers…)'), marks (integer) }.

TAPPABILITY: commandWord is a consecutive word-token run in stem (multi-word cue = exact run).
GROUNDING (non-negotiable): a REAL SEC question from ${TXT}/jc-geography-YYYY-CL-{paper,marking-scheme}.txt (2022-2025).
grep/Read the paper + scheme. Do NOT invent question numbers, marks, or scheme wording. Stay within JC scope. If your slot
CANNOT be grounded (the cue genuinely does not occur 2022-2025), return found:false with grep evidence. Return data only.
`

const STEM_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
  level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
  stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
  trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
}
const ONE_SCHEMA = { type: 'object', required: ['found'], properties: { found: { type: 'boolean' }, note: { type: 'string' }, stem: { type: 'object', properties: STEM_PROPS } } }

const SLOTS = [
  { key: 'distinguish', want: `cue 'Distinguish between' (or 'Compare', or 'Give one difference between') on a real contrast (erosion vs deposition, developed vs developing country, nucleated vs dispersed settlement, weathering vs erosion, igneous vs sedimentary rock). Trap: only one side, or two non-contrasting facts.` },
  { key: 'measure-distance', want: `cue 'Measure' (or 'Calculate' framed as measure) the straight-line or road DISTANCE between two points on the 1:50,000 OS map, converting with the scale (map cm x 0.5 = km). Trap: scale-conversion slip / wrong units.` },
  { key: 'identify-feature', want: `cue 'Identify' a river/coastal/glacial feature, a settlement pattern, or a land use from an OS map or an aerial/satellite PHOTOGRAPH. Trap: confusing lookalike features; a description where a named feature is wanted.` },
  { key: 'suggest', want: `cue 'Suggest' — "Suggest one/two reasons why ..." on a population/settlement/location/economic pattern. Demand: a plausible geography-based reason. Trap: a guess with no geography.` },
  { key: 'label', want: `cue 'Label' — "Label the diagram / On the sketch map label ..." — adding the correct names to a supplied diagram or sketch (e.g. parts of a volcano, a river, a coastline). Distinct from Draw. Trap: wrong/missing labels.` },
  { key: 'account-for', want: `cue 'Account for' — "Account for ..." a weather/climate/geo-system pattern (e.g. why an area has high/low temperature, rainfall, population density). Demand: the cause/process. Trap: describing the pattern instead of giving the reason.` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE stem (level 'common') for this slot (or found:false with evidence).`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))
const stems = authored.filter(Boolean).filter((r) => r.found && r.stem).map((r) => r.stem)
log(`Authored ${stems.length}/${SLOTS.length} gap stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: STEM_PROPS },
  },
}
const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Geography (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem?\n` +
    `2. GROUNDING: real question at ${s.questionRef} (2022-2025 CL)? marks + marking rule match the scheme?\n` +
    `3. GEOGRAPHY SENSE + SCOPE: correct, within JC scope, right cue (method right for a skills stem), level exactly 'common'?\n` +
    `4. QUALITY: demand/trap specific, real marking pattern?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedStem (keep id, level 'common'). If sound, accept. If fabricated, reject.\n\nTHE STEM:\n${JSON.stringify(s, null, 2)}`,
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
return { kept, keptCount: kept.length, unfounded: authored.filter(Boolean).filter((r) => !r.found).map((r) => r.note || 'no note') }
