# Evidence Dossier — The Teaching Effect

**Module:** `teaching-effect-protocol` (`components/TheTeachingEffectModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/teachingEffect.ts`.

**Reviewer note.** A well-grounded study-skills module built on three solid sources:
expecting-to-teach improves recall and organisation of knowledge even when no teaching
occurs (Nestojko et al. 2014); self-explanation deepens learning and transfer (Chi et al.
1989); and the broad technique-effectiveness review rating practice testing high and
highlighting/re-reading/summarising low (Dunlosky et al. 2013). **One reframe:** a "82% vs
46%" statistic in §3 was presented as an explain-vs-read *experiment*, but Chi et al.
(1989) was a *correlational* good-vs-poor-solver study — that causal framing and those
precise numbers misrepresent the design, so they were reframed to the accurately-
attributed qualitative effect. Two minor tightenings: §1 "performed better on every type
of question" → "remembered more and organised it better, especially the main points"
(matching Nestojko's free-recall measure); §5 "far and away the most effective" →
"among the most effective" (Dunlosky rates self-explanation moderate, testing high). The
Teach-vs-Test chart and Explain-It-Back / Feynman widgets are illustrative interactions.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| nestojko2014 | Nestojko, Bui, Kornell & Bjork (2014). Expecting to teach enhances learning and organization of knowledge in free recall of text passages. *Memory & Cognition*. | [10.3758/s13421-014-0416-z](https://doi.org/10.3758/s13421-014-0416-z) |
| chi1989 | Chi, Bassok, Lewis, Reimann & Glaser (1989). Self-explanations: How students study and use examples in learning to solve problems. *Cognitive Science*. | [10.1016/0364-0213(89)90002-5](https://doi.org/10.1016/0364-0213(89)90002-5) |
| dunlosky2013 | Dunlosky, Rawson, Marsh, Nathan & Willingham (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest*. | [10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266) |

---

## Claim-by-claim record

- **§1 Why Teaching Beats Testing** — Expecting to teach (vs expecting a test) improved
  recall and the organisation of knowledge, with no actual teaching required
  (**nestojko2014**). Verified; "every type of question" tightened to the recall measure.
- **§2 Explaining Changes How You Think** — Explaining/self-explaining forces
  restructuring and exposes gaps; "rebuilding" (generative) beats "parroting"
  (**chi1989**). Verified.
- **§3 You Don't Need an Audience** — Self-explanation of worked examples produces better
  problem-solving transfer than passive reading (**chi1989**). Verified. The "82%/46%"
  experimental framing was reframed (TE-001).
- **§4 The Simplicity Technique** — Generative explanation (the "Feynman technique") beats
  passive reading (**chi1989**). The technique is a named study method; the underlying
  generative-learning claim is cited. Verified.
- **§5 Putting It All Together** — Self-testing ranks among the most effective techniques
  and highlighting/re-reading/summarising among the least (**dunlosky2013**). Verified;
  self-explanation ranking softened to "among the most effective."

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| TE-001 | § 3 | "solved 82% … only 46%" (explain-vs-read experiment) → "solved far more new problems than those who just read" | The self-explanation effect is kept and cited (Chi 1989), but Chi 1989 was correlational (good vs poor solvers), so the experimental framing and precise percentages misrepresent the design. |
