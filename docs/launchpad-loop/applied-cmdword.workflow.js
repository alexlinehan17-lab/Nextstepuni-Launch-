export const meta = {
  name: 'applied-cmdword',
  description: 'Author + adversarially verify Applied Mathematics Command-Word Reflex stems from real SEC papers/schemes (new spec 2023+)',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic recomputes + checks tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/applied_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert APPLIED MATHEMATICS (the CURRENT modelling spec, first examined
2023). The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns
what that cue demands and the marking-scheme trap behind it.

EXAM SHAPE: written paper 400 marks, TEN questions, answer ANY EIGHT, 50 marks each; HL + OL; context/modelling-driven.

APPLIED-MATHS CUE GRAMMAR (ground demands/traps in it):
 - 'Calculate' / 'Find' (the dominant cues): the worked value — formula, substitution, value, UNIT; the scheme awards the
   setup and intermediate steps, so a bare answer or a missing unit loses marks.
 - 'Solve': the full solution of the equation/system (e.g. a difference/differential equation) including the constant(s)
   from initial conditions.
 - 'Use …' / 'Hence': you MUST use the stated method/result (e.g. 'Use Dijkstra's algorithm…', 'Use your answer from
   part (a)…') — a correct answer by a different method may earn little.
 - 'Draw' / 'Sketch': a labelled diagram/graph (network, v-t graph, project network) with the key features the scheme
   lists — unlabelled or missing-feature drawings drop marks.
 - 'Write down' / 'State': the immediate answer, no working demanded — but it must be exact.
 - 'Show that': arrive at the GIVEN result with full working — you cannot use the target as an input; the marks are in
   the derivation steps.
 - 'Explain' / 'Comment' / 'Verify': a reasoned statement in context (the modelling spec rewards interpreting maths in
   the real-world context — e.g. explain what a value MEANS for the scenario).

THE TYPE (one object per stem):
  id            kebab, prefix 'am-', unique (e.g. 'am-calculate-critical-path-hl')
  subjectId     MUST be exactly 'applied-mathematics'
  subjectLabel  'Applied Mathematics'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Q3(a)' or '2025 OL · Q7(b)'
  stem          the question stem, faithful to the paper (summarise long context briefly; embed the key data). MUST
                contain commandWord verbatim.
  commandWord   the cue ('Calculate', 'Find', 'Solve', 'Use', 'Draw', 'Write down', 'State', 'Show that', 'Explain', 'Hence')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (missing unit, bare answer with no setup,
                ignoring the mandated method on 'Use', using the target in 'Show that', no context interpretation on
                'Explain'). Point to the scheme award where it bites.
  source        'LC Applied Mathematics {YEAR} {LEVEL} marking scheme, Q… ("…scheme answer/award…")'
  marks         integer marks at stake (from the scheme)
  figureSpec    OPTIONAL — only if the cue depends on a diagram printed in the question (a network to run an algorithm
                on, a v-t graph). Shape { year, level, questionRef, source ('paper'|'scheme'), describes, whyNeeded }.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem.

GROUNDING (non-negotiable): every stem is a REAL SEC question from 2023, 2024 or 2025 ONLY (new spec; 2021-2022 are the
old syllabus — do NOT use). Papers + schemes at ${TXT}/ — applied-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read
for the exact stem + scheme award. RECOMPUTE any value you cite and confirm it matches the scheme.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'show your working' [say WHICH working the scheme awards],
'read the question', 'manage your time'). trap = a real scheme-grounded rule. Prefer cue DIVERSITY: Calculate, Find,
Solve, Use, Draw, Write down, State, Show that, Explain, Hence. Plain text; unicode (×, ², θ, ½) fine.

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
  { key: 'calculate-find', cues: 'Calculate, Find',
    topics: 'the dominant numeric cues across all strands — calculate a speed/tension/coefficient/critical path duration/loan balance, find a shortest path length/projectile range. Demand: formula → substitution → value + UNIT (the scheme awards the steps). Trap: bare answer, missing unit, skipping the awarded setup.' },
  { key: 'use-hence-draw', cues: 'Use, Hence, Draw, Sketch, Complete',
    topics: 'the method-mandating cues — "Use Dijkstra\'s algorithm to find…", "Use Prim\'s/Kruskal\'s algorithm…", "Hence, or otherwise…", "Draw a network diagram…", "Complete the table…". Demand: the NAMED method/diagram with its required features (Dijkstra labels, MST edge order, labelled axes). Trap: right answer by eyeballing/another method earns little when the method is mandated; unlabelled diagrams drop marks. Network cues can carry a figureSpec.' },
  { key: 'solve-show', cues: 'Solve, Show that, Verify',
    topics: 'the derivation cues — "Solve the difference equation…", "Solve the differential equation…", "Show that…" (a given result: e.g. show the time of flight is T, show the equation reduces to a given form). Demand: full solution incl. constants from initial conditions; for Show-that, derive the target without assuming it. Trap: using the given result as an input, dropping the constant of integration, not finishing to the stated form.' },
  { key: 'state-explain', cues: 'Write down, State, Explain, Comment',
    topics: 'the immediate + interpretive cues — "Write down the value of…", "State one assumption…" (the modelling spec LOVES assumption/limitation questions), "Explain what this value means in context…", "Comment on the suitability of the model…". Demand: exact immediate answers; for Explain/Comment, interpret the maths IN THE REAL-WORLD CONTEXT (the modelling spec\'s signature). Trap: restating the number without the contextual meaning; vague assumptions ("it\'s simplified") instead of specific ones ("air resistance is neglected").' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT cue where possible, spread across 2023-2025 and across the four strands. RECOMPUTE any value you cite. Make the demand and trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'mathChecks', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, reason: { type: 'string' },
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
    `Independent SKEPTIC verifying ONE Applied Mathematics Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question from 2023-2025 ONLY near ${s.questionRef}? marks + scheme award match? A 2021/2022 old-spec grounding → reject.\n` +
    `3. MATHS: RECOMPUTE any numeric value in the demand/trap from the question data; must match the scheme.\n` +
    `4. QUALITY: demand specific to cue+question (no filler)? trap a real scheme pattern (unit, mandated method, show-that discipline, context interpretation)?\n` +
    `5. FIGURE: if figureSpec present, does the cue truly need the printed diagram? else drop it.\n` +
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
  `Completeness critic for an Applied Mathematics Command-Word Reflex stem set (Irish LC, new spec). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef, hasFigure: !!k.figureSpec })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — Calculate dominates the real paper but the set should ALSO cover Use (mandated method), Show that, Solve, Draw, State/Write down, and Explain-in-context; flag missing, (3) strand spread (networks, kinematics/dynamics, changing world, modelling/assumptions), (4) whether the signature traps are present: missing UNIT, mandated-method (Use Dijkstra), show-that discipline, and the modelling spec's interpret-in-context. List concrete gap slots (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
