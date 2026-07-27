/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * The student's home screen and the guidance counsellor's dashboard must show
 * the SAME streak for the same student. They didn't: the student recomputed
 * live from the completions map while the GC rendered a stored snapshot that is
 * only ever written by one of the two completion paths — so a student who used
 * "Study Now" had a real 9-day streak and a GC-visible 0, and a student who
 * stopped a fortnight ago still showed 12 to their counsellor.
 */
import { describe, it, expect } from 'vitest';
import { computeStreak } from '../components/timetableAlgorithm';
import { mapProgressDocToStudent } from '../components/GCDashboard';
import { lastActiveDateFrom } from '../utils/weekDates';
import { getStudentStatus } from '../utils/studentStatus';
import { type GCStudentFullData } from '../components/gc/gcTypes';
import { type SessionUser } from '../utils/authUtils';

const USER: SessionUser = { uid: 'u1', name: 'Cian', avatar: 'a' };

const key = (daysAgo: number) => {
  const d = new Date();
  d.setDate(d.getDate() - daysAgo);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
};

const emptyProfile = { subjects: [], restDays: [] as string[], examStartDate: null, createdAt: '2025-01-01', updatedAt: '2025-01-01' };

describe('streak parity — student vs GC', () => {
  it('gives the GC the same number ProgressContext gives the student', () => {
    const completions = { [key(2)]: ['b1'], [key(1)]: ['b2'], [key(0)]: ['b3'] };
    // What ProgressContext computes for the student's own screen:
    const studentSide = computeStreak(completions, []);
    // What the GC loader derives:
    const gcSide = mapProgressDocToStudent(USER, { timetableCompletions: completions, subjectProfile: emptyProfile });
    expect(gcSide.streak?.currentStreak).toBe(studentSide.currentStreak);
  });

  it('does not inherit a stale snapshot from the timetable toggle', () => {
    const completions = { [key(20)]: ['b1'] };
    const gcSide = mapProgressDocToStudent(USER, {
      timetableCompletions: completions,
      timetableStreak: { currentStreak: 9, longestStreak: 9, lastActiveDate: key(20) },
      subjectProfile: emptyProfile,
    });
    expect(gcSide.streak?.currentStreak).toBe(0);
  });

  it('picks up a streak built entirely through "Study Now" (which never writes the snapshot)', () => {
    const completions = { [key(2)]: ['b1'], [key(1)]: ['b2'], [key(0)]: ['b3'] };
    // No timetableStreak field at all — this is the Study-Now-only student.
    const gcSide = mapProgressDocToStudent(USER, { timetableCompletions: completions, subjectProfile: emptyProfile });
    expect(gcSide.streak?.currentStreak).toBeGreaterThan(0);
  });

  it('honours a purchased rest-day pass, like the student\'s own timetable card', () => {
    // Studied Mon+Tue, bought a rest-day pass for the gap day, studied Thu+Fri.
    // computeStreak treats a passed day as a continuation — dropping the 4th
    // argument would show the GC a shorter streak than the student sees, and
    // could push a student who PAID to protect their streak into 'drifting'.
    const completions = { [key(4)]: ['b1'], [key(3)]: ['b2'], [key(1)]: ['b3'], [key(0)]: ['b4'] };
    const gap = key(2);

    const withoutPass = mapProgressDocToStudent(USER, {
      timetableCompletions: completions, subjectProfile: emptyProfile,
    });
    const withPass = mapProgressDocToStudent(USER, {
      timetableCompletions: completions, subjectProfile: emptyProfile,
      earnedRest: { restDayPasses: [gap] },
    });

    expect(withPass.streak!.currentStreak).toBeGreaterThan(withoutPass.streak!.currentStreak);
    // ...and it matches what the student's own screen computes.
    expect(withPass.streak!.currentStreak).toBe(computeStreak(completions, [], new Date(), [gap]).currentStreak);
  });

  it('never reports a zero-activity student as active today', () => {
    // computeStreak returns today's key when the streak is 0 — the trap that
    // would silently disable every at-risk alert.
    expect(computeStreak({}, []).lastActiveDate).toBeTruthy();      // documents the trap
    expect(lastActiveDateFrom({})).toBeNull();                      // what we use instead
    const gcSide = mapProgressDocToStudent(USER, { timetableCompletions: {}, subjectProfile: emptyProfile });
    expect(gcSide.streak?.lastActiveDate).toBe('');
  });
});

describe('student status classification', () => {
  const base = (extra: Partial<GCStudentFullData>): GCStudentFullData => ({
    user: USER, progress: {}, subjectProfile: null, northStar: null, journeyResult: null,
    streak: null, points: null, timetableCompletions: null, futureFinder: null,
    mockResults: null, recentDebriefs: null, collegeCompass: null, ...extra,
  });

  it('does not pin a long-dormant, profile-less student at "new" forever', () => {
    // Skipping onboarding writes nothing to Firestore, so these students have
    // no createdAt anywhere and used to return 'new' unconditionally — they
    // could never surface as inactive no matter how long they were gone.
    const s = base({ user: { ...USER, createdAt: '2025-01-01T00:00:00Z' } });
    expect(getStudentStatus(s, [])).not.toBe('new');
  });

  it('still reports a genuinely new account as new', () => {
    const s = base({ user: { ...USER, createdAt: new Date().toISOString() } });
    expect(getStudentStatus(s, [])).toBe('new');
  });

  it('reaches at-risk for a student with a broken long streak', () => {
    const s = base({
      user: { ...USER, createdAt: '2025-01-01T00:00:00Z' },
      timetableCompletions: { [key(16)]: ['b1'] },
      streak: { currentStreak: 0, longestStreak: 12, lastActiveDate: key(16) },
    });
    expect(getStudentStatus(s, [])).toBe('at-risk');
  });
});
