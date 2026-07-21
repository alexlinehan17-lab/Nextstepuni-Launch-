# Evidence Dossier — Mix It Up (Interleaving)

**Module:** `mastering-interleaving-protocol` (`components/MasteringInterleavingModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/interleaving.ts`.

**Outcome:** No content required reframing or cutting — every claim maps to an
established interleaving finding. Citations added only.

---

## Verified references

| Key | Citation | DOI | Verification |
|-----|----------|-----|--------------|
| rohrer2007 | Rohrer, D., & Taylor, K. (2007). The shuffling of mathematics problems improves learning. *Instructional Science*. | [10.1007/s11251-007-9015-8](https://doi.org/10.1007/s11251-007-9015-8) | CrossRef confirmed. |
| rohrer2015 | Rohrer, D., Dedrick, R. F., & Stershic, S. (2015). Interleaved practice improves mathematics learning. *Journal of Educational Psychology*. | [10.1037/edu0000001](https://doi.org/10.1037/edu0000001) | CrossRef confirmed (journal article, not the dataset record). |
| kornell2008 | Kornell, N., & Bjork, R. A. (2008). Learning concepts and categories: Is spacing the enemy of induction? *Psychological Science*. | [10.1111/j.1467-9280.2008.02127.x](https://doi.org/10.1111/j.1467-9280.2008.02127.x) | CrossRef confirmed. |
| sb2015 | Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*. | [10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000) | CrossRef confirmed; covers desirable difficulties. |

---

## Claim-by-claim record

### § 1 — Why "Finishing a Topic" Fools You
- **Claim:** Blocked practice gives a false sense of mastery and fails to train
  discrimination between similar problem types — exactly what exams require.
- **Source:** rohrer2007. **Verified** — interleaved (mixed) maths practice improves
  learning over blocked practice, specifically by building discrimination.

### § 2 — The "Topic Salad" Method
- **Claim:** Mixing topics within and across sessions is harder but produces better
  learning. **Source:** rohrer2015 (interleaved practice improves maths learning).
  **Verified.**

### § 3 — Why Harder Feels Better
- **Claim A:** The added effort of switching is a "good kind of difficulty."
  **Source:** sb2015 (desirable difficulties). **Verified.**
- **Claim B:** Placing similar-but-different concepts side by side forces the brain to
  discriminate and learn *when* to apply each — improving category/inductive learning.
  **Source:** kornell2008 (interleaving aids inductive category learning) +
  rohrer2007/2015 (maths discrimination). **Verified.**
- *Note:* The chain-rule/product-rule "Problem Spotter" is an illustrative exercise, not
  presented as data.

### § 4 — The "Worst First" Timetable
- A study-management heuristic (retrospective, RAG-rated, weakest-first) that
  operationalises mixing + targeting weak areas. Application of the above; no separate
  empirical claim to verify.

### § 5 — Your Mix-It-Up Game Plan
- Practical application (shuffle question types / topics). No separate claim.

---

## Reframed / cut content
None.

## Citation-order audit (2026-07-21)
A full-site sweep verified the invariant that inline citation numbers ascend by first
appearance on every render path. This module violated it (§3 cited the
desirable-difficulty claim before the discrimination claim, but the list numbered them
the other way round). Fixed by swapping entries 3↔4 in `data/references/interleaving.ts`
(now 1 rohrer2007 · 2 rohrer2015 · 3 sb2015 · 4 kornell2008) and renumbering the §3
markers to match. Every claim→source pairing is unchanged; both paths now read 1,2,3,4.
