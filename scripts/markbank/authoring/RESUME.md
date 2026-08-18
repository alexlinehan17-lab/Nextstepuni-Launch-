# Mark Bank — Home Economics Section C — RESUME NOTE

## Where we are
Section C was the last uncovered section in the whole bank (every other subject
already had all its sections). Working paper by paper, newest first.

DONE and pushed:
  2025 HL  24 cards   2025 OL  25 cards
  2024 HL  28 cards   2024 OL  31 cards
  2023 HL  37 cards   2023 OL  11 cards  <-- PARTIAL: Electives 1 and 2 only
Bank total 4424. 422 HE cards built (228 higher / 194 ordinary), 21 held.

## NEXT ACTION
Finish 2023 OL: Elective 3 and Question 4 (Core). Script to extend:
  scratchpad/he_2023_ol_secC.py   (append before the final emit(cards) block)
Scheme bounds already worked out:  SEC = tidy(T[22298:43193])

Cards still to author for 2023 OL (all read from the scheme, notes below):
  q3ai   (6)  Define unemployment              2 @ 3, flat (4 opts)
  q3aii  (24) Effects of unemployment          3 rows @ 8 (individual/family/society, 2 @ 4 each)
  q3aiii (12) Role of education for work       3 @ 4, flat
  q3aiv-name (4) Statutory scheme NAME only    -- HOLD the 4-mark details strand,
                 the scheme prints names and no marking points for the detail
  q3bi   (15) Primary school + development     3 @ 5, bundles: physical/emotional/intellectual/social
  q3bii  (15) Factors in educational achievement 3 @ 5, flat (cap 14)
  q3ci   (15) Social/economic change           3 rows @ 5 (three named headings)
  q3cii  (15) Benefits of voluntary work       3 @ 5, flat
  q4ai   (20) Osteoporosis causes/effects      fixed 3 rows (5 / 5 / 10 floating)
  q4aii  (15) Preventing osteoporosis          3 @ 5, pool lifestyle+dietary
  q4aiii (15) Food labelling + special diets   3 @ 5, flat
  q4bi   (15) Factors affecting household income 3 @ 5, bundles: age/gender/social class/
                 lower socio-economic group/cultural factors
  q4bii  (15) Benefits of a budget plan        3 @ 5, flat
  q4ci   (15) Changing role of the adolescent  3 @ 5, flat
  q4cii  (15) Family and child development     3 @ 5, pool physical+emotional

Then the remaining papers, same rhythm: 2022 HL, 2022 OL, 2021 HL, 2021 OL.

## The loop, per paper
1. python3 scratchpad/scout.py <year> <higher|ordinary>   -> Section C bounds + question map
2. Read each elective with he_lib.block(), author into scratchpad/he_<year>_<lvl>_secC.py
3. Run it; emit() prints AUDIT lines to stderr - must be silent
4. Merge into scripts/markbank/authored/home-economics.json (+ -held.json)
5. node scripts/markbank/build-deck.mjs scripts/markbank/authored/home-economics.json
   -- every new card must build; only the 5 legacy Section A drops are expected
6. python3 scratchpad/rebaseline.py home-economics   -- refuses if any ID vanished
7. npm run lint && npm run typecheck && npm test && npm run build
8. Commit + push

## Conventions that matter
- Option text is always SLICED from the scheme, never retyped (provenance gate).
- NON-anyN rows have their verbatim provenance-checked; anyN verbatim is free.
  So any invented row label must be an anyN row.
- Option cap is 14 for Section C. "One flat list, taken in order to the cap."
- Where the examiner prints N parallel accounts (fibres, milk heat treatments,
  cooking methods, packaging materials), author ONE CARD PER account with its
  own questionRef -- never pool them into one menu.
- Where a strand has no marking points at all, ship the strand that does have
  them as its own card and HOLD the other, recording the marks it accounts for.
- Figure-dependent parts (outfit/room photos) are HELD, not shipped blind.
- he_lib guards now in place: heads() rejects non-increasing anchors,
  block() rejects an ambiguous start anchor, semis() strips leading/trailing
  "etc." and drops page furniture / "Accept ..." examiner notes.

## Known pre-existing issue, NOT caused by this work
5 Section A cards are dropped by the build every run and always have been:
  he-2025-hl-sa-q8    rows sum to 8, tariff is 6
  he-2025-ol-sa-q8/q10/q11/q12   row offers Nx2 on a 6-mark question
Worth fixing separately - they are real tariff errors in older authoring.
