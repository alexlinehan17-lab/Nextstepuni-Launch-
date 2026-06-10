export const meta = {
  name: 'art-cmdword-topup',
  description: 'Fill Art Command-Word gap: HL Section B European-art essay cue (currently only 1 OL Section B stem)',
  phases: [
    { title: 'Author', detail: 'targeted Section B European stems' },
    { title: 'Verify', detail: 'skeptic checks grounding + art-facts + tappability' },
  ],
}

const TXT = '/tmp/art_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert ART — VISUAL STUDIES (written paper). The student taps the COMMAND
WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

EXAM SHAPE: Section B "Europe and the wider world" = a 50-mark ESSAY (answer one). The cues are 'Discuss', 'Analyse',
'Compare', 'Describe', 'Outline'. The essay demands a structured argument: named movement/artist + context + named work(s)
+ analysis with art vocabulary. Trap: narration/biography or listing without analysis, or no named work.

GROUNDING: ground in REAL SEC LC Art Section B questions + schemes at ${TXT}/ (art-YYYY-{HL,OL}-{written,marking-scheme}.txt,
pages ===PAGE n===; favour 2023-2025). grep/Read for the exact Section B stem + scheme indicative content. Do NOT invent
question numbers/marks/wording. Art facts MUST be accurate.

OUTPUT one object (schema's "stem"): id (kebab, 'art-' prefix, cue+topic), subjectId='art', subjectLabel='Art', level,
questionRef ('… HL · Section B · Q…'), stem (faithful; MUST contain commandWord verbatim), commandWord, demand, trap,
source ('LC Art (Visual Studies) {YEAR} {LEVEL} marking scheme, Section B, Q… ("…")'), marks (50 for the essay). NO
figureSpec (Section B essays are not plate-based).

TAPPABILITY (a test enforces it): commandWord must be a consecutive token-run in stem (strip non-letters, lowercase).

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','be creative'). trap = a real scheme
pattern. Return data only; never edit a file.
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
      },
    },
  },
}

const SLOTS = [
  { key: 'hl-sectionB-european', level: 'higher',
    topic: 'A HIGHER Section B "Europe and the wider world" essay stem (cue Discuss/Analyse/Compare) on a European movement/artist/theme — currently there is NO HL Section B stem. Use a real 2023-2025 HL Section B question. Demand: a structured essay (movement/context + named work(s) + analysis with art vocabulary). Trap: narration/biography without analysis, or no specific named work.' },
  { key: 'hl-sectionB-second', level: 'higher',
    topic: 'A SECOND HL Section B essay stem with a DIFFERENT cue or theme from the first (e.g. if the first is "Discuss", use "Compare" or "Analyse"; or a different European theme — architecture, a design movement, a contemporary issue). Real 2023-2025 HL Section B question. Same demand/trap logic.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nLEVEL: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded Section B stem.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.stem ? { ...r.stem, _slot: s.key } : null),
))

const stems = authored.filter(Boolean)
log(`Authored ${stems.length} top-up stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'factsAccurate', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, factsAccurate: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Art Section B Command-Word stem against ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive token-run in stem? else fix.\n` +
    `2. GROUNDING: a real ${s.level} Section B question near ${s.questionRef}? marks (50) + scheme match? else grounded:false.\n` +
    `3. ART-FACT ACCURACY: any wrong art fact in stem/demand/trap? else factsAccurate:false.\n` +
    `4. QUALITY: demand specific (no filler)? trap a real scheme pattern (narration-not-analysis / no named work)?\n` +
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
