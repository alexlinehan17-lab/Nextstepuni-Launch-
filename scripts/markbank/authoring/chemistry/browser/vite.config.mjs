import { defineConfig } from 'vite';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import base from '../../../../../vite.config.ts';
export default defineConfig(env => {
  const config = typeof base === 'function' ? base(env) : base;
  // A dependency cache of its own, OUTSIDE the worktree. node_modules is shared
  // with other worktrees, whose dev servers would re-optimise over a shared
  // cache; and a cache inside the worktree is swept up by `npm run typecheck`
  // (tsconfig has allowJs and no "include"), which ran tsc out of memory on
  // 2026-10-14 typechecking 58 MB of bundled dependencies under tmp/.
  const cacheDir = process.env.CHEM_QA_VITE_CACHE ?? path.join(os.tmpdir(), 'nsu-chemistry-qa-vite-cache');
  return { ...config, cacheDir,
    server: { ...config.server, fs: { allow: [process.cwd(), fs.realpathSync('node_modules')] } } };
});
