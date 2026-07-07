/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the Paper Trail local recents + pins store: recents dedupe newest-first
 * and cap at 6, pins toggle and cap, and everything is isolated per uid.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import {
  isPinned,
  listPins,
  listRecentOpens,
  recordRecentOpen,
  togglePin,
  MAX_PINS,
  MAX_RECENTS,
  type PaperRef,
} from '../components/PaperTrail/recentsStore';

const ref = (n: number): Omit<PaperRef, 'at'> => ({
  key: `biology|${2010 + n}|higher|ev|f${n}`,
  subjectId: 'biology',
  year: 2010 + n,
  level: 'higher',
  lang: 'ev',
  fileid: `f${n}`,
  label: 'Paper One',
  kind: 'paper',
});

describe('Paper Trail — recents store', () => {
  beforeEach(() => localStorage.clear());

  it('records opens newest-first and dedupes by key', () => {
    recordRecentOpen('u1', ref(1), 1000);
    recordRecentOpen('u1', ref(2), 2000);
    recordRecentOpen('u1', ref(1), 3000); // re-open moves to front, no dupe
    const recents = listRecentOpens('u1');
    expect(recents.map(r => r.fileid)).toEqual(['f1', 'f2']);
    expect(recents[0].at).toBe(3000);
  });

  it(`caps recents at ${MAX_RECENTS}`, () => {
    for (let i = 0; i < MAX_RECENTS + 3; i++) recordRecentOpen('u1', ref(i), i);
    const recents = listRecentOpens('u1');
    expect(recents).toHaveLength(MAX_RECENTS);
    expect(recents[0].fileid).toBe(`f${MAX_RECENTS + 2}`); // newest survives
  });

  it('is isolated per uid (and anon)', () => {
    recordRecentOpen('u1', ref(1), 1);
    recordRecentOpen(undefined, ref(2), 2);
    expect(listRecentOpens('u1')).toHaveLength(1);
    expect(listRecentOpens('u2')).toHaveLength(0);
    expect(listRecentOpens(undefined).map(r => r.fileid)).toEqual(['f2']);
  });

  it('toggles pins on and off, reporting the new state', () => {
    expect(togglePin('u1', ref(1), 100)).toBe(true);
    expect(isPinned('u1', ref(1).key)).toBe(true);
    expect(listPins('u1')).toHaveLength(1);
    expect(togglePin('u1', ref(1), 200)).toBe(false);
    expect(isPinned('u1', ref(1).key)).toBe(false);
    expect(listPins('u1')).toHaveLength(0);
  });

  it(`caps pins at ${MAX_PINS}, newest pin first`, () => {
    for (let i = 0; i < MAX_PINS + 2; i++) togglePin('u1', ref(i), i);
    const pins = listPins('u1');
    expect(pins).toHaveLength(MAX_PINS);
    expect(pins[0].fileid).toBe(`f${MAX_PINS + 1}`);
  });

  it('survives corrupt storage by reading empty', () => {
    localStorage.setItem('nsu-pt-recents:u1', '{not json');
    localStorage.setItem('nsu-pt-pins:u1', '"a string"');
    expect(listRecentOpens('u1')).toEqual([]);
    expect(listPins('u1')).toEqual([]);
  });
});
