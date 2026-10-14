/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — where pdf.js finds its runtime data, shared by the app and the
 * Vite plugin that serves it (vite.config.ts).
 *
 * pdf.js decodes CCITT and JBIG2 scans with jbig2.wasm, JPEG 2000 with
 * openjpeg.wasm, and fetches CMaps and standard fonts on demand. Without these
 * URLs it asks the main thread for the bytes through the message handler of
 * whichever document was opened MOST RECENTLY on the shared worker: the decoder
 * keeps that handler in a static field. Closing that document destroys the
 * handler, and the next scan on any other document waits for a reply that never
 * comes, so a Topic Atlas crop stayed blank after the Viewer opened and closed.
 * With these URLs and `useWorkerFetch` the worker fetches the files itself and
 * no document depends on another one staying open.
 *
 * The path carries the pdfjs-dist version so a cached worker never pairs with
 * a decoder from another release.
 */

/** The pdfjs-dist directories pdf.js reads at runtime. */
export const PDFJS_RESOURCE_DIRS = ['cmaps', 'standard_fonts', 'wasm'] as const;

/** Site path under which the pdfjs-dist `version` resources are served. */
export function pdfjsResourceRoot(version: string): string {
  return `/pdfjs-${version}/`;
}

/** The file inside pdfjs-dist that a request path names, or null when the
 *  path is not one of the served resources. */
export function pdfjsResourceFile(pathname: string, version: string): string | null {
  const root = pdfjsResourceRoot(version);
  if (!pathname.startsWith(root)) return null;
  const rest = pathname.slice(root.length);
  const slash = rest.indexOf('/');
  const dir = rest.slice(0, slash);
  const name = rest.slice(slash + 1);
  if (slash < 0 || !(PDFJS_RESOURCE_DIRS as readonly string[]).includes(dir)) return null;
  if (!/^[A-Za-z0-9_.-]+$/.test(name) || name.startsWith('.')) return null;
  return `${dir}/${name}`;
}

export interface PdfjsResourceOptions {
  cMapUrl: string;
  cMapPacked: true;
  standardFontDataUrl: string;
  wasmUrl: string;
  useWorkerFetch: true;
}

/** getDocument options that let the worker fetch every resource itself.
 *  URLs are absolute because the worker resolves relative ones against its
 *  own script URL. */
export function pdfjsResourceOptions(version: string, base: string): PdfjsResourceOptions {
  const root = new URL(pdfjsResourceRoot(version), base).href;
  return {
    cMapUrl: `${root}cmaps/`,
    cMapPacked: true,
    standardFontDataUrl: `${root}standard_fonts/`,
    wasmUrl: `${root}wasm/`,
    useWorkerFetch: true,
  };
}
