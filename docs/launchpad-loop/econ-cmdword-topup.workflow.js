export const meta = {
  name: 'econ-cmdword-topup',
  description: 'Fill Economics Command-Word gaps: Define/Distinguish/Discuss cues, fiscal/taxation, factors/circular-flow, a figure-based PED calc',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + accuracy-checks each' },
  ],
}

const TXT = '/tmp/econ_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert ECONOMICS (NEW spec, examined 2022+). The student taps the
COMMAND WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — economics-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages
===PAGE n===). PRIORITISE 2022-2025 (current spec); 2021 is OLD syllabus — avoid unless identical. grep/Read for the
exact stem + scheme award points. Do NOT invent question numbers/marks/wording. If you can't verify the stem AND the
scheme, pick a different real question that fits the slot. RECOMPUTE any number.

OUTPUT one object (schema's "stem"): id (kebab, 'econ-' prefix, cue+topic), subjectId='economics', subjectLabel='Economics',
level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord verbatim), commandWord,
demand (answer-shaping move + scheme-rewarded thing), trap (scheme rule + marks consequence; quote the award),
source ('LC Economics {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int),
figure (ONLY if the cue genuinely needs a graph AND you reuse a committed crop whose source-question matches — else omit).

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify it yourself; use the casing as it appears in the stem.

COMMITTED economics figures reusable ONLY if your stem genuinely IS that exact question:
  /exam-figures/economics/economics-2022-hl-ped-facemasks-demand.png — 2022 HL Q1(a) face-mask demand curve (P €4↔€5 at Q 8↔4; reading off gives PED = -3)
  /exam-figures/economics/economics-2024-hl-cpi-annual-change.png — 2024 HL Q12(b) CPI all-items annual %-change graph
  /exam-figures/economics/economics-2022-hl-eur-gbp-exchange-rate.png — 2022 HL Q15(b) €/£ exchange-rate graph
figure.source = 'SEC Leaving Certificate Economics {YEAR} {LEVEL}, Q… — © State Examinations Commission' + a precise alt.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','show your working','plan your answer').
trap = a real scheme rule (elasticity sign, curve-shift, GDP/GNP relation, define-vs-opposite, name-AND-explain). € + unicode fine.
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
  { key: 'define-cue', level: 'higher',
    topic: 'A "Define" stem (commandWord = "Define"). Find a real question that begins "Define ..." (e.g. define a key economic term — GDP, inflation, the multiplier, opportunity cost, a tax). Teach the precise scheme-required wording for that definition.' },
  { key: 'distinguish-cue', level: 'higher',
    topic: 'A "Distinguish between" stem (commandWord = "Distinguish between"). Find a real question distinguishing two terms (e.g. GDP and GNP; appreciation and depreciation; direct and indirect tax; two unemployment types). Teach that you must contrast BOTH on the same dimension.' },
  { key: 'discuss-evaluate-cue', level: 'higher',
    topic: 'A higher-order HL cue: find a real stem using "Discuss", "Evaluate", "Analyse" or "Examine" (commandWord = that exact word). Teach that it demands developed evaluation/argument (advantages AND disadvantages, or a reasoned judgement), not a list.' },
  { key: 'fiscal-taxation', level: 'ordinary',
    topic: 'A GOVERNMENT FINANCE / FISCAL POLICY / TAXATION stem (economics-3-1) — currently a topic gap. Any real cue in the stem (Outline/Explain/State/Define) on the government budget, deficit/surplus, a type of tax, or the purpose of taxation. OL preferred to balance levels.' },
  { key: 'figure-ped-calc', level: 'higher',
    topic: 'A FIGURE-BASED calculation stem: the 2022 HL Q1(a) face-mask question that gives a DEMAND GRAPH and asks to calculate PED (commandWord = "calculate" or "Calculate" as it appears). Attach the committed figure economics-2022-hl-ped-facemasks-demand.png (it genuinely IS this question). This adds a figure + reduces the Outline-cue dominance. Demand: read the two price-quantity points off the graph, then apply the arc formula; PED = -3 (keep the sign).' },
  { key: 'factors-or-circular-flow', level: 'ordinary',
    topic: 'A FOUNDATIONS stem (economics-0 or economics-1-0 Market Economy) — factors of production, the circular flow of income, or economic systems. Currently thin. Any real cue in the stem. OL preferred.' },
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
    `Independent SKEPTIC verifying ONE Economics Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? else fix.\n` +
    `2. GROUNDING: real ${s.level} NEW-SPEC question near ${s.questionRef}? marks + demand's scheme thing + trap's quoted award match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any economics error (definition, elasticity sign, GDP/GNP, curve-shift, calc value)?\n` +
    `4. FIGURE (if present): src matches a stem genuinely from that exact question (e.g. PED graph only on 2022 HL Q1(a))? else drop the figure in a fix.\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme rule?\n` +
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
