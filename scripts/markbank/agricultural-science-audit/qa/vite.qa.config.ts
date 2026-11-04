import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
import {realpathSync} from 'node:fs';
export default defineConfig({root:process.cwd(),cacheDir:'tmp/agricultural-science-audit/vite-cache-qa',plugins:[react()],optimizeDeps:{entries:['scripts/markbank/agricultural-science-audit/qa/reader_qa.html']},server:{hmr:false,watch:{ignored:['**/2010-browser-qa/**','**/browser-runtime/**']},fs:{allow:[process.cwd(),realpathSync('node_modules'),realpathSync('paper-trail-corpus')]}}});
