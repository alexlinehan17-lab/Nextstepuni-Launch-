/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Full Loop save-and-exit store: places round-trip per paper
 * namespace, invalid/corrupt records read as null, and stale places expire.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import {
  clearLoopPlace,
  loadLoopPlace,
  saveLoopPlace,
  LOOP_PLACE_MAX_AGE_MS,
} from '../components/PaperTrail/loopResume';

const NS = 'u1|biology|2023|higher|ev|LC030ALP000EV.pdf';
const NOW = 1_700_000_000_000;

describe('Paper Trail — Full Loop resume store', () => {
  beforeEach(() => localStorage.clear());

  it('round-trips a saved place per paper namespace', () => {
    saveLoopPlace(NS, { idx: 3, total: 10, elapsedSec: 420, marked: 3 }, NOW);
    expect(loadLoopPlace(NS, NOW + 1000)).toEqual({
      idx: 3,
      total: 10,
      elapsedSec: 420,
      marked: 3,
      savedAt: NOW,
    });
    // A different paper (or account) sees nothing.
    expect(loadLoopPlace('u2|biology|2023|higher|ev|LC030ALP000EV.pdf', NOW)).toBeNull();
  });

  it('clears a place', () => {
    saveLoopPlace(NS, { idx: 1, total: 5, elapsedSec: 60, marked: 1 }, NOW);
    clearLoopPlace(NS);
    expect(loadLoopPlace(NS, NOW)).toBeNull();
  });

  it('expires stale places', () => {
    saveLoopPlace(NS, { idx: 2, total: 8, elapsedSec: 100, marked: 2 }, NOW);
    expect(loadLoopPlace(NS, NOW + LOOP_PLACE_MAX_AGE_MS - 1)).not.toBeNull();
    expect(loadLoopPlace(NS, NOW + LOOP_PLACE_MAX_AGE_MS + 1)).toBeNull();
    // The expired record is also removed.
    expect(localStorage.getItem('nsu-pt-loop:' + NS)).toBeNull();
  });

  it('rejects invalid or corrupt records', () => {
    localStorage.setItem('nsu-pt-loop:' + NS, '{oops');
    expect(loadLoopPlace(NS, NOW)).toBeNull();
    // idx out of range for the saved total.
    localStorage.setItem(
      'nsu-pt-loop:' + NS,
      JSON.stringify({ idx: 10, total: 10, elapsedSec: 1, marked: 0, savedAt: NOW }),
    );
    expect(loadLoopPlace(NS, NOW)).toBeNull();
    // negative idx / zero total.
    localStorage.setItem(
      'nsu-pt-loop:' + NS,
      JSON.stringify({ idx: -1, total: 0, elapsedSec: 1, marked: 0, savedAt: NOW }),
    );
    expect(loadLoopPlace(NS, NOW)).toBeNull();
  });

  it('normalises junk elapsed/marked fields to 0', () => {
    localStorage.setItem(
      'nsu-pt-loop:' + NS,
      JSON.stringify({ idx: 0, total: 4, elapsedSec: 'x', marked: -3, savedAt: NOW }),
    );
    const p = loadLoopPlace(NS, NOW)!;
    expect(p.elapsedSec).toBe(0);
    expect(p.marked).toBe(0);
    expect(p.idx).toBe(0);
  });
});
