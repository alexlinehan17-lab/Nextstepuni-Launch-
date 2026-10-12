/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Firebase Auth email action links.
 *
 * Firebase has ONE action URL per project, configured in the console
 * (Authentication → Templates), and every action email uses it: password
 * reset, email verification, email recovery and verify-and-change. Ours is
 * https://nextstepuni-app.web.app/reset-password, so a "Verify your email"
 * link lands on /reset-password too. Firebase appends
 * `?mode=<action>&oobCode=…&apiKey=…&lang=en`; `mode` says which action the
 * code belongs to. Dispatch on it — never assume a link here is a reset.
 */

export const AUTH_ACTION_MODES = [
  'resetPassword',
  'verifyEmail',
  'recoverEmail',
  'verifyAndChangeEmail',
  'revertSecondFactorAddition',
] as const;

export type AuthActionMode = (typeof AUTH_ACTION_MODES)[number];

export interface AuthActionLink {
  /** The raw `mode` parameter; may be missing or an unknown value. */
  mode: string | null;
  oobCode: string | null;
}

const KNOWN_MODES = new Set<string>(AUTH_ACTION_MODES);

export function isKnownAuthActionMode(mode: string | null): mode is AuthActionMode {
  return mode !== null && KNOWN_MODES.has(mode);
}

/**
 * The action link carried by this location, or null when the location is an
 * ordinary app URL. The configured path always counts (so a malformed link
 * still gets an explanation instead of the app); elsewhere a link needs both a
 * known mode and a code.
 */
export function readAuthActionLink(location: { pathname: string; search: string }): AuthActionLink | null {
  const params = new URLSearchParams(location.search);
  const mode = params.get('mode');
  const oobCode = params.get('oobCode');
  const onActionPath = location.pathname === '/reset-password'
    || location.pathname.startsWith('/reset-password/');
  if (onActionPath) return { mode, oobCode };
  if (isKnownAuthActionMode(mode) && oobCode) return { mode, oobCode };
  return null;
}

export function isAuthActionRequest(): boolean {
  if (typeof window === 'undefined') return false;
  return readAuthActionLink(window.location) !== null;
}
