# Italian HL — Second-Year Verification (2024 vs 2025)

## Purpose

Cross-year stability check for the marking rules taught in
`data/examinersChair/italian.ts`, which cite the **SEC Leaving Certificate
Italian Higher Level marking scheme 2025**. This document verifies each
load-bearing rule against a **different year's** scheme.

## Source obtained

- **SEC LC Italian Higher Level marking scheme 2024** — full 32-page marking
  scheme (English-medium, `LC013ALP000EV`).
  - Saved: `examiner-reports/italian/2024-marking-scheme.pdf`
  - Extracted: `examiner-reports/italian/2024-marking-scheme.md`
    (PyPDF2, `<!-- page N -->` markers).
  - Retrieval note: examinations.ie is behind a Cloudflare bot challenge
    (direct hotlinks return a "Just a moment…" 403). The identical SEC PDF was
    retrieved from the exams.ie mirror
    (`https://exams.ie/paper-files/lc/italian/higher/ms/2024/ms.pdf`,
    HTTP 200, `application/pdf`, 449 KB). The 2023 HL scheme
    (`.../ms/2023/ms.pdf`, 36 pp) was also downloaded as corroboration and
    matches on every rule below. The cover page confirms
    "Leaving Certificate 2024 … Marking Scheme … Higher Level … Italian".

## Rule-by-rule result

| # | Rule taught in `italian.ts` | `italian.ts` cite (2025) | 2024 scheme | Result |
|---|------------------------------|--------------------------|-------------|--------|
| IT1 | Writing scored **Content/Communication 15 + Language 10**; graduated cap: **content ≤ 7 → Language marked out of 5** | p.26 | **Present, verbatim.** p.20: "In C1 and C2 where the marks awarded for content and communication are 7 or less, language will be marked out of 5." Also the C3 tier ("12 or less → out of 7") and the 15+10 split are identical. | **STABLE** |
| IT2 | Answering in **Italian where English is required** (Q5 opinion question) triggers a **−50% deduction**, far harsher than the −1 excess penalty | p.11, p.13 (also listening p.5) | **Only partly reproduced.** The *English-answer requirement* is present (the Section A Q5 answer key on p.10 is written in English). **But the explicit "−50% of marks gained" wrong-language penalty is ABSENT from the 2024 scheme.** The 2024 general instructions and listening/reading rules state only the −1 (incomplete/manipulation) and excess/redundant-material penalties — no whole-question/whole-section "answered in Italian → deduct 50%" clause. The 2025 scheme states that clause three times (p.5 listening, p.11 and p.13 reading Q5). | **YEAR-SPECIFIC** (see note) |
| IT3 | "Candidates **must not produce something learnt off by heart and off the point**" — rote-off-task fails content | p.27 | **Present, verbatim.** p.20: "Candidates must not produce something learnt off by heart and off the point. It is not necessary to use all the words or phrases given." | **STABLE** |

## Notes on IT2

- The claim in `italian.ts` is **source-accurate**: the −50% wrong-language
  deduction is stated verbatim in the *cited* 2025 scheme (p.5, p.11, p.13),
  and every in-app citation is stamped "…marking scheme 2025". It is **not**
  fabricated.
- The finding is one of **cross-year stability only**: the 2024 scheme (and the
  2023 scheme) do **not** print the −50% clause, so it cannot be presented as a
  multi-year *standing* rule on the strength of these schemes. The underlying,
  year-stable fact both schemes support is narrower: **the Q5 "opinion"
  comprehension question must be answered in English** (2024 shows this by
  giving the answer key in English; 2025 states it explicitly and adds the
  −50% deduction).
- Recommended handling (proposed in the session report, not applied here):
  keep the −50% figure but pin it explicitly to the 2025 scheme and stop the
  copy from reading as a timeless standing rule. IT1 and IT3 need no change.

## Page-number cross-reference (for the record)

| Rule | 2025 scheme page (as cited in `italian.ts`) | 2024 scheme page |
|------|---------------------------------------------|------------------|
| Content cap (content ≤7 → Language /5) | p.26 | p.20 |
| Learnt-off-by-heart / off the point | p.27 | p.20 |
| −50% wrong-language penalty | p.5 (listening), p.11, p.13 (reading Q5) | not present |

Page numbers differ year-to-year (normal — the schemes paginate differently).
The `italian.ts` cites are correct for the 2025 source they name.

## Confidence

High. Both the 2024 and 2023 Higher Level schemes were obtained as genuine
full PDFs and read directly. IT1 and IT3 are reproduced word-for-word in 2024;
the IT2 −50% clause is verifiably absent from the 2024 (and 2023) schemes while
present in 2025.
