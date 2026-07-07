/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — pdf.js lazy singleton, shared by the Viewer and the Topic
 * Vault. Legacy build, module worker; a worker whose script fails to fetch
 * dies silently, so failures reset the singleton for a clean retry.
 */

// eslint-disable-next-line @typescript-eslint/consistent-type-imports -- typing a dynamic module namespace requires typeof import()
export type PdfjsModule = typeof import('pdfjs-dist/legacy/build/pdf.mjs');

let pdfjsPromise: Promise<PdfjsModule> | null = null;

export function loadPdfjs(): Promise<PdfjsModule> {
  if (!pdfjsPromise) {
    pdfjsPromise = import('pdfjs-dist/legacy/build/pdf.mjs').then(mod => {
      const worker = new Worker(
        new URL('pdfjs-dist/legacy/build/pdf.worker.mjs', import.meta.url),
        { type: 'module' },
      );
      // A worker whose script fails to fetch dies silently — reset the
      // singleton so the next attempt can retry with a fresh worker.
      worker.onerror = () => {
        pdfjsPromise = null;
      };
      mod.GlobalWorkerOptions.workerPort = worker;
      return mod;
    });
    pdfjsPromise.catch(() => {
      pdfjsPromise = null; // allow retry after a transient failure
    });
  }
  return pdfjsPromise;
}
