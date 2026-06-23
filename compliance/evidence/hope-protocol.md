# Evidence Dossier — The Science of Hope

**Module:** `hope-protocol` (`components/HopeProtocolModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/hopeProtocol.ts`.

**Reviewer note.** Built on Snyder's Hope Theory (hope = agency/"willpower" +
pathways/"waypower"; Snyder et al. 1991), wrapped in an engineering metaphor and combined
with adolescent dual-systems neuroscience (Casey et al. 2008), episodic future thinking
(Peters & Büchel 2010), stress/cortisol effects on cognition (Lupien et al. 2009) and
training-induced neuroplasticity (Draganski et al. 2004). All five constructs are well
sourced. **One reframe:** §3 over-attributed episodic future thinking's motivational pull
to an on-demand "dopamine hit" — Peters & Büchel (2010) showed EFT reduces delay
discounting via prefrontal-mediotemporal interactions, not a dopamine release, so the
neurochemical specifics were softened to the supported effect. One tightening: cortisol
"shuts down clear thinking" → "can impair clear thinking" (cited to Lupien 2009). The
Dopamine Dial, Cortisol Curve, Brain Mismatch and Hope Map widgets are illustrative
interactions, not measured data.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| snyder1991 | Snyder et al. (1991). The will and the ways: Development and validation of an individual-differences measure of hope. *J. Personality and Social Psychology*. | [10.1037/0022-3514.60.4.570](https://doi.org/10.1037/0022-3514.60.4.570) |
| casey2008 | Casey, Jones & Hare (2008). The adolescent brain. *Annals of the New York Academy of Sciences*. | [10.1196/annals.1440.010](https://doi.org/10.1196/annals.1440.010) |
| petersbuchel2010 | Peters & Büchel (2010). Episodic future thinking reduces reward delay discounting through an enhancement of prefrontal-mediotemporal interactions. *Neuron*. | [10.1016/j.neuron.2010.03.026](https://doi.org/10.1016/j.neuron.2010.03.026) |
| lupien2009 | Lupien, McEwen, Gunnar & Heim (2009). Effects of stress throughout the lifespan on the brain, behaviour and cognition. *Nature Reviews Neuroscience*. | [10.1038/nrn2639](https://doi.org/10.1038/nrn2639) |
| draganski2004 | Draganski et al. (2004). Changes in grey matter induced by training. *Nature*. | [10.1038/427311a](https://doi.org/10.1038/427311a) |

---

## Claim-by-claim record

- **§1 De-Coding Hope** — Hope = goals + agency (willpower) + pathways (waypower), a
  trainable cognitive set (**snyder1991**). Verified. Myth-buster cards are interactive.
- **§2 Your Brain's Circuit Board** — Adolescent "developmental mismatch": limbic/reward
  systems mature ahead of the prefrontal cortex (**casey2008**). Verified.
- **§3 Willpower** — Episodic future thinking (vividly simulating future success) makes
  future rewards more motivating now (**petersbuchel2010**). Verified; the "dopamine on
  demand" mechanism reframed (HP-001).
- **§4 Waypower** — Pathways thinking — planning, flexibility, problem-solving — is the
  second pillar of hope (**snyder1991**). Verified.
- **§5 Stress Shield** — Chronically elevated cortisol impairs memory and thinking
  (**lupien2009**); appraising an exam as a solvable problem (vs a disaster) lowers the
  threat response. Verified; "shuts down" softened to "can impair."
- **§6 Upgrading the Hardware** — Practising planning/goal-setting strengthens neural
  pathways — use-dependent neuroplasticity (**draganski2004**). Verified.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| HP-001 | § 3 | "trigger dopamine on demand / a small upfront hit of dopamine" → "switch on your reward system deliberately / an upfront motivation boost" | EFT is cited (Peters & Büchel 2010), but that study showed reduced delay discounting via prefrontal-mediotemporal interactions, not an on-demand dopamine release; the neurochemical specifics were over-attributed. |
