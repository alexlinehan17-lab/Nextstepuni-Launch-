# Mark Bank authoring — English

English cannot be authored as a list of exact answers. SEC schemes explicitly
treat their material as indicative rather than exhaustive, and most responses
are assessed through PCLM: Purpose, Coherence, Language and Mechanics.

## The card model

Every card contains the exact examination prompt and one of two published
marking modes:

- **Combined PCLM grid** for short responses, where the scheme awards one
  holistic mark from a printed grade band.
- **Discrete PCLM** for longer responses, where P, C and L carry 30% each and M
  carries 10%. Coherence and Language may not score above Purpose.

The marking side separates three things that must never be conflated:

1. **Task requirements** — a checklist that helps the student confirm that all
   parts of the prompt were answered. It carries no marks.
2. **The PCLM rubric** — the only source of the student's mark.
3. **Possible directions** — SEC-derived examples that help reflection, always
   labelled non-exhaustive and never presented as a checklist of required ideas.

This makes open-ended writing self-assessable without pretending that one model
answer is the only valid answer. Exemplar responses can be added later as
annotated calibration material, but must not replace the published rubric.

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

The current ledger contains 630 card units across 20 papers. The first authored
batch is the complete 2025 Higher Level Paper 1: all 19 selectable questions,
including all Question A parts, all Question B choices and all seven composing
choices. The remaining ledger entries stay explicitly queued until their exact
prompt and year-specific scheme rubric have been reviewed.

## Authoring order

Work newest-first while completing one whole paper at a time:

1. 2025 Ordinary Level Paper 1
2. 2025 Higher and Ordinary Level Paper 2
3. 2024 back through 2021, Paper 1 then Paper 2 at each level

No paper is described as complete until every census ID for that paper has a
live card and the one-to-one coverage test passes.
