export const meta = {
  name: 'econ-cmdword',
  description: 'Author + adversarially verify Economics Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue/topic clusters → grounded stems' },
    { title: 'Verify', detail: 'independent skeptic refutes each vs scheme' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/econ_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert ECONOMICS (Irish exam-technique tool, NEW spec examined 2022+).
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what
that cue demands and the marking-scheme trap behind it.

GROUNDING (non-negotiable): every stem is a REAL SEC LC Economics question. Text of all papers + schemes at ${TXT}/
(pages ===PAGE n===): economics-YYYY-{HL,OL}-{paper,marking-scheme}.txt. PRIORITISE 2022-2025 (current spec); 2021 is
the OLD syllabus — avoid unless the concept is identical. grep/Read for the exact stem + scheme award points. Do NOT
invent question numbers, marks, or scheme wording. RECOMPUTE any number you cite.

THE TYPE (one object per stem):
  id            kebab, prefix 'econ-', unique, includes cue + topic (e.g. 'econ-calculate-ped-2022-hl')
  subjectId     MUST be exactly 'economics'
  subjectLabel  'Economics'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2023 HL · Q1(a)' or '2024 OL · Q11(b)'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim.
  commandWord   the cue (or multi-word cue like 'Distinguish between', 'With reference to', 'Outline two')
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question. Name the exact thing the
                scheme rewards (the definition wording, the formula + sign, the diagram shift, the number of points).
  trap          the examiner/scheme-flagged mistake for THIS cue + the marks consequence. Quote the scheme where it bites
                (e.g. 'PED keeps its negative sign', 'a subsidy shifts SUPPLY not demand', 'name + explain — naming alone
                caps at half marks', 'GNP = GDP minus net factor income from abroad').
  source        'LC Economics {YEAR} {LEVEL} marking scheme, Q… ("…award point…")'
  marks         integer marks at stake (from the scheme)
  figure        OPTIONAL — only if the cue genuinely depends on a graph AND it is one of the committed crops below whose
                SOURCE QUESTION matches your stem. Shape { src, alt, source }.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. So 'Distinguish between' needs those two words consecutive in the stem. Verify per stem.

ALREADY-COMMITTED economics figures you MAY reuse ONLY if your stem genuinely IS that exact question:
  /exam-figures/economics/economics-2022-hl-ped-facemasks-demand.png — 2022 HL Q1(a) face-mask demand curve (P €4↔€5, Q 8↔4)
  /exam-figures/economics/economics-2022-hl-eur-gbp-exchange-rate.png — 2022 HL Q15(b) €/£ exchange-rate line graph (Dec-12 to Dec-21)
  /exam-figures/economics/economics-2024-hl-cpi-annual-change.png — 2024 HL Q12(b) CPI all-items annual %-change graph (Mar-Oct 2023)
figure.source = 'SEC Leaving Certificate Economics {YEAR} {LEVEL}, Q… — © State Examinations Commission' + a precise alt.
Most economics command-word stems are text-only — that is fine. Do NOT force a figure.

QUALITY BAR (reject your own draft if it fails):
- demand must be specific to cue+question, not generic. BANNED filler: 'read the question carefully', 'manage your time',
  'show your working', 'plan your answer', anything that fits any exam.
- trap must name a real scheme-grounded pattern (the elasticity sign, a curve-shift direction, GDP/GNP relation, a
  name-AND-explain rule, a unit, a number-of-points requirement).
- Prefer cue DIVERSITY: Define, State, Calculate, Explain, Outline, Distinguish between, Illustrate, Identify, Analyse,
  Discuss, 'With reference to', 'Outline two'.
- ASCII fine (%, ->); € and unicode (×, ↑↓) fine.

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
          figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'micro-foundations', cues: 'Define, Calculate, Explain, State, Outline',
    topics: 'scarcity & opportunity cost, the PPF, demand & the law of demand, supply, market equilibrium, elasticity (PED/YED/CED — calculate), the consumer & the firm, government intervention (price controls, taxes & subsidies)' },
  { key: 'markets', cues: 'Distinguish between, Explain, Illustrate, Outline, Identify',
    topics: 'market structures (perfect competition, monopoly, monopolistic competition, oligopoly), the labour market (wage determination, trade unions), market failure (externalities — positive/negative, public goods, merit goods) and government responses' },
  { key: 'policy-performance', cues: 'Calculate, Define, Explain, Outline, State',
    topics: 'national income (GDP, GNP, GNI*, the multiplier), fiscal policy & the budget, employment & unemployment (types, rates), monetary policy & prices (inflation, CPI, the ECB), the financial sector' },
  { key: 'international', cues: 'Define, Explain, Outline, Distinguish between, Identify',
    topics: 'economic growth vs development (HDI), globalisation (MNCs, FDI), trade & competitiveness (comparative advantage, balance of payments/trade, protectionism, the EU), exchange rates (appreciation/depreciation)' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 4 stems: aim for 2 Higher + 2 Ordinary, each with a DIFFERENT command word where possible, spread across years (2022-2025). Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation.`,
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
        figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Economics Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} NEW-SPEC (2022-2025) question near ${s.questionRef}? marks + demand's scheme-rewarded thing + trap's quoted award point match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any economics error (wrong definition, elasticity sign, curve-shift direction, GDP/GNP relation, wrong number/marks)?\n` +
    `4. FIGURE (if present): src matches a stem genuinely from that exact question? else drop the figure in a fix.\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme pattern?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated/old-spec, reject.\n\n` +
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
  `Completeness critic for an Economics Command-Word Reflex stem set (Irish LC, new spec). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef, hasFigure: !!k.figure })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) command-word diversity (flag if one cue dominates), (3) topic spread across the 5 ` +
  `strands (foundations/decisions, markets, policy/performance, international), (4) whether figure/calculation cues are ` +
  `present. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
