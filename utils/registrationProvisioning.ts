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
 * (The staff twin of this file, utils/staffProvisioning.ts, was retired with
 * the per-teacher claim flow on 2026-09-04 — staff accounts are provisioned
 * server-side before first sign-in now, so no staff race exists.)
 * handleRegisterSubmit calls createUserWithEmailAndPassword,
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
 * student is at that moment using.
 *
 * ─── WHY THIS IS NOT JUST A BOOLEAN ────────────────────────────────────────
 *
 * A marker that is only read during render can strand a student on a spinner
 * forever, because clearing it is a plain sessionStorage write that schedules
 * no React update. Two defences, because the failure mode is a dead screen:
 *
 *   1. The marker is stamped with a per-page-load nonce. A reload (or a
 *      duplicated tab, which inherits sessionStorage) gets a new nonce, so a
 *      marker left behind by a JS context that no longer exists is recognised
 *      as dead and cleared on the next read. That context's registration
 *      cannot still be running, so there is nothing left to hold for.
 *   2. Every marker change notifies reactive readers. sessionStorage writes do
 *      not schedule a React render by themselves; without this, clearing the
 *      hold before the user-document write still left onboarding waiting for
 *      that write's server acknowledgement to cause some unrelated render.
 *   3. remainingMs() lets the reader schedule its own repaint, so the expiry
 *      below is a real deadline rather than one that is only noticed if
 *      something else happens to re-render.
 *
 * The caller must ALSO guarantee an auth-state change on every failure path —
 * see the signOut fallback in LoginPage's rollback. Between the three, there
 * is no route to a terminal spinner.
 */

const KEY = 'nsu:registration-provisioning';
const CHANGE_EVENT = 'nsu:registration-provisioning-change';

/**
 * Notify React readers after the current stack has settled.
 *
 * registrationHoldRemainingMs() can clear a stale marker while a component is
 * rendering. Dispatching synchronously there would make the listener set React
 * state during render, so use a microtask. On the normal signup path this still
 * releases the loading screen before the background Firestore write settles.
 */
function notifyRegistrationProvisioningChange(): void {
  if (typeof window === 'undefined') return;
  queueMicrotask(() => {
    if (typeof window !== 'undefined') window.dispatchEvent(new Event(CHANGE_EVENT));
  });
}

/** Subscribe to begin/end/expiry changes so storage-backed state is reactive. */
export function subscribeToRegistrationProvisioning(listener: () => void): () => void {
  if (typeof window === 'undefined') return () => {};
  const handleChange = () => listener();
  window.addEventListener(CHANGE_EVENT, handleChange);
  return () => window.removeEventListener(CHANGE_EVENT, handleChange);
}

/**
 * How long the marker is honoured. Long enough for a cold-start callable plus
 * the forced token refresh; short enough that an abandoned attempt cannot
 * permanently lock a genuine student out of onboarding.
 */
const MAX_AGE_MS = 90_000;

/**
 * Identifies this JS context. Survives re-renders, not reloads — which is
 * exactly the distinction we need: a marker carrying a different nonce was
 * written by a page that is gone, so its registration died with it.
 */
const CONTEXT_ID = `${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`;

/** Mark that a student registration is in flight for this tab. */
export function beginRegistrationProvisioning(now: number = Date.now()): void {
  try {
    window.sessionStorage.setItem(KEY, `${CONTEXT_ID}:${now}`);
  } catch {
    /* storage unavailable — worst case the student sees the old flash */
  }
  notifyRegistrationProvisioningChange();
}

/** Clear the marker: the registration finished, or failed and we are back on the form. */
export function endRegistrationProvisioning(): void {
  try {
    window.sessionStorage.removeItem(KEY);
  } catch {
    /* nothing to do */
  }
  notifyRegistrationProvisioningChange();
}

/**
 * Milliseconds this hold has left, or 0 if it is not held. Callers that render
 * from it should schedule a repaint for this long, so expiry is observed even
 * when nothing else re-renders.
 */
export function registrationHoldRemainingMs(now: number = Date.now()): number {
  try {
    const raw = window.sessionStorage.getItem(KEY);
    if (!raw) return 0;
    const sep = raw.lastIndexOf(':');
    const contextId = sep === -1 ? '' : raw.slice(0, sep);
    const started = Number(sep === -1 ? raw : raw.slice(sep + 1));

    // Written by a page that no longer exists: its registration cannot still
    // be running, so holding for it could only ever hang this one.
    if (contextId !== CONTEXT_ID) { endRegistrationProvisioning(); return 0; }

    const age = now - started;
    if (!Number.isFinite(age) || age < 0 || age > MAX_AGE_MS) {
      endRegistrationProvisioning();
      return 0;
    }
    return MAX_AGE_MS - age;
  } catch {
    return 0;
  }
}

/**
 * True while a student registration is still in flight in THIS page context.
 * Self-expiring, and self-invalidating across reloads.
 */
export function isRegistrationProvisioning(now: number = Date.now()): boolean {
  return registrationHoldRemainingMs(now) > 0;
}

// ─── Carrying the failure reason across the remount ─────────────────────────

const ERROR_KEY = 'nsu:registration-error';

/**
 * Why a registration failed, as a code rather than a message.
 *
 * A code, deliberately: the copy is resolved at the point of render instead of
 * being persisted. Storing the rendered text meant putting a string built from
 * MIN_PASSWORD_LENGTH into sessionStorage, which is both a CodeQL
 * clear-text-storage finding and the wrong shape — UI copy should not be
 * durable state, and a message stashed by one build should not be replayed by
 * the next.
 */
export type RegistrationErrorCode =
  | 'weak-password'
  | 'email-in-use'
  | 'invalid-email'
  | 'bad-join-code'
  | 'school-unconfigured'
  | 'too-many-attempts'
  | 'generic';

const CODES: readonly RegistrationErrorCode[] = [
  'weak-password', 'email-in-use', 'invalid-email',
  'bad-join-code', 'school-unconfigured', 'too-many-attempts', 'generic',
];

/**
 * When a registration fails after the account was created, the rollback signs
 * the student out — which can unmount LoginPage before its setError paints.
 * The replacement instance would render a blank form, so the student sees only
 * an unexplained bounce back to the login screen. Stash the reason here and let
 * the next instance say it.
 */
export function stashRegistrationError(code: RegistrationErrorCode): void {
  try {
    window.sessionStorage.setItem(ERROR_KEY, code);
  } catch {
    /* storage unavailable — the student sees the bounce without the reason */
  }
}

/** Read and clear a stashed reason. Read-once, so it cannot haunt a later visit. */
export function takeRegistrationError(): RegistrationErrorCode | null {
  try {
    const raw = window.sessionStorage.getItem(ERROR_KEY);
    if (!raw) return null;
    window.sessionStorage.removeItem(ERROR_KEY);
    // Anything unrecognised came from another build or was hand-edited; ignore
    // it rather than rendering it, so this can never become an injection point.
    return (CODES as readonly string[]).includes(raw) ? (raw as RegistrationErrorCode) : null;
  } catch {
    return null;
  }
}
