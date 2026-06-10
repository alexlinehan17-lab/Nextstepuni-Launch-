export const meta = {
  name: 'jc-history-cmdword-topup',
  description: 'Targeted top-up of critic-identified cue/strand gaps (Give/count, Account for, cartoon, source-evaluation, 20th-century Europe) in the JC History Command-Word set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic per stem' } ],
}

const TXT = '/tmp/jc_history_txt'

const SHARED = `
You author ONE Command-Word Reflex stem for JUNIOR CYCLE HISTORY (reformed NCCA spec, first examined 2019). COMMON LEVEL
only — every stem level MUST be 'common'. Single terminal paper, 360 marks, 8 questions, source/cartoon/photo heavy. The
student taps the COMMAND WORD then learns the demand + the marking trap.

CUE GRAMMAR: Name/State/Give/Identify/List/Mention = exact named answer(s); count cues ("two reasons") need that many.
Describe/Outline/Write an account of = what happened in detail. Explain/Account for/Give a reason = the cause/reason.
Define / What is meant by = the precise meaning of a term. Distinguish between = the contrast on the SAME feature for both.
Using the source/document = answer FROM the supplied source (quote/refer). Using the cartoon = name the symbol + what it
stands for + the cartoonist's attitude/message. Source-evaluation = judge usefulness/reliability AND give a limitation/
reason. Do you think/agree = a view WITH supporting evidence.

THE TYPE: { id (kebab, prefix 'jchist-'), subjectId:'jc-history', subjectLabel:'History (Junior Cycle)', level:'common',
questionRef ('2024 CL · Q7(d)'), stem (faithful to the paper; MUST contain commandWord verbatim; describe any source/
cartoon in words), commandWord, demand (what THIS cue requires here), trap (the scheme-flagged mistake + marks
consequence), source ('SEC JC History {YEAR} CL marking scheme, Q… (…accepted answers…)'), marks (integer) }.

TAPPABILITY: commandWord is a consecutive word-token run in stem (multi-word cue = exact run).
GROUNDING (non-negotiable): a REAL SEC question from ${TXT}/jc-history-YYYY-CL-{paper,marking-scheme}.txt (2022-2025).
grep/Read the paper + scheme. Do NOT invent question numbers, marks, or scheme wording. Stay within JC scope. If your slot
CANNOT be grounded (the cue/topic genuinely does not occur 2022-2025), return found:false with grep evidence. Return data only.
`

const STEM_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
  level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
  stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
  trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
}
const ONE_SCHEMA = { type: 'object', required: ['found'], properties: { found: { type: 'boolean' }, note: { type: 'string' }, stem: { type: 'object', properties: STEM_PROPS } } }

const SLOTS = [
  { key: 'give-or-list-count', want: `cue 'Give' (or 'List' / 'Name two ...') with an explicit COUNT — "Give two reasons ...", "Name two features of ...", "List two effects of ...". Demand: that many distinct correct points. Trap: giving fewer than asked (count-short) loses the per-point marks.` },
  { key: 'account-for', want: `cue 'Account for' — "Account for ..." a development (the rise of a dictator, why an event happened). Demand: the cause(s)/reason. Trap: describing the event instead of accounting for WHY it happened.` },
  { key: 'using-the-cartoon', want: `cue 'Using the cartoon' (or "Look at the cartoon ...") — a political CARTOON-reading question (e.g. 2025 Q7 cartoon). Demand: name a symbol + what it represents + the cartoonist's attitude/message. Trap: describing what the cartoon literally shows without decoding the symbols or the message.` },
  { key: 'source-evaluation', want: `a SOURCE-EVALUATION cue — "How useful / How reliable is this source ...?" or "Give one reason this source might be biased/limited". Demand: a judgement of usefulness/reliability WITH a limitation/reason. Trap: giving usefulness with no limitation, or reliability with no reason.` },
  { key: 'identify-or-name-20thC-europe', want: `cue 'Name' / 'Identify' / 'State' on a 20th-CENTURY EUROPE/WIDER-WORLD content topic that is UNDER-represented — World War One or Two, life in Nazi Germany / Stalin's USSR (dictatorship), the Holocaust, or the Cold War. Demand: the exact named person/event/feature. Trap: a vague description where a named answer is needed.` },
  { key: 'explain-20thC-europe', want: `cue 'Explain' / 'Describe' on a 20th-CENTURY EUROPE/WIDER-WORLD content topic (WWI/WWII causes or course, a feature of life under a dictatorship, the Holocaust, the Cold War). Demand: the developed reason/account. Trap: an undeveloped one-liner.` },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nYOUR GAP SLOT: ${s.key}\n${s.want}\n\nProduce exactly ONE stem (level 'common') for this slot (or found:false with evidence).`,
    { label: `author:${s.key}`, phase: 'Author', schema: ONE_SCHEMA },
  ),
))
const stems = authored.filter(Boolean).filter((r) => r.found && r.stem).map((r) => r.stem)
log(`Authored ${stems.length}/${SLOTS.length} gap stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: STEM_PROPS },
  },
}
const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE JC History (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem?\n` +
    `2. GROUNDING: real question at ${s.questionRef} (2022-2025 CL)? marks + marking rule match the scheme?\n` +
    `3. HISTORY SENSE + SCOPE: historically correct, within JC scope, right cue, level exactly 'common'?\n` +
    `4. QUALITY: demand/trap specific, real marking pattern?\n` +
    `If fixable, verdict:fix WITH complete corrected fixedStem (keep id, level 'common'). If sound, accept. If fabricated, reject.\n\nTHE STEM:\n${JSON.stringify(s, null, 2)}`,
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
return { kept, keptCount: kept.length, unfounded: authored.filter(Boolean).filter((r) => !r.found).map((r) => r.note || 'no note') }
