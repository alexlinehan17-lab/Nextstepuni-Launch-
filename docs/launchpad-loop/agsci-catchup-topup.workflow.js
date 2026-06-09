export const meta = {
  name: 'agsci-catchup-topup',
  description: 'Fill AgSci Catch-Up gaps: stocking-rate calc, Scientific Practices depth, HL diagram/data, OL genetics, grassland/fertiliser',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic refutes + recomputes/fact-checks each' },
  ],
}

const TXT = '/tmp/agsci_txt'

const TOPICS = `Valid agricultural-science topicIds (NEW SPEC): agricultural-science-0-* (Scientific Practices: -0 Hypothesising, -1 Experimenting, -2 Evaluating Evidence, -3 Communicating, -4 Working Safely),
agricultural-science-1-* (Soils: -0 Formation/Classification, -1 Properties, -2 Chemical, -3 Physical, -4 Biological, -5 Management),
agricultural-science-2-* (Crops: -0 Plant Physiology, -1 Classification/ID, -2 Production, -3 Establishment, -4 Management, -5 Harvesting),
agricultural-science-3-* (Animals: -0 Physiology, -1 Classification/ID, -2 Production, -3 System/Enterprise, -4 Management, -5 Husbandry/Health). Card strand = topicId minus last -N.`

const SHARED = `
You author ONE Catch-Up Lane RECOVERY CARD for Leaving Cert AGRICULTURAL SCIENCE (NEW spec, examined 2021+). A card
teaches a student who lost marks how to recover them: clear gist, the ONE highest-leverage move, a check + model answer.

GROUNDING: ground in a REAL SEC LC Agricultural Science question + scheme at ${TXT}/ (pages ===PAGE n===):
agricultural-science-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact question + award points. Do NOT
invent wording/marks/scheme content. RECOMPUTE any calculation and confirm it matches the scheme.

${TOPICS}

CARD FIELDS: id (kebab, 'agsci-' prefix, includes topic), subjectId='agricultural-science', topicId (valid id),
subjectLabel='Agricultural Science', topicLabel (short), focus (short row label), level ('higher'|'ordinary'),
gist (2-5 sentences), oneMove {label, text} (specific ag-science move/error — not filler),
check {prompt (self-contained), modelAnswer (full), needed (>=2 award-point strings)},
source ('Topic … — SEC LC Agricultural Science {YEAR} {LEVEL}, Q… + marking scheme (…)'), marksWeight (int).
figureSpec OPTIONAL { year, level, questionRef, describes, whyNeeded } — ONLY if the check needs a graph/diagram/data the
exam SHOWS to interpret. If the student DRAWS the diagram, no figure (teach how). Embed small data tables inline. No 'figure'/'src'.

QUALITY: oneMove names a specific move/error. BANNED filler: 'show your working','read the question','manage your time'.
Plain text; unicode (×,°,→) fine. Return data only; never edit a file.
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
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const SLOTS = [
  { key: 'stocking-rate-calc', level: 'higher',
    topic: 'A STOCKING RATE / livestock-units (LU) CALCULATION (agricultural-science-3-3 or 3-4) — explicitly expected, currently absent. Find a real question that gives animal numbers + land area (and LU equivalents) and asks for stocking rate (LU/ha) or grazing days. Embed the data inline; recompute and match the scheme.' },
  { key: 'scientific-practices-experiment', level: 'ordinary',
    topic: 'A SCIENTIFIC-PRACTICES experiment card (agricultural-science-0-1 Experimenting or 0-2 Evaluating Evidence) — strand is one card deep. A real named experiment method/procedure (e.g. % water in a soil sample, separating soil into horizons/sedimentation, testing for starch, measuring soil pH) OR interpreting results/reliability. OL preferred.' },
  { key: 'hl-diagram-or-data', level: 'higher',
    topic: 'An HL DIAGRAM/DATA-interpretation card — both existing diagram cards are OL. Find a real HL question with a SHOWN graph/diagram/data table (e.g. a growth-response or grass-growth curve, a labelled plant/root/flower diagram, a soil-water graph). Add a figureSpec for the shown visual; the prompt must interpret it.' },
  { key: 'ol-genetics-cross', level: 'ordinary',
    topic: 'An OL GENETICS cross/ratio card (agricultural-science-3-2 or 2-0) — genetics is currently HL-only. A real OL monohybrid cross / Punnett-square / dominant-recessive ratio question. Embed the data inline; teach the cross and the 3:1 (or 1:1) ratio.' },
  { key: 'grassland-fertiliser', level: 'ordinary',
    topic: 'A GRASSLAND / FERTILISER (N-P-K) card (agricultural-science-2-4 Crops:Management or 1-5 Soils:Management) — a major staple currently absent. A real question on grassland management (rotational grazing, reseeding, fertiliser application, slurry/N-P-K) or a fertiliser calculation. OL or HL.' },
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
  type: 'object', required: ['verdict', 'grounded', 'accurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, accurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, corrected card (same shape, same id). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Agricultural Science Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question matching "${c.source}"? marks + scheme answer + award points match? else grounded:false.\n` +
    `2. ACCURACY: recompute any calc (stocking rate/LU, ratio, %); any agricultural/scientific error? else accurate:false.\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (+figureSpec/embedded data)? else selfContained:false.\n` +
    `4. QUALITY: oneMove specific (no filler)? needed[] real award points? topicId valid?\n` +
    `If fixable, verdict:fix with a complete corrected card in fixedCard (keep id; preserve/repair figureSpec). If sound, accept. If fabricated, reject.\n\n` +
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
