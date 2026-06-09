export const meta = {
  name: 'phys-cmdword-topup',
  description: 'Fill Physics Command-Word critic gaps: Heat, non-Doppler wave/light, a higher-order discursive cue, a graph/sketch cue',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes each vs scheme' },
  ],
}

const TXT = '/tmp/phys_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert PHYSICS. The student taps the COMMAND WORD in a real exam
stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use the real SEC text at ${TXT}/ — physics-YYYY-{HL,OL}-{paper,marking-scheme}.txt
(pages ===PAGE n===). grep/Read for the exact stem + scheme award points. Do NOT invent question numbers, marks, or
wording. If you can't verify the stem AND the scheme, pick a different real question that fits the slot. RECOMPUTE any number.

OUTPUT one object (schema's "stem"): id (kebab, 'phys-' prefix, cue+topic), subjectId='physics', subjectLabel='Physics',
level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord verbatim), commandWord,
demand (the answer-shaping move + the exact scheme-rewarded thing), trap (scheme-grounded mistake + marks consequence,
quote the award point), source ('LC Physics {YEAR} {LEVEL} marking scheme, Q… ("…award…")'), marks (int),
figure (ONLY if the cue genuinely needs a visual AND you reuse a committed crop whose source-question matches — else omit).

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
punctuation + lowercasing. Verify it yourself.

COMMITTED physics figures reusable ONLY if your stem genuinely IS that exact question:
  /exam-figures/physics/physics-2022-hl-xyz-circuit.png — 2022 HL Q9(c) X=1Ω series, Y=6Ω∥Z=3Ω, 12 V
  /exam-figures/physics/physics-2024-ol-concave-mirror-ray.png — 2024 OL Q8 concave-mirror 'copy and complete' ray diagram
figure.source = 'SEC Leaving Certificate Physics {YEAR} {LEVEL}, Q… — © State Examinations Commission' + precise alt.

QUALITY: demand specific to cue+question (BANNED filler: "read the question", "show your working", "manage your time",
"plan your answer"). trap = a real scheme-grounded pattern. ASCII physics fine (m s^-2, ×10^8, ohm); unicode (×,°,λ,Ω) fine.
Return data only; never edit a file.
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
        figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
      },
    },
  },
}

const SLOTS = [
  { key: 'heat-calculate', level: 'higher',
    topic: 'HEAT — a "Calculate" question on specific heat capacity or specific latent heat (e.g. energy = mcΔθ or energy = ml, or finding c / l from an experiment). REQUIRED cue word: "Calculate". Embed the data in the stem.' },
  { key: 'discursive-higher-order', level: 'higher',
    topic: 'A HIGHER-ORDER DISCURSIVE cue. Find a real LC Physics question whose stem uses one of: "Account for", "Justify", "Explain why", "Compare", or "Outline". The commandWord must be that exact phrase and must appear verbatim in the stem. Any topic — pick a strong real question (e.g. justify/account-for a physical observation).' },
  { key: 'wave-light-non-doppler', level: 'ordinary',
    topic: 'WAVES/LIGHT but NOT the Doppler effect — diffraction grating, interference, refraction/Snell, total internal reflection, lenses/mirrors, reflection, or wave speed. Any cue that genuinely appears in the stem (Calculate/Explain/Describe/State). Broadens wave/light coverage away from Doppler.' },
  { key: 'graph-or-sketch-cue', level: 'ordinary',
    topic: 'A GRAPH/DIAGRAM cue: find a real question whose stem uses "Draw" or "Sketch" (e.g. draw/sketch a graph, draw a labelled diagram, sketch a velocity-time graph) OR "Use the graph"/"Use the diagram". commandWord = that cue, appearing verbatim. If it is a "Use the graph/diagram" type that needs a visual, attach a figure ONLY if it matches a committed crop; otherwise prefer a "Draw"/"Sketch" stem (no figure needed, the student draws).' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED level: ${s.level}\nTOPIC: ${s.topic}\n\nReturn exactly one grounded stem for this slot.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.stem ? { ...r.stem, _slot: s.key } : null),
))

const stems = authored.filter(Boolean)
log(`Authored ${stems.length} top-up stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
        figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Physics Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? else fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme-rewarded thing + trap's quoted award point match the scheme text? else grounded:false, reject.\n` +
    `3. ACCURACY: any physics error (wrong definition/law/unit/formula/number/marks)?\n` +
    `4. FIGURE (if present): src matches a stem genuinely from that exact question? else drop the figure in a fix.\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme pattern?\n` +
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
