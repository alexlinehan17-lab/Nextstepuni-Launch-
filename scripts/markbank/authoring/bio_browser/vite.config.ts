/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The app's own Vite config, with the repository root served so the preview
 * page under scripts/ can be opened.
 */
import { defineConfig, mergeConfig } from 'vite';
import { realpathSync } from 'node:fs';
import base from '../../../../vite.config';

export default defineConfig(async env => mergeConfig(await (typeof base === 'function' ? base(env) : base), {
  server: { fs: { allow: [process.cwd(), realpathSync('node_modules')] } },
}));
