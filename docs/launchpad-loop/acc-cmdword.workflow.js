export const meta = {
  name: 'acc-cmdword',
  description: 'Author + adversarially verify Accounting Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand/cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes each vs scheme' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/acc_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert ACCOUNTING (Irish exam-technique tool). The student sees a real
exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue demands and the
marking-scheme trap behind it.

GROUNDING (non-negotiable): every stem is a REAL SEC LC Accounting question. Text of all papers + schemes (2021-2025,
HL+OL) at ${TXT}/ (pages ===PAGE n===): accounting-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact stem
+ scheme award points. Do NOT invent question numbers, marks, or scheme wording. RECOMPUTE any number you cite (a ratio,
a control-account balance, a net-worth profit, a break-even, an adjustment) and confirm it matches the scheme.

ACCOUNTING MARKING GRAMMAR (use it to write precise demands + traps):
 - 'Prepare'/'Show' a statement (final accounts, control account, bank rec, cash flow, club accounts) = a FORMATTED answer
   where the scheme awards marks per correct line/figure on the correct side; workings shown earn workings marks and an
   omitted/wrong-side figure forfeits that line. The cue demands the right format + each item in the right place, NOT prose.
 - 'Calculate' a ratio = state the FORMULA, put the right figures in, and give the answer in the correct UNIT (times, %,
   days/months, €) — the scheme penalises a missing unit or a wrong/forgotten formula even if arithmetic is right.
 - 'Comment on'/'Assess'/'Advise'/'Evaluate' = INTERPRET the figures (trend, comparison vs prior year / industry / the
   12% return on a risk-free alternative), give a reasoned recommendation — restating the number scores nothing.
 - 'Explain'/'Outline' theory = give the reason/mechanism with development; a one-word/named-only answer is capped.
 - 'State'/'Name'/'List'/'Define' = the exact term/definition only — no over-writing needed, but it must be the precise term.
 - 'Distinguish between' = contrast BOTH terms on the SAME dimension in one breath (not two separate descriptions).

THE TYPE (one object per stem):
  id            kebab, prefix 'acc-', unique, includes cue + topic (e.g. 'acc-calculate-acid-test-ratio-hl')
  subjectId     MUST be exactly 'accounting'
  subjectLabel  'Accounting'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2023 HL · Q5(a)' or '2024 OL · Q9(b)'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim. If the question shows data the
                cue acts on, summarise just enough inline that the cue makes sense — but keep it a STEM, not the full dataset.
  commandWord   the cue (or multi-word cue like 'Distinguish between', 'Comment on', 'State two')
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence. Quote/point to the scheme where it bites
                (the unit required, the workings mark, the correct side, 'name AND explain', the interpretation vs restating).
  source        'LC Accounting {YEAR} {LEVEL} marking scheme, Q… ("…award point / scheme answer…")'
  marks         integer marks at stake (from the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem (e.g. 'Distinguish between' needs both words consecutive in the stem; use the
casing exactly as it appears in the stem).

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question carefully','manage your time','show your
working' [it IS accounting — say WHICH working],'plan your answer'). trap = a real scheme-grounded rule. Prefer cue
DIVERSITY: Prepare, Show, Calculate, Explain, Outline, State, Define, Name, Distinguish between, Comment on, Advise,
Identify, Indicate. Plain text, ASCII fine; € and unicode fine. Accounting questions are nearly all TEXT/tabular — do NOT
add a figure field.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: {
      type: 'array',
      items: {
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
  },
}

const CLUSTERS = [
  { key: 'records-and-theory', cues: 'Explain, Outline, State, Define, Distinguish between',
    topics: 'Accounting Records — double-entry, bank reconciliation statement, control accounts (debtors/creditors), suspense accounts & correction of errors; Conceptual Framework theory — qualitative characteristics, going-concern/accruals/prudence/matching/materiality concepts, users of financial statements; Regulatory Framework & the role of the auditor (HL theory). Favour the theory/short-answer cues here.' },
  { key: 'final-accounts', cues: 'Prepare, Show, Calculate, Explain, State',
    topics: 'Sole Trader & Company final accounts — Trading and Profit & Loss Account, Balance Sheet, the ADJUSTMENTS (accruals, prepayments, depreciation, bad debts/provision for bad debts, closing stock), gross profit / net profit / net worth, share capital / reserves / debentures. The Prepare/Show cues demand correct format + workings.' },
  { key: 'specialised-incomplete-cashflow', cues: 'Prepare, Calculate, Show, Explain, Outline',
    topics: 'Specialised Accounts — Manufacturing Account (prime cost, factory overhead), Club/Service-firm accounts (accumulated fund, bar trading, subscriptions), Departmental, Farm; Incomplete Records — final accounts via control accounts, profit via the Net-Worth method (profit = closing capital - opening capital + drawings - capital introduced), profit via Mark-up/Margin (HL); Cash Flow Statements — operating/investing/financing, profit vs cash, working-capital movements.' },
  { key: 'ratios-and-management', cues: 'Calculate, Comment on, Advise, Explain, Assess',
    topics: 'Analysis of Financial Statements — profitability ratios (gross/net margin, return on capital employed), liquidity (current ratio, acid-test), efficiency (stock turnover, debtors/creditors days), gearing, investment (dividend per share, dividend cover, earnings, the investor decision vs a risk-free %), limitations of ratio analysis; Management Accounting — cost classification, Cost-Volume-Profit / break-even (units = fixed costs / contribution per unit), budgeting / cash budgets, flexible budgeting (HL). Calculate cues demand formula+figures+UNIT; Comment/Advise cues demand interpretation + a reasoned recommendation.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, each with a DIFFERENT command word where possible, spread across years 2021-2025. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation. Make the demand and trap specific to the exact question you cite.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

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
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme-rewarded thing + trap's quoted award point match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any accounting error (wrong formula, wrong unit on a ratio, wrong debit/credit side, wrong net-worth/break-even/control-account figure, wrong treatment P&L vs balance sheet, a recomputable number that does not check out)?\n` +
    `4. QUALITY: demand specific to cue+question (no banned filler)? trap a real scheme pattern, not generic?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated, reject.\n\n` +
    `THE STEM:\n${JSON.stringify(s, null, 2)}`,
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

phase('Critic')
const critic = await agent(
  `Completeness critic for an Accounting Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (need both, ideally ~60/40), (2) command-word diversity (flag if one cue dominates — Prepare/Calculate can crowd out the theory cues), (3) topic spread across the strands (Records/Theory, Final Accounts, Specialised/Incomplete/Cash Flow, Ratios/Management), (4) whether BOTH a Prepare-a-statement cue AND interpretation cues (Comment/Advise) are present, since both are core to accounting marking. List concrete gaps as a short bullet list of slots to top up (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
