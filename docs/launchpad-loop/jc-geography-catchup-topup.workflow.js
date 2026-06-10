export const meta = {
  name: 'jc-geography-catchup-topup',
  description: 'Top-up critic-identified signature gaps (area, sketch map, river/coastal landforms, volcano vs fold mountain, population pyramid, synoptic chart) in the JC Geography Catch-Up set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic re-checks geography correctness' } ],
}

const TXT = '/tmp/jc_geography_txt'

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for JUNIOR CYCLE GEOGRAPHY (reformed NCCA spec, first examined 2022). COMMON
LEVEL only — level MUST be 'common'. A card helps a student recover marks: gist + the ONE highest-leverage move + a
SELF-CONTAINED check + correct model answer. 360-mark paper, map/photo/graph heavy.

THE CARD: { id (kebab, prefix 'jcgeo-'), subjectId:'jc-geography', topicId, subjectLabel:'Geography (Junior Cycle)',
topicLabel (EXACT name), focus, level:'common', gist, oneMove:{label,text}, check:{prompt (SELF-CONTAINED — embed the
figures/place facts; describe any map/photo/graph in words), modelAnswer (correct), needed (>=2 marking points)}, source
('Topic … — SEC JC Geography {YEAR} CL, Q… + marking scheme (…accepted answers…)'), marksWeight (integer) }.

CORRECTNESS (hard): facts/place names/processes/skill methods correct and within JC scope. Skill methods must be exact:
area on a 1:50,000 OS map = count grid squares (each 1 km x 1 km = 1 km2). GROUNDING: real SEC questions + schemes at
${TXT}/jc-geography-YYYY-CL-{paper,marking-scheme}.txt (2022-2025). Do NOT invent question numbers/marks/wording. Return
data only.
`

const CARD_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
  subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
  level: { type: 'string', enum: ['common'] }, gist: { type: 'string' },
  oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
  check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
  source: { type: 'string' }, marksWeight: { type: 'integer' },
}
const ONE_SCHEMA = { type: 'object', required: ['card'], properties: { card: { type: 'object', required: ['id'], properties: CARD_PROPS } } }

const SLOTS = [
  { key: 'area-os-map', want: `topicId jc-geography-0-0 · topicLabel 'OS maps: grid references, scale & distance' · MEASURING AREA on a 1:50,000 OS map: each grid square is 1 km x 1 km = 1 km2, so area = number of squares across x number up (count full + part squares). Ground in a real area question (e.g. 2025 Q9 area = 108 km2). The check gives map dimensions in words.` },
  { key: 'sketch-map', want: `topicId jc-geography-0-2 · topicLabel 'OS maps: identifying features, sketch maps & settlement patterns' · DRAWING A SKETCH MAP: a proportioned frame (not a tracing), each named feature SHOWN in roughly the right relative position AND LABELLED. Ground in a real sketch-map question (e.g. 2024 Q4(a)(i)). Teach the show=graded + label=separate marking.` },
  { key: 'river-landforms', want: `topicId jc-geography-1-4 · topicLabel 'Rivers, the water cycle, sea & ice: erosion, deposition & landforms' · RIVER LANDFORMS by stage: youthful stage = V-shaped valley & waterfall (erosion); old-age = meander & floodplain (deposition). Teach naming + how one forms. Ground in a real river-landform question.` },
  { key: 'coastal-landforms', want: `topicId jc-geography-1-4 · topicLabel 'Rivers, the water cycle, sea & ice: erosion, deposition & landforms' · COASTAL EROSION landforms: headland, bay, sea cliff, sea cave, sea stack — identify them and how erosion forms a stack. Ground in a real coastal question (e.g. 2022 Q3 photo match).` },
  { key: 'volcano-vs-fold-mountain', want: `topicId jc-geography-1-0 · topicLabel 'Plate tectonics: volcanoes, earthquakes & fold mountains' · VOLCANO vs FOLD MOUNTAIN at a plate boundary: name the boundary type (a volcano at a destructive/constructive boundary; fold mountains where plates collide) and the landform formed. Ground in a real tectonics question.` },
  { key: 'population-pyramid', want: `topicId jc-geography-3-0 · topicLabel 'Population: structure & change (demographic transition)' · READING A POPULATION PYRAMID: a wide base = high birth rate / young population (typical developing country); a narrow base + wide top = ageing population (developed country). Teach what the shape tells you. Ground in a real population-pyramid question.` },
  { key: 'synoptic-chart', want: `topicId jc-geography-1-5 · topicLabel 'Weather, climate & climate of Ireland' · READING A SYNOPTIC (weather) CHART: isobars join points of equal pressure; closely-spaced isobars = strong wind, widely-spaced = light wind; fronts (warm/cold/occluded) and pressure in millibars. Ground in a real synoptic-chart question (e.g. 2024 Q5(c)).` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE card (level 'common'). Every fact/place/method must be correct.`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  )
))
const cards = authored.filter(Boolean).map((r) => r.card).filter(Boolean)
log(`Authored ${cards.length}/${SLOTS.length} gap cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', properties: CARD_PROPS },
  },
}
const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Geography (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. CORRECTNESS: facts/place names/processes correct + within JC scope? Skill method exact (area = grid squares in km2)? Landform formation right (stack from cave-arch-stack; meander outer-bank erosion/inner-bank deposition)? Population-pyramid reading right? If wrong → fix.\n` +
    `2. GROUNDING: real question near "${c.source}" (2022-2025 CL)? marks + accepted answers match?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (figures/place facts + any map/graph described in words)?\n` +
    `4. LEVEL 'common'? topicId valid (jc-geography-N-N leaf) + topicLabel exact?\n` +
    `5. oneMove specific?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedCard (same id, level 'common'). If sound, accept. If fabricated/unsalvageable, reject.\n\nTHE CARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ card: c, v }))
))
const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.card)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) kept.push({ ...r.card, ...r.v.fixedCard })
}
log(`Verify: ${kept.length}/${cards.length} kept`)
return { kept, keptCount: kept.length }
