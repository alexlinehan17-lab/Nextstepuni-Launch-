/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Examiner's Chair — save-and-exit resume slot.
 */

import { beforeEach, describe, expect, it } from 'vitest';
import {
  RESUME_STALE_MS,
  clearResume,
  describeResume,
  hasResumableProgress,
  loadResume,
  saveResume,
  type ChairResumeSnapshot,
} from '../components/ExaminersChair/sessionResume';

const NOW = 1_700_000_000_000;

const snap = (overrides: Partial<ChairResumeSnapshot> = {}): ChairResumeSnapshot => ({
  v: 1,
  sessionId: 'bu-h-1',
  sessionTitle: 'The two-mark link',
  stage: 'mark',
  scriptIdx: 1,
  scriptCount: 4,
  decisions: { 'a1:name': true },
  chosenLevel: null,
  scores: [{ scriptId: 's1', agreement: 0.75, studentMarks: 3, examinerMarks: 4, maxMarks: 5 }],
  misses: [{ key: 'business::Link', subject: 'business', label: 'Link', over: 1, under: 0, sessionId: 'bu-h-1' }],
  decisionDeltas: [{ sessionId: 'bu-h-1', scriptId: 's1', choice: 'a1:name:earned' }],
  reason: 'looked like a full link',
  borderlineOnly: false,
  dailyMode: false,
  restrictScriptId: null,
  elapsedMs: 3 * 60_000,
  savedAt: NOW,
  ...overrides,
});

beforeEach(() => localStorage.clear());

describe('resume slot round-trip', () => {
  it('saves and restores the desk exactly, per uid', () => {
    saveResume('u1', snap());
    const back = loadResume('u1', NOW + 1000);
    expect(back).toEqual(snap());
    expect(loadResume('someone-else', NOW + 1000)).toBeNull();
    expect(loadResume(undefined, NOW + 1000)).toBeNull();
  });

  it('clearResume drops the slot', () => {
    saveResume('u1', snap());
    clearResume('u1');
    expect(loadResume('u1', NOW)).toBeNull();
  });

  it('a later save overwrites the slot (one desk per account)', () => {
    saveResume('u1', snap());
    saveResume('u1', snap({ scriptIdx: 2, stage: 'reveal', savedAt: NOW + 500 }));
    const back = loadResume('u1', NOW + 1000);
    expect(back?.scriptIdx).toBe(2);
    expect(back?.stage).toBe('reveal');
  });

  it('keeps drill flags so a resumed daily/borderline run stays a drill', () => {
    saveResume('u1', snap({ dailyMode: true, restrictScriptId: 's2', borderlineOnly: false }));
    const back = loadResume('u1', NOW);
    expect(back?.dailyMode).toBe(true);
    expect(back?.restrictScriptId).toBe('s2');
  });
});

describe('validation and staleness', () => {
  it('returns null on garbage or malformed payloads', () => {
    localStorage.setItem('chair-resume:u1', 'not json');
    expect(loadResume('u1', NOW)).toBeNull();
    localStorage.setItem('chair-resume:u1', JSON.stringify({ v: 1, sessionId: 42 }));
    expect(loadResume('u1', NOW)).toBeNull();
    localStorage.setItem('chair-resume:u1', JSON.stringify({ ...snap(), v: 99 }));
    expect(loadResume('u1', NOW)).toBeNull();
    localStorage.setItem('chair-resume:u1', JSON.stringify({ ...snap(), stage: 'summary' }));
    expect(loadResume('u1', NOW)).toBeNull();
  });

  it('drops a stale slot but keeps a fresh one', () => {
    saveResume('u1', snap({ savedAt: NOW }));
    expect(loadResume('u1', NOW + RESUME_STALE_MS - 1)).not.toBeNull();
    expect(loadResume('u1', NOW + RESUME_STALE_MS + 1)).toBeNull();
  });

  it('defaults optional-ish fields defensively', () => {
    const raw = { ...snap() } as Record<string, unknown>;
    delete raw.reason;
    delete raw.elapsedMs;
    delete raw.chosenLevel;
    delete raw.restrictScriptId;
    localStorage.setItem('chair-resume:u1', JSON.stringify(raw));
    const back = loadResume('u1', NOW);
    expect(back?.reason).toBe('');
    expect(back?.elapsedMs).toBe(0);
    expect(back?.chosenLevel).toBeNull();
    expect(back?.restrictScriptId).toBeNull();
  });
});

describe('hasResumableProgress', () => {
  it('is false on an untouched desk', () => {
    expect(hasResumableProgress({ scores: [], decisions: {}, chosenLevel: null })).toBe(false);
  });

  it('is true once any call has been made', () => {
    expect(hasResumableProgress({ scores: [], decisions: { 'a:b': true }, chosenLevel: null })).toBe(true);
    expect(hasResumableProgress({ scores: [], decisions: {}, chosenLevel: 'mid' })).toBe(true);
    expect(hasResumableProgress({ scores: snap().scores, decisions: {}, chosenLevel: null })).toBe(true);
  });
});

describe('describeResume', () => {
  it('names the script position and the minutes in', () => {
    expect(describeResume(snap())).toBe('Script 2 of 4 · about 3 min in');
  });

  it('rounds sub-minute sessions to a friendly line', () => {
    expect(describeResume(snap({ elapsedMs: 20_000 }))).toBe('Script 2 of 4 · under a minute in');
  });

  it('never claims a script beyond the run length', () => {
    expect(describeResume(snap({ scriptIdx: 9, scriptCount: 4 }))).toContain('Script 4 of 4');
  });
});
