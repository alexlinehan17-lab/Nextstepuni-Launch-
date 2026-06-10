export const meta = {
  name: 'jc-irish-catchup',
  description: 'Author + adversarially verify Junior Cycle Irish (Gaeilge T2) Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'exam-area clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, level purity' },
    { title: 'Critic', detail: 'completeness + level/strand balance' },
  ],
}

const TXT = '/tmp/jc_irish_txt'

const TOPICS = `
VALID jc-irish topicIds (the VERIFIED taxonomy — confirmed against the official NCCA Gaeilge T2 spec 2026-06-10).
topicId MUST be one; topicLabel MUST be the curriculum subtopic's EXACT name.
Strand 1 Cumas Cumarsáide (jc-irish-0):
  -0 'Éisteacht: Cluastuiscint (Listening)'   [exam Roinn A, both levels]
  -1 'Léamhthuiscint (Reading Comprehension)' [HL Ceist 4; OL Ceisteanna 4/6/7-reading/8]
  -2 'Litríocht (Studied Literature)'          [HL ONLY in the written exam — Ceisteanna 5/8/10; NO OL literature question]
  -3 'Ceapadóireacht (Writing and Composition)' [HL Ceist 6; OL Ceisteanna 5/7-writing/9]
  -4 'Labhairt agus Idirghníomhú Cainte (Speaking and Interaction)' [oral/CBA only — do NOT use for written-exam cards]
Strand 2 Feasacht Teanga agus Chultúrtha (jc-irish-1):
  -0 'Cruinneas na Teanga (Language Accuracy: Séimhiú, Urú, Aimsirí)' [HL discrete Ceisteanna 7+9; at OL assessed ONLY inside writing rubrics]
  -1 'Feasacht Chultúrtha (Cultural Awareness)' [CBA — do not use]
  -2 'Feasacht ar an Dátheangachas (Bilingualism Awareness)' [CBA — do not use]
Strand 3 Féinfheasacht an Fhoghlaimeora (jc-irish-2): -0, -1 [CBA — do not use]
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE IRISH (Gaeilge T2 — English-medium schools, the majority cohort).
A card teaches a student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a
SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs; verified against the actual 2022-2025 papers):
HIGHER (270 marc, 2 hours): Roinn A Cluastuiscint 45 marc (Ceist 1-3, two plays of each píosa/comhrá). Roinn B 'Léamh,
Ceapadóireacht agus Litríocht' 225 marc: Ceist 4 Léamhthuiscint (65 marc), Ceist 5 Litríocht úrscéal/dráma (40 marc),
Ceist 6 Ceapadóireacht (50 marc — e.g. blag), Ceist 7 Cruinneas cloze/líon-na-bearnaí (10 marc), Ceist 8 Litríocht
gearrscéal/gearrscannán (25 marc), Ceist 9 Cruinneas pick-the-correct-form (10 marc — séimhiú/urú/aimsir/tuiseal),
Ceist 10 Litríocht dán/amhrán (25 marc).
ORDINARY (270 marc): Roinn A Cluastuiscint 60 marc (Ceist 1-3). Roinn B 'Léamh agus Ceapadóireacht' 210 marc: Ceist 4
fíor/bréagach ar fhógra (20), Ceist 5 teachtaireacht writing (20), Ceist 6 fógra/póstaer reading (30), Ceist 7 composite
reading + writing (80), Ceist 8 meaitseáil sentences-to-pictures (25), Ceist 9 sraith pictiúr picture-story writing (35).
OL has NO discrete Litríocht question and NO discrete Cruinneas question — at OL accuracy is rewarded ONLY inside the
writing rubrics ('na príomhghnéithe de cheart na teanga').

LANGUAGE REGISTER (house style — matches the existing LC Irish catch-up cards): BILINGUAL. gist/oneMove/modelAnswer are
English-led scaffolding that quotes the Irish exam terms and Irish examples inline (e.g. "past tense needs séimhiú:
'cheannaigh mé', NOT 'ceannaigh mé'"). Irish quoted from papers stays verbatim Irish. check.prompt may be an Irish task
with a short English gloss. The audience is a 14-15 year old in an English-medium school — clarity first.

LITRÍOCHT CARDS MUST BE TEXT-AGNOSTIC: students study texts from the Liosta Téacsanna Dualgais T2 (prescribed list) —
teach the TECHNIQUE (name title + author/composer PRECISELY, make a point, reference a precise moment, link to the
question) with a generic illustration — NEVER assume one specific text. The check must be answerable whatever text the
student studied. Litríocht cards are HIGHER level only (no OL literature question exists).

GROUNDING (non-negotiable): ground every card in REAL SEC JC Irish questions + marking schemes at ${TXT}/ —
jc-irish-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled 2020-2021).
grep/Read for the real question + the scheme's marking guidance. Do NOT invent question numbers, marks, or scheme wording.

LEVEL PURITY (hard rule): a card's level MUST match the level of the paper its question is on (HL card from HL paper, OL
from OL) — never put an HL question in the OL section.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jcir-', unique (e.g. 'jcir-cluastuiscint-predict-from-questions-hl')
  subjectId     MUST be exactly 'jc-irish'
  topicId       one of the valid ids above
  subjectLabel  'Irish (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Cluastuiscint: read the questions BEFORE the CD starts')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the technique + how the exam tests it. Plain, supportive, precise. Bilingual register.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC JC Irish move, e.g. 'in the
                Cluastuiscint, the answers come in ORDER — use the gap between plays to fill, not panic', 'name the
                title AND the author exactly — "Ní mór teideal an dáin/an amhráin sin agus ainm an té a chum a scríobh
                síos go cruinn" — that names line is a real mark', 'past tense = séimhiú on the verb')
  check         { prompt (SELF-CONTAINED — embed any short Irish text/sentences needed inline; litríocht checks must be
                  text-agnostic), modelAnswer, needed (>=2 award points) }
  source        'Topic … — SEC JC Irish (Gaeilge T2) {YEAR} {LEVEL}, Roinn …/Ceist … + marking scheme (…marking guidance…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge. Embed any needed extract or
example sentences. No CD audio exists in the app — cluastuiscint checks test the STRATEGY (e.g. predicting question
focus, recognising what a question word asks for: Cén uair→time, Cá→place, Cé→person) or transcript-snippet comprehension
with the snippet embedded.

QUALITY BAR: oneMove names a SPECIFIC JC Irish move. BANNED filler: 'read the question', 'manage your time', 'do your
best', 'learn vocabulary'. Plain text; unicode fine (fadas required — á é í ó ú).

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
  { key: 'cluastuiscint', strands: 'jc-irish-0-0 (Éisteacht: Cluastuiscint)',
    topics: 'listening strategy for Roinn A (HL 45 marc / OL 60 marc, Ceist 1-3): reading the printed questions BEFORE the audio to predict what to listen for; question words and what they demand (Cén uair→a time, Cá/Cén áit→a place, Cé→a person, Cén fáth→a reason, Cad/Céard→a thing); the two-plays structure (first play = gist, second play = details, sos between to write); answers in Irish; numbers/dates/times/ages as classic listening targets. Both levels. Checks: embed a 2-3 line transcript snippet or test question-word recognition.' },
  { key: 'leamhthuiscint', strands: 'jc-irish-0-1 (Léamhthuiscint)',
    topics: 'reading comprehension: HL Ceist 4 (65 marc — long sliocht, parts (a)-(g), find-and-lift vs own-words questions, the personal-response final part); OL Ceist 4 fíor/bréagach on a fógra (20), OL Ceist 6 reading a fógra/póstaer (30), OL Ceist 7 reading part, OL Ceist 8 meaitseáil sentences-to-pictures (25). Technique: locate the paragraph by matching key words, answer ONLY what is asked, fíor/bréagach justification, reading multimodal notices (dates, prices, times). Embed short Irish text inline for checks.' },
  { key: 'litriocht', strands: 'jc-irish-0-2 (Litríocht) — HIGHER ONLY',
    topics: 'the three HL literature questions (TEXT-AGNOSTIC technique): Ceist 5 úrscéal/dráma (40 marc), Ceist 8 gearrscéal/gearrscannán (25 marc), Ceist 10 dán/amhrán (25 marc). Teach: the AINMNIGH line is real marks — title + author/composer written exactly ("go cruinn"); structure an answer = point → precise moment/line from YOUR studied text → why it matters → link to the question; common asks (an príomhcharachtar, a theme/téama, an scéal, mothúcháin sa dán). ALL cards level higher.' },
  { key: 'ceapadoireacht', strands: 'jc-irish-0-3 (Ceapadóireacht)',
    topics: 'the writing tasks: HL Ceist 6 (50 marc — blag/scéal/alt with choice; judged on ábhar/content + Gaeilge/accuracy); OL Ceist 5 teachtaireacht (20 marc — short message with the required points covered), OL Ceist 7 writing part (write a fógra/póstaer with the required details), OL Ceist 9 sraith pictiúr (35 marc — tell the story of a 6-picture sequence, past tense, one or two sentences per picture). Teach genre features, covering EVERY required bullet/pictiúr, and tense discipline (sraith pictiúr = Aimsir Chaite).' },
  { key: 'cruinneas', strands: 'jc-irish-1-0 (Cruinneas na Teanga)',
    topics: 'accuracy: HL Ceist 7 líon-na-bearnaí cloze (10 marc — choose the right word/form in context) + HL Ceist 9 pick-the-correct-form (10 marc — séimhiú after mo/do/sa, urú after i/ar an, aimsirí na mbriathra, an tuiseal ginideach); the high-frequency rules (past tense séimhiú: cheannaigh/d’ól; urú after "i": i nGaillimh; séimhiú after "an-"/"mo"). For ORDINARY: accuracy lives INSIDE the writing rubrics — ground OL cruinneas cards in the OL marking scheme’s ceart-na-teanga writing criteria (e.g. one consistent tense in the sraith pictiúr), citing the OL scheme, NOT a nonexistent discrete OL grammar question.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 5 cards: aim for 3 Higher + 2 Ordinary (EXCEPT litriocht: 5 Higher, 0 Ordinary — no OL literature question exists), spread across DIFFERENT years/question parts. Ground in the scheme/paper. topicLabel MUST be the exact curriculum subtopic name. LEVEL PURITY: an OL card from an OL question only.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'selfContained', 'levelPure', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, selfContained: { type: 'boolean' }, levelPure: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; valid topicId). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Irish (Gaeilge T2) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question/section near "${c.source}" (2022-2025)? marks + scheme marking-guidance match? (HL: Cluastuiscint 45, C4 65, C5 40, C6 50, C7 10, C8 25, C9 10, C10 25. OL: Cluastuiscint 60, C4 20, C5 20, C6 30, C7 80, C8 25, C9 35.)\n` +
    `2. SELF-CONTAINMENT: answerable from the card + general knowledge? Any needed Irish text embedded? LITRÍOCHT cards must NOT require one specific prescribed text — if the card assumes one, fix to text-agnostic technique.\n` +
    `3. LEVEL PURITY: is the source paper actually ${c.level}? Litríocht discrete questions exist at HL ONLY — an OL litríocht card citing a discrete OL literature question is FABRICATED. An OL cruinneas card must cite the OL writing rubric, not a discrete OL grammar question (none exists).\n` +
    `4. ACCURACY: Irish correct (fadas, séimhiú/urú examples actually right)? topicId valid + topicLabel exact? Bilingual register (English-led scaffolding, Irish quoted verbatim)?\n` +
    `5. QUALITY: oneMove a specific JC Irish move (no filler)?\n` +
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
  `Completeness critic for a Junior Cycle Irish (Gaeilge T2) Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40 — but litríocht is HL-only by design), (2) coverage across Cluastuiscint, Léamhthuiscint, Litríocht (úrscéal/dráma + gearrscéal + dán/amhrán techniques all present?), Ceapadóireacht (HL blag/scéal + OL teachtaireacht + sraith pictiúr), and Cruinneas (HL discrete + OL in-writing) — flag thin areas, (3) signature techniques present: question-word prediction for listening, fíor/bréagach + meaitseáil at OL, the ainmnigh-title-and-author rule, sraith-pictiúr past-tense discipline, past-tense séimhiú, (4) any duplicate focus. List concrete gap slots (each: level + topicId + focus).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
