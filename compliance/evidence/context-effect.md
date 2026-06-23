# Evidence Dossier — The Context Effect

**Module:** `context-effect-protocol` (`components/TheContextEffectModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/contextEffect.ts`.

**Outcome:** Built on canonical context-dependent-memory studies. One reframe — the
"40%" recall figures overstated a real-but-modest effect (per the meta-analysis), so they
were reframed to qualitative and the effect is now described as "modest".

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| godden1975 | Godden & Baddeley (1975). Context-dependent memory in two natural environments: On land and underwater. *British J. of Psychology*. | [10.1111/j.2044-8295.1975.tb01468.x](https://doi.org/10.1111/j.2044-8295.1975.tb01468.x) |
| smith1978 | Smith, Glenberg & Bjork (1978). Environmental context and human memory. *Memory & Cognition*. | [10.3758/bf03197465](https://doi.org/10.3758/bf03197465) |
| mehta2012 | Mehta, Zhu & Cheema (2012). Is noise always bad? Exploring the effects of ambient noise on creative cognition. *J. Consumer Research*. | [10.1086/665048](https://doi.org/10.1086/665048) |
| smithvela2001 | Smith & Vela (2001). Environmental context-dependent memory: A review and meta-analysis. *Psychonomic Bulletin & Review*. | [10.3758/bf03196157](https://doi.org/10.3758/bf03196157) |

---

## Claim-by-claim record

- **§1 Why You Blank in the Exam Hall** — Memory is partly cued by the physical study
  environment; matching study/test context aids recall (the classic divers experiment,
  **godden1975**). Verified; "40%" reframed (CE-001). Interactives are illustrative.
- **§2 The "Switch It Up" Fix** — Studying the same material in varied environments
  ("encoding variability") produces more context-independent, portable memories than
  repeating in one place (**smith1978**, two-room study). Verified; "40%" reframed
  (CE-001).
- **§3 Does Noise Help or Hurt?** — Moderate ambient noise (~café level) can enhance
  creative cognition relative to silence or loud noise (**mehta2012**); focused/precise
  tasks favour quiet. Verified. The noise-performance curve and task matcher are
  illustrative.
- **§4 Why Switching Spots Works** — Encoding variability adds retrieval routes; the
  environmental context effect is **real but modest** and stacks with spacing/interleaving
  (**smithvela2001**, meta-analysis). Verified — the module now states the effect is
  modest, consistent with the meta-analysis.
- **§5 Setting Up Your Study Rotation** — Rotate 2–3 spots, match noise to task, practise
  in exam-like conditions. Practical application of the above.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| CE-001 | §§ 1–2 | "recalled 40% more" (×2) → "noticeably more" / "more" | Context-dependent memory is real (godden1975, smith1978) but modest and inconsistent per the meta-analysis (smithvela2001); the 40% figures overstated it. |
