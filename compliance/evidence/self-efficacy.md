# Evidence Dossier — Self Efficacy

**Module:** `self-efficacy-protocol` (`components/SelfEfficacyModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/selfEfficacy.ts`.

**Reviewer note.** A textbook-clean Bandura module. Self-efficacy and its four sources —
enactive mastery, vicarious experience, social persuasion, physiological states — are
Bandura's foundational theory (Bandura 1977). The coping-vs-mastery-model point in §3 is
backed by Schunk, Hanson & Cox (1987), who found coping models (who show struggle then
success) build observers' self-efficacy more than flawless mastery models. The §5 "If-Then"
tool is an implementation intention (Gollwitzer 1999). **No content cut.** The §4
"metacognitive regulation" mention is brief framing within the motivational "success
iceberg" exercise and carries no specific empirical claim, so no citation is attached
there. The Efficacy Radar, Role-Model Selector and Iceberg widgets are interactive
self-assessment/reflection tools.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| bandura1977 | Bandura (1977). Self-efficacy: Toward a unifying theory of behavioral change. *Psychological Review*. | [10.1037/0033-295x.84.2.191](https://doi.org/10.1037/0033-295x.84.2.191) |
| schunk1987 | Schunk, Hanson & Cox (1987). Peer-model attributes and children's achievement behaviors. *Journal of Educational Psychology*. | [10.1037/0022-0663.79.1.54](https://doi.org/10.1037/0022-0663.79.1.54) |
| gollwitzer1999 | Gollwitzer (1999). Implementation intentions: Strong effects of simple plans. *American Psychologist*. | [10.1037/0003-066x.54.7.493](https://doi.org/10.1037/0003-066x.54.7.493) |

---

## Claim-by-claim record

- **§1 The Belief Barrier** — Self-efficacy (belief in one's ability) drives effort,
  persistence and recovery from setbacks (**bandura1977**). Verified.
- **§2 How Belief is Built** — The four sources of self-efficacy: enactive mastery,
  vicarious experience, social persuasion, physiological states (**bandura1977**). Verified.
- **§3 The Role Model Myth** — Coping models (relatable figures who struggle then succeed)
  build self-efficacy more effectively than flawless mastery models (**schunk1987**).
  Verified.
- **§4 The Success Iceberg** — Motivational reframing (process behind visible success);
  brief metacognition mention, no specific empirical claim, so no inline citation.
- **§5 The Habit Blueprint** — Micro-habits + "If-Then" implementation intentions to make
  behaviour automatic (**gollwitzer1999**). Verified. (Micro-/tiny-habits framing is a
  popular method; the cited claim is the implementation-intention effect.)

---

## Reframed content
None cut. All cited constructs map to verified peer-reviewed sources; no removals, so no
`data/cutContent.ts` entry for this module.
