/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Every third-party host the service worker caches must also be allowed by
 * connect-src.
 *
 * This is not obvious and it cost us a live bug. img-src listed
 * api.dicebear.com, so a plain <img> would have been fine — but the SW has a
 * CacheFirst rule for that host, so the request is served by the worker, and
 * the worker fetches it with fetch(). fetch() is governed by connect-src, not
 * img-src. connect-src did not list the host, so every avatar request was
 * blocked, CacheFirst had nothing cached to fall back on, and every avatar in
 * the app rendered broken — while loading perfectly on direct navigation,
 * which is what made it so confusing to diagnose.
 *
 * The rule this locks: if you add a runtimeCaching entry for a new host, add
 * it to connect-src too.
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

function connectSrcHosts(): string[] {
  const firebaseJson = JSON.parse(readFileSync('firebase.json', 'utf8'));
  const headers = firebaseJson.hosting.headers.flatMap((h: { headers: { key: string; value: string }[] }) => h.headers);
  const csp = headers.find((h: { key: string }) => h.key === 'Content-Security-Policy')?.value ?? '';
  const directive = csp.split(';').map((d: string) => d.trim()).find((d: string) => d.startsWith('connect-src'));
  return (directive ?? '').split(/\s+/).slice(1);
}

/** Hosts the SW fetches, read off the runtimeCaching urlPatterns in vite.config.ts. */
function serviceWorkerHosts(): string[] {
  const vite = readFileSync('vite.config.ts', 'utf8');
  const patterns = vite.match(/urlPattern:\s*\/\^https:\\\/\\\/[^/]+\//g) ?? [];
  return patterns
    .map(p => p.replace(/urlPattern:\s*\/\^https:\\\/\\\//, '').replace(/\/$/, ''))
    .map(host => host.replace(/\\\./g, '.').replace(/\\\//g, '/'))
    .map(host => host.split('\\')[0])
    .filter(Boolean);
}

function allowedByConnectSrc(host: string, allowed: string[]): boolean {
  return allowed.some(entry => {
    const value = entry.replace(/^https:\/\//, '');
    if (value === host) return true;
    if (value.startsWith('*.')) return host.endsWith(value.slice(1));
    return false;
  });
}

describe('CSP covers every host the service worker fetches', () => {
  it('finds both lists, so the assertion below cannot pass vacuously', () => {
    expect(connectSrcHosts().length).toBeGreaterThan(3);
    expect(serviceWorkerHosts().length).toBeGreaterThan(2);
  });

  it('allows each cached third-party host in connect-src', () => {
    const allowed = connectSrcHosts();
    const missing = serviceWorkerHosts().filter(host => !allowedByConnectSrc(host, allowed));
    expect(missing).toEqual([]);
  });

  it('still allows the avatar host specifically', () => {
    // Named explicitly because this is the one that broke, and a future CSP
    // tidy-up that drops it would silently break every avatar again.
    expect(allowedByConnectSrc('api.dicebear.com', connectSrcHosts())).toBe(true);
  });

  it('does not route avatars through the service worker', () => {
    // The outage: a CacheFirst rule for api.dicebear.com meant the request was
    // served by fetch() inside the worker instead of as a plain <img> load, and
    // CacheFirst throws when it has no cached entry and the fetch does not
    // resolve — so every avatar in the app failed. Verified in-browser: worker
    // in control, all eight fail; worker not in control, all eight load.
    //
    // Re-adding a rule for this host would reintroduce that, so keep avatars as
    // ordinary image loads. img-src allows the host; the browser's HTTP cache
    // covers repeat views; offline falls back to initials in Avatar.tsx.
    expect(serviceWorkerHosts()).not.toContain('api.dicebear.com');
  });
});
