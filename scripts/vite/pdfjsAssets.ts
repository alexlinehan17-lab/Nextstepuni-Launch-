import { readFileSync, readdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import path from 'node:path';
import type { Plugin } from 'vite';
import { PDFJS_WASM_PATH } from '../../components/PaperTrail/pdfjsAssets';

/** PDF.js loads image decoders by filename, so preserve their directory layout. */
export function pdfjsAssets(): Plugin {
  const packageRoot = path.dirname(createRequire(import.meta.url).resolve('pdfjs-dist/package.json'));
  const directory = path.join(packageRoot, 'wasm');
  const files = new Set(readdirSync(directory));
  return {
    name: 'pdfjs-image-decoders',
    configureServer(server) {
      const prefix = `${server.config.base}${PDFJS_WASM_PATH}`;
      server.middlewares.use((req, res, next) => {
        const pathname = (req.url ?? '').split('?')[0];
        if (!pathname.startsWith(prefix)) return next();
        const filename = pathname.slice(prefix.length);
        if (!files.has(filename)) return next();
        res.setHeader('Content-Type', filename.endsWith('.wasm') ? 'application/wasm'
          : filename.endsWith('.js') ? 'text/javascript' : 'text/plain');
        res.end(readFileSync(path.join(directory, filename)));
      });
    },
    generateBundle() {
      for (const filename of files) {
        this.emitFile({ type: 'asset', fileName: PDFJS_WASM_PATH + filename,
          source: readFileSync(path.join(directory, filename)) });
      }
    },
  };
}
