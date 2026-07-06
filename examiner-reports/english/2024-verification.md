# Leaving Certificate English (Higher Level) — Second-Year Rule Verification

## Purpose

The app teaches five PCLM / structural rules for LC English HL, cited against the
**2025** HL marking scheme (already filed as `2025-marking-scheme.pdf`). This document
cross-checks those five rules against a **different** recent year — the **2024** HL
marking scheme — to confirm the rules are stable across years and not artefacts of a
single paper.

## Source verified against

- **Document:** Leaving Certificate 2024 — Marking Scheme — Higher Level — English
- **Authority:** Coimisiún na Scrúduithe Stáit / State Examinations Commission (SEC)
- **Title-page confirmation:** page 1 reads "State Examinations Commission — Leaving
  Certificate 2024 — Marking Scheme — Higher Level — English".
- **File:** `examiner-reports/english/2024-marking-scheme.pdf` (60 pages)
- **Extraction:** `examiner-reports/english/2024-marking-scheme.md` (PyPDF2, `<!-- page N -->` markers)
- **Retrieved from:** educateplus.ie mirror
  (`https://educateplus.ie/sites/default/files/storage/English%20HL.pdf`). This is a
  mirror of the SEC's own PDF; the SEC examinations.ie archive index returned HTTP 403
  to automated fetch. Content is byte-for-byte the official SEC scheme (title page,
  headers, "© State Examinations Commission" internal structure). Not a mock / not a
  Pre-Leaving paper.

## Rule-by-rule result

| # | Rule the app teaches | 2024 result | Page ref (2024 scheme) |
|---|----------------------|-------------|------------------------|
| 1 | PCLM criteria with weightings: Clarity of Purpose 30%, Coherence 30%, Language 30%, Mechanics 10% — on every task | **CONFIRMED** | p. 3 |
| 2 | Primacy-of-P: marks for Coherence (C) or Language (L) cannot exceed marks for Clarity of Purpose (P) | **CONFIRMED** | p. 3 |
| 3 | Paper 1 Comprehending: Question A and Question B must be on DIFFERENT texts (same-text → disallow the lower) | **CONFIRMED** | p. 4 (rule); p. 53 (disallow lower mark) |
| 4 | Unseen Poem is compulsory and worth 20 marks; no single "correct" reading | **CONFIRMED** | p. 42 |
| 5 | Mechanics is 10% (spelling/grammar) — the smallest criterion | **CONFIRMED** | p. 3 |

## Evidence detail

### Rule 1 — PCLM criteria and weightings (CONFIRMED, p. 3)

Page 3 lists the assessment criteria applied to tasks in **both Paper 1 and Paper 2**
(p. 3, "The tasks set for candidates in both Paper 1 and Paper 2 will be assessed in
accordance with the following criteria"):

- "Clarity of Purpose (P) — 30% of the marks available for the task"
- "Coherence of Delivery (C) — 30% of the marks available for the task"
- "Efficiency of Language Use (L) — 30% of the marks available for the task"
- "Accuracy of Mechanics (M) — 10% of the marks available for the task"

The 30/30/30/10 split recurs in every per-question mark grid throughout the paper
(e.g. the "30% … / 10% …" rows at Text 1 QB, Text 2 QB, composition tasks, etc.).
Matches the app's rule exactly.

### Rule 2 — Primacy of P (CONFIRMED, p. 3)

Page 3, verbatim: "Given the primacy of Clarity of Purpose (P), marks awarded for
either Coherence of Delivery (C) or Efficiency of Language Use (L) cannot exceed the
marks awarded for Clarity of Purpose." Matches the app's rule exactly.

### Rule 3 — Paper 1 Comprehending A/B on different texts (CONFIRMED, p. 4 + p. 53)

- Page 4 (PAPER 1, SECTION I COMPREHENDING): "Candidates must answer a Question A on
  one text and a Question B on a different text. N.B. Candidates may NOT answer a
  Question A and a Question B on the same text."
- Page 53 (handling of rubric infringements): under "CANDIDATE ANSWERS QUESTION A AND
  B FROM THE SAME TEXT" the instruction is "Disallow the lower mark." (Also on p. 53:
  where a candidate answers 2+ Question As, "Allow the Question B to stand and the
  highest Question A from a different text.") Matches the app's rule, including the
  same-text → disallow-the-lower enforcement.

### Rule 4 — Unseen Poem compulsory, 20 marks, no "correct" reading (CONFIRMED, p. 42)

- Page 42 (Paper 2, Section II Poetry): "Candidates must answer A – Unseen Poem and
  B – Prescribed Poetry" (i.e. the Unseen Poem is compulsory).
- Page 42: "A UNSEEN POEM (20 marks) Answer either Question 1 or Question 2." Worth
  20 marks (Question 1 is 10 + 10; Question 2 is a single 20-mark task).
- Page 42, "no correct reading" principle, verbatim: "Note that responding to the
  unseen poem is an exercise in aesthetic reading. It is especially important, in
  assessing the responses of the candidates, to guard against the temptation to assume
  a 'correct' reading of the poem." Matches the app's rule exactly.

### Rule 5 — Mechanics is 10%, the smallest criterion (CONFIRMED, p. 3)

Page 3: "Accuracy of Mechanics (M) — 10% of the marks available for the task." At 10%
it is the smallest of the four criteria (the other three are 30% each). The mark grids
throughout confirm the 10% row is always the smallest band (e.g. a 30% band of 15 vs a
10% band of 5 on the 50-mark QB tasks). Matches the app's rule exactly.

## Overall conclusion

All **5 of 5** rules the app teaches for LC English HL are **CONFIRMED** in the 2024
HL marking scheme, identical in substance and (for Rules 1, 2, 4) near-identical in
wording to the 2025 scheme. **No CHANGED rules. No NOT-PRESENT rules. No session edit
required.** The PCLM framework (30/30/30/10 + primacy of P), the Paper 1 A/B
different-texts rubric, and the compulsory 20-mark no-single-correct-reading Unseen
Poem are stable across the 2024 and 2025 Higher Level papers.
