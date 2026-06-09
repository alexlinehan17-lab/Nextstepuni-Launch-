export const meta = {
  name: 'chem-cmdword',
  description: 'Author + adversarially verify Chemistry Command-Word Reflex stems from real SEC schemes',
  phases: [
    { title: 'Author', detail: 'cue/topic clusters → grounded stems' },
    { title: 'Verify', detail: 'independent skeptic refutes each stem vs scheme' },
    { title: 'Critic', detail: 'completeness + balance critic' },
  ],
}

const TXT = '/tmp/chem_txt'

const SHARED = `
You are authoring Command-Word Reflex stems for Leaving Cert CHEMISTRY (an Irish exam-technique tool).
The student sees a real exam question STEM, taps the COMMAND WORD (the cue telling them what to DO),
then learns what that cue demands and the examiner/marking-scheme-flagged trap behind it.

GROUNDING — non-negotiable. Every stem must come from a REAL SEC LC Chemistry question. The text of the
papers and marking schemes (2021-2025, HL+OL) is at ${TXT}/ as plain text files:
  chemistry-YYYY-HL-paper.txt / chemistry-YYYY-OL-paper.txt (the question stems)
  chemistry-YYYY-HL-marking-scheme.txt / chemistry-YYYY-OL-marking-scheme.txt (award points, *starred answers, notes)
Pages are delimited by ===PAGE n===. Use grep/Read to find the exact stem and its scheme award points.
Do NOT invent question numbers, marks, or scheme wording. If you can't verify it in the files, drop it.

THE TYPE (output one object per stem):
  id            kebab-case, prefix 'chem-', unique, includes the cue + a topic word (e.g. 'chem-define-pdc-2023-hl')
  subjectId     MUST be exactly 'chemistry'
  subjectLabel  'Chemistry'
  level         'higher' | 'ordinary'
  questionRef   e.g. '2023 HL · Q4(a)' or '2024 OL · Q7(b) (rate graph)'
  stem          the question stem, faithful to the paper. MUST contain commandWord verbatim.
  commandWord   the single cue (or multi-word cue like 'Distinguish between', 'Write an equation for')
  demand        what that cue REQUIRES — the answer-shaping move, specific to this question. Name the
                exact thing the scheme rewards (the *starred answer / the award points / the unit / the step).
  trap          the examiner/marking-scheme-flagged mistake for THIS cue + the marks consequence. Quote the
                scheme where it bites (e.g. "scheme stars only '*planar' (3)" / "ignores the (2) in 2HCl").
  source        citation: 'LC Chemistry {YEAR} {LEVEL} marking scheme, Q… ("…award point…")'
  marks         integer marks at stake on that part (from the scheme)
  figure        OPTIONAL — only if the cue genuinely depends on a visual AND it is one of the already-committed
                crops below whose SOURCE QUESTION matches your stem. Shape: { src, alt, source }.

TAPPABILITY (hard constraint — a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of
word-tokens after stripping non-letters and lowercasing. So if commandWord is 'Calculate', the word
'Calculate' must literally be in the stem. For multi-word cues ('Distinguish between'), those words must be
consecutive in the stem. Verify this yourself before returning each stem: split the stem on spaces, strip
punctuation, and confirm the cue words appear in order.

ALREADY-COMMITTED chemistry figures you MAY reuse (ONLY if your stem is genuinely that exact question):
  /exam-figures/chemistry/chemistry-2021-hl-vsepr-shapes-table.png — 2021 HL Q10(a) VSEPR table (CH4/BF3/NH3/QX2, QX2 shape '??')
  /exam-figures/chemistry/chemistry-2023-hl-electronegativity-graph.png — 2023 HL Q5(b) electronegativity vs atomic number
  /exam-figures/chemistry/chemistry-2023-ol-titration-apparatus.png — 2023 OL Q2 (conical flask, A=wash bottle, B=pipette)
  /exam-figures/chemistry/chemistry-2021-ol-titration-apparatus.png — 2021 OL titration apparatus
  /exam-figures/chemistry/chemistry-2024-ol-h2o2-rate-apparatus.png — 2024 OL Q7 (H2O2/MnO2 gas-syringe rate apparatus)
  /exam-figures/chemistry/chemistry-2023-hl-pcl5-equilibrium-graph.png — 2023 HL Q9 (PCl3+Cl2⇌PCl5, Cl2 added, Le Chatelier)
  /exam-figures/chemistry/chromatography-ptc-2022-ol.png — 2022 OL Q8 chromatography P/T/C
  /exam-figures/chemistry/chemistry-2025-hl-electrolysis-pbbr2-cell.png — 2025 HL Q6(d) Part B molten PbBr2 electrolysis
If a figure source-question matches, set figure.source to the SEC attribution
('SEC Leaving Certificate Chemistry {YEAR} {LEVEL}, Q… — © State Examinations Commission') and write a precise alt.
Most chemistry command-word stems are text-only — that is fine and expected. Do NOT force a figure.

QUALITY BAR (reject your own draft if it fails):
- The demand must be specific to the cue+question, not generic. BANNED filler: "read the question carefully",
  "manage your time", "show your working", "plan your answer", or any sentence that fits any exam.
- The trap must name a real, scheme-grounded error pattern (a *starred-only answer, a unit that's essential,
  a "Kelvin essential" note, a ratio coefficient that must be used, 'clear' not accepted for colourless, etc.).
- Prefer cue DIVERSITY across your batch (mix of e.g. Define, State, Explain, Calculate, Name, Outline,
  Describe, Justify, Distinguish between, Write an equation for, Deduce, Identify).
- ASCII-safe chemistry is fine (e.g. 'Br2', 'mol/L', '->'); unicode (⇌, Δ, ², °) is also fine.

Return ONLY the structured output. Do NOT edit any file. Return data, never write to data files.
`

const STEM_SCHEMA = {
  type: 'object',
  required: ['stems'],
  properties: {
    stems: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'subjectId', 'subjectLabel', 'level', 'questionRef', 'stem', 'commandWord', 'demand', 'trap', 'source', 'marks'],
        properties: {
          id: { type: 'string' },
          subjectId: { type: 'string' },
          subjectLabel: { type: 'string' },
          level: { type: 'string', enum: ['higher', 'ordinary'] },
          questionRef: { type: 'string' },
          stem: { type: 'string' },
          commandWord: { type: 'string' },
          demand: { type: 'string' },
          trap: { type: 'string' },
          source: { type: 'string' },
          marks: { type: 'integer' },
          figure: {
            type: 'object',
            properties: { src: { type: 'string' }, alt: { type: 'string' }, source: { type: 'string' } },
          },
        },
      },
    },
  },
}

const CLUSTERS = [
  { key: 'atomic-bonding-periodicity', cues: 'Define, State, Explain, Name, Deduce',
    topics: 'atomic structure, electron configuration, ionisation energy, electronegativity, bonding & VSEPR shapes, periodic trends, oxidation/reduction definitions' },
  { key: 'calculations', cues: 'Calculate, Determine, Write an equation for',
    topics: 'volumetric/titration calcs, moles & concentration, dilution, gas laws, pH, Kc, empirical/molecular formula, heat of reaction/combustion' },
  { key: 'organic-experiments', cues: 'Describe, Outline, Name, Identify, Write',
    topics: 'organic chemistry (alkanes/alkenes/alcohols), mandatory experiments & apparatus, instrumentation, equations, mechanisms, naming/IUPAC' },
  { key: 'equilibrium-rates-water-options', cues: 'Explain, Justify, Distinguish between, State, Suggest',
    topics: 'reaction rates, chemical equilibrium & Le Chatelier, exo/endothermic, water (hardness, treatment, pH), electrochemistry/options' },
]

phase('Author')
const authored = await parallel(CLUSTERS.map((c) => () =>
  agent(
    `${SHARED}\n\nYOUR CLUSTER: ${c.key}\nCues to favour: ${c.cues}\nTopics to mine: ${c.topics}\n\n` +
    `Produce 4 stems: aim for 2 Higher + 2 Ordinary, each with a DIFFERENT command word where possible. ` +
    `Spread across different years/questions. Read the relevant ${TXT}/ files to ground every stem, demand, trap, marks and citation.`,
    { label: `author:${c.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ),
))

const stems = authored.filter(Boolean).flatMap((r) => r.stems || [])
log(`Authored ${stems.length} candidate stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'tappable', 'grounded', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['accept', 'reject', 'fix'] },
    tappable: { type: 'boolean' },
    grounded: { type: 'boolean' },
    reason: { type: 'string' },
    fixedStem: {
      type: 'object',
      description: 'If verdict=fix, the corrected stem object (same shape as authored stems). Omit otherwise.',
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
    `You are an independent SKEPTIC verifying ONE Command-Word Reflex chemistry stem against the real SEC sources at ${TXT}/.\n` +
    `Default to REJECT/FIX if anything is off. Check, using grep/Read on the marking scheme + paper text files:\n` +
    `1. TAPPABILITY: does commandWord appear as a consecutive run of word-tokens in stem (strip punctuation, lowercase)? If not → tappable:false, verdict:fix (move/insert the cue so the stem genuinely contains it, OR pick the cue that IS in the stem).\n` +
    `2. GROUNDING: is the stem a real ${s.level} chemistry question near ${s.questionRef}? Do the marks + the demand's "what the scheme rewards" + the trap's quoted award point actually match the scheme text? If fabricated/mis-cited → grounded:false.\n` +
    `3. ACCURACY: any chemistry error in demand/modelled answer? Wrong *starred answer, wrong coefficient, wrong unit, wrong marks?\n` +
    `4. FIGURE (if present): does the figure src match a stem genuinely from that exact question? If reused wrongly → reject the figure (in a fix, drop the figure field).\n` +
    `5. QUALITY: is the demand specific (not banned generic filler)? Is the trap a real scheme-grounded pattern?\n\n` +
    `If small problems are fixable, return verdict:fix WITH a complete corrected stem object in fixedStem (keep the same id). ` +
    `If the stem is sound, verdict:accept. If unsalvageable/fabricated, verdict:reject.\n\n` +
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
log(`Verify: ${kept.length}/${stems.length} kept (rejected ${stems.length - kept.length})`)

phase('Critic')
const critic = await agent(
  `You are a completeness critic for a Chemistry Command-Word Reflex stem set (Irish LC exam-technique tool).\n` +
  `Here are the ${kept.length} verified stems:\n${JSON.stringify(kept.map((k) => ({ id: k.id, level: k.level, commandWord: k.commandWord, questionRef: k.questionRef, hasFigure: !!k.figure })), null, 2)}\n\n` +
  `Assess: (1) HL vs OL balance, (2) command-word diversity (flag if one cue dominates), (3) topic spread across ` +
  `chemistry strands (atomic/bonding, calculations, organic/experiments, equilibrium/rates/water/options), ` +
  `(4) whether figure-dependent cues are represented. List concrete gaps. Keep it short.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { kept, critic, authoredCount: stems.length, keptCount: kept.length }
