/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * A student is signed in before their registration has finished provisioning.
 * This marks that window so the app does not route them into onboarding while
 * the account can still be rolled back underneath them.
 *
 * ─── THE RACE (2026-08-27) ─────────────────────────────────────────────────
 *
 * This is the student twin of utils/staffProvisioning.ts, and it is the same
 * shape of bug. handleRegisterSubmit calls createUserWithEmailAndPassword,
 * which signs the student in immediately. At that instant:
 *
 *   • users/{uid} does not exist yet, so AuthContext takes its no-user-doc
 *     fallback and sets needsOnboarding = true
 *   • AppRouter unmounts LoginPage and renders Onboarding, ~1-1.5s in
 *
 * But the registration flow is still running. It has yet to await
 * updateProfile, the claimStudentSchool callable (which can cold-start, and
 * which rejects on a wrong or unprovisioned join code) and a forced ID-token
 * refresh. `userDocStarted` stays false across all of it, so a rejection in
 * that window reaches the rollback and calls deleteUser() on an account the
 * student is at that moment using — deleting a live session mid-onboarding
 * and dropping them onto a fresh LoginPage with no error message, because the
 * LoginPage instance holding that message has just been unmounted.
 *
 * The 2026-08-21 fix closed only the half of this race that happens from the
 * users/{uid} write onward. This closes the half before it, the same way the
 * staff flow was fixed: hold the router on its loading state until the
 * registration resolves, so the student is never shown onboarding they could
 * be evicted from.
 *
 * sessionStorage rather than React state, for the same reason as the staff
 * marker: it must be readable by AppRouter, which is a different component
 * tree from LoginPage, and must survive a reload.
 */

const KEY = 'nsu:registration-provisioning';

/**
 * How long the marker is honoured. Long enough for a cold-start callable plus
 * the forced token refresh; short enough that an abandoned or crashed attempt
 * can never permanently lock a genuine student out of onboarding. Expiry is
 * the safety net — the flow clears the marker itself on every exit.
 */
const MAX_AGE_MS = 90_000;

/** Mark that a student registration is in flight for this tab. */
export function beginRegistrationProvisioning(now: number = Date.now()): void {
  try {
    window.sessionStorage.setItem(KEY, String(now));
  } catch {
    /* storage unavailable — worst case the student sees the old flash */
  }
}

/** Clear the marker: the registration finished, or failed and we are back on the form. */
export function endRegistrationProvisioning(): void {
  try {
    window.sessionStorage.removeItem(KEY);
  } catch {
    /* nothing to do */
  }
}

/**
 * True while a student registration is still in flight. Self-expiring, so a
 * marker left behind by a crash cannot trap a later student in a spinner.
 */
export function isRegistrationProvisioning(now: number = Date.now()): boolean {
  try {
    const started = window.sessionStorage.getItem(KEY);
    if (!started) return false;
    const age = now - Number(started);
    if (!Number.isFinite(age) || age < 0 || age > MAX_AGE_MS) {
      endRegistrationProvisioning();
      return false;
    }
    return true;
  } catch {
    return false;
  }
}
