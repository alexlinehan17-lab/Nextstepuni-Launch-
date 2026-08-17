/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A teacher is signed in before they are known to be staff. This marks that
 * window so the app does not mistake them for a student.
 *
 * ─── THE RACE (2026-08-17) ─────────────────────────────────────────────────
 *
 * handleStaffAccess must create/sign in an Auth account BEFORE it can call
 * claimStaffAccess — a callable needs an authenticated caller. But creating
 * the account fires onAuthStateChanged straight away, and at that instant:
 *
 *   • users/{uid} does not exist yet (it is written a few lines later), so
 *     AuthContext takes its no-user-doc fallback: no role, no school
 *   • that fallback sets needsOnboarding = true
 *   • AppRouter unmounts LoginPage and renders student Onboarding
 *
 * Meanwhile the flow still has to wait on the user-doc write (up to 8s) and a
 * claimStaffAccess call that can cold-start, before it reloads into the Staff
 * Dashboard. So the teacher watched 5–15 seconds of STUDENT onboarding — and
 * if they tapped through it they wrote a subjectProfile onto their own
 * progress doc, or got stranded there entirely if the reload never landed.
 *
 * The role check in AppRouter is correct and already sits ahead of the
 * onboarding gate; the gap is purely that role is not known yet. So: hold the
 * app on its loading state until provisioning resolves.
 *
 * sessionStorage, not React state, because the flow deliberately ends in
 * window.location.reload() — the marker has to survive that and be readable by
 * AppRouter, which is a different component tree from LoginPage.
 */

const KEY = 'nsu:staff-provisioning';

/**
 * How long the marker is honoured. Long enough for a cold-start callable plus
 * the 8s user-doc wait; short enough that a crashed or abandoned attempt can
 * never permanently lock a genuine student out of onboarding. Expiry is the
 * safety net — the flow clears the marker itself on both success and failure.
 */
const MAX_AGE_MS = 90_000;

/** Mark that a staff claim is in flight for this tab. */
export function beginStaffProvisioning(now: number = Date.now()): void {
  try {
    window.sessionStorage.setItem(KEY, String(now));
  } catch {
    /* storage unavailable — worst case the teacher sees the old flash */
  }
}

/** Clear the marker: the claim finished, or it failed and we are back on the form. */
export function endStaffProvisioning(): void {
  try {
    window.sessionStorage.removeItem(KEY);
  } catch {
    /* nothing to do */
  }
}

/**
 * True while a staff claim is still in flight. Self-expiring, so a marker left
 * behind by a crash cannot trap a later student in a spinner.
 */
export function isStaffProvisioning(now: number = Date.now()): boolean {
  try {
    const started = window.sessionStorage.getItem(KEY);
    if (!started) return false;
    const age = now - Number(started);
    if (!Number.isFinite(age) || age < 0 || age > MAX_AGE_MS) {
      endStaffProvisioning();
      return false;
    }
    return true;
  } catch {
    return false;
  }
}
