import { describe, expect, test } from 'vitest';
import { ALL_COURSES } from '@/courseData';
import { LEARNING_PATHS } from '@/learningPaths';
import { availableLearningPaths, filterCoursesForStudent, moduleAvailability } from '@/utils/courseVisibility';
import type { StudentSubjectProfile } from '@/components/subjectData';

const profile = (names: string[]): StudentSubjectProfile => ({ subjects: names.map(subjectName => ({ subjectName, level: 'higher' })), examStartDate: '2027-06-09', restDays: [], createdAt: '', updatedAt: '' });
describe('the student module catalogue', () => {
  test('shows relevant general strategies alongside each selected subject guide', () => {
    const courses = filterCoursesForStudent(ALL_COURSES, 'senior', profile(['English', 'Mathematics', 'Biology']));
    expect(courses.map(c => c.id)).toEqual(expect.arrayContaining(['mastering-english-protocol', 'learning-math-protocol', 'mastering-the-sciences-protocol', 'subject-english-protocol', 'subject-biology-protocol']));
    expect(courses.some(c => c.id === 'mastering-business-protocol')).toBe(false);
    expect(courses.some(c => c.id === 'subject-french-protocol')).toBe(false);
  });
  test('resolves canonical aliases instead of depending on display names', () => {
    const courses = filterCoursesForStudent(ALL_COURSES, 'senior', profile(['Applied Mathematics', 'Design and Communication Graphics']));
    expect(courses.map(c => c.id)).toEqual(expect.arrayContaining(['subject-applied-maths-protocol', 'subject-dcg-protocol', 'learning-math-protocol', 'applied-sciences-protocol']));
  });
  test('never includes an unavailable or coming-soon lesson in a Junior Cycle path', () => {
    const courses = filterCoursesForStudent(ALL_COURSES, 'junior', null);
    expect(moduleAvailability(ALL_COURSES.find(c => c.id === 'subject-english-protocol'), 'junior', null)).toBe('coming-soon');
    const paths = availableLearningPaths(LEARNING_PATHS, courses, 'junior');
    expect(paths.length).toBeGreaterThan(0);
    for (const path of paths) for (const id of path.moduleIds) {
      expect(moduleAvailability(courses.find(c => c.id === id), 'junior', null)).toBe('available');
    }
    expect(paths.find(p => p.id === 'exam-prep-sprint')?.moduleIds).not.toContain('points-optimization-protocol');
    expect(paths.find(p => p.id === 'master-your-learning')?.moduleIds).not.toContain('mental-modelling-protocol');
  });
});
