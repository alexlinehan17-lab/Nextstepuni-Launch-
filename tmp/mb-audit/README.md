# Mark Bank audit, 25 November 2026

The report is `output/markbank-audit-20261125/Mark-Bank-audit-2026-11-25.pdf`.

- `review.html` / `review.tsx`: dev-only page that opens any shipped card in the real session screen
  (`/tmp/mb-audit/review.html?paper=1&subject=biology&level=higher&card=<id>` under `npx vite`).
- `tools/`: the scripts used. They were run from a scratch folder, so paths inside them need adjusting:
  `mb-dump-entry.ts` exports every deck to JSON (bundle with esbuild), `textaudit.py` / `pageshare.py` /
  `pdfcheck.py` are the bank-wide checks, `sample.py` picks the cards, `shoot.mjs` and `stitch.mjs` photograph
  them, `compose.py` builds the review sheets, `build_report.py` + `topdf.mjs` build the PDF.
- `data/`: per-subject statistics, the sampled card list and the card-by-card review notes (`data/reviews/`).

Screenshots are not kept here; regenerate them with the tools.
