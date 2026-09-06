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

### Current whole-subject coverage — 5 September 2026

| Coverage status | Subjects |
| --- | ---: |
| Current/transition SEC subjects in scope | 32 |
| Audited taxonomies active in the app | 32 |
| Browser taxonomy audits still to activate | 0 |
| Future subjects with no existing SEC paper taxonomy | 3 |

All current subjects now have an active, level-aware exam taxonomy. Two linked
Physical Education replacement-course topic pages returned a persistent
StudyClix HTTP 500 during the association sweep; their labels and hierarchy are
active, while their unknown counts remain explicitly source-unavailable. The
three future-only reference entries—Climate Action and Sustainability; Drama,
Film and Theatre Studies; and Life, Community and Work (formerly LCVP)—are not
misrepresented as current SEC past-paper subjects.

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

The official-paper comparison found the same structural defect across the
2024–2026 listening sidecars. Parts A, B, C and D restart their printed question
numbers, but the generated maps had treated the number alone as unique. The
repair adds 48 previously inaccessible listening cards while preserving every
existing stable ID:

| Listening papers | Before | After | Recovered |
| --- | ---: | ---: | ---: |
| 2024 Higher + Ordinary | 17 | 33 | 16 |
| 2025 Higher + Ordinary | 14 | 30 | 16 |
| 2026 Higher + Ordinary | 15 | 31 | 16 |

The completed 2012–2022 listening sweep found five older year/level layouts
with the same restart collision in both EV and IV. Ten additive repairs retain
all 68 shipped card IDs and crops while exposing 82 previously inaccessible
question groups. The other 24 locally available maps retain their 96 existing
four-Part cards unchanged:

| Older listening maps | Before | After | Recovered |
| --- | ---: | ---: | ---: |
| 2012, four variants | 16 | 16 | 0 |
| 2013, four variants | 26 | 44 | 18 |
| 2014, four variants | 20 | 36 | 16 |
| 2015, four variants | 26 | 58 | 32 |
| 2016, four variants | 20 | 36 | 16 |
| 2017–2022, fourteen variants | 56 | 56 | 0 |
| **Total, 34 variants** | **164** | **246** | **82** |

The full-card visual pass also caught legacy answer crops polluted by the same
numbering collision. Thirteen cards now use additive, audited display regions
for the correct official answer while their frozen `region` identities remain
unchanged. Six 2015 Higher table-row cards likewise use additive paper regions
that restore their shared instructions and column headings. Explicit Part A
ends prevent all ten repaired maps from bleeding into Part B.

The 2023 written maps also stopped before their two production tasks at each
level. Those four cards are now restored, taking Higher from 30 to 32 and
Ordinary from 22 to 24.

The 2024–2026 written papers had no answer sidecars at all. Six dedicated,
reproducible maps now expose all 157 audited cards, including reading,
translation, kanji, grammar, culture and every Q4/Q5 production task:

| Written cards | Higher | Ordinary | Total |
| --- | ---: | ---: | ---: |
| 2024 | 27 | 25 | 52 |
| 2025 | 30 | 26 | 56 |
| 2026 | 20 | 29 | 49 |
| **Total** | **77** | **80** | **157** |

The 2019–2022 written maps had the same partial-coverage defect. Seven additive
repairs preserve all 153 existing IDs and expose 29 omitted assessed sections:

| Written repairs | Before | After | Recovered |
| --- | ---: | ---: | ---: |
| 2019 Higher + Ordinary | 46 | 51 | 5 |
| 2020 Higher | 20 | 26 | 6 |
| 2021 Higher + Ordinary | 44 | 53 | 9 |
| 2022 Higher + Ordinary | 43 | 52 | 9 |
| **Total** | **153** | **182** | **29** |

The 2012–2018 maps covered both EV and IV variants but all 28 stopped after
Question 3. A second additive builder preserves all 385 original card IDs and
adds the two official production tasks to every map:

| Written Q4/Q5 repairs | Before | After | Recovered |
| --- | ---: | ---: | ---: |
| 2012 Higher + Ordinary, EV + IV | 68 | 76 | 8 |
| 2013 Higher + Ordinary, EV + IV | 20 | 28 | 8 |
| 2014 Higher + Ordinary, EV + IV | 48 | 56 | 8 |
| 2015 Higher + Ordinary, EV + IV | 53 | 61 | 8 |
| 2016 Higher + Ordinary, EV + IV | 69 | 77 | 8 |
| 2017 Higher + Ordinary, EV + IV | 62 | 70 | 8 |
| 2018 Higher + Ordinary, EV + IV | 65 | 73 | 8 |
| **Total** | **385** | **441** | **56** |

The same paper/scheme sweep found separately marked Kanji, grammar and culture
tasks hidden inside coarse legacy reading cards. Seventy-five overlapping,
topic-addressable cards now expose those assessed sections without removing or
renumbering their parent cards:

| Granular written task | New cards |
| --- | ---: |
| Kanji | 31 |
| Grammar | 31 |
| Culture and society | 13 |
| **Total** | **75** |

The 28 maps therefore retain 385 original cards and now contain 516 cards after
the 56 Q4/Q5 additions and 75 granular additions. This structurally covers the
reference's Higher-level Kanji and grammar heading families for 2013–2018 as
well as the audited Ordinary-level omissions.

All newly mapped written paper/scheme pairings were rendered side by side and
checked, including all 75 granular task crops, every 2012–2018 Q4/Q5
language/level variant and the unusual three-page 2018 Irish Higher Q4 scheme.
Every recovered 2024–2026 listening crop received the same visual check. All
246 older listening card/scheme pairings across the 34 available 2012–2022
variants were also rendered side by side and checked, including a second pass
over every additive display correction.
Explicit physical `printOrder` values preserve listening and repaired legacy
written-paper sequence without renumbering shipped cards; the viewer now uses
that order when it presents question chips. Section-end guards prevent the next
section's heading from bleeding into the previous crop. The cards are linked to
the canonical Japanese reading, translation, kanji, grammar, culture, writing
and listening nodes, and every changed sidecar is in the audited Storage
re-upload manifest. In total, this Japanese pass has exposed 451 cards that were
formerly missing or inaccessible (294 repairs plus 157 new written cards).

The fourteen-topic `Common Level` exam overlay is now active in Topic Atlas.
Its generated crosswalk reconciles every one of the 232 factual reference
headings while retaining the complete local corpus:

| Japanese parity gate | Result |
| --- | ---: |
| Factual reference heading associations | 232 |
| Matched heading associations | 230 |
| Source-blocked oral associations | 2 |
| Matched local card links | 436 |
| Preserved local paper variants | 93 |
| Hosted paper-only fallback maps | 93 |
| Explicit local card mappings | 1,329 |
| Deduplicated student-facing Topic Atlas cards | 968 |

All fourteen browse topics resolve to real canonical Japanese curriculum nodes,
and every retained local card has at least one browse-topic classification. The
mapping preserves intentional overlaps: a broad legacy reading card can remain
available under comprehension while its separately exposed sub-card appears
under translation, and a production task can appear in both `Personal Writing
(All)` and the relevant theme bucket. EV/IV copies are deduplicated in the
student-facing count without deleting either stored language variant.

The two unmatched headings are the 2021 oral materials. Their factual headings
remain visible in audit metadata, but the official SEC archive does not expose a
separate Japanese oral paper or marking scheme for that year. The StudyClix-hosted
files were inspected only to confirm the source boundary and were not copied into
the repository. `ORAL Exam` therefore remains visible with a truthful zero local
question count until an official or otherwise entitled source is available.

All 93 Japanese paper variants now also have generated hosted paper-only
anchors. Topic Atlas prefers these until the audited answer maps are uploaded,
which removes dead and stale question crops without publishing answer regions.
Where a legacy page-jump map can verify only the containing page, the card shows
that complete official page rather than pretending to have a tighter crop.
Inline Japanese marking-scheme reveals remain deliberately unavailable on this
fallback path; the full paper/scheme route remains available and the richer
reveal returns once the audited Storage upload is complete.

### Japanese work still open

- Obtain an official or otherwise entitled source for the two 2021 oral
  materials, then add and visually verify those cards without importing
  StudyClix-hosted content.
- Upload the audited Japanese repair set before relying on it outside
  local/tests.
- Map the generated exam-topic associations to the remaining stable Mark Bank
  identities.
- Surface the now-verified exam-topic ↔ official-syllabus crosswalk in
  Syllabus X-Ray.

## Physics & Chemistry audit — in progress, 4 September 2026

StudyClix exposes one flat `Common Level` browse menu containing 28 topics: 12
chemistry buckets and 16 physics buckets. Inspection of the signed-in question
cards resolved an important ambiguity in that label: the referenced questions
are from the Higher Level SEC paper. The generated bridge therefore applies
the exact reference associations only to matching Higher Level printed
questions (and their English/Irish editions). It does not incorrectly assign a
Higher question's topics to the different Ordinary question with the same
number.

The reference sweep captured only factual headings and State-exam markers:

| Physics & Chemistry parity gate | Result |
| --- | ---: |
| Reference topic buckets | 28 |
| Factual reference heading associations | 706 |
| Matched headings in the local SEC corpus | 626 |
| Source-blocked 2008–2009 headings | 80 |
| Distinct matched Higher printed questions | 159 |
| Commercial mock associations copied | 0 |

Six reference buckets currently have no headings: `C | Chlorides`, `C |
Hydrides`, `C | Organic Chemistry`, `P | Gravitation`, `P | Heat`, and `P |
Reflection and Mirrors`. They remain structural menu entries. They are not
forced to stay empty in NextStepUni when an entitled local SEC paper contains
relevant material—for example, the inspected 2026 papers legitimately populate
all six.

The migration freezes all 53 pre-existing paper variants and all 635 of their
card identities. It also restores 2015 Higher English Q12, which existed in the
Irish edition and answer map but was absent from the English topic-tag wave,
and adds the four already-entitled 2026 Higher/Ordinary English/Irish variants.
The resulting local bridge contains 57 variants and 684 explicit mappings,
which deduplicate to 384 student-facing printed questions from 2010–2026. All
384 remain available through the shared 28-topic menu; Ordinary and reference-
omitted questions use their verified canonical tags, while the 48 2026
language-specific mappings were classified directly from the local official
SEC papers.

Every browse bucket links many-to-many to real canonical Physics & Chemistry
curriculum nodes, so the flatter practice menu does not replace Syllabus
X-Ray's official hierarchy. Local browser QA verified the exact 28 labels, the
384-question headline, separate Higher/Ordinary filtering, the 2026 additions,
and rendered official question crops in the `P | Force, Mass, Momentum` feed.

### Physics & Chemistry work still open

- Acquire and independently verify the official SEC papers and marking schemes
  behind the 80 referenced 2008–2009 headings; do not import StudyClix-hosted
  images or PDFs.
- Complete the required paper-by-paper and marking-scheme boundary sweep,
  including finite answer-route analysis, before declaring question coverage
  complete.
- Audit and repair any legacy paper variants that still lack an inline verified
  answer map, particularly the 2024 editions and 2010 Ordinary English.
- Map part-aware associations to stable Mark Bank card identities when a
  combined Physics & Chemistry deck is available.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## Religious Education audit — in progress, 4 September 2026

The signed-in Higher and Ordinary pages use the same ten official syllabus
sections as their flat practice menu. The exact published labels are retained
per level (including the reference site's full-stop/colon difference for
Ordinary Sections F-J), while the canonical syllabus keeps all 92 finer-grained
content nodes underneath those sections.

| Religious Education parity gate | Result |
| --- | ---: |
| Reference topic buckets | 20 |
| Factual official heading associations | 366 |
| Matched headings in the local SEC corpus | 276 |
| Source-blocked headings | 90 |
| Excluded commercial mock associations | 304 |
| Preserved pre-migration variants | 23 |
| Preserved pre-migration cards | 69 |
| Local variants after the additive repair | 58 |
| Explicit local section-card mappings | 464 |
| Deduplicated student-facing section cards | 248 |
| Hosted paper-only anchor maps | 58 |

The old tag wave exposed only three cards on 23 Ordinary-level editions, even
though Paper Trail already holds both levels and the official papers print
eight examined sections per edition. A subject-specific SEC parser now detects
the lettered Section A-J headers directly in every local paper. It preserves
all 69 shipped card identities and adds 35 paper variants plus 395 section
cards. Each generated card has a matching hosted paper-only anchor, so the
topic feed no longer depends on incomplete legacy answer maps. Inline answer
reveal is intentionally withheld on this fallback path; the full official
paper and marking scheme remain available.

StudyClix sometimes lists the two or three compulsory Section-A questions
separately. NextStepUni's current official sidecars keep the complete printed
Section A as one card. All such factual headings remain independently recorded
as part-aware metadata and point to that complete section, so content is not
lost or represented as a fabricated crop.

The 90 source-blocked headings are from 2006–2009 and 2013, for which the local
corpus has no matching official paper. Conversely, the SEC-paper pass found 20
language-edition mappings absent from the reference pages: all eight 2021
Ordinary sections, 2014 Higher Section H, and 2015 Ordinary Section J. Those
valid local sections remain explicitly classified rather than being deleted to
make the headline counts agree.

### Religious Education work still open

- Complete in-browser crop QA for both levels and every section rotation.
- Complete the full paper/marking-scheme boundary and finite answer-route
  sweep before declaring coverage complete.
- Acquire and independently verify official SEC sources for the 90 headings
  from 2006–2009 and 2013; do not import StudyClix-hosted material.
- Replace the temporary paper-only preference after the complete verified
  section maps are uploaded, restoring inline marking-scheme reveals.
- Map the level-aware section identities to stable Mark Bank cards.
- Surface the exam-topic ↔ official-syllabus crosswalk in Syllabus X-Ray.

## History audit — in progress, 4 September 2026

The signed-in History pages use the twelve official Later Modern Ireland and
Europe topics independently at Higher and Ordinary level. That is a strong
student-facing browse structure, so Topic Atlas now preserves the exact 24
level-specific labels while Syllabus X-Ray keeps each complete official topic
and its three case-study nodes underneath it.

| History parity gate | Result |
| --- | ---: |
| Reference topic buckets | 24 |
| Factual official heading associations | 466 |
| Matched headings in the local SEC corpus | 405 |
| Source-blocked headings | 59 |
| Documented reference anomalies | 2 |
| Excluded commercial mock associations | 455 |
| Preserved pre-migration variants | 18 |
| Preserved pre-migration cards | 72 |
| Local variants after the additive repair | 68 |
| Explicit local card mappings | 1,028 |
| Deduplicated student-facing cards | 514 |
| Hosted paper-only anchor maps | 68 |

The earlier History tag wave exposed only the four documents-based subquestion
cards on 18 Higher-level variants. The official Later Modern paper contains
eleven further independently selectable Ireland/Europe topic blocks: all six
topics except the one selected for the documents-based question. A dedicated
SEC-paper parser now preserves all four original IDs and adds those eleven
blocks across every available 2010–2026 Higher/Ordinary English/Irish edition.

Ordinary papers in 2023–2026 also print a distinct `Alternative Part A` task.
All eight language-edition cards are retained even though the reference pages
list only the 2024 and 2026 headings. The 2024 reference association places its
Jarrow March task under Ireland Topic 2; the official paper identifies Europe
Topic 3 as that year's documents-based topic, so NextStepUni records the
commercial association as an anomaly and maps the card to the official topic.

The paper inspection found a second verified anomaly in the 2010 Ordinary
English booklet. Its final Ireland block is printed as Topic 5, but its title,
content and front-page instructions identify Topic 6; Topic 5 is already the
documents-based question and is excluded from Section 2. StudyClix repeats the
misclassification and additionally labels it Section 3. NextStepUni documents
that paper trail while correctly keeping the card under Ireland Topic 6. A
separate 2010 StudyClix `Section 4` heading for Europe Topic 5 is likewise
normalised to the official Section 3 identity.

The resulting 68 paper variants contain 1,028 physical cards, which deduplicate
English/Irish editions to 514 student-facing tasks. Sixty variants have fifteen
cards; the eight 2023–2026 Ordinary variants have sixteen. Every card has one
explicit level-specific browse classification, and every newly exposed topic
block has a generated paper-only anchor. Existing documents-based cards still
use their richer verified maps where available; a new topic block falls through
to its hosted official-paper crop while the full SEC marking scheme remains
available beside it.

### History work still open

- Complete the in-browser crop pass across both levels, both languages, all
  documents-based rotations, the 2010 correction and all Alternative Part A
  editions.
- Complete the full paper/marking-scheme boundary and finite answer-route sweep
  before declaring question coverage complete.
- Acquire and independently verify official sources for the 2008–2009 and
  2022–2023 deferred headings; do not import StudyClix-hosted material.
- Map the level-aware topic associations to stable Mark Bank card identities.
- Surface the verified exam-topic ↔ official-syllabus links explicitly in
  Syllabus X-Ray.

## Economics audit — in progress, 4 September 2026

StudyClix exposes a flat, level-specific Economics practice menu: 19 Higher
topics and 21 Ordinary topics. This is a strong exam-navigation layer, so Topic
Atlas now keeps those exact 40 labels and their level separation. The official
NCCA five-strand, 21-node Economics curriculum remains canonical underneath;
the generated many-to-many bridge does not replace or rename it.

| Economics parity gate | Result |
| --- | ---: |
| Reference topic buckets | 40 |
| Reported reference associations | 1,851 |
| Factual official State-exam associations | 1,120 |
| Matched associations in the local SEC corpus | 903 |
| Source-blocked associations | 217 |
| Distinct matched local questions | 517 |
| Matched question-topic links | 816 |
| Entitled local questions omitted by the reference | 32 |
| Excluded commercial mock associations | 731 |
| Preserved pre-migration variants | 26 |
| Preserved pre-migration cards | 304 |
| Local variants after the additive repair | 66 |
| Explicit physical card mappings | 1,098 |
| Deduplicated student-facing questions | 549 |
| Hosted paper-only anchor maps available | 54 |

The old-format 2010–2020 papers contain nine short Section-A questions and
eight independently selectable Section-B questions. The earlier tag wave
exposed only Section A on a partial set of editions. A dedicated SEC-paper
parser now preserves every original `1`–`9` identity and adds stable `B1`–`B8`
cards across every entitled Higher/Ordinary English/Irish booklet. The
2021–2026 format keeps its printed continuous `1`–`16` sequence. This yields 66
paper variants and 1,098 physical mappings, deduplicated to 549 questions in
Topic Atlas without deleting or renumbering any of the original 304 cards.

Every one of the 1,120 factual official headings is retained as level-,
sitting-, section- and part-aware audit metadata. Of these, 903 resolve to the
local official SEC corpus. The remaining 217 are explicitly source-blocked:
the 2006–2009 papers predate the entitled local corpus, the 2020 item is a
new-specification sample paper not held locally, and the 2022 items belong to a
separate deferred booklet not held locally. No StudyClix-hosted question image,
PDF, solution, note, video or mock material was copied.

The factual reference leaves 32 valid local top-level questions unassociated.
Those SEC questions remain visible and are classified through reviewed
canonical curriculum tags. This deliberately gives Ordinary `4.4 Monetary
Policy & the Price Level` four entitled local cards even though its reference
bucket reports zero; deleting those papers to preserve a commercial zero would
violate the preservation rule. Both `Research Project` buckets remain visible
as structural zero-question entries.

All old-format papers now have complete hosted paper-only anchors for Section B.
The two 2025 Higher editions, whose classic answer maps were absent, also have
complete 16-question maps. Their genuine extended-response questions can span
four page transitions, so the audited sidecars carry a paper-specific crop
limit rather than weakening the global three-page safety guard. Browser QA
verified the exact 40-topic hierarchy, the 549-question headline, the retained
2010 Ordinary B6 and 2017 Ordinary B4 crops, and the full five-page 2025 Higher
Q12 crop. Inline answers remain honestly withheld on paper-only fallbacks; the
official paper and marking scheme still open together.

### Economics work still open

- Acquire and independently verify official sources for the 2006–2009 papers,
  2020 sample paper and 2022 deferred paper; do not import StudyClix-hosted
  material.
- Complete the in-browser crop pass across both levels, both languages, all
  old-format Section-B rotations and every new-format extended response.
- Complete the full paper/marking-scheme boundary and finite answer-route sweep
  before declaring question coverage complete.
- Map the level-aware topic and part associations to stable Mark Bank card
  identities.
- Surface the verified exam-topic ↔ official-syllabus links explicitly in
  Syllabus X-Ray.

## Design & Communication Graphics audit — in progress, 4 September 2026

StudyClix exposes a flat, level-specific drawing-topic menu: 16 Higher topics
and 13 Ordinary topics. Topic Atlas now keeps those exact 29 published labels,
including the reference spellings `Laminiar` and `Auxillary`, while the official
three-strand, 26-node DCG curriculum remains canonical underneath through an
explicit many-to-many crosswalk.

| DCG parity gate | Result |
| --- | ---: |
| Reference topic buckets | 29 |
| Reported reference associations | 787 |
| Factual official State-exam associations | 427 |
| Matched associations in the local SEC corpus | 386 |
| Source-blocked associations | 41 |
| Distinct matched local drawing tasks | 347 |
| Matched question-topic links | 373 |
| Entitled local tasks omitted by the reference | 49 |
| Excluded commercial mock associations | 360 |
| Preserved pre-migration variants | 62 |
| Preserved pre-migration cards | 496 |
| Local variants after the additive repair | 132 |
| Explicit physical card mappings | 792 |
| Deduplicated student-facing drawing tasks | 396 |
| Hosted paper-only anchor maps | 132 |

DCG publishes Section A as a separate A3 sheet containing four independently
selectable quadrant questions. The previous tag wave exposed only the eight
Section-B/C cards (`B1`–`B3`, then `C1`–`C5`) and also stopped before the four
2026 Section-B/C editions. A subject-specific generator preserves all 496
existing card identities unchanged, adds all 66 English/Irish Section-A sheets
as stable `A1`–`A4` cards, and adds the four entitled 2026 Section-B/C variants.
The resulting 132 physical documents contain 792 card mappings, deduplicated
across language editions to 396 student-facing tasks from 2010–2026.

Every Section-A card has an audited horizontal-and-vertical quadrant crop of
the real official sheet. This is important for DCG: a vertical-only crop would
show two unrelated questions side by side. The 2026 B/C additions have finite
single-page crops, and all 132 documents now have a matching hosted paper map.
Browser QA verified the 29-topic menu and 396-question headline, a 2010
Ordinary conic A1 crop, a 2026 Ordinary conic A1 crop, and the newly exposed
2026 Higher assemblies C5 crop.

The reference leaves its Higher `Assemblies` and Ordinary `Conic Sections`
buckets empty despite valid official SEC tasks in the entitled corpus. Those
topics remain in the exact hierarchy and are populated locally: all 17 Higher
C5 assembly drawings and 16 Ordinary ellipse/parabola drawings stay visible.
The other 16 omitted tasks are likewise retained from direct official-paper or
frozen canonical-tag review. No valid local question was deleted to preserve a
commercial zero.

All 427 factual headings remain in part-aware metadata. The 41 unresolved
associations are explicitly source-blocked: 17 are from 2009, before the local
corpus begins, and 24 belong to separate 2022/2023 deferred papers not held
locally. No StudyClix question text, image, PDF, solution, note, video or mock
content was copied.

### Design & Communication Graphics work still open

- Acquire and independently verify official SEC sources for the 2009 and
  2022/2023 deferred headings; do not import StudyClix-hosted material.
- Complete the full paper-by-paper and marking-scheme boundary sweep for both
  levels and both official-language editions before declaring coverage
  complete.
- Map the level-aware topic and part associations to stable Mark Bank card
  identities.
- Surface the verified exam-topic ↔ official-syllabus links explicitly in
  Syllabus X-Ray.

## Computer Science audit — in progress, 4 September 2026

StudyClix exposes a flat, level-specific Computer Science menu: 21 Higher
topics and 24 Ordinary topics. Topic Atlas now preserves those exact 45 labels
and their level separation, including the distinct `HTML/CSS` and `HTML / CSS`
spellings. The official NCCA three-strand, 61-node curriculum remains canonical
underneath through an explicit many-to-many crosswalk.

| Computer Science parity gate | Result |
| --- | ---: |
| Reference topic buckets | 45 |
| Reported reference associations | 420 |
| Factual official State-exam associations | 302 |
| Matched associations in the local SEC corpus | 253 |
| Source-blocked associations | 49 |
| Distinct matched local questions | 203 |
| Matched question-topic links | 240 |
| Entitled local questions omitted by the reference | 5 |
| Excluded commercial mock associations | 118 |
| Preserved pre-migration variants | 23 |
| Preserved pre-migration cards | 317 |
| Local variants after the additive repair | 52 |
| Explicit physical card mappings | 416 |
| Deduplicated student-facing questions | 208 |
| Hosted paper-only anchor maps | 52 |

The entitled corpus contains separate Section-A/B and Section-C booklets in
English and Irish. The previous topic file covered only 23 of those physical
documents and frequently omitted the standalone Question 16 card. A
subject-specific generator now preserves all 317 existing cards unchanged and
adds every missing booklet through 2026. It emits `1`–`15` for each A/B booklet
and `16` for each C booklet, yielding 52 physical variants and 416 mappings,
deduplicated to 208 student-facing questions from 2020–2026.

Every one of the 302 factual official headings remains available as level-,
sitting-, section- and part-aware metadata. All 253 main-paper associations
resolve to the entitled SEC corpus. The other 49 associations belong to the
official 2020 sample papers, which are not currently held locally; they remain
explicitly source-blocked pending acquisition and independent verification
from an official source. No StudyClix question text, image, PDF, solution,
note, video or mock content was copied.

The factual reference leaves five real local questions unassociated: Higher
2020 Q9, Higher 2021 Q2, Higher 2023 Q1 and Q9, and Ordinary 2025 Q12. They are
retained under their reviewed same-level curriculum-backed topics. Five menu
buckets also have no State headings in the snapshot—Higher `Data Analysis`,
and Ordinary `Databases`, `Decomposition`, `HTML / CSS`, and `Number Systems`.
The hierarchy stays exact while the independently verified local Data Analysis
question remains visible rather than being deleted to reproduce a commercial
zero.

All 52 booklets now carry finite paper-side maps. Section C is one long
programming question and can legitimately span up to eight page transitions;
the sidecars use audited per-paper limits and stop before rough-work pages.
The Topic Vault now additively overlays these paper endpoints onto the richer
verified answer map, retaining both the complete paper question and the inline
SEC marking-scheme reveal. Browser QA verified the exact 45-topic menu, the
208-question headline, the retained 2020 Higher Data Analysis Q9 crop, and all
seven pages of the 2026 Higher Q16 crop plus its eight-page scheme reveal.

### Computer Science work still open

- Acquire and independently verify the official 2020 sample papers; do not
  import StudyClix-hosted material.
- Complete the full paper-by-paper and marking-scheme boundary sweep for both
  levels and both official-language editions before declaring coverage
  complete.
- Map the level-aware topic and part associations to stable Mark Bank card
  identities.
- Surface the verified exam-topic ↔ official-syllabus links explicitly in
  Syllabus X-Ray.

## Biology audit — in progress, 4 September 2026

StudyClix exposes four overlapping Biology variants: Higher New Course (33
topics), Higher Old Course (31), Ordinary New Course (33), and Ordinary Old
Course (25). Topic Atlas now preserves all 122 exact labels and the published
New Course strand hierarchy while keeping each Old Course menu flat. The
official outgoing and redeveloped Biology specifications remain canonical
underneath through a complete 122-topic crosswalk; the commercial hierarchy is
a practice navigation layer, not a replacement syllabus.

| Biology parity gate | Result |
| --- | ---: |
| Reference topic buckets | 122 |
| Reported reference associations | 4,891 |
| Factual official State-exam associations | 2,419 |
| Matched associations in the local SEC corpus | 1,561 |
| Source-blocked associations | 858 |
| Distinct matched local questions | 485 |
| Entitled local questions retained beyond the reference | 49 |
| Excluded commercial mock associations | 2,333 |
| Excluded provider-owned sample associations | 139 |
| Preserved pre-migration variants | 89 |
| Preserved pre-migration cards | 971 |
| Verified corrected card identities | 48 |
| Local variants after the additive repair | 100 |
| Explicit physical card mappings | 1,068 |
| Deduplicated student-facing questions | 534 |
| Hosted paper-only anchor maps | 100 |

The entitled corpus contains the full Higher/Ordinary × English/Irish Biology
set from 2010–2026, split into Section A/B and Section C booklets from 2019
onwards. A subject-specific generator preserves every one of the 971 frozen
baseline tasks, adds all eight 2026 booklets, both missing 2022 Ordinary
Section-C editions, and the missing 2017 Ordinary Irish edition. This yields
100 physical documents and 1,068 mappings, deduplicated across official
languages to 534 student-facing questions.

Direct inspection of the official SEC papers uncovered a genuine inherited
identity error: the eight 2019/2020 Section-C editions had been tagged as
Questions 11–16, but the printed sequence is Questions 10–15. The generator
applies a one-to-one correction to those 48 card identities and proves every
frozen task still resolves to its corrected counterpart. This is a verified
renumbering, not a deletion. All other paper runs are asserted explicitly:
2010–2018 use Questions 1–15; 2019–2020 A/B use 1–9 and C uses 10–15; and
2021–2026 A/B use 1–10 and C uses 11–17.

All 2,419 factual official headings remain available byte-for-byte as
level-, sitting-, section- and part-aware metadata. The 858 unresolved
associations are explicitly source-blocked: 494 belong to 2004–2009 papers
outside the entitled local corpus, 231 belong to separate deferred sittings,
and 133 belong to official redeveloped-course sample papers not held locally.
The separate 139 StudyClix Sample Exam entries are retained as counts only.
No StudyClix question text, image, PDF, solution, note, video, mock, or
provider-owned sample content was copied.

The reference snapshot leaves 49 valid local questions without a matching
heading. Thirty-four are the directly reviewed 2026 Higher and Ordinary
questions; the other fifteen are earlier entitled SEC cards. They remain
visible through reviewed new-/old-course topic associations or the frozen
canonical curriculum fallback. Provider omissions therefore cannot erase a
real local question.

All 100 paper documents now have finite paper-side maps. Browser QA verified
the ten displayed course/strand groups and the `534 questions · 122 topics ·
2010–2026` headline; a reviewed 2026 Higher Q16 with three paper pages and five
scheme pages; 2026 Ordinary U2 questions and their scheme; both corrected 2019
and 2020 Higher Section-C Q10/Q15 boundaries; and the Irish 2019 Q15 paper and
scheme. No browser console errors were present. The runtime payload is stored
losslessly in compact generated form: the exact hierarchy, paths, counts,
headings and mappings are reconstructed and regression-tested while keeping
the Paper Trail production chunk below 2 MiB.

### Biology work still open

- Acquire and independently verify official sources for the 2004–2009,
  deferred and redeveloped-course sample-paper headings; do not import
  StudyClix-hosted material.
- Complete the full 100-document paper/marking-scheme boundary sweep across
  both levels and both official languages. Fifteen legacy or structurally
  problematic editions still rely on the honest full-scheme route rather than
  a verified inline answer sidecar.
- Map the level- and course-aware topic/part associations to stable Mark Bank
  card identities.
- Surface the verified exam-topic ↔ outgoing/redeveloped-syllabus links
  explicitly in Syllabus X-Ray.

## Chemistry audit — in progress, 4 September 2026

StudyClix exposes four overlapping Chemistry variants: Higher New Course (16
topics), Higher Old Course (23), Ordinary New Course (18), and Ordinary Old
Course (19). Topic Atlas now preserves all 76 exact labels and the 11 published
course/strand groups. The official outgoing 2026 specification and redeveloped
2027 specification remain canonical underneath through a complete 76-topic
crosswalk; the commercial hierarchy is a practice-navigation layer rather than
a replacement syllabus.

| Chemistry parity gate | Result |
| --- | ---: |
| Reference topic buckets | 76 |
| Reported reference associations | 4,026 |
| Factual official State-exam associations | 2,265 |
| Matched associations in the local SEC corpus | 1,406 |
| Source-blocked associations | 859 |
| Distinct matched local questions | 342 |
| Entitled local questions retained beyond the reference | 32 |
| Excluded commercial mock associations | 1,612 |
| Excluded provider-owned sample associations | 149 |
| Preserved pre-migration variants | 64 |
| Preserved pre-migration cards | 704 |
| Local variants after the additive repair | 68 |
| Explicit physical card mappings | 748 |
| Deduplicated student-facing questions | 374 |
| Hosted paper-only anchor maps | 68 |
| Verified marking-scheme maps | 67 |
| Hosted reviewed answer-map overrides | 7 |

The entitled corpus contains every Higher/Ordinary × English/Irish Chemistry
paper from 2010–2026. A subject-specific generator preserves all 704 frozen
baseline cards byte-for-byte, adds the four official 2026 editions, and emits
or verifies a finite Q1–Q11 paper map for all 68 documents. The result is 748
physical mappings, deduplicated across official languages to 374
student-facing questions.

All 2,265 factual official headings remain available byte-for-byte as level-,
sitting-, question- and part-aware metadata. Of those, 1,406 associations match
the entitled local SEC corpus. The other 859 remain explicitly source-blocked:
563 belong to 2001–2009 main papers outside the local corpus, 164 to separate
deferred sittings, and 132 to official sample materials not held locally. The
1,612 commercial mock associations and 149 StudyClix Sample Exam associations
are retained as counts only. No StudyClix question text, image, PDF, solution,
note, video, mock, or provider-owned sample content was copied.

The factual reference snapshot omits 32 valid local questions. Twenty-two are
the directly reviewed 2026 Higher and Ordinary questions; ten are earlier
Ordinary questions from 2010, 2011, 2012, 2022 and 2023. They remain visible
under directly reviewed same-level old- and equivalent new-course topics, so a
provider omission cannot delete an entitled SEC card.

Sixty-five inherited marking-scheme maps were already complete. Direct PDF
review recovered two more: 2012 Ordinary English Q4 starts at the scheme's
`SECTION B` heading, and the official 2014 Higher English scheme misspells its
Q2 and Q4 headings as `QUSESTION`. Both recovered maps exclude trailing blank
pages and reconcile all Q1–Q11 paper and answer boundaries. The only remaining
paper-only edition is 2020 Ordinary Irish, whose corresponding scheme is absent
from both the index and the entitled local corpus.

Browser QA verified the exact 11-group/76-topic hierarchy and the `374
questions · 76 topics · 2010–2026` headline; the two-page 2026 Higher Q1 crop;
the 2024 Higher Q1 paper and scheme crops; the directly retained 2023 Ordinary
Q4; and the 2026 Ordinary `U2. Investigating in chemistry` Q1–Q3 set. No browser
console errors were present. Static topic and corpus data now build into
separate 750 KB and 484 KB lazy chunks, leaving the interactive Paper Trail
viewer at 919 KB instead of pushing it past 2 MiB.

### Chemistry work still open

- Acquire and independently verify the official sources behind the 2001–2009,
  deferred-sitting and official-sample headings; do not import StudyClix-hosted
  material.
- Acquire the missing 2020 Ordinary Irish marking scheme from an authorised
  official source, if one exists, and independently verify its Q1–Q11 bounds.
- Include the two recovered sidecars in the eventual Paper Trail Storage upload;
  until that release, the currently published app will continue to use its
  honest paper-only fallback for those two cards.
- Complete the full 68-document paper/marking-scheme boundary sweep across both
  levels and both official languages before declaring coverage complete.
- Map the level- and course-aware topic/part associations to stable Mark Bank
  card identities.
- Surface the verified exam-topic ↔ outgoing/redeveloped-syllabus links
  explicitly in Syllabus X-Ray.

## Physics audit — in progress, 4 September 2026

StudyClix exposes four overlapping Physics variants: Higher New Course (25
topics), Higher Old Course (34), Ordinary New Course (28), and Ordinary Old
Course (26). Topic Atlas now preserves all 113 exact labels and all nine
published New Course strand groups while keeping the two Old Course menus
flat. The official outgoing syllabus and redeveloped 2027 specification remain
canonical underneath through a complete 113-topic crosswalk; the reference
hierarchy is a practice-navigation layer, not a replacement curriculum.

| Physics parity gate | Result |
| --- | ---: |
| Reference topic buckets | 113 |
| Reported reference associations | 4,701 |
| Factual official State-exam associations | 2,482 |
| Matched associations in the local SEC corpus | 1,703 |
| Source-blocked associations | 779 |
| Distinct matched local questions | 391 |
| Entitled local questions retained beyond the reference | 41 |
| Excluded commercial mock associations | 2,051 |
| Excluded provider-owned sample associations | 168 |
| Preserved pre-migration variants | 63 |
| Preserved pre-migration cards | 790 |
| Local variants after the additive repair | 68 |
| Explicit physical card mappings | 864 |
| Deduplicated student-facing questions | 432 |
| Hosted paper-only anchor maps | 68 |
| Verified marking-scheme maps | 67 |

The entitled corpus now contains every Higher/Ordinary × English/Irish Physics
paper from 2010–2026. A subject-specific generator preserves all 790 frozen
baseline cards, restores the omitted 2011 and 2012 Higher Q12 in both official
languages, adds the missing 2025 Ordinary English edition, and adds all four
2026 editions. Every document has a finite Q1–Q12 or Q1–Q14 paper map. The
result is 864 physical mappings, deduplicated across official languages to 432
student-facing questions.

All 2,482 factual official headings remain available byte-for-byte as level-,
course-, sitting-, question- and part-aware metadata. Of those, 1,703
associations match the entitled local SEC corpus. The remaining 779 are
explicitly source-blocked because they point to pre-2010, deferred, or official
sample material not held locally. The 2,051 mock and 168 provider-sample
associations are retained as counts only. No StudyClix question text, image,
PDF, solution, note, video, mock, or provider-owned sample content was copied.

The factual reference snapshot omits 41 valid local questions. Twenty-eight
are the directly reviewed 2026 Higher and Ordinary questions; thirteen are
older entitled questions from 2010, 2011, 2012, 2014 and 2016. They remain
visible under directly reviewed same-level topics, so a provider omission
cannot erase an SEC question.

Seven inherited answer maps were absent. Direct PDF review recovered 2012
Higher English and both official-language editions for 2024 Higher, 2025
Higher, and 2025 Ordinary. Their starts and terminal pages were visually
checked against the printed question headings. The sole paper-only edition is
2020 Ordinary Irish, because no corresponding marking scheme exists in the
index or entitled local corpus.

The live Storage sidecar for the newly exposed 2025 Ordinary English paper is
absent (HTTP 404), and several of the other six recovered maps supersede stale
Storage copies. The seven reviewed maps now also ship as small Hosting assets,
with an explicit per-file override rather than a subject-wide fallback. This
restores both the inline Topic Atlas reveal and the full-paper Answers overlay
without changing any paper, scheme or card identity. Browser QA verified the
113-topic/432-question Physics index, all 11 level/course group headings, 2026
Higher Q1, the restored 2012 Higher Q12, the 2025 Ordinary English paper crop,
its inline Q4 scheme on pages 9–10, and all 14 full-paper answer controls. No
application errors remained; the only browser messages were pdf.js dependent-
image readiness warnings while pages were rendering.

Mark Bank keeps its 1,133 shipped Physics cards and their canonical curriculum
IDs unchanged. A new cross-surface gate proves every one of those cards resolves
to the same-level exact practice map for its paper question. The independent
paper census remains deliberately visible rather than being mistaken for
completion: 1,119 of 1,224 printed task leaves are covered, 46 have documented
scheme-evidence exclusions, and 59 remain open; six citations are currently
orphaned by the census grammar and four census flags still need resolution.
Paper Trail uses stable top-level printed-question identities, while the Mark
Bank remains the task/part-level surface where finite response routes belong.

### Physics work still open

- Resolve the 59 open Mark Bank task leaves, six census-orphaned citations and
  four paper-census flags without deleting or renaming any shipped card.
- Acquire and independently verify the pre-2010, deferred and official-sample
  sources behind the 779 blocked headings; do not import StudyClix-hosted
  material.
- Acquire the missing 2020 Ordinary Irish marking scheme from an authorised
  official source, if one exists, and independently verify its Q1–Q12 bounds.
- Complete the full 68-document paper/marking-scheme boundary sweep across both
  levels and both official languages before declaring coverage complete.
- Surface the verified exam-topic ↔ outgoing/redeveloped-syllabus links
  explicitly in Syllabus X-Ray.

## Business audit — in progress, 4 September 2026

StudyClix exposes four overlapping Business variants: Higher New Course (20
topics), Higher Old Course (32), Ordinary New Course (26), and Ordinary Old
Course (27). Topic Atlas now preserves all 105 exact labels and all ten
published New Course strand groups, with explicit flat groups for both Old
Course menus. The official outgoing syllabus and redeveloped 2027
specification remain canonical underneath through a complete topic
crosswalk; the reference hierarchy is a practice-navigation layer, not a
replacement curriculum.

| Business parity gate | Result |
| --- | ---: |
| Reference topic buckets | 105 |
| Reported reference associations | 5,708 |
| Factual official State-exam associations | 3,075 |
| Matched associations in the local SEC corpus | 2,008 |
| Source-blocked associations | 1,067 |
| Distinct matched local questions | 663 |
| Entitled local questions retained beyond the reference | 58 |
| Excluded commercial mock associations | 2,437 |
| Excluded provider-owned sample associations | 196 |
| Preserved pre-migration variants | 50 |
| Preserved pre-migration cards | 523 |
| Local variants after the additive repair | 96 |
| Explicit physical card mappings | 1,442 |
| Deduplicated student-facing questions | 721 |
| Hosted paper-only anchor maps | 96 |
| Verified marking-scheme maps | 82 |
| Honest paper-only fallbacks | 14 |

The entitled corpus now contains every Higher/Ordinary × English/Irish
Business paper from 2010–2026. A subject-specific generator preserves all 523
frozen baseline cards and adds the previously absent sections and editions
without changing any old identity. Older papers use stable additive `ABQ`,
`S3Q1`–`S3Q7`, and `S2Q1`–`S2Q8` identities alongside the original short
questions. Every physical card has a finite one- or two-page paper region.
The result is 1,442 physical mappings, deduplicated across official languages
to 721 student-facing questions.

All 3,075 factual official headings remain available byte-for-byte as level-,
course-, sitting-, question- and part-aware metadata. Of those, 2,008
associations match the entitled local SEC corpus. The remaining 1,067 are
explicitly source-blocked because they point to pre-2010, deferred, or
official sample material not held locally. The 2,437 mock and 196
provider-sample associations are retained as counts only. No StudyClix
question text, image, PDF, solution, note, video, mock, or provider-owned
sample content was copied.

The factual reference snapshot omits 58 valid local questions: all 45 directly
reviewed 2026 questions and thirteen older entitled questions. They remain
visible under directly reviewed same-level topics, so a provider omission
cannot erase an SEC question. Four Ordinary New Course buckets — 1.6, 2.8 and
3.5 `Applying my learning`, plus `U3. Project planning` — have no official
question association in the captured reference and remain honestly empty.

The curriculum registry now models the official 2027 specification directly:
the six-element Unifying Strand plus Strands 1–4, 28 assessable topic nodes,
180 class hours, and the published 40% Business Alive Investigative Study / 60%
written-examination weighting. Legacy aliases keep all shipped Mark Bank cards
resolvable against that canonical structure while the current Mark Bank is
correctly labelled as the `outgoing 1999 syllabus`; it is not presented as the
redeveloped course.

Browser QA verified the 105-topic/721-question Business index, the exact New
and Old Course groupings, a 2026 Higher ABQ, a 2011 combined ABQ spanning two
pages, and 2019 Higher Section 3 Question 3 under `7.3 Global Business`.
Syllabus X-Ray displayed the exact official five-group/28-topic 2027
specification, source link, hours and assessment weighting. The Mark Bank
retained its existing cards and displayed the corrected outgoing-syllabus
label.

### Business work still open

- Acquire and independently verify the pre-2010, deferred and official-sample
  sources behind the 1,067 blocked headings; do not import StudyClix-hosted
  material.
- Complete the full 96-document paper/marking-scheme boundary sweep across both
  levels and both official languages before declaring coverage complete.
- Map the level-, course- and part-aware associations to stable Mark Bank card
  identities without deleting or renaming any shipped card.
- Surface the verified exam-topic ↔ outgoing/redeveloped-syllabus links
  explicitly in Syllabus X-Ray.

## Art audit — in progress, 4 September 2026

StudyClix exposes 18 Higher topics under three section groups and 14 Ordinary
topics, where `Section A: Today's World` is a flat topic and Sections B/C are
grouped. Topic Atlas now preserves all 32 exact labels, the five explicit
reference groups, and a sixth runtime group for that flat Ordinary section.
The official NCCA Visual Art curriculum remains canonical underneath through
a complete topic crosswalk; the commercial hierarchy is used only as the
exam-practice navigation layer.

| Art parity gate | Result |
| --- | ---: |
| Reference topic buckets | 32 |
| Explicit reference groups | 5 |
| Runtime display groups | 6 |
| Reported reference associations | 1,299 |
| Factual official State-exam associations | 690 |
| Matched associations in the local SEC corpus | 592 |
| Source-blocked associations | 98 |
| Distinct matched local questions | 541 |
| Matched question-topic links | 584 |
| Entitled local questions retained beyond the reference | 536 |
| Excluded commercial mock associations | 609 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 136 |
| Preserved pre-migration physical cards | 1,850 |
| Local variants after the additive repair | 152 |
| Explicit physical card mappings | 2,154 |
| Deduplicated student-facing questions | 1,077 |
| Newly added written-paper variants | 16 |
| Newly added physical mappings | 304 |
| Verified marking-scheme maps | 65 |
| Honest paper-only maps | 87 |

All 690 factual official headings remain available byte-for-byte as level-,
sitting-, question-, part-, language- and file-aware metadata: 378 Higher and
312 Ordinary. Of those, 592 associations match the entitled local SEC corpus.
The 98 remaining associations are explicitly source-blocked: 50 pre-2010 main
paper associations, 30 deferred-paper associations, and 18 official-sample
associations. The 609 mock associations are retained as counts only. No
StudyClix question text, image, PDF, solution, note, video, mock, or
provider-owned sample content was copied.

Art requires a file-aware join because the written paper and several practical
booklets reuse the same year, level and question numbers. The runtime therefore
includes the exact SEC file identity and keeps those cards separate. All 136
pre-migration variants and their 1,850 physical cards survive unchanged. The
repair adds the complete Higher/Ordinary × English/Irish written-paper set for
2023–2026, producing 152 variants, 2,154 physical mappings and 1,077
student-facing questions. Every card resolves to one or more same-level
practice topics. The 536 valid local questions that the reference does not
list remain visible: 144 written questions and 392 practical-booklet questions.

Two provider omissions were checked explicitly rather than silently dropped.
The reference omits the complete 2023 Ordinary written paper, so its Q1–Q7
cards remain under the broad Section A bucket and Q8–Q19 retain their reviewed
period mappings. It also omits 2023 Higher Q10, which remains under Baroque from
the entitled paper and existing reviewed mapping.

The finite paper/scheme sweep covers all 2,154 physical cards. It exposed a
blank-page gap between Sections B and C in the 2023–2026 written papers; the
Art map builder now writes an explicit end page and end coordinate at that
boundary, preventing Q13 from swallowing the intervening answer pages. The 16
repaired rich maps also ship as narrow per-file Hosting overrides while their
Storage sidecars are absent or stale. Browser QA verified the 32-topic/
1,077-question index, the exact six displayed section groups, 2023 Ordinary Q8
with its six-page scheme reveal, the repaired 2026 Higher Q13 paper crop and
six-page scheme reveal, and three distinct 2017 Higher Q1 practical-booklet
cards under `Artists: Processes and Media`. No browser-console errors remained.

Mark Bank keeps all 462 authored Art cards unchanged: 222 Higher and 240
Ordinary. Syllabus X-Ray continues to present the official Art curriculum and
assessment model rather than relabelling the provider's practice menu as a
curriculum.

### Art work still open

- Acquire and independently verify the pre-2010, deferred and official-sample
  sources behind the 98 blocked headings; do not import StudyClix-hosted
  material.
- Recover verified marking-scheme regions for the 87 paper-only maps where an
  entitled official scheme exists.
- Map the file- and part-aware associations to stable Mark Bank task identities
  without deleting or renaming any of the 462 shipped cards.
- Complete the manual visual sweep of all 152 paper/marking-scheme variants;
  the finite automated boundary sweep is complete but is not a substitute for
  full visual inspection.
- Surface the verified exam-topic ↔ official-curriculum links explicitly in
  Syllabus X-Ray.

## Construction Studies audit — in progress, 4 September 2026

StudyClix exposes four overlapping Construction Studies variants: Higher and
Ordinary outgoing-course menus, each flat, plus Higher and Ordinary New Course
menus, each grouped under the four Construction Technology strands. Topic
Atlas now preserves all 103 exact labels and all eight explicit New Course
groups, with one additional display group for each flat outgoing menu. The
official outgoing Construction Studies syllabus and the incoming Construction
Technology specification remain canonical underneath; the reference hierarchy
is the exam-practice navigation layer rather than a replacement curriculum.

| Construction Studies parity gate | Result |
| --- | ---: |
| Reference topic buckets | 103 |
| Explicit reference groups | 8 |
| Runtime display groups | 10 |
| Reported reference associations | 2,336 |
| Factual official State-exam associations | 1,396 |
| Matched associations in the local SEC corpus | 1,031 |
| Source-blocked associations | 365 |
| Distinct matched local questions | 302 |
| Matched question-topic links | 1,019 |
| Entitled local questions retained beyond the reference | 21 |
| Excluded commercial mock associations | 940 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 63 |
| Preserved pre-migration physical cards | 598 |
| Local variants after the additive repair | 68 |
| Explicit physical card mappings | 646 |
| Deduplicated student-facing questions | 323 |
| Newly added paper variants | 5 |
| Newly added physical mappings | 48 |
| Verified marking-scheme maps | 64 |
| Honest paper-only maps | 4 |

The entitled corpus now contains every Higher/Ordinary × English/Irish written
paper from 2010–2026. A subject-specific generator preserves all 63 frozen
variants and all 598 of their cards, adds the omitted 2014 Higher English
edition, and adds all four 2026 editions. Higher papers retain Q1–Q10 and
Ordinary papers Q1–Q9 throughout. The additive result is 68 physical editions,
646 physical card mappings and 323 student-facing questions; no previous paper,
question number or card identity is replaced.

All 1,396 factual official headings remain available byte-for-byte as level-,
course-, sitting-, question- and part-aware metadata: 877 Higher and 519
Ordinary. Of those, 1,031 associations match the entitled local corpus. The 365
remaining associations are explicitly source-blocked: 225 pre-2010 main-paper
associations, 49 deferred-paper associations and 91 official-sample-paper
associations. The 940 mock associations are retained as counts only. No
StudyClix question text, image, PDF, solution, note, video or mock content was
copied.

The factual reference snapshot omits 21 valid local questions. Direct review of
the entitled SEC papers confirmed two complete Higher questions and nineteen
Ordinary questions. Most of the latter are Q8 nine-term sets which deliberately
span several construction areas; each is retained under every evidenced
same-level reference bucket instead of being forced into the old `General`
catch-all. The remaining questions cover lifetime/universal design, external
wall performance, kitchen and furniture design, stairs, and rainwater systems.
This reviewed exception map prevents reference omissions from erasing valid SEC
cards.

The curriculum crosswalk covers every bucket. Outgoing topics bridge only to
the 65 canonical nodes in the official ten-section Construction Studies
syllabus. New Course topics bridge only to the 31 canonical nodes in the 2028
Construction Technology specification. StudyClix separates `Substructure` and
`Superstructure`, while the official specification publishes one combined
`Substructure and superstructure` node; both practice buckets therefore map to
that single canonical node without altering either hierarchy. Syllabus X-Ray
continues to show the cohort-safe 2027 outgoing map and its transition notice,
while the separate 2028 record retains the four official strands, 180 class
hours, and the 30% project / 20% craft assessment / 50% written assessment.

The finite paper/scheme sweep covers all 646 physical cards. Sixty-four editions
have verified scheme regions. Four remain honest paper-only maps: 2014 Ordinary
English and Irish, and 2020 Higher Irish and Ordinary Irish. Browser QA verified
the 103-topic/323-question index, all ten exact course/strand headings, the 2026
Higher Q1 paper crop plus three scheme pages, and the retained 2025 Ordinary Q8
under `Drainage` plus four scheme pages. Mark Bank kept all 505 authored cards
(255 Higher and 250 Ordinary) and now labels them explicitly as the outgoing
Construction Studies syllabus. Syllabus X-Ray displayed the official 2027
ten-section map and transition warning. No application errors remained; the
only browser messages were transient pdf.js dependent-image readiness warnings
while pages rendered.

### Construction Studies work still open

- Acquire and independently verify the pre-2010, deferred and official-sample
  sources behind the 365 blocked headings; do not import StudyClix-hosted
  material.
- Recover authorised marking-scheme regions for the four honest paper-only
  editions where an official scheme exists.
- Complete the manual visual sweep of all 68 paper/marking-scheme editions; the
  finite automated boundary sweep is complete but is not a substitute for full
  visual inspection.
- Map the part-aware factual associations to stable Mark Bank task identities
  without deleting or renaming any of the 505 shipped cards.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray
  while preserving the 2027/2028 cohort boundary.

## Technology audit — in progress, 4 September 2026

StudyClix exposes Technology as two flat practice menus: 21 Higher Level topics
and 16 Ordinary Level topics. Topic Atlas now carries those 37 exact labels as
two level-aware display groups while the official NCCA Technology syllabus
remains canonical in Syllabus X-Ray. This separation is important for the five
optional areas: the practice menu is useful navigation, but it is not the
curriculum authority.

| Technology parity gate | Result |
| --- | ---: |
| Reference topic buckets | 37 |
| Runtime display groups | 2 |
| Reported reference associations | 2,127 |
| Factual official State-exam associations | 1,190 |
| Matched associations in the local SEC corpus | 1,118 |
| Source-blocked associations | 72 |
| Distinct matched local questions | 580 |
| Matched question-topic links | 918 |
| Entitled local questions retained beyond the reference | 98 |
| Excluded commercial mock associations | 937 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 56 |
| Preserved pre-migration physical cards | 756 |
| Local variants after the additive repair | 132 |
| Explicit physical card mappings | 1,356 |
| Deduplicated student-facing questions | 678 |
| Newly added paper variants | 76 |
| Newly added physical mappings | 600 |
| Verified marking-scheme maps | 61 |
| Honest paper-only maps | 71 |

The previous local dataset exposed only Section A. The entitled SEC corpus also
contains the separately supplied Section B/C booklet for every available
Higher and Ordinary sitting from 2010–2026 (with no Ordinary sitting in 2020).
The additive repair keeps every one of the 56 frozen variants and all 756 of
their cards, adds ten missing Section A editions, and adds all 66 Section B/C
editions. Section A retains Q1–Q15 at Higher and Q1–Q12 at Ordinary; each B/C
booklet adds B2, B3 and C1–C5. Prefixing the long-question identities prevents
them from colliding with the numbered Section A cards.

The captured reference reports 2,127 items: 1,190 factual official-exam
associations and 937 commercial mock associations. All factual headings remain
available as metadata, including the source's literal 2016 Ordinary
`Question 100` heading; direct comparison with the SEC booklet safely targets
that association to Q10 without rewriting the captured heading. The 72 blocked
associations are all from 2009, before the entitled local corpus begins. No
StudyClix question text, solution, note, video, image, PDF or mock content was
copied.

Four local Section A questions have neither a factual reference association nor
a pre-existing usable tag. Direct SEC-paper review retains 2026 Higher Q8 and
Q15 under `Communications & Graphics Media`, 2022 Higher Q3 under `Technology
in Society`, and 2022 Higher Q4 under `Energy`. The other 94 retained logical
cards use either their pre-existing verified canonical tags or the option name
printed on the official Section C paper. This also keeps official C3–C5 work
reachable where the reference publishes an empty option bucket. Six reference
topics report zero total items; the Higher `Sample Project Folder` separately
contains three mock-only items and no official headings.

All 132 editions have finite paper regions. Sixty-one retain verified marking-
scheme crops. Seventy-one are explicitly paper-only: all 66 newly surfaced B/C
booklets, four previously hosted Section A maps, and the same-layout 2022 Higher
English Section A repair. Paper-only cards deliberately fall back to opening
beside the full marking scheme rather than presenting a fabricated answer crop.
Representative visual inspection confirmed the two-page Higher C4 boundary and
the single-page Higher/Ordinary terminal option boundaries. Technology has no
authored Mark Bank deck at present, so none was invented during the taxonomy
migration. Local browser QA confirmed one unambiguous `678 questions · 37
topics · 2010–2026` Technology shelf, the exact Higher/Ordinary headings, an
existing 2025 Higher Section A landing, a newly surfaced 2025 Higher B2
landing, the 2025 Higher C4 page-seven landing and its honest paper-only scheme
message. It also confirmed Syllabus X-Ray's successor, War Room Subject
Coverage, still shows the official 12 syllabus areas, the two-of-five option
rule and the published 50% project / 50% written assessment. The QA sweep found
and fixed a separate cycle-alias bug which had also admitted the same-named LCA
Technology archive into a regular Leaving Certificate student's `My subjects`
list. No localhost browser errors remained.

### Technology work still open

- Acquire and independently verify the 2009 sources behind the 72 blocked
  headings; do not import StudyClix-hosted material.
- Recover authorised marking-scheme regions for the 71 honest paper-only maps
  where an official scheme exists.
- Complete the manual visual sweep of all 132 paper/marking-scheme variants;
  the finite automated boundary sweep is complete but is not a substitute for
  full visual inspection.
- Build a Technology Mark Bank deck only from authorised official material;
  taxonomy parity does not author or infer marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Engineering audit — in progress, 4 September 2026

StudyClix exposes four overlapping Engineering variants: Higher and Ordinary
for the outgoing course, plus Higher and Ordinary for the course introduced to
fifth-year students in September 2026. Topic Atlas now carries all 74 exact
practice labels in ten level- and course-aware display groups: the two flat
outgoing menus and the four new-course strands at each level. Syllabus X-Ray
keeps the official outgoing Materials and Technology syllabus separate from
the incoming NCCA Engineering specification.

| Engineering parity gate | Result |
| --- | ---: |
| Reference topic buckets | 74 |
| Explicit reference groups | 8 |
| Runtime display groups | 10 |
| Reported reference associations | 4,681 |
| Factual official State-exam associations | 2,921 |
| Matched associations in the local SEC corpus | 2,287 |
| Source-blocked associations | 634 |
| Distinct matched local questions | 254 |
| Matched question-topic links | 1,568 |
| Excluded commercial mock associations | 1,760 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 62 |
| Preserved pre-migration physical cards | 476 |
| Local variants after the additive repair | 66 |
| Explicit physical card mappings | 508 |
| Deduplicated student-facing questions | 254 |
| Newly added paper variants | 4 |
| Newly added physical mappings | 32 |
| Verified marking-scheme maps | 64 |
| Honest paper-only maps | 2 |

The completed metadata capture reconciles all 4,681 reported items: 2,921
official State-exam associations and 1,760 commercial mock associations. No
StudyClix question text, solution, note, video, image, PDF or mock content was
copied. Every one of the 254 written questions in the entitled local SEC corpus
has at least one audited topic and every local question is retained. The 634
blocked official associations consist of 363 headings before the local corpus
begins, 173 deferred-paper headings and 98 official-sample headings. Those
headings remain factual evidence only until their underlying official sources
can be acquired and independently verified.

The additive repair freezes all 62 prior paper variants and their 476 physical
cards, then exposes the four already-entitled 2026 Higher/Ordinary English and
Irish editions. The resulting 66 variants contain 508 physical mappings and
deduplicate to 254 student-facing written questions. All editions have finite
question boundaries; 64 retain verified marking-scheme maps and two are
explicitly paper-only. A paper-only card opens beside the full scheme rather
than presenting an inferred answer crop.

Three anomalous 2016 reference headings literally use `Question A` with parts
`b`, `k` and `d`. They are preserved verbatim as reference metadata and safely
resolve to Q1 after comparison with the official paper. Four practice buckets
currently report zero questions: outgoing Higher `PRACTICAL EXAM`, outgoing
Higher `PROJECT`, new-course Higher `Project Planning and Evaluation`, and
new-course Ordinary `Control System Design`.

The incoming 2028 curriculum record keeps the specification's four official
strands canonical: Engineering Processes; Automation and Control Systems;
Design Capability; and Engineering Principles and Energy. Its 19 trackable
study areas align those official learning outcomes to the audited practice
clusters without presenting the commercial hierarchy as curriculum authority.
The record also retains the published 180 recommended class hours and 50%
design-and-manufacture project / 50% written-examination assessment. Topic
Atlas preserves the source's singular label `Advanced and Autonomous System`;
the canonical curriculum record correctly uses the specification's plural
`systems`.

Engineering browser QA confirmed one unambiguous `254 questions · 74 topics ·
2010–2026` shelf, all ten exact group headings, all 74 topic labels and honest
zero counts. The outgoing Higher `Energy, Electronics & Robotics` topic opened
with 51 questions across 17 years, including 2026 Q1, Q6 and Q9. The first 2026
card landed on paper page 3 of 12, its scheme on page 3 of 36, and the Q1 answer
dialog rendered the verified scheme pages 7–10. War Room Subject Coverage
showed the correct 2027 outgoing syllabus, transition warning and 50% written /
25% practical / 25% project assessment. Mark Bank retained all 466 authored
cards: 313 Higher and 153 Ordinary. No localhost browser warnings or errors
remained after the QA sweep.

### Engineering work still open

- Acquire and independently verify the pre-2010, deferred and official-sample
  sources behind the 634 blocked headings; do not import StudyClix-hosted
  material.
- Recover authorised marking-scheme regions for the two honest paper-only maps
  where an official scheme exists.
- Complete the manual visual sweep of all 66 paper/marking-scheme editions; the
  finite automated boundary sweep is complete but is not a substitute for full
  visual inspection.
- Map part-aware factual associations to stable Mark Bank task identities
  without deleting or renaming any of the 466 authored cards.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray
  while preserving the 2027/2028 cohort boundary.

## Italian audit — in progress, 5 September 2026

StudyClix exposes Italian as two flat practice menus: 12 Higher Level topics
and 12 Ordinary Level topics. Topic Atlas now carries those 24 exact labels as
two level-aware groups. Syllabus X-Ray remains grounded in the official Italian
curriculum nodes; the practice hierarchy is connected through an explicit
many-to-many bridge rather than replacing the curriculum.

| Italian parity gate | Result |
| --- | ---: |
| Reference topic buckets | 24 |
| Runtime display groups | 2 |
| Reported reference associations | 340 |
| Factual official State-exam associations | 340 |
| Matched associations in the local SEC corpus | 317 |
| Source-blocked associations | 23 |
| Matched local card links | 478 |
| Excluded commercial mock associations | 0 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 32 |
| Preserved pre-migration physical cards | 456 |
| Local variants after the additive repair | 98 |
| Explicit physical card mappings | 997 |
| Deduplicated student-facing questions | 730 |
| Newly added paper variants | 66 |
| Newly added physical mappings | 541 |
| Hosted paper-only fallback maps | 98 |

The metadata capture reconciles every reported item. All 317 headings from
2010–2025 resolve to entitled local SEC cards; all 23 blocked headings are from
2009, before the local corpus begins. No StudyClix question text, solution,
note, video, image or hosted PDF was copied. The exact factual heading remains
in the audit even where one reference heading expands to several finer local
cards.

The previous Italian tag wave covered only 32 written-paper variants and 456
cards. The additive repair freezes every one of those card IDs and canonical
tags, then incorporates all 96 existing Italian answer-map sidecars: written
and aural, Higher and Ordinary, and English/Irish editions where available. It
also restores the omitted 2018 Ordinary Section B Question 5, adds the complete
Section C writing tasks to the 2019–2025 papers, and adds both 2026 written
papers from verified official SEC page boundaries. The result is 98 paper
variants and 997 physical mappings, deduplicated to 730 student-facing cards.

The reference's title-specific prescribed-text buckets currently report zero
questions. The 2026 official paper now populates the correct `Le otto montagne`
and `Il treno dei bambini` reading and essay buckets without pretending that
older novels are either current title. Superseded prescribed-text cards remain
available under the broad Higher literary-reading practice bucket with explicit
`retained-local-historic-literary` provenance. The Ordinary `Fill in a Form`
bucket is likewise present exactly as captured and now has its verified local
writing cards. Only the unpublished Higher `Oral` paper bucket remains empty.

Every local card has a finite hosted paper-only fallback. Existing answer maps
continue to supply their reviewed scheme regions; a newly surfaced paper-only
card opens alongside the full official scheme instead of showing an inferred
answer crop. Italian has no authored Mark Bank deck at present, so taxonomy
parity did not fabricate one. Local browser QA confirmed the single `730
questions · 24 topics · 2010–2026` Italian shelf, both exact level headings and
all 24 labels. The current `Le otto montagne` card rendered from official paper
page 7, the restored 2018 Internet Safety card rendered across pages 14–15, and
the new Ordinary form-writing card rendered from page 18. The 2026 full-paper
jump and official full-scheme fallback both opened correctly. No browser
warnings or errors remained.

### Italian work still open

- Acquire and independently verify the 2009 sources behind the 23 blocked
  headings; do not import StudyClix-hosted material.
- Build reviewed marking-scheme regions for the newly surfaced paper-only
  writing and 2026 written cards where the official scheme supports them.
- Complete the manual visual sweep of all 98 paper variants; the finite
  automated boundary sweep is complete but is not a substitute for full visual
  inspection.
- Build an Italian Mark Bank deck only from authorised official material;
  taxonomy parity does not author or infer marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Spanish audit — in progress, 5 September 2026

StudyClix exposes Spanish as six level-aware shelves: Aural, Oral and Written
at Higher and Ordinary level. Topic Atlas now carries all 33 exact reference
labels in those six groups. One clearly marked local extension,
`Prescribed Literature (Historic Texts)`, keeps superseded official novels
available without mislabelling them as the current Ana Alcolea text. The
official Spanish curriculum remains canonical in Syllabus X-Ray and is linked
through a 34-topic many-to-many crosswalk.

| Spanish parity gate | Result |
| --- | ---: |
| Reference topic buckets | 33 |
| Local preservation-only topic buckets | 1 |
| Runtime display groups | 6 |
| Reported reference associations | 822 |
| Factual official State-exam associations | 471 |
| Matched associations in the local SEC corpus | 397 |
| Source-blocked associations | 74 |
| Matched local card links | 547 |
| Excluded commercial mock associations | 351 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 124 |
| Preserved pre-migration physical cards | 909 |
| Local variants after the additive repair | 136 |
| Explicit physical card mappings | 1,155 |
| Deduplicated student-facing questions | 616 |
| Newly added paper variants | 12 |
| Newly added physical mappings | 246 |
| Hosted paper-only fallback maps | 136 |

The signed-in metadata sweep traversed all 33 live topic pages and reconciled
all 822 reported items: 471 official State-exam associations and 351 commercial
mock associations. No StudyClix question text, solution, note, video, image or
hosted PDF was copied. Of the official associations, 397 resolve to the
entitled local SEC corpus. The 74 blocked headings consist of 51 before the
local corpus begins, 14 explicitly deferred 2022 headings whose booklet is not
held locally, and nine official oral role-play headings for which Paper Trail
does not hold the published oral booklet.

The additive repair freezes all 124 prior variants, all 909 cards and every
canonical tag verbatim. It incorporates the complete reviewed local answer-map
set, restores the missing 2020 Ordinary Irish written variant, exposes 2026,
and adds the Letter/Email, Note and Diary choices omitted from every legacy
Ordinary written card map. Both official-language Ordinary booklets were
checked when fixing those page boundaries. The reconciliation also found and
restored omitted Higher components in the 2011 and 2013 Irish maps, the 2016
English Section B map and the 2022 English short-comprehension map. Those
repairs use the corresponding official SEC booklet and same-layout language
edition, not competitor content.

Spanish historically stored written and aural cards under the same `single`
paper slot, with both restarting at Q1. The runtime join therefore includes the
normalised official booklet id; English and Irish editions deduplicate, while a
Written Q1 can never contaminate Aural Q1. All 1,155 physical cards have an
explicit file-aware topic mapping and a finite hosted paper-only fallback. A
paper-only card opens beside the official full paper/scheme rather than showing
an inferred answer crop.

The current 2026 prescribed-literature cards map only to `El medallón perdido`.
All 2010–2025 prescribed-text cards remain under the explicit Historic Texts
extension. Higher Section C's official dialogue, letter/email and diary/note
choices remain discoverable without duplicating the underlying umbrella card;
the reference's zero-count Ordinary comprehension bucket is populated by the
valid local SEC reading questions. Spanish has no authored Mark Bank deck, so
none was fabricated during the taxonomy migration.

Local browser QA confirmed one unambiguous `616 questions · 34 topics ·
2010–2026` Spanish shelf. Because Aural, Oral and Written occur at both levels,
Topic Atlas qualifies only those repeated presentation headings as `Higher
Level` or `Ordinary Level` while retaining the exact reference labels in the
taxonomy. The current Ana Alcolea literature feed showed its two 2026 cards;
the preservation extension showed 75 historic cards across 2010–2025. The
Ordinary Letter/Email feed exposed exactly one B1 card in every year, including
the restored 2020 Irish-language booklet. No localhost console warnings or
errors were produced by the Spanish QA paths.

### Spanish work still open

- Acquire and independently verify official sources behind the 51 pre-corpus,
  14 deferred and nine oral-booklet blocked headings; do not import
  StudyClix-hosted material.
- Build reviewed marking-scheme regions where the official schemes support the
  newly surfaced paper-only cards.
- Complete the manual visual sweep of all 136 paper variants; the finite
  automated boundary sweep is complete but is not a substitute for full visual
  inspection.
- Build a Spanish Mark Bank deck only from authorised official material;
  taxonomy parity does not author or infer marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## French audit — in progress, 5 September 2026

StudyClix exposes French as two flat practice menus: 19 Higher Level topics
and 14 Ordinary Level topics. Topic Atlas now carries those 33 exact labels as
two level-aware groups. Syllabus X-Ray remains grounded in the official French
curriculum; an explicit many-to-many bridge connects that curriculum to the
exam-practice hierarchy without replacing it.

| French parity gate | Result |
| --- | ---: |
| Reference topic buckets | 33 |
| Runtime display groups | 2 |
| Reported reference associations | 1,244 |
| Factual official State-exam associations | 739 |
| Matched associations in the local SEC corpus | 505 |
| Source-blocked associations | 234 |
| Matched local card links | 992 |
| Excluded commercial mock associations | 505 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 20 |
| Preserved pre-migration physical cards | 278 |
| Local variants after the additive repair | 98 |
| Explicit physical card mappings | 1,423 |
| Deduplicated student-facing questions | 1,003 |
| Newly added paper variants | 78 |
| Newly added physical mappings | 1,145 |
| Hosted paper-only fallback maps | 98 |

The signed-in metadata sweep traversed all 33 live topic pages and reconciled
all 1,244 reported items: 739 official State-exam associations and 505
commercial mock associations. There were no provider samples, unknown rows or
count mismatches. No StudyClix question text, solution, note, video, image or
hosted PDF was copied. Of the official associations, 505 resolve to entitled
local SEC material. The 234 blocked headings consist of 170 before the local
corpus begins, 60 explicitly deferred headings whose papers are not held
locally, and four Higher oral headings whose published oral material is not in
Paper Trail. The reference's Ordinary oral bucket genuinely reports zero.

The additive repair freezes all 20 prior variants, all 278 cards and every
canonical topic tag. It then incorporates the complete reviewed LC010 answer
map set across written and aural papers, both levels and both official-language
editions. It restores the missing 2015 and 2017 Ordinary A4 reading cards,
adds the indexed 2019 Ordinary written paper that previously had no sidecar,
and exposes all locally held papers through 2026. Six generic written-section
rows in the source sidecars are expanded into the actual official production
choices, including every Higher and Ordinary writing task in each locally held
written paper. Valid local tasks omitted from the reference topic pages remain
available with explicit retained-local provenance.

French written and aural papers both restart their visible question numbers,
so the runtime identity includes the official booklet id as well as level,
year, language and part. Equivalent English and Irish editions deduplicate,
while a Written Q1 can never be merged with Aural Q1. All 1,423 physical cards
have an explicit file-aware mapping and a finite hosted paper-only fallback.
Existing reviewed answer regions remain intact; newly surfaced paper-only
cards open beside the official full scheme rather than displaying an inferred
answer crop.

Only the two oral buckets are empty locally, because the authorised oral
booklets are not held. French has no authored Mark Bank deck, so taxonomy
parity did not fabricate marking content. Local browser QA confirmed the
single `1,003 questions · 33 topics · 2010–2026` shelf and both exact level
groups. The Higher newspaper/magazine feed exposed 151 cards across all 17
years; the retained 2010 B1A récit and current 2026 B1(c) récit both rendered.
The restored 2015 Ordinary A4 book-extract card appeared in its correct topic,
and the restored 2019 Ordinary B1B form card opened the official paper on page
10. The 2026 Higher aural feed kept Questions 1, 3 and 4 distinct from written
questions. No localhost console warnings or errors were produced by these
French QA paths.

### French work still open

- Acquire and independently verify the official sources behind the 170
  pre-corpus, 60 deferred and four oral-material headings; do not import
  StudyClix-hosted material.
- Build reviewed marking-scheme regions where the official schemes support the
  newly surfaced paper-only cards.
- Complete the manual visual sweep of all 98 paper variants; the finite
  automated boundary sweep is complete but is not a substitute for full visual
  inspection.
- Build a French Mark Bank deck only from authorised official material;
  taxonomy parity does not author or infer marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## German audit — in progress, 5 September 2026

StudyClix exposes German as four practice menus: Aural and Written at Higher
Level, and Aural and Written at Ordinary Level. Topic Atlas now carries all 25
exact topic labels in those four level-qualified groups. Syllabus X-Ray remains
grounded in the official German curriculum; a complete many-to-many bridge
connects the practice hierarchy to those canonical curriculum nodes.

| German parity gate | Result |
| --- | ---: |
| Reference topic buckets | 25 |
| Runtime display groups | 4 |
| Reported reference associations | 820 |
| Factual official State-exam associations | 479 |
| Matched associations in the local SEC corpus | 379 |
| Source-blocked associations | 100 |
| Matched local card links | 652 |
| Excluded commercial mock associations | 341 |
| Excluded provider-owned sample associations | 0 |
| Preserved pre-migration variants | 20 |
| Preserved pre-migration physical cards | 220 |
| Local variants after the additive repair | 100 |
| Explicit physical card mappings | 970 |
| Deduplicated student-facing questions | 664 |
| Newly added paper variants | 80 |
| Newly added physical mappings | 750 |
| Hosted paper-only fallback maps | 100 |

The signed-in metadata sweep traversed all 25 live topic pages and reconciled
all 820 reported items: 479 official State-exam associations and 341 commercial
mock associations. There were no provider samples, unknown rows or count
mismatches. No StudyClix question text, solution, note, video, image or hosted
PDF was copied. Of the official associations, 379 resolve to entitled local
SEC material. The 100 blocked headings consist of 90 before the local corpus
begins and ten explicitly deferred headings whose papers are not held locally.
The Ordinary `Write a Blog...` bucket contains six commercial mocks and no
official State-exam heading, so it correctly remains empty in Topic Atlas.

The additive repair freezes all 20 prior variants, all 220 cards and every
canonical topic tag verbatim. It then incorporates all 100 reviewed LC011
written and aural variants across 2010–2026, both levels and every locally held
official-language edition. Missing grammar, short-writing and final production
choices are restored from page boundaries checked in the official SEC
booklets. All 970 physical cards have an explicit file-aware topic mapping;
valid local questions omitted or multiply classified by the reference remain
available with explicit retained-local provenance. The extra 2013 Ordinary
Irish-edition reading identity is retained rather than deleted or silently
merged.

German's historic answer sidecars use several incompatible number runs: some
number only the reading questions, while grammar and writing restart or insert
their own labels. The student-facing IDs remain unchanged, but Topic Atlas now
prefers the generated semantic paper-only maps so a retained Reading Q5 can
never open the classic sidecar's Grammar Q5. Ambiguous legacy start anchors
fall back to the complete verified paper page, and explicit physical ordering
keeps grammar, reading, short writing and aural cards in booklet order. All 100
maps pass the finite-region safety gate; answer crops remain honestly disabled
until matching reviewed scheme regions are uploaded.

German has no authored Mark Bank deck, so taxonomy parity did not fabricate
marking content. Local browser QA confirmed the single `664 questions · 25
topics · 2010–2026` shelf and all four level-qualified groups. The 2026 Higher
aural Dialogue opened Question 3, Grammar opened its distinct G card, and the
Letter and Picture production feeds opened pages 18 and 19 respectively. The
2026 Ordinary Dialogue and Application choices remained distinct on the
verified short-writing pages; the Application full-paper action landed on page
14. The preserved 2013 Ordinary Gaeilge Q13 remained reachable, the mock-only
blog topic displayed zero official questions, and no localhost console warnings
or errors were produced by these German QA paths.

### German work still open

- Acquire and independently verify official sources behind the 90 pre-corpus
  and ten deferred headings; do not import StudyClix-hosted material.
- Build and upload reviewed marking-scheme regions for the semantic German
  cards so inline answer crops can be restored without number-run collisions.
- Complete the manual visual sweep of all 100 paper variants; the finite
  automated boundary sweep is complete but is not a substitute for full visual
  inspection.
- Build a German Mark Bank deck only from authorised official material;
  taxonomy parity does not author or infer marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Irish audit — in progress, 5 September 2026

StudyClix exposes Irish as three level menus: Higher, Ordinary and Foundation.
Topic Atlas now carries all 62 exact reference topic labels in those three
level-qualified groups. Syllabus X-Ray remains grounded in the official Irish
curriculum; a complete many-to-many bridge connects the practice hierarchy to
those canonical curriculum nodes. Two clearly labelled archive extensions
retain valid local material that the current reference hierarchy omits.

| Irish parity gate | Result |
| --- | ---: |
| Reference topic buckets | 62 |
| Preservation-only archive buckets | 2 |
| Runtime display groups | 3 |
| Reported reference associations | 1,481 |
| Factual official State-exam associations | 842 |
| Matched associations in the local SEC corpus | 534 |
| Source-blocked associations | 308 |
| Matched local card links | 744 |
| Excluded commercial mock associations | 563 |
| Excluded provider-owned sample associations | 76 |
| Preserved pre-migration variants | 26 |
| Preserved pre-migration physical cards | 286 |
| Local variants after the additive repair | 91 |
| Explicit physical card mappings | 979 |
| Deduplicated student-facing questions | 979 |
| Newly added paper variants | 65 |
| Newly added physical mappings | 693 |
| Hosted paper-only fallback maps | 91 |

The signed-in metadata sweep traversed all 62 live topic pages and reconciled
all 1,481 reported items: 842 official State-exam headings, 563 commercial
mocks and 76 provider-owned samples. No StudyClix question text, solution,
note, video, image or hosted PDF was copied. Of the official headings, 534
resolve to 744 entitled local SEC card links. The 308 blocked headings consist
of 129 before the local corpus begins, 91 deferred sittings whose papers are
not held locally, 28 provider sample-paper headings, and 60 oral-exam material
headings. The new-course poetry and prose title shelves are therefore present
but honestly empty where the only available items are provider samples.

The additive repair freezes all 26 prior variants, all 286 cards and every
canonical topic tag verbatim. It then incorporates all 91 locally held LC001
paper components across 2010–2026 and all three levels, yielding 979 explicit
physical mappings. Listening, reading, grammar, composition, prose and poetry
cards are assigned at their verified booklet locations. All 91 paper documents
have finite paper-side maps and every retained or newly surfaced local question
has at least one level-correct topic association.

Blindly replacing the local hierarchy would have deleted two legitimate
archives. Higher Paper 2 contains additional historic literature questions
that do not have a current reference bucket, so they remain under `Historic
Additional Literature (NextStepUni archive)`. The 24 frozen Foundation aural
cards from 2010 and 2011, plus their later locally held counterparts, remain
under `Cluastuiscint (NextStepUni archive)`. These are additive preservation
extensions, not claimed StudyClix labels.

Reference classification is retained as factual metadata without overriding
what the official booklet actually contains. For example, the 2024 Foundation
Q4B heading is filed under letter-writing by the reference even though the SEC
paper asks for a form. The local W-4B card consequently remains reachable from
the truthful form shelf as well as from the captured reference classification.

Irish's existing authored Mark Bank deck remains intact; the taxonomy repair
does not infer or copy marking content. Local browser QA confirmed the `979
questions · 64 topics · 2010–2026` shelf and all three level-qualified
groups. The 2026 Higher announcement opened on paper page 3; Grammar exposed
its distinct G-A and G-B cards; the preserved 2010 Higher additional-literature
card remained available as Question X; the preserved 2010 Foundation listening
shelf exposed all 12 frozen questions; the 2024 Foundation form/letter
cross-classification remained reachable; and the 2026 Foundation poem opened
on paper page 12. No application warnings or errors were produced by these
Irish QA paths.

### Irish work still open

- Acquire and independently verify official sources behind the 129 pre-corpus,
  91 deferred, 28 sample-paper and 60 oral-material headings; do not import
  StudyClix-hosted material.
- Build reviewed marking-scheme regions where the official schemes support the
  newly surfaced paper-only cards.
- Complete the manual visual sweep of all 91 paper components; the finite
  automated boundary sweep is complete but is not a substitute for full visual
  inspection.
- Keep the existing Irish Mark Bank deck covered by its independent authored
  content tests; taxonomy parity does not expand its marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Music audit — in progress, 5 September 2026

The resumed Chrome sweep captured every Music topic using one working tab. The
permanent metadata snapshot is `data/examTopics/music.json`; the fixed
pre-migration inventory is reproduced by
`scripts/paper-trail/reconcile-music-reference.mjs`. The additive runtime,
curriculum crosswalk, complete local tag wave and conservative paper-only maps
are generated by `scripts/paper-trail/build-music-exam-topic-crosswalk.mjs`.

| Music parity gate | Result |
| --- | ---: |
| Higher / Ordinary reference topic buckets | 21 / 13 |
| Explicit NextStepUni archive shelves | 9 |
| Runtime topic shelves | 43 |
| Reported reference associations | 1,127 |
| Factual official heading associations | 646 |
| Matched associations in the local SEC corpus | 459 |
| Source-blocked associations | 187 |
| Excluded mock associations | 481 |
| Mock-title / State-exam-badge conflicts excluded | 6 |
| Preserved pre-migration paper variants / cards | 20 / 184 |
| Local paper variants after the additive repair | 178 |
| Explicit physical card mappings | 978 |
| Deduplicated student-facing questions | 500 |
| Hosted paper-only anchor maps | 178 |
| Verified answer sidecars / crops | 161 / 775 |
| Complete / intentionally partial answer sidecars | 152 / 9 |
| Honest paper-only booklets | 17 |

The six conflicting items are all 2019 Ordinary composing entries. Their
titles identify them as mock papers although the source badges say State exam.
The snapshot excludes them from official headings and retains only their
counts. A regression gate rejects any mock title in the official metadata. No
question text, answer content, images, audio or provider-hosted PDFs were
copied. Transient zero counts during page loading were rechecked; only the
Higher and Ordinary `Practicals` reference buckets were finally empty.

The 187 source-blocked associations comprise 131 pre-2010 references, 22
deferred references and 34 references to the separately structured 2019
unprepared tests. A local main-sitting paper is never substituted for a
deferred paper, and the 2019 practical section/question numbers are not
equated with the legacy flattened 2013–2016 card numbers.

Music's local runtime join is now component- and file-aware. Composing (`006`),
Higher listening elective (`007`), core listening (`008`) and unprepared tests
(`U00`) all retain the historical `single` paper key and restart at Question
1. The generated mapping therefore carries each exact SEC file ID, preventing
same-number questions from different booklets from contaminating one another.
All 184 frozen cards and tags remain unchanged; the other 158 local variants
are added for a total of 978 physical mappings across 178 booklets.

The current Mozart, Berlioz, Deane and Beatles reference shelves are not
stretched across older prescribed works. Tchaikovsky, Gerald Barry, Freddie
Mercury and Bach each have an explicit archive shelf at both levels, and the
Higher listening elective has its own archive shelf. All 43 browse topics map
back to official Music curriculum nodes. Irish Music and the Higher Irish
Music Essay remain many-to-many browse associations over the same top-level
question without changing its canonical tag.

Every local booklet now has a finite hosted paper map. The 19 maps that existed
before migration are preserved. The other 159 use checked question-start pages
and conservative full-page paper regions; newer composing papers correctly
skip their summary pages and open Questions 1–3 on pages 4/6/8 and Questions
4–6 on pages 12/14/16. There are now 161 rich answer sidecars: 152 cover every
card in their booklet and nine listening maps are intentionally partial, for
775 verified scheme crops in total. Hosted paper anchors deliberately claim no
marking scheme; the app can merge their corrected paper extent with a verified
scheme crop without weakening the paper-only fallback contract.

A rendered integrity pass over every existing Music answer sidecar exposed 14
malformed legacy scheme joins: several composing maps had crossed into the
listening section, listening maps had crossed into elective or practical
material, and two older maps contained skipped, duplicated or backward page
segments. Those 14 layouts now use explicitly audited scheme boundaries. The
same repair reconciles 145 stale or missing paper starts against the separately
verified hosted paper anchors. A focused SEC table-row sweep then found nine
listening layouts and 23 composing layouts where the PDF had vertically centred
the printed question number inside a merged cell. Their crops now start at the
actual table or row border, so opening answer rows no longer sit in the preceding
question. Seven listening layouts and 22 composing layouts were additional;
two listening layouts and one composing layout refined the original set. That
brings the repair source to 43 unique layouts and 68 changed Music sidecar files
in total. The future sidecar generator now also aligns extracted question
numbers to their enclosing SEC table rows.

A repeatable repair check and generator/test gates reject invalid normalized
rectangles, backward segments, implausibly small crops and exact cross-component
region-map duplicates. All 775 crops pass that structural pass, and every
repaired layout was rendered and checked directly.

A second rendered endpoint sweep checked the first and final crop of all 132
answer maps. It found nine intentionally partial Irish listening maps whose last
reviewed question still ran into later, unmapped answers. Those nine tails now
stop at the next printed question boundary without adding or claiming any new
answer. The repair source therefore records 52 audited scheme-region corrections
in total: 43 layout repairs and nine partial-map tail trims.

A rendered 2026 start-page matrix now covers composing, listening and the
Higher listening elective at both levels where applicable, in both English and
Irish. It confirmed all 48 composing/listening question starts and exposed one
new-format exception that numeric bounds could not: the 2026 elective inserts
instructions and a `Do not write on this page` leaf, so its real response
section begins on PDF page 4 rather than the 2010–2025 page 2. The generator
and regression fixture now pin that exact year-specific shift. A fresh Chrome
recheck then caught the richer Storage answer map shadowing the corrected jump
inside the full viewer even though the Topic Atlas card preview was right. The
viewer now waits for the hosted paper anchor and overlays only its paper-side
coordinates onto the verified answer map; the live route lands on page 4 and
still exposes the genuine scheme crop.

The same rendered review corrected all four 2018 listening editions. Their
page 3 is the final-excerpt continuation of Question 1; Question 2 begins on
page 4 in both levels and both languages. The generated Question 1 region now
spans pages 2–3 and Question 2 starts on page 4, with a four-edition regression
preventing the former page-3 overlap from returning.

The older image-only and recent garbled-text outliers received a separate
rendered check rather than being treated as successful text extraction. All 48
composing/listening starts in the 2012 Higher/Ordinary English/Irish editions
were visually verified. A further 24 listening starts were visually verified
across 2022 Higher English, 2023 Higher and Ordinary English, and 2025 Ordinary
English. Together with the 50-start 2026 matrix and four-edition 2018 repair,
these focused checks supplied extra evidence for the extraction outliers.

All 32 locally held Higher listening-elective variants were then rendered as
one complete series. The 2010–2025 English and Irish response sheets all begin
on page 2 (with no 2020 elective sitting), while both 2026 editions begin on
page 4. A corpus-wide regression now pins every one of those visually checked
starts, rather than testing only a single historical comparison year.

The separately structured 2013–2016 unprepared-test corpus was also rendered
booklet by booklet. All 14 variants and 154 card positions match their printed
numbering: Higher has Questions 1–12, Ordinary has Questions 1–10, four cards
share each source page, and 2016 Higher alone begins on page 2 instead of page
3. Regression coverage now fixes those page groups and requires ordered,
non-overlapping crop bands within each page.

The final manual boundary sweep rendered 52 paper contact sheets covering all
178 physical booklets and all 978 paper-card starts. It also covered every one
of the 601 legacy scheme crops. A separate eight-sheet recovery matrix checked
all 174 starts in 29 newly recovered answer sidecars, with endpoint sheets used
to verify each final Question 6 boundary. That endpoint review caught and fixed
one Irish 2026 composing stop-heading error before the maps were frozen. The
complete reviewed surface is therefore all 978 paper mappings and all 775
stored scheme mappings, across both levels and both official-language editions.

The 29 recovered answer maps are reproducible from the SEC PDFs through
`music_sections.py --check-recovered`; the gate rebuilds and byte-compares the
whole recovery set. Seventeen booklets remain deliberately paper-only: all 14
unprepared-test papers use a shared generic practical rubric rather than
question-specific answer boundaries, while the three 2010 Higher Irish
composing, elective and listening booklets have no corresponding entitled
Irish scheme in the local SEC corpus. No English scheme is presented as an
Irish-edition answer map.

Local Chrome QA exposed and fixed one final identity bug in the shared Topic
Atlas aggregate: Music's separate components were initially deduplicated by
year/level/question number without their file IDs, producing a false 238-card
headline. The shared logical identity now retains Music's normalised booklet
ID, and the browser shows `500 questions · 43 topics · 2010–2026`. The same
one-tab pass verified the eight-year Higher Tchaikovsky archive sequence, all
16 locally held Higher listening-elective years, all twelve restored 2013
Higher practical cards, the 2025 Tchaikovsky route on listening page 3, the
corrected 2026 elective route on page 4, and the 2026 composing continuation
on page 4.

### Music work still open

- Acquire and independently verify entitled official sources for the 131
  pre-corpus, 22 deferred and 34 separately structured 2019 unprepared-test
  references; never substitute commercial mock or provider-hosted material.
- Retain the 17 honest paper-only booklets until question-specific U00 evidence
  or an entitled 2010 Higher Irish scheme is available; do not infer inline
  answers from the generic rubric or substitute the English edition.
- Refine the broad 2013–2016 practical shelf only after its printed test
  identities are independently reviewed; do not infer them from 2019 labels.
- When a Music Mark Bank deck is authored, split Higher listening Question 5
  into Part A and essay Part B at the printed mark boundary, then represent the
  essay's finite printed choice pool (four audited pre-2021 routes; five from
  2021 onward) as stable routes. Paper Trail deliberately retains the existing
  top-level Question 5 identity, and taxonomy parity does not manufacture new
  marking content.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## English audit — in progress, 5 September 2026

The one-tab signed-in sweep traversed all 86 English topic pages: 28 Higher
and 58 Ordinary. The permanent metadata snapshot is
`data/examTopics/english.json`; the compact app taxonomy and canonical bridge
are generated by
`scripts/paper-trail/build-english-geography-exam-topic-runtime.mjs`.

| English parity gate | Result |
| --- | ---: |
| Higher / Ordinary reference topic buckets | 28 / 58 |
| Explicit historical local archive shelves | 11 |
| Runtime topic shelves | 97 |
| Reported reference associations | 1,064 |
| Factual official heading associations | 566 |
| Excluded mock associations | 498 |
| Provider-owned sample associations | 0 |
| Source-label conflicts | 0 |
| Existing tagged paper variants / cards preserved | 24 / 125 |

The first 86 runtime topics reproduce the reference IDs, labels, level order
and paths exactly. The additional local archive contains ten previously
prescribed Higher poets and the former Higher Relationships comparative mode.
Those valid historical cards would otherwise disappear because the current
reference menu no longer exposes their year-specific topics. The archive is
visibly labelled as NextStepUni preservation and is not represented as a
StudyClix category.

Every current English Paper Trail tag resolves into the audited browse layer,
including the separate Paper 1 and Paper 2 slots. The original canonical tags
remain unchanged. All 1,064 displayed associations reconcile exactly as 566
factual official headings plus 498 mock counts; no mock title appears in the
official metadata and no provider question, answer or document content was
copied.

### English work still open

- Reconcile all 566 factual headings against exact local SEC booklet/card
  identities, including deferred sittings and older papers, and record each
  unresolved source boundary explicitly.
- Extend the existing topic-tag wave beyond its current 24 variants and 125
  cards without changing any stable Mark Bank card identity.
- Complete paper and marking-scheme visual QA before marking English complete.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Geography audit — in progress, 5 September 2026

The signed-in sweep traversed all 96 Geography topic pages: 29 Higher and 23
Ordinary outgoing-course topics, plus 22 Higher and 22 Ordinary topics for the
specification first examined in 2028. Its eight nested replacement-course
groups are retained as distinct level-qualified groups. The permanent metadata
snapshot is `data/examTopics/geography.json`; the same compact generator used
for English builds the app runtime and curriculum bridge.

| Geography parity gate | Result |
| --- | ---: |
| Outgoing Higher / Ordinary topic buckets | 29 / 23 |
| New-course Higher / Ordinary topic buckets | 22 / 22 |
| Nested new-course groups | 8 |
| Runtime display groups | 10 |
| Reported reference associations | 9,907 |
| Factual official heading associations | 5,475 |
| Excluded mock associations | 4,432 |
| Provider-owned sample associations | 0 |
| Source-label conflicts | 0 |
| Existing tagged paper variants / physical cards preserved | 60 / 720 |
| Language-deduplicated local question mappings | 480 |

All 96 reference topics are now active in Topic Atlas with exact labels,
paths, hierarchy and course identity. Outgoing topics bridge only to the
outgoing Geography curriculum; the 44 replacement-course topics bridge only
to the verified `geography:2028` specification. This prevents a current SEC
question from leaking into a future-course shelf merely because the wording is
similar.

Every existing Geography tag remains browsable after the atomic switch. The
720 physical language-edition cards collapse to 480 stable question mappings,
and each currently maps only to outgoing-course topics. The 9,907 displayed
reference associations reconcile exactly as 5,475 factual official headings
plus 4,432 excluded mock counts. No provider content was copied.

### Geography work still open

- Reconcile all 5,475 factual headings to exact local booklet/card identities,
  preserving main, deferred, sample and future-course boundaries.
- Complete source and answer-map coverage for the locally held paper corpus,
  especially historical map and aerial-photograph support material.
- Complete paper and marking-scheme visual QA before marking Geography
  complete.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Home Economics taxonomy — active, 5 September 2026

The signed-in sweep traversed all 54 Home Economics topic pages: 26 Higher and
28 Ordinary. The permanent metadata snapshot is
`data/examTopics/home-economics.json`; the compact app runtime uses the Paper
Trail identity `home-economics-s-and-s` while its crosswalk correctly retains
the canonical `home-economics-*` curriculum nodes.

| Home Economics parity gate | Result |
| --- | ---: |
| Higher / Ordinary topic buckets | 26 / 28 |
| Reported reference associations | 2,901 |
| Factual official heading associations | 1,561 |
| Excluded mock associations | 1,340 |
| Provider-owned sample associations | 0 |
| Source-label conflicts | 0 |
| Existing tagged paper variants / physical cards preserved | 51 / 484 |
| Language-deduplicated local question mappings | 200 |

All 54 exact labels, paths and level memberships are active in Topic Atlas.
Every captured page reconciles, every shelf maps to at least one official
curriculum node, and every existing tagged card remains browsable.

### Home Economics work still open

- Reconcile all 1,561 factual headings to exact local SEC booklet/card
  identities, with deferred and historical source gaps recorded explicitly.
- Complete paper and marking-scheme visual QA before marking the subject
  complete.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Mathematics taxonomy — active, 5 September 2026

The signed-in sweep traversed all 55 Mathematics topic pages: 26 Higher, 19
Ordinary and 10 Foundation. The exact three-level hierarchy is active from
`data/examTopics/mathematics.json`.

| Mathematics parity gate | Result |
| --- | ---: |
| Higher / Ordinary / Foundation topic buckets | 26 / 19 / 10 |
| Reported reference associations | 2,946 |
| Factual official heading associations | 1,768 |
| Excluded mock associations | 1,178 |
| Provider-owned sample associations | 0 |
| Source-label conflicts | 0 |
| Existing tagged paper variants / physical cards preserved | 140 / 1,281 |
| Language-deduplicated local question mappings | 656 |

Every captured page reconciles and all 55 shelves bridge to official
Mathematics curriculum nodes. Foundation remains a first-class level rather
than being collapsed into Ordinary. Historical counting, sequences, financial
mathematics and number-system cards absent from the narrower current menu are
retained through reviewed many-to-many canonical bridges.

### Mathematics work still open

- Reconcile all 1,768 factual headings to exact Paper 1/Paper 2 local card
  identities without collapsing language editions or paper slots.
- Complete paper and marking-scheme visual QA before marking the subject
  complete.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

## Physical Education taxonomy — active, 5 September 2026

The signed-in sweep covered all 88 hierarchy entries: 14 Higher and 10
Ordinary outgoing-course topics, plus 32 topics at each level for the 2028
replacement specification. Six nested replacement-course groups are retained
as level-qualified groups in `data/examTopics/physical-education.json`.

| Physical Education parity gate | Result |
| --- | ---: |
| Outgoing Higher / Ordinary topic buckets | 14 / 10 |
| New-course Higher / Ordinary topic buckets | 32 / 32 |
| Nested new-course groups | 6 |
| Fully reconciled topic pages | 86 |
| Reference-server-error topic pages | 2 |
| Reported associations on reachable pages | 1,803 |
| Factual official heading associations | 1,265 |
| Excluded mock associations | 538 |
| Existing tagged paper variants / physical cards preserved | 16 / 286 |
| Language-deduplicated local question mappings | 160 |

All 88 hierarchy topics are active. Outgoing topics bridge only to the 2018
curriculum. Replacement topics bridge only to the three official
`physical-education:2028` strand groups, preventing current questions from
leaking into future-course shelves. Every existing tagged local card remains
browsable in the outgoing course.

The Higher and Ordinary versions of `2.1 Apply the components of fitness in
terms of physical activity performance` each returned a StudyClix HTTP 500
from the published menu link, repeated direct navigation and two cache-busted
retries. Their hierarchy identity is preserved, but their displayed counts are
recorded as unavailable rather than inferred from another topic or level.

### Physical Education work still open

- Re-audit the two 2.1 replacement-course pages when the reference server is
  repaired, then reconcile their newly visible counts without overwriting the
  outage record.
- Reconcile the 1,265 reachable factual headings to exact local SEC booklet and
  card identities, keeping outgoing and 2028 course boundaries distinct.
- Complete paper and marking-scheme visual QA before marking the subject
  complete.
- Surface direct exam-topic ↔ official-syllabus navigation in Syllabus X-Ray.

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
