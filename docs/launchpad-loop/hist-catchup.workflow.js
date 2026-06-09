export const meta = {
  name: 'hist-catchup',
  description: 'Author + adversarially verify History Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'DBQ technique / essay craft / case-study clusters → cards' },
    { title: 'Verify', detail: 'skeptic refutes each vs paper + scheme' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/hist_txt'

const TOPICS = `
VALID history topicIds — the LC exam is FIELD OF STUDY: LATER MODERN, 1815-1993 ONLY. Use ONLY these two strands
(do NOT use the Early Modern strands history-0/history-1 — they are not examined at LC). The card's strand =
topicId minus its last -N segment (e.g. history-2-6 → strand history-2).

LATER MODERN: IRISH HISTORY 1815-1993 (strand history-2):
  -0 Ireland and the Union 1815-1870, -1 Case Study: Private Responses to Famine, -2 Case Study: Catholic Emancipation,
  -3 Case Study: The Synod of Thurles 1850, -4 Political & Social Reform 1870-1914, -5 Case Study: Elections of 1885 & 1886,
  -6 Case Study: Dublin 1913 Lockout, -7 Case Study: The GAA to 1891, -8 Sovereignty & Partition 1912-1949,
  -9 Case Study: The Treaty Negotiations 1921, -10 Case Study: Belfast During WWII, -11 Case Study: Eucharistic Congress 1932,
  -12 The Irish Diaspora 1840-1966, -13 Case Study: Grosse Isle, -14 Case Study: De Valera in America,
  -15 Case Study: Holy Ghost Mission, Nigeria, -16 Northern Ireland 1949-1993, -17 Case Study: The Sunningdale Agreement,
  -18 Case Study: Coleraine University, -19 Case Study: Apprentice Boys of Derry, -20 The Republic of Ireland 1949-1989,
  -21 Case Study: First Economic Programme, -22 Case Study: EEC Impact on Fisheries, -23 Case Study: Impact of RTE 1962-1972

LATER MODERN: EUROPE & WIDER WORLD 1815-1992 (strand history-3):
  -0 Nationalism & State Formation 1815-1871, -1 Case Study: 1848 Revolution in Germany, -2 Case Study: New Lanark,
  -3 Case Study: Haussmann's Paris, -4 Nation States & Tensions 1871-1920, -5 Case Study: Naval Policy of Wilhelm II,
  -6 Case Study: Women in the WWI Workforce, -7 Case Study: Early History of the Motor Car, -8 Dictatorship & Democracy 1920-1945,
  -9 Case Study: Stalin's Show Trials, -10 Case Study: The Jarrow March 1936, -11 Case Study: The Nuremberg Rallies,
  -12 Division & Realignment 1945-1992, -13 Case Study: Hungarian Uprising 1956, -14 Case Study: The Oil Crisis 1973,
  -15 Case Study: Second Vatican Council, -16 Retreat from Empire 1945-1990, -17 Case Study: British Withdrawal from India,
  -18 Case Study: Secession of Katanga, -19 Case Study: Race Relations in France, -20 The US and the World 1945-1989,
  -21 Case Study: Montgomery Bus Boycott, -22 Case Study: Johnson & Vietnam, -23 Case Study: The Moon Landing 1969
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert HISTORY (Irish exam-recovery tool). A card teaches a student
who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a check question + model answer.

GROUNDING (non-negotiable): ground every card in REAL SEC LC History questions + marking schemes. Text of all papers
+ schemes (2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): history-YYYY-{HL,OL}-{paper,marking-scheme}.txt
grep/Read to find the exact question + how the scheme awards it. Do NOT invent question wording, marks, or scheme content.
COPYRIGHT IS CLEARED for all SEC material + the documents — you may quote document extracts and reproduce facts faithfully.

HISTORY MARKING GRAMMAR (this is the whole game — teach it):
- The written paper = Section 1 Documents-Based Question (DBQ, 100 marks, on a rotating prescribed documents topic),
  Section 2 Ireland essays, Section 3 Europe & the Wider World essays. HL writes 1 DBQ + 2 essays; OL similar but shorter.
- ESSAYS are marked by CUMULATIVE marks: the examiner counts your Significant Relevant Statements (SRS) — each distinct,
  accurate, RELEVANT-TO-THE-QUESTION point. HL essay = 100 (e.g. up to ~12 SRS at the going rate + overall mark for
  coherence/structure). The killer skill is RELEVANCE: narration that doesn't address the question earns few SRS.
- DBQ has 4 question types: (a) COMPREHENSION (extract/quote info from a named document), (b) COMPARISON (compare what
  two documents say — cross-reference, don't summarise each separately), (c) CRITICISM (judge a document's reliability/
  usefulness/objectivity — by WHO wrote it, WHEN, WHY/for whom, propaganda vs eyewitness — NOT whether you agree), and
  (d) CONTEXTUALISATION (a mini-essay placing the documents in their wider historical context, marked cumulatively by SRS).

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'hist-', unique, includes the topic (e.g. 'hist-1913-lockout-causes-hl')
  subjectId     MUST be exactly 'history'
  topicId       one of the valid history-2-* / history-3-* ids above
  subjectLabel  'History'
  topicLabel    short human label (may match the syllabus subtopic)
  focus         short row label disambiguating same-subtopic cards (e.g. 'DBQ criticism: reliability', '1913 Lockout: causes')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core technique OR the core content + how the exam tests it. Supportive, precise.
  oneMove       { label, text } — the single highest-leverage move (a technique rule, or the argument the SRS reward)
  check         { prompt (self-contained, exam-style), modelAnswer (full — for essays, the KEY SRS as a model paragraph),
                  needed (>=2 strings: the SRS / award points the answer must contain) }
  source        'Topic … — SEC LC History {YEAR} {LEVEL}, Section …, Q… + marking scheme (…how it is awarded…)'
  marksWeight   integer marks at stake (from the scheme)
  figureSpec    OPTIONAL — include ONLY for a DBQ card built on a VISUAL document (a political cartoon, photograph,
                poster, map) that the student must read. Shape { year, level, questionRef, describes (what the source
                shows in detail), whyNeeded }. For TEXT document extracts, embed the quote inline in the prompt instead.
                DO NOT add a 'figure'/'src' field — the crop is extracted later by the main loop.

SELF-CONTAINMENT (hard rule): the check prompt must be answerable from the card itself + general history knowledge. If a
DBQ card needs a source, EITHER embed the text extract inline (for text documents) OR add a figureSpec (for visual
documents). Never let a prompt silently depend on an unseen document.

QUALITY BAR: oneMove must name a SPECIFIC history move (e.g. 'for criticism, weigh who wrote it and why, not whether it's
true', 'each distinct relevant point is one SRS — so make separate points, do not pad one idea', 'compare means
cross-reference the two documents, not summarise each'). BANNED filler: 'read the question', 'manage your time',
'plan your answer', 'write neatly'. Plain text; ASCII apostrophes/quotes fine; keep any quoted document extract short.

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
  { key: 'dbq-technique', n: 5,
    brief: 'DBQ SKILLS cards (Section 1). One card each for: COMPREHENSION (how to extract/quote the exact info the document gives), COMPARISON (cross-reference two documents, not summarise each), CRITICISM/reliability (judge a source by who/when/why — propaganda vs eyewitness vs hindsight), CONTEXTUALISATION (the mini-essay marked cumulatively by SRS). Build each on a REAL DBQ from a specific year (the DBQ topic rotates — find which topic each year used). Map topicId to the case study the documents relate to. Add a figureSpec ONLY if the document is VISUAL (cartoon/photo/poster); embed short text extracts inline otherwise. Aim 3 HL + 2 OL.' },
  { key: 'essay-craft', n: 3,
    brief: 'ESSAY-CRAFT cards: (1) the cumulative/SRS marking — what counts as a Significant Relevant Statement and how relevance to the exact question (not narration) drives the mark; (2) structure — a focused introduction that addresses the question + a conclusion that judges; (3) one card on a high-frequency essay command pattern (e.g. answering an "assess/discuss the contribution of X" or "what were the causes and consequences of Y"). Ground each in a real essay question + its scheme. Map topicId to the topic the example essay is on. Aim 2 HL + 1 OL.' },
  { key: 'ireland-content', n: 6,
    brief: 'LATER MODERN IRELAND case-study/topic CONTENT cards (strand history-2): high-frequency, high-yield topics — e.g. the 1913 Dublin Lockout, the Treaty negotiations 1921, Catholic Emancipation, Parnell/the 1885-86 elections, Northern Ireland/Sunningdale, the First Economic Programme/Lemass-Whitaker, the Eucharistic Congress 1932. Each card states the KEY SRS-worthy points (causes/course/consequences or key arguments) the scheme rewards for an essay on that topic. Ground in a real essay question + scheme. Aim 3 HL + 3 OL.' },
  { key: 'europe-content', n: 6,
    brief: 'LATER MODERN EUROPE & WIDER WORLD case-study/topic CONTENT cards (strand history-3): high-frequency topics — e.g. Stalin\'s Show Trials, the Nuremberg Rallies, Dictatorship & Democracy (Hitler/Mussolini rise), the Montgomery Bus Boycott, Johnson & Vietnam, the Moon Landing 1969, the Hungarian Uprising 1956, Nationalism (unification). Each states the KEY SRS-worthy points the scheme rewards. Ground in a real essay question + scheme. Aim 3 HL + 3 OL.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\n${c.brief}\n\nProduce ${c.n} cards. Read the relevant ${TXT}/ files to ground every card, claim, mark and citation in the real questions + schemes.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'historicallyAccurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, historicallyAccurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE History Catch-Up recovery card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: is there a real ${c.level} question matching "${c.source}"? Do the marks + the scheme's award approach (cumulative/SRS for essays; the specific DBQ award points) match the scheme text? If fabricated/mis-cited → grounded:false.\n` +
    `2. HISTORICAL ACCURACY: are all dates, names, events, causes/consequences correct? Flag any error (wrong date, wrong person, anachronism, a "fact" not supportable). historicallyAccurate:false if any.\n` +
    `3. SELF-CONTAINMENT: can a student answer check.prompt from the card alone (+ a figureSpec/embedded extract if it's a DBQ source card)? If it silently needs an unseen document → selfContained:false (fix by embedding the extract or adding a figureSpec for a visual source).\n` +
    `4. TECHNIQUE: for DBQ/essay-craft cards, is the move correct per the scheme (e.g. comparison = cross-reference; criticism = reliability by who/when/why; essays marked by SRS/relevance)?\n` +
    `5. QUALITY: is oneMove a specific history move (not banned filler)? Are needed[] real SRS/award points? Is topicId a valid history-2-* / history-3-* id?\n\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id; preserve/repair figureSpec). If sound, accept. If fabricated/inaccurate-unsalvageable, reject.\n\n` +
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
  `Completeness critic for a History Catch-Up Lane recovery-card set (Irish LC, Later Modern). The ${kept.length} kept cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec, marks: k.marksWeight })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) coverage of the FOUR DBQ skills (comprehension, comparison, criticism, contextualisation), ` +
  `(3) balance between Ireland (history-2) and Europe/Wider-World (history-3) content, (4) essay-craft (SRS/cumulative, relevance, structure) coverage, ` +
  `(5) whether high-frequency topics are represented and whether any visual-DBQ source figures are included. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
