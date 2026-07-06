# Agricultural Science — Second-Year Verification of "Examiner's Chair" Rules

## Purpose
`data/examinersChair/agscience.ts` teaches three SEC marking-scheme rules, each cited to the
**2024** Higher Level Agricultural Science marking scheme. This document checks whether those
load-bearing rules are **stable across a second, different year** so the feature does not depend
on a single year's scheme wording.

## Source used for cross-year check
- **SEC Leaving Certificate Agricultural Science, Higher Level, 2023 marking scheme**
- Retrieved from educateplus.ie mirror:
  `https://www.educateplus.ie/sites/default/files/storage/Ag%20Science%202023%20HL.pdf`
  (examinations.ie 403s direct hotlinks).
- Saved: `examiner-reports/agricultural-science/2023-marking-scheme.pdf` (32 pages, PDF v1.6)
- Extracted: `examiner-reports/agricultural-science/2023-marking-scheme.md` (PyPDF2, `<!-- page N -->` markers)
- **Spec note:** the revised Agricultural Science specification was first examined in 2021. Both the
  cited 2024 scheme and this 2023 comparison scheme fall within the current spec, so the comparison
  is spec-valid (2023 is adjacent to the cited 2024).

## Rule-by-rule result

| # | Rule (as taught in `agscience.ts`) | Cited (2024) | Found in 2023 scheme? | 2023 location | Verdict |
|---|---|---|---|---|---|
| Ag1 | **Front-loaded points list**: lists pay `4 + 2 + 2 + 2` — the first correct answer earns 4, each subsequent correct answer earns 2. | p.4 | **Yes — verbatim.** "The marking scheme might be as follows: 4 + 2 + 2 + 2. This means that the first correct answer encountered is awarded 4 marks and each subsequent correct answer is awarded 2 marks." | p.4 | **STABLE** |
| Ag2 | **Surplus-answer penalty**: a surplus wrong answer cancels a correct one; worked in the scheme as `4 − 1 = 3` on a breed-ID line, using "Texel". | p.4 | **Yes — verbatim, same worked example.** "Surplus answers — A surplus wrong answer cancels the marks awarded for a correct answer." Worked example: breed-ID line, candidate adds surplus "Texel", "the candidate scores 4 - 1 = 3 marks." Annotation `[` = "A surplus incorrect answer has cancelled a correct answer" (p.5). | p.4 (+ p.5 annotation) | **STABLE** |
| Ag3 | **IIS holistic banding**: each IIS section is one holistic band (Excellent / Very Good / Good / Fair / Weak), not additive points; the scheme warns markers not to penalise brevity nor reward length. | p.7 | **Yes — verbatim.** Page 7 header "Higher Level Agricultural Science Marking Criteria for Individual Investigative Study" with a five-column band table (Excellent / Very Good / Good / Fair / Weak). Note: "Be careful not to penalise skilful brevity, nor to reward unwarranted length." | p.7 | **STABLE** |

## Detail / exact 2023 wording captured

**Ag1 — front-loaded points (2023, p.4):**
> "The marking scheme might be as follows: 4 + 2 + 2 + 2. This means that the first correct answer
> encountered is awarded 4 marks and each subsequent correct answer is awarded 2 marks."

Matches the `agscience.ts` Ag1 shorthand `4 + 2 + 2 + 2` and its ruleNote exactly. Same page (p.4).

**Ag2 — surplus-answer penalty (2023, p.4):**
> "Surplus answers — A surplus wrong answer cancels the marks awarded for a correct answer.
> e.g. Question: Identify the cattle and sheep breeds. Marking scheme: A = Suffolk / B = Shorthorn /
> C = Belgian blue / D = Texel - 4(1). Candidate's Answer = A = Texel, Suffolk / … The surplus answer
> (Texel) is incorrect. Therefore, the candidate scores 4 - 1 = 3 marks."

The `agscience.ts` questionNote cites "worked in the scheme as 4 − 1 = 3 on a similar breed-ID line" and
uses Texel as the surplus wrong breed — this is the *identical worked example* the SEC uses, present in
both the 2024 (cited) and 2023 (comparison) schemes. Same page (p.4). The supporting annotation
(`[` = "A surplus incorrect answer has cancelled a correct answer") appears on p.5 in 2023.

**Ag3 — IIS holistic banding + brevity note (2023, p.7):**
> "Higher Level Agricultural Science Marking Criteria for Individual Investigative Study … Note: Be
> careful not to penalise skilful brevity, nor to reward unwarranted length."

Five-band table (Excellent / Very Good / Good / Fair / Weak) marked holistically per section. Matches
the `agscience.ts` Ag3 notes and takeaway exactly, same page (p.7).

Note on band mark values: the specific numeric band marks used in the `agscience.ts` Ag3 scale
(Weak 6 / Good 14 / Very Good 18 / Excellent 22) are an *illustrative* teaching scale, not quoted from
a specific IIS section — in both schemes the per-section IIS mark totals vary by section (e.g. 10-mark
sections use Excellent 9-10M, 15-mark sections use Excellent 14-15M). The load-bearing rule Ag3 teaches
(holistic band, not additive points; brevity/length note) is what is verified stable; the exact numbers
are not presented as a citation and are unaffected.

## Confidence
**High.** A second, distinct HL marking scheme (2023) was retrieved and text-extracted successfully.
All three load-bearing rules appear at the **same page numbers** cited in `agscience.ts` (p.4, p.4, p.7),
with **verbatim wording** and, for Ag2, the **identical worked example** (Texel, 4 − 1 = 3). No
retrieval failure; no logical-only fallback needed.

## Conclusion
**All three rules are STABLE across years.** Ag1 (front-loaded `4+2+2+2`), Ag2 (surplus wrong answer
cancels a correct one, `4−1=3`, Texel example), and Ag3 (IIS holistic five-band marking with the
brevity/length note) are reproduced verbatim and at the same page numbers in both the cited 2024 and
the comparison 2023 Higher Level schemes. These are standing SEC marking conventions, not year-specific
quirks. **No changes to `data/examinersChair/agscience.ts` are warranted.**
