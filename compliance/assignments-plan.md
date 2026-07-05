<!--
 @license
 SPDX-License-Identifier: Apache-2.0
-->

# Assignments (feature E9) — activation plan

A guidance counsellor sets a revision task for their school; students see it and
mark it done; completion flows back to the GC dashboard. Built **ship-gated** so
nothing touches the live schools app until the backing security rule is deployed
and verified.

## Data model

| Where | Doc | Written by | Read by |
|---|---|---|---|
| Task definitions | `assignments/{school}` → `{ items: Assignment[] }` | GC (same school) | GC + every same-school student |
| Student completion | `progress/{uid}.assignmentCompletions` → `{ [assignmentId]: ts }` | the student (self-write, merge) | the student + same-school GC |

`Assignment` shape and the pure status helpers live in `data/assignments.ts`
(`assignmentStatus`, `summariseAssignments` — unit-tested in
`test/assignments.test.ts`). Completion deliberately does **not** write to the
shared `assignments/{school}` doc, so no student needs write access to a shared
document.

## Security rule

Added to `firestore.rules` (mirrors the proven `gcEvents/{schoolId}` rule):

```
match /assignments/{schoolId} {
  allow read, write: if request.auth != null && isGC() && schoolId == gcSchool();
  allow read: if request.auth != null
              && get(/databases/.../users/$(request.auth.uid)).data.school == schoolId;
}
```

Student completion reuses the existing `progress/{uid}` self-update rule (an
extra `assignmentCompletions` map is not restricted by the points/achievements
guards), and the GC already has same-school read on `progress`.

## Why it's gated

`ASSIGNMENTS_LIVE = false` in `data/assignments.ts`. The rule is committed but
**Firestore rules do not deploy with hosting** — they need
`firebase deploy --only firestore:rules`. Until that runs, any read/write to
`assignments/{school}` is denied; the accessors swallow the error and return
empty, so nothing crashes, but the feature would appear empty. Keeping the UI
gated avoids shipping a visibly-broken surface.

## Activation steps (all required, in order)

1. **Review + deploy the rule**: `firebase deploy --only firestore:rules`;
   verify against the emulator that (a) a GC can write only their own school's
   doc, (b) a student can read only their own school's doc, (c) a student cannot
   write it, (d) a student can still self-write `assignmentCompletions`.
2. **Thread the student's school** into the Paper Trail student surface
   (`AssignedStrip`) — currently the only missing wiring; `GCAssignPanel`
   already has `school` in the dashboard.
3. **Flip** `ASSIGNMENTS_LIVE = true`.
4. QA the full loop with a test GC + test student in the emulator before a live
   deploy.

## Safeguarding

No new personal data leaves the existing boundary: task text is GC-authored,
completion is a timestamp in the student's own progress doc, and all reads stay
within `isGC()`/same-school scope already enforced elsewhere in the rules.
