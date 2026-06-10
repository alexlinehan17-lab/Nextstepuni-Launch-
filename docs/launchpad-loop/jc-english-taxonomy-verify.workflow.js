export const meta = {
  name: 'jc-english-taxonomy-verify',
  description: 'Adversarially verify the draft JC English taxonomy against the official NCCA spec + the real 2022-2025 JC English papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage HL, exam coverage OL, completeness/invention' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_english_taxonomy_draft.json'
const SPEC = '/tmp/jc_english_spec.txt'
const PAPERS = '/tmp/jc_english_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE ENGLISH (NCCA reformed spec, first examined 2017) before it becomes
a student app's single source of truth. Default to FAIL with findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC TEXT: ${SPEC} (3 strands Oral Language/Reading/Writing,
3 cross-cutting elements, 39 learning outcomes). REAL PAPERS: ${PAPERS}/jc-english-YYYY-{HL,OL}-{paper,marking-scheme}.txt
for 2022-2025 (JC exams cancelled 2020-2021).
The taxonomy deliberately uses the 3 official strands but EXAMINABLE-CONTENT-AREA subtopics (comprehension, studied novel,
Shakespeare/drama, poetry, film, functional writing, creative writing) rather than the spec's abstract 3 elements — that is
an intentional design choice for a student-facing, exam-focused tool. Judge whether the subtopics are LEGITIMATE
(traceable to spec learning outcomes / prescribed material) and COMPLETE for the exam, not whether they copy the elements.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 3 strand names exactly the official ones (Oral Language, Reading, Writing)? (2) Is every subtopic a real, examinable JC English content area traceable to the spec's learning outcomes or the prescribed-material requirements (read ${SPEC})? (3) Is anything INVENTED (a content area not in JC English) or misplaced under the wrong strand? Quote the spec where a node deviates.` },
  { key: 'exam-coverage-hl', prompt: `${COMMON}\n\nYOUR LENS: HL EXAM COVERAGE. Read the 2024 and 2023 HL papers in ${PAPERS}. For EVERY question, state which draft subtopic id it maps to. A question with NO natural home = blocker. Also flag any draft subtopic no HL question touches (note).` },
  { key: 'exam-coverage-ol', prompt: `${COMMON}\n\nYOUR LENS: OL EXAM COVERAGE. Same as HL but for the 2024 and 2023 ORDINARY papers in ${PAPERS}.` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + LEVEL/STRUCTURE. (1) Is any examinable JC English area MISSING from the taxonomy (e.g. a genre the exam tests with no home)? (2) Is the Oral Language strand appropriately handled (it is mainly CBA, not the written exam — is its inclusion + thinness reasonable)? (3) Are levels right (HL+OL, both exist)? (4) Any structural problem (duplicate ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC English taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
