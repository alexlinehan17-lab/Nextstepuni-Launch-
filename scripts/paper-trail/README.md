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
| 2.5 Anchor maps | `anchor-map.py` | `answers/<year>/<fileid>.json` (committed), `out/answers-manifest.jsonl`, `out/answers-report.md` |
| 3. Index     | `build-index.py` | `paperTrailData.ts`, `out/index-report.md`, `out/upload-manifest.jsonl`, `out/answers-upload-manifest.jsonl` |
| 4. Upload    | `upload.py`    | `gs://nextstepuni-app.firebasestorage.app/papers/**` (PDFs + answer sidecars) |

All stages are resume-safe and idempotent. Stage 1–2 are polite: single-thread,
~1.6s delay, exponential backoff, identifying User-Agent with contact address.

## "See the answer" — per-question answer maps (Stage 2.5)

`anchor-map.py` precomputes, per in-scope paper, a coordinates-only sidecar that
lets the viewer drop a CROP of the real marking-scheme region beside each
question (see `ANSWERS_PLAN.md` for the full design). It ships NO answer text and
NO image bytes — only page numbers + fractional rects. Sidecars are **committed**
generated artifacts (CI/deploy have no corpus), at `scripts/paper-trail/answers/`.

Scope is the per-subject **MARKER GRAMMAR** table in `anchor-map.py` (`GRAMMAR`),
keyed by `(subjectCode, language)`. Adding a subject = adding a table row + a
contact-sheet review, never a code change. Current pilot: Leaving Cert
Mathematics Higher Level, Paper 1 + 2, 2022–2025 EV.

The `answers:1` flag (which makes the viewer toggle appear) is gated TWICE:
`anchor-map.py` must have mapped the paper, AND its `(subjectId, level, lang)`
profile must be listed in `QA_PASSED_ANSWER_PROFILES` in `build-index.py`. That
set is empty until a human signs off the contact sheet — so the machinery can be
merged dark and lit per-profile later.

**Phase 5 QA gate (per grammar profile, before lighting it):**
1. `python3 anchor-map.py` → check `out/answers-report.md` is all FULL/PARTIAL, 0 dropped.
2. `python3 test_anchor_map.py` → the deterministic gate (Q1→one anchor, regions in-band, fractions ∈ [0,1]).
3. `python3 contact-sheet.py` → `out/contact-sheet.pdf`; a human confirms each paper question lines up with its scheme crop (esp. that P1 and P2 pull DIFFERENT bands of the shared scheme).
4. On sign-off, add the profile to `QA_PASSED_ANSWER_PROFILES`, re-run `build-index.py`, commit, `upload.py`, deploy.

## Annual refresh (each autumn, when the new year's papers publish)

1. Add the new year to `YEARS` in `enumerate.py`.
2. Run stages 1→4 in order (1–2 take a few hours; run overnight). Stage 2.5
   (`anchor-map.py`) runs after download, before index — add the new year to
   `SCOPE_YEARS` if answer maps should cover it.
3. `npx vitest run` (index integrity + JC guards + answer-sidecar integrity),
   commit `paperTrailData.ts` + any new `answers/` sidecars,
   `firebase deploy --only hosting`.
4. Canary: if stage 1 finds zero files for the new year, the SEC's form/URL
   scheme may have changed — check `enumerate.py`'s field names against the
   live form before assuming the year isn't published.
5. **Answer-map canary (the grammar-drift guard):** after Stage 2.5, check
   `out/answers-report.md`. If a subject-grammar profile that previously mapped
   cleanly now shows **0 anchors / DROP** for the new year, the SEC changed that
   subject's scheme layout — investigate and re-verify a contact sheet BEFORE the
   new year's `answers` flags ship. Do not auto-extend a profile to a year that
   tripped the canary. Marker counts alone don't catch a layout whose anchors
   merely shifted, so the contact-sheet spot-check for at least one new year per
   profile stays part of the refresh.

6. **Never ship `--fallback` output.** The universal navigation fallback in
   `anchor-map.py` places chips by PROPORTIONAL page position (`idx*apages//N`),
   not by matching scheme markers. The 2026 audit rendered all 64 fallback
   sidecars it produced and deleted every one: combined P1+P2 schemes (Maths IV),
   topic-organised schemes (History OL), descriptor-band schemes (Art, Applied
   Maths project), restructured new-spec schemes (Biology HL Q6 jumped to the
   scheme's Q12; Economics), section-restart papers (LCA Italian, Mandarin) and
   passage-paragraph-numbered languages all mis-navigate, and a 3-chip sample
   can never validate the unsampled chips of a proportional guess. The flag
   pipeline ships fallback sidecars UNGATED (`answers:1` without a QA profile),
   so a fallback run silently publishes wrong navigation. Use `--fallback` only
   for local experiments; delete its output before `build-index.py`.

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
