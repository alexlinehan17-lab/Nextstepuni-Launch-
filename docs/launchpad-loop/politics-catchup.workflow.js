export const meta = {
  name: 'politics-catchup',
  description: 'Author + adversarially verify Politics & Society Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, fact accuracy, self-containment' },
    { title: 'Critic', detail: 'completeness + level/strand balance' },
  ],
}

const TXT = '/tmp/politics_txt'

const TOPICS = `
VALID politics-and-society topicIds (the VERIFIED taxonomy — 4 strands / 42 subtopics, confirmed against the official NCCA
spec 2026-06-10). topicId MUST be one; topicLabel MUST be the curriculum subtopic's EXACT name.
Strand 1 Power and decision-making (politics-and-society-0): -0 Power in the School, -1 The Need for Rules, -2 Dimensions
  of Power, -3 Effects of Rules, -4 Making National Policy, -5 Selecting the Executive, -6 Social Class and Gender,
  -7 Arguments on Representation, -8 Effectiveness of Representation, -9 Media, Public Opinion and Democracy, -10 Key Thinkers
Strand 2 Active citizenship (politics-and-society-1): -0 Positive Contributions, -1 Starting an Initiative, -2 Means of
  Taking Action, -3 Setting and Achieving Goals, -4 Developing Personal Qualities, -5 Self-Appraisal and Feedback,
  -6 Freedom of Expression, -7 Listening and Communicating, -8 Resolving Conflicts, -9 Evaluating Information, -10 Democracy
  in Wider Society
Strand 3 Human rights and responsibilities (politics-and-society-2): -0 Rights of Young People, -1 Human Rights Principles,
  -2 Equality and Rights, -3 Arguments About Rights, -4 State Bodies for Rights, -5 The Right to Education, -6 Key Thinkers,
  -7 Rights in the Wider World, -8 Arguments on Global Rights, -9 International Cooperation
Strand 4 Globalisation and localisation (politics-and-society-3): -0 National Identity, -1 Diversity and Cultural Change,
  -2 Diversity in the EU, -3 Understanding Identity, -4 West and Non-West Culture, -5 Globalisation and Power, -6 Key
  Thinkers, -7 Acting for Sustainable Development, -8 Arguments on Sustainability, -9 Key Thinkers (Sustainability)
(Use the closest valid id; if a card is exam-technique it still tags the strand/topic it teaches.)
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert POLITICS & SOCIETY (Irish exam-recovery tool) — the WRITTEN paper.
A card teaches a student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a
SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): written paper 400 marks (80%; plus a 20% citizenship project). Section A Short Answer
Questions (50 marks; answer 10 of 15 — precise factual/short answers). Section B Data-based Questions (150 marks; read +
interpret a data dashboard/source and apply concepts). Section C Discursive Essays (200 marks; answer 2 of 5 @100 — a
structured argument). SIGNATURE: top essays cite a relevant KEY THINKER (the spec's "participants in these debates", e.g.
Marx, Weber, Arendt, Beauvoir, Locke, Rawls, Sen) and give a BALANCED argument with evidence + a clear conclusion.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Politics & Society questions + marking schemes at ${TXT}/ —
politics-and-society-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===). grep/Read for the real question + the
scheme's indicative content / marking guidance. Do NOT invent question numbers, marks, scheme wording, thinkers, dates,
institutions or facts. Politics facts MUST be accurate (PR-STV, the Oireachtas/Dáil/Seanad, the UDHR 1948, IHREC, the UN,
the SDGs, named thinkers and their ideas) — ground them, never guess.

LEVEL PURITY (hard rule): a card's level MUST match the level of the paper its question is on. An OL card from an OL
question, an HL card from an HL question — never put an HL question in the OL section.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'pas-', unique (e.g. 'pas-pr-stv-counting-hl')
  subjectId     MUST be exactly 'politics-and-society'
  topicId       one of the valid ids above
  subjectLabel  'Politics & Society'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'PR-STV: the quota + transfers')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the concept/technique + how the exam tests it. Plain, supportive, precise. Accurate names/facts.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC P&S move, e.g. 'a discursive essay
                must NAME a key thinker and use their idea, not just assert', 'in a data question quote the actual figure
                from the source, do not generalise', 'PR-STV reaches the quota by transferring surplus + eliminated votes')
  check         { prompt (SELF-CONTAINED — for an essay-skill card ask for the structure/points/the key thinker, not a
                  full essay; for a data card embed the small data inline), modelAnswer, needed (>=2 award/indicative points) }
  source        'Topic … — SEC LC Politics & Society {YEAR} {LEVEL}, Section …, Q… + marking scheme (…indicative content…)'
  marksWeight   integer marks at stake (Section A item ~5; Section B part; a Section C essay 100)
  figureSpec    Include ONLY if a Section B card genuinely needs a specific printed data chart/dashboard the student reads.
                Shape { year, level, questionRef, source ('paper'|'scheme'), describes, whyNeeded }. Most cards are text —
                do NOT force one.

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge + the figure (if figureSpec).

QUALITY BAR: oneMove names a SPECIFIC P&S move/fact. BANNED filler: 'read the question', 'manage your time', 'give your
opinion'. Plain text; unicode fine.

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
  { key: 'power-decision-making', strands: 'politics-and-society-0 (Power and decision-making)',
    topics: 'how power works + Irish political institutions: dimensions/sources of power, the need for rules; making national policy, the Oireachtas (Dáil/Seanad), how the executive (Taoiseach/government) is selected, PR-STV (the quota, surplus + eliminated transfers, proportionality), representation arguments + effectiveness, social class & gender in politics, media & public opinion in a democracy, and a Strand-1 key thinker (e.g. Weber on authority, Marx on class power, Arendt).' },
  { key: 'active-citizenship', strands: 'politics-and-society-1 (Active citizenship)',
    topics: 'the active-citizenship / citizenship-project content: making positive contributions, starting an initiative, means of taking action (local/national/international), setting + achieving goals and action plans, developing personal qualities, self-appraisal & feedback; rights in communication — freedom of expression in groups, listening & communicating, resolving conflicts, evaluating information, and how small-group democracy relates to wider society.' },
  { key: 'human-rights', strands: 'politics-and-society-2 (Human rights and responsibilities)',
    topics: 'human rights content + facts: rights of young people, human rights PRINCIPLES (universal, inalienable, indivisible), equality and rights, arguments about rights (individual vs collective, rights vs responsibilities), Irish state bodies (IHREC), the right to education; in the wider world — the UDHR (1948), the UN, the refugee crisis as a rights issue, international cooperation, and a human-rights key thinker (e.g. Locke, Arendt, Sen, Nussbaum).' },
  { key: 'globalisation-sustainability', strands: 'politics-and-society-3 (Globalisation and localisation)',
    topics: 'globalisation, identity & sustainability: representations of national identity, diversity & cultural change, diversity in the EU, understanding identity, interaction of western & non-western culture, globalisation & political power, and SUSTAINABLE DEVELOPMENT (the UN SDGs, arguments on sustainability, climate action) + a key thinker (e.g. on globalisation/identity).' },
  { key: 'exam-technique', strands: 'spread across strands (tag the topic each teaches)',
    topics: 'the exam-skill cards: Section A short-answer PRECISION (exact term/definition, no waffle); Section B DATA interpretation (quote the actual figure from the source, describe the trend, then apply a concept — do not generalise away from the data); Section C DISCURSIVE ESSAY structure — a clear position, BALANCED both-sides argument, EVIDENCE/examples, a NAMED KEY THINKER and their idea, and a reasoned conclusion (the single biggest mark-winner students miss is the key thinker + balance).' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 5 cards: aim for 3 Higher + 2 Ordinary, spread across DIFFERENT subtopics/years. Ground every fact in the scheme/paper. topicLabel MUST be the exact curriculum subtopic name. LEVEL PURITY: an OL card from an OL question only.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'factsAccurate', 'selfContained', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, factsAccurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; valid topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Politics & Society Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question/section near "${c.source}"? marks + scheme indicative content match?\n` +
    `2. FACT ACCURACY (critical): every politics fact correct — institutions (Dáil/Seanad/IHREC/UN), PR-STV mechanics, the UDHR 1948, the SDGs, named key thinkers + their actual ideas, dates? Any wrong fact → factsAccurate:false and fix.\n` +
    `3. LEVEL PURITY: is the source paper actually ${c.level}? An OL card sourced from an HL paper (or vice versa) → levelPure:false, fix the level.\n` +
    `4. SELF-CONTAINMENT: answerable from the card + general knowledge + figure (if figureSpec)? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific P&S move (no filler)? For essay cards, does it require the KEY THINKER + balance?\n` +
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
log(`Verify: ${kept.length}/${cards.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a Politics & Society Catch-Up Lane set (Irish LC). The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) coverage across the 4 strands (Power/decision-making, Active citizenship, Human rights, Globalisation/sustainability) + exam technique — flag thin strands, (3) whether the signature topics are present: PR-STV, the UDHR/human-rights principles, the SDGs/sustainability, a Section B data-interpretation skill, a Section C discursive-essay-structure card that requires a KEY THINKER, and at least one named key thinker per relevant strand, (4) any duplicate focus. List concrete gap slots (each: level + topicId + focus).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
