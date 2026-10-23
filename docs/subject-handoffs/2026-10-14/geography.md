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
python3 scripts/markbank/authoring/geography_cards.py            # write
python3 scripts/markbank/authoring/geography_cards.py --check    # must say "current"
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
priced base tasks, 3,862 carded, 7 held with span-level reasons; 4,146 cards; reconcile 0 orphans; cardlint
clean; every card files under a Topic Atlas heading that covers its syllabus topic; all 754 shipped ids still
resolve (preservation test). Irish (IV) editions stay deferred.

| Sitting | Tasks | Carded | Held | Cards | Companions |
| --- | --- | --- | --- | --- | --- |
| 2014 HL / OL | 103 / 111 | 103 / 111 | 0 / 0 | 110 / 125 | Dungarvan |
| 2013 HL / OL | 104 / 95 | 104 / 95 | 0 / 0 | 111 / 102 | Enniscorthy (aerial stored on its side) |
| 2012 HL / OL | 106 / 108 | 106 / 108 | 0 / 0 | 110 / 115 | Carrick-on-Shannon |
| 2011 HL / OL | 96 / 119 | 94 / 116 | 2 / 3 | 99 / 130 | Dingle (no legend published) |
| 2010 HL / OL | 99 / 102 | 99 / 101 | 0 / 1 | 106 / 113 | Carrick-on-Suir (JPEGs, names swapped) |

Holds (7): 2011 HL Part One Q2(i) and Q2(iii), 2011 OL Part One Q11(i) and the 1A and 7A sketch maps (each needs a
symbol meaning only the never-published 2011 legend gives); 2010 OL Part One Q4 (its answer is only the scheme's
labelled drawing); 2020 OL 9C (27 of 30 marks published; re-examined, no other priced line).

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
- `coverage-baseline.json` exclusions grew 1 -> 7, each accepted with `--accept-regression` after the evidence
  was re-read.

Whole-branch checks at 99eaa387f (23 October): full `npm test` 6,225/6,226 (the one failure is the known
`musicExamTopics` 30 s timeout under load; it passes alone, 21/21), `npm run build` and `npm run lint` pass.
Nothing is merged, deployed or opened as a PR; the branch ships later as one step onto current main
(regenerate `public/assets/landing/ask/topics.json` and `components/landing/subjectShowcase.json` after merging).
