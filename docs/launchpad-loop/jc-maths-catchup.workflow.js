export const meta = {
  name: 'jc-maths-catchup',
  description: 'Author + adversarially verify Junior Cycle Mathematics Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, maths correctness, level purity' },
    { title: 'Critic', detail: 'completeness + level/strand balance' },
  ],
}

const TXT = '/tmp/jc_maths_txt'

const TOPICS = `
VALID jc-mathematics topicIds (the VERIFIED taxonomy — 4 contextual strands; the Unifying strand jc-mathematics-0 has NO
exam questions, so DO NOT tag cards to it). topicId MUST be one of these; topicLabel MUST be the EXACT name.
Strand Number (jc-mathematics-1): -0 Number systems & arithmetic operations, -1 Indices & scientific notation,
  -2 Factors, multiples & primes, -3 Rounding & accuracy, -4 Fractions, decimals & percentages, -5 Ratio & proportion,
  -6 Financial maths (money problems), -7 Sets & Venn diagrams
Strand Geometry and trigonometry (jc-mathematics-2): -0 Measure, units & time, -1 2D shapes: perimeter & area,
  -2 3D solids: nets, volume & surface area, -3 Geometric reasoning, theorems & constructions,
  -4 Right-angled triangles & trigonometry, -5 Co-ordinate geometry of the line, -6 Transformations & symmetry
Strand Algebra and functions (jc-mathematics-3): -0 Patterns, sequences & the nth term, -1 Expressions, variables &
  equality, -2 Manipulating expressions & factorising, -3 Solving equations, -4 Inequalities, -5 Rearranging formulae,
  -6 Functions & graphs
Strand Statistics and probability (jc-mathematics-4): -0 Counting & sample spaces, -1 Probability of random events,
  -2 The data-handling cycle (statistical investigation), -3 Representing data (graphs & charts),
  -4 Summary statistics (averages & spread)
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE MATHEMATICS (Ireland, the reformed NCCA spec first examined 2022).
A card helps a student who fell behind recover the marks: a clear gist of the technique, the ONE highest-leverage move (or
the classic error), and a SELF-CONTAINED worked check + model answer.

EXAM SHAPE (use real questionRefs): a single terminal paper per level, HIGHER and ORDINARY, 270 marks, ~2 hours, ~13-15
questions of varying marks (no Section split). Questions are frequently CROSS-STRAND and contextual/real-world.
SEC MARKING (ground traps in it): marking uses SCALES with partial credit — Low Partial Credit (LPC) for a relevant first
step, High Partial Credit (HPC) for substantial progress, full marks for a correct complete answer. Key consequences a
card can teach: you earn LPC for STARTING correctly even if you can't finish (so always write the relevant first line/
formula); "Show that ..." requires showing the working that arrives at the GIVEN answer (a bare answer scores little);
"Hence ..." means you MUST use the previous part's result; a correct final answer with NO work shown can be capped; units
and rounding to the requested accuracy carry marks; a slip (numerical) is penalised once, a blunder (conceptual) more.

GROUNDING (non-negotiable): ground every card in REAL SEC JC Maths questions + marking schemes at ${TXT}/ —
jc-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled 2020-2021).
grep/Read for the real question + the scheme's marking guidance (scale names, accepted answers). Do NOT invent question
numbers, marks, or scheme wording.

LEVEL PURITY (hard rule): a card's level MUST match the level of the paper its question is on (HL card from HL paper, OL
from OL) — never put an HL question in the OL section.

MATHS CORRECTNESS (hard rule): every worked model answer must be mathematically CORRECT and complete; every "needed" step
must be a real step in the method. Show the actual arithmetic/algebra. Plain text maths is fine (x^2, sqrt(), pi, <=, >=,
fractions as a/b). NO Leaving-Cert methods (no calculus, sine/cosine rule, unit circle, enlargement scale factor, standard
deviation) — JC trig is right-angled-triangle SOHCAHTOA + Pythagoras only.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jcmth-', unique (e.g. 'jcmth-pythagoras-find-hypotenuse-hl')
  subjectId     MUST be exactly 'jc-mathematics'
  topicId       one of the valid contextual ids above
  subjectLabel  'Mathematics (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Volume: work in terms of pi, sub numbers last')
  level          'higher' | 'ordinary'
  gist          2-5 sentences: the technique/method + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC maths move, e.g. 'write the formula
                with the numbers substituted BEFORE simplifying — that line is the LPC mark even if you slip later', 'on
                "Show that", you must reach the GIVEN answer with visible steps, not just state it', 'on "Hence", reuse
                the previous part — re-deriving from scratch wastes time and often loses the link mark')
  check         { prompt (SELF-CONTAINED — a concrete problem the student can solve from the card; include any numbers/
                  diagram-in-words needed), modelAnswer (the full correct working + final answer), needed (>=2 award
                  points = the method steps that earn the marks) }
  source        'Topic … — SEC JC Maths {YEAR} {LEVEL}, Q… + marking scheme (…scale / accepted answer…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt must be solvable from the card alone — embed the numbers, and describe any
diagram in words (e.g. 'a right-angled triangle with legs 6 cm and 8 cm'). modelAnswer must show the working.

QUALITY BAR: oneMove names a SPECIFIC maths move or the exact marking behaviour. BANNED filler: 'read the question',
'manage your time', 'show your working' (too generic — instead say WHAT working earns WHICH mark), 'check your answer'.

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
        level: { type: 'string', enum: ['higher', 'ordinary'] }, gist: { type: 'string' },
        oneMove: { type: 'object', required: ['label', 'text'], properties: { label: { type: 'string' }, text: { type: 'string' } } },
        check: { type: 'object', required: ['prompt', 'modelAnswer', 'needed'], properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
        source: { type: 'string' }, marksWeight: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'number', strand: 'jc-mathematics-1 (Number)',
    topics: 'number systems & operations, indices & scientific notation (a x 10^n), factors/multiples/primes (HCF/LCM), rounding & accuracy (sig figs, decimal places), fractions/decimals/percentages, ratio & proportion, FINANCIAL MATHS (percentage profit/loss, compound interest up to 3 years, income tax standard rate / USC, average speed), and SETS & Venn diagrams (2-set + 3-set, set difference, complement, #(A)). These dominate the early questions and the contextual money questions.' },
  { key: 'geometry-trig', strand: 'jc-mathematics-2 (Geometry and trigonometry)',
    topics: 'measure & unit conversion & time, perimeter & area of 2D shapes (incl. circle, arc/sector as a fraction), VOLUME & surface area & NETS of prisms/cylinders/spheres, geometric reasoning + theorems + the 15 constructions (3 & 7 HL-only), RIGHT-ANGLED-TRIANGLE trig (sin/cos/tan + inverses, 0-90 deg) and PYTHAGORAS, co-ordinate geometry of the line (distance |AB|, midpoint, slope, equation y=mx+c / ax+by+c=0, parallel/perpendicular), and the four transformations (translation, central & axial symmetry, rotation). NO enlargement/scale-factor (LC only).' },
  { key: 'algebra-functions', strand: 'jc-mathematics-3 (Algebra and functions)',
    topics: 'patterns/sequences & the nth term (linear & quadratic patterns), expressions & equality, manipulating expressions & FACTORISING (common factor, grouping, difference of two squares, quadratic trinomials), SOLVING EQUATIONS (linear, simultaneous, quadratic by factorising/formula), inequalities on the number line (over N, Z, R), rearranging/changing the subject of a formula, and FUNCTIONS & GRAPHS (f(x), domain/range, reading a graph, solving f(x)=g(x) graphically, max/min, graph transformations).' },
  { key: 'statistics-probability', strand: 'jc-mathematics-4 (Statistics and probability)',
    topics: 'counting & sample spaces (fundamental principle of counting, two-way tables), PROBABILITY of random events (relative frequency, equally-likely outcomes, expected frequency), the data-handling cycle (posing a question, bias, primary/secondary data), REPRESENTING data (histograms incl. unequal intervals, stem-and-leaf incl. back-to-back, bar/pie charts, scatter graphs & correlation), and SUMMARY STATISTICS (mean incl. from a frequency table / grouped data, median, mode, range; effect of an outlier).' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrand: ${c.strand}\nTopics to mine: ${c.topics}\n\nProduce 6 cards: aim for 3 Higher + 3 Ordinary, spread across DIFFERENT subtopics of this strand and DIFFERENT years. Ground each in a real question + its marking scheme. topicLabel MUST be the exact curriculum subtopic name. LEVEL PURITY: an OL card from an OL question only. Every model answer must be mathematically correct with the working shown.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'mathCorrect', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, mathCorrect: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; valid topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Maths Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question/section near "${c.source}" (2022-2025)? marks + scheme scale/accepted-answer match?\n` +
    `2. MATHS CORRECTNESS: WORK THE PROBLEM YOURSELF. Is check.modelAnswer mathematically correct and complete? Does every 'needed' step really earn marks? If the maths is wrong → fix it (or reject if unsalvageable).\n` +
    `3. SELF-CONTAINMENT: solvable from the card alone (numbers + any diagram described in words embedded)?\n` +
    `4. LEVEL PURITY: is the source paper actually ${c.level}? Is the METHOD within JC scope (no calculus / sine-cosine rule / unit circle / enlargement / std deviation)? An OL card from an HL paper → fix the level.\n` +
    `5. QUALITY: oneMove a specific maths move or marking behaviour (no filler)? topicId valid + topicLabel exact + NOT the unifying strand?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (same id). If sound, accept. If fabricated/unsalvageable, reject.\n\n` +
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
  `Completeness critic for a Junior Cycle Maths Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~50/50), (2) coverage across all FOUR contextual strands and their key examinable topics — flag thin areas (each strand should have several cards; the signature topics must appear: financial maths %/compound-interest/income-tax, sets/Venn, volume/SA/nets, Pythagoras + right-angled trig, co-ordinate geometry, constructions, factorising, solving quadratics, inequalities, functions/graphs, probability, histograms/stem-and-leaf, grouped-mean), (3) whether the signature MARKING traps are present: write-the-substituted-formula-for-LPC, "Show that" needs working, "Hence" must reuse, units/rounding marks, (4) any duplicate focus. List concrete gap slots (each: level + topicId + focus).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
