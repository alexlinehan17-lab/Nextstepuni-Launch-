# Evidence Dossier — Game Day: Peak Performance

**Module:** `game-day-protocol` (`components/GameDayModule.tsx`)
**Group:** B (exam) — built on a sports-science analogy, but the load-bearing
claims are cognitive/physiological science, so it is grounded in peer-reviewed
DOI sources like Group A.
**Review date:** 2026-06-24
**Reviewer:** Pre-accreditation review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what a real, locatable source supports. Sources
surface via inline `Cite` markers + the **References** button; data in
`data/references/gameDay.ts`.

**Note.** The periodisation framing (macrocycle/mesocycle/microcycle, "exam athlete")
and the warm-up / packing routines are practical scaffolding and carry **no
citation**; the underlying empirical claims they hang on are cited. One athletic-taper
claim was softened (see Reframed content).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| raichle2002 | Raichle & Gusnard (2002). Appraising the brain's energy budget. *PNAS*. | [10.1073/pnas.172399499](https://doi.org/10.1073/pnas.172399499) |
| seery2011 | Seery (2011). Challenge or threat? Cardiovascular indexes of resilience and vulnerability to potential stress in humans. *Neuroscience & Biobehavioral Reviews*. | [10.1016/j.neubiorev.2011.03.003](https://doi.org/10.1016/j.neubiorev.2011.03.003) |
| micha2011 | Micha, Rogers & Nelson (2011). Glycaemic index and glycaemic load of breakfast predict cognitive function and mood in school children: An RCT. *British Journal of Nutrition*. | [10.1017/S0007114511002303](https://doi.org/10.1017/S0007114511002303) |
| rk2006 | Roediger & Karpicke (2006). Test-enhanced learning. *Psychological Science*. | [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x) |
| wixted2004 | Wixted (2004). The psychology and neuroscience of forgetting. *Annual Review of Psychology*. | [10.1146/annurev.psych.55.090902.141555](https://doi.org/10.1146/annurev.psych.55.090902.141555) |
| pham1999 | Pham & Taylor (1999). From thought to action: Effects of process- versus outcome-based mental simulations on performance. *PSPB*. | [10.1177/0146167299025002010](https://doi.org/10.1177/0146167299025002010) |
| scullin2018 | Scullin et al. (2018). The effects of bedtime writing on difficulty falling asleep. *J. Experimental Psychology: General*. | [10.1037/xge0000374](https://doi.org/10.1037/xge0000374) |
| balban2023 | Balban et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine*. | [10.1016/j.xcrm.2022.100895](https://doi.org/10.1016/j.xcrm.2022.100895) |
| hatfield1993 | Hatfield, Cacioppo & Rapson (1993). Emotional contagion. *Current Directions in Psychological Science*. | [10.1111/1467-8721.ep10770953](https://doi.org/10.1111/1467-8721.ep10770953) |

All nine DOIs verified against CrossRef.

---

## Claim-by-claim record

- **§1 The Athlete Mindset** — "Your brain uses 20% of your body's energy"
  (**raichle2002**, brain's energy budget). Challenge vs threat states — the
  challenge state's better blood flow / performance vs the threat state's
  vasoconstriction and impaired thinking (**seery2011**). The ChallengeThreat
  simulator is illustrative.
- **§2 1 Month Out** — Slow-release (lower-GI) foods give steadier morning cognition
  (**micha2011**). Adolescent circadian phase delay ("most teenagers are night owls")
  is stated as general background; the actionable advice (shift sleep gradually) is
  practical.
- **§3 The Final Week** — Testing yourself beats re-reading (**rk2006**). Stopping new
  material because last-minute cramming can displace older memories is retroactive
  interference (**wixted2004**). The athletic-taper "40-60%" claim was softened
  (GD-001); the Performance = Knowledge − Tiredness line is an illustrative framing.
- **§4 Mental Rehearsal** — Process simulation (rehearsing the steps) improves
  performance where outcome simulation (picturing the grade) can backfire
  (**pham1999**, the original process-vs-outcome study).
- **§5 The Day Before** — A pre-bed "brain dump" of what's on your mind helps you fall
  asleep: bedtime writing (especially to-do offloading) sped sleep onset in a
  polysomnographic study (**scullin2018**). Packing ritual and slow-release dinner are
  practical (dinner echoes micha2011).
- **§6 Game Day Morning** — Hydration, morning daylight, and the cognitive warm-up are
  presented as practical routines; the slow-energy breakfast point is the **micha2011**
  claim from §2. No new empirical assertion needing its own citation.
- **§7 In The Arena** — The Physiological Sigh lowers arousal fastest (**balban2023**,
  cyclic sighing). The 5-minute read-first rule is practical strategy.
- **§8 Halftime & Post-Game** — "Don't compare answers": emotional contagion spreads
  others' panic into your next paper (**hatfield1993**). The light meal and NSDR/nap
  recharge are practical recovery advice.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| GD-001 | §3 | "Cutting your study hours by 40-60% … actually improves your performance because you go in fresh" → "… helps you go in fresh instead of burnt out" | The athletic taper improving competition performance is established, but the quantified transfer to exam performance is an unstudied extrapolation; the avoid-burnout rationale is kept, the asserted performance gain removed. |
