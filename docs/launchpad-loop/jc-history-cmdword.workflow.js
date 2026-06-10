export const meta = {
  name: 'jc-history-cmdword',
  description: 'Author + adversarially verify Junior Cycle History (Common Level) Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic checks grounding, history sense, tappability' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/jc_history_txt'

const SHARED = `
You author Command-Word Reflex stems for JUNIOR CYCLE HISTORY (Ireland, reformed NCCA spec, first examined 2019). The
student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what that cue
demands and the marking trap behind it.

EXAM SHAPE: a SINGLE terminal paper at COMMON LEVEL (no Higher/Ordinary) — 360 marks, ~2h, 8 questions, source/document/
cartoon/photo heavy. EVERY stem's level MUST be 'common'. Marking: short answers have set accepted points; developed
answers need development (a point + explanation/example); a NAMED example is often its own mark.

JC-HISTORY CUE GRAMMAR (ground demands/traps in it):
 - 'Name' / 'State' / 'Give' / 'Identify' / 'List' / 'Mention': the exact short answer(s) / a named person/event/place —
   precise, no explanation; count cues need that many. Trap: a vague description where a NAMED answer is needed; fewer
   than asked.
 - 'Describe' / 'Outline' / 'Write an account of': set out WHAT happened with detail (the events/features in order). Trap:
   one undeveloped sentence where a developed account is wanted.
 - 'Explain' / 'Why' / 'Give a reason' / 'Account for': the CAUSE/reason it happened. Trap: describing the event instead
   of giving the reason; the marks are the cause/explanation.
 - 'Using the source/document/cartoon/photograph' (the SKILLS cues): read the supplied source — quote/refer to it,
   name the symbol + meaning + the creator's attitude for a cartoon, judge usefulness AND a limitation. Trap: answering
   from your own knowledge instead of FROM the source; giving usefulness with no limitation; missing the cartoon's message.
 - 'Distinguish between' / 'What is the difference between': the contrast on the SAME feature for BOTH (e.g. primary vs
   secondary source, cause vs consequence). Trap: only one side.
 - 'Define' / 'What is meant by': the precise meaning of a historical term (propaganda, genocide, continuity, plantation).
   Trap: an example with no definition.
 - 'Do you agree' / 'Judgement' cues: give a view AND support it with evidence/a reason. Trap: a yes/no with no support.

THE TYPE (one object per stem):
  id            kebab, prefix 'jchist-', unique (e.g. 'jchist-explain-1916-common')
  subjectId     MUST be exactly 'jc-history'
  subjectLabel  'History (Junior Cycle)'
  level         MUST be 'common'
  questionRef   e.g. '2024 CL · Q7(d)' or '2023 CL · Q1'
  stem          the question stem, faithful to the paper (summarise a long source briefly; if it needs a source/cartoon/
                photo, describe the essential detail in words). MUST contain commandWord verbatim.
  commandWord   the cue ('Name', 'State', 'Give', 'Identify', 'List', 'Mention', 'Describe', 'Outline', 'Explain',
                'Account for', 'Define', 'Distinguish', 'Using the source', 'Using the cartoon', 'Do you agree')
  demand        what that cue REQUIRES — the answer-shaping move specific to THIS question.
  trap          the scheme-flagged mistake for THIS cue + the marks consequence.
  source        'SEC JC History {YEAR} CL marking scheme, Q… (…accepted answers…)'
  marks         integer marks at stake (per the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. Multi-word cues ('Account for', 'Distinguish between', 'Using the source', 'Do you agree')
must appear as that exact consecutive run.

GROUNDING (non-negotiable): every stem is a REAL SEC JC History question (2022-2025; exams cancelled 2020-2021). Papers +
schemes at ${TXT}/ — jc-history-YYYY-CL-{paper,marking-scheme}.txt. grep/Read for the exact stem + scheme guidance. Do NOT
invent question numbers, marks, or scheme wording. Stay within JC scope.

QUALITY BAR: demand specific to cue+question (BANNED filler: 'read the question', 'learn the dates'). trap = a real marking
pattern. Prefer cue DIVERSITY (especially the source/cartoon skills cues and Explain vs Describe). Plain text.

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
  { key: 'source-skills', cues: 'Using the source, Using the cartoon, Define, Distinguish between',
    topics: 'the WORKING-WITH-EVIDENCE cues — "Using the source/document, ...", "Look at the cartoon/photograph and ...", "Define propaganda / genocide / continuity / plantation", "Distinguish between a primary and a secondary source". Demand: answer FROM the source; for a cartoon name the symbol + meaning + the attitude; a definition is the precise meaning. Trap: answering from your own knowledge not the source; usefulness with no limitation; an example with no definition.' },
  { key: 'name-state-identify', cues: 'Name, State, Give, Identify, List, Mention',
    topics: 'the short-answer/named cues across all strands — "Name one leader of ...", "State one effect of the Famine", "Identify the century", "Give one feature of an Early Christian monastery", "Mention one cause of World War One". Demand: the exact named person/event/place/feature; count cues need that many. Trap: a vague description where a named answer is wanted; fewer than asked.' },
  { key: 'describe-explain', cues: 'Describe, Outline, Explain, Account for, Give a reason',
    topics: 'the developed-answer cues — "Describe one event during the 1916 Rising", "Outline the causes of the Reformation", "Explain why people emigrated during the Famine", "Account for the rise of Hitler". Demand: Describe/Outline = what happened in detail; Explain/Account-for = the reason/cause. Trap: describing when a reason is asked; an undeveloped one-liner where a developed point is needed.' },
  { key: 'judgement-and-mixed', cues: 'Do you agree, plus any cue on a content topic',
    topics: 'the judgement + content cues — "Do you agree that ...? Give one reason", plus State/Explain/Describe questions on the big topics (Early Christian Ireland, plantations, the Famine, Home Rule, 1916/independence, the Renaissance, Reformation, exploration, the World Wars, dictatorship, the Holocaust, the Cold War). Demand: a view WITH supporting evidence; or the precise content answer. Trap: a yes/no with no support; a generic content answer with no named detail.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\nProduce 6 stems, each with a DIFFERENT cue where possible, across years and strands (all level 'common'). Ground every stem/demand/trap/marks/citation in the paper + scheme. Make demand+trap specific to the exact question.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object', required: ['verdict', 'tappable', 'grounded', 'correct', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' }, grounded: { type: 'boolean' }, correct: { type: 'boolean' }, reason: { type: 'string' },
    fixedStem: { type: 'object', properties: {
      id: { type: 'string' }, subjectId: { type: 'string' }, subjectLabel: { type: 'string' },
      level: { type: 'string' }, questionRef: { type: 'string' }, stem: { type: 'string' },
      commandWord: { type: 'string' }, demand: { type: 'string' }, trap: { type: 'string' },
      source: { type: 'string' }, marks: { type: 'integer' } } },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE Junior Cycle History (Common Level) Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase; multi-word cue = exact run)? If not → fix.\n` +
    `2. GROUNDING: real question near ${s.questionRef} (2022-2025 CL)? marks + the marking rule in demand/trap match the scheme? else grounded:false.\n` +
    `3. HISTORY SENSE + SCOPE: demand/trap historically correct and within JC scope? Is the cue the RIGHT command word for what the question asks? level exactly 'common'?\n` +
    `4. QUALITY: demand specific to this cue+question (no filler)? trap a real marking pattern (named-answer, count, describe-vs-explain, answer-from-the-source, usefulness-needs-limitation, cartoon symbol+attitude, judgement-needs-support)?\n` +
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
  `Completeness critic for a Junior Cycle History (Common Level) Command-Word Reflex stem set. The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) cue diversity — Name/State/Give/Identify/List, Describe/Outline, Explain/Account for, Define, Distinguish, the source/cartoon skills cues, and the judgement cue; flag missing cues, (2) coverage across the three strands (The nature of history — skills should be well represented, The history of Ireland, The history of Europe and the wider world), (3) whether the signature traps are present: named-answer not description, count-short, describe-vs-explain, answer-from-the-source, define-not-example, judgement-needs-support. List concrete gap slots (each: cue + topic/strand). All stems are level 'common'.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
