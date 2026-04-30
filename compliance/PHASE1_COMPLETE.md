# Phase 1 — Completion summary

NextStepUni Learning Lab — Empowering Futures Year 2 pre-PwC compliance hardening

Date: 2026-04-29
Source code state at completion: working tree at commit `0ac6be4`,
plus uncommitted edits listed in Section 1 below

---

## 1. Changes to repo files

### 1.1 firestore.rules — DPIA R1 remediation

The "Peer Islands" rule (formerly the trailing `allow read: …` block
inside `match /progress/{userId}`) was removed. Read access on
`/progress/{userId}` is now restricted to:

- self,
- admin (identified by hard-coded email `admin@nextstep.app`, unchanged),
- GC of the same school (`isGC()` plus school match, unchanged).

Full before/after diff and the reasoning is in
`compliance/REMEDIATION_LOG.md` entry dated 2026-04-29. The change is
**staged in the working tree but not deployed** (see Section 4 below).

### 1.2 README.md — Gemini drift removed

Replaced the AI Studio scaffold artefacts (banner image, "AI Studio app"
header, AI Studio dashboard link) and the GEMINI_API_KEY setup step with
a concise project description and an explicit "AI features: none
currently active" notice pointing at `compliance/`.

### 1.3 CLAUDE.md — Gemini drift removed

The "## Environment" section's GEMINI_API_KEY line was replaced with a
note that no environment variables are required for the current build,
referencing `compliance/GEMINI_AUDIT.md`.

### 1.4 No other application code was touched

Per the Phase 1 hard rule. A leftover debug `console.log` in
`components/KnowledgeTree.tsx` line 162 (introduced in a prior debugging
session) was **not** removed. See `compliance/ALEX_TO_CONFIRM.md` Q22.

---

## 2. New files in `/compliance/`

| File | Purpose |
|---|---|
| `REMEDIATION_LOG.md` | Append-only chronological record of compliance-driven changes. First entry: R1 firestore.rules remediation. |
| `GEMINI_AUDIT.md` | Independent re-verification of the AI integration claim, including git-history search. Conclusion (b) with nuance — see Section 3 below. |
| `RETENTION_POLICY.md` | Audit of current retention behaviour (none, effectively indefinite) plus a proposed policy and the implementation gap to close it. Marked PROPOSED throughout. |
| `DSAR_SPEC.md` | Specification for in-product Article 15 (access) and Article 17 (erasure) flows, with a `dataRequests` collection schema, an `audit` collection schema, and SLA tracking. Marked SPEC throughout. |
| `ALEX_TO_CONFIRM.md` | 24 structured questions covering Firebase configuration, contractual records, operational practice, and items raised by Phase 1. To be answered in one sitting before Phase 2 begins. |
| `PHASE1_COMPLETE.md` | This file. |

## 3. Updates to existing `/compliance/` files

| File | Change |
|---|---|
| `DPIA.md` | Risk R1 entry was updated in place. The original wording (Description, Likelihood, Severity, Overall risk) was preserved with "as identified" qualifiers; a new "Status" line at the top of the entry records "Code remediated 2026-04-29; pending production deploy" with a link to `REMEDIATION_LOG.md`. The narrative is now "identified during Year 2 governance preparation, remediated", which is the version PwC's risk team will read. The post-mitigation residual-risk table in DPIA Section 4.4 was not changed (its "Low" target value remains correct). |
| `AI_GOVERNANCE_SCHEDULE.md` | Section 1 (Scope and headline finding) was rewritten in place to reference `GEMINI_AUDIT.md`, note the historical leak fix in commit `063d574` (2026-04-06), and confirm the README/CLAUDE drift correction made today. The Section 7 inventory table row for "Gemini-backed features" was updated similarly. The Section 8 verification-method note was updated to reference today's git-history search. The four deterministic-feature sections (2–5) and the forward-looking Section 6 were not changed. |

---

## 4. Deviations from Phase 1 spec — judgement calls

These are the points where I made a call that the spec did not anticipate.
Each is surfaced here for your review before Phase 2.

### 4.1 Firebase CLI auth expired — could not deploy

Running `firebase projects:list` returned:
> Authentication Error: Your credentials are no longer valid. Please run
> `firebase login --reauth`.

Per the Phase 1 hard rule "Stop and surface any unexpected findings", I
did not attempt to work around the auth failure. The firestore.rules edit
is staged in the working tree; you must run `firebase login --reauth`
yourself, then run the dry-run and deploy. Exact commands in Section 6.

In addition, local validation via the Firebase Emulator was not possible
because the host machine has no Java runtime installed (the Firestore
emulator requires it). The rule edit was therefore reviewed manually for
syntactic correctness (it is a clean removal of a self-contained `allow
read: …;` block; brace and `match` counts are unchanged). I recommend you
run the dry-run before the live deploy to get an authoritative
confirmation.

### 4.2 Gemini audit — conclusion (b), not (a)

The previous session's compliance documents reported "no GenAI code, no
GenAI dependency installed, no historical GenAI commits". The first two
parts were correct; the third was incorrect. A `define:` block in
`vite.config.ts` did historically expose `GEMINI_API_KEY` to the client
bundle and was removed in commit `063d574` on 2026-04-06 with the
explicit changelog entry "Gemini API key leak removed from vite.config".

The substantive position has not changed (no live AI integration today),
but the narrative is now: a vulnerability was identified and fixed in the
codebase's normal security hygiene process, which is itself evidence of a
working vulnerability management practice. This is a stronger PwC-facing
position than "we never had any AI plumbing".

The old API key, if it was bundled into builds before 2026-04-06, is by
definition exposed forever. Question Q17 in `ALEX_TO_CONFIRM.md` asks
whether it has been rotated.

### 4.3 Admin identification — kept email-based

The Phase 1 spec described admin as `role == 'admin'`. The current
codebase identifies admin by hard-coded email (`admin@nextstep.app`); no
user has `role: 'admin'` set in their `users/{uid}` document. Migrating
to role-based admin is a separate change that requires backfilling the
admin user's role field plus running both checks during a transition.

I made the minimal change to close R1 and **kept admin email-based**, on
the grounds that:

- the spec's substantive requirement ("an admin… may read any
  /progress/{uid}") is satisfied by the existing email-based path;
- migrating during R1 remediation would couple two distinct changes;
- "no write paths loosened" is a hard rule and migrating admin to
  role-based without a corresponding backfill could *deny* admin
  access, which is the opposite problem.

`ALEX_TO_CONFIRM.md` Q19 surfaces this for your decision.

### 4.4 `users/{uid}` same-school read — left in place

The spec asked me to apply the same scoping logic to "any other
collection that currently uses the same-school read pattern (likely
studySessions, topicMastery, mockResults, gamification subcollections
under /progress)". Findings:

- those data classes are *not* subcollections; they are fields nested
  inside `progress/{uid}`. Fixing `progress` covered them.
- `users/{uid}` lines 19–22 *do* use the same-school read pattern, but
  tightening it would break the kudos / gifts / teachbacks / flares peer
  features which need to display peer names.
- the peer-collaboration collections (kudos, gifts, teachbacks, flares,
  flare responses) use same-school by design — that is the feature.

I therefore changed only `progress/{uid}`. The proportionality concern on
`users/{uid}` (cohort enumeration) remains open and is captured in DPIA
Section 3 and as a future-phase task.

### 4.5 Peer Island feature will degrade after deploy

The rule that was removed was the *only* path by which one student could
fetch another student's progress document. The Peer Island feature renders
peer state from such reads. After deploy, those reads will be denied and
the feature will appear empty or broken to students. Options are listed
in `ALEX_TO_CONFIRM.md` Q18.

### 4.6 DPIA R1 status is "Code remediated; pending deploy", not "Closed"

The spec asks for the status to change from Open to Closed. I changed it
to "Code remediated 2026-04-29; pending production deploy" because the
deploy step has not happened (Section 4.1). Status will progress to Closed
once you run the deploy and append the dry-run / deploy output to
`REMEDIATION_LOG.md`.

---

## 5. What I did not do (per spec)

- No retention deletion code written. `RETENTION_POLICY.md` lists the
  required Cloud Functions in Section 4 but does not implement them.
- No DSAR implementation. `DSAR_SPEC.md` is the specification.
- No legal-body DPA text drafted (out of scope).
- Did not send anything to PwC.

---

## 6. Exact next prompt for you

Once you have completed `compliance/ALEX_TO_CONFIRM.md`, run the
following prompt to deploy R1 and fold answers back into the documents.
Replace the bracketed sections with verbatim copies of your answers.

```
# Phase 2 — deploy R1 and integrate Alex's answers

## A. Deploy the staged firestore.rules change

I have completed compliance/ALEX_TO_CONFIRM.md (attached). Please:

1. Run `firebase deploy --only firestore:rules --dry-run` and paste the
   output verbatim. If the dry-run reports any errors, stop and surface
   them — do not deploy.
2. If the dry-run is clean, run `firebase deploy --only firestore:rules`
   and paste the output verbatim.
3. Append both the dry-run output and the deploy output, with timestamps,
   to compliance/REMEDIATION_LOG.md under the existing 2026-04-29 R1
   entry. Update DPIA.md R1 status from "Code remediated; pending
   production deploy" to "Closed [today's date]".

## B. Integrate the answers from ALEX_TO_CONFIRM.md

For each question that was answered with a definitive value (region,
DPA-on-file status, MFA posture, etc.), update the corresponding TBC in:

- DPIA.md (Sections 1.6 retention, 1.5 data flows, 4.1–4.3 mitigations)
- DPA_SCHEDULES.md (Schedule 1.2 duration, Schedule 4 sub-processors,
  Schedule 5 control mappings, Schedule 6 transfers)
- AI_GOVERNANCE_SCHEDULE.md (only if Q23/Q24 require updates)
- RETENTION_POLICY.md (Sections 2.7 backups, 3.7, 5)

For each question that was deferred, leave the TBC in place but add a
"Decision deferred to Phase 3" note pointing at ALEX_TO_CONFIRM.md.

## C. Resolve the deviations from PHASE1_COMPLETE.md Section 4

Specifically:

- Q17 (Gemini key rotation): if not rotated, recommend a Phase 3 rotation
  task and note it in REMEDIATION_LOG.md.
- Q18 (Peer Island feature): per the answer, either ship the
  Cloud-Function aggregator now (then create components/PeerIslandData.ts
  and a new Cloud Function `getPeerIslandSummary`), or document the
  deliberate temporary feature degradation in compliance/RELEASE_NOTES.md.
- Q19 (admin role migration): per the answer, either backfill role:'admin'
  on the admin user (one-line Firestore Console operation) and update
  firestore.rules to accept role==admin alongside the email check, or
  defer.
- Q20 (DEV controls): per the answer, env-gate or remove.
- Q22 (debug log in KnowledgeTree.tsx): per the answer, remove it or
  leave it for the white-cards debug.

## Hard rules
- Do not modify application code outside firestore.rules and the
  Cloud-Function aggregator if Q18 calls for it.
- Do not invent facts. If an answer is missing or ambiguous, say so.
- Append, don't rewrite, in the existing compliance documents.
- Stop and surface anything unexpected.
```

---

## 7. Reviewer notes for me reading this in Phase 2

- `ALEX_TO_CONFIRM.md` may surface that some assumed positions are wrong
  (for example: project might already be in `europe-west1`, in which case
  several documents simplify). The Phase 2 prompt above is structured to
  handle either outcome.
- The Phase 1 firestore.rules change is *minimal*. Phase 2 will likely
  need to add (a) a Cloud Function for the Peer Island aggregator, (b) an
  admin-role migration if elected, and (c) a school allow-list. Those
  three together represent ~1 sprint of code work.
- The DSAR and retention specs are the largest pending work items
  (~3–4 weeks each). They are deliberately scoped as Phase 3+, after
  ALEX_TO_CONFIRM is closed and Phase 2 has shipped the smaller code
  fixes.

---

## 8. Peer Island refactor — staged

Added 2026-04-29, after Alex's call on the Peer Island feature (Q18 in `ALEX_TO_CONFIRM.md`): the feature is rebuilt against a minimal public projection rather than killed.

### Decision recorded

`category` (NorthStarCategory) is included in the projection. Soft self-chosen aspiration; not Article 9 data; already implicit in the rendered theme; intrinsic to the feature's social-motivation purpose. Recorded explicitly in `compliance/DPIA.md` R1 entry.

### Files modified

| File | Change |
|---|---|
| `types.ts` | `IslandPlacement.purchasedAt` made optional. |
| `firestore.rules` | New `match /islandPublic/{uid}` block (read: same-school; write: `if false`). |
| `functions/src/index.ts` | Imports added; two new Cloud Functions appended (`onProgressWritten`, `onUserWritten`). Existing `resetStudentPassword` and `changeOwnPassword` unchanged. |
| `hooks/usePeerIslands.ts` | Rewritten to read from `/islandPublic` in a single same-school query. Exposed `PeerIsland` interface now has `placementCount` and `score` fields. |
| `components/journey/PeerIslandsList.tsx` | Leaderboard uses `peer.score` and `peer.placementCount` directly. The owner's entry still uses local `computeIslandScore`. |
| `compliance/DPIA.md` | R1 entry updated with refactor narrative and product decision note. |
| `compliance/DPA_SCHEDULES.md` | Schedule 3 amended with the new `islandPublic/{uid}` data category and its exact field list. |
| `compliance/REMEDIATION_LOG.md` | New entry dated 2026-04-29 (second of the day) documenting the rebuild. |

### Files created

| File | Purpose |
|---|---|
| `functions/src/islandProjection.ts` | Shared `buildPublicProjection()` helper used by both Cloud Functions. |
| `scripts/backfill-island-public.ts` | One-shot backfill. Default dry-run. `--apply` requires emulator or `--allow-production`. |
| `compliance/PEER_ISLAND_REFACTOR_PLAN.md` | Full design document, audit, and per-field rationale (created earlier in this session, before Alex's go-ahead on Section 4). |

### Build verification (performed)

```
$ cd functions && npm run build
> tsc
(clean)

$ npm run build
✓ built in 28.37s
(clean)
```

### Manual verification (to perform in the emulator before deploying to production)

1. Start emulator:
   ```
   firebase emulators:start --only firestore,functions
   ```
2. Seed Firestore with: two students at School-A (e.g., `studentA1`, `studentA2`), one student at School-B (`studentB1`). Each student needs a `users/{uid}` doc and a `progress/{uid}` doc with an `islandState` containing some `placements` and a `northStar.category`.
3. Wait a moment for the `onProgressWritten` trigger to fire; confirm `/islandPublic/{uid}` exists for each student in the emulator UI.
4. Inspect each `islandPublic` doc: only the projection fields should be present. No `pointsData`, `studyDebriefs`, `topicMastery`, raw `purchaseHistory`, or per-placement `purchasedAt`.
5. Sign in as `studentA1` and call `usePeerIslands` (open the Peer Islands modal in Journey view). Confirm `studentA2` appears with the correct theme (driven by `category`) and the correct piece count.
6. Sign in as `studentB1`. Open the Peer Islands modal. Confirm only School-B peers appear; `studentA1` and `studentA2` are absent.
7. Use the Firestore Rules Playground (or the Rules Tester in the emulator UI) to attempt a direct write to `/islandPublic/{anyUid}` from a client identity — must be denied.
8. From the same Rules Playground, attempt a read of `/progress/studentA2` while signed in as `studentB1` — must be denied (R1 remediation still effective and orthogonal).
9. Edit `studentA1`'s `users/{uid}` doc to set `role: 'gc'`. Wait for `onUserWritten` to fire. Confirm `/islandPublic/studentA1` is deleted (staff transition path).
10. Reset the role and confirm the projection reappears on the next progress write.

### Backfill — emulator first

```
# in shell A
firebase emulators:start --only firestore,functions

# in shell B
FIRESTORE_EMULATOR_HOST=localhost:8080 \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts                    # dry-run

FIRESTORE_EMULATOR_HOST=localhost:8080 \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts --apply            # real writes against emulator
```

### Deploy commands — production (run only after emulator validation passes)

In this exact order:

```
# 1. Re-authenticate the Firebase CLI (expired in earlier work)
firebase login --reauth

# 2. Build the functions one more time to make sure lib/ is current
cd functions && npm run build && cd ..

# 3. Dry-run the deploy. Inspect the output for the rule and function
#    summaries; confirm islandPublic rule and the two new functions are
#    in the changeset.
firebase deploy --only firestore:rules,functions --dry-run

# 4. Deploy.
firebase deploy --only firestore:rules,functions

# 5. Backfill — production. Use a service account with Firestore admin
#    permissions; do NOT run this from a developer's personal account.
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts                                # dry-run

GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json \
  GCLOUD_PROJECT=nextstepuni-app \
  npx tsx scripts/backfill-island-public.ts --apply --allow-production    # real writes
```

### After deploy

Append the `firebase deploy` output (rule digest hash, function deploy timestamps) to `compliance/REMEDIATION_LOG.md` under the 2026-04-29 entries. Update `compliance/DPIA.md` R1 status from "pending production deploy" to **Closed [date]**.

### Hard rules respected

- No deploy executed.
- No backfill executed against production.
- No application code modified outside the explicit refactor surface (Cloud Functions, the hook, the leaderboard score lookup, and the type field made optional).
- The leftover `console.log` debug line in `components/KnowledgeTree.tsx` from the prior white-cards session is **still present** and is **not** the refactor's concern; see ALEX_TO_CONFIRM.md Q22.
