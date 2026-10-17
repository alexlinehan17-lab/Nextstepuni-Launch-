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
Never run two stages that fetch from examinations.ie at the same time.

## Scope (since 2026-10-17)

`enumerate.py` `SCOPE` walks four archive views:

| view | exams | years |
|---|---|---|
| `exampapers` | LC, LCA | 1995–2026 (the archive's full year list) |
| `markingschemes` | LC, LCA | 2001–2026 (no schemes are published before 2001) |
| `exampapers` / `markingschemes` | JC | 2017–2026 minus 2020/2021; new-spec filter at decode |
| `deferredexams` / `deferredmarkingschemes` | LC (LCA and JC probed: empty) | 2022–2025 |

Deliberately out: **Junior Certificate before 2017** (the old Junior Certificate,
a different programme from the new Junior Cycle), audio/video (`.mp3/.mov/.mp4/.avi`),
and the Senior Cycle *Additional Assessment Component* sample briefs (coursework, not papers).

- **Deferred sitting.** The SEC reuses the June fileid for the deferred paper of
  the same year (`LC032ALP000EV.pdf` is both). The corpus keeps the SEC name under
  `paper-trail-corpus/deferred{exams,markingschemes}/<year>/`; the INDEX and Storage
  name is `<fileid stem>-deferred.<ext>` (`build-index.py` `sitting_doc_id`), so
  every year+fileid identity in the app — Storage path, recents/pins, deep links,
  answer sidecars, hosted anchors, topic tags — stays distinct. Deferred papers
  pair only with deferred schemes (the sitting is part of the pairing key), are
  listed after the June papers in the same year entry with labels
  `Deferred · …`, and never carry `answers:1`.
- **Sample papers.** Specifications not yet examined have no archive rows. The SEC
  publishes their sample papers on `https://www.examinations.ie/scr/` (one fragment
  per subject code, e.g. `scr/571.php`). `sample-papers.json` is the curated list
  (source page per row); `download_samples.py` mirrors them into
  `paper-trail-corpus/samplepapers/<year>/`; `build-index.py` indexes them under the
  specification's first exam year as `sitting: 'sample'`, with no scheme.
- **Earlier syllabuses.** Which archived years predate a syllabus change lives in
  `data/paperTrail/syllabusChanges.ts` (from the SEC's own syllabus-change tables);
  the UI tags and explains those years — the index carries no flag.
- **Hand-curated index decisions** (`HOSTED_ANSWER_FLAGS`, `CROSS_LANG_SCHEMES`)
  reproduce edits once made to `paperTrailData.ts` by hand. Never hand-edit the
  generated file: a rebuild must reproduce it.

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

1. Bump `CURRENT_YEAR` in `enumerate.py` (and `DEFERRED_YEARS` once the archive
   lists that summer's deferred sitting), `LC_YEAR_MAX`/`JC_YEAR_MAX` in
   `build-index.py` and `CURRENT_YEAR` in `upload.py`. When a new specification is
   first examined, add its year to `data/paperTrail/syllabusChanges.ts`, and move
   its sample papers out of `sample-papers.json` once real papers exist (or keep
   them — they stay labelled as samples).
2. Run stages 1→4 in order (1–2 take a few hours; run overnight). For a scope
   extension, `download.py --only-new` fetches only rows with no download record
   (it never re-fetches bucket-reconstructed files), and `upload.py --manifest
   <subset.jsonl>` uploads and verifies exactly a list of new objects.
   `enumerate.py` never re-lists a cached view|exam|year, so material the SEC
   publishes after a crawl is missed: run `refresh_year.py <year>` for the
   current year each autumn (the Junior Cycle marking schemes arrive months
   after the papers — the 2026 JC schemes were only picked up on 2026-10-17). Stage 2.5
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
