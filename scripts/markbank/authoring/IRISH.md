# Irish Mark Bank authoring

Irish is a complete written-paper corpus, not a sample deck. It covers every
independently selectable response on the 2021–2025 Higher and Ordinary Level
papers. Compulsory linked subparts remain on one card. The oral examination and
Foundation Level are outside this corpus.

## Census

| Level | Paper 1 per year | Paper 2 per year | Five-year total |
|---|---:|---:|---:|
| Higher | 17 | 26 | 215 |
| Ordinary | 15 | 22 | 185 |
| **All** |  |  | **400** |

The generated ledger is
`scripts/markbank/authored/irish-census.json`. A successful build must report
20 papers, 400 unique card units, 400 authored and zero queued.
Searchable scheme extracts are generated alongside it in
`examiner-reports/irish/schemes/`; they are the review surface used by the
shared paper/citation guards and must remain in sync with `authored.json`.

## Marking grammar

Irish does not use English PCLM. Cards reproduce the scheme family actually
printed for the response:

- Listening and reading use question-specific exact answers and tariffs.
- Higher composition uses Stíl (5), Ábhar (15) and Cumas Gaeilge (80).
- Ordinary composition uses Tasc (2), Ábhar (8) and Cumas agus Cruinneas
  Gaeilge (40), with the published even-numbered language placements.
- Higher literature awards Eolas (25 or 35) and Gaeilge (5).
- Ordinary literature awards Eolas (25) and applies the printed 0–4 Gaeilge
  deduction. A deduction is never presented as an award.
- Literature supporting points are explicitly non-exhaustive; alternatives are
  judged on their merits.

## Required material

Reading passages and printed poems are attached as page references to the real
Paper Trail PDF. Multi-page texts open in the swipeable source reader. Listening
cards carry the official SEC recording identity and a verified Educateplus
playback mirror; a transcript is never shown because it would reveal answers.

The canonical audio filename is `LC001ZLP017IV.mp3`. The 2021 mirror is split by
Cuid A/B/C; later years use the full annual recording. If a mirror changes,
update playback URLs without changing the SEC identity or card IDs.

## Rebuild and verify

The source PDFs live in `examiner-reports/irish/papers/` and are intentionally
gitignored. Generated data is committed.

```sh
python3 scripts/markbank/authoring/irish_cards.py
python3 scripts/markbank/authoring/irish_cards.py --check
python3 scripts/markbank/authoring/reconcile.py irish --open
python3 scripts/markbank/authoring/reconcile.py irish --baseline check
npm run typecheck
npx vitest run test/markBankIrish.test.ts
```

The generator fails on a missing paper section, a wrong per-paper count, a
duplicate ID, unreconciled marking criteria, an implausibly short prompt, source
page disorder, or question/scheme furniture leaking into a card.
