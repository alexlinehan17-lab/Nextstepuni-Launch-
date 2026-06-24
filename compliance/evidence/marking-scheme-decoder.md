# Evidence Dossier — The Marking Scheme Decoder

**Module:** `marking-scheme-decoder-protocol` (`components/MarkingSchemeDecoderModule.tsx`)
**Group:** B (exam / strategy) — grounded in documented SEC marking conventions and the
CAO points grid, **not** peer-reviewed psychology journals.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. For this
module the sources are the published SEC Leaving Certificate marking schemes
(examiner-authored, citable) and the CAO points grid. Sources surface via inline `Cite`
markers + the **References** button; data in `data/references/markingSchemeDecoder.ts`.

**Sourcing note (SEC site 403).** examinations.ie blocks automated fetches (HTTP 403),
so live marking-scheme PDFs could not be re-downloaded this session. The claims here are
*standard, stable marking conventions* that recur across SEC marking schemes year on
year (positive marking, the attempt/method/answer structure, "or equivalent", "any N
points", graduated partial credit, per-label diagram marks). They were cross-checked
against the in-repo Business 2015 and Maths 2015 examiner materials and general SEC
marking practice. One glossary item ("PCLM") used a coined acronym the SEC schemes do
not use and was reframed to the documented partial-credit mechanism (MSD-001).

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | SEC Leaving Certificate marking schemes — positive marking, attempt/method/answer marks, "or equivalent", "any N points", graduated partial credit, per-label diagram marks | official | [examinations.ie](https://www.examinations.ie/exammaterialarchive/) |
| 2 | CAO common points grid — grade→points conversion (for the CAO-points cost of blank answers) | official | [cao.ie/points](https://www.cao.ie/index.php?page=points&p=calculation) |

---

## Claim-by-claim record

- **§1 The Examiner's Secret** — Positive marking: examiners credit what is right and
  ignore what is wrong; the marking scheme is published on examinations.ie
  (**secMarkingSchemes**). Verified marking convention.
- **§2 The Three Types of Marks** — Attempt / method / answer marks; you can earn the
  majority of a Maths question's marks for correct method with a wrong final answer
  (**secMarkingSchemes** — attempt and partial/method credit). The "15+/25" figure is an
  illustration of method-heavy partial credit, consistent with the schemes.
- **§3 Reading a Real Marking Scheme** — Notation: "4M", "or equivalent", "any N points",
  graduated partial credit (**secMarkingSchemes**). The "PCLM" item was reframed (MSD-001)
  to the real partial-credit-by-scale mechanism.
- **§4 The Keyword Effect** — Using exact syllabus terminology earns marks where vague
  phrasing does not; examiners scan for the expected terms (**secMarkingSchemes** —
  schemes list the specific indicative terms/SRPs that earn credit). Verified convention.
- **§5 Attempt Marks: The Free Points** — A blank scores zero; any relevant attempt earns
  attempt marks (**secMarkingSchemes**). The cost of blanks in CAO points
  (**caoPoints**). Verified; the "10-15 points / H3-vs-H4" figures are illustrative
  applications of the points grid.
- **§6 The Presentation Protocol** — Per-label diagram marks; method marks awarded per
  clear step; "if the examiner can't find it, they can't mark it" (**secMarkingSchemes** —
  per-label and per-step credit are standard). Verified convention.
- **§7 Your Decoding Action Plan** — Download schemes from examinations.ie, read them
  against past papers, self-mark. Practical procedure; no new empirical claim.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| MSD-001 | §3 | "PCLM — Partial Credit Level Marks" → "partial credit — on-the-right-track work earns part-marks … graduated low/mid/high partial credit" | SEC Maths schemes award graduated partial credit via scales, not an acronym "PCLM"; the real mechanism is kept and the coined acronym dropped. |

## Outstanding for accreditation
When examinations.ie is accessible, spot-check the exact notation strings in a current
marking scheme (e.g. a Maths and a Biology scheme) to confirm the glossary wording
matches the live conventions; the underlying mechanisms are stable and verified.
