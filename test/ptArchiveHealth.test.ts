/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail archive-health probe: status classification (a 402
 * billing refusal or 403/5xx reads as an archive outage; 2xx and a mere 404
 * do not; a network error is inconclusive), once-per-load caching of a
 * conclusive result, and re-probing after an inconclusive network error.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  archiveHealth,
  classifyProbe,
  resetArchiveHealthForTests,
} from '../components/PaperTrail/archiveHealth';

describe('classifyProbe', () => {
  it('reads success as ok (200 full, 206 partial)', () => {
    expect(classifyProbe(200)).toBe('ok');
    expect(classifyProbe(206)).toBe('ok');
  });

  it('reads a missing object as ok — one 404 says nothing about the archive', () => {
    expect(classifyProbe(404)).toBe('ok');
  });

  it('reads server-side refusals as down (402 billing, 403 rules, 5xx outage)', () => {
    expect(classifyProbe(402)).toBe('down');
    expect(classifyProbe(403)).toBe('down');
    expect(classifyProbe(500)).toBe('down');
    expect(classifyProbe(503)).toBe('down');
  });

  it('reads no response as unknown — the student’s own connection may be at fault', () => {
    expect(classifyProbe(null)).toBe('unknown');
  });
});

describe('archiveHealth', () => {
  const URL = 'https://example.test/papers/probe.pdf';

  beforeEach(() => {
    resetArchiveHealthForTests();
  });
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('probes with a 2-byte range request and caches a conclusive result', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 402 });
    vi.stubGlobal('fetch', fetchMock);
    await expect(archiveHealth(URL)).resolves.toBe('down');
    await expect(archiveHealth(URL)).resolves.toBe('down');
    expect(fetchMock).toHaveBeenCalledTimes(1);
    expect(fetchMock).toHaveBeenCalledWith(URL, { headers: { Range: 'bytes=0-1' } });
  });

  it('caches ok results too — one probe per page load', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ status: 206 });
    vi.stubGlobal('fetch', fetchMock);
    await expect(archiveHealth(URL)).resolves.toBe('ok');
    await expect(archiveHealth(URL)).resolves.toBe('ok');
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('does not cache an inconclusive network error — the next call re-probes', async () => {
    const fetchMock = vi
      .fn()
      .mockRejectedValueOnce(new Error('offline'))
      .mockResolvedValueOnce({ status: 200 });
    vi.stubGlobal('fetch', fetchMock);
    await expect(archiveHealth(URL)).resolves.toBe('unknown');
    await expect(archiveHealth(URL)).resolves.toBe('ok');
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
