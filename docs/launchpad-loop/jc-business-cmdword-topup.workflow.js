export const meta = {
  name: 'jc-business-cmdword-topup',
  description: 'Targeted top-up of critic-identified cue gaps (Define, What is meant by, Distinguish, Suggest) in the JC Business Studies Command-Word set, then skeptic-verify',
  phases: [ { title: 'Author', detail: 'one agent per gap slot' }, { title: 'Verify', detail: 'skeptic per stem' } ],
}

const TXT = '/tmp/jc_business_txt'

const SHARED = `
You author ONE Command-Word Reflex stem for JUNIOR CYCLE BUSINESS STUDIES (reformed NCCA spec, first examined 2019).
COMMON LEVEL only — every stem level MUST be 'common'. Single terminal paper, 270 marks, Section A short Qs + Section B
applied Qs. The student taps the COMMAND WORD then learns the demand + the marking trap.

CUE GRAMMAR: State/Name/Give/List/Identify = exact named term(s); count cues need that many. Define / What is meant by =
the precise meaning of the term (often define + brief example earns both marks). Explain/Outline/Describe = a DEVELOPED
point (what + consequence). Distinguish between / Compare = the contrast on the SAME feature for BOTH items. Suggest /
Recommend / Advise = a justified choice/idea WITH a business reason. Calculate/Complete/Balance/Post = the numeric/
accounting task with correct figures/entries.

THE TYPE: { id (kebab, prefix 'jcbus-'), subjectId:'jc-business-studies', subjectLabel:'Business Studies (Junior Cycle)',
level:'common', questionRef ('2024 CL · Section A · Q14'), stem (faithful to the paper; MUST contain commandWord verbatim;
describe any figure in words), commandWord, demand (what THIS cue requires here), trap (the scheme-flagged mistake + marks
consequence), source ('SEC JC Business Studies {YEAR} CL marking scheme, Q… (…accepted answers…)'), marks (integer) }.

TAPPABILITY: commandWord is a consecutive word-token run in stem (multi-word cue = exact run).
SCOPE (hard): JC only — NO Leaving-Cert accounting (no break-even chart, no ROCE/acid-test ratios, no depreciation-method
comparison, no control accounts).
GROUNDING (non-negotiable): a REAL SEC question from ${TXT}/jc-business-studies-YYYY-CL-{paper,marking-scheme}.txt
(2022-2025). grep/Read the paper + scheme. Do NOT invent question numbers, marks, or scheme wording. If your slot CANNOT
be grounded (the cue genuinely does not occur 2022-2025), return found:false with grep evidence. Return data only.
`

const STEM_PROPS = {
  id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
  level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
  stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
  trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
}
const ONE_SCHEMA = { type: 'object', required: ['found'], properties: { found: { type: 'boolean' }, note: { type: 'string' }, stem: { type: 'object', properties: STEM_PROPS } } }

const SLOTS = [
  { key: 'define', want: `cue 'Define' — "Define the term ..." on an Our-economy or Personal-finance term (e.g. opportunity cost, inflation, scarcity, a tax term). Demand: the precise meaning (define + brief example earns both marks). Trap: giving an example with no actual definition.` },
  { key: 'what-is-meant-by', want: `cue 'What is meant by' — "What is meant by ...?" on a Personal-finance / Enterprise term (e.g. gross pay, net pay, a credit note, target market, globalisation). Demand: the precise meaning. Trap: a vague gesture rather than the defined meaning.` },
  { key: 'distinguish', want: `cue 'Distinguish between' (or 'Compare') — "Distinguish between ... and ..." on a real contrast (e.g. fixed vs variable / current vs capital expenditure, a debit and a credit, field vs desk research, sole trader vs partnership, direct vs indirect tax). Demand: the contrast on the SAME feature for BOTH items. Trap: describing only one side, or two non-contrasting facts.` },
  { key: 'suggest', want: `cue 'Suggest' — "Suggest one way ..." on Enterprise (e.g. a way a business could reduce costs / promote a product / be more sustainable). Demand: a plausible idea WITH a brief business reason. Trap: a bare idea with no justification (the lower-stakes sibling of Recommend).` },
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
    `Independent SKEPTIC verifying ONE JC Business Studies (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem?\n` +
    `2. GROUNDING: real question at ${s.questionRef} (2022-2025 CL)? marks + marking rule match the scheme?\n` +
    `3. BUSINESS SENSE + SCOPE: correct, within JC scope (no LC-only accounting), right cue, level exactly 'common'?\n` +
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
