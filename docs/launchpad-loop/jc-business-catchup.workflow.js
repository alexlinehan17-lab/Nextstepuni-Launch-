export const meta = {
  name: 'jc-business-catchup',
  description: 'Author + adversarially verify Junior Cycle Business Studies (Common Level) Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, business/accounting correctness' },
    { title: 'Critic', detail: 'completeness + strand balance' },
  ],
}

const TXT = '/tmp/jc_business_txt'

const TOPICS = `
VALID jc-business-studies topicIds (the VERIFIED taxonomy — 3 strands, all examinable). topicId MUST be one; topicLabel the EXACT name.
Personal finance (jc-business-studies-0): -0 Managing money: income, expenditure, needs & wants, -1 Household budgeting &
  your financial position, -2 The financial lifecycle: needs at different life stages, -3 Saving & borrowing: sources,
  costs, interest & risk, -4 Insurance: cover for personal needs, premiums & claims, -5 Personal taxes & charges (PAYE,
  USC, PRSI, DIRT), -6 Wage slips & calculating your take-home pay, -7 Being an informed consumer: rights &
  responsibilities, -8 Consumer agencies, banks & financial institutions, -9 Ethical & sustainable consumer choices,
  -10 How globalisation & technology shape consumer choice
Enterprise (jc-business-studies-1): -0 Types of enterprise: financial, cultural & social, -1 Being enterprising & the role
  of the entrepreneur, -2 Forms of business ownership & how a business is set up, -3 Work, employment & volunteerism,
  -4 Rights & responsibilities of employers and employees, -5 A business and its community: impact & responsibility (CSR),
  -6 Digital technologies in business: rewards & costs, -7 Market research: field & desk research, target market, -8 The
  marketing mix & promoting a product, -9 Writing a business plan, -10 Business documents (invoice, quotation, receipt,
  credit note), -11 Cash flow, club/business budgets & sources of finance, -12 Analysed cash book, ledgers & the trial
  balance, -13 Final accounts: trading, profit & loss and financial position, -14 Interpreting the accounts: analysing
  financial performance & position
Our economy (jc-business-studies-2): -0 Scarcity, choice & opportunity cost, -1 Economic systems: how resources are
  distributed, -2 Supply, demand & how markets set prices, -3 Government finances: revenue, spending & the National
  Budget, -4 Taxation: why we pay tax and how it works, -5 Economic growth, sustainability & the environment,
  -6 International trade & globalisation, -7 Ireland in the European Union & the eurozone, -8 Economic indicators:
  inflation, employment, interest rates, -9 Current economic issues & government economic policy
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE BUSINESS STUDIES (Ireland, reformed NCCA spec, first examined
2019). A card helps a student who fell behind recover the marks: a clear gist of the concept/method, the ONE
highest-leverage move (or classic error), and a SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 270 marks, ~2 hours,
Section A (15 short questions, 6 marks each = 90) + Section B (3 long APPLIED questions, 60 marks each = 180; these
integrate strands and include the accounting/numerical work). EVERY card's level MUST be 'common'.
SEC MARKING (ground traps in it): Section A short answers have set accepted points. Section B accounting questions are
marked per correct line/figure — the analysed cash book, ledger postings, trial balance, final accounts and budgets each
award marks for correct entries on the correct side, correct totals, and the carried-down balance. Key consequences a card
can teach: a budget/cash-book needs the CLOSING balance = opening + income − expenditure carried correctly; debits vs
credits / the correct side of an account; "Explain"/"Outline" needs development, not one word; define-then-example earns
both marks; consumer-rights answers must name the actual right/agency.

GROUNDING (non-negotiable): ground every card in REAL SEC JC Business Studies questions + marking schemes at ${TXT}/ —
jc-business-studies-YYYY-CL-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled
2020-2021). grep/Read for the real question + the scheme's accepted answers / figures. Do NOT invent question numbers,
marks, or scheme wording.

CORRECTNESS (hard rule): every fact, definition and worked calculation must be CORRECT and within JC scope. NO Leaving-Cert
accounting (no formal ratio analysis like ROCE/acid-test, no break-even, no depreciation-method comparison, no control
accounts) — JC accounting is the analysed cash book, ledgers, trial balance, trading/profit&loss + statement of financial
position, club & household budgets, and analyse/recommend on those.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jcbus-', unique (e.g. 'jcbus-household-budget-closing-balance')
  subjectId     MUST be exactly 'jc-business-studies'
  topicId       one of the valid ids above
  subjectLabel  'Business Studies (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Budget: closing cash = opening + income − expenditure')
  level         MUST be 'common'
  gist          2-5 sentences: the concept/method + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC business move, e.g. 'in the analysed
                cash book, every receipt goes on the DEBIT side and every payment on the CREDIT side, then the analysis
                columns must add across to the total column', 'on Explain, give a developed point + a because', 'net pay =
                gross pay − total deductions (PAYE after tax credits, USC, PRSI)')
  check         { prompt (SELF-CONTAINED — embed the figures/scenario; for an accounts/budget question give the data in
                  words/a simple list), modelAnswer (the full correct answer with working), needed (>=2 award points = the
                  marking points / correct figures) }
  source        'Topic … — SEC JC Business Studies {YEAR} CL, Section …/Q… + marking scheme (…accepted answers/figures…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card alone — embed all figures and scenario. modelAnswer
shows the working/the correct entries.

QUALITY BAR: oneMove names a SPECIFIC business/accounting move or marking behaviour. BANNED filler: 'read the question',
'manage your time', 'learn the definitions', 'show your working' as a bare phrase.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const CARD_SCHEMA = {
  type: 'object', required: ['cards'],
  properties: {
    cards: { type: 'array', items: { type: 'object',
      required: ['id', 'subjectId', 'topicId', 'subjectLabel', 'topicLabel', 'focus', 'level', 'gist', 'oneMove', 'check', 'source', 'marksWeight'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
        subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
        level: { type: 'string', enum: ['common'] }, gist: { type: 'string' },
        oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
        check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
        source: { type: 'string' }, marksWeight: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'personal-finance', strand: 'jc-business-studies-0 (Personal finance)',
    topics: 'managing money (income/expenditure/needs vs wants), HOUSEHOLD BUDGETING (opening cash, income, expenditure, net cash, CLOSING cash; fixed/irregular/discretionary expenditure), saving & borrowing (sources, interest, APR, risk), INSURANCE (premium, the principle of utmost good faith / indemnity, claims, no-claims/loading), PERSONAL TAXES (PAYE, USC, PRSI, DIRT — what each is), WAGE SLIPS & take-home pay (gross pay − deductions = net pay; tax credits), being an INFORMED CONSUMER (rights, redress, the law on misleading ads), consumer AGENCIES & banks. The household budget and net-pay calculations are high-frequency.' },
  { key: 'enterprise-skills', strand: 'jc-business-studies-1 (Enterprise) — the non-accounting subtopics 1-0 to 1-11',
    topics: 'types of enterprise (financial/cultural/social), being ENTERPRISING & the entrepreneur, FORMS OF OWNERSHIP (sole trader/partnership/company — features, advantages), work/employment/volunteerism, EMPLOYER & EMPLOYEE rights & responsibilities, CSR & a business in its community, DIGITAL technologies (rewards & costs), MARKET RESEARCH (field vs desk, target market), the MARKETING MIX (product/price/place/promotion) & promotion methods, the BUSINESS PLAN (purpose, contents), BUSINESS DOCUMENTS (the order: quotation → order → invoice → receipt; credit note; what each is for), and cash-flow/club budgets & SOURCES OF FINANCE (short vs long term).' },
  { key: 'accounting', strand: 'jc-business-studies-1 (Enterprise) — the accounting subtopics 1-12, 1-13, 1-14',
    topics: 'the JC accounting cycle: the ANALYSED CASH BOOK (receipts on the debit side, payments on the credit side, analysis columns adding across), POSTING to LEDGER accounts & the TRIAL BALANCE (debit balances = credit balances), FINAL ACCOUNTS — the Trading account (sales − cost of sales = gross profit), Profit & Loss account (gross profit + gains − expenses = net profit), and the Statement of Financial Position (assets = liabilities + capital; working capital = current assets − current liabilities), and INTERPRETING the accounts (is the business doing well? analyse/recommend from net profit & working capital). Self-contained worked checks with small figure sets.' },
  { key: 'our-economy', strand: 'jc-business-studies-2 (Our economy)',
    topics: 'SCARCITY/choice/OPPORTUNITY COST, economic systems, SUPPLY & DEMAND & how markets set the equilibrium price (reading/shifting the curves), GOVERNMENT FINANCES (revenue vs current/capital expenditure, the National Budget, deficit/surplus), TAXATION (direct vs indirect, why we pay tax, examples), economic GROWTH & SUSTAINABILITY, INTERNATIONAL TRADE & globalisation (imports/exports, balance of trade), Ireland in the EU & the EUROZONE (benefits), ECONOMIC INDICATORS (inflation, employment, interest rates), and current economic issues/government policy.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrand: ${c.strand}\nTopics to mine: ${c.topics}\n\nProduce 6 cards spread across DIFFERENT subtopics and DIFFERENT years (all level 'common'). Ground each in a real question + its marking scheme. topicLabel MUST be the exact curriculum subtopic name. Every definition/calculation must be correct and within JC scope. For the accounting cluster, every worked figure must be arithmetically correct.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; valid topicId; level common). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Business Studies (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. CORRECTNESS: is everything in gist/oneMove/modelAnswer correct and within JC scope (no LC-only accounting — no ROCE/acid-test ratios, no break-even, no depreciation-method comparison)? For ANY calculation (budget, net pay, trading/P&L, working capital, interest) WORK IT YOURSELF and check the figures. If wrong → fix (or reject if unsalvageable). Check debits/credits on the right side.\n` +
    `2. GROUNDING: real question/section near "${c.source}" (2022-2025)? marks + accepted answers/figures match the scheme?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (all figures/scenario embedded)?\n` +
    `4. LEVEL: is level exactly 'common'? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific business/accounting move (no filler)?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (same id, level 'common'). If sound, accept. If fabricated/unsalvageable, reject.\n\n` +
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
  `Completeness critic for a Junior Cycle Business Studies (Common Level) Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) coverage across all THREE strands — Personal finance, Enterprise (BOTH the enterprise-skills AND the accounting subtopics 1-12/1-13/1-14), Our economy — flag thin areas, (2) whether the signature high-frequency / high-mark topics appear: household budget, net pay/wage slip, taxation (PAYE/USC/PRSI/DIRT), insurance, consumer rights, the analysed CASH BOOK, ledgers/trial balance, FINAL ACCOUNTS (trading/P&L/SOFP), business documents, marketing mix, market research, forms of ownership, supply&demand, opportunity cost, government Budget, EU/eurozone, (3) whether the signature MARKING traps are present (budget closing-balance, debit/credit side, Explain-needs-development, define+example, name-the-actual-right/agency), (4) any duplicate focus. List concrete gap slots (each: topicId + focus). All cards are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
