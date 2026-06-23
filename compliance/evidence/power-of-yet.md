# Evidence Dossier — The Power of "Yet"

**Module:** `power-of-yet-protocol` (`components/ThePowerOfYetModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/powerOfYet.ts`.

**Reviewer note (replication-sensitive lineage).** A Dweck-lineage "growth mindset"
module, but a low-risk one: it does not claim that adopting "yet" raises grades (the
contested broad claim; see Sisk et al. 2018). Instead it rests on two supported points —
(1) error-related brain activity is modulated by mindset (Moser et al. 2011), and (2)
turning "yet" into a *specific, concrete* next step is an implementation intention, which
research shows beats vague intentions (Gollwitzer 1999). **One reframe:** the "Chicago
school replaced Fail with Not Yet and students tried harder" example is from Dweck's TED
talk, not a study, and its effort/achievement outcome is unverifiable — the grading
practice is kept as illustration, the outcome claim removed. The Yet Reframe / Bridge
Builder / Yet Audit widgets are interactive exercises, not data claims.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| moser2011 | Moser, Schroder, Heeter, Moran & Lee (2011). Mind your errors: evidence for a neural mechanism linking growth mind-set to adaptive posterror adjustments. *Psychological Science*. | [10.1177/0956797611419520](https://doi.org/10.1177/0956797611419520) |
| gollwitzer1999 | Gollwitzer (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*. | [10.1037/0003-066x.54.7.493](https://doi.org/10.1037/0003-066x.54.7.493) |

---

## Claim-by-claim record

- **§1 The Full Stop** — Fixed-mindset "I can't" framing as a self-imposed dead end.
  Conceptual framing; no specific empirical stat, no inline citation.
- **§2 The Software Patch** — Adding "yet" reframes a verdict as a progress update; some
  schools use "Not Yet" grading. Illustration retained; the unverifiable Chicago outcome
  claim reframed out (POY-001).
- **§3 The Brain on "Yet"** — Error-monitoring brain activity is modulated by mindset:
  growth-oriented individuals show a stronger error-attention signal and engage with the
  mistake, fixed-oriented individuals a weaker one (**moser2011**). Verified; tightened
  to "tends to / in one study."
- **§4 The Action Bridge** — Following "yet" with a specific, concrete next step (vs a
  vague "try harder") is an implementation intention, which reliably improves follow-
  through (**gollwitzer1999**). Verified.
- **§5 Your "Yet" Audit** — Application exercise (identify block → add yet → bridge to
  action). No new empirical claim.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| POY-001 | § 2 | "A school in Chicago replaced Fail with Not Yet and students started trying harder and finishing more work" → the "Not Yet" grading practice kept as illustration, outcome removed | The example is from Dweck's 2014 TED talk, not peer-reviewed; the specific effort/achievement outcome is unverifiable. |
