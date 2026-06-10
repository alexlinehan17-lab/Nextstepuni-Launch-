export const meta = {
  name: 'jc-irish-catchup-topup',
  description: 'Top-up the two critic-identified gap slots in the JC Irish Catch-Up set, then skeptic-verify each',
  phases: [
    { title: 'Author', detail: 'one agent per gap slot' },
    { title: 'Verify', detail: 'skeptic per card' },
  ],
}

const TXT = '/tmp/jc_irish_txt'

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for JUNIOR CYCLE IRISH (Gaeilge T2). A card teaches a student who lost marks
how to recover them: gist, the ONE highest-leverage move, and a SELF-CONTAINED check + model answer.

LANGUAGE REGISTER: BILINGUAL — English-led scaffolding quoting Irish exam terms/examples verbatim (audience: 14-15,
English-medium school). Fadas correct everywhere.

THE CARD: { id (kebab, prefix 'jcir-'), subjectId: 'jc-irish', topicId, subjectLabel: 'Irish (Junior Cycle)',
topicLabel (EXACT curriculum subtopic name), focus, level ('higher'|'ordinary'), gist (2-5 sentences),
oneMove { label, text }, check { prompt (SELF-CONTAINED — embed any Irish text needed; litríocht checks text-agnostic),
modelAnswer, needed (>=2 award points) }, source ('Topic … — SEC JC Irish (Gaeilge T2) {YEAR} {LEVEL}, Ceist … + marking
scheme (…guidance…)'), marksWeight (integer) }.

GROUNDING (non-negotiable): real SEC questions + schemes at ${TXT}/jc-irish-YYYY-{HL,OL}-{paper,marking-scheme}.txt
(2022-2025). Do NOT invent question numbers, marks, or scheme wording. LEVEL PURITY: card level = paper level.
QUALITY: oneMove a specific JC Irish move; banned filler ('read the question', 'manage your time').
Return data only; edit no files.
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
  { key: 'ol-meaitseail', want: `ORDINARY · topicId jc-irish-0-1 · topicLabel 'Léamhthuiscint (Reading Comprehension)' · focus ≈ "Meaitseáil (Ceist 8): lock in the pairs you KNOW first, then place the leftovers by elimination — never leave a box empty". Ground in a real OL Ceist 8 (e.g. 2024 or 2023 OL — 6-item sentences-to-pictures matching, 25 marc or per-scheme value; check the scheme for per-item marks). The check must embed a small self-contained matching task (e.g. 4 short Irish sentences + 4 picture descriptions in English) testing the elimination strategy.` },
  { key: 'hl-gearrsceal-eachtra', want: `HIGHER · topicId jc-irish-0-2 · topicLabel 'Litríocht (Studied Literature)' · focus ≈ "Gearrscéal (Ceist 8): retell ONE eachtra in 3-4 aimsir-chaite sentences — what kicked it off, what happened, how it ended". Ground in a real HL Ceist 8 (e.g. 2024 HL "Déan cur síos ar eachtra amháin sa ghearrscéal" + its band descriptors). TEXT-AGNOSTIC: teach the eachtra-retell structure for ANY studied gearrscéal; check answerable with any studied (or generic illustrative) story.` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE card.`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).map((r) => r.card).filter(Boolean)
log(`Authored ${cards.length}/${SLOTS.length} gap cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', properties: CARD_PROPS },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Irish Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question near "${c.source}"? marks + scheme guidance match?\n` +
    `2. SELF-CONTAINMENT: answerable from the card alone? litríocht card text-agnostic?\n` +
    `3. LEVEL PURITY: source paper actually ${c.level}?\n` +
    `4. ACCURACY: Irish correct (fadas, mutations)? topicId valid + topicLabel exact ('Léamhthuiscint (Reading Comprehension)' / 'Litríocht (Studied Literature)')?\n` +
    `5. QUALITY: oneMove specific, no filler?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedCard (same id). If sound, accept. If fabricated, reject.\n\nTHE CARD:\n${JSON.stringify(c, null, 2)}`,
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
