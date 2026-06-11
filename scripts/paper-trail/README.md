# Paper Trail pipeline

One-time mirror of the SEC Exam Material Archive → Firebase Storage, plus the
generated in-app index. See compliance/SEC_ARCHIVE_TERMS_2026-06-11.md for the
terms-of-use record and compliance/SEC_COURTESY_EMAIL_DRAFT.md for the
notification sent to the SEC.

## Stages

| stage | script | output |
|---|---|---|
| 1. Enumerate | `enumerate.py` | `out/manifest.jsonl` (authoritative archive catalogue) |
| 2. Download  | `download.py`  | `paper-trail-corpus/` (gitignored), `out/downloads.jsonl` |
| 3. Index     | `build-index.py` | `paperTrailData.ts`, `out/index-report.md`, `out/upload-manifest.jsonl` |
| 4. Upload    | `upload.py`    | `gs://nextstepuni-app.firebasestorage.app/papers/**` |

All stages are resume-safe and idempotent. Stage 1–2 are polite: single-thread,
~1.6s delay, exponential backoff, identifying User-Agent with contact address.

## Annual refresh (each autumn, when the new year's papers publish)

1. Add the new year to `YEARS` in `enumerate.py`.
2. Run stages 1→4 in order (1–2 take a few hours; run overnight).
3. `npx vitest run` (index integrity + JC guards), commit `paperTrailData.ts`,
   `firebase deploy --only hosting`.
4. Canary: if stage 1 finds zero files for the new year, the SEC's form/URL
   scheme may have changed — check `enumerate.py`'s field names against the
   live form before assuming the year isn't published.

Note: current-year files upload with `max-age=86400` (SEC occasionally
re-issues schemes); when a year stops being current, the next refresh re-uploads
it under the immutable policy.

## Cost guard / kill switch

- Budget: "NextStepUni monthly guard", €50/month on billing account
  0138B2-5E7F8E-0CED30, email alerts at 50% / 90% / 100%
  (created 2026-06-11; realistic monthly spend is €1–2 — an alert means abuse).
- Kill switch if egress is being abused: make the corpus private —

      firebase deploy --only storage   # after setting papers/** read to false

  in storage.rules (`allow read: if false;`). The app degrades gracefully
  (viewer shows its error state with "open in browser"); nothing else breaks.
