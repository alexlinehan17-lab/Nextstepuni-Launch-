# Exam-topic parity audit

Status: active — not a completion record.

## Decision

NextStepUni keeps two linked taxonomies:

1. The canonical curriculum hierarchy resolved through `curriculumRegistry.ts`.
   Curriculum Online/NCCA remains authoritative here. Syllabus X-Ray tracks
   this complete hierarchy, including syllabus content that has no neat past-
   paper question bucket.
2. A level-aware exam-practice hierarchy used by Topic Atlas and, as each deck
   is migrated, Mark Bank. StudyClix is the initial comparison reference for
   this browse layer because its groupings are familiar and useful to students.

The exam layer is an overlay, not a replacement. This avoids deleting official
syllabus nodes, breaking saved mastery IDs, or losing a valid NextStepUni
question merely because a reference site did not classify it.

## Provenance boundary

The audit records factual metadata only: topic labels, level, official State-
exam question identity, and counts of excluded mock associations. It does not
copy StudyClix question text, solutions, notes, videos, or commercial mock
content. Missing official questions must come from NextStepUni's SEC corpus (or
another source we are entitled to use), not from a competitor's files.

Commercial mock papers remain out of scope unless NextStepUni separately owns
the relevant reproduction rights.

## Reference hierarchy snapshot — 3 September 2026

The signed-in Leaving Certificate subject index and every linked level/course
variant were traversed. The factual hierarchy snapshot in
`data/examTopics/studyclix-subject-taxonomy.json` contains:

- 35 reference subject slugs;
- 84 level/course variants;
- 99 nested topic groups;
- 1,747 leaf topic labels.

All 84 variants resolved, every nested group has a label, and topic paths are
unique inside each variant. `data/examTopics/studyclixSubjectMap.ts` explicitly
reconciles every reference subject with a Paper Trail/curriculum ID or marks it
as a future subject with no SEC paper yet. This snapshot is an audit input, not
an instruction to replace official NCCA curriculum structure.

The sweep also exposed and fixed an independent Paper Trail generator error:
same-named Leaving Certificate Applied entries could overwrite the canonical
Leaving Certificate curriculum link. Engineering, French, German, Italian,
Spanish and Technology now point to their LC curriculum records, and History no
longer points to the retired early-modern record. A generator regression test
prevents cross-cycle curriculum IDs from returning.

## Stable identities

An audited official association uses:

`{ cycle, subject, level, year, sitting, paper slot, question }`

Level and sitting are not optional. A label is display text, never the durable
join key. Multi-paper subjects cannot be activated until the paper slot is
captured explicitly.

## Accounting pilot — 3 September 2026

The signed-in Premium topic pages were swept at both levels and committed as
metadata in `data/examTopics/accounting.json`.

| Measure | Higher | Ordinary | Total |
| --- | ---: | ---: | ---: |
| Topic buckets | 22 | 21 | 43 |
| Official topic associations | 238 | 204 | 442 |
| Distinct official questions | 215 | 197 | 412 |
| Excluded mock topic associations | 200 | 193 | 393 |

The 412 distinct reference questions break down as follows:

- 304 main-paper questions from 2010–2026;
- 18 explicitly labelled deferred-paper questions from 2022 and 2023;
- 90 main-paper questions from 2005–2009.

NextStepUni's current local Accounting corpus contains the 306 main-paper
questions from 2010–2026. The reference topic pages omit two of them:

- 2017 Higher Q4 — the SEC paper titles it “Departmental Final Accounts of a
  Sole Trader”; it is retained under Higher `Final Accounts - Sole Trader`.
- 2017 Ordinary Q5 — retained under Ordinary `Interpretation of Accounts`.

Those are explicit preservation exceptions, not silent count adjustments.

The Topic Atlas pilot now renders:

- the exact 22 Higher and 21 Ordinary reference topic labels;
- separate Higher Level and Ordinary Level sections;
- all 306 local main-paper questions from 2010–2026;
- distinct question counts (English and Irish editions no longer inflate the
  headline as if they were different questions);
- a many-to-many crosswalk back to canonical Accounting syllabus nodes.

Question crops and available marking-scheme reveals were verified in the local
demo account. The 2023 Higher cash-budget question, for example, renders its
paper crop and SEC marking-scheme regions in the topic feed.

### Accounting work still open

- Acquire and verify the official SEC PDFs and schemes for the 90 questions
  from 2005–2009 before adding them to Paper Trail.
- Acquire and verify the official 2022/2023 deferred papers and schemes before
  adding those 18 questions.
- Complete the paper-by-paper visual and marking-scheme sweep required before
  declaring the Accounting corpus complete.
- Map an eventual Accounting Mark Bank deck to the exam-topic IDs without
  changing or deleting any existing card identity.
- Surface the exam-topic ↔ syllabus crosswalk in Syllabus X-Ray/War Room.

## Applied Mathematics pilot — 3 September 2026

Both levels were swept down to their official State-exam headings. The exact
reference menu is now the Topic Atlas browse layer:

| Measure | Higher | Ordinary | Total |
| --- | ---: | ---: | ---: |
| Topic buckets | 15 | 18 | 33 |
| Official heading associations | 226 | 143 | 369 |
| Main-paper heading associations | 183 | 125 | 308 |
| Deferred heading associations | 26 | 0 | 26 |
| Sample-paper heading associations | 17 | 18 | 35 |

New-format questions are often classified by part rather than only by their
top-level question number. The audit therefore retains the factual subdivision
label for future Mark Bank card mapping while Topic Atlas joins all applicable
parts back to the top-level Paper Trail question. One question can legitimately
appear under several topics.

NextStepUni has 318 distinct, anchored main-paper questions from 2010–2026:
170 Higher and 148 Ordinary. The reference menu covers every local question
from 2023 onward, but its topic pages omit 113 valid questions from 2010–2022.
Those omissions are retained through their already-verified canonical tags and
recorded individually as preservation associations. No source question or
question identity was removed.

Some retained former-course material has no like-for-like Higher-level label in
the current reference menu. It is conservatively discoverable through the
closest current concept (for example, relative velocity through `Vectors`, and
equilibrium material through `Newton's laws & Connected Particles`) while its
canonical syllabus tag remains unchanged. Ordinary-level legacy labels such as
`Relative Velocity`, `Statics`, `Centre of Gravity`, and `Hydrostatics` remain
available directly. Empty reference buckets are still rendered with a zero
count so the menu itself does not drift.

### Applied Mathematics work still open

- Acquire official SEC sources for referenced 2007–2009, deferred and sample
  questions before adding any missing papers to NextStepUni.
- Visually verify every newly surfaced 2023–2026 paper/question anchor and
  marking-scheme region, including the Irish edition used where an English
  answer map is not yet verified.
- Map part-aware references to independently stable Mark Bank card IDs.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## Agricultural Science pilot — 3 September 2026

Both levels now use the exact reference browse menu while retaining the
official curriculum hierarchy underneath it:

| Measure | Higher | Ordinary | Total |
| --- | ---: | ---: | ---: |
| Topic buckets | 19 | 16 | 35 |
| Official heading associations | 561 | 466 | 1,027 |
| Excluded mock associations | 544 | 466 | 1,010 |

The part-aware parser normalises pre-2021 lettered short questions to their
top-level Paper Trail identity while keeping the original subdivision label as
factual metadata. The reference associations resolve to 533 distinct official
questions: 411 main-paper questions from 2010 onward, 74 older main-paper
questions, 18 deferred-paper questions and 30 sample-paper questions.

NextStepUni has 458 anchored main-paper questions from 2010–2026: 207 Higher
and 251 Ordinary. Forty-seven valid local questions are absent from the
reference topic pages and are therefore recorded as explicit preservation
associations. This includes 2021 Higher Q4, which was missing from both the
reference and the earlier local tagging wave; it remains discoverable under
the environment topic based on the official SEC question.

The local demo was checked against the activated menu. It reports 458 distinct
questions across all 35 buckets, and the 2026 Animal Diseases feed renders its
paper crops and SEC marking-scheme crops without fallback cards.

### Agricultural Science work still open

- Acquire and verify official SEC sources for the 74 pre-2010, 18 deferred and
  30 sample-paper questions before adding those paper editions.
- Complete the full paper-by-paper crop and marking-scheme sweep.
- Map part-aware associations to stable Mark Bank card IDs.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## LCVP Link Modules pilot — 4 September 2026

The Common-level browse layer now contains the exact ten reference buckets,
including the eight content headings plus `Audio Visual` and `Case Study`.
The raw reference snapshot contains 181 official headings and 120 excluded
mock associations. Expanding section-level ranges and lists produces 348
part-aware references: 318 main and 30 deferred.

Paper Trail restarts printed question numbers in each section, whereas its
stable local identity is continuous. The bridge therefore maps Section A
questions 1–8 to local Q1–Q8, Section B questions 1–3 to local Q9–Q11, and
Section C questions to local Q12 onward. That preserves all 295 anchored
main-paper questions from 2010–2026. Twenty-five local questions omitted by the
reference are recorded individually rather than dropped.

The local demo reports 295 distinct questions across ten topics. The `Audio
Visual` feed spans all 17 local years, has no crop fallbacks, and its first 2026
paper crop and matching SEC marking-scheme crop were verified in-browser.

### Link Modules work still open

- Acquire and verify official sources for the 36 pre-2010 main-paper questions
  and 30 deferred-paper questions represented by the reference.
- Complete the full paper-by-paper crop and marking-scheme sweep.
- Map section-aware associations to stable Mark Bank card IDs.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## Classical Studies pilot — 4 September 2026

The exact eight-bucket reference menu is now active independently at Higher
and Ordinary level. The reference snapshot contains 169 Higher and 184
Ordinary official heading associations, with no commercial mock entries. Those
353 associations resolve to 287 distinct reference question identities: 258
main-paper questions and 29 sample-paper questions.

NextStepUni has 378 anchored main-paper questions from 2010–2026: 194 Higher
and 184 Ordinary. The reference omits 153 of those local identities, primarily
because its modern eight-topic menu retains only selected fragments of the
retired ten-topic course and because its topic pages do not yet include 2026.
All 153 are explicit preservation associations. Retired-course questions are
cross-listed conservatively in the closest surviving bucket; all 32 questions
from 2026 were classified directly from the official SEC papers.

The local demo reports 378 distinct questions across the 16 level-scoped
buckets. Both topic groups and all eight labels were verified in-browser. The
2026 Higher `Temples` feed renders Questions 1, 2 and 15 without fallback cards,
and the Question 1 SEC marking-scheme crop opens correctly.

### Classical Studies work still open

- Acquire and verify the 33 referenced pre-2010 main-paper questions and the
  29 sample-paper questions before adding those paper editions.
- Complete the full paper-by-paper crop and marking-scheme sweep.
- Map the exam-topic identities to stable Mark Bank card IDs.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## Politics and Society pilot — 4 September 2026

The exact ten-bucket reference menu is now active independently at Higher and
Ordinary level. It keeps the eight official content themes student-friendly,
then adds two useful overlapping practice lenses: `Data-Based Questions` and
`Key Thinkers`.

| Measure | Higher | Ordinary | Total |
| --- | ---: | ---: | ---: |
| Topic buckets | 10 | 10 | 20 |
| Official heading associations | 267 | 257 | 524 |
| Excluded mock associations | 217 | 254 | 471 |

The SEC paper structure does not map one-to-one to those headings. Higher-level
Section A lettered items form one local Q1 card and its complete data-based
Section B forms Q2. Ordinary-level Section B is exposed locally as Q2–Q4 even
where the reference abbreviates the whole section to “Question 2”. Expanding
that structure yields 550 part-aware references: 467 main, 27 deferred and 56
sample-paper associations.

NextStepUni has 140 distinct anchored main-paper cards from 2018–2026: 60
Higher and 80 Ordinary. Every card remains reachable. The reference omits two
valid Higher cards:

- 2018 Q4 is retained from its frozen, hand-verified curriculum tags under the
  relevant Irish human-rights and national decision-making themes.
- 2024 Q2 is retained under `Data-Based Questions`, national/European
  decision-making, and human rights in Ireland after direct inspection of the
  official SEC paper on women’s political representation and gender quotas.

The exam-practice menu is linked many-to-many to the official curriculum.
`Data-Based Questions` intentionally spans all eight themes because it is an
assessment format, while `Key Thinkers` links only to the curriculum’s thinker
nodes. This keeps Syllabus X-Ray authoritative without losing either of the
two cross-cutting practice views.

The local demo reports all 140 cards across the 20 buckets. Browser QA verified
the omitted 2018 Higher Q4, all three 2026 Ordinary DBQ cards, and the complete
2024 Higher Q2 paper and marking-scheme crops. That sweep also fixed the crop
guard for legitimately long Politics booklets and raised the bounded PDF LRU
above one normal eight-card viewport so active renders are not evicted.

### Politics and Society work still open

- Complete the full paper-by-paper crop and marking-scheme sweep.
- Map the part-aware exam associations to stable Mark Bank card IDs.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## Japanese audit — in progress, 4 September 2026

The reference uses one shared fourteen-topic menu rather than separate Higher
and Ordinary menus. It contains 232 official heading associations, no mock
associations, and three especially useful aural buckets: `Conversation`,
`Interview/Speech`, and `Radio/News`. The menu currently stops at 2025, so its
labels are a useful browse model but its question list is not a complete source
of truth for the current SEC corpus.

The first official-paper comparison found a structural defect in NextStepUni's
2026 listening sidecars. Parts A, B, C and D restart their printed question
numbers, but the generated maps treated the number alone as unique. Both levels
therefore omitted every Part B and Part C card plus Part D questions 1–3. The
repair adds sixteen previously inaccessible cards while preserving every
existing stable ID:

| 2026 listening | Before | After | Recovered |
| --- | ---: | ---: | ---: |
| Higher | 8 | 16 | 8 |
| Ordinary | 7 | 15 | 8 |

Every recovered paper crop and SEC marking-scheme crop was rendered and checked
side by side. An explicit physical `printOrder` now records the true sequence
without renumbering shipped cards, and section-end guards prevent the next
section's heading from bleeding into the previous crop. The new cards are also
tagged against the canonical Japanese listening nodes: conversation,
interview/speech, and radio/news.

### Japanese work still open

- Do not activate the fourteen-topic exam overlay yet. The 2024–2026 written
  papers lack complete per-question maps, and the existing 2023 written maps do
  not expose the Section 4/5 production tasks represented in the reference.
- Recover those written cards from the official SEC papers and map Higher and
  Ordinary separately even though the student-facing menu is shared.
- Reconcile all 232 reference headings against every retained local identity;
  keep 2026 official questions as explicit reference omissions.
- Upload the two corrected 2026 listening sidecars through the audited Storage
  publish manifest before relying on them outside local/tests.
- Complete the full cross-year paper and marking-scheme visual sweep, then map
  stable Mark Bank cards and expose the syllabus crosswalk in Syllabus X-Ray.

## Preservation gates

Every subject migration must pass all of these before activation:

1. Freeze the exact pre-migration local paper/question identities.
2. Prove every frozen identity remains reachable after the migration.
3. Prove every local question has at least one exam-topic association.
4. Prove every exam-topic ID and canonical crosswalk target resolves.
5. Reconcile each reference official question as present, added from an
   authorised official source, or explicitly excluded with a written reason.
6. Keep commercial mock content excluded unless rights are documented.
7. For Mark Bank, run card-ID preservation plus curriculum/deck regressions.
8. Visually sweep every official paper and cross-check the marking scheme
   before a subject receives a complete status.

The project-level goal is not complete until these gates pass for every
applicable subject.
