# Politics & Society — Second-Year Verification (2024 vs cited 2025)

## Purpose

`data/examinersChair/politics.ts` teaches SEC Politics & Society marking rules cited to the
**2025** HL and OL marking schemes. This document cross-checks each load-bearing rule against a
**different year** — the **2024** HL and OL marking schemes — to confirm the rules are stable
standing features of the marking grammar, not artefacts of a single year's paper.

## Sources obtained

| File | Level | Year | Provenance |
|------|-------|------|------------|
| `2024-marking-scheme.pdf` / `.md` | Higher | 2024 | SEC LC Politics & Society HL marking scheme, via educateplus.ie mirror of examinations.ie (17 pp). Cover page reads "Leaving Certificate 2024 … Politics and Society … Higher Level". |
| `2024-ol-marking-scheme.pdf` / `.md` | Ordinary | 2024 | SEC LC Politics & Society OL marking scheme, via educateplus.ie mirror of examinations.ie (21 pp). Cover page reads "Leaving Certificate 2024 … Politics and Society … Ordinary Level". |

Retrieval succeeded — no logical-only fallback needed. Page markers `<!-- page N -->` embedded in
the `.md` extractions (PyPDF2). Page numbers below are the PDF/print pages of the **2024** schemes;
they differ from the 2025 cites because pagination shifts year to year — the marking grammar is what
is being verified, not the page coordinates.

---

## Rule-by-rule result

| # | Session rule (cited to 2025) | 2025 cite | Found in 2024? | 2024 location | Verbatim 2024 text | Verdict |
|---|------------------------------|-----------|----------------|---------------|--------------------|---------|
| **PS1** | 20-mark data item marked by descriptor band; top band 16–20 = "independent and insightful", Good band 11–15 = "relevant but lacking insight"; accurate/relevant description caps in Good. | HL p.11 | **Yes** | HL p.9–10 | "Very good … 16‑20M independent, insightful comment using both documents"; "Good … 11‑15M relevant comment but lacking insight". Also (evaluation variant) "Very good answer 16‑20M clear, accurate, insightful evaluation"; "Good answer 11‑15M relevant but lacking insight". | **STABLE** — identical band boundaries and identical descriptor wording. |
| **PS2** | Section C essay marked on analytic criteria (Analysis & Synthesis, Evaluation, Cohesion…) then reconciled to H1–H8 holistic bands; lower band descriptor = "summary and repetition often take the place of discussion"; summary ≠ discussion caps in lower bands. | HL p.14–15 / p.15 | **Yes** | HL p.12–13 (analytic grid + holistic band grid); H1–H8 bands p.13 (H1 = 90–100 marks … H8) | Analytic criteria grid present (Analysis & Synthesis /20, Evaluation /15, Cohesion /15 etc.); holistic band descriptor: "Summary and repetition often take the place of discussion." | **STABLE** — analytic-then-holistic H1–H8 structure and the exact "summary and repetition … take the place of discussion" phrase both present. |
| **PS3** | 50-mark documents-question capstone marked on a **split** rubric of two separately-awarded scales: argument /30 + Use of documents /20; both must be earned. | HL p.12 | **Yes** | HL p.10 | Capstone item worth 50 marks split as: "[argument scale] (30 marks)" — Very Good 24‑30M … Weak 0‑8M — **plus** "Use of documents (20 marks)" — Very Good 16‑20M comprehensive use of documents … Weak 0‑5M vague/inaccurate. | **STABLE (structure)** — 30 + 20 split into two independent scales, both required, is identical. See note below on the 30-mark scale's *label*. |
| **PS4 (OL)** | OL Section C essay /50 on six criteria: Introduction 10, Knowledge 10, Evidence 10, Analysis 5, Evaluation 5, Cohesion 10 — Analysis/Evaluation are the lightest (5 each), reverse of HL. | OL p.15 | **Yes** | OL p.14 | Introduction (I) **10 marks**; Knowledge **10 marks**; Evidence **10 marks**; Analysis & Synthesis **5 marks**; Evaluation **5 marks**; Cohesion **10 marks** (= 50). | **STABLE** — exact same six criteria and exact same weightings (10/10/10/5/5/10). |

---

## Note on PS3 — the one year-specific *wording* (not a rule change)

The **structure** PS3 teaches — a 50-mark capstone split into a /30 argument scale and a /20 "Use
of documents" scale, marked separately, both required — is identical in 2024 and 2025.

What varies by year is the **label of the 30-mark scale**, because it takes the command word of that
year's capstone question:

- **2025 scheme / session:** the capstone task was a *conclusions* task, so the 30-mark scale is
  labelled **"Conclusions"**.
- **2024 scheme:** the capstone item (g) was "…critique the use of quotas…", so the 30-mark scale is
  labelled **"Critique (30 marks)"**.

In other years it can be "Discuss", "Evaluate", etc. The "**Use of documents (20 marks)**" scale is
constant. So the load-bearing rule (split 30/20, two separate scales, ignore the documents and you
forfeit up to 20) is fully stable; only the human-readable name of the argument half tracks the
question. This is a question-artefact, not a marking-rule change, so `politics.ts` is not wrong — but
see the optional reframe in the accompanying report if a fully year-agnostic phrasing is preferred.

---

## Overall verdict

All four load-bearing rules (PS1 insight-beats-relevance bands, PS2 summary-isn't-discussion
holistic bands, PS3 split documents rubric, PS4 OL criteria weightings) are **STABLE across a second,
independent year (2024)**. Descriptor wording, band boundaries, mark totals and criteria weightings
match the cited 2025 scheme. Page coordinates differ (expected). Confidence: **high** — verified
against retrieved primary PDFs at both levels, not a logical inference.
