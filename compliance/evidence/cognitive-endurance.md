# Evidence Dossier — Cognitive Endurance

**Module:** `cognitive-endurance-protocol` (`components/CognitiveEnduranceModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/cognitiveEndurance.ts`.

**Outcome:** Mostly well-evidenced neuroscience/performance claims. Two overreaching
claims reframed (CE-001 mouth-rinse "mental boost"; CE-002 NSDR "single most
effective"). Dietary "sugar crash" and the 20-20-20 eye-rule are retained as hedged
practical guidance (see notes).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| raichle2002 | Raichle & Gusnard (2002). Appraising the brain's energy budget. *PNAS*. | [10.1073/pnas.172399499](https://doi.org/10.1073/pnas.172399499) |
| mcewen1998 | McEwen (1998). Protective and damaging effects of stress mediators. *NEJM*. | [10.1056/nejm199801153380307](https://doi.org/10.1056/nejm199801153380307) |
| walker2009 | Walker & van der Helm (2009). Overnight therapy? The role of sleep in emotional brain processing. *Psychological Bulletin*. | [10.1037/a0016570](https://doi.org/10.1037/a0016570) |
| chambers2009 | Chambers, Bridge & Jones (2009). Carbohydrate sensing in the human mouth. *J. Physiology*. | [10.1113/jphysiol.2008.164285](https://doi.org/10.1113/jphysiol.2008.164285) |
| arnsten2009 | Arnsten (2009). Stress signalling pathways that impair prefrontal cortex structure and function. *Nature Reviews Neuroscience*. | [10.1038/nrn2648](https://doi.org/10.1038/nrn2648) |
| balban2023 | Balban et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine*. | [10.1016/j.xcrm.2022.100895](https://doi.org/10.1016/j.xcrm.2022.100895) |

---

## Claim-by-claim record

- **§1 Marathon Mindset** — Brain uses ~20% of body energy (**raichle2002**); cumulative
  stress ("stress load") produces wear and tear — the allostatic-load concept
  (**mcewen1998**). Verified. The allostatic-load charts use illustrative data, not
  study results.
- **§2 Sleep** — REM sleep (concentrated in later cycles) supports problem-solving and
  emotional regulation; cutting sleep short sacrifices it (**walker2009**). Verified.
  The Sleep Cycle Architect's REM-loss % is computed from an illustrative model
  hypnogram. Mouth-rinse cited (**chambers2009**); see CE-001.
- **§3 Fueling** — Brain runs on glucose (background, **raichle2002**). The
  carbohydrate **mouth-rinse** mechanism is evidenced for effort/endurance
  (**chambers2009**); claim reframed (CE-001). *Note:* the "high-GI → spike-and-crash
  mid-exam" claim is retained as hedged ("can…") general nutritional guidance; the
  cognitive-performance evidence is mixed, so it is not presented as a strong empirical
  finding.
- **§4 In-Exam Toolkit** — Acute stress impairs prefrontal "thinking brain" function and
  shifts control to amygdala-driven responses (**arnsten2009**). The **physiological
  sigh** (cyclic sighing) reduces physiological arousal (**balban2023**). Verified.
  *Note:* the 20-20-20 eye-rule is a standard optometric recommendation retained as
  practical guidance (limited trial evidence).
- **§5 Training Plan** — Progressive build-up of focus duration; framed as practical
  application of progressive overload / deliberate practice. No strong standalone claim.
- **§6 Recovery** — Active recovery (walking, guided relaxation) over "junk rest." NSDR
  recommendation reframed from a superlative (CE-002); breathing tool retained
  (**balban2023**).

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| CE-001 | § 3 | mouth rinse "real mental boost in the final hour" → evidenced for effort/endurance; "may" help mentally, evidence "less settled" | Mouth-rinse benefit established for physical effort (chambers2009), not for exam-type cognition. |
| CE-002 | § 6 | NSDR "the single most effective way to recharge" → "one of the best ways" | Superlative unsupported; NSDR/yoga-nidra evidence base limited. |
