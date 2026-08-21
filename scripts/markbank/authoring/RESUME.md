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
Nothing outstanding on Section C. Two things remain worth doing, both
pre-existing and neither caused by this work:

1. **5 Section A cards drop on every build** and always have. They are real
   tariff errors in older authoring, not extraction problems:
       he-2025-hl-sa-q8              rows sum to 8, tariff is 6
       he-2025-ol-sa-q8/q10/q11/q12  row offers Nx2 on a 6-mark question
   Fixing them is a small, self-contained job.

2. **27 held cards** across the bank, listed in
   `scripts/markbank/authored/home-economics-held.json` with a `heldReason`
   each. Most need a figure the markdown extraction does not carry (room
   photographs, outfit photographs, floor plans). A few are strands the scheme
   prices but prints no marking points for. They would need the figures adding
   before they could ship.

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
