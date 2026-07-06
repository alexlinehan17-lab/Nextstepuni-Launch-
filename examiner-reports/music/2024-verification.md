# Music — Examiner's Chair second-year verification (2024 main sitting)

## Purpose
`data/examinersChair/music.ts` teaches three SEC Music (Higher Level) marking
rules, cited to the **2022 Deferred-sitting** marking scheme
(`examiner-reports/music/2022-marking-scheme-deferred.*`). A deferred sitting is
a fallback; this document verifies the same load-bearing rules against a
**recent main-sitting** scheme so the teaching does not rest on a single,
non-standard paper.

## Second source obtained
- **SEC Leaving Certificate Music, Higher Level, marking scheme, 2024 (main sitting).**
- Retrieved: `https://exams.ie/paper-files/lc/music/higher/ms/2024/p0/ms.pdf`
  (exams.ie mirror of the SEC marking scheme).
- Saved: `examiner-reports/music/2024-marking-scheme.pdf` (68 pp., 1.85 MB).
- Extracted: `examiner-reports/music/2024-marking-scheme.md` via PyPDF2 with
  `<!-- page N -->` markers (marker N = extracted PDF page, which aligns with the
  SEC printed page for the Listening/Composing body).
- The document is the combined Composing + Listening (Core) marking scheme, i.e.
  it covers all three rules under review.

Retrieval succeeded, so this is a **full documentary cross-year check**, not a
logical-only inference.

## Rule-by-rule result

| # | Load-bearing rule (as taught in `music.ts`) | 2022 cite in `music.ts` | 2024 main-sitting location | Verbatim 2024 text | Stable? |
|---|---|---|---|---|---|
| MU1 | Two opposite over-answering regimes: on "name/identify a specific number of features" items **each extra incorrect answer cancels a correct one**; on explicit-choice questions examiners **mark all and award the best**. | p.9 (General Notes to Examiners, over-answering) | Extracted p.13 — "General Notes to Examiners", notes 2 & 3 | (2) "Where there is a choice of question to answer (Q5B), if a candidate answers more than one question, mark all answers and award the marks for the best answer." (3) "In questions where the candidate is asked to identify/name/choose a specific number of features/instruments, each extra incorrect answer cancels a correct one." | **YES — verbatim, both regimes stated side by side** |
| MU2 | Full marks need a fully-correct statement; a **partially-correct / vague answer is capped at 1 mark** regardless of length. | p.11–18 (partially-correct = 1 cap) | Extracted p.13 (General Notes) + recurring across Listening pp.14–22 | "NB Full marks can only be awarded for statements/descriptions that are fully correct." + 15 line-items reading "Partially correct answer/description = 1m" across the Listening paper. | **YES — same cap, applied throughout** |
| MU3 | A chord earns 1 mark **only as part of a good progression** (not correct-in-isolation); specific voice-leading moves such as **V7–V are rejected**. | p.7 (chord-in-progression rule; rejected moves) | Extracted pp.7–8 (Composing, chord descriptors) | "1 mark for each chord that is part of a good progression in all chord boxes"; "Marks for chords are not awarded in isolation. Chords must be part of a good progression."; "V7 - V not accepted"; "Vb or V7b should generally be followed by i". | **YES — verbatim, incl. the V7–V rejection** |

## Notes on page numbering
The **rules** are identical across the two years; only the **page numbers shift**
(the 2024 General Notes / over-answering rules sit on p.13 rather than 2022's p.9,
and the partially-correct cap recurs across pp.14–22 rather than 2022's p.11–18,
because the two papers paginate differently). The cites inside `music.ts` are
explicitly year-locked to the **2022** scheme (`SEC Music HL marking scheme 2022,
p.X`), so those page references remain correct for their stated source. No page
cite in `music.ts` needs to change: it does not claim 2024 pages.

## Verdict
All three load-bearing rules are **STABLE across a second, main-sitting year**
(2024 HL). The 2024 scheme actually strengthens the MU1 teaching: it prints both
over-answering regimes as adjacent numbered notes in the General Notes to
Examiners, exactly as `music.ts` frames them. The earlier concern — that the
teaching rested only on a non-standard *deferred* paper — is resolved: the marking
grammar is confirmed on the main sitting.

**No changes proposed to `data/examinersChair/music.ts`.** Its cites are correct
for the 2022 source they name; this document is the corroborating second-year
evidence.
