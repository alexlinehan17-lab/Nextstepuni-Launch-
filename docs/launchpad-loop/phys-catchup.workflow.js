export const meta = {
  name: 'phys-catchup',
  description: 'Author + adversarially verify Physics Catch-Up Lane recovery cards from real SEC schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each card vs scheme' },
    { title: 'Critic', detail: 'completeness + level/topic balance' },
  ],
}

const TXT = '/tmp/phys_txt'

const TOPICS = `
VALID physics topicIds (topicId MUST be one of these; the card's strand = topicId minus its last -N segment, e.g. physics-0-2 → strand physics-0):
MECHANICS (physics-0): -0 Linear Motion, -1 Vectors and Scalars, -2 Newton's Laws of Motion, -3 Conservation of Momentum, -4 Gravity, -5 Density and Pressure, -6 Moments, -7 Conditions for Equilibrium, -8 Work, -9 Energy, -10 Power, -11 Circular Motion (HL), -12 Simple Harmonic Motion and Hooke's Law (HL)
TEMPERATURE (physics-1): -0 Concept of Temperature, -1 Thermometric Property, -2 Thermometers and Temperature Scales
HEAT (physics-2): -0 Concept of Heat, -1 Specific Heat Capacity, -2 Specific Latent Heat, -3 Heat Transfer: Conduction, -4 Heat Transfer: Convection, -5 Heat Transfer: Radiation
WAVES (physics-3): -0 Properties of Waves, -1 Wave Phenomena, -2 Doppler Effect
VIBRATIONS AND SOUND (physics-4): -0 Wave Nature of Sound, -1 Characteristics of Notes, -2 Resonance, -3 Vibrations in Strings and Pipes, -4 Sound Intensity
LIGHT (physics-5): -0 Laws of Reflection, -1 Mirrors, -2 Laws of Refraction, -3 Total Internal Reflection, -4 Lenses, -5 Diffraction and Interference, -6 Light as a Transverse Wave, -7 Dispersion, -8 Colours, -9 Electromagnetic Spectrum, -10 The Spectrometer
ELECTRICITY (physics-6): -0 Electrification by Contact, -1 Electrification by Induction, -2 Distribution of Charge on Conductors, -3 The Electroscope, -4 Force Between Charges, -5 Electric Fields, -6 Potential Difference, -7 Capacitors and Capacitance, -8 Electric Current, -9 Sources of EMF and Current, -10 Conduction in Materials, -11 Resistance, -12 Effects of an Electric Current, -13 Domestic Circuits and Safety, -14 Magnetism and Magnetic Fields, -15 Current in a Magnetic Field, -16 Electromagnetic Induction, -17 Alternating Current, -18 Mutual and Self-Induction
MODERN PHYSICS (physics-7): -0 The Electron, -1 Thermionic Emission, -2 Photoelectric Emission, -3 X-Rays, -4 Structure of the Atom, -5 Structure of the Nucleus, -6 Radioactivity, -7 Nuclear Energy, -8 Ionising Radiation: Hazards and Uses, -9 Particle Physics (Option, HL)
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert PHYSICS (Irish exam-recovery tool). A card teaches a
student who lost marks on a topic how to recover them: a clear gist, the ONE highest-leverage move, and a
check question with a model answer.

GROUNDING (non-negotiable): every card is grounded in REAL SEC LC Physics questions + marking schemes. The text
of all papers + schemes (2021-2025, HL+OL) is at ${TXT}/ as plain text (pages: ===PAGE n===):
  physics-YYYY-HL-paper.txt / physics-YYYY-OL-paper.txt
  physics-YYYY-HL-marking-scheme.txt / physics-YYYY-OL-marking-scheme.txt
grep/Read to find the exact question + its scheme award points. Do NOT invent question numbers, marks, scheme
wording, or data. RECOMPUTE every calculation from the data and confirm it matches the scheme's answer.
LC Physics formulae/data come from the official Formulae & Tables booklet — use standard values (g = 9.8 m s^-2,
c = 3.0×10^8 m s^-1, etc.) and the data the question gives.

${TOPICS}

THE CARD (one object per card):
  id            kebab-case, prefix 'phys-', unique, includes the topic (e.g. 'phys-momentum-conservation-2023-hl')
  subjectId     MUST be exactly 'physics'
  topicId       one of the valid ids above
  subjectLabel  'Physics'
  topicLabel    a short human label (may match the syllabus subtopic name)
  focus         short row label disambiguating same-subtopic cards (e.g. 'Momentum: explosion calc')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core idea + how the exam tests it. Plain, supportive, precise.
  oneMove       { label: short imperative, text: the single highest-leverage move that wins the marks }
  check         { prompt: a self-contained exam-style question, modelAnswer: full worked answer,
                  needed: [>=2 award-point strings the answer must contain] }
  source        citation: 'Topic … — SEC LC Physics {YEAR} {LEVEL}, Q… + marking scheme (…the scheme answer…)'
  marksWeight   integer marks at stake (from the scheme)
  figureSpec    OPTIONAL — include ONLY if the question genuinely needs a visual (circuit diagram, graph,
                ray diagram, apparatus, vector diagram) for the check to be answerable. Shape:
                { year, level, questionRef, describes (what the figure shows in detail), whyNeeded }.
                DO NOT put a 'figure' field or a src — the crop does not exist yet; the main loop extracts it.

SELF-CONTAINMENT (hard rule): the check prompt must be answerable from what the card itself provides + general
physics knowledge. If it needs a diagram/graph/circuit/data, EITHER (a) add a figureSpec so the real figure can
be cropped, OR (b) embed the needed numbers/setup in the prompt text, OR (c) rewrite it self-contained. Never
let a prompt silently depend on an unseen figure. Most calculation/definition cards are naturally self-contained.

QUALITY BAR: oneMove must name a SPECIFIC physics move/error (e.g. 'convert °C to K before the gas law',
'the scheme needs the direction of the induced current, not just its size', 'mark for the formula even if the
arithmetic is wrong'). BANNED filler: 'show your working', 'read the question', 'manage your time'. ASCII physics
is fine (m s^-2, ×10^8, ->, Ω as 'ohm'); unicode (×, °, λ, Ω, μ) is also fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const CARD_SCHEMA = {
  type: 'object', required: ['cards'],
  properties: {
    cards: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'subjectId', 'topicId', 'subjectLabel', 'topicLabel', 'focus', 'level', 'gist', 'oneMove', 'check', 'source', 'marksWeight'],
        properties: {
          id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
          subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
          level: { type: 'string', enum: ['higher', 'ordinary'] }, gist: { type: 'string' },
          oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
          check: {
            type: 'object', required: ['prompt', 'modelAnswer', 'needed'],
            properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } },
          },
          source: { type: 'string' }, marksWeight: { type: 'integer' },
          figureSpec: {
            type: 'object',
            properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } },
          },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'mechanics', strands: 'physics-0 (Mechanics)',
    topics: 'linear motion (equations of motion, v-t graphs), Newton\'s laws & force, momentum & collisions/explosions, work-energy-power, gravity & gravitation, circular motion (HL), SHM & Hooke\'s law (HL), moments & equilibrium, density & pressure' },
  { key: 'heat-waves-sound', strands: 'physics-1 (Temperature), physics-2 (Heat), physics-3 (Waves), physics-4 (Vibrations and Sound)',
    topics: 'temperature & thermometric property, specific heat capacity & latent heat calcs, heat transfer (U-values/conduction), wave properties (f, λ, v=fλ), Doppler effect, resonance & stationary waves in strings/pipes, fundamental frequency, sound intensity level (dB)' },
  { key: 'light-optics', strands: 'physics-5 (Light)',
    topics: 'reflection & mirrors (1/u+1/v=1/f, magnification), refraction & Snell\'s law, total internal reflection & critical angle, lenses & power, diffraction grating (nλ=dsinθ), dispersion, the spectrometer, EM spectrum' },
  { key: 'electricity-em', strands: 'physics-6 (Electricity, incl. magnetism & electromagnetism)',
    topics: 'charge & Coulomb\'s law & electric fields, capacitance, current/pd/resistance (V=IR), resistivity, series/parallel circuits, Wheatstone bridge & potential divider, domestic electricity & safety (fuses, RCD), semiconductors, magnetic fields & force on a conductor, electromagnetic induction (Faraday/Lenz), transformers, AC' },
  { key: 'modern-physics', strands: 'physics-7 (Modern Physics)',
    topics: 'the electron & e/m, photoelectric effect (E=hf, threshold frequency, work function), X-rays, atomic structure & energy levels, the nucleus, radioactivity (α/β/γ, half-life, decay equations), nuclear energy (E=mc², fission/fusion), ionising radiation hazards/uses, particle physics (HL option)' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(
    `${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\n` +
    `Produce 4 recovery cards: aim for 2 Higher + 2 Ordinary, spread across DIFFERENT subtopics and years. ` +
    `Favour the high-frequency, high-mark exam questions. Read the relevant ${TXT}/ files; recompute every ` +
    `calculation and confirm it matches the scheme. Add figureSpec ONLY where the check truly needs a visual.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'mathChecks', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, selfContained: { type: 'boolean' },
    reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `You are an independent SKEPTIC verifying ONE Physics Catch-Up recovery card against the real SEC sources at ${TXT}/.\n` +
    `Default to REJECT/FIX if anything is off. Using grep/Read on the paper + marking-scheme text files:\n` +
    `1. GROUNDING: is this a real ${c.level} question near "${c.source}"? Do the marks + the scheme's modelled answer + the award points actually match the scheme text? If fabricated/mis-cited → grounded:false.\n` +
    `2. MATHS: RECOMPUTE every number in the modelAnswer from the data. Does it match (units, magnitude, sig figs, the scheme's answer)? If any calc is wrong → mathChecks:false.\n` +
    `3. PHYSICS ACCURACY: any conceptual error (wrong law, wrong direction, wrong formula, wrong definition)?\n` +
    `4. SELF-CONTAINMENT: can a student answer check.prompt from the card alone (text + figureSpec if present)? If it silently needs an unseen figure/data and has no figureSpec → selfContained:false (fix by adding a figureSpec or embedding the data).\n` +
    `5. QUALITY: is oneMove a specific physics move (not banned filler)? Are needed[] real award points?\n\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep the same id; preserve/repair figureSpec). ` +
    `If sound, verdict:accept. If fabricated/unsalvageable, verdict:reject.\n\n` +
    `THE CARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ card: c, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.card)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) kept.push({ ...r.card, ...r.v.fixedCard })
}
log(`Verify: ${kept.length}/${cards.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a Physics Catch-Up Lane recovery-card set (Irish LC). The ${kept.length} kept cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec, marks: k.marksWeight })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) strand spread across the 8 physics strands (Mechanics, Temperature, Heat, ` +
  `Waves, Vibrations/Sound, Light, Electricity/EM, Modern Physics) — flag any strand with no card, (3) mix of ` +
  `calculation vs definition/explanation cards, (4) whether figure-needing topics (circuits, graphs, ray/vector ` +
  `diagrams, apparatus) are represented. List concrete gaps to fill in a top-up round. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
