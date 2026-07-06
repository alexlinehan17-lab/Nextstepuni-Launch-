# LCVP Link Modules — Second-Year Verification (2023 vs 2024)

**Purpose.** Cross-year stability check for the load-bearing marking rules taught in
`data/examinersChair/lcvp.ts`, which cites the **SEC LCVP Link Modules Written Paper
marking scheme 2024** (Common Level). This document verifies those rules against a
**different year** — the **SEC LCVP Link Modules Written Paper marking scheme 2023**
(Common Level) — to confirm they are not one-year artefacts.

LCVP Link Modules is a **single common-level** subject (no Higher/Ordinary split), so
there is no cross-level dimension to check — only cross-year.

## Sources

| Year | File | Retrieval |
|---|---|---|
| 2024 (session file's cited source) | `examiner-reports/lcvp/2024-marking-scheme.pdf` / `.md` | already in repo |
| 2023 (this check) | `examiner-reports/lcvp/2023-marking-scheme.pdf` / `.md` | Downloaded 2026-07-06 from educateplus.ie mirror (`https://educateplus.ie/sites/default/files/storage/LCVP%202023%20CL.pdf`), 24pp, extracted via PyPDF2 with `<!-- page N -->` markers |

Page references below use the scheme's **own printed page numbers** (matching how
`lcvp.ts` cites 2024). In the 2023 `.md`, printed page = PDF `<!-- page N -->` marker − 1
(printed "1" sits on PDF page 2).

## Load-bearing rules under test

| # | Rule in `lcvp.ts` | Session | 2024 cite in file |
|---|---|---|---|
| R1 | Some points are marked **all-or-nothing** — an undeveloped point scores **0**, not a consolation 1 — vs the standard **(1+1)** partial-credit point+expansion grid. "The notation is the instruction." | LC1 (`lcvp-cliff`) | p.2 |
| R2 | The **9-mark "explain three" closers** are marked `3 × (1+1+1)` and carry a **"no repetition of points/expansions"** rule — a reworded restatement scores 0. | LC2 (`lcvp-repetition`) | p.6, p.14 |
| R3 | In the **Section B case study**, credit is gated on **relevance to the specific case/person** — a correct but generic, unapplied answer can score nothing. | LC3 (`lcvp-apply`) | p.3 |

## Rule-by-rule result

| # | Rule | 2023 evidence (printed page / PDF marker) | Verdict |
|---|---|---|---|
| **R1** | All-or-nothing vs (1+1) partial credit | **All-or-nothing present:** Section A Q6 — "Three valid reasons — **2 × 3 marks (0/3)**" (printed p.4 / PDF p.5). **(1+1) partial-credit grid pervasive:** Q5 "4 marks 2@2 **(1+1)**" (p.4), Q8 "3 × 2 marks **(1+1)**" (p.4), and throughout Sections B & C (Section B Q1 "3 × 2 marks (1+1)", Section C Q1(a) "2 × 2 marks (1+1)", etc.). | **STABLE (principle).** Both notations co-exist in 2023 exactly as the rule describes. **Notation caveat:** the *specific token* is year/question-dependent — the all-or-nothing grid appears as **(0/3)** on a 3-mark item in 2023, vs **(0/2)** on 2-mark items in 2024. The rule the app teaches ("some items give nothing without expansion") holds regardless of which `(0/n)` token is used. |
| **R2** | No-repetition on the 9-mark `3×(1+1+1)` closers | **Directly confirmed, multiple instances:** Section C Q1(d) "Assess … (Brexit) … **9 marks — 3 × 3 marks (1+1+1)** … **No repetitions**" (printed p.9 / PDF p.10); Q4(d) "Explain three methods … **9 marks — 3 × 3 marks (1+1+1)** … **No repetition of reasons**" (printed p.15 / PDF p.16). "No repetition of expansions/points" also recurs on the 6-mark grids: Section A Q8 "no repetition of expansions" (p.4), Section B Q2(ii) "no repetition of points" (p.5), Section C Q1(c) "No repetitions of expansions" (p.8), Q3(c) "No repetition of expansions" (p.13). | **STABLE.** The 9-mark closer structure (`3×(1+1+1)`) and the no-repetition rule are present verbatim in 2023. Strongest of the three — confirmed word-for-word across both years. |
| **R3** | Section B credit gated on relevance to the specific case/person | **Structurally present, explicit-phrasing year-specific.** Section B 2023 is a case study (the town of Ballyfert / a Community Development Committee / refugees), with every question anchored to that case; Q3(ii) requires areas "**other than those mentioned in the case study**" (printed p.6) — i.e. relevance to the given case is the gate. The general note (printed p.2) states model answers "are not exhaustive and alternative valid responses … are acceptable." **However**, the *exact explicit instruction* the 2024 cite quotes — "List is not exhaustive, but **answer must be relevant to Sandra**" — does **not** appear in 2023, because the 2023 case names **no individual person** (it is a town/committee). "List is not exhaustive" appears in 2023 only in Section **C** (pp.8, 13, 18), not paired with a named-person relevance line. | **STABLE (principle); explicit named-person instruction is year-specific.** The underlying rule — Section B answers must be applied to the specific case — is structurally true both years. The *named person* ("Sandra") and the explicit "must be relevant to Sandra" instruction are 2024-specific; 2023 enforces the same relevance requirement implicitly through case-anchored questions. **No false claim in the app:** `lcvp.ts` already (a) labels the scenario "authored for this exercise", (b) pins the "relevant to Sandra" quote to the 2024 scheme, and (c) frames the rule generally as "the specific case/**person**". |

## Confidence

- **R2 — HIGH.** Verbatim confirmation in 2023 (two `3×(1+1+1)` 9-markers with "No repetitions" / "No repetition of reasons", plus four further no-repetition grids). Genuinely year-stable.
- **R1 — HIGH (principle) / MEDIUM (exact token).** The all-or-nothing-vs-partial grammar is unambiguously present in 2023. Only the specific `(0/n)` token varies (2023: `(0/3)`; 2024: `(0/2)`), which does not affect the rule the app teaches.
- **R3 — MEDIUM-HIGH.** The relevance-to-the-case principle is structurally stable, but the explicit "must be relevant to [named person]" instruction is year-dependent (a person is named only when the year's case study features one). The app's framing already accounts for this.

## Retrieval note

2023 PDF was retrievable and machine-extractable (no fabrication / no logical-only
fallback required). Extraction is clean for all marking grids and instruction lines
relevant to R1–R3.

## Conclusion

**All three load-bearing rules are year-stable in principle** — every one is
independently evidenced in the 2023 scheme. R2 is confirmed verbatim. R1 and R3 are
confirmed at the level the app actually teaches them (general marking grammar), with the
documented caveats that (i) the all-or-nothing token is `(0/3)` in 2023 vs `(0/2)` in
2024, and (ii) the explicit "relevant to Sandra" named-person instruction is 2024-specific
while the relevance-to-the-case gate itself is present both years.

**No change to `data/examinersChair/lcvp.ts` is warranted.** Its scenarios are explicitly
authored, its year-specific quotes are correctly pinned to the 2024 scheme, and its rule
text is already framed in year-stable terms ("some items", "the specific case/person").
