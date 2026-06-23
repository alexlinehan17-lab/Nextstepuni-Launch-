# Evidence Dossier — The Science of Making Mistakes

**Module:** `science-of-making-mistakes-protocol` (`components/TheScienceOfMakingMistakesModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/scienceOfMistakes.ts`.

**Reviewer note.** Built on solid error-monitoring neuroscience: the ERN (the fast,
automatic error signal; Gehring et al. 1993), the Pe (the later error-awareness signal
whose amplitude tracks post-error correction and is modulated by mindset; Moser et al.
2011), and acute stress impairing prefrontal-cortex function (Arnsten 2009). The
mechanisms are supported. **One reframe:** the module claimed exam stress specifically
"squashes the Pe signal" — that particular finding is not established (the
anxiety/error-monitoring literature is mixed and often shows the *opposite* for the
earlier ERN), so it was cut back to the supported prefrontal-impairment mechanism. The
"amygdala hijack" term is Goleman's popularisation but maps onto the Arnsten mechanism
and is kept as framing. The Amygdala Hijack Simulator (cortisol bar, PFC/amygdala
meters) is an illustrative interaction, not claimed measurement.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| gehring1993 | Gehring, Goss, Coles, Meyer & Donchin (1993). A neural system for error detection and compensation. *Psychological Science*. | [10.1111/j.1467-9280.1993.tb00586.x](https://doi.org/10.1111/j.1467-9280.1993.tb00586.x) |
| moser2011 | Moser, Schroder, Heeter, Moran & Lee (2011). Mind your errors: evidence for a neural mechanism linking growth mind-set to adaptive posterror adjustments. *Psychological Science*. | [10.1177/0956797611419520](https://doi.org/10.1177/0956797611419520) |
| arnsten2009 | Arnsten (2009). Stress signalling pathways that impair prefrontal cortex structure and function. *Nature Reviews Neuroscience*. | [10.1038/nrn2648](https://doi.org/10.1038/nrn2648) |

---

## Claim-by-claim record

- **§1 The Brain's Alarm** — The ERN, a fast automatic neural error signal that fires
  within a fraction of a second of a mistake (**gehring1993**). Verified. (Tooltip
  softened from a hard "50 ms" to "a fraction of a second" / "about a tenth of a second"
  — the ERN onsets very fast and peaks ~80–100 ms, so the looser phrasing is safer.)
  Alex's Junior Cert story is first-person testimony, not an empirical claim.
- **§2 The Second Signal** — The Pe, a later signal reflecting conscious error awareness;
  its amplitude is linked to the likelihood of correcting the error next time
  (**moser2011**). Verified. ("literally predicts" softened to "is linked to.")
- **§3 The Mindset Switch** — Pe amplitude is modulated by mindset: growth-mindset
  individuals show a larger Pe and better post-error accuracy than fixed-mindset
  individuals (**moser2011**). Verified; tightened to "is linked to / tends to."
- **§4 The High-Stakes Hijack** — Acute stress impairs prefrontal-cortex function, making
  calm error analysis harder ("amygdala hijack") (**arnsten2009**). Verified. The
  unsupported "Pe gets squashed under stress" claim was reframed out (SOM-001).
- **§5 Your Error Toolkit** — Practical "mistake log" habit (treat errors as information,
  record cause + one fix). Reasoning/advice consistent with the cited error-monitoring
  and metacognition literature; no specific empirical stat, so no inline citation.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| SOM-001 | § 4 | "that important Pe signal gets squashed" (under stress) → acute stress weakens the prefrontal cortex | No established finding that exam stress reduces Pe amplitude (anxiety literature is mixed and often shows the opposite for ERN). Kept the supported prefrontal-impairment mechanism (Arnsten 2009). |
