# Evidence Dossier — Using Controllable Variables to Grow

**Module:** `controllable-variables-protocol` (`components/ControllableVariablesModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/controllableVariables.ts`.

**Reviewer note.** A physiology-of-performance module (sleep, nutrition, exercise) — the
most empirically dense in the set, with eight verified primary/secondary sources. The
mechanisms are all well supported: adolescent prefrontal development (Casey 2008), the
sleep-deprivation prefrontal–amygdala "decoupling" (Yoo 2007), sleep-dependent memory
consolidation (Diekelmann & Born 2010), the cumulative cost of chronic sleep restriction
(Van Dongen 2003), the wakefulness ≈ alcohol-impairment equivalence (Dawson & Reid
1997), the brain's ~20% share of energy use (Raichle & Gusnard 2002), exercise-driven
BDNF / brain health (Cotman 2007), and sleep loss shifting the leptin/ghrelin appetite
hormones (Spiegel 2004). **Two reframes**, both about over-precise numbers that could not
be traced to a locatable source: a "17% working-memory drop / A-to-C" claim, and a "30%"
simulator milestone + a "1% dehydration impairs working memory" line + a "legally drunk"
label. The verified directional/qualitative versions were kept and cited; an over-strong
"exercise will make you learn faster" causal line was also softened to "is linked to."
The Glycemic Index, Cognitive Impairment Clock and Checklist widgets are illustrative.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| casey2008 | Casey, Jones & Hare (2008). The adolescent brain. *Annals of the New York Academy of Sciences*. | [10.1196/annals.1440.010](https://doi.org/10.1196/annals.1440.010) |
| yoo2007 | Yoo, Gujar, Hu, Jolesz & Walker (2007). The human emotional brain without sleep — a prefrontal amygdala disconnect. *Current Biology*. | [10.1016/j.cub.2007.08.007](https://doi.org/10.1016/j.cub.2007.08.007) |
| diekelmann2010 | Diekelmann & Born (2010). The memory function of sleep. *Nature Reviews Neuroscience*. | [10.1038/nrn2762](https://doi.org/10.1038/nrn2762) |
| vandongen2003 | Van Dongen, Maislin, Mullington & Dinges (2003). The cumulative cost of additional wakefulness. *Sleep*. | [10.1093/sleep/26.2.117](https://doi.org/10.1093/sleep/26.2.117) |
| dawson1997 | Dawson & Reid (1997). Fatigue, alcohol and performance impairment. *Nature*. | [10.1038/40775](https://doi.org/10.1038/40775) |
| raichle2002 | Raichle & Gusnard (2002). Appraising the brain's energy budget. *PNAS*. | [10.1073/pnas.172399499](https://doi.org/10.1073/pnas.172399499) |
| cotman2007 | Cotman, Berchtold & Christie (2007). Exercise builds brain health: key roles of growth factor cascades and inflammation. *Trends in Neurosciences*. | [10.1016/j.tins.2007.06.011](https://doi.org/10.1016/j.tins.2007.06.011) |
| spiegel2004 | Spiegel, Tasali, Penev & Van Cauter (2004). Sleep curtailment … decreased leptin, elevated ghrelin, increased hunger. *Annals of Internal Medicine*. | [10.7326/0003-4819-141-11-200412070-00008](https://doi.org/10.7326/0003-4819-141-11-200412070-00008) |

---

## Claim-by-claim record

- **§1 The Performance Engine** — The adolescent prefrontal cortex is still developing
  (**casey2008**); under sleep loss the prefrontal–amygdala connection decouples
  ("neural decoupling") (**yoo2007**). Verified.
- **§2 Sleep** — Sleep consolidates memory (encoding → hippocampus → consolidation, SWS
  for declarative) (**diekelmann2010**); chronic sleep restriction accrues a growing
  cognitive deficit (**vandongen2003**); ~17 h awake ≈ BAC 0.05% impairment
  (**dawson1997**). Verified. The "17%/A-to-C" precision was reframed (CV-001); simulator
  "30%"/"legally drunk" reframed (CV-002).
- **§3 Nutrition** — The brain consumes ~20% of the body's energy (**raichle2002**);
  high-GI spike-and-crash vs low-GI steady release. Verified. The "1% dehydration impairs
  working memory" line softened (CV-002).
- **§4 Exercise** — Exercise raises BDNF and supports brain plasticity/health
  (**cotman2007**). Verified; "will learn faster" softened to "is linked to."
- **§5 The Vicious Cycle** — Sleep loss lowers leptin and raises ghrelin, increasing
  appetite/cravings (**spiegel2004**); poor diet in turn disrupts deep sleep. Verified.
- **§6 The Blueprint** — Practical daily checklist; application, no new empirical claim.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| CV-001 | § 2 | "working memory drops by ~17% … A to a C" → "takes a real hit … a cumulative cognitive deficit" | Directional claim supported (Van Dongen 2003); the precise 17% and the grade equivalence are untraceable to a source. |
| CV-002 | § 2 / § 3 | sim "30%" + "LEGALLY DRUNK"; "1% dehydration impairs working memory" → qualitative wording | The numbers are untraceable and "legally drunk" is jurisdiction-specific; the alcohol-equivalence core is kept and cited (Dawson & Reid 1997). |
