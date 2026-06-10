export const meta = {
  name: 'jc-history-taxonomy-verify',
  description: 'Adversarially verify the draft JC History taxonomy against the official NCCA spec + the real 2022-2025 JC History (Common Level) papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage 2024, exam coverage 2023+2025, completeness/structure' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_history_taxonomy_draft.json'
const SPEC = '/tmp/jc_history_spec.txt'
const PAPERS = '/tmp/jc_history_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE HISTORY (Ireland; NCCA reformed specification, first examined 2019;
COMMON LEVEL only, NO Higher/Ordinary) before it becomes a student app's single source of truth. Default to FAIL with
findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC SUMMARY: ${SPEC} (THREE strands: 'The nature of history',
'The history of Ireland', 'The history of Europe and the wider world'; 38 learning outcomes coded 1.x / 2.x / 3.x. Strand 1
'The nature of history' is a unifying strand whose working-with-evidence skills — sources primary vs secondary, bias/
propaganda, chronology, cause & consequence, change & continuity, historical significance, empathy, the historian's job &
archaeology — PERMEATE strands 2 & 3 and are examined throughout). REAL PAPERS:
${PAPERS}/jc-history-YYYY-CL-{paper,marking-scheme}.txt for 2022-2025 (single Common-Level terminal paper, 360 marks, ~2h,
8 questions; source/document/cartoon/photo heavy; JC exams cancelled 2020-2021).
The draft puts 'The nature of history' FIRST (jc-history-0) because its skills are the most examined — a sensible
student-facing ordering, but the OFFICIAL strand names must be exact. Judge whether the 3 strand names are exact, whether
every subtopic is a LEGITIMATE examinable area traceable to a real learning outcome, and whether the set is COMPLETE for
the written exam. Each year's paper SAMPLES a subset of LOs — a subtopic untouched in one year is fine if it is a real LO.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 3 strand names EXACTLY the official ones (The nature of history; The history of Ireland; The history of Europe and the wider world)? (2) Is every subtopic a real, examinable JC History content area/skill traceable to a real learning outcome (read ${SPEC})? (3) Is the 'nature of history' skills group accurate (sources, bias/propaganda, chronology, cause & consequence, change & continuity, significance, empathy, the historian's job/archaeology)? (4) Is anything INVENTED or a Leaving-Cert-only topic, or misplaced under the wrong strand (Irish content under Ireland, wider-world content under Europe & wider world)? Quote the spec where a node deviates.` },
  { key: 'exam-coverage-2024', prompt: `${COMMON}\n\nYOUR LENS: 2024 EXAM COVERAGE. Read the 2024 CL paper + marking scheme in ${PAPERS}. For EVERY question (incl. the source-analysis / document / cartoon / photo parts) state which draft subtopic id it maps to — the skills parts should map to jc-history-0. A question/part with NO natural home = blocker. Flag any draft subtopic no 2024 question touches (note — fine if it is a real LO sampled in another year).` },
  { key: 'exam-coverage-2023-2025', prompt: `${COMMON}\n\nYOUR LENS: 2023 + 2025 EXAM COVERAGE. Same as the 2024 lens but for the 2023 AND 2025 CL papers + schemes in ${PAPERS}. Confirm every question maps to a strand/subtopic across both years; note how heavily the source/skills (jc-history-0) appear.` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + STRUCTURE. (1) Is any examinable JC History area MISSING (a topic the exam tests with no home — e.g. working with sources/bias/propaganda, chronology, cause & consequence, the historian's job/archaeology; ancient civilisations, the Middle Ages, the Renaissance, the Reformation, plantations, the Famine, exploration/colonisation, the Age of Revolutions/1798, the Industrial Revolution, the 1916 Rising/War of Independence/Civil War, the World Wars, fascism/Nazism/Stalin, the Holocaust, the Cold War, Northern Ireland/the Troubles, social change in 20th-century Ireland, the EU, patterns of change/significance)? (2) Is the level right (COMMON only — confirm levels:['common'] and category 'social-environmental', NOT higher/ordinary)? (3) Any structural problem (duplicate ids, non-sequential ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC History taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered (e.g. a Leaving-Cert topic that crept in; Irish vs wider-world content misfiled; the skills strand double-counting content; levels accidentally including higher/ordinary)? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
