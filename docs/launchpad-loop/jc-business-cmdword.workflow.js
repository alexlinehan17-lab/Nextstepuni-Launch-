export const meta = {
  name: 'jc-business-cmdword',
  description: 'Author + adversarially verify Junior Cycle Business Studies (Common Level) Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, business sense, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_business_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE BUSINESS STUDIES (Ireland, reformed NCCA spec, first examined 2019).
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that
cue demands and the marking trap behind it.

EXAM SHAPE: a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 270 marks, ~2h, Section A (15 short Qs, 6 marks
each) + Section B (3 long applied Qs, 60 marks each, incl. the accounting/numerical work). EVERY stem's level MUST be
'common'.
SEC MARKING: Section A has set accepted points; Section B accounting is marked per correct entry/figure; develop-cues need
development; count cues ("two reasons") need that many distinct points.

JC-BUSINESS-STUDIES CUE GRAMMAR (ground demands/traps in it):
 - 'State' / 'Name' / 'Give' / 'List' / 'Identify': the exact short answer(s) — precise term, no explanation; count cues
   need that many distinct points. Trap: a vague description where a NAMED term is needed; giving fewer than asked.
 - 'Define' / 'What is meant by': the precise meaning of the term (often define + a brief example earns both marks). Trap:
   an example with no actual definition.
 - 'Explain' / 'Outline' / 'Describe': a DEVELOPED point — say what it is AND a consequence/how/why. Trap: a one-word or
   undeveloped answer; the marks need the development.
 - 'Distinguish between' / 'Compare': the contrast on the SAME feature for BOTH items (e.g. debit vs credit, field vs desk
   research, sole trader vs partnership). Trap: describing only one side, or two non-contrasting facts.
 - 'Calculate' / 'Complete' / 'Balance' / 'Post': the numeric/accounting task — Calculate (net pay, interest, % , a budget
   figure) needs working + the figure; Complete/Balance (a budget, an analysed cash book, a ledger, final accounts) needs
   the correct entries on the correct side and the carried-down balance/total. Trap: wrong side (debit vs credit), a budget
   closing balance that doesn't equal opening + income − expenditure, missing totals.
 - 'Draw' / 'Illustrate': produce an accurate figure (e.g. a supply & demand graph with labelled axes and curves, the
   equilibrium point). Trap: unlabelled axes, curves the wrong way (demand slopes down, supply up).
 - 'Recommend' / 'Suggest' / 'Advise': a justified choice — state the option AND a business reason. Trap: a choice with no
   justification; the marks are in the reason.

THE TYPE (one object per stem):
  id            kebab, prefix 'jcbus-', unique (e.g. 'jcbus-complete-cashbook-common')
  subjectId     MUST be exactly 'jc-business-studies'
  subjectLabel  'Business Studies (Junior Cycle)'
  level         MUST be 'common'
  questionRef   e.g. '2024 CL · Section A · Q9' or '2023 CL · Section B · Q17(a)'
  stem          the question stem, faithful to the paper (summarise a long applied scenario briefly; if it needs a
                figure/account layout, describe the essential figures in words). MUST contain commandWord verbatim.
  commandWord   the cue ('State', 'Name', 'Give', 'List', 'Identify', 'Define', 'Explain', 'Outline', 'Describe',
                'Distinguish', 'Compare', 'Calculate', 'Complete', 'Balance', 'Post', 'Draw', 'Illustrate', 'Recommend',
                'Suggest', 'Advise')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question.
  trap          the scheme-flagged mistake for THIS cue + the marks consequence.
  source        'SEC JC Business Studies {YEAR} CL marking scheme, Q… (…accepted answers/figures…)'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Multi-word cues ('Distinguish between', 'What is meant by') must appear as that exact run.

GROUNDING (non-negotiable): every stem is a REAL SEC JC Business Studies question (2022-2025; exams cancelled 2020-2021).
Papers + schemes at ${TXT}/ — jc-business-studies-YYYY-CL-{paper,marking-scheme}.txt. grep/Read for the exact stem +
scheme guidance. Do NOT invent question numbers, marks, or scheme wording. Stay within JC scope (no LC-only accounting).

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'learn the topic'). trap = a real marking
pattern. Prefer cue DIVERSITY (especially the accounting Complete/Balance/Calculate, Distinguish, Recommend). Plain text.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: { type: 'array', items: { type: 'object',
      required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
        stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
        trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'recall-define', cues: 'State, Name, Give, List, Identify, Define, What is meant by',
    topics: 'the short-answer/recall + definition cues across all strands — "Name two sources of finance", "State one function of money", "Identify the type of insurance", "Define opportunity cost", "What is meant by globalisation". Demand: the exact named term(s) / the precise meaning; count cues need that many. Trap: a vague description where a named term is needed; an example with no definition; fewer than asked.' },
  { key: 'explain-develop', cues: 'Explain, Outline, Describe',
    topics: 'the developed-point cues — "Explain one benefit of a budget", "Outline two reasons people save", "Describe how the marketing mix helps a product". Demand: a developed point (what it is + a consequence/how/why). Trap: an undeveloped one-word answer; the marks need the development.' },
  { key: 'distinguish-recommend', cues: 'Distinguish, Compare, Recommend, Suggest, Advise',
    topics: 'the contrast + justified-choice cues — "Distinguish between field and desk research", "Distinguish between a debit and a credit", "Recommend a form of business ownership and justify", "Advise the consumer of their rights". Demand: the contrast on the SAME feature for both / the choice WITH a business reason. Trap: only one side of a contrast; a choice with no justification.' },
  { key: 'accounting-numerical', cues: 'Calculate, Complete, Balance, Post',
    topics: 'the numeric + accounting cues — "Calculate the net pay / the DIRT / the closing cash", "Complete the household budget", "Complete and balance the Analysed Cash Book", "Post the totals to the ledger". Demand: working + the figure / correct entries on the correct side + the carried-down balance/total. Trap: a budget closing balance ≠ opening + income − expenditure; a receipt on the credit side; missing totals; no working on a Calculate.' },
  { key: 'graph-and-mixed', cues: 'Draw, Illustrate, Calculate (graph), plus any cue on Our-economy',
    topics: 'the supply & demand GRAPH cues + economy questions — "Draw a supply and demand diagram and show the equilibrium", "Illustrate the effect of an increase in demand", plus State/Explain on scarcity, taxation, the National Budget, the EU/eurozone, inflation. Demand: labelled axes, demand sloping down + supply up, the equilibrium point; for economy questions the precise term/effect. Trap: unlabelled or reversed curves; a vague economy answer.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems, each with a DIFFERENT cue where possible, across years and strands (all level 'common'). Ground every stem/demand/trap/marks/citation in the paper + scheme. Make demand+trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: {
      id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
      level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
      commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
      source: { type: 'string' }, marks: { type: 'integer' } } },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Business Studies (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase; multi-word cue = exact run)? If not → fix.\n` +
    `2. GROUNDING: real question near ${s.questionRef} (2022-2025 CL)? marks + the marking rule in demand/trap match the scheme? else grounded:false.\n` +
    `3. BUSINESS SENSE + SCOPE: demand/trap correct and within JC scope (no LC-only accounting)? Is the cue the RIGHT command word for what the question asks? level exactly 'common'?\n` +
    `4. QUALITY: demand specific to this cue+question (no filler)? trap a real marking pattern (named-term, count, undeveloped, wrong side/closing-balance, no-justification)?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id, level 'common'). If sound, accept. If fabricated, reject.\n\n` +
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
  `Completeness critic for a Junior Cycle Business Studies (Common Level) Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) cue diversity — State/Name/Give/List/Identify, Define/What-is-meant-by, Explain/Outline/Describe, Distinguish/Compare, Calculate/Complete/Balance/Post, Draw/Illustrate, Recommend/Suggest/Advise; flag missing cues, (2) coverage across the three strands (Personal finance, Enterprise incl. accounting, Our economy) — the accounting Complete/Balance/Calculate cues and a supply&demand Draw must appear, (3) whether the signature traps are present: named-term not description, count-short, undeveloped Explain, debit/credit wrong side, budget closing-balance, no-justification on Recommend. List concrete gap slots (each: cue + topic/strand). All stems are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
