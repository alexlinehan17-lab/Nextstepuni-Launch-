/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The write→read contract between the student tools and the GC dashboard.
 *
 * This is the test that would have caught the 2026-07 data-accuracy incident.
 * The GC loader is the ONLY consumer of these Firestore fields outside the tool
 * that owns them, so when a refactor moved mock results to a top-level array and
 * Future Finder to a new namespace, nothing failed — the dashboard just quietly
 * read fields nobody wrote any more and rendered the absence as zero.
 *
 * Rule for anyone adding a field to `mapProgressDocToStudent`: add a case here
 * that feeds in a document shaped exactly the way the WRITING tool shapes it.
 */
import { describe, it, expect } from 'vitest';
import { mapProgressDocToStudent } from '../components/GCDashboard';
import { type SessionUser } from '../utils/authUtils';

const USER: SessionUser = { uid: 'u1', name: 'Aoife', avatar: 'seed', role: 'student', school: 'stmarys' };

describe('GC loader contract — mock results', () => {
  it('reads the top-level `mockResults` array that hooks/useMockResults actually writes', () => {
    // Exactly the shape of types.ts UnifiedMockResult.
    const doc = {
      mockResults: [{
        id: 'm1',
        label: 'Christmas Mocks',
        date: '2026-02-10',
        entries: [
          { subjectName: 'Mathematics', grade: 'H3', level: 'higher' },
          { subjectName: 'English', grade: 'H2', level: 'higher' },
        ],
        totalPoints: 300,
        timestamp: 1770000000000,
      }],
    };
    const s = mapProgressDocToStudent(USER, doc);
    expect(s.mockResults).toHaveLength(2);
    // Flattened to one row per subject, with subject/grade populated —
    // GCStudentDetail, SubjectHealthPanel and both exporters rely on this shape.
    expect(s.mockResults![0]).toMatchObject({ subject: 'Mathematics', grade: 'H3', date: '2026-02-10' });
    expect(s.mockResults![1]).toMatchObject({ subject: 'English', grade: 'H2' });
  });

  it('falls back to the legacy warRoom blob for students dormant since the refactor', () => {
    const doc = { warRoom: { mockResults: [{ id: 'x', subject: 'Biology', grade: 'H4', date: '2025-11-01', timestamp: 1 }] } };
    const s = mapProgressDocToStudent(USER, doc);
    expect(s.mockResults).toHaveLength(1);
    expect(s.mockResults![0].subject).toBe('Biology');
  });

  it('prefers the current field when a doc holds both', () => {
    const doc = {
      mockResults: [{ id: 'm1', label: 'New', date: '2026-02-10', entries: [{ subjectName: 'Physics', grade: 'H1', level: 'higher' }], totalPoints: 100, timestamp: 2 }],
      warRoom: { mockResults: [{ id: 'x', subject: 'Biology', grade: 'H4', date: '2025-11-01', timestamp: 1 }] },
    };
    expect(mapProgressDocToStudent(USER, doc).mockResults![0].subject).toBe('Physics');
  });

  it('is null, not an empty table, when the student has logged no mocks', () => {
    expect(mapProgressDocToStudent(USER, {}).mockResults).toBeNull();
  });

  it('falls through to the legacy blob when every migrated record has empty entries', () => {
    // The forward-migration maps `entries: m.grades || []`, but legacy records
    // have no `grades` key — so a migrated doc can hold a NON-EMPTY mockResults
    // array whose every record has `entries: []`. Testing the raw array length
    // would let that shadow the still-intact legacy blob and hide real grades.
    const doc = {
      mockResults: [{ id: 'x', label: 'Mock Exam', date: '2025-11-01', entries: [], totalPoints: 0, timestamp: 1 }],
      warRoom: { mockResults: [{ id: 'x', subject: 'Biology', grade: 'H3', date: '2025-11-01', timestamp: 1 }] },
    };
    const s = mapProgressDocToStudent(USER, doc);
    expect(s.mockResults).toHaveLength(1);
    expect(s.mockResults![0]).toMatchObject({ subject: 'Biology', grade: 'H3' });
  });
});

describe('GC loader contract — Future Finder', () => {
  it('reads futureFinderRevamped.picks — the namespace the LIVE senior tool writes', () => {
    const s = mapProgressDocToStudent(USER, {
      futureFinderRevamped: { picks: ['DN150', 'CK101'], completedAt: '2026-07-01T10:00:00Z' },
    });
    expect(s.futureFinder?.topPicks).toEqual(['DN150', 'CK101']);
    // Saved picks are save-order, not a ranking — the render layer must not
    // number them 1/2/3.
    expect(s.futureFinder?.source).toBe('saved');
  });

  it('falls back to the persisted ranking when the student bookmarked nothing', () => {
    const s = mapProgressDocToStudent(USER, {
      futureFinderRevamped: { picks: [], topMatches: ['TR004', 'DN101'], updatedAt: '2026-07-02T10:00:00Z' },
    });
    expect(s.futureFinder?.topPicks).toEqual(['TR004', 'DN101']);
    expect(s.futureFinder?.source).toBe('ranked');
  });

  it('still reads the legacy namespace for students who only used the old tool', () => {
    const s = mapProgressDocToStudent(USER, { futureFinder: { topPicks: ['GY101'], completedAt: '2025-12-01' } });
    expect(s.futureFinder?.topPicks).toEqual(['GY101']);
    expect(s.futureFinder?.source).toBe('legacy');
  });

  it('prefers the live namespace over a stale legacy list', () => {
    const s = mapProgressDocToStudent(USER, {
      futureFinder: { topPicks: ['GY101'] },
      futureFinderRevamped: { picks: ['DN150'] },
    });
    expect(s.futureFinder?.topPicks).toEqual(['DN150']);
  });

  it('treats an empty topPicks array as no result (it is truthy in JS)', () => {
    // The JC Subject Explorer writes `topPicks: []`; `[]` being truthy used to
    // open an empty "Insights" section with nothing inside it.
    expect(mapProgressDocToStudent(USER, { futureFinder: { topPicks: [] } }).futureFinder).toBeNull();
  });
});

describe('GC loader contract — points', () => {
  it('reads the real pointsData map', () => {
    const s = mapProgressDocToStudent(USER, { pointsData: { totalEarned: 190, totalSpent: 20 } });
    expect(s.points?.totalEarned).toBe(190);
  });

  it('is not fooled by the phantom dotted root field', () => {
    // Locks the known-bad shape a `setDoc({'pointsData.totalEarned': ...})`
    // produces: one literal root key, not a nested path. Docs written before
    // the fix still carry it; the loader must not treat it as the real total.
    const s = mapProgressDocToStudent(USER, {
      'pointsData.totalEarned': 45,
      pointsData: { totalEarned: 10, totalSpent: 0 },
    });
    expect(s.points?.totalEarned).toBe(10);
  });
});

describe('GC loader contract — streak is derived, never trusted from the snapshot', () => {
  const dayKey = (daysAgo: number) => {
    const d = new Date();
    d.setDate(d.getDate() - daysAgo);
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  };

  it('ignores a stale stored streak for a student who stopped studying', () => {
    // The snapshot only ever updates when the student toggles a block, so a
    // student who walked away a fortnight ago kept showing a live 12-day run.
    const s = mapProgressDocToStudent(USER, {
      timetableStreak: { currentStreak: 12, longestStreak: 12, lastActiveDate: dayKey(14) },
      timetableCompletions: { [dayKey(14)]: ['b1'] },
      subjectProfile: { subjects: [], restDays: [], examStartDate: null, createdAt: '', updatedAt: '' },
    });
    expect(s.streak?.currentStreak).toBe(0);
    // longestStreak is preserved so the "had a 7+ run" alert gate still works.
    expect(s.streak?.longestStreak).toBe(12);
  });

  it('reports lastActiveDate from the completions map, never as today', () => {
    // computeStreak returns TODAY when the streak is 0. Wiring that through
    // would mark every dormant student "active today" and silently disable the
    // at-risk and streak-broken alerts.
    const s = mapProgressDocToStudent(USER, {
      timetableCompletions: { [dayKey(20)]: ['b1'] },
      subjectProfile: { subjects: [], restDays: [], examStartDate: null, createdAt: '', updatedAt: '' },
    });
    expect(s.streak?.lastActiveDate).toBe(dayKey(20));
  });

  it('ignores day-keys left behind with an empty array', () => {
    const s = mapProgressDocToStudent(USER, {
      timetableCompletions: { [dayKey(3)]: ['b1'], [dayKey(1)]: [] },
      subjectProfile: { subjects: [], restDays: [], examStartDate: null, createdAt: '', updatedAt: '' },
    });
    expect(s.streak?.lastActiveDate).toBe(dayKey(3));
  });
});

describe('GC loader contract — module progress', () => {
  it('keeps only entries shaped like module progress', () => {
    const s = mapProgressDocToStudent(USER, {
      'mastering-active-recall': { unlockedSection: 4 },
      subjectProfile: { subjects: [], restDays: [], examStartDate: null, createdAt: '', updatedAt: '' },
      pointsData: { totalEarned: 5, totalSpent: 0 },
    });
    expect(Object.keys(s.progress)).toEqual(['mastering-active-recall']);
  });

  it('handles a student with no progress document at all', () => {
    const s = mapProgressDocToStudent(USER, null);
    expect(s.progress).toEqual({});
    expect(s.subjectProfile).toBeNull();
    expect(s.futureFinder).toBeNull();
    expect(s.mockResults).toBeNull();
    // No document means no derivation — not a confident zero-streak.
    expect(s.streak).toBeNull();
  });
});
