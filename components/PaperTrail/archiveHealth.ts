/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Paper Trail — archive health probe.
 *
 * When the Storage backend refuses media downloads wholesale (billing lapse →
 * HTTP 402, rules misdeploy → 403, provider outage → 5xx), every paper in the
 * tool fails one by one with no explanation. This module makes ONE tiny
 * range-request against a known corpus document and classifies the archive as
 * up or down, so the home screen can show a single honest banner instead of
 * letting students discover the outage paper by paper.
 *
 * The probe costs two bytes of billed download, runs at most once per page
 * load (module-level cache; an inconclusive network error is not cached so a
 * flaky connection can re-probe on the next mount), and NEVER blocks the UI —
 * callers render normally and only react to a confirmed 'down'.
 */

export type ArchiveHealth = 'ok' | 'down' | 'unknown';

/** Classify a probe response status. Pure — unit-tested in
 *  test/ptArchiveHealth.test.ts.
 *  - 2xx (200 full / 206 partial) → the archive serves documents: ok.
 *  - 404 → THIS object is missing, which says nothing about the archive: ok.
 *  - any other 4xx/5xx (402 billing, 403 rules, 5xx outage) → down.
 *  - null (network error / no response) → unknown: the student's own
 *    connection may be at fault, so no banner is shown. */
export function classifyProbe(status: number | null): ArchiveHealth {
  if (status == null) return 'unknown';
  if (status >= 200 && status < 300) return 'ok';
  if (status === 404) return 'ok';
  if (status >= 400) return 'down';
  return 'unknown';
}

let cached: Promise<ArchiveHealth> | null = null;

/** Probe the archive once per page load. `probeUrl` should be any real corpus
 *  document URL (the caller picks the first paper in the index). */
export function archiveHealth(probeUrl: string): Promise<ArchiveHealth> {
  if (!cached) {
    cached = fetch(probeUrl, { headers: { Range: 'bytes=0-1' } })
      .then(r => classifyProbe(r.status))
      .catch(() => 'unknown' as ArchiveHealth);
    // An inconclusive probe must not stick for the rest of the session.
    cached.then(h => {
      if (h === 'unknown') cached = null;
    });
  }
  return cached;
}

/** Test hook — resets the module cache between cases. */
export function resetArchiveHealthForTests(): void {
  cached = null;
}
