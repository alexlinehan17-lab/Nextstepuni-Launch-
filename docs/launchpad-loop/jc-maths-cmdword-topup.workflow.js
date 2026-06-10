export const meta = {
  name: 'jc-maths-cmdword-topup',
  description: 'Targeted top-up of critic-identified gaps (Statistics/Probability strand + Express cue + OL balance) in the JC Maths Command-Word set, then skeptic-verify',
  phases: [
    { title: 'Author', detail: 'one agent per gap slot' },
    { title: 'Verify', detail: 'skeptic per stem' },
  ],
}

const TXT = '/tmp/jc_maths_txt'

const SHARED = `
You author ONE Command-Word Reflex stem for JUNIOR CYCLE MATHEMATICS (reformed NCCA spec, first examined 2022). The student
taps the COMMAND WORD, then learns what it demands + the marking trap. Single terminal paper per level, HL+OL, 270 marks;
marking uses SCALES with Low/High Partial Credit.

CUE GRAMMAR: 'Show that'/'Verify' = derive the GIVEN result with visible steps (bare answer scores little). 'Hence' = reuse
the previous part (restarting loses the link). 'Solve'/'Find'/'Calculate' = the value(s) with working + correct units/
rounding (one root of a quadratic when two exist = lost mark). 'Factorise'/'Simplify' = transform FULLY. 'Express ... in
the form' = match the requested form. 'Justify'/'Give a reason'/'Explain' = a claim backed by the maths/figures (bare
assertion scores little). 'Construct'/'Draw'/'Plot' = accurate figure, constructions need visible arcs.

SCOPE (hard): JC maths only. Valid 'Express' forms at JC are: scientific notation 'a x 10^n', indices 'as 5^p', a ratio
'in the form 1:n', or a single fraction/percentage — NOT 'complete the square' / a(x+b)^2+c (that is LEAVING CERT, do not
use it). No calculus, sine/cosine rule, unit circle, enlargement, standard deviation.

THE TYPE: { id (kebab, prefix 'jcmth-'), subjectId:'jc-mathematics', subjectLabel:'Mathematics (Junior Cycle)',
level('higher'|'ordinary'), questionRef ('2024 OL · Q4(b)'), stem (faithful to the paper; MUST contain commandWord
verbatim; describe any figure's essential numbers in words), commandWord, demand (what THIS cue requires here), trap (the
scheme-flagged mistake + marks consequence), source ('SEC JC Maths {YEAR} {LEVEL} marking scheme, Q… (…scale/rule…)'),
marks (integer) }.

TAPPABILITY: commandWord is a consecutive word-token run in stem (multi-word cue = exact run).
GROUNDING (non-negotiable): a REAL SEC question from ${TXT}/jc-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt (2022-2025).
grep/Read the paper + scheme. Do NOT invent question numbers, marks, or scheme wording. LEVEL PURITY: stem level = paper
level. If your slot CANNOT be grounded, return found:false with a note. Return data only; edit no files.
`

const STEM_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
  level: { type: 'string', enum: ['higher', 'ordinary'] }, questionRef: { type: 'string' },
  stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
  trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
}
const ONE_SCHEMA = { type: 'object', required: ['found'], properties: { found: { type: 'boolean' }, note: { type: 'string' }, stem: { type: 'object', properties: STEM_PROPS } } }

const SLOTS = [
  { key: 'ol-justify-statistics', want: `ORDINARY · a Statistics cue ('Give a reason' / 'Justify' / 'Explain') interpreting a measure of centre/spread from a data set (e.g. why the mean differs from the median, effect of an outlier, which average best represents the data). Trap: a bare assertion with no reference to the data/figures.` },
  { key: 'hl-justify-probability', want: `HIGHER · a Probability cue ('Justify' / 'Explain' / 'Give a reason') on fairness / expected frequency / relative-frequency-vs-theoretical. Trap: restating the answer instead of reasoning from the probabilities.` },
  { key: 'ol-calculate-statistics', want: `ORDINARY · 'Calculate' (or 'Find') the mean / median / mode from a frequency table or data set. Trap: dividing by the wrong total (number of categories vs total frequency), or units/rounding.` },
  { key: 'hl-express-algebra-or-number', want: `HIGHER · 'Express' in a JC-VALID form — e.g. 'Express in the form a x 10^n' (scientific notation) or 'Express ... as 5^p' (indices/surds) or a single algebraic fraction. ABSOLUTELY NOT complete-the-square. Trap: partial manipulation / a sign or index error / not matching the requested form.` },
  { key: 'ol-express-number', want: `ORDINARY · 'Express' a ratio 'in the form 1:n' OR a quantity as a percentage/fraction. Trap: ratio in the wrong order, or rounding error.` },
  { key: 'ol-hence', want: `ORDINARY · 'Hence' — a later part that must reuse the previous part's result (Algebra or Geometry). Trap: restarting from scratch instead of carrying the prior value.` },
  { key: 'ol-solve', want: `ORDINARY · 'Solve' a linear equation or a simple quadratic. Trap: giving only one root when two exist / losing a solution.` },
  { key: 'ol-simplify', want: `ORDINARY · 'Simplify' an expression (collect like terms / simplify a fraction or index expression). Trap: partial simplification (stopping early).` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE stem for this slot (or found:false with evidence).`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))
const stems = authored.filter(Boolean).filter((r) => r.found && r.stem).map((r) => r.stem)
log(`Authored ${stems.length}/${SLOTS.length} gap stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: STEM_PROPS },
  },
}
const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC Maths Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem?\n` +
    `2. GROUNDING: real ${s.level} question at ${s.questionRef} (2022-2025)? marks + marking rule match the scheme?\n` +
    `3. LEVEL PURITY + SCOPE: source paper actually ${s.level}? Within JC scope (NO complete-the-square / calculus / sine-cosine rule / std deviation)?\n` +
    `4. QUALITY: demand/trap specific, correct cue, real marking pattern?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedStem (keep id). If sound, accept. If fabricated/out-of-scope, reject.\n\nTHE STEM:\n${JSON.stringify(s, null, 2)}`,
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
return { kept, keptCount: kept.length, unfounded: authored.filter(Boolean).filter((r) => !r.found).map((r) => r.note || 'no note') }
