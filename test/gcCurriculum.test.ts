/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * Junior Cycle and LCA students have complete, valid subject profiles that
 * contain no H/O grade — bands and credits respectively. Treating "has a
 * profile" as "has CAO grades" ran them through the CAO path and printed a
 * confident 0 next to their name on the guidance-counsellor dashboard.
 */
import { describe, it, expect } from 'vitest';
import { hasCAOGrades, getStudentCurrentCAO, getStudentTargetCAO, getVisibleCourses, getOverallProgress } from '../components/gc/gcUtils';
import { type GCStudentFullData } from '../components/gc/gcTypes';
import { type StudentSubject, type StudentSubjectProfile } from '../components/subjectData';
import { ALL_COURSES } from '../courseData';

const profile = (subjects: StudentSubject[], extra: Partial<StudentSubjectProfile> = {}): StudentSubjectProfile => ({
  subjects, examStartDate: null, restDays: [], createdAt: '2026-01-01', updatedAt: '2026-01-01', ...extra,
});

const student = (p: StudentSubjectProfile | null, extra: Partial<GCStudentFullData> = {}): GCStudentFullData => ({
  user: { uid: 'u1', name: 'Test', avatar: 'a' },
  progress: {}, subjectProfile: p, northStar: null, journeyResult: null, streak: null,
  points: null, timetableCompletions: null, futureFinder: null, mockResults: null,
  recentDebriefs: null, collegeCompass: null, ...extra,
});

describe('hasCAOGrades', () => {
  it('is true for a Leaving Cert profile', () => {
    expect(hasCAOGrades(student(profile([
      { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    ])))).toBe(true);
  });

  it('is FALSE for a Junior Cycle band-only profile', () => {
    expect(hasCAOGrades(student(profile([
      { subjectName: 'Science', level: 'common', currentBand: 'Merit', targetBand: 'Higher Merit' },
    ], { curriculumLevel: 'junior', yearGroup: '2nd' })))).toBe(false);
  });

  it('is FALSE for an LCA level-only profile', () => {
    // The trap: LCA maps to curriculumLevel 'senior', so an isJunior check
    // alone lets these students fall straight through to the CAO path.
    expect(hasCAOGrades(student(profile([
      { subjectName: 'Mathematical Applications', level: 'common' },
      { subjectName: 'English and Communications', level: 'common' },
    ], { yearGroup: 'LCA1' })))).toBe(false);
  });

  it('is false when the student has no profile yet', () => {
    expect(hasCAOGrades(student(null))).toBe(false);
  });
});

describe('CAO points', () => {
  it('applies the Higher-Level Maths bonus', () => {
    const s = student(profile([
      { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H3', targetGrade: 'H1' },
    ]));
    // H3 = 77, +25 bonus (H3 is above the H6/46-point threshold).
    expect(getStudentCurrentCAO(s)).toBe(102);
    expect(getStudentTargetCAO(s)).toBe(125);
  });

  it('counts only the best six subjects', () => {
    const seven: StudentSubject[] = ['A', 'B', 'C', 'D', 'E', 'F', 'G'].map(n => ({
      subjectName: n, level: 'higher' as const, currentGrade: 'H1' as const, targetGrade: 'H1' as const,
    }));
    // 6 × 100, never 7.
    expect(getStudentCurrentCAO(student(profile(seven)))).toBe(600);
  });
});

describe('visible-course denominator', () => {
  it('scores a student against the modules they can open, not the full catalogue', () => {
    const s = student(profile([
      { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    ], { curriculumLevel: 'senior' }), { curriculumLevel: 'senior' });

    const visible = getVisibleCourses(s, ALL_COURSES);
    expect(visible.length).toBeGreaterThan(0);
    expect(visible.length).toBeLessThan(ALL_COURSES.length);

    // A student who finished every module available to them must read 100%,
    // not "100 completed out of the whole catalogue".
    const finished = student(profile([
      { subjectName: 'Mathematics', level: 'higher', currentGrade: 'H3', targetGrade: 'H2' },
    ], { curriculumLevel: 'senior' }), {
      curriculumLevel: 'senior',
      progress: Object.fromEntries(visible.map(c => [c.id, { unlockedSection: c.sectionsCount }])),
    });
    expect(getOverallProgress(finished.progress, getVisibleCourses(finished, ALL_COURSES))).toBe(100);
    // Against the whole catalogue the same student reads as materially less.
    expect(getOverallProgress(finished.progress, ALL_COURSES)).toBeLessThan(100);
  });

  it('never divides by zero for a student with no profile', () => {
    const s = student(null);
    expect(getOverallProgress(s.progress, getVisibleCourses(s, ALL_COURSES))).not.toBeNaN();
  });
});
