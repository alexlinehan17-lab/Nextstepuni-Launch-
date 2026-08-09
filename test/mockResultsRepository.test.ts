import { describe, expect, it } from 'vitest';
import { mockResultsStoragePatch, reconcileMockResults } from '../services/mockResultsRepository';

describe('mock results academic record', () => {
  it('unifies Points Passport, War Room and canonical history without losing a result', () => {
    const results = reconcileMockResults({
      unifiedMockResults: [{ id: 'canonical', label: 'Pre-LC', date: '2026-02-01', entries: [{ subjectName: 'English', grade: 'H2', level: 'higher' }], totalPoints: 88, timestamp: 3 }],
      mockResults: [{ id: 'canonical', label: 'Pre-LC', date: '2026-02-01', entries: [{ subjectName: 'English', grade: 'H2', level: 'higher' }], totalPoints: 88, timestamp: 3 }],
      pointsPassport: { mockResults: [{ id: 'passport', label: 'Christmas', date: '2025-12-12', grades: [{ subjectName: 'Irish', grade: 'H3', level: 'higher' }], totalPoints: 77, timestamp: 2 }] },
      warRoom: { mockResults: [{ id: 'war', subject: 'Mathematics', grade: 'H1', level: 'higher', date: '2025-11-01', timestamp: 1 }] },
    });

    expect(results.map(result => result.id)).toEqual(['canonical', 'passport', 'war']);
    expect(results[2].entries).toEqual([{ subjectName: 'Mathematics', grade: 'H1', level: 'higher' }]);
  });

  it('writes the canonical field and compatibility mirror identically', () => {
    const results = reconcileMockResults({ mockResults: [{ id: 'one', label: 'Mock', date: '2026-01-01', entries: [], totalPoints: 0, timestamp: 1 }] });
    const patch = mockResultsStoragePatch(results);
    expect(patch.unifiedMockResults).toBe(patch.mockResults);
  });

  it('unions subjects when transitional copies of one sitting diverge', () => {
    const results = reconcileMockResults({
      unifiedMockResults: [{ id: 'same', label: 'Mocks', date: '2026-02-01', entries: [{ subjectName: 'English', grade: 'H2', level: 'higher' }], totalPoints: 88, timestamp: 2 }],
      mockResults: [{ id: 'same', label: 'Mocks', date: '2026-02-01', entries: [{ subjectName: 'Irish', grade: 'H3', level: 'higher' }], totalPoints: 77, timestamp: 2 }],
    });
    expect(results).toHaveLength(1);
    expect(results[0].entries.map(entry => entry.subjectName)).toEqual(['English', 'Irish']);
  });
});
