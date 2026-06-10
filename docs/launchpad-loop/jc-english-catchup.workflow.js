export const meta = {
  name: 'jc-english-catchup',
  description: 'Author + adversarially verify Junior Cycle English Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards' },
    { title: 'Verify', detail: 'skeptic checks grounding, self-containment, level purity' },
    { title: 'Critic', detail: 'completeness + level/strand balance' },
  ],
}

const TXT = '/tmp/jc_english_txt'

const TOPICS = `
VALID jc-english topicIds (the VERIFIED taxonomy — 3 strands, confirmed against the official NCCA JC English spec
2026-06-10). topicId MUST be one; topicLabel MUST be the curriculum subtopic's EXACT name.
Strand 1 Oral Language (jc-english-0): -0 Spoken Communication and Presentation, -1 Discussion, Debate and Persuasion,
  -2 Influence and Register of Spoken Language  [mostly CBA, not the written exam — use rarely]
Strand 2 Reading (jc-english-1): -0 Reading Comprehension (Unseen Texts), -1 Studied Fiction (Novel and Short Story),
  -2 Studied Drama and Shakespeare, -3 Poetry (Studied and Unseen), -4 Film Studies, -5 Responding to Texts (Theme,
  Character, Author's Craft)
Strand 3 Writing (jc-english-2): -0 Functional and Transactional Writing, -1 Personal and Creative Writing, -2 Writing
  About Studied Texts, -3 Language, Grammar and Structure
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for JUNIOR CYCLE ENGLISH (Irish exam-recovery tool) — the final written exam.
A card teaches a student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a
SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): the JC English final exam is a single 2-hour written paper, 180 marks, Sections A/B/C
(all answered), at HIGHER and ORDINARY level. It tests: reading comprehension of UNSEEN texts (literary, non-literary,
multimodal), the STUDIED texts (novel/short story, drama incl. a full Shakespeare play at HL, poetry, film), and WRITING
(functional + personal/creative). Marking: WRITING is judged on P-C-L-M — Purpose (on task/genre), Coherence (organised),
Language (clear/fluent/ambitious), Mechanics (spelling/grammar/punctuation). READING/responding is judged on engagement +
understanding + CRITICAL APPRECIATION OF LANGUAGE — i.e. analyse HOW the writer/director achieves an effect and SUPPORT
with reference/quotation, not just retell what happens.

STUDIED-TEXT CARDS MUST BE TEXT-AGNOSTIC: students choose their own novel/play/poems/film from prescribed lists, so a
studied-text card teaches the TECHNIQUE (make a point → support with a reference to YOUR studied text → analyse the craft →
link to the question) using a GENERIC illustration — NEVER assume a specific prescribed text. The check must be answerable
by any student whatever text they studied.

GROUNDING (non-negotiable): ground every card in REAL SEC JC English questions + marking schemes at ${TXT}/ —
jc-english-YYYY-{HL,OL}-{paper,marking-scheme}.txt (pages ===PAGE n===; years 2022-2025 — JC exams cancelled 2020-2021).
grep/Read for the real question + the scheme's marking guidance. Do NOT invent question numbers, marks, or scheme wording.

LEVEL PURITY (hard rule): a card's level MUST match the level of the paper its question is on (HL card from HL paper, OL
from OL) — never put an HL question in the OL section.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'jceng-', unique (e.g. 'jceng-comprehension-quote-and-analyse-hl')
  subjectId     MUST be exactly 'jc-english'
  topicId       one of the valid ids above
  subjectLabel  'English (Junior Cycle)'
  topicLabel    the curriculum subtopic's EXACT name
  focus         short row label (e.g. 'Comprehension: quote then say HOW it works')
  level          'higher' | 'ordinary'
  gist          2-5 sentences: the technique + how the exam tests it. Plain, supportive, precise.
  oneMove       { label, text } — the single highest-leverage move/error (a SPECIFIC JC English move, e.g. 'after your
                point, QUOTE three words and explain the effect of the writer's word choice — that is the appreciation
                mark', 'match the functional genre's features: a speech needs a greeting + rhetorical questions + a sign-off',
                'in a studied-text answer, name a precise moment and reference it — vague plot summary scores low')
  check         { prompt (SELF-CONTAINED — for comprehension embed a SHORT unseen extract inline; for writing/studied-text
                  ask for the technique/structure/features, answerable by any student), modelAnswer, needed (>=2 award points) }
  source        'Topic … — SEC JC English {YEAR} {LEVEL}, Section …, Q… + marking scheme (…marking guidance…)'
  marksWeight   integer marks at stake (per the scheme)

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge. Embed any needed extract.
Studied-text checks must NOT require a specific prescribed text.

QUALITY BAR: oneMove names a SPECIFIC JC English move (P-C-L-M for writing; quote+analyse for reading). BANNED filler:
'read the question', 'manage your time', 'be creative', 'write neatly'. Plain text; unicode fine.

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
  { key: 'comprehension', strands: 'jc-english-1-0 (Reading Comprehension) + jc-english-1-5 (Responding to Texts)',
    topics: 'reading comprehension of UNSEEN texts: the quote-and-analyse technique (point → short quotation → explain the EFFECT of the writer\'s word choice = the critical-appreciation mark), answering "in your own words" (don\'t copy the text), reading MULTIMODAL/visual stimulus (image + text), identifying tone/atmosphere/purpose, and supporting every point with reference. Embed a short unseen extract inline so the check is self-contained.' },
  { key: 'studied-texts', strands: 'jc-english-1-1 Novel, jc-english-1-2 Drama/Shakespeare, jc-english-1-3 Poetry, jc-english-1-4 Film',
    topics: 'how to ANSWER studied-text questions (TEXT-AGNOSTIC technique): the studied novel/short story (character, theme, key moment), studied drama & Shakespeare (a relationship, a dramatic moment, staging), studied poetry (imagery, a poem that affected you), film studies (a scene, atmosphere, a director\'s technique). Each card teaches: make a point → reference a precise moment in YOUR studied text → analyse the craft → link to the question. Generic illustration only — never a specific prescribed text.' },
  { key: 'functional-writing', strands: 'jc-english-2-0 (Functional and Transactional Writing)',
    topics: 'the functional genres the exam sets — speech/talk, formal & informal letter, report, review, blog/article, diary entry, instructions. Teach the GENRE FEATURES + register for each + the P-C-L-M marking (clear Purpose = match the genre + audience; Coherence = structure; Language = appropriate register; Mechanics). Self-contained technique cards.' },
  { key: 'creative-writing', strands: 'jc-english-2-1 (Personal and Creative Writing) + jc-english-2-3 (Language, Grammar and Structure)',
    topics: 'personal & creative composition (short story, descriptive writing, personal essay, character-perspective pieces) — show-don\'t-tell, an opening that grabs, structure/paragraphing, and the LANGUAGE + MECHANICS marks (varied sentences, accurate spelling/punctuation; the 2023 HL rewrite-with-punctuation task — capitals, commas, inverted commas for direct speech, apostrophes, full stops). P-C-L-M literacy: know what each letter rewards.' },
  { key: 'writing-about-studied-texts', strands: 'jc-english-2-2 (Writing About Studied Texts) + jc-english-1-5',
    topics: 'composing a developed WRITTEN response about a studied text (the Section A/C studied-text answers): structure the answer (point-reference-explain-link / PEEL), keep it on the QUESTION asked (not a prepared essay), balance content with analysis, and support with precise references to YOUR chosen text. Text-agnostic technique. Plus exam technique: answering the actual question, the mark split.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 5 cards: aim for 3 Higher + 2 Ordinary, spread across DIFFERENT subtopics/years. Ground in the scheme/paper. topicLabel MUST be the exact curriculum subtopic name. LEVEL PURITY: an OL card from an OL question only. Studied-text cards MUST be text-agnostic + self-contained.`,
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
    `Independent SKEPTIC verifying ONE Junior Cycle English Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question/section near "${c.source}" (2022-2025)? marks + scheme marking-guidance match?\n` +
    `2. SELF-CONTAINMENT: answerable from the card + general knowledge? Comprehension cards embed the extract? STUDIED-TEXT cards must NOT require a specific prescribed novel/play/poem/film — if the card assumes one, fix to text-agnostic technique.\n` +
    `3. LEVEL PURITY: is the source paper actually ${c.level}? An OL card from an HL paper (or vice versa) → levelPure:false, fix the level.\n` +
    `4. ACCURACY: marking grammar right (P-C-L-M for writing; quote+analyse/critical-appreciation for reading)? topicId valid + topicLabel exact?\n` +
    `5. QUALITY: oneMove a specific JC English move (no filler)?\n` +
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
  `Completeness critic for a Junior Cycle English Catch-Up Lane set. The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) coverage across Reading (comprehension, studied novel, drama/Shakespeare, poetry, film, responding) and Writing (functional, creative, writing-about-studied-texts, language/mechanics) — flag thin areas, (3) whether the signature techniques are present: quote-and-analyse comprehension, a Shakespeare/studied-drama answer, a studied-poetry answer, a film answer, the functional-genre features, personal/creative writing, and P-C-L-M literacy, (4) any duplicate focus. List concrete gap slots (each: level + topicId + focus).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
