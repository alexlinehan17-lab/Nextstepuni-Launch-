# Mark Bank authoring toolkit — Home Economics

The scripts that produced the Home Economics cards in
`scripts/markbank/authored/`. They live here rather than in a scratch directory
because Section C is a multi-session job and each paper's slicing decisions are
worth keeping: every option is cut out of the marking scheme by anchor, so the
script *is* the record of where each marking point came from.

Every script is reproducible — re-running one emits the same cards that are in
the deck today. That is asserted by `test/markBankAuthoringToolkit.test.ts`.

## Files

| File | What it does |
|---|---|
| `he_lib.py` | Shared helpers: `load`, `block`, `heads`, `semis`, `anyN`, `card`, `audit`, `emit` |
| `scout.py` | `python3 scout.py <year> <higher\|ordinary>` — prints Section C bounds and the question map |
| `rebaseline.py` | Verifies no card ID vanished, then updates the preservation baseline. Refuses on loss |
| `provcheck.mjs` | `node provcheck.mjs /tmp/out.json` — runs the build's provenance gate on a script's output *before* merging |
| `econ_refcheck.py` | Checks every Economics **citation** against the question paper. The provenance gate checks what a card claims; this checks which question it says it came from |
| `econ_refs.py` | The nineteen citations the paper corrected, and the cards the checker cannot place, each read by hand |
| `econ_parts.py` | Segments a scheme into parts, reads each tariff, splits the responses. Output is candidates, never cards |
| `econ_auto.py` | `Paper(year, level, section).menu(...)` — one card per call, against `econ_parts` |
| `econ_all.py` | Runs every `econ_<year>_<level>[_secA].py` and writes `authored/economics.json`. Refuses on a duplicate id |
| `he_<year>_<level>_secC.py` | One Section C paper each |
| `he_<year>_<level>.py` | The earlier Section A/B papers |
| `RESUME.md` | Current state and the next action |

## Two gates, two documents

A card makes two kinds of claim, and each is checked against a different
document.

- **What it says the examiner accepts** is checked against the marking scheme,
  by `provcheck.mjs`. Every marking point must appear in its own scheme,
  contiguously, after normalisation.
- **Which question it came from** is checked against the QUESTION PAPER, by
  `econ_refcheck.py`. It has to be the other document: the scheme is a table
  flattened into one long line, and the question number a part sits under is
  exactly what that flattening loses. A question number printed at the foot of
  one page comes back as more parts of the question before it — which is how
  nineteen shipped cards came to cite a question they were not from while every
  one of their claims still traced, because the claims came from the right block
  of text.

Papers live in `examiner-reports/economics/papers/<year>-<hl|ol>-paper.pdf`.

## Why the guards exist

Each one is here because it caught a real bug that would otherwise have shipped:

- **`heads()` rejects non-increasing anchors.** A bare `age` anchor matched
  inside `mortgage`, which emptied one option and filled the next with the wrong
  text.
- **`block()` rejects an ambiguous start anchor.** A heading almost always
  appears twice — once in the question's bullet list, once over the marking
  points — and taking the first match silently returned the question text plus
  everything after it. That is what made four fibre cards show 14 options each.
- **`semis()` strips `etc.` from both ends and drops page furniture.** The
  examiner uses `etc.` mid-list to close one cluster and open another, which was
  prefixing the next marking point with `etc.`; and a running page footer once
  reached a card as a student-facing marking point.

## The loop, per paper

```bash
python3 scripts/markbank/authoring/scout.py 2022 higher     # bounds + question map
python3 scripts/markbank/authoring/he_2022_hl_secC.py > /tmp/out.json   # AUDIT lines on stderr must be silent
node scripts/markbank/authoring/provcheck.mjs /tmp/out.json             # must be 0 untraceable
# merge into scripts/markbank/authored/home-economics.json
node scripts/markbank/build-deck.mjs scripts/markbank/authored/home-economics.json
python3 scripts/markbank/authoring/rebaseline.py home-economics
npm run lint && npm run typecheck && npm test && npm run build
```

## Rules that matter

- Option text is **sliced from the scheme, never retyped** — the build's
  provenance gate requires every option to appear in its own scheme, and both
  historical scheme corruptions in this repo came from hand transcription.
- **Non-`anyN` rows have their `verbatim` provenance-checked.** Only an `anyN`
  row's verbatim is free, so any invented row label must be an `anyN` row.
- Option cap is **14** for Section C. Over that, take the list in scheme order.
- Where the examiner prints N parallel accounts (fibres, milk heat treatments,
  cooking methods, packaging materials), author **one card per account** with its
  own `questionRef` — never pool them into one menu.
- Where a strand has no marking points at all, ship the strand that does and
  **hold** the other, recording the marks it accounts for.
- Figure-dependent parts are **held**, not shipped blind.

## Cross-subject card-boundary and presentation rules

These rules apply to every subject, including decks produced by older or
subject-specific generators.

- A card may cover only **one independently practicable printed task**. Do not
  merge a neighbouring roman, lettered part, practical-project rubric,
  companion booklet, or later question merely because PDF extraction placed
  their text in one block.
- Preserve the complete parent path in `questionRef` (`Q4(a)(ii)`, not
  `Q4(ii)`). A roman-only citation is ambiguous and can make the source audit
  match the wrong task.
- When the official extract, photograph, map, graph, table, tick-box layout,
  code listing, or diagram is needed to answer, attach an inspected source page
  or crop. Keep `questionText` to the actual ask; do not also flatten the
  attached source into a long, visually broken paragraph.
- A crop is not accepted because it exists or hashes successfully. Open the
  generated image and verify that it includes all required shared context,
  excludes adjacent asks and answer furniture, and remains legible at phone
  width.
- One printed ask has one stable card identity. Exact repeated asks are
  withdrawn through the correction/alias ledger so saved progress migrates;
  finite legitimate answer routes belong in `answerVariants`, not duplicate
  cards.
- Theory-paper, practical-project and companion-booklet boundaries are hard
  boundaries. Confirm the paper component before importing marks or criteria;
  never infer a shared question number means shared content.
- Compact long rubrics by grouping parallel, compulsory checks into bounded
  rows. Do not change their total, optionality or route tariff to meet a visual
  row cap.
- Every newly supported subject must be added to the global deck sample,
  integrity, accessibility, size and preservation guards. A subject-specific
  test alone cannot catch cross-deck duplicates or UI assumptions.
