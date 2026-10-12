import { defineConfig, mergeConfig } from 'vite';
import { realpathSync } from 'node:fs';
import base from '../../../../../vite.config';
export default defineConfig(async env => mergeConfig(await (base as Function)(env), {server:{fs:{allow:[process.cwd(), realpathSync('node_modules')]}}}));
