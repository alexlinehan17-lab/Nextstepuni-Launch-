# Paper Trail — "See the answer" (in-paper marking-scheme answers)

Plan of record. Produced by an adversarial design workflow (5 competing approaches →
3-lens judge panel → a kill-skeptic who re-verified every load-bearing claim against the
real corpus → synthesis → completeness critic). Approach chosen: **Authentic Scheme-Peek**.

## Locked decisions (founder, 2026-06-13)

1. **QA gate = per-subject-grammar-profile review** (NOT per-paper, NOT automated-only).
   Verify ~3 representative papers/years per profile on a contact sheet → flags go live →
   auto-extend to that profile's other years while the autumn zero-anchor canary stays green.
2. **Pilot = Maths Higher Level first** (P1 + P2, 2022–2025 EV, ~8 papers). Essays
   (History HL → Geography HL) are the Phase 6 workstream, gated on a worst-case render test.
3. **Offline = yes.** Phase 0 adds the Workbox runtime-cache rule for the Storage scheme
   PDFs + sidecars (CacheFirst + RangeRequestsPlugin for PDFs; SWR for JSON; capped
   maxEntries/maxAge). Reveals work after one online open. Accepted: caches multi-MB scheme
   PDFs on-device + modest egress, within the €50/mo guard.

## Build status (2026-06-13)

- **Phase 0** ✅ Workbox cache rules for Storage PDFs + sidecars (in the built SW).
- **Phase 1** ✅ `anchor-map.py` engine — 8/8 Maths HL papers fully mapped, 80/80
  questions, independently audited (zero mis-anchors), `test_anchor_map.py` gate.
- **Phase 2** ✅ `PaperAnswerMap` contract + `answers:1` flag + sidecar upload +
  `test/paperTrailAnswers.test.ts`. Flag gated behind `QA_PASSED_ANSWER_PROFILES`.
- **Phase 3** ✅ Viewer "Answers" toggle + per-question chips.
- **Phase 4** ✅ `CropView` scheme-region reveal (visual gate + code review passed).
- **Phase 5** ✅ **SHIPPED LIVE (2026-06-13)** — founder approved live deploy (no
  students until September launch). `("mathematics","higher","ev")` added to
  `QA_PASSED_ANSWER_PROFILES`; 8 sidecars uploaded to Storage; deployed to
  `https://nextstepuni-app.web.app`. Maths HL P1+P2 2022–25 now show the Answers
  toggle; every other paper is unchanged. Founder reviewing live, will advise
  changes.

Coverage beyond the pilot stays narrow-and-slow by design: each new subject is a
`GRAMMAR` row + a contact-sheet review + adding its profile to
`QA_PASSED_ANSWER_PROFILES`. Unmapped papers behave exactly as before.

## The one-sentence idea

An **"Answers"** toggle appears on a paper when we have a verified question-map for it.
Turn it on, and a small **"See answer"** chip pins beside each mapped question. Tap it, and
the student sees the marking scheme's **own pixels** for *that exact question* — a crop of
the real SEC scheme rendered in place — without leaving the paper or losing their spot.

## The core decision: show pixels, never generated text

We render a **crop of the real marking-scheme PDF region** for each question. We never
generate, summarise, or "extract a value into the box." Why this beat every alternative:

- **Accuracy is the gate, not a feature.** With authentic pixels, the worst possible
  failure is a *missing chip* or the *wrong region of the real scheme* — both of which the
  student catches instantly via the always-present "View full scheme" jump. A
  confidently-**wrong** answer (the thing an exam tool can never afford) is structurally
  impossible because we author no answer.
- **Maths proves it.** On the real Maths HL Q1 solution page the maths extracts as
  **mojibake** — 63 non-ASCII glyphs incl. math-italic 𝑎𝑏𝑐𝑚𝑛𝑥. Text extraction
  *garbles the maths*, so "the answer in the box as text" is not just lossy, it's wrong.
  Pixels are mandatory. A maths "answer" is also a multi-step **method** worth most of the
  marks — so the reveal is the **whole model-solution region**, never a distilled value.
- **Copyright posture is unchanged.** We already mirror SEC PDFs with
  "© State Examinations Commission" attribution. Coordinates-only sidecars + client-side
  clipped render means **no new derivative artifact** — byte-identical posture to today.

## What the student sees

1. Opens a paper exactly as today (paper/scheme toggle, each side keeps its scroll).
2. If this paper has a verified map, an **"Answers"** toggle appears in the header. It is
   **never a dead button** — a 1-byte `answers:1` flag on the paper tells the UI up front.
3. Toggle on → subtle **"See answer"** chips pin beside each mapped question; the scheme PDF
   quietly prefetches so reveals work offline later. Nothing reveals automatically
   (try-first pedagogy preserved).
4. **Maths:** tap → the whole model-solution region drops as a scrollable card in the
   rough-work lane *under* the question.
5. **Essays (History/Geography):** chip reads "What the marking scheme credits" → opens a
   docked bottom-sheet showing the scheme's indicative content + mark allocations, with the
   honest line *"This is how examiners award marks — not a model essay."*
6. Every reveal carries © SEC and a **"View full scheme"** link that jumps the Scheme side
   to that exact page (self-verify in one tap).
7. Uncertain anchor → the chip degrades to **"Open the marking scheme here"** (a reliable
   page-jump), **never** a wrong inline crop. No map → today's exact UI.

## How correctness is guaranteed (the gates the skeptic forced in)

Four fixes were verified-necessary against the real files and are **blocking**:

1. **Word-boundary token location, not `search_for`.** `search_for("Question 1")` returns
   page 27 ("Question 10") on the real Maths P1 — which would *omit your flagship Q1*. Fix:
   `get_text("words")` exact-token matching at the left margin. CI fixture asserts Q1 of
   Maths HL P1 2022 yields exactly **one** anchor on page 3.
2. **Component-band split (the fatal P1/P2 case).** Paper 1 and Paper 2 **share one scheme
   file** (`LC003ALP000EV.pdf`); "Q1" legitimately appears at pages 6–8 (P1) *and* 34–36
   (P2). Without scoping to the paper's own component band, a student on Paper 1 could be
   shown Paper 2's solution. Fix: split the scheme on its verified "Paper 1"(p2)/"Paper
   2"(p30) dividers; every region must fall inside the paper's band or the whole paper omits.
3. **Rotation/cropbox normalization** — emit fractions of the *rotated* page box, or omit
   anchors on rotated pages (degrade to page-jump). Every emitted fraction asserted ∈ [0,1].
4. **Human QA per subject-grammar-profile** (NOT per-paper, NOT a spot-check). The P1/P2
   collision passes *every* automated check and is caught only by a human comparing position
   on a contact sheet. So: verify ~3 representative papers/years per subject-grammar profile
   on a contact sheet before that profile's flags ship; auto-extend to its other years only
   while an autumn **zero-anchor canary** stays green.

Deterministic omit-on-doubt floor (any failure → no chip): monotonic + no-gaps +
non-overlapping + count-reconcile, conservative bounding (uncertain boundary →
`mode:'pagejump'` as the *primary* behaviour), front-matter/summary-grid exclusion.

## Data & architecture

- **Sidecar, not inlined.** Per-paper coordinates-only JSON `PaperAnswerMap` (page +
  fractional rects, scheme region scoped to this paper's component band — **no text, no
  image bytes**, ~1 KB on the wire per opened paper). Stored at
  `papers/{cycle}/{subjectId}/{year}/answers/{fileid}.json`, fetched over the existing
  CORS/range REST path. ~1–2 MB gzipped across the whole corpus; client fetches only the one
  paper it opened.
- **Eager flag only.** `answers?:1` on `PaperItem` (<5 KB total in the 736 KB
  `paperTrailData.ts`) so the toggle is never a dead button.
- **New pipeline stage `anchor-map.py`** runs after `download`, before `build-index`
  (deterministic, resume-safe, fitz-only). A per-subject **MARKER GRAMMAR table** keyed by
  (subject-code, language) — a new subject is one table row + one review pass, not a code
  change.
- **Viewer overlay rides existing geometry for free.** Chips are absolute children of the
  page holder positioned by fractional `top` → they ride the zoom scroller, dpr≤2 backing
  scale, and IntersectionObserver virtualisation with no new layout math. Crop renders
  client-side from the already-loaded scheme `PDFDocumentProxy` reusing the double-buffer +
  `MAX_CANVAS_PIXELS` path.

## Phased, loop-ready build (each independently shippable, each gated)

- **Phase 0 (blocker, found by the critic):** add a Workbox runtime-cache rule for the
  Storage PDF + sidecar URLs (CacheFirst + RangeRequestsPlugin for PDFs; SWR for the JSON)
  with maxEntries/maxAge caps — **today there is no SW rule for Firebase Storage**, so the
  offline claim is false until this exists. (Or drop the offline-answers claim.)
- **Phase 1:** `anchor-map.py` — Maths HL pilot engine (word-boundary location +
  component-band split + grid exclusion). Gate: deterministic re-run byte-identical; Q1→one
  anchor on p3 fixture; every region inside its paper's band; monotonic/in-[0,1] asserts pass.
- **Phase 2:** sidecar contract + `answers?:1` flag + `storage.ts` kind union + upload
  wiring. Gate: typecheck clean; `paperTrailData.ts` grows <5 KB; integrity test (every
  flagged paper has a loadable in-band sidecar).
- **Phase 3:** Viewer fractional-anchor overlay + chips (no crop yet). Gate on a real
  cheap phone: chips stay glued through all 6 zoom steps + rotation; tear down with their
  page; no map → zero chips.
- **Phase 4:** Maths crop renderer — inline rough-work card + "View full scheme" escape
  hatch + © SEC. Gate: crop pixel-matches the full scheme; offline render works after one
  online open.
- **Phase 5:** Maths HL pilot human-QA gate + **ship** (flag-gated; everything else
  untouched). Gate: 100% of mapped pilot questions position-confirmed (incl. P1-Q1→p6,
  P2-Q1→p34). **Pilot live.**
- **Phase 6:** Essay workstream — **first** measure worst-case multi-page History render on
  a low-end device at the pixel cap, **then** History HL + Geography HL with the bottom-sheet.
  Gate: render stays under cap within a few seconds; per-profile contact-sheet QA; canary green.

## Honest trade-offs (state plainly)

- **Narrow-and-slow by design.** Coverage grows at *human* pace (per-profile review), not
  code pace. Most of the 4,291 papers stay **unmapped = behave exactly like today** until
  verified. This is the correct trust trade-off: narrow-and-right over wide-and-maybe-wrong.
- **A mix of inline crops and page-jumps** within a mapped paper — conservative bounding
  degrades to a page-jump whenever a boundary is uncertain. Still "don't lose your place,"
  just not all-inline.
- **Maths first, essays second.** Your History/Geography example comes in Phase 6, after
  maths proves the engine on the riskiest shared-scheme case.
- **Sub-question (A/B/i/ii) granularity is v1-coarse** — the student gets the whole
  top-level question's region and scrolls within it.

## Explicitly OUT of v1 scope (omit cleanly, never half-wire)

OL/Foundation, Irish-medium (IV) & BV bilingual, Irish T1/T2, JC, LCA (LB — incl. the
tasks-vs-written dual-scheme shape), and **aural/listening** (A00/U00 + music/language
answer-booklets, which index questions against an audio track, not the page). These are a
clean component-code skip in `anchor-map.py`. The grammar table is keyed by
(subject-code, **language**) so an Irish-medium scheme ("Ceist N", not "Question N") is
detected as a grammar miss (canary), never silently mapped against an EV scheme.

## Production safety after ship (critic)

Lightweight, **PII-free, aggregate-only** telemetry (consistent with the outstanding
minors'-consent gate B4): chip reveal, immediate "View full scheme" tap after a reveal (a
proxy for "that crop looked wrong"), reveal→fast-dismiss. A spike in the reveal→full-scheme
ratio for a subject/year flags a mis-anchored grammar row **in the field**, not just at
build. Threshold + owner live in the autumn-refresh runbook.

## Recents / portal interaction (critic — decide before Phase 3/6)

`RecentPaper` has no "Answers was on" bit — decide: persist `answersOn` (small migration,
mirrors `lastLevel`/`lastLang`) or reset to off on every open and say so. The essay sheet
must render **inside the existing Viewer portal**, respect the modal scroll-lock, and the
back button closes the sheet first (one back = close reveal, second = close viewer).
