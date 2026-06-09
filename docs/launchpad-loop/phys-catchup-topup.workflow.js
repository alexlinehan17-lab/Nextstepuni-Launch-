export const meta = {
  name: 'phys-catchup-topup',
  description: 'Fill Physics Catch-Up critic gaps: empty strands, definition/law/experiment cards, + figure-bearing circuit/graph/ray cards',
  phases: [
    { title: 'Author', detail: 'one targeted card per flagged gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each vs scheme' },
  ],
}

const TXT = '/tmp/phys_txt'

const TOPICS = `
VALID physics topicIds (topicId MUST be one; strand = topicId minus last -N):
MECHANICS physics-0: -0 Linear Motion … -2 Newton's Laws … -6 Moments … -9 Energy … -12 SHM & Hooke (HL)
TEMPERATURE physics-1: -0 Concept of Temperature, -1 Thermometric Property, -2 Thermometers and Temperature Scales
HEAT physics-2: -1 Specific Heat Capacity, -2 Specific Latent Heat, -3/-4/-5 Heat Transfer (cond/conv/rad)
WAVES physics-3: -0 Properties of Waves, -1 Wave Phenomena, -2 Doppler Effect
VIBRATIONS AND SOUND physics-4: -0 Wave Nature of Sound, -1 Characteristics of Notes, -2 Resonance, -3 Vibrations in Strings and Pipes, -4 Sound Intensity
LIGHT physics-5: -0 Laws of Reflection, -1 Mirrors, -2 Laws of Refraction, -3 Total Internal Reflection, -4 Lenses, -5 Diffraction and Interference, -9 EM Spectrum, -10 The Spectrometer
ELECTRICITY physics-6: -4 Force Between Charges, -5 Electric Fields, -6 Potential Difference, -7 Capacitors, -8 Electric Current, -11 Resistance, -12 Effects of a Current, -13 Domestic Circuits and Safety, -14 Magnetism, -15 Current in a Magnetic Field, -16 Electromagnetic Induction, -17 AC
MODERN physics-7: -2 Photoelectric Emission, -3 X-Rays, -4 Structure of the Atom, -5 Structure of the Nucleus, -6 Radioactivity, -7 Nuclear Energy
`

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for Leaving Cert PHYSICS (Irish exam-recovery tool). A card teaches a
student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a check with a model answer.

GROUNDING (non-negotiable): ground the card in a REAL SEC LC Physics question + scheme. Text of all papers + schemes
(2021-2025 HL+OL) at ${TXT}/ (pages ===PAGE n===): physics-YYYY-{HL,OL}-{paper,marking-scheme}.txt
grep/Read for the exact question + award points. Do NOT invent question numbers, marks, scheme wording, or data.
RECOMPUTE any calculation from the data and confirm it matches the scheme. Use standard LC values (g=9.8, c=3.0e8, etc.).

${TOPICS}

CARD FIELDS: id (kebab, 'phys-' prefix, includes topic), subjectId='physics', topicId (one valid id),
subjectLabel='Physics', topicLabel (short), focus (short row label), level ('higher'|'ordinary'),
gist (2-5 sentences), oneMove {label, text} (the single highest-leverage move/error — SPECIFIC physics, not filler),
check {prompt (self-contained, exam-style), modelAnswer (full), needed (>=2 award-point strings)},
source ('Topic … — SEC LC Physics {YEAR} {LEVEL}, Q… + marking scheme (…answer…)'), marksWeight (int).

SELF-CONTAINMENT: the check prompt must be answerable from the card alone + general physics. If it needs a
diagram/graph/circuit, set figureSpec {year, level, questionRef, describes (detailed), whyNeeded}. DO NOT add a
'figure'/'src' field — the crop is extracted later by the main loop. If a card is a pure definition/law/experiment
description it needs no figure.

QUALITY: oneMove names a specific physics move/error. BANNED filler: 'show your working', 'read the question',
'manage your time'. ASCII physics fine (m s^-2, ×10^8, ->, ohm); unicode (×,°,λ,Ω,μ) fine. Return data only; never edit a file.
`

const STEM_SCHEMA = {
  type: 'object', required: ['card'],
  properties: {
    card: {
      type: 'object',
      required: ['id', 'subjectId', 'topicId', 'subjectLabel', 'topicLabel', 'focus', 'level', 'gist', 'oneMove', 'check', 'source', 'marksWeight'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
        subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
        level: { type: 'string', enum: ['higher', 'ordinary'] }, gist: { type: 'string' },
        oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
        check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
        source: { type: 'string' }, marksWeight: { type: 'integer' },
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const SLOTS = [
  { key: 'sound-fundamental-freq-hl', level: 'higher', figure: false,
    topic: 'VIBRATIONS AND SOUND (physics-4, prefer -3 Vibrations in Strings and Pipes or -2 Resonance): a HL calculation — fundamental frequency of a stretched string f = (1/2L)*sqrt(T/mu), or of a pipe (open f=c/2L, closed f=c/4L), or a resonance-tube length. Embed all data in the prompt.' },
  { key: 'sound-intensity-or-resonance-ol', level: 'ordinary', figure: false,
    topic: 'VIBRATIONS AND SOUND (physics-4, prefer -4 Sound Intensity or -2 Resonance): an OL question — sound intensity level in dB and the doubling rule, OR a resonance/tuning-fork/frequency question. Embed data in the prompt.' },
  { key: 'temperature-ol', level: 'ordinary', figure: false,
    topic: 'TEMPERATURE (physics-1): an OL question — define a thermometric property / name thermometric properties / explain how a thermometer is calibrated using fixed points / convert between Celsius and Kelvin. Likely definition-style (low/no calc).' },
  { key: 'circuit-resistance-figure', level: 'higher', figure: true,
    topic: 'ELECTRICITY (physics-6, -11 Resistance or -6 Potential Difference): a circuit question needing a CIRCUIT DIAGRAM — series/parallel resistance, a potential divider, or a Wheatstone bridge. REQUIRED: provide a figureSpec for the circuit diagram (genuinely from that exact SEC question).' },
  { key: 'graph-slope-experiment-figure', level: 'higher', figure: true,
    topic: 'A MANDATORY-EXPERIMENT GRAPH question (any strand — e.g. resistivity vs length, specific heat, half-life activity-vs-time decay curve, or u-v for a lens) where the student must read a SLOPE or intercept off a graph. REQUIRED: figureSpec for the graph (from that exact SEC question).' },
  { key: 'definition-law-card', level: 'ordinary', figure: false,
    topic: 'A DEFINITION/LAW card (NO calculation): state a law or define a quantity exactly as the scheme rewards it — e.g. Newton\'s 2nd law, the principle/law of conservation of momentum, the laws of refraction, define specific heat capacity, define the volt/ampere, or state the laws of equilibrium. Pick one that is high-frequency and quote the scheme\'s accepted wording.' },
  { key: 'experiment-procedure-card', level: 'higher', figure: false,
    topic: 'An EXPERIMENT-DESCRIPTION card (Section A mandatory experiment): describe the procedure/precaution/source-of-error for a named experiment (e.g. measure specific heat capacity, focal length of a converging lens, resistivity of a wire, verify Joule\'s law). Ground the steps + the precaution/error in the scheme. May add figureSpec if the apparatus diagram genuinely helps, else omit.' },
  { key: 'optics-ray-figure', level: 'ordinary', figure: true,
    topic: 'LIGHT (physics-5, -3 Total Internal Reflection or -4 Lenses or -1 Mirrors): an optics question that genuinely needs a RAY DIAGRAM (e.g. TIR in a prism/optical fibre, image formation in a lens/mirror). REQUIRED: figureSpec for the ray diagram (from that exact SEC question).' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED level: ${s.level}\n` +
    (s.figure ? `REQUIRED: this card MUST include a figureSpec for a real figure from that exact SEC question.\n` : ``) +
    `TOPIC: ${s.topic}\n\nReturn exactly one grounded card for this slot.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.card ? { ...r.card, _slot: s.key } : null),
))

const cards = authored.filter(Boolean)
log(`Authored ${cards.length} top-up cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'mathChecks', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Physics Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question near "${c.source}"? marks + scheme answer + award points match the scheme text? else grounded:false.\n` +
    `2. MATHS: RECOMPUTE every number in modelAnswer from the data; matches (units, magnitude, sig figs, scheme answer)? else mathChecks:false.\n` +
    `3. PHYSICS: any conceptual/definition/law error?\n` +
    `4. SELF-CONTAINMENT: answerable from the card alone (+figureSpec if present)? If it silently needs an unseen figure and has no figureSpec → selfContained:false.\n` +
    `5. FIGURE: if figureSpec present, does it describe a real figure from that exact question? If a figure is needed but absent, fix by adding figureSpec.\n` +
    `6. QUALITY: oneMove specific (no filler)? needed[] real award points?\n` +
    `If fixable, verdict:fix with a complete corrected card in fixedCard (keep id; preserve/repair figureSpec). If sound, accept. If fabricated, reject.\n\n` +
    `THE CARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c._slot}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ card: c, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  const clean = { ...r.card }; delete clean._slot
  if (r.v.verdict === 'accept') kept.push(clean)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) { const f = { ...clean, ...r.v.fixedCard }; delete f._slot; kept.push(f) }
}
log(`Top-up verify: ${kept.length}/${cards.length} kept`)
return { kept, authoredCount: cards.length, keptCount: kept.length }
