export const meta = {
  name: 'construction-catchup',
  description: 'Author + adversarially verify Construction Studies Catch-Up Lane recovery cards (theory + drawings) from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards (+figureSpec for drawings)' },
    { title: 'Verify', detail: 'skeptic checks grounding, accuracy, self-containment' },
    { title: 'Critic', detail: 'completeness + level/strand/figure balance' },
  ],
}

const TXT = '/tmp/construction_txt'

const TOPICS = `
VALID construction-studies topicIds. topicId MUST be one of these; topicLabel MUST be the curriculum subtopic's EXACT name
below (the syllabus is the source of truth — do not invent headings). Card's strand = topicId minus its last -N.
Part 1 — Construction Theory & Drawings (construction-studies-0): -0 General, -1 Substructure, -2 Superstructure,
  -3 Internal Construction, -4 Services, External Works & Drainage, -5 Heat & Thermal Effects, -6 Illumination & Light in
  Buildings, -7 Sound in Buildings, -8 Sustainability, Passive House & U-Values
Part 3 — Building Science (construction-studies-2, the material-science topics examined on the written theory paper):
  -2 Building Science: Timber & Adhesives, -3 Building Science: Porosity & Durability, -4 Building Science: Aggregates &
  Concrete, -5 Building Science: Binders & Setting, -6 Building Science: Paints & Pigments, -7 Building Science: Water &
  Comfort, -8 Building Science: Heat, -9 Building Science: Light, -10 Building Science: Electricity, -11 Building Science:
  Acoustics
(Use Part 1 strands for construction detailing/services/thermal/sustainability; use the Building Science subtopics for
material questions — timber seasoning/defects/decay, concrete/aggregates, paints, adhesives.)
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert CONSTRUCTION STUDIES (Irish exam-recovery tool) — the WRITTEN
THEORY paper. A card teaches a student who lost marks how to recover them: a clear gist, the ONE highest-leverage move,
and a SELF-CONTAINED check + model answer. Construction Studies is a DRAWING-HEAVY subject — lean toward attaching a real
figure (see figureSpec) whenever a topic is a construction detail/section/junction.

EXAM SHAPE (use real questionRefs): The Theory paper is 300 marks; candidates answer ANY FIVE questions (60 marks each),
3 hours. Q1 is usually the mandatory SCALE SECTION DRAWING ("To a scale of 1:10, draw a vertical section through…").
Other questions ask to "Discuss in detail, using notes and freehand sketches…". HIGHER and ORDINARY both exist (HL = code
A, OL = code G). Marking: drawings/sketches in pencil, labelled with the NAME, SIZES and DIMENSIONS of each material;
award points are LISTED construction details (e.g. for a cavity wall: larch cladding rainscreen, battens/counter-battens,
cavity wall blockwork & wall ties, full-fill insulation, cavity closer, wall plate, DPC). U-value questions want the
formula U = 1/ΣR (ΣR = Σ thickness/conductivity, + surface resistances) — RECOMPUTE any number.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Construction Studies questions + marking schemes. Text of all
papers + schemes (2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): construction-studies-YYYY-{HL,OL}-written.txt and
construction-studies-YYYY-{HL,OL}-marking-scheme.txt. grep/Read for the exact question + the scheme's bulleted award
points. Do NOT invent question numbers, marks, scheme wording, materials, dimensions, or U-values. RECOMPUTE every U-value.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'cons-', unique, includes the topic (e.g. 'cons-cavity-wall-dpc-hl')
  subjectId     MUST be exactly 'construction-studies'
  topicId       one of the valid ids above
  subjectLabel  'Construction Studies'
  topicLabel    the curriculum subtopic's EXACT name (syllabus-aligned — see TOPICS)
  focus         short row label disambiguating same-subtopic cards (e.g. 'Cavity wall: DPC position & function')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core technique/detail + how the exam tests it. Plain, supportive, precise. Name real
                materials/dimensions (e.g. '100 mm full-fill insulation', 'DPC 150 mm above finished ground level').
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks (a specific detail, not filler)
  check         { prompt (SELF-CONTAINED — a conceptual recall/explain/calculate question answerable from the card + the
                  figure if present; NOT "draw X" which can't be self-marked here. For U-values embed the layers +
                  conductivities inline), modelAnswer (full answer; for a calc, the worked U = 1/ΣR), needed (>=2 award
                  points/details a full answer lists) }
  source        'Topic … — SEC LC Construction Studies {YEAR} {LEVEL}, Q… + marking scheme (…the scheme award points…)'
  marksWeight   integer marks at stake (from the scheme; a full question is 60, a part is less)
  figureSpec    Include whenever the topic is a construction DETAIL/SECTION/JUNCTION or the question shows/expects a
                drawing — DEFAULT TO INCLUDING IT when in doubt (user rule: show the figure for context). Shape:
                { year, level, questionRef, source ('scheme' if the model exemplar drawing in the marking scheme, or
                'paper' if a diagram printed in the question), describes (what the drawing shows in detail — the section/
                junction + the labelled parts), whyNeeded }. DO NOT put a real 'figure'/'src' — the crop does not exist
                yet; the main loop renders the page, views it, crops the exemplar, and attaches it.

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge + the figure (if figureSpec
present). Never silently depend on an unseen drawing — attach a figureSpec or embed the detail in the prompt.

QUALITY BAR: oneMove names a SPECIFIC construction move/error (e.g. 'the DPC must lap the DPM to make the damp barrier
continuous', 'wall ties slope DOWNWARD to the outer leaf so water drains out', 'put the vapour-control layer on the WARM
side of the insulation to stop interstitial condensation', 'rafters bird-mouthed over the wall plate'). BANNED filler:
'read the question', 'manage your time', 'show your working', 'draw neatly'. Plain text; unicode (×, °, ², Ω, ≤) fine.

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
  { key: 'substructure', strands: 'construction-studies-0-1 (Substructure)',
    topics: 'strip/raft/pad foundations, the DPC (position 150mm above ground, function) and DPM and how they lap to form a continuous barrier, rising damp, radon barrier/sump, hardcore & blinding, sub-floor (solid ground floor build-up, insulation under/over slab), sites & setting out. Most are section details → add figureSpec.' },
  { key: 'superstructure-roofs', strands: 'construction-studies-0-2 (Superstructure)',
    topics: 'the cavity wall (outer/inner leaf, full-fill vs partial-fill insulation, wall ties sloping outward, cavity closer, wall plate), external wall finishes/rainscreen, floors (solid vs suspended timber, joists), pitched & lean-to ROOFS (rafters, wall plate & bird-mouth, ridge, eaves: fascia/soffit/gutter, slate/tile + battens + breather membrane, roof ventilation), verge. Heavily visual → figureSpec on nearly all.' },
  { key: 'internal-services-drainage', strands: 'construction-studies-0-3 (Internal Construction), construction-studies-0-4 (Services, External Works & Drainage)',
    topics: 'internal partitions (stud/block), stairs (going/rise/pitch), first & second fixing; cold & hot water supply, central heating, the drainage system (gully, inspection chamber/manhole, the trap/water seal, septic tank & percolation area), surface-water vs foul drainage, electricity supply & the consumer unit. Add figureSpec for drainage/stair details.' },
  { key: 'thermal-sustainability', strands: 'construction-studies-0-5 (Heat & Thermal Effects), construction-studies-0-8 (Sustainability, Passive House & U-Values)',
    topics: 'the U-VALUE CALCULATION (U = 1/ΣR, ΣR = Σ thickness/conductivity + Rsi + Rso) — embed the layers inline and RECOMPUTE; heat loss; surface vs INTERSTITIAL condensation, the dew point, the vapour-control layer on the warm side; insulation types; airtightness (<0.6 ACH @50Pa passive house), thermal bridging/cold bridge; passive house (MVHR heat recovery); renewables (heat pump COP, solar PV vs solar thermal). Mix of CALC cards (self-contained) + detail cards (figureSpec).' },
  { key: 'light-sound-building-science', strands: 'construction-studies-0-6 (Illumination & Light), construction-studies-0-7 (Sound), construction-studies-2-2..-11 (Building Science)',
    topics: 'daylight/illumination & rooflights; sound insulation (airborne vs impact, flanking transmission); BUILDING SCIENCE materials — TIMBER (seasoning, moisture content, defects: shakes/warping, decay: wet/dry rot fungal + woodworm insect attack, preservation), CONCRETE (cement+fine+coarse aggregate+water, water-cement ratio, curing, reinforcement & why steel), paints (primer/undercoat/topcoat), adhesives. Material cards are mostly self-contained; add figureSpec where a defect/section is shown.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 6 cards: aim for ~4 Higher + ~2 Ordinary, spread across DIFFERENT subtopics and years. Favour high-frequency, high-mark questions. Read the relevant ${TXT}/ files; ground every detail/award-point in the scheme; recompute any U-value. Add a figureSpec for every card whose topic is a construction detail/section/drawing (default to including it). Each card's topicLabel MUST be the exact curriculum subtopic name.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards (${cards.filter((c) => c.figureSpec).length} with figureSpec)`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'accurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, accurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; preserve/repair figureSpec). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Construction Studies Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question near "${c.source}"? Do the marks + the scheme's bulleted award points match the scheme text? else grounded:false.\n` +
    `2. ACCURACY: any construction error (wrong DPC position, wrong wall-tie slope, vapour layer on wrong side, wrong material/dimension, a U-value that does not recompute as U=1/ΣR)? RECOMPUTE any U-value. else accurate:false.\n` +
    `3. SELF-CONTAINMENT: answerable from the card + general knowledge + the figure (if figureSpec)? If it silently needs an unseen drawing and has no figureSpec → selfContained:false (fix by adding figureSpec or embedding the detail).\n` +
    `4. FIGURE JUDGEMENT: if the topic is a construction detail/section and there is NO figureSpec, add one (show-when-in-doubt). If a figureSpec is present, is its year/level/questionRef/source real and does the described drawing exist in that paper/scheme?\n` +
    `5. SYLLABUS ALIGNMENT: is topicId valid and is topicLabel the exact curriculum subtopic name? else fix.\n` +
    `6. QUALITY: oneMove a specific construction move (no banned filler)? needed[] real award points?\n` +
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
  `Completeness critic for a Construction Studies Catch-Up Lane set (Irish LC written theory paper). The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec, marks: k.marksWeight })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) strand spread across Substructure, Superstructure/Roofs, Internal/Services/Drainage, Heat & Thermal/Sustainability, Light/Sound, and Building Science (timber/concrete/etc.) — flag thin areas, (3) whether the signature topics are present: a U-VALUE calculation, the cavity-wall section, a roof/eaves detail, interstitial condensation/vapour layer, a drainage detail, timber decay, (4) figureSpec coverage — for a drawing-heavy subject most detail cards SHOULD have one; flag detail cards lacking a figureSpec. List concrete gap slots to top up (each: level + topicId + focus + whether a figure is needed).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
