export const meta = {
  name: 'jc-irish-taxonomy-verify',
  description: 'Adversarially verify the draft JC Irish (Gaeilge T2) taxonomy against the official NCCA spec + the real 2022-2025 JC Irish papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage HL, exam coverage OL, completeness/invention' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_irish_taxonomy_draft.json'
const SPEC = '/tmp/jc_irish_spec.txt'
const PAPERS = '/tmp/jc_irish_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE IRISH (Gaeilge, specification T2 = English-medium schools, the
MAJORITY cohort; NCCA spec first examined 2022) before it becomes a student app's single source of truth. Default to FAIL
with findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC TEXT: ${SPEC} (3 snáitheanna/strands:
Cumas cumarsáide / Feasacht teanga agus chultúrtha / Féinfheasacht an fhoghlaimeora; built on five language skills
éisteacht/léamh/labhairt/idirghníomhú/scríobh; learning outcomes numbered 1.x / 2.x / 3.x). REAL PAPERS:
${PAPERS}/jc-irish-YYYY-{HL,OL}-{paper,marking-scheme}.txt for 2022-2025 (JC exams cancelled 2020-2021).
The taxonomy deliberately uses the 3 official strands but EXAMINABLE-CONTENT-AREA subtopics (Cluastuiscint/listening,
Léamhthuiscint/reading comprehension, Litríocht/studied literature, Ceapadóireacht/writing, Cruinneas/accuracy, plus the
oral Labhairt and the cultural/self-awareness areas) rather than copying the spec's abstract skill elements verbatim — that
is an intentional design choice for a student-facing, exam-focused tool. Judge whether the subtopics are LEGITIMATE
(traceable to spec learning outcomes / the exam structure) and COMPLETE for the written exam, not whether they copy the
elements. NOTE the written terminal exam tests Cluastuiscint + Léamhthuiscint + Litríocht + Ceapadóireacht + Cruinneas;
Labhairt/oral and Féinfheasacht are assessed mainly via the CBAs/oral, included for spec fidelity.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 3 strand (snáithe) names exactly the official ones (Cumas cumarsáide; Feasacht teanga agus chultúrtha; Féinfheasacht an fhoghlaimeora)? (2) Is every subtopic a real, examinable JC Irish content area traceable to the spec's learning outcomes (read ${SPEC})? (3) Are the LO-range citations in each specRef plausible/correct, or invented? (4) Is anything INVENTED (a content area not in JC Irish T2) or misplaced under the wrong strand? Quote the spec where a node deviates.` },
  { key: 'exam-coverage-hl', prompt: `${COMMON}\n\nYOUR LENS: HL EXAM COVERAGE. Read the 2024 and 2023 HL papers + marking schemes in ${PAPERS}. For EVERY question (Cluastuiscint, Léamhthuiscint, Litríocht, Ceapadóireacht, Cruinneas/gramadach), state which draft subtopic id it maps to. A question with NO natural home = blocker. Also flag any draft subtopic no HL question touches (note).` },
  { key: 'exam-coverage-ol', prompt: `${COMMON}\n\nYOUR LENS: OL EXAM COVERAGE. Same as HL but for the 2024 and 2023 ORDINARY papers + schemes in ${PAPERS}. Note where OL omits sections HL has (e.g. less Litríocht/Cruinneas), and whether the taxonomy still fits.` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + LEVEL/STRUCTURE. (1) Is any examinable JC Irish written-exam area MISSING from the taxonomy (a section of the paper with no home)? (2) Are the oral/Labhairt + Féinfheasacht strands appropriately handled (mainly CBA/oral, not the written terminal exam — is their inclusion + thinness reasonable)? (3) Are levels right (HL+OL, both exist)? (4) Any structural problem (duplicate ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC Irish (Gaeilge T2) taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered (e.g. T1 vs T2 confusion — confirm this is the T2 spec)? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
