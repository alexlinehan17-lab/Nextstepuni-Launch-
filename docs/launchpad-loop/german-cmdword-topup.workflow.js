export const meta = {
  name: 'german-cmdword-topup',
  description: 'Fill German Command-Word gaps: 4 OL stems (balance) + HL Perfekt Applied-Grammar cue',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic checks German + scheme + tappability' },
  ],
}

const TXT = '/tmp/german_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert GERMAN (written paper). The student taps the COMMAND WORD in a real
exam stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — german-YYYY-{HL,OL}-{written,aural,marking-scheme}.txt (pages
===PAGE n===). grep/Read for the exact stem + scheme answer. Do NOT invent question numbers/marks/wording. If you can't
verify the stem AND scheme, pick a different real question. Every German word/case/ending/Umlaut correct.

GERMAN CUE GRAMMAR: question-words (Warum/Wie/Was/Welche/Wo) under "auf Deutsch" → answer IN GERMAN ("Answers in language
not specified = half marks"); "Answer … in English" → English. Applied Grammar ("Schreiben Sie … im Perfekt") → the EXACT
tense/form ("Present Tense = 0" style penalties). Production ("Schreiben Sie X Sätze", "Beschreiben Sie") → Communication +
Language. Comprehension answers must be MANIPULATED into your own German (verbatim copy = half marks).

OUTPUT one object (schema's "stem"): id (kebab, 'de-' prefix, cue+topic), subjectId='german', subjectLabel='German', level,
questionRef, stem (faithful; MUST contain commandWord verbatim, same casing/Umlauts), commandWord, demand, trap (scheme
rule + marks consequence), source ('LC German {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int).

TAPPABILITY (a test enforces it): commandWord must be a CONSECUTIVE token-run in stem after stripping non-letters and
lowercasing. Verify it yourself.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','learn vocab'). trap = a real scheme rule.
Return data only; never edit a file.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stem'],
  properties: {
    stem: {
      type: 'object',
      required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string', enum: ['higher', 'ordinary'] }, questionRef: { type: 'string' },
        stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
        trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
      },
    },
  },
}

const SLOTS = [
  { key: 'ol-question-word-german', level: 'ordinary',
    topic: 'An ORDINARY German-answer comprehension stem with a question-word cue (Warum/Was/Wie/Welche/Wo) answered "auf Deutsch". Real OL Text question. Demand: extract the asked info and answer in German. Trap: answering in English (half marks), or missing the info.' },
  { key: 'ol-answer-english', level: 'ordinary',
    topic: 'An ORDINARY "Answer … in English" comprehension stem (the English-answer section of an OL Text). Demand: answer in English with the asked detail. Trap: answering in German loses marks; missing detail.' },
  { key: 'ol-production-schreiben', level: 'ordinary',
    topic: 'An ORDINARY production stem — "Schreiben Sie …" (e.g. a short note/email, or "Schreiben Sie X Sätze"). Real OL written-production question. Demand: produce the German text covering the points. Trap: missing a point/too few sentences (Communication); broken cases/verbs/word-order (Language).' },
  { key: 'ol-beschreiben-or-wie', level: 'ordinary',
    topic: 'A SECOND ORDINARY comprehension/production stem with a DIFFERENT cue from the others (e.g. "Beschreiben Sie…", or a "Wie/Wo" question, or "Wann"). Real OL question. Same demand/trap logic, in German where the rubric requires German.' },
  { key: 'hl-perfekt-applied-grammar', level: 'higher',
    topic: 'A HIGHER Applied-Grammar (Angewandte Grammatik) stem for the PERFEKT — "Schreiben Sie die folgenden unterstrichenen Verben im Perfekt" (or equivalent). The highest-yield, most-botched HL tense conversion. Demand: form the Perfekt correctly (haben/sein auxiliary + past participle; movement/change verbs take SEIN; ge-…-t weak vs ge-…-en strong). Trap: wrong auxiliary (sein vs haben), wrong participle, or leaving it in another tense scores 0.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nPREFERRED level: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded stem for this slot.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.stem ? { ...r.stem, _slot: s.key } : null),
))

const stems = authored.filter(Boolean)
log(`Authored ${stems.length} top-up stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'germanCorrect', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, germanCorrect: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC + native-level German checker verifying ONE Command-Word stem against ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive token-run in stem? else fix.\n` +
    `2. GERMAN ACCURACY: every German word/case/ending/verb form/Umlaut in stem, demand, trap correct? (esp. Perfekt: sein vs haben, participle).\n` +
    `3. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + scheme rule match? else grounded:false.\n` +
    `4. QUALITY: demand specific (no filler)? trap a real scheme rule?\n` +
    `If fixable, verdict:fix with a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated, reject.\n\n` +
    `THE STEM:\n${JSON.stringify(s, null, 2)}`,
    { label: `verify:${s._slot}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ stem: s, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  const clean = { ...r.stem }; delete clean._slot
  if (r.v.verdict === 'accept') kept.push(clean)
  else if (r.v.verdict === 'fix' && r.v.fixedStem) { const f = { ...clean, ...r.v.fixedStem }; delete f._slot; kept.push(f) }
}
log(`Top-up verify: ${kept.length}/${stems.length} kept`)
return { kept, authoredCount: stems.length, keptCount: kept.length }
