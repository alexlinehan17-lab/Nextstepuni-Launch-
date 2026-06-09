export const meta = {
  name: 'chem-cmdword-topup',
  description: 'Fill completeness-critic gaps in Chemistry Command-Word set (redox, acids/base, distinguish, outline, +figure)',
  phases: [
    { title: 'Author', detail: 'one targeted stem per flagged gap slot' },
    { title: 'Verify', detail: 'independent skeptic refutes each vs scheme' },
  ],
}

const TXT = '/tmp/chem_txt'

const SHARED = `
Authoring ONE Command-Word Reflex stem for Leaving Cert CHEMISTRY (Irish exam-technique tool).
The student taps the COMMAND WORD in a real exam stem, then learns what the cue demands + the marking-scheme trap.

GROUNDING (non-negotiable): use the real SEC text at ${TXT}/ —
  chemistry-YYYY-{HL,OL}-paper.txt and chemistry-YYYY-{HL,OL}-marking-scheme.txt (pages: ===PAGE n===).
grep/Read to find the exact stem + its scheme award points. Do NOT invent question numbers, marks, or wording.
If you cannot verify the stem AND the scheme award lines, pick a different real question that fits the slot.

OUTPUT one object (the schema's "stem" field). Fields:
  id (kebab, prefix 'chem-', includes cue+topic), subjectId='chemistry', subjectLabel='Chemistry',
  level ('higher'|'ordinary'), questionRef (e.g. '2023 HL · Q4(a)'), stem (faithful; MUST contain commandWord verbatim),
  commandWord, demand (the answer-shaping move + the exact scheme-rewarded thing), trap (scheme-grounded mistake + marks
  consequence, quote the award point), source ('LC Chemistry {YEAR} {LEVEL} marking scheme, Q… ("…award…")'),
  marks (int from scheme), figure (ONLY if required + reusing a committed crop whose source-question matches — else omit).

TAPPABILITY (a test enforces it): commandWord must appear in stem as a CONSECUTIVE run of word-tokens after stripping
punctuation + lowercasing. Verify it yourself: the cue's words must appear, in order, as whole words in the stem.

COMMITTED chemistry figures you MAY reuse ONLY if your stem genuinely IS that exact question:
  /exam-figures/chemistry/chemistry-2023-ol-titration-apparatus.png — 2023 OL Q2 (conical flask, A=wash bottle, B=pipette)
  /exam-figures/chemistry/chemistry-2021-ol-titration-apparatus.png — 2021 OL titration apparatus
  /exam-figures/chemistry/chemistry-2024-ol-h2o2-rate-apparatus.png — 2024 OL Q7 (H2O2/MnO2 gas-syringe rate apparatus)
  /exam-figures/chemistry/chromatography-ptc-2022-ol.png — 2022 OL Q8 chromatography P/T/C
  /exam-figures/chemistry/chemistry-2021-hl-vsepr-shapes-table.png — 2021 HL Q10(a) VSEPR table (CH4/BF3/NH3/QX2)
  /exam-figures/chemistry/chemistry-2025-hl-electrolysis-pbbr2-cell.png — 2025 HL Q6(d) Part B molten PbBr2 electrolysis
figure.source = 'SEC Leaving Certificate Chemistry {YEAR} {LEVEL}, Q… — © State Examinations Commission' + a precise alt.

QUALITY: demand specific to cue+question (BANNED filler: "read the question carefully", "show your working",
"manage your time", "plan your answer", anything that fits any exam). Trap = a real scheme-grounded pattern.
ASCII chemistry fine ('Br2','mol/L','->'); unicode (⇌,Δ,°) fine. Return data only; never edit a file.
`

const STEM_SCHEMA = {
  type: 'object',
  required: ['stem'],
  properties: {
    stem: {
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
}

// Each slot fills a critic-flagged gap. cue is the REQUIRED command word; topic constrains the question.
const SLOTS = [
  { key: 'redox-deduce-oxnum', cue: 'Deduce', level: 'higher',
    topic: 'REDOX / oxidation numbers — find a question asking to deduce/find the oxidation number of an element in a species (e.g. Mn in MnO4-, Cr in Cr2O7^2-, S in SO4^2-). The cue word in the stem must be "Deduce".' },
  { key: 'acids-distinguish', cue: 'Distinguish between', level: 'ordinary',
    topic: 'ACIDS/BASES or organic saturation — a "Distinguish between" question (e.g. strong vs weak acid; a saturated vs unsaturated hydrocarbon; an acid vs a base). The exact words "Distinguish between" must be consecutive in the stem.' },
  { key: 'outline-experiment', cue: 'Outline', level: 'higher',
    topic: 'EXPERIMENT/PROCEDURE — a question whose stem uses "Outline" (e.g. outline how a standard solution is prepared, outline the steps of a named preparation/recrystallisation). The cue word must be "Outline".' },
  { key: 'apparatus-name-figure', cue: 'Name', level: 'ordinary',
    topic: 'APPARATUS (figure-dependent) — a "Name" question about a labelled piece of titration apparatus, genuinely from 2023 OL Q2 (A=wash bottle, B=pipette) so you can attach chemistry-2023-ol-titration-apparatus.png. The cue word must be "Name" and the stem must reference the labelled apparatus.' },
  { key: 'acidbase-meaning', cue: 'Calculate', level: 'higher',
    topic: 'ACIDS/BASES pH — a "Calculate" question on pH / [H+] / Kw / pH of a strong acid or base (a real HL pH calculation). The cue word must be "Calculate". (This is the one extra Calculate we accept, to cover the acids/base topic gap.)' },
]

phase('Author')
const authored = await parallel(SLOTS.map((s) => () =>
  agent(`${SHARED}\n\nSLOT: ${s.key}\nREQUIRED command word: "${s.cue}"\nREQUIRED level: ${s.level}\nTOPIC: ${s.topic}\n\nReturn exactly one grounded stem for this slot.`,
    { label: `author:${s.key}`, phase: 'Author', schema: STEM_SCHEMA },
  ).then((r) => r && r.stem ? { ...r.stem, _slot: s.key, _wantCue: s.cue } : null),
))

const stems = authored.filter(Boolean)
log(`Authored ${stems.length} top-up stems`)

phase('Verify')
const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'tappable', 'grounded', 'reason'],
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
    `Independent SKEPTIC verifying ONE Chemistry Command-Word stem against real SEC sources at ${TXT}/. Default to REJECT/FIX if off.\n` +
    `1. TAPPABILITY: does commandWord appear as a consecutive word-token run in stem (strip punctuation, lowercase)? If not → fix.\n` +
    `2. GROUNDING: real ${s.level} question near ${s.questionRef}? Do marks + demand's "scheme-rewarded thing" + trap's quoted award point match the scheme text? If fabricated/mis-cited → grounded:false, reject.\n` +
    `3. ACCURACY: any chemistry error (wrong oxidation number, wrong pH, wrong *starred answer, wrong marks)?\n` +
    `4. FIGURE (if present): src must match a stem genuinely from that exact question; else drop the figure in a fix.\n` +
    `5. QUALITY: demand specific (no banned filler)? trap a real scheme pattern?\n` +
    `If fixable, verdict:fix with a complete corrected stem in fixedStem (keep id). If sound, accept. If fabricated, reject.\n\n` +
    `THE STEM:\n${JSON.stringify(s, null, 2)}`,
    { label: `verify:${s._slot}`, phase: 'Verify', schema: VERDICT_SCHEMA },
  ).then((v) => ({ stem: s, v })),
))

const kept = []
for (const r of verified.filter(Boolean)) {
  if (!r.v) continue
  const clean = { ...r.stem }; delete clean._slot; delete clean._wantCue
  if (r.v.verdict === 'accept') kept.push(clean)
  else if (r.v.verdict === 'fix' && r.v.fixedStem) kept.push({ ...clean, ...r.v.fixedStem })
}
log(`Top-up verify: ${kept.length}/${stems.length} kept`)
return { kept, authoredCount: stems.length, keptCount: kept.length }
