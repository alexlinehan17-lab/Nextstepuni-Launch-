export const meta = {
  name: 'applied-cmdword-topup',
  description: 'Fill Applied Maths Command-Word gaps: HL Draw-forces, OL explicit-unit Write down, OL Justify, modelling/dimensional stem, OL standalone Solve',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic recomputes + checks tappability' },
  ],
}

const TXT = '/tmp/applied_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert APPLIED MATHEMATICS (current modelling spec, first examined 2023).
The student taps the COMMAND WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): real SEC questions from 2023, 2024 or 2025 ONLY at ${TXT}/ —
applied-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===). grep/Read for the exact stem + scheme award.
RECOMPUTE any value and confirm vs the scheme. Do NOT invent question numbers/marks/wording.

OUTPUT one object (schema's "stem"): id (kebab, 'am-' prefix, cue+topic), subjectId='applied-mathematics',
subjectLabel='Applied Mathematics', level, questionRef, stem (faithful; MUST contain commandWord verbatim; embed key data),
commandWord, demand (the answer-shaping move per the scheme's awards), trap (the scheme rule + marks consequence),
source ('LC Applied Mathematics {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int), figureSpec ONLY if the cue depends
on a printed diagram { year, level, questionRef, source ('paper'|'scheme'), describes, whyNeeded }.

TAPPABILITY (a test enforces it): commandWord must be a CONSECUTIVE token-run in stem after stripping non-letters and
lowercasing. Verify it yourself.

QUALITY: demand specific to cue+question (BANNED filler: 'show your working' [name WHICH working the scheme awards],
'read the question'). trap = a real scheme-grounded rule. Return data only; never edit a file.
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
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const SLOTS = [
  { key: 'hl-draw-forces', level: 'higher',
    topic: 'The HL "Draw a diagram to show the forces acting on…" cue — the most repeated non-Calculate HL command (e.g. 2024 HL Q2(a)(i) jeep, 2023 HL Q3(i) chair-swing seat, 2024 HL Q9 mass on a plane). Pick ONE real instance. Demand: a labelled free-body diagram with EVERY force named (weight, normal reaction, tension/friction…), correct directions. Trap: a missing/extra force or unlabelled arrows loses the diagram marks that anchor the rest of the part. Likely needs a figureSpec only if the question prints a setup diagram the forces refer to — else self-contained.' },
  { key: 'ol-write-down-unit', level: 'ordinary',
    topic: 'The OL explicit-UNIT cue — 2024 OL Q9(iii)/(iv) "Write down the minimum time, in hours, …" (project scheduling) or equivalent. Demand: the immediate value IN THE UNIT ASKED. Trap: the signature missing-unit/wrong-unit penalty — the scheme\'s answer line carries the unit, and an unconverted or unitless answer drops the award.' },
  { key: 'ol-justify', level: 'ordinary',
    topic: 'The "…? Justify your answer." decision cue at OL (e.g. 2023 OL or 2024 OL — find a real instance: a yes/no or which-option question + justification). Demand: the DECISION plus the numeric/mathematical reason (the marks sit on the justification). Trap: an answer with no supporting computation/reason earns little; a justification that does not reference the computed value is vague.' },
  { key: 'modelling-assumption', level: 'higher',
    topic: 'A modelling-spec signature cue: "State one assumption…" / "State one limitation of the model…" / "Suggest one refinement…" at HL (2023-2025 — find a real instance; these recur across contexts). Demand: a SPECIFIC assumption/limitation tied to this model (e.g. "air resistance is neglected", "the rate stays constant between observations"). Trap: vague answers ("it\'s only a model", "it\'s simplified") score zero — the scheme lists concrete acceptable answers.' },
  { key: 'ol-solve-standalone', level: 'ordinary',
    topic: 'The OL standalone "Solve" cue — 2025 OL Q10(a)(ii) "Solve the characteristic equation" (difference equation chain) or another real OL Solve. Demand: the full solution of the named equation (roots/general solution), feeding the next part. Trap: stopping at one root / not writing the general solution; sign slips in the quadratic that corrupt the chained parts.' },
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
    `Independent SKEPTIC verifying ONE Applied Mathematics Command-Word stem against ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive token-run in stem? else fix.\n` +
    `2. GROUNDING: real ${s.level} question from 2023-2025 ONLY near ${s.questionRef}? marks + scheme award match? old-spec grounding → reject.\n` +
    `3. MATHS: RECOMPUTE any numeric value; must match the scheme.\n` +
    `4. QUALITY: demand specific? trap a real scheme rule (forces all named, the unit, the justification, the concrete assumption)?\n` +
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
