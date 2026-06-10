export const meta = {
  name: 'jc-business-catchup-topup',
  description: 'Top-up critic-identified gaps (P&L account, forms of ownership, marketing mix 4Ps, CCPC agency, international trade) in the JC Business Studies Catch-Up set + the real "Differentiate between" command cue, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic re-checks correctness' } ],
}

const TXT = '/tmp/jc_business_txt'

// ---- Catch-up cards ----
const CARD_SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for JUNIOR CYCLE BUSINESS STUDIES (reformed NCCA spec, first examined 2019).
COMMON LEVEL only — level MUST be 'common'. A card helps a student recover marks: gist + the ONE highest-leverage move +
a SELF-CONTAINED check + correct model answer. 270-mark paper, Section A short Qs + Section B applied Qs.

THE CARD: { id (kebab, prefix 'jcbus-'), subjectId:'jc-business-studies', topicId, subjectLabel:'Business Studies (Junior
Cycle)', topicLabel (EXACT name), focus, level:'common', gist, oneMove:{label,text}, check:{prompt (SELF-CONTAINED — embed
figures/scenario), modelAnswer (correct, with working), needed (>=2 marking points)}, source ('Topic … — SEC JC Business
Studies {YEAR} CL, Q… + marking scheme (…figures/accepted answers…)'), marksWeight (integer) }.

CORRECTNESS (hard): facts/definitions/calculations correct and within JC scope (NO LC-only accounting — no break-even,
ROCE/acid-test ratios, depreciation-method comparison, control accounts). GROUNDING: real SEC questions + schemes at
${TXT}/jc-business-studies-YYYY-CL-{paper,marking-scheme}.txt (2022-2025). Do NOT invent question numbers/marks/wording.
Return data only.
`
const CARD_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
  subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
  level: { type: 'string', enum: ['common'] }, gist: { type: 'string' },
  oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
  check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
  source: { type: 'string' }, marksWeight: { type: 'integer' },
}
const CARD_ONE = { type: 'object', required: ['card'], properties: { card: { type: 'object', required: ['id'], properties: CARD_PROPS } } }

const CARD_SLOTS = [
  { key: 'profit-and-loss', want: `topicId jc-business-studies-1-13 · topicLabel 'Final accounts: trading, profit & loss and financial position' · the PROFIT & LOSS account (the missing link in the final-accounts chain): net profit = gross profit + gains − expenses. Teach building the P&L from a gross profit figure. Ground in a real final-accounts question.` },
  { key: 'forms-of-ownership', want: `topicId jc-business-studies-1-2 · topicLabel 'Forms of business ownership & how a business is set up' · sole trader vs partnership vs limited company — a feature/advantage of each (signature high-frequency topic). Ground in a real question/scheme.` },
  { key: 'marketing-mix-4ps', want: `topicId jc-business-studies-1-8 · topicLabel 'The marketing mix & promoting a product' · the 4 Ps (Product/Price/Place/Promotion): identify which P a scenario describes. Trap = naming a method but not the correct P. Ground in a real marketing question.` },
  { key: 'ccpc-agency', want: `topicId jc-business-studies-0-8 · topicLabel 'Consumer agencies, banks & financial institutions' · name the ACTUAL consumer agency (the CCPC — Competition and Consumer Protection Commission) and what it does. Trap = "a consumer agency" earns no mark; you must NAME it. Ground in a real consumer question.` },
  { key: 'international-trade', want: `topicId jc-business-studies-2-6 · topicLabel 'International trade & globalisation' · imports vs exports and the balance of trade (visible exports − visible imports; surplus vs deficit). Trap = mixing up the direction/sign. Ground in a real trade/economy question.` },
]

phase('Author')
const cardResults = await parallel(CARD_SLOTS.map((s) => () =>
  agent(`${CARD_SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE card (level 'common'). Any calculation must be correct.`,
    { label: `card:${s.key}`, phase: 'Author', schema: CARD_ONE },
  )
))

// ---- One command-word stem: the REAL "Differentiate between" cue ----
const STEM_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
  level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
  stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
  trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
}
const STEM_ONE = { type: 'object', required: ['found'], properties: { found: { type: 'boolean' }, note: { type: 'string' }, stem: { type: 'object', properties: STEM_PROPS } } }

const stemResult = await agent(
  `You author ONE Command-Word Reflex stem for JUNIOR CYCLE BUSINESS STUDIES (Common Level; level MUST be 'common'). The
cue is 'Differentiate between' — the genuine contrast cue used by the SEC (e.g. 2023 CL Section B Q9(iii) "Differentiate
between employment and volunteerism for Martin"; 2024 CL "differentiate between the rights and responsibilities of an
employee"). commandWord MUST be 'Differentiate between' and appear verbatim as a consecutive token-run in the stem.
Demand: state the contrast on the SAME feature for BOTH items. Trap: describing only one side, or two non-contrasting
facts. Ground it in a REAL 2022-2025 question + scheme at ${TXT}/ (grep for "ifferentiate"). Do NOT invent question
numbers/marks/wording. Fields: { id (prefix 'jcbus-'), subjectId:'jc-business-studies', subjectLabel:'Business Studies
(Junior Cycle)', level:'common', questionRef, stem, commandWord, demand, trap, source, marks }. If not grounded, found:false.`,
  { label: 'stem:differentiate', phase: 'Author', schema: STEM_ONE },
)

phase('Verify')
const CARD_VERDICT = {
  type: 'object', required: ['verdict', 'grounded', 'correct', 'reason'],
  properties: { verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] }, grounded: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' }, fixedCard: { type: 'object', properties: CARD_PROPS } },
}
const cards = cardResults.filter(Boolean).map((r) => r.card).filter(Boolean)
const cardVer = await parallel(cards.map((c) => () =>
  agent(`Independent SKEPTIC verifying ONE JC Business Studies (Common Level) Catch-Up card vs real SEC sources at ${TXT}/. Default REJECT/FIX.\n1. CORRECTNESS: facts/definitions correct + within JC scope (no LC-only accounting)? WORK any calculation (P&L net profit, balance of trade) yourself. 2. GROUNDING: real question near "${c.source}"? 3. SELF-CONTAINMENT: answerable from the card? 4. LEVEL 'common'? topicId valid (jc-business-studies-N-N leaf, not strand) + topicLabel exact? 5. oneMove specific?\nIf fixable, verdict:fix WITH fixedCard (same id, level 'common', leaf topicId). Else accept/reject.\n\nCARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c.id}`, phase: 'Verify', schema: CARD_VERDICT },
  ).then((v) => ({ c, v }))
))
const keptCards = []
for (const r of cardVer.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') keptCards.push(r.c)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) keptCards.push({ ...r.c, ...r.v.fixedCard })
}

const STEM_VERDICT = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'reason'],
  properties: { verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] }, tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' }, fixedStem: { type: 'object', properties: STEM_PROPS } },
}
let keptStems = []
if (stemResult && stemResult.found && stemResult.stem) {
  const s = stemResult.stem
  const v = await agent(`Independent SKEPTIC verifying ONE JC Business Studies Command-Word stem vs real SEC sources at ${TXT}/. Default REJECT/FIX.\n1. TAPPABILITY: 'Differentiate between' a consecutive token-run in stem? 2. GROUNDING: real question at ${s.questionRef}? marks+rule match scheme? 3. SCOPE: within JC, level 'common'? 4. demand/trap specific?\nIf fixable verdict:fix WITH fixedStem (same id, level 'common'). Else accept/reject.\n\nSTEM:\n${JSON.stringify(s, null, 2)}`,
    { label: `verify:${s.id}`, phase: 'Verify', schema: STEM_VERDICT })
  if (v && v.verdict === 'accept') keptStems.push(s)
  else if (v && v.verdict === 'fix' && v.fixedStem) keptStems.push({ ...s, ...v.fixedStem })
}
log(`Verify: ${keptCards.length}/${cards.length} cards, ${keptStems.length} stems kept`)
return { keptCards, keptStems, unfounded: (stemResult && !stemResult.found) ? [stemResult.note] : [] }
