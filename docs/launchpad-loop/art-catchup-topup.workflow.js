export const meta = {
  name: 'art-catchup-topup',
  description: 'Fill Art Catch-Up gaps: HL 20th-c/contemporary European movement, OL Impressionism, OL modern Irish artist',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic checks grounding + art-fact accuracy' },
  ],
}

const TXT = '/tmp/art_txt'

const SHARED = `
Authoring ONE Catch-Up Lane RECOVERY CARD for Leaving Cert ART — VISUAL STUDIES (written paper). A card teaches a student
who lost marks how to recover them: gist, the ONE highest-leverage move, and a SELF-CONTAINED check + model answer.

EXAM SHAPE: Visual Studies written paper 150 marks. Section A (short, plates). Section B "Europe and the wider world"
(50-mark essay). Section C "Ireland and its place" (50-mark essay). These essay cards teach the BACKBONE (movement/context
+ named artist + named work + analysis), self-contained (the student supplies the example) — NO figureSpec.

GROUNDING: ground in REAL SEC LC Art questions + schemes at ${TXT}/ (art-YYYY-{HL,OL}-{written,marking-scheme}.txt, pages
===PAGE n===). Do NOT invent question numbers/marks/scheme wording. Art FACTS MUST be accurate — artist names, artwork
titles, DATES, movements, places. Ground facts in the scheme or a real exam reference; never guess a date or attribution.

THE CARD (schema "card"): id (kebab, 'art-' prefix, unique), subjectId='art', topicId (EXACTLY the slot's id), subjectLabel='Art',
topicLabel (the curriculum subtopic's EXACT name — see slot), focus, level, gist (2-5 sentences, accurate facts),
oneMove {label,text} (a specific art move/fact), check {prompt (SELF-CONTAINED; ask for the essay structure/key points,
not a full essay), modelAnswer, needed (>=2 indicative-content points)}, source ('Topic … — SEC LC Art (Visual Studies)
{YEAR} {LEVEL}, Section …, Q… + marking scheme (…)'), marksWeight (int). NO figureSpec for these essay cards.

QUALITY: oneMove names a SPECIFIC art fact (e.g. 'Impressionists painted en plein air with broken colour to catch
changing light — Monet, Impression, Sunrise, 1872'; 'Pop Art took mass-culture imagery — Warhol, Campbell's Soup Cans,
1962'). BANNED filler: 'read the question','manage your time','be creative'. Return data only; never edit a file.
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
      },
    },
  },
}

const SLOTS = [
  { key: 'hl-european-20thc', level: 'higher', topicId: 'art-3-1', topicLabel: 'Artists and Artworks',
    topic: 'A 20th-century / contemporary EUROPEAN movement for Section B (Section B is currently all pre-1910). Pick ONE real movement and a named artist + work: Surrealism (Dalí, The Persistence of Memory, 1931), Abstract Expressionism (Pollock), Pop Art (Warhol, Campbell\'s Soup Cans, 1962; or Hamilton), Expressionism (Munch, The Scream, 1893) or a contemporary installation/conceptual artist. Teach the essay backbone: movement + context + named work + analysis. Accurate dates.' },
  { key: 'ol-impressionism', level: 'ordinary', topicId: 'art-3-1', topicLabel: 'Artists and Artworks',
    topic: 'IMPRESSIONISM at OL — the most commonly attempted OL Section B essay, currently missing. Teach the backbone: the movement (1870s France, painting en plein air, broken colour, capturing fleeting light/atmosphere, visible brushwork), a named artist + work (Monet, Impression, Sunrise, 1872; or Renoir; Degas). Self-contained essay scaffold.' },
  { key: 'ol-irish-modern', level: 'ordinary', topicId: 'art-3-1', topicLabel: 'Artists and Artworks',
    topic: 'A 20th-century IRISH artist for Section C at OL (OL Irish is currently only heritage — Kells, Georgian). Pick ONE real modern Irish artist + work: Jack B. Yeats (expressive late paintings, e.g. The Liffey Swim, 1923), Harry Clarke (stained glass, e.g. the Geneva Window / Bewley\'s windows), Louis le Brocquy, Paul Henry (West of Ireland landscapes), Evie Hone or Mainie Jellett (Irish modernism). Teach the essay backbone with accurate facts.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED topicId: ${s.topicId}\nREQUIRED topicLabel: ${s.topicLabel}\nLEVEL: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded, self-contained card for this slot with topicId='${s.topicId}'.`,
    { label: `author:${s.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ).then((r) => r && r.card ? { ...r.card, _slot: s.key } : null),
))

const cards = authored.filter(Boolean)
log(`Authored ${cards.length} top-up cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'factsAccurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, factsAccurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id + same topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC + art historian verifying ONE Art (Visual Studies) Catch-Up card. Default REJECT/FIX if off.\n` +
    `1. ART-FACT ACCURACY (critical): every artist name, artwork TITLE, DATE, movement and place correct? (e.g. Impression, Sunrise is 1872, Monet; Campbell's Soup Cans 1962, Warhol; The Liffey Swim 1923, Jack B. Yeats). Any wrong fact → factsAccurate:false and fix it.\n` +
    `2. GROUNDING: is this a real LC Art Section B/C essay topic? topicId='${c.topicId}', topicLabel the exact curriculum name?\n` +
    `3. SELF-CONTAINMENT: check answerable from the card + general knowledge (essay scaffold, no unseen plate)?\n` +
    `4. QUALITY: oneMove a specific art fact (no filler)? needed[] real indicative-content points?\n` +
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
