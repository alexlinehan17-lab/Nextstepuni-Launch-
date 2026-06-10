export const meta = {
  name: 'jc-maths-cmdword',
  description: 'Author + adversarially verify Junior Cycle Mathematics Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, level purity, maths sense, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_maths_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE MATHEMATICS (Ireland, reformed NCCA spec first examined 2022). The
student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue
demands and the marking trap behind it.

EXAM SHAPE: single terminal paper per level, HIGHER + ORDINARY, 270 marks, ~2h, ~13-15 questions of varying marks,
contextual + cross-strand. Marking uses SCALES with partial credit (Low/High Partial Credit) — a relevant first step earns
LPC even if unfinished.

JC-MATHS CUE GRAMMAR (ground demands/traps in it — these are the real maths command words):
 - 'Show that' / 'Prove' / 'Verify': you are GIVEN the answer/result; you must demonstrate it with visible, correct steps
   that ARRIVE at the given result. Trap: stating the result or checking one number — the marks are for the derivation;
   a bare answer scores little because the answer was handed to you.
 - 'Hence' / 'Hence, or otherwise': you MUST use the previous part's result/method. Trap: restarting from scratch — you
   lose the link and waste time; "or otherwise" allows a fresh method but "Hence" alone signals the intended route.
 - 'Solve' / 'Find' / 'Calculate' / 'Evaluate' / 'Work out': produce the value(s) with working. Trap: no working means no
   partial credit if the final answer is wrong; wrong units / wrong rounding loses the accuracy mark; for 'Solve' a
   quadratic, giving only one root when two exist.
 - 'Factorise' / 'Simplify' / 'Express ... in the form': transform the expression fully. Trap: partial factorising
   (not taking out the full common factor; stopping before difference-of-two-squares); not matching the requested form.
 - 'Construct' / 'Draw' / 'Plot': produce an accurate figure with the correct instruments/scale. Trap (Construct): no
   construction arcs shown (the marks are for the method, not a freehand line); wrong/again-measured instead of compass-
   and-straight-edge; (Plot/Draw a graph): mis-scaled axes or too few points.
 - 'Justify' / 'Explain' / 'Give a reason' / 'Investigate': make a reasoned statement supported by the maths. Trap: an
   opinion with no calculation/where the figures don't back the claim.
 - 'Write down' / 'State' / 'List': a short exact answer, no working needed. Trap: over-working a 1-mark item.

THE TYPE (one object per stem):
  id            kebab, prefix 'jcmth-', unique (e.g. 'jcmth-showthat-volume-hl')
  subjectId     MUST be exactly 'jc-mathematics'
  subjectLabel  'Mathematics (Junior Cycle)'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Q7(b)' or '2023 OL · Q5'
  stem          the question stem, faithful to the paper (summarise a long context briefly; if it needs a figure, describe
                the essential numbers in words so the cue is still meaningful). MUST contain commandWord verbatim.
  commandWord   the cue ('Show that', 'Prove', 'Verify', 'Hence', 'Solve', 'Find', 'Calculate', 'Evaluate', 'Factorise',
                'Simplify', 'Express', 'Construct', 'Draw', 'Plot', 'Justify', 'Explain', 'Investigate', 'Write down', 'State')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (no derivation on Show that, restart on
                Hence, partial factorising, no construction arcs, one root on Solve, units/rounding, etc.).
  source        'SEC JC Maths {YEAR} {LEVEL} marking scheme, Q… (…scale / marking rule…)'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Multi-word cues ('Show that', 'Write down') must appear as that exact consecutive run.

GROUNDING (non-negotiable): every stem is a REAL SEC JC Maths question (2022-2025; exams cancelled 2020-2021). Papers +
schemes at ${TXT}/ — jc-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme guidance.
Do NOT invent question numbers, marks, or scheme wording.

LEVEL PURITY (hard rule): the stem's level MUST match the level of the paper it is on. Scope: JC maths only (no calculus /
sine-cosine rule / unit circle / enlargement / standard deviation).

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'show your working'
as a bare phrase). trap = a real marking pattern. Prefer cue DIVERSITY (especially 'Show that', 'Hence', 'Construct',
'Justify' — the cues students most misread). Plain text; maths notation as x^2, sqrt(), pi.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: { type: 'array', items: { type: 'object',
      required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string', enum: ['higher', 'ordinary'] }, questionRef: { type: 'string' },
        stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
        trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'show-prove-verify', cues: 'Show that, Prove, Verify',
    topics: 'the demonstrate-a-given-result cues — "Show that the surface area = 22y + 60", "Show that |AB| = |BC|", "Verify that ...". Demand: visible correct steps ARRIVING at the given result. Trap: stating it / checking one value scores little because the answer was given; the marks are the derivation.' },
  { key: 'hence-justify-explain', cues: 'Hence, Justify, Explain, Investigate, Give a reason',
    topics: 'the use-the-previous-part + reasoned-statement cues — "Hence solve ...", "Hence, find ...", "Justify your answer", "Explain why ...", "Investigate whether ...". Demand: Hence reuses the prior result; Justify/Explain need the maths to back the claim. Trap: restarting from scratch on Hence; an unsupported opinion on Justify/Explain.' },
  { key: 'solve-find-calculate', cues: 'Solve, Find, Calculate, Evaluate, Work out',
    topics: 'the produce-the-value cues across Number/Algebra/Geometry/Stats — "Solve the equation", "Find the value of x", "Calculate the volume / the mean / the probability", "Evaluate". Demand: the value(s) with working, correct units/rounding. Trap: only one root of a quadratic; no working → no partial credit; wrong units or rounding loses the accuracy mark.' },
  { key: 'factorise-simplify-express', cues: 'Factorise, Simplify, Express, Write down, State',
    topics: 'the manipulate-the-expression + short-answer cues — "Factorise fully", "Simplify", "Express in the form a x 10^n / 5^p", "Write down the next term / the range". Demand: transform fully / match the requested form. Trap: partial factorising (missing the full common factor or difference of two squares); not matching the form; over-working a State/Write-down item.' },
  { key: 'construct-draw-plot', cues: 'Construct, Draw, Plot',
    topics: 'the produce-a-figure cues — "Construct the axis of symmetry / a triangle / an angle of 60", "Draw the graph of the function", "Plot the points / the data". Demand: accurate figure with the right instruments/scale; constructions need compass-and-straight-edge arcs left visible. Trap: no construction arcs (marks are for the method); mis-scaled axes or too few plotted points.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT cue where possible, across years and strands. Ground every stem/demand/trap/marks/citation in the paper + scheme. LEVEL PURITY: an OL stem from an OL paper only. Make demand+trap specific to the exact question and its marking scale.`,
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
    fixedStem: { type: 'object', properties: {
      id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
      level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
      commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
      source: { type: 'string' }, marks: { type: 'integer' } } },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Maths Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase; multi-word cue = exact run)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef} (2022-2025)? marks + the marking rule in demand/trap match the scheme? else grounded:false.\n` +
    `3. LEVEL PURITY + SCOPE: is the source paper actually ${s.level}? Is it within JC scope (no LC-only method)? else fix.\n` +
    `4. QUALITY: demand specific to this cue+question (no filler)? trap a real marking pattern (no-derivation on Show that, restart on Hence, partial factorising, one-root, no-arcs, units/rounding)? Is the cue the RIGHT command word for what the question asks?\n` +
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
  `Completeness critic for a Junior Cycle Maths Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~55/45), (2) cue diversity — the signature maths cues must appear: 'Show that', 'Hence', 'Solve', 'Find'/'Calculate', 'Factorise', 'Construct', 'Justify'/'Explain', plus 'Express'/'Write down'; flag missing cues, (3) coverage across the four strands (Number, Geometry/trig, Algebra/functions, Statistics/probability), (4) whether the signature traps are present: no-derivation on Show that, restart on Hence, partial factorising, no construction arcs, one-root quadratic, units/rounding. List concrete gap slots (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
