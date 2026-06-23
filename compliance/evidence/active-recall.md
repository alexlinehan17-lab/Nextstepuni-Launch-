# Evidence Dossier — Mastering Active Recall

**Module:** `mastering-active-recall-protocol` (`components/MasteringActiveRecallModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (ahead of DCU / Brian MacCraith)
**Governing rule:** A claim is only stated or advised where peer-reviewed literature
supports it. Every DOI below was confirmed to resolve via CrossRef. No citation is
attached unless it points to a real, locatable paper that supports the specific
claim. Claims that could not be verified against an accessible primary source were
reframed to the supported version (logged under *Reframed content*) rather than
cited to an unconfirmed figure.

In-app, references surface to students as faint superscript markers (`Cite`) that map
to a module-wide **References** button (desktop: beside the progress wheel; mobile:
top of the Sections drawer) which opens the full source list (`ReferencesModal`). The
authoritative reference data lives in `data/references/activeRecall.ts`
(`ACTIVE_RECALL_REFERENCE_LIST` — the order defines the superscript numbering).

---

## Verified references

| Key | Citation | DOI | Verification |
|-----|----------|-----|--------------|
| rk2006 | Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*. | [10.1111/j.1467-9280.2006.01693.x](https://doi.org/10.1111/j.1467-9280.2006.01693.x) | CrossRef confirmed (title/authors/journal/year). |
| kr2008 | Karpicke, J. D., & Roediger, H. L. (2008). The critical importance of retrieval for learning. *Science*. | [10.1126/science.1152408](https://doi.org/10.1126/science.1152408) | CrossRef confirmed; abstract retrieved and supports the qualitative claim. |
| sb2015 | Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science*. | [10.1177/1745691615569000](https://doi.org/10.1177/1745691615569000) | CrossRef confirmed. |
| butler2010 | Butler, A. C. (2010). Repeated testing produces superior transfer of learning relative to repeated studying. *J. Exp. Psychol. LMC*. | [10.1037/a0019902](https://doi.org/10.1037/a0019902) | CrossRef confirmed. |
| kb2011 | Karpicke, J. D., & Blunt, J. R. (2011). Retrieval practice produces more learning than elaborative studying with concept mapping. *Science*. | [10.1126/science.1199327](https://doi.org/10.1126/science.1199327) | CrossRef confirmed (original *Science* article, not the review record). |
| agarwal2014 | Agarwal, P. K., D'Antonio, L., Roediger, H. L., McDermott, K. B., & McDaniel, M. A. (2014). Classroom-based programs of retrieval practice reduce middle school and high school students' test anxiety. *J. Applied Research in Memory and Cognition*. | [10.1016/j.jarmac.2014.07.002](https://doi.org/10.1016/j.jarmac.2014.07.002) | CrossRef confirmed; primary full text paywalled (see reframe AR-002). |

---

## Claim-by-claim record

### § 1 — The Great Forgetting
- **Claim:** Re-readers do slightly better after a few minutes, but a week later have
  forgotten far more than students who tested themselves; testing slows forgetting.
- **Source:** rk2006.
- **Support:** Direct — this is the central crossover finding of Roediger & Karpicke
  (2006): a short-delay restudy advantage that reverses to a robust testing advantage
  at one week. **Verified.**

### § 2 — Why Testing Yourself Works
- **Claim A:** The "testing effect" — retrieval strengthens memory more than restudy.
  **Source:** rk2006. **Verified.**
- **Claim B:** Memory has distinct "storage strength" (learning) vs "retrieval
  strength" (current accessibility); re-reading inflates the latter without building
  the former. **Source:** sb2015 (learning-vs-performance distinction). **Verified.**
- *Note:* The `StrengthMeter` bar values are illustrative of the concept, not reported
  data, and are not presented to students as study results.

### § 3 — The "I Know This" Trap  → see reframe AR-001
- **Claim:** Continuing to test after first success produces far better one-week
  retention than dropping the item, despite equal confidence at the time.
- **Source:** kr2008.
- **Support:** Abstract states repeated testing "produced a large positive effect"
  while repeated study after learning "had no effect," and that learners' predictions
  were uncorrelated with performance. The qualitative claim is **verified**; the
  original specific figures (35% / 80%) were **reframed** (primary paywalled).

### § 4 — Beyond Just Memorising Facts (transfer)
- **Claim:** Retrieval practice improves transfer/application to novel problems, not
  just verbatim recall.
- **Sources:** butler2010 (title: "…superior transfer of learning…"); kb2011
  (retrieval practice beat concept mapping, including on inference questions).
  **Verified.**

### § 5 — The Anxiety Myth  → see reframe AR-002
- **Claim:** Most students report low-stakes quizzing helps them learn and reduces
  exam nerves.
- **Source:** agarwal2014 (title: "…retrieval practice reduce[s]…students' test
  anxiety").
- **Support:** The paper's topic and finding support the qualitative claim. The
  original specific figures (92% / 72%) were **reframed** (primary paywalled; figures
  corroborated only by secondary sources).

### § 6 — Your Recall Toolkit
- **Rule 1 (reframed, AR-004):** "Desirable difficulties" — effortful-but-successful
  retrieval builds durable memory; not all difficulty helps. **Source:** sb2015.
  **Verified** (after reframe from the over-general "if it feels hard, it's working").
- **Rule 2:** Don't judge knowledge with the book open (familiarity ≠ retrievability).
  Supported by the storage/retrieval distinction (sb2015) and the metacognitive-
  illusion finding (kr2008). **Verified.**
- **Rule 3:** Keep testing after first success. **Source:** kr2008. **Verified.**
- **Micro-commitment (reframed, AR-003):** Weight study time toward retrieval over
  restudy. Principle supported by rk2006 / kr2008; the specific "20/80" ratio was
  removed as unsupported.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| AR-001 | § 3 | "35% … 80% — more than double" → "remembered far more a week later" | Figures from paywalled Karpicke & Roediger (2008); exact numbers unverifiable against primary source. |
| AR-002 | § 5 | "92% … 72%" → "the large majority … most" | Figures from paywalled Agarwal et al. (2014); corroborated only by secondary sources. |
| AR-003 | § 6 | "20/80 rule" → "spend most of your time actively recalling" | Specific ratio is a popularisation with no empirical basis. |
| AR-004 | § 6 | "If It Feels Hard, It's Working" → "A Bit of Struggle Is the Point" | Over-general; corrected to the precise "desirable difficulties" concept (sb2015). |

## Outstanding items
- If the **Karpicke & Roediger (2008)** and **Agarwal et al. (2014)** PDFs are
  obtained, the exact figures in AR-001 / AR-002 can be confirmed against the primary
  source and restored verbatim.
