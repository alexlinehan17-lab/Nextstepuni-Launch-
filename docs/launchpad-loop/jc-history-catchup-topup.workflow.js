export const meta = {
  name: 'jc-history-catchup-topup',
  description: 'Top-up critic-identified gaps (source usefulness+limitation, Famine, independence, Troubles, a revolution, World Wars, dictatorship, Holocaust) in the JC History Catch-Up set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic re-checks historical accuracy' } ],
}

const TXT = '/tmp/jc_history_txt'

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for JUNIOR CYCLE HISTORY (reformed NCCA spec, first examined 2019). COMMON
LEVEL only — level MUST be 'common'. A card helps a student recover marks: gist + the ONE highest-leverage move + a
SELF-CONTAINED check + correct model answer. 360-mark paper, 8 questions, source/cartoon/photo heavy.

THE CARD: { id (kebab, prefix 'jchist-'), subjectId:'jc-history', topicId, subjectLabel:'History (Junior Cycle)',
topicLabel (EXACT name), focus, level:'common', gist, oneMove:{label,text}, check:{prompt (SELF-CONTAINED — embed any
source extract / describe the cartoon-photo in words and give the facts), modelAnswer (correct), needed (>=2 marking
points)}, source ('Topic ... — SEC JC History {YEAR} CL, Q... + marking scheme (...accepted answers...)'), marksWeight
(integer) }.

HISTORICAL ACCURACY (hard): every fact, name, date and event correct and within JC scope (no LC-only depth). GROUNDING:
real SEC questions + schemes at ${TXT}/jc-history-YYYY-CL-{paper,marking-scheme}.txt (2022-2025). Do NOT invent question
numbers/marks/wording. Return data only. Use plain apostrophes inside text (avoid breaking JSON).
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
  { key: 'source-usefulness-limitation', want: `topicId jc-history-0-0 · topicLabel 'Working with sources and evidence (primary vs secondary, usefulness and limitations)' · the MUST-ADD: judging a source's USEFULNESS and a LIMITATION. Teach: say how the source is useful (what it tells a historian) AND give one limitation (it is one-sided / does not show the whole picture / the author was biased). The signature trap: giving usefulness with NO limitation. Ground in a real source-usefulness question.` },
  { key: 'great-famine', want: `topicId jc-history-1-2 · topicLabel 'The Great Famine and the Irish Diaspora' · the Great Famine (1845-1849): a cause (potato blight / over-dependence on the potato), effects (death, mass emigration), and the Diaspora. Ground in a real Famine question.` },
  { key: 'struggle-for-independence', want: `topicId jc-history-1-5 · topicLabel 'Nationalism, unionism and the struggle for independence, 1911-1923 (1916 Rising, War of Independence, Civil War)' · the 1916 Rising and the road to independence: a cause/event/consequence, a key figure (Pearse, Connolly, Collins, de Valera). Ground in a real independence question.` },
  { key: 'northern-ireland-troubles', want: `topicId jc-history-1-9 · topicLabel 'The Northern Ireland Troubles and North-South / Anglo-Irish relations' · the Troubles: a cause (discrimination / civil rights), an event (Bloody Sunday, internment), or the path to peace (the Good Friday Agreement, 1998). Ground in a real Troubles question.` },
  { key: 'a-revolution', want: `topicId jc-history-2-5 · topicLabel 'A revolution in pre-twentieth-century Europe or the wider world (e.g. American, French)' · the American OR French Revolution: a cause (taxation, Enlightenment ideas) and a consequence (a republic, the Declaration / Rights of Man). Ground in a real revolution question.` },
  { key: 'world-wars', want: `topicId jc-history-2-7 · topicLabel 'World War One or World War Two: causes, course and impact' · WWI or WWII: a cause (alliances / the assassination of Franz Ferdinand for WWI; the Treaty of Versailles / Hitler's expansion for WWII) and an impact on ordinary people. Ground in a real World War question.` },
  { key: 'dictatorship', want: `topicId jc-history-2-8 · topicLabel 'Dictatorship in the twentieth century: life in a fascist and a communist country' · life under a dictatorship — Nazi Germany (Hitler, the SS, propaganda, persecution) or Stalin's USSR (collectivisation, the secret police, the Five-Year Plans). Teach a feature of how the dictator controlled people. Ground in a real dictatorship question.` },
  { key: 'the-holocaust', want: `topicId jc-history-2-9 · topicLabel 'Genocide and the Holocaust' · the Holocaust: what it was (the Nazi murder of six million Jews and others), a stage (ghettos, concentration/death camps), and why survivor/eyewitness testimony is a key primary source. Handle with care and accuracy. Ground in a real Holocaust question (e.g. 2023 Q6 Tomi Reichental).` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE card (level 'common'). Every fact/name/date must be correct.`,
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
    `Independent SKEPTIC verifying ONE JC History (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. HISTORICAL ACCURACY: every fact, name, date and event correct and within JC scope? (Famine 1845-49; WWI 1914-18 / WWII 1939-45; Holocaust = 6 million Jews; Good Friday Agreement 1998; 1916 Rising.) For the source-usefulness card: does it require a limitation as well as usefulness? If wrong → fix.\n` +
    `2. GROUNDING: real question near "${c.source}" (2022-2025 CL)? marks + accepted answers match?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (source extract / facts embedded)?\n` +
    `4. LEVEL 'common'? topicId valid (jc-history-N-N leaf) + topicLabel exact?\n` +
    `5. oneMove specific? Sensitive topics handled accurately and respectfully?\n` +
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
