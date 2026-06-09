export const meta = {
  name: 'hist-catchup-topup',
  description: 'Fill History Catch-Up gaps: OL DBQ comparison + contextualisation, value/usefulness criticism, OL essay craft (non-Stalin)',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + accuracy-checks each' },
  ],
}

const TXT = '/tmp/hist_txt'

const VALID = `Valid history topicIds (Later Modern ONLY): history-2-* (Irish 1815-1993) and history-3-* (Europe & Wider World).
e.g. history-2-6 Dublin 1913 Lockout, 2-9 Treaty Negotiations 1921, 2-17 Sunningdale Agreement, 2-2 Catholic Emancipation,
2-11 Eucharistic Congress 1932, 2-21 First Economic Programme; history-3-13 Hungarian Uprising 1956, 3-21 Montgomery Bus
Boycott, 3-22 Johnson & Vietnam, 3-23 Moon Landing 1969, 3-8 Dictatorship & Democracy 1920-1945. Card strand = topicId minus last -N.`

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for Leaving Cert HISTORY (Later Modern, 1815-1993). A card teaches a student
who lost marks how to recover them: clear gist, the ONE highest-leverage move, a check question + model answer.

GROUNDING: ground the card in a REAL SEC LC History question + marking scheme. Text of papers + schemes (2021-2025,
HL+OL) at ${TXT}/ (pages ===PAGE n===): history-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact
question + how the scheme awards it. Do NOT invent wording, marks, or scheme content. Copyright cleared — quote short
document extracts faithfully.

IMPORTANT — the 2021-2025 DBQ documents are TEXT extracts (no cartoons/photos/posters in these years). Embed the needed
text extract INLINE in the prompt. Do NOT invent a visual source and do NOT add a figureSpec.

HISTORY MARKING GRAMMAR: essays marked by CUMULATIVE marks counting Significant Relevant Statements (SRS) — each
distinct, accurate, RELEVANT point; relevance to the exact question (not narration) drives the mark. DBQ Q-types:
comprehension (lift the stated point), COMPARISON (cross-reference two documents on the same theme — single-doc answers
capped at half marks), CRITICISM (judge reliability/VALUE/usefulness/objectivity by who/when/why), CONTEXTUALISATION
(a mini-essay placing the documents in wider context, marked cumulatively by SRS — the biggest single DBQ mark earner).

${VALID}

CARD FIELDS: id (kebab, 'hist-' prefix, includes topic), subjectId='history', topicId (valid history-2-*/3-*),
subjectLabel='History', topicLabel (short), focus (short row label), level ('higher'|'ordinary'),
gist (2-5 sentences), oneMove {label, text} (specific history move — not filler),
check {prompt (self-contained; embed any needed extract inline), modelAnswer (full), needed (>=2 SRS/award-point strings)},
source ('Topic … — SEC LC History {YEAR} {LEVEL}, Section …, Q… + marking scheme (…)'), marksWeight (int).
QUALITY: BANNED filler: 'read the question', 'manage your time', 'plan your answer', 'write neatly'. Plain text, ASCII quotes.
Return data only; never edit a file.
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
      },
    },
  },
}

const SLOTS = [
  { key: 'ol-dbq-comparison', level: 'ordinary',
    topic: 'OL DBQ COMPARISON card. Find a real OL Documents-Based Question comparison sub-question (the "do both documents..." / "compare" type) from an OL paper. Teach cross-referencing the two documents on the same theme rather than summarising each. Embed the two short text extracts inline. NON-Stalin topic preferred. Peg topicId to the DBQ case study.' },
  { key: 'ol-dbq-contextualisation', level: 'ordinary',
    topic: 'OL DBQ CONTEXTUALISATION card (the biggest single OL DBQ mark earner — the final mini-essay placing the documents in their wider context, marked cumulatively). Find a real OL DBQ contextualisation question. Teach building the answer from several SRS about the wider context, not re-summarising the documents. NON-Stalin topic preferred.' },
  { key: 'hl-criticism-value-usefulness', level: 'higher',
    topic: 'HL DBQ CRITICISM card on the VALUE/USEFULNESS phrasing specifically ("What would you consider to be the value of document X as a historical source?" / "How useful is this source to a historian?"). The 2023 HL DBQ uses exactly this ("the value of document A as a historical source"). Teach judging value by who wrote it/when/why + what it does and does NOT tell a historian (limitation). NON-Stalin (e.g. the 2023 Sunningdale/UWC-strike DBQ). Embed the relevant short extract inline.' },
  { key: 'ol-essay-craft', level: 'ordinary',
    topic: 'OL ESSAY-CRAFT card: how an OL essay earns marks — building the answer from several accurate, relevant statements (SRS/cumulative), staying on the exact question, and a clear opening + closing. Ground it on a real OL essay question + scheme. NON-Stalin topic. Teach the relevance/SRS idea at OL level.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED level: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded card for this slot.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.card ? { ...r.card, _slot: s.key } : null),
))

const cards = authored.filter(Boolean)
log(`Authored ${cards.length} top-up cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'historicallyAccurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, historicallyAccurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE History Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question matching "${c.source}"? marks + scheme award approach (cumulative/SRS; the specific DBQ award points) match the scheme text? else grounded:false.\n` +
    `2. HISTORICAL ACCURACY: all dates/names/events/causes correct? else historicallyAccurate:false.\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (text extract embedded if a DBQ card)? else selfContained:false.\n` +
    `4. TECHNIQUE: comparison=cross-reference; criticism=value-by-who/when/why+limitation; contextualisation=wider-context SRS; essays=SRS/relevance. Correct per scheme?\n` +
    `5. QUALITY: oneMove a specific move (no filler)? needed[] real award points? topicId a valid history-2-*/3-* id? NOT a visual/figure dependency?\n` +
    `If fixable, verdict:fix with a complete corrected card in fixedCard (keep id). If sound, accept. If fabricated/inaccurate, reject.\n\n` +
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
