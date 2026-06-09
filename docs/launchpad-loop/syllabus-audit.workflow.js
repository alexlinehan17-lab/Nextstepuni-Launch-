export const meta = {
  name: 'syllabus-audit',
  description: 'Audit curriculum.ts accuracy per subject vs the official SEC/NCCA spec + author the Syllabus X-Ray prioritisation overlay (single source of truth)',
  phases: [
    { title: 'Audit', detail: 'per subject: accuracy check + strand prioritisation overlay' },
    { title: 'Verify', detail: 'skeptic checks corrections + overlay vs spec' },
  ],
}

const subjectIds = Array.isArray(args) ? args : JSON.parse(args)  // array of subject id strings (args may arrive stringified)
const INPUT = '/tmp/syllabus_audit_input.json'  // full per-subject taxonomy: [{id,name,levels,strands:[{id,name,subtopics:[{id,name}]}],coarseTopicsRef}]

const SHARED = `
You are auditing ONE Leaving Certificate subject's taxonomy and authoring its study-prioritisation overlay, to make
curriculum.ts the SINGLE SOURCE OF TRUTH that Syllabus X-Ray, Catch-Up Lane and Command-Word all share.

FIRST: read ${INPUT} (a JSON array) and find the object whose "id" equals YOUR subject id (given below). That object
has the subject's CURRENT curriculum structure (strands -> subtopics, each with a STABLE id) and, where it exists, a
"coarseTopicsRef" list of legacy Syllabus X-Ray topic names (reference only). Use python3/jq/Read to extract it.

TWO JOBS:

(1) ACCURACY AUDIT vs the official spec. Use WebSearch/WebFetch to find the official Leaving Certificate specification
for this subject (curriculumonline.ie / ncca.ie / examinations.ie) and compare. Classify every correction by ID-SAFETY,
because ~700 existing content cards reference these strand/subtopic IDs:
  - 'rename-strand' / 'rename-subtopic'  → SAFE (id unchanged, name improved). Give targetId + newName.
  - 'add-subtopic'  → SAFE. Give parentStrandId + newName (the main loop will assign the next id).
  - 'add-strand'    → SAFE. Give newName + its subtopics.
  - 'flag-structural' → DANGEROUS (would remove/re-index/merge existing ids and could orphan content). DO NOT propose as
    an applied change — only FLAG it with a detail note for human review.
Prefer the smallest set of corrections that makes the taxonomy accurate. If the structure is already accurate, say so.

(2) PRIORITISATION OVERLAY. For EACH existing strand (by its strandId), author study-prioritisation metadata grounded in
the REAL exam structure (paper layout + mark allocation):
  - section: the paper/section label where this strand is examined (e.g. 'Section A (Q1)', 'Paper 2', 'Section B').
  - markWeight: approximate % of total exam marks this strand can occupy (integer or 1-decimal; across a subject the
    strand weights should be plausible relative to each other — they need not sum to exactly 100).
  - examFrequency: 1-10 (10 = appears every year).
  - difficulty: 1-5 (5 = very hard).
  - studyHours: estimated hours to study this strand thoroughly.
  - tip: ONE specific, exam-savvy sentence (not generic) — name the guaranteed question, the common trap, or the
    highest-yield sub-area. BANNED: 'study hard', 'manage time', 'practise', anything generic.
Also author per-subject meta: totalMarks (the exam total), papers [{name, marks, duration}], keyAdvice (2-3 sentences of
the single most useful strategic guidance for this subject's paper).
Where the legacy coarse topics map onto strands, reuse their insight (weights/tips) — but key everything to the real strandIds.

Return ONLY the structured output. Do NOT edit any file.
`

const SCHEMA = {
  type: 'object',
  required: ['subjectId', 'accuracyVerdict', 'corrections', 'subjectMeta', 'strandOverlay'],
  properties: {
    subjectId: { type: 'string' },
    accuracyVerdict: { type: 'string', enum: ['accurate', 'minor-fixes', 'major-gaps'] },
    accuracyNotes: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
    corrections: {
      type: 'array',
      items: {
        type: 'object',
        required: ['type', 'detail'],
        properties: {
          type: { type: 'string', enum: ['rename-strand', 'rename-subtopic', 'add-subtopic', 'add-strand', 'flag-structural'] },
          targetId: { type: 'string' }, parentStrandId: { type: 'string' }, newName: { type: 'string' },
          newSubtopics: { type: 'array', items: { type: 'string' } },
          detail: { type: 'string' },
        },
      },
    },
    subjectMeta: {
      type: 'object',
      required: ['totalMarks', 'papers', 'keyAdvice'],
      properties: {
        totalMarks: { type: 'integer' },
        papers: { type: 'array', items: { type: 'object', properties: { name: { type: 'string' }, marks: { type: 'integer' }, duration: { type: 'string' } } } },
        keyAdvice: { type: 'string' },
      },
    },
    strandOverlay: {
      type: 'array',
      items: {
        type: 'object',
        required: ['strandId', 'section', 'markWeight', 'examFrequency', 'difficulty', 'studyHours', 'tip'],
        properties: {
          strandId: { type: 'string' }, section: { type: 'string' },
          markWeight: { type: 'number' }, examFrequency: { type: 'integer' }, difficulty: { type: 'integer' }, studyHours: { type: 'integer' }, tip: { type: 'string' },
        },
      },
    },
  },
}

phase('Audit')
log(`Auditing ${subjectIds.length} subjects`)

const results = await pipeline(
  subjectIds,
  // Stage 1: audit + author
  (id) => agent(
    `${SHARED}\n\nYOUR SUBJECT id: "${id}". Read ${INPUT}, extract that subject object, then audit it and author one ` +
    `strandOverlay entry per strand id, plus the corrections and subjectMeta. Use WebSearch/WebFetch to ground accuracy in the official spec.`,
    { label: `audit:${id}`, phase: 'Audit', schema: SCHEMA },
  ),
  // Stage 2: skeptic verify
  (audit, id) => audit ? agent(
    `Independent SKEPTIC reviewing an audit + prioritisation overlay for Leaving Cert subject id "${id}". First read ${INPUT} and ` +
    `extract that subject's real strand ids. Use WebSearch if needed. Check, and return a corrected version if anything is off:\n` +
    `1. Does every strandOverlay.strandId EXACTLY match one of this subject's real strand ids in the input file? Drop/fix any that don't; ensure EVERY strand has exactly one overlay entry.\n` +
    `2. Are the accuracy corrections correct and correctly ID-safety-classified (renames/adds = safe; anything removing/re-indexing existing ids must be 'flag-structural', NOT applied)?\n` +
    `3. Is the overlay sane: markWeights plausible relative to each other, examFrequency/difficulty realistic, tips SPECIFIC (no generic filler), section labels matching the real paper?\n` +
    `4. Is subjectMeta (totalMarks, papers, keyAdvice) correct for the real exam?\n` +
    `Return the FULL corrected object (same schema). If it was already sound, return it unchanged.\n\n` +
    `THE AUDIT:\n${JSON.stringify(audit)}`,
    { label: `verify:${id}`, phase: 'Verify', schema: SCHEMA },
  ) : null,
)

const kept = results.filter(Boolean)
log(`Audited+verified ${kept.length}/${subjectIds.length} subjects`)
const flags = kept.flatMap((k) => (k.corrections || []).filter((c) => c.type === 'flag-structural').map((c) => `${k.subjectId}: ${c.detail}`))
log(`Structural flags for human review: ${flags.length}`)
return { kept, structuralFlags: flags, count: kept.length }
