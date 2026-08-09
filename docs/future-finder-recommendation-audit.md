# Future Finder recommendation audit

Last reviewed: 9 August 2026

## Decision

Future Finder now keeps two ideas distinct:

1. **Interest match** is the visible RIASEC match percentage. Points never alter it.
2. **Recommendation order** answers “what should I explore first?” and combines interest fit, target-point feasibility, work values and route suitability.

This avoids both failure modes found in the audit: presenting a 500-point route as the first practical recommendation to a student targeting roughly 100 points, or treating a Level 5/6/7 route as inherently worse for a student with high projected points.

## What the audit found

- The Full questionnaire has 60 interest items (10 per RIASEC scale); Quick has 30 (5 per scale). Both add 12 work-value items.
- Interest fit uses a six-scale RIASEC profile and Pearson profile correlation. The displayed percentage remains an independent interest signal.
- The previous default order sorted almost entirely by interest correlation. Work values were displayed but did not determine order, while points were only shown as a badge.
- The previous points estimate used **current grades**. The intended product behaviour is now best-six **target grades**, falling back subject-by-subject to current grade only for older profiles without targets. Higher Level Maths receives the standard 25-point bonus at H6 or above.
- The catalogue has 149 records: 118 Level 8, 12 Level 7, 7 Level 6 and 12 Level 5 records. Because Level 8 dominates the data, a simple blended score is not sufficient; recommendations are banded into realistic, ambitious and explore before their blended score is compared.
- All 149 catalogue records have RIASEC metadata. The metadata was produced through a multi-rater pass with strong agreement, but still needs a human guidance-counsellor ratification pass.
- The course model supports `requiredSubjects`, but **none of the current records populate it**. Consequently, “known entry requirements” presently means the architecture is ready, not that course matriculation and subject-grade requirements are complete.
- Course points are labelled as 2025 CAO Round 1 data. They are indicative historical cut-offs, not guaranteed 2026 requirements, and need a versioned annual refresh.

## Recommendation policy (version 2)

The default order uses:

- 58% interest-profile similarity
- 22% target-points feasibility
- 12% work-values congruence
- 8% route suitability (NFQ level/pathway relative to projected attainment)

Before that score is compared, routes are grouped:

- **Realistic:** within the match/safety range and with no known missing requirement
- **Ambitious:** within the normal reach range
- **Explore:** a longer points stretch or a known missing requirement

The fit band adds a calibrated ordering advantage rather than acting as an absolute gate. This keeps credible routes prominent without allowing an unrelated accessible course to outrank a strongly matched course simply because the latter is modestly ambitious. A student can still sort explicitly by points. A high-target student may still see a Level 5/6/7 route when it is a strong fit, but it will not normally displace a similarly fitting Level 8 route. A lower-target student sees accessible routes first and high-points options as labelled stretches; implausible high-points routes are still heavily suppressed.

Interest correlation is non-linear in the blended score: a neutral correlation provides only a weak signal, while excellent correlations retain their prominence. Courses more than 180 points above the student's projection receive an additional penalty, increasing beyond 250 points. This deliberately distinguishes a useful stretch from a misleading recommendation.

## Verification added

- Target-grade calculation, best-six selection and Higher Maths bonus
- Monotonic points-feasibility behaviour
- Route-level behaviour at 100 and 500 projected points
- A realistic strong fit beating a slightly stronger but implausible stretch
- Real-catalogue scenario checks ensuring a 100-point profile is not headed by 500-point routes and a 500-point profile is predominantly shown suitable Level 8 routes
- Versioned re-ranking of saved results, so downstream features receive the new top ten without forcing a retake

## Remaining data work

These are catalogue/data-governance tasks, not reasons to hold back the ranking correction:

1. Import and version official 2026 course data when available, retaining the source year and round on each point value.
2. Populate minimum entry requirements and subject/grade gates for every course.
3. Add historical points ranges rather than presenting one previous cut-off as certainty.
4. Have an Irish guidance counsellor review course-to-RIASEC and work-value metadata, prioritising high-volume and regulated programmes.
5. Validate result quality with anonymised aggregate usage: recommendation saves, comparisons and later course exploration—not enrolment or demographic steering.

## Guardrails

- The tool is exploration support, not an admissions decision.
- It must never describe NFQ Level 5/6/7 as inferior; they are different recognised routes with progression pathways.
- Target grades express a student’s plan, not their worth or a permanent ceiling.
- Stretch courses remain discoverable and clearly labelled.
- Points and requirements move; students should verify current information with CAO, the institution and their guidance counsellor.

## Research basis

- O*NET Interest Profiler technical documentation for the Holland RIASEC model, questionnaire forms and vocational-interest use.
- Quality and Qualifications Ireland’s National Framework of Qualifications for comparing qualification levels and progression pathways.
- CAO order-of-merit guidance for the role of points in course offers.
