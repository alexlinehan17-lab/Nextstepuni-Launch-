/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

/**
 * Which modules a given student can actually see.
 *
 * This was inlined in App.tsx's `studentCourses` useMemo, which made it the
 * student app's private knowledge — so the GC dashboard scored every student
 * against the full 83-module catalogue while the student's own counter used
 * their (much shorter) visible list. A 7-subject senior who had completed
 * everything they could open read as ~73% to their guidance counsellor.
 *
 * Cards, paths, search and direct links share this boundary. A visible preview
 * tile is distinct from an available lesson, so unfinished Junior Cycle guides
 * cannot leak their Leaving Certificate content through a different route.
 */

import { type CourseData } from '../components/Library';
import { SUBJECT_TO_MODULE } from '../courseData';
import { type StudentSubjectProfile } from '../components/subjectData';
import { type CurriculumLevel } from './authUtils';
import { resolveSubjectId } from '../curriculumRegistry';
import type { LearningPath } from '../learningPaths';

// These are lesson audiences, not a second curriculum taxonomy. All subject
// names/aliases are resolved by the canonical registry before matching them.
const STRATEGY_AUDIENCES: Record<string, string[]> = {
  'learning-math-protocol': ['mathematics', 'applied-mathematics'],
  'mastering-foreign-languages-protocol': ['irish', 'french', 'german', 'spanish', 'italian', 'japanese', 'russian', 'arabic', 'mandarin-chinese', 'portuguese', 'polish', 'lithuanian'],
  'mastering-the-sciences-protocol': ['biology', 'chemistry', 'physics', 'agricultural-science'],
  'applied-sciences-protocol': ['engineering', 'design-and-communication-graphics', 'computer-science', 'construction-studies', 'technology'],
  'mastering-english-protocol': ['english'],
  'mastering-business-protocol': ['business', 'accounting', 'economics'],
  'mastering-the-creatives-protocol': ['art', 'music', 'drama-film-and-theatre-studies'],
  'mastering-the-humanities-protocol': ['history', 'geography', 'politics-and-society', 'religious-education', 'classical-studies'],
};

export type ModuleAvailability = 'available' | 'coming-soon' | 'unavailable';

export function moduleAvailability(
  course: CourseData | undefined,
  curriculumLevel: CurriculumLevel | undefined,
  studentProfile: StudentSubjectProfile | null | undefined,
): ModuleAvailability {
  if (!course) return 'unavailable';
  const level = curriculumLevel ?? studentProfile?.curriculumLevel ?? 'senior';
  if (course.curriculum && course.curriculum !== 'both' && course.curriculum !== level) return 'unavailable';
  if (!course.curriculum && level !== 'senior') return 'unavailable';
  if (course.category === 'subject-specific-science' && studentProfile?.subjects.length) {
    const subjects = new Set(studentProfile.subjects.map(subject => resolveSubjectId(subject.subjectName)));
    const moduleIds = new Set(Object.entries(SUBJECT_TO_MODULE)
      .filter(([name]) => subjects.has(resolveSubjectId(name)))
      .map(([, id]) => id));
    if (course.id.startsWith('subject-') && !moduleIds.has(course.id)) return 'unavailable';
    const audience = STRATEGY_AUDIENCES[course.id];
    if (audience && !audience.some(subject => subjects.has(subject))) return 'unavailable';
  }
  return level === 'junior' && course.jcStatus === 'coming-soon' ? 'coming-soon' : 'available';
}

export function availableLearningPaths(paths: LearningPath[], courses: CourseData[], level?: CurriculumLevel): LearningPath[] {
  const available = new Set(courses.filter(course => moduleAvailability(course, level, null) === 'available').map(course => course.id));
  return paths.map(path => ({ ...path, moduleIds: path.moduleIds.filter(id => available.has(id)) }))
    .filter(path => path.moduleIds.length > 0);
}

export function filterCoursesForStudent(
  allCourses: CourseData[],
  curriculumLevel: CurriculumLevel | undefined,
  studentProfile: StudentSubjectProfile | null | undefined,
): CourseData[] {
  return allCourses.filter(course => moduleAvailability(course, curriculumLevel, studentProfile) !== 'unavailable');
}
