/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — shared PDF documents for the Topic Vault feed. A topic's
 * question cards span many papers; this keeps a small LRU of open documents
 * (bytes come through the CacheStorage pdfCache first) and serialises loads
 * so scrolling a feed doesn't fan out a dozen multi-megabyte fetches at once.
 *
 * Cards render a crop ONCE into canvases, so evicting (destroying) a document
 * later never blanks anything already on screen.
 */

import type { PDFDocumentLoadingTask, PDFDocumentProxy } from 'pdfjs-dist';
import { loadPdfjs } from './pdfjsLoader';
import { fetchPdfCached } from './pdfCache';

const MAX_OPEN_DOCS = 6;

interface OpenDoc {
  task: PDFDocumentLoadingTask;
  doc: PDFDocumentProxy;
}

const open = new Map<string, Promise<OpenDoc>>(); // insertion order = LRU
let queue: Promise<unknown> = Promise.resolve();

const evictIfNeeded = () => {
  while (open.size > MAX_OPEN_DOCS) {
    const oldest = open.keys().next().value as string | undefined;
    if (oldest === undefined) return;
    const doomed = open.get(oldest)!;
    open.delete(oldest);
    doomed.then(e => e.task.destroy()).catch(() => { /* already failed */ });
  }
};

/** Open (or reuse) the PDF at `url`. Loads are serialised via a simple chain;
 *  failures are not cached so a retry gets a fresh attempt. */
export function vaultPdf(url: string): Promise<PDFDocumentProxy> {
  const hit = open.get(url);
  if (hit) {
    // refresh LRU position
    open.delete(url);
    open.set(url, hit);
    return hit.then(e => e.doc);
  }
  const p: Promise<OpenDoc> = queue.then(async () => {
    const pdfjs = await loadPdfjs();
    const bytes = await fetchPdfCached(url);
    const task = bytes
      ? pdfjs.getDocument({ data: new Uint8Array(bytes) })
      : pdfjs.getDocument({ url });
    const doc = await task.promise;
    return { task, doc };
  });
  // Serialise the next load behind this one, but don't poison the chain.
  queue = p.catch(() => undefined);
  open.set(url, p);
  p.catch(() => open.delete(url));
  evictIfNeeded();
  return p.then(e => e.doc);
}

/** Drop and destroy everything — call when leaving the vault. */
export function releaseVaultPdfs(): void {
  for (const p of open.values()) p.then(e => e.task.destroy()).catch(() => { /* noop */ });
  open.clear();
}
