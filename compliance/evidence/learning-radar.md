# Evidence Dossier — The Learning Radar

**Module:** `learning-radar-protocol` (`components/TheLearningRadarModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/learningRadar.ts`.

**Outcome:** Strong underlying metacognition science, but this module needed the most
care so far — **three reframes**: two unverifiable statistics and one popular-but-false
visualisation (the "rollercoaster" Dunning-Kruger curve). The core findings (delayed-JOL
effect, Kruger-Dunning, testing improves calibration) are well evidenced and retained.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| zell2014 | Zell & Krizan (2014). Do people have insight into their abilities? A metasynthesis. *Perspectives on Psychological Science*. | [10.1177/1745691613518075](https://doi.org/10.1177/1745691613518075) |
| kruger1999 | Kruger & Dunning (1999). Unskilled and unaware of it. *J. Personality and Social Psychology*. | [10.1037/0022-3514.77.6.1121](https://doi.org/10.1037/0022-3514.77.6.1121) |
| nelson1991 | Nelson & Dunlosky (1991). The "delayed-JOL effect". *Psychological Science*. | [10.1111/j.1467-9280.1991.tb00147.x](https://doi.org/10.1111/j.1467-9280.1991.tb00147.x) |
| dunlosky2013 | Dunlosky et al. (2013). Improving students' learning with effective learning techniques. *PSPI*. | [10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266) |
| koriat2005 | Koriat & Bjork (2005). Illusions of competence in monitoring one's knowledge during study. *JEP: LMC*. | [10.1037/0278-7393.31.2.187](https://doi.org/10.1037/0278-7393.31.2.187) |

---

## Claim-by-claim record

- **§1 Confidence blind spot** — People's self-assessments correlate only modestly with
  actual performance (**zell2014**, metasynthesis); learners overpredict recall. Verified
  (qualitative). Specific 70%/37% figures and "barely better than chance" reframed
  (LR-001).
- **§2 Dunning-Kruger** — Low performers overestimate their relative standing; the skills
  needed to perform are the skills needed to self-evaluate (**kruger1999**). Verified in
  prose. The interactive "rollercoaster" curve is a popular meme, not the K-D data — now
  labelled an illustration (LR-002).
- **§3 Delayed JOLs** — Judgments of learning made *immediately* after study are poorly
  calibrated; judgments made after a delay are far more accurate (the delayed-JOL effect,
  **nelson1991**). Verified — "far more accurate" matches the high delayed-JOL gamma
  correlations.
- **§4 Traffic Light Audit** — Self-testing improves the accuracy of one's knowledge
  judgements and exposes "familiar but not retrievable" topics (**dunlosky2013**, practice
  testing). Verified.
- **§5 Monitoring during study** — Skilled learners actively monitor comprehension;
  familiarity during study can create illusions of competence that monitoring counters
  (**koriat2005**). Verified.
- **§6 Prediction Game** — Repeatedly predicting then checking performance improves
  calibration over time and tends to generalise. Verified (qualitative); "50% over a
  year" and the strong cross-subject transfer claim reframed (LR-003).

*The interactive components (Calibration Quiz, Confidence-vs-Reality curve, Timing Effect,
Traffic Light Audit, Prediction Tracker) are illustrations/exercises; their internal
numbers are not presented as study data.*

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| LR-001 | § 1 | "70% predicted / 37% actual"; "barely better than chance" → "predict far more than they remember"; "modestly" | Specific figures unverifiable; "chance" overstates (zell2014: modest correlation). |
| LR-002 | § 2 | rollercoaster "Dunning-Kruger curve" presented as data → labelled a simplified illustration | The valley-of-despair curve is a meme, not the kruger1999 finding. |
| LR-003 | § 6 | "50% more accurate over a year" + strong cross-subject transfer → qualitative improvement + "tends to carry over" | Figure unverifiable; metacognitive transfer across domains is contested. |
