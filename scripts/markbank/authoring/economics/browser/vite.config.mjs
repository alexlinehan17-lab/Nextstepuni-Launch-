import { defineConfig } from 'vite';
import fs from 'node:fs';
import base from '../../../../../vite.config.ts';
export default defineConfig(env => {
  const config = typeof base === 'function' ? base(env) : base;
  return { ...config, server: { ...config.server, fs: { allow: [process.cwd(), fs.realpathSync('node_modules')] } } };
});
