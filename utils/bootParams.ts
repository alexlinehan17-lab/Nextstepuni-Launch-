/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Boot-time URL parameter snapshot.
 *
 * NavigationContext serialises its own whitelist (view/cat/mod/tool/from) back
 * into the URL on the app's first commit, stripping anything else — so any
 * extra deep-link parameters (e.g. Paper Trail's ?subject=&year=) must be
 * captured before that happens. This module is imported for its side effect
 * from App.tsx (eager chunk), guaranteeing the snapshot is taken at module-
 * evaluation time, long before any lazy tool chunk loads.
 */

const snapshot: ReadonlyMap<string, string> = (() => {
  const m = new Map<string, string>();
  if (typeof window !== 'undefined') {
    new URLSearchParams(window.location.search).forEach((v, k) => m.set(k, v));
  }
  return m;
})();

/** Read a parameter as it stood at boot (before any URL rewriting). */
export const getBootParam = (name: string): string | null => snapshot.get(name) ?? null;
