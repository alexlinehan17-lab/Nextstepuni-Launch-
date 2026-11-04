/** @license SPDX-License-Identifier: Apache-2.0 */

export type ArchiveHealth = 'ok' | 'down' | 'unknown';

// A failed sample warns that papers may be unavailable; it does not prove
// every document is down. Missing objects and client errors are inconclusive.
export function classifyProbe(status: number | null): ArchiveHealth {
  if (status == null) return 'unknown';
  if (status >= 200 && status < 300) return 'ok';
  if ([402, 403, 429].includes(status) || status >= 500) return 'down';
  return 'unknown';
}

let cached: { url: string; expires: number; result: Promise<ArchiveHealth> } | null = null;

/** Share concurrent probes, but check for recovery on a later visit. Cancel
 * the body if a server ignores the two-byte range. */
export function archiveHealth(probeUrl: string): Promise<ArchiveHealth> {
  if (cached?.url === probeUrl && cached.expires > Date.now()) return cached.result;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8_000);
  const result = fetch(probeUrl, {
    headers: { Range: 'bytes=0-1' }, signal: controller.signal,
  }).then(response => {
    void response.body?.cancel().catch(() => {});
    return classifyProbe(response.status);
  }).catch(() => 'unknown' as ArchiveHealth).finally(() => clearTimeout(timeout));
  cached = { url: probeUrl, expires: Date.now() + 60_000, result };
  void result.then(health => {
    if (health === 'unknown' && cached?.result === result) cached = null;
  });
  return result;
}

export function resetArchiveHealthForTests(): void {
  cached = null;
}
