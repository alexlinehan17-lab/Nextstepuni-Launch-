export const meta = {
  name: 'jc-maths-taxonomy-verify',
  description: 'Adversarially verify the draft JC Mathematics taxonomy against the official NCCA spec + the real 2022-2025 JC Maths papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage HL, exam coverage OL, completeness/structure' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_maths_taxonomy_draft.json'
const SPEC = '/tmp/jc_maths_spec.txt'
const PAPERS = '/tmp/jc_maths_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE MATHEMATICS (Ireland; NCCA reformed specification, introduced in
schools 2018, first examined by the SEC 2022 — NOT the old Project Maths Junior Certificate syllabus, NOT Leaving Cert)
before it becomes a student app's single source of truth. Default to FAIL with findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC SUMMARY: ${SPEC} (built from the real spec PDF — the four
contextual strands Number / Geometry and trigonometry / Algebra and functions / Statistics and probability, PLUS a
content-free Unifying strand of six elements that permeates the others; learning outcomes coded U.x / N.x / GT.x / AF.x /
SP.x). REAL PAPERS: ${PAPERS}/jc-maths-YYYY-{HL,OL}-{paper,marking-scheme}.txt for 2022-2025 (single terminal paper per
level, HL+OL, 270 marks, ~2h; JC exams were cancelled 2020-2021).
The taxonomy deliberately keeps the Unifying strand as a clearly-labelled, content-free strand (no standalone exam
question maps to it — its skills surface across questions) and puts ALL examinable content under the four contextual
strands. Judge whether the strand names are the OFFICIAL ones, whether every subtopic is a LEGITIMATE examinable JC Maths
content area traceable to the spec's learning outcomes, and whether the set is COMPLETE for the exam.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 4 contextual strand names EXACTLY the official ones (Number; Geometry and trigonometry; Algebra and functions; Statistics and probability)? Is the Unifying strand handled honestly (content-free, six named elements: Building blocks, Representation, Connections, Problem solving, Generalisation and proof, Communication)? (2) Is every subtopic a real, examinable JC Maths content area traceable to the spec's learning outcomes (read ${SPEC})? (3) Is anything INVENTED (a content area not in JC Maths, or a Leaving-Cert/Project-Maths-only topic like calculus or the unit circle) or misplaced under the wrong strand? Quote the spec where a node deviates.` },
  { key: 'exam-coverage-hl', prompt: `${COMMON}\n\nYOUR LENS: HL EXAM COVERAGE. Read the 2024 and 2023 HL papers + marking schemes in ${PAPERS}. For EVERY question (and major sub-part), state which draft subtopic id it maps to. A question/part with NO natural home = blocker. Note cross-strand questions explicitly. Also flag any draft subtopic that NO HL question touches across both years (note).` },
  { key: 'exam-coverage-ol', prompt: `${COMMON}\n\nYOUR LENS: OL EXAM COVERAGE. Same as HL but for the 2024 and 2023 ORDINARY papers + schemes in ${PAPERS}. Note where OL omits content HL covers (and whether the taxonomy still fits both levels with one shared strand set).` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + STRUCTURE. (1) Is any examinable JC Maths content area MISSING from the taxonomy (a topic the exam tests with no home — e.g. Pythagoras, sets/Venn, financial maths, coordinate geometry, functions/graphs, statistics graphs)? (2) Is the Unifying-strand inclusion + content-free labelling reasonable for an exam-focused tool? (3) Are levels right (HL+OL, both exist)? (4) Any structural problem (duplicate ids, non-sequential ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC Mathematics taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered (e.g. Project-Maths-syllabus vs reformed-spec confusion; a Leaving-Cert topic that crept in; the unifying strand double-counting content)? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
