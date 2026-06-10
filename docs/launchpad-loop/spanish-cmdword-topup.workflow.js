export const meta = {
  name: 'spanish-cmdword-topup',
  description: 'Fill Spanish Command-Word gaps: OL synonym cue, OL answer-in-Spanish, HL answer-in-English trap, OL inference, OL production',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic checks Spanish + scheme + tappability' },
  ],
}

const TXT = '/tmp/spanish_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert SPANISH. The student taps the COMMAND WORD / CUE in a real exam
stem, then learns what the cue demands + the marking-scheme trap. Spanish cues are bilingual (some questions answered in
Spanish, some in English).

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — spanish-YYYY-{HL,OL}-{written,aural,marking-scheme}.txt (pages
===PAGE n===). grep/Read for the exact stem + scheme award. Do NOT invent question numbers/marks/wording. If you can't
verify the stem AND the scheme, pick a different real question that fits the slot. Every Spanish word/accent/form correct.

SPANISH MARKING GRAMMAR:
 - LIFT/TRANSCRIPTION ("Busca/Escribe/Cita la frase"): exact words — "No marks if words added or omitted. Exact transcription required."
 - SYNONYM ("Encuentra/Busca la palabra que significa…/que tenga el mismo sentido"): the ONE matching word FROM the text, not a self-made synonym.
 - ANSWER IN THE LANGUAGE INDICATED: Spanish question → answer in Spanish ("no marks for English"); "Answer in English" heading → answer in English. Wrong language = 0.
 - INFERENCE ("¿Por qué…?", "Explica"): own words; many schemes warn "No marks for answers supported by reference to the extract."
 - PRODUCTION ("Escribe", "Describe", "Rellena"): marked on Communication AND Language (grammar/tense/vocab).

OUTPUT one object (schema's "stem"): id (kebab, 'es-' prefix, cue+topic), subjectId='spanish', subjectLabel='Spanish',
level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord verbatim with the SAME casing/accents),
commandWord (the tappable cue), demand, trap (scheme rule + marks consequence; quote/point to the award), source
('LC Spanish {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int).

TAPPABILITY (a test enforces it): commandWord must be a CONSECUTIVE token-run in stem after stripping non-letters AND
accents and lowercasing (so 'Explica' matches 'explica', 'en español' matches). Verify it yourself.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','learn vocab'). trap = a real scheme rule.
Plain text; Spanish accents/ñ/¿¡ fine. Return data only; never edit a file.
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
  { key: 'ol-synonym', level: 'ordinary',
    topic: 'An ORDINARY-level synonym/same-meaning cue — a real OL Section A question like "Busca/Encuentra en el texto la palabra (o frase) que significa lo mismo (más o menos) que…" or "…que tenga el mismo sentido…". The synonym cue is currently HL-only; OL papers use it too. Demand: copy the ONE matching word FROM the text. Trap: a self-made synonym not in the text, or added/omitted words, scores 0.' },
  { key: 'ol-answer-in-spanish', level: 'ordinary',
    topic: 'An ORDINARY-level cue whose answer MUST be in Spanish — a real OL Section A comprehension question asked in Spanish (e.g. "Contesta en español:" or a Spanish-worded "¿Qué…?/¿Dónde…?" item the scheme answers in Spanish). Demand: answer in Spanish using the text. Trap: answering in English forfeits the marks ("no marks for answers in English"). Pick a real OL question + its scheme Spanish answer.' },
  { key: 'hl-answer-in-english-trap', level: 'higher',
    topic: 'A HIGHER-level question explicitly headed "Answer the following questions in ENGLISH" (the journalistic-text section), where the trap is answering in Spanish. Choose a real HL journalistic-text question (e.g. "What is said about…? Give full details", "Why…?"). commandWord can be "in English" or "Give full details" — whichever is the tappable load-bearing cue. Demand: answer in English with full detail. Trap: a Spanish answer, or skimping detail where the scheme wants several points, loses marks.' },
  { key: 'ol-inference', level: 'ordinary',
    topic: 'An ORDINARY-level reasoning/justify cue answered in Spanish — a real OL "¿Por qué…?" or "Explica…" question (topic travel/sport/daily life). OL currently has only one ¿Por qué. Demand: give the reason in Spanish from the text. Trap: answering in English, or a one-word answer where the scheme wants the reason, loses marks.' },
  { key: 'ol-production', level: 'ordinary',
    topic: 'An ORDINARY-level WRITTEN PRODUCTION cue other than "Describe" — a real OL Section B task like "Escribe una postal/un correo…", "Rellena el formulario…", or "Escribe una nota…". Demand: produce the text covering the bullet points. Trap: missing a required bullet point loses Communication marks; broken verbs/tenses lose Language marks (production is marked on Communication AND Language).' },
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
  type: 'object', required: ['verdict', 'tappable', 'spanishCorrect', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, spanishCorrect: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
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
    `Independent SKEPTIC + native-level Spanish checker verifying ONE Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive token-run in stem (strip punctuation/accents, lowercase)? else fix.\n` +
    `2. SPANISH ACCURACY: every Spanish word/accent/verb form in stem, demand, trap correct?\n` +
    `3. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + scheme rule in demand/trap match the scheme text? else grounded:false.\n` +
    `4. MARKING ACCURACY: demand/trap match the real scheme grammar for this cue (synonym-from-text, answer-in-required-language, inference-own-words, production Communication+Language)?\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme rule?\n` +
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
