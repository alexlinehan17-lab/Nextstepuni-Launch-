export const meta = {
  name: 'jc-science-catchup',
  description: 'Author + adversarially verify Junior Cycle Science (Common Level) Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, science correctness' },
    { title: 'Critic', detail: 'completeness + strand balance' },
  ],
}

const TXT = '/tmp/jc_science_txt'

const TOPICS = `
VALID jc-science topicIds (the VERIFIED taxonomy — 5 strands, ALL examinable). topicId MUST be one; topicLabel the EXACT name.
Nature of science (jc-science-0): -0 How science works & how ideas change over time, -1 Asking scientific questions &
  writing testable hypotheses, -2 Designing fair tests: variables, controls, reliability, accuracy, precision & safety,
  -3 Choosing and using measuring instruments & apparatus, -4 Recording & representing data: tables, graphs and charts,
  -5 Analysing data, spotting patterns & anomalies, drawing & justifying conclusions, -6 Evaluating sources, reliability,
  bias & media claims about science, -7 Science in society: scientists' contributions, ethics & global importance
Physical world (jc-science-1): -0 Measuring physical quantities (length/mass/time/temperature/area/volume/density),
  -1 Speed, acceleration & motion graphs, -2 Forces, -3 Electricity: current, potential difference, resistance &
  electrical power, -4 Electric circuits: series, parallel & simple electronic circuits, -5 Energy conservation,
  transfer, dissipation & efficiency (Sankey diagrams), -6 Technological applications of physics & their impact,
  -7 Ethics & sustainability of generating and using electricity
Chemical world (jc-science-2): -0 States of matter, the particle model & conservation of mass, -1 Atomic structure
  (protons/neutrons/electrons/mass/charge), -2 Classifying substances (elements/compounds/mixtures/metals/non-metals),
  -3 The Periodic Table & chemical formulae, -4 Properties of materials (solubility/conductivity/melting&boiling;
  separation techniques), -5 Rates of reaction & the variables that affect them, -6 Acids, bases, indicators & the pH
  scale, -7 Energy in reactions (exo/endothermic, activation energy, energy profiles), -8 Sustainability of materials
  (extraction/use/disposal/recycling)
Biological world (jc-science-3): -0 Cells (plant & animal structure/function), -1 Reproduction, inheritance & genetics,
  -2 Evolution by natural selection & the diversity of life, -3 Human body systems (digestive/circulatory/respiratory),
  -4 Habitats, adaptation, competition & interdependence (habitat studies), -5 Human health (nutrition/lifestyle/
  inherited factors/micro-organisms), -6 Respiration, photosynthesis & energy flow through ecosystems, -7 Human sexual
  reproduction & related ethical and societal issues, -8 Conserving biodiversity, food production & benefits from ecosystems
Earth and space (jc-science-4): -0 The solar system & universe, -1 The origin of the universe & comparing Earth with
  other planets/moons, -2 The Earth-Sun-Moon system (day&night/seasons/lunar phases/eclipses), -3 Cycling of matter (the
  carbon and water cycles), -4 Energy sources & meeting Earth's energy needs, -5 Climate, climate change & initiatives,
  -6 Space exploration: hazards, benefits & its future role
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE SCIENCE (Ireland, reformed NCCA spec, first examined 2019). A
card helps a student who fell behind recover the marks: a clear gist of the concept, the ONE highest-leverage move (or the
classic error), and a SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 360 marks, ~2 hours,
Section A (10 short questions, 15 marks each) + Section B (long questions; the NUMBER of Section B questions varies by year
— 2022:5, 2023:5, 2024:7, 2025:4). So EVERY card's level MUST be 'common'.
SEC MARKING (ground traps in it): each part has accepted answers, often "any one/two from: ...". Key consequences a card
can teach: "Name TWO ..." needs exactly two distinct correct points (one scores half); "Explain"/"Justify" needs a reason,
not just a restatement; a graph answer needs correct axes + plotted points + a line; "accuracy" (closeness to the true
value) is NOT "precision" (closeness of repeats); a testable hypothesis must be a checkable prediction, not a question; a
fair test changes ONE variable and controls the rest.

GROUNDING (non-negotiable): ground every card in REAL SEC JC Science questions + marking schemes at ${TXT}/ —
jc-science-YYYY-CL-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled 2020-2021).
grep/Read for the real question + the scheme's accepted answers. Do NOT invent question numbers, marks, or scheme wording.

SCIENCE CORRECTNESS (hard rule): every fact and model answer must be scientifically CORRECT and within JC scope (no
Leaving-Cert-only depth — e.g. no moles/stoichiometry, no detailed organic chemistry, no equations of motion v=u+at
beyond speed=distance/time and simple acceleration). Working-scientifically cards (Nature of science) teach the SKILL.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jcsci-', unique (e.g. 'jcsci-fair-test-one-variable')
  subjectId     MUST be exactly 'jc-science'
  topicId       one of the valid ids above
  subjectLabel  'Science (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Fair test: change one variable, control the rest')
  level         MUST be 'common'
  gist          2-5 sentences: the concept/skill + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC science move, e.g. 'in a fair test
                name the ONE changed (independent) variable and at least one controlled variable — that pairing is the
                marks', 'when asked to Explain, add a "because ..." with the science reason', 'accuracy = close to the
                true value; precision = repeats close together — do not swap them')
  check         { prompt (SELF-CONTAINED — embed any data/scenario needed; for graph/apparatus questions describe it in
                  words), modelAnswer (the full correct answer), needed (>=2 award points = the marking points) }
  source        'Topic … — SEC JC Science {YEAR} CL, Section …/Q… + marking scheme (…accepted answers…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card alone — embed the data/scenario and describe any
diagram in words. modelAnswer states the correct science.

QUALITY BAR: oneMove names a SPECIFIC science concept or marking behaviour. BANNED filler: 'read the question', 'manage
your time', 'learn the definitions', 'revise the topic'.

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
  { key: 'nature-of-science', strand: 'jc-science-0 (Nature of science — working scientifically)',
    topics: 'the working-scientifically skills examined throughout every paper: writing a TESTABLE hypothesis (a checkable prediction, not a question), designing a FAIR TEST (the one changed/independent variable + the controlled variables + why you repeat/replicate for reliability), ACCURACY vs PRECISION, choosing the right measuring instrument, RECORDING & GRAPHING data (axes, plotting, line of best fit), drawing & JUSTIFYING conclusions from data (does the data support the hypothesis?), evaluating a source for reliability/bias, and science-in-society/ethics. These are high-frequency, high-mark, and students lose easy marks on them.' },
  { key: 'physical-world', strand: 'jc-science-1 (Physical world)',
    topics: 'measuring quantities incl. DENSITY (mass/volume), SPEED = distance/time + acceleration + reading motion graphs (distance-time, speed-time), FORCES (weight vs mass, friction, balanced/unbalanced), ELECTRICITY (current, potential difference, resistance, power = VI; Ohm-style V=IR calcs), CIRCUITS (series vs parallel, what happens when a bulb fails, reading a circuit diagram), and ENERGY (conservation, transfer, dissipation as heat, efficiency, SANKEY diagrams). JC scope only.' },
  { key: 'chemical-world', strand: 'jc-science-2 (Chemical world)',
    topics: 'STATES of matter & the particle model & conservation of mass, ATOMIC STRUCTURE (protons/neutrons/electrons — mass, charge, location), elements/compounds/MIXTURES & metals/non-metals, the PERIODIC TABLE (groups/periods) & simple chemical formulae, properties & SEPARATION techniques (filtration, distillation, chromatography, evaporation; solubility), RATES OF REACTION & the variables that change them (temperature, surface area, concentration), ACIDS/BASES/INDICATORS & the pH scale, and ENERGY in reactions (exothermic vs endothermic, energy profile diagrams, activation energy). No moles/stoichiometry (LC).' },
  { key: 'biological-world', strand: 'jc-science-3 (Biological world)',
    topics: 'CELLS (plant vs animal structure & function), REPRODUCTION/INHERITANCE/GENETICS (dominant/recessive alleles, genotype/phenotype, Punnett-style ratios), EVOLUTION by natural selection, HUMAN BODY SYSTEMS (digestive, circulatory, respiratory), HABITATS/adaptation/competition/interdependence & food chains & the quadrat method, human HEALTH (nutrition, micro-organisms), RESPIRATION & PHOTOSYNTHESIS (word equations, energy flow through ecosystems), human reproduction, and conserving BIODIVERSITY. JC scope.' },
  { key: 'earth-and-space', strand: 'jc-science-4 (Earth and space)',
    topics: 'the SOLAR SYSTEM & universe (planets, moons, asteroids vs comets, stars, galaxies), origin of the universe & comparing Earth with other planets, the EARTH-SUN-MOON system (day & night, SEASONS, lunar PHASES, ECLIPSES — and why they occur), the CARBON and WATER CYCLES (cycling of matter — note: this lives under Earth and space per the spec), ENERGY SOURCES (renewable vs non-renewable, meeting energy needs), CLIMATE CHANGE & initiatives, and SPACE EXPLORATION (hazards, benefits).' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrand: ${c.strand}\nTopics to mine: ${c.topics}\n\nProduce 6 cards spread across DIFFERENT subtopics of this strand and DIFFERENT years (all level 'common'). Ground each in a real question + its marking scheme. topicLabel MUST be the exact curriculum subtopic name. Every model answer must be scientifically correct and within JC scope.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'sciCorrect', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, sciCorrect: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; valid topicId; level common). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Science (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. SCIENCE CORRECTNESS: is everything in gist/oneMove/modelAnswer scientifically CORRECT and within JC scope (no LC-only depth — no moles/stoichiometry, no v=u+at, no detailed organic)? If a fact is wrong → fix (or reject if unsalvageable). Common student-myth checks: accuracy vs precision not swapped; testable hypothesis is a prediction; fair test changes ONE variable.\n` +
    `2. GROUNDING: real question/section near "${c.source}" (2022-2025)? marks + accepted answers match the scheme?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (data/scenario + any diagram described in words embedded)?\n` +
    `4. LEVEL: is level exactly 'common'? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific science move or marking behaviour (no filler)?\n` +
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
  `Completeness critic for a Junior Cycle Science (Common Level) Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) coverage across all FIVE strands — Nature of science (working scientifically), Physical, Chemical, Biological, Earth and space — flag thin strands (each should have several cards; Nature of science especially matters because it is examined throughout), (2) whether the signature high-frequency topics appear: fair-test/variables, accuracy-vs-precision, graphs, electricity/circuits, energy/Sankey, rates of reaction, acids/pH, atomic structure, separation, genetics/Punnett, body systems, photosynthesis/respiration, food chains, Earth-Sun-Moon (phases/eclipses), carbon cycle, energy sources, climate change, (3) whether the signature MARKING traps are present (name-TWO needs two, Explain needs a reason, accuracy≠precision, testable hypothesis, fair-test one-variable), (4) any duplicate focus. List concrete gap slots (each: topicId + focus). All cards are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
