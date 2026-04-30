# Data Retention Policy

NextStepUni Learning Lab — proposed retention policy and implementation gap

Document status: PROPOSED — not yet implemented in code
Prepared by: NextStepUni Ltd
Date: 2026-04-29

---

## 1. Purpose

This document records:

a. **What the application does today** about retention (audit of current
   behaviour).
b. **What it should do** to satisfy GDPR Article 5(1)(e) "storage
   limitation" given the data classes involved (DPIA Section 1.2 lists the
   exhaustive set).
c. **What code work is required** to move from (a) to (b).

The policy text in Section 3 is **proposed**. No deletion code has been
written or is to be written under Phase 1; Section 4 lists the work for a
later phase. Until the deletion code is shipped, the application is in a
state of *de facto* indefinite retention, which is not defensible under
Article 5(1)(e).

---

## 2. Current retention behaviour (audit)

### 2.1 Firestore TTL

There is **no Firestore TTL policy** configured on any collection. `firebase.json` does not define one. No collection has an `expireAt`-equivalent field that Google's TTL system is configured to act on.

### 2.2 Scheduled deletions or cron jobs

There are **no scheduled Cloud Functions** in `functions/src/index.ts`. The only Cloud Functions defined are `resetStudentPassword` and `changeOwnPassword` — neither performs any deletion or anonymisation.

### 2.3 In-product deletion paths

| Path | Where | What it deletes | Cascade? |
|---|---|---|---|
| GC-initiated student deletion | GC dashboard (per `docs/firestore-audit.md`) | `deleteDoc` on `progress/{uid}` then on `users/{uid}` | **Partial.** Does **not** delete `settings/{uid}`, `responses/{uid}`, `notifications/{uid}`, `gcNotes/{schoolId}/students/{uid}`, kudos/gifts/teachbacks/flares authored by the student, or the Firebase Auth account itself. |
| Admin-initiated student deletion | AdminDashboard (firestore.rules:40–41 grants delete on `users/{uid}` and `progress/{uid}` to `admin@nextstep.app`) | Same as GC | Same gaps |
| Self-initiated account deletion | **Not implemented** | n/a | n/a |
| Self-initiated data export (Article 15) | **Not implemented** | n/a | n/a |

### 2.4 Per-collection retention semantics observed in code

| Collection | Field that *implies* a retention boundary | Acted on? |
|---|---|---|
| `users/{uid}` | none | n/a |
| `progress/{uid}` (entire document — gamification, progress, study sessions, debriefs, mock results, topic mastery, etc., are nested fields, not subcollections) | none | n/a |
| `settings/{uid}` | none | n/a |
| `responses/{uid}` | none | n/a |
| `notifications/{uid}` | none | n/a |
| `gcNotes/{schoolId}/students/{studentId}` | none | n/a |
| `gcSettings/{schoolId}` | none | n/a |
| `gcEvents/{schoolId}` | per-event `date` field (semantic only) | not used for cleanup |
| `kudos/{kudosId}` | none | n/a |
| `gifts/{giftId}` | none | n/a |
| `teachbacks/{teachbackId}` | none | n/a |
| `flares/{flareId}` | `expiresAt` (set 24 hours after creation in `useFlares.ts`) | **Used only for client-side filtering of "active" flares; no deletion is triggered.** Documents persist indefinitely. |
| `flares/{flareId}/responses/{responseId}` | none | n/a |

### 2.5 Firebase Authentication

There is no inactivity-based account expiration policy configured. Firebase
Auth retains the account, password hash, sign-in metadata and any provider
linkage indefinitely until explicit `auth.deleteUser()` is called.

### 2.6 Local storage and IndexedDB

`localStorage['nextstep-settings']` (UI preferences only — see DPIA Section
3.2) persists until the user clears their browser storage. Firestore's
persistent local cache (configured in `firebase.ts`) is managed by the
Firebase SDK and is cleared when Firebase Authentication signs the user
out, when storage quota is exceeded, or when the user clears site data. The
Processor does not implement an explicit cache eviction policy beyond the
SDK default.

### 2.7 Backups

**TBC — Alex to confirm** whether any Firestore export-to-Cloud-Storage
backup schedule is configured at the project level. If yes, the backup
retention period is itself a retention boundary that the policy below must
be reconciled against.

### 2.8 Summary

The application today is **in effective indefinite retention**. The only
exit path for a student's data is a manual GC- or admin-initiated deletion
that leaves several derivative collections orphaned. There is no
per-collection TTL, no scheduled purge, no inactivity-based anonymisation,
and no documented retention period.

---

## 3. Proposed retention policy

The policy below applies only after it is implemented in code (Section 4).
Until then, it is the documented intent only.

### 3.1 Active student accounts

While the student is enrolled in the programme — defined operationally as
"the student's `users/{uid}` document exists and has been signed-in to within
the past 12 months" — all data classes listed in DPA Schedule 3 are retained
in their original form to support the educational service.

### 3.2 Post-Leaving Cert / inactivity stage 1 (24 months)

24 months after the latest of (a) the student's recorded `examStartDate`,
(b) the student's last sign-in, or (c) the student's `users/{uid}` document
creation date, the account transitions to "inactive". On transition:

- `users/{uid}.name` is replaced with a neutral string (e.g. `"Alumnus"` or
  a school-anonymised label).
- `users/{uid}.avatar` is set to a fixed default seed.
- The Firebase Authentication record's email is replaced with a synthetic
  unique email (`anon-<sha256-truncated>@nextstep.app`); password is reset
  to a random unrecoverable value.
- `responses/{uid}` is deleted in full (free-text reflective content cannot
  be reconciled with anonymisation).
- `progress/{uid}.studyDebriefs` (free-text reflections) is replaced with
  the structured aggregate metadata only (date, subject, confidence
  before/after, perceived grade, points earned) — the free-text field is
  removed.
- `notifications/{uid}` is deleted in full.
- `gcNotes/{schoolId}/students/{uid}` is deleted in full.
- The aggregate, non-identifying parts of `progress/{uid}` (points totals,
  module unlock state, study session counts and durations, topic mastery
  state, mock result patterns) are retained for programme analytics. They
  are no longer linked to a real identity at this point.

### 3.3 Inactivity stage 2 (36 months from creation, i.e. 12 months after
stage 1)

36 months after the originating event in 3.2, all remaining records are
deleted in full:

- `users/{uid}`
- the entirety of `progress/{uid}`
- `settings/{uid}`
- the Firebase Authentication account
- any kudos / gifts / teachbacks / flares / flare responses where the
  user was author or recipient (these are scheduled for cascade deletion
  at this stage, since the linked author/recipient identifier is no
  longer attached to a real person).

### 3.4 Guidance Counsellor accounts

When the school notifies NextStepUni that a GC has left their role, the GC
account is deleted within 30 calendar days. Deletion comprises:

- the Firebase Authentication account,
- the `users/{uid}` document,
- any `gcSettings/{schoolId}` and `gcEvents/{schoolId}` records *authored
  by* this GC are retained (they are school-level data, not GC-personal).

The GC's name on previously-recorded `gcNotes/{schoolId}/students/{uid}`
documents is replaced with a generic "Former counsellor" label so that the
student-facing record is preserved (the school may need it for continuity)
while the personal identifier of the former GC is removed.

### 3.5 GC notes referencing students who have been deleted

When a student account transitions to inactivity stage 2 (Section 3.3), any
`gcNotes/{schoolId}/students/{uid}` document for that student is deleted at
the same time as the underlying user record.

### 3.6 Operational records

System logs, audit logs (DSAR fulfilment log, password reset log if
implemented per DPIA T-NEW-6) are retained for 24 months from creation,
then deleted. This is an operational compliance requirement, not a
student-facing retention rule.

### 3.7 Backups

**TBC — Alex to confirm** Firestore backup schedule. If backups exist, the
policy will be: backups are retained for 35 days (Google Cloud Firestore
default for managed exports). The Processor will not retrieve from backup
to restore data that has reached its retention end-of-life under the
policy above.

---

## 4. Implementation gap and proposed work

The policy in Section 3 cannot be enforced until the following code is
written. **None of this is to be implemented under Phase 1.** This list is
the input for Alex's next-phase planning.

### 4.1 Scheduled Cloud Function: `markInactiveAccounts`

- Trigger: Cloud Scheduler, daily at 03:00 Europe/Dublin.
- Behaviour: query `users/{uid}` for records meeting the Section 3.2
  trigger (24 months elapsed since latest of `examStartDate`, last
  sign-in, or document creation). For each, run the anonymisation
  transaction in 3.2. Append a record to a new `audit/{auditId}`
  collection writable only by Cloud Functions.
- Idempotency: each record carries a flag (e.g. `inactiveStage1At`) so a
  re-run does not reprocess.
- Surface area: only `progress/{uid}.studyDebriefs`,
  `responses/{uid}`, `notifications/{uid}`,
  `gcNotes/{schoolId}/students/{uid}`, and the identity fields on
  `users/{uid}` and Firebase Auth. The aggregate progress data is
  retained.

### 4.2 Scheduled Cloud Function: `purgeFullyExpiredAccounts`

- Trigger: Cloud Scheduler, daily at 04:00 Europe/Dublin.
- Behaviour: query for records with `inactiveStage1At` older than 12
  months. For each, atomically delete:
  - `users/{uid}`, `progress/{uid}`, `settings/{uid}`
  - Firebase Authentication account (`auth.deleteUser`)
  - Cascade across `notifications/{uid}` (already deleted at stage 1, but
    re-checked), `responses/{uid}` (same)
  - `kudos`, `gifts`, `teachbacks`, `flares`, `flares/.../responses` where
    `fromUid`, `toUid`, `authorUid`, `senderUid` or `responderUid` equals
    the deleted user. (This requires Firestore queries that may be
    expensive at scale; the implementation should use a Firestore listener
    or a paginated `getDocs` loop with a batch limit per execution.)

### 4.3 Cloud Function: `removeGuidanceCounsellor`

- Trigger: Cloud Functions `onCall`, callable only by admin (per
  firestore.rules's existing admin path).
- Behaviour: delete the GC's auth account and `users/{uid}` document.
  Update `gcNotes/{schoolId}/students/*` documents authored by this GC to
  set the author label to "Former counsellor".

### 4.4 Firestore TTL on `flares/{flareId}`

- Configure Firestore TTL with `expiresAt` field as the trigger. This
  delivers Section 3 indirectly for the flares collection only (flares
  have a 24-hour active window; once expired, they should not persist).
- Ensure subcollection `flares/{flareId}/responses/{responseId}` is
  deleted by the same TTL or by a Cloud Function triggered on parent
  delete.

### 4.5 New `audit` Firestore collection

- Schema: `{ event, actorUid, targetUid, summary, timestamp }`.
- Rules: writable only by Cloud Functions (using the Admin SDK, which
  bypasses Firestore Security Rules); readable only by admin role.
- Used by all scheduled functions above and by the DSAR fulfilment flow
  (see `compliance/DSAR_SPEC.md`).

### 4.6 Retention status indicators in the UI

- Student-facing: at sign-in, if the account is within 6 months of stage 1
  anonymisation, display a notice ("Your account will be anonymised on
  [date]; sign in any time to extend").
- Admin/GC dashboard: a column showing each student's projected stage 1
  date, allowing exceptions to be flagged.

### 4.7 Migration of existing accounts

When the policy is first enabled, a one-time migration is required to set
`inactiveStage1At` on accounts that are already past the 24-month boundary,
so they are not anonymised in a single batch on the first run of the
scheduled function. The migration should run those accounts through the
anonymisation transaction one-by-one over a controlled window, with logging
to `audit`, and surface unexpected cases (e.g. accounts that have been
inactive for more than 36 months but never deleted) for manual review.

### 4.8 Estimated effort

| Item | Calendar effort |
|---|---|
| 4.1 markInactiveAccounts | 2–4 days |
| 4.2 purgeFullyExpiredAccounts (incl. cascade) | 4–6 days |
| 4.3 removeGuidanceCounsellor | 1 day |
| 4.4 Firestore TTL on flares | < 1 day |
| 4.5 audit collection | 1 day |
| 4.6 UI status indicators | 2–3 days |
| 4.7 Migration of existing accounts | 2–3 days, plus controlled rollout window |
| **Total** | **2–3 weeks of engineering, plus migration window** |

Plus: written retention notice to students/parents, signed off by school
DP lead. Plus: confirmation from legal counsel that the periods (24m / 36m
/ 30d / 24m operational logs) are defensible.

---

## 5. Reviewer notes

- **The 24-month / 36-month numbers are proposals, not legal requirements.**
  Irish DPC guidance does not specify retention durations for educational
  services serving minors; it requires that retention be documented,
  proportionate, and enforced. Legal counsel may compress or extend these
  periods. The Processor's reasoning for the proposed values: 24 months
  covers a typical "appeal / repeat year / bridging" window after the
  Leaving Cert; an additional 12 months at Stage 2 covers any retrospective
  programme analytics with a clear cut-off.
- **PwC may ask whether the aggregate retention at Stage 1 is itself
  personal data.** If retained study patterns are linkable back to an
  individual via combination with other fields (school, year group,
  subject mix), the anonymisation in Section 3.2 has not actually been
  achieved. The Processor's position: school-and-year-and-subject-mix is
  re-identifying for very small cohorts; the retained aggregate must
  therefore be coarse (counts and durations, not session-by-session). The
  implementation in 4.1 must enforce this.
- **Backups (Section 3.7) and the policy's interaction with them must be
  documented in the privacy notice.** A right-to-erasure request that
  precedes a backup snapshot must result in the backup itself being
  re-generated or scrubbed; this is operationally non-trivial. **TBC.**

---

## 6. Document control

- This policy is companion to `compliance/DPIA.md` (R10) and
  `compliance/DSAR_SPEC.md`.
- Source code reviewed: commit `0ac6be4` on branch `main`, plus
  `firestore.rules` post-2026-04-29 R1 remediation.
