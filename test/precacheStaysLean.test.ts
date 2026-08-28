/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The service worker precache is a latency budget, not a cache setting.
 *
 * Every deploy rewrites every asset hash, so the ENTIRE precache is
 * re-downloaded by every returning browser, in the background, exactly while a
 * student is trying to log in or sign up — competing with the auth and callable
 * requests they are actually waiting on. Measured against the live site on
 * 2026-08-28: 4.4MB compressed, ~4s to pull on a fast connection with six
 * parallel connections. Half of it was exam corpus and lazy-tool data that
 * nobody on the login screen has any use for.
 *
 * So anything behind a lazy route belongs in globIgnores. It is not lost — the
 * runtime `app-chunks` NetworkFirst rule caches each chunk the moment the
 * student opens the tool. The only thing given up is having it cached offline
 * BEFORE first use, which is a fine trade against a slow session after every
 * single deploy.
 *
 * This test exists because that reasoning is invisible at the call site: a
 * globIgnores list looks like clutter, and "tidying" it would quietly put ~14MB
 * back into every deploy.
 */
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';

function globIgnores(): string[] {
  const config = readFileSync('vite.config.ts', 'utf8');
  const block = config.match(/globIgnores:\s*\[([\s\S]*?)\]/);
  expect(block, 'globIgnores block not found in vite.config.ts').toBeTruthy();
  return [...block![1].matchAll(/'([^']+)'/g)].map(m => m[1]);
}

describe('service worker precache stays lean', () => {
  it('keeps every lazy-route payload out of the precache', () => {
    const ignored = globIgnores();
    // Grouped by why each is lazy, so a future reader can tell whether a new
    // chunk belongs on this list.
    const mustBeIgnored = [
      '**/pdf.worker*.js', '**/vendor-pdfjs*.js',   // Paper Trail viewer
      '**/DiagramVault*.js',                        // Diagram Vault
      '**/higher-*.js', '**/ordinary-*.js',         // per-subject exam corpora
      '**/catchUpLaneData*.js',                     // Catch-Up Lane
      '**/commandWordData*.js',                     // Command Word Reflex
      '**/vendor-three*.js',                        // 3D module scenes
      '**/vendor-jspdf*.js', '**/html2canvas*.js',  // PDF export
    ];
    expect(ignored).toEqual(expect.arrayContaining(mustBeIgnored));
  });

  it('does not ignore the app shell, which must stay precached', () => {
    const ignored = globIgnores();
    // A pattern broad enough to swallow index-*.js or the CSS would take the
    // shell offline, which is the one thing the precache is genuinely for.
    for (const pattern of ignored) {
      expect(pattern).not.toMatch(/^\*\*\/\*\.(js|css)$/);
      expect(pattern).not.toMatch(/^\*\*\/index-/);
    }
    expect(ignored.some(p => p.includes('index.html'))).toBe(false);
  });
});
