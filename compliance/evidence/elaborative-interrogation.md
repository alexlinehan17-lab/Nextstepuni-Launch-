# Evidence Dossier — Elaborative Interrogation

**Module:** `elaborative-interrogation-protocol` (`components/ElaborativeInterrogationModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/elaborativeInterrogation.ts`.

**Outcome:** The elaborative-interrogation ("ask why") effect is well evidenced; the
specific 72%/37% retention figures could not be tied to a verifiable source and were
reframed (EI-001). The subject-application sections (STEM, SRPs, Irish oral) are
exam-technique applications, not separate psychological claims.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| stein1979 | Stein & Bransford (1979). Constraints on effective elaboration: Effects of precision and subject generation. *J. Verbal Learning and Verbal Behavior*. | [10.1016/s0022-5371(79)90481-x](https://doi.org/10.1016/s0022-5371(79)90481-x) |
| pressley1987 | Pressley, McDaniel, Turnure, Wood & Ahmad (1987). Generation and precision of elaboration. *JEP: LMC*. | [10.1037/0278-7393.13.2.291](https://doi.org/10.1037/0278-7393.13.2.291) |
| dunlosky2013 | Dunlosky et al. (2013). Improving students' learning with effective learning techniques. *PSPI*. | [10.1177/1529100612453266](https://doi.org/10.1177/1529100612453266) |

---

## Claim-by-claim record

- **§1 The "Why" Engine** — Generating an explanation for why a fact is true
  ("elaborative interrogation") produces substantially better retention than passive
  reading; the "hungry man" precise-elaboration paradigm is the classic demonstration.
  **stein1979, pressley1987**; reviewed in **dunlosky2013**. Verified (qualitative).
  Specific 72%/37% figures reframed (EI-001).
- **§2 Rules of the Road** — EI's benefit depends on prior domain knowledge (low prior
  knowledge → poorer self-generated explanations); it is also effortful. **dunlosky2013**
  (notes prior-knowledge moderation). Verified.
- **§3 STEM Toolkit** — Applying "why" to connect concepts (and *not* during timed
  calculation) — application of EI to science/maths. Mechanism cited in §1.
- **§4 Humanities Engine** — "Why" to build argument / Geography SRP "statement +
  development". SRP structure is SEC exam technique, not a psychological claim.
- **§5 Language Edge** — "Why" to build a flexible idea-web for the Irish oral instead of
  rote scripts — exam-technique application.
- **§6 Study Plan** — Four-step routine + "why" flashcards; application of EI.

---

## Reframed content (also logged in `data/cutContent.ts`)

| ID | Section | Original → Reframed | Reason |
|----|---------|---------------------|--------|
| EI-001 | § 1 | "72% … 37% … (72% vs 37%)" → "far more … come close to doubling" | Specific figures not tied to a verifiable source; EI effect itself is well evidenced (stein1979, pressley1987, dunlosky2013). |
