/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Vitest config — separate from vite.config.ts so the PWA plugin doesn't run
 * under test. Reuses the React plugin + the "@" alias.
 */
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';

// Run every test in the timezone the product actually lives in.
//
// This app models Irish calendar days — an exam countdown, "today's" mock date,
// the Monday-to-Sunday study week. Tests that pin a wall-clock instant (e.g.
// setSystemTime('2026-06-03T00:30:00+01:00') and then assert the date input
// reads 2026-06-03) only mean what they say when the runner is on Irish time.
// GitHub Actions runners are UTC, so from 23:00 to midnight IST the "local day"
// diverged and those assertions failed in CI while passing on every Irish
// laptop — which is what blocked the deploy pipeline from 10 Aug 2026.
// Set as the config is evaluated, before any worker spawns, so they inherit it.
// Unconditional on purpose: these assertions are about Irish calendar days, so
// an inherited TZ from the environment must not silently change their meaning.
process.env.TZ = 'Europe/Dublin';

const root = fileURLToPath(new URL('.', import.meta.url));

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': root } },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./test/setup.ts'],
    include: ['test/**/*.{test,spec}.{ts,tsx}'],
    exclude: ['test/rules/**'],
    // A handful of corpus-backed smoke tests import large generated datasets.
    // They remain synchronous assertions, but cold CI workers can spend more
    // than Vitest's 5s default transforming those modules before the assertion.
    testTimeout: 30_000,
  },
});
