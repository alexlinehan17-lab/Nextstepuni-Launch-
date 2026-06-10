export const meta = {
  name: 'jc-irish-cmdword',
  description: 'Author + adversarially verify Junior Cycle Irish (Gaeilge T2) Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, level purity, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_irish_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE IRISH (Gaeilge T2 — English-medium schools) — the final written
exam. The student sees a real exam question STEM (in Irish, faithful to the paper), taps the COMMAND WORD (the Irish cue
telling them what to DO), then learns what that cue demands and the marking trap behind it.

EXAM SHAPE (verified against the actual 2022-2025 papers):
HIGHER (270 marc, 2h): Roinn A Cluastuiscint 45 marc (Ceist 1-3). Roinn B 225 marc: Ceist 4 Léamhthuiscint (65),
Ceist 5 Litríocht úrscéal/dráma (40), Ceist 6 Ceapadóireacht (50), Ceist 7 Cruinneas cloze (10), Ceist 8 Litríocht
gearrscéal/gearrscannán (25), Ceist 9 Cruinneas pick-correct-form (10), Ceist 10 Litríocht dán/amhrán (25).
ORDINARY (270 marc): Roinn A Cluastuiscint 60 (Ceist 1-3). Roinn B 210: Ceist 4 fíor/bréagach (20), Ceist 5
teachtaireacht (20), Ceist 6 fógra/póstaer reading (30), Ceist 7 composite reading+writing (80), Ceist 8 meaitseáil (25),
Ceist 9 sraith pictiúr (35). OL has NO discrete Litríocht or Cruinneas questions.

JC-IRISH CUE GRAMMAR (the Irish command words; ground demands/traps in the schemes):
 - 'Ainmnigh' (name): the exact title/author/character — written precisely ('go cruinn'); the naming line carries real
   marks in HL Litríocht. Trap: vague or missing title/author loses the naming marks and can undermine the whole answer.
 - 'Scríobh' (write): a full piece in the named genre/format covering EVERY required point/bullet/picture. Trap: skipping
   a required bullet or pictiúr caps the ábhar/content mark; wrong format loses genre marks.
 - 'Líon' / 'Líon na bearnaí' (fill the blanks): the grammatically correct form in context. Trap: right word, wrong form
   (missing séimhiú/urú or wrong tense) = no mark.
 - 'Cuir ciorcal' / 'Roghnaigh' (circle/choose): pick the correct option (grammar) or option-with-justification. Trap:
   guessing without applying the rule (séimhiú after mo/sa, urú after i/ar an, the tense the time-word demands).
 - 'Luaigh' (mention/state): a brief, specific point — no development needed. Trap: writing an essay where one phrase
   scores, wasting time; or being too vague to earn the point.
 - 'Mínigh' (explain): the point PLUS a reason/evidence from the text. Trap: restating without explaining 'cén fáth'.
 - 'Déan cur síos' (describe): developed description with specific details/moments. Trap: one bare sentence.
 - 'Inis' (tell): recount the relevant events/details (e.g. an scéal in a sraith pictiúr or a studied text). Trap:
   missing the required tense (past) or key beats.
 - 'Freagair' (answer): answer the set parts — read what each sub-part actually asks.
 - 'Meaitseáil' (match): match items exactly; the trap is near-miss distractors sharing a key word.

THE TYPE (one object per stem):
  id            kebab, prefix 'jcir-', unique (e.g. 'jcir-ainmnigh-urscal-hl')
  subjectId     MUST be exactly 'jc-irish'
  subjectLabel  'Irish (Junior Cycle)'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Roinn B · Ceist 5' or '2023 OL · Roinn B · Ceist 9'
  stem          the question stem in IRISH, faithful to the paper (summarise long stimulus briefly; keep the fadas).
                MUST contain commandWord verbatim.
  commandWord   the Irish cue ('Ainmnigh', 'Scríobh', 'Líon', 'Cuir ciorcal', 'Roghnaigh', 'Luaigh', 'Mínigh',
                'Déan cur síos', 'Inis', 'Freagair', 'Meaitseáil')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question. BILINGUAL register:
                English-led explanation quoting the Irish terms (the audience is 14-15, English-medium school).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence. Bilingual register.
  source        'SEC JC Irish (Gaeilge T2) {YEAR} {LEVEL} marking scheme, Ceist … ("…marking guidance…")'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing (fadas are letters and are preserved — 'Mínigh' must appear as 'Mínigh', and multi-word cues
like 'Déan cur síos' or 'Cuir ciorcal' must appear as that exact consecutive run). Verify per stem.

GROUNDING (non-negotiable): every stem is a REAL SEC JC Irish question (2022-2025; exams cancelled 2020-2021). Papers +
schemes at ${TXT}/ — jc-irish-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme guidance.
Do NOT invent question numbers, marks, or scheme wording.

LEVEL PURITY (hard rule): the stem's level MUST match the level of the paper it is on — never tag an HL question as OL or
vice versa. Litríocht cues (Ainmnigh a studied text, etc.) exist at HL ONLY.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'learn vocab').
trap = a real marking pattern from the scheme. Prefer cue DIVERSITY. Plain text; unicode fine (fadas required).

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
  { key: 'litriocht-cues', cues: 'Ainmnigh, Déan cur síos, Mínigh, Inis, Luaigh — HIGHER ONLY',
    topics: 'the HL Litríocht cues (Ceisteanna 5/8/10): "Ainmnigh úrscéal nó dráma… a ndearna tú staidéar air", "Roghnaigh dán/amhrán… Ní mór teideal… agus ainm an té a chum a scríobh síos go cruinn", then the follow-on cues (Déan cur síos ar…, Mínigh…, Inis…). Demand: precise naming + a developed point referencing YOUR studied text. ALL stems level higher.' },
  { key: 'scriobh-writing', cues: 'Scríobh (HL Ceapadóireacht + OL writing tasks)',
    topics: 'the writing cues: HL Ceist 6 ("Scríobh blag…"), OL Ceist 5 ("Scríobh teachtaireacht chuig cara…"), OL Ceist 7 writing part ("Scríobh fógra/póstaer…"), OL Ceist 9 ("…inis scéal na sraithe pictiúr" / "Scríobh an scéal…"). Demand: the named format covering EVERY required point/pictiúr; tense discipline. Mix HL and OL.' },
  { key: 'cruinneas-cues', cues: 'Líon, Cuir ciorcal, Roghnaigh — HIGHER for discrete grammar Qs',
    topics: 'the HL Cruinneas cues: Ceist 7 ("Líon na bearnaí…" cloze, 10 marc) and Ceist 9 ("Cuir ciorcal ar an bhfocal ceart…", 10 marc — séimhiú/urú/aimsir/tuiseal). Demand: apply the RULE, not the guess. These discrete questions are HL only — do not invent OL versions.' },
  { key: 'comprehension-cues', cues: 'Luaigh, Mínigh, Freagair, Meaitseáil, Cuir (tic), question-word stems',
    topics: 'the comprehension cues across Léamhthuiscint + Cluastuiscint at BOTH levels: HL Ceist 4 sub-parts ("Luaigh dhá…", "Mínigh…", own-words requirements), OL Ceist 4 fíor/bréagach, OL Ceist 8 ("Meaitseáil…" sentences to pictures), Cluastuiscint instructions ("Freagair na ceisteanna…"). Demand per cue: brief point for Luaigh, point+reason for Mínigh, exact matching for Meaitseáil. Mix HL and OL.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary (EXCEPT litriocht-cues and cruinneas-cues: 5 Higher, 0 Ordinary — those discrete questions do not exist at OL), each with a DIFFERENT cue where possible, across years. Ground every stem/demand/trap/marks/citation. LEVEL PURITY: an OL stem from an OL paper only.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
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
    `Independent SKEPTIC verifying ONE Junior Cycle Irish (Gaeilge T2) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase, fadas preserved)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef} (2022-2025)? marks + the marking rule in demand/trap match the scheme? Irish in the stem faithful to the paper (fadas correct)? else grounded:false.\n` +
    `3. LEVEL PURITY: is the source paper actually ${s.level}? Discrete Litríocht + Cruinneas questions are HL ONLY — an OL stem citing one is FABRICATED.\n` +
    `4. QUALITY: demand specific to this cue+question (no filler)? trap a real marking pattern? Bilingual register in demand/trap (English-led, Irish terms quoted)?\n` +
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
  `Completeness critic for a Junior Cycle Irish (Gaeilge T2) Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (noting Litríocht + Cruinneas cues are HL-only by design — OL should still be well represented via Scríobh/Meaitseáil/comprehension cues), (2) cue diversity — Ainmnigh, Scríobh, Líon, Cuir ciorcal, Luaigh, Mínigh, Déan cur síos, Inis, Meaitseáil; flag missing cues, (3) coverage across Cluastuiscint, Léamhthuiscint, Litríocht, Ceapadóireacht, Cruinneas, (4) whether the signature traps are present: the go-cruinn naming rule, the cover-every-bullet rule for Scríobh, the right-word-wrong-form cloze trap, the past-tense sraith-pictiúr rule. List concrete gap slots (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
