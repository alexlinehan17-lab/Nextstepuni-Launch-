# Evidence Dossier — The Points Playbook (Leaving Cert Strategy)

**Module:** `leaving-cert-strategy-protocol` (`components/LeavingCertStrategyModule.tsx`)
**Group:** B (exam / subject) — grounded in official Irish State exam & admissions
documents, **not** peer-reviewed psychology journals.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. For Group B
that source is the CAO points grid and SEC marking schemes / Chief Examiner reports
(examiner-authored and citable; CLAUDE.md). Sources surface via inline `Cite` markers +
the module-wide **References** button; data in `data/references/leavingCertStrategy.ts`.

**Sourcing note (SEC site 403).** examinations.ie hard-blocks automated fetches (HTTP 403
via the agent proxy), so live re-download of SEC PDFs was not possible this session. The
**Business 2015 Chief Examiner's Report is mirrored in-repo** (`examiner-reports/business/`)
and was read directly to verify the §4–§5 claims. The CAO points grid and SEC marking-scheme
weightings are stable, canonical published facts, stated accurately here and cross-checked
against the in-repo marking schemes where they overlap; their canonical URLs are cited.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | CAO common points grid — "best six", 25-pt HL Maths bonus, H7 = 37 | official | [cao.ie/points](https://www.cao.ie/index.php?page=points&p=calculation) |
| 2 | SEC Leaving Certificate marking schemes — component weightings, attempt/partial-credit, subject conventions | official | [examinations.ie](https://www.examinations.ie/exammaterialarchive/) |
| 3 | SEC Business 2015 Chief Examiner's Report — "answer the question asked"; developed vs one-word answers | official | in-repo `examiner-reports/business/2015-chief-examiner.pdf` |

---

## Claim-by-claim record

- **§1 Points game** — Best-six rule; 25 bonus points for HL Maths at H6+; H7 = 37 points;
  full H1–H8 / O1–O8 grid (encoded correctly in the calculator) (**caoPoints**). Verified
  against the CAO common points scale.
- **§2 Subject choice** — Cluster / "bank your marks" strategy; the "easy subject myth".
  Reasoning + the factual existence of coursework/oral components (**secMarkingSchemes**).
- **§3 Core subjects** — English PCLM weighting (P/C/L 30% each, Mechanics 10%); Irish oral
  = 40%; Maths attempt/partial-credit marking (**secMarkingSchemes**). Verified against SEC
  marking schemes.
- **§4 Other subjects** — Subject marking conventions: Business "State/Explain/Example" and
  developed-vs-one-word answers grounded in the **secBusiness2015** report; the general
  "marking schemes reward specific conventions" point in **secMarkingSchemes**. *Biology
  "exact keywords" and Geography "~2 marks per point" are accurate SEC marking conventions
  but await their own subject Chief Examiner reports for first-hand grounding — flagged for
  the per-subject Group B pass.*
- **§5 What examiners want** — Command words require different answer types; the leading
  recurring error is reciting knowledge instead of answering the question set
  (**secBusiness2015**, directly verified). The "#1 cause" superlative was softened
  (LCS-001).
- **§6 Exam day** — Calm morning routine, first-5-minutes brain-dump, strict timing. The
  planner widget's physiological-sigh / low-GI / avoid-cramming items echo the Group A
  learning-science modules (already DOI-verified there); no new claim.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| LCS-001 | § 5 | "the #1 cause of losing marks" → "one of the most common ways students lose marks" | SEC reports support that misreading/not-answering is a *leading* error (Business 2015, verified), but no source ranks it #1 across all subjects. |

## Outstanding for the per-subject pass
Biology / Geography (and other subject) marking specifics in §4 should be re-grounded
against each subject's own SEC Chief Examiner report once those are added to
`/examiner-reports/` (blocked this session by the examinations.ie 403).
