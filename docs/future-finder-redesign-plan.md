# Future Finder — scientific re-base (planning doc, 2026-06-03)

**Goal:** keep the **same outcome set** (the 149 CAO courses in `futureFinderData.ts`) but re-base the **questions** and the **scoring algorithm** on a validated framework so the recommendations are defensible. This is a plan, not yet implemented.

---

## 1. Verdict on the current tool: not framework-based

The current Future Finder is **hand-built tag-matching**, not anchored to any recognised model.

- **Questions:** 10 items (`futureFinderAlgorithm.ts:405-539`) — pick-your-interests (Q1), "scenarios" (Q2, mapped to interest tags), three 1-5 values sliders (salary/security/helping), work-style multi-select (Q6), team/solo (Q7), study length (Q8), location (Q9-10).
- **Scoring:** a single blended 0-1 score per course = **interest 45%** (tag-overlap count capped at `matchCount/3`) + **values 30%** (weighted average of slider matches) + **feasibility 25%** (points "sigmoid" + study-level). Tags are **100% hand-authored** per course; the weights (45/30/25, the `/3` and `/2` caps) are **unvalidated editorial choices**.
- **Weaknesses:** (a) tags/weights are bespoke and unjustifiable to a third party; (b) it **blends interest-fit with points-feasibility into one number**, so a course can rank low because of points even if it fits perfectly — and the student can't see why; (c) some items are leading/double-barrelled; (d) no evidence base behind any of it.

It works as product engineering, but you can't "stand behind it" scientifically. That's the gap this plan closes.

## 2. Recommended framework: RIASEC interests + a work-values layer

**Anchor on Holland's RIASEC** (the model under the US Dept of Labor's free, public-domain **O*NET Interest Profiler**), with a short **work-values** layer (the O*NET six: Achievement, Independence, Recognition, Relationships, Support, Working Conditions). Big Five **only as optional colour**, never the matcher.

Why this stack:
- **RIASEC is the validated, dominant, operationalisable core.** Six interest types (Realistic, Investigative, Artistic, Social, Enterprising, Conventional). Long-form reliability α ≈ .93–.97; short-form (10 items/scale) α ≈ .81; replicated hexagonal structure; predicts **college-major choice and persistence** and training/job performance — and *interest–environment congruence* predicts outcomes better than raw scores (direct support for person-environment fit). [O*NET IP_RVS](https://www.onetcenter.org/dl_files/IP_RVS.pdf), [Nye et al. 2012](https://journals.sagepub.com/doi/10.1177/1745691612449021), [Allen & Robbins 2008](https://link.springer.com/article/10.1007/s11162-007-9064-5).
- **Interests, not personality, carry the field-of-study signal.** Big Five answers "how you behave," not "what to study"; interests add incremental validity over Big Five + ability for major choice. [Rounds & Su 2014](https://education.illinois.edu/docs/default-source/edpsy-documents/rounds-pub.pdf), [Stoll et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10013216/).
- **A work-values layer resolves within-cluster ambiguity interests can't** (two "Social" students diverge: nursing vs clinical psychology vs social enterprise, by what conditions satisfy them). Grounded in Theory of Work Adjustment. [O*NET Work Importance Locator](https://www.onetcenter.org/dl_files/WIL_zips/WIL-UG-deskp.pdf).
- **It's what Irish guidance already uses.** **CareersPortal.ie** and **Qualifax** both run RIASEC interest profilers (+ values on CareersPortal). The **CAO does no interest/aptitude assessment at all** — choosing *which* courses to list is left entirely to the student. So RIASEC makes the tool *interoperable* with the national tools counsellors and students already trust, and fills the exact gap CAO leaves. [CareersPortal](https://careersportal.ie/careerplanning/interest_profiler.php), [Qualifax](https://www.qualifax.ie/index.php?option=com_wrapper&view=wrapper&Itemid=25).
- **Super sets the tone:** Leaving-Cert students are in the *Exploration* stage — present "directions to explore," not a verdict. **Gati's PIC** sets the flow: prescreen → explore in depth → choose.

## 3. The new question set

- **Activity-based items, never job titles.** O*NET deliberately uses work/study-activity statements ("Run a chemistry experiment to identify an unknown substance," "Choreograph a dance routine") because *title* items amplify gender/ethnic stereotypes and narrow horizons. [O*NET IP Development](https://www.onetcenter.org/dl_files/IP.pdf), [Ludwikowski et al. 2020](https://journals.sagepub.com/doi/10.1177/1069072718821600).
- **8th-grade reading level**, Irish-context wording (O*NET's own target, since youngest users are ~13). [IP Development](https://www.onetcenter.org/dl_files/IP.pdf).
- **5-point "dislike → like" Likert** (what web O*NET + the Strong Interest Inventory use). Maximises variance for the correlation-based matching; avoids ipsative forced-choice distortions.
- **Length: Full = 60 interest items (10 × 6 RIASEC scales), α ≈ .81** — the public O*NET benchmark and reliability sweet spot. **Plus an optional "Quick" version = the best 5 items/scale (30 interest items)** the student chooses up front — exactly how O*NET ships a Long form + a Short form that is a *curated subset* of the Long. Build: author 10 items/scale, flag the best 5 (highest item-total correlation, gender-balanced) as the Quick subset. **Quick results are reliability-flagged** ("indicative — re-take the full version for a sharper read"). O*NET items are public domain and lawfully adaptable to Irish context.
- **+ a short work-values block** (~6-12 items) for the secondary layer.
- **Gender-balance screening:** drop/rewrite any item with a male–female mean endorsement difference > .30 (O*NET's own rule), because People–Things interest gaps are large (Things–People d ≈ 0.93) and a raw quiz can *amplify* stereotyped routing. [Su, Rounds & Armstrong 2009](https://pubmed.ncbi.nlm.nih.gov/19883140/).

## 4. The scoring model

1. **Profile, don't tag-count.** Sum the Likert responses within each scale → the student's **six-number RIASEC profile** (and, for display only, a 1-3 letter Holland code with ties shown together, e.g. "I-A/R").
2. **Match by profile *shape*.** Give each course a six-number RIASEC profile (§5). Compute the **Pearson correlation between the student's profile and each course's profile** — O*NET's exact method. It uses all six numbers, matches on pattern not absolute level, and needs **no tie-breaking**. [O*NET IP Manual](https://www.onetcenter.org/reports/IP_Manual.html).
3. **Fit buckets** (O*NET's cutoffs): r ≥ .729 = *Best fit*; .608-.728 = *Great fit*; 0-.608 = *Good fit*; negative = not shown.
4. **Human-readable "interest match" number:** show **Iachan's M (/28)** or **Brown-Gore C (/18)** alongside — both are hexagon-aware (reward *near* matches, not just exact letters) and have tie/two-letter extensions. (Implemented in the peer-reviewed `holland` R package; we re-implement in TS.) [holland pkg](https://cran.r-project.org/web/packages/holland/holland.pdf), [Iachan 1984](https://eric.ed.gov/?id=EJ302511).
5. **Work-values** scored as a *separate* congruence number, never blended into the interest score.

## 5. Tagging the 149 courses (outcome set unchanged)

Add `riasecProfile` (six numbers) + a derived `riasecCode`, and optional `workValues`, **alongside** the existing fields — the 149 course objects stay; nothing is removed.

The research finding: **this is mostly derivation, not re-research.** ~80-90% of the RIASEC signal is already implicit in the current `workStyleTags`/`interestTags` (`hands-on`→R, `research-driven`/`analytical`→I, `creative`+arts/design/music→A, `people-focused`+social-care/healthcare/education→S, `leadership`+business/finance/law→E, `structured`+finance/accounting→C). Plan:
1. Write a deterministic `workStyle/interest → RIASEC` lookup, auto-generate first-draft six-number profiles for all 149.
2. **Most defensible upgrade:** where a course maps cleanly to O*NET destination occupations, *inherit* their published expert-rated interest profiles (average them) instead of deriving — these are validated codes.
3. Human review/tie-break pass (ideally ≥3 raters, report agreement, mirroring O*NET's 4-judge panels). Realistically a few hours of curation, not 149 from scratch.
4. Work-values: 3-4 of the six already map from `salaryBand`/`employability`/`people-focused`/`independent`; Achievement + Support need a light hand-pass.

## 6. Honesty architecture: separate Fit / Reach / Eligibility

The biggest correctness win — **never blend interest-fit with points again.** Three independent axes, combined only at the display layer:

- **Axis 1 — Fit:** the RIASEC congruence (Pearson r / Iachan M). *Points and subjects never alter this number.*
- **Axis 2 — Reach:** student's predicted/target points vs each course's recent cutoff → **Safety / Match / Reach / Out-of-reach** (with an explicit "points move yearly" caveat, using last year's cutoffs).
- **Axis 3 — Eligibility:** required subjects/grades (HL Maths, a lab science, a language…) and optionally region — **binary gates**, not fit modifiers.

Present a **2-D view**: high-fit courses ranked by congruence, each annotated with a Reach badge + eligibility flag — so a perfect-fit course that's a points reach is shown as *exactly that* and never silently demoted. Always surface the **lower-points / PLC / apprenticeship pathway to the same field** beside a reach course (standard Irish guidance advice). If one ranked list is ever required, sort by Fit and use feasibility only as a shown tie-breaker — never `fit × feasibility`. [RTÉ Brainstorm](https://www.rte.ie/brainstorm/2024/0822/1402701-cao-points-college-courses-career/), [Pathways Guidance](https://www.pathwaysguidance.ie/post/low-points-does-not-mean-low-potential).

## 7. How it should look (UX)

PIC flow + Super framing:
1. **Choose length, then quiz** — student picks **Full** (~9-11 min, most accurate) or **Quick** (~4-5 min, a rough steer); single-tap activity cards ("How much would you enjoy…?"), 5-point like/dislike, progress bar, chunked into 6 themed sets, pause/resume. Plain Irish-context language.
2. **Your profile** — a friendly RIASEC read-back (hexagon or six bars), top 2-3 types in plain English, *"a snapshot, not a verdict — worth re-taking."*
3. **Directions to explore** — course families grouped by interest fit, each course card showing: **Fit** (great/good + the match number), a **Reach** badge, eligibility flags, related careers, and pathway alternatives. Surface high-fit **nontraditional** options deliberately (counter gender narrowing).
4. **Explore / shortlist / hand to a counsellor** — frame as decision *support*, not a decision.

## 8. Ethics & caveats to bake in (not optional)

- **Snapshot, not verdict.** Interests aren't stable in mid-adolescence (stability only r ≈ .64 by 18-22); encourage re-taking, never hard-route. [Adolescent interest stability](https://www.sciencedirect.com/science/article/abs/pii/S0001879103001660).
- **Expand, don't narrow.** Always show a *range* (~10 per level), reward hexagon-adjacent near-matches, never let one low scale delete a whole field.
- **Gender-aware.** Activity items + balanced-endorsement screening + deliberately surfacing nontraditional high-fit courses (option-expanding, à la ACT UNIACT).
- **Congruence ≠ guaranteed satisfaction.** The congruence-satisfaction link is debated; present matches as *reasoned exploration suggestions*, never a deterministic "best course." [Tinsley, Congruence Myth](https://www.researchgate.net/publication/232359731_The_Congruence_Myth_An_Analysis_of_the_Efficacy_of_the_Person-Environment_Fit_Model).
- **Minors / decision support.** Frame alongside a qualified guidance counsellor — ties into the outstanding consent/privacy work.

## 9. Migration / phasing

- **Phase A — engine + data ✅ DONE (2026-06-03):** `components/futureFinderRiasec.ts` (profile↔code, Pearson-r matching, Iachan M, fit buckets, Fit/Reach/Eligibility separation) + `components/futureFinderRiasecData.ts` (all 149 courses coded). Coding was **multi-rater** (3 independent rater agents/course, position-weighted consensus): **lead-letter unanimous 95%, majority 100%, mean pairwise Iachan congruence 0.973**, zero adjudications. Outcome set untouched; not yet wired into the live tool. Recommended final 10%: a human guidance-counsellor ratification pass on the codes.
- **Phase C (questions):** swap the question set for the 60-item adapted O*NET Short Form + values block; keep the existing answer-persistence shape where possible.
- **Phase D (results UX):** the 2-D Fit/Reach view + Super framing. Tests: scoring determinism, a known-profile → expected-course fixture, gender-balance check on items, and a fit-never-changes-with-points regression.

## 10. Decisions (locked 2026-06-03)
1. **Quiz length:** Full 60-interest-item default **+ an optional "Quick" 30-item** version (the best 5 items/scale, a curated subset) the student can choose; Quick results reliability-flagged as indicative.
2. **Work-values layer:** included — interests + the 6 O*NET work-values (~12 items).
3. **Results presentation:** the honest **Fit / Reach / Eligibility** 2-D view (interest fit ranked; points Reach badge + eligibility flags annotated; pathway alternatives surfaced).
4. **Tagging rigour:** most-defensible — derive first-draft from existing tags → **inherit O*NET occupation interest codes where courses map cleanly** → multi-rater review with reported agreement. Outcome set (149 courses) unchanged; add `riasecProfile` / `workValues` fields alongside existing data.

## Sources
O*NET IP Development https://www.onetcenter.org/dl_files/IP.pdf · IP Reliability/Validity https://www.onetcenter.org/dl_files/IP_RVS.pdf · IP Short-Form psychometrics https://www.onetcenter.org/dl_files/IPSF_Psychometric.pdf · IP Manual (matching/OIP/Job Zones) https://www.onetcenter.org/reports/IP_Manual.html · Work Importance Locator https://www.onetcenter.org/dl_files/WIL_zips/WIL-UG-deskp.pdf · Nye et al. 2012 (interests & performance) https://journals.sagepub.com/doi/10.1177/1745691612449021 · Rounds & Su 2014 https://education.illinois.edu/docs/default-source/edpsy-documents/rounds-pub.pdf · Allen & Robbins 2008 (major persistence) https://link.springer.com/article/10.1007/s11162-007-9064-5 · Su, Rounds & Armstrong 2009 (sex differences) https://pubmed.ncbi.nlm.nih.gov/19883140/ · Ludwikowski et al. 2020 (gender & item type) https://journals.sagepub.com/doi/10.1177/1069072718821600 · holland R package https://cran.r-project.org/web/packages/holland/holland.pdf · Iachan 1984 https://eric.ed.gov/?id=EJ302511 · Adolescent interest stability https://www.sciencedirect.com/science/article/abs/pii/S0001879103001660 · CareersPortal RIASEC https://careersportal.ie/careerplanning/interest_profiler.php · Qualifax RIASEC https://www.qualifax.ie/index.php?option=com_wrapper&view=wrapper&Itemid=25 · CAO (no interest test) https://www.citizensinformation.ie/en/education/third-level-education/applying-to-college/applying-for-college-and-the-cao/
