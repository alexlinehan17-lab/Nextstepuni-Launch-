# Evidence Dossier — The 625 Blueprint (Points Optimization)

**Module:** `points-optimization-protocol` (`components/PointsOptimizationModule.tsx`)
**Group:** B (exam / strategy) — grounded in official Irish State exam & admissions
documents, **not** peer-reviewed psychology journals.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. For Group B
that source is the CAO points grid, SEC marking schemes, and SEC examination statistics
(official, citable). Sources surface via inline `Cite` markers + the **References**
button; data in `data/references/pointsOptimization.ts`.

**Sourcing note (SEC site 403) — DATA-ACCURACY CAVEAT.** examinations.ie hard-blocks
automated fetches (HTTP 403 via the agent proxy), so the SEC annual examination
statistics tables could not be re-downloaded and re-verified this session. The CAO
points-grid claims (§1–§2) and the SRP/surplus marking convention (§6) are stable,
canonical published facts and are stated accurately. **The per-subject H1-rate figures
in §3 and in the `SUBJECTS_DATA` table that drives the H1 Rate Dashboard are
approximate, indicative of recent SEC Higher Level grade distributions, and are
explicitly labelled as such in-app** (a footnote on the dashboard and a sentence in
§3). They were sanity-checked as directionally correct against public knowledge of
recent distributions (Applied Maths and the sciences among the highest H1 rates;
English, Geography, Art among the lowest), but the exact percentages should be
re-grounded against the published SEC statistics tables once examinations.ie is
accessible. **This is the one open accuracy item for accreditation on this module.**
Per the agreed handling (user decision, 2026-06-24): cite the SEC examination
statistics as the official source and carry this caveat, rather than reframe the
figures away or hold the module.

The `objectivity` scores in the same table (e.g. Maths 95, English 25) are **editorial
heuristics**, not SEC-published numbers; they are presented as an illustrative spectrum,
not as sourced statistics, and carry no citation.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | CAO common points grid — grade→points scale (H1 100 / H2 88 / H3 77 …), 25-pt HL Maths bonus, "best six" | official | [cao.ie/points](https://www.cao.ie/index.php?page=points&p=calculation) |
| 2 | SEC Leaving Certificate examination statistics — annual grade distributions by subject & level (H1 rates) | official | [examinations.ie/statistics](https://www.examinations.ie/statistics/) |
| 3 | SEC Leaving Certificate marking schemes — SRP-based marking, surplus valid points, subject conventions | official | [examinations.ie](https://www.examinations.ie/exammaterialarchive/) |

---

## Claim-by-claim record

- **§1 The 12-Point Cliff** — Grade→points values and the 12-point H1→H2 drop (vs 11 for
  H2→H3 and H3→H4); the 2017 grading redesign. All from the CAO common points scale
  (**caoPoints**), and the GRADE_POINTS table in code (H1 100 / H2 88 / H3 77 / H4 66 /
  H5 56 / H6 46 / H7 37 / H8 0) matches it exactly. Verified.
- **§2 The Maths Multiplier** — 25-point HL Maths bonus at H6+; H1 = 125, H6 = 71, vs H3
  = 77 in another subject (**caoPoints**). Verified against the CAO scale.
- **§3 H1 Probability Map** — H1 rates vary substantially by subject (**secExamStatistics**).
  The *direction* (Applied Maths/sciences high; English/Geography/Art low) is robust; the
  *exact* percentages are approximate and labelled as such in-app — see the data-accuracy
  caveat above.
- **§4 The Objectivity Advantage** — Objective (right/wrong) vs subjective (examiner
  discretion) marking. Presented as an editorial framing/spectrum; the objectivity scores
  are heuristics, not sourced statistics — no citation attached.
- **§5 Subject Overlap** — Curriculum content overlaps (Maths/Applied Maths/Physics
  mechanics; Biology/Chemistry/Ag Science organic chemistry; shared language grammar).
  Practical study observation from syllabus content; no citation.
- **§6 The Surplus Rule** — SRP-based marking lists more valid points than required, so
  writing a surplus is a safety net with no penalty for extra correct material
  (**secMarkingSchemes** — a documented SEC marking convention). Verified as a marking
  convention; the specific "+3" is presented as practical advice.
- **§7 Your 625 Blueprint** — Pulls the above together (points recap → **caoPoints**).
  The grade-adjustment phase-out claim was reframed to the documented SEC/Department
  policy and cited to **secExamStatistics** (POPT-001). The 93-95% practice buffer is
  practical advice.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| POPT-001 | §7 | "marking standards are tightening. The generous adjustments from 2022-2024 are being phased out…" → "the post-pandemic grade adjustments are being phased out, so the very high recent H1 rates are expected to ease back toward pre-2020 levels…" | Tightened to the documented SEC/Department policy (unwinding of post-2020 grade adjustments), cited to SEC examination statistics, rather than an unsourced claim about marker behaviour. |

## Outstanding for accreditation
Re-verify the §3 / `SUBJECTS_DATA` H1-rate percentages against the published SEC
Leaving Certificate examination statistics tables once examinations.ie is accessible,
and update any figures that have drifted. Until then they stand as labelled approximate
/ indicative values.
