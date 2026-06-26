# Evidence Dossier — Exam Hall Strategies

**Module:** `exam-hall-strategies-protocol` (`components/ExamHallStrategiesModule.tsx`)
**Group:** B (exam) — but the load-bearing claims are cognitive science, so this one
is grounded in peer-reviewed DOI sources like Group A.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. Sources
surface via inline `Cite` markers + the **References** button; data in
`data/references/examHallStrategies.ts`.

**Note.** This sits in Exam Zone, but its substance is the cognitive science of
performing under pressure: acute stress narrowing prefrontal access, the
expressive-writing ("brain dump") effect, incubation, and slow paced breathing.
The remaining content — reading-time triage, the traffic-light/anchor system,
minutes-per-mark budgeting, the hard-stop, and the practice drills — is practical
exam strategy (procedural advice, not an empirical claim) and so carries **no
citation**. **No content cut.**

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| arnsten2009 | Arnsten (2009). Stress signalling pathways that impair prefrontal cortex structure and function. *Nature Reviews Neuroscience*. | [10.1038/nrn2648](https://doi.org/10.1038/nrn2648) |
| ramirez2011 | Ramirez & Beilock (2011). Writing about testing worries boosts exam performance in the classroom. *Science*. | [10.1126/science.1199427](https://doi.org/10.1126/science.1199427) |
| sio2009 | Sio & Ormerod (2009). Does incubation enhance problem solving? A meta-analytic review. *Psychological Bulletin*. | [10.1037/a0014212](https://doi.org/10.1037/a0014212) |
| balban2023 | Balban et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine*. | [10.1016/j.xcrm.2022.100895](https://doi.org/10.1016/j.xcrm.2022.100895) |

All four DOIs verified against CrossRef.

---

## Claim-by-claim record

- **§1 Knowing vs. Showing It** — Acute stress imposes extra mental load that "steals
  the brainpower you need for the actual questions." Grounded in the prefrontal-cortex
  effects of acute stress (**arnsten2009**). The competence/performance framing itself
  is illustrative, not a single empirical claim.
- **§2 The Brain Dump** — "Stress hormones spike, which can block access to your memory"
  (**arnsten2009**). The brain-dump device — writing fragile facts / exam worries down
  in the first minutes — is supported by the expressive-writing-before-exams effect:
  writing about testing worries raised classroom exam performance (**ramirez2011**).
  Framed as "tend to score higher," matching the study's effect, not a guarantee.
- **§3 Reading Time Triage** — Traffic-light sorting, anchor questions. Practical
  strategy; no citation.
- **§4 Order of Attack** — "Stepping away can sometimes help" when you skip and return:
  the incubation effect (**sio2009**). *Reframed after the verification pass (EHS-001):
  Sio & Ormerod find incubation helps most for divergent tasks and least when the break is
  filled with other high-demand work — exactly the exam case — so the earlier prescriptive
  "your brain keeps working … the answer often clicks when you come back" was softened to
  non-prescriptive "can sometimes help."* The 30-second rule and momentum framing are
  practical heuristics.
- **§5 Time Budgeting** — Minutes-per-mark, hard-stop, the sunk-cost trap. Exam-time
  arithmetic and decision framing; no empirical citation attached.
- **§6 Staying Calm Under Pressure** — Slow, structured breathing lowers physiological
  arousal (**balban2023**, a randomised study of brief structured respiration), with Box
  Breathing presented as one such pattern. *Reframed after the verification pass
  (EHS-002): balban2023's significant arousal reduction is for breathwork broadly
  (especially cyclic sighing) over daily practice, not box-breathing-specific or an acute
  "calms in under a minute" effect — so those specifics were dropped and the claim narrowed
  to "slow structured breathing settles the nervous system."* The 3-3-3 grounding and
  reappraisal/reframing tools are practical techniques without an empirical citation.
- **§7 Practice Drills** — Exam wrappers and timed drills. Practical metacognitive
  advice; no citation.

---

## Reframed content (also logged in `data/cutContent.ts`)
Nothing was cut at first review. The independent verification pass (2026-06-26) then
softened two claims to match their sources:

| ID | Section | Reframe | Reason |
|----|---------|---------|--------|
| EHS-001 | §4 | "your brain keeps working on it … the answer often clicks when you come back" → "stepping away can sometimes help" | sio2009 finds incubation weakest exactly in the exam case (break filled with other hard questions); prescriptive overreach softened. |
| EHS-002 | §6 | "the fastest trick is Box Breathing … calms your nervous system in under a minute" → "slow, structured breathing … settles your nervous system" | balban2023 supports structured breathwork broadly (esp. cyclic sighing) over daily practice, not box-breathing-specific acute rescue. |
