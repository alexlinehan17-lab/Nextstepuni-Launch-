import { defineConfig } from 'vite';
import fs from 'node:fs';
import base from '../../../../../vite.config.ts';
export default defineConfig(env => {
  const config = typeof base === 'function' ? base(env) : base;
  // A cache of its own: node_modules is shared with other worktrees, and their
  // dev servers would otherwise re-optimise over each other's cache.
  return { ...config, cacheDir: 'tmp/chemistry-audit/vite-cache',
    server: { ...config.server, fs: { allow: [process.cwd(), fs.realpathSync('node_modules')] } } };
});
