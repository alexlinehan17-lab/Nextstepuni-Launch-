export const meta = {
  name: 'jc-history-catchup',
  description: 'Author + adversarially verify Junior Cycle History (Common Level) Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, historical accuracy' },
    { title: 'Critic', detail: 'completeness + strand balance' },
  ],
}

const TXT = '/tmp/jc_history_txt'

const TOPICS = `
VALID jc-history topicIds (the VERIFIED taxonomy — 3 strands, all examinable). topicId MUST be one; topicLabel the EXACT name.
The nature of history (jc-history-0 — the working-with-evidence SKILLS, examined throughout):
  -0 Working with sources and evidence (primary vs secondary, usefulness and limitations), -1 Detecting bias and
  propaganda; fact, opinion and viewpoint, -2 Reading visual sources: photos, cartoons, posters, maps and statistical
  tables, -3 Chronology, time and space: timelines, eras and date patterns, -4 Cause and consequence, -5 Change and
  continuity, -6 Historical significance: why people, events and places are remembered, -7 Historical empathy and seeing
  the past from more than one perspective, -8 The job of the historian, archaeology and dating the past, -9 Repositories
  of evidence: museums, archives, libraries and the census, -10 The big picture: connecting people, issues and events
  across eras
The history of Ireland (jc-history-1):
  -0 Early Christian Ireland: monasteries, art and the influence of Christianity, -1 Settlement and plantation, and their
  impact on Irish identity, -2 The Great Famine and the Irish Diaspora, -3 The parliamentary tradition: Irish political
  leaders and Home Rule, -4 The physical force tradition and pre-twentieth-century rebellion (e.g. 1798), -5 Nationalism,
  unionism and the struggle for independence, 1911-1923 (1916 Rising, War of Independence, Civil War), -6 The impact of
  the World Wars on Irish people, -7 How women's lives changed in twentieth-century Ireland, -8 A sporting, cultural or
  social movement in Irish life (e.g. the GAA), -9 The Northern Ireland Troubles and North-South / Anglo-Irish relations,
  -10 The 1960s as a decade of change in Ireland, -11 Ireland's links with Europe and the European Union, -12 Local,
  personal and family history and its wider connections
The history of Europe and the wider world (jc-history-2):
  -0 Early people and an ancient or medieval civilisation (e.g. Egypt, Rome), -1 Life and death in medieval times,
  -2 The Renaissance: change in the arts and science, -3 The Reformation and the actions of one Reformer, -4 Exploration,
  conquest and colonisation (Portuguese and Spanish), -5 A revolution in pre-twentieth-century Europe or the wider world
  (e.g. American, French), -6 Technology and innovation as drivers of historical change (incl. the Industrial Revolution),
  -7 World War One or World War Two: causes, course and impact, -8 Dictatorship in the twentieth century: life in a
  fascist and a communist country, -9 Genocide and the Holocaust, -10 The Cold War in international relations,
  -11 International co-operation: the European Union and the United Nations, -12 The 1960s as a decade of change in Europe
  and the wider world, -13 Patterns of change over time in a chosen theme (crime and punishment, food and drink, work and
  leisure, fashion, health and medicine)
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE HISTORY (Ireland, reformed NCCA spec, first examined 2019). A
card helps a student who fell behind recover the marks: a clear gist of the concept/skill/topic, the ONE highest-leverage
move (or classic error), and a SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 360 marks, ~2 hours,
8 questions (a mix of SOURCE-based and content questions). Each year samples a subset of the syllabus. The WORKING-WITH-
EVIDENCE skills (sources, bias/propaganda, cartoons/photos, chronology, cause & consequence) appear in nearly every
question. EVERY card's level MUST be 'common'.
SEC MARKING (ground traps in it): short answers have set accepted points; developed answers need DEVELOPMENT (a stated
point + explanation/example). Key consequences a card can teach: a source-usefulness answer must say usefulness AND a
limitation; a "primary source" must be from the time (an eyewitness/artefact) not a textbook; reading a CARTOON means
naming the symbol AND what it represents AND the cartoonist's attitude; "cause" vs "consequence" must be the right
direction; a developed historical point = a fact PLUS its significance/explanation; a NAMED example (a real person/event/
place) is often a separate mark.

GROUNDING (non-negotiable): ground every card in REAL SEC JC History questions + marking schemes at ${TXT}/ —
jc-history-YYYY-CL-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled 2020-2021).
grep/Read for the real question + the scheme's accepted answers. Do NOT invent question numbers, marks, or scheme wording.

HISTORICAL ACCURACY (hard rule): every fact, name, date and event must be CORRECT and within JC scope (no Leaving-Cert
depth — no LC documents-question framing, no LC case-study detail). For a SKILLS card the method (primary vs secondary,
how to read a cartoon, cause vs consequence) must be exactly right.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jchist-', unique (e.g. 'jchist-primary-vs-secondary-source')
  subjectId     MUST be exactly 'jc-history'
  topicId       one of the valid ids above
  subjectLabel  'History (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Primary vs secondary: from the time, or about it later?')
  level         MUST be 'common'
  gist          2-5 sentences: the concept/skill/topic + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC history move, e.g. 'a primary source
                comes FROM the time you are studying (an eyewitness, a photo, an artefact); a secondary source is made
                LATER about it (a textbook, a documentary)', 'to read a cartoon, name the symbol, say what it stands for,
                then state the cartoonist\'s attitude', 'a cause comes BEFORE the event; a consequence comes AFTER')
  check         { prompt (SELF-CONTAINED — for a source/skills card embed a SHORT source extract or describe the
                  cartoon/photo in words; for a content card give the scenario), modelAnswer (the full correct answer),
                  needed (>=2 award points = the marking points) }
  source        'Topic … — SEC JC History {YEAR} CL, Q… + marking scheme (…accepted answers…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card alone — embed any source extract / describe any
cartoon/photo in words and give the facts needed. modelAnswer states the correct history.

QUALITY BAR: oneMove names a SPECIFIC history concept, skill method or marking behaviour. BANNED filler: 'read the
question', 'manage your time', 'learn the dates', 'revise the topic'.

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
  { key: 'nature-of-history', strand: 'jc-history-0 (The nature of history — working-with-evidence skills, the most-examined)',
    topics: 'PRIMARY vs SECONDARY sources (from the time vs made later) + usefulness AND limitations of a source, detecting BIAS & PROPAGANDA (fact vs opinion vs viewpoint, why a source is one-sided), reading VISUAL sources — CARTOONS (name the symbol, what it stands for, the cartoonist\'s attitude), photos, posters, maps, statistical tables, CHRONOLOGY & time (timelines, eras BC/AD, centuries, ordering events, calculating elapsed years), CAUSE & CONSEQUENCE (before vs after), CHANGE & CONTINUITY, historical SIGNIFICANCE, EMPATHY/perspectives, the JOB OF THE HISTORIAN & ARCHAEOLOGY/dating, and REPOSITORIES (museums, archives, the CENSUS). High-frequency, easy marks lost on method.' },
  { key: 'history-of-ireland', strand: 'jc-history-1 (The history of Ireland)',
    topics: 'EARLY CHRISTIAN IRELAND (monasteries, manuscripts/high crosses, the spread of Christianity), SETTLEMENT & PLANTATION & its impact on identity, the GREAT FAMINE & the Diaspora (causes, effects, emigration), the PARLIAMENTARY tradition & HOME RULE (O\'Connell, Parnell, Redmond, Carson — leaders & methods), the PHYSICAL FORCE tradition (1798), the STRUGGLE FOR INDEPENDENCE 1911-1923 (the 1916 Rising, War of Independence, Civil War, key figures), the WORLD WARS\' impact on Irish people, WOMEN\'S lives in 20th-C Ireland, a SPORTING/CULTURAL movement (the GAA), the NORTHERN IRELAND Troubles, the 1960s in Ireland, and Ireland & the EU. Named people/events/dates matter.' },
  { key: 'europe-wider-world', strand: 'jc-history-2 (The history of Europe and the wider world)',
    topics: 'an ANCIENT/MEDIEVAL civilisation (Rome/Egypt — daily life, sources like Vindolanda), LIFE & DEATH in MEDIEVAL times, the RENAISSANCE (art & science change — Leonardo, Michelangelo, the printing press), the REFORMATION (Martin Luther, causes & effects), EXPLORATION/conquest/COLONISATION (Columbus, the Portuguese & Spanish, consequences for native peoples), a pre-20th-C REVOLUTION (American/French), TECHNOLOGY & the INDUSTRIAL REVOLUTION, WORLD WAR ONE/TWO (causes/course/impact), DICTATORSHIP (life in Nazi Germany / Stalin\'s USSR, propaganda, collectivisation), GENOCIDE & the HOLOCAUST, the COLD WAR, the EU/UN, and the 1960s in the wider world. Named people/events/dates matter.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrand: ${c.strand}\nTopics to mine: ${c.topics}\n\nProduce ${c.key === 'nature-of-history' ? 8 : 7} cards spread across DIFFERENT subtopics and DIFFERENT years (all level 'common'). Ground each in a real question + its marking scheme. topicLabel MUST be the exact curriculum subtopic name. Every fact/name/date must be correct and within JC scope.`,
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
    `Independent SKEPTIC verifying ONE Junior Cycle History (Common Level) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. HISTORICAL ACCURACY: is every fact, name, date and event CORRECT and within JC scope (no LC-only depth)? For a SKILLS card CHECK THE METHOD: primary = from the time / secondary = made later; cartoon-reading = symbol + meaning + attitude; cause = before, consequence = after; source usefulness needs a limitation too. If wrong → fix (or reject if unsalvageable).\n` +
    `2. GROUNDING: real question/section near "${c.source}" (2022-2025)? marks + accepted answers match the scheme?\n` +
    `3. SELF-CONTAINMENT: answerable from the card alone (any source extract / cartoon described in words + facts embedded)?\n` +
    `4. LEVEL: is level exactly 'common'? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific history move/method (no filler)?\n` +
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
  `Completeness critic for a Junior Cycle History (Common Level) Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) coverage across all THREE strands — The nature of history (MUST be strong — its skills are examined throughout), The history of Ireland, The history of Europe and the wider world — flag thin areas, (2) whether the signature high-frequency topics appear: primary vs secondary source, source usefulness+limitation, bias/propaganda, cartoon reading, chronology, cause & consequence; Early Christian Ireland, plantations, the Famine, Home Rule, 1916/independence, the GAA, the Troubles; the Renaissance, Reformation, exploration/colonisation, a revolution, the Industrial Revolution, the World Wars, dictatorship, the Holocaust, the Cold War, (3) whether the signature MARKING traps are present (primary-from-the-time, usefulness-needs-a-limitation, cartoon symbol+attitude, cause-vs-consequence direction, developed-point-needs-explanation, named-example-required), (4) any duplicate focus. List concrete gap slots (each: topicId + focus). All cards are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
