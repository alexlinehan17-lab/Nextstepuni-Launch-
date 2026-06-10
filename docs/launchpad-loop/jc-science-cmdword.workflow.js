export const meta = {
  name: 'jc-science-cmdword',
  description: 'Author + adversarially verify Junior Cycle Science (Common Level) Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, science sense, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_science_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE SCIENCE (Ireland, reformed NCCA spec, first examined 2019). The
student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue
demands and the marking trap behind it.

EXAM SHAPE: a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 360 marks, ~2h, Section A (10 short Qs, 15 marks
each) + Section B (long Qs; number varies by year). EVERY stem's level MUST be 'common'.
SEC MARKING: each part has accepted answers, often "any one/two from: ...". A reason-cue needs the science reason; a count
cue ("two ways", "three structures") needs that many distinct points.

JC-SCIENCE CUE GRAMMAR (ground demands/traps in it):
 - 'State' / 'Name' / 'Give' / 'List' / 'Identify': the exact short answer(s) — precise term, no explanation. Trap: a
   vague description where the marks need the NAMED term; or giving fewer than the number asked ("name TWO").
 - 'Describe' / 'Outline': say WHAT happens / the steps, in order, with enough detail. Trap: one-word answers where a
   process is wanted; missing a key stage.
 - 'Explain' / 'Why' / 'Give a reason' / 'Account for': a CAUSE — the science reason ("because ..."). Trap: restating the
   observation instead of giving the reason; the marks are the "because".
 - 'Calculate' / 'Work out' / 'Determine': a numeric answer with the formula + working + UNIT. Trap: no formula/working
   (no partial credit), wrong or missing unit.
 - 'Draw' / 'Plot' / 'Complete' / 'Label': produce/finish a graph, circuit, diagram or table accurately. Trap (graph):
   wrong axes / unplotted points / no line; (diagram): unlabelled or wrong-component symbol.
 - 'Suggest' / 'Predict': a plausible science-based answer (often open) backed by reasoning. Trap: a guess with no science.
 - 'Distinguish between' / 'Compare' / 'Give a difference': state the contrast for BOTH things on the same property.
   Trap: describing only one, or two unrelated facts that don't actually contrast.
 - WORKING-SCIENTIFICALLY cues: 'Write a hypothesis' (a testable prediction), 'Identify the variable' (the one changed /
   the controlled), 'How could you make it a fair test / more reliable'. Trap: a hypothesis that's a question; naming the
   wrong variable.

THE TYPE (one object per stem):
  id            kebab, prefix 'jcsci-', unique (e.g. 'jcsci-explain-eclipse-common')
  subjectId     MUST be exactly 'jc-science'
  subjectLabel  'Science (Junior Cycle)'
  level         MUST be 'common'
  questionRef   e.g. '2024 CL · Section A · Q5' or '2023 CL · Section B · Q13(c)'
  stem          the question stem, faithful to the paper (summarise a long stimulus briefly; if it needs a figure,
                describe the essential detail in words). MUST contain commandWord verbatim.
  commandWord   the cue ('State', 'Name', 'Give', 'List', 'Identify', 'Describe', 'Outline', 'Explain', 'Give a reason',
                'Calculate', 'Draw', 'Plot', 'Complete', 'Label', 'Suggest', 'Predict', 'Distinguish', 'Compare',
                'Write a hypothesis', 'Account for')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question.
  trap          the scheme-flagged mistake for THIS cue + the marks consequence (named-term vs description, count short,
                reason missing, unit missing, hypothesis-as-question, etc.).
  source        'SEC JC Science {YEAR} CL marking scheme, Q… (…accepted answers…)'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Multi-word cues ('Give a reason', 'Write a hypothesis', 'Distinguish between') must appear as
that exact consecutive run.

GROUNDING (non-negotiable): every stem is a REAL SEC JC Science question (2022-2025; exams cancelled 2020-2021). Papers +
schemes at ${TXT}/ — jc-science-YYYY-CL-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme guidance. Do
NOT invent question numbers, marks, or scheme wording. Stay within JC scope.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'learn the topic'). trap = a real
marking pattern. Prefer cue DIVERSITY (especially Explain/Give-a-reason, the count cues, and the working-scientifically
cues). Plain text.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object', required: ['stems'],
  properties: {
    stems: { type: 'array', items: { type: 'object',
      required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
      properties: {
        id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
        level: { type: 'string', enum: ['common'] }, questionRef: { type: 'string' },
        stem: { type: 'string' }, commandWord: { type: 'string' }, demand: { type: 'string' },
        trap: { type: 'string' }, source: { type: 'string' }, marks: { type: 'integer' },
      } } },
  },
}

const CLUSTERS = [
  { key: 'state-name-list', cues: 'State, Name, Give, List, Identify',
    topics: 'the short-answer/recall cues across all strands — "Name the gas produced", "State one function of ...", "Give two examples of ...", "Identify the part labelled X", "List the planets in order". Demand: the exact named term(s); for count cues exactly that many distinct correct points. Trap: a vague description where a NAMED term is needed; giving fewer than the number asked.' },
  { key: 'explain-reason', cues: 'Explain, Give a reason, Account for, Why, Suggest',
    topics: 'the cause/reasoning cues — "Explain why a lunar eclipse occurs", "Give a reason why the bulb did not light", "Account for the increase in rate", "Suggest why ...". Demand: the science reason ("because ..."). Trap: restating the observation instead of the cause; a Suggest answer with no science.' },
  { key: 'describe-distinguish-compare', cues: 'Describe, Outline, Distinguish, Compare, Give a difference',
    topics: 'the process + contrast cues — "Describe how to separate sand from salt water", "Outline the steps of ...", "Distinguish between accuracy and precision", "Compare series and parallel circuits". Demand: the steps in order / the contrast on the SAME property for BOTH things. Trap: one-word answers where a process is wanted; describing only one side of a contrast.' },
  { key: 'calculate-draw-complete', cues: 'Calculate, Draw, Plot, Complete, Label',
    topics: 'the numeric + graphical/diagram cues — "Calculate the density / the resistance / the speed", "Draw a circuit diagram", "Plot the points and draw a graph", "Complete the table", "Label the diagram". Demand: formula + working + UNIT for Calculate; correct axes/points/line for graphs; correct labelled components for diagrams. Trap: no working / missing unit; wrong axes or unplotted points; unlabelled or wrong circuit symbols.' },
  { key: 'working-scientifically', cues: 'Write a hypothesis, Identify (the variable), Suggest (an improvement), Predict',
    topics: 'the Nature-of-science cues — "Write a testable hypothesis for this investigation", "Identify the variable that was changed", "Name one variable that should be kept the same", "How could the student make the test more reliable / a fair test", "Predict what will happen if ...". Demand: a testable PREDICTION (not a question); the correct independent/controlled variable; a valid reliability move (repeat & average). Trap: a hypothesis phrased as a question; naming the wrong variable; "do it more carefully" instead of repeat-and-average.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 5 stems, each with a DIFFERENT cue where possible, across years and strands (all level 'common'). Ground every stem/demand/trap/marks/citation in the paper + scheme. Make demand+trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'sciCorrect', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, sciCorrect: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: {
      id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
      level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
      commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
      source: { type: 'string' }, marks: { type: 'integer' } } },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle Science (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase; multi-word cue = exact run)? If not → fix.\n` +
    `2. GROUNDING: real question near ${s.questionRef} (2022-2025 CL)? marks + the marking rule in demand/trap match the scheme? else grounded:false.\n` +
    `3. SCIENCE: is the demand/trap scientifically correct and within JC scope? Is the cue the RIGHT command word for what the question asks? level exactly 'common'?\n` +
    `4. QUALITY: demand specific to this cue+question (no filler)? trap a real marking pattern (named-term, count, missing reason, missing unit, hypothesis-as-question)?\n` +
    `If fixable, verdict:fix WITH a complete corrected stem in fixedStem (keep id, level 'common'). If sound, accept. If fabricated, reject.\n\n` +
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
  `Completeness critic for a Junior Cycle Science (Common Level) Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) cue diversity — State/Name/Give/List/Identify, Describe/Outline, Explain/Give a reason/Account for, Calculate, Draw/Plot/Complete/Label, Distinguish/Compare, Suggest/Predict, and the working-scientifically cues (Write a hypothesis, Identify the variable); flag missing cues, (2) coverage across the five strands (Nature of science, Physical, Chemical, Biological, Earth and space), (3) whether the signature traps are present: named-term not description, count-short, reason-missing on Explain, unit-missing on Calculate, hypothesis-as-question, one-sided contrast. List concrete gap slots (each: cue + topic/strand). All stems are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
