import { describe, expect, it } from 'vitest';

// Vite hook handlers are typed as unions; the tests call them directly.
type AnyFunction = (...args: unknown[]) => unknown;
import { pdfjsAssets } from '../scripts/vite/pdfjsAssets';
import { PDFJS_WASM_PATH, pdfjsDocumentOptions } from '../components/PaperTrail/pdfjsAssets';

describe('PDF image decoder delivery', () => {
  it('ships real decoders, JavaScript fallbacks and their licences at the reader URL', () => {
    const emitted: { fileName: string; source: Buffer }[] = [];
    const plugin = pdfjsAssets();
    const generate = plugin.generateBundle as unknown as AnyFunction;
    generate.call({ emitFile: (file: typeof emitted[number]) => emitted.push(file) });
    for (const name of ['jbig2.wasm', 'openjpeg.wasm', 'qcms_bg.wasm']) {
      const file = emitted.find(f => f.fileName === PDFJS_WASM_PATH + name)!;
      expect([...file.source.subarray(0, 4)]).toEqual([0, 97, 115, 109]);
    }
    for (const name of ['jbig2_nowasm_fallback.js', 'openjpeg_nowasm_fallback.js',
      'LICENSE_JBIG2', 'LICENSE_OPENJPEG', 'LICENSE_QCMS']) {
      expect(emitted.find(f => f.fileName === PDFJS_WASM_PATH + name)?.source.length).toBeGreaterThan(0);
    }
    expect(new URL(pdfjsDocumentOptions().wasmUrl).pathname).toBe('/' + PDFJS_WASM_PATH);
  });

  it('serves binary decoder bytes under a deployment base and ignores unknown paths', () => {
    let middleware: AnyFunction;
    const configure = pdfjsAssets().configureServer as unknown as AnyFunction;
    configure({ config: { base: '/preview/' }, middlewares: { use: (fn: AnyFunction) => { middleware = fn; } } });
    const headers: Record<string, string> = {};
    let data: Buffer | undefined;
    let missed = 0;
    const response = { setHeader: (key: string, value: string) => { headers[key] = value; }, end: (value: Buffer) => { data = value; } };
    middleware!({ url: '/preview/' + PDFJS_WASM_PATH + 'jbig2.wasm?v=1' }, response, () => { missed++; });
    expect(headers['Content-Type']).toBe('application/wasm');
    expect([...data!.subarray(0, 4)]).toEqual([0, 97, 115, 109]);
    middleware!({ url: '/preview/' + PDFJS_WASM_PATH + '../package.json' }, response, () => { missed++; });
    expect(missed).toBe(1);
  });
});
