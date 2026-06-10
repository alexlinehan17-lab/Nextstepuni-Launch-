export const meta = {
  name: 'art-cmdword',
  description: 'Author + adversarially verify Art (Visual Studies) Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, art-facts, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/art_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert ART — VISUAL STUDIES (Irish exam-technique tool), the WRITTEN paper.
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that
cue demands and the marking-scheme trap behind it.

EXAM SHAPE: Visual Studies written paper, 150 marks. Section A "Today's world" (short Qs @10, many referencing artworks on
the accompanying PLATES sheet). Section B "Europe and the wider world" + Section C "Ireland and its place" (one 50-mark
essay each). NEW spec examined 2023+; prioritise 2023-2025.

ART CUE GRAMMAR (ground demands/traps in it):
 - 'Describe' / 'Discuss' / 'Analyse' an artwork (the dominant cues): give DEVELOPED points using ART VOCABULARY — the art
   ELEMENTS (line, shape, form, tone, colour, texture, space) and DESIGN PRINCIPLES (balance, contrast, emphasis, rhythm,
   proportion, unity) — backed by SPECIFIC visual evidence from the work. A vague "it is nice / realistic" with no art
   terms or evidence is capped; the marks are for specific, supported analysis.
 - 'Justify your answer' / 'Explain': the marks are in the REASONS, not the opinion/choice — give the why.
 - 'Compare': treat BOTH works on the SAME criteria (style/medium/composition/mood) in one analysis, not two separate
   descriptions.
 - 'Name' / 'Identify': the EXACT artist, artwork title, movement or term — and where asked, one you have genuinely studied
   in the correct category (e.g. "a contemporary LIVING sculptor").

THE TYPE (one object per stem):
  id            kebab, prefix 'art-', unique, includes cue + topic (e.g. 'art-describe-print-depth-hl')
  subjectId     MUST be exactly 'art'
  subjectLabel  'Art'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2024 HL · Section A · Q2(a)' or '2025 OL · Section C'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim. Keep it a stem.
  commandWord   the cue ('Describe', 'Discuss', 'Analyse', 'Justify', 'Explain', 'Compare', 'Name', 'Identify', 'Outline')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question (per the grammar above).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (vague non-art-vocabulary answer, opinion
                without justification, two separate descriptions instead of a comparison, wrong/non-specific naming).
  source        'LC Art (Visual Studies) {YEAR} {LEVEL} marking scheme, Section …, Q… ("…indicative content / award…")'
  marks         integer marks at stake (Section A part ~5-10; a Section B/C essay 50)
  figureSpec    OPTIONAL — include ONLY if the cue refers to a SPECIFIC artwork printed on the plates ("…illustrated on the
                accompanying sheet"). Shape { year, level, questionRef, source:'plates', artwork (artist + title),
                describes, whyNeeded }. For 'a work you have studied' / essay cues, NO figureSpec.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem.

GROUNDING (non-negotiable): every stem is a REAL SEC LC Art question. Text of papers + schemes (2021-2025, HL+OL) at
${TXT}/ — art-YYYY-{HL,OL}-written.txt / art-YYYY-{HL,OL}-marking-scheme.txt. grep/Read for the exact stem + scheme award.
Do NOT invent question numbers, marks, artists, artworks, dates, or scheme wording. Art facts MUST be accurate.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'manage your time', 'be creative'). trap
= a real scheme pattern. Prefer cue DIVERSITY: Describe, Discuss, Analyse, Justify, Explain, Compare, Name, Identify,
Outline. Plain text; unicode (é, í, ó, ×) fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
        properties: {
          id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
          level: { type: 'string', enum: ['higher', 'ordinary'] }, questionRef: { type: 'string' },
          stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
          trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
          figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, artwork: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'describe-artwork', cues: 'Describe',
    topics: 'the "Describe" cue on a specific plate artwork or a studied work — describe the composition / use of colour / mood / technique. Demand: art vocabulary (elements + principles) + specific visual evidence. Several reference a named plate work → figureSpec. Trap: vague description with no art terms.' },
  { key: 'discuss-analyse', cues: 'Discuss, Analyse',
    topics: 'the "Discuss"/"Analyse" cues, incl. Section B/C essay stems ("Discuss the work of a named European/Irish artist…", "Discuss two works…") and Section A analysis. Demand: developed, supported analysis with art vocabulary + context; for essays, a structured argument with named works. Trap: narration/listing without analysis.' },
  { key: 'justify-explain', cues: 'Justify, Explain, Outline',
    topics: 'the reasoning cues — "Justify your answer", "Explain…", "Outline…" (e.g. justify why an edition is valuable, explain a technique, outline the impact of a movement). Demand: the reasons/mechanism, not the bare choice. Trap: stating an opinion/answer with no justification.' },
  { key: 'compare-name-identify', cues: 'Compare, Name, Identify',
    topics: 'the comparison + knowledge cues — "Compare two works/artists" (same criteria, one analysis), "Name a contemporary living artist/sculptor you have studied", "Identify the movement/technique". Demand: comparison on shared criteria; exact, correctly-categorised naming. Trap: two separate descriptions instead of a comparison; a wrong/non-specific or wrong-category name.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems: aim for 3 Higher + 2 Ordinary, spread across years (favour 2023-2025) and sections. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation. Add a figureSpec only where the cue refers to a specific plate artwork. Make the demand and trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems (${stems.filter((s) => s.figureSpec).length} with figureSpec)`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'factsAccurate', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, factsAccurate: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
        figureSpec: { type: 'object', properties: { year: { type: 'string' }, level: { type: 'string' }, questionRef: { type: 'string' }, source: { type: 'string' }, artwork: { type: 'string' }, describes: { type: 'string' }, whyNeeded: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Art (Visual Studies) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + the scheme rule in demand/trap match? else grounded:false.\n` +
    `3. ART-FACT ACCURACY: any wrong art fact (artist, title, date, movement, technique, whether an artist is living)? else factsAccurate:false.\n` +
    `4. QUALITY: demand specific to cue+question (no filler)? trap a real scheme pattern (vague/no-art-vocab, opinion-without-justification, two-descriptions-not-a-comparison, wrong naming)?\n` +
    `5. FIGURE: if a figureSpec is present, does the cue truly reference a specific plate artwork (artist+title named)? else drop it.\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated, reject.\n\n` +
    `THE STEM:\n${JSON.stringify(s, null, 2)}`,
    { label: `verify:${s.id}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ stem: s, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  if (r.v.verdict === 'accept') kept.push(r.stem)
  else if (r.v.verdict === 'fix' && r.v.fixedStem) kept.push({ ...r.stem, ...r.v.fixedStem })
}
log(`Verify: ${kept.length}/${stems.length} kept`)

phase('Critic')
const critic = await agent(
  `Completeness critic for an Art (Visual Studies) Command-Word Reflex stem set (Irish LC). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef, hasFigure: !!k.figureSpec })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance (~60/40), (2) cue diversity — Describe/Discuss dominate the real paper, but the set should ALSO cover Analyse, Justify, Explain, Compare, Name/Identify; flag any missing, (3) section spread (A artwork-analysis, B European, C Irish), (4) whether the signature "use art vocabulary + visual evidence, not vague description" trap AND a Compare-on-same-criteria stem are present. List concrete gap slots to top up (each: level + cue + topic).`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
