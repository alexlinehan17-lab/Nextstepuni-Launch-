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
| 2 | biology, geography (Part One), chemistry, physics, agricultural-science, business 2025 HL+OL | respective `examiner-reports/<subject>/*-marking-scheme.md` | Agent-authored under wave-1 rules; CI gates + human spot-checks of notation fidelity against the scheme markdown before shipping (recorded below when merged) |

Pitfall sources in use: Chief Examiner's Report 2015 (Business HL), pp.14 & 17 —
the same page-cited insights surfaced by `data/paperTrail/examinerInsights.ts`.

## Presentation honesty

- The panel is titled "How the marks are given" and footers every open state with
  the scheme cite + "© State Examinations Commission".
- The lens renders only where an entry exists — no dead buttons, no generated
  fallback content.
- The lens never replaces the scheme itself: the full scheme crop remains one tap
  away in the same card.
