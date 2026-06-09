export const meta = {
  name: 'econ-catchup-topup',
  description: 'Fill Economics Catch-Up gaps: perfect competition, OL foundations/micro, negative externality, non-elasticity demand/supply',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each' },
  ],
}

const TXT = '/tmp/econ_txt'

const TOPICS = `Valid economics topicIds (NEW SPEC): economics-0-* (What Is Economics?: -0 thinking, -1 Scarcity & Choice, -2 Sustainability),
economics-1-* (Economic Decisions: -0 Market Economy, -1 Consumer/Demand, -2 Firm/Supply, -3 Government Intervention),
economics-2-* (What Can Markets Do?: -0 Market Structures, -1 Labour Market, -2 Market Failure),
economics-3-* (Policy & Performance), economics-4-* (International). Card strand = topicId minus last -N.`

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for Leaving Cert ECONOMICS (NEW specification, examined 2022+). A card teaches
a student who lost marks how to recover them: clear gist, the ONE highest-leverage move, a check question + model answer.

GROUNDING: ground in a REAL SEC LC Economics question + scheme at ${TXT}/ (pages ===PAGE n===):
economics-YYYY-{HL,OL}-{paper,marking-scheme}.txt. PRIORITISE 2022-2025 (current spec); 2021 is the OLD syllabus — only
use it if the concept is identical in the new spec. grep/Read for the exact question + award points. Do NOT invent
wording/marks/scheme content. RECOMPUTE any calculation and confirm it matches the scheme.

${TOPICS}

CARD FIELDS: id (kebab, 'econ-' prefix, includes topic), subjectId='economics', topicId (valid id), subjectLabel='Economics',
topicLabel (short), focus (short row label), level ('higher'|'ordinary'), gist (2-5 sentences),
oneMove {label, text} (specific economics move/error — not filler),
check {prompt (self-contained), modelAnswer (full), needed (>=2 award-point strings)},
source ('Topic … — SEC LC Economics {YEAR} {LEVEL}, Q… + marking scheme (…)'), marksWeight (int).
figureSpec OPTIONAL { year, level, questionRef, describes, whyNeeded } — ONLY if the check needs a graph/diagram to
INTERPRET. If the question asks the student to DRAW a diagram, no figure is needed (teach how to draw it); embed any data
table inline. DO NOT add a 'figure'/'src' field.

QUALITY: oneMove names a specific move/error. BANNED filler: 'show your working','read the question','manage your time'.
Plain text; € and unicode fine. Return data only; never edit a file.
`

const STEM_SCHEMA = {
  type: 'object', required: ['card'],
  properties: {
    card: {
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
}

const SLOTS = [
  { key: 'perfect-competition', level: 'higher',
    topic: 'PERFECT COMPETITION (economics-2-0 Market Structures) — entirely absent from the set. Features (many buyers/sellers, homogeneous product, price-taker, free entry/exit, perfect information) and the long-run normal-profit outcome (P = MC = ATC). Ground in a real new-spec question. Add a figureSpec ONLY if the exam shows a cost-curve diagram to interpret; if the question asks to draw it, teach how to draw it (no figure).' },
  { key: 'ol-foundations', level: 'ordinary',
    topic: 'OL FOUNDATIONS (economics-0-1 Scarcity & Choice or economics-1-0/1-1 Market Economy/Demand) — the set has NO OL card in strand 0 or strand 1. Pick a real OL question on scarcity/opportunity cost, the factors of production, demand and the factors affecting demand, or market equilibrium. Keep it OL-level and self-contained.' },
  { key: 'negative-externality', level: 'higher',
    topic: 'NEGATIVE EXTERNALITY / market failure (economics-2-2 Market Failure) — only POSITIVE externalities are covered (twice). Negative externality (e.g. pollution, the cost imposed on third parties, why the market over-produces, and the government response: tax/regulation). Ground in a real new-spec question.' },
  { key: 'demand-supply-non-elasticity', level: 'ordinary',
    topic: 'A non-elasticity DEMAND/SUPPLY card (economics-1-1 Consumer/Demand or economics-1-2 Firm/Supply) — strand 1 is over-weighted on elasticity (3 of 4). Cover the factors/determinants that SHIFT demand or supply, or a movement-vs-shift distinction, or market equilibrium price determination. OL level. Ground in a real new-spec question.' },
  { key: 'ol-macro-or-micro-extra', level: 'ordinary',
    topic: 'One more OL card to balance levels (set is 13 HL / 7 OL). Pick a high-frequency OL topic NOT already covered well — e.g. inflation/CPI effects (OL), types of unemployment (OL, if not duplicating structural), economic growth, the labour market, or a market-structure (OL monopoly is covered — avoid). Ground in a real new-spec OL question.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nPREFERRED level: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded card for this slot.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.card ? { ...r.card, _slot: s.key } : null),
))

const cards = authored.filter(Boolean)
log(`Authored ${cards.length} top-up cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'mathChecks', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Economics Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} NEW-SPEC (2022-2025) question matching "${c.source}"? marks + scheme answer + award points match? else grounded:false.\n` +
    `2. MATHS (if any calc): recompute; matches scheme (value/sign/units)? else mathChecks:false.\n` +
    `3. ECONOMICS ACCURACY: any conceptual error (definition, diagram shift, market-structure features, externality direction)?\n` +
    `4. SELF-CONTAINMENT: answerable from the card alone (+figureSpec/embedded data)? else selfContained:false.\n` +
    `5. QUALITY: oneMove specific (no filler)? needed[] real award points? topicId valid?\n` +
    `If fixable, verdict:fix with a complete corrected card in fixedCard (keep id; preserve/repair figureSpec). If sound, accept. If fabricated/old-spec, reject.\n\n` +
    `THE CARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c._slot}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ card: c, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  const clean = { ...r.card }; delete clean._slot
  if (r.v.verdict === 'accept') kept.push(clean)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) { const f = { ...clean, ...r.v.fixedCard }; delete f._slot; kept.push(f) }
}
log(`Top-up verify: ${kept.length}/${cards.length} kept`)
return { kept, authoredCount: cards.length, keptCount: kept.length }
