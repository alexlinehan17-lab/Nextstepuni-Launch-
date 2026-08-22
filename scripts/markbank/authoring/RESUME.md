# Mark Bank — Home Economics Section C — RESUME NOTE

## Where we are

**Section C is COMPLETE.** It was the last uncovered section in the whole bank,
so every subject now has every section.

  2025 HL  24 cards   2025 OL  25 cards
  2024 HL  28 cards   2024 OL  31 cards
  2023 HL  37 cards   2023 OL  26 cards
  2022 HL  27 cards   2022 OL  25 cards
  2021 HL  27 cards   2021 OL  26 cards

Home Economics builds **569 cards and drops 0** — higher 296, ordinary 273.
Bank total 4684.

## NEXT ACTION

Held is down to **6**, and every one is blocked on something outside the card
model. (It was 27; the rest were recovered by adding the exam papers from Paper
Trail, extracting and inspecting their figures, and re-reading the schemes.)

All 6 are strands the SEC prices and then prints no marking points for.
Shipping them means inventing the detail the examiner declined to print, which
is what the provenance rule exists to prevent. These will not be fixed.

The figure-dependent ones are done: papers came from Paper Trail via
`fetch-paper.mjs`, figures out through `extract-figures.py` /
`crop-question-art.py`, each image inspected, and the verified alt text bound
into `components/MarkBank/figures.json` by `bind-figures.mjs`. The build still
refuses a figure nothing has looked at, so that route is the only one.

## Elsewhere in the bank — reworked 2026-08-22

Every deck now builds, and outside Chemistry every remaining drop is one the
build is RIGHT to make.

    subject               built (HL/OL)   drops   of those, intentional
    home-economics          296 / 273        0    —
    agricultural-science    401 / 389        0    —
    business                267 / 317        0    —
    physics                 409 / 425       17    17 supersessions
    biology                 562 / 581       22    21 supersessions
    chemistry               439 / 325       35    21 supersessions

Bank total **4684**. A "supersession" is a question carded twice, once before a
verified figure existed and once after; the build keeps the one with the figure.

### What the earlier estimate got wrong

This note used to say ~95 cards needed genuine re-authoring, and that the table
append recovered exactly one card. Both were true of the tooling as it stood and
false about the cards. Diagnosing every failure one at a time found FIVE
separate faults in how a scheme is read, not one:

1. **Interleaved columns.** The SEC sets parallel answers side by side and the
   flat extraction reads across the page. `append-scheme-columns.py` reads them
   apart from word coordinates — which reaches the ones `append-scheme-tables.py`
   cannot, because where the two answers share ONE table cell there is no cell
   boundary to split at.
2. **Stacked fractions.** A formula is the one thing a scheme states that is not
   written on a line. `append-scheme-fractions.py` finds the drawn bar and
   splices numerator/denominator back into the line as `num/den`.
3. **Equation-font digits.** The SEC's equation font maps the ten digits into the
   Oriya letter block, so 22.50/187.5 extracts as "ଶଶ.ହ଴ / ଵ଼଻.ହ". Folded as an
   added scheme form in `schemeText.mjs`.
4. **The degree sign**, printed as a superscript letter o ("17oC"), and the **"tt"
   ligature** that one font prints as a single t ("pipete", "atraction").
5. **The deferred paper.** `biology/2023-marking-scheme.pdf` is the DEFERRED
   Higher Level paper — a different exam — and both appenders preferred that name
   over `2023-hl-marking-scheme.pdf`, so its answers were sitting in the main
   paper's scheme text.

Every append is APPEND-ONLY and every fold is an ADDED form, so no card that
passed can start failing. Measured at each step: 0 lost, every time. Folding the
Oriya digits symmetrically inside `normalise()` was tried first and DID cost a
card; that is why it is a form.

The rest were card-side, and each one was checked against the printed scheme:
authors had written out one branch of a slash alternative ("melts if current is
too high" for "melts/breaks if current is too high"), composed a pairing across
two columns that no line of the scheme prints, spelled a symbol out ("Omega",
"½", the letter x for ×), or led a formula with a label the scheme prints
nowhere near it ("Kc = ").

### What is left: 14 Chemistry formulae, and they are not recoverable by text

All 14 are calculations or equilibrium expressions the PDF does not encode
recoverably. The 2023 Higher scheme is the clear case: its equation font's
ToUnicode maps several glyphs to the same codepoint, so "118" extracts as six
copies of MATHEMATICAL BOLD DIGIT ONE and "2.43" as "22.4444". The characters
are simply not in the file — `page.get_text()` recovers some pages and not
others, which is what `append-scheme-maths.py` picks up.

    chem-2021-hl-q6-d        S + O2 -> SO2  ΔH = –296.8 kJ
    chem-2021-hl-q7-d-iv     (1.5 × 10⁻³)² ÷ 0.10 = 2.25 × 10⁻⁵
    chem-2021-hl-q9-c-ii     the ICE table for N2 + 3H2 ⇌ 2NH3
    chem-2021-ol-q10-c-ii    n = m/Ar = 1620/60
    chem-2022-hl-q5-d        218/84 Po        (isotope notation, no drawn bar)
    chem-2022-hl-q11-a-v-vi  Mn2+ -> +2 (II) and MnO4– -> +7 (VII)
    chem-2023-hl-q7-b-ii     pH = –log√(Ka[HA])
    chem-2023-hl-q9-b-i      Kc = [PCl5] / ([PCl3][Cl2])
    chem-2023-hl-q10-b-ii    1.77/(14n + 90) moles (CH2)n(COOH)2
    chem-2023-hl-q10-b-iii   1.77/(14n + 90) = 2.43/(14n + 134)
    chem-2023-hl-q10-b-iv    0.03 = (0.12 × V)/1000 ⇒ V = 250 cm³
    chem-2023-hl-q10-c-iii   ¹³¹₅₄Xe          (isotope notation, no drawn bar)
    chem-2023-hl-q11-a-ii    pV = nRT ⇒ V/T = nR/p = constant
    chem-2023-ol-q11-b-ii    [NH3]^2 over [N2][H2]^3

Shipping them means typing a formula off a rendered image, which is the
hand-transcribed path both historical figure corruptions came through. If they
are worth having, do it the way figures are done: render the equation's region,
have something LOOK at it, and record the reading with the page and an image
hash, so the transcription is auditable rather than assumed.

### The tools, and when to run them

Each appends its own marked block to `examiner-reports/<subject>/schemes/*.md`
and is idempotent — re-running replaces the block.

    append-scheme-tables.py      cells from find_tables(), and column runs joined
    append-scheme-columns.py     columns read apart from word coordinates
    append-scheme-fractions.py   stacked fractions spliced back into their line
    append-scheme-maths.py       equation pages re-read the plain way
    fetch-paper.mjs              pull a paper or scheme out of Paper Trail
    provdiag.mjs                 where a claim stops matching, and the raw wording
    suggest-verbatim.mjs         propose the scheme's own slash-alternative form

Run all four appenders with `--all` after adding any scheme PDF.

### One deliberate drop

`bio-2025-hl-q9-b-ii`. Strip its content-free row and what remains is a single
3-mark point on a question asking for a whole 21-mark activity, which would
teach a student to under-answer. Q9(a) and Q9(b)(i) carry that experiment.

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
