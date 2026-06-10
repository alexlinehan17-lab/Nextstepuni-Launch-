export const meta = {
  name: 'spanish-cmdword',
  description: 'Author + adversarially verify Spanish Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks Spanish + scheme + tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/spanish_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert SPANISH (Irish exam-technique tool). The student sees a real exam
question STEM, taps the COMMAND WORD / CUE (the word telling them what to DO), then learns what that cue demands and the
marking-scheme trap behind it. Spanish exam cues are bilingual: some questions are asked in Spanish (and must be answered
in Spanish), some in English (journalistic-text questions answered in English).

GROUNDING (non-negotiable): every stem is a REAL SEC LC Spanish question. Text of all papers + schemes (2021-2025, HL+OL)
at ${TXT}/ (pages ===PAGE n===): spanish-YYYY-{HL,OL}-{written,aural,marking-scheme}.txt. grep/Read for the exact stem +
scheme award. Do NOT invent question numbers, marks, or scheme wording. Every Spanish word/accent/form must be correct.

SPANISH MARKING GRAMMAR (ground demands/traps in it):
 - LIFT / TRANSCRIPTION cues ("Busca/Escribe/Cita la frase…", "¿Cómo se dice…?"): copy the EXACT phrase from the text —
   "No marks awarded if words are added or omitted. Exact transcription required."
 - SYNONYM / VOCABULARY cues ("Encuentra la palabra que significa…", "Da un sinónimo de…"): find the ONE word/expression
   in the text that matches — a definition or a near-miss synonym not in the text scores nothing.
 - ANSWER IN THE LANGUAGE INDICATED: a Spanish-language question must be answered in Spanish ("No marks for answers in
   English"); a question headed "Answer in English" must be in English. Answering in the wrong language forfeits the marks.
 - INFERENCE / OPINION cues ("¿Por qué…?", "Explica", "Según el texto"): answer in your OWN words — several schemes warn
   "No marks awarded for answers supported by reference to the extract" (you may not just quote).
 - JUSTIFY cues ("¿Verdadero o Falso? Justifica tu respuesta"): the mark is for the QUOTED justifying line, not the V/F tick.
 - PRODUCTION cues ("Escribe", "Describe", "Explica tu opinión"): marked on Communication AND Language (grammar/tense/vocab).

THE TYPE (one object per stem):
  id            kebab, prefix 'es-', unique, includes cue + topic (e.g. 'es-busca-la-frase-comprehension-hl')
  subjectId     MUST be exactly 'spanish'
  subjectLabel  'Spanish'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Section A · Q1(b)' or '2023 OL · Q2'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim (same casing/accents as stem).
                Keep it a stem; you may add "(in the text)" context but do not paste a whole passage.
  commandWord   the cue word/phrase the student taps (e.g. 'Busca', 'Encuentra', 'Justifica', 'Explica', 'Describe',
                'Menciona', '¿Por qué?', 'in English', 'Escribe'). Must be a consecutive token-run in the stem.
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (exact transcription, wrong language,
                quoting on inference, V/F without the justifying quote, broken Language marks on production). Quote/point
                to the scheme where it bites.
  source        'LC Spanish {YEAR} {LEVEL} marking scheme, Q… ("…scheme answer / award note…")'
  marks         integer marks at stake (from the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letter characters and lowercasing (accents are stripped too, so 'Explica' matches). Verify per stem.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'learn vocab').
trap = a real scheme-grounded rule. Prefer cue DIVERSITY across: Busca, Escribe, Encuentra, Cita, ¿Cómo se dice,
Justifica, Explica, Describe, Menciona, Da, ¿Por qué, 'in English', Escribe (production). Plain text; Spanish accents/ñ/¿¡
and unicode fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: {
      type: 'array',
      items: {
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
  },
}

const CLUSTERS = [
  { key: 'lift-transcription', cues: 'Busca, Escribe, Cita, ¿Cómo se dice/expresa',
    topics: 'the lift-the-phrase / exact-transcription questions in Section A reading comprehension — "Busca la frase que muestra/indica…", "Escribe la frase…", "¿Cómo se expresa la idea de…?". The cue demands copying the EXACT words from the text; the trap is adding/omitting words ("Exact transcription required").' },
  { key: 'synonym-vocabulary', cues: 'Encuentra, Da (un sinónimo), Busca la palabra, ¿Qué significa',
    topics: 'the synonym/vocabulary-matching questions — "Encuentra en el texto la palabra que significa…", "Da un sinónimo de…", the word-meaning items. The cue demands the ONE matching word/expression FROM the text; the trap is giving a dictionary definition or a synonym not present in the passage.' },
  { key: 'inference-justify-spanish', cues: 'Justifica, Explica, ¿Por qué, Según el texto, Describe, Menciona',
    topics: 'the higher-order Spanish-language comprehension — Verdadero/Falso + "Justifica tu respuesta", "¿Por qué…?", "Explica…", "Según el texto…", "Describe/Menciona dos…". The cue demands answering IN SPANISH (no marks for English) and, for inference, in your OWN words (no marks for answers supported by quoting the extract); for V/F the mark is the justifying quote.' },
  { key: 'english-answer-and-production', cues: 'in English, Give full details, What, Why, Escribe, Describe (production)',
    topics: 'the journalistic-text questions headed "Answer the following questions in English" ("Give full details", "What is said about…", "Why…", "Mention two…") where answering in Spanish loses marks; PLUS Section B opinion writing and Section C / OL Section B written production cues ("Escribe un correo…", "Describe…", "Explica tu opinión…") marked on Communication AND Language.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT cue where possible, spread across years 2021-2025. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation. Make the demand and trap specific to the exact question you cite.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

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
    `1. TAPPABILITY: is commandWord a consecutive word-token run in stem (strip punctuation/accents, lowercase)? If not → fix the stem or the commandWord so it is.\n` +
    `2. SPANISH ACCURACY: every Spanish word/accent/verb form in the stem, demand and trap correct?\n` +
    `3. GROUNDING: real ${s.level} question near ${s.questionRef} in the named file? marks + the scheme rule in demand/trap match the scheme text? else grounded:false.\n` +
    `4. MARKING ACCURACY: does the demand/trap match the real scheme grammar for this cue (exact transcription on lifts, synonym-from-text, answer-in-required-language, no-quote-on-inference, justify=quote, Communication+Language on production)?\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme pattern?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated, reject.\n\n` +
    `THE STEM:\n${JSON.stringify(s, null, 2)}`,
    { label: `verify:${s.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ stem: s, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.stem)
  else if (r.v.verdict === 'fix' && r.v.fixedStem) kept.push({ ...r.stem, ...r.v.fixedStem })
}
log(`Verify: ${kept.length}/${stems.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a Spanish Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — flag if one cue dominates; the set should cover lift/transcription, synonym, inference/justify (Spanish-answer), AND English-answer/production cues, (3) whether BOTH the exact-transcription trap AND the wrong-language trap are represented (both are the signature Spanish marks-losers), (4) any duplicate cue+topic. List concrete gap slots to top up (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
