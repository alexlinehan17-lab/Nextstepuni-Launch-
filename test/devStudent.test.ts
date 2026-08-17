/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import { ALL_COURSES } from '@/courseData';
import { computeStreak } from '@/components/timetableAlgorithm';
import {
  DEMO_STUDENT_UID,
  createDemoStudentLoadedData,
  createDemoStudentNorthStar,
  createDemoStudentProfile,
  createDemoStudentSession,
} from '@/data/devStudent';
import { filterCoursesForStudent } from '@/utils/courseVisibility';

const FIXED_NOW = new Date('2026-08-09T12:00:00.000Z');

describe('localhost Demo Account', () => {
  test('creates a complete senior-cycle session', () => {
    expect(createDemoStudentSession()).toMatchObject({
      uid: DEMO_STUDENT_UID,
      name: 'Demo Student',
      role: 'student',
      yearGroup: '6th',
      curriculumLevel: 'senior',
    });
  });

  test('starts with the seven configured subjects used for local UI work', () => {
    const profile = createDemoStudentProfile(FIXED_NOW);
    expect(profile.examStartDate).toBe('2027-06-09');
    expect(profile.subjects.map(subject => subject.subjectName)).toEqual([
      'Politics & Society',
      'Geography',
      'Mathematics',
      'Applied Maths',
      'English',
      'Irish',
      'Accounting',
    ]);
    expect(new Set(profile.subjects.map(subject => subject.currentGrade)).size).toBeGreaterThan(1);
    expect(profile.subjects.every(subject => subject.level === 'higher')).toBe(true);
  });

  test('hydrates the demo account with a North Star and bypasses onboarding', () => {
    const northStar = createDemoStudentNorthStar(FIXED_NOW);
    const loaded = createDemoStudentLoadedData(FIXED_NOW);

    expect(northStar.category).toBe('options-freedom');
    expect(northStar.visionBoard).toEqual(['real-choices', 'see-world', 'freedom-no']);
    expect(loaded.needsOnboarding).toBe(false);
    expect(loaded.studentProfile.subjects).toHaveLength(7);
    expect(loaded.northStar).toEqual(northStar);
    expect(loaded.rawProgressDoc).toMatchObject({
      subjectProfile: loaded.studentProfile,
      northStar,
    });
  });

  test('seeds every dashboard data source with a substantial, varied history', () => {
    const loaded = createDemoStudentLoadedData(FIXED_NOW);
    const sessions = loaded.rawProgressDoc.studySessions ?? [];
    const confidenceLabels = new Set(sessions.map(session => session.confidenceLabel));
    const techniques = new Set(sessions.flatMap(session => session.strategiesShown ?? []));

    expect(sessions.length).toBeGreaterThanOrEqual(60);
    expect(sessions.filter(session => session.date === '2026-08-09')).toHaveLength(3);
    expect(new Set(sessions.map(session => session.subject)).size).toBe(7);
    expect(confidenceLabels).toEqual(new Set(['lost', 'shaky', 'okay', 'good', 'confident']));
    expect(techniques.size).toBeGreaterThanOrEqual(7);
    expect(loaded.rawProgressDoc.reflections?.length).toBeGreaterThan(25);
    expect(loaded.rawProgressDoc.studyDebriefs?.length).toBeGreaterThan(5);
    expect(Object.keys(loaded.rawProgressDoc.topicMasteryV2?.topics ?? {}).length).toBeGreaterThan(40);
    expect(loaded.rawProgressDoc.unifiedMockResults).toHaveLength(9);
    expect(loaded.rawProgressDoc.pointsData).toEqual({ totalEarned: 6_240, totalSpent: 1_175 });
    expect(loaded.rawProgressDoc.gamification?.unlockedAchievements?.length).toBeGreaterThan(25);
    expect(loaded.rawProgressDoc.gamification?.unlockedAchievements).not.toContain('jc-first-step');
    expect(Object.keys(loaded.timetableCompletions).length).toBeGreaterThan(50);
    expect(computeStreak(loaded.timetableCompletions, ['Sunday'], FIXED_NOW).currentStreak).toBe(18);
  });

  test('paints all five programme mountains with completed and in-progress modules', () => {
    const loaded = createDemoStudentLoadedData(FIXED_NOW);
    const visibleCourses = filterCoursesForStudent(ALL_COURSES, 'senior', loaded.studentProfile);
    const categories = [...new Set(visibleCourses.map(course => course.category))];

    expect(categories).toHaveLength(5);
    for (const category of categories) {
      const courses = visibleCourses.filter(course => course.category === category);
      const completed = courses.filter(course => (
        (loaded.userProgress[course.id]?.unlockedSection ?? 0) >= course.sectionsCount
      ));
      const inProgress = courses.filter(course => {
        const unlocked = loaded.userProgress[course.id]?.unlockedSection ?? 0;
        return unlocked > 0 && unlocked < course.sectionsCount;
      });
      expect(completed.length, `${category} should have completed modules`).toBeGreaterThan(0);
      expect(inProgress.length, `${category} should have an active module`).toBeGreaterThan(0);
    }
  });

  test('replaces the old development skip affordance with the Demo Account control', () => {
    const loginPage = readFileSync(resolve(__dirname, '../components/LoginPage.tsx'), 'utf8');
    expect(loginPage).toContain('Demo Account');
    expect(loginPage).not.toContain('DEV: Skip Login');
  });

  test('passes the shared subject profile into Launchpad instead of requiring a second successful read', () => {
    const router = readFileSync(resolve(__dirname, '../components/AppRouter.tsx'), 'utf8');
    const launchpadCall = /<InnovationZone[\s\S]*?\/>/.exec(router)?.[0];
    expect(launchpadCall, 'InnovationZone call site not found').toBeTruthy();
    expect(launchpadCall).toContain('initialSubjectProfile={studentProfile}');
  });
});
