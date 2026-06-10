export const meta = {
  name: 'jc-science-cmdword-topup',
  description: 'Targeted top-up of critic-identified cue/strand gaps (Distinguish, Predict, Plot, Calculate, List, Earth-systems) in the JC Science Command-Word set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic per stem' } ],
}

const TXT = '/tmp/jc_science_txt'

const SHARED = `
You author ONE Command-Word Reflex stem for JUNIOR CYCLE SCIENCE (reformed NCCA spec, first examined 2019). COMMON LEVEL
only — every stem level MUST be 'common'. Single terminal paper, 360 marks, Section A short Qs + Section B long Qs.
The student taps the COMMAND WORD then learns the demand + the marking trap.

CUE GRAMMAR: State/Name/Give/List/Identify = exact named term(s); count cues ("List three") need that many distinct
points. Describe/Outline = the steps/what-happens in order. Explain/Why/Give a reason/Account for = the science cause
("because ..."). Calculate = formula + working + UNIT. Draw/Plot/Complete/Label = accurate graph/diagram/table (Plot =
plot the given data points then draw the line/curve). Distinguish between/Compare = the contrast on the SAME property for
BOTH things. Suggest/Predict = a plausible science-based answer (Predict = a forward inference of what will happen).

THE TYPE: { id (kebab, prefix 'jcsci-'), subjectId:'jc-science', subjectLabel:'Science (Junior Cycle)', level:'common',
questionRef ('2024 CL · Section B · Q14(c)'), stem (faithful to the paper; MUST contain commandWord verbatim; describe any
figure's essential detail in words), commandWord, demand (what THIS cue requires here), trap (the scheme-flagged mistake +
marks consequence), source ('SEC JC Science {YEAR} CL marking scheme, Q… (…accepted answers…)'), marks (integer) }.

TAPPABILITY: commandWord is a consecutive word-token run in stem (multi-word cue = exact run).
GROUNDING (non-negotiable): a REAL SEC question from ${TXT}/jc-science-YYYY-CL-{paper,marking-scheme}.txt (2022-2025).
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
  { key: 'distinguish', want: `cue 'Distinguish between' (or 'Compare', or 'Give one difference between') — e.g. distinguish between two related terms (renewable/non-renewable, series/parallel, element/compound, accuracy/precision, exothermic/endothermic). Trap: describing only one side, or two facts that don't contrast on the same property.` },
  { key: 'predict', want: `cue 'Predict' — a forward inference of what will happen if a variable changes (e.g. predict the effect on rate / on the bulb / on the organism). Trap: a guess with no science reasoning.` },
  { key: 'plot', want: `cue 'Plot' — "Plot the (given) points/data on the grid (and draw the line/curve)". A graphing question. Trap: wrong axes, unplotted/mis-plotted points, or no line drawn.` },
  { key: 'calculate-physical', want: `cue 'Calculate' on a PHYSICAL-world quantity NOT already covered — e.g. density (mass/volume), speed (distance/time), acceleration, electrical resistance or power. Demand: formula + working + UNIT. Trap: missing unit or no working shown.` },
  { key: 'earth-systems', want: `ANY cue on EARTH-AND-SPACE NON-cosmology Earth systems — the WATER cycle, the CARBON cycle, the Earth-Sun-Moon system (seasons / day & night / lunar phases / eclipses), or climate change evidence/initiatives. (The base set's Earth-and-Space stems are all astronomy; add an Earth-systems one.)` },
  { key: 'account-for-or-list', want: `EITHER cue 'Account for' / 'Give a reason' on a Chemical or Physical property (e.g. account for why a metal conducts / why a rate increased) OR cue 'List' with an explicit count ("List three ..."). Pick whichever is well-grounded in a real paper. Trap: restating the observation (Account for) / giving fewer than the number asked (List).` },
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
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'sciCorrect', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, sciCorrect: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: STEM_PROPS },
  },
}
const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Science (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem?\n` +
    `2. GROUNDING: real question at ${s.questionRef} (2022-2025 CL)? marks + marking rule match the scheme?\n` +
    `3. SCIENCE + LEVEL: scientifically correct, within JC scope, right cue, level exactly 'common'?\n` +
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
