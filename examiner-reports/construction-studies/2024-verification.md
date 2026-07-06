# Construction Studies — Second-Year Verification (2024 vs 2025)

## Purpose

`data/examinersChair/construction.ts` teaches three load-bearing SEC marking
rules, each cited to the **SEC LC Construction Studies HL marking scheme 2025**
(`examiner-reports/construction-studies/2025-marking-scheme.*`). This document
re-checks those rules against a **different year** — the **2024 Higher Level
marking scheme** — to confirm they are standing conventions and not artefacts of
a single year's paper.

## Source obtained

- **Report:** SEC Leaving Certificate 2024 Marking Scheme — Construction Studies,
  Higher Level.
- **Retrieved:** `Construction Studies HL.pdf` (13.35 MB) from the educateplus.ie
  mirror, https://www.educateplus.ie/sites/default/files/storage/Construction%20Studies%20HL.pdf
- **Cover confirms:** "Leaving Certificate 2024 / Marking Scheme / Higher Level /
  Construction Studies" (PDF page 1).
- **Saved as:** `2024-marking-scheme.pdf`, extracted to `2024-marking-scheme.md`
  via PyPDF2 with `<!-- page N -->` markers (64 PDF pages).
- **Page-number note:** page cites below are the marking scheme's **printed**
  page numbers (the "- 34 -" footer style), which trail the PDF page index by 2.
  The construction.ts file cites 2025 printed pages; this file cites 2024 printed
  pages. The point of the check is that the **rule** recurs, not that the page
  number is identical.

## Confidence

**High.** A genuine, official 2024 HL marking scheme was retrieved and all three
rules were located verbatim in the 2024 scheme's mark tables. No fabrication or
logical-only inference was required.

## Rule-by-rule result

| # | Load-bearing rule (as taught in `construction.ts`) | 2025 cite (in file) | 2024 evidence | Verdict |
|---|----------------------------------------------------|---------------------|---------------|---------|
| CS1 | Sectional/vertical-detail drawings are marked **element by element**, each element split **3 (drawing) + 1 (annotation)** — so annotation is a quarter of every element and unlabelled line-work forfeits it. | p.37, p.43 | **Q1(a)** p.34: "External wall and eaves / Roof / Front wall … **4 × 4 marks … (3 for drawing, 1 for annotation)**". **Q7(a)** p.40: "External wall / Head of window / First floor … **5 × 4 marks … (3 for drawing, 1 for annotation)**". | **STABLE — verbatim match** |
| CS2 | "Describe / show **with the aid of a sketch**" defaults to a **note 3 + sketch 3** split; a text-only answer caps at half. | p.38, p.40 | **Q2(a)** p.35: each detail marked "**Notes (3) … Sketches (3)**" (note and sketch scored as separate 3-mark halves). The half-marks principle also scales up: **Q10** p.43 marks "Notes 6 / Sketches 6" per part. | **STABLE — verbatim match** (note+sketch marked as separate, equal halves; the 3+3 figure recurs exactly) |
| CS3 | U-value calculation is marked **per step** — each material-layer resistance is its own 3-mark tick, each substitution scores separately, ≈33 marks across ≈11 steps, so a bare final answer banks almost nothing. | p.41 (Q5) | **Q5(a)** p.38: "**(a) U-value of external wall (11 × 3 marks)**" — a tabulated 11-line mark grid (external surface resistance, each material element resistance, total resistance, calculation of U-value), **each line = 3 marks**, totalling 33. | **STABLE — verbatim match** (11 × 3 = 33, per-layer) |

## Conclusion

**All three load-bearing rules are stable across a second year.** Each appears in
the 2024 Higher Level marking scheme with the same marking grammar the module
teaches:

- the **3-draw / 1-annotate** per-element split (CS1),
- the **note-3 / sketch-3** equal-halves split for sketch-required parts (CS2), and
- the **per-layer 11 × 3 = 33-mark** U-value tabulation (CS3).

No rule is year-specific or paper-specific. **No changes to
`data/examinersChair/construction.ts` are warranted.**

## Files created by this verification

- `examiner-reports/construction-studies/2024-marking-scheme.pdf`
- `examiner-reports/construction-studies/2024-marking-scheme.md`
- `examiner-reports/construction-studies/2024-verification.md` (this file)
