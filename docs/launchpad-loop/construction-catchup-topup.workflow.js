export const meta = {
  name: 'construction-catchup-topup',
  description: 'Fill CS Catch-Up gaps: OL timber decay, OL condensation, OL sound, OL drainage, HL interstitial condensation/dew-point',
  phases: [
    { title: 'Author', detail: 'one targeted card per gap slot' },
    { title: 'Verify', detail: 'skeptic checks grounding, accuracy, self-containment' },
  ],
}

const TXT = '/tmp/construction_txt'

const SHARED = `
Authoring ONE Catch-Up Lane RECOVERY CARD for Leaving Cert CONSTRUCTION STUDIES (written theory paper). A card teaches a
student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a SELF-CONTAINED check +
model answer.

GROUNDING (non-negotiable): ground in REAL SEC LC Construction Studies questions + schemes at ${TXT}/ —
construction-studies-YYYY-{HL,OL}-written.txt / -marking-scheme.txt (pages ===PAGE n===). grep/Read for the real
question + the scheme's bulleted award points. Do NOT invent question numbers, marks, materials, dimensions or wording.

EXAM SHAPE: Theory paper — HIGHER 300 marks (answer any 5, 60 each); ORDINARY 200 marks (answer any 4, 50 each). Drawings/
sketches in pencil, labelled with material NAMES + sizes/dimensions. Award points are LISTED construction details.

THE CARD (schema "card"): id (kebab, 'cons-' prefix, unique, topic in it), subjectId='construction-studies',
topicId (EXACTLY the slot's valid id), subjectLabel='Construction Studies', topicLabel (the curriculum subtopic's EXACT
name — see slot), focus (short disambiguating label), level ('higher'|'ordinary'), gist (2-5 sentences, real materials/
dimensions), oneMove {label,text} (specific construction move/error), check {prompt (SELF-CONTAINED conceptual recall/
explain — NOT "draw X"), modelAnswer, needed (>=2 award points)}, source ('Topic … — SEC LC Construction Studies {YEAR}
{LEVEL}, Q… + marking scheme (…award points…)'), marksWeight (int), figureSpec OPTIONAL { year, level, questionRef,
source ('scheme'|'paper'), describes, whyNeeded } — include if the topic is a detail/diagram a student should SEE (default
to including for a construction detail; the main loop crops it). No real 'figure'/'src'.

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge + the figure (if figureSpec).

QUALITY: oneMove names a SPECIFIC construction move/error. BANNED filler: 'read the question','manage your time','show
your working','draw neatly'. Plain text; unicode (×,°,²,≤) fine. Return data only; never edit a file.
`

const CARD_SCHEMA = {
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
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const SLOTS = [
  { key: 'ol-timber-decay', level: 'ordinary', topicId: 'construction-studies-2-2', topicLabel: 'Building Science: Timber & Adhesives',
    topic: 'TIMBER DECAY/DEFECTS (a Building Science staple currently ABSENT). Wet rot vs DRY ROT (the fungus, the >20% moisture it needs, why dry rot is more serious — spreads through masonry, dry conditions after), woodworm/insect attack, moisture content & seasoning, and PREVENTION (keep timber dry/ventilated, preservative treatment). Self-contained recall check.' },
  { key: 'ol-condensation', level: 'ordinary', topicId: 'construction-studies-0-5', topicLabel: 'Heat & Thermal Effects',
    topic: 'SURFACE CONDENSATION at OL — where it forms (cold surfaces/cold bridges, poorly ventilated rooms like bathrooms/kitchens, behind furniture on cold walls), the problems (mould, damage), and the THREE preventions: adequate ventilation, adequate heating, adequate insulation. Self-contained.' },
  { key: 'ol-sound', level: 'ordinary', topicId: 'construction-studies-0-7', topicLabel: 'Sound in Buildings',
    topic: 'SOUND INSULATION at OL — reducing AIRBORNE vs IMPACT sound through a party wall or intermediate floor (mass/density, isolation/discontinuity, absorbent quilt, resilient/floating floor, soft floor finish). One real OL question + scheme. Self-contained.' },
  { key: 'ol-drainage', level: 'ordinary', topicId: 'construction-studies-0-4', topicLabel: 'Services, External Works & Drainage',
    topic: 'A DRAINAGE detail at OL — the inspection chamber/manhole (purpose: access for cleaning/rodding at changes of direction), OR the back-inlet gully / the trap & water seal (stops foul air/smells entering), OR house foul vs surface-water drainage. One real OL question + scheme. figureSpec likely.' },
  { key: 'hl-interstitial-condensation', level: 'higher', topicId: 'construction-studies-0-5', topicLabel: 'Heat & Thermal Effects',
    topic: 'INTERSTITIAL CONDENSATION / DEW POINT at HL (signature topic, currently only the vapour-layer card). Explain WHERE in the wall build-up the dew point falls, why warm moist air diffusing out condenses when it meets a surface below dew point inside the construction, and the fix: VAPOUR-CONTROL LAYER on the WARM side of the insulation + a ventilated outer cavity to carry moisture away. Self-contained reasoning check.' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED topicId: ${s.topicId}\nREQUIRED topicLabel: ${s.topicLabel}\nLEVEL: ${s.level}\nTASK: ${s.topic}\n\nReturn exactly one grounded, self-contained card for this slot with topicId='${s.topicId}'.`,
    { label: `author:${s.key}`, phase: 'Author', schema: CARD_SCHEMA },
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
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id + same topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Construction Studies Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question + scheme award points behind the claim? else grounded:false.\n` +
    `2. ACCURACY: any construction error (e.g. dry rot needs DRY not wet conditions? — dry rot needs damp/>20% MC then spreads in drier conditions; wrong prevention; wrong sound principle; dew point logic)? else accurate:false.\n` +
    `3. SELF-CONTAINMENT: answerable from the card + general knowledge + figure (if figureSpec)?\n` +
    `4. SYLLABUS ALIGNMENT: topicId is '${c.topicId}' and topicLabel the exact curriculum subtopic name?\n` +
    `5. QUALITY: oneMove specific (no filler)? needed[] real award points?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (same id + topicId). If sound, accept. If irredeemable, reject.\n\n` +
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
