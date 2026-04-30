# Remediation Log

NextStepUni Learning Lab — record of compliance-driven changes

This file is the chronological record of fixes applied in response to findings
in `compliance/DPIA.md` (and elsewhere). Entries are append-only and identify
the DPIA risk reference, the change applied, the verification performed, and
the post-change status.

---

## 2026-04-29 — DPIA risk R1: same-school cross-tenant read of `/progress/{userId}`

### Issue (factual)

`firestore.rules` previously contained, inside `match /progress/{userId}`, a
rule block titled "Peer Islands: students can read progress of same-school
peers" that granted `allow read` to any authenticated student whose
`users/{request.auth.uid}.school` matched the document owner's `school`. The
rule scoped reads at the *school* boundary, not at the *individual student*
boundary. A student logged into a participating DEIS school could therefore
issue a Firestore read for any peer's `/progress/{otherUid}` document and
receive that document in full, including the peer's `studyDebriefs` (free-text
reflective content), `topicMastery`, `studySessions`, `unifiedMockResults` and
all gamification fields. Reflective content may incidentally contain Article
9 health-adjacent material (DPIA Section 1.4).

The pedagogical justification for the rule was the in-app "Peer Island"
feature, which renders only a small subset of fields (notably points totals
and decorative state). The rule granted access to the entire document, not
the fields the feature consumed; this was disproportionate to the stated
purpose under GDPR Article 5(1)(c).

### Resolution

`firestore.rules` was edited at the document path
`/Users/alexlinehan/Nextstepuni-Launch-/firestore.rules`. The rule block was
removed in its entirety and replaced with an explanatory comment.

#### Old (removed)

```
      // Peer Islands: students can read progress of same-school peers
      allow read: if request.auth != null
                  && request.auth.uid != userId
                  && get(/databases/$(database)/documents/users/$(request.auth.uid)).data.school
                     == get(/databases/$(database)/documents/users/$(userId)).data.school;
```

#### New (in place)

```
      // Remediation 2026-04-29 (DPIA risk R1): the previous same-school
      // "Peer Islands" peer-read rule on /progress/{userId} was removed.
      // Read access is now restricted to: self, admin, GC of same school.
      // See compliance/REMEDIATION_LOG.md.
```

After the change, read access on `/progress/{userId}` is permitted under
exactly three conditions, all of which were already present in the rules
file before this change:

1. Self: `request.auth.uid == userId` (line 51).
2. Admin (currently identified by hard-coded email
   `admin@nextstep.app` — see "Deviation note" below): lines 53–54.
3. GC of the same school: `isGC()` and the document owner's school equals
   `gcSchool()` (lines 56–58, where `isGC()` checks
   `users/{request.auth.uid}.role == 'gc'`).

No write paths (`create`, `update`, `delete`) on `/progress/{userId}` were
modified. No other collection rules were modified.

### Deviation from spec (surfaced for review)

The Phase 1 instructions described admin as `role == 'admin'`. The current
codebase identifies admin by email (`admin@nextstep.app`), and the existing
admin user does not have `role: 'admin'` set in their `users/{uid}` document.
Migrating admin from email-based to role-based identification is a separate
change with its own risk surface: it requires either (a) backfilling
`role: 'admin'` onto the existing admin user document, or (b) running both
checks in parallel.

This Phase 1 change therefore makes only the minimal edit required to close
R1 — it does not migrate admin. The admin read on `/progress/{userId}` is
still permitted via the email check, which satisfies the spec's substantive
requirement ("an admin… may read any /progress/{uid}") without introducing
the migration risk. A role-based admin migration is captured as a question
for the next phase in `compliance/ALEX_TO_CONFIRM.md`.

### Other collections considered

The Phase 1 spec asked whether the same-school read pattern appears in other
progress-related collections (the spec named "studySessions, topicMastery,
mockResults, gamification subcollections under /progress").

Findings: those data classes are not stored as Firestore subcollections of
`/progress`. They are nested *fields* of the single `/progress/{userId}`
document. Restricting `/progress/{userId}` reads therefore restricts all of
them simultaneously. No further rule edits were required for this group.

The same-school read pattern does appear elsewhere in the rules file:

- `users/{userId}` lines 19–22: same-school peer read of the user document.
  Tightening this would break the kudos/gifts/teachbacks/flares peer
  features which need to display peer names. Not changed in Phase 1.
- `kudos`, `gifts`, `teachbacks`, `flares`, `flares/.../responses`: the
  same-school constraint is intrinsic to the feature semantics (peer
  collaboration is school-scoped by design). Not changed in Phase 1.
- `gcEvents/{schoolId}` lines 246–248: students read their own school's
  calendar events. Acceptable for the stated purpose (school calendar is
  shared by definition). Not changed in Phase 1.

The proportionality concern about `users/{userId}` cohort enumeration
remains open and is captured as a future-phase task.

### Verification

`firebase deploy --only firestore:rules --dry-run` was **not run** as part of
this remediation because the local Firebase CLI session is no longer
authenticated:

```
$ firebase projects:list
Authentication Error: Your credentials are no longer valid.
Please run firebase login --reauth
```

Local emulator validation was also unavailable because the host machine does
not have a Java runtime installed, which the Firestore emulator requires.

The rule edit was reviewed manually for syntactic correctness:

- the deleted rule block was a self-contained `allow read: if …;` statement
  bounded by a leading comment and trailing blank line;
- removal does not affect the brace structure of the surrounding
  `match /progress/{userId}` block;
- the file's `match` and brace counts before and after the edit are
  unchanged when counted by `grep -c`.

The deploy step is therefore staged but not executed. Alex must run, in this
order:

```
firebase login --reauth
firebase deploy --only firestore:rules --dry-run
firebase deploy --only firestore:rules
```

The dry-run output and the deploy confirmation will be appended to this log
once available.

### Re-classified status in DPIA risk register

- DPIA risk **R1** (same-school cross-tenant read of `progress`):
  status changes from **Open** to **Code remediated 2026-04-29; pending
  deploy**.
- The status will progress to **Closed** once the deploy step above
  completes successfully.

### Reviewer note

Legal counsel may reasonably ask whether the change has had any operational
impact on students. Because the rule that was removed was the *only* path by
which one student could fetch another student's progress document, any
in-product feature that depended on that path will have changed behaviour.
The Peer Island feature in particular renders peer state from
`progress/{otherUid}` reads. After deploy, these reads will be denied. Alex
must validate the Peer Island flow against the deployed rules and either
(a) restructure the feature to consume only data already accessible (for
example via a Cloud Function aggregator that returns only the small subset
of fields the feature needs), or (b) accept the feature degrades until that
restructure ships. This trade-off is captured in
`compliance/ALEX_TO_CONFIRM.md`.

---

## 2026-04-29 — Peer Island feature rebuild on minimal public projection

### Issue (factual)

The R1 remediation (above) closed the cross-tenant exposure by removing the same-school `progress/{userId}` read rule. That single rule was also the only path by which the Peer Island feature could load other students' islands. After deploy, the feature would have appeared empty to every user.

The Peer Island feature is a Year 2 priority and has substantive social-motivation purpose. Killing it was not the desired outcome of R1; the cross-tenant exposure was.

### Resolution

A new Firestore collection `/islandPublic/{uid}` was introduced. It contains a deliberately minimal projection of the data other students see in the peer view, and only that data:

- `name`, `avatar`, `school` (duplicated from `users/{uid}` for self-contained queries)
- `category` (NorthStarCategory; product decision to include — see `DPIA.md` R1)
- `placements[]` with per-placement `purchasedAt` **stripped**
- `placementCount` (pre-computed, non-starter)
- `score` (pre-computed; replaces raw `purchaseHistory`)
- `schemaVersion`, `updatedAt`

The full design and field-level reasoning is in `compliance/PEER_ISLAND_REFACTOR_PLAN.md`. The decision on the `category` field is recorded in `compliance/DPIA.md` R1 entry as a deliberate product call by Alex on 2026-04-29.

#### Code changes (staged in working tree, not yet deployed)

| Path | Change |
|---|---|
| `types.ts` | `IslandPlacement.purchasedAt` made optional (was required). Backwards-compatible: existing `HexIsland.tsx` already handled undefined via short-circuit. |
| `functions/src/islandProjection.ts` | New file. Shared `buildPublicProjection()` helper used by both Cloud Functions. Inlines its own `IslandPlacement` types so it has no dependency on the parent `types.ts`. |
| `functions/src/index.ts` | Added two new Cloud Functions: `onProgressWritten` (Firestore `onWrite` on `/progress/{uid}`) and `onUserWritten` (Firestore `onWrite` on `/users/{uid}`). Both write to `/islandPublic/{uid}` via the Admin SDK, which bypasses Firestore Security Rules. Both correctly handle deletions and role transitions (a user becoming staff causes the projection to be deleted). |
| `firestore.rules` | Added a new `match /islandPublic/{uid}` block before the default-deny rule. Read: same-school students only (with `exists()` defensiveness). Write: `if false` (server-side only via Admin SDK). |
| `hooks/usePeerIslands.ts` | Refactored. Now performs a single `where('school', '==', school)` query against `/islandPublic`, instead of the previous two-step (`/users` → per-user `/progress/{uid}`) pattern. The hook's exported `PeerIsland` interface now uses a thin `islandState` shape (just `category` and `placements`) plus pre-computed `placementCount` and `score`. |
| `components/journey/PeerIslandsList.tsx` | Leaderboard now uses `peer.score` and `peer.placementCount` directly from the projection. The current user's leaderboard entry continues to call `computeIslandScore(currentUserIsland.islandState)` because the owner has the full local state. |
| `scripts/backfill-island-public.ts` | New file. One-shot script to read every existing `/progress/{uid}` and write the projection. Default mode is dry-run; `--apply` requires the emulator unless `--allow-production` is also passed. |

#### Build verification

- `cd functions && npm run build` — clean, no TypeScript errors.
- `npm run build` (root) — clean, no TypeScript errors.

#### Behavioural verification (to be performed in emulator)

The emulator-based verification plan is documented in `compliance/PEER_ISLAND_REFACTOR_PLAN.md` Section 6 Step G. Briefly:

1. Seed two students at School-A, one at School-B.
2. Confirm same-school visibility, cross-school denial.
3. Confirm direct client writes to `/islandPublic` are denied.
4. Confirm cross-school reads of `/progress/{uid}` are denied (R1 still effective).

This is a manual emulator test; it is not yet performed because the Firebase CLI session expired (see R1 entry above).

### Verification (deploy step)

`firebase deploy --only firestore:rules,functions --dry-run` was **not run** as part of this remediation, again because the local Firebase CLI session is no longer authenticated. Alex must run, in this order:

```
firebase login --reauth
cd functions && npm run build
cd ..
firebase deploy --only firestore:rules,functions --dry-run
firebase deploy --only firestore:rules,functions
```

After deploy, run the backfill script:

```
# Emulator first (recommended)
firebase emulators:start --only firestore,functions
# in another shell:
FIRESTORE_EMULATOR_HOST=localhost:8080 \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts            # dry-run
FIRESTORE_EMULATOR_HOST=localhost:8080 \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts --apply    # real writes against emulator

# Production (only after emulator validation)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts                                # dry-run
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts --apply --allow-production    # real writes
```

The Cloud Function `onProgressWritten` ensures projections stay current going forward; the backfill is a one-shot to populate projections for students who already have `progress/{uid}` documents at deploy time.

### Re-classified status in DPIA risk register

DPIA risk **R1**: status was previously "Code remediated 2026-04-29; pending production deploy" (closing the data exposure only). It is now augmented with the rebuild — the underlying Peer Island use case is preserved via the `/islandPublic` projection, with the academic / behavioural / reflective field families excluded by design. Status will progress to **Closed** once the rules and Cloud Functions are deployed and the backfill is run.

### Reviewer note

PwC's risk team may reasonably ask whether the projection itself constitutes a new data exposure surface. The answer recorded for the audit:

- The projection contains *less* data than the previous rule allowed (academic, behavioural, reflective fields absent).
- The same-school read-only condition is unchanged from the prior rule's school-matching condition.
- The write path is now server-side only, removing client-side trust.
- The data exposure of `name`, `avatar`, `school`, `placements`, and `category` is unchanged from the existing peer-view UX; nothing visible to peers today is being moved to a *more* visible surface.

The trade-off is a small operational increase (two Cloud Functions, one new collection, one backfill) in exchange for a substantial reduction in disclosed data per peer view.

---

## 2026-04-30 — Finding: Firestore region is `europe-west2`, not `us-central1`

While deploying the new `onProgressWritten` / `onUserWritten` Firestore-triggered Cloud Functions, the Firebase CLI surfaced the actual database region in the Eventarc trigger path (`projects/nextstepuni-app/locations/europe-west2/triggers/...`). DPIA Section 1.5, DPIA R8, DPA Schedule 6 and ALEX_TO_CONFIRM Q1 had recorded `us-central1` as the assumed region; the actual region is `europe-west2` (London, EEA). Compliance documents to be updated in a later pass; flagged today only.

---

## 2026-04-30 — R1 fully closed: rules + functions + hosting deployed; smoke test passed

### Deploy chronology

1. `firebase deploy --only firestore:rules,functions` — rules deployed cleanly, but the two new Firestore-triggered functions (`onProgressWritten`, `onUserWritten`) failed to create on the first attempt with an Eventarc Service Agent permission-propagation error. Cause: this was the project's first 2nd-gen Firestore-triggered function; the Eventarc Service Agent had just been provisioned and IAM grants had not yet propagated. Standard Firebase first-time setup behaviour.

2. Retry of `firebase deploy --only functions` (after a few minutes for IAM propagation) — both new functions created successfully in `us-central1`. The existing `resetStudentPassword` and `changeOwnPassword` were skipped (no source change).

3. New GCP APIs enabled as a consequence (each required for v2 Firestore triggers, accepted in advance):
   - `run.googleapis.com`
   - `eventarc.googleapis.com`
   - `pubsub.googleapis.com`
   - `storage.googleapis.com` (already in use)

4. Smoke test surfaced an issue: Peer Islands appeared empty in the live app. Root cause: the original `match /islandPublic/{uid}` rule used `get()` on the *target* `/users/{uid}` doc to verify the school match, which Firestore's query verifier cannot evaluate against a query's potential result set, so the query was being denied wholesale even though individual docs would have been readable.

5. Rule updated to compare `resource.data.school` (the queried projection's own school field, which is part of the projection by design) against `get(/databases/$(database)/documents/users/$(request.auth.uid)).data.school`. Single `get()` on the requester's user doc; the target doc's school is read directly from the queried document via `resource`. Re-deployed with `firebase deploy --only firestore:rules`.

6. Smoke test still empty after the rule fix. Diagnostic `logger.info` added to `onProgressWritten` confirmed the projections were being written correctly (both Marino test accounts had matching `school: "marino"` in the projection). Investigation identified the live hosting bundle was the pre-refactor build (`index-DMpBYGTJ.js`); the refactored client code reading from `/islandPublic` had never been deployed. Phase 1 deploy plan in `compliance/PHASE1_COMPLETE.md` Section 8 listed only `firestore:rules,functions` and missed hosting. Process gap noted.

7. `npm run build` + `firebase deploy --only hosting` — new bundle (`index-XSKZi0Fr.js`) released. Verified live by curl-ing the homepage and matching the served `index-*.js` file against the local `dist/`.

8. Smoke test passed: with two Marino test accounts (one in `prove-myself` category, one in `options-freedom`), each account opening Peer Islands now sees the other's island with the correct theme, piece count, and score. Cross-school denial verified by virtue of the rule shape (no second school account on hand to test, but the rule structure cannot match across schools).

9. Diagnostic `logger.info` lines added in step 6 were reverted in `functions/src/index.ts` (they were logging `user.role`, `user.school`, `user.isAdmin`, `northStarCategory` and placement counts on every write — PII-adjacent data in Cloud Logging with default ~30-day retention; not appropriate as a permanent state). `onProgressWritten` redeployed without them.

### Final state in production

- `firestore.rules`: R1 peer-islands rule removed; `/islandPublic` rule live with the corrected `resource.data.school` comparison.
- Cloud Functions: `onProgressWritten` and `onUserWritten` running in `us-central1`, triggered off Firestore in `europe-west2`. `resetStudentPassword` and `changeOwnPassword` unchanged.
- Hosting: refactored client live; `usePeerIslands` reads from `/islandPublic` only; self-view continues to read `/progress/{uid}` directly.
- `/islandPublic` collection: populating organically as students do progress writes (no backfill run; deferred by deliberate decision — natural traffic catches up within days).

### Status

DPIA risk **R1**: **Closed 2026-04-30**. The cross-tenant exposure has been removed and the underlying Peer Island feature has been preserved on the minimal projection collection.

### Reviewer notes

- The rule fix in step 5 was a real bug, not a workaround. The original rule was incorrect for queries; the corrected rule is the right shape for this access pattern. PwC's risk team can verify the fix from the rule text directly: `resource.data.school` is the queried doc's school; the comparison against the requester's school via a single `get()` on `/users` is what makes the query verifier accept the rule.
- The hosting-deploy gap in step 6 was a process error in the Phase 1 plan, not a code issue. The deploy plan in `compliance/PHASE1_COMPLETE.md` Section 8 has been left unedited as a record of what was originally planned; the corrected end-to-end deploy sequence is captured in this entry.

---

(Future entries appended below.)
