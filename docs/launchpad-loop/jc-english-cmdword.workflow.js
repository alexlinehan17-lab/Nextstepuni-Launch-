export const meta = {
  name: 'jc-english-cmdword',
  description: 'Author + adversarially verify Junior Cycle English Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, level purity, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_english_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE ENGLISH (Irish exam-technique tool) — the final written exam. The
student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue
demands and the marking trap behind it.

EXAM SHAPE: single 2-hour paper, 180 marks, Sections A/B/C, HL + OL. Tests unseen reading comprehension, studied texts
(novel/short story, drama incl. a full Shakespeare play at HL, poetry, film) and writing (functional + personal/creative).
Marking: WRITING on P-C-L-M (Purpose/Coherence/Language/Mechanics); READING on engagement + understanding + CRITICAL
APPRECIATION OF LANGUAGE (analyse HOW + support with quotation).

JC-ENGLISH CUE GRAMMAR (ground demands/traps in it):
 - 'Write' / 'Compose' / 'Imagine' (the dominant cues): a full piece in the named GENRE with the right register — judged on
   P-C-L-M. Trap: wrong genre/register, no structure, or careless mechanics caps the piece; ignoring the audience/purpose.
 - 'Explain' / 'Describe' / 'Discuss': a developed point SUPPORTED by reference/quotation + (for reading) analysis of the
   writer's craft. Trap: a bare statement or plot-retelling with no quotation/analysis.
 - 'Name' / 'Identify' / 'Give' (short answers): the exact answer only — precise, no waffle.
 - 'Choose' / 'Select … and …': pick an option AND do the follow-on task (justify / explain your choice) — the marks are in
   the justification, not the choice.
 - STUDIED-TEXT cues ('… a [character/play/poem/film] you have studied …'): refer to YOUR own studied text with a PRECISE
   reference. Trap: vague general comment with no specific reference to the chosen text.

THE TYPE (one object per stem):
  id            kebab, prefix 'jceng-', unique (e.g. 'jceng-write-speech-hl')
  subjectId     MUST be exactly 'jc-english'
  subjectLabel  'English (Junior Cycle)'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Section A · Q2' or '2023 OL · Q5'
  stem          the question stem, faithful to the paper (summarise long stimulus briefly). MUST contain commandWord verbatim.
  commandWord   the cue ('Write', 'Compose', 'Imagine', 'Explain', 'Describe', 'Discuss', 'Name', 'Identify', 'Give', 'Choose', 'Outline', 'Rewrite')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (wrong genre/register on Write, no
                quotation/analysis on Explain, vague no-reference studied-text answer, no justification on Choose).
  source        'SEC JC English {YEAR} {LEVEL} marking scheme, Section …, Q… ("…marking guidance…")'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem.

GROUNDING (non-negotiable): every stem is a REAL SEC JC English question (2022-2025; exams cancelled 2020-2021). Papers +
schemes at ${TXT}/ — jc-english-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme guidance.
Do NOT invent question numbers, marks, or scheme wording.

LEVEL PURITY (hard rule): the stem's level MUST match the level of the paper it is on — never tag an HL question as OL or
vice versa.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'be creative'). trap =
a real marking pattern. Prefer cue DIVERSITY: Write, Compose, Imagine, Explain, Describe, Discuss, Name, Identify, Give,
Choose, Outline, Rewrite. Plain text; unicode fine.

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
  { key: 'write-compose-imagine', cues: 'Write, Compose, Imagine, Rewrite',
    topics: 'the dominant writing cues — "Write a speech/letter/report/review/blog/diary…", "Imagine you are [character]… write…", "Rewrite the passage adding punctuation/direct speech". Demand: the named GENRE with correct register, structured, judged on P-C-L-M. Trap: wrong genre conventions/register, no structure, careless mechanics.' },
  { key: 'explain-describe-discuss', cues: 'Explain, Describe, Discuss',
    topics: 'the developed-response cues across reading + studied texts — "Explain how the writer creates atmosphere…", "Describe the relationship between…", "Discuss…". Demand: a developed point SUPPORTED by reference/quotation + analysis of craft. Trap: a bare statement or plot-retelling with no quotation/analysis.' },
  { key: 'name-identify-give-choose', cues: 'Name, Identify, Give, Choose, Outline',
    topics: 'the short-answer + selection cues — "Name a character/film/poem you have studied", "Identify…", "Give two reasons…", "Choose … and explain your choice". Demand: the exact answer; for Choose, pick AND justify; for studied-text Name, name a REAL studied text + then the follow-on. Trap: waffle on Name/Identify; no justification on Choose; vague studied-text reference.' },
  { key: 'studied-text-response', cues: 'Write, Explain, Discuss (studied-text framed)',
    topics: 'the studied-text cues that say "… a [novel/play/character/poem/film] you have studied …" (e.g. "Write about a relationship in a studied play", "a Shakespearean play you have studied"). Demand: refer to YOUR OWN studied text with a PRECISE reference (a named moment/character/quotation) and answer the actual question. Trap: a vague general comment with no specific reference to the chosen text scores low.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT cue where possible, across years and sections. Ground every stem/demand/trap/marks/citation. LEVEL PURITY: an OL stem from an OL paper only. Make demand+trap specific to the exact question.`,
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
    `Independent SKEPTIC verifying ONE Junior Cycle English Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef} (2022-2025)? marks + the marking rule in demand/trap match? else grounded:false.\n` +
    `3. LEVEL PURITY: is the source paper actually ${s.level}? else fix the level.\n` +
    `4. QUALITY: demand specific (no filler)? trap a real marking pattern (P-C-L-M genre/register on Write, no-quotation on Explain, no-justification on Choose, vague studied-text reference)?\n` +
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
  `Completeness critic for a Junior Cycle English Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — Write dominates the real paper, but the set should ALSO cover Explain/Describe/Discuss, Name/Identify/Give/Choose, and the studied-text framing; flag missing, (3) coverage of reading vs studied-text vs writing, (4) whether the signature traps are present: P-C-L-M genre/register on Write, quotation+analysis on Explain, justification on Choose, and the precise-studied-text-reference rule. List concrete gap slots (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
