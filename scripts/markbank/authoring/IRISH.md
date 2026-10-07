# Irish Mark Bank authoring

The required scope is all 91 Irish Paper Trail components from 2010–2026 at
Higher, Ordinary and Foundation Level. The archive is **not complete**.
`scripts/markbank/authored/irish-archive-inventory.json` records the paper-level
backlog; card presence is never proof that every part or answer route is covered.

The legacy generator retains all 400 Higher/Ordinary card identities from 2021–2025
and adds seven reviewed Higher literature routes plus 44 reading tasks (451 cards). Its
`irish-census.json` is a generated ledger, not an independent completeness audit.
Known omitted alternatives and unsplit reading tasks still require review. The
five additional-poetry Q4F cards have separately documented source corrections.

`irish_higher_routes.py`, called by the legacy generator, reviews Q2 and Q3B of
2022 and 2024 Higher Paper 2. It restores the two omitted drama routes per year
and expands the 2022 optional-poetry images/contrast/emotions choice into three
whole responses. Twelve existing responses receive verified prompt/rubric
corrections. Each poetry card exposes 13/5/7 knowledge marks and one shared
five-mark Gaeilge award. Nineteen exact Bank/Atlas task identities, source
hashes and raw selection decisions are recorded in `irish-higher-route-review.json`.
This is a partial review: neither Higher paper is certified complete.

`irish_reading.py` reviews all 100 reading marks in 2024 Higher Paper 2. It adds
44 practice cards and repairs the twelve retained whole-question rubrics, with
56 exact Bank/Atlas joins. Thirty-nine non-overlapping tasks cover the section;
retained whole questions and complete subparts overlap these tasks. Grammar
pairs stay together at 0/2/3 because the first correct item earns two marks.
A6(b) retains the shared opinion condition; B6(b) exposes both six-mark insights.
Every task includes both passage pages. `irish-reading-review.json` pins the
boundaries, hashes and raw selection decisions; this is not a full-paper review.

`irish_foundation.py` adds the visually reviewed 2025 Foundation paper: fourteen
listening parts, ten matching parts, thirty reading parts, six whole writing
routes, six paired reading routes, and twelve paired writing routes. The paired
routes reproduce the printed choose-two instructions; their marks are not added
to individual alternatives to infer the examination total. Source hashes and
selection decisions are committed beside the cards in `foundation-authored.json`.

## Marking boundaries and selections

Use the actual year's scheme. Separately marked reading and listening parts can
be practised independently. A whole written response with one shared language
award stays whole; show its published content allocations inside the rubric.

Expand closed task choices, including choices inside a task. The 2025 form has
three interview dates, which produce three 45-mark routes. Combining it with
another writing task therefore expands each relevant pair into three 90-mark
routes. Multiple-choice distractors are answers to one task, not alternative
valid tasks. Required headings, indicative examples and open choices such as
school subjects or hobbies are not finite task pools.

Penalties scoped to an award use `deductFrom`. They cannot reduce a different
response or its language award. Do not invent unprinted word-count thresholds:
the 2025 Foundation form names a maximum length deduction of three marks, but
its explicit table only supplies zero and minus one placements.

## Material and topic parity

Attach every required passage, poem, form, map and picture page to the source
reader. A combined listening exercise must retain all its member source pages.
Listening requires the actual recording; never expose the answer transcript.

Higher/Ordinary use `LC001ZLP017IV.mp3`. Foundation has a different recording,
`LC001BLP017IV.mp3`; the 2025 official SEC URL has been checked. These filenames
must not be interchanged. The older Higher/Ordinary cards retain their playback
mirrors until individually reviewed.

Foundation task IDs join to exact year/level/file/question identities in the
Irish exam-topic crosswalk builder. Reviewed 2025 anchors include both question
pages and scheme pages. Canonical IDs come from the existing curriculum and
exam-topic registry, never copied topic-name arrays. A mixed-topic selection
retains all relevant curriculum nodes for Mark Bank filtering.

Reviewed Higher routes also carry question and scheme pages. Their Atlas route
instruction remains visible above the paper on phones. Prescribed prose has an
archive shelf linked to the reviewed works' existing canonical nodes; it is not
filed as optional prose. Existing Atlas identities and the twelve original
reading-answer records in each Higher sidecar retain their original fields.
Reviewed reading display regions are additive: they show the full passage and
all relevant scheme pages without changing frozen identities or original crops.

## Rebuild and verification

The complete source PDFs live under `paper-trail-corpus/`; the legacy generator
also uses its local `examiner-reports/irish/papers/` inputs. Generated data and
searchable scheme extracts are committed. Never write through another checkout's
corpus symlink.

```sh
python3 scripts/markbank/authoring/irish_cards.py --check
python3 scripts/markbank/authoring/irish_foundation.py --check
node scripts/paper-trail/build-irish-exam-topic-crosswalk.mjs
node scripts/paper-trail/topic-tags/build-tags.mjs
python3 scripts/markbank/authoring/irish_inventory.py --check
npm run typecheck
npx vitest run test/markBankIrish.test.ts test/markBankIrishReading.test.ts test/markBankIrishHigherRoutes.test.ts test/markBankIrishFoundation.test.ts test/markBankSession.test.tsx test/markBankProfileDefaults.test.ts test/irishExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts
```

The Foundation generator fails if the reviewed PDFs change, if an extracted
selection directive occurs on an unclassified page, or if a selection decision
no longer matches its page. The tests pin route IDs, wording, tariffs, source
pages, topics and scheme anchors. These guards support, and never replace, the
required full visual paper/scheme sweep. Do not update preservation baselines to
hide unfinished coverage.
