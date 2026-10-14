/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — pdf.js lazy singleton, shared by the Viewer and the Topic
 * Vault. Legacy build, module worker; a worker whose script fails to fetch
 * dies silently, so failures reset the singleton for a clean retry.
 *
 * Every document shares that one worker, so every document opens through
 * openPdfDocument: see pdfjsResources.ts for why one opened without the
 * resource URLs can blank a crop on another.
 */

import type { PDFDocumentLoadingTask } from 'pdfjs-dist';
import type { DocumentInitParameters } from 'pdfjs-dist/types/src/display/api';
import { pdfjsResourceOptions } from './pdfjsResources';

// eslint-disable-next-line @typescript-eslint/consistent-type-imports -- typing a dynamic module namespace requires typeof import()
export type PdfjsModule = typeof import('pdfjs-dist/legacy/build/pdf.mjs');

/** Open a PDF on the shared worker with the resource URLs pdf.js needs. */
export function openPdfDocument(pdfjs: PdfjsModule, src: DocumentInitParameters): PDFDocumentLoadingTask {
  return pdfjs.getDocument({ ...src, ...pdfjsResourceOptions(pdfjs.version, document.baseURI) });
}

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
