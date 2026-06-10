export const meta = {
  name: 'jc-business-taxonomy-verify',
  description: 'Adversarially verify the draft JC Business Studies taxonomy against the official NCCA spec + the real 2022-2025 JC Business Studies (Common Level) papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage 2024, exam coverage 2023+2025, completeness/structure' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_business_taxonomy_draft.json'
const SPEC = '/tmp/jc_business_spec.txt'
const PAPERS = '/tmp/jc_business_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE BUSINESS STUDIES (Ireland; NCCA reformed specification, first
examined 2019; COMMON LEVEL only — there is NO Higher/Ordinary split) before it becomes a student app's single source of
truth. Default to FAIL with findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC SUMMARY: ${SPEC} (THREE strands: 'Personal finance',
'Enterprise', 'Our economy'; 35 learning outcomes coded 1.x / 2.x / 3.x; outcomes are cross-grouped by three pedagogical
ELEMENTS — Managing my resources / Exploring business / Using skills for business — which are NOT taxonomy nodes). REAL
PAPERS: ${PAPERS}/jc-business-studies-YYYY-CL-{paper,marking-scheme}.txt for 2022-2025 (single Common-Level terminal paper,
270 marks, ~2h, Section A 15 short Qs + Section B 3 long applied Qs incl. accounting/numerical work; JC exams cancelled
2020-2021).
The accounting/numerical work (analysed cash book, ledgers, trial balance, final/trading/profit&loss accounts, club &
household budgets, ratios/interpreting accounts) is NOT a separate strand — it lives as the 'Using skills for business'
outcomes INSIDE the three strands. Judge whether the strand names are the OFFICIAL ones, whether every subtopic is a
LEGITIMATE examinable JC Business Studies content area traceable to the spec's learning outcomes, and whether the set is
COMPLETE for the written exam.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 3 strand names EXACTLY the official ones (Personal finance; Enterprise; Our economy)? (2) Is every subtopic a real, examinable JC Business Studies content area traceable to the spec's learning outcomes (read ${SPEC})? (3) Is anything INVENTED (a content area not in JC Business Studies, or a Leaving-Cert-only topic like detailed depreciation methods or break-even analysis if not in the JC spec) or misplaced under the wrong strand? Note where a node is examinable-but-not-a-discrete-LO (e.g. forms of business ownership, ratios) and whether the placement/justification is honest. Quote the spec where a node deviates.` },
  { key: 'exam-coverage-2024', prompt: `${COMMON}\n\nYOUR LENS: 2024 EXAM COVERAGE. Read the 2024 CL paper + marking scheme in ${PAPERS}. For EVERY question (Section A Q1-15 and Section B Q16-18, including the accounting/numerical parts — analysed cash book, final accounts, ratios, budgets) state which draft subtopic id it maps to. A question/part with NO natural home = blocker. Flag any draft subtopic no 2024 question touches (note).` },
  { key: 'exam-coverage-2023-2025', prompt: `${COMMON}\n\nYOUR LENS: 2023 + 2025 EXAM COVERAGE. Same as the 2024 lens but for the 2023 AND 2025 CL papers + schemes in ${PAPERS}. Confirm every question maps to a strand/subtopic across both years; note how Section B integrates multiple strands in one applied question.` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + STRUCTURE. (1) Is any examinable JC Business Studies content area MISSING (a topic the exam tests with no home — e.g. household budget, analysed cash book, club accounts, trading/profit&loss account, statement of financial position, ratios, consumer rights, saving/borrowing/insurance, banking, taxation PAYE/USC/PRSI/DIRT, business plan/enterprise skills, marketing mix, forms of ownership, business documents, work/employment, economic systems, supply&demand, government/National Budget, international trade, sustainability/ethics)? (2) Is the level right (COMMON only — confirm levels:['common'] and category 'business', NOT higher/ordinary)? (3) Any structural problem (duplicate ids, non-sequential ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC Business Studies taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered (e.g. a Leaving-Cert accounting topic that crept in; the element-grouping mistaken for strands; levels accidentally including higher/ordinary; the heavily-examined analysed-cash-book / final-accounts having a clear home)? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
