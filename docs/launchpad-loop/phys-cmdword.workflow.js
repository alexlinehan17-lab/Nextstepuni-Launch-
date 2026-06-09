export const meta = {
  name: 'phys-cmdword',
  description: 'Author + adversarially verify Physics Command-Word Reflex stems from real SEC schemes',
  phases: [
    { title: 'Author', detail: 'cue/topic clusters → grounded stems' },
    { title: 'Verify', detail: 'independent skeptic refutes each vs scheme' },
    { title: 'Critic', detail: 'completeness + balance critic' },
  ],
}

const TXT = '/tmp/phys_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert PHYSICS (Irish exam-technique tool). The student sees a real
exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue demands and
the examiner/marking-scheme-flagged trap behind it.

GROUNDING (non-negotiable): every stem is a REAL SEC LC Physics question. Text of all papers + schemes (2021-2025,
HL+OL) is at ${TXT}/ as plain text (pages ===PAGE n===): physics-YYYY-{HL,OL}-{paper,marking-scheme}.txt
grep/Read to find the exact stem + its scheme award points. Do NOT invent question numbers, marks, or scheme
wording. If you can't verify the stem AND the scheme, drop it. RECOMPUTE any number you cite.

THE TYPE (one object per stem):
  id            kebab, prefix 'phys-', unique, includes cue + topic (e.g. 'phys-define-velocity-2023-ol')
  subjectId     MUST be exactly 'physics'
  subjectLabel  'Physics'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2023 HL · Q5(a)' or '2024 OL · Q6(b)'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim.
  commandWord   the single cue (or multi-word cue like 'Distinguish between', 'What is meant by', 'Show that')
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question. Name the exact thing
                the scheme rewards (the definition wording, the formula, the unit, the *starred answer, the steps).
  trap          the examiner/scheme-flagged mistake for THIS cue + the marks consequence. Quote the scheme where it
                bites (e.g. "scheme needs 'per unit time' for the def", "mark for the formula even if arithmetic wrong",
                "must give the DIRECTION of the induced current", "Kelvin essential").
  source        'LC Physics {YEAR} {LEVEL} marking scheme, Q… ("…award point…")'
  marks         integer marks at stake on that part (from the scheme)
  figure        OPTIONAL — only if the cue genuinely depends on a visual AND it is one of the committed crops below
                whose SOURCE QUESTION matches your stem. Shape { src, alt, source }.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after
stripping non-letters and lowercasing. So if commandWord is 'Calculate', the word 'Calculate' must literally be in
the stem; for 'Distinguish between', those two words must be consecutive in the stem. Verify this yourself per stem.

ALREADY-COMMITTED physics figures you MAY reuse ONLY if your stem genuinely IS that exact question:
  /exam-figures/physics/physics-2022-hl-xyz-circuit.png — 2022 HL Q9(c): X=1Ω in series with a 12 V supply, Y=6Ω ∥ Z=3Ω
  /exam-figures/physics/physics-2024-ol-concave-mirror-ray.png — 2024 OL Q8: 'copy and complete' concave-mirror ray diagram (object, f, mirror)
figure.source = 'SEC Leaving Certificate Physics {YEAR} {LEVEL}, Q… — © State Examinations Commission' + a precise alt.
Most physics command-word stems are text-only — that is fine and expected. Do NOT force a figure.

QUALITY BAR (reject your own draft if it fails):
- demand must be specific to cue+question, not generic. BANNED filler: "read the question carefully", "manage your
  time", "show your working", "plan your answer", or any sentence that fits any exam.
- trap must name a real, scheme-grounded error pattern (a definition phrase the scheme requires, a unit that's
  essential, a formula-mark rule, a sign/direction requirement, 'Kelvin essential', the per-unit-X wording, etc.).
- Prefer cue DIVERSITY: mix Define, State, Calculate, Explain, Describe, Name, Outline, Derive, Show that, Justify,
  Distinguish between, What is meant by, Account for.
- ASCII physics fine (m s^-2, ×10^8, ->, ohm); unicode (×,°,λ,Ω,μ) fine.

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
          figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'mechanics-heat', cues: 'Define, State, Calculate, Show that',
    topics: 'linear motion & equations of motion, Newton\'s laws & force, momentum & conservation, work/energy/power, circular motion, SHM, moments/equilibrium, density/pressure, temperature, specific heat capacity, latent heat, heat transfer' },
  { key: 'waves-sound-light', cues: 'Define, Explain, Calculate, Describe',
    topics: 'wave properties (f, λ, v=fλ), Doppler effect, resonance & stationary waves, sound intensity, reflection/mirrors, refraction & Snell\'s law, total internal reflection, lenses, diffraction grating, dispersion, EM spectrum' },
  { key: 'electricity-em', cues: 'Define, Calculate, Describe, State, Derive',
    topics: 'charge & electric fields, capacitance, potential difference, current, resistance & resistivity, series/parallel circuits, Wheatstone bridge, potential divider, domestic electricity & safety, semiconductors, magnetic fields & force on a conductor, electromagnetic induction, transformers, AC' },
  { key: 'modern-physics', cues: 'Define, State, Explain, Name, Write, Distinguish between',
    topics: 'the electron & e/m, photoelectric effect & work function, X-rays, atomic structure & energy levels, the nucleus, radioactivity (α/β/γ, half-life), nuclear decay equations, nuclear energy (fission/fusion, E=mc²), ionising radiation hazards/uses, particle physics (HL)' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(
    `${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\n` +
    `Produce 4 stems: aim for 2 Higher + 2 Ordinary, each with a DIFFERENT command word where possible. ` +
    `Spread across different years/questions. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

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
    `1. TAPPABILITY: does commandWord appear as a consecutive word-token run in stem (strip punctuation, lowercase)? If not → tappable:false, verdict:fix (pick the cue that IS in the stem, or adjust the stem to the faithful wording that contains it).\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? Do marks + demand's "scheme-rewarded thing" + trap's quoted award point match the scheme text? If fabricated/mis-cited → grounded:false.\n` +
    `3. ACCURACY: any physics error in demand (wrong definition, wrong law, wrong unit, wrong formula, wrong number, wrong marks)?\n` +
    `4. FIGURE (if present): src must match a stem genuinely from that exact question; else drop the figure in a fix.\n` +
    `5. QUALITY: demand specific (no banned filler)? trap a real scheme pattern?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep the id). If sound, accept. If fabricated, reject.\n\n` +
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
  `Completeness critic for a Physics Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef, hasFigure: !!k.figure })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) command-word diversity (flag if one cue dominates), (3) topic spread across ` +
  `mechanics/heat, waves/sound/light, electricity/EM, modern physics, (4) whether figure-dependent cues are present. ` +
  `List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
