/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Guards the GC cohort-tag store (feature E8): toggling adds/removes, tags are
 * scoped per school + student, and clearing the last tag drops the entry.
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { getTags, toggleTag } from '../components/gc/cohortTags';

describe('GC cohort tags', () => {
  beforeEach(() => localStorage.clear());

  it('toggles a tag on and off', () => {
    expect(getTags('stA', 'u1')).toEqual([]);
    expect(toggleTag('stA', 'u1', 'DEIS')).toEqual(['DEIS']);
    expect(getTags('stA', 'u1')).toEqual(['DEIS']);
    expect(toggleTag('stA', 'u1', 'DEIS')).toEqual([]);
    expect(getTags('stA', 'u1')).toEqual([]);
  });

  it('keeps multiple tags and scopes per student + school', () => {
    toggleTag('stA', 'u1', 'DEIS');
    toggleTag('stA', 'u1', 'Priority');
    expect(getTags('stA', 'u1').sort()).toEqual(['DEIS', 'Priority']);
    expect(getTags('stA', 'u2')).toEqual([]);
    expect(getTags('stB', 'u1')).toEqual([]);
  });
});
