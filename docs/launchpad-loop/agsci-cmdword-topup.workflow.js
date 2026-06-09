export const meta = {
  name: 'agsci-cmdword-topup',
  description: 'Fill AgSci Command-Word gaps: Scientific Practices, Distinguish, OL calc, a Crops cue, a ruminant figure-based Identify',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + fact-checks each' },
  ],
}

const TXT = '/tmp/agsci_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert AGRICULTURAL SCIENCE (new spec 2021+). The student taps the
COMMAND WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — agricultural-science-YYYY-{HL,OL}-{paper,marking-scheme}.txt
(pages ===PAGE n===). grep/Read for the exact stem + scheme award points. Do NOT invent question numbers/marks/wording.
If you can't verify the stem AND the scheme, pick a different real question that fits the slot. RECOMPUTE any number.

OUTPUT one object (schema's "stem"): id (kebab, 'agsci-' prefix, cue+topic), subjectId='agricultural-science',
subjectLabel='Agricultural Science', level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord
verbatim), commandWord, demand (answer-shaping move + scheme-rewarded thing), trap (scheme rule + marks consequence;
quote the award), source ('LC Agricultural Science {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int),
figure (ONLY if the cue genuinely needs the committed diagram below AND your stem IS that exact question — else omit).

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify it yourself; use the casing as it appears in the stem.

COMMITTED Ag Science figure reusable ONLY if your stem genuinely IS that exact question:
  /exam-figures/agricultural-science/agricultural-science-2021-ol-ruminant-stomach.png — 2021 OL Q2(a): label the sheep's
  digestive system parts A (Rumen), B (Abomasum), C (Omasum); Oesophagus/Small Intestine/Reticulum already labelled.
figure.source = 'SEC Leaving Certificate Agricultural Science 2021 Ordinary Level, Q2(a) — © State Examinations Commission' + a precise alt.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','show your working','plan your answer').
trap = a real scheme rule. Plain text; unicode (×,°,→) fine. Return data only; never edit a file.
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
  { key: 'scientific-practices', level: 'higher',
    topic: 'A SCIENTIFIC PRACTICES stem (the strand currently has 0 command-word stems). A real question whose cue is "Describe" / "Outline" on an experiment method/procedure, or a data-handling/validity question (reliability, controlling variables, the Individual Investigative Study). The commandWord must appear in the stem.' },
  { key: 'distinguish-cue', level: 'higher',
    topic: 'A "Distinguish between" stem (commandWord = "Distinguish between") — currently absent. A real question distinguishing two terms (e.g. soil texture vs structure; two soil types; two crops; two breeding terms; ruminant vs monogastric). Teach contrasting BOTH on the same dimension. Prefer Soils or Crops to rebalance away from Animals.' },
  { key: 'ol-calculate', level: 'ordinary',
    topic: 'An OL CALCULATE stem (commandWord = "Calculate") — both existing calc stems are HL. A real OL calculation (stocking rate / livestock units, % organic matter or water, fertiliser, a ratio, a financial/yield figure). Embed the data inline; recompute and match the scheme.' },
  { key: 'crops-cue', level: 'ordinary',
    topic: 'A CROPS stem (rebalance away from Animals) with a cue NOT already dominant — prefer "Define", "List", "Name", "Give an account of", or "State". A real crops question (plant physiology, grassland, cereals, establishment, weed/pest/disease, silage). The commandWord must appear in the stem.' },
  { key: 'ruminant-figure-identify', level: 'ordinary',
    topic: 'The 2021 OL Q2(a) ruminant question: "Identify the labelled parts A, B and C on the diagram using the correct word from the list" (commandWord = "Identify"). Attach the committed figure agricultural-science-2021-ol-ruminant-stomach.png (it genuinely IS this question). Demand: read A/B/C off the diagram and name them (A=Rumen, B=Abomasum, C=Omasum); trap = the scheme awards each named part separately, so describing position instead of naming, or swapping B/C, loses marks.' },
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
    `Independent SKEPTIC verifying ONE Agricultural Science Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? else fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme thing + trap's quoted award match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any ag-science error (term, soil pH direction, digestive compartment, ratio, calc value)?\n` +
    `4. FIGURE (if present): src matches a stem genuinely from that exact question (ruminant only on 2021 OL Q2a)? else drop the figure in a fix.\n` +
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
