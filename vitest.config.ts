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
