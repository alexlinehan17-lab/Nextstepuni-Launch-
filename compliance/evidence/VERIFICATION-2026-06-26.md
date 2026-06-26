# Independent Citation Verification Pass — 2026-06-26

A second, adversarial check of the accredited modules, run after the per-module dossiers
were complete. The goal was the bar the governing rule actually sets: not "does the cited
paper exist" (DOIs were already checked on CrossRef) but **"does the cited source
genuinely support the *specific* claim it is attached to."**

## Method

- **Scope:** all 48 accredited module dossiers (38 learning-science + 8 Exam Zone + Business
  & Mathematics).
- **Assess:** one independent reviewer per module re-read every cited claim and checked it
  against its source — fetching abstracts/metadata via CrossRef and Europe PMC for the
  peer-reviewed citations, and against actual SEC marking-scheme/grade-statistics structure
  for the official sources. Reviewers were told to be skeptical and flag figures,
  superlatives, "real paper / wrong claim" mismatches, and official-source overreach.
- **Verify:** every flagged issue was independently re-tested by a second reviewer
  instructed to *refute* it. Only issues that survived refutation were upheld.

## Results

| | |
|---|---|
| Modules audited | 48 |
| Cited claims re-checked | 297 |
| Modules fully clean | 26 |
| Issues raised (assess) | 30 |
| Issues upheld (after refutation) | **13** |
| Issues resolved | **13 (all)** |

The refutation phase did its job: of the issues raised, fewer than half survived — e.g. a
HIGH-severity flag on `neuroplasticity / casey2008` was correctly refuted as a false
positive.

## The 13 upheld issues — and their fixes

| Module | Source | Issue | Resolution |
|--------|--------|-------|------------|
| Answer Engineering | secMarkingSchemes | "final answer = 4-5 of 25 marks / 80% is process" asserted as cited fact; no scheme fixes that split | Dropped the figures; kept the qualitative "most marks are for method" (AE-002) |
| Reframing Catastrophic Thoughts | lupien2009 | §2 acute-retrieval claim cited to a *chronic*-stress review | Re-cited to **kuhlmann2005** (acute psychosocial stress impairs retrieval) |
| Digital Distractions | mark2008 | "~23 min to refocus" attributed to the wrong Mark paper (speed/stress) | Re-attributed to **mark2005** ("No task left behind?", resumption of work) |
| Exam Hall Strategies | balban2023 | box-breathing-specific + acute "under a minute" overstated the study | Reframed to "slow, structured breathing settles arousal" (EHS-002) |
| Exam Hall Strategies | sio2009 | incubation stated prescriptively in its weakest (exam) case | Softened to "stepping away can sometimes help" (EHS-001) |
| How Your Memory Works | dunlosky2013 | interleaving lumped into the "high-utility" tier | Dossier corrected: testing/spacing high-utility, interleaving moderate |
| Points Optimization | secExamStatistics | §3 H1 bands contradicted by public SEC figures (Physics/Chem, English) | Bands removed → qualitative tiers; dashboard Physics/Chem corrected; relabelled illustrative (POPT-002) |
| Points Optimization | secExamStatistics | §7 forward *forecast* carried by a backward-looking dataset | Reframed to a non-prescriptive historical observation (POPT-003) |
| Reframing Progress | koriat2005 | dossier row mislabelled (wrong title/authors/journal) | Dossier row corrected to match CrossRef/library |
| Reverse Engineering | petersbuchel2010 | "motivation boost" overstated a delay-discounting study | Reframed to the delay-discounting mechanism (RE-001) |
| Spaced Repetition | cepeda2008 | optimal-gap proportion stated *backwards* + range truncated | Reframed to the source's actual ridgeline (SR-001) |
| The Teaching Effect | chi1989 (§3) | "than those who just read" — a head-to-head Chi's correlational design can't license | Softened to the association (TE-002) |
| The Teaching Effect | chi1989 (§4) | "beats passive reading every time" — same overreach | Softened to the association (TE-002) |

Two new correctly-attributed sources were added to the library (`mark2005`, `kuhlmann2005`).
Every student-facing reframe is recorded in `data/cutContent.ts` (and surfaces on the Cut
Content page); source re-attributions and dossier-label fixes are recorded in the
respective dossiers.

## Takeaway

No fabricated citations were found. The issues were the subtler, expert-spotted kind —
right topic, wrong specificity; right finding, wrong paper; a correlational study dressed
as an experiment; a backward-looking dataset asked to forecast. All 13 are now resolved,
which is exactly what this pass existed to do: surface them before the review, not during.
