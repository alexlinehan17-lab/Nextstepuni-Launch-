export const meta = {
  name: 'jc-maths-catchup-topup',
  description: 'Top-up the critic-identified gaps (functions/graphs, constructions, histograms, Show-that/Hence traps) in the JC Maths Catch-Up set, then skeptic-verify',
  phases: [
    { title: 'Author', detail: 'one agent per gap slot' },
    { title: 'Verify', detail: 'skeptic re-works the maths per card' },
  ],
}

const TXT = '/tmp/jc_maths_txt'

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for JUNIOR CYCLE MATHEMATICS (reformed NCCA spec, first examined 2022). A card
helps a student recover marks: a clear gist of the technique, the ONE highest-leverage move (or classic error), and a
SELF-CONTAINED worked check + correct model answer.

EXAM: single terminal paper per level, HL+OL, 270 marks; marking uses SCALES with Low/High Partial Credit. A relevant
first step earns LPC even if unfinished; "Show that" needs visible working to the GIVEN answer; "Hence" must reuse the
previous part; constructions earn marks for visible compass arcs; units + rounding to the requested accuracy carry marks.

THE CARD: { id (kebab, prefix 'jcmth-'), subjectId:'jc-mathematics', topicId, subjectLabel:'Mathematics (Junior Cycle)',
topicLabel (EXACT name), focus, level('higher'|'ordinary'), gist (2-5 sentences), oneMove:{label,text}, check:{prompt
(SELF-CONTAINED — embed the numbers; describe any diagram in words), modelAnswer (full correct working + answer), needed
(>=2 method steps that earn marks)}, source ('Topic … — SEC JC Maths {YEAR} {LEVEL}, Q… + marking scheme (…scale…)'),
marksWeight (integer) }.

MATHS CORRECTNESS (hard): the model answer must be mathematically correct and complete; show the actual working. Plain
text maths (x^2, sqrt(), pi, <=). JC scope only — no calculus / sine-cosine rule / unit circle / enlargement / std
deviation; JC trig is right-angled SOHCAHTOA + Pythagoras.

GROUNDING: real SEC questions + schemes at ${TXT}/jc-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt (2022-2025). Do NOT
invent question numbers, marks, or scheme wording. LEVEL PURITY: card level = paper level. Return data only; edit no files.
`

const CARD_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
  subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
  level: { type: 'string', enum: ['higher', 'ordinary'] }, gist: { type: 'string' },
  oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
  check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
  source: { type: 'string' }, marksWeight: { type: 'integer' },
}
const ONE_SCHEMA = { type: 'object', required: ['card'], properties: { card: { type: 'object', required: ['id'], properties: CARD_PROPS } } }

const SLOTS = [
  { key: 'hl-functions-graphs', want: `HIGHER · topicId jc-mathematics-3-6 · topicLabel 'Functions & graphs' · the single biggest gap. Teach reading/using a function graph: find f(x) for a given x, read roots/intercepts off a graph, solve f(x)=g(x) graphically, or "use your graph to estimate ...". Ground in a real HL functions/graph question (e.g. 2024 HL Q8 reading a graph + transformation y=g(x)-2). The check must be self-contained (give the function rule or describe the graph's key points in words).` },
  { key: 'hl-constructions', want: `HIGHER · topicId jc-mathematics-2-3 · topicLabel 'Geometric reasoning, theorems & constructions' · a NAMED construction (e.g. construct the axis of symmetry / perpendicular bisector of a segment, an angle of 60, a triangle from given data). oneMove must encode the signature trap: marks are for the visible COMPASS ARCS / construction lines, not the final freehand figure; measuring instead of constructing scores little. Ground in a real HL construction question (e.g. 2023 HL Q12(a)).` },
  { key: 'hl-showthat-coordgeom', want: `HIGHER · topicId jc-mathematics-2-5 · topicLabel 'Co-ordinate geometry of the line' · a "Show that" on coordinate geometry (e.g. show three points are collinear via equal slopes, or show two slopes are equal/perpendicular). Encode the trap: when the answer is given, you must SHOW the slope calculations — stating it or eyeballing the grid scores little. Ground in a real HL coord-geometry question.` },
  { key: 'ol-histogram', want: `ORDINARY · topicId jc-mathematics-4-3 · topicLabel 'Representing data (graphs & charts)' · a HISTOGRAM card. Teach: for a histogram the bars TOUCH (continuous data) and for equal-width intervals the bar height = frequency; reading/drawing it; and "Hence, use your histogram to ..." means REUSE the graph you drew, don't restart. Ground in a real OL data-representation question.` },
  { key: 'ol-income-tax', want: `ORDINARY · topicId jc-mathematics-1-6 · topicLabel 'Financial maths (money problems)' · INCOME TAX (standard rate). Teach: gross tax = rate x gross income, then SUBTRACT the tax credit to get the tax actually due (net tax). The signature trap: forgetting to subtract the tax credit, or applying the rate to the wrong amount. Ground in a real OL/ HL income-tax question (USC/income tax appear most years).` },
  { key: 'ol-units-rounding', want: `ORDINARY · topicId jc-mathematics-2-0 · topicLabel 'Measure, units & time' · UNITS & ROUNDING. Teach: cm vs cm^2 (area) vs cm^3 (volume), converting units, and rounding to the requested accuracy (nearest cent / 2 d.p. / nearest m^2) — the correct unit and the correct rounding each carry a mark. Ground in a real OL measure/rounding question.` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE card. The model answer must be mathematically correct.`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))
const cards = authored.filter(Boolean).map((r) => r.card).filter(Boolean)
log(`Authored ${cards.length}/${SLOTS.length} gap cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'mathCorrect', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, mathCorrect: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', properties: CARD_PROPS },
  },
}
const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Maths Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. MATHS CORRECTNESS: WORK THE PROBLEM YOURSELF — is check.modelAnswer correct and complete? Does each 'needed' step earn marks? If wrong → fix.\n` +
    `2. GROUNDING: real ${c.level} question near "${c.source}"? marks + scheme scale match?\n` +
    `3. SELF-CONTAINMENT: solvable from the card alone (numbers + any diagram described in words)?\n` +
    `4. LEVEL PURITY + SCOPE: source paper actually ${c.level}? Method within JC scope (no LC-only technique)?\n` +
    `5. QUALITY: oneMove a specific maths move or marking behaviour? topicId valid + topicLabel exact + NOT the unifying strand?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedCard (same id). If sound, accept. If fabricated/unsalvageable, reject.\n\nTHE CARD:\n${JSON.stringify(c, null, 2)}`,
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
return { kept, keptCount: kept.length }
