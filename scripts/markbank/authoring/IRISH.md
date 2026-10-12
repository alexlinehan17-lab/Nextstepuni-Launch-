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
The Q2/Q3B review alone is partial. The combined reviews now complete 2024
Higher Paper 2; the rest of 2022 Higher Paper 2 remains pending.

`irish_reading.py` reviews all 100 reading marks in 2024 Higher Paper 2. It adds
44 practice cards and repairs the twelve retained whole-question rubrics, with
56 exact Bank/Atlas joins. Thirty-nine non-overlapping tasks cover the section;
retained whole questions and complete subparts overlap these tasks. Grammar
pairs stay together at 0/2/3 because the first correct item earns two marks.
A6(b) retains the shared opinion condition; B6(b) exposes both six-mark insights.
Every task includes both passage pages. `irish-reading-review.json` pins the
boundaries, hashes and raw selection decisions.

`irish_literature_2024.py` restores the complete Q3A and Q4 scheme guidance and
classifies every selection-directive line in the full 2024 paper, including
source narrative. Two adjectives retrieved from the printed poem are answers
to one interpretation task, not an enumerated task menu; the scheme examples
are expressly non-exhaustive. The named poet condition, one-adjective cap and
incomplete-essay caps remain with their respective awards.

`irish-paper-reviews.json` records the independent full 2024 Higher Paper 2
review: all sixteen paper pages and all applicable combined-scheme pages,
72 exact Bank/Atlas joins, no open issues, and mobile source/scheme checks.
Its 55 non-overlapping task/route cards cover both required passages, all six
prose routes, four poetry responses and six additional-literature responses.
The candidate answers 100 + 30 + 30 + 40 marks; alternative tariffs are not
added together. The archive inventory now has three reviewed components and
88 pending components. Sixty-nine still have no Mark Bank cards.

`irish_foundation.py` adds the visually reviewed 2025 Foundation paper: fourteen
listening parts, ten matching parts, thirty reading parts and six whole writing
cards. Each reading part and writing option carries the printed choose-two
instruction in its task requirements; no card combines two choices. Source hashes and
selection decisions are committed beside the cards in `foundation-authored.json`.

`irish_foundation_2024.py` independently reviews all twenty 2024 Foundation
paper pages and all twenty-four scheme pages. Its 78 cards cover fourteen
listening parts, ten sign matches, thirty reading parts and six whole writing
cards. The three
interview dates are 25 June, 27 June and 3 July; each form remains 45 marks. The
2024 length table differs from 2025 and is preserved exactly. Sixty individual
task and option cards represent the permitted practice choices; the examination
total is 120 + 40 + 50 + 60 + 90 = 360.

Every 2024 task joins to the correct Atlas topic with complete source and scheme
pages. The external reference's letter association for the form is explicitly
corrected against SEC page 15, while its original heading remains in the audit.
The runtime registry filters incompatible reference tags against these local
joins. All prior 529 Bank cards and 1125 Atlas identities remain. The original
three Foundation section crops are preserved; corrected regions are additive.
Mobile PDF rendering, source navigation, focus return and official audio playback
passed. `foundation-2024-authored.json` pins source hashes, exact raw directive
lines and boundary decisions; `irish-review.json` records runtime checks.

## Marking boundaries and selections

Use the actual year's scheme. Separately marked reading and listening parts can
be practised independently. A whole written response with one shared language
award stays whole; show its published content allocations inside the rubric.

Choice is not a route. When the student chooses N of M printed items, each
printed option or part keeps its own card and the choose instruction goes into
its task requirements; never make a card per combination. The one exception is
a scheme that marks a set jointly, which becomes one card with slot criteria.
Closed variants inside one task still get one card each: the 2025 form has
three interview dates, which produce three 45-mark form cards, never multiplied
by another writing choice. `irish_choice.withdraw_combinations` enforces this in
every generator and `test/irishChoiceIsNotARoute.test.ts` guards it.
Multiple-choice distractors are answers to one task, not alternative
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
`LC001BLP017IV.mp3`; the 2024 and 2025 official SEC URLs have been checked. These filenames
must not be interchanged. The older Higher/Ordinary cards retain their playback
mirrors until individually reviewed.

Foundation task IDs join to exact year/level/file/question identities in the
Irish exam-topic crosswalk builder. Reviewed 2024/2025 anchors include both question
pages and scheme pages. Canonical IDs come from the existing curriculum and
exam-topic registry, never copied topic-name arrays. A mixed-topic selection
retains all relevant curriculum nodes for Mark Bank filtering.

Reviewed Higher routes also carry question and scheme pages. Their Atlas route
instruction remains visible above the paper on phones. Prescribed prose and poetry have
archive shelves linked to the reviewed works' existing canonical nodes. Existing Atlas identities and the twelve original
reading-answer records in each Higher sidecar retain their original fields.
Reviewed reading display regions are additive: they show the full passage and
all relevant scheme pages without changing frozen identities or original crops.

Three legacy schemes missing from the index have been recovered from the SEC:
2010 Higher/Ordinary and 2011 Foundation use `EV` filenames despite their Irish
content. `irish-recovered-schemes.json` pins their URLs, hashes and local/hosted
paths. Exact year/file overrides now pair all eight affected components to those
schemes. The three verified PDFs are bundled with Hosting and available in an
isolated corpus overlay; the original shared corpus is untouched. All 91 indexed
components now have local papers and paired schemes. Source availability does
not establish task completeness: these eight components still await review.

Reviewed answer maps use explicit physical print order for lettered task IDs and
effective scheme regions to bound the full answer range, including the final
2024 Higher literature pages. Existing IDs and frozen crop fields are preserved.

## Rebuild and verification

The complete source PDFs live under `paper-trail-corpus/`; the legacy generator
also uses its local `examiner-reports/irish/papers/` inputs. Generated data and
searchable scheme extracts are committed. Never write through another checkout's
corpus symlink.

```sh
python3 scripts/markbank/authoring/irish_cards.py --check
python3 scripts/markbank/authoring/irish_foundation.py --check
python3 scripts/markbank/authoring/irish_foundation_2024.py --check
node scripts/paper-trail/build-irish-exam-topic-crosswalk.mjs
node scripts/paper-trail/topic-tags/build-tags.mjs
python3 scripts/markbank/authoring/irish_inventory.py --check
npm run typecheck
npx vitest run test/markBankIrish.test.ts test/markBankIrishReading.test.ts test/markBankIrishLiterature2024.test.ts test/markBankIrishHigherRoutes.test.ts test/markBankIrishFoundation.test.ts test/markBankIrishFoundation2024.test.ts test/markBankSession.test.tsx test/markBankProfileDefaults.test.ts test/irishExamTopics.test.ts test/markBankCardPreservation.test.ts test/curriculumRegistry.test.ts test/markBankDeck.test.ts
```

The Foundation generator fails if the reviewed PDFs change, if an extracted
selection directive is unclassified, or if a selection decision no longer matches
its source. The 2024 guard pins every exact directive line and rejects unknown
additions even on already-reviewed pages. The tests pin route IDs, wording, tariffs, source
pages, topics and scheme anchors. These guards support, and never replace, the
required full visual paper/scheme sweep. Do not update preservation baselines to
hide unfinished coverage.
