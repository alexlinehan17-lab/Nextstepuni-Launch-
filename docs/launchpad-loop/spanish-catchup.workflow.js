export const meta = {
  name: 'spanish-catchup',
  description: 'Author + adversarially verify Spanish Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'topic clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic refutes + checks Spanish accuracy vs scheme' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/spanish_txt'

const TOPICS = `
VALID spanish topicIds. topicId MUST be one of these; card's strand = topicId minus its last -N.
spanish-0 Basic Communicative Proficiency: -0 Meeting People/Socialising, -1 Making Plans/Future Action, -2 Climate/Weather,
  -3 Travel/Transport, -4 Buying Goods/Services, -5 Emergencies, -6 Transactional Language/Role-Plays, -7 Expressing
  Feelings/Attitudes, -8 Managing a Conversation, -9 Engaging in Discussion, -10 Passing On Messages
spanish-1 Language Awareness: -0 Comprehending Target-Language Material (Aural and Reading), -1 Exploring Meaning,
  -2 Relating Language to Attitude, -3 Writing About Your Experience, -4 Consulting Reference Materials
spanish-2 Cultural Awareness: -0 Present-Day Target Culture, -1 Reading Modern Literary Texts (Section A Literature Option),
  -2 Everyday Life in the Community, -3 Relations With Ireland, -4 Cross-Cultural Issues, -5 Prescribed Literature and Film
  for Opinion Writing
GUIDANCE: grammar/tense/structure cards → spanish-1-3 (Writing About Your Experience). Comprehension-attack technique →
spanish-1-0 / spanish-1-1. Opinion/attitude writing → spanish-1-2. Written-production task formats (email, diary, note,
opinion) → spanish-1-3 or the relevant spanish-0-N functional topic. Culture/literature → spanish-2-0 / spanish-2-5.
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert SPANISH (Irish exam-recovery tool). A card teaches a student who
fell behind how to recover marks: a clear gist, the ONE highest-leverage move, and a self-marked check question + model
answer. The exam has two written papers per level plus aural + oral; YOUR cards target the WRITTEN paper skills (reading
comprehension technique, grammar/tenses, opinion writing, written production) and the underlying language knowledge.

EXAM SHAPE (use real questionRefs):
 - HIGHER written paper: Section A Reading Comprehension (70 marks; Q1 = EITHER (a) Prescribed Literature OR (b)
   Journalistic Text, Q2 a second comprehension), Section B Reading Comprehension + Opinion Writing (100 marks),
   Section C Written Production (50 marks). 220 marks total written.
 - ORDINARY written paper: Section A Reading Comprehension (160 marks; Q1-Q4), Section B Written Production (60 marks).
 - SEC MARKING GRAMMAR (ground demands/traps in it): lift-the-phrase / transcription answers need the EXACT words —
   "No marks awarded if words are added or omitted. Exact transcription required". Questions must be answered IN THE
   LANGUAGE INDICATED on the paper — Spanish-language questions get "No marks for answers in English"; English questions
   must be in English. Inference/opinion questions: "No marks awarded for answers supported by reference to the extract"
   (you must use your own words, not quote). Written Production / Opinion is marked on Communication (the message gets
   across) AND Language (accuracy of grammar/vocab/tense) — fluent waffle with broken verbs loses the Language marks.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Spanish papers + schemes. Text of all papers + schemes
(2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): spanish-YYYY-{HL,OL}-{written,aural,marking-scheme}.txt. grep/Read
for the real question + scheme answer. Do NOT invent question numbers, marks, or scheme wording. Every Spanish word,
accent, gender, and verb form you write MUST be correct — recheck conjugations, ser/estar, agreement, accents (á é í ó ú ñ ¿ ¡).

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'es-', unique, includes the topic (e.g. 'es-preterito-vs-imperfecto-hl')
  subjectId     MUST be exactly 'spanish'
  topicId       one of the valid ids above
  subjectLabel  'Spanish'
  topicLabel    short human label for the subtopic
  focus         short row label disambiguating same-subtopic cards (e.g. 'Pretérito vs imperfecto: event vs background')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core technique/rule + how the exam tests it. Plain, supportive, precise. Spanish
                examples with English glosses in brackets.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks
  check         { prompt (SELF-CONTAINED — embed any Spanish text/sentence the student needs right in the prompt; a
                  fill-the-gap, choose-the-form, or short-translation works well), modelAnswer (full answer with the
                  correct Spanish + a one-line why), needed (>=2 specific things a full answer includes) }
  source        'Topic … — SEC LC Spanish {YEAR} {LEVEL}, Q… + marking scheme (…the scheme point…)' (cite the real paper
                you grounded the technique/topic in; the grammar rule itself is general but tie it to where it is tested)
  marksWeight   integer marks the topic protects (from the scheme / section weighting)

SELF-CONTAINMENT (hard rule): the check prompt must be answerable from the card itself + general Spanish knowledge. For a
comprehension-technique card, embed a SHORT Spanish snippet (1-3 sentences) inline and ask them to apply the technique to
it. NEVER reference an unseen passage, literary text, or aural clip the student cannot see.

QUALITY BAR: oneMove names a SPECIFIC Spanish move/error (e.g. 'use SER for permanent identity/origin, ESTAR for
location and temporary states — "está muerto" not "es muerto"'; 'the pretérito is the completed event, the imperfecto is
the background/habit — "comía cuando llegó"'; 'after expressions of wish/emotion/doubt + que, switch to the subjunctive —
"quiero que vengas" not "vienes"'; 'POR = cause/duration/exchange, PARA = goal/destination/recipient'; 'on a lift question
copy the EXACT phrase — adding or dropping a word scores zero'). BANNED filler: 'read the question', 'manage your time',
'learn your vocab'. Plain text; Spanish accents/ñ/¿¡ and unicode fine.

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
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'grammar-tenses', topicHint: 'spanish-1-3',
    topics: 'core verb tenses students lose marks on: PRESENT (regular + key irregulars tener/ir/ser/estar/hacer), PRETÉRITO INDEFINIDO vs IMPERFECTO (completed event vs background/habit/description), the PERFECT (he hablado), the FUTURE and CONDITIONAL, and SER vs ESTAR. Each card = one contrast/rule with a fill-the-gap or choose-the-form check.' },
  { key: 'grammar-structures', topicHint: 'spanish-1-3',
    topics: 'high-frequency structures: the PRESENT SUBJUNCTIVE and its triggers (querer que, es importante que, cuando + future, ojalá), POR vs PARA, adjective + noun AGREEMENT and position, the PERSONAL "a", GUSTAR-type verbs (me gusta / me gustan / le interesa), object PRONOUNS and their placement, ACCENTS and ¿¡ punctuation. One rule per card with a self-contained check.' },
  { key: 'comprehension-technique', topicHint: 'spanish-1-0',
    topics: 'how to ATTACK the reading comprehension for marks: the lift-the-phrase / "Busca la frase" question (exact transcription, no added/omitted words), the synonym/vocabulary-matching question ("Encuentra la palabra que significa…"), the Verdadero/Falso + justify question (you MUST quote the justifying line), answering IN THE LANGUAGE INDICATED (Spanish question→Spanish answer, "no marks for English"), and the inference question where you may NOT quote the extract. Embed a short Spanish snippet inline so the check is self-contained.' },
  { key: 'written-production-and-opinion', topicHint: 'spanish-1-3',
    topics: 'the productive writing tasks: Section B OPINION WRITING (state + justify an opinion with connectors — en mi opinión, creo que, por un lado/por otro lado, sin embargo), and Section C / OL Section B WRITTEN PRODUCTION formats (informal email/message to a friend, a diary entry/note, reacting to a stimulus). Teach structure + the Communication-AND-Language marking. Cards can be technique-with-model rather than a specific unseen prompt.' },
  { key: 'culture-and-literature', topicHint: 'spanish-2-0',
    topics: 'the cultural/literature dimension: writing an opinion on the PRESCRIBED LITERATURE or FILM (Q1(a) literature option / opinion writing), and present-day Spanish-speaking culture knowledge students draw on. Keep checks self-contained (a technique + model, or a short embedded quote to react to) — NEVER require an unseen set text.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nDefault topicId (use the most accurate valid id per card): ${c.topicHint}\nTopics to mine: ${c.topics}\n\nProduce 5 cards: aim for 3 Higher + 2 Ordinary, spread across the topics, each a DIFFERENT subtopic/focus. Read the relevant ${TXT}/ files to ground the technique + cite a real question where it is tested. Every Spanish form must be correct.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'spanishCorrect', 'selfContained', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    spanishCorrect: { type: 'boolean' }, selfContained: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, topicId: { type: 'string' },
        subjectLabel: { type: 'string' }, topicLabel: { type: 'string' }, focus: { type: 'string' },
        level: { type: 'string' }, gist: { type: 'string' },
        oneMove: { type: 'object', properties: { label: { type: 'string' }, text: { type: 'string' } } },
        check: { type: 'object', properties: { prompt: { type: 'string' }, modelAnswer: { type: 'string' }, needed: { type: 'array', items: { type: 'string' } } } },
        source: { type: 'string' }, marksWeight: { type: 'integer' },
      },
    },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC + native-level Spanish checker verifying ONE Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. SPANISH ACCURACY (most important): every Spanish word, verb conjugation, gender/agreement, accent (á é í ó ú ñ), and ¿¡ correct? ser/estar, por/para, subjunctive, pretérito/imperfecto used correctly in the gist, oneMove, check prompt AND modelAnswer? Any wrong form → fix it.\n` +
    `2. SELF-CONTAINMENT: is check.prompt answerable from the card alone + general Spanish (any needed Spanish snippet embedded)? If it references an unseen passage/text/aural → fix to embed or rewrite.\n` +
    `3. GROUNDING: is the technique/topic real for LC Spanish and is the cited question/section real (near the questionRef in the named file)? marks/section weighting plausible? else grounded:false.\n` +
    `4. MARKING ACCURACY: does the demand match the scheme grammar (exact transcription on lifts, answer-in-required-language, no-quote-on-inference, Communication+Language on production)?\n` +
    `5. QUALITY: oneMove specific (no banned filler)?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id, topicId valid). If sound, accept. If fabricated/irredeemable, reject.\n\n` +
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
  `Completeness critic for a Spanish Catch-Up Lane set (Irish LC). The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) coverage spread across grammar (tenses + structures), comprehension technique, written production/opinion, and culture/literature — flag any of these four areas that is thin, (3) whether the highest-value grammar contrasts (ser/estar, pretérito/imperfecto, subjunctive, por/para) are all present, (4) any duplicate focus. List concrete gap slots to top up (each: level + topicId + focus).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
