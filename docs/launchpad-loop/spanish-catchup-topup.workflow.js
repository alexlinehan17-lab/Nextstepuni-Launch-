export const meta = {
  name: 'spanish-catchup-topup',
  description: 'Fill Spanish Catch-Up gaps: HL literature personal-response, OL cultural content, HL subjunctive vs indicative',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic checks Spanish + self-containment + grounding' },
  ],
}

const TXT = '/tmp/spanish_txt'

const SHARED = `
Authoring ONE Catch-Up Lane RECOVERY CARD for Leaving Cert SPANISH. A card teaches a student who fell behind how to
recover written-paper marks: a clear gist, the ONE highest-leverage move, and a SELF-CONTAINED check + model answer.

GROUNDING: use real SEC text at ${TXT}/ — spanish-YYYY-{HL,OL}-{written,aural,marking-scheme}.txt (pages ===PAGE n===).
Ground the technique + cite a real question/section where it is tested. Do NOT invent marks/wording. Every Spanish word,
accent, gender, and verb form MUST be correct.

SPANISH WRITTEN-PAPER SHAPE: HIGHER = Section A Reading Comp (70; Q1 EITHER (a) Prescribed Literature OR (b) Journalistic
Text, Q2), Section B Reading Comp + Opinion Writing (100), Section C Written Production (50). ORDINARY = Section A Reading
Comp (160), Section B Written Production (60). Production/opinion is marked on Communication AND Language (grammar/tense/vocab).
The Prescribed Literature option (Q1(a)) includes a "Discuss/your opinion" written response on the set text.

THE CARD (schema "card"): id (kebab, 'es-' prefix, unique, topic in it), subjectId='spanish', topicId (EXACTLY the slot's
valid id), subjectLabel='Spanish', topicLabel (short), focus (short disambiguating row label), level ('higher'|'ordinary'),
gist (2-5 sentences; Spanish examples with English glosses), oneMove {label,text} (the single highest-leverage move/error),
check {prompt (SELF-CONTAINED — embed any Spanish snippet inline; a fill-gap / structure-this / short-write works),
modelAnswer (correct Spanish + one-line why), needed (>=2 specific things a full answer includes)}, source ('Topic … —
SEC LC Spanish {YEAR} {LEVEL}, Q… + marking scheme (…)'), marksWeight (int).

SELF-CONTAINMENT (hard rule): the check must be answerable from the card + general Spanish. NEVER require an unseen set
text, passage, or aural. For a literature card, teach the STRUCTURE/technique with a self-contained model (a student does
NOT need to have read a specific novel) — e.g. "react to a theme" using a short embedded quote or a named common theme.

QUALITY: oneMove names a SPECIFIC move/error. BANNED filler: 'read the question','manage your time','learn vocab'. Spanish
accents/ñ/¿¡ fine. Return data only; never edit a file.
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
  { key: 'hl-literature-response', level: 'higher', topicId: 'spanish-2-5',
    topic: 'HL PRESCRIBED LITERATURE written response (Section A Q1(a) "Discuss" / opinion on the set text). Teach how to STRUCTURE a personal reaction: name the theme + state your view + back it with a reason — NOT plot summary. The marks reward your own analysis in Spanish, not retelling the story. Keep self-contained: use a generic theme (e.g. la familia, la injusticia, la esperanza) and a short embedded model; the student must not need to have read a specific novel.' },
  { key: 'ol-cultural-content', level: 'ordinary', topicId: 'spanish-2-0',
    topic: 'OL CULTURAL-TOPIC content (present-day Spanish-speaking world). Teach giving a concrete cultural fact in the set language — name a Spanish-speaking country / festival / famous figure and one real fact (e.g. La Tomatina in Buñol, Día de los Muertos in Mexico, the siesta, tapas). The current culture cards are technique-only; this adds real content the student can deploy. Self-contained check: recall/produce one fact in Spanish.' },
  { key: 'hl-subjunctive-vs-indicative', level: 'higher', topicId: 'spanish-1-3',
    topic: 'HL SUBJUNCTIVE vs INDICATIVE after the SAME conjunction — the high-frequency error the triggers card does not isolate. Teach "cuando + subjunctive for the future/unknown (cuando sea mayor = when I am older) vs cuando + indicative for habitual/past fact (cuando soy/era…)", and similar (aunque, hasta que). Self-contained fill-gap check contrasting the two.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED topicId: ${s.topicId}\nLEVEL: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded, self-contained card for this slot with topicId='${s.topicId}'.`,
    { label: `author:${s.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ).then((r) => r && r.card ? { ...r.card, _slot: s.key } : null),
))

const cards = authored.filter(Boolean)
log(`Authored ${cards.length} top-up cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'spanishCorrect', 'selfContained', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    spanishCorrect: { type: 'boolean' }, selfContained: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
        subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
        level: { type: 'string' }, gist: { type: 'string' },
        oneMove: { type: 'object', properties: { label: { type: 'string' }, text: { type: 'string' } } },
        check: { type: 'object', properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
        source: { type: 'string' }, marksWeight: { type: 'integer' },
      },
    },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC + native-level Spanish checker verifying ONE Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. SPANISH ACCURACY: every word/accent/conjugation/gender correct in gist, oneMove, check prompt AND modelAnswer? (subjunctive forms, ser/estar, agreement).\n` +
    `2. SELF-CONTAINMENT: check answerable from the card alone + general Spanish (no unseen set text/passage)? If it needs a specific novel the student may not have read → fix to a self-contained model.\n` +
    `3. GROUNDING: technique real for LC Spanish, topicId is '${c.topicId}', cited section plausible?\n` +
    `4. CULTURAL FACT (if a culture card): is the fact TRUE (real festival/place/figure)? else fix.\n` +
    `5. QUALITY: oneMove specific (no filler)?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id + topicId). If sound, accept. If irredeemable, reject.\n\n` +
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
