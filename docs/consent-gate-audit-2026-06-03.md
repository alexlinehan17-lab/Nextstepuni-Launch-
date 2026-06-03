# Minors' Consent Gate — Audit & Remediation Plan (2026-06-03)

Verification of the GDPR consent/privacy gate added in commit `309f3f0`. **Status: not bulletproof — two blockers + several gaps.** The fixes touch the live auth/registration path and involve legal + product decisions, so they are documented here for review rather than auto-applied. Nothing in this file has been changed in code yet.

## How it works today

- **Consent UI:** a checkbox on email/password registration **step 3** (`components/LoginPage.tsx:830-854`), enforced by a disabled button (`:856`) and a submit re-check (`:420-424`). On accept it writes `users/{uid}.consent = { policyVersion, acceptedAt, basis }` (`:431-443`).
- **Legal text:** `components/legal/LegalModal.tsx` — a real, substantive Privacy Notice (11 sections) + Terms (8). Reachable during registration and via Settings → Legal. **Marked DRAFT** ("under review by our legal advisers"), and internally hedges legal basis, retention, and rights handling.
- **App-entry gate:** the only gate is `if (!user) return <LoginPage/>` (`components/AppRouter.tsx:264`). Nothing reads `consent` after the account exists — `contexts/AuthContext.tsx` never checks it.

## Blockers

1. **Google sign-in bypasses consent entirely (live on web).** `handleGoogleSignIn` (`LoginPage.tsx:300-335`) is rendered on both login and register views and, on first sign-in, creates `users/{uid}` with `{ name, avatar, school: '' }` — **no consent field, no notice shown**. A minor can create an account end-to-end with zero consent recorded. (`SHOW_GOOGLE_SIGN_IN` only hides it on native iOS/Android; it's active on the deployed web app.)

2. **Consent is a registration-click gate, not an app-entry gate.** Because nothing re-checks `consent` after creation, three populations skip it: Google sign-ups (blocker 1), users who registered **before** the gate existed, and any returning/refreshed session. The single highest-leverage fix is to read `users/{uid}.consent` at app entry and show an acceptance interstitial when it's missing or the `policyVersion` is stale — this covers all three at once.

## Gaps

3. **Under-16 (Irish digital age of consent = 16) is not handled at all.** No DOB/age is collected anywhere (`LegalModal.tsx:67` even states this). The model leans entirely on Art 8 parental consent "captured at school enrolment" as an **offline** control that is asserted in the notice but not evidenced anywhere in code. → **Product/legal decision required:** either capture a DOB/age-band and branch consent, or formally document + evidence the school-enrolment parental-consent mechanism.

4. **Firestore rules don't require consent.** `firestore.rules:27` (`allow create`) checks `name`/`avatar`/`school` only. A user doc can be created with no consent. (Note: adding this rule **without first** routing Google through consent would break Google sign-up — sequence matters.)

5. **Legal docs are DRAFT.** The persistent "Draft — under review by our legal advisers" banner + hedged legal-basis/retention/rights wording means the gate currently rests on non-final text. → **Needs counsel sign-off before relying on it.**

6. **No re-consent on `policyVersion` bump** (the version field is written but never read), **client-clock `acceptedAt`** (not `serverTimestamp()` — weak as evidence), **no consent-withdrawal flow** distinct from account deletion, and the policies are **modal-only** (no `/privacy` `/terms` URL, unreachable to logged-out visitors).

## Recommended sequence (each step is safe only in this order)

1. **Build the app-entry consent interstitial** (`AuthContext`/`AppRouter`): when `users/{uid}.consent` is missing or stale, block the app and show the LegalModal acceptance step, writing consent on accept. **Fail-open on load error** (never lock a user out due to a transient read failure). This single change neutralises blockers 1 & 2 and gap 6's re-consent. ⚠️ Touches the auth path for *all* users — smoke-test sign-in (new email, new Google, returning session, legacy account) before trusting it.
2. **Use `serverTimestamp()` for `acceptedAt`.**
3. **Add the Firestore rule** requiring a well-formed `consent` map on `allow create` — only after step 1 guarantees every create path provides it.
4. **Make a decision on under-16 / DOB** (product + legal).
5. **Get counsel sign-off and drop the DRAFT banner** — or treat the gate as not-ship-ready.
6. Add stable `/privacy` + `/terms` reachability and a true consent-withdrawal flow.

## Why this wasn't auto-applied
Step 1 changes the login path of a product used by minors, where a subtle bug = mass lockout, and it can't be end-to-end verified without the Firebase Auth emulator (the unit smokes mock Firebase). Steps 4–5 are legal/product calls. These need a human in the loop — hence this plan rather than a blind deploy.

_Relevant files: `components/legal/LegalModal.tsx`, `components/LoginPage.tsx`, `components/AppRouter.tsx`, `contexts/AuthContext.tsx`, `firestore.rules`, `compliance/ALEX_TO_CONFIRM.md`._
