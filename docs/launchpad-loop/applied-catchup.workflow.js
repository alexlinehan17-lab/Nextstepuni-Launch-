export const meta = {
  name: 'applied-catchup',
  description: 'Author + adversarially verify Applied Mathematics Catch-Up Lane recovery cards from real SEC papers/schemes (new spec 2023+)',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards (+figureSpec for diagrams)' },
    { title: 'Verify', detail: 'skeptic RECOMPUTES every value vs the scheme' },
    { title: 'Critic', detail: 'completeness + level/strand balance' },
  ],
}

const TXT = '/tmp/applied_txt'

const TOPICS = `
VALID applied-mathematics topicIds (the VERIFIED taxonomy — topicLabel MUST be the EXACT name below; this is the single
source of truth, adversarially verified against the NCCA spec):
Strand 1 Mathematical Modelling (applied-mathematics-0): -0 The Problem-Solving Cycle, -1 Formulating Problems,
  -2 Translating Problems into Mathematics, -3 Computing Solutions, -4 Evaluating Solutions
Strand 2 Networks and Graphs (applied-mathematics-1): -0 Networks and Their Associated Terminology, -1 Matrices, Matrix
  Algebra and Adjacency, -2 Minimum Spanning Trees (Kruskal and Prim), -3 Dynamic Programming and Shortest Paths (Bellman,
  Dijkstra), -4 Algorithms: Greedy vs Dynamic Programming, -5 Project Scheduling and Critical Paths
Strand 3 Physical World (applied-mathematics-2): -0 Kinematics: Particle Motion in One Dimension, -1 Describing Motion
  with Calculus, -2 Particle Motion in 2D: Vectors and Projectile Motion, -3 Forces, Newton's Laws and Free-Body Diagrams,
  -4 Momentum, Impulse and Collisions, -5 Connected Masses, Friction and Drag, -6 Work, Energy and Conservation,
  -7 Circular Motion of a Particle, -8 Dimensional Analysis
Strand 4 Changing World (applied-mathematics-3): -0 Recurrence Relations and Differences, -1 Modelling Incremental Change
  with Difference Equations, -2 Solving Difference Equations (Homogeneous and Inhomogeneous), -3 Modelling Continuous
  Change with Differential Equations, -4 Solving Differential Equations (Separable; Reducible Second-Order)
TAGGING RULES (verified): 'apply Dijkstra/Kruskal/Prim' → -1-2/-1-3; 'classify/justify greedy-vs-DP' → -1-4.
Momentum-conservation cards → -2-4, never -2-6.
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert APPLIED MATHEMATICS (Irish exam-recovery tool) — the CURRENT
modelling specification (first examined 2023). A card teaches a student who lost marks how to recover them: a clear gist,
the ONE highest-leverage move, and a SELF-CONTAINED check + fully worked model answer.

EXAM SHAPE (use real questionRefs): written paper 400 marks (80%), TEN questions, answer ANY EIGHT, 50 marks each, 2.5
hours, HL and OL; plus a 20% modelling project on a common SEC brief. Questions mix strands and are CONTEXT-driven
(modelling). OL is simpler; HL includes the bold (HL-only) outcomes like calculus-heavy kinematics.

GROUNDING (non-negotiable): ground every card in REAL SEC questions + marking schemes at ${TXT}/ —
applied-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===). USE ONLY 2023, 2024, 2025 (the new spec);
2021-2022 are the OLD syllabus — do NOT use them. grep/Read for the exact question + the scheme's worked solution. Do NOT
invent question numbers, marks, data, or scheme values. RECOMPUTE EVERY numeric value from the question data and confirm
it matches the scheme answer EXACTLY (g = 9.8 m s^-2 unless the question says otherwise). Applied Maths answers are
precise — formula, substitution, value, UNIT.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'am-', unique (e.g. 'am-dijkstra-shortest-path-hl')
  subjectId     MUST be exactly 'applied-mathematics'
  topicId       one of the valid ids above
  subjectLabel  'Applied Mathematics'
  topicLabel    the verified subtopic's EXACT name
  focus         short row label (e.g. 'Dijkstra: label-and-settle, never guess by eye')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the technique + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks (a SPECIFIC applied-maths
                move, e.g. 'resolve along and perpendicular to the incline, never vertically', 'in restitution e applies
                to the SEPARATION speed along the line of centres', 'set up the difference equation BEFORE iterating',
                'check the units/dimensions of your answer')
  check         { prompt (SELF-CONTAINED — embed ALL data inline; small numeric problems work best; reference the figure
                  if figureSpec present), modelAnswer (FULLY WORKED: formula → substitution → value with UNIT),
                  needed (>=2 award points: the formula/setup, the key intermediate, the final value+unit) }
  source        'Topic … — SEC LC Applied Mathematics {YEAR} {LEVEL}, Q… + marking scheme (…scheme answer…)'
  marksWeight   integer marks at stake (a full question is 50; parts are less per the scheme)
  figureSpec    Include when the question's diagram is genuinely needed (a NETWORK/graph to run an algorithm on, a v-t
                graph to read, a project-scheduling network, a pulley/incline diagram). Shape { year, level, questionRef,
                source ('paper'|'scheme'), describes, whyNeeded }. Default to including it for network/graph questions
                (user rule: show the figure for context); pure-algebra cards need none. No real 'figure'/'src'.

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge + the figure (if figureSpec).
Embed every number needed. For network questions without a figure, embed a small edge-list/table inline instead.

QUALITY BAR: oneMove names a SPECIFIC move/error. BANNED filler: 'show your working', 'read the question', 'practice more',
'manage your time'. Plain text; unicode (×, ², θ, ∝, →, ½) fine.

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
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'modelling-networks', strands: 'applied-mathematics-0 (Modelling) + applied-mathematics-1 (Networks and Graphs)',
    topics: 'the modelling cycle (assumptions → model → solve → EVALUATE, incl. one card on attacking the 20% project); adjacency matrices (build/read, interpret the matrix product), minimum spanning trees by Kruskal AND Prim, Dijkstra shortest path (label-and-settle), Bellman dynamic programming (work backwards stage by stage), greedy vs DP, project scheduling (critical path, early/late times, floats). Network questions get a figureSpec.' },
  { key: 'kinematics', strands: 'applied-mathematics-2-0/-2-1/-2-2',
    topics: '1D kinematics: SUVAT (choose the right equation from what is given/wanted), v-t graphs (area = displacement, slope = acceleration, two-phase journeys), motion with calculus (differentiate/integrate motion functions, deriving SUVAT); 2D: vectors (components, dot product), projectile motion (split horizontal/vertical, time of flight, max height, range). v-t graph + projectile questions can carry a figureSpec.' },
  { key: 'forces-collisions', strands: 'applied-mathematics-2-3/-2-4/-2-5',
    topics: 'free-body diagrams + resolving on horizontal/inclined planes (along/perpendicular), Newton\'s second law F=ma systems, connected masses (pulleys — separate equations per mass, same a and T), friction (F = μR, limiting friction), momentum conservation, impulse, direct + oblique collisions with the coefficient of restitution e (Newton\'s experimental law sign convention), drag F ∝ v^n. Pulley/incline diagrams can carry a figureSpec.' },
  { key: 'energy-circular-dimensions', strands: 'applied-mathematics-2-6/-2-7/-2-8',
    topics: 'work-energy: work done by constant + variable forces, GPE/KE, conservation of energy (when to use energy vs SUVAT), elastic springs/strings (Hooke\'s law work); circular motion: horizontal circle (conical pendulum style) + vertical circle (critical speed at the top, energy + F=ma toward centre combined); dimensional analysis (check an answer\'s dimensions/units).' },
  { key: 'changing-world', strands: 'applied-mathematics-3 (Changing World)',
    topics: 'first/higher differences of sequences; SETTING UP difference equations from context (Malthusian/restricted growth, loans/interest, disease spread) and iterating/solving them (homogeneous + inhomogeneous linear); setting up differential equations from continuous-change contexts (cooling, decay, population, motion with variable force); solving first-order separable + second-order reducible; interpreting solutions in context.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 6 cards: aim for ~4 Higher + ~2 Ordinary, spread across DIFFERENT subtopics and years 2023-2025. RECOMPUTE every value and confirm it matches the scheme. Add figureSpec where the diagram is genuinely needed (networks/graphs default to including it). topicLabel MUST be the exact verified subtopic name.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards (${cards.filter((c) => c.figureSpec).length} with figureSpec)`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'mathChecks', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, mathChecks: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; preserve/repair figureSpec). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Applied Mathematics Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question (2023-2025 ONLY — the new spec) near "${c.source}"? marks + scheme answer match? If grounded in a 2021/2022 old-spec paper → reject.\n` +
    `2. MATHS (most important): RECOMPUTE every number in check.modelAnswer from the prompt data step by step. Formula right? Substitution right? Final value + UNIT matches your recomputation AND the scheme (g=9.8 unless stated)? Any mismatch → mathChecks:false and fix with the correct working.\n` +
    `3. CONCEPTS: any applied-maths error (wrong sign convention in restitution, resolving vertically on an incline, wrong Dijkstra/Bellman procedure, wrong difference-equation setup)?\n` +
    `4. SELF-CONTAINMENT: answerable from the card + figure (if figureSpec)? All data embedded? Network cards need either a figureSpec or an inline edge-list.\n` +
    `5. TAXONOMY: topicId valid + topicLabel the exact verified name? (apply-algorithm → -1-2/-1-3, classify → -1-4; momentum → -2-4.)\n` +
    `6. QUALITY: oneMove specific (no filler)? needed[] real award points?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (same id). If sound, accept. If fabricated, reject.\n\n` +
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
log(`Verify: ${kept.length}/${cards.length} kept (${kept.filter((c) => c.figureSpec).length} with figureSpec)`)

phase('Critic')
const critic = await agent(
  `Completeness critic for an Applied Mathematics Catch-Up Lane set (Irish LC, new spec). The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) strand spread across Modelling, Networks/Graphs, Physical World (kinematics + dynamics + energy/circular), Changing World — flag thin areas, (3) signature topics present: Dijkstra OR Bellman, an MST, a projectile, connected masses/pulley, a collision with restitution, a difference equation from context, a separable differential equation, a v-t graph?, (4) figureSpec coverage on network/graph cards. List concrete gap slots (each: level + topicId + focus + figure?).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
