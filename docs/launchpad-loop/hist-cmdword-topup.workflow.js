export const meta = {
  name: 'hist-cmdword-topup',
  description: 'Fill History Command-Word gaps: Assess/Discuss/Outline cues, a Compare DBQ cue, USA topic, more OL',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + accuracy-checks each' },
  ],
}

const TXT = '/tmp/hist_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert HISTORY (Later Modern 1815-1993). The student taps the COMMAND
WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — history-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages
===PAGE n===). grep/Read for the exact stem + how the scheme awards it. Do NOT invent wording/marks/scheme content.
If you can't verify the stem AND the scheme, pick a different real question that fits the slot.

HISTORY MARKING GRAMMAR: essays marked by CUMULATIVE marks counting Significant Relevant Statements (HL up to 60 CM +
40 OE; OL Part C 30 CM + 10 OE). Two/three-element stems cap the CM if you miss an element ('NOTE: TWO elements... If
only ONE, Max CM = 50'). DBQ comparison ('Do both documents'/'Compare') needs cross-referencing both documents (single-
document answers capped, marked 2M+4M+4M). Judgement cues (Assess, Discuss, To what extent) demand an evaluation, rewarded
through the Overall Evaluation and relevance, not narration. 'Outline'/'Give an account of' = OL lower-order recall.

OUTPUT one object (schema's "stem"): id (kebab, 'hist-' prefix, cue+topic), subjectId='history', subjectLabel='History',
level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord verbatim), commandWord,
demand (answer-shaping move + scheme-rewarded approach), trap (scheme rule + marks consequence; quote the NOTE/award),
source ('LC History {YEAR} {LEVEL} marking scheme, Section …, Q… ("…")'), marks (int). No figure field (DBQs are text).

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify it yourself. Use the command word with the SAME casing as it appears in the stem.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','plan your answer','write neatly').
trap = a real scheme rule. Plain text, ASCII quotes. Return data only; never edit a file.
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
  { key: 'assess-judgement', level: 'higher',
    topic: 'An "Assess" essay cue (commandWord = "Assess"). Find a real HL essay question that begins "Assess ..." (e.g. assess the achievements/contribution/successes of a figure or movement). Teach that Assess demands a JUDGEMENT supported by evidence (rewarded via Overall Evaluation), not a narrative.' },
  { key: 'discuss-ol', level: 'ordinary',
    topic: 'A "Discuss" cue at OL if available, else HL (commandWord = "Discuss"). Find a real essay question using "Discuss". Teach that Discuss = present and develop several relevant points/arguments (cumulative SRS), staying on the exact question.' },
  { key: 'outline-give-account-ol', level: 'ordinary',
    topic: 'A lower-order OL cue: "Outline" or "Give an account of" (commandWord exactly as in the stem). Common at OL. Find a real OL question. Teach that it wants several accurate, relevant Core Statements describing the topic — breadth of distinct points, each developed enough to score.' },
  { key: 'usa-topic', level: 'ordinary',
    topic: 'A stem on "The United States and the world, 1945-1989" (Section 3) — e.g. civil rights, a US president, the Cold War, the Cuban Missile Crisis, the space race. Any real cue that appears in the stem (Why did / What were / How did / Discuss). Fills the USA-topic gap.' },
  { key: 'compare-or-extra-ol', level: 'ordinary',
    topic: 'EITHER a DBQ comparison cue using the word "Compare" if one exists in a real OL/HL DBQ ("Compare the views..."), OR a second real OL essay stem on a topic NOT already heavy in the set (avoid de Valera, Stalin, New Imperialism). Pick a high-frequency OL topic (e.g. the Treaty, Northern Ireland civil rights, Nazi Germany, the Cold War).' },
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
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE History Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? else fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme approach + trap's quoted rule match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any history error? cue meaning right (Assess/Discuss=judgement+develop; Outline=describe; Compare=cross-reference)?\n` +
    `4. QUALITY: demand specific (no filler)? trap a real scheme rule? no figure field?\n` +
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
