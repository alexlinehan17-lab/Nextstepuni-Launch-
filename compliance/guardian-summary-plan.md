<!--
 @license
 SPDX-License-Identifier: Apache-2.0
-->

# Weekly guardian summary (feature E10) — activation plan

An opt-in weekly email to a parent/guardian reporting **effort, not grades** —
minutes revised, questions practised, streak. Sparx reports ~95% parent
engagement via exactly this channel; it's low-bandwidth and a strong DEIS/PwC
signal. Built **ship-gated** — the consent UI and the send both stay off until a
Cloud Function and email provider are in place.

## What ships now (safe, gated)

- `data/guardianSummary.ts` — the pure `buildGuardianEmail` composer (effort
  only; **no grade/mark/percentage language**, guarded by
  `test/guardianSummary.test.ts`), the `GuardianConsent` shape, and consent
  accessors that read/write the student's **own settings doc** (self-write,
  already permitted — no rule change).
- `components/PaperTrail/GuardianConsent.tsx` — consent card (guardian email +
  opt-in + live preview of the exact email), rendered in the progress dashboard.
- Everything behind `GUARDIAN_EMAILS_LIVE = false`, so nothing appears until
  activation.

## The send (activation step — not built here)

A scheduled Cloud Function (add to `functions/src`, export from `index.ts`):

1. Runs weekly (Cloud Scheduler / `onSchedule`).
2. Queries `settings` for docs with `guardianSummary.optIn == true`.
3. For each, aggregates that student's week (focus minutes, cards reviewed,
   streak, focus topic) from `progress`/sessions — server-side, Admin SDK.
4. Calls the shared `buildGuardianEmail(summary)` (reuse this exact module).
5. Sends via a provider (SendGrid / Postmark / Firebase "Trigger Email"
   extension). Include a one-click unsubscribe.

## Consent & safeguarding (must clear before flip)

- The email address is a **third party's (a guardian's)**. Confirm the lawful
  basis with the school: consent should be captured/authorised at the school
  level for under-18s, not by the minor alone — the in-app opt-in is the
  student's request, gated behind school authorisation.
- Store only what's needed (address + opt-in). Provide unsubscribe + deletion.
- No grades, marks or rankings ever — enforced by the builder and its test.
- Log sends for audit; honour Irish DPC / GDPR for minors.

## Activation steps (in order)

1. Legal sign-off on guardian consent for minors (school-mediated).
2. Add + deploy the scheduled function and provider credentials (secrets).
3. Confirm the consent write path and function read path in the emulator.
4. Flip `GUARDIAN_EMAILS_LIVE = true`.
5. Pilot with a small opt-in cohort before school-wide rollout.
