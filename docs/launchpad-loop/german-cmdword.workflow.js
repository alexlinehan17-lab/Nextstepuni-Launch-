export const meta = {
  name: 'german-cmdword',
  description: 'Author + adversarially verify German Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks German + scheme + tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/german_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert GERMAN (Irish exam-technique tool), the WRITTEN paper. The student
sees a real exam question STEM, taps the COMMAND WORD / CUE (the word telling them what to DO), then learns what that cue
demands and the marking-scheme trap behind it. German cues are bilingual + include question-words and Applied-Grammar
instructions.

GROUNDING (non-negotiable): every stem is a REAL SEC LC German question. Text of papers + schemes (2021-2025, HL+OL) at
${TXT}/ — german-YYYY-{HL,OL}-{written,aural,marking-scheme}.txt (pages ===PAGE n===). grep/Read for the exact stem +
scheme answer. Do NOT invent question numbers, marks, or scheme wording. Every German word/case/ending/Umlaut correct.

GERMAN CUE GRAMMAR (ground demands/traps in it):
 - QUESTION-WORD cues in a German question (Warum=why, Wie=how, Was=what, Welche=which, Wo=where, Wer=who) under
   "Beantworten Sie auf Deutsch": find the info the question word asks for and answer IN GERMAN — "No marks for English"
   where German is required; often "Schreiben Sie X Sätze" fixes the number of sentences/details.
 - LANGUAGE-INSTRUCTION cues: "Beantworten Sie … auf Deutsch" (answer in German) vs "Answer … in English" — answering in
   the WRONG language forfeits the marks. This is the signature German marks-loser.
 - APPLIED-GRAMMAR cues ("Schreiben Sie … im Präsens / im Perfekt", "im richtigen Fall/mit der richtigen Endung"):
   manipulate the underlined verb/adjective/noun into the EXACT instructed form (tense/case/ending) — a wrong form scores 0.
 - PRODUCTION cues ("Schreiben Sie", "Beschreiben Sie", "Erklären Sie"): produce text covering the points; marked on
   Communication AND Language (grammar/case/verb/word-order accuracy).

THE TYPE (one object per stem):
  id            kebab, prefix 'de-', unique (e.g. 'de-warum-comprehension-german-hl')
  subjectId     MUST be exactly 'german'
  subjectLabel  'German'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Text I · Q1(a)' or '2023 OL · Q2'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim (same casing/Umlauts as stem).
  commandWord   the cue ('Warum', 'Wie', 'Was', 'Welche', 'Beantworten Sie', 'auf Deutsch', 'in English', 'Schreiben Sie',
                'im Präsens', 'im Perfekt', 'Beschreiben Sie'). Must be a consecutive token-run in the stem.
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (wrong language, wrong grammatical form,
                too few sentences, missing the asked info). Point to the scheme where it bites.
  source        'LC German {YEAR} {LEVEL} marking scheme, Q… ("…scheme answer / award…")'
  marks         integer marks at stake (from the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letter characters and lowercasing (Umlauts are stripped to their base by the test's letter filter — verify the cue is
a clean token-run). Verify per stem.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question','manage your time','learn vocab'). trap =
a real scheme-grounded rule. Prefer cue DIVERSITY across: Warum, Wie, Was, Welche, Wo, Beantworten Sie, auf Deutsch,
in English, Schreiben Sie, im Präsens, im Perfekt, Beschreiben Sie. Plain text; German Umlauts/ß and unicode fine.

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
  { key: 'question-words-german', cues: 'Warum, Wie, Was, Welche, Wo, Wer',
    topics: 'the German-language comprehension questions under "Beantworten Sie auf Deutsch" — "Warum…?", "Wie…?", "Was…?", "Welche…?". Demand: extract the info the question word asks for and answer IN GERMAN (often "Schreiben Sie X Sätze"). Trap: answering in English (no marks), or giving fewer than the required number of sentences/details.' },
  { key: 'language-instruction', cues: 'auf Deutsch, Beantworten Sie, in English, Answer',
    topics: 'the language-instruction cues — "Beantworten Sie … auf Deutsch" (the German-answer sections) vs the Text II / later questions headed "Answer Questions … in English". Demand: answer in the instructed language. Trap: the signature German marks-loser — answering a German question in English (or vice versa) loses the marks.' },
  { key: 'applied-grammar', cues: 'Schreiben Sie, im Präsens, im Perfekt, im Imperfekt',
    topics: 'the Angewandte Grammatik (Applied Grammar) section — "Schreiben Sie die folgenden unterstrichenen Verben im Präsens/Perfekt/Imperfekt", or change adjectives/nouns to the right ending/case. Demand: produce the EXACT instructed grammatical form (correct tense/ending/case). Trap: a wrong verb form, wrong adjective ending or wrong case scores 0 even if the word is right.' },
  { key: 'production-describe', cues: 'Schreiben Sie, Beschreiben Sie, Erklären Sie',
    topics: 'the productive cues — "Schreiben Sie zwei/drei Sätze…", "Beschreiben Sie…", the Äußerung zum Thema and Schriftliche Produktion ("Schreiben Sie eine E-Mail/einen Brief…"). Demand: produce the text covering the required points/number of sentences. Trap: missing a point/too few sentences loses Communication marks; broken cases/verbs/word-order lose Language marks (production is marked on Communication AND Language).' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT cue where possible, spread across years. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation. Make the demand and trap specific to the exact question you cite.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

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
    `Independent SKEPTIC + native-level German checker verifying ONE Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: is commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix the stem or commandWord.\n` +
    `2. GERMAN ACCURACY: every German word/case/ending/verb form/Umlaut in stem, demand and trap correct?\n` +
    `3. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + the scheme rule in demand/trap match? else grounded:false.\n` +
    `4. MARKING ACCURACY: matches scheme grammar for this cue (answer-in-language-indicated, exact-form on Applied Grammar, count-of-sentences, Communication+Language on production)?\n` +
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
  `Completeness critic for a German Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — should cover the question-words (Warum/Wie/Was/Welche), the language-instruction cues (auf Deutsch / in English), the Applied-Grammar cues (im Präsens/Perfekt), and production (Schreiben/Beschreiben); flag any missing, (3) whether BOTH the wrong-language trap AND the Applied-Grammar exact-form trap are represented (the two signature German marks-losers), (4) duplicate cue+topic. List concrete gap slots to top up (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
