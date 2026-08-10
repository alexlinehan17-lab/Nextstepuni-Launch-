/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

import {
  DEV_STUDENT_UID,
  createDevStudentLoadedData,
  createDevStudentNorthStar,
  createDevStudentProfile,
  createDevStudentSession,
} from '@/data/devStudent';

const FIXED_NOW = new Date('2026-08-09T12:00:00.000Z');

describe('DEV: Skip Login student', () => {
  test('creates a complete senior-cycle session', () => {
    expect(createDevStudentSession()).toMatchObject({
      uid: DEV_STUDENT_UID,
      role: 'student',
      yearGroup: '6th',
      curriculumLevel: 'senior',
    });
  });

  test('starts with the seven configured subjects used for local UI work', () => {
    const profile = createDevStudentProfile(FIXED_NOW);
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
    expect(profile.subjects.every(subject => subject.currentGrade === 'H4' && subject.targetGrade === 'H2')).toBe(true);
  });

  test('hydrates the dev account with a North Star and bypasses onboarding', () => {
    const northStar = createDevStudentNorthStar(FIXED_NOW);
    const loaded = createDevStudentLoadedData(FIXED_NOW);

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

  test('passes the shared subject profile into Launchpad instead of requiring a second successful read', () => {
    const router = readFileSync(resolve(__dirname, '../components/AppRouter.tsx'), 'utf8');
    const launchpadCall = /<InnovationZone[\s\S]*?\/>/.exec(router)?.[0];
    expect(launchpadCall, 'InnovationZone call site not found').toBeTruthy();
    expect(launchpadCall).toContain('initialSubjectProfile={studentProfile}');
  });
});
