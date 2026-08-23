# Security rollout runbook

Status: the hardened backend, Firestore and Storage rules, Functions, Hosting
release, administrator claim, Authentication password policy, retention
policies, browser-key restrictions and web App Check registration were rolled
out to `nextstepuni-app` on 2026-08-23. App Check enforcement and retirement of
the legacy CI key remain deliberately staged as described below.

The deployed release now fails closed around revoked sessions, server-owned
roles, peer actions, account deletion and privileged administration.

## Production rollout record — 2026-08-23

Completed:

- exported all 978 Firestore documents (1.69 MB) to
  `gs://nextstepuni-app.firebasestorage.app/2026-08-23T14:04:23_85324` before
  changing the backend;
- issued the `admin: true` custom claim to the exact verified owner account,
  wrote its active server-side administrator profile and revoked its existing
  refresh tokens;
- deployed Firestore rules and indexes, Storage rules, 25 Cloud Functions and
  the matching Hosting build, in that order;
- set Firebase Authentication to require 12–128 character passwords while
  retaining email-enumeration protection; the platform owner's Google account
  already has two-step verification with passkeys;
- enabled TTL on `expiresAt` for `anonymousFeedback`, `feedbackRateLimits`,
  `peerInteractionRateLimits`, `staffMessageRateLimits` and
  `aggregateRateLimits`; all five policies report `Serving`;
- restricted the production Firebase browser key to the eight existing web
  referrers and the six APIs the client uses: App Check, Firebase
  Installations, Cloud Firestore, Cloud Storage, Identity Toolkit and Secure
  Token;
- created and registered a score-based reCAPTCHA Enterprise web key for the
  three production domains, configured a one-hour App Check token lifetime,
  and shipped the site-key identifier in the verified production bundle;
- created the keyless `github-deployer@nextstepuni-app.iam.gserviceaccount.com`
  deployment identity and a Workload Identity Federation provider restricted
  to this repository's immutable owner/repository IDs and `refs/heads/main`;
- added the Workload Identity provider, deploy-service-account and App Check
  site-key values to GitHub Actions secrets, and independently verified all 25
  Firebase deployment permissions plus both runtime-service-account
  impersonation boundaries using short-lived credentials; and
- completed two clean local release gates: lint, application and test
  type-checks, 2,665 tests, production build, Functions build, 18 Firestore
  rules-emulator tests and both dependency audits with zero vulnerabilities.

Production acceptance evidence:

- `/`, `/privacy`, `/terms` and `/delete-account` all return HTTP 200;
- CSP, HSTS, frame, MIME-sniffing, referrer and permissions-policy headers are
  present on the production response;
- the live module bundle contains the registered App Check site-key identifier;
  and
- Firebase reports all 25 expected Functions deployed.

Still staged intentionally:

- App Check enforcement remains off for Functions, Firestore and Storage until
  iOS and Android providers are registered, released and verified in App Check
  metrics. Enforcing it now would lock out the current native clients.
- The legacy `FIREBASE_SERVICE_ACCOUNT` GitHub secret and matching Google Cloud
  key must remain active until the Workload Identity workflow in this checkout
  is committed to `main` and completes one real federated deployment. Deleting
  it before that proof would break the workflow that currently exists on
  `main`.
- The historical App Review password must be changed by the account owner in a
  password manager and the private store-review consoles; no replacement
  credential may be generated or recorded in this repository.
- The historical Gemini credential identified by the audit is not a credential
  of the current Firebase project. Its owning provider/project must be
  identified from the organisation's secret inventory before it can be
  revoked safely.

## 1. Deploy identity and authorization changes safely

1. Take a Firestore export and record the currently deployed Functions and
   rules release.
2. Create a least-privilege Google Cloud deploy service account and Workload
   Identity Federation provider for this repository.
3. Add `GCP_WORKLOAD_IDENTITY_PROVIDER` and
   `GCP_DEPLOY_SERVICE_ACCOUNT` to the GitHub Actions environment. Do not add a
   service-account JSON key.
4. Complete the administrator bootstrap in section 2 before merging; the new
   rules intentionally reject an email-only administrator and require its
   active server-side profile.
5. Run the pull-request workflow. Confirm web tests, Functions compilation,
   rules-emulator tests, dependency audits and CodeQL are green.
6. Merge only after the backend deployment succeeds. The workflow deploys
   Firestore, Storage and Functions before Hosting so a newer client cannot
   reach an older trust boundary.
7. Treat the access-code cutover as a short maintenance window. Every guidance
   counsellor must open **School access**, generate a student join code, and
   distribute it through the school's approved channel. Predictable legacy
   codes and plaintext staff codes are deliberately no longer accepted.
8. After a successful federated deployment, revoke and delete any old deploy
   service-account JSON key and remove its GitHub secret.

## 2. Bootstrap the administrator claim

The exact verified account `nextstepuniinfo@gmail.com` also needs a
server-issued `admin: true` custom claim. Email alone is deliberately
insufficient.

Before merging the new rules, run this from a trusted administrator
workstation using Application Default Credentials:

```sh
cd functions
npm run provision:admin -- <confirmed-firebase-auth-uid>
```

The script refuses a UID mismatch or unverified mailbox, never accepts a
password or service-account file, and revokes existing refresh tokens after
setting the claim. Sign out and back in, then verify that an email-only test
account cannot open admin data.

## 3. Align Firebase Authentication policy

In Firebase Authentication settings:

- require passwords between 12 and 128 characters, matching both client and
  callable validation;
- enable email-enumeration protection;
- enable MFA for the platform owner's Google account and require phishing-
  resistant MFA for every person with Firebase/Google Cloud console access;
- retire shared `gc-*` credentials in favour of named counsellor accounts.
  The new one-person staff invitations, roster and revocation controls are a
  migration path, not a justification for retaining shared privileged logins.

Re-test email reset, counsellor temporary reset, forced password change,
revocation, demotion and disabled-account flows after enabling the policy.

## 4. Stage and enforce Firebase App Check

Do this in stages so released native clients are not locked out.

1. Register the web application with reCAPTCHA Enterprise and provide the
   resulting site key as `VITE_FIREBASE_APPCHECK_SITE_KEY` to the verified web
   build. The key is an identifier, not a secret.
2. Integrate and release App Attest/DeviceCheck for iOS and Play Integrity for
   Android. Register debug providers only for controlled development devices;
   never ship a debug token.
3. Observe App Check metrics for web, iOS and Android and confirm legitimate
   traffic is verified.
4. Set the typed Functions parameter `ENFORCE_APP_CHECK` to `true` through the
   Firebase Functions parameter/deployment flow and redeploy Functions.
5. Enable App Check enforcement for Firestore and Storage in the Firebase
   console only after all supported clients have passed the observation
   period.

Until step 4, callables still enforce authentication, live server-side role
documents, quotas and input allowlists; App Check is an additional client-
attestation layer, not an authorization replacement.

## 5. Restrict and rotate credentials

- The Firebase web API key is necessarily public. Restrict it in Google Cloud
  to the exact production and preview origins and only the Firebase APIs the
  application uses. Use package/bundle restrictions for native keys and test
  sign-in, callable, Firestore and Storage flows before removing old rules.
- Revoke the historical Gemini key referenced in the repository's governance
  history, even though it is no longer in the current bundle. Search provider
  usage logs for unexpected calls before deletion and issue a new key only if a
  reviewed server-side feature actually needs one.
- Review GitHub Actions, Firebase and Google Cloud secrets for unused keys and
  remove them after the federated workflow is proven.
- Immediately rotate the App Review account password that appeared in the
  previous tracked play-listing/seed script. Keep the replacement only in the
  release password manager and the private App Store/Play review consoles;
  repository history cannot be made safe by deleting the current file alone.

## 6. Enable automatic retention

Configure Firestore TTL on the `expiresAt` field for:

- `feedbackRateLimits`;
- `peerInteractionRateLimits`;
- `staffMessageRateLimits`;
- `aggregateRateLimits`;
- `anonymousFeedback` (currently a 365-day product-feedback retention period).

TTL is asynchronous and is not a quota control; the callables enforce quotas
transactionally. Record the policy IDs and activation date in the retention
policy, then confirm expired test documents are eventually removed.

## 7. Production acceptance checks

- A demoted or disabled staff account loses dashboard access with an already
  issued token.
- A counsellor cannot reset an account outside their school or any staff/admin
  account.
- A temporary password expires after 24 hours, cannot be reused as the chosen
  password and ends all old sessions.
- Staff invitation codes are single-use; student join codes rotate without
  exposing stored plaintext secrets.
- Kudos, gifts, class counters and staff messages reject direct Firestore
  writes and accept only server-composed choices within their quotas.
- Account deletion remains visibly pending/failed until the full data and Auth
  cascade succeeds; a failed cascade is retried and auditable.
- Browser sign-out clears application storage, a new browser session requires
  sign-in, Android backup cannot restore app data, and CSP violations are not
  present on the main student journeys.
- Dependency audits report zero high/critical production vulnerabilities and
  CodeQL has no unresolved high-severity alert.

Record evidence for every check. If any check fails, roll back the matching
release rather than weakening the rule or bypassing the callable.
