# Evidence Dossier — The Myelin Manual

**Module:** `myelin-manual-protocol` (`components/TheMyelinManualModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/myelinManual.ts`.

**Reviewer note (flagged module):** Built on Daniel Coyle's popular *The Talent Code*
framing ("deep practice → myelin"). Flagged for heavy scrutiny. **Verdict: the core
science is now genuinely supported** — activity-dependent / adaptive myelination was
validated by primary research *after* Coyle's book (Gibson 2014; McKenzie 2014). The
overreach was in the narrative gloss, not the mechanism, so **two reframes** rather than
a rewrite: (1) the claim that the *feeling of struggle* literally "places the order" for
myelin; (2) the claim that myelinated skills are "permanent" (contradicting the prior
module's use-it-or-lose-it juggling study).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| gibson2014 | Gibson et al. (2014). Neuronal activity promotes oligodendrogenesis and adaptive myelination in the mammalian brain. *Science*. | [10.1126/science.1252304](https://doi.org/10.1126/science.1252304) |
| mckenzie2014 | McKenzie et al. (2014). Motor skill learning requires active central myelination. *Science*. | [10.1126/science.1254960](https://doi.org/10.1126/science.1254960) |
| scholz2009 | Scholz, Klein, Behrens & Johansen-Berg (2009). Training induces changes in white-matter architecture. *Nature Neuroscience*. | [10.1038/nn.2412](https://doi.org/10.1038/nn.2412) |
| ericsson1993 | Ericsson, Krampe & Tesch-Römer (1993). The role of deliberate practice in the acquisition of expert performance. *Psychological Review*. | [10.1037/0033-295x.100.3.363](https://doi.org/10.1037/0033-295x.100.3.363) |
| sb2015 | Soderstrom & Bjork (2015). Learning versus performance. *Perspectives on Psychological Science*. | [10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000) |

---

## Claim-by-claim record

- **§1 The Silent Revolution** — Oligodendrocytes myelinate axons; myelin speeds neural
  conduction (**gibson2014**). Verified. The Myelin Wrapper sim is illustrative (its
  m/s values are within the rough real range of conduction velocities, not a study
  result).
- **§2 The Signal of Struggle** — Neural activity from focused practice drives
  myelination ("activity-dependent / adaptive myelination") (**gibson2014**,
  **mckenzie2014**). Verified. The narrative that the *feeling of struggle* "places the
  order for myelin" was reframed (MM-001).
- **§3 Deep Practice** — Effortful, error-rich, edge-of-ability practice ("deep
  practice") drives skill — i.e. deliberate practice (**ericsson1993**) at a desirable
  difficulty (**sb2015**). Verified.
- **§4 The Mastery Metaphors** — Broadband / dirt-road→motorway metaphors for white-matter
  changes with training (**scholz2009**). Illustrative; verified.
- **§5 The Rules of Myelination** — A "sweet spot" of effortful, error-correcting practice
  (**sb2015**); skill is durable but slow to build. The "permanent / sticks for good"
  claim was reframed (MM-002) for consistency with use-it-or-lose-it (draganski2004,
  prior module).

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| MM-001 | § 2 | "struggle = your brain placing the order for myelin; no struggle, no upgrade" → effortful focused practice drives the change | Activity-dependent myelination is real (gibson2014, mckenzie2014), but the *feeling of struggle* as the literal myelin trigger is popularised overreach. |
| MM-002 | § 5 | "permanent … sticks for good" → "durable but reversible if abandoned" | Contradicts use-it-or-lose-it (draganski2004 juggling study reversal); reframed for internal consistency. |
