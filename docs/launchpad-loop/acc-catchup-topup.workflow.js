export const meta = {
  name: 'acc-catchup-topup',
  description: 'Fill Accounting Catch-Up gaps: company final accounts, club I&E, depreciation, bad-debts provision, concepts theory, a profitability ratio',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each' },
  ],
}

const TXT = '/tmp/acc_txt'

const VALID = `Valid accounting topicIds: accounting-0-* (Conceptual Framework: -2 Users, -3 Qualitative Characteristics, -5 Fundamental Concepts SSAP2, -6 Other Concepts),
accounting-3-* (Sole Traders: -1 Trading/P&L/Balance Sheet), accounting-4-* (Company: -0 Share Capital, -1 Financial Statements of Companies),
accounting-5-* (Specialised: -0 Manufacturing, -2 Club/Service Firm), accounting-8-* (Analysis: -4 Profitability/Efficiency, -5 Working Capital, -6 Liquidity, -7 Gearing, -8 Investment).
Card strand = topicId minus last -N.`

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for Leaving Cert ACCOUNTING. A card teaches a student who lost marks how to
recover them: clear gist, the ONE highest-leverage move, a check question + full worked model answer.

GROUNDING: ground in a REAL SEC LC Accounting question + scheme at ${TXT}/ (pages ===PAGE n===):
accounting-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact question + scheme workings. Do NOT invent
question numbers/marks/wording. RECOMPUTE every calculation and confirm it matches the scheme. Get formula, euro figure,
debit/credit side and P&L-vs-balance-sheet treatment exactly right.

${VALID}

CARD FIELDS: id (kebab, 'acc-' prefix, includes topic), subjectId='accounting', topicId (valid id), subjectLabel='Accounting',
topicLabel (short), focus (short row label), level ('higher'|'ordinary'), gist (2-5 sentences),
oneMove {label, text} (specific accounting move/error — not filler),
check {prompt (self-contained — EMBED all figures/trial-balance/adjustments inline as a compact list/table), modelAnswer (full worked), needed (>=2 award-point strings)},
source ('Topic … — SEC LC Accounting {YEAR} {LEVEL}, Q… + marking scheme (…)'), marksWeight (int).
For a big question (company final accounts), you may CONDENSE the trial balance to the key lines + the adjustment bundle so it
fits one card, but it must remain a faithful, internally-consistent worked example whose figures reconcile.

QUALITY: oneMove names a specific move/error. BANNED filler: 'show your working','read the question','manage your time'.
Plain text; € and unicode fine. No figureSpec/figure (accounting data is tabular — embed inline). Return data only; never edit a file.
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
      },
    },
  },
}

const SLOTS = [
  { key: 'company-final-accounts', level: 'higher',
    topic: 'The COMPANY FINAL ACCOUNTS anchor (accounting-4-1) — the flagship high-mark question, currently missing. A condensed but faithful worked example: from key trial-balance lines + the standard adjustment bundle (depreciation, debenture/loan interest due, provision for bad debts, taxation, closing stock), prepare the trading & profit-and-loss + appropriation account to net profit, and the key balance-sheet figures. Teach the order and where each adjustment lands. Embed the data compactly inline.' },
  { key: 'club-income-expenditure', level: 'ordinary',
    topic: 'CLUB Income & Expenditure account + subscriptions + Accumulated Fund (accounting-5-2). The classic club question: treat subscriptions in advance vs in arrears correctly, compute the accumulated fund (opening capital), and build the I&E account. Embed the figures inline.' },
  { key: 'depreciation-charge', level: 'ordinary',
    topic: 'DEPRECIATION charge as an adjustment (accounting-3-1) — straight-line vs reducing-balance: compute the annual charge, show it as an expense in the P&L AND as accumulated depreciation reducing the asset to net book value in the balance sheet. Currently only disposal is covered. Embed the figures inline.' },
  { key: 'provision-bad-debts', level: 'higher',
    topic: 'PROVISION FOR BAD/DOUBTFUL DEBTS adjustment (accounting-3-1) — create/increase/decrease the provision: the INCREASE goes as an expense in the P&L (a decrease is a gain), and the provision is deducted from debtors in the balance sheet. Distinguish bad debts written off from the provision. Embed the figures inline.' },
  { key: 'concepts-theory', level: 'higher',
    topic: 'A THEORY card on accounting CONCEPTS / qualitative characteristics / users (accounting-0-3, -5 or -2) — the set is calculation-heavy. A real short-theory question: explain a fundamental concept (going concern, accruals, prudence, consistency, materiality) OR the qualitative characteristics OR the users of accounting information and their interests. Ground in a real scheme.' },
  { key: 'profitability-working-capital-ratio', level: 'higher',
    topic: 'A PROFITABILITY / WORKING-CAPITAL RATIO card (accounting-8-4 or -5) NOT already covered (avoid acid-test, gearing, dividend cover): e.g. return on capital employed (ROCE), net/gross margin, stock turnover (rate of stock turnover), period of credit given to debtors / taken from creditors. Calculate AND interpret. Embed the figures inline.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nPREFERRED level: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded card for this slot.`,
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
    `Independent SKEPTIC verifying ONE Accounting Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question matching "${c.source}"? marks + scheme workings/treatment match? else grounded:false.\n` +
    `2. MATHS: RECOMPUTE every number (the final-accounts adjustments + net profit, the ratio formula+value, depreciation charge, provision movement, accumulated fund). Internally consistent and matching the scheme? else mathChecks:false.\n` +
    `3. ACCOUNTING ACCURACY: correct treatment (adjustment side, P&L vs balance sheet, provision increase=expense, subs advance/arrears direction, ROCE formula)?\n` +
    `4. SELF-CONTAINMENT: all figures embedded so it is answerable without an unseen trial balance? else selfContained:false.\n` +
    `5. QUALITY: oneMove specific (no filler)? needed[] real award points? topicId valid?\n` +
    `If fixable, verdict:fix with a complete corrected card in fixedCard (keep id; embed any missing data). If sound, accept. If fabricated, reject.\n\n` +
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
