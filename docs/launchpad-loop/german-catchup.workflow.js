export const meta = {
  name: 'german-catchup',
  description: 'Author + adversarially verify German Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'topic clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic + native-German checker per card' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/german_txt'

const TOPICS = `
VALID german topicIds. topicId MUST be one; topicLabel = the curriculum subtopic's EXACT name. Card strand = topicId minus last -N.
german-0 Basic Communicative Proficiency: -0 Meeting People & Social Relations, -1 Making Plans & Future Action, -2 Climate
  & Weather, -3 Travel & Transport, -4 Buying Goods & Services, -5 Dealing With Emergencies, -6 Encouraging or Impeding
  Action, -7 Feelings & Attitudes, -8 Managing a Conversation, -9 Engaging in Discussion, -10 Passing on Messages
german-1 Language Awareness: -0 Learning From Target Language Material, -1 Exploring Meaning, -2 Relating Language to
  Attitude, -3 Writing About Your Experience, -4 Consulting Reference Materials
GUIDANCE: grammar (cases, articles, adjective endings, verbs, word order, Applied Grammar) + written production → german-1-3.
Comprehension-attack technique → german-1-0 / german-1-1. Opinion/attitude → german-1-2.
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert GERMAN (Irish exam-recovery tool), the WRITTEN paper. A card
teaches a student who fell behind how to recover marks: a clear gist, the ONE highest-leverage move, and a SELF-CONTAINED
check + model answer.

EXAM SHAPE (use real refs): HIGHER written paper 220 marks — Text I Reading Comprehension (60) + ANGEWANDTE GRAMMATIK /
Applied Grammar (25, Q1 or Q2: manipulate verbs/adjectives/cases as instructed, e.g. "Schreiben Sie die Verben im
Präsens/Perfekt"); Text II Reading Comprehension (60) + Äußerung zum Thema (short written piece, 25); Schriftliche
Produktion / Written Production (50). German is distinctive in testing APPLIED GRAMMAR explicitly. ORDINARY is simpler
(comprehension + written production). Aural + oral are separate.
SEC MARKING GRAMMAR: comprehension questions must be answered IN THE LANGUAGE INDICATED — "Beantworten Sie auf Deutsch"
(answer in German) vs "Answer in English"; wrong language loses marks. Applied Grammar needs the EXACT correct form (right
verb ending/tense, right adjective ending, right case) — a wrong form scores nothing. Written Production is marked on
Communication AND Language (grammar/case/verb/word-order accuracy).

GROUNDING (non-negotiable): ground every card in REAL SEC LC German papers + schemes at ${TXT}/ — german-YYYY-{HL,OL}-
{written,aural,marking-scheme}.txt (pages ===PAGE n===). grep/Read for the real question + scheme answer. Do NOT invent
question numbers/marks/wording. Every German word, article, case, ending, verb form and Umlaut (ä ö ü ß) MUST be correct.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'de-', unique (e.g. 'de-cases-nominative-accusative-hl')
  subjectId     MUST be exactly 'german'
  topicId       one of the valid ids above
  subjectLabel  'German'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'The four cases: who does what to whom')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core rule/technique + how the exam tests it. German examples with English glosses.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks
  check         { prompt (SELF-CONTAINED — embed any German text the student needs; a fill-the-gap / choose-the-form /
                  short-translate works well), modelAnswer (correct German + one-line why), needed (>=2 specific things) }
  source        'Topic … — SEC LC German {YEAR} {LEVEL}, Q… + marking scheme (…the scheme point…)'
  marksWeight   integer marks the topic protects

SELF-CONTAINMENT (hard rule): check answerable from the card + general German. Embed any needed German snippet. Never
reference an unseen text/aural.

QUALITY BAR: oneMove names a SPECIFIC German move/error (e.g. 'in the accusative the masculine article changes der→den —
"Ich sehe DEN Mann"'; 'after weil the verb goes to the END — "..., weil ich müde BIN"'; 'separable prefix splits off and
goes to the end — "Ich STEHE um 7 Uhr AUF"'; 'dative after mit/nach/bei/von/zu/aus — "mit DEM Bus"'; 'Perfekt = haben/sein
+ ge-…-t/-en, movement verbs take SEIN — "Ich BIN gefahren"'). BANNED filler: 'read the question','learn your vocab'.
German Umlauts/ß and unicode fine.

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
  { key: 'cases-articles-endings', topicHint: 'german-1-3',
    topics: 'the CASE system — the four cases (Nominativ subject, Akkusativ direct object, Dativ indirect object / after dative prepositions, Genitiv possession), how der/die/das/den/dem and ein-words change by case+gender, the accusative/dative PREPOSITIONS (durch/für/gegen/ohne/um = acc; aus/bei/mit/nach/seit/von/zu = dat), and ADJECTIVE endings. One rule per card with a fill-the-gap check.' },
  { key: 'verbs-tenses', topicHint: 'german-1-3',
    topics: 'VERBS — present tense (regular + key irregulars sein/haben/werden + stem-changing fahren→fährt), the PERFEKT (haben/sein + past participle; movement/change verbs take sein; ge-…-t weak vs ge-…-en strong), the PRÄTERITUM (esp. war/hatte and in narration), MODAL verbs (können/müssen/wollen… + infinitive at the end), the FUTURE (werden + infinitive). Fill-the-gap / choose-the-form checks.' },
  { key: 'word-order-applied-grammar', topicHint: 'german-1-3',
    topics: 'WORD ORDER + the ANGEWANDTE GRAMMATIK (Applied Grammar) section technique: the verb is SECOND in a main clause; the verb goes to the END after subordinating conjunctions (weil, dass, wenn, obwohl); time-manner-place order; SEPARABLE verbs split (aufstehen → ich stehe … auf). How to attack the Applied Grammar question — manipulate the underlined verb/adjective/noun into the EXACT form instructed (a tense, a case, an ending). Self-contained transform checks.' },
  { key: 'comprehension-technique', topicHint: 'german-1-0',
    topics: 'how to ATTACK the reading comprehension for marks: answering "Beantworten Sie auf Deutsch" IN GERMAN (a German question must get a German answer — no marks for English) vs "Answer in English"; the "Schreiben Sie X Sätze" requirement (give the exact number of sentences/details); finding the right phrase in the text; richtig/falsch + justify. Embed a short German snippet inline so the check is self-contained.' },
  { key: 'written-production-opinion', topicHint: 'german-1-3',
    topics: 'the productive writing: the Äußerung zum Thema (short opinion piece — state + justify an opinion with connectors: meiner Meinung nach, weil, einerseits/andererseits, deshalb) and the Schriftliche Produktion formats (informal email/letter to a friend, a reaction/opinion piece, a formal letter). Teach structure + the Communication-AND-Language marking (verbs/cases/word-order accuracy protect the Language marks). Technique-with-model, self-contained.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nDefault topicId (use the most accurate valid id per card): ${c.topicHint}\nTopics to mine: ${c.topics}\n\nProduce 5 cards: aim for 3 Higher + 2 Ordinary, each a DIFFERENT subtopic/focus. Read the relevant ${TXT}/ files to ground the technique + cite a real question. Every German form (article, case, ending, verb, Umlaut) MUST be correct.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'germanCorrect', 'selfContained', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    germanCorrect: { type: 'boolean' }, selfContained: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id + valid topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC + native-level German checker verifying ONE Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GERMAN ACCURACY (most important): every article, CASE, adjective ending, verb conjugation/tense, word order, plural and Umlaut (ä ö ü ß) correct in gist, oneMove, check prompt AND modelAnswer? (der/den/dem, weil-verb-final, sein vs haben in Perfekt, separable verbs, dative prepositions). Any wrong form → fix it.\n` +
    `2. SELF-CONTAINMENT: check answerable from the card alone + general German (snippet embedded)? else fix.\n` +
    `3. GROUNDING: real LC German technique/topic; cited question plausible; topicId valid + topicLabel exact?\n` +
    `4. MARKING ACCURACY: matches scheme grammar (answer-in-language-indicated, exact form in Applied Grammar, Communication+Language on production)?\n` +
    `5. QUALITY: oneMove specific (no filler)?\n` +
    `If fixable, verdict:fix WITH a complete corrected card in fixedCard (keep id + topicId). If sound, accept. If irredeemable, reject.\n\n` +
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
  `Completeness critic for a German Catch-Up Lane set (Irish LC). The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) coverage across cases/articles, verbs/tenses, word-order + Applied Grammar, comprehension technique, and written production — flag thin areas, (3) whether the highest-value German topics are present (the four cases, accusative vs dative, the Perfekt with sein/haben, weil-verb-to-end, separable verbs, adjective endings), (4) any duplicate focus. List concrete gap slots to top up (each: level + topicId + focus).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
