/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — CacheStorage layer for corpus PDFs (poor-connection support).
 *
 * SEC PDFs are immutable per URL (versionless stable Storage paths), so
 * cache-first with NO revalidation is correct: a hit is served straight from
 * CacheStorage — instant on repeat opens, and it works fully offline. Misses
 * fetch over the network and populate the cache, capped at MAX_PDF_CACHE_ENTRIES
 * with LRU eviction (order tracked in localStorage — cache.keys() order is
 * insertion order, which never reflects re-use).
 *
 * This complements the service-worker 'paper-trail-pdfs' CacheFirst rule
 * (vite.config.ts): the SW only helps once registered + activated; this layer
 * works from the very first session, in dev, and in browsers where the SW
 * didn't install. Every cache operation is wrapped so a CacheStorage failure
 * can NEVER break the normal fetch path — worst case we degrade to plain
 * fetch, and if that fails too the caller falls back to pdf.js's own loader.
 *
 * The pure LRU bookkeeping is unit-tested in test/ptPdfCache.test.ts.
 */

export const PDF_CACHE_NAME = 'nsu-pt-pdfs-v1';
export const MAX_PDF_CACHE_ENTRIES = 40;

const LRU_KEY = 'nsu-pt-pdfcache-lru';

/** Pure LRU step: move `url` to the front of `order`, dedupe, and report which
 *  entries fall off the end at `max`. */
export function touchLru(
  order: string[],
  url: string,
  max: number,
): { order: string[]; evict: string[] } {
  const next = [url, ...order.filter(u => u !== url)];
  return { order: next.slice(0, max), evict: next.slice(max) };
}

const readLruOrder = (): string[] => {
  try {
    const raw = localStorage.getItem(LRU_KEY);
    const list = raw ? (JSON.parse(raw) as string[]) : [];
    return Array.isArray(list) ? list.filter(u => typeof u === 'string') : [];
  } catch {
    return [];
  }
};

const writeLruOrder = (order: string[]) => {
  try {
    localStorage.setItem(LRU_KEY, JSON.stringify(order));
  } catch {
    /* quota / private mode — LRU order is best-effort */
  }
};

const cachesAvailable = (): boolean =>
  typeof caches !== 'undefined' && typeof caches.open === 'function';

/** Record a use of `url` and evict anything beyond the cap. Best-effort. */
async function noteUse(cache: Cache, url: string): Promise<void> {
  const { order, evict } = touchLru(readLruOrder(), url, MAX_PDF_CACHE_ENTRIES);
  writeLruOrder(order);
  await Promise.all(evict.map(u => cache.delete(u).catch(() => false)));
}

/**
 * Fetch a corpus PDF, cache-first. Returns the bytes, or null when both the
 * cache and the network fail (the caller then lets pdf.js try its own URL
 * loader, which surfaces the existing retry / open-in-browser UI).
 */
export async function fetchPdfCached(url: string): Promise<ArrayBuffer | null> {
  if (cachesAvailable()) {
    try {
      const cache = await caches.open(PDF_CACHE_NAME);
      const hit = await cache.match(url);
      if (hit) {
        const bytes = await hit.arrayBuffer();
        // Touch, but never let bookkeeping failures lose a served hit.
        await noteUse(cache, url).catch(() => {});
        return bytes;
      }
      const res = await fetch(url);
      if (!res.ok) return null;
      const copy = res.clone();
      const bytes = await res.arrayBuffer();
      try {
        await cache.put(url, copy);
        await noteUse(cache, url);
      } catch {
        /* quota — the fetched bytes are still good */
      }
      return bytes;
    } catch {
      /* CacheStorage unusable (private mode, quota, disabled) — plain fetch */
    }
  }
  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    return await res.arrayBuffer();
  } catch {
    return null;
  }
}
