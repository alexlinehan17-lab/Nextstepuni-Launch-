# Geography handoff — paused 14 October 2026

Alex paused Geography to save CPU. Nothing was pushed, merged or deployed.
No dev server, browser or heavy check of this branch is running.

## Location

- Worktree: `/Users/alexlinehan/Documents/Nextstepuni-Geography-Audit-20261011`
- Branch: `claude/geography-audit-20261011` (base `6652f80cc`, the branch's merge-base with `origin/main`)
- HEAD at pause: the commit that adds this file. The commit before it is
  `8d169a9d5` "WIP (paused 2026-10-14): Geography 2015 Ordinary — chain checks left".

## Sittings done

Every sitting below has a review ledger (`scripts/markbank/authoring/geography_review_YYYY_{hl,ol}.py`),
an extracted scheme (`examiner-reports/geography/schemes/YYYY-{hl,ol}.md`), a pin test in
`test/markBankGeography.test.ts`, and passed the full check chain (14-file vitest, typecheck,
typecheck:test, eslint on the three Geography tests, phone browser run of six cards plus a Topic Atlas
row) unless marked otherwise.

| Sitting | Tasks | Cards | Companions (place) |
| --- | --- | --- | --- |
| 2021–2026 HL and OL | (earlier batches) | | |
| 2020 HL / OL | 114 / 120 (119 carded) | 125 / 125 | Arklow |
| 2019 HL / OL | 113 / 127 | 121 / 138 | Templemore |
| 2018 HL / OL | 122 / 124 | 130 / 131 | Sligo |
| 2017 HL / OL | 110 / 122 | 125 / 130 | Macroom |
| 2016 HL / OL | 106 / 118 | 108 / 128 | Westport |
| 2015 HL | 105 | 113 | Kenmare |
| 2015 OL | 102 | 107 | Kenmare — **WIP, see below** |

Corpus at HEAD: 3,025 Geography cards (HL 1,469, OL 1,556); census 2,826 base tasks, 2,825 carded,
1 held; selection audit 170 (104 routed, 66 one-card pools); preservation additions 2,364; Topic Atlas
mapping count 1,345 (unchanged: single-booklet sittings add topics to existing Part Two rows).

## Exact resume point

1. **Finish 2015 Ordinary** (commit `8d169a9d5`). Already passed: `geography_cards.py --check`,
   cardlint clean, reconcile 2825/2826 with the baseline written. Not yet run: the subject showcase
   rebuild (`components/landing/subjectShowcase.json` is not yet regenerated), the 14-file vitest,
   typecheck, typecheck:test, eslint on the three Geography tests, and the `ol15` browser case (already
   added to `tmp/geography-audit/browser/browser.mjs`). Run the chain below with `ol15`; if green, amend
   nothing — make a follow-up commit with the regenerated showcase JSON.
2. **2014 Higher** (next new sitting). Page text and scheme lines were dumped but no ledger exists yet.
   Findings so far: the Part One scheme (p4) prints a centred heading — "Each question: 4 parts @ 2 marks
   each or 8 parts @ 1 mark each" and "Q4(iv), Q9(iv), Q11(iv) & Q12(iv) @ 1 + 1 mark" — over unpriced
   answer lines in two columns (clips LEFT `(0, 0.32, 0.472, 1)`, RIGHT `(0.472, 0.32, 1, 1)`; the page
   footer splits into "Pag" / "ge 2 of 44", so end the last slices there). Q4(ii) is printed
   "Award 2m (ambiguous wording)": carry that line as the guidance. Model on the 2015 Higher ledger,
   which handles a heading-priced Part One. The 2014 scheme prints its note bullets as "¾ ·" (a mangled
   arrow glyph): repair it before carding, deriving the map from the glyph ids, never by hand.
   Selection scan: `[[1,2,'attempt ten'],[1,13,'attempt four'],[1,14,'attempt two'],[1,15,'attempt one'],
   [1,15,'one of the following'],[1,16,'answer (i) or (ii)'],[1,18,'attempt one'],[1,19,'any two'],
   [1,20,'any two'],[1,21,'attempt one'],[1,22,'one of the following'],[1,23,'any two'],
   [1,28,'one of the following'],[1,29,'attempt one']]`.
3. Then 2014 OL, 2013, 2012, 2011, 2010 (HL then OL each), newest first.

## Sources for what is left (English editions, Paper Trail corpus, bytes)

| Year | HL paper | OL paper | HL scheme | OL scheme | Map `LC005CLP003EV` | Legend `LC005CLPC00EV` | Aerial `LC005CLP004EV` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2014 | 1,649,594 | 2,451,016 | 456,897 | 156,491 | .pdf 4,043,493 (8 stacked strips) | .pdf 587,436 | .pdf 2,196,383 |
| 2013 | 3,686,604 | 3,000,630 | 1,035,658 | 493,862 | .pdf 1,340,745 (1379 x 1936 image) | .pdf 1,167,773 | .pdf 1,646,330 |
| 2012 | 2,999,085 | 1,496,544 | 1,089,373 | 454,708 | .pdf 1,738,631 | .pdf 267,008 | .pdf 3,193,770 |
| 2011 | 4,390,619 | 1,469,613 | 1,286,377 | 347,448 | .pdf 2,360,445 | **no legend file** | .pdf 726,238 (2 images) |
| 2010 | 3,619,088 | 3,266,667 | 855,544 | 503,193 | .jpg 4,062,934 | `LC005CLP000EV.jpg` 1,636,000 (unlabelled; likely the legend — verify) | .jpg 2,806,497 |

Papers are `LC005ALP000EV.pdf` (HL) and `LC005GLP000EV.pdf` (OL) in `paper-trail-corpus/exampapers/YYYY/`;
schemes are the same names in `paper-trail-corpus/markingschemes/YYYY/`. 2014 is Dungarvan. Before
carding 2011, open the map sheet to see whether it carries the legend; if it does not, the legend-
dependent tasks are census-held with that reason rather than carded without their source. 2010's
JPEG names need a look before they are wired into `COMPANIONS`.

## Regenerate and check (run from the worktree; heavy commands only through the session's heavy lock)

```sh
cd /Users/alexlinehan/Documents/Nextstepuni-Geography-Audit-20261011
# audit aids
python3 scripts/markbank/authoring/geography_review_tools.py dump YEAR LEVEL OUT_DIR
python3 scripts/markbank/authoring/geography_review_tools.py draft geography_review_YYYY_xx OUT.json   # from scripts/markbank/authoring
python3 scripts/markbank/authoring/geography_review_tools.py show OUT.json
# wire: import the ledger and add (YEAR, LEVEL) to REVIEWED, and the year to COMPANIONS, in geography_cards.py
python3 scripts/markbank/authoring/geography_figures.py --write  # render bound crops (before the generator)
python3 scripts/markbank/authoring/geography_cards.py            # write
python3 scripts/markbank/authoring/geography_cards.py --check    # must say "current"
python3 scripts/markbank/authoring/geography_refcheck.py         # citations against the printed paper
(cd scripts/markbank/authoring && python3 cardlint.py geography && python3 reconcile.py geography && python3 reconcile.py geography --baseline write)
cp paper-trail-corpus/markingschemes/YEAR/LC005{A|G}LP000EV.pdf examiner-reports/geography/schemes/YEAR-xx.pdf
python3 scripts/markbank/extract-scheme.py examiner-reports/geography/schemes/YEAR-xx.pdf --marks-column -o examiner-reports/geography/schemes/YEAR-xx.md
for f in tables columns fractions maths; do python3 scripts/markbank/append-scheme-$f.py geography YEAR xx; done
rm examiner-reports/geography/schemes/YEAR-xx.pdf
# check chain
node scripts/build-subject-showcase.mjs
npx vitest run test/markBankGeography.test.ts test/geographyExamTopics.test.ts test/markBankCardPreservation.test.ts \
  test/markBankCoverage.test.ts test/markBankDeck.test.ts test/curriculumRegistry.test.ts test/examTopicRegistry.test.ts \
  test/paperTrailTopics.test.ts test/markBankSession.test.tsx test/subjectShowcase.test.ts test/studyclixQuestionParity.test.ts \
  test/waysInKeyPartsGold.test.ts test/askThePapers.test.tsx test/waysInKeyParts.test.ts
npm run typecheck && npm run typecheck:test
npx eslint --max-warnings 0 test/markBankGeography.test.ts test/geographyExamTopics.test.ts test/markBankCardPreservation.test.ts
GEO_CASES=<case> bash tmp/geography-audit/browser/run.sh      # phone browser on port 5710; harness is git-ignored
node scripts/landing/ask-topics.mjs   # after a Higher sitting only; commit the index on its own
```

Tests to update per sitting: census/card/sitting counts, the per-sitting card map, HIGHER/ORDINARY/ALL,
selection audit and pool counts, `REVIEWED`, the single-booklet Atlas table, the aerial fileid table
(Higher), a pin test, and the preservation additions count (never rewrite a frozen hash).

## Known issues

- **2020 OL 9C is held**: its published allocation adds to 27 against the printed 30 marks; it stays in
  the census as excluded with that reason.
- **Question echo in directions**: 369 cards in sittings carded on this branch (mostly 2017–2021
  Ordinary) list the scheme's reprint of the question as an examiner direction (for example
  "(ii) · Explain briefly ..."). Nothing is wrong, but it repeats the question. 2015 and 2016 avoid it
  by starting each slice at the allocation line; a one-line generator fix (drop a direction whose text is
  the card's question) would clear the rest. Not done.
- `test/musicExamTopics.test.ts` ("reproduces all 29 recovered scheme maps") timed out at 30 s inside the
  full `npm test` under load; it passes alone. Unrelated to Geography.
- The 2016 and 2017 map extracts are the official low-resolution files (a ~1136 x 784 image in a one-page
  PDF); legible at full size.
- Full `npm test`, `npm run build` and `npm run lint` were last run at `cb3900a54` (build then failed on
  the factory chunk; fixed in `753b03c71` and rebuilt clean). They have not been re-run since; run them
  before integrating.

## Integration notes (files shared with other subjects)

- `components/MarkBank/SessionScreen.tsx`: Geography rubric sliders step by the criterion's permitted
  increment; an "Examiner directions" list under the criteria.
- `components/MarkBank/SourceMaterialReader.tsx`: shows a companion published as a JPEG/PNG (an aerial
  photograph, an older legend) as the exact image, with a load-failure message and an open-original
  link; PDFs are unchanged.
- `components/MarkBank/cardAliases.ts`: Geography progress aliases (choose-N combination cards collapsed
  into one card; 93 Geography aliases against `origin/main`, 0 ids lost).
- `types/markBank.ts` (`GeographyRubric.directions`), `data/examTopics/registry.ts` (registers
  `geography-reviewed-question-runtime.json`), `components/MarkBank/cards/geography/factory.ts`.
- `vite.config.ts` + `test/precacheStaysLean.test.ts`: `**/factory-*.js` kept out of the service-worker
  precache (the Geography factory chunk passed the 3 MiB limit and failed `npm run build`).
- `test/markBankCoverage.test.ts`: the Geography citation grammar accepts lettered parts (a)-(d).
- `test/waysInKeyParts.test.ts`, `test/fixtures/waysInKeyPartsGold.json`: Ways In gold entries for
  collapsed Geography cards.
- Landing: `public/assets/landing/ask/topics.json` and `components/landing/subjectShowcase.json` are
  generated by every subject; regenerate them after merging rather than merging their text.
- `components/MarkBank/cards/sizes.json` is generated.

## Completed 23 October 2026: every English sitting, 2010–2026

All 34 English (EV) sittings, 2010–2026 Higher and Ordinary, are reviewed and wired. Census: 3,869 separately
priced base tasks, all 3,869 carded, none held; 4,153 cards; reconcile 3,869/3,869, 0 excluded, 0 open, 0 orphans,
0 unparsed; every citation agrees with the printed paper (`geography_refcheck.py`, 4,153/4,153); every card files
under a Topic Atlas heading that covers its syllabus topic; all 754 shipped ids still resolve (preservation test).
Irish (IV) editions stay deferred.

| Sitting | Tasks | Carded | Held | Cards | Companions |
| --- | --- | --- | --- | --- | --- |
| 2014 HL / OL | 103 / 111 | 103 / 111 | 0 / 0 | 110 / 125 | Dungarvan |
| 2013 HL / OL | 104 / 95 | 104 / 95 | 0 / 0 | 111 / 102 | Enniscorthy (aerial stored on its side) |
| 2012 HL / OL | 106 / 108 | 106 / 108 | 0 / 0 | 110 / 115 | Carrick-on-Shannon |
| 2011 HL / OL | 96 / 119 | 96 / 119 | 0 / 0 | 101 / 133 | Dingle (no legend published) |
| 2010 HL / OL | 99 / 102 | 99 / 102 | 0 / 0 | 106 / 114 | Carrick-on-Suir (JPEGs, names swapped) |

The seven parts once held are carded with only what the paper and scheme print (coordinator, 23 October):
- 2011 HL Part One Q2(i), Q2(iii) and 2011 OL Part One Q11(i): the printed question, the official map plus a crop
  of it around the grid reference asked about (`geography_figures.py`), the scheme's printed answers and marks, and
  a note that the SEC published no 2011 legend, so the symbol's meaning is given in the marking scheme.
- 2011 OL 1A and 7A sketches: the scheme's itemised sketch allocation, as 2011 OL 12A, with a note naming the
  items the map shows only by symbols.
- 2010 OL Part One Q4: the question is the paper's own print (a crop of the heading, instruction, the ruled row of
  five terms and the diagram with its empty boxes, shown before the reveal as `questionFigure`); the question text
  carries the term row lifted cell by cell (`Lift(table=True)`); each criterion carries its own printed scheme
  label at 2 marks (the scheme's drawing is sliced into its two label columns); the scheme's labelled diagram is a
  solution crop shown only after the reveal. Ways In gets the paper's crop, never the scheme's.
- 2020 OL 9C: the scheme's two priced lines as printed are the criteria ("Impact identified 1 SRP 3m" in a 3-mark
  SRP, "Explanation 8 SRP’s @ 3m each 24m" in 3-mark steps) against the printed total of 30. The 3 marks the scheme
  allocates to no line stay unpriced (`Task.unpriced` in the ledger, `rubric.unpricedMarks: 3` on the card): never
  derived, never redistributed, so the card places at most 27 of 30 and its note says so. (An earlier draft put a single 0-30
  slider in 1-mark steps over all three lines, which let a student award marks the scheme never gives.)

New shared-for-Geography machinery on this branch since the pause:
- `geography_review.py`: drops a direction that only reprints the card's question (369 lines on 2017–2021
  cards); repairs symbol-font glyphs by glyph id (`geography_glyphs.py` -> `glyphmap-geography.json`; the 2014
  schemes' Wingdings bullet "¾" -> "•"); a lone bullet joins the line on its own baseline; `SchemeSlice.keep_digits`.
- `geography_cards.py`: a companion may be `None` (2011 legend); HELD rows may name one part (`sub`).
- 2010's COMPANIONS map CLP004 (map) / CLP003 (aerial) / CLP000 (legend) — the reverse of later years. Paper Trail's
  index labels 2010 CLP003 "Map" and CLP004 "Picture/Illustration" (a Paper Trail labelling issue, untouched).
- 2010–2013 Higher options print "3 @ 27 + 27 + 26" or "4 @ 20" with coherence inside each aspect (no Overall
  Coherence table); cards carry identifying + coherence (32) and discussion (24 SRPs, 48), true under either.
- The 2011 schemes' covers print "HIGHER/ORDINARY LEVEL" in capitals, which the shared `append-scheme-*.py` passes
  do not match (case-sensitive), so `2011-*.md` hold the base extraction only (Geography reads the .md for presence).
- `coverage-baseline.json` exclusions grew 1 -> 7 during the run and are back to 0; the final baseline was
  written without `--accept-regression`.
- Card model (shared): `SecRubricCard` may carry a `figure` (the session screen already renders one and holds a
  `solution` crop until the reveal) and a `questionFigure` (as `SecQuestionCard`: the paper's print, shown before
  the reveal in place of the typeset stem); the Geography factory passes both and a factual `note` (shown first in
  "How to use this guide"). Crops live in `public/exam-figures/geography/markbank/` (5 PNGs, MD5 on the card),
  rendered by `geography_figures.py --write` and checked by it with no argument.
- Card model (shared): `GeographyRubric.unpricedMarks` declares a printed remainder the scheme prices on no line;
  `tariffReconciles` counts it (criteria + unpriced = printed total; unpriced a non-negative integer below the
  total), so the bank-wide "marks reconcile against the printed tariff" check still catches any undeclared gap.
  Only 2020 OL 9C uses it (pinned by a test).
- `geography_review.py`: `Lift(table=True)` lifts a ruled table cell by cell; `Task.question_figure`; `Task.unpriced`
  (a printed remainder the scheme allocates to no line; the build requires a note with it).
- Three earlier cards asked about "the table below" with no table on the card (the rows were only criterion labels,
  which appear after the reveal): 2017 OL Part One Q9 and 2020 HL Part One Q5(i), Q5(ii) now carry the official
  question page, as their sibling questions do.
- `cardlint.py geography` prints "clean" without reading a Geography card (it reads
  `scripts/markbank/authored/geography.json`, which does not exist; the cards are
  `components/MarkBank/cards/geography/authored.json`) — the same trap as English. Run over the real cards, the rules
  flag 48: 46 "undecoded-letters" (lettered diagram questions; every one carries the official question page and its
  scheme rows decode the letters — the rubric model, not a defect) and 2 "ghost-figure" false positives (2015 HL 5C,
  2021 HL 6C print the table's five items as the card's first line).
- `geography_refcheck.py` (new): the Geography census is built from the ledgers, so reconcile's zero orphans cannot
  catch a wrong question number. This gate reads the paper: it finds each card's text on its cited page and checks
  the nearest printed heading ("Question 7" + "A.", "9C.", "4.") against the citation, and the printed roman.
- Ways In (shared): `components/WaysIn/sources.ts` no longer offers a `solution` figure as the question's figure.
  This also stops 59 Economics and 2 Chemistry scheme-answer crops (tick tables, a p-orbital drawing) appearing
  before the reveal in Ways In.

**Topic Atlas, Part One of 2010–2019 (done 23 October).** Before 2020 one booklet printed Part One (Q1–12) and
then Part Two, which restarts at Q1. Three things numbered it differently: the Viewer's Storage sidecar anchors Part
Two 1–12 (live Higher maps stop at Q12; the repo copies add the option essays 13–24), the hosted paper-anchors the Atlas
reads for these booklets (TV-10) anchored Part One 1–12, and the StudyClix crosswalk joined both parts' headings to one
number. So `(single, n)` named two questions: a Part Two topic could show a Part One crop, a Part One card resolved to
the Part Two question of its number, and opening the Viewer from the Atlas moved a Part Two chip onto the Part One
page. Now:
- `(single, n)` is Part Two, as the Viewer's chips, Full Loop and Topics tool number it. Part One files as
  `(single, 1000 + n)`.
- `geography_atlas_anchors.py` builds the 40 hosted maps (2010–2019, Higher/Ordinary, English/Irish) as section-restart
  maps (the `printOrder` + `label` mechanism `test/vaultAnchors.test.ts` documents): Part Two copies the sidecar's own
  n, page and band (identical to live Storage, checked by download), plus the reviewed Higher option regions; Part One
  takes 1001–1012, the label "Part One · Question N" ("Cuid a hAon · Ceist N" in Irish, as printed) and the exact crop
  the Atlas showed before, frozen in `scripts/paper-trail/geography-part-one-anchors.json`. 2017 Ordinary Q12 gets
  an audited end on page 27. No Storage upload: the Viewer's sidecars are untouched, so its chips and Full Loop stops
  are unchanged; Part One gets no chips.
- `geography_cards.py` re-keys the StudyClix crosswalk's shared-booklet associations (386 headings, 772 English and
  Irish targets) evidence first (the topic proven by only one part's review decides; otherwise the heading's shape: a
  Part Two question prints A/B/C or is an option essay) and files each row's shipped topics on its own part. The Irish
  edition's rows mirror the English identities (no Irish content re-reviewed). 2020+ rows are byte-identical.
- `questionLabel` (components/PaperTrail/topics.ts) names a Part One question "Part One · Question 4" wherever the app
  printed a raw number (Atlas card title before its map loads, Mock Exam list, review deck, Viewer's cross-year chips).
- Measured: every one of the 4,153 cards now resolves to its own Atlas question and is listed under each of its own
  headings (before: 3,504; the 649 Part One cards of 240 questions resolved to the same-numbered Part Two question).
  Atlas questions for Geography: 780 -> 1,020 (English), exam-topic mappings 1,345 -> 1,825 (with the Irish mirror).
- Re-run order after the StudyClix builder (`build-browser-question-parity-crosswalks.ts`): `geography_cards.py`
  (re-keys the crosswalk) then `geography_atlas_anchors.py --check`.

Also on 23 October: `origin/main` (through #263) is merged into this branch (conflicts resolved in shared files:
types, SourceMaterialReader, cardAliases, the preservation test's frozen-identity framework, vite precache, landing
topics). The merge exposed nine stale Ways In gold entries for reviewed Geography cards (re-annotated by the fixture's
conventions; no floor changed). `cardlint.py geography` now reads the Geography deck (it used to print "clean" without
reading a card); it reported the 48 flags of the manual run, resolved as: a rubric card decodes its letters in the
scheme's rows and needs only its printed page (46), and two cards whose printed table is five headings carried in the
question text (cardlint-reviewed.json). English has the same missing-file shape and is not wired yet (one entry in
`DECK_CARDS`). This worktree's `node_modules` now links to the Agri ship worktree's (identical lockfile to main), as
main added `@capacitor/local-notifications`.

Checks at the final commit (23 October): `geography_cards.py --check` current; `geography_figures.py` 5 crops current;
`geography_atlas_anchors.py` 40 maps current; `cardlint.py geography` clean; `reconcile.py geography` 3,869/3,869, 0 excluded, 0 open,
0 orphans, 0 unparsed, baseline written without `--accept-regression`; `geography_refcheck.py` 4,153/4,153; the
14-file vitest chain plus paperTrailAnswers, vaultAnchors, markBankTopicAtlas and precacheStaysLean: 18 files,
4,282/4,282 (includes the preservation test: frozen 754 ids by hash, 3,492 additions); typecheck,
typecheck:test and `npm run lint` clean; Chrome phone (390) and desktop (1280) runs of 2011 HL Q2(i), 2011 OL Q11(i),
1A, 2010 OL Q4, 2020 OL 9C and 2017 OL Q9 (no page errors, no horizontal overflow; the Q4 scheme drawing appears only
after the reveal; 9C places 27 / 30), and of the Atlas (2010 OL Part One Q4 and Part Two Q4, 2011 HL Part One Q2) and
the Viewer opened from it (`1004` lands on page 4 with no chip; `4` on page 17; the 12 chips on exactly the live
sidecar's pages). Full `npm test` and `npm run build` were last run by the previous session before
these final changes (6,229/6,230, the known `musicExamTopics` timeout; build and lint passed).
Nothing is merged, deployed or opened as a PR; the branch ships later as one step onto current main
(regenerate `public/assets/landing/ask/topics.json` and `components/landing/subjectShowcase.json` after merging).
