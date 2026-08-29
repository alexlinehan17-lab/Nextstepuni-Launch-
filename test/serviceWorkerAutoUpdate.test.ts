/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * NextStepUni registers its service worker manually so Capacitor never installs
 * it inside the native WebView. vite-plugin-pwa only injects `skipWaiting` and
 * `clientsClaim` for auto-update mode when it also owns registration, so our
 * manual path must set both explicitly. Otherwise a deployed worker waits behind
 * open tabs and refreshes continue to boot a stale app shell indefinitely.
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

const viteConfig = readFileSync('vite.config.ts', 'utf8');
const indexEntry = readFileSync('index.tsx', 'utf8');
const firebaseConfig = JSON.parse(readFileSync('firebase.json', 'utf8')) as {
  hosting: { headers: Array<{ source: string; headers: Array<{ key: string; value: string }> }> };
};

describe('service worker auto-update handoff', () => {
  it('keeps registration out of the native Capacitor shell', () => {
    expect(viteConfig).toContain("injectRegister: false");
    expect(indexEntry).toContain('if (!Capacitor.isNativePlatform())');
    expect(indexEntry).toContain("import('virtual:pwa-register')");
  });

  it('activates and claims the latest worker despite manual registration', () => {
    expect(viteConfig).toContain("registerType: 'autoUpdate'");
    expect(viteConfig).toMatch(/workbox:\s*\{[\s\S]*?skipWaiting:\s*true/);
    expect(viteConfig).toMatch(/workbox:\s*\{[\s\S]*?clientsClaim:\s*true/);
  });

  it('explicitly checks for a newer worker at launch and while the app stays open', () => {
    expect(indexEntry).toContain('onRegisteredSW:');
    expect(indexEntry).toContain('registration.update()');
    expect(indexEntry).toMatch(/window\.setInterval\(checkForUpdate,\s*60 \* 60 \* 1000\)/);
  });

  it('does not let the browser cache the worker update check', () => {
    const workerHeaders = firebaseConfig.hosting.headers.find(({ source }) => source === '/sw.js')?.headers ?? [];
    const cacheControl = workerHeaders.find(({ key }) => key.toLowerCase() === 'cache-control')?.value ?? '';

    expect(cacheControl).toMatch(/no-cache/);
    expect(cacheControl).toMatch(/must-revalidate/);
  });
});
