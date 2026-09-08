/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guest setup: the initial onboarding run WITHOUT an account.
 *
 * A visitor arrives from the landing page's "Set up without an account"
 * (`/?from=landing&setup=guest`), answers the same onboarding the app asks a
 * new student, and reaches "Dive in" — a placeholder page saying accounts and
 * payment open at launch. Nothing on this path may write to Firestore, call
 * Auth, or record a funnel event: there is no account to write against, and
 * an unauthenticated write is a rules rejection plus a console error.
 *
 * State lives in sessionStorage, so a reload keeps the draft and closing the
 * tab forgets it. Two kinds of key:
 *   - the PHASE marker, which is what makes the app route to the guest flow
 *     on a reload after NavigationContext has tidied `setup=guest` out of the
 *     URL. Ending guest setup removes it; the draft can outlive it.
 *   - the DRAFT / RESULT, the answers themselves. They are kept when the guest
 *     goes to create an account, so a later change can adopt them into the
 *     new account (adopting is NOT done here; the data is only kept).
 *
 * Why the boot snapshot: AuthContext calls clearLocalSessionData() on every
 * unauthenticated boot, which wipes sessionStorage before AppRouter renders —
 * exactly the reload this module exists to survive. This module is evaluated
 * (statically, via AppRouter) long before that async clear runs, so it copies
 * every guest key at load and hands them back on the first read after the
 * clear. Removals also remove from the snapshot, so nothing deliberately
 * ended is resurrected. The cleaner fix is an allow-list for these keys in
 * utils/sessionPrivacy.ts; until that lands, this is self-contained.
 */

import { getBootParam } from '../../utils/bootParams';

export const GUEST_USER_ID = 'guest';
/** The flow never asks for a name, so the greeting reads "Hi there". */
export const GUEST_USER_NAME = 'there';

/** The landing page reaches the guest flow with `?setup=guest`. */
export const GUEST_SETUP_PARAM = 'setup';
export const GUEST_SETUP_VALUE = 'guest';

/** Where the guest goes when they leave the flow. */
export const LANDING_PAGE_URL = '/landing-dev.html';
/** The existing sign-up path: the app's welcome/login page, "Create your account". */
export const CREATE_ACCOUNT_URL = '/?from=landing';

export type GuestPhase = 'onboarding' | 'dive-in';

const PREFIX = 'nsu:guest-setup:';
const PHASE_KEY = `${PREFIX}phase`;
const RESULT_KEY = `${PREFIX}result`;

const isGuestKey = (key: string | null): key is string => typeof key === 'string' && key.startsWith(PREFIX);

/** Everything under the guest prefix as it stood when this module loaded. */
const bootSnapshot: Map<string, string> = (() => {
  const m = new Map<string, string>();
  try {
    const store = window.sessionStorage;
    for (let i = 0; i < store.length; i += 1) {
      const key = store.key(i);
      if (isGuestKey(key)) {
        const value = store.getItem(key);
        if (value !== null) m.set(key, value);
      }
    }
  } catch { /* storage unavailable: the guest flow still runs, in memory */ }
  return m;
})();

/** In-memory mirror for the session where storage throws (Safari private mode). */
const memory = new Map<string, string>(bootSnapshot);

function rawGet(key: string): string | null {
  try {
    const live = window.sessionStorage.getItem(key);
    if (live !== null) return live;
  } catch { /* fall through to memory */ }
  return memory.get(key) ?? null;
}

function rawSet(key: string, value: string): void {
  memory.set(key, value);
  bootSnapshot.set(key, value);
  try { window.sessionStorage.setItem(key, value); } catch { /* memory keeps it */ }
}

function rawRemove(key: string): void {
  memory.delete(key);
  bootSnapshot.delete(key);
  try { window.sessionStorage.removeItem(key); } catch { /* nothing to remove */ }
}

/**
 * Put back whatever the unauthenticated-boot clear took. Call once the auth
 * listener has settled (AuthContext clears BEFORE it publishes userResolved).
 * Safe to call any number of times; a no-op with nothing to restore.
 */
export function restoreGuestSetupState(): void {
  for (const [key, value] of memory) {
    try {
      if (window.sessionStorage.getItem(key) === null) window.sessionStorage.setItem(key, value);
    } catch { /* memory still holds it */ }
  }
}

/**
 * A Storage-shaped view of the guest namespace, so the onboarding components
 * can swap it in for localStorage without learning anything about guests.
 * Keys are prefixed on the way in and never collide with an account's draft.
 */
export const guestStorage: Pick<Storage, 'getItem' | 'setItem' | 'removeItem'> = {
  getItem: (key: string) => rawGet(PREFIX + key),
  setItem: (key: string, value: string) => rawSet(PREFIX + key, value),
  removeItem: (key: string) => rawRemove(PREFIX + key),
};

// ─── Phase ────────────────────────────────────────────────────────────────

export function readGuestPhase(): GuestPhase | null {
  const value = rawGet(PHASE_KEY);
  return value === 'onboarding' || value === 'dive-in' ? value : null;
}

export function setGuestPhase(phase: GuestPhase): void {
  rawSet(PHASE_KEY, phase);
}

/** True while a guest setup is in progress in this tab (any phase). */
export function isGuestSetupActive(): boolean {
  return readGuestPhase() !== null;
}

/**
 * Should the app route a signed-out visitor to the guest flow? Either the
 * page was opened with `?setup=guest` (read at boot, before the URL is
 * rewritten) or a guest setup is already under way in this tab.
 */
export function isGuestSetupRequested(): boolean {
  return getBootParam(GUEST_SETUP_PARAM) === GUEST_SETUP_VALUE || isGuestSetupActive();
}

/**
 * Leave the guest flow. The phase marker always goes, so the next visit to
 * the app root is the ordinary login page. The answers go only when asked:
 * "Create your account" keeps them for a later adoption; "Skip for now"
 * throws them away.
 */
export function endGuestSetup(options: { keepDraft: boolean }): void {
  rawRemove(PHASE_KEY);
  if (options.keepDraft) return;
  for (const key of Array.from(memory.keys())) if (isGuestKey(key)) rawRemove(key);
  try {
    const store = window.sessionStorage;
    const doomed: string[] = [];
    for (let i = 0; i < store.length; i += 1) {
      const key = store.key(i);
      if (isGuestKey(key)) doomed.push(key);
    }
    doomed.forEach(key => store.removeItem(key));
  } catch { /* storage unavailable */ }
}

// ─── Result ───────────────────────────────────────────────────────────────

/** What the guest built. Kept verbatim so an account can adopt it later. */
export interface GuestSetupResult {
  version: 1;
  completedAt: string;
  profile: unknown;
  northStar: unknown;
  essentialsMode: boolean;
}

export function saveGuestSetupResult(result: Omit<GuestSetupResult, 'version' | 'completedAt'>): void {
  const record: GuestSetupResult = { version: 1, completedAt: new Date().toISOString(), ...result };
  try { rawSet(RESULT_KEY, JSON.stringify(record)); } catch { /* unserialisable: keep going */ }
}

export function readGuestSetupResult(): GuestSetupResult | null {
  const raw = rawGet(RESULT_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as Partial<GuestSetupResult>;
    return parsed.version === 1 && typeof parsed.completedAt === 'string' ? (parsed as GuestSetupResult) : null;
  } catch {
    return null;
  }
}
