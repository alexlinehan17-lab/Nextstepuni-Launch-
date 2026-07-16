# Security & Penetration Review — NextStepUni (pre-launch)

**Date:** 2026-07-16
**Type:** Authorised white-box security review of the owner's own pre-launch
application (no live users / no minors' data at risk at time of review).
**Method:** static audit of the access-control boundary (Firestore + Storage
rules), the Cloud Functions backend, client auth flows, secrets & dependencies,
and the XSS / PII / minors-data / GDPR surface. No live probing of a running
instance.
**Scope reviewed:** `firestore.rules`, `storage.rules`, `firebase.json`,
`functions/src/{index,dataRights,islandProjection}.ts`, `functions/package.json`,
`components/LoginPage.tsx`, `contexts/AuthContext.tsx`, `utils/exportCsv.ts`,
`components/gc/*`, `components/PaperTrail/GuardianConsent.tsx`,
`data/guardianSummary.ts`, `docs/pre-ship-audit.md`, and the wider
`components/`, `hooks/`, `contexts/`, `utils/` tree for injection sinks.

> **Context.** The platform serves largely **minors** (Irish secondary
> students; Irish GDPR digital age of consent = 16). Multi-tenant by *school*.
> The Firestore security rules are the real access-control boundary, and they
> are mature and defensible — the prior same-school `/users` and `/progress`
> peer-read leaks were already remediated (DPIA R1) and there is a default-deny
> catch-all. The findings below are hardening and completeness items, **not** an
> open door. **No Critical, and no cross-school IDOR, was found.**

---

## Severity summary (consolidated, de-duplicated)

| Sev | Count | Fixed in this change | Flagged for owner decision / action |
|-----|------:|---------------------:|------------------------------------:|
| HIGH | 3 | 1 | 2 |
| MEDIUM | 8 | 6 | 2 |
| LOW / Info | 8 | 4 | 4 |

"Fixed" = shipped in the same change as this report and verified through the
gate (lint 0 / typecheck 0 / 1770 tests / app build / functions `tsc`).
"Flagged" = requires a product/design decision, a backend flow that can't be
safely auto-built, or an action only the owner can perform (e.g. revoking a key
in Google Cloud Console).

---

## HIGH

### H-1 — GC could reset-password / cascade-delete another *staff* account in the same school  ✅ FIXED
- **Where:** `functions/src/index.ts` `resetStudentPassword`; `functions/src/dataRights.ts` `authorize()` GC branch (reached by `requestAccountDeletion` and `exportMyData`).
- **Exploit:** A GC (role `gc`) passed the UID of *another GC at the same school* as the target. The code verified same-school but never that the target was a **student**, so a malicious/compromised GC could reset (→ impersonate) or cascade-delete a colleague GC — and, if an admin ever carried a matching `school`, admin too.
- **Fix shipped:** both GC paths now reject a target whose `role` is `gc`/`admin` or whose `isAdmin === true`. GCs can only act on student accounts.

### H-2 — Self-asserted `school` = no verified tenant isolation  ⚠️ FLAGGED (design decision)
- **Where:** `firestore.rules` `/users` create rule — `school` is any client-supplied string ≤50 chars, immutable after.
- **Exploit:** A student (or anyone who can register) types *any* school name and thereby joins that school's peer graph — reads same-school peers' free-text posts (teachbacks), becomes visible to that school's GC, and can inject content into that school's student feed (a safeguarding concern, not just privacy). There is no join-code / GC-approval / email-domain verification binding a user to a school.
- **Why not auto-fixed:** the remedy is a product decision that changes onboarding UX. Options: (a) per-school **join codes** issued by the GC; (b) **GC approval** of new students before they enter the peer graph; (c) **email-domain allow-list** per school. See the question at the end of this document.

### H-3 — Guardian-summary consent is self-asserted by the minor and unverified  ⚠️ FLAGGED (must-fix-before-activation; feature currently OFF)
- **Where:** `components/PaperTrail/GuardianConsent.tsx`, `data/guardianSummary.ts`.
- **Exploit:** The weekly guardian summary (effort-only, never grades) is enabled entirely by the student typing *any* email — no confirmation, no proof of parental responsibility. Under Irish GDPR (age 16), processing an under-16's data on a consent basis needs consent given/authorised by the holder of parental responsibility; a child self-asserting an address does not satisfy that.
- **Mitigating:** the feature is **ship-gated OFF** (`GUARDIAN_EMAILS_LIVE = false`) — no email is sent today, so this is not a live leak.
- **Why not auto-fixed:** the real fix is a **double-opt-in verification flow** (guardian must click a confirmation link) plus a recorded parental-consent artefact / routing consent through the school as controller — a backend flow that should be designed, not silently scaffolded. **Do not flip `GUARDIAN_EMAILS_LIVE` to true until this exists.**

---

## MEDIUM

### M-1 — GDPR erasure was incomplete: the user's replies on *other* students' flares survived  ✅ FIXED
- **Where:** `functions/src/dataRights.ts` `cascadeDeleteUser`.
- **Detail:** erasure deleted flares the user *sent* and their responses, but not responses the user *authored* on someone else's flare (`responderUid == uid`) — leaving user-authored free text + identifier after a valid Article-17 erasure.
- **Fix shipped:** added a collection-group sweep over `responses` filtered by `responderUid == uid` (in-memory filter to avoid a new index; flares is decommissioned so volume is negligible), counted as `flareResponsesDeleted` in the cascade report.

### M-2 — Self-export handed the student the GC's private notes  ✅ FIXED
- **Where:** `functions/src/dataRights.ts` `exportMyData`.
- **Detail:** `gcNotes` was included for **any** actor, so a student self-export returned the guidance counsellor's private pastoral/safeguarding notes (third-party data; commonly under subject-access exemptions).
- **Fix shipped:** `gcNotes` is now included only when the actor is `gc`/`admin`, never on a `self` export.

### M-3 — `islandState.placements` copied into the peer-readable projection unbounded  ✅ FIXED
- **Where:** `functions/src/islandProjection.ts` `buildPublicProjection`.
- **Detail:** `islandState` is entirely student-controlled; the trigger copied `placements` verbatim into `/islandPublic/{uid}`, which every same-school peer downloads → read-amplification / cost DoS, and unbounded write cost in the trigger.
- **Fix shipped:** cap `placements` (and `purchaseHistory`) to 500 entries, clamp each string field to 120 chars, and coerce `type`/`q`/`r` to safe values.

### M-4 — CSV formula/macro injection in the GC export  ✅ FIXED
- **Where:** `utils/exportCsv.ts` `escapeCSV`.
- **Detail:** a student's display name (unrestricted content) flowed into GC-exported CSVs. `escapeCSV` didn't neutralise the spreadsheet formula prefixes `= + - @`, so a name like `=HYPERLINK(…)` executes when a GC opens the file in Excel/Sheets, able to exfiltrate adjacent cells (other minors' data) or trigger DDE.
- **Fix shipped:** any cell beginning with `= + - @` / tab / CR is now prefixed with an apostrophe before quoting; also handle a stray `\r`.

### M-5 — Weak 6-char password floor for a minors' platform  ✅ FIXED (client + function)
- **Where:** `components/LoginPage.tsx` (register validation + strength hint), `functions/src/index.ts` `changeOwnPassword`.
- **Fix shipped:** minimum raised to **8** in the register step, the live strength hint, and the Cloud Function floor. **Owner follow-up:** also enable Firebase Identity Platform's server-side password policy so the length floor can't be bypassed via the Auth REST API directly.

### M-6 — GC login flow disclosed which schools have a provisioned counsellor account  ✅ FIXED
- **Where:** `components/LoginPage.tsx` `handleGCLogin`.
- **Detail:** distinct "no account for this school" vs "wrong password" messages let anyone enumerate provisioned GC accounts (GC emails are deterministic; the school list is public) to target for brute-force.
- **Fix shipped:** collapsed to a single generic "Sign-in failed" message (network error kept separate). **Owner follow-up:** ensure Identity Platform email-enumeration protection is ON at the project level (hardens the reset flow too).

### M-7 — "Anonymous" teach-backs are de-anonymisable by same-school peers  ⚠️ FLAGGED (needs projection like islandPublic)
- **Where:** `firestore.rules` teachbacks read rule; `components/study/TeachBackCard.tsx` ("A classmate shared…").
- **Detail:** the stored doc carries `authorUid` and the read rule grants every same-school student the whole document → a peer can map an "anonymous" explanation back to its author's UID. For minors this is a real anonymity-promise gap.
- **Why not auto-fixed:** the correct fix mirrors `islandPublic` — serve teach-backs through a **Cloud-Function-written projection** holding only `subject` + `explanation` + counts (no `authorUid`), and deny direct peer reads of the source doc. That's a new trigger + rules change + client read-path change that should be built and tested deliberately rather than rushed under a security patch. Recommended as the next backend task.

### M-8 — Special-category minor welfare labels (DEIS / At-risk / Priority) in plaintext localStorage  ⚠️ FLAGGED (recommend server-side move)
- **Where:** `components/gc/cohortTags.ts` — keyed by student UID under `gc:cohortTags:{school}`, unencrypted, school-scoped (not GC-scoped), never cleared on logout, and outside the DSAR cascade.
- **Why not auto-fixed:** the right fix is to move these labels into a **GC-scoped, rules-protected Firestore collection** (like `gcNotes`) so they get access control, DSAR export/erasure coverage, and no shared-device exposure. That's a data-model change with a migration, not a one-line patch. Interim hardening (bind the key to the GC's UID + clear on logout) is possible but leaves the data client-side; recommend the server-side move.

---

## LOW / Informational

### L-1 — Temp passwords used `Math.random()` (not a CSPRNG)  ✅ FIXED
`functions/src/index.ts` now uses `crypto.randomInt` for the GC-reset temporary password.

### L-2 — Client trusted `data.isAdmin` from the user doc for the session flag  ✅ FIXED
`components/LoginPage.tsx` now derives `isAdmin` from `cred.user.email === 'admin@nextstep.app'` (matching `AuthContext` and the server-side rules check) — a single source of truth. (Never exploitable as-is: `isAdmin` is forbidden on client writes and real admin access is gated on the verified email token, not the doc field.)

### L-3 — Missing CSP + HSTS headers  ✅ PARTIALLY FIXED
`firebase.json` now sends **HSTS** (`max-age=31536000; includeSubDomains`) and a **Content-Security-Policy-Report-Only** (so it cannot break the app while the policy is observed). **Owner follow-up:** review CSP reports, then promote to an enforcing `Content-Security-Policy` (tighten `script-src`/`style-src` away from `'unsafe-inline'` once Vite/framer-motion needs are confirmed).

### L-4 — Live-looking Gemini API key committed in a tracked doc  ✅ REDACTED / ⚠️ OWNER MUST REVOKE
- **Where:** `docs/pre-ship-audit.md` contained `GEMINI_API_KEY=AIza…VvE` in plaintext (also in git history, commit `88e86fb`).
- **Fixed here:** the literal value is redacted in the doc.
- **Owner must do:** **revoke/regenerate the key** in Google Cloud Console → APIs & Services → Credentials (it powers nothing, so revocation is zero-risk). Because it's in git history, revocation is the real remediation. Close `compliance/ALEX_TO_CONFIRM.md` Q17. Also set **HTTP-referrer restrictions** on the (expected-public) Firebase web `apiKey` in `firebase.ts`.

### L-5 — No email verification before account use  ⚠️ FLAGGED
Registration grants a session with no email-ownership proof. Low escalation potential (no privileged role reachable this way), but it undermines the enrolment consent basis and account recovery. Recommend sending a verification email and gating password-reset (or sensitive actions) on it. Not auto-fixed because it changes the onboarding flow and needs a "check your email" UI.

### L-6 — Dependency CVEs (non-reachable) + `npm audit fix`  ⚠️ FLAGGED (owner, low priority)
Root: 1 critical (`websocket-driver` via unused `@firebase/database`) + 1 high (`undici` via test-only `jsdom`) — both non-reachable at client runtime. `functions/`: 18 transitive under `firebase-admin`, low practical exploitability. Recommend `cd functions && npm audit fix` at next maintenance and re-verify the functions build/deploy; not launch-blocking.

### L-7 — Cohort-stat poisoning / no server-side rate limits  ⚠️ FLAGGED
Aggregate counters (`chairCohorts/*`, `focusPresence/*`) are pinned `+1`/bounded but allow unlimited writes, and per-user daily limits on kudos/gifts/teachbacks are client-side only → a single student can poison a class aggregate or spam peers. Proper mitigation is server-side (Cloud Function or App Check + throttling), out of scope for a rules-only patch. Small at pilot scale; recommend before wider rollout.

### L-8 — Small-cohort de-anonymisation; DEV "Skip Login" button (native only)
- Cohort aggregates with a 1–2 person class code reveal the individual — apply a minimum-N suppression (n ≥ 5) before showing percentages/histograms. Low priority.
- `components/LoginPage.tsx` DEV "Skip Login" is correctly gated to native/localhost (stripped from the deployed web app); remove before an App Store submission.

---

## Done well — controls to preserve (do NOT regress)

- **No cross-school IDOR.** Every school comparison in the functions reads *both* the caller's and target's `/users` doc **server-side**; rules gate GC reads on `school == gcSchool()`.
- **Admin & GC authority is server-enforced** (`request.auth.token.email == 'admin@nextstep.app'`; `isGC()` reads the server-side, client-immutable `role`), not a client-only gate. Client `isAdmin`/`role` flags gate UI only.
- **`role` / `school` / `isAdmin` are immutable / forbidden on client writes** to `/users` — closes the classic client-writable-role escalation.
- **`/islandPublic` is `write: if false`** — only the Admin-SDK trigger writes it; peers read a minimal projection that strips `purchasedAt` / raw `purchaseHistory`.
- **DSAR implemented end-to-end** with fresh-re-auth for self-service erasure, peer-UID hashing on export, and server-only audit rows to `/dataRequests`.
- **XSS surface is essentially nil** — no `dangerouslySetInnerHTML`/`innerHTML`/`eval`/`new Function` anywhere in app source; all UGC rendered as auto-escaped JSX; DiceBear via `encodeURIComponent` + `<img>`; PDFs are a trusted, non-writable corpus.
- **No injection surface** in functions — parameterised Firestore queries, no `eval`/shell/child_process, no user-controlled outbound fetch (no SSRF).
- **Security headers** already present: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`.
- **Default-deny catch-all** at the bottom of `firestore.rules`; documented remediation history; storage `papers/**` read-only with deny-all-else.

---

## Owner action list (things only you can do)

1. **Revoke the Gemini key** in Google Cloud Console (L-4) and close `ALEX_TO_CONFIRM.md` Q17.
2. **Set HTTP-referrer restrictions** on the Firebase web `apiKey` (L-4).
3. **Enable Firebase Identity Platform** server-side password policy + email-enumeration protection (M-5, M-6).
4. **Do not activate guardian summaries** (`GUARDIAN_EMAILS_LIVE`) until a verified double-opt-in consent flow exists (H-3).
5. **Decide the school-verification model** (H-2) — join codes / GC approval / domain allow-list. *See question below.*
6. Optional/next-task: teach-back projection (M-7), cohort-tags server-side move (M-8), `npm audit fix` in functions (L-6), server-side rate limits (L-7), promote CSP to enforcing (L-3).

## Open question for the owner (H-2 — highest-value design decision)

How should a user be bound to a school so they can't just type any school name
and join its peer graph? Recommended: **per-school join codes issued by the GC**
(lowest friction, works for the pilot). Alternatives: GC approval of new
students, or per-school email-domain allow-list. This is the one finding whose
fix is a genuine product decision — everything else above is either shipped or
an owner action.
