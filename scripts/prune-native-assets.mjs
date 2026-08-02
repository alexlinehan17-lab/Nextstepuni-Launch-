#!/usr/bin/env node
/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Strip the exam-figure corpus out of the native shells after `cap sync`.
 *
 * Capacitor copies the whole of `dist/` into each platform, and
 * `dist/exam-figures` is 539 MB across 3,114 PNGs. That produced a 569 MB
 * Android bundle — which Google Play rejects outright — and a ~600 MB iOS app
 * that only passed because Apple's ceiling is 4 GB. It is a punishing download
 * for a student on mobile data, and most of it is never opened: Geography alone
 * is 154 MB that a Biology candidate has no use for.
 *
 * The figures are already served from Firebase Hosting for the web app, and
 * `utils/figureUrl.ts` points the native builds at that same origin. Nothing is
 * lost by dropping them from the bundle — the app cannot show a figure before it
 * has reached Firebase for auth and Firestore anyway.
 *
 * Run this after EVERY `cap sync`, or the directory comes straight back. The
 * `cap:*` npm scripts do it for you.
 *
 *   node scripts/prune-native-assets.mjs
 */

import { rmSync, existsSync, statSync, readdirSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

/** Directories inside each native web root that must not ship. */
const PRUNE = ['exam-figures'];

/** Where each platform keeps its copy of dist/. Missing platforms are skipped. */
const WEB_ROOTS = [
  'ios/App/App/public',
  'android/app/src/main/assets/public',
];

const mb = (bytes) => (bytes / 1024 / 1024).toFixed(1);

/** Recursive size, because the point of this script is the number it reports. */
function dirSize(path) {
  let total = 0;
  for (const entry of readdirSync(path, { withFileTypes: true })) {
    const full = join(path, entry.name);
    total += entry.isDirectory() ? dirSize(full) : statSync(full).size;
  }
  return total;
}

let freed = 0;
let touched = 0;

for (const webRoot of WEB_ROOTS) {
  const rootAbs = resolve(ROOT, webRoot);
  if (!existsSync(rootAbs)) continue;
  touched += 1;
  for (const name of PRUNE) {
    const target = join(rootAbs, name);
    if (!existsSync(target)) {
      console.log(`  ${webRoot}/${name} — already absent`);
      continue;
    }
    const size = dirSize(target);
    rmSync(target, { recursive: true, force: true });
    freed += size;
    console.log(`  ${webRoot}/${name} — removed ${mb(size)} MB`);
  }
  console.log(`  ${webRoot} now ${mb(dirSize(rootAbs))} MB`);
}

if (touched === 0) {
  console.log('No native platforms found — nothing to prune.');
} else {
  console.log(`\nPruned ${mb(freed)} MB across ${touched} platform(s).`);
  console.log('Figures resolve to Firebase Hosting at runtime — see utils/figureUrl.ts');
}
