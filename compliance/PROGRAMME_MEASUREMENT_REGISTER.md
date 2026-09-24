# Programme Measurement Purpose Register

Status: implementation record; controller and legal sign-off required before production deployment  
Owner: NextStepUni Ltd  
Date: 24 September 2026  
Schema version: 1

The implementation is disabled by default in both the client and callable
function. It must remain disabled until controller/legal approval, the
existing-student notice/acknowledgement decision, Year-2 aggregate scaling and
load-tested export/erasure handling are complete.

## Scope and design

NextStepUni uses a first-party event stream to evaluate programme reach,
participation, retention and product quality. It does not use Google Analytics,
advertising identifiers, cross-site tracking, session replay, raw keystrokes or
screen recording.

Each student is assigned a random analytics identifier in the server-only
`analyticsSubjects/{uid}` mapping. Raw `programmeEvents` contain that identifier
and server-resolved school/year cohort fields, but never name, email, free text,
answers, reflection content or exact study duration. Client access to raw events,
identifier mappings and rate limits is denied. The admin dashboard receives an
aggregate callable response, suppresses cohorts below five students, and also
hides individual metric cells when fewer than five students contribute.

Raw events expire after 400 days. Rate-limit records expire after 48 hours.
Account erasure deletes the identifier mapping and all linked raw events. Data
access exports include the event record and identifier.

## Event purposes

| Event | Purpose | Decision enabled | Permitted structured fields |
|---|---|---|---|
| `account_registered` | Establish registration volume after measurement begins | Improve invitations and account setup | platform, app version, session ID |
| `session_started` | Count active days/weeks and returning participation | Set participation targets and identify dormancy | platform, app version, session ID |
| `feature_exposed` | Separate “not used” from “never shown” | Improve placement and discoverability | feature ID |
| `feature_started` | Measure feature adoption and first meaningful action | Improve, reposition or retire weak tools | feature ID, source |
| `feature_completed` | Measure whether a bounded feature flow succeeds | Redesign flows with poor completion | feature ID, source |
| `module_started` | Measure learning-module adoption and activation | Improve module placement and sequence | canonical module ID |
| `module_completed` | Measure successful module flow completion | Identify content with weak completion | canonical module ID |
| `plan_activity_completed` | Measure follow-through on planned study | Adjust workload, reminder and task size | source only |
| `study_session_started` | Establish the denominator for study-session completion | Find setup or timer abandonment | session type |
| `study_session_completed` | Measure purposeful study and post-session confidence | Improve session length, pacing and debrief | session type, duration band, confidence 1-5 |
| `practice_attempt_completed` | Measure practice volume and broad self-marked accuracy by curriculum area | Improve practice coverage, difficulty and sequencing | canonical subject/topic IDs, coarse accuracy band |

Every event also receives server-owned event time, local day/week, academic year,
rollout cohort, school ID and year group. These fields exist only to produce the
approved cohort/time reports. They must not be repurposed for individual scoring,
discipline, hidden risk classification or marketing.

## Reporting definitions

- Activation: among accounts whose complete seven-day window has elapsed, the
  first module, feature or study-session start within seven days of registration.
  Accounts with no measurement identifier remain in the denominator as not yet
  activated. Registration time currently comes from the account profile and is
  a documented pilot limitation pending a server-owned registration timestamp.
- Weekly participation: activated students with a recorded app session in the
  most recent seven days, divided by activated students in the selected cohort.
- Four-week retention: activated students with an app session during days 21-27
  after activation, divided by cohorts old enough to have completed week four.
- Feature success: for flows with implemented completion instrumentation,
  distinct students who both start and finish inside the selected reporting
  period divided by distinct students starting in that period. Generic tool
  launches show adoption only until a real completion boundary is instrumented.
- Confidence after study: mean of voluntary 1-5 responses attached to completed
  study sessions; response count is always displayed.

Percentages must show their numerator and denominator. No causal claim may be
made from usage data alone. Eligible-student counts, rollout milestones,
baseline/endline surveys and verified educational outcomes remain unavailable
until the programme supplies those inputs under a separately documented purpose.

## Explicit exclusions

The event schema rejects unknown fields. Do not add names, email addresses,
precise location, IP address, advertising IDs, typed text, answers, reflections,
private notes, exact duration, inferred health/disability/vulnerability labels,
individual quality scores or cross-service identifiers.

Any new event or field requires all of the following in the same change:

1. A named reporting purpose and product/programme decision in this register.
2. Server validation and a bounded vocabulary.
3. A retention and erasure rule.
4. Child-facing notice review.
5. DPIA review and controller approval where the risk or purpose changes.

## Production-readiness gates

- Replace the pilot in-memory summary scan with bounded, pre-aggregated cohort
  buckets before Year-2 rollout.
- Move high-volume programme-event access/erasure to the asynchronous export
  and deletion workflow, then load-test it at the permitted retention volume.
- Present the updated notice to existing students in the form approved by the
  school/controller; do not infer consent or acknowledgement from a login.
- Enable `VITE_PROGRAMME_MEASUREMENT_ENABLED` and the server-side
  `PROGRAMME_MEASUREMENT_ENABLED` parameter only in the approved release.

## Authorities reviewed

- Irish Data Protection Commission, *The Fundamentals for a Child-Oriented
  Approach to Data Processing* (final version, 2021).
- Irish Data Protection Commission, *Guide to Data Protection Impact
  Assessments*.
- GDPR Articles 5 and 25 (data minimisation, storage limitation and data
  protection by design/default).
