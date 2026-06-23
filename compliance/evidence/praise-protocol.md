# Evidence Dossier — The Power of Praise

**Module:** `praise-protocol` (`components/ThePraiseProtocolModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/praiseProtocol.ts`.

**Reviewer note (replication-sensitive module).** This module sits in the Carol Dweck
mindset lineage, where the *broad* claim — that brief "growth-mindset interventions"
reliably raise grades — is contested. The two Sisk et al. (2018) meta-analyses found
the average mindset–achievement correlation is weak (r ≈ 0.10) and intervention effects
small and inconsistent. **Crucially, this module does not make that broad claim.** It
rests on three specific, well-replicated findings: (1) person vs. process praise changes
children's response to later failure (Mueller & Dweck 1998); (2) error-related brain
signals differ by mindset (Moser 2011); (3) naturalistic parent praise predicts later
mindset and achievement (Gunderson 2013, 2018). Those study-level claims are kept and
cited. Two pieces of **narrative gloss** were reframed: a derived "three times" ratio,
and an unverified dopamine mechanism. Sisk 2018 is logged here as balancing context but
is not cited inline (the module never asserts what it qualifies).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| mueller1998 | Mueller & Dweck (1998). Praise for intelligence can undermine children's motivation and performance. *J. Personality and Social Psychology*. | [10.1037/0022-3514.75.1.33](https://doi.org/10.1037/0022-3514.75.1.33) |
| moser2011 | Moser, Schroder, Heeter, Moran & Lee (2011). Mind your errors: evidence for a neural mechanism linking growth mind-set to adaptive posterror adjustments. *Psychological Science*. | [10.1177/0956797611419520](https://doi.org/10.1177/0956797611419520) |
| gunderson2013 | Gunderson et al. (2013). Parent praise to 1- to 3-year-olds predicts children's motivational frameworks 5 years later. *Child Development*. | [10.1111/cdev.12064](https://doi.org/10.1111/cdev.12064) |
| gunderson2018 | Gunderson et al. (2018). Parent praise to toddlers predicts fourth grade academic achievement via children's incremental mindsets. *Developmental Psychology*. | [10.1037/dev0000444](https://doi.org/10.1037/dev0000444) |
| sisk2018 *(context only)* | Sisk, Burgoyne, Sun, Butler & Macnamara (2018). To what extent and under which circumstances are growth mind-sets important to academic achievement? Two meta-analyses. *Psychological Science*. | [10.1177/0956797617739704](https://doi.org/10.1177/0956797617739704) |

---

## Claim-by-claim record

- **§1 The Praise Paradox** — Two kinds of praise (person/trait vs. process/effort) have
  different downstream effects (**mueller1998**). Framing claim; verified. The Praise
  Decoder game is a sorting exercise, not a data claim.
- **§2 The Praise Experiment** — Children praised for intelligence vs. effort diverged on
  task choice, persistence after failure, and honesty about scores; ~40% of
  ability-praised children misrepresented their scores (**mueller1998**, Studies 1–6).
  Verified. The "three times more honest" ratio was reframed to "far more honest"
  (PRAISE-001) — the 40% figure is the paper's; the ratio was not.
- **§3 The Brain on Praise** — Error-related brain activity (the Pe component) is larger
  in growth-mindset individuals and is associated with greater post-error attention and
  improved accuracy on the next trial (**moser2011**). Verified. The preceding dopamine
  "wiring" mechanism was reframed (PRAISE-002) as unsupported popularisation; the
  behavioural point it carried is supported by Mueller & Dweck.
- **§4 The Real World Data** — Naturalistic parent process praise (averaging ~18% of
  praise) at ages 1–3 predicted a stronger incremental/growth framework five years later
  (**gunderson2013**); a follow-up linked that early praise to fourth-grade Maths and
  reading achievement, mediated by the child's mindset (**gunderson2018**). The gender
  difference in praise type is from Gunderson 2013. Verified. "Led to better results"
  softened to "predicted… with mindset as the link" (mediation, not RCT); the
  girls→fixed-mindset line kept its hedge ("may be one reason").
- **§5 The 'Effort' Trap** — Conceptual guidance (effort praise without strategy =
  "consolation"; tie effort to what worked). Drawn from Dweck's later writing on "false
  growth mindset"; framed as practical reasoning, not an empirical stat, so no citation
  attached.
- **§6 The Feedback Audit** — Reflective action prompt; no empirical claim.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| PRAISE-001 | § 2 | "three times more honest" → "far more honest" | The 40% figure is in Mueller & Dweck 1998 and is kept + cited; the precise ratio is a derived comparison not stated in the paper. |
| PRAISE-002 | § 3 | dopamine "wired to effort / craves effort" mechanism → behavioural framing of person vs. process praise | The dopamine pathway is popularised overreach; the supported claim (helpless vs. mastery response to failure) is retained, and the error-signal claim is cited to Moser 2011. |
