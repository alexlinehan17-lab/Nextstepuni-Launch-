# Curriculum source of truth

Curriculum data is academic data, not interface copy. A spelling change, retired
specification or independently invented hierarchy can misstate coverage,
misallocate revision time and attach exam performance to the wrong topic.

## Authority order

1. **Curriculum Online / NCCA specification or syllabus** — content hierarchy,
   learning outcomes, cohort transition and assessment-component rules.
2. **State Examinations Commission material** — papers, marking schemes,
   examination instructions and year-specific operational detail.
3. **NextStepUni editorial metadata** — shorter display labels, aliases, study
   estimates and prioritisation. Editorial data may annotate an official node;
   it may not create a competing curriculum.

The application gateway is `curriculumRegistry.ts`. Product code should resolve
a `subject + examination year` there rather than importing a feature-local list.

## Required identity

Every stored or displayed curriculum node should carry:

- `specificationId` — for example `biology:2027`;
- stable canonical node `id`;
- official title plus optional student-facing alias;
- official source URL;
- first/last applicable examination year where a transition exists.

Names are labels, never database keys. Student mastery, Mark Bank cards and paper
tags must eventually store canonical IDs. Existing name-keyed mastery needs a
versioned migration, not an in-place rename.

## Content is not assessment structure

Strands/units describe what is taught. Papers, coursework and choice rules
describe what is assessed. They are related but cannot be flattened into one
list. Religious Education is the immediate example: Sections A–J exist, but the
written examination requires A, two of B–D and one of E–J. Coverage screens must
show those rules rather than imply that all ten are equally compulsory.

## Current transition risks

- Every selectable Leaving Certificate Established subject for the live 2026
  examination cohort has been checked against its Curriculum Online/NCCA
  syllabus or specification. The 2026 inventory gate permits no
  `audit-required` records.
- Biology, Chemistry, Physics and Business resolve to the outgoing taxonomy for
  the 2026 examination and the redeveloped taxonomy from 2027.
- Ancient Greek, Latin and Arabic resolve to purpose-built outgoing 2026
  records. Their newer strand structures and assessment arrangements are not
  allowed to leak into the 2026 cohort.
- Agricultural Science's Mark Bank taxonomy is registered against its current
  specification.
- Religious Education has official selection rules in the registry.
- Applied Mathematics has its four official strands and 20% modelling project /
  80% written assessment contract in the registry.
- History, outgoing Geography and Home Economics carry their distinct 20%
  coursework / 80% written assessment contracts. Geography's outgoing syllabus
  is explicitly bounded to the 2027 examination.
- Classical Studies, Design and Communication Graphics and Technology carry
  their verified assessment splits. Technology's two-option rule and Music's
  elective activity are represented explicitly rather than flattened into the
  content hierarchy.
- Level-dependent language assessment percentages are not represented as one
  shared weighting. Until the assessment schema supports per-level values, the
  registry links to the official table and records the distinction in notes.
- Replacement specifications outside the current 2026 scope must be introduced
  as separate year-bounded records. An outgoing taxonomy must never be extended
  into a later cohort merely to keep a subject selectable.

## Build guards

`test/curriculumRegistry.test.ts` verifies:

- unique specification and node IDs;
- correct cohort resolution at specification transitions;
- a zero-gap audit assertion for the live 2026 established-subject catalogue;
- explicit outgoing 2026 resolution for Ancient Greek, Latin and Arabic;
- official provenance for verified specifications;
- Religious Education selection-rule references;
- every built Mark Bank card resolves to the correct canonical topic.

`test/markBankCardPreservation.test.ts` additionally protects all 4,133 source
cards by ID and content fingerprint. Curriculum consolidation may remap metadata
but cannot remove, overwrite or silently hide a card.

Topic mastery now dual-writes the backwards-compatible label map and the stable
`topicMasteryV2` namespace. Exact unique labels migrate; custom or ambiguous
records remain losslessly in `unresolved`. War Room renders canonical IDs.

Syllabus X-Ray's marks/frequency overlay is only returned when all of its nodes
belong to the student's resolved specification. During a transition it shows a
verification state instead of silently attaching outgoing advice to a new
syllabus. `test/curriculumFeatureParity.test.ts` enforces this boundary.
