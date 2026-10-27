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
- **An answer the scheme prices is a claimable row, never prose.** The student
  must see the answer and its marks as a button (`6.1 · 3m`), the way a science
  card shows its marking points. Scheme prose is only for examiner directions:
  caps, "accept any valid…", diagram conditions. A rubric criterion whose
  guidance carries `… 6.1 ⟨3m⟩`, `• German — 5 Marks` or `Oifigeach = 2 mharc`
  as text over a slider or dropdown is a defect (Alex, 2026-10-23: "the marking
  scheme answers should always be clear to students, not buried in blocks of
  text"). Where the scheme prices an answer without printing one ("Tectonic
  plate named 3m"), the row shows the scheme's own words and says any correct
  answer scores; it never carries an example the scheme did not print. A point
  row that is only a tariff ("Phase named") or that welds several priced
  answers into one string is the same defect. `test/markBankAnswerClarity.test.ts`
  counts these per subject and must only ever fall. Geography rows come from
  `components/MarkBank/cards/geography/allocation.ts`; French listening,
  reading and cloze rows from `components/MarkBank/cards/french/answers.ts`,
  which cuts the lifted `answerGuide` lines at load time (the JSON stays the
  lifted scheme text). A French card the parser cannot reconcile shows its
  lines as a list, never as paragraphs, over mark buttons. Irish listening
  and reading rows come from `components/MarkBank/cards/irish/answers.ts`,
  which cuts the welded exact guidance at its "= 2 mharc" prices into
  sub-questions and rows; a scheme excerpt that `irish_cards.py` cut short or
  started mid-question cannot reconcile and stays prose, so fix the excerpt,
  not the parser. Politics and Society rows and ladders come from
  `components/MarkBank/cards/politics-and-society/answers.ts`: a quality band
  ("Very good explanation · 8 - 10M") is a row the student places themselves
  on, an exact answer is a claimable row, and the scheme's indicative points
  ("Responses may make reference to") are a visible list labelled as such,
  never a checklist; a sub-part priced in the scheme's margin ("(c) (i) One
  fact 2 marks") is a part of its own, and `corrections.ts` restores, from the
  scheme PDF with its page named, a price line the lifted block lost (the text
  layer gives a margin price its own line, which `politics_author.readable()`
  drops). Physical Education rows come from
  `components/MarkBank/cards/physical-education/answers.ts`, which cuts each
  criterion's reviewed guidance sentence ("Good description: 2; fair
  description: 1.", "Phase named: 1; … good 2, fair 1", "4 marks + 2 marks",
  "Vector.") into bands and rows whose reachable marks must equal the
  criterion's permitted marks; write new PE guidance in those shapes. Art
  2010–2022 components come from `components/MarkBank/cards/art/answers.ts`,
  which makes each printed row a placement at its Marks cell and cuts a
  Notes cell that splits the row ("5 for name, 10 for description &
  discussion", "5 for names (3/2)", "10/10/10" beside printed headings,
  "2 x 5 for functions", "Location - 5 Function - 5") into parts that add
  up to the row; a cell that prices nothing stays a note under the row.
  History Ordinary Level answer lines priced in halves ("Sods (3M) and
  saplings (3M)") are cut at the printed prices by `hist_rows.py`, which
  `hist_all.py` applies to every card it builds and which also upgrades an
  authored `history.json` in place (`--write`); a price that is the whole
  with partials after it becomes one row with printed steps, "Any TWO: …
  (3M + 3M)" an any-two group, and a "5M + 5M Max =" fragment the row's note.
  Construction Studies criterion rows priced in named components ("Design
  feature 1 (2 for point, 4 for discussion)", "Scale - 4 marks Drafting - 4
  marks") carry them as `parts` of the row (`construction_rows.py`): one row,
  several placements, so the five-rows-per-task cap and the yearly
  validators' pinned row lists stand; the pass records every changed card in
  its year's review ledger and changes nothing on a second run.
  Construction Studies drawing rows priced "Any 7 of the above details (5
  marks each)" become option groups (`construction_choices.py --write`): the
  options are the scheme table's own priced detail lines (Higher Level's under
  PERFORMANCE CRITERIA, headed by the part's tariff line), a line the table
  prints twice is a detail drawn twice and stays twice, and the row claims N
  at the unit price for its unchanged marks with the printed tariff as its
  note. The pass mirrors each task's group into its complete-question twin and
  the 2015 Q1 checkpoint draft, records every changed card in its year's
  review ledger, and writes the group into the yearly validator
  (`CHOICES.update`, the LEAF row without steps). A second run finds nothing to
  convert and changes nothing; to re-lift after changing the reader, check out
  the data, the validators and the draft first. 2019 HL Q1(a) ("Any 12 ×
  4marks" over 25 details in three menus) is the one row left as prose: one
  pool, past the 17 options a question may show.
  Italian answers priced in halves on one line ("Erano stati compagni (1m)
  di scuola (4m)", "By summer [2] 2022 [1]") are cut at the printed prices by
  `it_rows.py`, which `it_all.py` applies to every card it builds and which
  also upgrades an authored `italian.json` in place (`--write`); a shorter
  answer the scheme prices under the full one, which was a sentence in the
  row's note, becomes a printed step on a fixed-tariff point row, and a full
  answer the SEC wrapped onto a second line is joined back from the note
  (`it_scheme.py` joins it at the source now too).
  Applied Mathematics cards price their solution in "Published step N"
  allocations beside a crop of the whole solution; `am_steps.py` cuts each
  step's own lines from the scheme page (the band from the step before it to
  its margin mark — "5" in the margin on the 2010–2017 schemes, "(5)" right
  of the working from 2018) and writes the crop region into the allocation
  (`reviewed.json`), so the step shows its content; the equation-editor text
  layer is fragments, never words, so nothing is transcribed. A card whose
  margin marks do not match its steps in number and value keeps the whole
  crop and is listed with its reason in
  `authored/applied-maths-steps-residue.json`.
  Business rubric cards carry the responses the scheme prints for their part
  as `rubric.expected` rows (`bus_expected.py`): the lifter reads the card's
  cited "Possible Responses" / "Support Notes" pages, cuts the block at the
  part's printed marker, drops the echoed question and the page furniture, and
  keeps one item per printed response; what it cannot lift (a marker with no
  response under it, a table the text layer flattened, glyph damage, a block
  that is a whole question) is listed with its pages in
  `authored/business-expected-review.json`, never typed in. `--write`
  rewrites `rubric-authored.json`; a second run changes nothing.
  Irish reading and literature excerpts are re-cut across the scheme pages
  they run onto by `irish_excerpts.py` (`--write` upgrades `authored.json`;
  `irish_cards.py` applies the same pass to every card it builds): a reading
  question whose "(a)" sits on the page before, or whose "N." and "(a)" are on
  different lines, and a literature option that `literature_scheme` cut at
  1,550 characters, each lost their tariff. The literature tariff itself
  ("Príomhthéama = 2 mharc", "Dhá phointe eolais = 4 mharc + 4 mharc", a band
  table under "Tréith 1 = 13 mharc") is cut into rows at load by
  `cards/irish/tariffs.ts`, which also reads the last reading question's
  composite tariff where `answers.ts` cannot.
  Where that text reading leaves a Business card for review, stage B reads the
  cited pages' word positions with PyMuPDF (`bus_expected.py`, the same run):
  a table's rows become items line by line, a tick names the column header
  above it, "True"/"False" in the right-hand column names its statement, a
  numbers row over a letters row pairs them; every word is one the page
  prints (the gate checks word by word, since the text layer holds a table's
  words in another order). What neither reading can lift — a tick table whose
  ticks are drawn, not typed; a marker the page does not print — stays in
  `authored/business-expected-review.json` with both readings' reasons.
  Accounting tasks carry the scheme's priced lines as rows (`acc_rows.py`,
  `cards/accounting/rows.json`): the scheme PDF is read as word lines with
  PyMuPDF and every bracketed mark becomes a row — the figure before it and
  the words that label the line, a mark on its own line taking the figure
  above or below it at the same x, a theory part the unpriced lines after
  its mark, a boxed section no mark follows a block of points; section
  totals (drawn squares, the title's bracketed total, a lone sum of two or
  more parts) are never rows. A task's rows are its heading span when they
  add up to its total, else the question's rows shared out to its tasks in
  paper order; a task they cannot be made to fit, or a grid the geometry
  cannot label, keeps its crop and stepper and is listed with its reason in
  `authored/accounting-rows-residue.json`. The 2022 schemes embed subset
  fonts with no ToUnicode map; `acc_glyphs_2022.py` derives
  `glyphmap-accounting-2022.json` from word evidence (never hand-typed) and
  `acc_rows.py` reads those pages glyph by glyph through it.
- Every newly supported subject must be added to the global deck sample,
  integrity, accessibility, size and preservation guards. A subject-specific
  test alone cannot catch cross-deck duplicates or UI assumptions.
