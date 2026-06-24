# Evidence Dossier — Answer Engineering

**Module:** `answer-engineering-protocol` (`components/AnswerEngineeringModule.tsx`)
**Group:** B (exam / strategy) — grounded in documented SEC marking conventions and the
in-repo Business Chief Examiner report, **not** peer-reviewed psychology journals.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. Sources
surface via inline `Cite` markers + the **References** button; data in
`data/references/answerEngineering.ts`.

**Note.** The answer-structure frameworks themselves — **PEEL** (Point/Evidence/Explain/
Link), **S³S** (State/Substitute/Solve/State), the **marks-shape decoder**, and the
**60% rescue** — are pedagogical scaffolds / mnemonics, not empirical claims, and carry
no citation (same treatment as "Backward Design" elsewhere). What *is* cited is the
underlying SEC marking convention each framework exploits. One unverifiable specific
("400+ scripts / 2-3 minutes per answer") was reframed to the qualitative claim
(AE-001).

**Sourcing note (SEC site 403).** examinations.ie blocks automated fetches, so live
marking schemes could not be re-downloaded. The marking conventions cited here are
stable and recurring, and the developed-answer point is verified directly against the
in-repo **Business 2015 Chief Examiner's Report**.

---

## Verified sources

| # | Source | Kind | Locator |
|---|--------|------|---------|
| 1 | SEC Leaving Certificate marking schemes — method/attempt/answer marks, mark allocation signalling answer length, separately-marked sub-parts, per-label diagram marks | official | [examinations.ie](https://www.examinations.ie/exammaterialarchive/) |
| 2 | SEC Business 2015 Chief Examiner's Report — developed vs one-word answers; State/Explain/Example; answering the question asked | official | in-repo `examiner-reports/business/2015-chief-examiner.pdf` |

---

## Claim-by-claim record

- **§1 The Structure Gap** — Examiners mark at volume under time pressure, so points the
  examiner cannot find go unmarked (**secMarkingSchemes**); developed, clearly-structured
  points outscore one-word or buried answers (**secBusiness2015**, directly verified). The
  "400+ scripts / 2-3 minutes" specifics were reframed (AE-001).
- **§2 The PEEL Framework** — PEEL is a pedagogical paragraph scaffold; no empirical claim,
  no citation. (The premise that structured, evidence-backed paragraphs earn marks is the
  §1 marking-convention point.)
- **§3 The Science Answer Stack (S³S)** — S³S is a mnemonic scaffold. The verifiable claim
  underneath — method marks earned at each step, with the final answer worth only ~4-5 of
  25 marks — is the SEC partial/method-credit convention (**secMarkingSchemes**).
- **§4 The Marks-Shape Connection** — Mark allocation signals expected answer length and
  structure; "3 × 5" style allocations are separately-marked sub-parts
  (**secMarkingSchemes**). Verified convention.
- **§5 The 60% Answer** — A structured partial answer (numbered points, definitions,
  labelled diagrams, question language) lets the examiner find and award every point
  (**secMarkingSchemes** — per-label and per-point credit). Verified.
- **§6 Subject-Specific Structures** — Command-word structures (State/Explain/Example,
  Describe/Explain/Evaluate, business Point-Explain-Example-Apply) mirror what schemes and
  the Chief Examiner reward (**secBusiness2015** for the Business developed-answer pattern).
  The per-subject cards are a practical reference.
- **§7 Your Engineering Toolkit** — Recap of the four frameworks. No new claim.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| AE-001 | §1 | "Examiners read 400+ scripts. They spend 2-3 minutes per answer." → "Examiners work through large volumes of scripts under real time pressure … limited time to each answer." | The volume/time-pressure point is verifiable and emphasised in Chief Examiner reports, but the precise figures could not be verified against a locatable SEC source, so the false precision was removed. |

## Outstanding for accreditation
When examinations.ie is accessible, the per-subject command-word structures in §6 can be
spot-checked against each subject's current marking scheme / Chief Examiner report; the
Business pattern is already verified in-repo.
