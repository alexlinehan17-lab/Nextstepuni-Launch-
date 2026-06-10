export const meta = {
  name: 'art-catchup',
  description: 'Author + adversarially verify Art (Visual Studies) Catch-Up Lane recovery cards from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand clusters → grounded recovery cards (+figureSpec for plate artworks)' },
    { title: 'Verify', detail: 'skeptic checks grounding, art-fact accuracy, self-containment' },
    { title: 'Critic', detail: 'completeness + level/strand/figure balance' },
  ],
}

const TXT = '/tmp/art_txt'

const TOPICS = `
VALID art topicIds (the WRITTEN Visual Studies paper maps to the Respond strand + the Visual Studies Framework). topicId
MUST be one; topicLabel MUST be the curriculum subtopic's EXACT name below.
art-2 Respond Strand: -0 "3.1 Analysis", -1 "3.2 Contextual Enquiries", -2 "3.3 Impact and Value", -3 "3.4 Critical and
  Personal Reflection", -4 "3.5 Process"
art-3 Visual Studies Framework: -0 "Context", -1 "Artists and Artworks", -2 "Analysis", -3 "Art Elements and Design
  Principles", -4 "Media and Areas of Practice"
GUIDANCE: artwork-analysis technique (composition, the art elements/design principles) → art-3-3 or art-3-2 or art-2-0;
media/print/sculpture techniques → art-3-4; European/Irish art movements, artists, buildings, heritage → art-3-0 (Context)
or art-3-1 (Artists and Artworks); impact/value/exhibitions/personal reflection → art-2-2 or art-2-3.
`

const SHARED = `
You author Catch-Up Lane RECOVERY CARDS for Leaving Cert ART — VISUAL STUDIES (Irish exam-recovery tool), the WRITTEN
paper. A card teaches a student who lost marks how to recover them: a clear gist, the ONE highest-leverage move, and a
SELF-CONTAINED check + model answer.

EXAM SHAPE (use real questionRefs): The Visual Studies written paper is 150 marks. Section A "Today's world" (50; answer
any FIVE short questions @10 marks, several referencing artworks on the accompanying ILLUSTRATIONS/PLATES sheet). Section B
"Europe and the wider world" (50; answer ONE essay). Section C "Ireland and its place in the wider world" (50; answer ONE
essay). NEW spec examined 2023+ ("Visual Studies"); 2021-2022 are the older "History & Appreciation of Art" format —
PRIORITISE 2023-2025 for question structure, but Irish/European art FACTS from any year are fine if accurate.

GROUNDING (non-negotiable): ground every card in REAL SEC LC Art questions + marking schemes at ${TXT}/ —
art-YYYY-{HL,OL}-written.txt and art-YYYY-{HL,OL}-marking-scheme.txt (pages ===PAGE n===). grep/Read for the real
question + the scheme's indicative content / award points. Do NOT invent question numbers, marks, scheme wording, artists,
artworks, dates, or movements. Art facts MUST be accurate (artist names, artwork titles, dates, movements, Irish heritage
sites) — if unsure, ground it in the scheme text or a real exam reference, never guess.

${TOPICS}

THE CARD (one object per card):
  id            kebab, prefix 'art-', unique, includes the topic (e.g. 'art-analysing-composition-hl')
  subjectId     MUST be exactly 'art'
  topicId       one of the valid ids above
  subjectLabel  'Art'
  topicLabel    the curriculum subtopic's EXACT name (syllabus-aligned)
  focus         short row label disambiguating same-subtopic cards (e.g. 'Creating depth: foreground/middle/background')
  level         'higher' | 'ordinary'
  gist          2-5 sentences: the core idea/technique/context + how the exam tests it. Plain, supportive, precise. Name
                real art elements/principles, movements, artists, works where relevant.
  oneMove       { label, text } — the single highest-leverage move/error that wins the marks (specific, art-grounded)
  check         { prompt (SELF-CONTAINED — a recall/analyse/explain question answerable from the card + the figure if
                  present; for an essay-skill card, ask for the structure/points not a full essay), modelAnswer, needed
                  (>=2 award points / indicative-content items) }
  source        'Topic … — SEC LC Art (Visual Studies) {YEAR} {LEVEL}, Section …, Q… + marking scheme (…indicative content…)'
  marksWeight   integer marks at stake (Section A part ~10; a Section B/C essay 50)
  figureSpec    Include for a card that analyses a SPECIFIC artwork shown on the plates (Section A). Shape: { year, level,
                questionRef, source:'plates', artwork (the artist + title named in the question, e.g. 'Rosmoney by Sinead
                Wall'), describes, whyNeeded }. The main loop crops the artwork from the plates booklet. For 'choose a work
                you studied' questions or essay cards, NO figureSpec (the student supplies the example).

SELF-CONTAINMENT (hard rule): check.prompt answerable from the card + general knowledge + the figure (if figureSpec). For
an artwork-analysis card, attach the figureSpec so the work is shown. Never silently depend on an unseen plate.

QUALITY BAR: oneMove names a SPECIFIC art move/fact (e.g. 'overlapping + diminishing scale + a high horizon create depth';
'an edition is a set of identical prints the artist numbers and signs'; 'the Book of Kells uses interlace, zoomorphic
initials and the chi-rho page'; 'Impressionists painted en plein air with broken colour to catch changing light'). BANNED
filler: 'read the question', 'manage your time', 'be creative'. Plain text; unicode (×, é, í, ó) fine.

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
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, artwork: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'artwork-analysis', strands: 'art-3-3 (Art Elements and Design Principles), art-3-2 / art-2-0 (Analysis)',
    topics: 'how to ANALYSE an artwork for Section A marks: the art ELEMENTS (line, shape, form, tone, colour, texture, space) and DESIGN PRINCIPLES (balance, contrast, emphasis/focal point, rhythm, proportion, unity); creating DEPTH/perspective (overlapping, diminishing scale, linear/aerial perspective, high horizon); reading composition, mood and the artist intention. Cards that analyse a SPECIFIC plate artwork get a figureSpec.' },
  { key: 'media-areas-of-practice', strands: 'art-3-4 (Media and Areas of Practice)',
    topics: 'media and technique vocabulary the paper tests: PRINTMAKING (relief/lino, intaglio/etching, screenprint; what an EDITION is, why artists number/sign prints), PAINTING (oil, watercolour, acrylic; techniques), SCULPTURE (carving, modelling, casting, assemblage; relief vs in-the-round), photography/film, applied art & craft/design. Define + give the marks-winning detail.' },
  { key: 'european-art-context', strands: 'art-3-0 (Context), art-3-1 (Artists and Artworks)',
    topics: 'Section B "Europe and the wider world" essay knowledge — major movements & their hallmarks + a named artist/work: e.g. Renaissance (Leonardo, Michelangelo; perspective, humanism), Baroque (Caravaggio chiaroscuro), Impressionism (Monet; en plein air, broken colour), Post-Impressionism (Van Gogh, Cézanne), Cubism (Picasso, Braque), Surrealism (Dalí), Pop Art (Warhol), Modern architecture. Teach the essay backbone (movement + context + named work + analysis).' },
  { key: 'irish-art-heritage', strands: 'art-3-0 (Context), art-3-1 (Artists and Artworks)',
    topics: 'Section C "Ireland and its place" essay knowledge — Irish art & heritage: prehistoric (NEWGRANGE passage tomb, megalithic art), Early Christian/Celtic (BOOK OF KELLS, High Crosses, the Ardagh Chalice & Tara Brooch metalwork, round towers), Georgian architecture/Dublin, 20th-century Irish artists (Jack B. Yeats, Harry Clarke stained glass, Evie Hone, Louis le Brocquy, Mainie Jellett, Paul Henry), contemporary Irish art, Irish museums/galleries (NGI, IMMA). Teach the essay backbone with accurate facts.' },
  { key: 'respond-impact-value', strands: 'art-2-2 (3.3 Impact and Value), art-2-3 (3.4 Critical and Personal Reflection)',
    topics: 'the Respond skills the paper rewards: the IMPACT and VALUE of art (cultural, social, economic, personal), exhibitions/galleries & how art is displayed/conserved, public art & its role, the role of the gallery/curator, careers in the visual arts, and CRITICAL + PERSONAL reflection (justifying a personal response with art vocabulary, not just "I like it"). Self-contained.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nStrands: ${c.strands}\nTopics to mine: ${c.topics}\n\nProduce 5 cards: aim for 3 Higher + 2 Ordinary, spread across DIFFERENT subtopics/years (favour 2023-2025). Read the relevant ${TXT}/ files; ground every fact in the scheme/paper. Add a figureSpec ONLY for cards that analyse a specific named artwork shown on the plates. Each card's topicLabel MUST be the exact curriculum subtopic name.`,
    { label: `author:${c.key}`, phase: 'Author', schema: CARD_SCHEMA },
  ),
))

const cards = authored.filter(Boolean).flatMap((r) => r.cards || [])
log(`Authored ${cards.length} candidate cards (${cards.filter((c) => c.figureSpec).length} with figureSpec)`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'grounded', 'factsAccurate', 'selfContained', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    grounded: { type: 'boolean' }, factsAccurate: { type: 'boolean' }, selfContained: { type: 'boolean' }, reason: { type: 'string' },
    fixedCard: { type: 'object', description: 'If verdict=fix, the corrected card (same shape + same id; preserve/repair figureSpec). Omit otherwise.' },
  },
}

const verified = await parallel(cards.map((c) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Art (Visual Studies) Catch-Up card against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. GROUNDING: real ${c.level} question/section near "${c.source}"? marks + the scheme's indicative content match? else grounded:false.\n` +
    `2. ART-FACT ACCURACY (critical): are ALL art facts correct — artist names, artwork titles, DATES, movements, techniques, Irish heritage sites (e.g. Book of Kells is in Trinity College; Newgrange is Neolithic c.3200 BC; an edition is numbered prints)? Any wrong fact → factsAccurate:false.\n` +
    `3. SELF-CONTAINMENT: answerable from the card + general knowledge + the figure (if figureSpec)? An artwork-analysis card that names a plate work but has no figureSpec → selfContained:false (add figureSpec).\n` +
    `4. SYLLABUS ALIGNMENT: topicId valid + topicLabel the exact curriculum subtopic name?\n` +
    `5. QUALITY: oneMove a specific art move/fact (no banned filler)? needed[] real award points?\n` +
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
  `Completeness critic for an Art (Visual Studies) Catch-Up Lane set (Irish LC). The ${kept.length} verified cards:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, topicId: k.topicId, focus: k.focus, hasFigureSpec: !!k.figureSpec })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) coverage across the three exam sections — Section A artwork-analysis/technique, Section B European art, Section C Irish art/heritage — plus media/areas-of-practice and impact/value; flag thin areas, (3) whether the signature topics are present: art elements & design principles, creating depth, an edition/printmaking, a European movement (Impressionism/Cubism/Renaissance), Irish heritage (Newgrange/Book of Kells), and an Irish 20th-c artist, (4) figureSpec coverage for Section-A artwork cards. List concrete gap slots to top up (each: level + topicId + focus + figure-needed?).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: cards.length, keptCount: kept.length }
