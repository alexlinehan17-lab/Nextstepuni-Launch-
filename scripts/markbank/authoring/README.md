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
| `he_<year>_<level>_secC.py` | One Section C paper each |
| `he_<year>_<level>.py` | The earlier Section A/B papers |
| `RESUME.md` | Current state and the next action |

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
