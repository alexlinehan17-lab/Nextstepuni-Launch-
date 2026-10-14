/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — a scanned crop still renders after the Viewer opens and
 * closes. pdf.js decodes CCITT scans with jbig2.wasm, and unless every
 * document supplies the resource URLs it borrows the message handler of the
 * newest document on the shared worker to fetch that file. Closing the Viewer
 * destroyed that handler and the next scan on a Topic Atlas card waited
 * forever (2026 HL Agricultural Science, page 17).
 *
 * The fixture is synthetic, a 400 x 80 ruled box saved as a CCITT Group 4
 * image mask with Pillow, so no examination material is involved.
 */

import React from 'react';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { cleanup, render, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { PDFDocumentLoadingTask, PDFDocumentProxy } from 'pdfjs-dist';
import * as pdfjs from 'pdfjs-dist/legacy/build/pdf.mjs';
import Viewer from '../components/PaperTrail/Viewer';
import type * as PdfjsLoader from '../components/PaperTrail/pdfjsLoader';
import { releaseVaultPdfs, vaultPdf } from '../components/PaperTrail/vaultDocs';
import { pdfjsResourceFile } from '../components/PaperTrail/pdfjsResources';

const ROOT = process.cwd();
const FIXTURE = fs.readFileSync(path.join(ROOT, 'test/fixtures/paper-trail/ccitt-g4.pdf'));

// Every document the app opens goes through this spy, so a test can wait for
// the Viewer's own document to finish closing.
const tasks: PDFDocumentLoadingTask[] = [];
vi.mock('../components/PaperTrail/pdfjsLoader', async importOriginal => {
  const real = await importOriginal<typeof PdfjsLoader>();
  const lib = await import('pdfjs-dist/legacy/build/pdf.mjs');
  const spied = {
    ...lib,
    getDocument: (src: Parameters<typeof lib.getDocument>[0]) => {
      const task = lib.getDocument(src);
      tasks.push(task);
      return task;
    },
  };
  return { ...real, loadPdfjs: () => Promise.resolve(spied) };
});
vi.mock('../components/PaperTrail/pdfCache', () => ({
  fetchPdfCached: vi.fn(() => Promise.resolve(new Uint8Array(FIXTURE).buffer)),
}));

const served: string[] = [];
beforeEach(() => {
  served.length = 0;
  // The Viewer paints pages into canvases; jsdom has no 2D context.
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(null);
  // The worker's own fetch of pdf.js resources, answered from node_modules
  // exactly as the pdfjs-resources Vite plugin answers it.
  vi.stubGlobal('fetch', vi.fn((input: string | URL | Request) => {
    const url = new URL(input instanceof Request ? input.url : String(input));
    const file = url.origin === window.location.origin ? pdfjsResourceFile(url.pathname, pdfjs.version) : null;
    if (!file) return Promise.resolve(new Response(null, { status: 404, statusText: 'Not Found' }));
    served.push(file);
    return Promise.resolve(new Response(fs.readFileSync(path.join(ROOT, 'node_modules/pdfjs-dist', file))));
  }));
});
afterEach(async () => {
  cleanup();
  releaseVaultPdfs();
  await Promise.all(tasks.splice(0).map(task => task.destroy().catch(() => {})));
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

/** Operator list of page 1, or 'timeout' if pdf.js never answers. */
const firstPageOps = async (doc: PDFDocumentProxy) => {
  const page = await doc.getPage(1);
  return Promise.race([
    page.getOperatorList().then(list => list.fnArray),
    new Promise<'timeout'>(resolve => setTimeout(() => resolve('timeout'), 5000)),
  ]);
};

describe('Paper Trail pdf.js resources', () => {
  it('decodes a CCITT scan on a Topic Atlas crop document', async () => {
    const card = await vaultPdf('https://papers.example/control.pdf');
    const ops = await firstPageOps(card);
    expect(ops).not.toBe('timeout');
    expect(ops).toContain(pdfjs.OPS.paintImageMaskXObject);
    expect(served).toContain('wasm/jbig2.wasm');
  });

  it('still decodes it after the Viewer opens its own copy and closes', async () => {
    const card = await vaultPdf('https://papers.example/card.pdf');
    const opened = tasks.length;
    render(<Viewer title="Synthetic paper" paper={{ url: 'https://papers.example/viewer.pdf', label: 'Paper', bytes: 0 }} onClose={() => {}} />);
    await waitFor(() => expect(document.querySelector('[data-page="1"]')).not.toBeNull());
    const viewerTasks = tasks.slice(opened);
    expect(viewerTasks).toHaveLength(1);
    cleanup();
    await Promise.all(viewerTasks.map(task => task.destroy()));
    const ops = await firstPageOps(card);
    expect(ops).not.toBe('timeout');
    expect(ops).toContain(pdfjs.OPS.paintImageMaskXObject);
  });

  it('opens every app document through openPdfDocument', () => {
    // A single document opened without the resource URLs puts the borrowed
    // handler back, so the guard is on every call site, not just the three.
    const files = execFileSync('git', ['ls-files', '*.ts', '*.tsx'], { cwd: ROOT, encoding: 'utf8' })
      .split('\n')
      .filter(file => file && !/^(test|scripts|functions)\//.test(file) && file !== 'components/PaperTrail/pdfjsLoader.ts');
    const direct = files.filter(file => /\bgetDocument\s*\(/.test(fs.readFileSync(path.join(ROOT, file), 'utf8')));
    expect(direct).toEqual([]);
  });
});
