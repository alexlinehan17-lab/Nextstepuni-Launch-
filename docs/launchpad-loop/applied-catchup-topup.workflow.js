export const meta = {
  name: 'applied-catchup-topup',
  description: 'Fill Applied Maths Catch-Up gaps: OL Kruskal MST, OL networks terminology, OL Forces/FBD, OL circular motion, HL modelling cycle',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic recomputes vs scheme' },
  ],
}

const TXT = '/tmp/applied_txt'

const SHARED = `
Authoring ONE Catch-Up Lane RECOVERY CARD for Leaving Cert APPLIED MATHEMATICS (current modelling spec, first examined
2023). Recover lost marks: gist, the ONE highest-leverage move, a SELF-CONTAINED check + FULLY WORKED model answer.

GROUNDING (non-negotiable): real SEC questions from 2023, 2024 or 2025 ONLY at ${TXT}/ —
applied-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===). 2021-2022 are the OLD syllabus — do NOT use.
grep/Read for the real question + scheme. RECOMPUTE every value vs the scheme (g = 9.8 unless stated). Do NOT invent.

LEVEL PURITY (hard rule): the card's level MUST match the level of the paper the question is on. An OL slot card must be
grounded in an ORDINARY-level question; if the topic only appears at HL, say so and ground at HL instead (never put an HL
question in the OL section).

THE CARD (schema "card"): id (kebab, 'am-' prefix, unique), subjectId='applied-mathematics', topicId (EXACTLY the slot id),
subjectLabel='Applied Mathematics', topicLabel (the verified subtopic's EXACT name — see slot), focus, level, gist,
oneMove {label,text} (specific move/error), check {prompt (SELF-CONTAINED — embed ALL data inline; for a network embed the
edge-list/table OR add a figureSpec), modelAnswer (FULLY WORKED: formula→substitution→value+UNIT), needed (>=2 award
points)}, source ('Topic … — SEC LC Applied Mathematics {YEAR} {LEVEL}, Q… + marking scheme (…)'), marksWeight (int),
figureSpec OPTIONAL { year, level, questionRef, source ('paper'|'scheme'), describes, whyNeeded } for a printed network/graph.

QUALITY: oneMove specific (BANNED filler: 'show your working','read the question','practice more'). Return data only.
`

const CARD_SCHEMA = {
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
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const SLOTS = [
  { key: 'ol-kruskal', level: 'ordinary', topicId: 'applied-mathematics-1-2', topicLabel: 'Minimum Spanning Trees (Kruskal and Prim)',
    topic: 'OL KRUSKAL minimum spanning tree (Kruskal absent from the whole set; the subtopic is literally named Kruskal AND Prim). Find a real OL question (e.g. 2025 OL Q9(a) uses Kruskal). Teach: sort edges ascending, add each unless it forms a cycle, stop at n−1 edges. Embed the distance table OR add a figureSpec. RECOMPUTE the total.' },
  { key: 'ol-networks-terminology', level: 'ordinary', topicId: 'applied-mathematics-1-0', topicLabel: 'Networks and Their Associated Terminology',
    topic: 'OL networks terminology / reading a network (subtopic 1-0 has zero cards). A real OL question on vertices/edges/weights/degree/connected, or building/reading an adjacency representation. Embed the small network inline or add a figureSpec.' },
  { key: 'ol-forces-fbd', level: 'ordinary', topicId: 'applied-mathematics-2-3', topicLabel: "Forces, Newton's Laws and Free-Body Diagrams",
    topic: 'OL Forces / Newton\'s second law (2-3 is HL-only in the set). A real OL F=ma question (a car/block on a horizontal or inclined plane, a lift, a simple connected system). Teach resolving + F=ma. RECOMPUTE the value+unit.' },
  { key: 'ol-circular-motion', level: 'ordinary', topicId: 'applied-mathematics-2-7', topicLabel: 'Circular Motion of a Particle',
    topic: 'OL circular motion (2-7 is HL-only; basic v=rω, a=v²/r, ω is on the OL spec — e.g. 2024 OL Q3 merry-go-round). A real OL question. Teach the relationships and one calculation. RECOMPUTE.' },
  { key: 'hl-modelling-cycle', level: 'higher', topicId: 'applied-mathematics-0-1', topicLabel: 'Formulating Problems',
    topic: 'HL modelling-cycle content (HL students currently see ZERO explicit modelling cards). A real HL question part that asks to STATE an assumption / define variables / justify a simplification (these recur across HL questions). Teach naming a SPECIFIC assumption tied to the model. Self-contained.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED topicId: ${s.topicId}\nREQUIRED topicLabel: ${s.topicLabel}\nLEVEL: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded, self-contained, fully-worked card with topicId='${s.topicId}'.`,
    { label: `author:${s.key}`, phase: 'Author', schema: CARD_SCHEMA },
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
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id + same topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Applied Mathematics Catch-Up card against ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question from 2023-2025 ONLY? marks + scheme match? LEVEL PURITY: is the source paper actually ${c.level}? (an OL card sourced from an HL paper → fix the level or reject.)\n` +
    `2. MATHS: RECOMPUTE every value in modelAnswer from the prompt; matches the scheme + units?\n` +
    `3. CONCEPTS: correct procedure (Kruskal cycle-check, F=ma resolution, v=rω)?\n` +
    `4. SELF-CONTAINMENT: data embedded or figureSpec present? topicId='${c.topicId}' + exact topicLabel?\n` +
    `5. QUALITY: oneMove specific?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (same id + topicId). If sound, accept. If irredeemable, reject.\n\n` +
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
