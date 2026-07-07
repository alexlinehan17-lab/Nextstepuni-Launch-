/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * QoL shell features — pure-logic tests: command palette fuzzy scoring,
 * the last-visited store, and the what's-new seen marker.
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { fuzzyScore, TOOL_TITLES } from '../components/CommandPalette';
import { recordVisit, getLastVisit } from '../components/lastVisited';
import { CHANGELOG, LATEST_CHANGELOG_ID } from '../data/changelog';

describe('command palette fuzzy scoring', () => {
  it('ranks prefix > word start > substring > initials > subsequence', () => {
    const prefix = fuzzyScore('paper', 'Paper Trail');
    const wordStart = fuzzyScore('trail', 'Paper Trail');
    const substring = fuzzyScore('aper', 'Paper Trail');
    const initials = fuzzyScore('cps', 'CAO Points Simulator');
    const subseq = fuzzyScore('ppl', 'Paper Trail');
    expect(prefix).toBeGreaterThan(wordStart);
    expect(wordStart).toBeGreaterThan(substring);
    expect(substring).toBeGreaterThan(initials);
    expect(initials).toBeGreaterThan(subseq);
    expect(subseq).toBeGreaterThan(0);
  });

  it('is case-insensitive and rejects non-matches', () => {
    expect(fuzzyScore('PAPER', 'paper trail')).toBe(100);
    expect(fuzzyScore('xyz', 'Paper Trail')).toBe(0);
    expect(fuzzyScore('', 'Paper Trail')).toBe(0);
  });

  it('has a title for every launchpad tool id it exposes', () => {
    for (const [id, title] of Object.entries(TOOL_TITLES)) {
      expect(id).toMatch(/^[a-z][a-z0-9-]*$/);
      expect(title.length).toBeGreaterThan(2);
    }
  });
});

describe('last-visited store', () => {
  beforeEach(() => localStorage.clear());

  it('round-trips a module visit per uid', () => {
    recordVisit('u1', { kind: 'module', id: 'active-recall', label: 'Mastering Active Recall' });
    const v = getLastVisit('u1');
    expect(v?.kind).toBe('module');
    expect(v?.id).toBe('active-recall');
    expect(v?.at).toBeGreaterThan(0);
    expect(getLastVisit('u2')).toBeNull();
  });

  it('overwrites with the most recent visit and keeps sub detail', () => {
    recordVisit('u1', { kind: 'module', id: 'a', label: 'A' });
    recordVisit('u1', { kind: 'tool', id: 'paper-trail', label: 'Paper Trail', sub: 'Biology · 2023 · Higher' });
    const v = getLastVisit('u1');
    expect(v?.kind).toBe('tool');
    expect(v?.sub).toBe('Biology · 2023 · Higher');
  });

  it('returns null on malformed stored data', () => {
    localStorage.setItem('nsu-lastvisit:u1', '{"kind":"nope"}');
    expect(getLastVisit('u1')).toBeNull();
    localStorage.setItem('nsu-lastvisit:u1', 'not json');
    expect(getLastVisit('u1')).toBeNull();
  });
});

describe('changelog', () => {
  it('is newest-first with unique ids and the latest id exported', () => {
    expect(CHANGELOG.length).toBeGreaterThan(0);
    const ids = CHANGELOG.map(e => e.id);
    expect(new Set(ids).size).toBe(ids.length);
    expect(LATEST_CHANGELOG_ID).toBe(ids[0]);
    for (const e of CHANGELOG) {
      expect(e.lines.length).toBeGreaterThan(0);
      expect(e.lines.length).toBeLessThanOrEqual(3);
    }
  });
});
