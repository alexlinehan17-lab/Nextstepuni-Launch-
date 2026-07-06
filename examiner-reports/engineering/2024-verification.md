<!--
  @license
  SPDX-License-Identifier: Apache-2.0
-->

# Engineering — Cross-Year Verification (2024 vs 2025 marking scheme)

**Feature verified:** The Examiner's Chair — `data/examinersChair/engineering.ts`
**Session-file cited year:** 2025 (SEC LC Engineering HL marking scheme 2025)
**Second year checked:** 2024 (this document)
**Purpose:** Confirm the three load-bearing marking rules the feature teaches are
*stable across a second year*, not a 2025-only artefact.

---

## Source of the second-year evidence

- **Report type:** Marking Scheme (SEC, finalised)
- **Year:** 2024
- **Level:** Higher
- **Subject full title:** Engineering — Materials and Technology
- **Retrieved from:** educateplus.ie mirror of the SEC PDF
  (`https://educateplus.ie/sites/default/files/storage/Engineering%20HL_0.pdf`).
- **Verified as the SEC document by its cover page** (PDF p.1):
  "Coimisiún na Scrúduithe Stáit / State Examinations Commission — Leaving
  Certificate 2024 — Marking Scheme — ENGINEERING – Materials and Technology —
  Higher Level." Page-6 header repeats "Marking Scheme 2024".
- **Renamed to:** `2024-marking-scheme.pdf` (36 pages — same structure as 2025)
- **Extracted to:** `2024-marking-scheme.md` via PyPDF2 with `<!-- page N -->`
  markers (PDF page order; printed "Page N" footers match the PDF page number).
- **Retrieval date:** 2026-07-06
- **Retrieval status:** SUCCESS (no fabrication / fallback needed).

Note: like 2025 this is a per-paper marking scheme, so verification is against the
**structural marking grammar** (mark-split notation and the "Any N @…" caps), which
is exactly what the feature teaches — not against holistic cohort commentary.

---

## Load-bearing rules in `engineering.ts` (as written, cited to 2025)

| # | Session | Rule it teaches | 2025 cite in file |
|---|---------|-----------------|-------------------|
| EN1 | `en-anyn` | "Any N @…" menu cap — only N answers count; over-answering earns nothing extra. Grid is a single binary criterion "Property properly discussed @ 6" (`Any three @ 6 + 6 + 6`). | p.20 |
| EN2 | `en-headline` | "explain" points marked **3 + 2** — 3 for stating the point, 2 for developing it; the headline is the bigger, must-be-stated mark. | p.7–9 |
| EN3 | `en-labels` | Diagrams credit required **labels separately** from the drawing (**8 + 1 + 1**); an unlabelled diagram forfeits the label marks. | p.16–17 |

---

## Rule-by-rule cross-year result

| Rule | 2025 (session basis) | 2024 (this check) | Verdict |
|------|----------------------|-------------------|---------|
| **EN1 — "Any N @…" menu cap** | Rubric "Answer any six questions"; Q1 "Any ten @ 5"; part-(b) of long Qs "Any three @ 6 + 6 + 6"; "Any two @ 8 + 8". (2025 p.6 grid; worked p.20.) | **Identical.** Page-6 grid (PDF p.6): "Answer any six questions", Q1 "Any ten @ 5 marks each", "Any two @ 5 + 5", "Any two @ 8 + 8", and **"Any three @ 6 + 6 + 6"** on Q6(b)/Q7(b)/Q8(b)/Q9(b). Worked instances at PDF **p.21, p.24, p.26, p.29**. | **STABLE** |
| **EN2 — 3 + 2 point + development** | Dominant "explain" split; Q1(a),(c),(f),(h),(j) etc. (2025 p.7–9). | **Identical.** Page-6 grid shows `3 + 2` across Q1(a),(b),(d),(f),(g),(l) and Q2/Q3 sub-parts; worked model answers at PDF **p.7–8**. `3 + 2` recurs throughout (30+ instances). | **STABLE** |
| **EN3 — labels credited separately from the drawing** | Q5(b)(i) "Draw … and label" = **8 + 1 + 1** (2025 p.16–17). | **Principle STABLE; exact `8 + 1 + 1` is year-specific.** The 2024 paper's equilibrium/phase question is a different item, so the literal `8 + 1 + 1` string does not appear. But the *rule* — labels are their own separately-credited granules — is explicit: Q4(b)(i) credits five region labels (A–E) at **`1 + 1 + 1 + 1 + 1`** (PDF **p.16**), separate from the 8-mark process diagram above it. The `+1`-per-label convention is present in both years. | **STABLE (rule); example year-specific** |
| **General marking instructions** | Four numbered instructions p.4: examples only / detail scales with marks / Irish 5% rounded down / annotation table. | **Verbatim-identical wording** at PDF p.4 (instructions 1–4), incl. "The solutions presented are examples only. All other valid solutions are acceptable." | **STABLE** |

**Bottom line: all three load-bearing rules are stable across 2024 and 2025.** The
"Any N @…" cap, the 3 + 2 split, and separately-credited diagram labels are all
present in the 2024 HL scheme with the same grammar. The only non-recurrence is the
*specific* `8 + 1 + 1` allocation, which is a 2025-question artefact — the underlying
rule EN3 teaches (labels are separate marks) holds in both years via 2024's
`1 + 1 + 1 + 1 + 1` label block.

---

## Accuracy flag on EN1 — "first N" vs "best N" (not a cross-year drift)

The task's note ("make sure the rule EN1 teaches is genuinely in the scheme") surfaces
a real wording issue that is **stability-neutral but worth recording**.

EN1 teaches that only the **first** N answers written are counted, and that strong
material appearing after the Nth is *wasted*:
- `questionNote`: "only the first N answers count … if your best material comes after
  the Nth, it falls outside the counted set."
- `ruleNote`: "Only the first three answers are marked … if your strongest points come
  fourth and fifth they fall outside the counted three and score nothing."
- `en1-a-3.keyNote`: "only the first three count, so those are uncounted and score nothing."

**What the scheme actually supports:** Neither the 2024 nor the 2025 scheme text states
*which* N over-answers are read (first-in-order vs best). Both simply print the cap
("Any three @ 6 + 6 + 6") and the general instructions (p.4) are silent on excess
answers. The scheme genuinely supports **(a)** only N answers are credited and **(b)**
extras earn nothing — but it does **not** state the specific "first-in-written-order,
best-later-is-wasted" mechanism EN1 leans on.

**Repo-internal conflict:** the sibling file `2025-insights.md` (line 43) infers the
opposite — "writing more than N earns nothing extra — **only the best N are read**."
So EN1's "first N" framing contradicts this repo's own 2025 evidence note.

This is **not a year-to-year difference** (both schemes are identical and silent), so it
does not fail the stability check. It is an accuracy-to-scheme note carried forward for
the maintainer. A proposed year-stable reframe is in the handback report; no session
file was edited (per task scope).

---

## Files in this check

- `2024-marking-scheme.pdf` — SEC LC Engineering HL 2024 scheme (retrieved, 36 pp.)
- `2024-marking-scheme.md` — PyPDF2 text extraction with `<!-- page N -->` markers
- `2024-verification.md` — this document
