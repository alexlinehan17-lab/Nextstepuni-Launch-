import { defineConfig, mergeConfig } from 'vite';
import base from '../../../../../../vite.config';
import { realpathSync } from 'node:fs';
import { resolve } from 'node:path';
export default defineConfig(env => mergeConfig(typeof base === 'function' ? base(env) : base, {
  server: { fs: { allow: [process.cwd(), realpathSync(resolve('node_modules'))] } },
}));
