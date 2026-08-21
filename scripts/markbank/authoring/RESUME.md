# Mark Bank — Home Economics Section C — RESUME NOTE

## Where we are

**Section C is COMPLETE.** It was the last uncovered section in the whole bank,
so every subject now has every section.

  2025 HL  24 cards   2025 OL  25 cards
  2024 HL  28 cards   2024 OL  31 cards
  2023 HL  37 cards   2023 OL  26 cards
  2022 HL  27 cards   2022 OL  25 cards
  2021 HL  27 cards   2021 OL  26 cards

Bank total 4544. Home Economics: 542 cards built, higher deck 282, ordinary 260.
Held 27.

## NEXT ACTION

Home Economics now builds **553 cards and drops 0**. Held is down to 21, and
every one of those is blocked on something outside the card model:

**13 need a figure from the exam paper** (outfit photographs, a kitchen floor
plan, a bathroom photograph). Blocked on missing source material: the repo has
Home Economics MARKING SCHEMES only, no exam-paper PDFs, and
`public/exam-figures/home-economics-s-and-s/` holds 15 charts and care symbols,
none of which are these. To ship them someone must add the HE exam papers
(2021-2025, HL and OL), then `extract-figures.py`, inspect each image, write
verified alt text into `components/MarkBank/figures.json`, and attach
`figureKey`. The alt text has to be written by something that actually looked at
the image -- the build refuses a figure that has not been inspected.

**5 have no marking points to ship.** The scheme prices a strand and then prints
nothing for it. Shipping these means inventing the detail the examiner declined
to print, which the provenance rule exists to prevent. These will not be fixed.

**3 are corrupted table extractions.** `he-2025-hl-sb-q3a` was investigated on
2026-08-21: the PDF table extracts cleanly, but the provenance gate reads the
scheme MARKDOWN, which interleaves the columns, so half the cells are not
contiguous. It needs the scheme re-extracted with table awareness -- a change
that touches every card built from that file. The other two are 2022 and 2023,
whose scheme PDFs are not in the repo at all.

## Elsewhere in the bank — NOT Home Economics

Home Economics is the only subject at zero drops. As of 2026-08-21:

    business       575 built,  9 dropped
    chemistry      718 built, 81 dropped
    physics        807 built, 44 dropped
    biology       1112 built, 53 dropped
    agricultural   790 built,  0 dropped

Some of those are deliberate ("superseded by a card carrying its figure"), but
**88 are provenance failures** -- marking points that cannot be found in their
own scheme -- plus unverified figure alt text, content-free rows and
too-short question text. `provcheck.mjs` is the tool for the provenance ones.
Nobody has looked at these.

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
