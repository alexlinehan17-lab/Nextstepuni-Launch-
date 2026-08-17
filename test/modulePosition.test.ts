/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { describe, expect, test } from 'vitest';

import { resolveModulePosition } from '@/contexts/ModulePositionContext';
import { ALL_COURSES } from '@/courseData';
import { filterCoursesForStudent } from '@/utils/courseVisibility';

const visibleModules = [
  { id: 'mind-1', category: 'mind' },
  { id: 'exam-1', category: 'exam' },
  { id: 'exam-2', category: 'exam' },
  { id: 'exam-3', category: 'exam' },
  { id: 'mind-2', category: 'mind' },
];

describe('module display position', () => {
  test('uses the module order within its visible category', () => {
    expect(resolveModulePosition(visibleModules, 'exam-3')).toEqual({
      displayNumber: '03',
      position: 3,
      total: 3,
    });
  });

  test('recalculates after modules are filtered from the student view', () => {
    const filtered = visibleModules.filter(module => module.id !== 'exam-2');

    expect(resolveModulePosition(filtered, 'exam-3')).toEqual({
      displayNumber: '02',
      position: 2,
      total: 2,
    });
  });

  test('returns no position for a module outside the visible catalogue', () => {
    expect(resolveModulePosition(visibleModules, 'missing')).toBeNull();
  });

  test('matches the production Arena order for Exam Hall Strategies', () => {
    expect(resolveModulePosition(ALL_COURSES, 'exam-hall-strategies-protocol')).toMatchObject({
      displayNumber: '03',
      position: 3,
    });
  });

  test('matches the Junior Cycle Arena after senior-only modules are removed', () => {
    const juniorModules = filterCoursesForStudent(ALL_COURSES, 'junior', null);

    expect(juniorModules.some(module => module.id === 'leaving-cert-strategy-protocol')).toBe(false);
    expect(resolveModulePosition(juniorModules, 'exam-hall-strategies-protocol')).toMatchObject({
      displayNumber: '02',
      position: 2,
    });
  });

  test('numbers subject modules from the student-selected subject list', () => {
    const businessStudentModules = filterCoursesForStudent(ALL_COURSES, 'senior', {
      subjects: [{ subjectName: 'Business', level: 'higher' }],
      examStartDate: '2027-06-09',
      restDays: ['Sunday'],
      createdAt: '2026-08-13',
      updatedAt: '2026-08-13',
    });

    expect(resolveModulePosition(businessStudentModules, 'subject-business-protocol')).toMatchObject({
      displayNumber: '01',
      position: 1,
      total: 1,
    });
    expect(resolveModulePosition(businessStudentModules, 'subject-physics-protocol')).toBeNull();
  });
});
