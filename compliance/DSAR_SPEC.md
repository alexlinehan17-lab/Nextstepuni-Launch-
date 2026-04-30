# DSAR / Erasure Request Flow — Specification

NextStepUni Learning Lab — GDPR Articles 15 (right of access) and 17 (right to erasure)

Document status: SPEC — not yet implemented in code
Prepared by: NextStepUni Ltd
Date: 2026-04-29

---

## 1. Purpose

This is the specification for the in-product flows that satisfy GDPR
Articles 15 (right of access — i.e. data subject access request, "DSAR")
and 17 (right to erasure). It documents what must be built; no code is
shipped under Phase 1.

Until these flows are implemented, the documented manual fallback (a parent
or student writes to NextStepUni's published support address; an engineer
fulfils manually) remains in force. That fallback is acceptable at pilot
scale (~534 students) but not at Year 2 scale (~2,000 students); see
`compliance/DPIA.md` R9.

---

## 2. Scope of the data subject's rights

### 2.1 Article 15 — Right of access

A data subject is entitled to:

- a confirmation that processing is occurring;
- a copy of the personal data being processed;
- the categories, source, recipients, retention period, and the data
  subject's other rights — most of which are already documented in the
  Controller's privacy notice (DPA Schedule 6 Section 6.3 has draft
  language) and can be returned as a static document accompanying the
  data export.

### 2.2 Article 17 — Right to erasure

A data subject is entitled to deletion of their personal data when:

- the data is no longer necessary for the original purpose (Art. 17(1)(a)),
- consent is withdrawn (17(1)(b)) — applicable since the lawful basis
  combines public-interest task with parental consent at school level,
- the subject objects under Art. 21 and there is no overriding legitimate
  ground (17(1)(c)),
- the data has been unlawfully processed (17(1)(d)).

Article 17 does **not** apply where processing is necessary for compliance
with a legal obligation, public health, archiving in the public interest,
or the establishment / exercise / defence of legal claims (17(3)). For an
edtech service these exceptions are rarely engaged; the operator should
fulfil the request unless a specific exception is documented.

### 2.3 Other rights mentioned in passing

- Article 16 (rectification): partly addressed in-product today (the
  student can edit their `subjectProfile`, `northStar`, name, avatar). A
  rectification request that names a specific field can usually be
  satisfied by directing the student to the in-product equivalent; the
  manual back-office process handles edge cases.
- Article 18 (restriction): not specced under Phase 1. Operationally rare
  in the edtech context; the Processor will handle case-by-case until
  volume justifies tooling.
- Article 20 (portability): the export format from the Article 15 flow
  (Section 4 below) is also the portability artefact. No separate flow
  required.
- Article 21 (objection): operationally maps to Article 17 in this
  service.

The Phase 1 spec calls for Article 15 and Article 17 only; that is what
this document specifies.

---

## 3. Identity verification

For both Article 15 and Article 17, the requester must prove identity
before any data is released or deleted. The following ladder is proposed:

1. **Authenticated request from inside the app** — the strongest proof.
   The request originates from a logged-in session, so the subject's
   identity is bound to their `request.auth.uid`. No additional verification
   needed.
2. **Authenticated request after a fresh sign-in** — for an erasure
   request, force a re-authentication immediately before the irreversible
   action. This protects against an unattended laptop being used to delete
   a student's data.
3. **Out-of-band request from a parent** — typically by email to the
   school. The school verifies the parent–child relationship through its
   own enrolment records, then forwards to NextStepUni. The Processor
   does not directly verify parents.
4. **Out-of-band request from a former student post-erasure stage 1** —
   if the student's account has already been anonymised under
   `compliance/RETENTION_POLICY.md` Section 3.2, identity cannot be
   verified by NextStepUni unilaterally. The Processor will direct the
   former student to their school of record to evidence identity, and
   will note in the response that identifying data has already been
   removed.

For Phase 1 implementation, only ladder rungs 1 and 2 are in scope (all
flows are in-app, authenticated). Ladders 3 and 4 are documented for the
manual fallback only.

---

## 4. Article 15 flow specification

### 4.1 Entry point

A new "Privacy" tab in the existing Settings view. It contains two
buttons: "Download my data" (Art. 15) and "Delete my account" (Art. 17).

### 4.2 User journey: Download my data

1. Student taps "Download my data".
2. UI shows: "We will prepare a machine-readable export of all the
   personal data we hold about you. This usually completes within a few
   minutes; we'll let you know when it's ready. Continue?"
3. On confirm, the client calls a new Cloud Function
   `requestDataExport({ uid })`. The function:
   a. Verifies `request.auth.uid == uid`.
   b. Creates a record in a new `dataRequests/{requestId}` collection
      `{ type: 'access', requesterUid, requestedAt, status: 'pending',
      slaDeadline (= +30 days) }`.
   c. Enqueues a background task (Cloud Tasks or a follow-up scheduled
      Cloud Function) to perform the export.
4. Background task reads, in parallel:
   - `users/{uid}`
   - `progress/{uid}`
   - `settings/{uid}`
   - `responses/{uid}`
   - `notifications/{uid}` (collection query)
   - `kudos` where `fromUid == uid` OR `toUid == uid`
   - `gifts` where `fromUid == uid` OR `toUid == uid`
   - `teachbacks` where `authorUid == uid`
   - `flares` where `senderUid == uid`
   - `flares/*/responses` where `responderUid == uid`
   - `gcNotes/{schoolId}/students/{uid}` (the GC notes about the student)
   - From Firebase Auth: email, account creation timestamp, last
     sign-in timestamp.
   The output is a single JSON document with one top-level key per
   collection, plus an `_audit` block recording the request ID, time,
   schema version and a SHA-256 of the export.
5. The export is stored to Firebase Cloud Storage at
   `data-exports/{uid}/{requestId}.json` with a 30-day signed-URL TTL.
6. The `dataRequests/{requestId}` record is updated:
   `status: 'fulfilled'`, `fulfilledAt`, `exportPath`.
7. A notification (in `notifications/{uid}`) is created: "Your data
   export is ready" with a deep-link to the download.
8. Download link is gated behind a fresh sign-in (per Section 3 ladder
   rung 2), to ensure the export is not collected by an unattended
   browser.

### 4.3 What the export must include

- All personal data above.
- The static "categories, sources, recipients, retention" notice
  (Article 15(1)(a)–(h)) — provided as a separate `notice.md` alongside
  the JSON.
- The Controller's contact details (the school) and the Processor's
  contact details (NextStepUni Ltd).
- The Processor's record of the data subject's previous DSARs (a list
  drawn from `dataRequests` for that uid).

### 4.4 What the export must NOT include

- Pseudonymous identifiers belonging to *other* users that happen to
  appear in the requesting user's records. Specifically: the `fromUid`
  on a kudos sent *to* this student is another student's UID; that UID
  is replaced in the export with a stable hash (`peer-<sha256(uid)[:8]>`)
  so that the export is portable but does not leak peer identifiers.
- GC private notes that the GC has marked as confidential (no such field
  exists today; if added later, this carve-out activates).

### 4.5 SLA

The Processor will fulfil within 30 calendar days of the
`requestedAt` timestamp. Operationally most requests will fulfil within
minutes. The 30-day SLA is the legal ceiling.

---

## 5. Article 17 flow specification

### 5.1 User journey: Delete my account

1. Student taps "Delete my account" (same Settings → Privacy entry as
   Section 4.1).
2. UI shows a clear and non-dismissable warning:
   "This will permanently delete your account and all associated data.
   This cannot be undone. If you only want a copy of your data, use
   'Download my data' instead.
   Are you sure?"
3. Student confirms (button "Yes, delete my account").
4. UI requires re-authentication: "Please re-enter your password to
   continue." (Section 3 ladder rung 2.)
5. UI shows a second confirmation: "Type DELETE to confirm" — a typed
   string match. Belt-and-braces against accidental deletion of a
   minor's account.
6. On confirm, the client calls a new Cloud Function
   `requestAccountDeletion({ uid })`. The function:
   a. Verifies `request.auth.uid == uid` and that the auth token is
      fresh (issued in the last 5 minutes).
   b. Creates a record in `dataRequests/{requestId}`
      `{ type: 'erasure', requesterUid, requestedAt, status: 'pending',
      slaDeadline (= +30 days) }`.
   c. Enqueues the deletion task.
7. Deletion task atomically (or as atomically as Firestore allows —
   Firestore transactions cap at 500 writes; a deletion that exceeds
   that is paginated and recorded as a multi-step task in
   `dataRequests`):
   - Delete `users/{uid}`
   - Delete `progress/{uid}`
   - Delete `settings/{uid}`
   - Delete `responses/{uid}`
   - Delete every doc in `notifications/{uid}` collection
   - For `kudos` where `fromUid == uid`: delete (this removes
     encouragement *sent by* the student; the recipient still has the
     record of having received it, but the sender field is set to a
     hashed peer label first, then the doc is deleted on the next pass —
     the spec proposes deletion outright, with a reviewer note below)
   - For `kudos` where `toUid == uid`: delete (the encouragement *to* the
     student is theirs to take with them)
   - For `gifts` where `fromUid == uid` OR `toUid == uid`: delete
   - For `teachbacks` where `authorUid == uid`: delete
   - For `flares` where `senderUid == uid`: delete; also delete the
     subcollection `flares/{flareId}/responses/*`
   - For `flares/*/responses` where `responderUid == uid`: delete
   - For `gcNotes/{schoolId}/students/{uid}`: delete
   - From Firebase Auth: `auth.deleteUser(uid)`
8. `dataRequests/{requestId}` is updated to `status: 'fulfilled'`.
9. The student is signed out client-side and shown a final screen
   confirming deletion is complete.

### 5.2 What is NOT deleted

- Anonymous, aggregate metrics derived from this student's activity
  before deletion (e.g. "in March 2026, students at school X completed
  1,247 study sessions") — these are not personal data and are out of
  scope.
- The audit-log record of the deletion itself in `dataRequests` and in
  the Cloud Function's Cloud Logging output. This must be retained
  because the Processor must be able to evidence fulfilment of the
  request to a regulator. The audit record contains the requester UID
  (now disconnected from any other personal data), the request ID, and
  timestamps. Reviewer note: this retention is permitted under Article
  17(3)(b) (legal obligation — accountability under Article 5(2)).

### 5.3 Edge cases

- **Pending DSAR at time of deletion**: if a download export is in
  progress when the deletion request arrives, the export is cancelled
  and any partial export file is deleted from Cloud Storage. The
  fulfilled-deletion notice supersedes.
- **GC initiating deletion of a student**: this path already exists in
  the GC dashboard but is incomplete (DPIA R9). Its replacement is the
  same `requestAccountDeletion` function, called from the GC dashboard
  with `{ uid: studentUid }` and a server-side check that the caller is
  GC of the same school. The student's record in `dataRequests` is
  attributed to the GC's UID (`actorUid`) so the audit trail is
  preserved.
- **Admin initiating deletion**: similar — same function, with
  server-side admin check.
- **Deletion of a student whose account is already at retention stage 1
  (anonymised)**: the function still runs and deletes the remaining
  aggregated data and Auth account, fulfilling the request fully.

### 5.4 SLA

30 calendar days from the request timestamp, same as Article 15. In
practice, the deletion is synchronous and completes within seconds; the
SLA covers the case where the deletion task is queued behind a backlog.

---

## 6. SLA tracking mechanism

### 6.1 The `dataRequests` collection

Schema (proposed):

```
dataRequests/{requestId}: {
  type: 'access' | 'erasure',
  requesterUid: string,            // who the request concerns
  actorUid: string,                // who initiated (== requesterUid for self-service)
  actorRole: 'self' | 'gc' | 'admin',
  requestedAt: Timestamp,
  slaDeadline: Timestamp,          // +30 days from requestedAt
  status: 'pending' | 'fulfilled' | 'cancelled' | 'partial-fail',
  fulfilledAt: Timestamp | null,
  exportPath: string | null,       // Storage path for access requests
  failureReason: string | null,    // populated if status == partial-fail
  cascadeReport: {                 // for erasure, what was actually deleted
    usersDeleted: number,
    progressDeleted: number,
    notificationsDeleted: number,
    kudosDeleted: number,
    giftsDeleted: number,
    teachbacksDeleted: number,
    flaresDeleted: number,
    flareResponsesDeleted: number,
    gcNotesDeleted: number,
    authDeleted: boolean,
  } | null
}
```

Firestore Security Rules:

- Read: only the requester (`requesterUid == request.auth.uid`), GCs of
  the requester's school, and admin.
- Create / update / delete: only by Cloud Functions (using the Admin
  SDK, which bypasses rules). No client write path.

### 6.2 Daily monitoring

A scheduled Cloud Function (`monitorDataRequestSla`, daily at 06:00
Europe/Dublin) queries `dataRequests` for any record with
`status == 'pending' && slaDeadline < now()`. Each such record is logged
to Cloud Logging at ERROR severity and emails NextStepUni's published
support address. **No request should ever hit this state** in normal
operation; the monitoring is a safety net.

### 6.3 Quarterly DSAR report

For PwC's Year 2 reporting cadence, a query of `dataRequests` for the
quarter produces:

- count by type and outcome,
- median fulfilment latency,
- any breaches of the 30-day SLA.

This is added as an appendix to the quarterly programme report that
NextStepUni is contracted to produce for participating schools.

---

## 7. Audit log format

Every action — request received, request fulfilled, request cancelled,
SLA monitor finding — appends an entry to a separate Firestore collection
`audit/{auditId}` with schema:

```
audit/{auditId}: {
  event: 'data-request.received' | 'data-request.fulfilled' |
         'data-request.cancelled' | 'data-request.sla-breach' |
         'account.deleted' | 'export.generated' | 'export.expired' |
         'gc.password-reset' | 'retention.stage1' | 'retention.stage2',
  actorUid: string,            // who caused the action
  actorRole: 'self' | 'gc' | 'admin' | 'system',
  targetUid: string,           // whose data is affected
  targetSchoolId: string | null,
  requestId: string | null,    // links to dataRequests
  timestamp: Timestamp,
  summary: string,             // human-readable one-line
  payload: object | null,      // structured detail; never includes free-text
                               // student content, only references and counts
}
```

Firestore Security Rules:

- Read: admin only.
- Create / update / delete: Cloud Functions only.

Retention: `audit` records persist for 24 months from creation, then are
deleted by the same scheduled function (`purgeFullyExpiredAccounts`) used
for general retention (Section 4.6 of `compliance/RETENTION_POLICY.md`).

---

## 8. Implementation gap

This entire spec is unimplemented. Estimated calendar effort:

| Item | Effort |
|---|---|
| `requestDataExport` Cloud Function + background export builder + Storage signed URL | 4–5 days |
| `requestAccountDeletion` Cloud Function + cascade implementation | 4–6 days |
| `monitorDataRequestSla` scheduled function | < 1 day |
| `dataRequests` and `audit` collections + Firestore rules | 1 day |
| Settings → Privacy UI tab + flows | 3–4 days |
| Re-auth middleware (or per-call token freshness check) | 1 day |
| Tests (the project has no test framework today; testing this end-to-end will require setting one up — see DPIA review note) | 3–5 days |
| **Total** | **3–4 weeks of engineering** |

Plus: written privacy-notice update describing the new in-product DSAR
flows; legal sign-off on the export schema and the carve-outs in
Section 4.4; alignment with the retention policy
(`compliance/RETENTION_POLICY.md`) so that an erasure on a partially-
anonymised account behaves correctly.

---

## 9. Reviewer notes

- The Phase 1 spec reasonably presumes that the DSAR flows operate on
  data the student can verify. In an edtech context, students under 18
  may legally have their rights exercised by a parent/guardian. The
  spec above does not implement a parental DSAR flow; that remains
  manual (Section 3 ladder 3). Legal counsel should confirm that this
  is acceptable for an in-product self-service feature, given that the
  underlying lawful basis sits with the school as Controller.
- The export carve-out in Section 4.4 (peer UIDs hashed) is a
  proportionality call. An auditor might prefer the carve-out to
  default the *other way* — peer UIDs are part of *this* student's
  data because they appear in *this* student's records. The Processor's
  position is the conservative one: do not export another data subject's
  identifier, even pseudonymous, in this subject's export. If counsel
  disagrees, change one line in the export builder and revisit.
- The `audit` collection retention (24 months) is the Processor's
  proposal. Evidencing fulfilment of an Article 17 request to a
  regulator requires retaining *some* record after the underlying data
  is deleted. 24 months is long enough for any reasonable regulator
  follow-up; 6 years would be the alternative ceiling (Statute of
  Limitations) but is excessive for a non-litigated edtech service.

---

## 10. Document control

- Companion to `compliance/DPIA.md` (R9), `compliance/RETENTION_POLICY.md`,
  and DPA Schedule 5 (operations security and rights workflow).
- Source code reviewed: commit `0ac6be4` on branch `main`, plus
  `firestore.rules` post-2026-04-29 R1 remediation.
