export const meta = {
  name: 'acc-cmdword-topup',
  description: 'Fill Accounting Command-Word gaps: OL ratio Calculate, OL Distinguish, OL Advise/Comment, HL clubs/revaluation Prepare, HL costing concept',
  phases: [
    { title: 'Author', detail: 'one targeted stem per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each' },
  ],
}

const TXT = '/tmp/acc_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert ACCOUNTING. The student taps the COMMAND WORD in a real exam
stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use real SEC text at ${TXT}/ — accounting-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages
===PAGE n===). grep/Read for the exact stem + scheme award points. Do NOT invent question numbers/marks/wording. If you
can't verify the stem AND the scheme, pick a different real question that fits the slot. RECOMPUTE any number and confirm
it matches the scheme (a ratio, a control-account balance, a break-even/margin figure, an adjustment).

ACCOUNTING MARKING GRAMMAR (write precise demands + traps):
 - 'Calculate' a ratio = state the FORMULA, put the right figures in, answer in the correct UNIT (times, %, days, €) —
   the scheme penalises a missing unit or a forgotten/wrong formula even if arithmetic is right.
 - 'Distinguish between' = contrast BOTH terms on the SAME dimension in one breath, not two separate definitions.
 - 'Comment on'/'Advise'/'Assess' = INTERPRET the figures (trend, vs prior year / industry / a risk-free return), give a
   reasoned recommendation — restating the number scores nothing.
 - 'Prepare'/'Show' a statement = correct FORMAT + each figure on the correct side + workings shown; prose does not earn it.
 - 'Explain'/'Outline' theory = reason/mechanism with development; a named-only answer is capped.

OUTPUT one object (schema's "stem"): id (kebab, 'acc-' prefix, cue+topic), subjectId='accounting', subjectLabel='Accounting',
level ('higher'|'ordinary'), questionRef, stem (faithful; MUST contain commandWord verbatim, casing as in the stem),
commandWord, demand (answer-shaping move + scheme-rewarded thing), trap (scheme rule + marks consequence; quote/point to
the award), source ('LC Accounting {YEAR} {LEVEL} marking scheme, Q… ("…")'), marks (int). No figure field — accounting
data is tabular.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify it yourself.

QUALITY: demand specific (BANNED filler: 'read the question','manage your time','show your working' [say WHICH working],
'plan your answer'). trap = a real scheme rule. Plain text; € and unicode fine. Return data only; never edit a file.
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
  { key: 'ol-calculate-ratio', level: 'ordinary',
    topic: 'An OL "Calculate" stem for a profitability or liquidity RATIO (current ratio, acid-test/quick ratio, return on capital employed, gross/net profit percentage, or stock turnover) — OL Calculate is currently records-only, no ratio. Embed the needed figures inline in the stem. Demand: the formula + figures + correct UNIT (times / % / €). Recompute and match the scheme.' },
  { key: 'ol-distinguish', level: 'ordinary',
    topic: 'An OL "Distinguish between" stem (commandWord = "Distinguish between") for a real OL term-pair — e.g. capital vs revenue expenditure, fixed vs current assets, debtors vs creditors, gross profit vs net profit, a debenture vs a share. Currently Distinguish is HL-only. Teach contrasting both terms on the SAME dimension.' },
  { key: 'ol-interpretation', level: 'ordinary',
    topic: 'An OL "Comment on" or "Advise"/"State your opinion" stem asking for applied judgement for a shareholder/investor/member based on ratios or figures (e.g. would you invest, is the liquidity/profitability satisfactory, compare to a risk-free return). OL has only one interpretation stem. Demand: interpret the figure + give a reasoned recommendation, not restate the number.' },
  { key: 'hl-prepare-clubs-or-revaluation', level: 'higher',
    topic: 'An HL "Prepare" stem OUTSIDE the Final-Accounts/Cash-Flow cluster — a Club/Service-firm statement (Accumulated Fund, Income & Expenditure account, Bar Trading account) OR a revaluation of fixed assets, OR a departmental/farm account. All current Prepare stems are sole-trader/company/cash-flow. Demand: correct format + figures on the correct side + workings.' },
  { key: 'hl-costing-concept', level: 'higher',
    topic: 'An HL "Explain" or "Outline" stem for a SECOND costing/budgeting concept beyond margin of safety — contribution per unit, the break-even point, fixed vs variable cost behaviour, the purpose/benefits of a cash budget, or flexible budgeting. HL costing theory currently rests on one margin-of-safety stem. Demand: the reason/mechanism with development.' },
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
    `Independent SKEPTIC verifying ONE Accounting Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? else fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme thing + trap's quoted award match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any accounting error (wrong formula, wrong unit on a ratio, wrong debit/credit side, recomputable number that does not check out, wrong treatment)?\n` +
    `4. QUALITY: demand specific (no filler)? trap a real scheme rule?\n` +
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
