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

## Elsewhere in the bank — investigated 2026-08-21

Home Economics and Agricultural Science build at **zero drops**. The rest:

    chemistry      720 built, 79 dropped
    physics        807 built, 44 dropped
    biology       1112 built, 53 dropped
    business       575 built,  9 dropped

**95 of those are provenance drops** — 134 marking points that cannot be found
in their own scheme. `provdiag.mjs <subject> <card-id>` shows where each one
stops matching.

### The cause is the scheme markdown, not the cards

I first read the build's "1 marking point" counts as ~41 cheap one-line fixes.
**That was wrong.** Diagnosing them shows one dominant cause: the scheme
markdown flattens TWO-DIMENSIONAL layout into lines, so any marking point that
spans columns or a fraction can never be contiguous.

    Runners (strawberries)        <- the card, correctly pairing method + example
    Method    Runners  Root suckers  Leaflets  Bulbs      <- the scheme, row 1
    examples: (strawberries) (holly bush) ...             <- the scheme, row 2

"Runners" matches and then the scheme continues "rootsuckersleafletsbulbs..." --
the next columns. Same for stacked fractions and isotope notation:
`Kc = [NH3]² / [N2][H2]³` has its numerator and denominator on different lines
with "(c) (i) WRITE:" between them. **70 of the 134 are mathematical.** It is the
same root cause as the Home Economics held tables.

### What was fixed

`foldDigits` in `schemeText.mjs` folded mathematical bold DIGITS but not
mathematical bold LETTERS, so `[𝐍𝐇𝟑]𝟐` normalised to `32` -- the letters were
stripped as punctuation -- and could never match `[NH3]²`. The schemes contain
94 distinct mathematical alphanumeric characters. Folding the whole
U+1D400-U+1D7FF block via NFKD recovered 2 chemistry cards. Correct on
principle regardless: 𝐇 IS H.

### What was NOT done, and why

Mechanical transforms recover only 27 of the 134, and every one of them changes
the marking point: stripping "(strawberries)" from "Runners (strawberries)"
loses the SEC's own example. That is degrading content to satisfy a gate, which
is what the provenance rule exists to prevent. Not done.

### The append was built and measured — it recovers ONE card

`append-scheme-tables.py` exists and works. Run across every scheme whose PDF is
in the repo it appended ~27,000 table cells and recovered **one** card.

The enabler half works: "sublevel: 2p" and "orbital: e.g. 2px" both match
afterwards where neither did before. But the cards that fail do not quote a
cell — they quote a PAIRING the author composed across two cells,
`"sublevel: 2p; orbital: e.g. 2px"`, and only **2 of 133** failing claims are
joins whose every part matches.

So the appends were reverted and the tool kept. Carrying 27,000 machine-written
lines in nine ground-truth scheme files for one card is not a good trade; run it
at the point someone authors those questions, which is when the cells are needed.

### What the remaining ~95 cards actually need

Genuine re-authoring against the scheme: read what the SEC actually printed and
rewrite the marking points so each one is a thing the examiner wrote, rather than
a pairing composed across cells. That is the same work as authoring a paper, for
about 95 cards across four subjects. None of chemistry, physics, biology or
business has authoring scripts, so it would be JSON edits or new scripts.

Two mechanical shortcuts were measured and rejected: stripping parentheticals
and "or"-alternatives recovers 27 of 133 but ALTERS the marking point (dropping
"(strawberries)" loses the SEC's own example), and splitting joins recovers 2.
Degrading content to satisfy the gate is what the provenance rule exists to
prevent.

**Also blocked on missing PDFs for most of it.** Scheme PDFs in the repo cover only
recent years, and the drops are spread across 2021-2025:

    chemistry  2021:10 2022:5 2023:11 2024:18 2025:6   PDFs: 2024, 2025 only
    physics    2021:6  2022:4 2023:1  2024:9  2025:6   PDFs: 2023, 2025 only
    biology    2021:3  2022:7                          PDFs: 2023, 2025 only  -> reaches NONE
    business   2021:1  2023:2 2024:4  2025:1           PDFs: 2024, 2025 only

Roughly 36 of the 95 are reachable without adding PDFs. The rest need the
marking-scheme PDFs for 2021-2023 added first.

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
