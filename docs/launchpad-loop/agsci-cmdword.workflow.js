export const meta = {
  name: 'agsci-cmdword',
  description: 'Author + adversarially verify Agricultural Science Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'strand/cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic refutes + fact-checks each' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/agsci_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert AGRICULTURAL SCIENCE (Irish exam-technique tool, new spec 2021+).
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what
that cue demands and the marking-scheme trap behind it.

GROUNDING (non-negotiable): every stem is a REAL SEC LC Agricultural Science question. Text of all papers + schemes
(2021-2025, HL+OL) at ${TXT}/ (pages ===PAGE n===): agricultural-science-YYYY-{HL,OL}-{paper,marking-scheme}.txt.
grep/Read for the exact stem + scheme award points. Do NOT invent question numbers, marks, or scheme wording. RECOMPUTE
any number you cite.

THE TYPE (one object per stem):
  id            kebab, prefix 'agsci-', unique, includes cue + topic (e.g. 'agsci-describe-silage-process-hl')
  subjectId     MUST be exactly 'agricultural-science'
  subjectLabel  'Agricultural Science'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2023 HL · Q5(a)' or '2024 OL · Q12(b)'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim.
  commandWord   the cue (or multi-word cue like 'Distinguish between', 'Give an account of', 'State two')
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question (Describe = give the steps/
                detail; Explain = give the reason/mechanism; Name/State = the exact term; Calculate = the worked value;
                Distinguish = contrast both on the same dimension; Suggest = a reasoned plausible answer).
  trap          the scheme-flagged mistake for THIS cue + the marks consequence. Quote the scheme where it bites (the
                exact term required, the number of points needed, a unit, 'name AND explain', a direction e.g. lime RAISES pH).
  source        'LC Agricultural Science {YEAR} {LEVEL} marking scheme, Q… ("…award point…")'
  marks         integer marks at stake (from the scheme)
  figure        OPTIONAL — only if the cue genuinely depends on a diagram AND it is the committed crop below whose SOURCE
                QUESTION matches your stem. Shape { src, alt, source }.

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Verify per stem (e.g. 'Distinguish between' needs both words consecutive in the stem).

ALREADY-COMMITTED Ag Science figure you MAY reuse ONLY if your stem genuinely IS that exact question:
  /exam-figures/agricultural-science/agricultural-science-2021-ol-ruminant-stomach.png — 2021 OL Q2(a): label the sheep's
  digestive system parts A (Rumen), B (Abomasum), C (Omasum); Oesophagus/Small Intestine/Reticulum already labelled.
figure.source = 'SEC Leaving Certificate Agricultural Science {YEAR} {LEVEL}, Q… — © State Examinations Commission' + a precise alt.
Most stems are text-only — that is fine. Do NOT force a figure.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question carefully','manage your time','show your
working','plan your answer'). trap = a real scheme-grounded rule. Prefer cue DIVERSITY: Define, State, Name, Describe,
Explain, Outline, Identify, Calculate, Distinguish between, Suggest, Compare, 'Give an account of'. Plain text, ASCII fine; unicode (×,°,→) fine.

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
          figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'scientific-practices-soils', cues: 'Define, State, Describe, Explain, Calculate',
    topics: 'experiment design & fair test/variables, evaluating evidence; soil formation/classification, soil texture & structure, soil pH & liming, chemical properties (CEC, leaching, N-P-K), drainage, organic matter, soil organisms, soil management' },
  { key: 'crops', cues: 'Name, Describe, Explain, Outline, Identify',
    topics: 'plant physiology (photosynthesis, respiration), crop classification/ID, grassland & cereal production, establishment (seedbed, sowing), management (fertiliser, weed/pest/disease control), harvesting & the silage process' },
  { key: 'animals-physiology-production', cues: 'Describe, Explain, Name, State, Outline',
    topics: 'ruminant digestion (rumen, microbial cellulose breakdown), the reproductive system & oestrous cycle, lactation, dairy/beef/sheep production systems, nutrition & feeding, grass-based systems' },
  { key: 'animals-genetics-health', cues: 'Explain, Suggest, Distinguish between, Calculate, State',
    topics: 'genetics & breeding (monohybrid cross, selective breeding, EBI/breeding indices, heritability), animal health & disease (mastitis, liver fluke, BVD, parasite control, antibiotics/withdrawal), microbiology, agri-environment/sustainability' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 4 stems: aim for 2 Higher + 2 Ordinary, each with a DIFFERENT command word where possible, spread across years. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
        commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
        source: { type: 'string' }, marks: { type: 'integer' },
        figure: { type: 'object', properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } } },
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Agricultural Science Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme-rewarded thing + trap's quoted award point match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any ag-science error (wrong term, wrong soil-pH direction, wrong digestive compartment, wrong genetics ratio, wrong number/marks)?\n` +
    `4. FIGURE (if present): src matches a stem genuinely from that exact question (ruminant figure only on 2021 OL Q2a)? else drop the figure in a fix.\n` +
    `5. QUALITY: demand specific (no filler)? trap a real scheme pattern?\n` +
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
  `Completeness critic for an Agricultural Science Command-Word Reflex stem set (Irish LC, new spec). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef, hasFigure: !!k.figure })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) command-word diversity (flag if one cue dominates), (3) topic spread across the 4 strands (Scientific Practices, Soils, Crops, Animals), (4) whether calculation/figure cues are present. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
