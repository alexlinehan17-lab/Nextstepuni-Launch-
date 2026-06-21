# App Store Submission Plan — NextStepUni (iOS)

_Status as of 2026-06-21. Owner key: **[You]** = manual / account-bound steps only you can do; **[Me]** = build/asset work I can do in the repo; **[Blocked]** = needs the Apple Developer account to exist first._

App identity (locked in):
- **Display name:** NextStepUni
- **Bundle ID:** `com.nextstepuni.app`
- **Category:** Education
- **Devices:** iPhone only (TARGETED_DEVICE_FAMILY = 1)
- **Min iOS:** 15.6

---

## Workstream A — Apple Developer Program (Organization) · [You] · START NOW
The long pole. Everything in C/D and the final signing step are blocked on this.

1. [ ] Create/confirm an Apple ID for `nextstepuniinfo@gmail.com` → https://account.apple.com
2. [ ] Enroll the company → https://developer.apple.com/enroll/
   - Entity type: **Company / Organization**
   - Have ready: registered **legal entity name** (exact), **D-U-N-S number** (you have it), company address + phone, website URL
   - Confirm you have legal authority to bind the company
   - Pay **$99/year**
3. [ ] Pass Apple's verification (often a phone/email check) — typically a few days
4. [ ] Note the **Team ID** Apple assigns (replaces the leftover `YHL8M48TL7`)

## Workstream B — iOS build readiness · [Me] (mostly account-independent)
1. [x] Align bundle ID + display name to production identity; iPhone-only; unsigned build passes (`BUILD SUCCEEDED`)
2. [x] App icon validated (1024×1024, no alpha)
3. [x] Remove `DEV: Skip Login` from native/production builds (dev server only) — typecheck clean
4. [x] **Sign in with Apple** — built & build-verified; final config [Blocked on account].
   - [x] **Custom native plugin** `ios/App/App/SignInWithApplePlugin.swift` using Apple's system `AuthenticationServices` only — **no third-party SDK bundled** (verified: built app links only Capacitor + Cordova frameworks). JS bridge: `utils/signInWithApple.ts`.
     - _Why custom:_ the only Cap-8-compatible drop-in (`@capgo/capacitor-social-login`) bundles the **Facebook SDK** into the IPA and its provider-exclusion only patches Podfile/Gradle, not SPM (we use SPM) — unacceptable for a minors' app promising "no tracking SDKs". The older `@capacitor-community/apple-sign-in` has a hard Cap-8 SPM conflict.
   - [x] "Sign in with Apple" entitlement (`ios/App/App/App.entitlements`) wired into both build configs
   - [x] Apple button (HIG black) + handler in `LoginPage.tsx`, shown on native only; nonce→SHA-256→Firebase `OAuthProvider('apple.com')`; records `consent` on first sign-in like the email flow
   - [ ] **[Blocked]** Enable "Sign in with Apple" **capability on the App ID** in the developer portal (automatic once Xcode signs under the org with the entitlement present)
   - [ ] **[Blocked]** Enable the **Apple provider in Firebase Console** (needs a Services ID + key from the Apple Developer portal)
   - [ ] **[Blocked]** Runtime-test on a device (can't be verified until the two steps above are done)
   - Note: Google is hidden on native (`SHOW_GOOGLE_SIGN_IN = !isNativePlatform`), so the iOS app is email/password + Apple → Guideline 4.8 satisfied (Apple was not strictly required, but it's now in place).
5. [ ] [Blocked] Swap signing to the company Team ID; enable Automatic signing under the org

## Workstream C — App Store Connect listing · [Me] prepares, submit after A
1. [ ] Create the app record in App Store Connect (after account) [Blocked]
2. [ ] **Screenshots** — iPhone 6.9" (required) + 6.5". Capture via the dev-login harness (no real login needed)
3. [ ] **Metadata** — name, subtitle, promotional text, description, keywords, support URL, marketing URL
4. [ ] **App Privacy "nutrition label"** — declare collection per `compliance/DPIA.md`: name, email, user content (reflections/answers), identifiers, usage data. **No third-party tracking.** Data is linked to the user, not used for tracking.
5. [ ] **Age rating** questionnaire (education; expected 4+/12+)
6. [ ] **Privacy policy URL** (see D2) — required field

## Workstream D — Compliance / legal · [You] decide
1. [ ] Confirm the lawful-basis model still holds now that **NextStepUni Ltd** is the registered processor (privacy notice already names "NextStepUni Ltd"). Review `compliance/ALEX_TO_CONFIRM.md` open items.
2. [x] **Public Privacy Policy + Terms pages built** — `/privacy.html` + `/terms.html`, generated at build time from a single shared source (`components/legal/legalContent.ts`) by the `legal-static-pages` Vite plugin, so they can never drift from the in-app notice. Build-verified in `dist/`. **Canonical URL for App Store Connect: `https://<your-domain>/privacy.html`** (needs the deploy domain + a `firebase deploy`).
3. [ ] The in-app Privacy Notice + Terms are marked *"pending review by legal counsel."* Decide whether to get that sign-off before submitting (recommended for an app serving minors).

---

## Critical-path summary
1. **You:** start Apple enrollment today (A1–A2) — multi-day.
2. **Me, in parallel (no account needed):** build Sign in with Apple client code, build the public `/privacy` + `/terms` pages, capture screenshots, draft all listing metadata.
3. **After the account clears:** swap signing to the company team, finish Apple-provider config, create the App Store Connect record, archive + upload, submit for review.
