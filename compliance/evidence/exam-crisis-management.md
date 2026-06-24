# Evidence Dossier — Exam Crisis Management

**Module:** `exam-crisis-management-protocol` (`components/ExamCrisisManagementModule.tsx`)
**Group:** B (exam) — but the load-bearing claims are cognitive / physiological
science, so this one is grounded in peer-reviewed DOI sources like Group A.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. Sources
surface via inline `Cite` markers + the **References** button; data in
`data/references/examCrisisManagement.ts`.

**Note.** Sits in Exam Zone, but its substance is the science of performing under
acute stress: stress narrowing prefrontal access, paced breathing lowering arousal,
emotional contagion, sleep banking, overnight metabolite clearance, and low-GI
breakfast and cognition. The WRAP crisis-plan and the 7-day countdown are a practical
self-management framework / procedure and carry **no citation**. Two nutrition claims
were softened (see Reframed content).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| arnsten2009 | Arnsten (2009). Stress signalling pathways that impair prefrontal cortex structure and function. *Nature Reviews Neuroscience*. | [10.1038/nrn2648](https://doi.org/10.1038/nrn2648) |
| balban2023 | Balban et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine*. | [10.1016/j.xcrm.2022.100895](https://doi.org/10.1016/j.xcrm.2022.100895) |
| hatfield1993 | Hatfield, Cacioppo & Rapson (1993). Emotional contagion. *Current Directions in Psychological Science*. | [10.1111/1467-8721.ep10770953](https://doi.org/10.1111/1467-8721.ep10770953) |
| rupp2009 | Rupp, Wesensten, Bliese & Balkin (2009). Banking sleep: Realization of benefits during subsequent sleep restriction and recovery. *Sleep*. | [10.1093/sleep/32.3.311](https://doi.org/10.1093/sleep/32.3.311) |
| xie2013 | Xie et al. (2013). Sleep drives metabolite clearance from the adult brain. *Science*. | [10.1126/science.1241224](https://doi.org/10.1126/science.1241224) |
| micha2011 | Micha, Rogers & Nelson (2011). Glycaemic index and glycaemic load of breakfast predict cognitive function and mood in school children: A randomised controlled trial. *British Journal of Nutrition*. | [10.1017/S0007114511002303](https://doi.org/10.1017/S0007114511002303) |

All six DOIs verified against CrossRef.

---

## Claim-by-claim record

- **§1 Why You "Go Blank"** — Going blank is an acute stress response: the "alarm brain
  hijacks the thinking brain" and memory access is temporarily cut off. Grounded in the
  prefrontal-cortex effects of acute stress (**arnsten2009**). The hot/cold-cognition
  framing is illustrative.
- **§2 The "Blank Mind" Fix** — The Physiological Sigh (double inhale, long exhale)
  calms the nervous system fastest. This is the cyclic-sighing protocol that
  **balban2023** found most effective for reducing physiological arousal. Sensory
  grounding and the "easy win" are practical techniques.
- **§3 Protect Your Head After Exams** — "Other people's panic is contagious": emotional
  contagion, the tendency to catch others' affective states (**hatfield1993**). The
  post-exam ban and uncertainty-tolerance advice are practical strategy.
- **§4 Sleep: Your Secret Weapon** — Sleep banking: extending sleep beforehand builds a
  reserve that buffers later restriction (**rupp2009**). The overnight "cleaning cycle"
  flushing metabolic waste is glymphatic clearance during sleep (**xie2013**). Both
  verified.
- **§5 Food and Focus** — A slower-release (lower-GI) breakfast is linked to steadier
  cognitive function and mood in school children through the morning (**micha2011**,
  RCT). The deterministic "sugar crash mid-exam" wording and the L-theanine "calm focus"
  aside were softened (ECM-001, ECM-002). Caffeine tapering is presented as practical
  advice.
- **§6 Your Personal Crisis Plan** — The WRAP (Wellness Recovery Action Plan) is a named
  self-management framework, presented as a tool; no empirical citation attached.
- **§7 The 7-Day Countdown** — Tapering caffeine, shifting sleep to exam times, steady-
  energy food, easing off study. Practical scheduling advice; the underlying sleep and
  nutrition points are cited in §4–§5.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| ECM-001 | §5 | "quick-burn foods … cause a crash that will hit you right in the middle of your exam" → "can leave your energy dipping partway through … a slower-release breakfast is linked to steadier concentration in students" | RCT (micha2011) supports lower-GI breakfast → better morning cognition/mood, but not a guaranteed mid-exam crash in healthy students; deterministic causal claim softened. |
| ECM-002 | §5 | "tea … has a natural ingredient that gives you calm focus without the jitters" → "many people find it a gentler lift than coffee" | The implied L-theanine mechanism has mixed RCT support and was uncited; reframed to a non-prescriptive experiential statement rather than attach a borderline claim. |
