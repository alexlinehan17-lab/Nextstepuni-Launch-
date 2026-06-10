export const meta = {
  name: 'applied-maths-taxonomy-verify',
  description: 'Adversarially verify the draft Applied Maths taxonomy against the official NCCA spec + the real 2023-2025 SEC papers before it becomes the single source of truth',
  phases: [
    { title: 'Verify', detail: '5 independent lenses: spec fidelity x2, HL coverage, OL coverage, old-spec contamination' },
    { title: 'Critic', detail: 'completeness critic over all verdicts' },
  ],
}

const DRAFT = '/tmp/applied_taxonomy_draft.json'
const SPEC = '/tmp/applied_maths_spec.txt'
const PAPERS = '/tmp/applied_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' },
    pass: { type: 'boolean', description: 'true ONLY if the draft passes this lens with no material defect' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] },
      detail: { type: 'string' },
      suggestedChange: { type: 'string' },
    } } },
  },
}

const COMMON = `
You are an independent SKEPTIC verifying a DRAFT syllabus taxonomy for Leaving Certificate APPLIED MATHEMATICS before it
becomes the app's single source of truth. The stakes: every future content card keys to these strand/subtopic ids, and a
guard test + 3 tools depend on it. Default to FAIL with findings if anything is materially off.

THE DRAFT: ${DRAFT} (JSON; every node carries a specRef claiming where in the spec it comes from).
THE OFFICIAL SPEC (primary source, NCCA 2021 specification, first examined 2023): ${SPEC} — the strands + learning
outcomes are on pages 16-21 (search '===== PAGE 16 =====' through PAGE 21).
THE REAL EXAM PAPERS + MARKING SCHEMES: ${PAPERS}/applied-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt for 2021-2025.
NOTE: 2021-2022 are the OLD pre-modelling syllabus (last examined 2022) and must NOT shape the taxonomy; 2023-2025 are the
CURRENT spec the taxonomy must match.

Severity: 'blocker' = wrong/invented/missing content that would corrupt the source of truth; 'fix' = a naming/placement
improvement with a concrete suggestedChange; 'note' = observation, no change needed. pass=true only with zero blockers.
Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity-a',
    prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY (forward). Walk the DRAFT node by node. For EVERY strand and subtopic: (1) does its name + specRef faithfully match the spec's actual strand titles and 'STUDENTS LEARN ABOUT' cells on pages 16-21 (read them — do not trust the specRef)? (2) is anything INVENTED (a topic not in the spec)? (3) are the strand names the official ones? Quote the spec where a node deviates.` },
  { key: 'spec-fidelity-b',
    prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY (reverse). Walk the SPEC pages 16-21 cell by cell. For EVERY 'STUDENTS LEARN ABOUT' cell and every named concept inside it (e.g. dot product, coefficient of restitution, Bellman's Principle, floats, dimensional analysis, integration by parts, second-order reducible): does it have a clear home in exactly the right draft subtopic? List any spec content with NO home or an ambiguous/wrong home.` },
  { key: 'exam-coverage-hl',
    prompt: `${COMMON}\n\nYOUR LENS: HL EXAM COVERAGE. Read the 2023, 2024 and 2025 HL papers in ${PAPERS}. For EVERY question (10 per paper), state in one line which draft subtopic id it maps to. A question with NO natural home = blocker. Also flag any draft subtopic that no HL question in 3 years has touched (note, not blocker — the spec is the authority, the papers are the sanity check).` },
  { key: 'exam-coverage-ol',
    prompt: `${COMMON}\n\nYOUR LENS: OL EXAM COVERAGE. Same as the HL lens but for the 2023, 2024 and 2025 ORDINARY papers in ${PAPERS}: map every question to a draft subtopic id; a question with no home = blocker; untouched subtopics = note.` },
  { key: 'old-spec-contamination',
    prompt: `${COMMON}\n\nYOUR LENS: OLD-SPEC CONTAMINATION. The old syllabus (examined to 2022) contained: relative velocity as a standalone topic, simple harmonic motion, statics/equilibrium of rigid bodies, moments of inertia/rigid-body rotation, hydrostatics. Check: (1) does the DRAFT contain any topic that exists ONLY in the old syllabus (blocker)? (2) does the draft accidentally omit anything the NEW spec kept (e.g. circular motion IS in the new spec)? Read the 2022 HL paper vs the 2024 HL paper to ground the difference, and pages 16-21 of the spec as the authority.` },
]

const verdicts = await parallel(LENSES.map((l) => () =>
  agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA }),
))

const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/5 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a syllabus-taxonomy verification. The draft (${DRAFT}) was checked by 5 independent lenses; their verdicts:\n` +
  `${JSON.stringify(got, null, 2)}\n\n` +
  `Your job: (1) is any MATERIAL defect raised by one lens but dismissed/missed by the others? (2) do the lenses conflict anywhere — and who is right (re-check the spec at ${SPEC} pages 16-21 yourself for any conflict)? (3) is there any verification angle nobody covered (e.g. HL-only learning outcomes in bold; the modelling project component; strand ordering)? Give a final SHIP / FIX-FIRST verdict with the exact list of changes (if any) that must be applied to the draft before it becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)

return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
