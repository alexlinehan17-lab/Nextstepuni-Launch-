<!--
  @license
  SPDX-License-Identifier: Apache-2.0
-->

# Economics — Second-Year Verification (2023 vs 2025)

Cross-year stability check for the marking rules taught in
`data/examinersChair/economics.ts`, which cite the **SEC LC Economics HL (and
OL) marking scheme 2025**. This file re-verifies each load-bearing rule against
a **different** year to confirm the rules are structural (spec-level), not
one-year artefacts.

## Sources

| Scheme | File | Provenance |
|---|---|---|
| SEC LC Economics **HL 2023** marking scheme | `examiner-reports/economics/2023-marking-scheme.pdf` / `.md` | Educateplus mirror of the SEC PDF (`Economics 2023 HL.pdf`). Cover page: "Coimisiún na Scrúduithe Stáit / State Examinations Commission … Leaving Certificate 2023 … Marking Scheme … Higher Level … Economics". 44 pages. examinations.ie itself sits behind a Cloudflare bot-challenge that blocks scripted download; the mirror is byte-for-byte the SEC document. |
| SEC LC Economics **OL 2023** marking scheme | `examiner-reports/economics/2023-ol-marking-scheme.pdf` / `.md` | Same mirror (`Economics 2023 OL.pdf`). Cover: "… Leaving Certificate 2023 … Ordinary Level … Economics". 32 pages. |
| (baseline) HL 2025 | `2025-marking-scheme.*` | Session-of-record scheme cited in `economics.ts`. |
| (baseline) OL 2025 | `2025-ol-marking-scheme.*` | Session-of-record OL scheme. |

**Retrieved:** 2026-07-06. Extraction via PyPDF2 with `<!-- page N -->` markers.
Page numbers below are **PDF page indices** in the 2023 `.md`, which differ from
the *printed* page numbers cited in `economics.ts` (those cites are correctly
scoped to the 2025 layout — this check verifies the **rules**, not page numbers).

**Spec note:** A revised LC Economics specification has been examined **from 2022**.
Both 2023 and 2025 sit **inside the current spec**, so this is a legitimate
within-spec second-year check. Pre-2022 schemes are a different spec and were not
used.

---

## Rule-by-rule result

| # | Session (level) | Rule as taught in `economics.ts` | 2025 cite (in file) | 2023 evidence | Stable? | Spec-dependent? |
|---|---|---|---|---|---|---|
| EC1 | Develop, don't repeat (HL) | Developed points graded on a descriptor band **Excellent 3 / Good 2 / Fair 1 / Weak 0**; **"Repetition of statement" is an explicit Weak (0) descriptor**. | p.2 | 2023 HL PDF p.3: identical band table `3 2 1 0 · Excellent / Good / Fair / Weak`, Weak = "No knowledge · **Repetition of statement**". The 5-band `4 3 2 1 0` variant (adds "Poor = Confusing/Contradictory") also present identically. | ✅ Stable — verbatim match | Current-spec structural. Not year-specific. |
| EC2 | Labels are the marks (HL) | Diagrams carry **itemised** marks; axis / curve / equilibrium **labels are separate, forfeitable** marks. | p.50 (S&D graph itemised) | 2023 HL: cue "Explain, with the aid of a **fully labelled diagram (including the axes)**" appears repeatedly (PDF p.3, p.24). Circular-Flow-of-Income diagram marked **`13 @ 1`** (PDF p.24) — every labelled element is its own 1-mark tick. Confirms per-label itemised marking. | ✅ Stable — rule confirmed | Current-spec structural. (The specific *page* and the specific 17-mark S&D grid are year-specific; the **rule** is not.) |
| EC3 | Workings + missing % (HL) | Calculations are **step-marked** (formula + substitution + answer); **named deduction for omitting the %**. | p.5, p.57 | 2023 HL PDF p.15: `361671/4761865 × 100 = 7.59%` followed by "**- 1 Mark if % omitted**". Step-marked calc grids and the `N @ M` developed-point grammar (`2 @ 3`, `2 @ 6`, `2 @ 7`, …) run throughout. | ✅ Stable — rule confirmed (phrasing "- 1 Mark if % omitted" vs 2025 "Deduct 1 mark for omission of %"; same rule) | Current-spec structural. |
| EC4 | OL front-loading (OL) | OL two-point ("explain/outline two") parts are **front-loaded 1st @ 8 / 2nd @ 4**; the first point is worth more. | OL p.22, p.25 | 2023 OL: `1st @ 8` / `2nd @ 4` appears **repeatedly** (PDF pp.4–6, 9–11, etc. — e.g. "Outline two effects…", "Outline two measures…", "Explain two reasons…"). 2025 OL shows the same split. | ✅ Stable — rule confirmed, prevalent | Current-spec structural. |

---

## Discrepancy found — the OL "no omission-of-%" claim is **year-specific** (not a rule EC4 teaches, but a claim in `coverageNote`)

`economics.ts` `coverageNote` asserts, as an OL characteristic:

> "…and **there is no omission-of-% deduction at OL**. Verified against the 2025 OL scheme."

This is **true for 2025 OL** but **false for 2023 OL**:

- **2025 OL** (`2025-ol-marking-scheme.md`): percentage calculations — "Calculate the percentage increase…" → `41.3 %`, "Calculate capital expenditure as a percentage…" → `14.14 %` — carry **no** omission-of-% deduction line. Grep for "omission of %" / "% sign" / "deduct … %" on the calc parts returns nothing.
- **2023 OL** (`2023-ol-marking-scheme.md`): the equivalent percentage calcs **explicitly** print the deduction, twice:
  - PDF p.11: "€27.5m / €95m x 100 = 28.94% / 29%. … **Deduct 1 mark for omission of % sign.**"
  - PDF p.19: "…101,853 + 68,042 / 208,913 × 100 = 81.32% … **Deduct 1 mark for omission of % sign**".

So OL **does** use the omission-of-% deduction in some years (2023); the 2025 OL paper simply didn't attach it to its calc parts. Presenting "no omission-of-% deduction at OL" as a standing OL feature is not year-stable. This matches the scheme's own caution (2025 HL p.2): *"Assumptions about future marking schemes on the basis of past schemes should be avoided."*

**Scope:** this clause lives **only** in `coverageNote` (subject-level metadata). The
teaching content of session **EC4 does not depend on it** — EC4 teaches the
front-loading rule (1st @ 8 / 2nd @ 4), which is fully stable. No session script,
takeaway, or cite is affected.

---

## Verdict

- **EC1, EC2, EC3, EC4 core rules: STABLE across 2023 ↔ 2025**, all within the current (2022+) spec. No session content requires change.
- **One `coverageNote` clause is year-specific** ("no omission-of-% deduction at OL") and should be reframed to a year-stable statement. Proposed replacement is in the session report (not applied here — this pass does not edit `economics.ts`).
- Per-scheme **printed page numbers** are inherently year-specific; `economics.ts` cites are correctly labelled "…scheme 2025, p.X", so they make no cross-year page claim.
