# Evidence Dossier — Spaced Repetition

**Module:** `mastering-spaced-repetition-protocol` (`components/MasteringSpacedRepetitionModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef; unverifiable specifics reframed (logged in `data/cutContent.ts`).
References surface in-app via inline `Cite` markers + the module-wide **References**
button (`ReferencesModal`); data in `data/references/spacedRepetition.ts`.

---

## Verified references

| Key | Citation | DOI | Verification |
|-----|----------|-----|--------------|
| murre2015 | Murre, J. M. J., & Dros, J. (2015). Replication and analysis of Ebbinghaus' forgetting curve. *PLOS ONE*. | [10.1371/journal.pone.0120644](https://doi.org/10.1371/journal.pone.0120644) | CrossRef confirmed; open-access replication of the forgetting curve. |
| cepeda2006 | Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*. | [10.1037/0033-2909.132.3.354](https://doi.org/10.1037/0033-2909.132.3.354) | CrossRef confirmed; meta-analytic synthesis of the spacing effect. |
| sb2015 | Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*. | [10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000) | CrossRef confirmed; covers desirable difficulties. |
| cepeda2008 | Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H. (2008). Spacing effects in learning: A temporal ridgeline of optimal retention. *Psychological Science*. | [10.1111/j.1467-9280.2008.02209.x](https://doi.org/10.1111/j.1467-9280.2008.02209.x) | CrossRef confirmed; source of the optimal gap-as-proportion-of-retention-interval finding. |

---

## Claim-by-claim record

### § 1 — The Forgetting Curve  → see reframe SR-001
- **Claim:** Without review, memory of new material fades sharply soon after learning.
- **Source:** murre2015. **Verified** (qualitative). The original specific figures
  ("over 50% within an hour, up to 80% within a day") were **reframed** — the 80%/24h
  figure overstates the replicated curve.

### § 2 — The Cramming Paradox  → see reframe SR-002
- **Claim:** For equal study time, spacing produces much longer-lasting retention than
  massed practice (cramming).
- **Source:** cepeda2006 (meta-analysis). **Verified** (qualitative). The original
  "triple" multiplier was **reframed** to "dramatically increase" — the effect is robust
  but the specific multiplier is not a general figure.
- *Note:* The interactive cram-vs-space visualisations use illustrative values to convey
  the shape of the effect; they are not presented as data from a specific study.

### § 3 — The Struggle Sweet Spot
- **Claim:** Letting memory fade slightly so retrieval takes effort ("desirable
  difficulty") strengthens learning. **Source:** sb2015. **Verified.**

### § 4 — The Best Review Schedule
- **Claim:** The optimal review gap is roughly 5–20% of the time until the test; longer
  retention intervals call for proportionally longer gaps.
- **Source:** cepeda2008 (temporal ridgeline of optimal retention). **Verified** — the
  optimal gap-as-proportion-of-retention-interval finding supports the rule of thumb and
  the worked examples.

### § 5 — Apps That Do It For You
- Describes how spaced-repetition software (e.g. Anki) schedules reviews. This is a tool
  description grounded in the spacing effect (cepeda2006/2008), not a separate empirical
  claim. No additional citation required.

### § 6 — Your Spacing Blueprint
- Practical Day 1 / Day 2–3 / Day 7 schedule applying the spacing principle, with the
  "test yourself, don't just re-read" instruction (retrieval practice). Application of
  the above; no separate claim to verify.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| SR-001 | § 1 | "over 50% within an hour, up to 80% within a day" → "a large share … within the first day or two" | 80%/24h overstates the replicated forgetting curve (murre2015). |
| SR-002 | § 2 | "can triple how long you remember" → "can dramatically increase…" | "Triple" not supported as a general figure; spacing effect robust but variable (cepeda2006). |
