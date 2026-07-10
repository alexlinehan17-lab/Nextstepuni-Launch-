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
