# Mark Bank authoring — English

English cannot be authored as a list of exact answers. SEC schemes explicitly
treat their material as indicative rather than exhaustive, and most responses
are assessed through PCLM: Purpose, Coherence, Language and Mechanics.

## The card model

Every card contains the exact examination prompt and one of three published
marking modes:

- **Combined PCLM grid** for short responses, where the scheme awards one
  holistic mark from a printed grade band.
- **Discrete PCLM** for longer responses, where P, C and L carry 30% each and M
  carries 10%. Coherence and Language may not score above Purpose.
- **Composite PCLM** for linked compulsory parts that receive separate grids.
  Components can be combined or discrete — for example an Ordinary Level
  Comparative card uses two 15-mark combined grids followed by one 40-mark
  discrete grid. The card stays together, but each part is placed and totalled
  on its own published tariff.

The marking side separates three things that must never be conflated:

1. **Task requirements** — a checklist that helps the student confirm that all
   parts of the prompt were answered. It carries no marks.
2. **The PCLM rubric** — the only source of the student's mark.
3. **Possible directions** — SEC-derived examples that help reflection, always
   labelled non-exhaustive and never presented as a checklist of required ideas.

This makes open-ended writing self-assessable without pretending that one model
answer is the only valid answer. Exemplar responses can be added later as
annotated calibration material, but must not replace the published rubric.

## Required source material

A prompt that says the response must be based on, supported by, or developed
from a printed text is not a complete card until that text is available before
the scheme reveal. Add `sourceMaterial` with:

- the paper's own source label and title;
- every one-based PDF page the source spans, in reading order; and
- the concise author/publication introduction printed with the source.

The source reader renders those pages directly from Paper Trail's verified
question-paper PDF. Do not retype the passage, manufacture a facsimile, point at
the marking scheme, or add raster copies to the app bundle. Resolve
`paperFileid` from the Paper Trail index and verify the pages visually against
the local authoring PDF.

Do not attach a long source merely because a self-contained writing prompt
mentions its theme or includes a quotation from it. The test is whether a
student needs to read the source to answer the exact task faithfully. This keeps
Question B and composing cards focused while guaranteeing that every direct
comprehension, unseen-poetry or other source-dependent ask is actually usable.

## What counts as one card

A card represents every independently selectable response opportunity printed
on a paper. A student should never have to answer one card in order to reveal a
different choice. A compulsory prompt with tightly linked printed subparts may
remain one card; those subparts are recorded in `printedParts` so none can
silently disappear.

`english_census.py` reads all 2021–2025 Higher and Ordinary Level Paper 1 and
Paper 2 question papers and creates the authoritative coverage ledger at
`scripts/markbank/authored/english-census.json`. It never derives question
coverage from a marking scheme.

```bash
python3 scripts/markbank/authoring/english_census.py
python3 scripts/markbank/authoring/english_census.py --check
python3 scripts/markbank/authoring/reconcile.py english --open
```

The current ledger contains 660 card units across 20 papers. Every unit has a
live PCLM card: 210 Higher Level and 450 Ordinary Level. The total includes all
Question A parts, all Question B and composing choices, every Single Text and
Comparative option, both unseen-poetry routes, and every printed prescribed-
poetry choice. Ordinary Level prescribed poetry is counted as one linked Q1
card for its compulsory (a)/(b) parts plus three separate Q2 alternatives.

`english_cards.py` extracts every prompt from the question paper, maps required
source pages, and traces the wording to its own year's marking scheme before it
writes the committed runtime manifest:

```bash
python3 scripts/markbank/authoring/english_cards.py
python3 scripts/markbank/authoring/english_cards.py --check
```

## Authoring order

The corpus was reviewed newest-first, completing one whole paper at a time:

1. 2025 Ordinary Level Paper 1
2. 2025 Higher and Ordinary Level Paper 2
3. 2024 back through 2021, Paper 1 then Paper 2 at each level

No paper is described as complete unless every census ID for that paper has a
live card and the one-to-one coverage test passes.
