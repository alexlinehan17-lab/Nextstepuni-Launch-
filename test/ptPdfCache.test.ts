/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail PDF CacheStorage layer: pure LRU bookkeeping, cache-hit
 * serving without a network round-trip, miss-populate, LRU eviction at the cap,
 * and graceful fallback to plain fetch when CacheStorage is broken or absent.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  fetchPdfCached,
  touchLru,
  MAX_PDF_CACHE_ENTRIES,
} from '../components/PaperTrail/pdfCache';

// Minimal Response stand-in with just the surface fetchPdfCached touches.
const fakeRes = (byte: number, ok = true) => ({
  ok,
  clone(): unknown {
    return fakeRes(byte, ok);
  },
  arrayBuffer: () => Promise.resolve(new Uint8Array([byte]).buffer),
});

class FakeCache {
  store = new Map<string, { arrayBuffer: () => Promise<ArrayBuffer> }>();
  match(url: string) {
    return Promise.resolve(this.store.get(url));
  }
  put(url: string, res: { arrayBuffer: () => Promise<ArrayBuffer> }) {
    this.store.set(url, res);
    return Promise.resolve();
  }
  delete(url: string) {
    return Promise.resolve(this.store.delete(url));
  }
}

describe('Paper Trail — PDF cache LRU (pure)', () => {
  it('moves a touched url to the front and dedupes', () => {
    expect(touchLru(['a', 'b', 'c'], 'c', 5)).toEqual({ order: ['c', 'a', 'b'], evict: [] });
    expect(touchLru([], 'a', 5)).toEqual({ order: ['a'], evict: [] });
  });

  it('evicts least-recently-used entries beyond the cap', () => {
    const { order, evict } = touchLru(['a', 'b', 'c'], 'd', 3);
    expect(order).toEqual(['d', 'a', 'b']);
    expect(evict).toEqual(['c']);
  });
});

describe('Paper Trail — PDF cache fetch path', () => {
  let cache: FakeCache;
  const fetchSpy = vi.fn();

  beforeEach(() => {
    localStorage.clear();
    cache = new FakeCache();
    fetchSpy.mockReset();
    vi.stubGlobal('caches', { open: () => Promise.resolve(cache) });
    vi.stubGlobal('fetch', fetchSpy);
  });
  afterEach(() => vi.unstubAllGlobals());

  it('populates the cache on a miss and returns the bytes', async () => {
    fetchSpy.mockResolvedValue(fakeRes(7));
    const bytes = await fetchPdfCached('https://x/paper.pdf');
    expect(new Uint8Array(bytes!)[0]).toBe(7);
    expect(fetchSpy).toHaveBeenCalledTimes(1);
    expect(cache.store.has('https://x/paper.pdf')).toBe(true);
  });

  it('serves a cache hit without touching the network', async () => {
    cache.store.set('https://x/paper.pdf', fakeRes(9));
    const bytes = await fetchPdfCached('https://x/paper.pdf');
    expect(new Uint8Array(bytes!)[0]).toBe(9);
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it(`evicts the least-recently-used PDF past ${MAX_PDF_CACHE_ENTRIES} entries`, async () => {
    fetchSpy.mockImplementation(() => Promise.resolve(fakeRes(1)));
    for (let i = 0; i < MAX_PDF_CACHE_ENTRIES + 1; i++) {
      await fetchPdfCached(`https://x/p${i}.pdf`);
    }
    expect(cache.store.size).toBe(MAX_PDF_CACHE_ENTRIES);
    expect(cache.store.has('https://x/p0.pdf')).toBe(false); // oldest evicted
    expect(cache.store.has(`https://x/p${MAX_PDF_CACHE_ENTRIES}.pdf`)).toBe(true);
  });

  it('returns null (no cache write) for a non-OK response', async () => {
    fetchSpy.mockResolvedValue(fakeRes(0, false));
    expect(await fetchPdfCached('https://x/missing.pdf')).toBeNull();
    expect(cache.store.size).toBe(0);
  });

  it('falls back to plain fetch when CacheStorage is broken', async () => {
    vi.stubGlobal('caches', { open: () => Promise.reject(new Error('nope')) });
    fetchSpy.mockResolvedValue(fakeRes(5));
    const bytes = await fetchPdfCached('https://x/paper.pdf');
    expect(new Uint8Array(bytes!)[0]).toBe(5);
    expect(fetchSpy).toHaveBeenCalledTimes(1);
  });

  it('falls back to plain fetch when CacheStorage is absent', async () => {
    vi.unstubAllGlobals();
    vi.stubGlobal('fetch', fetchSpy);
    fetchSpy.mockResolvedValue(fakeRes(4));
    const bytes = await fetchPdfCached('https://x/paper.pdf');
    expect(new Uint8Array(bytes!)[0]).toBe(4);
  });

  it('returns null when everything fails (caller falls back to pdf.js)', async () => {
    fetchSpy.mockRejectedValue(new Error('offline'));
    expect(await fetchPdfCached('https://x/paper.pdf')).toBeNull();
  });
});
