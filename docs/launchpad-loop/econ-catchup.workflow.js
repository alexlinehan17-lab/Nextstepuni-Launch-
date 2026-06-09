export const meta = {
  name: 'econ-catchup',
  description: 'Author + adversarially verify Economics Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each vs scheme' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/econ_txt'

const TOPICS = `
VALID economics topicIds (NEW SPECIFICATION, first examined 2022). topicId MUST be one of these; the card's strand =
topicId minus its last -N (e.g. economics-1-1 → strand economics-1).
STRAND 1 What Is Economics? (economics-0): -0 Economics as a Way of Thinking, -1 Scarcity & Choice, -2 Sustainability
STRAND 2 Economic Decisions (economics-1): -0 The Market Economy, -1 The Consumer (Demand), -2 The Firm (Supply), -3 Government Intervention
STRAND 3 What Can Markets Do? (economics-2): -0 Market Structures, -1 The Labour Market, -2 Market Failure
STRAND 4 Policy & Performance (economics-3): -0 National Income, -1 Fiscal Policy & the Budget, -2 Employment & Unemployment, -3 Monetary Policy & Prices, -4 Financial Sector
STRAND 5 International Economics (economics-4): -0 Growth & Development, -1 Globalisation, -2 Trade & Competitiveness
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert ECONOMICS (Irish exam-recovery tool). A card teaches a student
who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a check question + model answer.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Economics questions + marking schemes. Text of all papers +
schemes at ${TXT}/ (pages ===PAGE n===): economics-YYYY-{HL,OL}-{paper,marking-scheme}.txt.
IMPORTANT — the NEW Economics specification was first examined in 2022. PRIORITISE 2022-2025 (the current spec). The
2021 paper is the OLD syllabus (different format/topics) — only use a 2021 question if the concept is identical in the
new spec, and prefer the 2022-2025 papers. grep/Read for the exact question + scheme award points. Do NOT invent question
numbers, marks, scheme wording, or data. RECOMPUTE every calculation (elasticity, multiplier, % change, index/CPI,
exchange-rate conversion) and confirm it matches the scheme.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'econ-', unique, includes the topic (e.g. 'econ-ped-elasticity-calc-2023-hl')
  subjectId     MUST be exactly 'economics'
  topicId       one of the valid ids above
  subjectLabel  'Economics'
  topicLabel    short human label
  focus         short row label disambiguating same-subtopic cards (e.g. 'PED: calculate + interpret sign')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core idea/technique + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks
  check         { prompt (self-contained, exam-style), modelAnswer (full worked answer), needed (>=2 award-point strings) }
  source        'Topic … — SEC LC Economics {YEAR} {LEVEL}, Q… + marking scheme (…the scheme answer…)'
  marksWeight   integer marks at stake (from the scheme)
  figureSpec    OPTIONAL — include ONLY if the check genuinely needs a visual (a demand/supply or cost-curve DIAGRAM to
                interpret, a data GRAPH/chart, a PPF). Shape { year, level, questionRef, describes, whyNeeded }. For data
                TABLES or short figures, embed the numbers inline in the prompt instead. If the question asks the student
                to DRAW a diagram, no figure is needed (the card teaches how to draw it). DO NOT add a 'figure'/'src'.

SELF-CONTAINMENT (hard rule): the check prompt must be answerable from the card itself + general economics knowledge. If
it needs a diagram/graph/data, EITHER add a figureSpec (for a graph/chart to interpret) OR embed the data inline (tables)
OR rewrite self-contained. Never let a prompt silently depend on unseen stimulus.

QUALITY BAR: oneMove must name a SPECIFIC economics move/error (e.g. 'PED is negative — state the sign and that demand is
inelastic if |PED|<1', 'the multiplier = 1/MPS, so a leakage rise SHRINKS it', 'a subsidy shifts SUPPLY right, not
demand', 'GNP = GDP minus net factor income from abroad'). BANNED filler: 'show your working', 'read the question',
'manage your time'. Plain text; ASCII (%, ->, euro as 'EUR' or the word) fine; unicode (€, ×, ↑↓) also fine.

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
  { key: 'foundations-decisions', strands: 'economics-0 (What Is Economics?), economics-1 (Economic Decisions)',
    topics: 'scarcity & opportunity cost, the PPF/production possibility frontier, economics-as-thinking & sustainability, the market economy, demand & the law of demand, supply, market equilibrium (price/quantity), elasticity (PED/YED/CED — calculate + interpret), the consumer & utility, the firm & costs, government intervention (price ceilings/floors, taxes & subsidies)' },
  { key: 'markets', strands: 'economics-2 (What Can Markets Do?)',
    topics: 'market structures (perfect competition, monopoly, oligopoly — features, diagrams, price/output), the labour market (wage determination, trade unions, MRP), market failure (externalities — negative/positive, public goods, merit/demerit goods, asymmetric information) and government responses' },
  { key: 'policy-performance', strands: 'economics-3 (Policy & Performance)',
    topics: 'national income (GDP vs GNP, the circular flow, the multiplier = 1/MPS), fiscal policy & the budget (deficit/surplus, automatic stabilisers, national debt), employment & unemployment (types — cyclical/structural/frictional, rates), monetary policy & prices (inflation, CPI/index numbers, the ECB & interest rates, deflation), the financial sector' },
  { key: 'international', strands: 'economics-4 (International Economics)',
    topics: 'economic growth vs development (HDI, indicators), globalisation (MNCs, FDI, benefits/costs), trade & competitiveness (comparative advantage, balance of payments, protectionism vs free trade, the EU/Single Market, exchange rates)' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 5 recovery cards: aim for ~3 Higher + ~2 Ordinary, spread across DIFFERENT subtopics and years (2022-2025 new spec). Favour high-frequency, high-mark questions; include at least one calculation card and one diagram/data card where the strand supports it. Read the relevant ${TXT}/ files; recompute every calculation and confirm it matches the scheme. Add figureSpec ONLY where the check truly needs a graph/diagram to interpret.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'mathChecks', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `You are an independent SKEPTIC verifying ONE Economics Catch-Up recovery card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question matching "${c.source}"? Is it NEW-SPEC (2022-2025, not an old-2021-syllabus topic that no longer applies)? Do marks + the scheme's modelled answer + award points match the scheme text? else grounded:false.\n` +
    `2. MATHS: RECOMPUTE every number in modelAnswer (elasticity incl. its sign, multiplier=1/MPS, % change, index/CPI, exchange-rate conversion). Matches the scheme (value, sign, units)? else mathChecks:false.\n` +
    `3. ECONOMICS ACCURACY: any conceptual error (wrong definition, wrong diagram shift, wrong elasticity interpretation, GDP/GNP mixed up, multiplier direction)?\n` +
    `4. SELF-CONTAINMENT: answerable from the card alone (+figureSpec/embedded data if needed)? If it silently needs unseen stimulus and has no figureSpec/embedded data → selfContained:false.\n` +
    `5. QUALITY: oneMove specific (not banned filler)? needed[] real award points? topicId valid?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id; preserve/repair figureSpec). If sound, accept. If fabricated/old-spec/unsalvageable, reject.\n\n` +
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
  `Completeness critic for an Economics Catch-Up Lane recovery-card set (Irish LC, new spec). The ${kept.length} kept cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec, marks: k.marksWeight })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) coverage across the 5 strands (economics-0..4) — flag any strand thin/empty, ` +
  `(3) mix of calculation vs definition vs diagram/data cards, (4) whether diagram/data-interpretation cards (D/S, cost ` +
  `curves, PPF, data graphs) are represented. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
