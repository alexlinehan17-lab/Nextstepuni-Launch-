export const meta = {
  name: 'jc-science-catchup-topup',
  description: 'Top-up critic-identified signature-topic gaps (accuracy/precision, phases/eclipses, food chains, renewable energy, element/compound/mixture) in the JC Science Catch-Up set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic re-checks the science per card' } ],
}

const TXT = '/tmp/jc_science_txt'

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for JUNIOR CYCLE SCIENCE (reformed NCCA spec, first examined 2019). COMMON
LEVEL only — every card level MUST be 'common'. A card helps a student recover marks: a clear gist of the concept, the ONE
highest-leverage move (or classic error), and a SELF-CONTAINED check + correct model answer.

EXAM: single Common-Level terminal paper, 360 marks, Section A short Qs + Section B long Qs. Marking gives accepted
answers, often "any one/two from: ...". "Name TWO" needs two distinct points; "Explain/Justify" needs the reason.

THE CARD: { id (kebab, prefix 'jcsci-'), subjectId:'jc-science', topicId, subjectLabel:'Science (Junior Cycle)',
topicLabel (EXACT name), focus, level:'common', gist (2-5 sentences), oneMove:{label,text}, check:{prompt (SELF-CONTAINED
— embed the data/scenario; describe any diagram in words), modelAnswer (correct answer), needed (>=2 marking points)},
source ('Topic … — SEC JC Science {YEAR} CL, Q… + marking scheme (…accepted answers…)'), marksWeight (integer) }.

SCIENCE CORRECTNESS (hard): everything must be scientifically correct and within JC scope (no LC-only depth).
GROUNDING: real SEC questions + schemes at ${TXT}/jc-science-YYYY-CL-{paper,marking-scheme}.txt (2022-2025). Do NOT invent
question numbers, marks, or scheme wording. Return data only; edit no files.
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
  { key: 'accuracy-precision', want: `topicId jc-science-0-2 · topicLabel 'Designing fair tests: variables, controls, reliability, accuracy, precision & safety' · focus on ACCURACY vs PRECISION (the signature trap): accuracy = how close a measurement is to the TRUE value; precision = how close repeated measurements are to EACH OTHER. They are NOT the same. Ground in a real question (e.g. 2024 Q12 accuracy/precision). The check must make the student distinguish the two correctly.` },
  { key: 'phases-eclipses', want: `topicId jc-science-4-2 · topicLabel 'The Earth-Sun-Moon system: day & night, seasons, lunar phases & eclipses' · focus on WHY we see Moon phases vs why eclipses occur/are rare (phases = the half-lit Moon seen from different orbital positions; a solar eclipse = the Moon directly between Sun and Earth in a line). Ground in a real Earth-Sun-Moon question (e.g. 2024 Q14).` },
  { key: 'food-chain', want: `topicId jc-science-3-4 · topicLabel 'Habitats, adaptation, competition & interdependence (habitat studies)' · focus on reading a FOOD CHAIN: arrows show energy flow (eaten → eater); name producer vs consumer; predict what happens to one population when another is removed (interdependence). Ground in a real food-chain question (e.g. 2024 Q1).` },
  { key: 'renewable-nonrenewable', want: `topicId jc-science-4-4 · topicLabel 'Energy sources & meeting Earth's current and future energy needs' · focus on classifying an energy source as RENEWABLE vs NON-RENEWABLE and giving ONE advantage or drawback with a reason. Ground in a real energy-sources question (e.g. 2024 Q2).` },
  { key: 'element-compound-mixture', want: `topicId jc-science-2-2 · topicLabel 'Classifying substances: elements, compounds, mixtures, metals & non-metals' · focus on element vs compound vs mixture: a compound is chemically joined in a fixed ratio; a mixture is just physically mixed and easily separated — classify a given substance and justify. Ground in a real classifying-substances question.` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE card (level 'common'). The science must be correct.`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))
const cards = authored.filter(Boolean).map((r) => r.card).filter(Boolean)
log(`Authored ${cards.length}/${SLOTS.length} gap cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'sciCorrect', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, sciCorrect: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', properties: CARD_PROPS },
  },
}
const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Science (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. SCIENCE CORRECTNESS: is everything correct and within JC scope? Especially: accuracy≠precision not swapped; phases vs eclipses correct; food-chain arrows = energy flow; renewable/non-renewable classified right; compound (chemically joined, fixed ratio) vs mixture (physically mixed, separable). If wrong → fix.\n` +
    `2. GROUNDING: real question near "${c.source}" (2022-2025 CL)? marks + accepted answers match?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (scenario + any diagram described in words)?\n` +
    `4. LEVEL: level exactly 'common'? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific science move or marking behaviour?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedCard (same id, level 'common'). If sound, accept. If fabricated/unsalvageable, reject.\n\nTHE CARD:\n${JSON.stringify(c, null, 2)}`,
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
