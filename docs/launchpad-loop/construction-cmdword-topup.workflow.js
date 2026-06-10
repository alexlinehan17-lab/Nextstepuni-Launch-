export const meta = {
  name: 'construction-cmdword-topup',
  description: 'Fill Construction Studies Command-Word gaps: 2nd sketch-required HL junction detail, OL sustainability Discuss-with-sketches',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic checks grounding + tappability' },
  ],
}

const TXT = '/tmp/construction_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert CONSTRUCTION STUDIES (written theory paper). The student taps the
COMMAND WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

EXAM SHAPE: HIGHER 300 marks (answer any 5, 60 each); ORDINARY 200 marks (answer any 4, 50 each). Sketches in pencil;
"Neat freehand sketches to illustrate written descriptions should be made"; materials must be NAMED with sizes/dimensions.

CUE GRAMMAR: 'Discuss in detail, using notes and freehand sketches' / 'Show … on your drawing' = DEVELOPED points WITH
labelled freehand sketches (a text-only answer is capped — the scheme splits marks Notes + Sketches). 'Calculate' (HL only)
= U = 1/ΣR with units. 'State/Give/List' = the exact number of named points.

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — construction-studies-YYYY-{HL,OL}-written.txt /
construction-studies-YYYY-{HL,OL}-marking-scheme.txt (pages ===PAGE n===). grep/Read for the exact stem + scheme award.
Do NOT invent question numbers/marks/materials/wording. If you can't verify the stem AND the scheme, pick a different real
question that fits the slot.

OUTPUT one object (schema's "stem"): id (kebab, 'cons-' prefix, cue+topic), subjectId='construction-studies',
subjectLabel='Construction Studies', level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord
verbatim), commandWord, demand, trap (scheme rule + marks consequence; the Notes+Sketches split where a sketch is
required), source ('LC Construction Studies {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int). figureSpec ONLY if the
cue depends on a diagram printed in the question.

TAPPABILITY (a test enforces it): commandWord must be a CONSECUTIVE token-run in stem after stripping non-letters and
lowercasing. Verify it yourself.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','show your working','draw neatly'). trap =
a real scheme rule. Plain text; unicode (×,°,²,≤) fine. Return data only; never edit a file.
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
  { key: 'hl-show-sketch-junction', level: 'higher',
    topic: 'A HIGHER "Show" or "Draw" stem for a specific CONSTRUCTION JUNCTION DETAIL drawn to scale with a labelled freehand sketch — e.g. an eaves/wall-plate junction, a window head/sill/reveal, a foundation-to-wall junction, a roof verge. This is the 2nd instance of the signature sketch-required trap. Demand: the labelled, dimensioned detail with named materials; trap = the scheme splits marks Notes/Drawing + an unlabelled/undimensioned drawing loses the drawing marks.' },
  { key: 'ol-discuss-sustainability', level: 'ordinary',
    topic: 'An ORDINARY "Discuss" / "Describe" stem (using notes and freehand sketches) on a SUSTAINABILITY / INSULATION / energy-upgrade topic — e.g. improving the BER, fitting external/internal wall insulation, draught-proofing, a renewable energy source, reducing heat loss. Demand: developed points WITH labelled sketches; trap = text-only answer forfeits the sketch marks (scheme splits Notes + Sketches).' },
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
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Construction Studies Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive token-run in stem (strip punctuation, lowercase)? else fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + scheme rule in demand/trap match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any construction error (wrong material/dimension/detail)?\n` +
    `4. QUALITY: demand specific (no filler)? trap a real scheme rule (Notes+Sketches split where a sketch is required)?\n` +
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
