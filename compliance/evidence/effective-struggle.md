# Evidence Dossier — Effective Struggle and Growth

**Module:** `effective-struggle-protocol` (`components/EffectiveStruggleAndGrowthModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/effectiveStruggle.ts`.

**Reviewer note.** A synthesis module built on four well-established, well-replicated
pillars — the testing effect (Roediger & Karpicke 2006), cognitive load theory (Sweller
et al. 1998), working-memory capacity (Cowan 2001) and desirable difficulties /
learning-vs-performance (Soderstrom & Bjork 2015) — plus a documented finding that
retrieval practice lowers test anxiety (Agarwal et al. 2014). The mechanisms are sound.
**One reframe:** a chart and two sentences quoted *prediction* percentages (90% vs 40%)
that are not the predictions Roediger & Karpicke actually reported. The verified
one-week retention figures (40% vs 61%) were kept; the fabricated predictions were
removed and the confidence point made qualitatively. The Zone of Proximal Development
(§3) is presented as conceptual framing (Vygotskian) with no specific empirical stat, so
it carries no inline citation. The day-by-day "Confidence Trap" curves and the
"Cognitive Load Balancer"/"Stairs vs Escalator" widgets are illustrative interactions,
not claimed study data.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| rk2006 | Roediger & Karpicke (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*. | [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x) |
| sweller1998 | Sweller, van Merriënboer & Paas (1998). Cognitive architecture and instructional design. *Educational Psychology Review*. | [10.1023/a:1022193728205](https://doi.org/10.1023/a:1022193728205) |
| cowan2001 | Cowan (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences*. | [10.1017/s0140525x01003922](https://doi.org/10.1017/s0140525x01003922) |
| sb2015 | Soderstrom & Bjork (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*. | [10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000) |
| agarwal2014 | Agarwal, D'Antonio, Roediger, McDermott & McDaniel (2014). Classroom-based programs of retrieval practice reduce middle school and high school students' test anxiety. *J. Applied Research in Memory and Cognition*. | [10.1016/j.jarmac.2014.07.002](https://doi.org/10.1016/j.jarmac.2014.07.002) |

---

## Claim-by-claim record

- **§1 The Fallacy of Ease** — Self-testing beats re-reading on delayed retention even
  though re-reading feels easier and breeds higher confidence; one week later, repeated
  study ≈ 40% vs repeated testing ≈ 61% (**rk2006**, Exp 2). Verified. The fabricated
  90%/40% *prediction* figures were reframed (ES-001).
- **§2 Your Brain's Bottleneck** — Working memory holds only a handful of items
  (~3–5; "magical number 4") (**cowan2001**); learning is governed by intrinsic,
  extraneous and germane cognitive load (**sweller1998**). Verified. The slider
  percentages in the balancer are user-set illustration, not study values.
- **§3 The Sweet Spot** — Zone of Proximal Development (stretch but don't overwhelm).
  Conceptual Vygotskian framing; no specific empirical stat, so no inline citation.
- **§4 The Engine of Memory** — Storage vs retrieval strength and "desirable difficulty":
  durable learning is built when retrieval is effortful, not fluent (**sb2015**). The
  re-read-vs-test experiment (40% vs 61% at one week) is **rk2006**. Verified.
- **§5 The Unified Model** — A diagnostic combining the above (right difficulty + low
  noise + real retrieval). Synthesis of cited material; the scenario quiz is application,
  not a new claim.
- **§6 Recalibrate Your Dashboard** — Low-stakes retrieval practice can reduce test
  anxiety (**agarwal2014**). Verified; "kills/crushes anxiety" softened to "can ease."

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| ES-001 | § 1 (prose + "Great Deception" chart) | "predicted 90% … predicted 40%" → confidence stated qualitatively; chart shows only the verified 40% vs 61% one-week retention | The 40%/61% retention is RK2006's headline result (kept + cited); the precise prediction percentages are not what the study reported (predictions were ~half for both; the paper supports only that re-reading raised confidence). Fabricated predictions removed. |
