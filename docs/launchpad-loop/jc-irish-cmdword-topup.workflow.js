export const meta = {
  name: 'jc-irish-cmdword-topup',
  description: 'Targeted top-up of critic-identified gap slots in the JC Irish Command-Word set, then skeptic-verify each',
  phases: [
    { title: 'Author', detail: 'one agent per gap slot' },
    { title: 'Verify', detail: 'skeptic per stem' },
  ],
}

const TXT = '/tmp/jc_irish_txt'

const SHARED = `
You author ONE Command-Word Reflex stem for JUNIOR CYCLE IRISH (Gaeilge T2). The student sees a real exam question STEM
(in Irish, faithful to the paper), taps the COMMAND WORD, then learns what that cue demands and the marking trap.

EXAM SHAPE: HIGHER (270 marc): Roinn A Cluastuiscint 45 (Ceist 1-3). Roinn B 225: C4 Léamhthuiscint 65, C5 Litríocht
úrscéal/dráma 40, C6 Ceapadóireacht 50, C7 cloze 10, C8 gearrscéal 25, C9 Cruinneas 10, C10 dán/amhrán 25.
ORDINARY (270 marc): Roinn A Cluastuiscint 60 (Ceist 1-3). Roinn B 210: C4 fíor/bréagach 20, C5 teachtaireacht 20,
C6 fógra/póstaer reading 30, C7 composite reading+writing 80, C8 meaitseáil 25, C9 sraith pictiúr 35.

THE TYPE: { id (kebab, prefix 'jcir-'), subjectId: 'jc-irish', subjectLabel: 'Irish (Junior Cycle)',
level ('higher'|'ordinary'), questionRef ('2024 OL · Roinn B · Ceist 7'), stem (IRISH, faithful to the paper, fadas
correct, MUST contain commandWord verbatim), commandWord (the Irish cue actually printed on the paper), demand
(BILINGUAL register — English-led explanation quoting Irish terms; what THIS cue requires on THIS question, per the
scheme), trap (the scheme-flagged mistake + marks consequence; bilingual), source ('SEC JC Irish (Gaeilge T2) {YEAR}
{LEVEL} marking scheme, Ceist … ("…guidance…")'), marks (integer, per the scheme) }.

TAPPABILITY: commandWord must appear in stem as a CONSECUTIVE word-token run (strip non-letters incl. fadas-insensitive
normalisation happens app-side — just quote the cue exactly as it appears in your stem). Multi-word cues fine.

GROUNDING (non-negotiable): a REAL SEC question from ${TXT}/jc-irish-YYYY-{HL,OL}-{paper,marking-scheme}.txt (2022-2025).
grep/Read the paper for the exact wording + the scheme for the marking rule. Do NOT invent question numbers, marks, or
scheme wording. LEVEL PURITY: the stem's level MUST match the paper's level.

QUALITY: demand/trap specific to this cue+question; banned filler ('read the question', 'manage your time').
If your slot CANNOT be grounded (the cue/question genuinely does not occur 2022-2025), return found:false with a note
instead of forcing it. Return data only; edit no files.
`

const STEM_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
  level: { type: 'string', enum: ['higher', 'ordinary'] }, questionRef: { type: 'string' },
  stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
  trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
}
const ONE_SCHEMA = {
  type: 'object', required: ['found'],
  properties: { found: { type: 'boolean' }, note: { type: 'string' }, stem: { type: 'object', properties: STEM_PROPS } },
}

const SLOTS = [
  { key: 'ol-ceist7-composite', want: 'ORDINARY · OL Roinn B Ceist 7 (composite reading + writing, 80 marc — the biggest OL question; e.g. 2024 OL Taylor Swift/Dermot Kennedy). Use the cue actually printed (likely Freagair for the reading part or Scríobh for the writing part — pick the one with the richer scheme rule).' },
  { key: 'hl-cluastuiscint', want: 'HIGHER · Roinn A Cluastuiscint (45 marc; e.g. 2024 HL Ceist 1-3). Use the cue printed on the paper (e.g. Freagair na ceisteanna / Cuir tic / Líon isteach). Teach the listening-section move: questions printed in advance, answers in order, two plays + sos.' },
  { key: 'ol-cluastuiscint', want: 'ORDINARY · Roinn A Cluastuiscint (60 marc — the largest OL block; e.g. 2024 OL Ceist 1). Use the cue printed on the paper.' },
  { key: 'ol-ceist6-fogra', want: 'ORDINARY · OL Ceist 6 fógra/póstaer reading (30 marc; e.g. 2023 OL). Use the cue printed (likely Freagair/Luaigh/Cén-style instruction — choose the printed imperative).' },
  { key: 'inis-if-real', want: 'EITHER LEVEL · the cue "Inis" wherever it GENUINELY occurs on a 2022-2025 paper (grep all 8 papers for "Inis "). If it never occurs as an imperative cue, return found:false with the grep evidence in note — do NOT force it.' },
  { key: 'hl-minigh-comprehension', want: 'HIGHER · a Léamhthuiscint "Mínigh…" sub-part in HL Ceist 4 (2022-2025) — Mínigh in its comprehension sense (explain why, from the text), distinct from the existing score-justification Mínigh. If no Mínigh occurs in C4 in any year, return found:false with evidence.' },
  { key: 'hl-ceist9b', want: 'HIGHER · HL Ceist 9(b), the unsampled half of Cruinneas (2022-2025 — check what 9(b) actually asks, e.g. Athscríobh/Líon/Cuir). Use the printed cue and the scheme rule for it.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE stem for this slot (or found:false with evidence).`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).filter((r) => r.found && r.stem).map((r) => r.stem)
log(`Authored ${stems.length}/${SLOTS.length} gap stems (${authored.filter(Boolean).filter((r) => !r.found).length} unfounded slots)`)

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
    `Independent SKEPTIC verifying ONE JC Irish (Gaeilge T2) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem?\n` +
    `2. GROUNDING: real ${s.level} question at ${s.questionRef} (2022-2025)? marks + the marking rule in demand/trap match the scheme? Irish faithful (fadas)?\n` +
    `3. LEVEL PURITY: source paper actually ${s.level}?\n` +
    `4. QUALITY: demand/trap specific, bilingual register, no filler?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedStem (keep id). If sound, accept. If fabricated, reject.\n\nTHE STEM:\n${JSON.stringify(s, null, 2)}`,
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
const unfounded = authored.filter(Boolean).filter((r) => !r.found).map((r) => r.note || 'no note')
return { kept, keptCount: kept.length, unfounded }
