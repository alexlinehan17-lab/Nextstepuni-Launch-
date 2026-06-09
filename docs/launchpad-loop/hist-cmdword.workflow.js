export const meta = {
  name: 'hist-cmdword',
  description: 'Author + adversarially verify History Command-Word Reflex stems from real SEC papers/schemes',
  phases: [
    { title: 'Author', detail: 'DBQ + essay cue clusters → grounded stems' },
    { title: 'Verify', detail: 'skeptic refutes + accuracy-checks each' },
    { title: 'Critic', detail: 'completeness + balance' },
  ],
}

const TXT = '/tmp/hist_txt'

const SHARED = `
You author Command-Word Reflex stems for Leaving Cert HISTORY (Irish exam-technique tool, Later Modern 1815-1993).
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO), then learns what
that cue demands and the marking-scheme trap behind it.

GROUNDING (non-negotiable): every stem is a REAL SEC LC History question. Text of all papers + schemes (2021-2025,
HL+OL) is at ${TXT}/ (pages ===PAGE n===): history-YYYY-{HL,OL}-{paper,marking-scheme}.txt. grep/Read for the exact
stem + how the scheme awards it. Do NOT invent question wording, marks, or scheme content. Copyright cleared.

HISTORY MARKING GRAMMAR (the trap engine):
- Essays (Section 2 Ireland, Section 3 Europe & Wider World) are marked by CUMULATIVE marks counting Significant
  Relevant Statements (SRS): HL essay = up to 60 Cumulative Mark + 40 Overall Evaluation = 100; OL Part C = 30 CM +
  10 OE = 40. RELEVANCE to the exact question (not narration) drives the mark.
- TWO-ELEMENT questions ("X and Y", "causes and consequences", "how + significance"): the scheme caps the Cumulative
  Mark (e.g. HL max CM = 50 instead of 60) if you answer only ONE element. This is the single most common essay trap.
- DBQ (Section 1): comprehension (lift the stated point from a NAMED document), COMPARISON ("do both documents..." —
  cross-reference; single-document answers capped at half marks), CRITICISM ("value/usefulness of document X" — judge
  by who/when/why + limitation), CONTEXTUALISATION (mini-essay, wider context, marked by SRS).

THE TYPE (one object per stem):
  id            kebab, prefix 'hist-', unique, includes cue + topic (e.g. 'hist-account-for-partition-2023-hl')
  subjectId     MUST be exactly 'history'
  subjectLabel  'History'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2023 HL · Section 2 · Q3' or '2024 OL · Section 1 (DBQ) · Q3(b)'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim.
  commandWord   the cue (or multi-word cue like 'Account for', 'To what extent', 'Why did', 'What were',
                'According to', 'Do both documents', 'Examine the contribution of')
  demand        what that cue REQUIRES — the answer-shaping move, specific to THIS question. (e.g. 'Discuss' = argue
                several developed points for/against; 'Account for' = give the reasons/causes; 'Assess' / 'To what
                extent' = reach a judgement weighing evidence; a two-element stem = cover BOTH to lift the CM cap.)
  trap          the marking-scheme-flagged mistake for THIS cue + the marks consequence (quote the scheme: the CM cap,
                the 'both documents required' rule, 'relevance' / 'narrative-not-rewarded', the two-element NOTE).
  source        'LC History {YEAR} {LEVEL} marking scheme, Section …, Q… ("…award/NOTE…")'
  marks         integer marks at stake (from the scheme)

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
non-letters and lowercasing. So 'Account for' requires the words "Account for" consecutive in the stem; 'Why did'
requires "Why did" consecutive. Verify per stem before returning.

QUALITY BAR: demand specific to the cue+question (BANNED filler: 'read the question', 'manage your time', 'plan your
answer', 'write neatly'). trap must be a real scheme-grounded rule (CM cap, two-element NOTE, comparison half-mark cap,
SRS/relevance). Prefer cue DIVERSITY: Discuss, Account for, Assess, 'To what extent', 'Why did', 'What were', Examine,
'How did', Explain, Outline, 'According to', 'Do both documents'. Plain text, ASCII quotes. The 2021-2025 DBQ documents
are TEXT (no figures) — do NOT add a figure field.

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
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'dbq-cues', cues: 'According to, Explain, Do both documents, What would you consider, Outline',
    brief: 'DBQ (Section 1) command words — comprehension ("According to document A, ...", "Explain ..."), comparison ("Do both documents ..."), criticism ("What would you consider to be the value of document ...", "How useful ..."). Ground in real DBQ questions across years. 2 HL + 2 OL.' },
  { key: 'ireland-essay-cues', cues: 'Why did, What were, Discuss, Assess, How did',
    brief: 'Ireland essay (Section 2) command words on Later Modern Irish topics (Treaty, Lockout, Emancipation, Northern Ireland, economic programme, Parnell). Favour two-element stems where the CM-cap trap applies. 2 HL + 2 OL.' },
  { key: 'europe-essay-cues', cues: 'Account for, To what extent, Examine, Discuss, What were',
    brief: 'Europe & Wider World essay (Section 3) command words on Later Modern Europe topics (Stalin, Hitler/Mussolini, Nazism, Cold War, civil rights, decolonisation, nationalism). Favour two-element / judgement stems. 2 HL + 2 OL.' },
  { key: 'higher-order-cues', cues: 'To what extent, Assess, Account for, Examine the contribution of',
    brief: 'Higher-order judgement cues across any topic — "To what extent", "Assess", "Account for", "Examine the contribution of X". These demand a JUDGEMENT/evaluation, not just narration; tie the trap to the Overall Evaluation mark and relevance. 3 HL + 1 OL.' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(`${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\n${c.brief}\n\nProduce 4 stems, each with a DIFFERENT command word where possible, spread across years/topics. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation.`,
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
      },
    },
  },
}

const verified = await parallel(stems.map((s) => () =>
  agent(
    `Independent SKEPTIC verifying ONE History Command-Word stem against real SEC sources at ${TXT}/. Default REJECT/FIX if off.\n` +
    `1. TAPPABILITY: commandWord a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix (pick the cue that IS in the stem, or use the faithful wording that contains it).\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? marks + demand's scheme-rewarded approach + trap's quoted rule (CM cap / two-element NOTE / both-documents / SRS) match the scheme text? else grounded:false.\n` +
    `3. ACCURACY: any history error in the demand/trap? Is the cue's meaning right (e.g. 'Account for' = give reasons; comparison = cross-reference)?\n` +
    `4. QUALITY: demand specific (no filler)? trap a real scheme rule? No figure field?\n` +
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
  `Completeness critic for a History Command-Word Reflex stem set (Irish LC, Later Modern). The ${kept.length} verified stems:\n` +
  `${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) command-word diversity (flag if one cue dominates), (3) coverage across DBQ cues vs essay cues vs higher-order judgement cues, (4) Ireland vs Europe topic spread. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
