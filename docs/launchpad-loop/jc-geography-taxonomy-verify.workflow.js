export const meta = {
  name: 'jc-geography-taxonomy-verify',
  description: 'Adversarially verify the draft JC Geography taxonomy against the official NCCA spec + the real 2022-2025 JC Geography (Common Level) papers before it becomes source of truth',
  phases: [
    { title: 'Verify', detail: '4 lenses: spec fidelity, exam coverage 2024, exam coverage 2023+2025, completeness/structure' },
    { title: 'Critic', detail: 'adjudicate + final SHIP/FIX verdict' },
  ],
}

const DRAFT = '/tmp/jc_geography_taxonomy_draft.json'
const SPEC = '/tmp/jc_geography_spec.txt'
const PAPERS = '/tmp/jc_geography_txt'

const VERDICT_SCHEMA = {
  type: 'object', required: ['lens', 'pass', 'findings'],
  properties: {
    lens: { type: 'string' }, pass: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'object', required: ['severity', 'detail'], properties: {
      severity: { type: 'string', enum: ['blocker', 'fix', 'note'] }, detail: { type: 'string' }, suggestedChange: { type: 'string' } } } },
  },
}

const COMMON = `
You verify a DRAFT syllabus taxonomy for JUNIOR CYCLE GEOGRAPHY (Ireland; NCCA reformed specification, first examined 2022
— the 2021 first sitting was cancelled for Covid; COMMON LEVEL only, NO Higher/Ordinary) before it becomes a student app's
single source of truth. Default to FAIL with findings if anything is materially off.
DRAFT: ${DRAFT} (JSON; each node has a specRef). OFFICIAL SPEC SUMMARY: ${SPEC} (THREE official strands: 'Exploring the
physical world', 'Exploring how we interact with the physical world', 'Exploring people, place and change'; 28 learning
outcomes coded 1.x / 2.x / 3.x; PLUS three cross-cutting ELEMENTS, one of which is 'Geographical skills' / graphicacy —
Mapping / Visuals / Data analysis). REAL PAPERS: ${PAPERS}/jc-geography-YYYY-CL-{paper,marking-scheme}.txt for 2022-2025
(single Common-Level terminal paper, 360 marks, ~2h; map/photo/graph heavy; JC exams cancelled 2020-2021).
The draft DELIBERATELY adds a 4th student-facing group 'Geographical skills: maps, photos & data' (jc-geography-0) for the
OS-map / aerial-photo / climate-graph skills, because those are the most heavily examined area — derived from the spec's
'Geographical skills' element, NOT invented as a strand. Judge whether the THREE official strand names are exact, whether
every subtopic (incl. the skills group) is a LEGITIMATE examinable area traceable to the spec, and whether the set is
COMPLETE for the written exam.
severity: blocker = wrong/invented/missing content that would corrupt the source of truth; fix = a naming improvement with
a suggestedChange; note = observation. pass=true only with zero blockers. Return data only.`

phase('Verify')
const LENSES = [
  { key: 'spec-fidelity', prompt: `${COMMON}\n\nYOUR LENS: SPEC FIDELITY. (1) Are the 3 OFFICIAL strand names EXACTLY right (Exploring the physical world; Exploring how we interact with the physical world; Exploring people, place and change)? (2) Is the 'Geographical skills' group honestly derived from the spec's skills element (not invented), and are its subtopics real exam skills (OS-map grid refs/scale/distance/area/height/slope, aerial/satellite photo interpretation, sketch maps, climate graphs/data)? (3) Is every contextual subtopic traceable to a real learning outcome? (4) Anything INVENTED or a Leaving-Cert-only topic, or misplaced under the wrong strand? Quote the spec where a node deviates.` },
  { key: 'exam-coverage-2024', prompt: `${COMMON}\n\nYOUR LENS: 2024 EXAM COVERAGE. Read the 2024 CL paper + marking scheme in ${PAPERS}. For EVERY question (incl. the OS-map, aerial-photo and climate-graph parts) state which draft subtopic id it maps to. A question/part with NO natural home = blocker. Flag any draft subtopic no 2024 question touches (note).` },
  { key: 'exam-coverage-2023-2025', prompt: `${COMMON}\n\nYOUR LENS: 2023 + 2025 EXAM COVERAGE. Same as the 2024 lens but for the 2023 AND 2025 CL papers + schemes in ${PAPERS}. Confirm every question maps to a strand/subtopic across both years; note how many questions are skills-based (map/photo/graph).` },
  { key: 'completeness', prompt: `${COMMON}\n\nYOUR LENS: COMPLETENESS + STRUCTURE. (1) Is any examinable JC Geography content area MISSING (a topic the exam tests with no home — e.g. OS map skills, photo interpretation, plate tectonics/volcanoes/earthquakes/fold mountains, rocks & the rock cycle, weathering & erosion (rivers/sea/glaciation), landforms, soils, weather & climate & climate graphs, climate change, the water cycle, population (distribution/density/change/migration), settlement & urbanisation, primary/secondary/tertiary economic activities, development & interdependence, resources & sustainability, fieldwork)? (2) Is the level right (COMMON only — confirm levels:['common'] and category 'social-environmental', NOT higher/ordinary)? (3) Any structural problem (duplicate ids, non-sequential ids, wrong nesting)? Read the spec ${SPEC} and the papers ${PAPERS}.` },
]

const verdicts = await parallel(LENSES.map((l) => () => agent(l.prompt, { label: `verify:${l.key}`, phase: 'Verify', schema: VERDICT_SCHEMA })))
const got = verdicts.filter(Boolean)
log(`Verdicts: ${got.length}/4 — ${got.filter((v) => v.pass).length} pass`)

phase('Critic')
const critic = await agent(
  `Completeness critic for a JC Geography taxonomy verification. The draft (${DRAFT}) was checked by 4 lenses:\n${JSON.stringify(got, null, 2)}\n\n` +
  `(1) Any material defect one lens raised but others missed? (2) Lens conflicts — re-check the spec ${SPEC} yourself to adjudicate. (3) Any verification angle nobody covered (e.g. a Leaving-Cert topic that crept in; the skills group double-counting strand content; levels accidentally including higher/ordinary; the OS-map skills having a clear home)? Give a final SHIP / FIX-FIRST verdict with the EXACT list of changes (if any) to apply before this becomes the source of truth.`,
  { label: 'completeness-critic', phase: 'Critic' },
)
return { verdicts: got, critic, passCount: got.filter((v) => v.pass).length }
