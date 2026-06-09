export const meta = {
  name: 'acc-catchup',
  description: 'Author + adversarially verify Accounting Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'topic clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each vs scheme' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/acc_txt'

const TOPICS = `
VALID accounting topicIds. topicId MUST be one; card strand = topicId minus its last -N.
accounting-0 Conceptual Framework: -0 Nature/Purpose, -1 Objectives of Financial Reporting, -2 Users, -3 Qualitative Characteristics, -4 Concepts/Bases/Policies, -5 Fundamental Concepts (SSAP 2), -6 Other Concepts/Conventions
accounting-1 Regulatory Framework (HL): -0 Nature/Objectives, -1 Regulatory Bodies, -2 Mechanism, -3 True and Fair View, -4 Role of the Auditor, -5 Monitoring
accounting-2 Accounting Records: -0 Double-Entry Bookkeeping, -1 Bank Reconciliation Statement, -2 Control Accounts, -3 Suspense Accounts
accounting-3 Sole Traders: -0 Nature, -1 Trading/P&L/Balance Sheet, -2 Gross Profit/Net Profit/Net Worth
accounting-4 Company Accounting: -0 Share Capital/Reserves/Loans, -1 Financial Statements of Companies, -2 Annual Reports of PLCs (HL)
accounting-5 Specialised Accounts: -0 Manufacturing, -1 Stock, -2 Club and Service Firm, -3 Departmental, -4 Farm
accounting-6 Incomplete Records: -0 Why they arise, -1 Final Accounts via Control Accounts, -2 Profit via Net Worth, -3 Profit via Mark-Up and Margin (HL)
accounting-7 Cash Flow Statements: -0 Importance, -1 Profit vs Cash, -2 Cash v Non-Cash Items, -3 Sources of Inflows/Outflows, -4 Working Capital and Cash Flows, -5 Preparing Cash Flow Statements
accounting-8 Analysis of Financial Statements: -0 Objective, -1 Accounting Ratios, -2 Users/Interests, -3 Limitations, -4 Profitability/Efficiency, -5 Working Capital, -6 Liquidity/Solvency, -7 Gearing, -8 Investment, -9 Interpreting, -10 Presentation (HL)
accounting-9 Management Accounting: -0 Nature/Scope, -1 Cost Classifications, -2 Product Costing, -3 Cost-Volume-Profit (break-even), -4 Budgetary Planning/Control, -5 Flexible Budgeting (HL)
accounting-10 IT in Accounting: -0 Importance, -1 Spreadsheets
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert ACCOUNTING (Irish exam-recovery tool). A card teaches a student
who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a check question + model answer.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Accounting questions + marking schemes. Text of all papers +
schemes (2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): accounting-YYYY-{HL,OL}-{paper,marking-scheme}.txt.
grep/Read for the exact question + scheme workings. Do NOT invent question numbers, marks, scheme wording, or figures.
RECOMPUTE every calculation (a ratio, an adjustment, a control-account balance, a break-even, a net-worth profit, a cash
flow) and confirm it matches the scheme. Accounting answers are PRECISE — get the formula, the euro figure, and the
treatment (debit/credit, P&L vs balance sheet) exactly right.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'acc-', unique, includes the topic (e.g. 'acc-current-ratio-acid-test-hl')
  subjectId     MUST be exactly 'accounting'
  topicId       one of the valid ids above
  subjectLabel  'Accounting'
  topicLabel    short human label
  focus         short row label disambiguating same-subtopic cards (e.g. 'Acid-test ratio: exclude closing stock')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core technique/concept + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks
  check         { prompt (self-contained — embed all figures/data inline as a small table or list), modelAnswer (full
                  worked answer with the calculation), needed (>=2 award-point strings) }
  source        'Topic … — SEC LC Accounting {YEAR} {LEVEL}, Q… + marking scheme (…the scheme answer…)'
  marksWeight   integer marks at stake (from the scheme)
  figureSpec    OPTIONAL and RARE — only if the check genuinely needs a visual the exam SHOWS (e.g. a break-even CHART to
                read). Almost all accounting data is tabular — EMBED it inline in the prompt instead. Shape
                { year, level, questionRef, describes, whyNeeded }. DO NOT add a 'figure'/'src' field.

SELF-CONTAINMENT (hard rule): the check prompt must be answerable from the card itself. Embed every figure/balance/data
item the student needs directly in the prompt (a short inline table or bullet list). Never reference an unseen ledger,
trial balance, or appendix the student cannot see.

QUALITY BAR: oneMove must name a SPECIFIC accounting move/error (e.g. 'the acid-test ratio EXCLUDES closing stock from
current assets', 'an accrued expense is ADDED to the expense in the P&L and shown as a current liability', 'in the bank
rec start from the adjusted/corrected cash-book balance', 'break-even units = fixed costs / contribution per unit', 'in
the net-worth method, profit = closing capital - opening capital + drawings - capital introduced'). BANNED filler: 'show
your working' (it IS accounting — be specific about WHAT working), 'read the question', 'manage your time'. Plain text;
€ and unicode fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const CARD_SCHEMA = {
  type: 'object', required: ['cards'],
  properties: {
    cards: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'subjectId', 'topicId', 'subjectLabel', 'topicLabel', 'focus', 'level', 'gist', 'oneMove', 'check', 'source', 'marksWeight'],
        properties: {
          id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
          subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
          level: { type: 'string', enum: ['higher', 'ordinary'] }, gist: { type: 'string' },
          oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
          check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
          source: { type: 'string' }, marksWeight: { type: 'integer' },
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'records-framework', strands: 'accounting-2 (Records), accounting-0 (Conceptual Framework), accounting-1 (Regulatory, HL)',
    topics: 'double-entry, bank reconciliation statement (start from adjusted cash book), control accounts (debtors/creditors control), suspense accounts & correction of errors; conceptual framework — qualitative characteristics, the going-concern/accruals/prudence/matching concepts, users of accounts; regulatory framework & the auditor (HL theory)' },
  { key: 'final-accounts', strands: 'accounting-3 (Sole Traders), accounting-4 (Company Accounting)',
    topics: 'trading/profit-and-loss account and balance sheet, the ADJUSTMENTS (accruals, prepayments, depreciation, bad debts/provision, closing stock), gross profit & net profit, company final statements, share capital/reserves' },
  { key: 'specialised-incomplete-cashflow', strands: 'accounting-5 (Specialised), accounting-6 (Incomplete Records), accounting-7 (Cash Flow)',
    topics: 'club/service-firm accounts (accumulated fund, subscriptions, bar trading account), manufacturing accounts (prime cost, factory cost), incomplete records (profit via net-worth method, profit via mark-up/margin HL, final accounts via control accounts), cash flow statements (profit vs cash, operating activities)' },
  { key: 'analysis-management', strands: 'accounting-8 (Ratios/Analysis), accounting-9 (Management Accounting)',
    topics: 'accounting ratios — gross/net margin, return on capital employed, current ratio, acid-test (quick) ratio (exclude stock), gearing, dividend cover, return on investment, stock turnover, debtors period — calculate AND interpret; management accounting — cost classification, cost-volume-profit/break-even (units = fixed costs / contribution per unit), margin of safety, budgeting' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 5 recovery cards: aim for ~3 Higher + ~2 Ordinary, spread across DIFFERENT subtopics and years. Favour high-frequency, high-mark questions; include calculation cards (ratios, adjustments, break-even, net-worth) AND a couple of theory/short-answer cards. Read the relevant ${TXT}/ files; recompute every calculation and confirm it matches the scheme. Embed all data inline in each prompt.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'mathChecks', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `You are an independent SKEPTIC verifying ONE Accounting Catch-Up recovery card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question matching "${c.source}"? Do marks + the scheme's modelled answer + workings match the scheme text? else grounded:false.\n` +
    `2. MATHS: RECOMPUTE every number (ratio formula + value, adjustment, control-account balance, break-even, net-worth profit, cash flow). Matches the scheme (formula, euro figure, units, debit/credit, P&L vs balance-sheet treatment)? else mathChecks:false.\n` +
    `3. ACCOUNTING ACCURACY: any error in the rule/treatment (e.g. acid-test wrongly includes stock; accrual on wrong side; wrong ratio formula; net-worth profit sign)?\n` +
    `4. SELF-CONTAINMENT: are all figures/data embedded in the prompt so it is answerable without an unseen trial balance/ledger? else selfContained:false.\n` +
    `5. QUALITY: oneMove specific (not banned filler)? needed[] real award points? topicId valid?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id; embed any missing data). If sound, accept. If fabricated/unsalvageable, reject.\n\n` +
    `THE CARD:\n${JSON.stringify(c, null, 2)}`,
    { label: `verify:${c.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ card: c, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.card)
  else if (r.v.verdict === 'fix' && r.v.fixedCard) kept.push({ ...r.card, ...r.v.fixedCard })
}
log(`Verify: ${kept.length}/${cards.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for an Accounting Catch-Up Lane recovery-card set (Irish LC). The ${kept.length} kept cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, marks: k.marksWeight })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) coverage across the high-frequency exam areas (final accounts/adjustments, ratios, ` +
  `control accounts, bank rec, incomplete records, club accounts, cash flow, break-even/CVP, conceptual framework theory), ` +
  `(3) calculation vs theory mix, (4) any major exam topic with no card. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
