export const meta = {
  name: 'agsci-catchup',
  description: 'Author + adversarially verify Agricultural Science Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes/fact-checks each' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/agsci_txt'

const TOPICS = `
VALID agricultural-science topicIds (NEW SPECIFICATION, examined 2021+). topicId MUST be one of these; card strand =
topicId minus its last -N (e.g. agricultural-science-2-0 → strand agricultural-science-2).
STRAND 1 Scientific Practices (agricultural-science-0): -0 Hypothesising, -1 Experimenting, -2 Evaluating Evidence, -3 Communicating, -4 Working Safely
STRAND 2 Soils (agricultural-science-1): -0 Formation and Classification, -1 Properties, -2 Properties: Chemical, -3 Properties: Physical, -4 Properties: Biological, -5 Management
STRAND 3 Crops (agricultural-science-2): -0 Plant Physiology, -1 Classification/Identification, -2 Production, -3 Production: Establishment, -4 Production: Management, -5 Production: Harvesting
STRAND 4 Animals (agricultural-science-3): -0 Animal Physiology, -1 Classification/Identification, -2 Production, -3 Production: System/Enterprise, -4 Production: Management, -5 Production: Husbandry and Health
(Genetics/breeding → map to Animals or Crops; microbiology → Soils or Animals; sustainability/agri-environment → Soils or Crops.)
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert AGRICULTURAL SCIENCE (Irish exam-recovery tool, new spec).
A card teaches a student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a check
question + model answer.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Agricultural Science questions + marking schemes. Text of
all papers + schemes (2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): agricultural-science-YYYY-{HL,OL}-{paper,marking-scheme}.txt.
The new spec = 75% terminal written exam + 25% coursework (the Individual Investigative Study, IIS). All 2021-2025 papers
are the new spec. grep/Read for the exact question + scheme award points. Do NOT invent question numbers, marks, scheme
wording, or data. RECOMPUTE any calculation (stocking rate, livestock units, fertiliser N-P-K, % / ratio, financial) and
confirm it matches the scheme.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'agsci-', unique, includes the topic (e.g. 'agsci-ruminant-digestion-hl')
  subjectId     MUST be exactly 'agricultural-science'
  topicId       one of the valid ids above
  subjectLabel  'Agricultural Science'
  topicLabel    short human label
  focus         short row label disambiguating same-subtopic cards (e.g. 'Soil pH: liming to correct acidity')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core idea/technique + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks
  check         { prompt (self-contained, exam-style), modelAnswer (full), needed (>=2 award-point strings) }
  source        'Topic … — SEC LC Agricultural Science {YEAR} {LEVEL}, Q… + marking scheme (…the scheme answer…)'
  marksWeight   integer marks at stake (from the scheme)
  figureSpec    OPTIONAL — include ONLY if the check genuinely needs a visual the exam SHOWS (a data graph/chart to read,
                a labelled soil-profile/digestive-system/plant diagram to interpret, a photograph of a plant/weed/breed,
                a data table). Shape { year, level, questionRef, describes, whyNeeded }. If the question asks the student
                to DRAW/label a diagram, no figure is needed (teach how). Embed small data tables inline. DO NOT add 'figure'/'src'.

SELF-CONTAINMENT (hard rule): the check prompt must be answerable from the card itself + general ag-science knowledge. If
it needs a graph/diagram/data, EITHER add a figureSpec (for a shown graph/diagram to interpret) OR embed the data inline.
Never let a prompt silently depend on unseen stimulus.

QUALITY BAR: oneMove must name a SPECIFIC ag-science move/error (e.g. 'name the enzyme AND its substrate', 'lime RAISES
soil pH — acidity is corrected by adding lime', 'in a ruminant, microbial digestion of cellulose happens in the rumen',
'a fair test changes ONE variable and controls the rest'). BANNED filler: 'show your working', 'read the question',
'manage your time'. Plain text; ASCII fine; unicode (×, °, →, μ) fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const CARD_SCHEMA = {
  type: 'object', required: ['cards'],
  properties: {
    cards: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'subjectId', 'topicId', 'subjectLabel', 'topicLabel', 'focus', 'level', 'gist', 'oneMove', 'check', 'source', 'marksWeight'],
        properties: {
          id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
          subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
          level: { type: 'string', enum: ['higher', 'ordinary'] }, gist: { type: 'string' },
          oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
          check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
          source: { type: 'string' }, marksWeight: { type: 'integer' },
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'scientific-practices-soils', n: 5, strands: 'agricultural-science-0 (Scientific Practices), agricultural-science-1 (Soils)',
    topics: 'experiment design & the fair test (independent/dependent/controlled variables), evaluating evidence/reliability, the Individual Investigative Study (IIS) skills; soil formation & classification, soil texture & structure, soil pH & liming, chemical properties (CEC, leaching, N-P-K), physical properties (drainage, water/air), biological properties (organic matter, earthworms, micro-organisms), soil management. Aim ~2 Scientific Practices + 3 Soils.' },
  { key: 'crops', n: 5, strands: 'agricultural-science-2 (Crops)',
    topics: 'plant physiology (photosynthesis, respiration, transpiration, plant structure), crop classification/identification, grassland production & management, cereal (e.g. spring barley) production, establishment (seedbed, sowing), management (fertiliser, weed/pest/disease control), harvesting & silage (the silage process, anaerobic fermentation). Mix HL + OL.' },
  { key: 'animals-physiology-production', n: 5, strands: 'agricultural-science-3 (Animals)',
    topics: 'animal physiology (the RUMINANT digestive system & microbial cellulose digestion, the reproductive system, the oestrous cycle, lactation), classification/identification (breeds), production systems/enterprises (dairy, beef, sheep), production management (nutrition, feeding, grass-based systems). Mix HL + OL.' },
  { key: 'animals-genetics-health', n: 5, strands: 'agricultural-science-3 (Animals), with genetics/microbiology where mapped',
    topics: 'genetics & breeding (Mendelian crosses/monohybrid, selective breeding, EBI/breeding indices, heritability), animal husbandry & health (common diseases e.g. mastitis/liver fluke/BVD, prevention, antibiotics/withdrawal, parasite control), microbiology (bacteria/fungi in agriculture, fermentation), and agri-environment/sustainability where it maps to animals. Mix HL + OL; include a genetics CALCULATION (e.g. a monohybrid cross ratio) if supported.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce ${c.n} recovery cards: aim for ~3 Higher + ~2 Ordinary, spread across DIFFERENT subtopics and years. Favour high-frequency, high-mark questions. Read the relevant ${TXT}/ files; recompute every calculation and fact-check against the scheme. Add figureSpec ONLY where the check truly needs a graph/diagram/data the exam SHOWS.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'accurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, accurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `You are an independent SKEPTIC verifying ONE Agricultural Science Catch-Up recovery card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question matching "${c.source}"? Do marks + the scheme's modelled answer + award points match the scheme text? else grounded:false.\n` +
    `2. ACCURACY: any scientific/agricultural error (wrong enzyme, wrong soil-pH direction [lime RAISES pH], wrong digestive compartment, wrong genetics ratio, wrong calc)? Recompute any number. else accurate:false.\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (+figureSpec/embedded data if needed)? If it silently needs unseen stimulus and has no figureSpec/embedded data → selfContained:false.\n` +
    `4. QUALITY: oneMove specific (not banned filler)? needed[] real award points? topicId valid?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id; preserve/repair figureSpec). If sound, accept. If fabricated/inaccurate, reject.\n\n` +
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
  `Completeness critic for an Agricultural Science Catch-Up Lane recovery-card set (Irish LC, new spec). The ${kept.length} kept cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec, marks: k.marksWeight })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) coverage across the 4 strands (Scientific Practices, Soils, Crops, Animals) — flag thin/empty, ` +
  `(3) mix of definition/short-answer vs experiment vs calculation (genetics cross, stocking rate) vs diagram/data, ` +
  `(4) whether high-frequency topics (ruminant digestion, soil pH/liming, photosynthesis, silage, genetics cross, common diseases) are present. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
