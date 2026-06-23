# Evidence Dossier — The Implementation Playbook

**Module:** `implementation-protocol` (`components/TheImplementationProtocolModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/implementationProtocol.ts`.

**Reviewer note.** An exemplary module for this review: every quantitative claim is the
headline figure of a specific, locatable study, and each was verified. The intention-action
gap (intentions explain ~28% of behaviour) is Sheeran's review (Sheeran 2002);
implementation intentions ("if-then" plans) are Gollwitzer (1999), with the "94 studies,
roughly doubled follow-through" figure from the Gollwitzer & Sheeran (2006) meta-analysis;
temptation bundling and the "+51% gym attendance" result are Milkman, Minson & Volpp
(2014); and the self-imposed-deadlines / commitment-device finding is Ariely & Wertenbroch
(2002). **No content cut** — the figures match their sources. (The "over 400 studies"
phrasing reflects Sheeran 2002 synthesising prior meta-analyses; the precise variance
figure ~28% / R² ≈ .28 is the paper's own.) The Intention-Action Gap chart and If-Then Plan
Builder are illustrative/practical tools (the chart curves are stylised, not study data).

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| sheeran2002 | Sheeran (2002). Intention–behavior relations: A conceptual and empirical review. *European Review of Social Psychology*. | [10.1080/14792772143000003](https://doi.org/10.1080/14792772143000003) |
| gollwitzer1999 | Gollwitzer (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*. | [10.1037/0003-066x.54.7.493](https://doi.org/10.1037/0003-066x.54.7.493) |
| gollwitzerSheeran2006 | Gollwitzer & Sheeran (2006). Implementation intentions and goal achievement: A meta-analysis of effects and processes. *Advances in Experimental Social Psychology*. | [10.1016/s0065-2601(06)38002-1](https://doi.org/10.1016/s0065-2601(06)38002-1) |
| milkman2014 | Milkman, Minson & Volpp (2014). Holding the Hunger Games hostage at the gym: An evaluation of temptation bundling. *Management Science*. | [10.1287/mnsc.2013.1784](https://doi.org/10.1287/mnsc.2013.1784) |
| arielyWertenbroch2002 | Ariely & Wertenbroch (2002). Procrastination, deadlines, and performance: Self-control by precommitment. *Psychological Science*. | [10.1111/1467-9280.00441](https://doi.org/10.1111/1467-9280.00441) |

---

## Claim-by-claim record

- **§1 The Intention-Action Gap** — Intentions explain only ~28% of behaviour; motivation
  alone is a weak predictor of action (**sheeran2002**). Verified.
- **§2 If-Then Plans** — Implementation intentions (**gollwitzer1999**) roughly double
  follow-through across 94 studies (**gollwitzerSheeran2006**). Verified.
- **§3 Temptation Bundling** — Pairing a "want" exclusively with a "should" (audiobooks at
  the gym) raised attendance ~51% (**milkman2014**). Verified.
- **§4 Commitment Devices** — Self-imposed deadlines with penalties beat total flexibility
  (**arielyWertenbroch2002**). Verified.
- **§5 Building Your Protocol** — Combines the above; if-then plans are especially helpful
  for harder goals / those who struggle with follow-through (**gollwitzerSheeran2006**).
  Verified.

---

## Reframed content
None cut. Every quantitative claim matches its cited primary source; no removals, so no
`data/cutContent.ts` entry for this module.
