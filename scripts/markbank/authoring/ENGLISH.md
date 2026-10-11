# Mark Bank authoring — English

English cannot be authored as a list of exact answers. SEC schemes explicitly
treat their material as indicative rather than exhaustive, and most responses
are assessed through PCLM: Purpose, Coherence, Language and Mechanics.

## The card model

Every card contains the exact examination prompt and one of three published
marking modes:

- **Combined PCLM grid** for short responses, where the scheme awards one
  holistic mark from a printed grade band.
- **Discrete PCLM** for longer responses, normally P/C/L at 30% each and M at
  10%. The 2021–2022 Ordinary Single Text 35-mark responses instead use the
  published 11/11/11/2 allocation. Apply that year's published grading rules:
  the modern Coherence/Language cap at Purpose must not be projected backwards.
  For example, the 2011–2012 Ordinary schemes cap Language at the top of D
  only when both Purpose and Coherence fail D, and assess Mechanics independently.
  Historical grade bands and rounding also differ from modern H/O bands.
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

Comprehension Question A parts receive their text's reader by default. When a
part is self-contained (for example 2016 OL Text 1 A(iii)(b), a trip of the
candidate's own, or Text 3 A(iii)(a), their own First Year diary) and the scheme
requires no reference to the text, record a `kind: not-required` entry in
`english-source-review.json`. It binds the paper hash, the question wording and
the exact default reader it removes (`excludedSource` label, title and pages),
with a written reason. The extractor refuses an exclusion whose inputs no longer
match, and the task-review hash covers the missing reader, so deleting the
exclusion later makes that scheme review stale.

When a question explicitly names other studied poems absent from the paper,
an attributed reading edition may use `kind: supplementary-text`, empty PDF
`pages`, and `texts` with the edition, source URL, and verified stanza/line
breaks. Keep this separate from SEC print: identify it as supplementary reading,
explain that it is absent from the examination, and record edition evidence in
the source-review ledger. Only reproduce works for which reproduction is
permitted. Never substitute a different printed poem merely because it shares
the question's section heading or poet.

For works that cannot be reproduced in the app, `kind: linked-reading` provides
attributed, page-specific links to verified reading copies on their publishers'
sites. Use empty PDF `pages` and `readings` containing title, author, edition,
location and HTTPS `sourceUrl`. Label these as other studied poems absent from
the examination; the links explicitly open in a new tab. Record document hashes,
verified PDF pages and permission acknowledgements in the source-review ledger.
Do not copy the poem into the app or attempt to bypass a site's embedding rules.

## What counts as one card

A card represents every independently selectable response opportunity printed
on a paper. A student should never have to answer one card in order to reveal a
different choice. A compulsory prompt with tightly linked printed subparts may
remain one card; those subparts are recorded in `printedParts` so none can
silently disappear.

`english_census.py` is the legacy 2021–2025 ledger, not the full English
denominator. Paper Trail currently holds **68 papers across 2010–2026**.
`english_complete.py` inventories those exact indexed documents and pins their
PDF hashes in `english-paper-inventory.json`. The complete-corpus work is tracked
in `docs/english-completion-RESUME.md`.

```bash
python3 scripts/markbank/authoring/english_census.py
python3 scripts/markbank/authoring/english_census.py --check
python3 scripts/markbank/authoring/reconcile.py english --open
```

The legacy ledger contains 660 entries across 20 papers, represented by 650
canonical runtime cards (210 Higher, 440 Ordinary) after ten recorded aliases.
It bundles separately marked tasks and does not expand every internal finite
choice. These counts must not be used to claim completeness.

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

Completion requires a visual paper sweep, scheme-checked task boundaries,
all finite routes, verified source material, and exact Mark Bank/Topic Atlas
parity. Agreement between a parser and its own census is not independent proof.

The full-corpus pipeline keeps its output outside the runtime until
`english_review_gate.check(tasks, strict=True)` passes. The gate reconciles
source-bound choices, a separate raw-PDF directive scan, exact task/scheme
evidence, every-page visual sweeps and independent task/route tallies. Any
`openFindings` in the visual ledger also block publication.

`english-task-context.json` records verified instructions that lie outside a
numbered task, including shared section instructions and cross-question
dependencies. These bind both question wording and paper hashes. Carry their
notes, each task's parent stem, sources, and criteria into every split or
expanded route. Preserve legacy bundled card IDs while adding the separately
practicable tasks required by the repository's corpus rules.

## Publishing reviewed papers (paper by paper)

`english_publish.py` is the runtime publisher for the full corpus. A paper is
published only when its OWN strict gate passes
(`english_review_gate.check_paper`): the paper's visual ledger entry, every one
of its tasks scheme-reviewed against current hashes, zero pending selections,
every raw directive on that paper classified, and no orphaned context. The
corpus-wide gate may still refuse because of other years; that never blocks a
reviewed paper and never lets an unreviewed one through.

```bash
python3 scripts/markbank/authoring/english_publish.py          # regenerate
python3 scripts/markbank/authoring/english_publish.py --check  # CI-style staleness check
node scripts/paper-trail/build-english-geography-exam-topic-runtime.mjs  # after new archive topics
```

- Output: `components/MarkBank/cards/english/published-{higher,ordinary}.json`.
  Card id = reviewed task id, or route id for a finite printed pool (the
  parent is then not a card). Every route keeps the parent tariff, reader,
  context and reviewed scheme pages.
- Legacy 2021-2025 cards stay in `authored.json` and are untouched. A legacy
  paper is refused until `english-legacy-bridge.json` maps every legacy card
  of that paper to a reviewed id (keeping the legacy id or recording a
  progress alias). Reviewed companion readers of legacy leaves are aggregated
  onto their bundled parent (`legacyAdditionalSources`).
- Grids and caps: `scripts/markbank/authored/english-marking-grids.json` is an
  exact transcription of each printed grid (2010-2016 HL A+..E-, 2010-2016 OL
  A..F/NG with its printed overlaps and the 10-mark F/NG 1, 2018 and 2026
  H1-H8/O1-O8) and of each year's cap rule (2010-2015 HL none; 2010-2015 OL
  Language capped at the top of D only when both P and C are below D; 2016,
  2018 HL and 2026 C/L <= P; 2018 OL none printed). The publisher refuses a
  grid whose cells are not printed on the bound scheme page.
- Topic Atlas: the publisher also writes additive archive topics for
  canonical nodes the reference menu lacks and exact booklet links for every
  published sidecar block (`data/examTopics/english-reviewed-*.json`); the
  registry unions them in and never replaces an existing mapping.
- Coverage: the English ledger = legacy census + published papers + every
  other non-legacy paper declared open (candidate tasks, labelled unreviewed).
