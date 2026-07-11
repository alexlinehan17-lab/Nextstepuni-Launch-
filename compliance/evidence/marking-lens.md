# Evidence Dossier — Marking Lens

**Tool:** Marking Lens (a layer inside the Topic Vault question card, `components/PaperTrail/VaultQuestionCard.tsx`)
**Content data:** `data/markingLens/{types,index,<subject>}.ts`
**Review date:** 2026-07-10 (living document — updated with every authoring wave)
**Governing rule:** Marking Lens attaches to REAL past-paper questions and shows how
the SEC marking scheme allocates their marks. Every `notation` is transcribed
**verbatim** from the filed scheme (normalised spacing only); every `decoded` line
restates only what that notation allocates — never advice, model answers, or claims
the scheme does not make; every entry cites the exact scheme document and question.
Optional `pitfall` lines appear only where a Chief Examiner's Report documents the
behaviour for that question type, with their own page-cited source. Where a scheme
section is ambiguous or its parts cannot be made to sum to the printed question
total, the question is **skipped** — a missing lens is acceptable, a wrong one is not.

The sources are official SEC marking schemes and Chief Examiner's Reports — exam
marking allocations are administrative facts, so verification is against the SEC
documents held in `/examiner-reports/` (PDF + markdown), not CrossRef/DOI records.

## Machine-checked integrity (every CI run — `test/markingLens.test.ts`)

1. Every entry keys to a real tagged Topic Vault question (paper tagged, `n` in its
   tag list) — no orphan lenses.
2. Every entry's parts sum **exactly** to its `totalMarks` — a ladder that doesn't
   add up misstates the scheme and fails the build.
3. Every entry carries a scheme cite; every pitfall carries a report cite.
4. Keys are unique.

## Authoring waves

| Wave | Subject / papers | Source document(s) | Verification |
|------|------------------|--------------------|--------------|
| 1 (golden) | Business 2024 HL — 12 Section-1 shorts + 8 long questions (EV + IV mirror), 28 entries | `examiner-reports/business/2024-marking-scheme.md` | Hand-authored; every notation transcribed from the scheme and every sum checked line-by-line against its "Available Marks"; CI gates green |
| 2 | business 2025 HL+OL, physics 2023+2025 HL, chemistry 2024+2025 HL, agricultural-science 2023+2024 HL (EV + IV mirrors) | respective `examiner-reports/<subject>/*-marking-scheme.md` | Agent-authored under wave-1 rules; CI gates + notation spot-checks; shipped |
| 2b | biology 2025 HL+OL (68 entries), geography Part One 2024 HL + 2025 OL (36 entries), EV + IV mirrors | `biology/2025-{hl,ol}-marking-scheme.md`; `geography/2024-marking-scheme.md`, `geography/2025-ol-marking-scheme.md` | Booklet/keying re-verified against the served Topic Vault tags before registering (see keying notes below); CI gates green; 1735 tests pass |
| 2c | economics 2025 OL + 2023 OL (64 entries: Q1–16 each year, EV + IV mirror) | `economics/2025-ol-marking-scheme.md/.pdf`, `economics/2023-ol-marking-scheme.md/.pdf` | The prose scheme's Max-Mark column does not bind to its parts in the flattened markdown, so the part↔mark ladder was extracted with **PyMuPDF `find_tables()`** off the source PDF (Section A = 12 marks each; Section B = 75 = (a)+(b)+(c) with printed per-part totals). Every internal notation and every question total independently re-verified against the extraction before registering; single booklet, so not booklet-ambiguous. CI gates green |
| 2d | home-economics S&S 2025 HL + 2024 HL + 2025 OL + 2024 OL (152 entries: 14 Section-A shorts + 5 Section-B longs per paper, EV + IV mirror) | `home-economics/2025-marking-scheme.md/.pdf`, `2024-…`, `2025-ol-…`, `2024-ol-…` | Two-booklet split solved independently against the tags before authoring (the first attempt stalled on exactly this): **LP014 = Section A** (14 short questions, 6 marks each), **LP039 = Section B** (Q1 = 80, Q2–5 = 50). Notation is the scheme's additive "N points @ M marks (graded M:…:0)" tokens, verbatim. Both booklets share n1–5, so all 8 home-ec booklets are on the booklet-safety gate's verified list (gate 5). Sums, keys and the LP014→Section-A / LP039→Section-B direction all re-verified; CI gates green |

**Home Economics closed wave 2 at 8 subjects.** A later re-assessment probed the
filed subjects the ceiling section had covered only by a blanket claim, and
three proved cleanly authorable — see wave 3 below. The remaining filed subjects
stay ruled out for the reasons in "Coverage ceiling" (grade-banded, or no
scheme∩tag overlap).

**Wave 3 — technical subjects (probe-then-author):**

| Wave | Coverage | Source schemes | Verification notes |
|------|----------|----------------|--------------------|
| 3a | engineering 2024 HL + 2025 HL (36 entries: Q1–9 each year, EV + IV mirror) | `engineering/2024-marking-scheme.md/.pdf`, `engineering/2025-marking-scheme.md/.pdf` | Fully additive scheme ("Any ten @ 5 marks each", per-part notation repeated verbatim under each model answer). The mark-grid pages are column-scrambled in the md extraction, so every notation was taken from the per-question body pages and cross-checked against the grid. Choice menus modelled at the capped total (Q1's 13 printed 5-mark options would sum to 65 — the row is the printed "Any ten @ 5 marks each" at 50). Part-(c) OR forks carry both printed routes in one row (both sum to the same 16). Single fileid per sitting, n=1–9 maps 1:1 — no booklet ambiguity. OL sittings are tagged but no OL scheme is filed, so OL is NOT authored. No pitfalls: no LC Engineering Chief Examiner's Report exists (confirmed in `engineering/2025-insights.md`). CI gates green |
| 3b | construction-studies 2024 HL + 2025 HL (40 entries: Q1–10 each year, EV + IV mirror) | `construction-studies/2024-marking-scheme.md/.pdf`, `construction-studies/2025-marking-scheme.md/.pdf` | PERFORMANCE CRITERIA / MAXIMUM MARK tables summing to a printed TOTAL 60 per question. Because the md extraction scrambles table columns, **every mark-grid page of both PDFs was rendered to images and read visually** — this caught the filed `2025-insights.md` misquoting 2025 Q7's slate-courses row (it is 6 marks, not 4; the insights arithmetic would give 64 ≠ 60). The 8-mark Scale/Drafting row (Q1/Q7 both years) is decoded exactly as printed ("Excellent 8, Good 6, Fair 4") as its own additive row. Both years also print a "Question 10 (Alternative)" grid; the tagged Q10 was resolved to the **main** version both years via the Topic Vault stem texts (2024 EnerPHit retrofit, 2025 Passive House) — the Alternative grids are unkeyed, not silently merged. Single booklet per sitting; OL tagged but no OL scheme filed → not authored; no CE report filed → no pitfalls. CI gates green |
| 3c | design-and-communication-graphics 2024 HL + 2025 HL (32 entries: n1–8 each year, EV + IV mirror) | `dcg/2024-marking-scheme.md/.pdf`, `dcg/2025-marking-scheme.md/.pdf` | Additive graphical step-ladders (roman-indexed steps with explicit marks) summing to 60 per question. **Keying verified 8/8 per year** by matching tag topic labels to scheme question content (e.g. 2024 n2 "Developments and Envelopments" ↔ B-2 salad-box surface development; 2025 n4 "Geologic Geometry" ↔ C-1 strike/dip/thickness) — the Biology-precedent check, exceeded. Tag n `'1'`–`'8'` = scheme B-1…B-3, C-1…C-5 on the LC562ALP039* booklet. **Section A (A-1…A-4) is authorable on scheme evidence but its booklet (LC562ALP014*) carries no Topic Vault tags — dropped as orphan keys rather than mis-keyed.** OL tagged but no OL scheme filed → not authored; no CE report → no pitfalls. Marks re-extracted from the PDFs (pypdf) and cross-checked against the md. CI gates green |

**Applied Maths** (additive, but tags stop at 2022 vs 2023/24 schemes across a
syllabus change) and **French** (reading comprehension additive, but tags stop
at 2018) join Accounting in the blocked-by-data family: authorable in marking
style, but no scheme∩tag overlap to key to today. With wave 3, Marking Lens
covers **11 subjects (~603 entries)** — and the Answer Architect and Definition
Drill projections deepen automatically with it.

**Keying notes (wave 2b — the checks that matter for "a wrong lens is worse than a missing one"):**

- **Biology booklet split** — each sitting is served as two booklets. The `…LP038…`
  booklet carries vault `n 1–10` = scheme Q1–Q10 (Sections A + B); the `…LP040…`
  booklet carries `n 1–7` = scheme Q11–Q17 (Section C). Confirmed against the tags by
  three unambiguous topic matches on the LP040 booklet (n2 Genetics ↔ Q12, n4 Responses
  to Stimuli ↔ Q14, n5 Ecology ↔ Q15). IV papers mirror EV under the same scheme.
- **Geography is two booklets, and the lens covers Part One only.** Part One shorts are
  served on the `…LP042…` (p1) booklet; Part Two structured questions on `…LP043…` (p2).
  An earlier draft mis-keyed the Part One lens to the LP043 booklet — that would have
  shown Part One 8-mark marking on Part Two questions (a wrong-crop error), so it was
  corrected to LP042 before registering.
- **Geography 2025 HL Part One is deliberately omitted.** The Topic Vault only tags the
  2025 HL Part Two booklet (LC005ALP043EV); the Part One booklet (LC005ALP042EV) is not
  served, so there is no vault question to attach the (already-authored) Part One marks
  to. Held back rather than mis-keyed — a missing lens is acceptable, a wrong one is not.

Pitfall sources in use:
- Chief Examiner's Report 2015 (Business HL), pp.14 & 17 — surfaced by `data/paperTrail/examinerInsights.ts`.
- Chief Examiner's Report 2012 (Geography HL), p.23 — Part One short-answer commentary
  (Q1 Glacial Landforms: arête/pyramidal peak/lateral moraine confusion; Q6 Regions:
  brief definitions in part (ii)), filed at `examiner-reports/geography/2012-chief-examiner.md`.
- SEC Marking Scheme 2025 Biology HL (p.4) and OL (pp.4–5) — the Section-A surplus rule
  and the Q16/Q17 best-two-of-four rule, printed verbatim in the schemes themselves.

## Coverage ceiling — subjects assessed and NOT authored (why)

Marking Lens is only honest where a scheme allocates marks by **named, additive
point values** that sum to the printed question total. Two large families of
subject do not, and were deliberately left uncovered rather than fabricated:

- **Grade-banded subjects** (Religious Education, History, Classical Studies, and
  the essay papers generally): these schemes award a part by a descriptor band
  (Excellent / Very Good / Good / Fair / Weak / Poor → a mark *range*), not by
  summing named points. There is no ladder to show without inventing sub-marks,
  so no lens is authored. Verified directly: the RE OL 2024/2025 schemes are
  band-only; History 2025 HL is band-only for source evaluation and essays (only
  the RSR outline-plan citations are discretely marked).
- **Blocked by data, not by marking style: Accounting.** Filed schemes are 2023/24
  but the Topic Vault tags stop at 2020, so there is no tagged question to key a
  lens to. Revisit if/when 2023–24 accounting papers are tagged.

## Presentation honesty

- The panel is titled "How the marks are given" and footers every open state with
  the scheme cite + "© State Examinations Commission".
- The lens renders only where an entry exists — no dead buttons, no generated
  fallback content.
- The lens never replaces the scheme itself: the full scheme crop remains one tap
  away in the same card.
