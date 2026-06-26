# Evidence Dossier — Mastering Mathematics (subject module)

**Module:** `subject-mathematics-protocol` (data-driven via `components/SubjectModule.tsx`;
content in `subjectContentStem.ts` under key `mathematics`)
**Group:** B (subject-specific) — grounded in official SEC sources + the CAO points grid,
with two study-technique claims grounded in the peer-reviewed learning-science library.
**Review date:** 2026-06-26
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. Sources
surface via inline `{{cite:N}}` markers (rendered as `<Cite/>`) + the **References**
button; data in `data/references/subjectMathematics.ts`.

**Corrections — this module mis-stated the paper structure and it was fixed against the
in-repo 2015 Maths Chief Examiner's Report.** See the table below; all are logged in
`data/cutContent.ts`.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | SEC Mathematics 2015 Chief Examiner's Report — paper structure (each paper 300 marks, 2½ hrs; Section A 6×25 + Section B contexts; answer all) and the requirement to show supporting work for credit | official | in-repo `examiner-reports/maths/2015-chief-examiner.pdf` (verified directly) |
| 2 | CAO common points grid — the 25-point Higher Level Mathematics bonus at H6+ | official | [cao.ie/points](https://www.cao.ie/index.php?page=points&p=calculation) |
| 3 | Roediger & Karpicke (2006), Test-enhanced learning — retrieval practice beats re-reading | paper | [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x) |
| 4 | Rohrer & Taylor (2007), The shuffling of mathematics problems improves learning — interleaving | paper | [10.1007/s11251-007-9015-8](https://doi.org/10.1007/s11251-007-9015-8) |

---

## Claim-by-claim record

- **§1 How Mathematics Actually Works** — Two papers, **each 300 marks**, 2½ hours;
  **Section A (6×25) + Section B (usually 3 questions)**; answer all (**secMaths2015**,
  verified directly — the original "150 marks/paper, six questions" was wrong; corrected,
  MATH-001/002). Strand→paper split is accurate. The 25-point HL bonus at H6+
  (**caoPoints**).
- **§2 What the Examiner Rewards** — Attempt marks / partial credit for relevant steps;
  the Chief Examiner states full marks are withheld without supporting work and an
  incorrect answer with no work shown earns nothing (**secMaths2015**, quoted directly).
  The scale-marks description was made notation-accurate (MATH-003).
- **§3 Where Your Marks Are** — Calculus dominates Paper 1; Probability & Statistics is
  high-yield on Paper 2; part (a)s are accessible; Financial Maths is high marks-to-effort.
  These are reasonable past-paper observations (the report confirms the strand→paper
  mapping and that Section A is largely procedural fluency); the specific mark figures are
  hedged and carry no citation.
- **§4 What Costs You Marks** — Skipping steps forfeits attempt marks (**secMaths2015**).
  Time-management guidance was corrected from the wrong "6 questions / 25 min each" to a
  marks-based pace (≈1 minute per 2 marks) (MATH-004). Sign errors and learning the finite
  set of geometry proofs are practical.
- **§5 How to Study Mathematics** — Past-paper practice (practical). Reworking a wrong
  problem from scratch is retrieval practice (**rk2006**). Topic rotation is interleaving,
  shown specifically for maths problems (**rohrer2007**). The Formulae & Tables booklet is
  a real SEC resource.
- **§6 Your Mathematics Action Plan** — Practical plan; no new empirical claim (priorities
  recap §3, timed papers against the marking scheme).

---

## Corrections & reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Corrected | Reason |
|----|---------|----------------------|--------|
| MATH-001 | §1 | "each worth 150 marks … total of 300 marks" → "each worth 300 marks … total of 600 marks" | Factual error. The 2015 Chief Examiner's Report states each paper is "marked out of 300 marks." Corrected, with bullets updated. |
| MATH-002 | §1 | "six questions, and you must answer all of them" → "two sections — Section A (6×25) and Section B (usually 3) — answer all" | The paper is not six questions; it is Section A (6 questions × 25) + Section B (Contexts & Applications). Corrected to the report's structure. |
| MATH-003 | §2 | "A '5A' or '5B' scale means 5 marks are available" → "each part is graded on a numbered scale (e.g. out of 5 or out of 10), partial credit at each level" | The scale letters do not denote marks available; reframed to the accurate numbered-scale-with-partial-credit description, which the report supports. |
| MATH-004 | §4 | "With 6 compulsory questions in 150 minutes, roughly 25 minutes per question" → "Each paper is 300 marks in 150 minutes … about a minute per two marks" | Consequence of the structure error: there are ~9 questions across two sections, not 6, so the per-question timing was wrong. Replaced with a marks-based pace. |

## Outstanding for accreditation
The §3 high-value mark figures (Calculus "50+ marks", Prob/Stats "40-50 marks", part (a)
"60+ marks") are reasonable but not from a counted source; if wanted as hard evidence,
build a topic-frequency/marks table from recent papers. Section B question count can vary
year to year — the module now says "usually 3," matching the 2015 report's note.
