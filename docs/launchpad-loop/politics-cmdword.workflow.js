export const meta = {
  name: 'politics-cmdword',
  description: 'Author + adversarially verify Politics & Society Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks facts, level purity, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/politics_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert POLITICS & SOCIETY (Irish exam-technique tool) — the WRITTEN paper.
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that
cue demands and the marking-scheme trap behind it.

EXAM SHAPE: 400 marks. Section A Short Answer (50; 10 of 15). Section B Data-based (150; read + interpret a data source).
Section C Discursive Essays (200; 2 of 5 @100). SIGNATURE: discursive essays must give a BALANCED argument with EVIDENCE
and cite a relevant KEY THINKER ('participant in the debate'); data answers must USE the actual figures from the source.

P&S CUE GRAMMAR (ground demands/traps in it):
 - 'Explain' / 'Describe' (the dominant cues): give a developed account WITH a concrete example/evidence — a one-line
   definition is capped; the scheme rewards development + an example.
 - 'Discuss' / 'Evaluate' / 'Examine' (the 100-mark essay cues): a BALANCED argument (both sides), evidence/examples, a
   NAMED key thinker and their idea, and a reasoned conclusion — a one-sided assertion or no key thinker caps the band.
 - 'Identify' / 'Name' / 'State' (short-answer cues): the exact term/institution/fact only — precise, no waffle.
 - DATA cues ('Referring to the data…', 'Using the information in the source…'): quote the actual figure/trend FROM the
   source and then apply the concept — a generalisation that ignores the data scores little.
 - 'Outline' / 'Suggest' / 'Account for': a structured set of reasons/points; 'Suggest' wants a reasoned plausible answer.

THE TYPE (one object per stem):
  id            kebab, prefix 'pas-', unique (e.g. 'pas-discuss-globalisation-identity-hl')
  subjectId     MUST be exactly 'politics-and-society'
  subjectLabel  'Politics & Society'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Section C · Q3(a)' or '2023 OL · Section A · Q5'
  stem          the question stem, faithful to the paper (summarise long stimulus briefly). MUST contain commandWord verbatim.
  commandWord   the cue ('Explain', 'Describe', 'Discuss', 'Evaluate', 'Examine', 'Identify', 'Name', 'State', 'Outline')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (no example on Explain, one-sided/no key
                thinker on Discuss, generalising away from the data, waffle on a Name/State). Point to the scheme where it bites.
  source        'LC Politics & Society {YEAR} {LEVEL} marking scheme, Section …, Q… ("…indicative content/award…")'
  marks         integer marks at stake (Section A item ~5; a Section C essay 100)
  figureSpec    OPTIONAL — only if a Section B cue depends on a specific printed data chart. Shape { year, level,
                questionRef, source ('paper'|'scheme'), describes, whyNeeded }.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem.

GROUNDING (non-negotiable): every stem is a REAL SEC question. Papers + schemes (2021-2025, HL+OL) at ${TXT}/ —
politics-and-society-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme award. Do NOT invent
question numbers, marks, thinkers, institutions, dates, or scheme wording. Politics facts MUST be accurate.

LEVEL PURITY (hard rule): the stem's level MUST match the level of the paper it is on — never tag an HL question as OL or
vice versa.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'give your opinion').
trap = a real scheme rule. Prefer cue DIVERSITY: Explain, Describe, Discuss, Evaluate, Examine, Identify, Name, State,
Outline. Plain text; unicode fine.

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
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'explain-describe', cues: 'Explain, Describe',
    topics: 'the dominant short/medium cues across all strands — explain a concept (power, a right, globalisation, sustainability), describe an institution/process (PR-STV, the Oireachtas, the UN, IHREC). Demand: a developed account WITH a concrete example/evidence. Trap: a bare one-line definition with no development/example is capped.' },
  { key: 'discuss-evaluate-essay', cues: 'Discuss, Evaluate, Examine',
    topics: 'the Section C 100-mark discursive-essay cues — "Discuss the impact of globalisation on identity…", "Evaluate the effectiveness of representation…", "Examine human rights in the context of…". Demand: a BALANCED both-sides argument + evidence + a NAMED key thinker and their idea + a conclusion. Trap: a one-sided assertion, no evidence, or NO key thinker caps the essay band (the scheme rewards balance + a relevant thinker).' },
  { key: 'short-answer-precision', cues: 'Identify, Name, State, Outline',
    topics: 'the Section A short-answer cues — "Name the electoral system used…", "State one function of the Seanad…", "Identify…", "Outline one argument…". Demand: the exact term/institution/fact (or a tight set of points for Outline). Trap: waffle/over-writing where one precise term is wanted; too few points for Outline.' },
  { key: 'data-based', cues: 'Referring to the data, Using the, Describe (the trend), Explain (the data)',
    topics: 'the Section B data-based cues — "Referring to the data above…", "Using the information in the source…", describe a trend in the dashboard then apply a concept. Demand: quote the actual FIGURE/trend from the source, then apply the relevant P&S concept. Trap: generalising away from the data (giving a textbook answer that ignores the specific figures) scores little. Add a figureSpec where the cue needs the printed chart.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT cue where possible, spread across years and sections. Ground every stem, demand, trap, marks and citation. LEVEL PURITY: an OL stem from an OL paper only. Make the demand and trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'factsAccurate', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, factsAccurate: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Politics & Society Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + the scheme rule in demand/trap match? else grounded:false.\n` +
    `3. FACT ACCURACY: any wrong politics fact (institution, electoral system, thinker, date, the UDHR/SDGs)? else factsAccurate:false.\n` +
    `4. LEVEL PURITY: is the source paper actually ${s.level}? else fix the level.\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme pattern (no example on Explain, one-sided/no-thinker on Discuss, generalising off the data)?\n` +
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
  `Completeness critic for a Politics & Society Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — Explain/Describe dominate but the set should ALSO cover Discuss/Evaluate (the essay cue), Identify/Name/State (short-answer), and a data-based cue; flag missing, (3) section spread (A short, B data, C essay), (4) whether the signature traps are present: the discursive-essay BALANCE + KEY THINKER requirement, and the data 'use the actual figures' rule. List concrete gap slots (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
