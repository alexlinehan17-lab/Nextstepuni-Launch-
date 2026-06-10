export const meta = {
  name: 'jc-geography-catchup',
  description: 'Author + adversarially verify Junior Cycle Geography (Common Level) Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'group clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, geography correctness' },
    { title: 'Critic', detail: 'completeness + group balance' },
  ],
}

const TXT = '/tmp/jc_geography_txt'

const TOPICS = `
VALID jc-geography topicIds (the VERIFIED taxonomy — 4 groups, all examinable). topicId MUST be one; topicLabel the EXACT name.
Geographical skills (jc-geography-0): -0 OS maps: grid references, scale & distance, -1 OS maps: direction, height, relief
  & slope, -2 OS maps: identifying features, sketch maps & settlement patterns, -3 Aerial & satellite photo
  interpretation, -4 Climate graphs, charts & data interpretation
Exploring the physical world (jc-geography-1): -0 Plate tectonics: volcanoes, earthquakes & fold mountains, -1 Rocks & the
  rock cycle, -2 Weathering & mass movement, -3 Soils, -4 Rivers, the water cycle, sea & ice: erosion, deposition &
  landforms, -5 Weather, climate & climate of Ireland, -6 Energy resources from the physical world, -7 Physical processes
  in a chosen location (fieldwork)
Exploring how we interact with the physical world (jc-geography-2): -0 Living with tectonic hazards & responding to natural
  disasters, -1 Rock exploitation & energy resources: consequences, -2 Primary economic activities & the physical
  landscape, -3 Natural resources: water, fish stocks, forestry & soil, -4 Secondary economic activity: function &
  location, -5 Climate change: causes & implications, -6 Managing surface processes, -7 Tourism, transport & the physical
  world
Exploring people, place and change (jc-geography-3): -0 Population: structure & change (demographic transition),
  -1 Migration: causes & consequences, -2 Settlement: rural & urban location, -3 Urbanisation: urban change in an Irish
  town or city, -4 Development & global patterns, -5 Life chances in developed & developing countries, -6 Development
  assistance (aid) & interdependence, -7 Globalisation: people, settlement & development
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE GEOGRAPHY (Ireland, reformed NCCA spec, first examined 2022). A
card helps a student who fell behind recover the marks: a clear gist of the concept/skill, the ONE highest-leverage move
(or classic error), and a SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 360 marks, ~2 hours;
the number of questions varies by year (2024:9, 2023:10). The exam is MAP/PHOTO/GRAPH-HEAVY: OS-map skills (grid refs,
scale & distance, area, direction, height, sketch maps, settlement), aerial-photo interpretation and climate graphs/tables
appear throughout. EVERY card's level MUST be 'common'.
SEC MARKING (ground traps in it): each part has accepted answers, often "any X from a list", and named landform/process
answers. Key consequences a card can teach: a SIX-FIGURE GRID REFERENCE reads EASTINGS (along the bottom) BEFORE NORTHINGS
(up the side) — reverse them and you get zero; DISTANCE from a 1:50,000 map = map cm × 0.5 km (the scale conversion);
"Explain" needs a process reason, "Describe" needs what-it-looks-like; a NAMED EXAMPLE (a real river/volcano/town) is often
a separate mark; reading a CLIMATE GRAPH means quoting the figure + its month/unit.

GROUNDING (non-negotiable): ground every card in REAL SEC JC Geography questions + marking schemes at ${TXT}/ —
jc-geography-YYYY-CL-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled 2020-2021).
grep/Read for the real question + the scheme's accepted answers. Do NOT invent question numbers, marks, or scheme wording.

CORRECTNESS (hard rule): every fact, place name, process and skill method must be geographically CORRECT and within JC
scope (no Leaving-Cert depth — no regional-geography blocks, no GIS, no LC plate-tectonics detail). For skills cards the
method (grid-ref order, scale conversion, area = length × width in km) must be exactly right.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jcgeo-', unique (e.g. 'jcgeo-six-figure-grid-ref')
  subjectId     MUST be exactly 'jc-geography'
  topicId       one of the valid ids above
  subjectLabel  'Geography (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Grid refs: eastings first, then northings')
  level         MUST be 'common'
  gist          2-5 sentences: the concept/skill + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC geography move, e.g. 'read the
                six-figure grid ref as eastings then northings — "along the corridor, up the stairs"', 'to explain a
                river meander, name erosion on the outer bank and deposition on the inner bank', 'always give a NAMED
                example — a real volcano/river/town earns its own mark')
  check         { prompt (SELF-CONTAINED — for a skills card describe the map/photo/graph detail in words and give the
                  numbers needed; for a content card give the scenario), modelAnswer (the full correct answer), needed
                  (>=2 award points = the marking points) }
  source        'Topic … — SEC JC Geography {YEAR} CL, Q… + marking scheme (…accepted answers…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card alone — embed the figures/place facts and describe any
map/photo/graph in words (e.g. 'on a 1:50,000 OS map two points are 7 cm apart'). modelAnswer states the correct geography.

QUALITY BAR: oneMove names a SPECIFIC geography concept, skill method or marking behaviour. BANNED filler: 'read the
question', 'manage your time', 'learn the places', 'study the map'.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const CARD_SCHEMA = {
  type: 'object', required: ['cards'],
  properties: {
    cards: { type: 'array', items: { type: 'object',
      required: ['id', 'subjectId', 'topicId', 'subjectLabel', 'topicLabel', 'focus', 'level', 'gist', 'oneMove', 'check', 'source', 'marksWeight'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
        subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
        level: { type: 'string', enum: ['common'] }, gist: { type: 'string' },
        oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
        check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
        source: { type: 'string' }, marksWeight: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'geographical-skills', strand: 'jc-geography-0 (Geographical skills) — the most-examined area',
    topics: 'OS-MAP skills: SIX-FIGURE GRID REFERENCES (eastings before northings), SCALE & DISTANCE on a 1:50,000 map (map cm × 0.5 = km; straight-line vs along a road), AREA in km² (count grid squares / length × width), DIRECTION (8-point compass between two points), HEIGHT & RELIEF & SLOPE (spot heights, contours, steep vs gentle), identifying map FEATURES from the legend, SKETCH MAPS (drawing/labelling), SETTLEMENT PATTERNS on a map (nucleated/dispersed/linear); AERIAL/SATELLITE PHOTO interpretation (foreground/background, left/right, land use); CLIMATE GRAPHS/TABLES (read temperature & rainfall, calculate the annual temperature RANGE = highest − lowest, total/mean rainfall, population pyramids). High-frequency, easy marks lost on method.' },
  { key: 'physical-world', strand: 'jc-geography-1 (Exploring the physical world)',
    topics: 'PLATE TECTONICS (plate boundaries, how a VOLCANO/EARTHQUAKE/FOLD MOUNTAIN forms, labelled diagrams), ROCKS & the rock cycle (igneous/sedimentary/metamorphic — formation & an example), WEATHERING & MASS MOVEMENT (mechanical/chemical weathering; landslides), SOILS, RIVERS/SEA/ICE + the WATER CYCLE (erosion/deposition/transport; landforms like meanders, waterfalls, U-shaped valleys, beaches; the hydrological cycle stages), WEATHER & CLIMATE (the Cool Temperate Oceanic climate of Ireland, synoptic charts, fronts), and ENERGY resources from the physical world. JC scope, with named examples.' },
  { key: 'interaction', strand: 'jc-geography-2 (Exploring how we interact with the physical world)',
    topics: 'LIVING WITH TECTONIC HAZARDS & responding to disasters (e.g. the Turkey-Syria earthquake — effects, short vs long-term responses), rock/energy EXPLOITATION consequences, PRIMARY economic activity & the landscape, NATURAL RESOURCES (water pollution, fish stocks, forestry, soil), SECONDARY economic activity (function & location factors), CLIMATE CHANGE (causes — greenhouse gases; implications), MANAGING surface processes (e.g. coastal/river protection), and TOURISM/TRANSPORT & the physical world. Named real examples matter.' },
  { key: 'people-place-change', strand: 'jc-geography-3 (Exploring people, place and change)',
    topics: 'POPULATION structure & change (the DEMOGRAPHIC TRANSITION model, birth/death rates, reading a POPULATION PYRAMID), MIGRATION (push/pull causes, consequences, a barrier to migration), SETTLEMENT (rural & urban location factors), URBANISATION (urban change in an Irish town/city — causes & effects of growth/decline), DEVELOPMENT & global patterns (developed vs developing, indicators like GNI/literacy/life expectancy), LIFE CHANCES, development ASSISTANCE/AID & interdependence, and GLOBALISATION. Named examples and data reading.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nGroup: ${c.strand}\nTopics to mine: ${c.topics}\n\nProduce 6 cards spread across DIFFERENT subtopics and DIFFERENT years (all level 'common'). Ground each in a real question + its marking scheme. topicLabel MUST be the exact curriculum subtopic name. Every fact/place/skill method must be correct and within JC scope.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; valid topicId; level common). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Geography (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. CORRECTNESS: is everything in gist/oneMove/modelAnswer geographically CORRECT and within JC scope (no LC-only depth)? For a SKILLS card CHECK THE METHOD: six-figure grid ref = eastings THEN northings; distance on 1:50,000 = map cm × 0.5 km; area = length × width in km; temperature range = highest − lowest. For a content card check the process/place facts. If wrong → fix (or reject if unsalvageable).\n` +
    `2. GROUNDING: real question/section near "${c.source}" (2022-2025)? marks + accepted answers match the scheme?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (figures/place facts + any map/photo/graph described in words)?\n` +
    `4. LEVEL: is level exactly 'common'? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific geography move/method (no filler)?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (same id, level 'common'). If sound, accept. If fabricated/unsalvageable, reject.\n\n` +
    `THE CARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ card: c, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.card)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) kept.push({ ...r.card, ...r.v.fixedCard })
}
log(`Verify: ${kept.length}/${cards.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a Junior Cycle Geography (Common Level) Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) coverage across all FOUR groups — Geographical skills (must be strong — it is the most examined), Physical world, Interaction, People/place/change — flag thin areas, (2) whether the signature high-frequency topics appear: six-figure grid ref, distance/scale, area, direction, sketch map, photo interpretation, climate graph/table, plate tectonics (volcano/earthquake/fold mountain), rock cycle, weathering/mass movement, river/coastal/glacial landforms, water cycle, weather/synoptic chart, climate change, population pyramid/demographic transition, migration, urbanisation, development indicators, (3) whether the signature MARKING traps are present (grid-ref order, scale conversion, named example required, describe-vs-explain, quote-the-figure), (4) any duplicate focus. List concrete gap slots (each: topicId + focus). All cards are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
