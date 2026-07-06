# Art (Visual Studies) — Second-Year Verification for `data/examinersChair/art.ts`

## Purpose

`data/examinersChair/art.ts` cites the **SEC LC Art Visual Studies written-paper marking scheme 2024** for its
three load-bearing rules, and tags all three sessions `level:'common'` on the claim that the written-paper
descriptor bands are word-for-word identical at Higher and Ordinary level.

This document performs an independent **second-year** check against a **different** scheme year within the same
(current, revised) Visual Studies specification, and re-confirms the OL = HL descriptor-identity claim by comparing
the Higher and Ordinary schemes for that year directly.

## Sources retrieved (this verification)

| File | Level | Year | Origin |
|------|-------|------|--------|
| `2023-visual-studies-marking-scheme.pdf` / `.md` | Higher | 2023 | SEC via educateplus.ie mirror (`Art%202023%20HL.pdf`) |
| `2023-visual-studies-ol-marking-scheme.pdf` / `.md` | Ordinary | 2023 | SEC via educateplus.ie mirror (`Art%202023%20OL.pdf`) |

Both are the CURRENT revised-specification Visual Studies written paper (Section A "Today's world" 50 marks;
Sections B "Europe and the wider world" / C "Ireland and its place in the wider world" 50 marks each; Section B/C
marked by four independent strands). This is the same paper architecture as the cited 2024 scheme, and distinct
from the pre-2022 "History & Appreciation" paper.

Page markers in the `.md` files are PDF page indices; the SEC printed footer number is PDF index − 1 (e.g. PDF
page 23 = printed footer 22), exactly as in the 2024 extraction. All page cites below are the **printed footer**
numbers used by `art.ts`.

## Rule-by-rule cross-year result

| # | `art.ts` rule (cite) | 2023 HL finding | 2023 OL finding | Stable? |
|---|----------------------|-----------------|-----------------|---------|
| ART1 | Subject Knowledge is a **/20** strand marked Low/Moderate/High; High band demands *"critical thinking to analyse and evaluate their knowledge"*; recall alone cannot reach the top band. (printed p.22) | "Subject Knowledge. 20 Marks." Low 0-7 / Moderate 8-13 / High 14-20. High band bullet: *"A thorough level of critical thinking to analyse and evaluate their knowledge of the section of focus."* Printed footer p.22 (PDF p.23). | Identical text, identical mark bands, identical location (printed p.22 / PDF p.23). | ✅ STABLE |
| ART2 | Relevant Examples is a separable **/10** strand; vague/unrecognised references cap Low; recognised, specific works score High. (printed p.23) | "Relevant Examples. 10 Marks." Low 0-3 (*"limited relevance/not recognised"*) / Moderate 4-6 (*"mostly relevant/recognised"*) / High 7-10 (*"most relevant/recognised … thorough understanding of the … artworks/artefacts used"*). Printed footer p.23 (PDF p.24). | Identical text, identical mark bands, identical location (printed p.23 / PDF p.24). | ✅ STABLE |
| ART3 | Section A part (a) is answered **using the paper's given headings**; a general description that ignores the named headings can't reach the top band; banded Low/Moderate/High. (printed pp.17–19, p.17) | Section A "Today's world" short-question descriptor at printed p.16 (PDF p.17); Question 1(a) et al. explicitly phrased *"Description of this painting using the given headings: colour, style"* etc., each banded Low/Moderate/High. Given-headings mechanic present and load-bearing. Printed pp.16–18 (PDF pp.17–19). | Q1(a): *"Description of the painting using the given headings: colour, composition."* Same given-headings mechanic, same banding. | ✅ STABLE (see note) |

### Note on ART3 — mark value varies, rule does not

The *specific* named headings and the *exact* mark value of a Section A part-(a) vary question-to-question and
year-to-year: 2024 Q1(a) was a 6-mark item (0-2 / 3-4 / 5-6) with headings "composition, perspective, colour";
2023 Q1(a) was a 5-mark item (0-1 / 2-3 / 4-5) with headings "colour, style", while other 2023 Section A (a)
parts are 6-mark. `art.ts` ART3 handles this correctly by hedging — its question says *"for example composition,
perspective and colour"* and its notes speak of "the given headings" generically rather than a fixed heading list
or a fixed mark total. The **load-bearing rule** (answer around the named headings; a heading-blind general
description is capped below the top band) is stable across 2023 and 2024. No year-specific text is baked in that
would go stale. The illustrative `bands([2,4,6])` / /6 framing in ART3 matches the common 6-mark case and remains
representative.

## OL = HL descriptor identity — re-confirmed for a second year

The three Section B/C strand descriptors were compared line-by-line between the **2023 Higher** and **2023
Ordinary** schemes:

- **Coherence and Focus (/10):** identical wording, identical bands (Low 0-3 / Moderate 4-6 / High 7-10).
- **Subject Knowledge (/20):** identical wording, identical bands (Low 0-7 / Moderate 8-13 / High 14-20).
- **Relevant Examples (/10):** identical wording, identical bands (Low 0-3 / Moderate 4-6 / High 7-10).

The only differences between the HL and OL extractions are OCR line-break artefacts (e.g. "thinki ng",
"recogn ised"); the descriptor prose, strand weights and band boundaries are **word-for-word identical**.
Differentiation between levels is carried by the **question paper / stimulus material** (OL uses simpler,
everyday-visual-culture stimuli and shorter given-heading lists), **not** by the marking descriptors.

This is the same finding the 2024 HL-vs-OL comparison produced, now independently reproduced for 2023.
The `level:'common'` tagging in `art.ts` is therefore justified across two exam years.

## Verdict

- **All three load-bearing rules are STABLE** across a second scheme year (2023 vs the cited 2024), including the
  exact printed-footer page locations (p.22, p.23, p.17).
- **OL and HL descriptors remain identical** in 2023, re-confirming the `common` tagging.
- **No edits to `data/examinersChair/art.ts` are warranted.**

## Retrieval confidence

HIGH. Two genuine full 28-page SEC PDFs (2023 HL and 2023 OL) were retrieved and machine-extracted; the relevant
descriptor pages were read directly, not inferred. The mirror (educateplus.ie) reproduces the SEC PDFs verbatim
(matching internal page footers and SEC formatting).
