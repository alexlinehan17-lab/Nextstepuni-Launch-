export const meta = {
  name: 'jc-science-taxonomy-verify',
  description: 'Adversarially verify the draft JC Science taxonomy against the official NCCA spec + the real 2022-2025 JC Science (Common Level) papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage 2024, exam coverage 2023+2025, completeness/structure' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_science_taxonomy_draft.json'
const SPEC = '/tmp/jc_science_spec.txt'
const PAPERS = '/tmp/jc_science_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE SCIENCE (Ireland; NCCA reformed specification, introduced 2016,
first examined by the SEC 2019; COMMON LEVEL only — there is NO Higher/Ordinary split) before it becomes a student app's
single source of truth. Default to FAIL with findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC SUMMARY: ${SPEC} (5 strands: a unifying 'Nature of science'
PLUS four contextual strands 'Physical world', 'Chemical world', 'Biological world', 'Earth and space'; the four
contextual strands are organised by the elements Building blocks / Systems and interactions / Energy / Sustainability;
learning outcomes coded NoS / PW / CW / BW / ESS). REAL PAPERS: ${PAPERS}/jc-science-YYYY-CL-{paper,marking-scheme}.txt for
2022-2025 (single Common-Level terminal paper, 360 marks, ~2h, Section A short Qs + Section B long Qs; JC exams cancelled
2020-2021).
Unlike a pure 'unifying' strand, 'Nature of science' DOES carry examinable content here — working-scientifically skills
(fair tests, variables, accuracy/precision, apparatus, graphs/data, conclusions, safety, science-in-society) are tested
throughout every paper — so it is correctly modelled as a full strand with subtopics. Judge whether the strand names are
the OFFICIAL ones, whether every subtopic is a LEGITIMATE examinable JC Science content area traceable to the spec's
learning outcomes, and whether the set is COMPLETE for the written exam.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 5 strand names EXACTLY the official ones (Nature of science; Physical world; Chemical world; Biological world; Earth and space)? (2) Is every subtopic a real, examinable JC Science content area traceable to the spec's learning outcomes (read ${SPEC})? (3) Is anything INVENTED (a content area not in JC Science, or a Leaving-Cert-only topic) or misplaced under the wrong strand (e.g. carbon/water cycle belongs under Earth and space per the spec even though it touches chem/bio)? (4) Is the Nature-of-science strand's content (working scientifically) accurate? Quote the spec where a node deviates.` },
  { key: 'exam-coverage-2024', prompt: `${COMMON}\n\nYOUR LENS: 2024 EXAM COVERAGE. Read the 2024 CL paper + marking scheme in ${PAPERS}. For EVERY question (Section A Q1-11 and Section B), state which draft subtopic id it maps to — including the working-scientifically parts (accuracy/precision, hypotheses, variables, graphs, conclusions) which should map to Nature of science. A question/part with NO natural home = blocker. Flag any draft subtopic no 2024 question touches (note).` },
  { key: 'exam-coverage-2023-2025', prompt: `${COMMON}\n\nYOUR LENS: 2023 + 2025 EXAM COVERAGE. Same as the 2024 lens but for the 2023 AND 2025 CL papers + schemes in ${PAPERS}. Confirm every question maps to a strand/subtopic across both years; note the varying number of Section B questions year to year.` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + STRUCTURE. (1) Is any examinable JC Science content area MISSING (a topic the exam tests with no home — e.g. electricity/circuits, forces/energy, atomic structure, chemical reactions, acids/bases, cells, human biology, genetics, ecology, the carbon cycle, space/the solar system)? (2) Is the Nature-of-science strand appropriately a full content strand (not empty)? (3) Is the level right (COMMON only — confirm the draft has levels:['common'] and NOT higher/ordinary)? (4) Any structural problem (duplicate ids, non-sequential ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC Science taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered (e.g. a Leaving-Cert topic that crept in; the four contextual strands' element-grouping being mis-mapped; levels accidentally including higher/ordinary)? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
