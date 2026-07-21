# Evidence Dossier — Reframing Progress

**Module:** `reframing-progress-protocol` (`components/ReframingProgressModule.tsx`)
**Review date:** 2026-06-23
**Reviewer:** Pre-accreditation literature review (DCU / Brian MacCraith)
**Governing rule:** Only state/advise what peer-reviewed literature supports; every DOI
verified via CrossRef. References surface via inline `Cite` markers + the module-wide
**References** button; data in `data/references/reframingProgress.ts`.

**Reviewer note.** A study-productivity module that is mostly *systems and heuristics*
rather than psychological claims, so the citation footprint is deliberately small and
precise. The three genuine psychology constructs are cited: the illusion of competence /
fluency-based overconfidence in judgments of learning (Koriat et al. 2005); deliberate
practice — targeted work on weaknesses with feedback (Ericsson et al. 1993); and mastery
(vs performance) goal orientation (Dweck & Leggett 1988). **No content cut.** Two parts of
the module sit *outside* the peer-reviewed-literature scope and carry no journal citation,
which is the correct treatment: **§2 the "80/20 Pareto" heuristic** is a strategic
rule-of-thumb (and the "80% of marks from 20% of the syllabus" figure is illustrative, not
a measured statistic); and **§3 "Banked Grades"** quotes Irish Leaving Certificate
component weightings (Irish oral 40%, History RSR ~20%, Geography investigation ~20%) which
are SEC syllabus/administrative facts — flagged here for separate verification against
current SEC subject specifications. The Kanban, Retrospective Log and XP systems (§5–§7)
are practical productivity tools, not empirical claims.

---

## Verified references

| Key | Citation | DOI |
|-----|----------|-----|
| koriat2005 | Koriat & Bjork (2005). Illusions of competence in monitoring one's knowledge during study. *J. Experimental Psychology: Learning, Memory, and Cognition*. | [10.1037/0278-7393.31.2.187](https://doi.org/10.1037/0278-7393.31.2.187) |
| ericsson1993 | Ericsson, Krampe & Tesch-Römer (1993). The role of deliberate practice in the acquisition of expert performance. *Psychological Review*. | [10.1037/0033-295x.100.3.363](https://doi.org/10.1037/0033-295x.100.3.363) |
| dweckleggett1988 | Dweck & Leggett (1988). A social-cognitive approach to motivation and personality. *Psychological Review*. | [10.1037/0033-295x.95.2.256](https://doi.org/10.1037/0033-295x.95.2.256) |

---

## Claim-by-claim record

- **§1 The Time Trap** — Hours logged ≠ learning; re-reading breeds the illusion of
  competence (**koriat2005**); deliberate practice on weaknesses with feedback drives
  improvement (**ericsson1993**). Verified.
- **§2 The 80/20 Protocol** — Pareto heuristic for prioritising high-yield topics.
  Strategic rule-of-thumb, not a measured statistic; no journal citation (outside scope).
- **§3 The "Banked Grade" Heist** — Irish LC component weightings (oral/RSR/field study).
  SEC administrative fact; flagged for separate verification, no journal citation.
- **§4 The Quest System** — Gamifying study to build a mastery (vs performance) goal
  orientation (**dweckleggett1988**). Verified.
- **§5 The Kanban Flow / §6 Retrospective Log / §7 XP Engine** — Practical productivity
  systems (visualise work, "worst first" prioritisation, points/rewards). No specific
  empirical claim, so no inline citation.

---

## Reframed content
None cut. Pareto (§2) and the Irish LC weightings (§3) are correctly treated as heuristic /
administrative content outside the peer-reviewed scope (see reviewer note); no removals, so
no `data/cutContent.ts` entry for this module.

## Citation-order audit (2026-07-21)
A full-site sweep verified the invariant that inline citation numbers ascend by first
appearance on every render path. The Essentials path violated it: the §1 simplified
branch omitted the Illusion-of-Competence claim, so its first visible marker was ².
Fixed by restoring the koriat2005-backed claim (recognition-driven false confidence
during re-reading — exactly what Koriat & Bjork 2005 demonstrates) with its ¹ marker to
the Essentials branch. No numbering changed; both paths now read 1,2,3.
