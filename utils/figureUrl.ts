/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Where an exam figure is loaded from.
 *
 * `public/exam-figures/` is 539 MB across 3,114 PNGs, and Capacitor copies the
 * whole of `dist/` into each native shell — which produced a 569 MB Android
 * bundle (rejected outright by Play) and a ~600 MB iOS app that passed review
 * only because Apple's ceiling is 4 GB. Most of it is dead weight for any given
 * student: Geography alone is 154 MB that a Biology candidate never opens.
 *
 * So the native builds do NOT ship them. `scripts/prune-native-assets.mjs`
 * strips the directory after `cap sync`, and this resolves the same paths
 * against Firebase Hosting instead, which already serves them for the web app.
 * Nothing is lost by it: the app needs the network for Firebase auth and
 * Firestore before a student can see a figure at all.
 *
 * On web this is the identity function — the files are served from the same
 * origin as the page, exactly as before.
 */

import { Capacitor } from '@capacitor/core';

/** The origin the web app is served from, and where the figures live. */
const HOSTED_ORIGIN = 'https://nextstepuni-app.web.app';

/** Only this prefix is pruned from the native bundle, so only it is rewritten.
 *  Everything else in dist/ still ships locally and must keep resolving locally. */
const PRUNED_PREFIX = '/exam-figures/';

/**
 * Resolve a figure's `src` for the platform it is about to render on.
 *
 * Pass any figure src through this at the point of render. Data files keep
 * root-relative paths — they are shared with the web build and with the
 * generated Mark Bank decks, whose provenance tests assert those exact strings.
 */
export function figureUrl(src: string): string {
  if (!src.startsWith(PRUNED_PREFIX)) return src;
  return Capacitor.isNativePlatform() ? `${HOSTED_ORIGIN}${src}` : src;
}
